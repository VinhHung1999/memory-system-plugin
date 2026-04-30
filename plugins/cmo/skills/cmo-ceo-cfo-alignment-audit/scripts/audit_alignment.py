#!/usr/bin/env python3
"""
CMO CEO CFO Alignment Audit
============================

Standalone diagnostic for the CMO-CEO-CFO trio. Scores alignment
across 12 indicators (6 CEO axis, 6 CFO axis), produces a
traffic-light scorecard, and emits a structured markdown scaffold
that an LLM can expand into a remediation playbook.

No external dependencies. Stdlib only.
"""

import argparse
import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Indicator data model
# ---------------------------------------------------------------------------

@dataclass
class Indicator:
    id: str
    axis: str  # "ceo" or "cfo"
    weight: int  # 1 or 2
    question: str
    choices: Dict[str, str] = field(default_factory=dict)  # a..d -> text
    interpretations: Dict[str, str] = field(default_factory=dict)  # a..d


# Score map: a=3 (healthy), b=2, c=1, d=0 (high-risk)
SCORE_MAP = {"a": 3, "b": 2, "c": 1, "d": 0}


def build_indicators() -> List[Indicator]:
    return [
        # ------------------------- CEO axis -----------------------------
        Indicator(
            id="ceo_1on1_cadence",
            axis="ceo",
            weight=2,
            question="Cadence of CMO-CEO 1:1s in the last 90 days?",
            choices={
                "a": "Weekly, never cancelled",
                "b": "Bi-weekly, mostly held",
                "c": "Monthly or sporadic",
                "d": "No standing 1:1, ad-hoc only",
            },
            interpretations={
                "a": "Healthy. CEO sees marketing as a peer function.",
                "b": "Workable but susceptible to drift in busy quarters.",
                "c": "Yellow — you are reacting, not co-shaping.",
                "d": "Red — you are out of the strategic loop.",
            },
        ),
        Indicator(
            id="ceo_articulates_metrics",
            axis="ceo",
            weight=2,
            question="Can the CEO articulate marketing's top 3 metrics WITHOUT looking at notes?",
            choices={
                "a": "Yes, all 3 — and links them to revenue",
                "b": "Yes, names 2 of 3",
                "c": "Vague — knows the categories but not the numbers",
                "d": "No — would name brand awareness or vanity metrics",
            },
            interpretations={
                "a": "CEO has internalized the marketing scoreboard.",
                "b": "Close, but one metric is not landing — find which.",
                "c": "CEO does not actually know what you measure.",
                "d": "Red — marketing is invisible at exec scoreboard level.",
            },
        ),
        Indicator(
            id="ceo_exec_sync_seat",
            axis="ceo",
            weight=1,
            question="Does marketing have a permanent seat in the weekly exec sync?",
            choices={
                "a": "Yes, standing seat with speaking slot",
                "b": "Yes, seat but no consistent agenda slot",
                "c": "Invited when topic is marketing-adjacent",
                "d": "Not invited regularly",
            },
            interpretations={
                "a": "Marketing is structurally embedded in exec rhythm.",
                "b": "You are present but reactive.",
                "c": "Marketing is treated as a guest function.",
                "d": "Red — strategic decisions happen without you.",
            },
        ),
        Indicator(
            id="ceo_pivot_consultation",
            axis="ceo",
            weight=2,
            question="On the last strategic pivot, were you consulted BEFORE the decision?",
            choices={
                "a": "Yes, my input shaped the pivot",
                "b": "Consulted in parallel with other functions",
                "c": "Informed during the decision meeting",
                "d": "Found out after the decision was made",
            },
            interpretations={
                "a": "You are operating as a co-architect of strategy.",
                "b": "Acceptable — but verify your input was weighted.",
                "c": "You are a downstream stakeholder, not a shaper.",
                "d": "Red — you have execution authority but not influence.",
            },
        ),
        Indicator(
            id="ceo_board_slot",
            axis="ceo",
            weight=1,
            question="Do you have a standing slot in the board meeting agenda?",
            choices={
                "a": "Yes, recurring slot every board meeting",
                "b": "Yes, every other meeting or quarterly",
                "c": "Only when asked to present a specific topic",
                "d": "No board exposure",
            },
            interpretations={
                "a": "Board sees marketing as a strategic lever.",
                "b": "Decent exposure but inconsistent narrative continuity.",
                "c": "You are a topic, not a voice.",
                "d": "Red — board has no direct line to marketing thinking.",
            },
        ),
        Indicator(
            id="ceo_public_quotes",
            axis="ceo",
            weight=1,
            question="Do the CEO's public-facing quotes about marketing reflect your actual strategy?",
            choices={
                "a": "Yes, on-message and uses our framing",
                "b": "Mostly aligned, occasional drift",
                "c": "Generic 'marketing is important' lines",
                "d": "Off-message or contradicts strategy",
            },
            interpretations={
                "a": "CEO is an authentic amplifier of marketing.",
                "b": "Good — tighten alignment via talking points.",
                "c": "Yellow — CEO defaults to platitudes.",
                "d": "Red — CEO does not know what marketing is doing.",
            },
        ),
        # ------------------------- CFO axis -----------------------------
        Indicator(
            id="cfo_attribution_trust",
            axis="cfo",
            weight=2,
            question="Does the CFO trust your marketing attribution model?",
            choices={
                "a": "Yes, CFO defends it in board meetings",
                "b": "Yes privately, but does not vouch externally",
                "c": "Skeptical — questions the numbers regularly",
                "d": "Openly distrusts it",
            },
            interpretations={
                "a": "Highest-leverage CFO trust signal you can have.",
                "b": "Workable but fragile under scrutiny.",
                "c": "Every budget conversation starts at a deficit.",
                "d": "Red — your attribution is a liability, not an asset.",
            },
        ),
        Indicator(
            id="cfo_budget_basis",
            axis="cfo",
            weight=2,
            question="How is marketing budget allocated this year?",
            choices={
                "a": "Opportunity-based with investment thesis per bet",
                "b": "Mostly opportunity-based with some legacy carry-over",
                "c": "Last year plus or minus a percentage",
                "d": "Cut by finance with no marketing input",
            },
            interpretations={
                "a": "Marketing is a capital allocation, not a cost center.",
                "b": "Trending right but legacy spend dilutes ROI signal.",
                "c": "Yellow — you have lost the budget narrative.",
                "d": "Red — finance owns the budget, marketing executes.",
            },
        ),
        Indicator(
            id="cfo_dashboard_funnel",
            axis="cfo",
            weight=1,
            question="Is MQL to SQL conversion in the CFO's monthly dashboard?",
            choices={
                "a": "Yes, with target and variance",
                "b": "Yes, raw number only",
                "c": "Tracked elsewhere, CFO does not see it",
                "d": "Not tracked or CFO does not care",
            },
            interpretations={
                "a": "CFO is monitoring the marketing-to-revenue handoff.",
                "b": "Visibility exists but no accountability frame.",
                "c": "Funnel health is invisible at the finance layer.",
                "d": "Red — CFO has no leading indicator on marketing ROI.",
            },
        ),
        Indicator(
            id="cfo_forecast_variance",
            axis="cfo",
            weight=2,
            question="Marketing forecast variance over the last 4 quarters?",
            choices={
                "a": "Under 10 percent every quarter",
                "b": "Under 10 percent in 3 of 4 quarters",
                "c": "10 to 20 percent variance regularly",
                "d": "Over 20 percent or chronically off",
            },
            interpretations={
                "a": "Marketing forecasts are finance-grade.",
                "b": "Solid — investigate the miss to prevent regression.",
                "c": "Yellow — CFO is discounting your numbers internally.",
                "d": "Red — marketing forecasts are noise to finance.",
            },
        ),
        Indicator(
            id="cfo_co_built_model",
            axis="cfo",
            weight=1,
            question="Have you co-built any model (LTV, attribution, forecast) with a CFO finance analyst?",
            choices={
                "a": "Yes, multiple models co-owned with finance",
                "b": "Yes, one model co-built",
                "c": "Finance has reviewed marketing models but not co-built",
                "d": "No co-build relationship exists",
            },
            interpretations={
                "a": "Finance has skin in the marketing models — trust compounds.",
                "b": "Good foothold — expand to a second model.",
                "c": "Yellow — review is not ownership.",
                "d": "Red — every model is interpreted as marketing advocacy.",
            },
        ),
        Indicator(
            id="cfo_budget_framing",
            axis="cfo",
            weight=1,
            question="How is your marketing budget request framed?",
            choices={
                "a": "Investment thesis per bet with payback period and kill criteria",
                "b": "Investment thesis but without quantified payback",
                "c": "Categorized spend buckets (brand, demand, ops)",
                "d": "Single line item — total marketing spend",
            },
            interpretations={
                "a": "Speaks finance fluently — capital allocation language.",
                "b": "Right frame, missing rigor.",
                "c": "Bucket thinking — finance cannot evaluate per-bet ROI.",
                "d": "Red — you are asking for a check, not capital.",
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@dataclass
class IndicatorResult:
    indicator: Indicator
    answer_letter: str
    raw_score: int
    weighted_score: int
    max_weighted: int
    light: str  # "red", "yellow", "green"


def light_for(raw: int) -> str:
    if raw >= 3:
        return "green"
    if raw == 2:
        return "yellow"
    return "red"


LIGHT_EMOJI = {"green": "🟢", "yellow": "🟡", "red": "🔴"}


def score_axis(results: List[IndicatorResult]) -> Tuple[float, int, int]:
    """Return (normalized_score_out_of_15, weighted_total, max_weighted_total)."""
    weighted = sum(r.weighted_score for r in results)
    max_weighted = sum(r.max_weighted for r in results)
    if max_weighted == 0:
        return (0.0, 0, 0)
    normalized = round((weighted / max_weighted) * 15, 1)
    return (normalized, weighted, max_weighted)


def overall_band(total_normalized: float) -> Tuple[str, str]:
    """Return (band_label, traffic_light)."""
    if total_normalized >= 24:
        return ("Healthy", "🟢")
    if total_normalized >= 17:
        return ("Watch", "🟡")
    if total_normalized >= 10:
        return ("At-risk", "🟠")
    return ("Crisis", "🔴")


def reaudit_window(band_label: str) -> str:
    return {
        "Healthy": "90 days",
        "Watch": "60 days",
        "At-risk": "30 days",
        "Crisis": "14 days",
    }.get(band_label, "30 days")


# ---------------------------------------------------------------------------
# Input collection
# ---------------------------------------------------------------------------

def prompt_interactive(indicators: List[Indicator]) -> Dict[str, str]:
    answers: Dict[str, str] = {}
    print("\n=== CMO ⇄ CEO ⇄ CFO Alignment Audit ===\n")
    print("Answer a, b, c, or d for each question. Be honest — the audit is\n"
          "diagnostic, not aspirational.\n")
    for idx, ind in enumerate(indicators, start=1):
        print(f"\n[{idx}/{len(indicators)}] ({ind.axis.upper()}) {ind.question}")
        for letter in ("a", "b", "c", "d"):
            print(f"  {letter}) {ind.choices[letter]}")
        while True:
            raw = input("Your answer (a-d): ").strip().lower()
            if raw in SCORE_MAP:
                answers[ind.id] = raw
                break
            print("  -> please enter a, b, c, or d")
    return answers


def load_csv_answers(path: Path) -> Dict[str, str]:
    answers: Dict[str, str] = {}
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            if len(row) < 2:
                continue
            indicator_id = row[0].strip()
            letter = row[1].strip().lower()
            if letter not in SCORE_MAP:
                print(f"warning: skipping {indicator_id} — bad answer '{letter}'",
                      file=sys.stderr)
                continue
            answers[indicator_id] = letter
    return answers


# ---------------------------------------------------------------------------
# Scoring pass
# ---------------------------------------------------------------------------

def evaluate(indicators: List[Indicator], answers: Dict[str, str],
             scope: str) -> List[IndicatorResult]:
    results: List[IndicatorResult] = []
    for ind in indicators:
        if scope != "both" and ind.axis != scope:
            continue
        if ind.id not in answers:
            print(f"warning: no answer for {ind.id} — skipping",
                  file=sys.stderr)
            continue
        letter = answers[ind.id]
        raw = SCORE_MAP[letter]
        results.append(IndicatorResult(
            indicator=ind,
            answer_letter=letter,
            raw_score=raw,
            weighted_score=raw * ind.weight,
            max_weighted=3 * ind.weight,
            light=light_for(raw),
        ))
    return results


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_markdown(results: List[IndicatorResult], scope: str) -> str:
    ceo_results = [r for r in results if r.indicator.axis == "ceo"]
    cfo_results = [r for r in results if r.indicator.axis == "cfo"]

    ceo_norm, ceo_w, ceo_max = score_axis(ceo_results) if ceo_results else (0.0, 0, 0)
    cfo_norm, cfo_w, cfo_max = score_axis(cfo_results) if cfo_results else (0.0, 0, 0)

    if scope == "both":
        total = round(ceo_norm + cfo_norm, 1)
        max_total = 30
    elif scope == "ceo":
        total = ceo_norm
        max_total = 15
    else:
        total = cfo_norm
        max_total = 15

    band_label, band_light = overall_band(total if scope == "both"
                                          else total * 2)
    reaudit = reaudit_window(band_label)

    lines: List[str] = []
    lines.append("# CMO ⇄ CEO ⇄ CFO Alignment Audit Report")
    lines.append("")
    lines.append(f"**Scope:** {scope}  ")
    lines.append(f"**Overall verdict:** {band_light} **{band_label}** "
                 f"({total} / {max_total})  ")
    lines.append(f"**Re-audit recommended in:** {reaudit}")
    lines.append("")

    # Executive summary
    red_count = sum(1 for r in results if r.light == "red")
    yellow_count = sum(1 for r in results if r.light == "yellow")
    green_count = sum(1 for r in results if r.light == "green")
    lines.append("## Executive Summary")
    lines.append("")
    summary = (
        f"This audit covers {len(results)} indicators across the {scope} "
        f"axis(es). Scoring shows {green_count} green, {yellow_count} yellow, "
        f"and {red_count} red signals. Overall verdict is **{band_label}**, "
        f"with a normalized score of {total}/{max_total}. "
    )
    if band_label == "Healthy":
        summary += ("The trio is structurally aligned. Use the watch items "
                    "below as preventative maintenance, not crisis response.")
    elif band_label == "Watch":
        summary += ("Alignment is workable but exposed. The red items below "
                    "will compound into trust gaps within 1-2 quarters if "
                    "left untreated.")
    elif band_label == "At-risk":
        summary += ("The CMO is operating with structural disadvantage in "
                    "exec relationships. Expect budget defense to be hard "
                    "and strategic input to be marginalized until the top "
                    "gaps are closed.")
    else:
        summary += ("The CMO role is in crisis-trust territory. Without a "
                    "30-day intervention, marketing risks being recategorized "
                    "as an execution-only function or losing the seat.")
    lines.append(summary)
    lines.append("")

    # Per-axis table
    lines.append("## Per-Axis Scores")
    lines.append("")
    lines.append("| Axis | Normalized | Weighted Total | Indicators |")
    lines.append("|------|-----------:|---------------:|-----------:|")
    if ceo_results:
        lines.append(f"| CEO  | {ceo_norm}/15 | {ceo_w}/{ceo_max} | "
                     f"{len(ceo_results)} |")
    if cfo_results:
        lines.append(f"| CFO  | {cfo_norm}/15 | {cfo_w}/{cfo_max} | "
                     f"{len(cfo_results)} |")
    if scope == "both":
        lines.append(f"| **Total** | **{total}/30** | "
                     f"**{ceo_w + cfo_w}/{ceo_max + cfo_max}** | "
                     f"**{len(results)}** |")
    lines.append("")

    # Per-indicator detail
    def render_block(title: str, block: List[IndicatorResult]) -> None:
        if not block:
            return
        lines.append(f"## {title}")
        lines.append("")
        for r in block:
            ind = r.indicator
            chosen_text = ind.choices[r.answer_letter]
            interp = ind.interpretations[r.answer_letter]
            weight_tag = " (2x weight)" if ind.weight == 2 else ""
            lines.append(f"### {LIGHT_EMOJI[r.light]} {ind.question}{weight_tag}")
            lines.append("")
            lines.append(f"- **Your answer ({r.answer_letter}):** {chosen_text}")
            lines.append(f"- **Score:** {r.raw_score}/3")
            lines.append(f"- **Interpretation:** {interp}")
            lines.append("")

    render_block("CEO Axis Indicators", ceo_results)
    render_block("CFO Axis Indicators", cfo_results)

    # Top 3 gaps
    lines.append("## Top 3 Gaps to Fix First")
    lines.append("")
    gap_priority = sorted(
        results,
        key=lambda r: (r.raw_score, -r.indicator.weight),
    )
    top_gaps = [r for r in gap_priority if r.light != "green"][:3]
    if not top_gaps:
        lines.append("_No red or yellow gaps. The trio is healthy. "
                     "Maintain rituals._")
    else:
        for i, r in enumerate(top_gaps, start=1):
            ind = r.indicator
            lines.append(f"{i}. **[{LIGHT_EMOJI[r.light]} {ind.axis.upper()}]** "
                         f"{ind.question}")
            lines.append(f"   - Current state: {ind.choices[r.answer_letter]}")
            lines.append(f"   - Why this is priority: weight={ind.weight}x, "
                         f"score={r.raw_score}/3")
            lines.append("")

    # Next-step LLM prompt scaffold
    lines.append("## Next-Step Prompt for LLM")
    lines.append("")
    lines.append("Use the following structured ask to expand this scaffold "
                 "into a remediation playbook:")
    lines.append("")
    lines.append("```")
    lines.append("Given the audit results above, produce:")
    lines.append("")
    lines.append("1. WEEK-1 ACTIONS (per top-3 gap)")
    lines.append("   - One concrete behavior to change this week")
    lines.append("   - Who to talk to and what to say")
    lines.append("   - Measurable success indicator by Friday")
    lines.append("")
    lines.append("2. 30-DAY ACTIONS (per top-3 gap)")
    lines.append("   - One artifact to ship (model, brief, dashboard, doc)")
    lines.append("   - One meeting cadence to install")
    lines.append("   - One stakeholder to convert from skeptic to advocate")
    lines.append("")
    lines.append("3. QUARTERLY RITUALS TO INSTALL")
    lines.append("   - Reference templates/quarterly-trio-review.md")
    lines.append("   - Identify which rituals close which red gaps")
    lines.append("")
    lines.append(f"4. RE-AUDIT TIMING: {reaudit} from today")
    lines.append("   - Specify which indicators to re-test first")
    lines.append("   - Define the 'graduation' threshold per gap")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CMO CEO CFO alignment audit (stdlib only).",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Walk through indicators one question at a time.",
    )
    parser.add_argument(
        "--answers",
        type=Path,
        help="Path to CSV file with rows of indicator_id,answer_letter.",
    )
    parser.add_argument(
        "--scope",
        choices=["ceo", "cfo", "both"],
        default="both",
        help="Which axis to audit. Default both.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        help="Optional path to write the markdown report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.interactive and not args.answers:
        print("error: provide --interactive or --answers <csv>", file=sys.stderr)
        return 2

    indicators = build_indicators()
    if args.scope != "both":
        indicators = [i for i in indicators if i.axis == args.scope]

    if args.interactive:
        answers = prompt_interactive(indicators)
    else:
        answers = load_csv_answers(args.answers)

    results = evaluate(indicators, answers, args.scope)
    if not results:
        print("error: no scored indicators — check inputs", file=sys.stderr)
        return 1

    md = render_markdown(results, args.scope)
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(md, encoding="utf-8")
        print(f"wrote {args.output_md}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
