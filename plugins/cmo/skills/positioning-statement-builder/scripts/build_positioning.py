#!/usr/bin/env python3
"""
build_positioning.py — Build a 3-element positioning statement (IE methodology).

Inputs:
  --target       Target segment description (required).
  --value-prop   Draft value proposition text (required).
  --competitors  Comma-separated competitor list (required).
  --frame-by     The need or category being framed (required).
  --rtb          Optional JSON map of PoD-name to RTB string/list.

Output: Markdown report covering:
  - 3-element positioning statement (target / value prop / frame of reference)
  - Per-PoD 3-filter table (Relevant / Exclusive / Trustworthy)
  - Frame-of-reference quality check (need-based vs category-based)
  - Next-step prompt for the LLM
"""

import argparse
import json
import re
import sys


# Categories that, when used alone as a frame, signal category-framing not need-framing.
CATEGORY_HINTS = {
    "software", "fintech", "saas", "tools", "platforms", "platform",
    "tool", "app", "apps", "service", "services", "product", "solution",
    "system", "suite", "marketplace",
}

# Generic superlatives that fail the Exclusive filter without a benchmark.
GENERIC_TERMS = {
    "leading", "best", "fastest", "smartest", "innovative", "cutting-edge",
    "world-class", "next-generation", "next-gen", "premier", "top",
    "revolutionary", "disruptive", "powerful", "robust", "seamless",
    "easy", "simple", "intuitive",
}

# Conjunctions / separators used to split a value prop into candidate PoDs.
SPLIT_PATTERN = re.compile(r"\s*(?:,|;| and | plus |/|\|)\s*", re.IGNORECASE)

# Tokens that aren't useful for keyword overlap scoring.
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "with", "to", "in", "on",
    "at", "by", "is", "are", "be", "as", "from", "that", "this", "we",
    "our", "their", "your", "you", "us", "it", "its",
}


def tokenize(text):
    """Lowercase, strip punctuation, drop stopwords, return token set."""
    if not text:
        return set()
    cleaned = re.sub(r"[^a-z0-9\s\-]", " ", text.lower())
    return {t for t in cleaned.split() if t and t not in STOPWORDS and len(t) > 1}


def split_pods(value_prop):
    """Split the value prop into candidate PoD phrases."""
    parts = [p.strip() for p in SPLIT_PATTERN.split(value_prop) if p.strip()]
    # Drop ultra-short fragments (likely noise).
    return [p for p in parts if len(p) >= 4]


def check_frame_quality(frame_by):
    """Return (is_need_based, message)."""
    tokens = tokenize(frame_by)
    if not tokens:
        return False, "Frame is empty — cannot evaluate."
    # Single-word category match.
    if len(tokens) == 1 and next(iter(tokens)) in CATEGORY_HINTS:
        return False, (
            "Frame appears to be a CATEGORY name, not a NEED. "
            "Reframe by the customer need or job-to-be-done. "
            "Example: not 'CRM software' but 'unified customer relationship workflow'."
        )
    if any(t in CATEGORY_HINTS for t in tokens) and len(tokens) <= 2:
        return False, (
            "Frame leans on category vocabulary. Test: does this describe a "
            "customer NEED, or a product type? If product type, widen to need."
        )
    return True, "Frame appears need-based (not a bare category)."


def filter_relevant(pod, segment_tokens):
    """Heuristic: PoD should reference vocabulary that overlaps the segment."""
    pod_tokens = tokenize(pod)
    overlap = pod_tokens & segment_tokens
    if overlap:
        return True, f"PoD references segment vocabulary ({', '.join(sorted(overlap))})."
    return False, (
        "PoD does not reference any segment-named pain or context. "
        "Tie it to a specific pain or workflow named in the target description."
    )


def filter_exclusive(pod):
    """Heuristic: penalize generic superlatives without numbers/benchmarks."""
    pod_tokens = tokenize(pod)
    has_number = bool(re.search(r"\d", pod))
    generic_hits = pod_tokens & GENERIC_TERMS
    if generic_hits and not has_number:
        return False, (
            f"Uses generic superlative(s) without benchmark: {', '.join(sorted(generic_hits))}. "
            "Replace with a measurable, comparison-anchored claim."
        )
    if has_number:
        return True, "PoD contains a measurable claim (number/benchmark)."
    if not generic_hits:
        return True, "PoD avoids generic superlatives — likely distinctive enough to test."
    return False, "Generic phrasing — sharpen with specifics."


def filter_trustworthy(pod, rtb_map):
    """Pass if any RTB entry references this PoD's keywords."""
    if not rtb_map:
        return False, "No RTBs provided — claim is speculative until backed by evidence."
    pod_tokens = tokenize(pod)
    for key, value in rtb_map.items():
        key_tokens = tokenize(key)
        # Overlap between RTB key and PoD content -> credit.
        if pod_tokens & key_tokens or any(
            t in pod.lower() for t in key.lower().split()
        ):
            return True, f"RTB present for '{key}': {value}"
    return False, (
        "RTB list provided but no entry maps to this PoD. "
        "Add a benchmark, third-party validation, or methodology note."
    )


