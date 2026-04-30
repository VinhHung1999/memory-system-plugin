#!/usr/bin/env bash
# Wiki inject — aggregates ALL of brain2/wiki/ at SessionStart / PostCompact.
# Shows top-level wiki sections with .md file counts + today's raw inbox path.
# Does NOT load file content — Claude reads on demand via recall skills.

set -e

VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
WIKI="$VAULT/wiki"
RAW_ROOT="$VAULT/raw"
TODAY=$(date +%F)
RAW_TODAY="$RAW_ROOT/$TODAY"

# Read stdin
INPUT=$(cat)
HOOK_EVENT=$(echo "$INPUT" | sed -n 's/.*"hook_event_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
HOOK_EVENT="${HOOK_EVENT:-SessionStart}"

# Bail silently if vault missing (graceful for users without brain2)
if [ ! -d "$WIKI" ]; then
  echo '{}'
  exit 0
fi

# Collect top-level wiki sections + recursive .md counts.
# Skip folders starting with "_" or "." (templates / hidden).
SECTIONS_PLAIN=""
SECTION_COUNT=0
for dir in "$WIKI"/*/; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  case "$name" in _*|.*) continue ;; esac
  count=$(find "$dir" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  SECTIONS_PLAIN="${SECTIONS_PLAIN}  • ${name}/ (${count})"$'\n'
  SECTION_COUNT=$((SECTION_COUNT + 1))
done
SECTIONS_PLAIN="${SECTIONS_PLAIN%$'\n'}"

# ANSI codes for systemMessage banner
C_RESET=$'\033[0m'
C_BOLD=$'\033[1m'
C_DIM=$'\033[2m'
C_CYAN=$'\033[36m'
C_YELLOW=$'\033[33m'

case "$HOOK_EVENT" in
  SessionStart) ICON="🚀" ;;
  PostCompact)  ICON="🔁" ;;
  *)            ICON="✨" ;;
esac

WIKI_SHORT="${WIKI/#$HOME/~}"

SYSTEM_MSG="${ICON} ${C_BOLD}${C_CYAN}Brain2 wiki${C_RESET} ${C_DIM}@ ${WIKI_SHORT}${C_RESET} ${C_DIM}(${C_YELLOW}${SECTION_COUNT}${C_DIM} sections)${C_RESET}"

CONTEXT_MSG="[Brain2 Wiki] Hung's persistent knowledge in brain2 vault.

- **Wiki root (curated):** \`${WIKI}/\`
- **Today's raw inbox (staging):** \`${RAW_TODAY}/\`

## Wiki Sections (${SECTION_COUNT})
${SECTIONS_PLAIN}

## Skills (all under /second-brain:)
- \`memory-recall\` — query universal cross-project lessons (wiki/code-knowledge/, READ-ONLY)
- \`project-memory-recall role=<po|dev|qc|cmo>\` — query per-project role memory
- \`second-brain\` (mega) — ingest, query, lint, note, journal, kanban

## Memory capture is automatic
- Every Claude turn is auto-logged to workspace \`observation.md\` by Stop hook
- Nightly dream skill (2 AM, planned) reads observation.md → extracts insights
  into wiki/projects/<X>/memory/<role>.md → archives the day's log
- Active store skills retired — no manual storing needed

## When to recall
- Universal cross-project lesson → memory-recall
- Project-specific (stakeholder pattern, codebase quirk) → project-memory-recall role=<role> project=<name>
- Brand new topic / discrete note → second-brain
- Trivial ops (typo, build cmd, quick lookup) → skip memory entirely
"

# JSON-escape via python
escape_json() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"
}

SYSTEM_MSG_JSON=$(escape_json "$SYSTEM_MSG")
CONTEXT_MSG_JSON=$(escape_json "$CONTEXT_MSG")

# PostCompact schema does NOT allow hookSpecificOutput.additionalContext;
# only SessionStart (and UserPromptSubmit/PostToolUse) do. For PostCompact,
# emit only the top-level systemMessage.
case "$HOOK_EVENT" in
  PostCompact)
    cat <<EOF
{
  "systemMessage": $SYSTEM_MSG_JSON
}
EOF
    ;;
  *)
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "$HOOK_EVENT",
    "additionalContext": $CONTEXT_MSG_JSON
  },
  "systemMessage": $SYSTEM_MSG_JSON
}
EOF
    ;;
esac
