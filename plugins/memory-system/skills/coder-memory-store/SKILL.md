---
name: coder-memory-store
description: Store universal coding patterns into ~/.claude/memory/ files. Auto-invokes after difficult tasks with broadly-applicable lessons. Trigger with "--store" or when user expresses frustration (strong learning signals). Skip for trivial or project-specific patterns (use project-memory-store for those).
---

## MANDATORY: Use Task Tool (Sub-Agent)

**NEVER execute directly in main context!** Use Task tool with `subagent_type: "general-purpose"` to keep main context clean.

---

## When NOT to Store

- Simple commands, basic operations, well-documented patterns
- Project-specific patterns (use project-memory-store instead)
- Anything Google-able in 30 seconds

**Only store hard-won lessons** — non-obvious bugs, surprising patterns, failures, universal insights.

---

## Storage Location

All memories go to `~/.claude/memory/` organized by **self-discovered** topic folders.

**No fixed folder list.** Topics emerge organically from actual usage:

```
~/.claude/memory/
├── <topic-1>/INDEX.md
├── <topic-2>/INDEX.md
└── ...
```

Common topics that tend to appear: `backend-patterns/`, `frontend-patterns/`, `mobile-patterns/`, `debugging/`, `qa-patterns/`, `devops-patterns/`, `universal-patterns/`. But users can have any topic they need — `blockchain-patterns/`, `game-dev/`, `ml-ops/`, etc.

## Folder Routing (Smart Auto-Discovery)

When storing a memory, pick the folder in this order:

**Step 1 — List existing folders**
```bash
ls -d ~/.claude/memory/*/
```

**Step 2 — Match task context to an existing folder**
- Read the task/insight content
- Compare to existing folder names + their `INDEX.md` (first 30 lines) if present
- If clear match → **use existing folder** (strongly prefer reuse over creating new)

**Step 3 — If no existing folder matches well**
- Is the insight genuinely a **new domain**? (e.g., first blockchain pattern in a codebase that's never had any)
  → Create new folder with kebab-case name, suffix `-patterns` if unclear (e.g., `blockchain-patterns/`)
- Is the insight **general / cross-domain**?
  → Save to `universal-patterns/` (create if missing)

**Step 4 — Create the chosen folder if it doesn't exist**

### Naming rules for new folders

- **kebab-case** only
- Use meaningful domain names: `blockchain-patterns`, `game-dev`, `data-engineering`
- **Avoid** one-off names (`feature-123-patterns` ❌) or project names (`acme-corp-patterns` ❌)
- When in doubt → `universal-patterns/`

### Anti-fragmentation rule

Don't create a new folder for a **single** insight unless you're very confident it's a distinct domain. If only 1 insight might go there, prefer `universal-patterns/` until you have 2-3 related ones — then reorganize later.

---

## Workflow

### 1. Extract Insights

Analyze conversation for **0-3 insights** (usually 0-1).

**Criteria (ALL must be true):**
- **Non-obvious**: Not standard practice → "useCallback without deps causes stale closures"
- **Universal**: Applies beyond one project → "Exponential backoff with jitter prevents thundering herd"
- **Actionable**: Concrete guidance → "Use debouncing (300ms) for autocomplete inputs"
- **Valuable**: Helps future similar situations

### 2. Check for Duplicates

```bash
grep -r "keyword" ~/.claude/memory/<role>-patterns/
```

Read `INDEX.md` in the target directory if it exists.

- **Duplicate** → MERGE into existing file
- **Related** → UPDATE existing file with new info
- **New** → CREATE new file

### 3. Write Memory File

**Filename**: `<short-descriptive-name>.md` (lowercase, hyphens)

**Format**:
```markdown
# <Title>

**Type:** Episodic | Procedural | Semantic
**Tags:** #tag1 #tag2 #success or #failure
**Created:** YYYY-MM-DD

---

## Description
One sentence summary.

## Content
3-5 sentences: what happened, what was tried, what worked/failed, key lesson.

## Related
Links to related memories if any.
```

### 4. Update INDEX.md

Append to `~/.claude/memory/<role>-patterns/INDEX.md`:
```markdown
- [Title](filename.md) — one-line summary
```

Create INDEX.md if it doesn't exist.

---

## Handling Conflicts

| Situation | Action |
|-----------|--------|
| Near-identical memory exists | **MERGE** — combine best parts into one file |
| Related memory exists | **UPDATE** — add "Updated YYYY-MM-DD:" section |
| 2+ episodic show a common pattern | **GENERALIZE** — create semantic memory linking to them |
| Contradicts old memory | **UPDATE** — add "Previous approach:" to show evolution |

---

## Frustration = Strong Learning Signal

When user expresses frustration (fuck, shit, wtf, stupid, etc.), this is a **critical learning moment**:
1. Store with full failure context
2. Tag with `#failure` and `#strong-signal`
3. Prioritize over routine successes

---

## Examples

**Good** (backend-patterns/rate-limit-thundering-herd.md):
```markdown
# API Rate Limiting: Thundering Herd

**Type:** Semantic
**Tags:** #backend #api #rate-limiting #failure #success
**Created:** 2026-02-06

---

## Description
Simple retry logic causes thundering herd; use exponential backoff with jitter.

## Content
When implementing rate limiting, fixed-delay retries cause all clients to retry simultaneously, overwhelming the server. Solution: exponential backoff (2^n seconds) with random jitter (±30%). This spreads retry attempts and prevents cascading failures. Key lesson: distributed systems need randomness to avoid synchronization disasters.
```

**Bad** (too vague):
```markdown
# Fixed API Bug
Fixed a rate limiting bug. It works now.
```
