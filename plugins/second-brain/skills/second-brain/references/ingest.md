# Ingest workflow

Read this in full before processing any source. Ingest is the heaviest
operation — a single source can touch many wiki pages. Doing it sloppily
creates orphans, contradictions, and a wiki that the next ingest has to
fight. Doing it well makes every future query cheaper.

## Inputs you may receive

The user invokes `/second-brain ingest <thing>` where `<thing>` can be:

- **A local file path** (PDF, .md, .txt, .epub, image, audio transcript)
- **A URL** (article, blog post, paper, video page)
- **`-`** (read pasted text from the conversation that follows)
- **A folder** (batch ingest — confirm approach with user first)
- **An image path** (screenshots, photos with embedded text, diagrams)

If the form is ambiguous, ask.

## Step-by-step

### 1. Confirm vault is initialized

```bash
ls $SECOND_BRAIN_VAULT/wiki/wiki.md
```

If missing, run `bash <skill-dir>/scripts/init.sh` first.

### 2. Read the wiki router + the source

In parallel:

- `Read brain2/wiki/wiki.md` — the top-level MOC. From there, identify
  which life-area folder the source belongs to (work / code-knowledge /
  projects / …) and read that area's MOC too.
- Read the source itself (`Read` for files, `WebFetch` for URLs,
  view for images).

For URLs with substantial images (diagrams, charts) that matter to
meaning: download to `brain2/raw/assets/` and view them — text-only
ingest of an image-heavy article leaves holes.

For PDFs > 10 pages: use the `pages` parameter on Read; don't load 200
pages into context when 20 will do.

### 3. Stash the raw source

If the source is a local file outside `brain2/`, copy it to `brain2/raw/`.
If it's a URL, save the fetched markdown to `brain2/raw/<slug>.md`.

```bash
cp /path/to/source.pdf $SECOND_BRAIN_VAULT/raw/
```

Never modify a file once it's in `raw/` — immutable record.

### 4. Discuss key takeaways with the user

This is what distinguishes the LLM Wiki from RAG. Don't silently
summarize. Surface 3-7 key takeaways and ask:

