# Query workflow

Read this in full before answering. Queries are different from ingests —
mostly read, occasionally write. The write part matters: a good query
answer should be **filed back** as a synthesis page so the next query
benefits from this work.

## Inputs

User invokes `/second-brain query <question>` or asks a question you
recognize as a wiki query (phrases like "what does my brain say about X",
"synthesize from my notes", "compare X and Y in my wiki").

Question shapes:
- **Factual**: "What sources do I have about Jung?"
- **Synthetic**: "What does my wiki say about meaning-making?"
- **Comparative**: "How do X and Y differ in my notes?"
- **Reflective**: "What have I learned in the last month?"
- **Exploratory**: "What concepts are connected to individuation?"

## Step-by-step

### 1. Pick the right READ strategy

Two paths, pick by query shape:

**MOC traversal** (default for hierarchy-aware questions):
```
Read brain2/wiki/wiki.md
```
Start from top-level folder-note → drill into life-area MOC → leaf pages.
Best for: "what's my X setup?", "walk me through Y", area-scoped questions.

**qmd search** (primary for keyword / semantic / exploratory):

```bash
# Keyword (exact terms, ~30ms)
qmd search "Hermes bytecode" -c brain2 -n 5

# Semantic (meaning-based, ~2s) — use when user might not know exact vocabulary
qmd vsearch "memory management on low-end devices" -c brain2 -n 5

# Deep (query expansion + rerank, ~10s) — best for hard/vague queries
qmd query "how does the platform handle mini-app failures" -c brain2 -n 5
```

Or via MCP tools: `mcp__qmd__search`, `mcp__qmd__vector_search`, `mcp__qmd__deep_search`.
Collection name: `brain2`. Output includes docid, score, snippet — use snippets to pick candidates, then `Read` the full file(s).

**Graph/wikilink exploration** (cross-reference hunting):
```bash
grep -rln "\[\[<slug>\]\]" $SECOND_BRAIN_VAULT/wiki/
```
Best for: "what else connects to concept X?"

**Combining**: a typical non-trivial query = `qmd search` to find candidates → `Read` candidates → MOC check if needed for context → synthesize.

### 2. Read candidate pages

After MOC traversal, read candidate leaf pages in parallel. Follow
wikilinks only when load-bearing for the answer — not exhaustively.

For broad questions, also peek at:
- `brain2/wiki/overview.md` — top-level picture.
- Recent `brain2/log.md` entries — what's been added lately.

### 3. Synthesize with citations

Write the answer. Hard rules:

- **Every claim has a citation** via bare wikilinks:
  `Jung argued individuation is a lifelong process ([[individuation]],
  originally from [[red-book-summary]])`.
- **Distinguish wiki-claims from your reasoning**. If you're connecting
  dots the wiki doesn't explicitly draw, say so: "Combining [[X]] and
  [[Y]] suggests…".
- **Surface gaps**. If the wiki can't fully answer, say what's missing.
- **Surface contradictions**. If two pages disagree, present both.

### 4. Offer to file the answer back

After the answer:

> "Should I file this as a synthesis page so it compounds with the wiki?"

If yes:

- **Placement**: put it in the most relevant life-area folder (e.g., a
  synthesis about MoMo architecture goes in `work/momo/<area>/`; a
  cross-cutting technical analysis goes in `code-knowledge/<area>/`).
- **Filename**: kebab-case from the question: `what-does-jung-say-to-me.md`.
- **Frontmatter**: `type: synthesis`, `question:` = verbatim, `sources:` =
  every source page cited.
- **Body**: lightly edited for permanence (drop conversational phrasing).
- Add a `## What's still uncertain` section for the gaps you surfaced.
- Update the containing folder's MOC — add a line under a `## Syntheses`
  section (or create one).
- Append to `brain2/log.md`:
  ```
  ## [YYYY-MM-DD] query | <question>
  Synthesized from [[...]], [[...]]. Filed as [[<synthesis-slug>]].
  ```

If no: just answer in conversation and stop. Not every query deserves
a permanent page.

### 5. Suggest next moves

If the query exposed gaps ("the wiki doesn't have anything on X"),
recommend specific sources to ingest, or a lint run.

## When to use external search

The wiki is primary. But when info genuinely isn't there:

- Use `WebSearch` / `WebFetch` for fresh facts.
- Use `qmd` MCP server (if available) for full-text search over the
  vault when MOC traversal feels insufficient.
- Clearly separate in the answer: what came from the wiki vs. external.
- External info isn't a wiki claim — if worth keeping, suggest ingesting
  the external source first, then re-querying.

## Output formats

Default to markdown answer in conversation. Offer alternatives when fit:

- **Comparison table** for "compare X and Y".
- **Bullet list** for "list everything I know about X".
- **Mermaid diagram** for "show how concepts connect".
- **Marp slides** for presentation-style output (user has Obsidian Marp plugin).

These are also fileable — a comparison table can become a synthesis.

## Edge cases

### "What did I learn last week?"

Grep recent log:
```bash
grep "^## \[" brain2/log.md | tail -20
```
Then summarize from those, not by re-reading every page.

### "What does my wiki say about <thing not in wiki>?"

Be honest: nothing yet. Suggest sources to ingest, or offer to ingest
the current conversation if the user wants to think out loud.

### Vague queries ("tell me about myself")

Read `brain2/wiki/overview.md` first. If well-maintained, that's the
answer. If stub-y, run a mini-scan of each life-area MOC and surface what
the wiki *does* contain — let the user narrow.

### Queries that are really lint requests

"What's missing in my wiki?" / "Where are the gaps?" — that's lint, not
query. Switch to `references/lint.md`.

## What "good query" looks like

User should:
- Get an answer grounded in their wiki, not generic LLM knowledge.
- See citations they can follow in Obsidian.
- Know what the wiki *doesn't* have, not just what it does.
- Optionally have the answer filed for compounding.

If the answer reads like something you'd say with no wiki at all, you
didn't actually use the wiki. Re-anchor.
