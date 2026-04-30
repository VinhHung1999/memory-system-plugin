#!/usr/bin/env python3
"""
diagnose_red_zone.py — Walk the 4-step root-cause detective method on a
red-zone marketing KPI: Gather Evidence -> Break Aggregate -> Identify
Pattern -> Conclude Root Cause. Output is a structured diagnosis with a
corrective action that targets cause (not symptom), success indicator,
and verification cadence.

Stdlib only.

Usage:
  python3 diagnose_red_zone.py \\
    --kpi "Paid search conversion rate" \\
    --current 2.1 --target 3.5 \\
    --evidence '{"channels": {"google_search": 1.4, "bing": 3.8}, \\
                 "campaigns": {"demo-request": 1.2, "free-trial": 3.6}, \\
                 "trend": "declining 4 weeks", \\
                 "segments": {"smb": 2.5, "enterprise": 0.8}}'
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Step 1 — gather evidence (list what we have, flag what's missing)
# ---------------------------------------------------------------------------

EXPECTED_EVIDENCE_KEYS = [
    "channels",      # channel-level breakdown (e.g., google vs bing)
    "campaigns",     # campaign-level breakdown
    "segments",      # segment breakdown (e.g., smb vs enterprise)
    "trend",         # time-series description ("declining 4 weeks")
    "external",      # competitor / seasonality / market events
    "funnel",        # funnel-stage breakdown
    "data_validation",  # has the data been validated for tracking errors?
]


def gather_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    present = {k: v for k, v in evidence.items() if v not in (None, "", {}, [])}
    missing = [k for k in EXPECTED_EVIDENCE_KEYS if k not in present]
    return {"present": present, "missing": missing}


# ---------------------------------------------------------------------------
# Step 2 — break the aggregate
# ---------------------------------------------------------------------------

def break_aggregate(current: float, target: float, evidence: dict[str, Any]) -> dict[str, Any]:
    findings: list[str] = []
    concentrations: list[dict[str, Any]] = []

    for dim_key in ("channels", "campaigns", "segments"):
        dim = evidence.get(dim_key)
        if not isinstance(dim, dict) or not dim:
            continue
        # Find sub-elements significantly under target and significantly above target
        below = [(name, val) for name, val in dim.items() if isinstance(val, (int, float)) and val < target * 0.85]
        above = [(name, val) for name, val in dim.items() if isinstance(val, (int, float)) and val >= target * 0.95]
        if below:
            below_str = ", ".join(f"{n}={v}" for n, v in below)
            findings.append(f"{dim_key}: underperformers -> {below_str} (vs target {target})")
        if above:
            above_str = ", ".join(f"{n}={v}" for n, v in above)
            findings.append(f"{dim_key}: healthy -> {above_str}")
        if below and above:
            concentrations.append(
                {
                    "dimension": dim_key,
                    "underperformers": [n for n, _ in below],
                    "healthy": [n for n, _ in above],
                }
            )

    return {"findings": findings, "concentrations": concentrations}


# ---------------------------------------------------------------------------
# Step 3 — identify pattern
# ---------------------------------------------------------------------------

def identify_pattern(broken: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    concentrations = broken.get("concentrations", [])
    trend = (evidence.get("trend") or "").lower()

    if concentrations:
        pattern = "concentrated underperformance"
        rationale = (
            "Specific channels/campaigns/segments are dragging the aggregate down "
            "while others perform on or above target. The aggregate KPI is masking the "
            "real story; fix targets the concentration, not the average."
        )
    elif "declin" in trend or "falling" in trend or "down" in trend:
        pattern = "broad decline"
        rationale = (
            "Performance is dropping across the board with no clear concentration. "
            "Look for systemic causes: tracking change, attribution model drift, "
            "macro/seasonality, or org-wide execution issue."
        )
    elif "cyclic" in trend or "seasonal" in trend or "weekly" in trend:
        pattern = "cyclical / seasonal"
        rationale = (
            "Pattern matches a known cycle. Compare same-period YoY before treating as a problem."
        )
    else:
        pattern = "unknown — collect more evidence"
        rationale = (
            "Insufficient evidence to call a pattern. Run channel/campaign/segment "
            "breakdown and 4-week trend before recommending corrective action."
        )

    return {"pattern": pattern, "rationale": rationale}


# ---------------------------------------------------------------------------
# Step 4 — conclude root cause vs symptom
# ---------------------------------------------------------------------------

def conclude_root_cause(broken: dict[str, Any], pattern: dict[str, Any], kpi: str, evidence: dict[str, Any]) -> dict[str, Any]:
    concentrations = broken.get("concentrations", [])
    trend = (evidence.get("trend") or "").lower()
    external = evidence.get("external") or ""

    symptom = f"{kpi} is below target."
    if concentrations:
        # build a specific cause hypothesis from the concentration
        bits = []
        for c in concentrations:
            bits.append(
                f"{c['dimension']} '{', '.join(c['underperformers'])}' is underperforming "
                f"while '{', '.join(c['healthy'])}' is healthy"
            )
        concentration_text = "; ".join(bits)
        cause_hypotheses = []
        # generic root-cause hypothesis classes for marketing
        cause_hypotheses.append(
            f"Competitor outbid us on the keyword set targeting that segment/campaign"
        )
        cause_hypotheses.append("Ad creative or landing-page change caused conversion fatigue or breakage")
        cause_hypotheses.append("Audience targeting drift (the campaign is now reaching out-of-ICP traffic)")
        cause_hypotheses.append("Attribution model or tracking change altered the measurement of this segment")

        if external:
            cause_hypotheses.insert(0, f"External event noted: {external}")

        # if trend has a specific date, use it
        date_hint = ""
        for token in trend.split():
            if any(month in token for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]):
                date_hint = token
                break

        cause = (
            f"Concentration: {concentration_text}. "
            f"This is the root cause to investigate, NOT the aggregate KPI."
        )
        if date_hint:
            cause += f" Onset signal: '{date_hint}' — overlay this date on competitive bids, ad-copy/landing-page change log, and tracking changes to confirm the trigger."

        return {
            "symptom": symptom,
            "cause": cause,
            "cause_hypotheses": cause_hypotheses,
            "verification_steps": [
                "Pull last 90 days of bid history and competitor share-of-voice on the affected campaign keywords",
                "Diff ad creative + landing page changes around the onset date",
                "Validate tracking and attribution: confirm pixels firing, conversion goals correctly mapped",
                "Re-segment by geo / device / new vs returning to confirm the concentration holds",
            ],
        }

    # broad decline
    return {
        "symptom": symptom,
        "cause": (
            f"No concentration detected. {pattern['rationale']} "
            "Before recommending a fix, validate data integrity (most common cause of "
            "broad declines that aren't real)."
        ),
        "cause_hypotheses": [
            "Tracking break / pixel misfire / attribution model change",
            "Macro shift (seasonality, market downturn)",
            "Org-wide execution slip (team capacity, vendor change, brand crisis)",
        ],
        "verification_steps": [
            "Run data validation FIRST: confirm sources, calculations, attribution",
            "Check 1-year and 2-year YoY for the same period",
            "Survey downstream funnel stages for shared upstream cause",
        ],
    }


# ---------------------------------------------------------------------------
# Corrective action recommendation
# ---------------------------------------------------------------------------

def recommend_action(broken: dict[str, Any], conclusion: dict[str, Any], kpi: str, current: float, target: float) -> dict[str, Any]:
    concentrations = broken.get("concentrations", [])
    if concentrations:
        first = concentrations[0]
        underperformer = first["underperformers"][0] if first["underperformers"] else "the underperforming sub-segment"
        action = (
            f"Targeted intervention on {first['dimension']} '{underperformer}'. "
            f"Pause/reduce spend on the underperforming sub-segment, run a 7-day diagnostic "
            f"(creative refresh + bid recalibration + landing-page check), and re-bid "
            f"only after the verification steps confirm the cause. "
            f"DO NOT cut the healthy sub-segment(s)."
        )
    else:
        action = (
            f"Hold off on broad campaign restructuring. Run data validation + funnel "
            f"decomposition first. Only structural change after a falsifiable hypothesis is in hand."
        )

    success_indicator = (
        f"{kpi} returns from {current} to within 5pp of target ({target}) in 2-3 weeks, "
        f"with the corrective action attributable to the move (not coincidence)."
    )

    return {
        "action": action,
        "success_indicator": success_indicator,
        "verification_cadence": "Weekly review until back in green zone for 2 consecutive weeks.",
    }


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(kpi: str, current: float, target: float, evidence: dict[str, Any],
           gathered: dict[str, Any], broken: dict[str, Any],
           pattern: dict[str, Any], conclusion: dict[str, Any],
           recommendation: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Red-Zone Diagnosis: {kpi}")
    lines.append("")
    lines.append(f"**Current:** {current}    **Target:** {target}    **Gap:** {current - target}")
    lines.append("")

    lines.append("## Step 1 — Gather evidence")
    lines.append("")
    lines.append("**Available:**")
    if gathered["present"]:
        for k, v in gathered["present"].items():
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- (none)")
    lines.append("")
    if gathered["missing"]:
        lines.append("**Missing (collect before final action):**")
        for k in gathered["missing"]:
            lines.append(f"- {k}")
        lines.append("")

    lines.append("## Step 2 — Break the aggregate")
    lines.append("")
    if broken["findings"]:
        for f in broken["findings"]:
            lines.append(f"- {f}")
    else:
        lines.append("_No sub-dimensional evidence supplied. Re-run with channel/campaign/segment data._")
    lines.append("")

    lines.append("## Step 3 — Identify pattern")
    lines.append("")
    lines.append(f"**Pattern:** {pattern['pattern']}")
    lines.append("")
    lines.append(pattern["rationale"])
    lines.append("")

    lines.append("## Step 4 — Conclude root cause vs symptom")
    lines.append("")
    lines.append(f"**Symptom:** {conclusion['symptom']}")
    lines.append("")
    lines.append(f"**Root cause:** {conclusion['cause']}")
    lines.append("")
    lines.append("**Cause hypotheses to verify (rank-ordered):**")
    for h in conclusion["cause_hypotheses"]:
        lines.append(f"- {h}")
    lines.append("")
    lines.append("**Verification steps:**")
    for v in conclusion["verification_steps"]:
        lines.append(f"- {v}")
    lines.append("")

    lines.append("## Corrective action")
    lines.append("")
    lines.append(recommendation["action"])
    lines.append("")
    lines.append(f"**Success indicator:** {recommendation['success_indicator']}")
    lines.append("")
    lines.append(f"**Verification cadence:** {recommendation['verification_cadence']}")
    lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Walk the 4-step root-cause method on a red-zone marketing KPI.")
    parser.add_argument("--kpi", required=True, help="Red-zone KPI name.")
    parser.add_argument("--current", required=True, type=float, help="Current value.")
    parser.add_argument("--target", required=True, type=float, help="Target value.")
    parser.add_argument(
        "--evidence",
        default="{}",
        help='JSON evidence dict, e.g. {"channels": {...}, "campaigns": {...}, "trend": "..."}',
    )
    args = parser.parse_args()

    try:
        evidence = json.loads(args.evidence) if args.evidence else {}
    except json.JSONDecodeError as e:
        print(f"ERROR: --evidence must be valid JSON: {e}", file=sys.stderr)
        return 1

    gathered = gather_evidence(evidence)
    broken = break_aggregate(args.current, args.target, evidence)
    pattern = identify_pattern(broken, evidence)
    conclusion = conclude_root_cause(broken, pattern, args.kpi, evidence)
    recommendation = recommend_action(broken, conclusion, args.kpi, args.current, args.target)

    sys.stdout.write(
        render(args.kpi, args.current, args.target, evidence, gathered, broken, pattern, conclusion, recommendation)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
