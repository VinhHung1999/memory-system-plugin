---
name: init-memory
description: Initialize project memory system. Creates docs/memory/ with topic folders
  and configures auto memory to store there. Use when starting a new project, user says
  "init-memory" or "setup memory", or docs/memory/ does not exist. For rules, use
  /generate-rules instead.
---

# Init Memory

Initialize structured memory for a project. Auto memory will write to `docs/memory/` inside the project.

**For rules** → use `/memory-system:generate-rules` (separate skill)

## Memory Architecture (Do NOT change this)

| Scope | Mechanism | Location | How |
|-------|-----------|----------|-----|
| **Project-specific (this skill)** | Built-in auto memory | `docs/memory/` (in project) | Automatic — Claude learns as you work |

---

## Pre-Flight Checks

1. Check if `docs/memory/` exists in the project root
2. If exists → Report what's there, offer to add missing topics. Stop.
3. If not → Full setup.

---

## Phase 1 — Analyze Project

Detect project type by reading available signals:

1. **Read** (if they exist): `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `CLAUDE.md`, `README.md`
2. **Run**: `ls` on project root
3. **Detect**:
   - `project_name`: from package.json, pyproject.toml, folder name
   - `project_type`: `frontend`, `backend`, `fullstack`, `mobile`, `ml`, `data`, `generic`

| Signal | Type |
|--------|------|
| React, Vue, Next.js, Nuxt (no backend) | `frontend` |
| Express, FastAPI, Django, Flask, Spring (no frontend) | `backend` |
| Both frontend + backend | `fullstack` |
| React Native, Expo, Flutter, Swift, Kotlin | `mobile` |
| PyTorch, TensorFlow, scikit-learn | `ml` |
| pandas, dbt, airflow | `data` |
| None of the above | `generic` |

---

## Phase 2 — Select Memory Topics

### Always included:
- `bugs-and-lessons` — Bugs encountered and lessons learned
- `decisions` — Architecture and technology decisions

### Conditional topics:

| Condition | Topic | Description |
|-----------|-------|-------------|
| `frontend` or `fullstack` | `design-decisions` | UI/UX decisions, component patterns (replaces `decisions`) |
| `backend` or `fullstack` | `api-design` | API endpoints, auth patterns, error handling |
| `mobile` | `platform-notes` | Platform-specific gotchas, native module issues |
| Has DB/migrations | `data-model` | Schema, ORM patterns, migration notes |
| Has Docker/CI | `deployment` | Docker, CI/CD, infrastructure decisions |
| `ml` | `experiments` | Experiments, hyperparameters, results |
| Complex folder structure | `architecture` | System structure, module boundaries |

### Rules:
- **Minimum 3 topics**, **maximum 6 topics**
- If `design-decisions` selected, drop `decisions` (it replaces it)

### User Confirmation:

```
Detected: {project_name} ({project_type})

Memory topics:
1. bugs-and-lessons — Bugs encountered and lessons learned
2. decisions — Architecture and technology decisions
3. api-design — API endpoints, auth patterns

Create these? (or suggest changes)
```

---

## Phase 3 — Create Memory Structure

> **⚠️ IMPORTANT**: Do NOT skip any sub-step. The system requires BOTH the root `MEMORY.md` AND per-topic `INDEX.md` files. If you only create the topic folders without MEMORY.md, the inject hook will fall back to auto-generating stubs — but the result is inferior to proper init.

### 3a. MEMORY.md (entrypoint — REQUIRED)

Write to `docs/memory/MEMORY.md`:

```markdown
# {Project Name} — Project Memory

## Topics

| Topic | Description |
|-------|-------------|
| [bugs-and-lessons](bugs-and-lessons/) | Bugs encountered and lessons learned |
| [decisions](decisions/) | Architecture and technology decisions |
| ... | ... |

## How This Works

Auto memory writes here automatically as Claude learns project patterns.
```

### 3b. Topic Folders (REQUIRED — each needs INDEX.md)

For each topic:
1. Create directory: `docs/memory/{topic}/`
2. Create **INDEX.md** (not README.md):

   ```markdown
   # {Topic Name}
   
   _{one-line description from the topic definition}_
   
   ## Entries
   
   _(empty — Claude will append entries here as memories accumulate)_
   ```

**Do not skip INDEX.md creation** — it's what the inject hook uses to preview each topic at SessionStart.

---

## Phase 4 — Configure Auto Memory

Set `autoMemoryDirectory` in project local settings so built-in auto memory writes to `docs/memory/`:

Write or update `.claude/settings.local.json`:

```json
{
  "autoMemoryDirectory": "docs/memory",
  "autoMemoryEnabled": true
}
```

This redirects auto memory from `~/.claude/projects/<project>/memory/` to the project's `docs/memory/` folder.

---

## Phase 5 — Update CLAUDE.md (Optional)

Only if CLAUDE.md exists and does NOT already mention memory:

Append:

```markdown

## Project Memory

- Project memory is in `docs/memory/` — auto memory writes here automatically
- Update knowledge after big changes: `/memory-system:knowledge-updater`
```

---

## Phase 6 — Final Report

```
Memory initialized for {project_name}!

Created:
  docs/memory/MEMORY.md
  docs/memory/bugs-and-lessons/README.md
  docs/memory/{topic}/README.md
  ...

Config:
  autoMemoryDirectory → docs/memory/
  autoMemoryEnabled → true

Auto memory will now write project learnings to docs/memory/.
For project rules: use /memory-system:generate-rules.
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Memory already exists | Report existing topics, offer to add more |
| No CLAUDE.md | Skip Phase 5 |
| Empty/new project | Use folder name, default topics: bugs-and-lessons, decisions, architecture |
| Monorepo | Create at repo root |
| settings.local.json already exists | Merge, don't overwrite existing settings |
