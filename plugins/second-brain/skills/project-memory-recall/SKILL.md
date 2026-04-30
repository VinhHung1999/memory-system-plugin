---
name: project-memory-recall
description: Retrieve role-partitioned project memory from Hung's brain2 wiki at `wiki/projects/<project>/memory/<role>.md`. Generic across the 4-role tmux team — pass `role=<po|dev|qc|cmo>` to scope the lookup, or `role=*` for cross-role view. Use when an agent (PO/DEV/QC/CMO) needs context on a project they've worked on, when a stakeholder mentions a known project name, when grooming for precedent, or when peeking at another role's notes ("what did DEV say about X in menh-viet"). Smart-routes between direct read (project name), qmd semantic search (concepts), and grep (exact keywords). Skip for brand-new projects with no memory yet.
---

## MANDATORY: Use Task Tool (Sub-Agent, Background)

**NEVER execute directly in main context.** Use Task tool with:
- `subagent_type: "general-purpose"`
- `run_in_background: true`

Background sub-agent lets the search run in parallel without blocking the
calling role's main conversation.

---

## Required input: role

The skill is role-aware. The caller MUST tell the skill which role's memory to
default to. Three modes:

| Mode | Form | Behavior |
|---|---|---|
| **Default (own role)** | `role=po` / `role=dev` / `role=qc` / `role=cmo` | Search both `memory/<role>.md` + `memory/shared.md` of matching projects. Rerank own-role hits above shared hits. This is the 99% case. |
| **Cross-role peek** | `role=<other-role>` (different from caller) | Search only that role's `memory/<role>.md`. Use when PO wants DEV's view, DEV wants QC's flaky-test notes, etc. |
| **Multi-role union** | `role=*` | Read all `memory/*.md` files (rare, "tell me everything about project X"). |

**Convention:** when invoked from a role agent (e.g. the `po` subagent), the
agent prepends its own role. Example:

```
/second-brain:project-memory-recall role=po menh-viet stakeholder shifts
```

If `role=` is missing AND the caller is not a role agent, default to
`role=*` (broad search) rather than guessing.

**Why `shared.md` is auto-included for own-role queries:** `memory/shared.md`
holds cross-cutting team notes (deploy quirks, conventions, technical
constraints). These often inform product/role decisions. Including them by
default means the caller doesn't have to remember a separate flag. Hits from
`shared.md` are labeled `[shared]` in the output so the source is clear.

---

## When to recall

**Recall when:**
- Stakeholder/user mentions a project by name
- Writing/grooming work for a project that has prior history
- Making a decision where past projects might offer precedent
- Peeking at another role's notes on the same project
- User explicitly asks ("--recall", "kiểm tra lại memory", "check past notes")

**Skip when:**
- Brand-new project (no memory exists — say so, then store after the task)
- Trivial ops (rephrase, label rename, format)
- Question answerable from current sprint/backlog alone

---

## Storage layout (what you're searching)

```
${SECOND_BRAIN_VAULT:-~/Documents/Notes/HungVault/HungVault/brain2}/
└── wiki/projects/                    # CURATED — only search target
    ├── projects.md                   # master index of all projects
    └── <project>/                    # one folder per project
        ├── <project>.md              # OVERVIEW (every role reads on join)
        ├── docs/                     # shared technical docs
        └── memory/                   # role-partitioned memory
            ├── shared.md             # cross-cutting team notes
            ├── po.md                 # PO: stakeholder, product trade-offs
            ├── dev.md                # DEV: bugs, gotchas, architecture decisions
            ├── qc.md                 # QC: flaky tests, edge cases, regressions
            └── cmo.md                # CMO: campaign experiments, channel ROI, positioning
```

**Search wiki ONLY — never `raw/`.** The `raw/` inbox is unreviewed staging.
The qmd `brain2` collection is rooted at `brain2/wiki/`, so paths like
`projects/<X>/memory/<role>.md` already mean wiki.

---

## Query routing — pick the strategy by query shape

Combine the `role=` parameter with the query shape:

| Query shape | Example | Strategy |
|---|---|---|
| **Direct project name** + own role | `role=po menh-viet` | Read `<project>/<project>.md` + `<project>/memory/po.md` + `<project>/memory/shared.md` |
| **Direct project name** + cross-role peek | `role=dev menh-viet flaky tests` | Read `<project>/memory/dev.md`, scope to query terms |
| **Concept across projects** + own role | `role=po stakeholder keeps shifting scope` | qmd vsearch across `projects/**/memory/{po,shared}.md` (rerank po hits first) |
| **Exact keyword across projects** + own role | `role=dev Soniox STT` | grep `projects/*/memory/{dev,shared}.md` |
| **Multi-role view of one project** | `role=* menh-viet` | Read `<project>/<project>.md` + all `<project>/memory/*.md` |

