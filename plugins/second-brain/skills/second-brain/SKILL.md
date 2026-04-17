---
name: second-brain
description: |
  Personal LLM-maintained knowledge wiki ("second brain") for a user's
  Obsidian vault. The vault path is read from the $SECOND_BRAIN_VAULT
  environment variable — if unset, stop and tell the user to export it
  (e.g. `export SECOND_BRAIN_VAULT=/path/to/your/vault`).
  Implements the LLM Wiki pattern: instead of doing RAG every query, the LLM
  incrementally compiles knowledge into a persistent, cross-linked wiki of
  markdown files. Use this skill whenever the user invokes /second-brain or
  says any of:
  (1) "ingest", "process", "add to my second brain", "feed into brain2",
      "wiki this" — read a source (file, URL, paste, image, conversation
      excerpt) and integrate it into the wiki.
  (2) "query my second brain", "what does my wiki say about X", "synthesize
      from my notes", "ask my brain2" — answer a question by reading the
      wiki and synthesizing with citations.
  (3) "lint my wiki", "audit my second brain", "wiki health check",
      "find broken links", "find contradictions in my notes" — run a
      health audit.
  (4) "note <title>:", "ghi chú <title>:", "save note" — one discrete
      note file in <vault>/wiki/notes/<slug>.md (has a title, topic-scoped).
  (5) "brain dump", "dump vào não", "journal:", "ghi lại ý" — timestamped
      stream-of-consciousness in <vault>/wiki/journal/YYYY-MM-DD.md.
  (6) "add task", "new task", "done task", "review task", "move task",
      "làm xong", "kanban ..." — add/move kanban tasks in
      <vault>/wiki/doing/doing.md. Tasks require [work] or [life] tag.
  NOTE vs BRAIN DUMP: note = topical file with a title; brain dump =
  messy timestamped entry in today's journal. Different destinations.
  Triggers on phrases "second brain", "brain2", "personal wiki",
  "knowledge wiki", "LLM wiki", "note <title>", "brain dump", "journal",
  "kanban", "task [work|life]", and on /second-brain slash command.
  This skill owns the configured vault exclusively — don't write outside it.
---

# Second Brain — LLM Wiki

A personal knowledge wiki for Hung that compiles, cross-links, and maintains
itself — instead of re-deriving knowledge from raw sources on every query.

**Vault path:** `$SECOND_BRAIN_VAULT`

## Operations (sub-commands)

The user invokes operations as `/second-brain <op> [args]` OR via natural
phrasing that triggers the description above.

| Operation | Purpose                                              | Reference            |
|-----------|------------------------------------------------------|----------------------|
| `init`    | One-time: create brain2/ folders + schema files      | `scripts/init.sh`    |
| `ingest`  | Read a source, extract knowledge, file into wiki     | `references/ingest.md` |
| `query`   | Answer a question from the wiki, with citations      | `references/query.md`  |
| `lint`    | Audit wiki health (broken links, orphans, gaps)      | `references/lint.md`   |
| `note`    | One discrete note file in wiki/notes/<slug>.md       | `references/capture.md` |
| `dump`    | Timestamped brain-dump into today's journal          | `references/capture.md` |
| `task`    | Add / move kanban task (Todo/Doing/Review/Done)      | `references/capture.md` |

**Heavyweight ops** (ingest/query/lint) write/read a lot — ask which if
unclear.
**Lightweight ops** (note/task) are fire-and-forget capture — just do it
when the phrasing is clear. See `references/capture.md`.

## Before you do anything

0. **Resolve the vault path.** Run:
   ```bash
   echo "${SECOND_BRAIN_VAULT:?SECOND_BRAIN_VAULT not set — export it to your vault path, e.g. export SECOND_BRAIN_VAULT=/path/to/your/brain2}"
   ```
   Capture the printed path. Every path below that begins with
   `$SECOND_BRAIN_VAULT` resolves to this value — when calling Read/Write/Edit
   (which need absolute paths), substitute the resolved value.
   If the env var is unset, stop and tell the user to export it.

1. **Confirm vault is initialized.** Run:
   ```bash
   ls "$SECOND_BRAIN_VAULT/wiki/wiki.md" 2>/dev/null
   ```
   If missing, run `bash <skill-dir>/scripts/init.sh` first. The init script
   is idempotent — it never overwrites existing files.

