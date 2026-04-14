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

All memories live in `~/.claude/memory/` organized by role:

```
~/.claude/memory/
├── README.md
├── backend-patterns/       ← API, database, auth, server
├── frontend-patterns/      ← React, Vue, component, UI, state
├── devops-patterns/        ← Docker, K8s, CI/CD, terraform
├── ai-patterns/            ← Model, training, LLM, embedding
├── security-patterns/      ← Vulnerability, encryption, pentest
├── mobile-patterns/        ← iOS, Android, React Native, Flutter
├── pm-patterns/            ← Coordination, team, sprint, planning
├── quant-patterns/         ← Trading, backtest, risk, portfolio
├── debugging/              ← Bug fixes, error workarounds, tracebacks
├── procedures/             ← Step-by-step workflows, how-tos, conversions
├── qa-patterns/            ← Testing, QC, automation, Appium, Playwright
└── universal-patterns/     ← Cross-domain patterns
```

## Role Detection

Pick which directory to search based on task keywords:

| Keywords | Search in |
|----------|-----------|
| api, endpoint, database, server, auth | `backend-patterns/` |
| react, vue, component, ui, css, state | `frontend-patterns/` |
| deploy, docker, kubernetes, ci, cd | `devops-patterns/` |
| model, training, neural, embedding, llm | `ai-patterns/` |
| vulnerability, encryption, pentest | `security-patterns/` |
| ios, android, react-native, flutter | `mobile-patterns/` |
| coordination, team, sprint, planning | `pm-patterns/` |
| trading, backtest, portfolio, risk | `quant-patterns/` |
| bug, error, traceback, fix, workaround | `debugging/` |
| workflow, step-by-step, how-to, conversion | `procedures/` |
| test, qc, qa, automation, appium, playwright, selenium | `qa-patterns/` |
| Cross-domain or unclear | `universal-patterns/` + most relevant role |

---

## Workflow

### 1. Identify Relevant Roles

From the task context, pick 1-2 role directories to search. Always include `universal-patterns/` if unsure.

### 2. Read INDEX.md

Start with `~/.claude/memory/<role>-patterns/INDEX.md` to see what memories exist. This avoids reading every file.

### 3. Search for Keywords

```bash
grep -r "keyword1\|keyword2" ~/.claude/memory/<role>-patterns/
```

Also search across all roles if the first search returns nothing:
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

| Task | Action |
|------|--------|
| Non-obvious bug in API | **Recall** backend-patterns |
| Complex React state issue | **Recall** frontend-patterns |
| Setting up CI/CD pipeline | **Recall** devops-patterns |
| Performance optimization | **Recall** universal-patterns |
| Multi-agent coordination | **Recall** pm-patterns |
| Fixing a typo | **Skip** |
| Running a build command | **Skip** |

---

## If No Results Found

1. Try broader keywords
2. Search `universal-patterns/` if not already searched
3. Search ALL directories as last resort
4. Report "No relevant memories found" — this is fine, not every task has prior learnings
