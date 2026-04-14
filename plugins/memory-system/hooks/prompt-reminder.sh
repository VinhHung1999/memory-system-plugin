#!/usr/bin/env bash
# UserPromptSubmit hook — inject a short memory-first reminder on every user prompt.
# Purpose: combat attention decay in long sessions. Fires at task-start moments,
# not on every tool call (unlike the deprecated PreToolUse Read hook).

set -e

MEMORY_DIR="$HOME/.claude/memory"

# Bail silently if memory dir doesn't exist
[ ! -d "$MEMORY_DIR" ] && exit 0

# Read stdin (we don't need its fields, just consume it)
cat > /dev/null

# List domain folder names (no counts, no contents — keep it light)
DOMAINS=""
for dir in "$MEMORY_DIR"/*/; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  DOMAINS="${DOMAINS}${name}, "
done
DOMAINS="${DOMAINS%, }"

# Nothing to show if no domains yet
[ -z "$DOMAINS" ] && exit 0

REMINDER="[Memory check] Before starting this task, consider whether universal memory has relevant past lessons.

Available domains: ${DOMAINS}

If the task touches any of these, scan the relevant ~/.claude/memory/<domain>/<category>/INDEX.md first, or use skill /memory-system:coder-memory-recall for keyword search. This prevents reinventing solutions already documented."

# JSON-escape via python
ESCAPED=$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$REMINDER")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": $ESCAPED
  }
}
EOF
