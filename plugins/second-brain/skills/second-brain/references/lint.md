# Lint workflow

Lint is a meta-audit of wiki health. It's what keeps a growing wiki from
rotting. Don't auto-fix — surface findings, let the user prioritize.

## When to run

User invokes `/second-brain lint`:
- Periodically (every 10-20 ingests is a reasonable cadence).
- After a burst of quick ingests.
- When a query exposed inconsistencies.
- When the wiki feels like it's drifting.

## Step-by-step

### 1. Broken wikilinks (run first — fast, high value)

```bash
bash <skill-dir>/scripts/check-broken-links.sh
```

Defaults to the standard vault path. Exit 0 = clean, 1 = broken links.
Script handles spaces, Unicode filenames, strips `|alias` and `#section`
markers, and reports which files reference each broken slug.

### 2. Take inventory

```bash
VAULT=$SECOND_BRAIN_VAULT

# Count files per life-area
find "$VAULT/wiki" -name "*.md" -type f -print0 \
  | while IFS= read -r -d '' f; do
      echo "$f" | sed "s|$VAULT/wiki/||" | awk -F/ '{print $1}'
    done | sort | uniq -c
```

Use `-print0` / `read -d ''` — NOT `for f in $(find ...)` which breaks on
filenames with spaces or Unicode. This bit us once; the fix is stored in
`~/.claude/memory/universal-patterns/bugs/bash-find-whitespace-split.md`.

### 3. Run the other checks

#### A. Orphan pages (no inbound wikilinks)

A page is an orphan if nothing else links to it. Some orphans are
intentional (`wiki.md`, `overview.md` are roots). Unintended orphans
usually mean a missed cross-reference during ingest.

```bash
find "$VAULT/wiki" -name "*.md" -type f -print0 \
  | while IFS= read -r -d '' page; do
      slug=$(basename "$page" .md)
      inbound=$(grep -rl "\[\[$slug" "$VAULT/wiki" --exclude="$page" | wc -l)
      if [ "$inbound" -eq 0 ]; then
        echo "ORPHAN: $page"
      fi
    done
```

Exclude expected roots: `wiki.md`, `overview.md`.

#### B. Folder-note coverage

Every folder under `wiki/` should have a same-named folder-note. Missing
MOCs mean broken navigation.

```bash
find "$VAULT/wiki" -type d | while IFS= read -r dir; do
  name=$(basename "$dir")
  if [ "$name" = "wiki" ]; then continue; fi
  if [ ! -f "$dir/$name.md" ]; then
    echo "MISSING FOLDER-NOTE: $dir/$name.md"
  fi
done
```

#### C. Stale claims

Pages not updated in 6+ months while related sources have been ingested
since.

```bash
find "$VAULT/wiki" -name "*.md" -type f -print0 \
  | while IFS= read -r -d '' page; do
      updated=$(grep -m1 "^updated:" "$page" | awk '{print $2}')
      echo "$updated $page"
    done | sort
```

For pages with old `updated:`, check whether their `sources:` frontmatter
is stale vs. recent log entries.

#### D. Concepts mentioned without dedicated pages

Terms that appear 3+ times across wiki body but have no dedicated page.
Rough heuristic:

```bash
grep -rho '[A-Z][a-z]\+\( [A-Z][a-z]\+\)\+' "$VAULT/wiki" \
  | sort | uniq -c | sort -rn | head -30
```

Filter manually — many will be false positives.

#### E. Frontmatter validity

Every page should have required frontmatter fields.

```bash
find "$VAULT/wiki" -name "*.md" -type f -print0 \
  | while IFS= read -r -d '' page; do
      head -10 "$page" | grep -q "^type:" || echo "MISSING type: $page"
      head -10 "$page" | grep -q "^updated:" || echo "MISSING updated: $page"
    done
```

#### F. `## Parent` sections (should be removed)

Convention says no `## Parent` sections — Obsidian Backlinks handle it.
Any page with one is non-compliant:

```bash
grep -rln "^## Parent$" "$VAULT/wiki" 2>/dev/null
```

(False positives: content section heads that legitimately start with
"Parent" like "## Parent–Child Executor pattern" — just eyeball.)

#### G. Contradictions across pages

Hardest to automate.
- Look for pages with `## Open questions` or `## Contradictions` sections;
  surface the unresolved ones.
- Cross-check entities/concepts appearing in multiple sources for
  contradictory claims (judgment-heavy; pick high-traffic pages).

### 4. Compose the report

Write findings in conversation, ordered by severity:

```markdown
# Lint report — YYYY-MM-DD

## High priority
- Broken wikilink `[[foo]]` referenced from [[bar]].
- Missing folder-note `work/momo/newfolder/newfolder.md`.

## Medium priority
- Orphan: [[some-page]] has no inbound links — likely a missed cross-ref.
- Unresolved Open Question on [[concept-x]] (flagged 3 months ago).

## Low priority
- Stale: [[entity-y]] not updated in 8 months, but 2 related sources
  added since.
- Concept candidate: "Active Imagination" mentioned in 5 pages, no page yet.

## Summary
N high, M medium, K low.
```

### 5. Ask the user how to proceed

Don't auto-fix. Ask:

> "Fix the high-priority items now? All of them? Just the broken links?"

For each confirmed fix:
- Apply the change.
- Update relevant folder MOCs if affected.
- Don't log individual fixes — one consolidated log entry at the end.

### 6. Append the log entry

```markdown
## [YYYY-MM-DD] lint | Health check
N high, M medium, K low. User confirmed fixes for: <list>. Skipped: <list>.
Wiki health: <one-sentence summary>.
```

## What lint should NOT do

- Don't fix without asking. User owns the wiki's voice; asymmetries may
  be intentional.
- Don't be a perfectionist about orphans. `wiki.md` and `overview.md`
  are intentional roots.
- Don't propose major restructurings (e.g., "rename the entire work/
  folder"). Lint is incremental hygiene, not architecture. Surface as
  recommendation, not action.

## Optional: web search for gap-filling

If lint exposes a concept the user cares about but has no source for,
offer to web-search and propose sources to ingest. Never ingest external
content without explicit user approval — sources are the user's
curatorial domain.
