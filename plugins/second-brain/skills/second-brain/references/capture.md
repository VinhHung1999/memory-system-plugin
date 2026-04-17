# Capture workflow — note / brain dump / task

Three lightweight capture modes for quick input into brain2/. Distinct from
the heavyweight ingest/query/lint — fire-and-forget, no discussion, no
cross-ref maintenance.

## Routing by phrase

| User phrase contains | Mode | Destination |
|---|---|---|
| "note <title>:", "ghi chú <title>:", "save note" | **Note** | `brain2/wiki/notes/<slug>.md` (one file per note) |
| "brain dump", "dump vào não", "journal:", "journal dump", "ghi lại ý" | **Brain dump** | `brain2/wiki/journal/YYYY-MM-DD.md` (timestamped) |
| "add task", "new task", "done task", "review task", "move task", "làm xong", "kanban ..." | **Kanban** | `brain2/wiki/doing/doing.md` |

**Note vs Brain dump**:
- **Note** = a discrete thought with a topic, worth keeping as its own file. Has a title.
- **Brain dump** = stream-of-consciousness, no title, timestamped in today's journal.

When ambiguous, ask — don't guess.

---

## Note mode

**File**: `brain2/wiki/notes/<slug>.md` — one file per note.

### Steps

1. Extract title from user phrasing (e.g., "note về Hermes bytecode:" → slug `hermes-bytecode`).
   If title unclear → ask.
2. Check if `brain2/wiki/notes/<slug>.md` exists.
   - Missing → create fresh.
   - Exists → append to existing (respect updated frontmatter).
3. Frontmatter on create:
   ```markdown
   ---
   type: note
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   tags: [<infer 1-2 tags from content or ask>]
   ---

   # <Title>

   <user's text>
   ```
4. Preserve wikilinks.
5. Confirm: path + title.

### Example

User: "note về Hermes bytecode: Hermes pre-compiles JS to bytecode at build time — reduces startup by ~30%. Key flag: `hermes.enabled=true` in gradle."

Action: create `brain2/wiki/notes/hermes-bytecode.md`:
```markdown
---
type: note
created: 2026-04-16
updated: 2026-04-16
tags: [react-native, hermes, performance]
---

# Hermes bytecode

Hermes pre-compiles JS to bytecode at build time — reduces startup by ~30%. Key flag: `hermes.enabled=true` in gradle.
```

Confirm: "Created `notes/hermes-bytecode.md` — 'Hermes bytecode'."

### Graduation

A note stays simple. When it **grows** enough to deserve cross-references and full schema (multiple sources, relationships to other pages), **graduate** it to a proper wiki page via `/second-brain ingest` or manual move to the right life-area folder. Suggest graduation when you notice a note:
- accumulates 5+ paragraphs, or
- gets wikilinked from 3+ other pages, or
- user says "this is bigger than a note now".

---

## Brain dump mode

**File**: `brain2/wiki/journal/YYYY-MM-DD.md` (today's date always).

### Steps

1. Compute today's path.
2. If file doesn't exist, create with frontmatter:
   ```markdown
   ---
   type: journal
   created: YYYY-MM-DD
   ---

   # YYYY-MM-DD
   ```
3. Append a timestamped section (24h, from system context):
   ```markdown

   ## HH:MM
   <user's text verbatim>
   ```
4. Preserve wikilinks.
5. Confirm: path + first ~80 chars of what was appended.

### Example

User: "dump vào não: hôm nay thấy MF phụ thuộc JSI nhiều hơn tôi nghĩ — [[module-federation]] đi cùng [[new-architecture]]"

Append to `brain2/wiki/journal/2026-04-16.md`:
```markdown

## 15:42
hôm nay thấy MF phụ thuộc JSI nhiều hơn tôi nghĩ — [[module-federation]] đi cùng [[new-architecture]]
```

Confirm: "Appended to journal/2026-04-16.md at 15:42."

---

## Kanban mode

**File**: `brain2/wiki/doing/doing.md`.

**Columns**: `## Todo`, `## Doing`, `## Review`, `## Done`, `## Archive`.

**Task format**: `- [ ] [tag] <text>` where tag is `[work]` or `[life]`.

### Hard rule — tag is mandatory

Every new task MUST have `[work]` or `[life]` prefix. If user doesn't include it → **ask**. Don't default or guess.

### Actions

#### Add task

User: `"add task [work] làm slides cho demo"` or `"new task [life] đi cắt tóc"`.

Steps:
1. Read `doing.md`.
2. Default target column = `Todo`. Respect explicit "to Doing" / "to Review" etc.
3. Find column header; insert new task as the last item under that section (before the next `##` heading or the `***` separator).
4. **Preserve** kanban-plugin frontmatter + trailing `%% kanban:settings %%` block.
5. Write. Confirm: "Added to <column>: `[tag] <text>`".

#### Move task

User: `"move task <substring> to Doing"` or `"review task <substring>"`.

Steps:
1. Read.
2. Find line matching substring (case-insensitive). 0 or 2+ matches → ask.
3. Remove from current column; insert at end of target column.
4. Write. Confirm: "Moved '<task>' from <old> to <new>".

#### Done task

User: `"done task <substring>"` / `"làm xong <substring>"` → move to `Done`. Don't tick `[x]` (user's kanban preserves `[ ]` across all columns).

---

## After every write — auto-sync qmd

After any capture (note / brain dump / task) succeeds, run:

```bash
qmd update 2>/dev/null || true
```

Silent-fail if qmd isn't configured. Cheap (~instant, local). Keeps BM25 search fresh so the next `qmd search` sees the new content.

Skip `qmd embed` here — embeddings cost OpenAI API calls; batch those via the cron (every 30-60 min) rather than per-capture. Only run `qmd embed` if the user explicitly asks or if they're about to run a semantic search.

## Boundary — what NOT to do

This is **capture**, not curation. Don't:

- Cross-link the note/task into entity/concept/synthesis pages (unless the user explicitly links inline).
- Update MOCs (notes folder's `notes.md` can be left; it'll be regenerated by Dataview if used).
- Run broken-link audit.
- Append to `log.md` (capture ops aren't wiki-level operations worth logging).

If the user asks for more (e.g., "note this and update [[app-platform]] too"): switch modes — "That's a `/second-brain ingest`. Want me to promote this to a full ingest?"

---

## Edge cases

- **Vault not initialized** (`brain2/wiki/` missing): stop; tell user to run `bash <skill-dir>/scripts/init.sh`.
- **Missing folders** (`notes/`, `journal/`, or `doing/` doesn't exist): `mkdir -p` and proceed for notes/journal; for doing.md, don't fabricate — tell user to run `/second-brain init` or create via template.
- **Note slug collision**: if `wiki/notes/<slug>.md` exists and the new content is unrelated → pick a more specific slug (`hermes-bytecode-2`) or ask.
- **Task without tag**: ask "work or life?" before writing.
- **Ambiguous phrasing** (note vs journal): ask the user which.

---

## What "good capture" looks like

- **Note**: topical file, clear title, frontmatter, 1-2 sensible tags, wikilinks preserved.
- **Brain dump**: in today's journal file, timestamped, wikilinks preserved, <2s ceremony.
- **Kanban**: in right column, `[work]`/`[life]` tagged, doesn't break rendering.
- Confirmation with path + snippet.
- Zero cross-contamination with the ingest/query/lint layer.
