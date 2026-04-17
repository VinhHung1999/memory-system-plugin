#!/bin/bash
# Check for broken wikilinks in the second-brain vault.
# Reports wikilinks that reference pages which don't exist.
#
# Usage:
#   bash check-broken-links.sh [vault-path]
#
# Defaults to $SECOND_BRAIN_VAULT.
# Exits 0 when clean, 1 when broken links found.

set -euo pipefail

VAULT="${1:-${SECOND_BRAIN_VAULT:?SECOND_BRAIN_VAULT not set — export it or pass vault path as first arg}}"

if [ ! -d "$VAULT/wiki" ]; then
  echo "Error: wiki/ not found at $VAULT/wiki" >&2
  exit 2
fi

SLUGS=$(mktemp)
USED=$(mktemp)
trap 'rm -f "$SLUGS" "$USED"' EXIT

# Collect all existing slugs: basenames of every .md file under wiki/.
# Use -print0 / read -d '' so filenames with spaces or Unicode survive.
find "$VAULT/wiki" -name "*.md" -type f -print0 | while IFS= read -r -d '' f; do
  basename "$f" .md
done | sort -u > "$SLUGS"

# brain2/log.md lives outside wiki/ but is wikilinked as [[log]] from wiki.md.
echo "log" >> "$SLUGS"
sort -u "$SLUGS" -o "$SLUGS"

# Collect all used wikilinks from every .md in wiki/.
#   Strip `|alias` (display text) and `#section` (anchor).
#   Exclude empty and "page-slug" (documentation placeholder).
grep -rho '\[\[[^]]*\]\]' "$VAULT/wiki" 2>/dev/null \
  | sed 's/\[\[//; s/\]\]//; s/|.*//; s/#.*//' \
  | grep -v '^$' \
  | sort -u > "$USED"

# Diff: used but not present.
BROKEN=$(comm -23 "$USED" "$SLUGS")

TOTAL_USED=$(wc -l < "$USED" | tr -d ' ')
TOTAL_SLUGS=$(wc -l < "$SLUGS" | tr -d ' ')

if [ -z "$BROKEN" ]; then
  echo "OK — no broken wikilinks."
  echo "    $TOTAL_USED unique links checked against $TOTAL_SLUGS existing slugs."
  exit 0
fi

echo "BROKEN wikilinks found:"
echo ""
echo "$BROKEN" | while IFS= read -r link; do
  [ -z "$link" ] && continue
  echo "  [[$link]]"
  grep -rln "\[\[$link" "$VAULT/wiki" 2>/dev/null | head -3 | sed 's|^|      ref: |'
  echo ""
done
exit 1
