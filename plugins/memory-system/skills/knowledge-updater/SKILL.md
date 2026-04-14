---
name: knowledge-updater
description: Analyze recent code changes and update the right knowledge store — CLAUDE.md, .claude/rules/, ~/.claude/memory/, or skills. Use this skill after making significant changes to a project, after a major refactor, when conventions change, or when you discover patterns worth preserving. Trigger with "/knowledge-updater" or when user says "update knowledge", "cập nhật kiến thức", "sync rules", or "update rules".
---

## What This Skill Does

After significant code changes, knowledge gets stale — CLAUDE.md may reference old build commands, rules may not cover new patterns, memory may miss new learnings. This skill analyzes what changed and routes updates to the correct knowledge store.

## Knowledge Stores — When to Update Each

| Store | Location | Update When | Examples |
|-------|----------|-------------|---------|
| **CLAUDE.md** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project-wide conventions change | New build command, project restructure, new git workflow |
| **Rules** | `./.claude/rules/*.md` | Domain-specific standards change | New API pattern for BE, new component convention for FE |
| **Memory** | `~/.claude/memory/<domain>/` | Non-obvious lesson learned | Surprising bug, debugging technique, architecture insight |
| **Skills** | `./.claude/skills/` | Workflow or procedure changes | Deploy process changed, new testing workflow |

**Decision tree:**

```
Is this a project-wide convention everyone must follow?
  → YES → CLAUDE.md (if < 200 lines) or .claude/rules/ (if domain-specific)
  
Is this specific to a file type or directory?
  → YES → .claude/rules/ with paths: frontmatter

Is this a hard-won lesson or non-obvious pattern?
  → YES (universal) → ~/.claude/memory/ via /coder-memory-store
  → YES (project-specific) → auto memory handles it automatically

Is this a changed workflow or procedure?
  → YES → Update the relevant skill in .claude/skills/
```

## Workflow

### 1. Analyze Changes

Examine what changed in this session:

```bash
# Recent changes in working tree
git diff --stat
git diff --name-only

# Recent commits (if already committed)
git log --oneline -5
git diff HEAD~1 --stat
```

Also consider conversation context — what was the user working on, what problems were solved, what decisions were made.

### 2. Categorize Changes

For each significant change, determine:

- **What changed**: file paths, patterns, conventions
- **Why it changed**: bug fix, refactor, new feature, convention update
- **Who needs to know**: everyone (CLAUDE.md), domain-specific (rules), future-self (memory), workflow (skills)

### 3. Route to Correct Store

**For CLAUDE.md updates:**
- Read current CLAUDE.md first
- Only add/modify what changed — don't rewrite the whole file
- Keep it under 200 lines total
- Focus on "always do X" rules, build commands, project structure

**For rules updates:**
- Check if a matching rule file exists in `.claude/rules/`
- If yes, update the existing rule file with the new convention
- If no rules exist at all, suggest running `/generate-rules` (it does deep codebase analysis)
- For adding a single new rule to an existing setup, create one with appropriate `paths:` frontmatter

**For memory updates:**
- Use skill `/coder-memory-store` for universal patterns (cross-project)
- Project-specific learnings are handled by built-in auto memory (automatic, no action needed)
- Route to correct domain folder based on keywords (see role detection table below)

**For skills updates:**
- Identify which skill's workflow changed
- Read the current SKILL.md and update the relevant section

### 4. Memory Domain Routing

Delegate to `/coder-memory-store` — it auto-discovers folders by scanning `~/.claude/memory/` and matches content to existing folder names/INDEX.md. It creates new folders only when a genuinely new domain appears, falling back to `universal-patterns/` for one-off insights.

### 5. Report

After making updates, report in 1-2 lines:

```
Updated: .claude/rules/backend.md (added new validation pattern for API endpoints)
Updated: ~/.claude/memory/debugging/ via /coder-memory-store (SSE connection timeout workaround)
```

### 6. Mark as Ran (unblock git commit/push)

After completing the review (whether updates were made or not), mark this session as done so the pre-commit gate unblocks:

```bash
SESSION_ID="${CLAUDE_SESSION_ID:-default}"
STATE_FILE="$HOME/.claude/knowledge_updater_state.json"
python3 -c "
import json, os
f = '$STATE_FILE'
d = json.load(open(f)) if os.path.exists(f) else {}
d['$SESSION_ID'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
json.dump(d, open(f, 'w'))
"
```

If you don't know the session_id, use 'default' as the key. This is safe — the next session will get a fresh gate.

## Important

- Read before writing — always check current content before modifying
- Don't duplicate — if the knowledge already exists, skip or merge
- Be concise — rules and CLAUDE.md should be specific and actionable, not verbose
- Respect scope — project-specific goes to rules/CLAUDE.md, universal goes to memory
- When updating memory, delegate to `/coder-memory-store` or `/project-memory-store` skills — they handle the file format, INDEX.md, and duplicate checking
