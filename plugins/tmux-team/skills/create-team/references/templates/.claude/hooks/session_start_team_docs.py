#!/usr/bin/env python3
"""
SessionStart hook for tmux multi-agent teams.

What it does
------------
When Claude Code starts inside a tmux pane created by setup-team.sh:
  1. Detects the role from the pane option `@role_name` (PO/DEV/QC).
  2. Detects the team from `@team_name` or via the TEAM_CONFIGS map below.
  3. Reads team workflow + current board state (sprint, backlog).
  4. Injects them into hookSpecificOutput.additionalContext so the agent boots
     with full context (no extra tool calls needed).
  5. Logs a one-line systemMessage so the user sees what was loaded.

The role agent itself (e.g. po.md) is NOT injected here — the pane is launched
with `claude --agent <role>`, which already loads the agent definition as the
system prompt. Injecting it again would duplicate ~5KB of context for nothing.

If the pane is NOT a team pane (no @role_name set), the hook exits silently.
On any exception, exits 0 with a notice — never blocks session start.

Wire into .claude/settings.json:

    {
      "hooks": {
        "SessionStart": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session_start_team_docs.py",
                "timeout": 5
              }
            ]
          }
        ]
      }
    }
"""

from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
from pathlib import Path


# ----- config ----------------------------------------------------------------

# Map tmux session name -> team folder under docs/tmux/.
# Override this when you create more teams in the same project.
TEAM_CONFIGS = {
    "{SESSION_NAME}": "{TEAM_NAME}",
}

# Roles that should also receive the product backlog at session start.
ROLES_WITH_BACKLOG = {"PO"}

# Max chars per included file (cheap guard against runaway docs).
MAX_FILE_CHARS = 20_000


# ----- helpers ---------------------------------------------------------------

def project_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def in_tmux() -> bool:
    return bool(os.environ.get("TMUX"))


def tmux_pane() -> str | None:
    return os.environ.get("TMUX_PANE")


def run(cmd: list[str]) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=2, check=False)
        return out.stdout.strip() if out.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def detect_role(pane: str) -> str | None:
    return run(["tmux", "show-options", "-p", "-t", pane, "-qv", "@role_name"]) or None


def detect_team(pane: str) -> str | None:
    team = run(["tmux", "show-options", "-p", "-t", pane, "-qv", "@team_name"])
    if team:
        return team
    session = run(["tmux", "display-message", "-p", "-t", pane, "#S"])
    return TEAM_CONFIGS.get(session or "")


def read_capped(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if len(text) > MAX_FILE_CHARS:
        text = text[:MAX_FILE_CHARS] + f"\n\n... [truncated at {MAX_FILE_CHARS} chars]"
    return text


def latest_active_sprint(root: Path) -> Path | None:
    candidates = sorted(glob.glob(str(root / "docs/board/sprints/active/sprint-*.md")))
    return Path(candidates[-1]) if candidates else None


# ----- main ------------------------------------------------------------------

def build_payload() -> tuple[str, str] | None:
    if not in_tmux():
        return None
    pane = tmux_pane()
    if not pane:
        return None

    role = detect_role(pane)
    team = detect_team(pane)
    if not role or not team:
        return None

    root = project_root()
    team_dir = root / "docs" / "tmux" / team
    workflow = team_dir / "workflow.md"
    sprint = latest_active_sprint(root)
    backlog = root / "docs/board/backlog.md" if role in ROLES_WITH_BACKLOG else None

    sections: list[str] = []
    loaded: list[str] = []
    skipped: list[str] = []

    def attach(long_label: str, short_label: str, path: Path | None) -> None:
        if path is None:
            return
        text = read_capped(path)
        try:
            rel = str(path.relative_to(root))
        except ValueError:
            rel = str(path)
        if text is None:
            skipped.append(short_label)
            return
        sections.append(f"### {long_label} — `{rel}`\n\n{text}")
        loaded.append(short_label)

    attach("Team Workflow", "workflow", workflow)
    attach("Active Sprint Board", "sprint", sprint)
    if backlog is not None:
        attach("Product Backlog", "backlog", backlog)

    if not sections:
        return None

    header = (
        f"# Tmux Team Init — Role: **{role}** · Team: **{team}**\n\n"
        f"You are running as the **{role}** role in this tmux team. Your role "
        "agent definition is already loaded as the system prompt (via "
        f"`claude --agent {role.lower()}`). The following team-specific docs "
        "were pre-loaded by the SessionStart hook so you don't need to re-read "
        "them. Communicate with other panes via `tm-send <ROLE> \"...\"` only.\n"
    )
    additional_context = header + "\n" + "\n\n---\n\n".join(sections)

    # Compact one-line status.
    C_TAG, C_ROLE, C_DIM, C_OK, C_MISS, C_RESET = (
        "\033[36m", "\033[1;32m", "\033[2m", "\033[32m", "\033[33m", "\033[0m",
    )
    parts = [f"{C_TAG}[tmux-team]{C_RESET} {C_ROLE}{role}{C_RESET}{C_DIM}@{team}{C_RESET}"]
    if loaded:
        parts.append(f"{C_OK}✓ {', '.join(loaded)}{C_RESET}")
    if skipped:
        parts.append(f"{C_MISS}✗ {', '.join(skipped)}{C_RESET}")
    system_message = " ".join(parts)

    return additional_context, system_message


def main() -> int:
    try:
        result = build_payload()
    except Exception as exc:
        print(json.dumps({"systemMessage": f"[tmux-team] hook error: {exc!r} (skipped)"}))
        return 0

    if result is None:
        return 0  # not a team pane — silent no-op

    additional_context, system_message = result
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        },
        "systemMessage": system_message,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
