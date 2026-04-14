#!/usr/bin/env bash
# Memory Injection Hook
# Tells Claude where universal memory lives and what topics are available.
# Does NOT load file content — Claude reads it on demand when relevant.

set -e

MEMORY_DIR="$HOME/.claude/memory"

# Read stdin input
INPUT=$(cat)

# Extract hook_event_name (fallback to PreToolUse)
HOOK_EVENT=$(echo "$INPUT" | sed -n 's/.*"hook_event_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
HOOK_EVENT="${HOOK_EVENT:-PreToolUse}"

# Exit silently if memory dir missing
[ ! -d "$MEMORY_DIR" ] && exit 0

# ANSI color codes
C_RESET=$'\033[0m'
C_BOLD=$'\033[1m'
C_DIM=$'\033[2m'
C_CYAN=$'\033[36m'
C_GREEN=$'\033[32m'
C_YELLOW=$'\033[33m'
C_MAGENTA=$'\033[35m'

# List all subdirectories (topic folders) with file counts — one per line
TOPICS=""
TOPICS_PLAIN=""
for dir in "$MEMORY_DIR"/*/; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  count=$(find "$dir" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  TOPICS="${TOPICS}  ${C_MAGENTA}•${C_RESET} ${C_GREEN}${name}${C_RESET} ${C_DIM}(${C_YELLOW}${count}${C_DIM})${C_RESET}"$'\n'
  TOPICS_PLAIN="${TOPICS_PLAIN}  • ${name} (${count})"$'\n'
done
TOPICS="${TOPICS%$'\n'}"
TOPICS_PLAIN="${TOPICS_PLAIN%$'\n'}"

# Pick icon
case "$HOOK_EVENT" in
  SessionStart) ICON="🚀" ;;
  PostCompact)  ICON="🔁" ;;
  *)            ICON="✨" ;;
esac

if [ "$HOOK_EVENT" = "SessionStart" ] || [ "$HOOK_EVENT" = "PostCompact" ]; then
  # Full list on session start and after compact (context was cleared)
  SYSTEM_MSG="${ICON} ${C_BOLD}${C_CYAN}Universal Memory${C_RESET} ${C_DIM}(global, cross-project knowledge) ready at ~/.claude/memory/${C_RESET}
$TOPICS"

  CONTEXT_MSG="[Universal Memory] This is your GLOBAL knowledge base shared across ALL projects (not project-specific). Stored at ~/.claude/memory/.

Available topic folders:
$TOPICS_PLAIN

When working on a task, if relevant universal knowledge might exist, read ~/.claude/memory/<topic>/INDEX.md first (or use skill /coder-memory-recall for keyword search). Save new cross-project patterns via /coder-memory-store.

Note: project-specific memory is handled separately by built-in auto memory — don't confuse the two."
else
  # Short reminder on Read — no folder list (already shown at SessionStart)
  SYSTEM_MSG="${ICON} ${C_DIM}Read Universal Memory if relevant → ~/.claude/memory/<topic>/${C_RESET}"

  CONTEXT_MSG="Universal Memory is at ~/.claude/memory/. If the current task matches any topic there, read the relevant <topic>/INDEX.md or specific files. Use /coder-memory-recall for keyword search, /coder-memory-store to save new patterns."
fi

# JSON-escape via python
escape_json() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"
}

SYSTEM_MSG_JSON=$(escape_json "$SYSTEM_MSG")
CONTEXT_MSG_JSON=$(escape_json "$CONTEXT_MSG")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "$HOOK_EVENT",
    "additionalContext": $CONTEXT_MSG_JSON
  },
  "systemMessage": $SYSTEM_MSG_JSON
}
EOF
