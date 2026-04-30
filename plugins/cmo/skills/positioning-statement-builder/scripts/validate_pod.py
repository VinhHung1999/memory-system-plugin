#!/usr/bin/env python3
"""
validate_pod.py — Validate a Point of Difference against IE's 3 filters.

Inputs:
  --pod      The proposed Point of Difference text (required).
  --segment  Target segment description (required).
  --rtb      Optional JSON object listing reasons-to-believe.

Output: per-filter pass/fail with reasoning, revision suggestions, final verdict.
"""

import argparse
import json
import re
import sys


GENERIC_TERMS = {
    "leading", "best", "fastest", "smartest", "innovative", "cutting-edge",
    "world-class", "next-generation", "next-gen", "premier", "top", "ultimate",
    "revolutionary", "disruptive", "powerful", "robust", "seamless",
    "easy", "simple", "intuitive", "modern", "smooth", "advanced",
}

# Verbs that imply outcome change (good for relevance) vs description.
OUTCOME_VERBS = {
    "reduce", "eliminate", "cut", "save", "automate", "accelerate",
    "increase", "double", "triple", "shrink", "remove", "prevent",
    "unlock", "convert", "close", "shorten", "scale",
}

DESCRIPTION_VERBS = {
    "is", "are", "has", "have", "provide", "offer", "include", "feature",
    "support", "enable",
}

VAGUE_SEGMENT_TOKENS = {
    "modern", "innovative", "forward-thinking", "cutting-edge",
    "best-in-class", "next-gen", "smart", "savvy", "general",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "with", "to", "in", "on",
    "at", "by", "is", "are", "be", "as", "from", "that", "this", "we",
    "our", "their", "your", "you", "us", "it", "its",
}


def tokenize(text):
    if not text:
        return set()
    cleaned = re.sub(r"[^a-z0-9\s\-]", " ", text.lower())
    return {t for t in cleaned.split() if t and t not in STOPWORDS and len(t) > 1}


def filter_relevant(pod, segment):
    pod_tokens = tokenize(pod)
    seg_tokens = tokenize(segment)
    if not seg_tokens:
        return False, (
            "Segment description is empty — cannot test relevance. Provide a "
            "specific segment with named pains and context."
        ), "Add a concrete segment description with named workflows / pains."

    vague_hits = seg_tokens & VAGUE_SEGMENT_TOKENS
    if vague_hits and len(seg_tokens) <= 4:
        return False, (
            f"Segment is vague (uses {', '.join(sorted(vague_hits))} without specifics). "
            "Cannot reliably test relevance against it."
        ), "Sharpen segment: add company size, role, workflow, or pain."

    overlap = pod_tokens & seg_tokens
    has_outcome_verb = any(v in pod.lower().split() for v in OUTCOME_VERBS)
    if overlap or has_outcome_verb:
        details = []
        if overlap:
            details.append(f"keyword overlap: {', '.join(sorted(overlap))}")
        if has_outcome_verb:
            details.append("uses outcome-change verb")
        return True, "Relevant — " + "; ".join(details) + ".", ""
    return False, (
        "PoD shares no vocabulary with the segment AND uses no outcome-change verb. "
        "It may not address what this segment cares about."
    ), "Anchor PoD on a named segment pain or describe a measurable outcome change."


def filter_exclusive(pod):
    pod_lower = pod.lower()
    pod_tokens = tokenize(pod)
    generic_hits = pod_tokens & GENERIC_TERMS
    has_number = bool(re.search(r"\d", pod))
    has_comparison = any(
        marker in pod_lower
        for marker in (" vs ", " versus ", "compared to", "than ", "x faster", "x more")
    )

    if generic_hits and not (has_number or has_comparison):
        return False, (
            f"Uses generic superlative(s): {', '.join(sorted(generic_hits))} "
            "with no benchmark or comparison anchor."
        ), (
            "Replace generic words with a specific number AND a comparison "
            "(e.g., '40 percent fewer steps than competitor X')."
        )
    if has_number or has_comparison:
        return True, "Specific / benchmarked language present.", ""
    if generic_hits:
        return False, (
            f"Generic word(s): {', '.join(sorted(generic_hits))}."
        ), "Sharpen with a measurable claim."
    return True, "No generic superlatives detected — distinctive enough to test.", ""


