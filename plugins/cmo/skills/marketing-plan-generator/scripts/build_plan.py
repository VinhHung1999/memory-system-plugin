#!/usr/bin/env python3
"""
build_plan.py — IE Business School 4-part marketing plan scaffolder.

Generates a structured marketing-plan skeleton with:
  Part 1 ANALYSIS  (5Cs + Internal differentiation/lifecycle + SWOT 2x2)
  Part 2 STRATEGY  (Financial / Non-financial / Customer / Target / Positioning)
  Part 3 MIX       (Product / Price / Channel / Communication)
  Part 4 RESULTS   (Metrics mirroring Part 2 + Budget + Anti-plan + Kill criteria)

The CONSTRAINT HEADER (sales target + budget) is auto-emitted at the top of
every section per the Nissan Leaf launch case rule — these are guardrails
that prevent scope creep mid-plan.

Stdlib only. No external deps.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date


# ----------------------------------------------------------------------------
# CONSTRAINT HEADER (Nissan Leaf rule)
# ----------------------------------------------------------------------------

def constraint_header(objectives: str, budget: str | None) -> str:
    budget_str = f"${budget}" if budget else "TBD (define in Part 4)"
    return (
        f"> **CONSTRAINT HEADER (guardrails):**  \n"
        f"> Sales target: {objectives}  \n"
        f"> Budget: {budget_str}  \n"
        f"> _Every decision in this section must respect both._\n"
    )


# ----------------------------------------------------------------------------
# PART 1 — ANALYSIS
# ----------------------------------------------------------------------------

def part_1_analysis(company: str, objectives: str, budget: str | None) -> str:
    return f"""## Part 1 — ANALYSIS (Where are we?)

{constraint_header(objectives, budget)}

**Company context:** {company}

### 1.1 External analysis — 5Cs

#### Context (PEST scan)
- Political / Regulatory: _[fill in: regulation, compliance pressure]_
- Economic: _[fill in: macro, interest rates, IT/marketing budgets]_
- Social / cultural: _[fill in: buyer behavior shifts]_
- Technological: _[fill in: AI, platform shifts, new entrants]_

#### Customers
- Total addressable market (TAM): _[size in units / value / number of accounts]_
- Trend: _[growing / stable / declining — specify rate]_
- Buying behavior: _[trigger, evaluation, decision-makers, cycle length]_
- Segments (preliminary): _[list by need + buying-behavior dimensions]_
- _NOTE: Run `customer-segmentation-canvas` for rigorous segmentation._

#### Collaborators
- Key partners / channels / integrations: _[list]_
- Dependency risk: _[which partner controls what]_

#### Competitors
- Direct competitors: _[list 3-5 with reverse-engineered marketing strategy]_
- For each: target segment / positioning / product / price / channel / comms
- Indirect competitors / substitutes: _[list]_
- Positioning map (axes): _[axis 1] x [axis 2] — plot self + competitors_

#### Company (us, from outside in)
- Market position today: _[rank, share, perception]_
- Reputation gaps: _[where we lose deals]_

### 1.2 Internal analysis (exactly 2 deliverables)

#### Differentiation (from CUSTOMER perspective only)
1. _[differentiator 1 — what customer would say is "better"]_
2. _[differentiator 2]_
3. _[differentiator 3]_
4. _[differentiator 4 — generate expansively, pick one for positioning later]_

#### Product life-cycle stage
- Stage: _[Introduction / Growth / Maturity / Decline]_
- Evidence: _[sales curve, profit shape, market saturation signal]_
- Implication for objectives: _[launch=awareness+trial; maturity=defense+margin]_

### 1.3 SWOT 2x2 matrix

| | INTERNAL | EXTERNAL |
|---|---|---|
| **Positive** | **Strengths** (from internal analysis only) | **Opportunities** (from external scan only) |
| | - _[S1]_ | - _[O1]_ |
| | - _[S2]_ | - _[O2]_ |
| | - _[S3]_ | - _[O3]_ |
| **Negative** | **Weaknesses** (from internal analysis only) | **Threats** (from external scan only) |
| | - _[W1 — be brutally honest]_ | - _[T1]_ |
| | - _[W2]_ | - _[T2]_ |
| | - _[W3]_ | - _[T3]_ |

