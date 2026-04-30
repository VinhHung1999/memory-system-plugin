#!/usr/bin/env python3
"""segment_canvas.py — DESIGN mode for the Customer Segmentation Canvas skill.

Stdlib only. Takes a market description, company stage, and objectives, and
emits a structured markdown canvas with:
  - recommended segmentation level
  - recommended criteria types
  - 2-4 candidate segment archetypes (keyword + pattern derived)
  - recommended Kotler segmentation strategy
  - next-step prompt for the LLM (validate via MAPDA, sharpen, map to positioning)

Usage:
  python3 segment_canvas.py \\
      --market "B2B fintech serving finance teams in companies 10M-500M revenue" \\
      --stage "Series B" \\
      --objectives "grow ARR 50pct, reduce CAC payback to under 14 months"
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional


# ---------- Stage normalization ----------

STAGE_BUCKETS = {
    "seed": "early",
    "pre-seed": "early",
    "series a": "early",
    "series-a": "early",
    "a": "early",
    "series b": "mid",
    "series-b": "mid",
    "b": "mid",
    "growth": "mid",
    "series c": "late",
    "series-c": "late",
    "c": "late",
    "series c+": "late",
    "late stage": "late",
    "late": "late",
    "public": "late",
    "mature": "late",
}


def normalize_stage(stage: str) -> str:
    s = stage.lower().strip()
    if s in STAGE_BUCKETS:
        return STAGE_BUCKETS[s]
    for key, bucket in STAGE_BUCKETS.items():
        if key in s:
            return bucket
    return "mid"


# ---------- Recommendation engine ----------

@dataclass
class LevelRecommendation:
    level: str
    rationale: str


@dataclass
class CriteriaRecommendation:
    primary: str
    secondary: str
    overlays: List[str]
    reasoning: str


@dataclass
class CandidateSegment:
    name: str
    who: str
    jtbd: str
    channel_hypothesis: str
    sizing_hypothesis: str


@dataclass
class StrategyRecommendation:
    name: str
    rationale: str
    risk: str


@dataclass
class CanvasOutput:
    market: str
    stage_input: str
    stage_bucket: str
    objectives: List[str]
    level: LevelRecommendation
    criteria: CriteriaRecommendation
    candidates: List[CandidateSegment]
    strategy: StrategyRecommendation
    notes: List[str] = field(default_factory=list)


# ---------- Level + criteria heuristics ----------

def recommend_level(stage_bucket: str, market_text: str) -> LevelRecommendation:
    text = market_text.lower()
    is_b2b = any(tok in text for tok in ["b2b", "enterprise", "saas", "platform", "companies", "teams", "finance teams", "ops teams", "controllers", "cfo"])
    is_b2c_mass = any(tok in text for tok in ["consumer", "retail", "household", "cpg", "shopper", "fmcg"]) and "mass" in text

    if stage_bucket == "early":
        return LevelRecommendation(
            level="niche",
            rationale=(
                "Early-stage companies (Seed / Series A) win by going narrow, not broad. "
                "Pick a single tight niche where the team can build deep know-how, achieve "
                "category leadership in one cluster, and earn premium pricing before "
                "expanding. Mass is structurally wrong at this stage; segments-of-one is "
                "premature without proven repeatability."
            ),
        )
    if stage_bucket == "mid":
        return LevelRecommendation(
            level="segment",
            rationale=(
                "At Series B / growth stage, the company has proven a beachhead and can "
                "responsibly expand into 1-2 adjacent segments with shared need-similarity. "
                "Avoid premature 'full coverage' before economics are solid; avoid retreating "
                "to a single niche if you have product-market fit signals across the cluster."
            ),
        )
    # late
    if is_b2b:
        return LevelRecommendation(
            level="segment",
            rationale=(
                "Late-stage B2B companies typically run market specialization or selective "
                "specialization across 2-4 segments. Full coverage is rarely correct in B2B "
                "because each segment has a distinct buying committee and channel."
            ),
        )
    if is_b2c_mass:
        return LevelRecommendation(
            level="mass",
            rationale=(
                "Late-stage B2C with homogeneous preferences may justify mass marketing "
                "for unit-cost economics. Re-test annually; markets fragment over time."
            ),
        )
    return LevelRecommendation(
        level="segment",
        rationale=(
            "Default to segment marketing with 2-4 differentiated value propositions. "
            "Re-evaluate vs full market coverage when scale economics demand it."
        ),
    )


def recommend_criteria(market_text: str) -> CriteriaRecommendation:
    text = market_text.lower()
    overlays: List[str] = []
    if any(tok in text for tok in ["country", "region", "city", "us ", "eu ", "apac", "global", "remote-first", "metro", "urban", "rural"]):
        overlays.append("geographic")
    if any(tok in text for tok in ["age", "income", "revenue", "size", "employees", "10m", "500m", "smb", "mid-market", "enterprise"]):
        overlays.append("demographic")

    return CriteriaRecommendation(
        primary="behavioral",
        secondary="psychographic",
        overlays=overlays,
        reasoning=(
            "Start with BEHAVIORAL (cluster customers by what they DO — usage rate, "
            "decision role, benefits sought, occasion of use). Behavior is observable "
            "and predicts future action better than self-reported attitudes. "
            "Layer PSYCHOGRAPHIC second (what they VALUE, attitudes, aspirations) to "
            "explain why behavior diverges. Use demographic and geographic ONLY as "
            "overlays for sizing and channel access — never as the primary criterion. "
            "Demographic-only segments fail the Differentiable filter because customers "
            "who look alike don't necessarily need different things."
        ),
    )


# ---------- Candidate segment generation ----------

ROLE_PATTERNS = [
    (re.compile(r"\bfinance teams?\b|\bcontrollers?\b|\bcfos?\b|\baccountants?\b|\bfp&a\b", re.I),
     ("Finance ops leader", "close the books faster and reduce manual reconciliation")),
    (re.compile(r"\bheads? of people\b|\bhr\b|\bchros?\b|\btalent\b|\bpeople ops?\b", re.I),
     ("People / HR leader", "scale onboarding and HR ops without a heavy HRIS")),
    (re.compile(r"\bctos?\b|\bvp engineering\b|\bplatform teams?\b|\bdevops\b|\bsre\b|\binfrastructure\b", re.I),
     ("Engineering leader", "ship faster and reduce platform toil")),
    (re.compile(r"\bcmos?\b|\bvp marketing\b|\bdemand gen\b|\bgrowth teams?\b", re.I),
     ("Marketing leader", "drive pipeline efficiency and brand differentiation")),
    (re.compile(r"\brevops\b|\bsales ops\b|\bvp sales\b|\bcros?\b", re.I),
     ("Revenue leader", "improve forecast accuracy and rep productivity")),
    (re.compile(r"\bcustomer success\b|\bcs leaders?\b|\bvp cs\b|\bsupport leaders?\b", re.I),
     ("CS leader", "reduce churn and expand existing accounts")),
    (re.compile(r"\bproduct managers?\b|\bcpos?\b|\bvp product\b", re.I),
     ("Product leader", "ship the right thing with less waste")),
    (re.compile(r"\bdata teams?\b|\banalysts?\b|\bdata engineers?\b|\bcdos?\b", re.I),
     ("Data leader", "deliver trusted analytics without the manual plumbing")),
]

SIZE_PATTERNS = [
    (re.compile(r"\bsmb\b|\bsmall\b.*\bbusiness\b|\b1-50\b|\b<\s*\$?\s*10m\b", re.I), "SMB (under $10M)"),
    (re.compile(r"\bmid-?market\b|\$?10\s*m[-\s]+\$?500\s*m|\$?20\s*m[-\s]+\$?200\s*m|\b50-?500\b|\b200-?2000\b", re.I), "Mid-market ($10M-$500M)"),
    (re.compile(r"\benterprise\b|\$?500\s*m\+|\bfortune\b", re.I), "Enterprise ($500M+)"),
]

GEO_PATTERNS = [
    (re.compile(r"\bus\b|\bunited states\b|\bnorth america\b|\bna\b", re.I), "US / North America"),
    (re.compile(r"\beu\b|\beurope\b|\bdach\b|\buk\b", re.I), "Europe"),
    (re.compile(r"\bapac\b|\basia\b|\bjapan\b|\bsingapore\b", re.I), "APAC"),
    (re.compile(r"\bglobal\b|\bworldwide\b", re.I), "Global"),
]


def detect_role_archetypes(market_text: str) -> List[tuple]:
    found = []
    seen = set()
    for pattern, (role, jtbd) in ROLE_PATTERNS:
        if pattern.search(market_text) and role not in seen:
            found.append((role, jtbd))
            seen.add(role)
    if not found:
        # generic fallback — emit two role-agnostic archetypes
        found = [
            ("Operational buyer (hands-on user)", "remove daily friction in the workflow"),
            ("Executive sponsor (budget owner)", "demonstrate measurable business outcome"),
        ]
    return found[:4]


def detect_size_band(market_text: str) -> str:
    for pattern, label in SIZE_PATTERNS:
        if pattern.search(market_text):
            return label
    return "Mid-market"


def detect_geo(market_text: str) -> str:
    for pattern, label in GEO_PATTERNS:
        if pattern.search(market_text):
            return label
    return "Primary geography (TBD)"


def channel_hypothesis_for(role: str) -> str:
    role_l = role.lower()
    if "finance" in role_l or "cfo" in role_l or "controller" in role_l:
        return "ERP / accounting marketplace listings, CFO peer communities, finance-leader podcasts, partner referrals from Big-4 advisors"
    if "people" in role_l or "hr" in role_l:
        return "HR community Slack groups, People Ops conferences (HR Transform, Transform), People Geeks newsletter"
    if "engineering" in role_l or "cto" in role_l:
        return "DevTools podcasts, GitHub awareness, Hacker News, technical conferences (re:Invent, KubeCon)"
    if "marketing" in role_l or "cmo" in role_l:
        return "Pavilion / Demandbase community, MarTech conferences, marketing-leader newsletters (Lenny, Demand Curve)"
    if "revenue" in role_l or "sales" in role_l or "cro" in role_l:
        return "Pavilion, RevOps Co-op, Sales Hacker, sales-leader podcasts"
    if "cs" in role_l or "customer success" in role_l:
        return "Gain Grow Retain community, ChurnZero / Gainsight events, CS leader newsletters"
    if "product" in role_l or "cpo" in role_l:
        return "Lenny's Newsletter, Mind the Product, ProductCon, product-leader Slack groups"
    if "data" in role_l:
        return "Locally Optimistic Slack, MDS Fest, dbt community, data-leader newsletters"
    return "Identified peer community + 1-2 named conferences (CONFIRM in research)"


def sizing_hypothesis(size_band: str) -> str:
    rough = {
        "SMB (under $10M)": "approx 200K addressable companies in NA; ARPC $2K-$8K",
        "Mid-market ($10M-$500M)": "approx 30K-50K addressable companies in NA; ARPC $15K-$60K",
        "Enterprise ($500M+)": "approx 5K addressable companies globally; ARPC $80K-$500K+",
    }
    base = rough.get(size_band, "Sizing TBD via primary research")
    return f"{size_band}: {base} (placeholder — confirm with company-data source)"


def build_candidates(market_text: str) -> List[CandidateSegment]:
    roles = detect_role_archetypes(market_text)
    size_band = detect_size_band(market_text)
    geo = detect_geo(market_text)
    candidates: List[CandidateSegment] = []
    for role, jtbd in roles:
        candidates.append(
            CandidateSegment(
                name=f"{role} at {size_band} companies in {geo}",
                who=f"{role} responsible for the relevant function in {size_band} companies, {geo}",
                jtbd=jtbd,
                channel_hypothesis=channel_hypothesis_for(role),
                sizing_hypothesis=sizing_hypothesis(size_band),
            )
        )
    return candidates


# ---------- Strategy recommendation ----------

def recommend_strategy(stage_bucket: str, candidates: List[CandidateSegment]) -> StrategyRecommendation:
    if stage_bucket == "early":
        return StrategyRecommendation(
            name="Single-segment concentration",
            rationale=(
                "At Seed / Series A, focus is the cardinal virtue. Pick the ONE candidate "
                "with the strongest pull, build deep know-how, and earn category leadership "
                "in that cluster before expanding. Examples: early Red Bull (extreme-sports "
                "drinkers), early Tesla (luxury early-adopters)."
            ),
            risk="Severe exposure to demand shifts in the chosen segment. Mitigate with adjacency-mapping every 6 months.",
        )
    if stage_bucket == "mid":
        if len(candidates) >= 2:
            return StrategyRecommendation(
                name="Selective specialization",
                rationale=(
                    "At Series B with proven beachhead, expand into 1-2 adjacent segments "
                    "where existing product covers the core JTBD. Each segment must be "
                    "profitable on its own (no cross-subsidy). Example: Mercedes A/C/E classes."
                ),
                risk="Channel and message complexity rises; risk of diluting brand if segments diverge sharply. Keep ICP scorecards per segment.",
            )
        return StrategyRecommendation(
            name="Single-segment concentration with adjacency probing",
            rationale=(
                "Continue concentration on the proven segment; run small probes on 1-2 "
                "adjacent segments before committing budget."
            ),
            risk="Slower top-of-funnel growth; mitigate with deeper account expansion.",
        )
    # late
    return StrategyRecommendation(
        name="Market specialization or selective specialization",
        rationale=(
            "Late-stage B2B companies typically run market specialization (one customer "
            "type, multiple products) or selective specialization (multiple unrelated "
            "segments, each profitable on its own). Full coverage is justified only when "
            "scale economics dominate (rare in B2B SaaS, common in CPG)."
        ),
        risk="Operational complexity, brand-portfolio governance, ICP drift across segments. Re-segment every 4-5 years per J&J expert practice.",
    )


# ---------- Markdown rendering ----------

def render_markdown(out: CanvasOutput) -> str:
    lines: List[str] = []
    lines.append("# Customer Segmentation Canvas")
    lines.append("")
    lines.append("## 1. Inputs")
    lines.append(f"- Market description: {out.market}")
    lines.append(f"- Company stage (input): {out.stage_input}  -> bucket: **{out.stage_bucket}**")
    if out.objectives:
        lines.append(f"- Business objectives: {', '.join(out.objectives)}")
    lines.append("")

    lines.append("## 2. Recommended segmentation level")
    lines.append(f"**Level: {out.level.level.upper()}**")
    lines.append("")
    lines.append(out.level.rationale)
    lines.append("")

    lines.append("## 3. Recommended criteria types")
    lines.append(f"- **Primary**: {out.criteria.primary}")
    lines.append(f"- **Secondary**: {out.criteria.secondary}")
    overlays = ", ".join(out.criteria.overlays) if out.criteria.overlays else "(none detected — use only as needed)"
    lines.append(f"- **Overlays for sizing / access only**: {overlays}")
    lines.append("")
    lines.append(out.criteria.reasoning)
    lines.append("")

    lines.append("## 4. Candidate segment archetypes")
    lines.append("")
    lines.append("These are working hypotheses generated from the market description. Each must be sharpened with primary research and then validated via MAPDA before any GTM commitment.")
    lines.append("")
    for idx, cand in enumerate(out.candidates):
        letter = chr(ord("A") + idx)
        lines.append(f"### Segment {letter}: {cand.name}")
        lines.append(f"- **Who**: {cand.who}")
        lines.append(f"- **Key need (JTBD)**: {cand.jtbd}")
        lines.append(f"- **Channel hypothesis**: {cand.channel_hypothesis}")
        lines.append(f"- **Sizing hypothesis**: {cand.sizing_hypothesis}")
        lines.append("")

    lines.append("## 5. Recommended Kotler segmentation strategy")
    lines.append(f"**Strategy: {out.strategy.name}**")
    lines.append("")
    lines.append(out.strategy.rationale)
    lines.append("")
    lines.append(f"**Key risk**: {out.strategy.risk}")
    lines.append("")

    lines.append("## 6. Next-step prompt for the LLM")
    lines.append("")
    lines.append("> The candidate segments above are HYPOTHESES, not validated segments. As the LLM running this skill, your next moves are:")
    lines.append(">")
    lines.append("> 1. **Validate each candidate against MAPDA** by running scripts/validate_segment.py with concrete evidence per segment (size estimate, named channel, ARPC range, needs_diff, capability_fit). Do not skip filters; do not accept vague evidence.")
    lines.append("> 2. **Sharpen each segment definition** with primary research evidence — Jaime Veiga (J&J) recommends 5-7 customer interviews per candidate minimum. Replace placeholders with named companies, named channels, named buying committees.")
    lines.append("> 3. **Drop any segment that fails MAPDA** — do not promote a vanity, aspirational, or demographic-only segment to the canvas.")
    lines.append("> 4. **Map each surviving segment to a positioning approach** by handing off to the positioning-statement-builder skill. Each segment gets its own frame of reference, point of difference, and reason to believe.")
    lines.append("> 5. **Define explicit ANTI-segments** — who you are NOT for. This is as load-bearing as who you are for.")
    lines.append("")

    if out.notes:
        lines.append("## 7. Notes / caveats")
        for n in out.notes:
            lines.append(f"- {n}")
        lines.append("")

    return "\n".join(lines)


# ---------- CLI entry ----------

def parse_objectives(s: Optional[str]) -> List[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="DESIGN a segmentation canvas from a market description.",
    )
    parser.add_argument(
        "--market",
        required=True,
        help="Market or customer-base description (free text).",
    )
    parser.add_argument(
        "--stage",
        default="growth",
        help="Company stage: Seed / Series A / Series B / Series C+ / Late stage. Default growth.",
    )
    parser.add_argument(
        "--objectives",
        default="",
        help="Comma-separated business objectives (e.g. grow ARR, reduce CAC payback).",
    )
    args = parser.parse_args(argv)

    stage_bucket = normalize_stage(args.stage)
    objectives = parse_objectives(args.objectives)

    level = recommend_level(stage_bucket, args.market)
    criteria = recommend_criteria(args.market)
    candidates = build_candidates(args.market)
    strategy = recommend_strategy(stage_bucket, candidates)

    notes: List[str] = []
    if len(candidates) < 2:
        notes.append(
            "Fewer than 2 candidate archetypes detected from the market text. Provide a richer description or add detected role hints."
        )
    if stage_bucket == "early" and len(candidates) > 2:
        notes.append(
            "Early-stage companies should resist serving more than one segment. Pick ONE for concentration; treat the others as future expansion."
        )

    out = CanvasOutput(
        market=args.market,
        stage_input=args.stage,
        stage_bucket=stage_bucket,
        objectives=objectives,
        level=level,
        criteria=criteria,
        candidates=candidates,
        strategy=strategy,
        notes=notes,
    )

    sys.stdout.write(render_markdown(out))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
