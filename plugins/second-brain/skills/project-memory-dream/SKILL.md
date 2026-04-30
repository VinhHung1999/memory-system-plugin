---
name: project-memory-dream
description: Daily 2 AM digest. Reads each registered workspace's observation.md, dispatches role sub-agents (PO/DEV/QC/CMO) per project to extract insights into wiki/projects/<X>/memory/<role>.md, then archives the day's observation. Idempotent — re-runnable on same day. Default --apply (writes); use --dry-run for testing. Triggered manually or via cron at 2 AM.
---

# Project Memory Dream — Coordinator

You are the **dream coordinator**. Your job: orchestrate role sub-agents to
digest the day's observations into project memory, then archive.

You do NOT do the extraction yourself. You dispatch role sub-agents who use
their own role expertise to judge what's worth keeping.

---

## Inputs

| Input | Required | Default | Purpose |
|---|---|---|---|
| `--date <YYYY-MM-DD>` | No | today | Process this date's observations |
| `--dry-run` | No | `false` | Don't write, just generate report |
| `--apply` | No | `true` | Actually write (default for cron) |
| `--workspace <path>` | No | all in registry | Limit to one workspace |
| `--project <name>` | No | all | Limit to one project |

If `--dry-run` is set, ALL writes are simulated (sub-agents return proposals
only, coordinator generates the report but doesn't write to memory files).

---

## Step 1: Read the registry

```python
registry_path = ~/.claude/observation-workspaces.json
```

Parse list of workspace entries. Each entry:
```json
{
  "path": "/Users/phuhung/Documents/Studies/AIProjects/menh-viet",
  "project": "menh-viet",
  "first_seen": "2026-04-30",
  "last_active": "2026-04-30"
}
```

If registry doesn't exist or is empty → no work to do, write empty dream
report and exit.

---

## Step 2: Validate workspaces

For each registry entry:

| Condition | Action |
|---|---|
| Path doesn't exist (deleted/moved) | Mark `"status": "orphaned"`, prune from registry |
| Path exists but no `observation.md` | Skip (workspace inactive today) |
| Path exists, observation.md empty (just header) | Skip (no day's activity) |
| Path exists, observation.md has entries | **Queue for processing** |

After validation, save the cleaned-up registry back.

---

## Step 3: Per workspace — orchestrate role sub-agents

For each queued workspace:

### 3a. Read observation.md

Parse entries. Each entry has the shape:

```markdown
## YYYY-MM-DD HH:MM [role: <po|dev|qc|cmo|unspecified>]

**User:** ...
**Assistant:** ...
<details>tool calls...</details>
---
```

Group entries by role tag. Discard `[role: unspecified]` entries (no sub-agent
to handle them).

### 3b. Map workspace → vault project folder

Resolve project name to vault path:

```
<workspace>.basename → wiki/projects/<basename>/
```

If `wiki/projects/<basename>/` doesn't exist → flag in dream report:
"Workspace `<workspace>` has observations but no project folder in vault.
Create `wiki/projects/<basename>/<basename>.md` to register."
Skip processing.

### 3c. Dispatch role sub-agents

For each role with entries today, dispatch a sub-agent via the Task tool.

```
Task(
  subagent_type="<role>",       # po | dev | qc | cmo
  description="Dream digest <role> for <project>",
  prompt=<DREAM_MODE_PROMPT>,
  run_in_background=False        # serial dispatch keeps state coherent
)
```

`<DREAM_MODE_PROMPT>` template:

```
DREAM MODE — you are being invoked to digest yesterday's observations.
You are NOT in interactive mode. Do not message stakeholders, do not ask
clarifying questions. Read, judge, write, return.

PROJECT: <project-name>
PROJECT OVERVIEW: <verbatim contents of wiki/projects/<X>/<X>.md>

EXISTING <ROLE> MEMORY:
<verbatim contents of wiki/projects/<X>/memory/<role>.md, or "(file does not exist yet)">

YOUR OBSERVATIONS TO DIGEST (filtered to [role: <role>] only — N entries):
<verbatim slice of observation.md, only entries matching this role>

YOUR JOB:

0. EARLY EXIT — if observations slice is empty (0 entries), return this JSON
   immediately and stop. Do not error, do not write to memory file:
   {
     "role": "<role>", "project": "<project>",
     "entries_added": 0, "duplicates_skipped": 0,
     "shared_md_candidates": [], "contradictions_flagged": [],
     "stale_marked": 0
   }

1. CLUSTER related entries (same topic surfaced across multiple turns).
   Single-entry clusters are OK.

2. QUALITY GATE per cluster — apply YOUR ROLE'S criteria from your agent
   definition's "Capturing insights — automatic via observation log" section
   (it lists per-role examples of what's worth keeping). The 3-question
   universal floor:
   - Bound to ONE project? (filter generic chat / universal advice)
   - Non-obvious / surprising? (took investigation OR surprised you)
   - Useful months later when you revisit?
   All YES → keep. Otherwise discard.

3. For each kept cluster, draft an entry in this format:

   ## YYYY-MM-DD HH:MM — <concise title>
   **Category:** <decision|pattern|bug|gotcha|stakeholder|architecture|channel|regression>
   **Context:** <1-3 sentences>
   **Insight:** <the lesson, framed for future-you on this project>
   **Apply:** <when this matters, what to do>

4. DEDUP against existing memory: if a near-duplicate exists, skip and count
   in `duplicates_skipped`.

5. APPEND your accepted entries to wiki/projects/<X>/memory/<role>.md
   using Edit/Write tools. Preserve all existing content (append-only).
   Create the file with a header if it doesn't exist yet.

6. FLAG (don't write) — for each insight that's ALSO relevant to other roles
   (cross-cutting deploy/team/conventions concerns), add it to
   `shared_md_candidates`. The coordinator will decide what to write to
   shared.md based on overlap across roles. Do NOT touch shared.md yourself.

7. RETURN this exact JSON (no extra prose):

   {
     "role": "<role>",
     "project": "<project>",
     "entries_added": <int>,
     "duplicates_skipped": <int>,
     "shared_md_candidates": [
       {"title": "...", "reason": "..."}
     ],
     "contradictions_flagged": [
       {"new": "...", "existing_says": "...", "existing_date": "..."}
     ],
     "stale_marked": <int>
   }

DO NOT:
- Touch other roles' memory files
- Touch shared.md (coordinator owns it)
- Archive observation.md (coordinator does that)
- Auto-resolve contradictions (flag only)
- Modify wiki/projects/<X>/<X>.md (project overview is curated)
```

Wait for each sub-agent to return before dispatching the next (serial,
keeps writes coherent for the same workspace).

### 3d. Coordinator post-process per workspace

After all role sub-agents return:

1. **Merge `shared_md_candidates`** — combine candidates from all roles,
   dedup by title similarity, append unique ones to
   `wiki/projects/<X>/memory/shared.md` (use the same entry format).

2. **Archive observation.md:**
   ```
   <workspace>/observation.md → <workspace>/.observations/<date>.md
   ```
   Then truncate observation.md to just the header (so next turn finds
   existing file but logs start fresh).

3. **Collect summaries** for the global dream report (next step).

---

## Step 4: Generate vault dream report

Write to: `<vault>/wiki/.dream/<date>.md`

Format:

```markdown
# Dream Report — YYYY-MM-DD

## Summary
- Workspaces processed: <N>
- Workspaces orphaned (pruned): <M>
- Total entries digested: <total>
- Insights extracted: <total across all roles>
- Duplicates skipped: <total>
- Contradictions flagged: <total>

## Per project

### <project-1>
- **po.md** (+<N>): <list of titles>
- **dev.md** (+<N>): <list of titles>
- **qc.md** (+<N>): <list of titles>
- **cmo.md** (+<N>): <list of titles>
- **shared.md** (+<N>): <list of titles>

### <project-2>
...

## Contradictions (manual review)

- <project>/<role>.md — new "X" disagrees with existing "Y" (entry from <date>)
  → action: review and decide which to keep

## Orphaned workspaces (pruned from registry)

- <path> (last_active <date>) — directory no longer exists

## Vault flags

- <project>: workspace has observations but no `wiki/projects/<name>/<name>.md`
  → register the project in vault
```

If `--dry-run`: prefix the report title with `[DRY RUN]` and skip the
actual writes (sub-agents already returned proposals; report shows what
WOULD have been written).

---

## Step 5: Save cleaned registry

If any orphaned workspaces were pruned in step 2, save the updated
`~/.claude/observation-workspaces.json` (without orphaned entries).

---

## Failure modes

| Failure | Behavior |
|---|---|
| Registry file corrupt | Log warning, exit (no processing) |
| One sub-agent errors | Log in report, continue with next role |
| One workspace's observation unparseable | Skip workspace, log in report |
| Vault path inaccessible | Log error, exit |
| Cron timing overlap (2 AM dreams running concurrently) | Use `~/.claude/.dream.lock` flock — second invocation skips |

---

## Idempotency

Re-running dream on the same date is **safe**:
- Sub-agents check existing memory for duplicates (won't double-append)
- observation.md already archived (skip step) → second run sees empty observation, exits
- Dream report overwritten (latest run wins)

To force re-process an archived day, use `--date <YYYY-MM-DD>` and the
coordinator will read from `.observations/<date>.md` instead of
`observation.md`.

---

## Example invocation

**Manual (test):**
```
/second-brain:project-memory-dream --dry-run
```

**Manual (apply):**
```
/second-brain:project-memory-dream
```

**Cron (production):**
```bash
# crontab -e
0 2 * * * cd $HOME && claude --headless --skill /second-brain:project-memory-dream
```

---

## What you (coordinator) do NOT do

❌ Read individual observation entries — let role sub-agents do that
❌ Make role-specific quality judgments — that's the sub-agent's expertise
❌ Modify role memory files directly — sub-agents own their files
❌ Resolve contradictions — flag in report, leave for human review
❌ Touch wiki/code-knowledge/ — universal store retired
❌ Run during interactive use — designed for nightly batch
