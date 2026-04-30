# Weekly Marketing KPI Review — Week of ${DATE}

**Attendees:** CMO + marketing leads
**Duration:** 30 minutes
**Cadence:** Weekly (every Monday or Friday — pick one and stick to it)
**Pre-read:** auto-generated scorecard sent 24h prior (see `templates/board-scorecard.md`)

---

## Agenda

### 1. Traffic-light status (5 min)
Walk the 8-12 KPI scorecard. Confirm zone classifications. No discussion of fixes yet — just confirm what is GREEN / YELLOW / RED.

### 2. Red-zone deep dive (15 min)
For each red-zone metric:
- **Root cause** (symptom vs cause — use `scripts/diagnose_red_zone.py` for new red metrics)
- **Corrective action** (specific lever, not "do better")
- **Owner + deadline** (single named human + date)
- **Success indicator** (what value moves it back to yellow/green by when)

### 3. Yellow-zone watch (5 min)
For each yellow:
- **Likely trajectory** (recovering / stable / declining)
- **Pre-stage corrective action** so it doesn't go red — what would we do, on what trigger?

### 4. New decisions (5 min)
- Any new KPI to add (validate first via `scripts/validate_kpi.py`)
- Any KPI to retire (orphan / vanity / duplicate)
- Any target re-baselining (if "everything is yellow" pattern emerges, targets are wrong, not performance)

---

## Outputs (recorded)
- Action items per red KPI with owner + due date
- Yellow-zone watch list
- Decisions on KPI changes (additions, retirements, re-baselines)

---

## Anti-patterns (DO NOT)
- **Status update without decisions.** This is a working session, not a readout.
- **Optimize green-zone metrics.** Waste of attention. Document the playbook so it can be replicated.
- **Retro on individual campaigns.** Do that in campaign post-mortems. This meeting is about the KPI system.
- **Re-debate KPI definitions.** Definitions are locked in the KPI documentation template. If a definition is broken, that's a separate decision in section 4.
- **Skip diagnosis, jump to action.** Symptom-treatment is the most common failure mode. Use the 4-step root-cause method.

---

## Success indicator (for the meeting itself)
Every red KPI from last week's review is now yellow or green, OR has a corrective action with measurable progress. If neither is true, the meeting is broken: the team is reporting status instead of running interventions.

---

## Roll-forward template

Copy this section week over week so trends across reviews are visible.

| Week | RED count | YELLOW count | GREEN count | Red KPIs that improved | Red KPIs that stayed red |
|---|---|---|---|---|---|
| ${WEEK_N-2} | | | | | |
| ${WEEK_N-1} | | | | | |
| ${WEEK_N}   | | | | | |