def filter_trustworthy(pod, rtb_map):
    if not rtb_map:
        return False, (
            "No RTB provided — claim is speculative."
        ), "Add at least 1 RTB: benchmark, methodology, or third-party validation."

    # Reward concrete RTBs (numbers, third-party language).
    concrete_signals = ("benchmark", "study", "audit", "iso", "certif", "report",
                        "third-party", "third party", "data", "result")
    has_concrete = False
    has_number = False
    rtb_descriptions = []
    for k, v in rtb_map.items():
        v_str = str(v).lower()
        rtb_descriptions.append(f"{k}: {v}")
        if any(sig in v_str for sig in concrete_signals):
            has_concrete = True
        if re.search(r"\d", v_str):
            has_number = True

    if has_number or has_concrete:
        return True, (
            "RTB(s) provided with concrete signals (numbers / third-party / benchmark). "
            f"Entries: {len(rtb_map)}."
        ), ""
    return False, (
        "RTB(s) provided but appear speculative (no numbers, no third-party language)."
    ), "Strengthen RTB with a specific number, study, or external certification."


def verdict(rel_pass, exc_pass, tru_pass):
    if rel_pass and exc_pass and tru_pass:
        return "KEEP"
    if not rel_pass and not exc_pass and not tru_pass:
        return "REPLACE"
    if not rel_pass:
        return "REPLACE"  # Irrelevance is fatal; rebuild from segment up.
    return "REVISE"


def render(args, rel, exc, tru):
    rel_pass, rel_msg, rel_fix = rel
    exc_pass, exc_msg, exc_fix = exc
    tru_pass, tru_msg, tru_fix = tru
    final = verdict(rel_pass, exc_pass, tru_pass)

    out = []
    out.append("# PoD Validation Report")
    out.append("")
    out.append(f"**PoD:** {args.pod}")
    out.append(f"**Segment:** {args.segment}")
    out.append("")
    out.append("## 3-Filter Results")
    out.append("")
    out.append("| Filter | Result | Reasoning |")
    out.append("|---|---|---|")
    out.append(f"| Relevant | {'PASS' if rel_pass else 'FAIL'} | {rel_msg} |")
    out.append(f"| Exclusive | {'PASS' if exc_pass else 'FAIL'} | {exc_msg} |")
    out.append(f"| Trustworthy | {'PASS' if tru_pass else 'FAIL'} | {tru_msg} |")
    out.append("")
    out.append("## Revision Suggestions")
    if rel_fix:
        out.append(f"- **Relevance:** {rel_fix}")
    if exc_fix:
        out.append(f"- **Exclusivity:** {exc_fix}")
    if tru_fix:
        out.append(f"- **Trust:** {tru_fix}")
    if not (rel_fix or exc_fix or tru_fix):
        out.append("- None — PoD passes all filters as written.")
    out.append("")
    out.append(f"## Final Verdict: **{final}**")
    if final == "KEEP":
        out.append("PoD is strong. Lock it into the positioning statement.")
    elif final == "REVISE":
        out.append("PoD has core merit but needs sharpening. Apply revisions above.")
    else:
        out.append("PoD is too weak to revise. Rebuild from a real segment pain or replace it.")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Point of Difference against IE's 3 filters."
    )
    parser.add_argument("--pod", required=True, help="Proposed Point of Difference.")
    parser.add_argument("--segment", required=True, help="Target segment description.")
    parser.add_argument("--rtb", default=None, help="Optional JSON object of RTBs.")
    args = parser.parse_args()

    rtb_map = {}
    if args.rtb:
        try:
            parsed = json.loads(args.rtb)
            if isinstance(parsed, dict):
                rtb_map = {str(k): v for k, v in parsed.items()}
            elif isinstance(parsed, list):
                rtb_map = {f"rtb_{i}": v for i, v in enumerate(parsed)}
        except json.JSONDecodeError as exc:
            print(f"Warning: --rtb is not valid JSON ({exc}); ignoring.", file=sys.stderr)

    rel = filter_relevant(args.pod, args.segment)
    exc = filter_exclusive(args.pod)
    tru = filter_trustworthy(args.pod, rtb_map)
    print(render(args, rel, exc, tru))


if __name__ == "__main__":
    main()
