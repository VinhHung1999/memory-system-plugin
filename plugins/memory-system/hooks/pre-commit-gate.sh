#!/usr/bin/env bash
# Pre-commit/push reminder: suggests running /knowledge-updater before git commit/push.
# Non-blocking — shows a tip via systemMessage but lets the git command proceed.
# Fires on PreToolUse Bash.

set -e

STATE_FILE="$HOME/.claude/knowledge_updater_state.json"

INPUT=$(cat)

# Extract command and session_id
CMD=$(echo "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))' 2>/dev/null || echo "")
SESSION_ID=$(echo "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("session_id","default"))' 2>/dev/null || echo "default")

# Only fire on git commit / git push
if ! echo "$CMD" | grep -qE '(^|[[:space:]])git[[:space:]]+(commit|push)([[:space:]]|$)'; then
  exit 0
fi

# Skip reminder if /knowledge-updater already ran this session
if [ -f "$STATE_FILE" ]; then
  RAN=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('$SESSION_ID',''))" 2>/dev/null || echo "")
  if [ -n "$RAN" ]; then
    exit 0
  fi
fi

# Soft reminder — does NOT block. Provides BOTH:
# - systemMessage: visible to the user
# - additionalContext: read by Claude so it knows to actually invoke the skill
cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "[Pre-commit check] You are about to run git commit/push. Before proceeding, consider whether this session made significant changes that should be captured via /memory-system:knowledge-updater. If yes: invoke the skill first (it will analyze the diff and update CLAUDE.md, rules, memory, or skills as needed). If nothing significant changed: continue with the commit. Either way, this hook does NOT block the git command."
  },
  "systemMessage": "💡 Tip: consider /memory-system:knowledge-updater before committing if you made significant changes this session (CLAUDE.md, rules, memory, skills)."
}
EOF
