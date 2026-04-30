#!/usr/bin/env python3
"""
validate_kpi.py — Apply the 3-filter check (strategic alignment, measurability,
actionability) to a single proposed marketing KPI before adding it to the
board scorecard.

Stdlib only.

Usage:
  python3 validate_kpi.py \\
    --kpi "Email open rate" \\
    --objective "Increase trial-to-paid conversion by 25 percent in Q3"
"""

from __future__ import annotations

import argparse
import re
import sys


# ---------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------

OUTCOME_VERBS = [
    "acquire", "acquisition", "retain", "retention",
    "expand", "expansion", "grow", "growth",
    "reduce", "lower", "decrease",
    "win", "convert", "conversion", "increase", "lift",
    "renew", "upsell", "cross-sell",
]

ACTIVITY_VERBS = [
    "run", "launch", "post", "send", "publish", "deliver",
    "schedule", "broadcast", "distribute", "produce",
]

# Words that imply a clean built-in measurement
MEASURABLE_TOKENS = [
    "rate", "ratio", "count", "time", "dollar", "$", "percent", "%", "pp",
    "score", "index", "duration", "frequency", "amount", "number",
    "value", "cost", "revenue", "lifetime", "payback", "cac", "ltv",
]

# Words that suggest heroic measurement (subjective without explicit instrument)
QUALITATIVE_RED_FLAGS = [
    "sentiment", "perception", "feeling", "vibe",
    "qualitative", "buzz", "impression of", "love",
]

# KPIs known to lack a clean corrective lever in isolation
LOW_ACTIONABILITY = [
    "nps", "net promoter", "brand health", "brand equity",
    "awareness", "perception", "sentiment", "share of voice",
]

# KPIs that map to clear corrective levers
HIGH_ACTIONABILITY = [
    "cac payback", "cac_payback", "ltv/cac", "ltv:cac",
    "conversion rate", "channel conversion", "trial-to-paid",
    "mql-to-sql", "sql-to-win", "pipeline coverage",
    "cost per acquisition", "cost per lead", "cpc", "cpa",
    "open-to-trial", "click-to-trial",
]

