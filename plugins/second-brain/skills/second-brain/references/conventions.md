# Conventions — brain2 vault

Vault path: `$SECOND_BRAIN_VAULT`

These conventions also live inside the vault as `brain2/CLAUDE.md` so any
LLM opened in that directory inherits them. Keep the two in sync.

## Folder layout — life-area buckets

```
brain2/
├── CLAUDE.md              # in-vault schema (mirror of this file)
├── log.md                 # chronological activity log (append-only)
├── raw/                   # immutable source documents — never edit
│   ├── assets/            # images
│   └── notion/            # Notion exports (preserved with hash IDs)
└── wiki/                  # LLM-owned markdown — organized by LIFE AREA
    ├── wiki.md            # vault router (folder-note)
    ├── overview.md        # identity ("who is Hung")
    ├── work/              # company/job knowledge — MoMo-specific lives here
    ├── code-knowledge/    # generic tech, transferable across jobs
    ├── projects/          # personal/side projects (when accreted)
    ├── research/          # active deep-dive research (when accreted)
    ├── doing/             # current focus / WIP / status (when accreted)
    └── personal/          # health, goals, journal (when accreted)
```

Inside each life-area folder, organize by **domain hierarchy**, not by
file type. Mirror real domain structure (e.g.
`work/momo/app-platform/load-miniapp/`). Files within a folder are flat —
the page's `type:` frontmatter distinguishes them.

**Hard rules:**
- Never modify files in `raw/` once written. They're the immutable record.
- Never write outside `brain2/`. Other HungVault folders (`Research/`,
  `Learning/`, `Projects/`, `Quick-notes/`, `Decisions/`, `my kanban.md`)
  are user-owned and outside this skill's scope.
- One concept = one page. Split when pages get long.
- BUT: gom into one page when multiple "concepts" describe the same
  thing in the same domain (user prefers coherent narratives over
  fragmented nodes). See `load-miniapp/execute-bundle.md` — that's 5
  merged concepts.
- English content, even though user converses in Vietnamese.
- No emoji unless explicitly asked.
- New life-area folders accrete as content arrives — don't pre-create.

## Folder-note pattern

Every folder has a file named after the folder: `work/work.md`,
`work/momo/momo.md`, `work/momo/app-platform/app-platform.md`. This file
is the folder's MOC.

Why this specific name:
- Bare wikilinks resolve cleanly: `[[work]]`, `[[momo]]` — no
  path-qualification needed.
- Unique across the vault — no `[[index]]` ambiguity between siblings.
- Obsidian's "Folder Note Core" community plugin maps folder clicks
  directly to this file — expected by convention.

MOC contents:
- Brief description of the area
- List of child topic-folders (`[[subfolder-name]]`)
- List of leaf pages in this folder
- Open questions / pending gaps

**Do NOT** include a `## Parent` section. Obsidian's Backlinks panel
shows which pages link here; an explicit parent wikilink creates
bidirectional graph arrows that clutter the view.

## File naming

- All filenames are **kebab-case**: `carl-jung.md`, `dynamic-bundle-injection.md`.
- Slug = filename without `.md`. Display name goes in frontmatter
  `aliases:` so `[[carl-jung]]` renders as "Carl Jung" in Obsidian.
- **Bare wikilinks only**: `[[carl-jung]]`, not `[[entities/carl-jung]]`.
  Obsidian resolves across the vault; folder paths are volatile.
- Slugs must be unique vault-wide. If collision seems unavoidable, rename
  one of them more specifically (`carl-jung` → `jung-the-psychologist`).

## Frontmatter

Every wiki page starts with YAML frontmatter. Required fields per type:

### Folder-note / MOC (`type: index`)
```yaml
---
type: index
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - Display Name
tags: [moc, <area>]
---
```

### `overview.md` (top-level identity)
```yaml
---
type: overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - Overview
---
```

### Source page (`type: source`)
```yaml
---
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_kind: article | book | paper | podcast | video | conversation | journal | image
source_path: raw/some-file.pdf      # if local file in raw/
source_url: https://...             # if web source
author: Name
date_published: YYYY-MM-DD
aliases:
  - Display Title
tags: [topic1, topic2]
---
```

### Entity page (`type: entity`)
```yaml
---
type: entity
entity_kind: person | place | org | product | event
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - Display Name
sources:
  - source-slug-1
tags: [topic]
---
```

### Concept page (`type: concept`)
```yaml
---
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - Display Name
sources:
  - source-slug-1
related:
  - other-concept-slug
tags: [topic]
---
```

### Synthesis page (`type: synthesis`)
```yaml
---
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
question: "the question this synthesis answers"
sources:
  - source-slug-1
aliases:
  - Display Name
tags: [topic]
---
```

Always update `updated:` when you edit a page. Use today's date from the
system context — never invent.

## Wikilinks

- Internal: `[[page-slug]]` or `[[page-slug|Display Text]]`. Bare slugs only.
- Citations: link to source pages, not raw files.
  E.g., "Jung argued the unconscious has structure ([[red-book-summary]])."
- Don't link every mention — once per page section is enough.
- `## Related` section at page end lists cross-references. Do NOT add
  `## Parent` — redundant with Backlinks.

## log.md

Append-only chronological log. Every entry: `## [YYYY-MM-DD] <op> | <title>`.

```markdown
## [2026-04-16] ingest | The Red Book by C.G. Jung
Created [[red-book-summary]]. Updated [[carl-jung]], [[individuation]].
Notable: introduced concept of [[shadow]].

## [2026-04-16] query | What does my wiki say about meaning-making?
Synthesized from [[red-book-summary]], [[mans-search-for-meaning]].
Filed as [[meaning-making-personal]].

## [2026-04-17] lint | Health check
3 broken wikilinks, 2 orphans. User fixed broken links; orphans deferred.
```

Operations: `init`, `ingest`, `query`, `lint`, `manual` (hand edits).

Grep recent activity: `grep "^## \[" log.md | tail -10`.

## Date handling

Always use today's date from the system context. Never guess. When
converting relative dates from a source ("last Thursday"), compute
against the source's known publish date, not today.

## Obsidian config

`.obsidian/app.json` has `userIgnoreFilters: ["brain2/raw/"]` so raw/ is
hidden from search, graph, and file tree. Don't write wikilinks that
resolve into raw/.

Folder-note pattern works natively (wikilinks resolve correctly). Install
"Folder Note Core" plugin for nicer UX (clicking a folder opens its note).
