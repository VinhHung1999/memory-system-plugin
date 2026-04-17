#!/usr/bin/env bash
# Wiki memory injection — points to Hung's brain2 vault.
# Shows domain folders in wiki/code-knowledge/ + raw/ inbox path.
# Does NOT load file content — Claude reads on demand via the recall skill.

set -e

VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
WIKI_CK="$VAULT/wiki/code-knowledge"
RAW_ROOT="$VAULT/raw"
TODAY=$(date +%F)
RAW_CK_TODAY="$RAW_ROOT/$TODAY/code-knowledge"

# Read stdin
INPUT=$(cat)
HOOK_EVENT=$(echo "$INPUT" | sed -n 's/.*"hook_event_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
HOOK_EVENT="${HOOK_EVENT:-SessionStart}"

# Bail silently if vault missing (let users without brain2 run the plugin harmlessly)
if [ ! -d "$WIKI_CK" ]; then
  echo '{}'
  exit 0
fi

# Collect domain folders + file counts (recursive over bugs/ and patterns/ subfolders)
DOMAINS_PLAIN=""
DOMAIN_COUNT=0
for dir in "$WIKI_CK"/*/; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  count=$(find "$dir" -maxdepth 3 -name "*.md" -not -name "$(basename "$dir").md" 2>/dev/null | wc -l | tr -d ' ')
  DOMAINS_PLAIN="${DOMAINS_PLAIN}  • ${name} (${count})"$'\n'
  DOMAIN_COUNT=$((DOMAIN_COUNT + 1))
done
DOMAINS_PLAIN="${DOMAINS_PLAIN%$'\n'}"

# ANSI color codes for systemMessage
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

WIKI_SHORT="${WIKI_CK/#$HOME/~}"

SYSTEM_MSG="${ICON} ${C_BOLD}${C_CYAN}Wiki memory${C_RESET} ${C_DIM}@ ${WIKI_SHORT}${C_RESET} ${C_DIM}(${C_YELLOW}${DOMAIN_COUNT}${C_DIM} domains)${C_RESET}"

CONTEXT_MSG="[Wiki memory] Hung's universal coding knowledge lives in brain2 vault.

- **Curated (read):** \`${WIKI_CK}/\` — each domain has \`bugs/\` and \`patterns/\` subfolders
- **Inbox (write via store skill):** \`${RAW_ROOT}/<YYYY-MM-DD>/code-knowledge/\` — date-bucketed staging (today: \`${TODAY}\`); Hung promotes to wiki/ manually later

## Domains (${DOMAIN_COUNT})
${DOMAINS_PLAIN}

## Workflow
1. **Non-trivial task?** Use \`/memory-system:coder-memory-recall\` — it picks qmd search (semantic) or grep depending on query.
2. **Hard-won lesson to save?** Use \`/memory-system:coder-memory-store\` — stages to \`raw/<YYYY-MM-DD>/code-knowledge/\` (today's date bucket). Never write to \`wiki/\` directly; that's Hung's curated space.
3. **Trivial task (typo, build cmd, quick lookup)?** Skip memory entirely — don't invoke the skills.

This is cross-project memory. Project-specific memory is built-in auto memory (separate system)."

# JSON-escape via python
escape_json() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"
}

SYSTEM_MSG_JSON=$(escape_json "$SYSTEM_MSG")
CONTEXT_MSG_JSON=$(escape_json "$CONTEXT_MSG")

# PostCompact schema does NOT allow hookSpecificOutput.additionalContext;
# only SessionStart (and UserPromptSubmit/PostToolUse) do. For PostCompact,
# emit only the top-level systemMessage — the SessionStart context is still
# loaded from earlier in the same session anyway.
if [ "$HOOK_EVENT" = "PostCompact" ]; then
  cat <<EOF
{
  "systemMessage": $SYSTEM_MSG_JSON
}
EOF
else
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "$HOOK_EVENT",
    "additionalContext": $CONTEXT_MSG_JSON
  },
  "systemMessage": $SYSTEM_MSG_JSON
}
EOF
fi
