#!/usr/bin/env python3
"""
score_vision.py — Heuristic scorer for marketing vision statements.

Scores a vision on three axes (Clarity, Alignment, Actionability),
0-3 each (max 9). Produces a verdict band, runs two stress-tests
(managers-in-the-room proxy + compass-vs-poster), flags missing
canvas elements, and prints a structured "next-step prompt" the
calling LLM can use to draft a revision.

Standard library only. No external dependencies. No LLM calls.
The scoring is deliberately transparent: every deduction is
attributed to a specific trigger word so the LLM (and a human
reviewer) can audit it.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from typing import List, Tuple


# -- Lexicons ---------------------------------------------------------------

# Vague "poster" words that don't survive the managers-in-the-room test.
VAGUE_WORDS = [
    "loved", "most loved", "best", "best-in-class", "most",
    "world-class", "world class", "delight", "delightful",
    "excellence", "excellent", "amazing", "awesome", "incredible",
    "unparalleled", "unmatched", "leading", "leader", "premier",
    "innovative", "innovation", "cutting-edge", "cutting edge",
    "next-generation", "next generation", "transformative",
    "synergy", "empower", "unlock", "unleash",
]

# Generic ranking-aspirations that are slogans, not visions.
RANK_WORDS = [
    "#1", "number one", "number 1", "no. 1", "top brand",
    "category leader", "market leader",
]

# Action-implying verbs that imply prioritisation, capability-build,
# kill/scale decisions, or a clear future-state shift.
ACTION_VERBS = [
    "reinvent", "rebuild", "redesign", "redefine", "rewrite",
    "accelerate", "transition", "shift", "transform",
    "build", "create", "design", "make",
    "save", "protect", "restore",
    "eliminate", "remove", "reduce", "kill",
    "scale", "double", "triple",
    "enable", "equip", "arm", "ship",
    "help", "serve",
]

# Customer-truth signals — words that tie the vision to a specific
# segment, JTBD, friction or alternative.
CUSTOMER_TRUTH_SIGNALS = [
    "customer", "customers", "buyer", "buyers", "user", "users",
    "people", "person", "shopper", "shoppers",
    "patient", "patients", "student", "students",
    "developer", "developers", "engineer", "engineers",
    "marketer", "marketers", "founder", "founders",
    "team", "teams", "company", "companies", "business", "businesses",
    "small business", "smb", "smbs", "enterprise", "mid-market",
    "host", "hosts", "guest", "guests", "traveler", "travelers",
    "family", "families", "household", "households",
    "remote", "hybrid", "onboarding",
    "experience", "experiences", "job", "jobs",
    "local", "authentic", "everyday",
]

# Mission-anchor signals — words that link to a broader company purpose,
# a cause, a sustained capability, or a long-horizon transition.
MISSION_ANCHOR_SIGNALS = [
    "world", "planet", "society", "energy", "sustainable", "sustainability",
    "transition", "future", "generation", "generations",
    "home", "humanity", "human", "human-centered",
    "mission", "purpose", "live", "living", "lives",
    "decade", "century", "north star",
]

# Strategic-capability signals — words that hint at a unique marketing
# capability the org will build (data, content, community, partnerships,
# product-led growth, etc).
CAPABILITY_SIGNALS = [
    "platform", "engine", "system", "network", "marketplace",
    "community", "ecosystem", "data", "ai", "model",
    "content", "story", "stories", "narrative",
    "partner", "partners", "partnership", "partnerships",
    "channel", "channels", "experience layer",
    "capability", "capabilities", "operating model",
    "go-to-market", "gtm", "growth loop", "flywheel",
]


# -- Data containers --------------------------------------------------------

@dataclass
class AxisScore:
    name: str
    score: int
    max_score: int = 3
    reasons: List[str] = field(default_factory=list)
    triggers_neg: List[str] = field(default_factory=list)
    triggers_pos: List[str] = field(default_factory=list)


@dataclass
class StressResult:
    name: str
    passed: bool
    detail: str
    sub_score: float = 0.0  # for the 1-5 managers proxy


# -- Helpers ----------------------------------------------------------------

def _find_hits(text_lower: str, lexicon: List[str]) -> List[str]:
    """Return lexicon items that appear as whole words/phrases in text."""
    hits = []
    for term in lexicon:
        # Use word-boundary regex; for multi-word terms, escape and
        # rely on substring with surrounding non-word constraint.
        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
        if re.search(pattern, text_lower):
            hits.append(term)
    return hits


def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


# -- Axis scorers -----------------------------------------------------------

def score_clarity(vision: str) -> AxisScore:
    axis = AxisScore(name="Clarity", score=0)
    text = vision.lower().strip()
    if not text:
        axis.reasons.append("Empty vision string.")
        return axis

    vague_hits = _find_hits(text, VAGUE_WORDS)
    rank_hits = _find_hits(text, RANK_WORDS)
    customer_hits = _find_hits(text, CUSTOMER_TRUTH_SIGNALS)
    capability_hits = _find_hits(text, CAPABILITY_SIGNALS)
    mission_hits = _find_hits(text, MISSION_ANCHOR_SIGNALS)
    word_count = _word_count(vision)

    score = 1  # neutral baseline

    if vague_hits:
        score -= 1
        axis.triggers_neg.extend(vague_hits)
        axis.reasons.append(
            f"Vague poster words ({', '.join(vague_hits)}) — line marketers "
            "will interpret these differently."
        )
    if rank_hits:
        score -= 1
        axis.triggers_neg.extend(rank_hits)
        axis.reasons.append(
            f"Ranking-aspiration phrasing ({', '.join(rank_hits)}) — describes "
            "a rank, not a future state."
        )

    # Reward concrete signals. Stacking multiple specific tokens earns
    # an extra bonus — the difference between a vague "businesses" and
    # a richly-painted "authentic local experiences".
    if customer_hits:
        score += 1
        axis.triggers_pos.extend(customer_hits)
        axis.reasons.append(
            f"Names a customer/segment signal ({', '.join(customer_hits[:3])})."
        )
        if len(customer_hits) >= 3:
            score += 1
            axis.reasons.append(
                "Stacks multiple specificity tokens — paints a vivid future state."
            )
    if capability_hits:
        score += 1
        axis.triggers_pos.extend(capability_hits)
        axis.reasons.append(
            f"Names a capability signal ({', '.join(capability_hits[:3])})."
        )
    if mission_hits and not customer_hits and not capability_hits:
        # A mission-only vision (Tesla, Patagonia) earns clarity for the
        # concrete future-state it implies.
        score += 1
        axis.triggers_pos.extend(mission_hits)
        axis.reasons.append(
            f"Names a concrete mission target ({', '.join(mission_hits[:3])})."
        )

    # Length sanity — over-long visions tend to be unclear.
    if word_count > 30:
        score -= 1
        axis.reasons.append(
            f"Vision is {word_count} words — too long to be a north star."
        )
    elif 4 <= word_count <= 20:
        score += 0  # neutral; short is fine if specific
    elif word_count < 4:
        score -= 1
        axis.reasons.append("Too short to articulate a future state.")

    axis.score = max(0, min(3, score))
    return axis


def score_alignment(vision: str, context: str = "") -> AxisScore:
    axis = AxisScore(name="Alignment", score=0)
    text = vision.lower().strip()
    if not text:
        axis.reasons.append("Empty vision string.")
        return axis

    customer_hits = _find_hits(text, CUSTOMER_TRUTH_SIGNALS)
    mission_hits = _find_hits(text, MISSION_ANCHOR_SIGNALS)
    capability_hits = _find_hits(text, CAPABILITY_SIGNALS)
    rank_hits = _find_hits(text, RANK_WORDS)
    vague_hits = _find_hits(text, VAGUE_WORDS)

    score = 1

    if customer_hits:
        score += 1
        axis.triggers_pos.extend(customer_hits)
        axis.reasons.append(
            f"Anchored to a customer truth signal ({', '.join(customer_hits[:3])})."
        )
        if len(customer_hits) >= 3:
            score += 1
            axis.reasons.append(
                "Multiple customer-truth tokens — alignment is rich, not generic."
            )
    if mission_hits:
        score += 1
        axis.triggers_pos.extend(mission_hits)
        axis.reasons.append(
            f"Carries a mission anchor ({', '.join(mission_hits[:3])}) linking "
            "to a broader purpose."
        )
        if len(mission_hits) >= 3:
            score += 1
            axis.reasons.append(
                "Multiple mission-anchor tokens — purpose is concrete, "
                "not just inspirational."
            )
    if capability_hits and (customer_hits or mission_hits):
        score += 1
        axis.triggers_pos.extend(capability_hits)
        axis.reasons.append(
            "Bridges customer/mission with a strategic capability — alignment "
            "between what we serve and how we serve it."
        )

    if rank_hits:
        score -= 2
        axis.triggers_neg.extend(rank_hits)
        axis.reasons.append(
            "Standalone rank-aspiration disconnects from customer reality."
        )
    if vague_hits and not customer_hits and not mission_hits:
        score -= 1
        axis.triggers_neg.extend(vague_hits)
        axis.reasons.append(
            "Aspirational language with no customer or mission anchor."
        )

    if context.strip():
        ctx_lower = context.lower()
        # If the vision actually echoes any context tokens, small bonus.
        ctx_tokens = set(re.findall(r"[a-z][a-z\-]{3,}", ctx_lower))
        vision_tokens = set(re.findall(r"[a-z][a-z\-]{3,}", text))
        overlap = ctx_tokens & vision_tokens
        # Strip generic stop-ish words.
        overlap -= {"with", "from", "that", "this", "have", "been",
                    "more", "than", "they", "their", "them", "into",
                    "company", "companies"}
        if overlap:
            score += 0  # informational, not bonus by default
            axis.reasons.append(
                f"Vision echoes context tokens: {', '.join(sorted(overlap))}."
            )

    axis.score = max(0, min(3, score))
    return axis


def score_actionability(vision: str) -> AxisScore:
    axis = AxisScore(name="Actionability", score=0)
    text = vision.lower().strip()
    if not text:
        axis.reasons.append("Empty vision string.")
        return axis

    action_hits = _find_hits(text, ACTION_VERBS)
    capability_hits = _find_hits(text, CAPABILITY_SIGNALS)
    customer_hits = _find_hits(text, CUSTOMER_TRUTH_SIGNALS)
    vague_hits = _find_hits(text, VAGUE_WORDS)
    rank_hits = _find_hits(text, RANK_WORDS)

    score = 1

    if action_hits:
        score += 1
        axis.triggers_pos.extend(action_hits)
        axis.reasons.append(
            f"Action-implying verbs ({', '.join(action_hits[:3])}) — supports "
            "kill/scale and prioritisation decisions."
        )
    if capability_hits:
        score += 1
        axis.triggers_pos.extend(capability_hits)
        axis.reasons.append(
            "Names a capability worth investing in — defensible budget line."
        )
    if action_hits and customer_hits:
        score += 0  # already rewarded; no double-count

    if not action_hits and (vague_hits or rank_hits):
        score -= 1
        axis.reasons.append(
            "Pure poster language — gives no clue what to do Monday morning."
        )
    if rank_hits and not action_hits:
        score -= 1
        axis.triggers_neg.extend(rank_hits)
        axis.reasons.append(
            "Rank claim without action verb — cannot drive a roadmap decision."
        )

    axis.score = max(0, min(3, score))
    return axis


# -- Stress tests -----------------------------------------------------------

def stress_managers(vision: str) -> StressResult:
    """
    Proxy for "would 5 marketing managers describe this the same way?"
    Higher specificity (named segment + named capability + action verb)
    → higher score on the 1-5 band.
    """
    text = vision.lower()
    customer_hits = _find_hits(text, CUSTOMER_TRUTH_SIGNALS)
    capability_hits = _find_hits(text, CAPABILITY_SIGNALS)
    action_hits = _find_hits(text, ACTION_VERBS)
    vague_hits = _find_hits(text, VAGUE_WORDS)
    rank_hits = _find_hits(text, RANK_WORDS)

    score = 1.0
    if customer_hits:
        score += 1.5
    if capability_hits:
        score += 1.0
    if action_hits:
        score += 1.0
    if vague_hits:
        score -= 0.75 * min(len(vague_hits), 2)
    if rank_hits:
        score -= 1.0
    score = max(1.0, min(5.0, score))

    passed = score >= 3.5
    detail = (
        f"Specificity proxy = {score:.1f}/5. "
        + ("Managers will likely converge on meaning."
           if passed else
           "Managers will likely interpret this differently — slogan risk.")
    )
    return StressResult(
        name="Managers in the room",
        passed=passed,
        detail=detail,
        sub_score=score,
    )


def stress_compass(vision: str) -> StressResult:
    """
    Compass-vs-poster: does it tell teams WHERE to go AND WHY?
    Heuristic: needs (action_verb OR mission_anchor) AND
    (customer_truth OR capability) to count as a compass.
    """
    text = vision.lower()
    action_hits = _find_hits(text, ACTION_VERBS)
    mission_hits = _find_hits(text, MISSION_ANCHOR_SIGNALS)
    customer_hits = _find_hits(text, CUSTOMER_TRUTH_SIGNALS)
    capability_hits = _find_hits(text, CAPABILITY_SIGNALS)

    has_direction = bool(action_hits or mission_hits)
    has_meaning = bool(customer_hits or capability_hits)
    passed = has_direction and has_meaning

    if passed:
        detail = (
            "Has both a direction signal and a why signal — passes the "
            "compass test."
        )
    elif has_direction and not has_meaning:
        detail = (
            "Tells teams to move but not why their work matters — "
            "half-compass, half-poster."
        )
    elif has_meaning and not has_direction:
        detail = (
            "Has meaning but no direction verb — describes a state of "
            "being, not a journey."
        )
    else:
        detail = "No direction and no meaning — pure poster."

    return StressResult(
        name="Compass-vs-poster",
        passed=passed,
        detail=detail,
    )


# -- Verdict and missing-elements ------------------------------------------

def verdict_band(total: int, strict: bool) -> str:
    if strict:
        if total >= 9:
            return "Strategic vision"
        if total >= 7:
            return "Worth revising"
        if total >= 4:
            return "Slogan"
        return "Empty aspiration"
    if total >= 8:
        return "Strategic vision"
    if total >= 5:
        return "Worth revising"
    if total >= 2:
        return "Slogan"
    return "Empty aspiration"


def missing_elements(vision: str) -> List[Tuple[str, bool, str]]:
    text = vision.lower()
    customer_hits = _find_hits(text, CUSTOMER_TRUTH_SIGNALS)
    mission_hits = _find_hits(text, MISSION_ANCHOR_SIGNALS)
    capability_hits = _find_hits(text, CAPABILITY_SIGNALS)
    return [
        (
            "Mission anchor",
            bool(mission_hits),
            "Link to the company's broader purpose (Tesla=clean energy, "
            "Unilever=sustainable living).",
        ),
        (
            "Customer truth",
            bool(customer_hits),
            "Named segment, JTBD, or buyer reality the vision serves.",
        ),
        (
            "Strategic capability",
            bool(capability_hits),
            "The unique marketing capability built over the next 3-5 years.",
        ),
    ]


# -- Output rendering -------------------------------------------------------

def render_markdown(
    vision: str,
    context: str,
    strict: bool,
    axes: List[AxisScore],
    stresses: List[StressResult],
) -> str:
    total = sum(a.score for a in axes)
    verdict = verdict_band(total, strict)
    missing = missing_elements(vision)

    lines: List[str] = []
    lines.append("# Marketing Vision Score")
    lines.append("")
    lines.append(f"**Vision:** {vision.strip()}")
    if context.strip():
        lines.append(f"**Context:** {context.strip()}")
    lines.append(f"**Strict mode:** {'on' if strict else 'off'}")
    lines.append("")

    lines.append("## Score Table")
    lines.append("")
    lines.append("| Axis | Score | Reason |")
    lines.append("|---|---|---|")
    for a in axes:
        reason = " ".join(a.reasons) if a.reasons else "No notable signal."
        # Escape pipe chars to keep table valid.
        reason = reason.replace("|", "/")
        lines.append(f"| {a.name} | {a.score}/{a.max_score} | {reason} |")
    lines.append(f"| **Total** | **{total}/9** | Verdict band: **{verdict}** |")
    lines.append("")

    lines.append(f"## Verdict — {verdict}")
    lines.append("")
    if verdict == "Strategic vision":
        lines.append(
            "This vision passes the rubric. Use it as the test for budget "
            "and roadmap decisions; revisit annually."
        )
    elif verdict == "Worth revising":
        lines.append(
            "This vision has the right shape but is missing one or two "
            "anchor elements. Rewrite using the canvas template."
        )
    elif verdict == "Slogan":
        lines.append(
            "This is motivational but not decision-guiding. Line marketers "
            "will interpret it differently. Rewrite from scratch using "
            "the canvas template — start with the customer truth."
        )
    else:
        lines.append(
            "This is an empty aspiration. Begin with the company mission "
            "and customer truth before drafting any vision text."
        )
    lines.append("")

    lines.append("## Stress-Test Results")
    lines.append("")
    for s in stresses:
        marker = "PASS" if s.passed else "FAIL"
        lines.append(f"- **{s.name}** — {marker}: {s.detail}")
    lines.append("")

    lines.append("## Missing Canvas Elements")
    lines.append("")
    for name, present, hint in missing:
        marker = "present" if present else "MISSING"
        lines.append(f"- **{name}** — {marker}. {hint}")
    lines.append("")

    lines.append("## Trigger Audit (transparent scoring)")
    lines.append("")
    for a in axes:
        if a.triggers_neg:
            lines.append(
                f"- {a.name} deductions triggered by: "
                + ", ".join(sorted(set(a.triggers_neg)))
            )
        if a.triggers_pos:
            lines.append(
                f"- {a.name} bonuses triggered by: "
                + ", ".join(sorted(set(a.triggers_pos)))
            )
    lines.append("")

    lines.append("## Next-Step Prompt for LLM")
    lines.append("")
    lines.append(
        "Use the structured findings above to draft a revision. Do NOT "
        "produce generic 'visions should be inspiring' advice. Instead, "
        "fill in the canvas at templates/vision-canvas.md in this order:"
    )
    lines.append("")
    lines.append("1. **Mission Anchor** — state what the company exists to do "
                 "and marketing's role in that mission.")
    lines.append("2. **Customer Truth** — name the primary segment, the JTBD, "
                 "and the friction in their current alternative.")
    lines.append("3. **Strategic Capability** — name the unique marketing "
                 "capability the org will build over 3-5 years and why it "
                 "is hard to copy.")
    lines.append("4. **Vision Statement** — 1-2 sentences that bind the three "
                 "above. Must contain at least one action verb, one customer "
                 "or mission signal, and one capability signal.")
    lines.append("5. **Stress-test answers** — write the literal answers a "
                 "line marketer would give to: what to double down on, what "
                 "to kill, who to hire.")
    lines.append("")

    missing_only = [name for name, present, _ in missing if not present]
    if missing_only:
        lines.append(
            "**Specifically address these missing elements first:** "
            + ", ".join(missing_only) + "."
        )
        lines.append("")

    lines.append(
        "After drafting the revision, re-run this script on the new "
        "vision text and confirm total >= 7 (or 8 in strict mode) "
        "before presenting it to the user."
    )
    lines.append("")
    return "\n".join(lines)


# -- CLI --------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    # NOTE: do not use the percent sign in any help string — macOS Python
    # 3.14 has a pyexpat/argparse interaction that crashes on it.
    parser = argparse.ArgumentParser(
        description=(
            "Score a marketing vision statement on Clarity, Alignment, "
            "and Actionability. Produces a verdict band, two stress-test "
            "results, missing-element flags, and a structured next-step "
            "prompt for the LLM to draft a revision."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--vision",
        required=True,
        help="The vision statement string to score.",
    )
    parser.add_argument(
        "--context",
        default="",
        help=(
            "Optional company context — industry, stage, segment. Used to "
            "check whether the vision echoes the company reality."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Strict mode raises the bar — 9/9 is required for the "
            "Strategic vision verdict, 7-8 is Worth revising."
        ),
    )
    return parser


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    axes = [
        score_clarity(args.vision),
        score_alignment(args.vision, args.context),
        score_actionability(args.vision),
    ]
    stresses = [
        stress_managers(args.vision),
        stress_compass(args.vision),
    ]
    md = render_markdown(args.vision, args.context, args.strict, axes, stresses)
    sys.stdout.write(md)
    if not md.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
