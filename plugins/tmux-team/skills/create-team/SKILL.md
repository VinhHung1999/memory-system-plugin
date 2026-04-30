---
name: create-team
description: Scaffold a multi-agent tmux Scrum team into the current project. Creates docs/tmux/<team>/ (workflow + setup script), docs/board/ (backlog + sprints folders), .claude/hooks/session_start_team_docs.py (role detection + context injection), and .claude/settings.json (hook registration). After setup, running setup-team.sh launches a tmux session with one Claude pane per role, each pre-loaded with team workflow + role agent + current board state. Use when the user wants to start a new tmux team for an existing project. Trigger phrases (VN+EN) - "tạo team", "setup team", "scrum team", "tmux team", "create team", "init team".
---

# Create Tmux Team

Scaffolds a multi-agent Scrum team into the current project. After this skill runs, the user has everything needed to launch a tmux session with one Claude pane per role (PO, DEV, QC, CMO by default), each pane auto-loaded with the team workflow + the role's agent definition (from the matching plugin: `po`, `dev`, `qc`, `cmo`) + current board state via a SessionStart hook.

## Prerequisites Check

Before scaffolding, verify:

1. **`tmux` is installed** — `command -v tmux`
2. **`tm-send` is installed at `~/.local/bin/tm-send`** — global tool for inter-pane messaging. If missing, instruct the user to install it (point them to `tmux-messenger` skill or manual install) BEFORE running `setup-team.sh`. Don't block scaffolding — just warn.
3. **The role plugins are installed** — `po`, `dev`, `qc`, `cmo`. Each pane needs its matching plugin's agent. If a plugin is missing, warn the user that pane will boot without the role agent definition.

## Inputs to Gather

Ask the user (or infer from context):

| Input | Default | Notes |
|---|---|---|
| Project root | `pwd` | Absolute path. Where to scaffold. |
| Team name | `scrum-team` | Folder under `docs/tmux/`. Use kebab-case. |
| Tmux session name | `scrum_team` | Used by `setup-team.sh`. Must match TEAM_CONFIGS in hook. |
| Roles | `PO DEV QC CMO` | Default 4-role team (ship-with-quality trio + GTM/marketing strategy). Order sets pane index. |
| Per-role model | `PO=opus DEV=opus QC=opus CMO=opus` | Default: opus across the board (high reasoning). Extend the MODELS map in `setup-team.sh` when adding more roles. |

If the user hasn't said, propose defaults and confirm before writing files.

## Template Structure (Mirrors Target Project)

The `references/templates/` folder mirrors exactly what gets scaffolded into the project,
so you can see at a glance which file lands where:

```
references/templates/
├── .claude/
│   ├── hooks/
│   │   └── session_start_team_docs.py    → {project}/.claude/hooks/...
│   └── settings.json                      → {project}/.claude/settings.json (merge)
└── docs/
    ├── board/
    │   ├── backlog.md                     → {project}/docs/board/backlog.md
    │   └── sprints/
    │       ├── active/.gitkeep            → {project}/docs/board/sprints/active/
    │       ├── archive/.gitkeep           → {project}/docs/board/sprints/archive/
    │       └── sprint-template.md         (kept in templates only — used by PO to seed new sprints)
    └── tmux/
        └── _team/                         → {project}/docs/tmux/{TEAM_NAME}/
            ├── workflow.md
            └── setup-team.sh              (chmod +x after copy)
```

The `_team` directory is a placeholder — when scaffolding, rename it to the
actual team name the user chose.

## Steps

1. **Confirm inputs** with the user.
2. **Walk `references/templates/`** and replicate the structure into the project:
   - Each path under `references/templates/` maps directly to a path under `{project}/` —
     copy the file, substitute placeholders (`{TEAM_NAME}`, `{SESSION_NAME}`,
     `{ROLES}`, `{PROJECT_NAME}`), then write.
   - Rename `references/templates/docs/tmux/_team/` → `{project}/docs/tmux/{TEAM_NAME}/`.
   - `references/templates/docs/board/sprints/sprint-template.md` is NOT copied — keep it
     in templates only and use it later when PO creates `sprint-1.md`. Just
     create empty `sprints/active/` and `sprints/archive/` directories.
3. **Special handling:**
   - `.claude/settings.json` — if the project already has one, merge the
     `SessionStart` hook entry instead of overwriting.
   - `setup-team.sh` — `chmod +x` after writing.
   - `session_start_team_docs.py` — `chmod +x` after writing.
4. **Verify scaffolding** — list created files, confirm executable bits set.
5. **Print next steps** for the user:
   - Install missing prerequisites if any (`tm-send`, role plugins).
   - Run `bash docs/tmux/{TEAM_NAME}/setup-team.sh` to launch the team.
   - Attach via `tmux attach -t {SESSION_NAME}`.
   - First action: PO pane defines the first sprint goal.

## Idempotency

- If the project already has `docs/tmux/{team-name}/` → ask before overwriting.
- If `.claude/settings.json` exists with a SessionStart hook → merge, don't overwrite.
- If `docs/board/` already has content → don't touch existing files; only create what's missing.

## Templates

All templates live in `references/templates/` next to this SKILL.md. Read them with the Read tool, substitute placeholders, then Write to the project. Placeholders use `{CURLY_BRACE}` style:

- `{TEAM_NAME}` — kebab-case folder name (e.g. `scrum-team`)
- `{SESSION_NAME}` — tmux session name (e.g. `scrum_team`)
- `{ROLES}` — space-separated role list (e.g. `PO DEV QC CMO`)
- `{PROJECT_ROOT}` — usually leave as-is so the script reads it from env

## After Scaffolding

Tell the user:

> Team scaffolded at `docs/tmux/{team-name}/`. To launch:
>
> ```bash
> bash docs/tmux/{team-name}/setup-team.sh
> tmux attach -t {session-name}
> ```
>
> Each pane will boot with the team workflow + role agent + current board state pre-loaded via the SessionStart hook. PO pane is the entry point — give it a sprint goal to start.

Do NOT auto-run `setup-team.sh` — the user reviews the scaffolded files first.
