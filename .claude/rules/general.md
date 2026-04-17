# maniax — Plugin Marketplace

Claude Code plugin marketplace. Ships three plugins that are packaged and distributed together:

| Plugin | What | Version source |
|---|---|---|
| `memory-system` | Hooks + skills for the 4-tier knowledge system (rules / project memory / universal memory / pre-commit sync gate). | `plugins/memory-system/.claude-plugin/plugin.json` |
| `marketing-toolkit` | 8 marketing skills (SEO audit, email campaign + metrics, social calendar + listening, A/B test, AI prompts, GA4+Ads dashboard). | `plugins/marketing-toolkit/.claude-plugin/plugin.json` |
| `learn-coursera` | Meta-skill that turns Coursera courses into Claude Code skills (discover → transcript → enrich → build). | `plugins/learn-coursera/.claude-plugin/plugin.json` |

## Tech stack

- **Markdown** — every skill, rule, README, and CHANGELOG.
- **Bash** — shell hooks (`inject.sh`, `pre-commit-gate.sh`, `prompt-reminder.sh`).
- **Python 3** — `memory_store_reminder.py` and helper scripts inside skills (e.g. `marketing-toolkit/skills/*/scripts/*.py`). Plain stdlib — no third-party deps bundled.
- **JSON** — every manifest (`.claude-plugin/marketplace.json`, `plugin.json`, `hooks/hooks.json`, plugin `settings.json`).

Hooks stream JSON on stdin and stdout, so Python and Bash both lean on `python3 -c 'import json,sys; …'` for parsing/escaping — keep that pattern instead of pulling in `jq`.

## Repo layout

```
maniax/
├── .claude-plugin/marketplace.json   # catalog: lists all 3 plugins, their source paths, versions
├── CHANGELOG.md                      # marketplace-level changelog (Keep a Changelog + SemVer)
├── README.md                         # marketplace README
├── LICENSE                           # MIT
└── plugins/
    ├── memory-system/
    │   ├── .claude-plugin/plugin.json
    │   ├── settings.json             # autoMemoryEnabled + pre-granted permissions
    │   ├── hooks/
    │   │   ├── hooks.json            # hook registration
    │   │   ├── inject.sh             # SessionStart: inject wiki memory index
    │   │   ├── prompt-reminder.sh    # UserPromptSubmit: tiny pointer
    │   │   ├── pre-commit-gate.sh    # PreToolUse Bash: nudge /knowledge-updater
    │   │   └── memory_store_reminder.py  # Stop: periodic reminder
    │   └── skills/
    │       ├── coder-memory-recall/
    │       ├── coder-memory-store/
    │       ├── generate-rules/
    │       ├── init-memory/
    │       ├── knowledge-updater/
    │       └── reorganize/
    ├── marketing-toolkit/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/<8 skills>/        # each has SKILL.md + references/ + optional scripts/, templates/, evals/
    └── learn-coursera/
        ├── .claude-plugin/plugin.json
        └── skills/learn-coursera/SKILL.md
```

The three plugins are independent — never cross-reference files between plugin directories. The marketplace manifest is the only thing that knows about all three.

## Versioning & CHANGELOG

- **SemVer** per plugin; the marketplace itself (`marketplace.json` → `metadata.version`) also uses SemVer.
- Bump the relevant `plugin.json` version **any time** you change a hook's behavior, a hook's output contract, or a skill's trigger description. Skill body edits that don't change behavior don't need a bump.
- Marketplace `metadata.version` bumps when the catalog changes (plugin added/removed) or a plugin bump is significant enough to re-announce.
- `CHANGELOG.md` follows Keep a Changelog: `## [x.y.z] — YYYY-MM-DD` → `### Added/Changed/Fixed/Removed`. Add a link reference at the bottom: `[x.y.z]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/vx.y.z`.

## Git workflow

- Remote: `git@github.com:VinhHung1999/memory-system-plugin.git` (hosts the whole marketplace despite its name).
- Commits use the `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` trailer when Claude did the work.
- Push to `main` directly is the norm for small fixes once the user has said "push".
- After editing hooks, remind the user to run `/reload-plugins` so changes take effect in the current session — the hook count in the `/reload-plugins` output doubles as a sanity check (e.g. dropping from 5 to 4 after removing a hook).

## Small but important

- **Never** write to `~/Documents/Notes/HungVault/HungVault/brain2/wiki/code-knowledge/` from code or skills — that's Hung's curated space. The `coder-memory-store` skill stages to `brain2/raw/code-knowledge/` (inbox); Hung promotes to `wiki/` manually.
- When hooks depend on the vault, they must bail silently (`echo '{}'; exit 0`) if the vault is missing — users without brain2 still install the plugin.
- The `./sample_codes` rule from the global CLAUDE.md does not apply here; this repo has no `sample_codes/`.
