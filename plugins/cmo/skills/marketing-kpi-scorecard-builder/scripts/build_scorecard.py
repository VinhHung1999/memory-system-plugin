#!/usr/bin/env python3
"""
build_scorecard.py — Turn a list of raw marketing metrics into a board-ready
1-page scorecard with traffic-light zones, activity-vs-impact audit, and
LLM next-step prompts.

Stdlib only. Reads CSV or JSON.

CSV/JSON columns expected:
  name, current, target, category (optional), strategic_objective (optional)

Usage:
  python3 build_scorecard.py \\
    --metrics metrics.csv \\
    --objectives "Revenue growth 50pp, Reduce CAC payback under 14mo, NPS +10" \\
    --output-md scorecard.md
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Activity vs Impact keyword library
# ---------------------------------------------------------------------------

ACTIVITY_KEYWORDS = [
    "impression", "impressions",
    "click", "clicks", "ctr", "click-through", "click through",
    "engagement", "engaged",
    "mql count", "mql_count", "mqls",
    "open rate", "open-rate", "open_rate",
    "session", "sessions",
    "page view", "pageview", "page-view",
    "follower", "followers",
    "like", "likes",
    "share", "shares",
    "reach",
    "view", "views",
    "subscriber", "subscribers",
    "bounce rate",
]

IMPACT_KEYWORDS = [
    "clv", "customer lifetime value", "lifetime value", "ltv",
    "nrr", "net revenue retention",
    "churn", "retention",
    "market share", "share of wallet",
    "advocacy", "nps", "net promoter",
    "brand health", "brand equity",
    "share of voice", "sov",
    "revenue", "arr", "mrr",
    "pipeline",
    "cac payback", "cac_payback", "payback period",
    "ltv/cac", "ltv:cac",
    "gross retention", "logo retention",
    "conversion rate",  # contextually impact when tied to revenue
    "trial-to-paid", "trial to paid",
    "win rate",
    "expansion revenue",
    "qualified pipeline",
]

# Activity -> impact twin suggestions
ACTIVITY_TWIN = {
    "impressions": "Reach within ICP (qualified reach)",
    "impression": "Reach within ICP (qualified reach)",
    "ctr": "Cost per qualified visitor",
    "click-through": "Cost per qualified visitor",
    "click through": "Cost per qualified visitor",
    "click_through_rate": "Cost per qualified visitor",
    "click through rate": "Cost per qualified visitor",
    "clicks": "Cost per qualified visitor",
    "click": "Cost per qualified visitor",
    "engagement": "Engaged-to-customer conversion rate",
    "engaged": "Engaged-to-customer conversion rate",
    "mql count": "MQL-to-SQL conversion rate",
    "mqls": "MQL-to-SQL conversion rate",
    "mql_count": "MQL-to-SQL conversion rate",
    "open rate": "Trial conversions from email",
    "open-rate": "Trial conversions from email",
    "open_rate": "Trial conversions from email",
    "email open rate": "Trial conversions from email",
    "sessions": "Sessions-to-pipeline ratio",
    "session": "Sessions-to-pipeline ratio",
    "page views": "Sessions-to-pipeline ratio",
    "page view": "Sessions-to-pipeline ratio",
    "pageview": "Sessions-to-pipeline ratio",
    "followers": "Engaged-followers-to-customers ratio",
    "follower": "Engaged-followers-to-customers ratio",
    "likes": "Net positive sentiment share",
    "like": "Net positive sentiment share",
    "shares": "Earned amplification by ICP accounts",
    "share": "Earned amplification by ICP accounts",
    "reach": "Reach within ICP (qualified reach)",
    "views": "Qualified-view-to-pipeline ratio",
    "view": "Qualified-view-to-pipeline ratio",
    "subscribers": "Subscriber-to-customer conversion rate",
    "subscriber": "Subscriber-to-customer conversion rate",
    "bounce rate": "Qualified-visitor session quality score",
}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def load_metrics(path: str) -> list[dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"metrics file not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    rows: list[dict[str, Any]] = []
    if ext == ".json":
        with open(path) as fh:
            data = json.load(fh)
        if isinstance(data, dict) and "metrics" in data:
            data = data["metrics"]
        if not isinstance(data, list):
            raise ValueError("JSON must be a list (or {metrics: [...]})")
        rows = data
    else:
        # treat as CSV
        with open(path, newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

    cleaned: list[dict[str, Any]] = []
    for r in rows:
        if not r.get("name"):
            continue
        try:
            current = float(str(r["current"]).strip().replace("%", "").replace(",", ""))
            target = float(str(r["target"]).strip().replace("%", "").replace(",", ""))
        except (KeyError, ValueError):
            print(f"WARN: skipping malformed row: {r}", file=sys.stderr)
            continue
        cleaned.append(
            {
                "name": str(r["name"]).strip(),
                "current": current,
                "target": target,
                "category": (r.get("category") or "").strip(),
                "strategic_objective": (r.get("strategic_objective") or "").strip(),
            }
        )
    return cleaned


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def variance_pct(current: float, target: float) -> float:
    if target == 0:
        return 0.0
    return (current - target) / target * 100.0


def zone_for(variance: float) -> str:
    # variance is signed: negative means below target.
    # Higher-is-better metrics are the dominant case; for "lower is better"
    # (CAC payback), the caller must invert sign. This script assumes higher
    # is better unless metric name implies otherwise (handled separately).
    if variance >= -5.0:
        return "green"
    if variance >= -15.0:
        return "yellow"
    return "red"


# Lower-is-better metric keywords (variance interpretation flips)
LOWER_IS_BETTER = [
    "cac payback", "cac_payback", "payback period",
    "churn",
    "cost per", "cpa", "cpc", "cpm",
    "bounce",
    "unsubscribe",
]


def is_lower_is_better(name: str) -> bool:
    n = name.lower()
    return any(k in n for k in LOWER_IS_BETTER)


def classify_zone(name: str, current: float, target: float) -> tuple[float, str]:
    raw_variance = variance_pct(current, target)
    if is_lower_is_better(name):
        # invert: if current < target, that's good
        effective = -raw_variance
    else:
        effective = raw_variance
    return raw_variance, zone_for(effective)


def classify_activity_vs_impact(name: str, category: str = "") -> str:
    blob = (name + " " + category).lower()
    # impact wins ties (impact metrics often contain activity-shaped sub-words)
    for k in IMPACT_KEYWORDS:
        if k in blob:
            return "impact"
    for k in ACTIVITY_KEYWORDS:
        if k in blob:
            return "activity"
    return "unclassified"


def suggest_twin(name: str) -> str | None:
    n = name.lower()
    # match longest key first
    for k in sorted(ACTIVITY_TWIN.keys(), key=len, reverse=True):
        if k in n:
            return ACTIVITY_TWIN[k]
    return None


# ---------------------------------------------------------------------------
# Top-3 metric ranking
# ---------------------------------------------------------------------------

def relevance_to_objectives(metric_name: str, objectives: list[str]) -> int:
    """Rough scoring: count keyword hits between metric and objectives."""
    score = 0
    nm = metric_name.lower()
    for obj in objectives:
        for tok in re.findall(r"[a-z][a-z0-9]+", obj.lower()):
            if len(tok) >= 4 and tok in nm:
                score += 1
    return score


def pick_top_three(metrics: list[dict[str, Any]], objectives: list[str]) -> list[dict[str, Any]]:
    impact = [m for m in metrics if m["kind"] == "impact"]
    pool = impact if impact else metrics
    scored = []
    for m in pool:
        rel = relevance_to_objectives(m["name"], objectives)
        # gap urgency: bigger negative variance (in effective terms) -> higher urgency
        if is_lower_is_better(m["name"]):
            effective = -m["variance"]
        else:
            effective = m["variance"]
        urgency = max(0.0, -effective)  # only count below-target as urgency
        # blended score: relevance dominates, urgency tiebreaks
        score = rel * 100 + urgency
        scored.append((score, m))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[:3]]


# ---------------------------------------------------------------------------
# Suggested action heuristics
# ---------------------------------------------------------------------------

def suggested_action(m: dict[str, Any]) -> str:
    z = m["zone"]
    if z == "green":
        return "Monitor; document playbook so other channels can replicate"
    if z == "yellow":
        return "Diagnose root cause this week; pre-stage corrective action before slippage"
    # red
    return "Intervene now: run root-cause detective method, assign owner + due date"


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

ZONE_EMOJI = {"green": "GREEN", "yellow": "YELLOW", "red": "RED"}
ZONE_LIGHT = {"green": "[GREEN]", "yellow": "[YELLOW]", "red": "[RED]"}


def fmt_var(v: float) -> str:
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.1f}pp"


def render_markdown(metrics: list[dict[str, Any]], objectives: list[str], top3: list[dict[str, Any]]) -> str:
    lines: list[str] = []

    # Top traffic-light verdict
    zone_counts = {"red": 0, "yellow": 0, "green": 0}
    for m in metrics:
        zone_counts[m["zone"]] += 1
    if zone_counts["red"] > 0:
        verdict_zone = "RED"
        verdict_line = f"{zone_counts['red']} red-zone KPIs require immediate intervention; do not defer."
    elif zone_counts["yellow"] > zone_counts["green"]:
        verdict_zone = "YELLOW"
        verdict_line = "Performance is drifting; pre-stage corrective actions on yellow-zone metrics this week."
    else:
        verdict_zone = "GREEN"
        verdict_line = "On track; replicate green-zone playbooks into yellow-zone areas."

    lines.append("# Marketing Performance Scorecard")
    lines.append("")
    lines.append(f"**Top-line:** [{verdict_zone}] {verdict_line}")
    lines.append("")

    # Executive summary
    lines.append("## Executive summary")
    lines.append("")
    activity_count = sum(1 for m in metrics if m["kind"] == "activity")
    impact_count = sum(1 for m in metrics if m["kind"] == "impact")
    summary = (
        f"Of {len(metrics)} tracked KPIs, {impact_count} are business-impact metrics "
        f"and {activity_count} are activity metrics that should be paired with impact twins. "
        f"Zoning: {zone_counts['green']} green, {zone_counts['yellow']} yellow, "
        f"{zone_counts['red']} red. The board sees {verdict_zone} as the headline status: "
        f"{verdict_line}"
    )
    lines.append(summary)
    lines.append("")

    # Calibration warning
    if metrics and zone_counts["yellow"] == len(metrics):
        lines.append("> **CALIBRATION WARNING — TARGETS ARE WRONG, NOT PERFORMANCE.**")
        lines.append(
            "> Every metric is yellow. When everything is between 5-15pp under target, "
            "the targets themselves are likely miscalibrated. Re-baseline before treating "
            "this as a performance crisis."
        )
        lines.append("")
    if metrics and zone_counts["red"] == 0 and zone_counts["green"] == len(metrics):
        lines.append("> **CALIBRATION CHECK — targets may be too easy.**")
        lines.append(
            "> If no metric is ever red, the team is not stretching. Reset 1-2 stretch targets."
        )
        lines.append("")

    # Top 3 metrics that matter
    lines.append("## Top 3 metrics that matter")
    lines.append("")
    if not top3:
        lines.append("_No business-impact metrics found. The current scorecard is activity-only — rebuild before board prep._")
    else:
        for i, m in enumerate(top3, 1):
            lines.append(
                f"{i}. **{m['name']}**: current {m['current']}, target {m['target']} "
                f"(variance {fmt_var(m['variance'])}, {ZONE_EMOJI[m['zone']]})"
            )
    lines.append("")

    # Per-zone tables
    for zone in ["red", "yellow", "green"]:
        bucket = [m for m in metrics if m["zone"] == zone]
        if not bucket:
            continue
        label = {"red": "RED zone (intervene now)", "yellow": "YELLOW zone (diagnose + prep action)", "green": "GREEN zone (monitor)"}[zone]
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| Metric | Current | Target | Variance | Suggested action |")
        lines.append("|---|---|---|---|---|")
        for m in bucket:
            lines.append(
                f"| {m['name']} | {m['current']} | {m['target']} | "
                f"{fmt_var(m['variance'])} | {suggested_action(m)} |"
            )
        lines.append("")

    # Activity-vs-impact audit
    lines.append("## Activity-vs-impact audit")
    lines.append("")
    activity_metrics = [m for m in metrics if m["kind"] == "activity"]
    if not activity_metrics:
        lines.append("_No orphan activity metrics found. Scorecard is impact-anchored._")
    else:
        lines.append("These activity metrics should be paired with their business-impact twin. "
                     "The board discounts activity numbers — pipeline contribution is the real story.")
        lines.append("")
        lines.append("| Activity metric | Suggested impact twin |")
        lines.append("|---|---|")
        for m in activity_metrics:
            twin = suggest_twin(m["name"]) or "Pair with downstream pipeline/revenue metric"
            lines.append(f"| {m['name']} | {twin} |")
    lines.append("")

    # KPI hygiene
    lines.append("## KPI hygiene")
    lines.append("")
    orphans = [m for m in metrics if not m["strategic_objective"]]
    if orphans:
        lines.append("**Orphan metrics (no traceable strategic objective):**")
        for m in orphans:
            lines.append(f"- {m['name']}")
        lines.append("")
        lines.append("Action: either assign each to an existing objective, or remove from the scorecard.")
    else:
        lines.append("_All metrics traced to a strategic objective._")
    lines.append("")

    # Stated objectives
    if objectives:
        lines.append("## Strategic objectives in scope")
        lines.append("")
        for o in objectives:
            lines.append(f"- {o}")
        lines.append("")

    # Next-step prompt for LLM
    lines.append("## Next-step prompt for LLM")
    lines.append("")
    red_names = [m["name"] for m in metrics if m["zone"] == "red"]
    activity_names = [m["name"] for m in metrics if m["kind"] == "activity"]
    lines.append("Use this prompt to sharpen the scorecard before sending to the board:")
    lines.append("")
    lines.append("```")
    lines.append("You are a CMO advisor. Given the scorecard above, do three things:")
    lines.append("")
    lines.append("1. SHARPEN the action prompt for each red-zone metric. Replace generic")
    lines.append("   phrasing like 'do better' with specific tactical levers (e.g., 'reduce")
    lines.append("   CAC payback by reallocating $200K from paid-social to inbound SEO and")
    lines.append("   lifting trial-to-paid by 3pp via onboarding email sequence redesign').")
    if red_names:
        lines.append(f"   Red-zone metrics to sharpen: {', '.join(red_names)}.")
    lines.append("")
    lines.append("2. PAIR every activity metric with its business-impact twin. Show the")
    lines.append("   pairing explicitly in the readout (e.g., 'visitors -> MQLs from organic',")
    lines.append("   'open rate -> trial conversions from email'). The board does not want to")
    lines.append("   see activity numbers without their downstream impact pair.")
    if activity_names:
        lines.append(f"   Activity metrics to pair: {', '.join(activity_names)}.")
    lines.append("")
    lines.append("3. QUANTIFY the dollar impact of moving each red-zone metric back to target.")
    lines.append("   Translate gap into ARR, pipeline, or margin terms a CFO understands.")
    lines.append("```")
    lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a board-ready marketing scorecard from raw metrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--metrics", required=True, help="Path to CSV or JSON metrics file.")
    parser.add_argument(
        "--objectives",
        default="",
        help="Comma-separated business objectives the marketing org owns.",
    )
    parser.add_argument("--output-md", default=None, help="Optional output markdown path.")
    args = parser.parse_args()

    metrics = load_metrics(args.metrics)
    if not metrics:
        print("ERROR: no metrics parsed. Check file format.", file=sys.stderr)
        return 1

    objectives = [o.strip() for o in args.objectives.split(",") if o.strip()]

    # enrich every metric
    for m in metrics:
        var, zone = classify_zone(m["name"], m["current"], m["target"])
        m["variance"] = var
        m["zone"] = zone
        m["kind"] = classify_activity_vs_impact(m["name"], m.get("category", ""))

    top3 = pick_top_three(metrics, objectives)
    md = render_markdown(metrics, objectives, top3)

    if args.output_md:
        with open(args.output_md, "w") as fh:
            fh.write(md)
        print(f"Scorecard written to {args.output_md}")
    else:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
