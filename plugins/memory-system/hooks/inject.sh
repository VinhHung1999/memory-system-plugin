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

# Auto-create memory dir on first run (zero-setup for new users)
mkdir -p "$MEMORY_DIR"

# Auto-bootstrap missing INDEX files so inject has something to load.
# Creates per-domain INDEX.md stub if missing, and root MEMORY.md if missing.

# Helper: create a per-domain INDEX.md stub
ensure_domain_index() {
  local dir="$1"
  local name
  name=$(basename "$dir")
  local index="$dir/INDEX.md"
  [ -f "$index" ] && return 0
  cat > "$index" <<EOF
# ${name}

_Auto-generated stub. Fill with category overview as memories accumulate._

## Categories

_(none yet — add subfolders bugs/, patterns/, decisions/, procedures/, structure/ as memories accumulate past the flat threshold of 3 files)_

## Highlights

_(none yet)_
EOF
}

# Ensure per-domain INDEX.md exists for every subfolder
for dir in "$MEMORY_DIR"/*/; do
  [ -d "$dir" ] || continue
  ensure_domain_index "$dir"
done

# Ensure root MEMORY.md exists
if [ ! -f "$MEMORY_DIR/MEMORY.md" ]; then
  {
    echo "# Memory Master Index"
    echo ""
    echo "_Auto-generated. Updated whenever new domains appear._"
    echo ""
    echo "## Domains"
    echo ""
    echo "| Domain | Description |"
    echo "|---|---|"
    for d in "$MEMORY_DIR"/*/; do
      [ -d "$d" ] || continue
      dname=$(basename "$d")
      echo "| [${dname}/](${dname}/INDEX.md) | _(add description)_ |"
    done
    echo ""
    echo "## How this works"
    echo ""
    echo "This is your GLOBAL cross-project knowledge base. Each domain has an INDEX.md listing its categories and highlights. Save new patterns via \`/memory-system:coder-memory-store\`."
  } > "$MEMORY_DIR/MEMORY.md"
fi

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
  # Load MEMORY.md content if exists (truncate to first 200 lines to stay lean)
  MEMORY_INDEX_CONTENT=""
  MEMORY_STATUS="✗ not found"
  if [ -f "$MEMORY_DIR/MEMORY.md" ]; then
    MEMORY_INDEX_CONTENT=$(head -n 200 "$MEMORY_DIR/MEMORY.md")
    memory_bytes=$(wc -c < "$MEMORY_DIR/MEMORY.md" | tr -d ' ')
    MEMORY_STATUS="✓ ${memory_bytes} bytes"
  fi

  # Also grab each domain's INDEX.md header (first 10 lines) so Claude sees what's inside each
  DOMAIN_INDEXES=""
  indexes_loaded=0
  for dir in "$MEMORY_DIR"/*/; do
    [ -d "$dir" ] || continue
    name=$(basename "$dir")
    if [ -f "$dir/INDEX.md" ]; then
      preview=$(head -n 10 "$dir/INDEX.md")
      DOMAIN_INDEXES="${DOMAIN_INDEXES}

### ${name}/INDEX.md (preview)
${preview}"
      indexes_loaded=$((indexes_loaded + 1))
    fi
  done

  # systemMessage shows what was loaded
  SYSTEM_MSG="${ICON} ${C_BOLD}${C_CYAN}Universal Memory loaded${C_RESET} ${C_DIM}from ~/.claude/memory/${C_RESET}
  ${C_DIM}└ MEMORY.md: ${C_RESET}${MEMORY_STATUS}
  ${C_DIM}└ Domain INDEX.md loaded: ${C_RESET}${C_YELLOW}${indexes_loaded}${C_RESET}
$TOPICS"

  CONTEXT_MSG="[Universal Memory] Your GLOBAL cross-project knowledge base at ~/.claude/memory/.

**⚠️  BEFORE starting ANY non-trivial task, CHECK THIS MEMORY FIRST.**

The indexes below tell you what's already been learned. If the current task touches a domain/category listed here, **read the relevant file** before reinventing the wheel. Past lessons may save you hours of debugging.

## Master index (MEMORY.md)
${MEMORY_INDEX_CONTENT:-(empty — no MEMORY.md yet)}

## Available topic folders
$TOPICS_PLAIN

## Domain INDEX previews
${DOMAIN_INDEXES:-(no domain INDEX files yet)}

---

## Workflow — always follow this order

1. **READ FIRST**: Before coding, scan the indexes above. Does any entry match your task?
   - If yes → read the full memory file at ~/.claude/memory/<domain>/<category>/<file>.md
   - If unsure → use skill /memory-system:coder-memory-recall for keyword search
2. **WORK**: Apply learned patterns. Avoid mistakes already documented.
3. **STORE**: When you discover a new non-obvious lesson → /memory-system:coder-memory-store

This is universal (cross-project) memory. Project-specific memory is handled separately by built-in auto memory — don't mix the two."
else
  # Short reminder on Read — no folder list (already shown at SessionStart)
  SYSTEM_MSG="${ICON} ${C_DIM}Read Universal Memory if relevant → ~/.claude/memory/<topic>/${C_RESET}"

  CONTEXT_MSG="Universal Memory is at ~/.claude/memory/. If the current task matches any topic there, read the relevant <topic>/INDEX.md or specific files. Use /memory-system:coder-memory-recall for keyword search, /memory-system:coder-memory-store to save new patterns."
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
