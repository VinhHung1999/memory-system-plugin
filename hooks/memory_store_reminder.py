#!/usr/bin/env python3
"""
Stop hook to remind Claude to store learnings after completing tasks.
Uses per-session counter: fires every Nth stop within a session (predictable, not random).
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
REMIND_EVERY_N_STOPS = 3  # Fire reminder every Nth stop (e.g., 3 = every 3rd turn)
MIN_TOOL_CALLS = 3  # Minimum tool calls in session to qualify as substantial
COOLDOWN_MINUTES = -1  # Disabled for tmux multi-session workflow
STATE_FILE = Path.home() / ".claude" / "memory_store_hook_state.json"


def load_state():
    """Load hook state from file."""
    if not STATE_FILE.exists():
        return {"invocations": [], "session_counters": {}, "last_reminder_tool_counts": {}}

    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            state.setdefault("session_counters", {})
            state.setdefault("last_reminder_tool_counts", {})
            return state
    except Exception:
        return {"invocations": [], "session_counters": {}, "last_reminder_tool_counts": {}}


def save_state(state):
    """Save hook state to file."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save state: {e}", file=sys.stderr)


def is_within_cooldown(state):
    """Check if we're within the cooldown period."""
    if COOLDOWN_MINUTES < 0:
        return False  # Cooldown disabled, always allow reminder
    if not state.get("invocations"):
        return False

    last_invocation = state["invocations"][-1]
    last_time = datetime.fromisoformat(last_invocation["timestamp"])
    cooldown_end = last_time + timedelta(minutes=COOLDOWN_MINUTES)

    return datetime.now() < cooldown_end


def count_session_invocations(state, session_id):
    """Count how many times hook was invoked for this session."""
    return sum(1 for inv in state.get("invocations", [])
               if inv.get("session_id") == session_id)


def count_tool_calls(input_data):
    """Count tool calls in the session to determine if it was substantial."""
    transcript_path = input_data.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        return 0
    try:
        with open(transcript_path, 'r') as f:
            content = f.read()
            # Count tool call markers in transcript
            return content.count('"tool_use"') + content.count('"tool_call"')
    except Exception:
        return 0


def should_remind(input_data, state):
    """Determine if we should remind Claude to store memory.
    Fires every Nth stop per session (counter-based, not random)."""

    # Safety check: Don't remind if stop hook is already active (prevents infinite loop)
    if input_data.get("stop_hook_active"):
        return False, "Stop hook already active"

    session_id = input_data.get("session_id", "default")
    counters = state.setdefault("session_counters", {})
    last_reminder_tool_counts = state.setdefault("last_reminder_tool_counts", {})

    # Increment counter for this session
    counters[session_id] = counters.get(session_id, 0) + 1
    current = counters[session_id]

    # Fire every Nth stop
    if current % REMIND_EVERY_N_STOPS != 0:
        return False, f"Stop #{current} in session — next reminder at #{(current // REMIND_EVERY_N_STOPS + 1) * REMIND_EVERY_N_STOPS}"

    # Count tool calls since last reminder (recent N turns only)
    total_tool_calls = count_tool_calls(input_data)
    last_count = last_reminder_tool_counts.get(session_id, 0)
    recent_tool_calls = total_tool_calls - last_count

    # Skip if recent turns didn't have enough tool calls
    if recent_tool_calls < MIN_TOOL_CALLS:
        return False, f"Stop #{current} — only {recent_tool_calls} tool calls in last {REMIND_EVERY_N_STOPS} turns (need {MIN_TOOL_CALLS})"

    # Update baseline so next check measures new turns only
    last_reminder_tool_counts[session_id] = total_tool_calls

    return True, f"Stop #{current} with {recent_tool_calls} recent tool calls — reminder fires"


def main():
    try:
        # Load input from stdin
        input_data = json.load(sys.stdin)

        # Load hook state
        state = load_state()

        # Determine if we should remind (also increments counter)
        should_remind_claude, reason = should_remind(input_data, state)

        # Always save state to persist the counter
        save_state(state)

        if should_remind_claude:
            # Record this invocation
            invocation = {
                "timestamp": datetime.now().isoformat(),
                "session_id": input_data.get("session_id"),
                "reminded": True
            }
            state.setdefault("invocations", []).append(invocation)
            save_state(state)

            # Block Claude from stopping and provide the reminder
            output = {
                "decision": "block",
                "reason": "Check if any hard-earned lessons or failure patterns warrant storage. Use skill /coder-memory-store for universal patterns (cross-project). Project-specific learnings are handled by built-in auto memory. Be selective — only store non-obvious bugs, surprising failures, or patterns you struggled with. If storing: store and report in 1 line. If not: say 'Nothing worth storing.' and move on. NO explanations or analysis."
            }
            print(json.dumps(output))
            sys.exit(0)

    except Exception as e:
        # On any error, don't block Claude from stopping
        print(f"Error in memory store hook: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
