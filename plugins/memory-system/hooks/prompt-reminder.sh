#!/usr/bin/env bash
# UserPromptSubmit hook — ultra-light pointer to wiki memory.
# Fires on every prompt but stays under 30 words to minimize context noise.

set -e

VAULT="${SECOND_BRAIN_VAULT:-$HOME/Documents/Notes/HungVault/HungVault/brain2}"
WIKI_CK="$VAULT/wiki/code-knowledge"

# Bail silently if vault missing
if [ ! -d "$WIKI_CK" ]; then
  echo '{}'
  exit 0
fi

cat > /dev/null  # consume stdin

WIKI_SHORT="${WIKI_CK/#$HOME/~}"

REMINDER="Wiki: ${WIKI_SHORT}/. Use /memory-system:coder-memory-recall only if task is non-trivial (unclear bug, design choice, unfamiliar domain). Skip for trivial ops (typo, build, lookup)."

ESCAPE() { python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"; }
CONTEXT_JSON=$(ESCAPE "$REMINDER")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": $CONTEXT_JSON
  }
}
EOF
