#!/usr/bin/env bash
# Pre-commit/push gate: blocks git commit/push until /knowledge-updater has run
# in this session. Fires on PreToolUse Bash.

set -e

STATE_FILE="$HOME/.claude/knowledge_updater_state.json"

INPUT=$(cat)

# Extract command and session_id
CMD=$(echo "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))' 2>/dev/null || echo "")
SESSION_ID=$(echo "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("session_id","default"))' 2>/dev/null || echo "default")

# Only gate git commit / git push
if ! echo "$CMD" | grep -qE '(^|[[:space:]])git[[:space:]]+(commit|push)([[:space:]]|$)'; then
  exit 0
fi

# Check if /knowledge-updater ran in this session
if [ -f "$STATE_FILE" ]; then
  RAN=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('$SESSION_ID',''))" 2>/dev/null || echo "")
  if [ -n "$RAN" ]; then
    exit 0
  fi
fi

# Block with reason
cat <<EOF
{
  "decision": "block",
  "reason": "🚫 Blocked: before 'git commit' or 'git push', run /knowledge-updater to capture any knowledge changes (CLAUDE.md, rules, memory, skills) from this session. If nothing significant changed, just run /knowledge-updater once and say 'Nothing to update'. After that, retry the git command."
}
EOF