---

## Search strategy

qmd is the local search engine. Three tools by cost:

| Tool | Speed | Use for |
|---|---|---|
| `qmd search "..."` | ~30 ms | full-text keyword (BM25, no LLM) |
| `qmd vsearch "..."` | ~2 s | pure vector similarity (concept) |
| `qmd query "..."` | ~10 s | expansion + reranking (hardest queries) |

Always scope with `-c brain2`. Filter results to paths under `projects/`.
Further filter by `<role>.md` or `shared.md` based on the `role=` parameter.

Check availability:

```bash
command -v qmd >/dev/null 2>&1 && qmd status >/dev/null 2>&1
```

If unavailable, fall back to grep.

### grep fallback

```bash
VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
PROJECTS="$VAULT/wiki/projects"
ROLE="<role>"  # po | dev | qc | cmo

# Direct project lookup (own-role mode — read all 3 files):
cat "$PROJECTS/<project>/<project>.md"
cat "$PROJECTS/<project>/memory/$ROLE.md"
cat "$PROJECTS/<project>/memory/shared.md"

# Cross-role peek (explicit other role, no shared.md auto-include):
cat "$PROJECTS/<project>/memory/<other-role>.md"

# Search own-role + shared across all projects:
grep -r -l "keyword" "$PROJECTS"/*/memory/{$ROLE,shared}.md

# Multi-role union (role=*):
grep -r -l "keyword" "$PROJECTS"/*/memory/

# NEVER widen to $VAULT/raw/.
```

---

## Workflow

### 1. Parse the input

Extract:
- `role=` value (default `*` if omitted AND caller is not a role agent)
- Project name(s) if any
- Topic/keyword/concept

### 2. Direct-name queries — read first, search second

If a project name is in the query, just Read the file(s). No search needed.
Always include both:
- `<project>.md` (overview — sets context)
- `<project>/memory/<role>.md` (the role's memory of that project)

For `role=*`, read all `memory/*.md` in that project's memory folder.

### 3. Concept / keyword queries — qmd preferred

1. `qmd search -c brain2 "<keyword>"` for concrete terms.
2. Escalate to `qmd vsearch -c brain2 "<concept>"` for fuzzy/semantic.
3. `qmd query -c brain2 "..."` for hardest queries (slowest, best recall).
4. Filter results to `projects/**/memory/<role>.md` (or `shared.md` / all).
5. `qmd get <path>` to read full content.

### 4. Read the top matches

Aim for 3–5 hits. For each, look for:
- Decisions with rationale (why we chose X over Y)
- Stakeholder / contributor patterns
- Recurring blockers, scope shifts, technical surprises
- Test/QC patterns (if `role=qc`)

### 5. Present results

Return concise summary (under 200 words). Rerank own-role hits above shared
hits. Label `[shared]` on hits from `memory/shared.md` so the source is clear.

```
## Project Memory Recall

**Role scope:** <role>
**Strategy:** <direct read | qmd vsearch | grep | cross-role peek>

**Findings:**
1. <project> · po.md           — <one-line takeaway>
2. <project> · po.md           — <one-line takeaway>
3. <project> · shared.md [shared] — <one-line takeaway>

**For your decision:** <one-line synthesis of how this applies>.
```

If nothing relevant: "No project memory hits for `<query>` (role=<role>). Worth
storing new insight after this task wraps up."

---

## Examples

### From PO agent
```
/second-brain:project-memory-recall role=po hexarian past stakeholder feedback
```
→ Reads `hexarian/hexarian.md` + `hexarian/memory/po.md`.

### Cross-role peek
```
/second-brain:project-memory-recall role=dev menh-viet API design gotchas
```
→ Reads `menh-viet/memory/dev.md`, surfaces only API-related notes.

### Multi-role overview
```
/second-brain:project-memory-recall role=* love-scrum
```
→ Reads `love-scrum/love-scrum.md` + every `memory/*.md` in that folder.

### Concept search (PO across projects)
```
/second-brain:project-memory-recall role=po stakeholders who keep adding scope mid-sprint
```
→ qmd vsearch across all `projects/*/memory/po.md`.
