---
name: marketing-kpi-scorecard-builder
description: |
  Build, validate, evaluate, and diagnose marketing KPIs at the executive
  scorecard level. Three modes: BUILD (turn raw tactical metrics into a
  board-ready 8-12 KPI scorecard with traffic-light zones), VALIDATE
  (3-filter check on a single proposed KPI: strategic alignment +
  measurability + actionability), and DIAGNOSE (root-cause walkthrough
  for a red-zone KPI). Distinguishes activity metrics (impressions,
  clicks, engagement) from business-impact metrics (CLV, NRR, churn,
  market share, advocacy) and reframes accordingly. Use when CMO needs
  to design a marketing KPI system, prep a board scorecard, validate a
  proposed metric, run weekly KPI review, or diagnose a missed KPI.
  Auto-trigger on phrases like "marketing KPIs", "board scorecard",
  "executive metrics", "KPI design", "validate this metric", "weekly
  KPI review", "diagnose KPI miss", "marketing dashboard for board",
  "performance scorecard", "kill activity metrics", "north-star metric".
---

# Marketing KPI Scorecard Builder

## What this does

Three modes for the full lifecycle of executive marketing KPIs:

### Mode 1 — BUILD (default)
Turn a list of raw tactical/operational metrics into a board-ready scorecard:
- Apply 4-layer design pattern (Strategic Objective → Performance Category → Specific Metric → Tracking Mechanism)
- Strip activity-only metrics (clicks, impressions, engagement, MQLs without conversion)
- Surface business-impact metrics (CLV, NRR, churn reduction, market share, advocacy/NPS, brand health)
- Auto-zone every metric Green/Yellow/Red based on variance vs target
- Output: 1-page scorecard + per-zone action prompts

### Mode 2 — VALIDATE
Single-KPI 3-filter check before adding to the scorecard:
- **Strategic alignment**: does this KPI trace upward to a business objective?
- **Measurability**: can you collect it reliably without heroic effort?
- **Actionability**: do you know the corrective move when it dips?
Output: pass/fail per filter + revision suggestion if fail.

### Mode 3 — DIAGNOSE
When a KPI is in the red zone, walk the root-cause detective method:
1. Gather evidence (don't assume)
2. Break aggregate to channel/campaign level (channel-average masks underperformers)
3. Identify pattern (trend, segment, period)
4. Conclude root cause vs symptom
5. Suggest fix targeting cause, not symptom
Output: structured diagnosis + corrective action with success indicator.

**The core problem this solves:** Most marketing dashboards are **tactical** (impressions, CTR, cost per click) — useful for marketing managers, but the CFO and board discount them. Executive-grade scorecards need **business-impact metrics** with traffic-light zones and root-cause analysis. Most CMOs don't have a rigorous framework, so they default to "report what we measure" instead of "report what proves the business is winning."

## When to invoke this skill

- Designing a marketing KPI system (annual planning, post-pivot)
- Pre-board-meeting prep (build the scorecard slide)
- Validating a proposed KPI before adding to dashboard
- Weekly/mid-quarter KPI review (zone metrics + prioritize attention)
- Diagnosing a KPI miss (figure out cause vs symptom)
- After a marketing miss → root-cause analysis
- Asked "what KPIs should we report to the board?" / "is this metric strategic?" / "why did this KPI miss?"

**Skip when:**
- Question is about positioning or vision (use other CMO skills)
- Question is about cross-functional translation of an insight (use translation matrix)
- Tactical campaign-level optimization (use ab-test-designer or similar)
- Pure attribution methodology (different problem)

## When NOT to use

- Question is about which marketing channel to invest in (different decision)
- Brand identity / messaging work
- Customer research design
- Generic "what is a KPI" educational question

## Workflow

### For BUILD mode
1. Capture inputs — list of current metrics + their targets + strategic objectives the marketing org is responsible for
2. Run `scripts/build_scorecard.py --metrics <csv|json> --objectives "<list>"`
3. Read `references/kpi-design-framework.md` for the 4-layer pattern + activity-vs-impact translation patterns
4. Apply `templates/board-scorecard.md` for 1-page exec format
5. Schedule recurring weekly review using `templates/weekly-kpi-review.md`

### For VALIDATE mode
1. Capture the proposed KPI + its claimed strategic objective
2. Run `scripts/validate_kpi.py --kpi "<text>" --objective "<text>"`
3. Read filter results + revision suggestion

### For DIAGNOSE mode
1. Capture the red-zone KPI + its current/target/trend
2. Run `scripts/diagnose_red_zone.py --kpi "<text>" --current <num> --target <num> --evidence "<json>"` (interactive walkthrough if no evidence flag)
3. Read structured diagnosis + corrective action

## Running the scripts

```bash
# Build mode
python3 /Users/phuhung/coursera/.claude/skills/marketing-kpi-scorecard-builder/scripts/build_scorecard.py \
  --metrics metrics.csv \
  --objectives "Revenue growth 25%, Retention >90%, Brand awareness +15pp"

# Validate mode (single KPI)
python3 /Users/phuhung/coursera/.claude/skills/marketing-kpi-scorecard-builder/scripts/validate_kpi.py \
  --kpi "Email open rate" \
  --objective "Increase trial-to-paid conversion by 20% in Q3"

# Diagnose mode (red-zone KPI)
python3 /Users/phuhung/coursera/.claude/skills/marketing-kpi-scorecard-builder/scripts/diagnose_red_zone.py \
  --kpi "Paid search conversion rate" \
  --current 2.1 --target 3.5 \
  --evidence '{"channels": {"google_search": 1.4, "bing": 3.8}, "trend": "declining 4 weeks"}'
```

If `python3` crashes with pyexpat error, fall back to `python3.13`.

## Output philosophy

**The scorecard must answer 4 questions for the board/CEO/CFO:**
1. **Are we winning?** (one-line top status, traffic-light)
2. **What 3 metrics matter most this quarter?** (the executive shortlist)
3. **Where do we need to act?** (red-zone metrics + recommended corrective action)
4. **What's our KPI hygiene?** (any orphan metrics that don't trace to a business objective)

DO NOT produce vanity-metric-heavy dashboards (impressions, click-through, engagement rate as TOP metrics). The script enforces business-impact framing.

DO NOT produce "everything is yellow" outputs. Force the calibration: if every KPI is between 80% and 120% of target, the targets are wrong, not the performance.

## References (load on demand)

- `references/kpi-design-framework.md` — 4-layer KPI design pattern + 4-pillar scaling framework + activity-vs-impact translation table + board metric library (CLV, NRR, churn, market share, advocacy, brand health, share of voice)
- `templates/board-scorecard.md` — 1-page exec format with traffic-light zones
- `templates/weekly-kpi-review.md` — recurring ritual template (Green/Yellow/Red zoning, action prompts, fixed columns)

## Sources

Built from TWO Coursera courses (Hurix Digital, 2025):

**Set and Evaluate Winning Marketing KPIs (this course's core content):**
- Module 1 Video: "Why Strategic KPIs Drive Marketing Success"
- Module 1 Reading: "KPI Framework Fundamentals for Marketing Performance"
- Module 1 Video: "Strategic Alignment Process for Marketing KPIs"
- Module 2 Reading: "Mid-Quarter Evaluation Methods for Marketing Performance"
- Module 2 Video: "Performance Analysis Techniques for Campaign Optimization"
- Module 2 Video: "Data Collection and Analysis Workflow"

**CMO Excellence (executive-layer board-metric framework):**
- Module 3 Video: "Measuring Marketing's True Impact"
- Module 3 Video: "Scaling Marketing Impact Across the Enterprise"
