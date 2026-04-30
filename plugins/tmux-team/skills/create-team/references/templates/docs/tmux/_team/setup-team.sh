#!/bin/bash
# {TEAM_NAME} — Tmux team launcher.
# Creates a tmux session with one Claude Code pane per role.
# Each pane's @role_name option is read by the SessionStart hook to
# inject team workflow + role agent + current board state.

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)}"
SESSION_NAME="${SESSION_NAME:-{SESSION_NAME}}"

echo "Starting {TEAM_NAME} setup..."
echo "  Project: $PROJECT_ROOT"
echo "  Session: $SESSION_NAME"

# 1. Existing session check
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Session '$SESSION_NAME' already exists."
  read -rp "Kill it and recreate? (y/N) " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then
    tmux kill-session -t "$SESSION_NAME"
  else
    echo "Aborted. Attach with: tmux attach -t $SESSION_NAME"
    exit 0
  fi
fi

ROLES=({ROLES})
NUM_PANES=${#ROLES[@]}

# 2. Create session + N-pane layout (one pane per role)
cd "$PROJECT_ROOT"
tmux new-session -d -s "$SESSION_NAME"
for ((i=1; i<NUM_PANES; i++)); do
  tmux split-window -h -t "$SESSION_NAME"
done
tmux select-layout -t "$SESSION_NAME" even-horizontal
tmux resize-window -t "$SESSION_NAME" -x $((NUM_PANES * 100)) -y 50 || true

# 3. Set per-pane role_name (used by SessionStart hook)
for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  tmux select-pane -t "$SESSION_NAME:0.$i" -T "$ROLE"
  tmux set-option -p -t "$SESSION_NAME:0.$i" @role_name "$ROLE"
  tmux set-option -p -t "$SESSION_NAME:0.$i" @team_name "{TEAM_NAME}"
done

# 4. Verify tm-send is installed (global, not project-specific)
if ! command -v tm-send >/dev/null 2>&1; then
  echo ""
  echo "WARNING: tm-send not found in PATH."
  echo "Install it (typically at ~/.local/bin/tm-send) before agents try to message each other."
  echo ""
fi

# 5. Per-role model assignment (extend this map as you add more roles)
#    Default: opus for everyone — pricier but high reasoning across the board.
declare -A MODELS=(
  [PO]="opus"
  [DEV]="opus"
  [QC]="opus"
  [CMO]="opus"
)

# 6. Launch Claude in each pane — model + matching subagent.
#    Agent name is the lowercased role (PO -> po, DEV -> dev, QC -> qc).
#    Requires the corresponding agent to exist in an installed plugin.
for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  MODEL="${MODELS[$ROLE]:-sonnet}"
  AGENT=$(echo "$ROLE" | tr '[:upper:]' '[:lower:]')
  tmux send-keys -t "$SESSION_NAME:0.$i" \
    "cd $PROJECT_ROOT && claude --model $MODEL --agent $AGENT" C-m
done

# 7. Wait for Claude to boot (SessionStart hook fires automatically)
echo "Waiting 15s for Claude instances to boot..."
sleep 15

# 8. Summary
echo ""
echo "{TEAM_NAME} ready."
echo "Roles: ${ROLES[*]}"
echo ""
echo "Attach: tmux attach -t $SESSION_NAME"
echo "Detach: Ctrl+B then D"
echo "Kill:   tmux kill-session -t $SESSION_NAME"
echo ""

# 9. Park cursor in pane 0 (typically PO)
tmux select-pane -t "$SESSION_NAME:0.0"
