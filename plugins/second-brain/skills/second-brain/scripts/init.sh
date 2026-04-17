#!/bin/bash
# Initialize the brain2 second-brain vault.
# Idempotent — never overwrites existing files.
#
# Creates:
#   brain2/CLAUDE.md             (schema — copied from skill asset)
#   brain2/log.md                (activity log — seeded with init entry)
#   brain2/raw/assets/           (image drop zone)
#   brain2/wiki/wiki.md          (vault router / folder-note)
#   brain2/wiki/overview.md      (identity page)
#
# Life-area folders (work/, code-knowledge/, etc.) are NOT pre-created.
# They accrete as content is ingested, each with its own folder-note.

set -euo pipefail

VAULT="${1:-${SECOND_BRAIN_VAULT:?SECOND_BRAIN_VAULT not set — export it or pass vault path as first arg}}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TODAY="$(date +%Y-%m-%d)"

echo "Initializing second-brain vault at: $VAULT"

mkdir -p "$VAULT"/raw/assets
mkdir -p "$VAULT"/wiki

# CLAUDE.md — in-vault schema
if [ ! -f "$VAULT/CLAUDE.md" ]; then
  cp "$SKILL_DIR/assets/CLAUDE.md.template" "$VAULT/CLAUDE.md"
  echo "  + CLAUDE.md"
else
  echo "  = CLAUDE.md (kept existing)"
fi

# log.md
if [ ! -f "$VAULT/log.md" ]; then
  cat > "$VAULT/log.md" <<EOF
# Log

Chronological record of wiki activity. Each entry:
\`## [YYYY-MM-DD] <op> | <title>\`.

Grep recent activity: \`grep "^## \\[" log.md | tail -10\`.

## [$TODAY] init | vault initialized
First initialization of brain2 second-brain wiki.
EOF
  echo "  + log.md"
else
  echo "  = log.md (kept existing)"
fi

# wiki/wiki.md — top-level folder-note
if [ ! -f "$VAULT/wiki/wiki.md" ]; then
  cat > "$VAULT/wiki/wiki.md" <<EOF
---
type: index
created: $TODAY
updated: $TODAY
aliases:
  - Wiki
  - Hung's Second Brain
tags: [moc, root]
---

# Wiki — Hung's Second Brain

Top-level router. Read first on every op. Drill into a life-area's
folder-note for specifics.

## Identity
- [[overview]] — who is Hung (top-level synthesis)

## Life areas

_(empty — folders accrete as content is ingested)_

Expected life areas (create when first page lands there):
- \`work/\` — company/job knowledge
- \`code-knowledge/\` — transferable tech
- \`projects/\` — personal/side projects
- \`research/\` — active deep-dive research
- \`doing/\` — current focus / WIP
- \`personal/\` — health, goals, journal

## Recent activity

See [[log]] for the chronological record.
EOF
  echo "  + wiki/wiki.md"
else
  echo "  = wiki/wiki.md (kept existing)"
fi

# wiki/overview.md
if [ ! -f "$VAULT/wiki/overview.md" ]; then
  cat > "$VAULT/wiki/overview.md" <<EOF
---
type: overview
created: $TODAY
updated: $TODAY
aliases:
  - Overview
  - Who is Hung
---

# Overview — Hung

Top-level synthesis of who Hung is. Updated on every ingest that
meaningfully changes the picture. For navigation, see [[wiki]].

## Identity
_(fill in as sources accumulate)_

## Goals & values
_(empty)_

## Skills & expertise
_(empty)_

## Recent direction
_(empty)_

## Open questions
_(empty)_

## How this wiki is organized

- [[wiki]] — vault router
- _(life-area folders accrete over time)_
EOF
  echo "  + wiki/overview.md"
else
  echo "  = wiki/overview.md (kept existing)"
fi

echo ""
echo "Vault ready. Layout:"
ls -la "$VAULT"
echo ""
echo "wiki/:"
ls -la "$VAULT/wiki"

echo ""
echo "Next: configure Obsidian to ignore raw/ — set userIgnoreFilters"
echo "in .obsidian/app.json to [\"brain2/raw/\"]."
