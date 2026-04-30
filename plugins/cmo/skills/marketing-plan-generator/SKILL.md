---
name: marketing-plan-generator
description: |
  Generate a complete IE Business School-style marketing plan with the
  required 4 sequential parts in strict order: Part 1 ANALYSIS (5Cs
  external + internal differentiation/lifecycle + SWOT 2x2 matrix),
  Part 2 STRATEGY (financial objectives + non-financial + customer
  attraction-vs-retention split + STP target segment + positioning),
  Part 3 MARKETING MIX (Product/Price/Channel/Communication 4P
  decisions traced to strategy), Part 4 EXPECTED RESULTS (metrics
  one-to-one with Part 2 objectives + budget total). Enforces the IE
  rule that EVERY metric in Part 4 must mirror an objective in Part 2,
  every 4P tactic in Part 3 must trace to a Part 2 strategic choice,
  and every Part 2 decision must be backed by Part 1 evidence. Use
  when CMO needs to write annual marketing plan, quarterly plan,
  product launch plan, post-pivot plan, or budget defense for board.
  Auto-trigger on phrases like "marketing plan", "annual marketing plan",
  "launch plan", "GTM plan", "plan marketing năm", "marketing roadmap",
  "lên plan marketing", "marketing plan structure", "SWOT analysis",
  "5Cs analysis".
---

# Marketing Plan Generator (IE 4-Part Structure)

## What this does

Generates a complete IE-methodology marketing plan with strict 4-part structure. Three modes:

### Mode 1 — FULL PLAN (default)
Generate complete 4-part plan from inputs:
- Part 1 ANALYSIS: 5Cs + Internal analysis + SWOT
- Part 2 STRATEGY: financial + non-financial objectives + customer attraction/retention split + target segment + positioning
- Part 3 MIX: 4Ps each traced to Part 2 strategic choices
- Part 4 RESULTS: metrics mirroring Part 2 objectives + budget

### Mode 2 — VALIDATE existing plan
Audit a draft plan against IE methodology rules:
- Does Part 4 mirror Part 2 one-to-one? (every objective has a metric)
- Does Part 3 trace to Part 2? (every 4P tactic backs a strategic choice)
- Does Part 2 trace to Part 1? (every decision has analytical evidence)
- Are constraints (budget + sales target) named at top of every section?

### Mode 3 — SINGLE PART
Generate or audit only one specific part (Analysis only / Strategy only / Mix only / Results only).

**The core problem this solves:** Most marketing "plans" are activity calendars with metrics tacked on. Real plans must answer 4 questions IN ORDER (Where are we? Where to? How? Measured how?), with each section traceable to the prior. Skip the order or skip the traceability and you get a plan that survives a creative review but not a CFO challenge.

## When to invoke this skill

- Annual marketing planning (CMO + leadership team)
- Quarterly plan refresh
- Product/feature launch GTM plan
- Post-strategic-pivot plan rewrite
- New CMO onboarding (write the plan in first 90 days)
- Budget defense season (CFO needs the structured rationale)
- Asked "build a marketing plan", "write our marketing plan", "audit this plan", "lên plan marketing"
- Investor / board prep

**Skip when:**
- Question is about a single tactic (use other skills: positioning, segmentation, KPIs)
- Question is about a specific decision (pricing, channels) — use specific skill
- Internal team comms or alignment (use translation matrix)
- Pure creative/messaging work

## When NOT to use

- Ad-hoc tactical decisions
- Pure positioning work (use positioning-statement-builder)
- Pure segmentation work (use customer-segmentation-canvas)
- KPI design only (use marketing-kpi-scorecard-builder)

## Workflow

### For FULL PLAN mode
1. Capture inputs: company context, business objectives, budget envelope, timeline (quarter/year)
2. Run `scripts/build_plan.py --company "<context>" --objectives "<list>" --budget <amount> --timeline "<period>"`
3. Read `references/marketing-plan-framework.md` for IE methodology + 4-part rules
4. Apply `templates/marketing-plan.md` for fillable structure
5. Validate completed plan with `scripts/validate_plan.py`

### For VALIDATE mode
1. Capture path to draft plan markdown file
2. Run `scripts/validate_plan.py --plan <file>`
3. Output: section-by-section pass/fail + missing-link diagnostics

### For SINGLE PART mode
Run `scripts/build_plan.py --part <1|2|3|4>` to generate just one section's scaffold.

## Running the scripts

```bash
# Full plan
python3 /Users/phuhung/coursera/.claude/skills/marketing-plan-generator/scripts/build_plan.py \
  --company "B2B SaaS, Series B, $20M ARR, mid-market finance teams" \
  --objectives "Grow ARR 50%, reduce CAC payback to <14mo, lift NPS by 10pts" \
  --budget 2500000 \
  --timeline "12 months"

# Validate existing plan
python3 /Users/phuhung/coursera/.claude/skills/marketing-plan-generator/scripts/validate_plan.py \
  --plan ./our-marketing-plan.md
```

If `python3` crashes with pyexpat error, fall back to `python3.13`.

## Output philosophy

**A plan must answer 4 questions IN ORDER:**
1. Where are we? (Part 1 = Analysis with 5Cs + SWOT)
2. Where do we want to be? (Part 2 = Strategy with quantified objectives)
3. How do we get there? (Part 3 = Marketing Mix 4Ps)
4. How do we measure? (Part 4 = Expected Results metrics + budget)

DO NOT produce:
- Plans that start with tactics ("we'll run a Q1 campaign")
- Plans where Part 4 metrics don't have matching Part 2 objectives
- Plans where 4P decisions aren't traced to strategic choices
- "Mid-market companies" as target segment (too broad — use segmentation skill first)
- Mix without budget allocation

DO produce:
- Strict 4-part order
- Quantified objectives (units, %, time-bound)
- Constraint header at every section (budget + sales target as guardrails)
- Anti-plan section (what we're NOT doing)
- Kill criteria + decision gates

## References (load on demand)

- `references/marketing-plan-framework.md` — full IE 4-part methodology + Veronica Santos / Luis Baptista expert insights + Nissan Leaf launch case + section-by-section rules
- `templates/marketing-plan.md` — fillable 4-part structure with placeholders
- `templates/single-part-templates/` — Analysis / Strategy / Mix / Results individual templates

## Sources

Built from IE Business School The Marketing Plan course (Course 4 of Marketing Strategy Specialization, 41 video lectures):

**Module 1 — Analysis (10 lectures):** 5Cs framework, External vs Internal analysis, SWOT matrix, Nissan Leaf launch case
**Module 2 — Marketing Strategy (8 lectures):** Financial + non-financial objectives, Attraction-vs-retention dilemma, STP, Kotler's 2-pillar strategy
**Module 3 — Marketing Mix Implementation (13 lectures):** 4Ps with Product / Price / Channel / Communication strategies + 3 expert interviews
**Module 4 — Expected Results (10 lectures):** Metrics for financial / non-financial / strategic / customer objectives + Marketing Plan budget

Augmented with: McKinsey-style "objective and task" budgeting + IE's strict trace-back rules.

**Note:** This skill INTEGRATES outputs from other CMO skills:
- `customer-segmentation-canvas` → feeds Part 2 target segment
- `positioning-statement-builder` → feeds Part 2 positioning
- `cmo-strategic-vision-canvas` → feeds Part 2 strategic objectives
- `marketing-kpi-scorecard-builder` → feeds Part 4 metrics

If running marketing-plan-generator standalone, the script generates skeleton placeholders for these inputs. For best output, run the prerequisite skills first.
