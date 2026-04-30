---
name: memory-recall
description: Retrieve universal cross-project lessons from Hung's brain2 wiki at `wiki/code-knowledge/`. Use before non-trivial tasks (unclear bugs, design choices, unfamiliar domains) or when user says "--recall". Uses qmd for semantic/keyword search, falls back to grep. Skip for trivial tasks — recall is expensive. For project-specific memory, use `/second-brain:project-memory-recall` instead.
---

## MANDATORY: Use Task Tool (Sub-Agent, Background)

**NEVER execute directly in main context.** Use Task tool with:
- `subagent_type: "general-purpose"`
- `run_in_background: true`

Background sub-agent lets the search happen in parallel without blocking the main conversation.

---

## When to recall (be strict — qmd search is ~2s, don't burn it on trivia)

**Recall when:**
- Debugging a bug whose cause isn't obvious
- Making an architecture/library decision
- Performance tuning, optimization
- Working in an unfamiliar domain (first time touching blockchain, IAP, ffmpeg, etc.)
- User explicitly asks to check memory (`--recall`, "do we have notes on X")

**Skip when:**
- Trivial ops: typos, format, build commands, git status, file listing
- Question answerable in 30 seconds from general knowledge
- Short lookups where the answer is in the current repo

---

## Storage layout (what you're searching)

```
${SECOND_BRAIN_VAULT:-~/Documents/Notes/HungVault/HungVault/brain2}/
└── wiki/code-knowledge/              # CURATED — only search target
    ├── code-knowledge.md             # top-level folder-note (MOC)
    └── <domain>/                     # frontend, backend, mobile, automation, claude-code, universal
        ├── <domain>.md               # per-domain MOC
        ├── bugs/
        │   └── <insight>.md
        └── patterns/
            └── <insight>.md
```

**Search wiki ONLY — never `raw/`.** The `raw/` inbox is staging-only; entries there are unreviewed and may be wrong, contradictory, or duplicates. Hung promotes valuable items into `wiki/` manually. The qmd `brain2` collection is configured against `brain2/wiki/` precisely so recall never surfaces raw entries. Even if grep is the fallback, restrict to `wiki/code-knowledge/`.

---

## Search strategy — prefer qmd, fall back to grep

qmd is Hung's local search engine over the brain2 collection. Three tools, by cost:

| Tool | Speed | Use for |
|---|---|---|
| `qmd search "..."` | ~30 ms | full-text keyword (BM25, no LLM) |
| `qmd vsearch "..."` | ~2 s | pure vector similarity (concept / meaning-based) |
| `qmd query "..."` | ~10 s | recommended — query expansion + reranking, best recall on hard queries |

Always scope to the brain2 collection with `-c brain2` so wiki hits aren't drowned out by other collections.

Check availability first:

```bash
command -v qmd >/dev/null 2>&1 && qmd status >/dev/null 2>&1
```

If qmd is available, use it. Otherwise fall back to grep.

### qmd workflow

1. Start with `qmd search -c brain2 "..."` for a concrete keyword (error message, function name, library name).
2. If zero or low-score results, escalate to `qmd vsearch -c brain2 "..."` for the conceptual version of the query.
3. Use `qmd query -c brain2 "..."` for hard queries where you want expansion + reranking — it's the highest-quality option but slowest.
4. Filter hits to `code-knowledge/` paths (the brain2 collection is rooted at `brain2/wiki/`, so `code-knowledge/...` already means wiki/code-knowledge — ignore `work/`, `notes/`, `journal/`, etc. unless the user asks).
5. Use `qmd get <path>` or `qmd multi-get "code-knowledge/<domain>/**/*.md"` to read full matches.

### grep fallback

```bash
VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
WIKI_CK="$VAULT/wiki/code-knowledge"

# Start narrow (one domain) if the task is clearly scoped
grep -r -l "keyword" "$WIKI_CK/<domain>/"

# Widen to all domains if no hits
grep -r -l "keyword" "$WIKI_CK/"

# Do NOT widen to $VAULT/raw/ — raw/ is unreviewed staging; entries there
# may be wrong or duplicate. If wiki returns nothing, report "no relevant
# memories found" rather than scraping the inbox.
```

---

## Workflow

### 1. Identify scope

Pick 1–2 likely domains from the task context. Keywords → domains:

| Task mentions | Domain |
|---|---|
| React, Next.js, Tailwind, Zustand, browser | `frontend` |
| API, auth, JWT, Postgres, server | `backend` |
| React Native, Expo, IAP, Swift, Kotlin | `mobile` |
| Appium, Playwright, test automation | `automation` |
| Claude Code, plugin, skill, MCP, hook | `claude-code` |
| Bash, shell, git, CLI, cross-platform | `universal` |

If genuinely cross-cutting, include `universal/`.

### 2. Read the domain MOC first

```bash
cat "$WIKI_CK/<domain>/<domain>.md"
```

The domain folder-note lists the bugs/ and patterns/ entries with one-line summaries. Often this alone answers the query — no need to read individual files.

### 3. Search

Use qmd per the "Search strategy" section. Aim for 3–5 top hits.

### 4. Read the top matches

Read full content of the top 3–5 files. Look for:
- Past decisions that constrain the current task
- Known failures in the same area
- Patterns/conventions already established
- Multi-step procedures that apply

### 5. Present results

Return a concise summary (under 200 words) to the main conversation. Include:
- Title + path of each relevant memory
- One-line takeaway per memory
- Your judgment on relevance (is this a direct fit, adjacent context, or loosely related)

**Don't force-fit patterns** — if nothing is relevant, say so. Missing knowledge is a signal to store a new insight once the task is done.

---

## If no results found

1. Broaden keywords (try synonyms, drop qualifiers)
2. Switch to `qmd vsearch` (or `qmd query` for the slowest/highest-recall option) if you only used `qmd search`
3. Search `universal/` if you only searched a specific domain
4. Report "No relevant memories found" — not every task has prior learnings, and that's fine. Do NOT fall back to `raw/`; it's unreviewed staging.

---

## Output format

```
## Recall for: "<task summary>"

Searched: qmd vsearch -c brain2 "<query>" in wiki/code-knowledge/<domain>/

Top matches:
1. **<title>** (<path>)
   <one-line takeaway>
2. ...

Relevance: <direct fit | adjacent | loose>. <optional one-line of judgment on how it applies>.
```
