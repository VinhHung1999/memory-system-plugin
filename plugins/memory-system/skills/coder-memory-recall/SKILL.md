---
name: coder-memory-recall
description: Retrieve universal coding patterns from ~/.claude/memory/ files. Auto-invokes before complex tasks or when user says "--recall". Searches relevant role directories based on task context. Skip for trivial tasks.
---

## MANDATORY: Use Task Tool (Sub-Agent, Background)

**NEVER execute directly in main context!** Use Task tool with:
- `subagent_type: "general-purpose"`
- `run_in_background: true`

Running the subagent in background keeps the main conversation flowing while the recall search happens in parallel. You'll be notified when results arrive.

---

## When NOT to Search

- Killing processes, starting servers, basic file operations
- Standard workflows, well-known patterns
- Simple tasks where basic knowledge suffices

**Only search for hard problems** — non-obvious bugs, complex architectures, performance issues, unfamiliar domains.

---

## Storage Location (2-level hierarchy)

```
~/.claude/memory/
├── <domain>/                    e.g., frontend-patterns, mobile-patterns
│   ├── INDEX.md                 top-level overview
│   ├── bugs/
│   │   ├── INDEX.md
│   │   └── <insight>.md
│   ├── patterns/
│   ├── decisions/
│   ├── procedures/
│   └── structure/
└── <another-domain>/
```

**Level 1 — Domain** (self-discovered): `backend-patterns/`, `frontend-patterns/`, `mobile-patterns/`, `blockchain-patterns/`, `universal-patterns/`, etc.

**Level 2 — Category** (fixed set): `bugs/`, `patterns/`, `decisions/`, `procedures/`, `structure/`.

## Smart Search (2-level)

**Step 1 — List domains**
```bash
ls -d ~/.claude/memory/*/
```

**Step 2 — Pick 1-2 relevant domains**
- Match task keywords/context to domain names + their `INDEX.md` (first 30 lines)
- Always include `universal-patterns/` if unsure

**Step 3 — Pick relevant CATEGORY within each domain**

Based on task type:
- Debugging a bug → `bugs/`
- Looking for best practice → `patterns/`
- Making architecture decision → `decisions/` + `patterns/`
- Setting up a workflow → `procedures/`
- Questioning folder layout → `structure/`

**Step 4 — Read category INDEX first**
```bash
cat ~/.claude/memory/<domain>/<category>/INDEX.md
```

**Step 5 — Grep within scope**
```bash
grep -r "keyword" ~/.claude/memory/<domain>/<category>/
```

Widen if no hits:
```bash
grep -r "keyword" ~/.claude/memory/<domain>/     # whole domain
grep -r "keyword" ~/.claude/memory/              # all domains
```

---

## Workflow

### 1. Identify Scope (domain + category)

See "Smart Search" above. Narrow to `<domain>/<category>/` before searching.

### 2. Read INDEX files top-down

1. `~/.claude/memory/<domain>/INDEX.md` — overview of categories + highlights
2. `~/.claude/memory/<domain>/<category>/INDEX.md` — full list of entries

This avoids reading every memory file.

### 3. Search for Keywords

```bash
grep -r "keyword1\|keyword2" ~/.claude/memory/<domain>/<category>/
```

Widen progressively if no hits:
```bash
grep -r "keyword" ~/.claude/memory/<domain>/     # whole domain (all categories)
grep -r "keyword" ~/.claude/memory/              # all domains (last resort)
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
