#!/usr/bin/env python3
"""validate_segment.py — VALIDATE mode for the Customer Segmentation Canvas skill.

Stdlib only. Runs the IE 5-filter MAPDA test against a proposed segment
description plus a structured evidence dict, and emits pass / fail / reasoning
per filter, revision suggestions, and a final verdict (KEEP / REVISE / REPLACE).

Usage:
  python3 validate_segment.py \\
      --segment "Heads of People at remote-first US companies (200-2000) ..." \\
      --evidence '{"size":"8000 companies","channel":"HR Slack groups + RUNNING REMOTE","arpc_range":"15K-45K","needs_diff":"high","capability_fit":"high"}'
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------- Filter result data class ----------

@dataclass
class FilterResult:
    name: str
    passed: bool
    score: int  # 0 = fail, 1 = weak, 2 = pass
    reasoning: str
    revision_suggestion: str = ""


# ---------- Helpers ----------

VAGUE_CHANNEL_TOKENS = [
    "marketing campaigns",
    "marketing",
    "advertising",
    "online",
    "digital marketing",
    "social media",
    "various channels",
    "multiple channels",
    "tbd",
    "to be defined",
]

VAGUE_SIZE_TOKENS = [
    "many",
    "lots",
    "large",
    "huge",
    "tbd",
    "to be sized",
    "unknown",
    "?",
]

VANITY_PSYCHO_TOKENS = [
    "forward-thinking",
    "forward thinking",
    "innovative",
    "innovation-embracing",
    "embraces new technology",
    "embrace new technology",
    "embraces innovation",
    "values innovation",
    "values quality",
    "modern",
    "ambitious",
    "visionary",
    "early adopters",
    "growth-minded",
    "growth minded",
    "tech-savvy",
    "tech savvy",
    "thought leaders",
    "innovators",
    "disruptive",
]


def has_concrete_number(text: str) -> Optional[str]:
    """Return matched number snippet if a concrete count is present."""
    m = re.search(r"\b(\d[\d,\.]*)\s*(k|m|million|thousand|companies|accounts|customers|users|orgs|firms)?\b", text, re.I)
    if m:
        return m.group(0)
    return None


def parse_arpc(text: str) -> Optional[Tuple[float, float]]:
    """Parse ARPC range from text like '15K-45K' or '$5K-$15K' or '5000-15000'."""
    if not text:
        return None
    cleaned = text.replace("$", "").replace(",", "").lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(k|m)?\s*[-to]+\s*(\d+(?:\.\d+)?)\s*(k|m)?", cleaned)
    if m:
        lo = float(m.group(1))
        hi = float(m.group(3))
        if m.group(2) == "k":
            lo *= 1_000
        elif m.group(2) == "m":
            lo *= 1_000_000
        if m.group(4) == "k":
            hi *= 1_000
        elif m.group(4) == "m":
            hi *= 1_000_000
        return (lo, hi)
    m2 = re.search(r"(\d+(?:\.\d+)?)\s*(k|m)?", cleaned)
    if m2:
        v = float(m2.group(1))
        if m2.group(2) == "k":
            v *= 1_000
        elif m2.group(2) == "m":
            v *= 1_000_000
        return (v, v)
    return None


def parse_size(text: str) -> Optional[float]:
    if not text:
        return None
    cleaned = text.replace(",", "").lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(k|m|thousand|million)?", cleaned)
    if not m:
        return None
    v = float(m.group(1))
    unit = m.group(2)
    if unit in ("k", "thousand"):
        v *= 1_000
    elif unit in ("m", "million"):
        v *= 1_000_000
    return v


# ---------- The 5 filters ----------

def filter_measurable(segment: str, evidence: Dict[str, Any]) -> FilterResult:
    raw = str(evidence.get("size") or evidence.get("size_estimate") or "").strip()
    if not raw:
        return FilterResult(
            name="Measurable",
            passed=False,
            score=0,
            reasoning="No sizing evidence supplied. We cannot tell how many customers exist in this segment, so we cannot size revenue potential.",
            revision_suggestion="Source a count from a public dataset (LinkedIn Sales Nav, Crunchbase, ZoomInfo, BuiltWith, Apollo, government statistics). Quote the count and the source.",
        )
    # vague tokens
    if any(tok in raw.lower() for tok in VAGUE_SIZE_TOKENS) and not has_concrete_number(raw):
        return FilterResult(
            name="Measurable",
            passed=False,
            score=0,
            reasoning=f"Sizing language is vague: '{raw}'. Vague sizing fails the Measurable filter because it cannot drive a TAM-SAM-SOM model.",
            revision_suggestion="Replace vague language with a concrete count plus source (e.g. 'approx 8,000 companies match per LinkedIn Sales Nav firmographic filter on date X').",
        )
    if has_concrete_number(raw):
        return FilterResult(
            name="Measurable",
            passed=True,
            score=2,
            reasoning=f"Concrete count present: '{raw}'. Segment is sizeable and the size can be re-verified.",
        )
    return FilterResult(
        name="Measurable",
        passed=False,
        score=1,
        reasoning=f"Sizing evidence supplied but not numeric: '{raw}'.",
        revision_suggestion="Convert qualitative language into a specific count from a named source.",
    )


def filter_accessible(segment: str, evidence: Dict[str, Any]) -> FilterResult:
    raw = str(evidence.get("channel") or evidence.get("channels") or "").strip()
    if not raw:
        return FilterResult(
            name="Accessible",
            passed=False,
            score=0,
            reasoning="No channel evidence supplied. We do not know how to reach this segment, so we cannot allocate GTM budget.",
            revision_suggestion="Name the specific channels: a marketplace (e.g., NetSuite, Salesforce AppExchange), a partner network, a community (Slack / Discord), a conference series (e.g., RUNNING REMOTE, Pavilion), or a publication.",
        )
    raw_l = raw.lower()
    has_concrete = any(c in raw_l for c in ["marketplace", "appexchange", "slack group", "discord", "conference", "podcast", "newsletter", "community", "linkedin", "partner network", "association", "summit", "forum", "running remote", "pavilion", "remote forward"])
    has_named_event = bool(re.search(r"[A-Z][A-Za-z]+\s+(Summit|Forward|Forum|Con|Conference|Live|Talks|Forge)", raw))
    is_vague = any(tok == raw_l.strip() or tok in raw_l for tok in VAGUE_CHANNEL_TOKENS) and not has_concrete and not has_named_event
    if is_vague:
        return FilterResult(
            name="Accessible",
            passed=False,
            score=0,
            reasoning=f"Channel description is vague ('{raw}'). 'Marketing campaigns' or 'digital marketing' is not a channel — it is a category. The Accessible filter requires a specific, identifiable touchpoint.",
            revision_suggestion="Replace generic 'marketing' with named channels: which marketplace, which community, which conference, which partner. If you cannot name them, you cannot reach this segment yet.",
        )
    if has_concrete or has_named_event:
        return FilterResult(
            name="Accessible",
            passed=True,
            score=2,
            reasoning=f"Named channel(s) supplied: '{raw}'. Reach is operationally feasible.",
        )
    return FilterResult(
        name="Accessible",
        passed=False,
        score=1,
        reasoning=f"Channel evidence supplied but not concrete: '{raw}'.",
        revision_suggestion="Convert into a named list of marketplaces / partners / communities / conferences.",
    )


def filter_profitable(segment: str, evidence: Dict[str, Any]) -> FilterResult:
    arpc_raw = str(evidence.get("arpc_range") or evidence.get("arpc_estimate") or evidence.get("arpc") or "").strip()
    size_raw = str(evidence.get("size") or evidence.get("size_estimate") or "").strip()
    arpc = parse_arpc(arpc_raw)
    size = parse_size(size_raw)
    if not arpc:
        return FilterResult(
            name="Profitable",
            passed=False,
            score=0,
            reasoning="No ARPC / ACV evidence supplied. We cannot estimate whether this segment generates enough value to justify GTM investment.",
            revision_suggestion="Provide an ARPC range (e.g. '$15K-$45K ACV based on competitor pricing'). Even a rough range unblocks the Profitable filter.",
        )
    if not size:
        return FilterResult(
            name="Profitable",
            passed=False,
            score=1,
            reasoning=f"ARPC range provided ({arpc_raw}) but segment size missing. Profitability needs both axes (count x ARPC).",
            revision_suggestion="Provide a count for the segment so we can compute a TAM and a 1-3pct SOM.",
        )
    lo, hi = arpc
    # Year-1 SOM at 1pct penetration:
    som_lo = lo * size * 0.01
    som_hi = hi * size * 0.01
    if som_hi < 1_000_000:
        return FilterResult(
            name="Profitable",
            passed=False,
            score=0,
            reasoning=(
                f"At ARPC {arpc_raw} and size {int(size):,}, even 1pct penetration yields only "
                f"approx ${int(som_lo):,}-${int(som_hi):,} Year-1 SOM. This is below the $1M threshold "
                "where the GTM motion typically pays back."
            ),
            revision_suggestion="Either expand the segment (broader definition, more geos), raise ARPC (premium feature bundle), or replace with a bigger segment.",
        )
    return FilterResult(
        name="Profitable",
        passed=True,
        score=2,
        reasoning=(
            f"At ARPC {arpc_raw} and size {int(size):,}, even 1pct Year-1 penetration yields "
            f"approx ${int(som_lo):,}-${int(som_hi):,} SOM. Economics are real."
        ),
    )


def filter_differentiable(segment: str, evidence: Dict[str, Any]) -> FilterResult:
    raw = str(evidence.get("needs_diff") or "").strip().lower()
    seg_l = segment.lower()
    has_vanity = any(tok in seg_l for tok in VANITY_PSYCHO_TOKENS)
    if has_vanity and not raw:
        return FilterResult(
            name="Differentiable",
            passed=False,
            score=0,
            reasoning=(
                "Segment description leans on vanity / aspirational language "
                "('forward-thinking', 'innovative', 'embraces new technology'). Every "
                "buyer self-identifies this way. The Differentiable filter requires that "
                "this group actually responds DIFFERENTLY to marketing-mix changes than "
                "adjacent groups — not that they self-describe as different."
            ),
            revision_suggestion="Replace aspirational language with observable behavior or measurable role: e.g. 'CTOs at $50M+ SaaS who are evaluating their data warehouse in next 12 months'. Behavior + role is testable; aspiration is not.",
        )
    if raw == "high":
        if has_vanity:
            return FilterResult(
                name="Differentiable",
                passed=False,
                score=1,
                reasoning="Evidence claims needs_diff=high, but the segment description still uses vanity language. Re-anchor on observable behavior before accepting the claim.",
                revision_suggestion="Rewrite the segment definition around what these customers DO differently, not what they BELIEVE about themselves.",
            )
        return FilterResult(
            name="Differentiable",
            passed=True,
            score=2,
            reasoning="Evidence indicates these customers respond differently than adjacent segments. They cluster on need-similarity, not just demographic similarity.",
        )
    if raw == "medium":
        return FilterResult(
            name="Differentiable",
            passed=False,
            score=1,
            reasoning="Needs_diff=medium suggests need-similarity is partial. The segment may collapse into an adjacent one under stress.",
            revision_suggestion="Run 5-7 customer interviews comparing this segment to its nearest neighbor. If their JTBDs do not diverge, merge them.",
        )
    if raw == "low":
        return FilterResult(
            name="Differentiable",
            passed=False,
            score=0,
            reasoning="Needs_diff=low means these customers do not respond meaningfully differently from adjacent segments. This is not a real segment.",
            revision_suggestion="Either find a behavioral wedge that splits them from neighbors, or merge into the adjacent segment.",
        )
    return FilterResult(
        name="Differentiable",
        passed=False,
        score=1,
        reasoning="No needs_diff evidence supplied. We cannot tell whether this segment behaves differently than neighbors.",
        revision_suggestion="Supply needs_diff (high / medium / low) backed by primary research (interviews) or observable behavior data (usage, conversion, churn divergence).",
    )


def filter_actionable(segment: str, evidence: Dict[str, Any]) -> FilterResult:
    raw = str(evidence.get("capability_fit") or "").strip().lower()
    if raw == "high":
        return FilterResult(
            name="Actionable",
            passed=True,
            score=2,
            reasoning="Capability fit is high — current product, sales motion, and CS motion can serve this segment without significant new build / hire.",
        )
    if raw == "medium":
        return FilterResult(
            name="Actionable",
            passed=False,
            score=1,
            reasoning="Capability fit is medium. Some new build / hire / partnership is required before serving this segment at scale.",
            revision_suggestion="Quantify the gap: which product capabilities, which sales-team archetype, which CS playbook? Cost the gap. If under 1 quarter and under $X to close, accept; else REVISE.",
        )
    if raw == "low":
        return FilterResult(
            name="Actionable",
            passed=False,
            score=0,
            reasoning="Capability fit is low. Serving this segment would require significant new product build, new sales motion, or new operations — wrong segment for current resources.",
            revision_suggestion="Either pick a closer-fit segment now and revisit this one in 12-18 months, or commit to the buildout as a deliberate strategic bet (not a marketing decision alone).",
        )
    return FilterResult(
        name="Actionable",
        passed=False,
        score=1,
        reasoning="No capability_fit evidence supplied.",
        revision_suggestion="Supply capability_fit (high / medium / low) based on product, sales, and CS readiness assessments.",
    )


# ---------- Verdict ----------

def compute_verdict(results: List[FilterResult]) -> str:
    passes = sum(1 for r in results if r.passed)
    fails_hard = sum(1 for r in results if r.score == 0)
    if passes == 5:
        return "KEEP"
    if fails_hard >= 3:
        return "REPLACE"
    if fails_hard >= 2:
        return "REPLACE"
    return "REVISE"


# ---------- Markdown rendering ----------

def render_markdown(segment: str, evidence: Dict[str, Any], results: List[FilterResult], verdict: str) -> str:
    lines: List[str] = []
    lines.append("# Segment Validation — MAPDA 5-filter test")
    lines.append("")
    lines.append("## Segment under review")
    lines.append("")
    lines.append(f"> {segment}")
    lines.append("")
    if evidence:
        lines.append("## Evidence supplied")
        for k, v in evidence.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    lines.append("## Filter-by-filter result")
    lines.append("")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        lines.append(f"### {r.name}: {status}  (score {r.score}/2)")
        lines.append("")
        lines.append(r.reasoning)
        if r.revision_suggestion:
            lines.append("")
            lines.append(f"**Revision suggestion**: {r.revision_suggestion}")
        lines.append("")

    passes = sum(1 for r in results if r.passed)
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Passed**: {passes} / 5 filters")
    lines.append("")
    lines.append(f"## Verdict: {verdict}")
    lines.append("")
    if verdict == "KEEP":
        lines.append("This segment passes all 5 MAPDA filters. Promote to the segmentation canvas. Define explicit ANTI-segments next, then hand off to the positioning-statement-builder skill.")
    elif verdict == "REVISE":
        lines.append("This segment fails 1-2 filters. Apply the revision suggestions above, refresh evidence, and re-run validation. Do NOT commit GTM budget against the current definition.")
    else:
        lines.append("This segment fails core filters and is not a real segment. Replace it: re-anchor on observable behavior + role + need, gather concrete sizing and channel evidence, then propose a fresh candidate.")
    lines.append("")
    return "\n".join(lines)


# ---------- CLI entry ----------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="VALIDATE a proposed segment against IE 5-filter MAPDA.",
    )
    parser.add_argument(
        "--segment",
        required=True,
        help="Proposed segment description (free text).",
    )
    parser.add_argument(
        "--evidence",
        default="{}",
        help='JSON dict with keys size, channel, arpc_estimate (or arpc_range), needs_diff, capability_fit.',
    )
    args = parser.parse_args(argv)

    try:
        evidence: Dict[str, Any] = json.loads(args.evidence) if args.evidence else {}
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Could not parse --evidence JSON: {e}\n")
        return 2

    results: List[FilterResult] = [
        filter_measurable(args.segment, evidence),
        filter_accessible(args.segment, evidence),
        filter_profitable(args.segment, evidence),
        filter_differentiable(args.segment, evidence),
        filter_actionable(args.segment, evidence),
    ]
    verdict = compute_verdict(results)

    sys.stdout.write(render_markdown(args.segment, evidence, results, verdict))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
