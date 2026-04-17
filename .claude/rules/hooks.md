---
paths:
  - "plugins/*/hooks/**/*"
---

# Hook authoring

Hooks run inside the Claude Code process lifecycle. Each hook reads a JSON event on stdin and must emit valid JSON on stdout — an invalid or unexpected schema surfaces as a loud red error in the session, so be strict.

Only `memory-system` ships hooks today. The registration file is `hooks/hooks.json`; scripts live alongside it.

## Registration — `hooks.json`

```json
{
  "hooks": {
    "SessionStart":       [ { "hooks": [ { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/inject.sh",              "timeout": 5,  "statusMessage": "…" } ] } ],
    "UserPromptSubmit":   [ { "hooks": [ { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/prompt-reminder.sh",      "timeout": 3 } ] } ],
    "PreToolUse":         [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/pre-commit-gate.sh", "timeout": 5, "statusMessage": "…" } ] } ],
    "Stop":               [ { "hooks": [ { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/memory_store_reminder.py", "timeout": 10 } ] } ]
  }
}
```

- Always reference scripts with `${CLAUDE_PLUGIN_ROOT}/hooks/...` — never a machine-absolute path. The CLI expands it per-install.
- `timeout` is seconds. Keep it tight (3–5s) for hot-path hooks (`SessionStart`, `UserPromptSubmit`, `PreToolUse`). Python hooks that read the transcript can go up to ~10s.
- `matcher` on `PreToolUse` filters by tool name (`Bash`, `Read`, etc.) — always set it; an unscoped `PreToolUse` hook fires on every tool call and kills latency.
- `statusMessage` is optional. When set, it shows in the status line while the hook runs — good for hooks over ~1s.

## Do NOT register `PostCompact` to re-run `inject.sh`

`SessionStart` fires with a `:compact` subtype on compact completion, so `inject.sh` already re-injects. A separate `PostCompact` registration doubles the banner and prints a redundant "completed successfully" log. This was removed in v1.10.3 — do not add it back.

## Output schemas (by event)

Hooks MUST emit one JSON object to stdout. The allowed top-level keys depend on the event:

| Event | `systemMessage` | `hookSpecificOutput.additionalContext` | `decision` | Notes |
|---|---|---|---|---|
| `SessionStart` (incl. `:compact`) | ✓ | ✓ | — | Full banner + context. |
| `UserPromptSubmit` | ✓ | ✓ | — | Keep `additionalContext` tiny — it fires on every prompt. |
| `PreToolUse` | ✓ | ✓ | — | Return `{}` silently to not interfere. |
| `PostCompact` | ✓ | ✗ | — | `additionalContext` is **not allowed** — emitting it raises a schema error. Only `systemMessage` is valid. |
| `Stop` | — | — | ✓ | Use `{"decision": "block", "reason": "…"}` to nudge Claude to do something before stopping; omit to allow stop. |

`inject.sh` branches on `$HOOK_EVENT` specifically because of the `PostCompact` restriction — keep that branching pattern for any hook that may be called from multiple events.

When a hook has nothing to say, emit `{}` and exit 0. Never exit non-zero for "no action needed"; non-zero surfaces as an error.

## Reading stdin safely

Events arrive as JSON on stdin. Reach for Python for anything beyond a single field:

```bash
CMD=$(echo "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))' 2>/dev/null || echo "")
```

Why Python over `jq`: no external dependency, already on every user's machine, handles Unicode and quoting without surprises. Keep the pattern consistent across hooks.

For escaping string output back into JSON, use the helper from `inject.sh`:

```bash
escape_json() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"
}
```

Never hand-build JSON with string concatenation of user-facing messages — newlines and quotes in the message will break the output.

## State across invocations

Hooks are stateless between calls. When state is needed, persist to files under `~/.claude/`:

| File | Used by | Shape |
|---|---|---|
| `~/.claude/knowledge_updater_state.json` | `pre-commit-gate.sh`, `knowledge-updater` skill | `{ "<session_id>": "<ISO8601 timestamp>" }` — marks the session as having run the sync. |
| `~/.claude/memory_store_hook_state.json` | `memory_store_reminder.py` | `{ "invocations": [...], "session_counters": {...}, "last_reminder_tool_counts": {...} }` — per-session counter to fire every Nth stop. |

Rules for state files:

- Always guard read: missing file → return default, don't crash.
- Always guard write: `mkdir -p` the parent directory, write with `try/except` that prints to stderr but doesn't exit non-zero (`sys.exit(1)` would surface as an error).
- Session ID comes from the event JSON's `session_id` field; default to `"default"` when absent.

## Vault-dependent hooks

`inject.sh` and `prompt-reminder.sh` key off `SECOND_BRAIN_VAULT` (default `$HOME/Documents/Notes/HungVault/HungVault/brain2`). If the vault is missing, bail silently with `echo '{}'; exit 0` — users without brain2 still install the plugin, and a missing vault is not a failure.

## `memory_store_reminder.py` tuning

Defaults live at the top of the file:

```python
REMIND_EVERY_N_STOPS = 6   # fire every Nth stop
MIN_TOOL_CALLS = 10        # recent window must have ≥ this many tool calls
COOLDOWN_MINUTES = 15      # suppress if last reminder was within this window
```

Higher numbers = quieter. The transcript-tool-call counter reads `transcript_path` from the event and greps the JSONL for `"tool_use"` / `"tool_call"` — it must tolerate a missing transcript path (returns 0) rather than erroring.

When the reminder fires, it emits `{"decision": "block", "reason": "…"}` which tells Claude to do one more thing (check for store-worthy lessons) before stopping. The `reason` string is what Claude reads — keep it short and action-oriented, not a lecture.

## After editing a hook

1. Bump `plugins/<plugin>/.claude-plugin/plugin.json` `version`.
2. Add a CHANGELOG entry describing the behavior change (not the diff).
3. Tell the user to run `/reload-plugins` — confirm the hook count in the output matches expectations.
