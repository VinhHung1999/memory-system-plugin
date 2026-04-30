# {TEAM_NAME} — Tmux Multi-Agent Team Workflow

<context>
A tmux-based multi-agent team. Each role is a Claude Code AI agent in its own
tmux pane, started with `claude --agent <role>`. Board and task management
uses Markdown files in Obsidian Kanban format — agents read/edit MD files
directly, no MCP server or database needed.

This team runs with **PO + DEV + QC + CMO** — a 4-role team focused on
shipping quality work alongside go-to-market thinking. PO handles backlog
and acceptance, DEV handles spec-to-verified-delivery, QC handles independent
black-box testing, CMO handles GTM strategy / positioning / demand. No
separate Scrum Master — PO + DEV + CMO coordinate the flow themselves
through the board and tm-send.
</context>

---

## Agent Roles

| Role | Pane | Plugin | Purpose |
|------|------|--------|---------|
| PO   | 0    | `po`   | Backlog management, priorities, stakeholder liaison |
| DEV  | 1    | `dev`  | Spec → TDD implementation → self-review → verification (any stack) |
| QC   | 2    | `qc`   | Black-box testing, acceptance verification, regression checks |
| CMO  | 3    | `cmo`  | GTM strategy, positioning, market sizing, demand-gen, brand & messaging |
| Boss | Outside tmux | — | Stakeholder: gives sprint goals, reviews completed work |

Each role's universal behavior is defined by its subagent in the corresponding
plugin (e.g. PO behavior comes from the `po` plugin's `agents/po.md`). This
`workflow.md` adds the **team-specific** layer: where the board lives and what
conventions this project follows.

---

## CRITICAL: Pane Detection

**NEVER use `tmux display-message -p '#{pane_index}'`** — that returns the active
cursor pane, not the pane the command runs in.

**Always use `$TMUX_PANE`:**

```bash
echo $TMUX_PANE
tmux list-panes -a -F '#{pane_id} #{pane_index} #{@role_name}' | grep $TMUX_PANE
```

The SessionStart hook uses `@role_name` (set by `setup-team.sh`) to identify the role.

---

## Communication Protocol — `tm-send`

Currently the team has only PO, so cross-pane messaging is rare. When more roles
are added, use `tm-send` for ALL inter-pane messages:

```bash
tm-send <ROLE> "<FROM> -> <TO> [HH:MM]: message"
```

**Never** use raw `tmux send-keys` for messages — it bypasses the routing
convention and breaks `@role_name` resolution.

---

## Board Management — Markdown Files

Board data lives in `docs/board/` as Obsidian Kanban format markdown files.
PO reads and edits these MD files directly using Read/Edit tools.

### File Structure

```
docs/board/
  backlog.md                     — product backlog (P0/P1/P2/P3 sections)
  sprints/active/sprint-{N}.md   — active sprint kanban board
  sprints/archive/sprint-{N}.md  — completed sprints
```

### Card Format

```
- [ ] **[ID]** Task title
      **Priority:** P1 · **Points:** 3 · **Assignee:** TBD · **Status:** todo
      **Description:**
      Description text...
      **Acceptance:**
      - [ ] Criterion 1
      - [ ] Criterion 2
      **Notes:**
      YYYY-MM-DD PO: Progress note...
```

### Common Operations (PO)

| Action | How |
|--------|-----|
| View backlog | Read `docs/board/backlog.md` |
| Create backlog item | Edit `backlog.md` — add card under priority section |
| Update priority | Edit `backlog.md` — move card between P0/P1/P2/P3 sections |
| View active sprint | Read `docs/board/sprints/active/sprint-{N}.md` |
| Create sprint | Create new `sprints/active/sprint-{N}.md` from template |
| Add item to sprint | Move card from `backlog.md` to sprint's `## Todo` |
| Complete sprint | Update metadata, move file to `sprints/archive/` |

---

## Sprint Workflow (PO + DEV + QC mode)

PO owns backlog + acceptance. DEV owns the technical path from spec to
self-verified delivery. QC is the independent black-box check before PO
acceptance. Boss is the external stakeholder.

```
1. Boss → PO: Sprint Goal / feature request
2. PO: Adds/updates items in backlog.md, prioritizes (P0–P3)
3. PO: Creates sprint-{N}.md, moves selected items to ## Todo
4. PO → DEV (via tm-send): Sprint scope ready
5. DEV: Picks task, moves to ## In Progress
6. DEV: Spec (if needed) → TDD implementation → self-review (karpathy + simplify)
        → verifies feature works end-to-end
7. DEV → QC (via tm-send): Task ready for testing
8. QC: Invokes /qc:qc-mobile-testing or /qc:qc-web-testing, runs through
       acceptance criteria + edge cases + error paths
9a. QC finds issues → tm-send DEV with bug report → DEV fixes → step 7 again
9b. QC passes → tm-send PO: ready for acceptance
10. PO: Verifies acceptance, marks task `- [x]` Done in sprint MD
11. End of sprint → PO → Boss: Review whole sprint at once
12. Boss confirms → PO archives sprint, plans next
```

Retrospectives (if any) are handled informally — PO captures lessons in
`memory/po.md`, DEV in `memory/dev.md`, QC in `memory/qc.md`, cross-cutting
team observations in `memory/shared.md` of each project.

---

## Files in This Team Folder

```
docs/tmux/{TEAM_NAME}/
├── workflow.md             # This file
└── setup-team.sh           # Launches the tmux session (one pane per role)
```

Board files live in `docs/board/`. Specs (when needed) go in `docs/specs/`.
