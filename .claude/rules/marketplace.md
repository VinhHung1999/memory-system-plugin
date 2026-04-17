---
paths:
  - ".claude-plugin/**/*.json"
  - "plugins/*/.claude-plugin/**/*.json"
  - "plugins/*/settings.json"
---

# Plugin & marketplace manifests

Two manifest levels coexist: the marketplace catalog and the per-plugin manifest. They must stay in sync — a mismatch makes `/plugin` silently fail to find the plugin.

## Marketplace catalog — `.claude-plugin/marketplace.json`

Fields used today:

```json
{
  "name": "maniax",
  "owner": { "name": "Phu Hung" },
  "metadata": {
    "description": "…",
    "version": "1.12.0"
  },
  "plugins": [
    {
      "name": "memory-system",
      "source": "./plugins/memory-system",
      "description": "…",
      "version": "1.0.0",
      "author": { "name": "Phu Hung" },
      "homepage": "https://github.com/VinhHung1999/memory-system-plugin",
      "repository": "https://github.com/VinhHung1999/memory-system-plugin",
      "license": "MIT",
      "keywords": ["…"],
      "category": "productivity"
    }
  ]
}
```

Rules:

- `source` must be a relative path (`./plugins/<name>`) — the CLI resolves it from the marketplace root.
- `plugins[].name` must match exactly the per-plugin `plugin.json` `name` field.
- `plugins[].version` in the catalog is a display value for the marketplace UI; the per-plugin `plugin.json` version is authoritative for install/update decisions. Keep them equal to avoid confusion.
- `category` values seen today: `productivity`, `marketing`. Stick with existing categories rather than inventing new ones unless the plugin genuinely doesn't fit.

## Per-plugin manifest — `plugins/<name>/.claude-plugin/plugin.json`

```json
{
  "name": "memory-system",
  "description": "…",
  "version": "1.10.3",
  "author": { "name": "Phu Hung", "url": "https://github.com/VinhHung1999" },
  "homepage": "https://github.com/VinhHung1999/memory-system-plugin",
  "license": "MIT"
}
```

- `version` is the source of truth Claude Code reads when deciding whether the user has the latest. Bump it **every time** you change hook behavior, hook output contracts, or skill triggers.
- `name` must be kebab-case and match the directory under `plugins/`.
- Keep descriptions short but specific — they render in `/plugin` lists.

## Plugin `settings.json`

`plugins/<name>/settings.json` is merged into the user's Claude Code settings when the plugin is enabled. Two concerns live here:

1. **Plugin defaults** — e.g. `autoMemoryEnabled: true` in `memory-system`. Only set defaults the plugin actually requires to function.
2. **Pre-granted permissions** — `permissions.allow` entries that stop subagent permission prompts for the plugin's own write paths. The `memory-system` plugin pre-grants `Write/Edit/Read/Bash` on `~/Documents/Notes/HungVault/HungVault/brain2/**` because its store/recall skills run in background subagents where an interactive prompt is never seen by the user.

When adding a new permission entry:

- Scope it as narrowly as possible — prefer a specific directory glob over `*`.
- Mirror any Bash commands the skill actually runs (e.g. `Bash(grep:*)`, `Bash(qmd:*)`, `Bash(mkdir -p <path>/**)`).
- After editing, tell the user to run `/reload-plugins` so the permission merge re-applies.

## When `/plugin` or `/reload-plugins` misbehaves

- Mismatched `name` between marketplace and plugin manifests → plugin looks missing. Check both files.
- Bumped `plugin.json` version but didn't touch `marketplace.json` → the marketplace UI still shows the old version. Bump the catalog entry too (or the marketplace `metadata.version`) if the change is user-visible.
- Changed hook script but count of hooks in `/reload-plugins` output didn't change → you probably edited the script but not `hooks.json`, which is fine; count only changes on registration changes.
