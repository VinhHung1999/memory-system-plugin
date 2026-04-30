#!/usr/bin/env bash
# UserPromptSubmit hook — ultra-light pointer to brain2 memory skills.
# Fires on every prompt but stays terse to minimize context noise.

set -e

VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
WIKI="$VAULT/wiki"

# Bail silently if vault missing
if [ ! -d "$WIKI" ]; then
  echo '{}'
  exit 0
fi

cat > /dev/null  # consume stdin

WIKI_SHORT="${WIKI/#$HOME/~}"

REMINDER="Brain2 wiki: ${WIKI_SHORT}/. Recall when there's specific past context to surface: (a) project name mentioned (working on it / stakeholder refers to it) → /second-brain:project-memory-recall role=<role> project=<name>; (b) unfamiliar domain / library / unknown error → /second-brain:memory-recall; (c) user explicitly asks (\"--recall\", \"what do we know about X\") → use the matching one. Default: skip — most prompts don't need recall."

# ANSI color codes for the visible banner
C_RESET=$'\033[0m'
C_DIM=$'\033[2m'
C_CYAN=$'\033[36m'

SYSTEM_MSG="${C_DIM}✨ ${C_CYAN}Brain2 memory${C_RESET}${C_DIM} → recall only when project mentioned / unfamiliar domain / explicit ask${C_RESET}"

ESCAPE() { python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"; }
CONTEXT_JSON=$(ESCAPE "$REMINDER")
SYSTEM_JSON=$(ESCAPE "$SYSTEM_MSG")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": $CONTEXT_JSON
  },
  "systemMessage": $SYSTEM_JSON
}
EOF
