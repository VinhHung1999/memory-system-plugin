# maniax — Claude Code plugin marketplace

Ships three plugins: `memory-system` (hooks + skills), `marketing-toolkit` (8 marketing skills), `learn-coursera` (Coursera → skill meta). See `CODEBASE.md` for a full map.

## Rules

Detailed rules live in `.claude/rules/`. Scoped rules load only when Claude edits a matching file.

| Rule file | Scope | What |
|---|---|---|
| `general.md` | Always | Tech stack, repo layout, SemVer + CHANGELOG, git workflow |
| `marketplace.md` | `.claude-plugin/**/*.json`, `plugins/*/.claude-plugin/**/*.json`, `plugins/*/settings.json` | Marketplace catalog + per-plugin manifest schema, plugin settings, permission pre-grants |
| `hooks.md` | `plugins/*/hooks/**/*` | Hook registration, event-specific JSON schemas (incl. PostCompact quirk), stdin parsing, state files, tuning |
| `skills.md` | `plugins/*/skills/**/*` | SKILL.md frontmatter + body, progressive disclosure, scripts vs references, multi-language triggers |

## Local workflow

- Edits to hooks or skill trigger descriptions require a `plugin.json` version bump + CHANGELOG entry, then `/reload-plugins` to take effect locally.
- Don't write to `brain2/wiki/code-knowledge/` from code — that's Hung's curated space. `brain2/raw/code-knowledge/` is the staging inbox.
- Remote is `git@github.com:VinhHung1999/memory-system-plugin.git` (hosts the whole marketplace despite its name).
