---
name: coder-memory-recall
description: Retrieve universal coding patterns from ~/.claude/memory/ files. Auto-invokes before complex tasks or when user says "--recall". Searches relevant role directories based on task context. Skip for trivial tasks.
---

## MANDATORY: Use Task Tool (Sub-Agent)

**NEVER execute directly in main context!** Use Task tool with `subagent_type: "general-purpose"` to keep main context clean.

---

## When NOT to Search

- Killing processes, starting servers, basic file operations
- Standard workflows, well-known patterns
- Simple tasks where basic knowledge suffices

**Only search for hard problems** — non-obvious bugs, complex architectures, performance issues, unfamiliar domains.

---

## Storage Location

All memories live in `~/.claude/memory/`. Topic folders are **self-discovered** — no fixed list.

```
~/.claude/memory/
├── <topic-1>/INDEX.md
├── <topic-2>/INDEX.md
└── ...
```

Topics emerge based on what user actually works on. Common ones: `backend-patterns/`, `frontend-patterns/`, `mobile-patterns/`, `debugging/`, `qa-patterns/`, `devops-patterns/`, `universal-patterns/`. But users may have any custom topic.

## Smart Folder Selection

**Step 1 — List what exists**
```bash
ls -d ~/.claude/memory/*/
```

**Step 2 — Pick 1-2 folders most relevant to the task**
- Match task keywords/context to folder names + their INDEX.md content (first 30 lines)
- Always include `universal-patterns/` if unsure
- Prefer existing folders over guessing

**Step 3 — If no folder matches**
- Search ALL folders with grep as a fallback
- Report "No relevant memories found" — fine, not every task has prior learnings

---

## Workflow

### 1. Identify Relevant Folders

See "Smart Folder Selection" above. Pick 1-2 folders based on existing directory listing.

### 2. Read INDEX.md

Start with `~/.claude/memory/<folder>/INDEX.md` to see what memories exist. This avoids reading every file.

### 3. Search for Keywords

```bash
grep -r "keyword1\|keyword2" ~/.claude/memory/<folder>/
```

Also search across all folders if the first search returns nothing:
```bash
grep -r "keyword" ~/.claude/memory/
```

### 4. Read Relevant Files

Read the top 3-5 most relevant memory files found. Look for:
- Past decisions that constrain current work
- Failures/bugs in similar areas
- Patterns/conventions already established
- Procedural workflows that apply

### 5. Present Results

Return concise summary of relevant memories found. Let the main Claude instance decide what to use — don't force-fit patterns.

---

## Decision Criteria: Recall or Skip?

**Recall when:**
- Non-obvious bug or complex architecture decision
- Performance optimization
- Unfamiliar domain where prior patterns could help
- User explicitly asks to check memory

**Skip when:**
- Fixing a typo
- Running a build command
- Simple tasks with well-known answers
- Trivial file operations

---

## If No Results Found

1. Try broader keywords
2. Search `universal-patterns/` if not already searched
3. Search ALL directories as last resort
4. Report "No relevant memories found" — this is fine, not every task has prior learnings
