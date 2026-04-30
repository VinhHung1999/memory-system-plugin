#!/usr/bin/env python3
"""translate_insight.py

Produce a structured cross-functional translation scaffold for a marketing
insight. The output is a markdown table (one row per target function) plus a
follow-up prompt the calling LLM can use to enrich each row.

The script is deterministic, stdlib-only, and DOES NOT call any LLM API. It
parses references/function-language-map.md when available and falls back to a
hardcoded canonical map for the eight default functions.

Avoids percent characters in argparse help strings to dodge the macOS
Python 3.14 pyexpat crash trap.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_REF_PATH = os.path.join(SKILL_DIR, "references", "function-language-map.md")


# Canonical fallback map. Used when the reference markdown is unavailable
# or a requested function is missing from it. Keys are normalized (lowercase,
# alpha-only) so user-facing aliases like "cfo" or "finance/cfo" both resolve.
FALLBACK_MAP: Dict[str, Dict[str, List[str]]] = {
    "finance": {
        "display": ["Finance / CFO"],
        "kpis": [
            "CAC payback period (months)",
            "LTV / CAC ratio",
            "Gross margin contribution",
            "Marketing efficiency ratio (new ARR per dollar)",
        ],
        "language": [
            "unit economics",
            "payback",
            "incremental contribution margin",
            "downside case",
        ],
        "evidence": [
            "cohort-level economics with statistical confidence",
            "incremental-lift attribution (not last-touch)",
            "sensitivity analysis (best/base/worst)",
            "audited finance-system data",
        ],
        "asks": [
            "incremental budget for a high-LTV segment",
            "reallocation from underperforming channel",
            "approval of a multi-year contract",
        ],
    },
    "product": {
        "display": ["Product / CPO"],
        "kpis": [
            "Activation rate",
            "Net Revenue Retention",
            "Feature adoption rate",
            "Time-to-value",
        ],
        "language": [
            "user job-to-be-done",
            "activation friction",
            "expansion lever",
            "wedge / counter-positioning",
        ],
        "evidence": [
            "behavioral cohort data from product analytics",
            "qualitative user research with JTBD framing",
            "A/B test with confidence interval",
            "funnel drop-off analysis",
        ],
        "asks": [
            "a roadmap slot for a segment-specific feature",
            "co-developed product-led-growth motion",
            "tighter activation flow for a high-CAC channel",
        ],
    },
    "operations": {
        "display": ["Operations / COO"],
        "kpis": [
            "Cost-to-serve per customer",
            "SLA attainment rate",
            "Throughput (units/day)",
            "Capacity utilization",
        ],
        "language": [
            "demand signal",
            "throughput bottleneck",
            "capacity plan",
            "unit cost impact",
        ],
        "evidence": [
            "demand forecast with confidence interval tied to campaign curve",
            "process maps showing handoff and SLA risks",
            "vendor capacity confirmations",
            "historical demand-spike fulfillment data",
        ],
        "asks": [
            "co-plan a demand surge with 60-90 day lead time",
            "adjust SLA tier for a high-LTV segment",
            "add a fulfillment node before a campaign",
        ],
    },
    "hr": {
        "display": ["HR / CHRO"],
        "kpis": [
            "Voluntary attrition rate",
            "Employee NPS",
            "Time-to-fill",
            "Quality-of-hire",
        ],
        "language": [
            "talent density",
            "employer brand",
            "capability gap",
            "org design",
        ],
        "evidence": [
            "engagement-survey verbatims and scores",
            "Glassdoor rating trends",
            "exit-interview themes",
            "external labor-market benchmarks",
        ],
        "asks": [
            "co-build employer-brand campaign tied to recruiting funnel",
            "hire net-new marketing capability",
            "DEI alignment on creator/supplier partnerships",
        ],
    },
    "sales": {
        "display": ["Sales / CRO"],
        "kpis": [
            "Pipeline coverage (3-4x quota)",
            "Win rate by stage and segment",
            "Average deal size (ACV)",
            "Sales cycle length (days)",
        ],
        "language": [
            "pipeline gen",
            "deal velocity",
            "land and expand",
            "air cover",
        ],
        "evidence": [
            "SQL-to-closed-won conversion by source",
            "win/loss interviews",
            "pipeline contribution with attribution model disclosed",
            "intent signals (6sense, Bombora)",
        ],
        "asks": [
            "co-prioritize an ABM target list",
            "adopt a new content asset in cadences",
            "provide air cover for an enterprise deal",
        ],
    },
    "legal": {
        "display": ["Legal / General Counsel"],
        "kpis": [
            "Open regulatory matters",
            "Contract cycle time",
            "Privacy DSR response time",
            "High-severity incidents per quarter",
        ],
        "language": [
            "material risk",
            "defensible position",
            "regulatory exposure",
            "reasonable basis (FTC standard)",
        ],
        "evidence": [
            "documented consent flows and audit trail",
            "claim-substantiation files",
            "data-flow maps showing PII movement",
            "regulator guidance citations (FTC, GDPR, HIPAA, CCPA)",
        ],
        "asks": [
            "pre-clear a campaign claim or testimonial format",
            "approve a vendor / DPA review",
            "define consent mechanism for a new geo",
        ],
    },
    "it": {
        "display": ["IT / CTO / Engineering"],
        "kpis": [
            "System uptime (99.9 percent)",
            "Mean time to recovery (MTTR)",
            "Security incidents per quarter",
            "API latency (p95 ms)",
        ],
        "language": [
            "single source of truth",
            "API-first",
            "identity and access management",
            "data residency",
        ],
        "evidence": [
            "architecture diagrams with integration points",
            "vendor SOC 2 Type II reports",
            "load-test results and capacity projections",
            "3-year total cost of ownership",
        ],
        "asks": [
            "integrate a new martech tool with security review",
            "stand up a customer-data warehouse view",
            "implement consent management or identity resolution",
        ],
    },
    "customersuccess": {
        "display": ["Customer Success / CCO"],
        "kpis": [
            "Net Revenue Retention",
            "Logo churn rate",
            "Expansion ARR per account",
            "Health-score distribution",
        ],
        "language": [
            "health score",
            "expansion play",
            "renewal motion",
            "voice of customer",
        ],
        "evidence": [
            "health-score breakdowns by segment",
            "verbatim VoC feedback",
            "cohort retention curves by acquisition source",
            "renewal forecast tied to account signals",
        ],
        "asks": [
            "co-build a customer-advocacy program",
            "identify expansion-ready accounts for upsell",
            "align lifecycle triggers with CS playbooks",
        ],
    },
}


# Aliases so users can pass natural names. Resolution happens after
# normalization (lowercase, strip non-alpha).
ALIASES: Dict[str, str] = {
    "cfo": "finance",
    "financecfo": "finance",
    "cpo": "product",
    "headofproduct": "product",
    "coo": "operations",
    "ops": "operations",
    "operationscoo": "operations",
    "chro": "hr",
    "people": "hr",
    "hrpeople": "hr",
    "headofpeople": "hr",
    "cro": "sales",
    "headofsales": "sales",
    "salescro": "sales",
    "generalcounsel": "legal",
    "gc": "legal",
    "legalgeneralcounsel": "legal",
    "cto": "it",
    "cio": "it",
    "engineering": "it",
    "itctoengineering": "it",
    "cs": "customersuccess",
    "cco": "customersuccess",
    "customer": "customersuccess",
}


def normalize(name: str) -> str:
    """Lowercase and strip non-alpha. 'Finance/CFO' -> 'financecfo'."""
    return re.sub(r"[^a-z]", "", name.lower())


def resolve_function(name: str) -> str:
    """Map a user-supplied function name to a canonical key."""
    key = normalize(name)
    if key in FALLBACK_MAP:
        return key
    if key in ALIASES:
        return ALIASES[key]
    return key  # may not exist; caller handles missing


def parse_reference_md(path: str) -> Dict[str, Dict[str, List[str]]]:
    """Parse the function-language-map.md file.

    Expects H2 headers per function with bullet sections labeled
    'KPIs they report on', 'Language patterns', 'Evidence types they trust',
    'Common asks marketing makes of them'. Returns dict keyed by canonical
    function name. Returns empty dict on parse failure or missing file.
    """
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
    except OSError:
        return {}

    out: Dict[str, Dict[str, List[str]]] = {}

    # Split by H2 sections.
    sections = re.split(r"^## ", content, flags=re.MULTILINE)
    for section in sections[1:]:
        lines = section.splitlines()
        if not lines:
            continue
        header = lines[0].strip()
        key = resolve_function(header)
        if not key:
            continue

        body = "\n".join(lines[1:])

        # For each labeled subsection, collect first-level bullets until next
        # bold-prefixed item.
        def grab(label_pattern: str) -> List[str]:
            pat = re.compile(
                r"\*\*" + label_pattern + r"[^*]*\*\*\s*:?\s*\n(.*?)(?=\n\s*-\s+\*\*|\Z)",
                re.DOTALL,
            )
            m = pat.search(body)
            if not m:
                return []
            block = m.group(1)
            items: List[str] = []
            for line in block.splitlines():
                stripped = line.strip()
                if stripped.startswith("- ") and not stripped.startswith("- **"):
                    items.append(stripped[2:].strip())
            return items

        kpis = grab(r"KPIs")
        language = grab(r"Language")
        evidence = grab(r"Evidence")
        asks = grab(r"Common asks")

        if any([kpis, language, evidence, asks]):
            out[key] = {
                "display": [header],
                "kpis": kpis or FALLBACK_MAP.get(key, {}).get("kpis", []),
                "language": language or FALLBACK_MAP.get(key, {}).get("language", []),
                "evidence": evidence or FALLBACK_MAP.get(key, {}).get("evidence", []),
                "asks": asks or FALLBACK_MAP.get(key, {}).get("asks", []),
            }

    return out


def get_function_data(
    key: str, parsed: Dict[str, Dict[str, List[str]]]
) -> Optional[Dict[str, List[str]]]:
    """Prefer parsed reference, fall back to hardcoded map."""
    if key in parsed:
        return parsed[key]
    if key in FALLBACK_MAP:
        return FALLBACK_MAP[key]
    return None


def md_escape(text: str) -> str:
    """Escape pipe characters so table rows render correctly."""
    return text.replace("|", "\\|").replace("\n", " ")


def build_row(
    function_key: str,
    data: Dict[str, List[str]],
    insight: str,
    user_evidence: Dict[str, str],
) -> str:
    display = data["display"][0] if data.get("display") else function_key.title()
    kpi_hook = data["kpis"][0] if data.get("kpis") else "their primary KPI"
    second_kpi = data["kpis"][1] if len(data.get("kpis", [])) > 1 else kpi_hook
    language_term = data["language"][0] if data.get("language") else "their core lever"
    evidence_pref = data["evidence"][:2] if data.get("evidence") else []
    ask = data["asks"][0] if data.get("asks") else "a specific decision"

    reframed = (
        f"{insight} -> moves {kpi_hook}; "
        f"specifically frames the result as a {language_term} "
        f"with implications for {second_kpi}."
    )

    evidence_parts: List[str] = []
    evidence_parts.extend(evidence_pref)
    for label, value in user_evidence.items():
        evidence_parts.append(f"user-supplied: {label} = {value}")
    evidence_str = "; ".join(evidence_parts) if evidence_parts else "TBD"

    ask_str = f"Ask: {ask} (time-bound, tied to next quarter goal)"

    return (
        f"| {md_escape(display)} "
        f"| {md_escape(reframed)} "
        f"| {md_escape(evidence_str)} "
        f"| {md_escape(ask_str)} |"
    )


def build_next_step_prompt(
    insight: str, function_keys: List[str], displays: List[str]
) -> str:
    bullets = "\n".join(f"  - {d}" for d in displays)
    return (
        "## Next-step prompt for LLM\n\n"
        "You have a structured scaffold above. Now expand each row by:\n\n"
        f"1. Rewriting the 'Reframed message' column in the actual voice of each function (use the language patterns from `references/function-language-map.md`). The base insight is: \"{insight}\".\n"
        "2. Replacing the generic evidence list with the SPECIFIC numbers, cohort cuts, or attribution outputs available in this engagement. If a number is unavailable, mark it as \"NEED: <data request>\" instead of inventing one.\n"
        "3. Sharpening the 'Specific ask' to a single sentence with: (a) the decision requested, (b) the dollar amount or roadmap quarter, (c) the deadline, (d) the link to that function's current pressure (e.g., the CFO's burn-multiple target this quarter).\n"
        "4. Adding a 'Why now' one-liner per function tying the ask to a current internal pressure or external trigger.\n"
        "5. Flagging any function-specific risk (e.g., for Legal: regulatory exposure; for IT: integration cost).\n\n"
        "Functions to expand:\n"
        f"{bullets}\n\n"
        "Do NOT use generic platitudes. Do NOT invent numbers. If a section needs data the user has not provided, surface it as a 'NEED' line."
    )


def parse_evidence(raw: Optional[str]) -> Dict[str, str]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            return {}
        return {str(k): str(v) for k, v in parsed.items()}
    except json.JSONDecodeError:
        return {}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Translate a marketing insight into a per-function reframing "
            "scaffold (one row per target function)."
        )
    )
    parser.add_argument(
        "--insight",
        required=True,
        help="The marketing insight string to translate (1-3 sentences).",
    )
    parser.add_argument(
        "--functions",
        default="finance,product,operations,hr",
        help=(
            "Comma-separated target functions. Default is the canonical four. "
            "Accepted aliases include cfo, cpo, coo, chro, cro, gc, cto, cs."
        ),
    )
    parser.add_argument(
        "--evidence",
        default=None,
        help=(
            "Optional JSON dict of available evidence, e.g. "
            "'{\"cohort_data\": \"18pt NPS uplift\", \"retention\": \"2x at 90d\"}'."
        ),
    )
    parser.add_argument(
        "--reference",
        default=DEFAULT_REF_PATH,
        help="Path to function-language-map.md. Default is the bundled reference.",
    )

    args = parser.parse_args(argv)

    insight = args.insight.strip()
    user_evidence = parse_evidence(args.evidence)
    parsed_ref = parse_reference_md(args.reference)

    requested = [f.strip() for f in args.functions.split(",") if f.strip()]
    if not requested:
        print("error: no functions provided", file=sys.stderr)
        return 2

    rows: List[str] = []
    displays: List[str] = []
    missing: List[str] = []
    for raw_name in requested:
        key = resolve_function(raw_name)
        data = get_function_data(key, parsed_ref)
        if data is None:
            missing.append(raw_name)
            continue
        rows.append(build_row(key, data, insight, user_evidence))
        displays.append(data["display"][0])

    print("# Cross-Functional Translation Matrix\n")
    print(f"**Insight:** {insight}\n")
    if user_evidence:
        evidence_summary = ", ".join(f"{k}={v}" for k, v in user_evidence.items())
        print(f"**Provided evidence:** {evidence_summary}\n")
    if missing:
        print(
            "**Unrecognized functions (skipped):** "
            + ", ".join(missing)
            + "\n"
        )

    print("| Function | Reframed message | Evidence to bring | Specific ask |")
    print("|---|---|---|---|")
    for row in rows:
        print(row)
    print()
    print(build_next_step_prompt(insight, requested, displays))

    return 0


if __name__ == "__main__":
    sys.exit(main())