- Which matter most for *their* second brain (it's personal)?
- Any claims surprising, controversial, or contradicting what they
  already believe?
- Which entities/concepts are new vs. already in the wiki (check the
  relevant area's MOC)?
- Embrace, challenge, or just note the source's framing?

Keep it tight — a few targeted questions. Goal is to surface what to
**emphasize** when filing.

**For user-authored sources (Notion exports, journals):** treat as a
review/refresh session ("ôn lại"). Ask comprehension questions ("does
this still hold? would you explain it differently now?") before filing —
the user wants their evolving view captured, not a literal copy of the
old notes.

### 5. Plan the writes (decide placement)

After discussion, tell the user concretely which pages you'll create/update.

**Placement decision — where does a page go?**

Work through this tree:

1. **Is it MoMo-specific OR transferable?**
   - MoMo-specific (only makes sense in the MoMo context): `work/momo/…`
   - Transferable (applies beyond this company): `code-knowledge/…`

2. **Within `work/momo/`, which sub-domain?**
   - App Platform internals (BridgeMode, MaxAPI, mini-app load) → `app-platform/…`
   - Trail tracking → `app-platform/tracking/`
   - A topic mentioned in the matrix but not ingested → create new subfolder
     (`app-platform/kmm/`, `app-platform/tracking/`, etc.) following the
     folder-note pattern.

3. **Within `code-knowledge/`, which platform/category?**
   - React Native specifics → `mobile/react-native/`
   - Kotlin concurrency → `mobile/kotlin/`
   - Cross-cutting (test automation, build tooling, etc.) → top-level
     category like `automation/`, `devops/` (create when first page arrives)

4. **Decide which TYPE the page is.**
   - `source` — the source itself (what Notion/URL/book said)
   - `entity` — a named thing (product, person, company)
   - `concept` — an idea, pattern, framework
   - `synthesis` — cross-cutting analysis (often from queries)
   - `index` — folder-note MOC (one per folder)

5. **Check for gom opportunities.** If your source would produce
   multiple pages that all describe the same thing, MERGE them into
   one page with sections. Don't fragment unnecessarily (see
   `execute-bundle.md` — 5 merged concepts about Phase 2 of mini-app
   load).

**Typical write plan:**

- **Create** the source page (or a merged explainer page) in the target
  folder.
- **Create or update** entity/concept pages (same folder or a sibling
  `entity`-style folder) for significant entities + concepts.
- **Update the folder-note MOC** of whichever area got new pages —
  add wikilinks to the new pages under the appropriate section.
- **Update `wiki/overview.md`** only if the source materially changes
  Hung's identity/focus.
- **Update parent folder-notes** up the chain if new sub-folders were
  introduced.
- **Append to `brain2/log.md`**.

Show the user this plan and let them adjust before writing.

### 6. Write pages following templates

Templates + frontmatter shapes in `references/conventions.md` and
`brain2/CLAUDE.md`. Hard rules:

- Every new page has full frontmatter with `created` + `updated` = today
  + type-specific fields.
- Every page mentions its sources via wikilinks.
- **Bare wikilinks only**: `[[carl-jung]]`, not `[[entities/carl-jung]]`.
- Each fact lives in one canonical place; everywhere else links.
- No `## Parent` sections — Obsidian Backlinks handle upward navigation.
- Use a `## Related` section at the end of content pages to list
  cross-refs (peers, not parents).

Updating an existing page:
- Read whole page first.
- Add to existing sections; don't create parallel ones with similar names.
- Contradictions: add `## Open questions` or `## Contradictions` section —
  don't silently overwrite.
- Bump `updated:` to today.

### 7. Update folder MOCs

For every new page: its containing folder's MOC needs a line added under
the appropriate section. If a new sub-folder was created, also update
the parent folder's MOC to link to the new subfolder's MOC.

### 8. Append the log

```markdown
## [YYYY-MM-DD] ingest | <Source title>
Created [[<slug>]]. Updated [[...]], [[...]]. Added new page [[...]].
Notable: <one-line user-facing summary of what changed — this is what
the user reads later to remember "what did this source teach me">.
```

### 9. Verify + re-index qmd + confirm with user

Run the broken-links check:

```bash
bash <skill-dir>/scripts/check-broken-links.sh
```

Re-index qmd so search reflects the new pages:

```bash
qmd update 2>/dev/null || true      # BM25 — always safe, cheap
qmd embed 2>/dev/null || true       # vector — embed only new/changed files
```

(Silent-fail if qmd not configured. `qmd update` is cheap. `qmd embed`
costs OpenAI API calls but only processes files whose content hash
changed — new/edited pages only.)

Show the user a brief summary:
- Pages created (with wikilinks)
- Pages updated
- Any contradictions / open questions flagged
- Suggested next ingests if the source pointed to adjacent material

Then stop.

## Edge cases

### Conversational ingest

Ingest the current conversation as a source:
- Treat as `source_kind: conversation`.
- Save excerpt to `brain2/raw/conversations/<date>-<topic>.md`.
- Source page is a summary, not the raw transcript.
- Carefully attribute: "what the user said" vs. "what I synthesized"
  vs. "what we agreed on".

### Image-heavy sources

Read text first, then view key images separately. In source page, embed
with Obsidian syntax: `![[assets/image-name.png]]` (after downloading
to `raw/assets/`). Note: `raw/` is Obsidian-ignored, so image embeds may
not render through ignore rules — consider copying important diagrams
to `wiki/<area>/_assets/` if inline render is critical.

### Contradictions

Feature, not bug. When a new source contradicts the wiki:
1. Add `## Open questions` or `## Contradictions` section to affected
   entity/concept/synthesis page (not to the source page).
2. State both sides with citations.
3. Surface in the ingest summary.

### Batch ingest (folder)

Confirm count + ask: "one-by-one with discussion, or all at once?"
Default to one-by-one unless user explicitly wants batch. For batch:
serial processing, one roll-up log entry at the end, individual source
pages for each file.

## What "good ingest" looks like

After ingest, a user can:
- Open the source page and learn what the source is + why it mattered in 90s.
- Click any wikilink to a relevant entity/concept.
- Open `brain2/log.md` and see the ingest in chronological context.
- Run a query a week later and have the wiki naturally surface this
  source via the pages it touched.
- Run `check-broken-links.sh` with clean output.

If those don't hold, the ingest was too shallow.