# Vanity activity metrics (extra penalty in alignment + actionability)
PURE_VANITY = [
    "follower count", "followers",
    "likes", "shares", "impressions",
    "page views", "video views",
    "subscriber count",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def tokenize(s: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[a-z][a-z0-9\-]+", s.lower())]


def contains_any(text: str, vocab: list[str]) -> list[str]:
    text_l = text.lower()
    hits = [v for v in vocab if v in text_l]
    return hits


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

def filter_strategic_alignment(kpi: str, objective: str) -> dict:
    obj_tokens = set(tokenize(objective))
    kpi_tokens = set(tokenize(kpi))

    shared = obj_tokens & kpi_tokens
    # remove common stopword-ish noise
    noise = {"by", "in", "the", "a", "of", "to", "and", "for", "our", "this", "with"}
    shared -= noise

    outcome_hits = contains_any(kpi, OUTCOME_VERBS) + contains_any(objective, OUTCOME_VERBS)
    activity_hits = contains_any(kpi, ACTIVITY_VERBS)
    vanity_hits = contains_any(kpi, PURE_VANITY)

    pass_ = True
    reasons = []
    suggestion = None

    if vanity_hits:
        pass_ = False
        reasons.append(f"KPI is a known vanity metric ({', '.join(vanity_hits)}) that does not trace to business outcomes.")
    if not shared and not outcome_hits:
        pass_ = False
        reasons.append(
            f"No vocabulary overlap between KPI and objective. "
            f"The KPI does not visibly trace to the stated objective."
        )
    if activity_hits and not outcome_hits:
        pass_ = False
        reasons.append(
            f"KPI uses activity verbs ({', '.join(activity_hits)}) without business-outcome framing."
        )

    if pass_:
        reasons.append(
            f"KPI vocabulary aligns with objective (shared tokens: {', '.join(sorted(shared)) or 'outcome verbs detected'})."
        )
    else:
        suggestion = (
            f"Replace with a metric that directly measures the objective. "
            f"For '{objective}', consider a metric whose name contains the objective's outcome "
            f"(e.g. trial-to-paid conversion rate, sourced ARR, qualified pipeline contribution)."
        )

    return {
        "filter": "Strategic alignment",
        "pass": pass_,
        "reasons": reasons,
        "suggestion": suggestion,
    }


def filter_measurability(kpi: str, definition: str) -> dict:
    blob = (kpi + " " + (definition or "")).lower()
    measurable = contains_any(blob, MEASURABLE_TOKENS)
    qualitative = contains_any(blob, QUALITATIVE_RED_FLAGS)

    pass_ = True
    reasons = []
    suggestion = None

    if qualitative and not definition:
        pass_ = False
        reasons.append(
            f"KPI uses qualitative language ({', '.join(qualitative)}) without an explicit measurement method."
        )
        suggestion = (
            "Either (a) anchor to an instrument: 'NPS via post-onboarding survey, n>=200/mo' "
            "or (b) replace with a quantitative proxy."
        )
    elif not measurable:
        pass_ = False
        reasons.append("KPI name has no measurement-shaped tokens (rate, count, ratio, dollar, time, percent).")
        suggestion = "Restate with explicit unit, e.g. '<KPI>-rate', '<KPI> per visit', '<KPI> in dollars'."
    else:
        reasons.append(f"Measurement-ready tokens present ({', '.join(measurable)}).")

    return {
        "filter": "Measurability",
        "pass": pass_,
        "reasons": reasons,
        "suggestion": suggestion,
    }


def filter_actionability(kpi: str) -> dict:
    low = contains_any(kpi, LOW_ACTIONABILITY)
    high = contains_any(kpi, HIGH_ACTIONABILITY)
    vanity = contains_any(kpi, PURE_VANITY)

    pass_ = True
    reasons = []
    suggestion = None

    if vanity:
        pass_ = False
        reasons.append(
            f"Vanity KPI ({', '.join(vanity)}) has no clear corrective lever — when it dips, "
            f"the team has no specific action to take that wouldn't be guesswork."
        )
        suggestion = (
            "Pair with a downstream conversion metric (e.g. social-sourced trial signups, "
            "social-influenced pipeline, social-to-paid conversion rate) so a dip triggers a specific fix."
        )
    elif low and not high:
        pass_ = False
        reasons.append(
            f"KPI ({', '.join(low)}) is a directional indicator without a clean corrective lever in isolation."
        )
        suggestion = (
            "Keep as a directional indicator but pair with a tactical KPI that has a clear lever "
            "(e.g. NPS + onboarding-completion rate; brand health + share of qualified search demand)."
        )
    else:
        if high:
            reasons.append(f"Maps to clear corrective levers ({', '.join(high)}).")
        else:
            reasons.append("KPI appears actionable; identify the specific corrective lever before adding to scorecard.")

    return {
        "filter": "Actionability",
        "pass": pass_,
        "reasons": reasons,
        "suggestion": suggestion,
    }


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def final_verdict(filters: list[dict]) -> str:
    fails = sum(1 for f in filters if not f["pass"])
    if fails == 0:
        return "KEEP"
    if fails == 1:
        return "REVISE"
    return "REPLACE"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def render(kpi: str, objective: str, definition: str, filters: list[dict], verdict: str) -> str:
    lines = []
    lines.append(f"# KPI Validation: {kpi}")
    lines.append("")
    lines.append(f"**Stated objective:** {objective}")
    if definition:
        lines.append(f"**Definition:** {definition}")
    lines.append("")
    lines.append("## 3-filter check")
    lines.append("")
    for f in filters:
        status = "PASS" if f["pass"] else "FAIL"
        lines.append(f"### {f['filter']}: {status}")
        for r in f["reasons"]:
            lines.append(f"- {r}")
        if f["suggestion"]:
            lines.append("")
            lines.append(f"_Revision suggestion:_ {f['suggestion']}")
        lines.append("")
    lines.append("## Final verdict")
    lines.append("")
    lines.append(f"**{verdict}**")
    lines.append("")
    if verdict == "KEEP":
        lines.append("All three filters pass. Add to scorecard with explicit owner + review cadence.")
    elif verdict == "REVISE":
        lines.append("One filter fails. Apply the revision suggestion and re-validate before adding.")
    else:
        lines.append(
            "Two or more filters fail. The KPI does not earn a place on the executive scorecard. "
            "Replace with a KPI that directly measures the stated objective and has a clear corrective lever."
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a single proposed marketing KPI against the 3-filter check."
    )
    parser.add_argument("--kpi", required=True, help="Proposed KPI name.")
    parser.add_argument("--objective", required=True, help="Strategic objective the KPI claims to serve.")
    parser.add_argument("--definition", default="", help="Optional explicit calculation definition.")
    args = parser.parse_args()

    filters = [
        filter_strategic_alignment(args.kpi, args.objective),
        filter_measurability(args.kpi, args.definition),
        filter_actionability(args.kpi),
    ]
    verdict = final_verdict(filters)
    sys.stdout.write(render(args.kpi, args.objective, args.definition, filters, verdict))
    return 0


if __name__ == "__main__":
    sys.exit(main())