def build_statement(target, value_prop, competitors, frame_by):
    """Compose a single-sentence positioning statement (IE 3-element template)."""
    competitor_str = competitors.strip()
    return (
        f"For {target.strip()}, we are the {value_prop.strip()} "
        f"within {frame_by.strip()} — distinctive vs {competitor_str}."
    )


def render_report(args, pods, frame_check, filter_results, statement, rtb_map):
    lines = []
    lines.append("# Positioning Statement Build Report")
    lines.append("")
    lines.append("## Final Positioning Statement (3 elements)")
    lines.append(f"> {statement}")
    lines.append("")
    lines.append("**Element 1 — Target segment:** " + args.target)
    lines.append("**Element 2 — Value proposition:** " + args.value_prop)
    lines.append("**Element 3 — Frame of reference:** " + args.frame_by)
    lines.append(f"**Competitor set in this frame:** {args.competitors}")
    lines.append("")
    lines.append("## Frame-of-Reference Quality Check")
    is_need, msg = frame_check
    verdict = "NEED-BASED (good)" if is_need else "CATEGORY-BASED (revise)"
    lines.append(f"- Verdict: **{verdict}**")
    lines.append(f"- Reasoning: {msg}")
    lines.append("")
    lines.append("## Per-PoD 3-Filter Validation")
    lines.append("")
    lines.append("| PoD | Relevant | Exclusive | Trustworthy | Verdict |")
    lines.append("|---|---|---|---|---|")
    for pod, result in zip(pods, filter_results):
        rel_pass, _ = result["relevant"]
        exc_pass, _ = result["exclusive"]
        tru_pass, _ = result["trustworthy"]
        all_pass = rel_pass and exc_pass and tru_pass
        verdict = "KEEP" if all_pass else ("REVISE" if (rel_pass or exc_pass) else "REPLACE")
        lines.append(
            f"| {pod} | {'PASS' if rel_pass else 'FAIL'} | "
            f"{'PASS' if exc_pass else 'FAIL'} | "
            f"{'PASS' if tru_pass else 'FAIL'} | {verdict} |"
        )
    lines.append("")
    lines.append("### Filter Reasoning")
    for pod, result in zip(pods, filter_results):
        lines.append(f"#### PoD: {pod}")
        for fname in ("relevant", "exclusive", "trustworthy"):
            passed, reason = result[fname]
            lines.append(f"- **{fname.title()}** ({'PASS' if passed else 'FAIL'}): {reason}")
        lines.append("")
    lines.append("## Next-Step Prompt for LLM")
    lines.append("")
    lines.append("```")
    lines.append("You are a positioning strategist using IE Business School methodology.")
    lines.append("Given the report above:")
    lines.append("1. For each PoD that failed the Relevant filter, rewrite it to anchor on a")
    lines.append("   specific named pain in the target segment description.")
    lines.append("2. For each PoD that failed the Exclusive filter, replace generic superlatives")
    lines.append("   with measurable, benchmarked language (e.g., '12s avg vs 45s competitor').")
    lines.append("3. For each PoD that failed the Trustworthy filter, propose 1-2 RTB candidates")
    lines.append("   as research/data tasks (which study, which benchmark, which third party).")
    lines.append("4. Stress-test the final statement against patterns in")
    lines.append("   references/positioning-framework.md — specifically the frame-by-need rule,")
    lines.append("   the 5 differentiation levers, and the alternative positioning options")
    lines.append("   (reverse / breakaway / stealth) to check whether a sharper play exists.")
    lines.append("5. Return the revised positioning statement plus a 4Ps consistency check.")
    lines.append("```")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Build a 3-element positioning statement (IE methodology)."
    )
    parser.add_argument("--target", required=True, help="Target segment description.")
    parser.add_argument("--value-prop", required=True, help="Draft value proposition text.")
    parser.add_argument("--competitors", required=True, help="Comma-separated competitors.")
    parser.add_argument(
        "--frame-by", required=True,
        help="The customer need or category being framed (need preferred).",
    )
    parser.add_argument(
        "--rtb", default=None,
        help="Optional JSON object mapping PoD-key to reason-to-believe text.",
    )
    args = parser.parse_args()

    rtb_map = {}
    if args.rtb:
        try:
            parsed = json.loads(args.rtb)
            if isinstance(parsed, dict):
                rtb_map = {str(k): str(v) for k, v in parsed.items()}
            elif isinstance(parsed, list):
                rtb_map = {f"rtb_{i}": str(v) for i, v in enumerate(parsed)}
        except json.JSONDecodeError as exc:
            print(f"Warning: --rtb is not valid JSON ({exc}); ignoring.", file=sys.stderr)

    segment_tokens = tokenize(args.target) | tokenize(args.frame_by)
    pods = split_pods(args.value_prop)
    if not pods:
        pods = [args.value_prop.strip()]

    frame_check = check_frame_quality(args.frame_by)

    filter_results = []
    for pod in pods:
        filter_results.append(
            {
                "relevant": filter_relevant(pod, segment_tokens),
                "exclusive": filter_exclusive(pod),
                "trustworthy": filter_trustworthy(pod, rtb_map),
            }
        )

    statement = build_statement(args.target, args.value_prop, args.competitors, args.frame_by)
    report = render_report(args, pods, frame_check, filter_results, statement, rtb_map)
    print(report)


if __name__ == "__main__":
    main()
