---
name: coder-memory-store
description: Stage universal coding lessons into Hung's brain2 wiki inbox at `raw/code-knowledge/`. Auto-invokes after difficult tasks with broadly-applicable insights (non-obvious bugs, surprising patterns, hard-won fixes). Trigger with "--store" or when user expresses frustration. Skip for trivial or project-specific patterns (built-in auto memory handles those).
---

## MANDATORY: Use Task Tool (Sub-Agent, Background)

**NEVER execute directly in main context.** Use Task tool with:
- `subagent_type: "general-purpose"`
- `run_in_background: true`

Background sub-agent keeps the main conversation flowing while the write happens. You'll be notified when it completes.

**Permissions**: The plugin pre-grants Write/Edit/Read/Bash on the vault path. If you see a permission error, check `settings.json` under `permissions.allow`.

---

## Core principle — inbox, not archive

This skill **stages** insights into a staging inbox. It does **NOT** file them into the curated wiki. Hung promotes raw inbox items into `wiki/code-knowledge/` manually when he has time to review them.

**You write to:** `${SECOND_BRAIN_VAULT:-~/Documents/Notes/HungVault/HungVault/brain2}/raw/code-knowledge/<domain>/<bugs|patterns>/<filename>.md`

**You never touch:** `wiki/code-knowledge/` — that's Hung's curated space.

Because the raw inbox is staging, don't over-engineer the write:
- Don't rebuild INDEX.md files
- Don't merge/dedupe against the wiki
- Don't agonize over domain classification — if unsure, default to `universal/` and let Hung reclassify during promotion

---

## When NOT to Store

Skip if any of the following is true:
- **Trivial** — typo fix, format cleanup, simple build command
- **Google-able in 30 seconds** — basic language syntax, well-documented library usage
- **Project-specific** — specific API endpoint names, private business logic, session-bound state (built-in auto memory handles these)
- **Already written** — if grep finds similar wording in `raw/code-knowledge/` or `wiki/code-knowledge/`, skip or merge rather than duplicate

Only store hard-won lessons: non-obvious bugs, surprising patterns, cross-project failures, fixes that took real debugging.

---

## Storage layout

```
${SECOND_BRAIN_VAULT}/raw/code-knowledge/
├── <domain>/                   e.g., frontend, backend, mobile, automation, claude-code, universal
│   ├── bugs/
│   │   └── <insight>.md        a specific failure + fix
│   └── patterns/
│       └── <insight>.md        a recurring best practice, decision, or pattern
```

**Only two subfolders per domain: `bugs/` and `patterns/`.** Finer classification (`decision` vs `pattern` vs `lesson` vs `structure` vs `library`) goes in the `category:` frontmatter field, not a folder. This keeps the inbox shallow so Hung can promote quickly.

**Picking the domain:**

| Content | Domain |
|---|---|
| React / Next.js / Zustand / browser / DOM | `frontend` |
| Node / Python / DB / auth / API server | `backend` |
| React Native / Expo / Swift / Kotlin / IAP | `mobile` |
| QA / Appium / Playwright / test automation / Selenium | `automation` |
| Claude Code plugins / skills / MCP / hooks | `claude-code` |
| Bash / git / shell / cross-platform tooling | `universal` |

If nothing fits cleanly → `universal/` and let Hung reclassify.

---

## Workflow

### 1. Extract insights

Analyze the recent conversation for 0–3 insights (usually 0–1).

**ALL must be true:**
- **Non-obvious** — not standard practice (e.g., `useCallback` stale-closure trap)
- **Universal** — applies beyond one project (e.g., exponential backoff with jitter)
- **Actionable** — concrete guidance, not vague ("be careful with X")
- **Valuable** — would save future-Hung real debugging time

### 2. Check for duplicates

```bash
VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
grep -r -l "keyword" "$VAULT/raw/code-knowledge/<domain>/" 2>/dev/null
grep -r -l "keyword" "$VAULT/wiki/code-knowledge/<domain>/" 2>/dev/null
```

- **Near-duplicate in raw** → merge into existing inbox file
- **Near-duplicate in wiki** → skip entirely (Hung already curated it)
- **Related but distinct** → new file, link the related one in the Related section
- **Novel** → create new file

### 3. Write file

Path: `${SECOND_BRAIN_VAULT}/raw/code-knowledge/<domain>/<bugs|patterns>/<slug>.md`

Filename slug: kebab-case, descriptive (`usecallback-stale-closure.md`, `sse-crlf-lf-parsing.md`).

**Frontmatter schema (match the wiki's B++ convention):**

```yaml
---
type: source | entity | concept | synthesis
category: pattern | decision | lesson | structure | library | bug
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - Display Name
tags: [domain, topic1, topic2]
status: inbox
---
```

- `type:` — usually `concept` for patterns, `synthesis` for multi-source lessons
- `category:` — finer-grain than folder; `bug` for `bugs/` files, one of the others for `patterns/` files
- `status: inbox` — marks this as unpromoted (Hung greps this when curating)

**Body:**

```markdown
# <Title>

## Description
One-sentence summary of the lesson.

## Content
3–5 sentences: what happened, what was tried, what worked/failed, the key lesson. Be specific — include error messages, tool versions, or file paths if they matter.

## Related
- Links to related wiki pages or prior inbox files (bare wikilinks: `[[page-slug]]`).
```

### 4. Sync qmd index (if available)

```bash
qmd update brain2 >/dev/null 2>&1 || true
```

Silent — don't fail the write if qmd isn't installed.

### 5. Report

One line back to the main conversation: `Stored to raw/code-knowledge/<domain>/<bugs|patterns>/<filename>.md`. Nothing more.

---

## Frustration = strong signal

When Hung expresses frustration (fuck, shit, wtf, "không hiểu sao", "why is this broken"), that's a critical learning moment:
1. Store with full failure context (error, what was tried, what fixed it)
2. Add `#failure #strong-signal` to `tags:`
3. Prioritize the write even if you'd otherwise skip

---

## Examples

**Good — backend/bugs/jose-jwt-jti.md:**

```markdown
---
type: concept
category: bug
created: 2026-04-16
updated: 2026-04-16
aliases:
  - JOSE JWT jti
tags: [backend, auth, jwt, bug]
status: inbox
---

# JOSE JWT: same iat + same payload = identical tokens

## Description
JOSE `SignJWT` with identical payloads and same-second `iat` produces byte-identical tokens, breaking revocation by token.

## Content
Signed two tokens in the same process tick with same claims — got duplicate strings, which broke our "revoke by token string" logic. Spec-compliant but surprising. Fix: always set `jti: randomUUID()` so tokens are unique even with identical payload + iat.

## Related
- [[axios-zustand-auth-pattern]]
```

**Bad — too vague:**

```markdown
# Fixed JWT bug
JWT was broken. Added jti.
```
