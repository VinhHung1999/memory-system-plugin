---
name: coder-memory-store
description: Store universal coding patterns into ~/.claude/memory/ files. Auto-invokes after difficult tasks with broadly-applicable lessons. Trigger with "--store" or when user expresses frustration (strong learning signals). Skip for trivial or project-specific patterns (use project-memory-store for those).
---

## MANDATORY: Use Task Tool (Sub-Agent, Background)

**NEVER execute directly in main context!** Use Task tool with:
- `subagent_type: "general-purpose"`
- `run_in_background: true`

Running the subagent in background keeps the main conversation flowing — you don't block on memory writes. You'll be notified when it completes, and can continue the current task immediately.

**Permissions**: The plugin pre-grants Write/Edit/Read/Bash access to `~/.claude/memory/**` so the subagent can write without permission prompts. If errors appear, check `settings.json` `permissions.allow` has the required patterns.

---

## When NOT to Store

- Simple commands, basic operations, well-documented patterns
- Project-specific patterns (use project-memory-store instead)
- Anything Google-able in 30 seconds

**Only store hard-won lessons** — non-obvious bugs, surprising patterns, failures, universal insights.

---

## Storage Location (2-level hierarchy)

All memories go to `~/.claude/memory/` with **domain → category → file** structure:

```
~/.claude/memory/
├── <domain>/                    e.g., frontend-patterns, mobile-patterns
│   ├── INDEX.md                 top-level index (lists categories + highlights)
│   ├── bugs/
│   │   ├── INDEX.md             category index
│   │   └── <insight>.md         actual memory file
│   ├── patterns/
│   │   ├── INDEX.md
│   │   └── <insight>.md
│   ├── decisions/
│   │   ├── INDEX.md
│   │   └── <insight>.md
│   ├── procedures/
│   │   ├── INDEX.md
│   │   └── <insight>.md
│   └── structure/               optional — project layout, organization
│       ├── INDEX.md
│       └── <insight>.md
└── <another-domain>/
    └── ...
```

### Level 1 — Domain (self-discovered)

Topics emerge organically: `backend-patterns/`, `frontend-patterns/`, `mobile-patterns/`, `blockchain-patterns/`, `claude-code-patterns/`, `universal-patterns/`, etc. Users can have any domain.

### Level 2 — Category (default set + extensible)

**Default categories** (prefer these; fits most insights):

| Category | What goes here | Example |
|---|---|---|
| `bugs/` | Bugs, errors, workarounds, fixes | "useCallback stale closure fix" |
| `patterns/` | Recurring best practices, idioms | "Exponential backoff with jitter" |
| `decisions/` | Architecture choices, tradeoffs | "Zustand over Redux for this use case" |
| `procedures/` | Step-by-step how-tos, workflows | "Setup Prisma + PostgreSQL" |
| `structure/` | Folder/project organization | "Monorepo layout for apps + packages" |

**Extending — create new category when needed**

If an insight genuinely doesn't fit the 5 defaults, create a new sub-category. Examples:
- `animations/` inside `frontend-patterns/` — specialized topic deserving its own bucket
- `performance/` inside `backend-patterns/` — if you accumulate enough perf insights
- `integrations/` inside `mobile-patterns/` — third-party SDK integrations

**Rules for new categories:**
- Use kebab-case, descriptive, singular or plural consistently
- Don't create for 1 insight — try fitting into a default first
- Promote to new category when you have 2-3 related insights that feel cramped in a default

Create the category folder and its INDEX.md when the first insight of that type arrives. Don't pre-create empty ones.

## Folder Routing (Smart Auto-Discovery)

**Step 1 — Pick the DOMAIN (level 1)**
```bash
ls -d ~/.claude/memory/*/
```
- Match task content to an existing domain folder (prefer reuse)
- If no match but clear domain → create new domain folder
- If genuinely cross-cutting → use `universal-patterns/`

**Step 2 — Pick the CATEGORY (level 2)**

First, list existing categories in the chosen domain:
```bash
ls -d ~/.claude/memory/<domain>/*/
```

**Match an existing category if possible** (reuse over create).

Otherwise classify into a default:
- Bug/error/workaround → `bugs/`
- Recurring best practice → `patterns/`
- Architecture decision with tradeoffs → `decisions/`
- Step-by-step workflow → `procedures/`
- Project/folder organization → `structure/`

**If none of the 5 defaults fits** (insight is a specialized topic): create a new sub-category (kebab-case), e.g., `animations/`, `performance/`, `integrations/`.

### Tie-breaker when ambiguous

When an insight fits multiple categories, pick the **most specific** in this priority order:

1. `bugs/` — if it's a fix for a specific error/failure
2. `decisions/` — if the focus is choosing X over Y with tradeoffs
3. `procedures/` — if it's a multi-step how-to
4. `structure/` — if it's about folder/project organization
5. `patterns/` — default catch-all for "this is how to do X well"

Example: "Use debounce 300ms for autocomplete (tested 100/300/500ms)"
- Has a specific choice with tradeoffs → `decisions/`
- Also a general pattern → would go to `patterns/`
- Tie-breaker says `decisions/` wins (#2 beats #5)

**Step 3 — Create path and write**

Full path: `~/.claude/memory/<domain>/<category>/<filename>.md`

Create `<category>/` subfolder and its `INDEX.md` if missing.

### Naming rules

- Domains: kebab-case, meaningful (`blockchain-patterns`, `game-dev`)
- Files: kebab-case, descriptive (`usecallback-stale-closure.md`)

### Default behavior

- **Prefer creating new domain folder** over dumping into `universal-patterns/`
- **Prefer creating new category subfolder** over skipping level 2
- `universal-patterns/` still has the same 2-level structure (bugs/, patterns/, decisions/, procedures/)

### Flat vs 2-level threshold

To avoid over-engineering small domains:

| Domain file count | Structure |
|---|---|
| **≤ 3 total files** | Flat — save directly to `<domain>/<filename>.md` |
| **> 3 total files** | Use 2-level — save to `<domain>/<category>/<filename>.md` |

**When crossing the threshold (4th file arrives)**: the skill should migrate existing flat files into sub-categories first. Suggest running `/memory-system:reorganize` for the domain, or do it inline if the migration is trivial (3-4 files).

This keeps small domains (e.g., `pm-patterns/` with 1 file) simple, and organizes large domains (e.g., `mobile-patterns/` with 13 files) clearly.

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

Search both domain and category:
```bash
grep -r "keyword" ~/.claude/memory/<domain>/<category>/
grep -r "keyword" ~/.claude/memory/<domain>/   # fallback, whole domain
```

Read `INDEX.md` files along the way:
- `~/.claude/memory/<domain>/INDEX.md` (overview)
- `~/.claude/memory/<domain>/<category>/INDEX.md` (detailed)

- **Duplicate** → MERGE into existing file
- **Related** → UPDATE existing file with new info
- **New** → CREATE new file in `<domain>/<category>/`

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

### 4. Update INDEX.md at BOTH levels

**Level 2 (category INDEX)** — `~/.claude/memory/<domain>/<category>/INDEX.md`

Append:
```markdown
- [Title](filename.md) — one-line summary
```

Create if missing, with header:
```markdown
# <Category> — <Domain>

## Entries
- [Title](filename.md) — one-line summary
```

**Level 1 (domain INDEX)** — `~/.claude/memory/<domain>/INDEX.md`

Keep it as an overview. Format:
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

Update the count column when adding new entries. Only list highlights (top 3-5 most referenced) — full lists live in category INDEX.md.

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
