---
name: customer-segmentation-canvas
description: |
  Design and validate customer segmentation strategy using the IE Business
  School methodology — pick segmentation level (mass / segment / niche /
  segment-of-one), choose criteria type (geographic / demographic /
  psychographic / behavioral), validate every candidate segment against
  the 5-filter MAPDA test (Measurable / Accessible / Profitable /
  Differentiable / Actionable), and select segmentation strategy from
  Kotler's 5 patterns (single-segment concentration, selective
  specialization, market specialization, product specialization, full
  market coverage). Use when CMO needs to define segments before
  positioning, audit existing segments, validate a proposed segment, or
  decide segmentation strategy. Auto-trigger on phrases like
  "segmentation", "target segment", "customer segments", "ICP definition",
  "MAPDA filter", "psychographic segmentation", "Kotler segmentation",
  "should we segment", "segment validation".
---

# Customer Segmentation Canvas (IE Methodology)

## What this does

Two modes for segmentation design and validation:

### Mode 1 — DESIGN (default)
Take a market or customer base description and propose a segmentation approach:
- Recommend segmentation level (mass / segment / niche / segment-of-one) based on company stage + market characteristics
- Choose criteria type (geographic / demographic / psychographic / behavioral) based on what differentiates needs
- Generate 2-4 candidate segments with key characteristics
- Recommend Kotler's segmentation strategy (which segments to serve)

Output: structured canvas with proposed segments + criteria rationale + strategy recommendation.

### Mode 2 — VALIDATE
Validate a proposed segment against the IE 5-filter MAPDA test:
- **Measurable** — can you size the segment? (population, value)
- **Accessible** — can you reach them through identifiable channels?
- **Profitable** — does the segment generate enough value to justify investment?
- **Differentiable** — does this segment respond differently than others?
- **Actionable** — can your org actually serve them with current capabilities?

Output: pass/fail per filter + revision suggestions.

**The core problem this solves:** Most "segments" are demographic descriptions ("mid-market companies, 50-500 employees") that fail the Differentiable + Actionable tests — they group customers who behave similarly demographically but DON'T need different things. Real segments cluster on need-similarity, validate on the 5 filters, and drive distinct go-to-market motions. This skill enforces the discipline.

## When to invoke this skill

- Defining segments before any positioning work (5Cs → segment → position)
- Auditing existing ICP / segment definitions for rigor
- Validating a new candidate segment before allocating budget
- Choosing segmentation strategy (which segments to focus on)
- Asked "what's our ICP?" / "should we segment?" / "is this segment real?"
- Pre-launch GTM planning when segments aren't yet defined
- After a strategic pivot — segments may need to change

**Skip when:**
- Question is about positioning a SPECIFIC segment (use positioning-statement-builder instead)
- Question is about messaging tactics for an existing segment
- Question is about cross-functional translation of insight (use translation matrix)
- Tactical campaign-level audience targeting

## When NOT to use

- Positioning statement work (different layer)
- Creative/messaging tactics
- Pricing strategy
- Personnel/team decisions

## Workflow

### For DESIGN mode
1. Capture inputs: market/customer description + company stage + objectives
2. Run `scripts/segment_canvas.py --market "<description>" --stage "<stage>" --objectives "<list>"`
3. Read `references/segmentation-framework.md` for criteria guidance + Kotler's 5 strategies
4. Apply `templates/segmentation-canvas.md` for fillable output

### For VALIDATE mode
1. Capture proposed segment definition + characteristics
2. Run `scripts/validate_segment.py --segment "<description>" --evidence '<json>'`
3. Output: 5-filter MAPDA pass/fail + revision suggestions

## Running the scripts

```bash
# Design mode
python3 /Users/phuhung/coursera/.claude/skills/customer-segmentation-canvas/scripts/segment_canvas.py \
  --market "B2B fintech serving finance teams in companies $10M-$500M revenue" \
  --stage "Series B" \
  --objectives "grow ARR 50%, reduce CAC payback to under 14 months"

# Validate mode
python3 /Users/phuhung/coursera/.claude/skills/customer-segmentation-canvas/scripts/validate_segment.py \
  --segment "Mid-market controllers running NetSuite who reconcile multi-currency manually" \
  --evidence '{"size": "12000 companies in NA", "channel": "NetSuite marketplace + ERP partner network", "arpc_estimate": "5K-15K", "needs_diff": "high"}'
```

If `python3` crashes with pyexpat error, fall back to `python3.13`.

## Output philosophy

**A strong segment must answer 4 questions:**
1. **Who is in it?** (specific characteristics, not "everyone interested in X")
2. **Why are they grouped?** (similar NEEDS, not similar demographics by accident)
3. **Can we reach them?** (identifiable channel, identifiable buying committee)
4. **Will it pay back?** (size × ARPC × win rate × LTV justifies the GTM motion)

DO NOT produce:
- Pure demographic segments without need-similarity ("mid-market 50-500 employees")
- Aspirational segments without channel access ("forward-thinking innovators")
- Vanity segments that flatter the buyer but can't be reached
- Segments smaller than the 5-filter MAPDA can validate

DO produce:
- Need-clustered segments with demographic + psychographic + behavioral evidence
- Channel access named explicitly per segment
- Sizing estimate (count × ARPC × penetration assumption)
- Differentiability evidence (these customers respond differently)

## References (load on demand)

- `references/segmentation-framework.md` — full IE methodology: 4 segmentation levels (mass/segment/niche/individual), 4 criteria types (geo/demo/psycho/behavioral) + when to use each, 5-filter MAPDA validator, Kotler's 5 segmentation strategies, expert insights from J&J global strategic insights
- `templates/segmentation-canvas.md` — fillable canvas with MAPDA stress-test

## Sources

Built from IE Business School Positioning course (Coursera, Course 2 of Marketing Strategy Specialization, 79K enrolled):

**Module 2 — Segmentation (10 lectures):**
- 2.0 What is a segment?
- 2.1 Mass / segments / niches / individuals
- 2.2 Segmentation levels
- 2.3 Why should we segment?
- 2.4 Reasons to segment
- 2.5 Geographic and demographic criteria
- 2.6 Psychographic and behavioral criteria
- 2.7 How to come up with effective segmentation (5-filter MAPDA)
- 2.8 Segmentation models (Kotler's 5 strategies)
- 2.9 Expert interview: Jaime Veiga (Johnson & Johnson global strategic insights)

**Note:** This skill works HAND-IN-HAND with `positioning-statement-builder`. Segmentation comes BEFORE positioning in the IE framework: 5Cs → segment → target → position → 4Ps. Use this skill to define segments, then hand off to positioning-statement-builder for the chosen target segment.