**Rule:** Never mix internal/external rows. Each cell needs 3-5 specific items.
**Action verbs downstream:** LEVERAGE strengths + EXPLOIT opportunities + HIDE weaknesses + DEFEND threats.
"""


# ----------------------------------------------------------------------------
# PART 2 — STRATEGY
# ----------------------------------------------------------------------------

def part_2_strategy(company: str, objectives: str, budget: str | None) -> str:
    return f"""## Part 2 — STRATEGY (Where do we want to be?)

{constraint_header(objectives, budget)}

**Inputs from Part 1:** SWOT conclusions + differentiation list + lifecycle stage.

### 2.1 Financial objectives (REQUIRED — 4 quantified rows)

| # | Objective | Target | Baseline | Time-box |
|---|-----------|--------|----------|----------|
| 1 | Sales — units (accounts/customers/seats) | _[N]_ | _[N0]_ | _[period]_ |
| 2 | Sales — value (revenue / ARR / GMV) | _[$]_ | _[$0]_ | _[period]_ |
| 3 | Market share (or category share) | _[N%]_ | _[N0%]_ | _[period]_ |
| 4 | Profit (gross contribution / net contribution / NOI) | _[$]_ | _[$0]_ | _[period]_ |

_Sanity check: if year-1 target > 5pct of TAM for a niche product, likely unrealistic._

### 2.2 Non-financial objectives (brand)

- **Brand awareness:** _[unaided / aided] from [N0pct] to [Npct]_
- **Brand preference:** _[N0pct] to [Npct] in target segment_
- **Brand associations:** _[3 attribute dials we want to own]_
- **Digital signals (only if running digital):** clicks / searches / followers / UGC volume / NPS / review rating

_Pick only what your tactics will actually influence — don't list metrics you won't move._

### 2.3 Customer objectives (explicit pct split — REQUIRED)

| Lever | pct of customer-acquisition budget | Rationale |
|------|---------------------------------|-----------|
| Attraction (new logos / first-time buyers) | _[N pct]_ | _[lifecycle stage justifies]_ |
| Retention (renewal / expansion / loyalty) | _[N pct]_ | _[install base value justifies]_ |

_Lifecycle drives split: Introduction ≈ heavy attraction; Maturity ≈ heavy retention._

### 2.4 Target segment (STP — strict order)

- **Segmentation criteria used:** _[geographic / demographic / psychographic / behavioral — combine multiple]_
- **Segments evaluated:** _[list 3-5 candidates]_
- **Targeted segment(s):** _[name + size + need + buying behavior]_
- **Why this segment (MAPDA test):** Measurable / Accessible / Profitable / Differentiable / Actionable

_NOTE: Run `customer-segmentation-canvas` if target is "mid-market companies" or similar too-broad label._

### 2.5 Positioning statement

> For _[target segment]_, _[brand]_ is the _[frame of reference / category]_ that delivers _[unique value / point of difference]_, because _[reason to believe / proof point]_.

- **Frame of reference:** _[competitor set we anchor against]_
- **Point of difference:** _[the ONE differentiator picked from Part 1 list]_
- **Reasons to believe:** _[3 proof points]_

_NOTE: Run `positioning-statement-builder` for 3-filter validation (Relevant / Exclusive / Trustable)._

**Kotler 2-pillar minimum check:** Target segment ✅ + Value proposition ✅ — both present?
"""


# ----------------------------------------------------------------------------
# PART 3 — MARKETING MIX
# ----------------------------------------------------------------------------

def part_3_mix(company: str, objectives: str, budget: str | None) -> str:
    return f"""## Part 3 — MARKETING MIX (How do we get there?)

{constraint_header(objectives, budget)}

**Trace-back rule:** Every 4P decision below must reference a strategic choice in Part 2.

### 3.1 Product

- **Lifecycle stage (from Part 1):** _[Introduction / Growth / Maturity / Decline]_
- **Product levels:**
  - Core benefit: _[the job-to-be-done]_
  - Basic product: _[features delivering the core]_
  - Expected product: _[table-stakes feature set]_
  - Augmented product: _[support / SLA / community / docs]_
  - Potential product: _[future expansion / roadmap]_
- **Branding decisions:** _[brand architecture, naming, sub-brands]_
- **Trace-back to Part 2:** _[which strategic choice this product config supports]_

### 3.2 Price

- **Strategy:** Cost-based / Value-based / Competitive — pick + justify
- **Positioning fit:** _[premium / mid / penetration — must match Part 2 positioning]_
- **6-criterion checklist:**
  1. Cost floor known? _[Y/N]_
  2. Customer willingness-to-pay known? _[Y/N]_
  3. Competitor benchmark? _[$]_
  4. Subsidy / discount stack modeled? _[Y/N]_
  5. Price elasticity assumption? _[%]_
  6. Anchor / reference price set? _[Y/N]_
