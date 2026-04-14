---
name: reorganize
description: Migrate flat memory files into the 2-level hierarchy (domain/category/file.md). Scans ~/.claude/memory/ for domains exceeding the flat threshold and sorts existing .md files into bugs/patterns/decisions/procedures/structure subcategories. Use when user says "reorganize memory", "migrate memory", "dọn memory", or after bumping plugin to 1.5.0+.
---

## MANDATORY: Use Task Tool (Sub-Agent, Background)

Use Task tool with:
- `subagent_type: "general-purpose"`
- `run_in_background: true`

Reorganization is a batch operation — background keeps the main conversation flowing.

## Purpose

The 2-level hierarchy (`<domain>/<category>/<file>.md`) replaces the old flat layout. This skill migrates existing flat files into the new structure without losing content or history.

## Scope

Run against `~/.claude/memory/`. Optionally scope to a single domain (`~/.claude/memory/<domain>/`) if user only wants to clean one folder.

## Workflow

### 1. List domains and file counts

```bash
for dir in ~/.claude/memory/*/; do
  name=$(basename "$dir")
  flat_count=$(find "$dir" -maxdepth 1 -name "*.md" -not -name "INDEX.md" 2>/dev/null | wc -l | tr -d ' ')
  echo "$name: $flat_count flat files"
done
```

### 2. Decide per domain

| Condition | Action |
|---|---|
| Flat count ≤ 3 | **Skip** — keep flat, no reorganization needed |
| Flat count > 3 AND no sub-folders yet | **Migrate** — sort into bugs/patterns/decisions/procedures/structure |
| Has sub-folders already | **Verify only** — spot-check files are in right category, leave alone otherwise |

### 3. Classify each flat file

Read each `.md` file (first 20 lines is usually enough to classify). Match content to a category using the same priority as `coder-memory-store`:

1. `bugs/` — fix for specific error, traceback, failure
2. `decisions/` — "chose X over Y" with tradeoffs
3. `procedures/` — step-by-step how-to
4. `structure/` — folder/project organization
5. `patterns/` — default catch-all for "best practice"

If none of the 5 fits and the insight is specialized (e.g., multiple entries on animations), create a named sub-category.

### 4. Move files

For each file needing migration:

```bash
mkdir -p ~/.claude/memory/<domain>/<category>
git mv ~/.claude/memory/<domain>/<file>.md ~/.claude/memory/<domain>/<category>/<file>.md
# If not git-tracked, use regular mv
```

Prefer `git mv` when the memory dir is a git repo (preserves history).

### 5. Rebuild INDEX.md at both levels

**Category-level INDEX** (`<domain>/<category>/INDEX.md`):
```markdown
# <Category> — <Domain>

## Entries
- [Title](filename.md) — one-line summary
- ...
```

**Domain-level INDEX** (`<domain>/INDEX.md`):
```markdown
# <Domain>

## Categories

| Category | Count | Description |
|---|---|---|
| [bugs/](bugs/INDEX.md) | N | Bug fixes and workarounds |
| [patterns/](patterns/INDEX.md) | N | Recurring best practices |
| [decisions/](decisions/INDEX.md) | N | Architecture choices |
| [procedures/](procedures/INDEX.md) | N | Step-by-step workflows |
| [structure/](structure/INDEX.md) | N | Project organization |

## Highlights
- [Most important entry 1](category/file.md)
- [Most important entry 2](category/file.md)
```

### 6. Report

Return a concise summary:

```
Reorganized 3 domains:
  mobile-patterns: 13 flat → bugs/5, patterns/4, procedures/3, decisions/1
  frontend-patterns: 9 flat → bugs/3, patterns/4, decisions/1, structure/1
  backend-patterns: 7 flat → bugs/2, patterns/3, decisions/1, procedures/1

Skipped (under threshold):
  pm-patterns (1 file), procedures (1 file), ai-patterns (3 files)

All INDEX.md files rebuilt.
```

## Safety

- **Read before move** — always classify content, never move blindly
- **Preserve filenames** — don't rename during migration, just relocate
- **Git-aware** — if `~/.claude/memory/` is a git repo, use `git mv` for history
- **Dry run option** — if user says "dry run" or "preview", list planned moves without executing
- **Don't touch files in existing sub-folders** — they're already migrated
- **Ambiguous files**: if a file truly doesn't fit anywhere, leave it flat at domain root and report it in the summary

## Edge cases

| Scenario | Behavior |
|---|---|
| Domain has both flat files AND sub-folders | Move only the flat files; leave sub-folders untouched |
| File is symlink | Skip, report |
| Two files with same name in different categories after migration | Shouldn't happen (names come from domain root) but report collisions |
| MEMORY.md at memory root | Leave alone — that's the master index, not a memory file |