2. **Read `brain2/CLAUDE.md`.** That file is the in-vault schema doc.
   It's a living document the user co-evolves. Trust it over this SKILL.md
   if they ever drift — the vault's CLAUDE.md is the source of truth for
   vault-specific conventions.

3. **Read `brain2/wiki/wiki.md`.** That's the vault's folder-note — the
   router. Always read before ingest/query/lint. It tells you what life-area
   folders exist and links to each of their MOCs. Drill from there.

## Layout — life-area buckets

```
brain2/
├── CLAUDE.md              # in-vault schema
├── log.md                 # chronological activity log
├── raw/                   # immutable source documents — never modify
│   ├── assets/            # images
│   └── notion/            # Notion exports (preserved with hash IDs)
└── wiki/                  # LLM-owned markdown, organized by life area
    ├── wiki.md            # vault router (folder-note)
    ├── overview.md        # identity — "who is Hung"
    ├── work/              # company/job knowledge
    ├── code-knowledge/    # transferable tech
    ├── projects/          # personal/side projects (when accreted)
    ├── research/          # active deep-dive research (when accreted)
    ├── doing/             # current focus / WIP (when accreted)
    └── personal/          # health, goals, journal (when accreted)
```

**Not type-based.** Pages within a life-area folder are flat; the page's
`type:` frontmatter (`source` / `entity` / `concept` / `synthesis` /
`index`) distinguishes them. Nest subfolders by domain (e.g.
`work/momo/app-platform/load-miniapp/`) when content clusters naturally.

**Folder-note pattern.** Every folder has a file **named after the folder**
(`work/work.md`, `momo/momo.md`). It's the folder's MOC and entry point.
Wikilinks are bare slugs: `[[work]]`, `[[momo]]` — never prefixed paths.

**No `## Parent` sections.** Obsidian's Backlinks panel handles upward
navigation. Explicit parent wikilinks create bidirectional arrows that
clutter the graph.

## Conventions (summary)

Full details in `references/conventions.md` and in `brain2/CLAUDE.md`.
Quick reminders:

- **Wikilinks**: bare `[[page-slug]]` (not `[[folder/page-slug]]`).
- **Frontmatter**: every wiki page has YAML with `type`, `created`,
  `updated`, `aliases`, and (for non-sources) `sources`.
- **Language**: English for wiki content, even though Hung converses in
  Vietnamese.
- **No emoji** in wiki content unless the user explicitly asks.
- **`raw/` is off-limits to Obsidian.** `.obsidian/app.json` has
  `userIgnoreFilters: ["brain2/raw/"]` — don't write wikilinks into raw/.

## Search — qmd integration

`brain2/wiki/` is indexed by `qmd` as collection **`brain2`**. For
queries that need keyword / semantic / exploratory search (not
hierarchy-aware MOC traversal), use qmd:

```bash
qmd search "<keywords>" -c brain2     # BM25, fast
qmd vsearch "<meaning>" -c brain2     # semantic
qmd query "<hard question>" -c brain2 # expansion + rerank
```

Or MCP tools: `mcp__qmd__search`, `mcp__qmd__vector_search`, `mcp__qmd__deep_search`.

Ingest re-indexes qmd automatically (`qmd update`). See `references/query.md` for the full decision tree between MOC traversal, qmd, and wikilink grep.

## Why this exists (so you can make judgment calls)

The big idea: knowledge should **compound**. Don't just answer the user
and let the answer disappear into chat history — file insights back into
the wiki so the next question benefits from this one.

You handle bookkeeping (cross-references, summaries, frontmatter, folder
MOC updates, log entries — the parts humans abandon wikis over). The user
handles curating sources, asking good questions, and steering the
synthesis. Be biased toward small, linked, well-typed pages over long
monolithic ones — but also gom pages together when they describe the
same thing (user prefers "nên chung" over fragmentation in MoMo's case).

When the user contradicts an existing wiki claim with a new source,
**don't silently overwrite**. Add a "Contradictions" or "Open questions"
section to the affected page so the disagreement is visible.

**Quality-first, never batch.** User explicitly wants this wiki to stay
high-signal — "tôi không muốn có rác trong đó". Default to one source at
a time with discussion. For sources the user authored (Notion, journals):
treat ingest as a review/refresh session. Batch mode only on explicit
request.

## Dispatch

When you've identified the sub-command, **read the matching reference
file in full** before starting work. The references contain step-by-step
workflows, page templates, and edge-case guidance. Do not improvise the
ingest/query/lint workflow from this SKILL.md alone.
