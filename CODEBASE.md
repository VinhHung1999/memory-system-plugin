# maniax — Codebase overview

A Claude Code plugin **marketplace** (catalog of plugins) hosted at `git@github.com:VinhHung1999/memory-system-plugin.git`. The marketplace name is `maniax`; it currently packages three plugins.

## Tech stack

| Layer | Tool | Where |
|---|---|---|
| Skill & rule authoring | Markdown | `plugins/*/skills/*/SKILL.md`, `.claude/rules/*.md` |
| Hooks | Bash + Python 3 (stdlib only) | `plugins/memory-system/hooks/` |
| Manifests & config | JSON | `.claude-plugin/*.json`, `hooks/hooks.json`, `settings.json` |
| Version scheme | SemVer, per-plugin | Each `plugin.json` + marketplace `metadata.version` |

No Node/npm, no Python venv, no build step. Ship-as-source.

## Directory map

```
maniax/
├── .claude-plugin/
│   └── marketplace.json           # catalog — lists all 3 plugins + versions + metadata
├── CLAUDE.md                      # project-level instructions for Claude (index to rules)
├── CODEBASE.md                    # this file
├── CHANGELOG.md                   # Keep-a-Changelog + SemVer
├── LICENSE                        # MIT
├── README.md                      # marketplace README (architecture + install)
├── .claude/
│   └── rules/                     # scoped rule files loaded on matching paths
│       ├── general.md
│       ├── marketplace.md
│       ├── hooks.md
│       └── skills.md
└── plugins/
    ├── memory-system/             # ⟶ the flagship plugin (hooks + skills + settings)
    │   ├── .claude-plugin/plugin.json
    │   ├── settings.json          # autoMemoryEnabled + pre-granted permissions for brain2
    │   ├── hooks/
    │   │   ├── hooks.json
    │   │   ├── inject.sh                  # SessionStart: wiki memory banner + context
    │   │   ├── prompt-reminder.sh         # UserPromptSubmit: tiny pointer
    │   │   ├── pre-commit-gate.sh         # PreToolUse Bash: nudge /knowledge-updater
    │   │   └── memory_store_reminder.py   # Stop: every-Nth reminder to store lessons
    │   └── skills/
    │       ├── coder-memory-recall/       # search brain2/wiki/code-knowledge
    │       ├── coder-memory-store/        # stage into brain2/raw/code-knowledge (inbox)
    │       ├── generate-rules/            # analyze repo → write .claude/rules/ + CODEBASE.md
    │       ├── init-memory/               # scaffold docs/memory/ + configure autoMemory
    │       ├── knowledge-updater/         # route recent diff to CLAUDE.md / rules / memory / skills
    │       └── reorganize/                # migrate flat memory to 2-level hierarchy
    ├── marketing-toolkit/         # ⟶ 8 self-contained skills
    │   ├── .claude-plugin/plugin.json
    │   └── skills/
    │       ├── ab-test-designer/          # + scripts/ab_significance.py, sample_size.py
    │       ├── ai-marketing-prompts/      # T-C-R-E-I prompt templates
    │       ├── email-campaign-builder/    # + templates/ for copy
    │       ├── email-metrics-analyzer/    # 9-metric benchmark vs industry
    │       ├── marketing-performance-dashboard/  # GA4 + Ads unified dashboard
    │       ├── seo-onpage-checklist/      # + scripts/seo_audit.py, evals/
    │       ├── social-listening-keywords-builder/
    │       └── social-media-content-calendar/
    └── learn-coursera/            # ⟶ single meta-skill
        ├── .claude-plugin/plugin.json
        └── skills/learn-coursera/SKILL.md
```

## Architecture

Three plugins with **no cross-dependencies** — each is independently installable. The only thing that knows about all three is `.claude-plugin/marketplace.json`.

```
┌────────────────────── Claude Code session ──────────────────────┐
│                                                                  │
│  SessionStart ─► inject.sh ──► banner + brain2 wiki context     │
│  UserPromptSubmit ─► prompt-reminder.sh ──► tiny recall hint    │
│  PreToolUse (Bash) ─► pre-commit-gate.sh ──► commit nudge       │
│  Stop ─► memory_store_reminder.py ──► every 6th turn reminder   │
│                                                                  │
│  Skills loaded on trigger:                                       │
│    /memory-system:*         (6 skills)                           │
│    (marketing skills load by description match)                  │
│    /learn-coursera                                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
             │                                │
             ▼                                ▼
   ~/.claude/knowledge_updater_state.json   ~/.claude/memory_store_hook_state.json
   (session→timestamp for sync gate)        (per-session turn counter)
             │
             ▼
   ~/Documents/Notes/HungVault/HungVault/brain2/
     ├── wiki/code-knowledge/       ← read-only (Hung's curated space)
     └── raw/code-knowledge/        ← inbox (stage skill writes here)
```

Data flow for the memory read path: `SessionStart` → `inject.sh` lists domain folders under `brain2/wiki/code-knowledge/` → emits `systemMessage` (banner) + `hookSpecificOutput.additionalContext` (the wiki pointer text). When Claude later hits a non-trivial task it invokes `coder-memory-recall`, which grep/qmd-searches the same folders.

Data flow for the memory write path: any skill/turn → `coder-memory-store` (background subagent) → writes a `.md` to `brain2/raw/code-knowledge/<domain>/<bugs|patterns>/` → Hung later promotes to `wiki/`.

## Key files

| File | Why it matters |
|---|---|
| `.claude-plugin/marketplace.json` | Source of truth for which plugins ship, their versions, categories. |
| `plugins/memory-system/hooks/hooks.json` | All hook registrations. Editing this changes what fires when. |
| `plugins/memory-system/hooks/inject.sh` | The heaviest hook — branches on `$HOOK_EVENT` because PostCompact has a stricter schema than SessionStart. Template for any future multi-event hook. |
| `plugins/memory-system/hooks/memory_store_reminder.py` | Only Python hook. Reference for stateful hooks (counter + cooldown + transcript grep). |
| `plugins/memory-system/settings.json` | Pre-granted permissions for subagent writes to brain2 — required so background skills don't hang on permission prompts. |
| `plugins/memory-system/skills/generate-rules/SKILL.md` | The skill that produced this very file. Self-hosting. |
| `CHANGELOG.md` | Marketplace-level history. Every behavior-changing edit should land here. |

## Development commands

- **Reload after editing hooks or skill descriptions**: `/reload-plugins` inside Claude Code. The hook count in the output doubles as a smoke test.
- **Install locally for testing**: `claude --plugin-dir ./plugins/memory-system` (or any single plugin folder).
- **Update the live catalog**: push to the GitHub remote, then users run `/plugin marketplace update maniax`.
- **No build, no test runner** — the validation loop is: edit → `/reload-plugins` → trigger the changed skill/hook → inspect output.

## Common gotchas

- Hook emits `additionalContext` on `PostCompact` → schema error. Only `systemMessage` is allowed there.
- Bumping `plugin.json` but forgetting `marketplace.json` → `/plugin` UI shows stale version.
- Writing to `brain2/wiki/` instead of `brain2/raw/` → breaks Hung's curated/inbox boundary.
- Missing brain2 vault on a user's machine → hooks must bail with `echo '{}'; exit 0`, not a failure.
