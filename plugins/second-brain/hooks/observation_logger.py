#!/usr/bin/env python3
"""
Stop hook: append latest user prompt + assistant response to
`observation.md` at the workspace root. Auto-creates the file with a
header if it doesn't exist.

Search order for observation.md:
  1. Walk up from CLAUDE_PROJECT_DIR / cwd looking for an existing file.
  2. If not found, create it at CLAUDE_PROJECT_DIR (or cwd) with a header.

Format (medium scope):
  • Timestamp + role tag (from tmux @role_name when available)
  • User message verbatim
  • Assistant response verbatim
  • Tool calls collapsed in <details>

Designed to feed the daily 2 AM dream skill, which reads observation.md
to extract insights into project memory and consolidate the wiki.
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ----- Config ---------------------------------------------------------------

# Walk up to find observation.md (cwd → project root).
MAX_WALK_UP = 6  # Safety: don't walk above this many parents.

# Registry of workspaces with active observation.md files.
# Read by the daily dream skill to know which workspaces to process.
WORKSPACE_REGISTRY = Path.home() / ".claude" / "observation-workspaces.json"


# ----- Helpers --------------------------------------------------------------

def find_or_create_observation_file():
    """
    Walk up from cwd / CLAUDE_PROJECT_DIR looking for observation.md.
    If not found, create it at CLAUDE_PROJECT_DIR (or cwd) with a header.
    Skips creation if cwd is HOME (don't pollute home dir).
    """
    start = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    home = Path.home().resolve()

    # Refuse to operate at HOME — too broad, would pollute everything.
    if start == home:
        return None

    # Walk up looking for existing file
    current = start
    for _ in range(MAX_WALK_UP):
        candidate = current / "observation.md"
        if candidate.is_file():
            return candidate
        if current == current.parent or current == home:
            break
        if (current / ".git").exists() and current != start:
            # Hit project root via .git — create observation.md here
            return create_observation_file(current)
        current = current.parent

    # No observation.md found anywhere walking up — auto-create at start
    return create_observation_file(start)


def create_observation_file(path):
    """Create observation.md at the given dir with a header. Returns the path or None."""
    target = path / "observation.md"
    if target.is_file():
        return target
    project_name = path.name
    today = datetime.now().strftime("%Y-%m-%d")
    header = (
        f"---\n"
        f"kind: observation-log\n"
        f"project: {project_name}\n"
        f"created: {today}\n"
        f"---\n\n"
        f"# Observation Log — {project_name}\n\n"
        f"Auto-appended by `observation_logger` Stop hook (in second-brain plugin).\n"
        f"Each entry is one Claude turn: user prompt + assistant response + tool summaries.\n"
        f"The daily 2 AM dream skill reads this to extract insights into project memory\n"
        f"(`wiki/projects/<project>/memory/<role>.md`) and then archives this file to\n"
        f"`.observations/<YYYY-MM-DD>.md`.\n\n"
        f"To opt out for this project, delete this file AND add `observation.md` to\n"
        f"`.gitignore` if you don't want it auto-recreated next session.\n\n"
        f"---\n\n"
    )
    try:
        target.write_text(header, encoding="utf-8")
        return target
    except OSError as e:
        print(f"observation_logger: failed to create {target}: {e}", file=sys.stderr)
        return None


def detect_role():
    """Detect role from tmux @role_name pane option, or None."""
    pane = os.environ.get("TMUX_PANE")
    if not pane:
        return None
    try:
        out = subprocess.run(
            ["tmux", "show-options", "-p", "-t", pane, "-qv", "@role_name"],
            capture_output=True, text=True, timeout=2, check=False,
        )
        return out.stdout.strip().lower() or None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def read_transcript(transcript_path):
    """Read transcript JSONL and return list of message events."""
    if not transcript_path or not os.path.exists(transcript_path):
        return []
    events = []
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return events


def extract_latest_exchange(events):
    """
    Pull the most recent user prompt + the assistant's response that followed.
    Returns (user_text, assistant_text, tool_summaries) — any may be None/[].
    """
    user_text = None
    assistant_text_parts = []
    tool_summaries = []

    # Find last user message index
    last_user_idx = None
    for i, ev in enumerate(events):
        msg = ev.get("message") or ev
        role = msg.get("role")
        if role == "user":
            last_user_idx = i

    if last_user_idx is None:
        return None, None, []

    # Extract user content
    user_msg = (events[last_user_idx].get("message") or events[last_user_idx])
    user_content = user_msg.get("content")
    if isinstance(user_content, str):
        user_text = user_content
    elif isinstance(user_content, list):
        # Anthropic-style content blocks
        parts = []
        for block in user_content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif "text" in block:
                    parts.append(block.get("text", ""))
        user_text = "\n".join(p for p in parts if p)

    # Walk forward from user message, collect assistant text + tool summaries
    for ev in events[last_user_idx + 1 :]:
        msg = ev.get("message") or ev
        role = msg.get("role")
        if role == "user":
            break  # Next user turn — stop
        if role != "assistant":
            continue
        content = msg.get("content")
        if isinstance(content, str):
            assistant_text_parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    assistant_text_parts.append(block.get("text", ""))
                elif btype == "tool_use":
                    tool_name = block.get("name", "tool")
                    tool_input = block.get("input", {}) or {}
                    summary = summarize_tool_call(tool_name, tool_input)
                    if summary:
                        tool_summaries.append(summary)

    assistant_text = "\n".join(p for p in assistant_text_parts if p).strip()
    return user_text, assistant_text or None, tool_summaries


def summarize_tool_call(name, input_obj):
    """One-line summary of a tool call (medium scope — no full inputs/outputs)."""
    name_lower = (name or "").lower()
    if name_lower == "bash":
        cmd = (input_obj.get("command") or "").splitlines()[0]
        if len(cmd) > 80:
            cmd = cmd[:77] + "..."
        return f"`Bash` — `{cmd}`"
    if name_lower in ("read", "edit", "write"):
        path = input_obj.get("file_path") or input_obj.get("path") or ""
        return f"`{name}` — `{path}`"
    if name_lower in ("grep", "glob"):
        pattern = input_obj.get("pattern") or ""
        return f"`{name}` — `{pattern}`"
    if name_lower == "task":
        desc = input_obj.get("description") or ""
        return f"`Task` — `{desc}`"
    if name_lower == "webfetch":
        url = input_obj.get("url") or ""
        return f"`WebFetch` — `{url}`"
    if name_lower == "websearch":
        query = input_obj.get("query") or ""
        return f"`WebSearch` — `{query}`"
    return f"`{name}`"


def format_entry(timestamp, role, user_text, assistant_text, tool_summaries):
    """Build the markdown entry to append."""
    role_tag = f"[role: {role}]" if role else "[role: unspecified]"
    parts = [f"## {timestamp} {role_tag}", ""]

    if user_text:
        parts.append("**User:**")
        parts.append("")
        # Quote-prefix user text
        for line in user_text.splitlines():
            parts.append(f"> {line}" if line else ">")
        parts.append("")

    if assistant_text:
        parts.append("**Assistant:**")
        parts.append("")
        parts.append(assistant_text)
        parts.append("")

    if tool_summaries:
        parts.append(f"<details>")
        parts.append(f"<summary>Tool calls ({len(tool_summaries)})</summary>")
        parts.append("")
        for s in tool_summaries:
            parts.append(f"- {s}")
        parts.append("")
        parts.append("</details>")
        parts.append("")

    parts.append("---")
    parts.append("")
    return "\n".join(parts)


def append_atomic(target_path, content):
    """Append content to target_path. Best-effort atomicity via single write call."""
    try:
        with open(target_path, "a", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError as e:
        print(f"observation_logger: failed to append: {e}", file=sys.stderr)
        return False


def register_workspace(obs_file):
    """
    Insert workspace into ~/.claude/observation-workspaces.json (if new) or
    bump last_active (if existing). Used by the daily dream skill to discover
    workspaces with active observation logs.
    """
    workspace = obs_file.parent.resolve()
    project = workspace.name
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        WORKSPACE_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        if WORKSPACE_REGISTRY.is_file():
            with open(WORKSPACE_REGISTRY, "r") as f:
                data = json.load(f)
        else:
            data = []
    except (OSError, json.JSONDecodeError):
        data = []

    # Match by path; bump last_active if existing
    for entry in data:
        if entry.get("path") == str(workspace):
            entry["last_active"] = today
            entry["project"] = project
            break
    else:
        data.append({
            "path": str(workspace),
            "project": project,
            "first_seen": today,
            "last_active": today,
        })

    try:
        with open(WORKSPACE_REGISTRY, "w") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        print(f"observation_logger: failed to update registry: {e}", file=sys.stderr)


# ----- Main -----------------------------------------------------------------

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Bad input — silent skip

    # Skip if hook is being re-entered (safety)
    if input_data.get("stop_hook_active"):
        sys.exit(0)

    # Find or create observation.md at project root
    obs_file = find_or_create_observation_file()
    if obs_file is None:
        sys.exit(0)  # cwd is HOME or write failed — skip silently

    # Read transcript and extract latest exchange
    transcript_path = input_data.get("transcript_path")
    events = read_transcript(transcript_path)
    user_text, assistant_text, tool_summaries = extract_latest_exchange(events)

    # Skip if nothing meaningful to append
    if not user_text and not assistant_text and not tool_summaries:
        sys.exit(0)

    # Build entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    role = detect_role()
    entry = format_entry(timestamp, role, user_text, assistant_text, tool_summaries)

    # Append
    if append_atomic(obs_file, entry):
        register_workspace(obs_file)
    sys.exit(0)


if __name__ == "__main__":
    main()