- **Trace-back to Part 2:** _[which strategic choice this pricing supports]_

### 3.3 Channel (distribution)

- **4-step design:**
  1. Customer need (where does target buy?): _[]_
  2. Channel options (own / partner / marketplace / direct sales): _[]_
  3. Channel economics (margin / CAC by channel): _[]_
  4. Channel mix decision + cuts: _[which channels we DON'T use and why]_
- **Trace-back to Part 2:** _[target segment lives where → that's where channel goes]_

### 3.4 Communication

- **5 M's:**
  - Mission (objective): _[awareness / preference / trial / loyalty]_
  - Message: _[positioning expressed in 1 sentence]_
  - Media: _[paid / owned / earned mix]_
  - Money (budget allocation): _[$ per channel]_
  - Measurement: _[forward to Part 4]_
- **IMC 6-criteria:** coverage / contribution / commonality / complementarity / conformability / cost
- **Buyer-readiness mix:**
  - Awareness stage: _[mass-reach channels, % budget]_
  - Knowledge / interest: _[content, % budget]_
  - Preference / conviction: _[social proof, demos, % budget]_
  - Purchase: _[sales enablement, retargeting, % budget]_
- **Trace-back to Part 2:** _[non-financial objective + target segment drives this mix]_
"""


# ----------------------------------------------------------------------------
# PART 4 — EXPECTED RESULTS
# ----------------------------------------------------------------------------

def part_4_results(company: str, objectives: str, budget: str | None) -> str:
    budget_str = f"${budget}" if budget else "_[TBD — sum of all line items below]_"
    return f"""## Part 4 — EXPECTED RESULTS (How do we measure?)

{constraint_header(objectives, budget)}

**Mirror rule:** Every Part 2 objective MUST have exactly one Part 4 metric. One-to-one.

### 4.1 Metrics mirroring Part 2 (one row per Part 2 objective)

| Part 2 objective | Part 4 metric | Measurement tool | Target | Cadence | Owner |
|------------------|---------------|------------------|--------|---------|-------|
| Financial — sales units | _[same target]_ | CRM / billing | _[N]_ | Monthly | _[role]_ |
| Financial — sales value | _[ARR / revenue]_ | Finance system | _[$]_ | Monthly | _[role]_ |
| Financial — market share | Market-share pct | Industry report | _[Npct]_ | Quarterly | _[role]_ |
| Financial — profit | Gross / net contribution | P&L | _[$]_ | Monthly | _[role]_ |
| Non-financial — awareness | Aided / unaided pct | Brand tracker | _[Npct]_ | Quarterly | _[role]_ |
| Non-financial — preference | Preference pct in target | Brand tracker | _[Npct]_ | Quarterly | _[role]_ |
| Non-financial — associations | Attribute association pct | Brand tracker | _[Npct]_ | Quarterly | _[role]_ |
| Customer — attraction | New logos / period | CRM | _[N]_ | Monthly | _[role]_ |
| Customer — retention | NRR / churn | CRM | _[Npct]_ | Monthly | _[role]_ |
| Strategic — target reach | pct of TAM in segment touched | Marketing ops | _[Npct]_ | Quarterly | _[role]_ |
| Strategic — positioning | Positioning attribute lift | Brand tracker | _[delta]_ | Quarterly | _[role]_ |

### 4.2 Budget (objective-and-task method)

**Total marketing budget: {budget_str}**

| Line item | Tactic | Linked Part 2 obj | Cost |
|-----------|--------|-------------------|------|
| Brand campaign | _[]_ | Awareness | _[$]_ |
| Content / SEO | _[]_ | Preference + attraction | _[$]_ |
| Paid acquisition | _[]_ | Attraction | _[$]_ |
| Lifecycle / retention | _[]_ | Retention | _[$]_ |
| Events / field | _[]_ | Pipeline + brand | _[$]_ |
| Marketing ops / tools | _[]_ | Enablement | _[$]_ |
| Headcount allocation | _[]_ | All | _[$]_ |
| **TOTAL** | | | **{budget_str}** |

_Method: objective-and-task. Each line item links to a Part 2 objective. Sum to total._

### 4.3 Anti-plan (what we are NOT doing)

- _[Channel / segment / tactic we deliberately exclude — and why]_
- _[Brand stretch we won't attempt]_
- _[Geo we won't enter this period]_

### 4.4 Kill criteria (what makes us stop)

- IF _[leading metric]_ is below _[threshold]_ by _[date]_ THEN stop / pivot.
- IF CAC payback exceeds _[months]_ in 2 consecutive quarters THEN reallocate.
- IF brand-tracker preference drops _[pct]_ THEN pause paid acquisition.

### 4.5 Decision gates

| Gate | Date | Decision | Owner | Data needed |
|------|------|----------|-------|-------------|
| Q1 review | _[date]_ | Continue / adjust mix | CMO + CFO | Pipeline, CAC, brand tracker |
| Mid-year | _[date]_ | Reforecast | CMO + CEO | All KPIs vs target |
| Q3 review | _[date]_ | Budget reallocation | CMO + CFO | ROI by channel |
| Year-end | _[date]_ | Plan renewal | CMO + Board | Full P&L impact |

_Drucker rule: what doesn't get measured doesn't get managed._
_Baptista rule: marketing is investment, not expense — every line item earns its return._
"""


# ----------------------------------------------------------------------------
# Next-step LLM prompt
# ----------------------------------------------------------------------------

def next_step_prompt(part_filter: str) -> str:
    if part_filter == "all":
        focus = "the full 4-part plan"
    else:
        focus = f"Part {part_filter}"
    return f"""## Next-step prompt for LLM

You have a scaffolded skeleton for {focus}. Now:

1. **Fill in the 5Cs** (Part 1) with specific industry/market data.
   - If unclear, run `customer-research-design-picker` first to gather inputs.
2. **Define the target segment** (Part 2.4) with name + size + need + buying behavior.
   - If target is "mid-market companies" or similar broad label, run `customer-segmentation-canvas` first.
3. **Write the positioning statement** (Part 2.5) using the 3-element template.
   - Run `positioning-statement-builder` for 3-filter validation.
4. **Validate Part 4 metrics mirror Part 2 objectives** — one-to-one. Every objective gets a metric. No orphans.
5. **Audit 4P consistency vs strategy** — every Product / Price / Channel / Communication choice must trace back to a specific Part 2 strategic decision (target segment, positioning, financial obj, customer split).
6. **Verify constraint header** (sales target + budget) is repeated at top of every section. This is the Nissan Leaf rule.
7. **Run `validate_plan.py --plan <file>`** before submitting.
"""


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate IE 4-part marketing plan scaffold (Analysis -> Strategy -> Mix -> Results).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--company",
        required=True,
        help="Company context: industry, stage, ARR, segment focus.",
    )
    p.add_argument(
        "--objectives",
        required=True,
        help="Comma-separated business objectives (sales, CAC, NPS, etc.).",
    )
    p.add_argument(
        "--budget",
        default=None,
        help="USD budget envelope (numeric). Optional.",
    )
    p.add_argument(
        "--timeline",
        default="12 months",
        help="Plan horizon. Default 12 months.",
    )
    p.add_argument(
        "--part",
        default="all",
        choices=["1", "2", "3", "4", "all"],
        help="Which part to generate. Default all.",
    )
    return p.parse_args(argv)


def build_plan(company: str, objectives: str, budget: str | None,
               timeline: str, part: str) -> str:
    today = date.today().isoformat()
    header = f"""# Marketing Plan — {timeline}

**Generated:** {today}
**Company:** {company}
**Business objectives:** {objectives}
**Budget envelope:** {f'${budget}' if budget else 'TBD'}
**Timeline:** {timeline}

> Built with the IE Business School 4-part methodology:
> Analysis -> Strategy -> Mix -> Results (strict order, never reorder).

---
"""

    sections = []
    if part in ("1", "all"):
        sections.append(part_1_analysis(company, objectives, budget))
    if part in ("2", "all"):
        sections.append(part_2_strategy(company, objectives, budget))
    if part in ("3", "all"):
        sections.append(part_3_mix(company, objectives, budget))
    if part in ("4", "all"):
        sections.append(part_4_results(company, objectives, budget))

    body = "\n\n---\n\n".join(sections)
    tail = "\n\n---\n\n" + next_step_prompt(part)
    return header + body + tail


def main(argv: list[str]) -> int:
    ns = parse_args(argv)
    out = build_plan(
        company=ns.company,
        objectives=ns.objectives,
        budget=ns.budget,
        timeline=ns.timeline,
        part=ns.part,
    )
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
