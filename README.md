# 🧠 Memory System — Claude Code Plugin

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Marketplace](https://img.shields.io/badge/marketplace-maniax-purple.svg)](https://github.com/VinhHung1999/memory-system-plugin)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-v2.1.59+-orange.svg)](https://code.claude.com)

A 4-tier knowledge & memory system for Claude Code. Bundles skills, hooks, and a pre-commit gate that enforces knowledge updates before `git commit`/`push`.

## Why?

Claude Code sessions are stateless. Every new conversation loses:
- Project conventions learned the hard way
- Non-obvious bug patterns
- Architecture decisions
- Cross-project universal patterns

This plugin fixes that with **4 complementary layers** and **auto-sync enforcement**.

---

## 🏗️ Architecture — 4 Tiers

```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE SYSTEM                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIER 1: ALWAYS-ON RULES                                     │
│    Skill: /generate-rules                                    │
│    • CLAUDE.md ──────────► Every session                     │
│    • .claude/rules/*.md ─► When file path matches            │
│                                                              │
│  TIER 2: PROJECT MEMORY (built-in auto memory)               │
│    • .claude/memory/ ────► Per-project, auto-updated         │
│    Setup: /init-memory                                       │
│                                                              │
│  TIER 3: UNIVERSAL MEMORY (cross-project)                    │
│    • ~/.claude/memory/<domain>/                              │
│    • Auto-discovered folders (backend, frontend, qa, ...)    │
│    Skills: /coder-memory-store, /coder-memory-recall         │
│                                                              │
│  TIER 4: SYNC + ENFORCEMENT                                  │
│    • /knowledge-updater (manual or pre-commit)               │
│    • Pre-commit gate blocks commits until sync runs          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 What's Inside

### Skills (5)

| Skill | Purpose |
|---|---|
| `/generate-rules` | Analyze codebase and generate `.claude/rules/` files with path-scoped frontmatter |
| `/init-memory` | Initialize project memory — creates `.claude/memory/` and configures `autoMemoryDirectory` |
| `/coder-memory-store` | Save universal patterns to `~/.claude/memory/<domain>/` |
| `/coder-memory-recall` | Retrieve patterns from universal memory |
| `/knowledge-updater` | Analyze recent changes and route to correct knowledge store |

### Hooks (3)

| Hook | Trigger | Purpose |
|---|---|---|
| `inject.sh` | SessionStart, PostCompact, PreToolUse Read | Inject Universal Memory index into context |
| `pre-commit-gate.sh` | PreToolUse Bash (`git commit`/`push`) | Block until `/knowledge-updater` runs |
| `memory_store_reminder.py` | Stop (every 3rd turn, ≥3 tool calls) | Remind to save universal patterns |

### Settings

- `autoMemoryEnabled: true` — enables built-in auto memory for project-specific learnings

---

## 🚀 Installation

### Step 1 — Add the marketplace

In Claude Code, run:

```
/plugin marketplace add VinhHung1999/memory-system-plugin
```

This fetches the marketplace catalog from GitHub.

### Step 2 — Install the plugin

```
/plugin install memory-system@maniax
```

Syntax: `/plugin install <plugin-name>@<marketplace-name>`

### Step 3 — Verify

```
/plugin
```

You should see `memory-system` in the enabled list. Skills are now available as `/memory-system:*`.

### Alternative: local testing

```bash
git clone https://github.com/VinhHung1999/memory-system-plugin.git
claude --plugin-dir ./memory-system-plugin/plugins/memory-system
```

### Updating

```
/plugin marketplace update maniax
```

---

## 📖 Usage

### Available commands

After install, all skills are prefixed with `memory-system:`:

| Command | When to use |
|---|---|
| `/memory-system:init-memory` | First time on a new project — setup `.claude/memory/` folders |
| `/memory-system:generate-rules` | Create/update `.claude/rules/` with path-scoped conventions |
| `/memory-system:knowledge-updater` | After significant changes — sync CLAUDE.md/rules/memory/skills |
| `/memory-system:coder-memory-store` | Save a universal pattern you just learned |
| `/memory-system:coder-memory-recall` | Search universal memory by keyword |

### Typical workflow

**1. New project setup (once)**
```
/memory-system:init-memory         # creates .claude/memory/ + auto memory config
/memory-system:generate-rules      # creates .claude/rules/*.md from codebase analysis
```

**2. Daily work (zero effort)**
- Claude sees Universal Memory index on every session start → `🚀 Universal Memory ready...`
- Rules auto-load when Claude reads files matching `paths:` patterns
- Auto memory learns project patterns silently
- Every 3rd substantial turn → reminder to capture new universal patterns

**3. Before committing**
```
# You: "commit these changes"
# Claude: runs `git commit` → 🚫 BLOCKED by gate
# Claude: runs /memory-system:knowledge-updater → reviews changes
# Claude: retries commit → ✅ passes
```

**4. When you learn something worth remembering**
```
/memory-system:coder-memory-store
# Claude picks the right domain folder (backend-patterns/, debugging/, etc.)
# Writes a structured memory file
# Updates INDEX.md
```

**5. When you need to recall something**
```
/memory-system:coder-memory-recall <keyword>
# Claude greps universal memory folders and returns relevant patterns
```

---

## 🎯 Quick Start

### 1. Initialize a project

```
/memory-system:init-memory
```

This will:
- Detect project type (frontend/backend/fullstack/mobile/ml)
- Create `.claude/memory/` with topic folders (bugs-and-lessons, decisions, etc.)
- Configure `autoMemoryDirectory` so built-in auto memory writes to that folder

### 2. Work normally

Claude sees universal memory location on every session start. When relevant, Claude reads topic INDEX.md files automatically.

### 3. Commit workflow

```bash
# You ask Claude to commit
"Commit these changes"

# Claude tries: git commit -m "..."
# → 🚪 BLOCKED by pre-commit-gate.sh
# → "Run /knowledge-updater first"

# Claude runs /knowledge-updater
# → Reviews git diff
# → Updates CLAUDE.md / rules / memory / skills if needed
# → Marks session as done

# Claude retries: git commit -m "..."
# → ✅ Passes, commits successfully
```

### 4. Capture universal lessons

When you hit a non-obvious bug or pattern:

```
/memory-system:coder-memory-store

# Claude analyzes conversation
# Picks domain folder (backend/frontend/debugging/qa/etc.)
# Writes structured memory file
# Updates INDEX.md
```

---

## 🔧 How Each Tier Works

### Tier 1: Rules

Use `/generate-rules` (bundled in this plugin) to create `.claude/rules/` files with path-scoped frontmatter:

```markdown
---
paths:
  - "src/api/**/*.py"
---
# Backend API rules
...
```

Rules auto-load when Claude reads matching files.

### Tier 2: Project Memory (auto)

After `/init-memory`:
- Built-in auto memory writes to `.claude/memory/<topic>/`
- Claude learns project-specific patterns automatically
- No manual action needed

### Tier 3: Universal Memory (manual skill)

- Organized by domain: `~/.claude/memory/backend-patterns/`, `frontend-patterns/`, etc.
- Folders auto-discovered — just create a new one and plugin picks it up
- Stop hook reminds every 3rd substantial turn to save lessons

### Tier 4: Sync + Enforcement

- `/knowledge-updater` reviews changes and updates the right store
- Pre-commit gate ensures you never forget to sync before sharing code

---

## 🛠️ Customization

### Change reminder frequency

Edit `hooks/memory_store_reminder.py`:

```python
REMIND_EVERY_N_STOPS = 3      # Fire every Nth stop
MIN_TOOL_CALLS = 3            # Require ≥ N tool calls in recent turns
```

### Disable the commit gate

Remove the `Bash` matcher entry from `hooks/hooks.json`.

### Add custom domain folders

Just create `~/.claude/memory/my-domain/` — the inject hook scans dynamically, no config needed.

---

## 📋 Requirements

- Claude Code v2.1.59+ (for auto memory support)
- `bash`, `python3` (for hooks)
- Git (for pre-commit gate to make sense)

---

## 🎨 What You'll See

### Session start
```
🚀 Universal Memory (global, cross-project knowledge) ready at ~/.claude/memory/
  • ai-patterns (3)
  • backend-patterns (7)
  • debugging (4)
  • frontend-patterns (9)
  • mobile-patterns (12)
  • qa-patterns (2)
  • universal-patterns (6)
```

### On every Read (dimmed reminder)
```
✨ Read Universal Memory if relevant → ~/.claude/memory/<topic>/
```

### On git commit (if not synced)
```
🚫 Blocked: before 'git commit', run /knowledge-updater first.
```

---

## 🐛 Troubleshooting

**Gate won't unblock?**

The `/knowledge-updater` skill writes to `~/.claude/knowledge_updater_state.json` with your session ID. If it fails to write, run:

```bash
echo '{"<your-session-id>": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' > ~/.claude/knowledge_updater_state.json
```

**Stop hook fires too often?**

Edit `hooks/memory_store_reminder.py` → increase `REMIND_EVERY_N_STOPS`.

**Inject hook not rendering colors?**

Your terminal or Claude Code version may not support ANSI. Colors degrade gracefully — functionality still works.

---

## 📝 License

MIT

## 🙏 Credits

Built through iterative co-design with Claude. Inspired by the "full combo memory system" patterns shared in the Claude Code community.
