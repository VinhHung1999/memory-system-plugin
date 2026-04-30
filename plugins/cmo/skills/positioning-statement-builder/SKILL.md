---
name: positioning-statement-builder
description: |
  Build, validate, and stress-test marketing positioning statements using
  the IE Business School methodology — the 3-element structure
  (target segment + value proposition with point of difference + frame of
  reference / competitor set), the 3-filter Point-of-Difference validator
  (Relevant / Exclusive / Trustworthy), the Urbany-Davis 3-circles model
  (customer needs ⊗ your perceived offering ⊗ competitor perceived
  offering), the "frame by NEED COVERED, not category" rule, and
  alternative positioning strategies (reverse, breakaway, stealth).
  Distinguishes positioning (5-10yr competitive POSITION vs alternatives)
  from VISION (5-10yr north star) and from messaging tactics. Use when
  CMO needs to write a new positioning, audit an existing one, validate a
  proposed point of difference, run competitive overlap analysis, or
  pick alternative positioning approaches. Auto-trigger on phrases like
  "positioning statement", "value proposition", "point of difference",
  "frame of reference", "competitive positioning", "differentiation
  strategy", "PoD", "PoP", "three circles model", "reverse positioning",
  "FOR/WHO/UNLIKE", "category competition".
---

# Positioning Statement Builder (IE Methodology)

## What this does

Three modes for the full positioning lifecycle:

### Mode 1 — BUILD (default)
Build a complete positioning statement from inputs:
- Target segment + segment characteristics
- Value proposition components (tangible attributes + intangibles)
- Frame of reference (NOT category — the customer NEED being covered)
- Competitor set within that frame

Output: 3-element statement with stress-test prompts + 3-filter validation per Point of Difference.

### Mode 2 — VALIDATE
Validate a proposed Point of Difference (PoD) against IE's 3 filters:
- **RELEVANT** — does this matter to the segment? (kill if no)
- **EXCLUSIVE** — distinctive vs market alternatives? (kill if any direct competitor matches)
- **TRUSTWORTHY** — is there a Reason To Believe (RTB)? (kill if speculative)

Output: pass/fail per filter + revision suggestion if fail + RTB recommendations.

### Mode 3 — DIAGNOSE (3-circles)
Apply the Urbany & Davis 3-circles model:
- Circle A: Customer needs/wishes (within segment)
- Circle B: Your offering as customers PERCEIVE it (not as you describe it)
- Circle C: Competitor offering as customers PERCEIVE it

Output: overlap analysis revealing
- **Sweet spot** = A ∩ B but NOT C → unique value
- **Surrender zone** = A ∩ B ∩ C → commodity (move out or accept)
- **Equity at risk** = B but NOT A → you're investing in non-needs (waste)
- **Opportunity** = A but NOT B and NOT C → unmet need to capture
- **Competitor strength** = A ∩ C but NOT B → catch up or concede

**The core problem this solves:** Most positioning statements are slogans dressed as strategy. They name a target, claim a benefit, and stop there. The IE methodology forces 3 disciplines: (1) frame the competition by NEED COVERED, not category (Starbucks competes vs bars/cinemas, not just cafes), (2) validate every claimed Point of Difference against 3 filters before committing, and (3) anchor in CUSTOMER PERCEPTION not internal description. This skill enforces all three.

## When to invoke this skill

- Writing a new positioning statement for a product/brand/segment
- Auditing an existing positioning that feels stale or weak
- Validating a proposed Point of Difference before committing budget
- Running competitive overlap analysis (3-circles)
- Picking alternative positioning approach (reverse, breakaway, stealth) when category is crowded
- Pre-launch GTM planning
- Post-pivot repositioning
- Asked "is this positioning strong?" / "how should we differentiate?" / "what's our PoD?"

**Skip when:**
- Question is about VISION (5-10yr north star) → use `cmo-strategic-vision-canvas` instead
- Question is about brand identity/voice/visual brand
- Question is about pure messaging/tagline crafting (positioning ≠ tagline)
- Cross-functional alignment of marketing insight → use translation matrix

## When NOT to use

- Vision crafting (different layer — use vision-canvas skill)
- Tactical campaign or ad copy
- Pricing strategy (uses positioning as input but is a different decision)
- Personnel/team/agency decisions

## Workflow

### For BUILD mode
1. Capture inputs: target segment + value prop draft + competitor frame
2. Run `scripts/build_positioning.py --target "<segment>" --value-prop "<draft>" --competitors "<list>" --frame-by "<need or category>"`
3. Read `references/positioning-framework.md` for 3-element template + frame-of-reference patterns
4. Apply `templates/positioning-statement.md` for fillable structure

