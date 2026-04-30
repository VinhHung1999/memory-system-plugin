#!/usr/bin/env python3
"""
validate_plan.py — Validate a marketing-plan markdown draft against
IE Business School 4-part methodology.

Runs 5 checks:
  1. ORDER       — 4 parts present in correct order (Analysis -> Strategy -> Mix -> Results).
  2. PART 1->2   — Strategy decisions reference Analysis findings.
  3. PART 2->3   — 4P tactics reference strategic choices.
  4. PART 2<->4  — Every Part 2 objective has a Part 4 metric.
  5. CONSTRAINT  — Sales target + budget appear at top of each section.

Stdlib only. Simple keyword + heading-pattern matching.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# ----------------------------------------------------------------------------
# Part-detection patterns
# ----------------------------------------------------------------------------

PART_PATTERNS = {
    "1": [r"part\s*1", r"analysis", r"5\s*c'?s?", r"swot", r"where\s+are\s+we"],
    "2": [r"part\s*2", r"strategy", r"objectives", r"target\s+segment",
          r"positioning", r"where\s+do\s+we\s+want"],
    "3": [r"part\s*3", r"marketing\s+mix", r"\bmix\b", r"4\s*p'?s?",
          r"product.*price.*channel", r"how\s+do\s+we\s+get"],
    "4": [r"part\s*4", r"expected\s+results", r"\bresults\b",
          r"\bmetrics?\b", r"\bbudget\b", r"how\s+do\s+we\s+measure"],
}

PART_LABELS = {
    "1": "Part 1 — ANALYSIS",
    "2": "Part 2 — STRATEGY",
    "3": "Part 3 — MIX",
    "4": "Part 4 — RESULTS",
}


def find_section_starts(text: str) -> dict[str, int]:
    """Return earliest heading-line index where each part begins."""
    starts: dict[str, int] = {}
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if not line.lstrip().startswith("#"):
            continue
        low = line.lower()
        for part, patterns in PART_PATTERNS.items():
            if part in starts:
                continue
            for pat in patterns:
                if re.search(pat, low):
                    starts[part] = idx
                    break
    return starts


def section_text(text: str, start_line: int, end_line: int) -> str:
    return "\n".join(text.splitlines()[start_line:end_line])


# ----------------------------------------------------------------------------
# Check 1 — Order
# ----------------------------------------------------------------------------

def check_order(starts: dict[str, int]) -> tuple[bool, list[str], list[str]]:
    diagnostics: list[str] = []
    fixes: list[str] = []
    missing = [p for p in ("1", "2", "3", "4") if p not in starts]
    if missing:
        for m in missing:
            diagnostics.append(f"Missing {PART_LABELS[m]} section.")
            fixes.append(f"Add a heading for {PART_LABELS[m]}. "
                         f"Run `build_plan.py --part {m}` for a scaffold.")
        return False, diagnostics, fixes

    order = sorted(starts.items(), key=lambda kv: kv[1])
    actual = [p for p, _ in order]
    expected = ["1", "2", "3", "4"]
    if actual != expected:
        diagnostics.append(
            f"Parts appear in wrong order: {actual}. Expected: {expected}."
        )
        fixes.append(
            "Reorder the document: Analysis -> Strategy -> Mix -> Results. "
            "Strategy before Analysis is the most common error."
        )
        return False, diagnostics, fixes

    return True, ["All 4 parts present in correct order."], []


# ----------------------------------------------------------------------------
# Check 2 — Part 1 -> 2 traceback
# ----------------------------------------------------------------------------

PART1_KEYWORDS = ["swot", "5cs", "5 c's", "differentiation", "lifecycle",
                  "life-cycle", "life cycle", "external", "internal",
                  "opportunit", "strength", "weakness", "threat",
                  "competitor", "customer", "context", "collaborator", "company"]


def check_part_1_to_2(p2_text: str) -> tuple[bool, list[str], list[str]]:
    if not p2_text:
        return False, ["Part 2 not found — cannot trace from Part 1."], \
               ["Generate Part 2 first: `build_plan.py --part 2`."]
    low = p2_text.lower()
    hits = [k for k in PART1_KEYWORDS if k in low]
    if len(hits) >= 2:
        return True, [f"Part 2 references Part 1 ({len(hits)} signals: {hits[:5]})."], []
    return False, [
        f"Part 2 weakly traces to Part 1 — only {len(hits)} keyword(s) found."
    ], [
        "Strategy decisions must cite Analysis findings. "
        "Add explicit phrases: 'based on SWOT', 'per our differentiation', "
        "'lifecycle stage implies', 'opportunity O2 motivates this objective'."
    ]


# ----------------------------------------------------------------------------
# Check 3 — Part 2 -> 3 traceback
# ----------------------------------------------------------------------------

PART2_KEYWORDS = ["target segment", "positioning", "objective",
                  "financial", "non-financial", "non financial",
                  "attraction", "retention", "value proposition",
                  "strategic choice", "strategy"]


def check_part_2_to_3(p3_text: str) -> tuple[bool, list[str], list[str]]:
    if not p3_text:
        return False, ["Part 3 not found — cannot trace from Part 2."], \
               ["Generate Part 3 first: `build_plan.py --part 3`."]
    low = p3_text.lower()
    hits = [k for k in PART2_KEYWORDS if k in low]
    has_traceback = "trace" in low or "trace-back" in low or "based on" in low \
                    or "supports" in low
    if len(hits) >= 2 and has_traceback:
        return True, [f"Part 3 traces to Part 2 ({len(hits)} signals + traceback phrasing)."], []
    fixes = []
    if len(hits) < 2:
        fixes.append(
            "Each P (Product/Price/Channel/Communication) must reference a Part 2 "
            "decision (target segment, positioning, financial objective, "
            "attraction-vs-retention split)."
        )
    if not has_traceback:
        fixes.append(
            "Add explicit 'Trace-back to Part 2:' line under each P. "
            "Tactics without strategic anchors are activity, not plan."
        )
    return False, [
        f"Part 3 weakly traces to Part 2 — {len(hits)} keyword(s), "
        f"traceback phrasing {'present' if has_traceback else 'missing'}."
    ], fixes


# ----------------------------------------------------------------------------
# Check 4 — Part 2 <-> 4 mirror
# ----------------------------------------------------------------------------

OBJECTIVE_HINTS = [
    ("financial", ["sales", "revenue", "arr", "profit", "market share", "margin"]),
    ("non-financial brand", ["awareness", "preference", "association",
                             "nps", "consideration", "intent"]),
    ("customer", ["attraction", "retention", "acquisition", "churn",
                  "loyalty", "expansion", "nrr"]),
    ("strategic", ["target", "positioning", "segment"]),
]


def check_part_2_to_4_mirror(p2_text: str, p4_text: str) -> tuple[bool, list[str], list[str]]:
    if not (p2_text and p4_text):
        return False, ["Part 2 or Part 4 missing — cannot run mirror check."], \
               ["Both parts must be present. Run `build_plan.py --part all`."]
    p2_low = p2_text.lower()
    p4_low = p4_text.lower()
    diagnostics = []
    fixes = []
    failures = 0
    for label, keys in OBJECTIVE_HINTS:
        in_p2 = any(k in p2_low for k in keys)
        in_p4 = any(k in p4_low for k in keys)
        if in_p2 and not in_p4:
            failures += 1
            diagnostics.append(
                f"  - {label}: present in Part 2 but NOT mirrored in Part 4."
            )
            fixes.append(
                f"Add a Part 4 metric for the {label} objective(s) "
                f"(keywords expected: {keys})."
            )
        elif in_p4 and not in_p2:
            diagnostics.append(
                f"  - {label}: in Part 4 but no matching Part 2 objective. "
                f"This metric is orphaned."
            )
            fixes.append(
                f"Either remove the orphan {label} metric or add the matching "
                f"objective in Part 2."
            )
            failures += 1
    if failures == 0:
        return True, ["Part 2 objectives are mirrored 1:1 in Part 4 metrics."], []
    return False, [f"Mirror check FAILED ({failures} mismatches):", *diagnostics], fixes


# ----------------------------------------------------------------------------
# Check 5 — Constraint header
# ----------------------------------------------------------------------------

CONSTRAINT_KEYWORDS = ["sales target", "budget", "constraint header", "guardrail"]


def check_constraint_header(text: str, starts: dict[str, int],
                            ordered_parts: list[str]) -> tuple[bool, list[str], list[str]]:
    lines = text.splitlines()
    diagnostics: list[str] = []
    fixes: list[str] = []
    failures = 0

    sorted_parts = sorted([(p, starts[p]) for p in ordered_parts if p in starts],
                          key=lambda kv: kv[1])
    for i, (part, start) in enumerate(sorted_parts):
        end = sorted_parts[i + 1][1] if i + 1 < len(sorted_parts) else len(lines)
        # Look at first ~15 lines of section.
        head = "\n".join(lines[start:min(start + 15, end)]).lower()
        has_target = ("sales target" in head or "objective" in head)
        has_budget = "budget" in head or "$" in head
        if not (has_target and has_budget):
            failures += 1
            diagnostics.append(
                f"  - {PART_LABELS[part]}: constraint header missing or incomplete "
                f"(target={'yes' if has_target else 'no'}, "
                f"budget={'yes' if has_budget else 'no'})."
            )
            fixes.append(
                f"Add at top of {PART_LABELS[part]}:\n"
                f"  > CONSTRAINT HEADER: Sales target: <X> | Budget: $<Y>\n"
                f"  This is the Nissan Leaf rule — guardrails prevent scope creep."
            )
    if failures == 0:
        return True, ["Constraint header present at top of every section."], []
    return False, [f"Constraint header check FAILED ({failures} sections):", *diagnostics], fixes


# ----------------------------------------------------------------------------
# Reporter
# ----------------------------------------------------------------------------

def report(results: list[tuple[str, bool, list[str], list[str]]]) -> str:
    lines = ["# Marketing Plan Validation Report", ""]
    pass_count = sum(1 for _, ok, _, _ in results if ok)
    total = len(results)
    lines.append(f"**Score: {pass_count}/{total} checks passed**")
    lines.append("")
    for name, ok, diag, fixes in results:
        badge = "PASS" if ok else "FAIL"
        lines.append(f"## [{badge}] {name}")
        for d in diag:
            lines.append(f"- {d}")
        if fixes:
            lines.append("")
            lines.append("**Suggested fixes:**")
            for f in fixes:
                lines.append(f"- {f}")
        lines.append("")
    if pass_count == total:
        lines.append("---")
        lines.append("All 5 IE methodology checks passed. Plan is structurally sound.")
    else:
        lines.append("---")
        lines.append(
            f"{total - pass_count} check(s) failed. Apply the fixes above and re-run."
        )
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Validate a marketing plan markdown against IE 4-part methodology."
    )
    p.add_argument("--plan", required=True, help="Path to draft plan markdown file.")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    ns = parse_args(argv)
    path = Path(ns.plan)
    if not path.exists():
        sys.stderr.write(f"Error: file not found: {path}\n")
        return 2
    text = path.read_text(encoding="utf-8")

    starts = find_section_starts(text)
    lines = text.splitlines()

    sorted_parts = sorted(starts.items(), key=lambda kv: kv[1])
    section_texts: dict[str, str] = {}
    for i, (part, start) in enumerate(sorted_parts):
        end = sorted_parts[i + 1][1] if i + 1 < len(sorted_parts) else len(lines)
        section_texts[part] = section_text(text, start, end)

    results: list[tuple[str, bool, list[str], list[str]]] = []

    ok, diag, fixes = check_order(starts)
    results.append(("Order check (4 parts in correct sequence)", ok, diag, fixes))

    ok, diag, fixes = check_part_1_to_2(section_texts.get("2", ""))
    results.append(("Part 1 -> Part 2 traceback", ok, diag, fixes))

    ok, diag, fixes = check_part_2_to_3(section_texts.get("3", ""))
    results.append(("Part 2 -> Part 3 traceback", ok, diag, fixes))

    ok, diag, fixes = check_part_2_to_4_mirror(
        section_texts.get("2", ""), section_texts.get("4", "")
    )
    results.append(("Part 2 <-> Part 4 mirror (every objective gets a metric)", ok, diag, fixes))

    ok, diag, fixes = check_constraint_header(text, starts, ["1", "2", "3", "4"])
    results.append(("Constraint header at top of each section (Nissan Leaf rule)", ok, diag, fixes))

    sys.stdout.write(report(results) + "\n")
    failed = sum(1 for _, ok, _, _ in results if not ok)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