### For VALIDATE mode
1. Capture proposed PoD + segment + claimed RTBs
2. Run `scripts/validate_pod.py --pod "<text>" --segment "<text>" --rtb "<json>"`
3. Output: 3-filter pass/fail with revision suggestions

### For DIAGNOSE mode (3-circles)
1. Capture customer needs, your perceived offering, competitor perceived offering
2. Run `scripts/three_circles.py --needs "<list>" --you "<list>" --competitor "<list>"`
3. Output: overlap analysis with sweet-spot / surrender-zone / equity-at-risk / opportunity classification

## Running the scripts

```bash
# Build mode
python3 /Users/phuhung/coursera/.claude/skills/positioning-statement-builder/scripts/build_positioning.py \
  --target "Mid-market finance teams ($50M-$500M ARR)" \
  --value-prop "One-click reconciliation inside Sage/NetSuite/QuickBooks" \
  --competitors "Bill.com, Tipalti, AvidXchange" \
  --frame-by "ERP-native AP/AR workflow"

# Validate PoD
python3 /Users/phuhung/coursera/.claude/skills/positioning-statement-builder/scripts/validate_pod.py \
  --pod "Fastest payment processing in fintech" \
  --segment "Mid-market controllers" \
  --rtb '{"speed_benchmark": "12s avg", "competitor_avg": "45s"}'

# 3-circles
python3 /Users/phuhung/coursera/.claude/skills/positioning-statement-builder/scripts/three_circles.py \
  --needs "ERP integration, audit trail, multi-currency, automation" \
  --you "ERP integration, audit trail, multi-currency" \
  --competitor "ERP integration, audit trail, fast support, low price"
```

If `python3` crashes with pyexpat error, fall back to `python3.13`.

## Output philosophy

**A strong positioning statement must answer 4 questions:**
1. **WHO is it for?** (specific segment, not "everyone interested")
2. **WHAT need does it cover?** (frame of reference by NEED, not by category)
3. **HOW is it different?** (Point of Difference passing 3 filters: Relevant + Exclusive + Trustworthy)
4. **WHY believe it?** (Reasons To Believe — proof points, not claims)

DO NOT produce:
- Generic positioning ("the leading X for Y") — fails Exclusive filter
- Internal-language positioning (feature lists vs customer outcomes)
- Frame-by-category positioning ("alternative to Bill.com") — limits the strategic playing field
- Speculative PoDs without RTB

DO produce:
- Specific segment + segment evidence
- Frame by customer NEED ("eliminate AP reconciliation" not "AP automation software")
- 1-3 PoDs each passing all 3 filters
- 1-2 RTBs per PoD

## References (load on demand)

- `references/positioning-framework.md` — full IE methodology: 5Cs pre-positioning analysis + 3-element template + 3-filter PoD validator + 3-circles model + 5 differentiation strategies (product/services/staff/R&D/image) + alternative positioning patterns (reverse, breakaway, stealth) + frame-by-need-not-category rule
- `templates/positioning-statement.md` — fillable 3-element structure with stress-test prompts
- `templates/three-circles-canvas.md` — Urbany & Davis 3-circles diagnostic worksheet

## Sources

Built from IE Business School Positioning course (Coursera, Course 2 of Marketing Strategy Specialization, 79K enrolled):

**Module 3 — Differentiation and Value Proposition (9 lectures):**
- 3.0 Why differentiation? — Porter's two paths (cost vs differentiation)
- 3.1 Differentiation and value proposition (tangible + intangible)
- 3.3 Frame of reference, Points of Parity and Points of Difference
- 3.4 How to come up with points of difference (3 filters)
- 3.5 The three circles model (Urbany & Davis)
- 3.6 Differentiation strategies (5 levers)

**Module 4 — Positioning (12 lectures):**
- 4.1 What is positioning?
- 4.3 Positioning Statement (3-element structure)
- 4.4 Commercial Plan based on positioning (4Ps consistency check)
- 4.5 Positioning maps (research-grounded)
- 4.6 Spider Web Perceptual Maps (multidimensional)
- 4.7 Alternative Positioning Strategies (reverse, breakaway, stealth)

Augmented with: real cases from Citroën, IKEA, Starbucks, Tesco, Apple, Vodafone Spain.

**Note:** This skill complements (does NOT duplicate) the existing CMO agent's high-level positioning template (FOR/WHO/IS A/THAT/UNLIKE/WE). The CMO agent has the structure; this skill operationalizes the IE methodology with validators and diagnostics.
