#!/usr/bin/env python3
"""
three_circles.py — Urbany & Davis 3-circles diagnostic.

Inputs (all comma-separated):
  --needs       Customer needs/wishes within segment.
  --you         Your offering as customers PERCEIVE it.
  --competitor  Competitor offering as customers PERCEIVE it.

Computes 6 zones:
  - Sweet spot      = needs ∩ you - competitor          (unique value)
  - Surrender zone  = needs ∩ you ∩ competitor          (commodity)
  - Equity at risk  = you - needs - competitor          (you invest in non-needs)
  - Opportunity     = needs - you - competitor          (unmet need)
  - Competitor strength = needs ∩ competitor - you      (catch up or concede)
  - Competitor waste    = competitor - needs - you      (their mistake)

Output: structured Markdown analysis with strategic recommendation per zone.
"""

import argparse
import re


# Trivial stemming: drop common suffixes for matching.
STEM_SUFFIXES = ("ing", "ation", "ions", "ed", "es", "s")


def normalize(item):
    """Lowercase, strip punctuation, collapse whitespace, light stemming."""
    item = item.strip().lower()
    item = re.sub(r"[^a-z0-9\s\-/]", " ", item)
    item = re.sub(r"\s+", " ", item).strip()
    return item


def stem(token):
    for suf in STEM_SUFFIXES:
        if len(token) > len(suf) + 2 and token.endswith(suf):
            return token[: -len(suf)]
    return token


def signature(item):
    """Return a stem-based signature set for fuzzy matching."""
    norm = normalize(item)
    tokens = [t for t in re.split(r"[\s/\-]+", norm) if t]
    return frozenset(stem(t) for t in tokens if t)


def parse_list(raw):
    """Split comma-separated list into normalized items keyed by signature."""
    if not raw:
        return {}
    items = [i.strip() for i in raw.split(",") if i.strip()]
    indexed = {}
    for item in items:
        sig = signature(item)
        if sig:
            # Keep first occurrence text for display.
            indexed.setdefault(sig, item.strip())
    return indexed


def zone_items(sig_set, lookup_a, lookup_b=None, lookup_c=None):
    """Resolve signature set back to display strings, preferring earlier sources."""
    out = []
    for sig in sig_set:
        for src in (lookup_a, lookup_b, lookup_c):
            if src and sig in src:
                out.append(src[sig])
                break
    return sorted(out, key=str.lower)


def render(zones):
    out = []
    out.append("# Three Circles Analysis (Urbany & Davis)")
    out.append("")
    out.append(
        "Each zone shows items + the recommended strategic action. "
        "All overlaps are computed via case-insensitive stem matching."
    )
    out.append("")

    sections = [
        ("Sweet Spot — UNIQUE VALUE",
         "needs ∩ you - competitor",
         zones["sweet"],
         "AMPLIFY in messaging, prioritize in roadmap, lead the positioning statement here."),
        ("Surrender Zone — COMMODITY",
         "needs ∩ you ∩ competitor",
         zones["surrender"],
         "Accept as table stakes (Points of Parity) OR push to differentiate further."),
        ("Equity at Risk — INVESTING IN NON-NEEDS",
         "you - needs - competitor",
         zones["equity_risk"],
         "KILL the spend OR reposition the attribute to map onto an unmet need."),
        ("Opportunity — UNMET NEED",
         "needs - you - competitor",
         zones["opportunity"],
         "VALIDATE demand with quick research, then BUILD capability — strongest PoD candidate."),
        ("Competitor Strength — CATCH UP OR CONCEDE",
         "needs ∩ competitor - you",
         zones["competitor_strength"],
         "Decide explicitly: close the gap (roadmap), neutralize (competitive PoP), or concede the segment slice."),
        ("Competitor Waste — THEIR MISTAKE",
         "competitor - needs - you",
         zones["competitor_waste"],
         "Note for intel; do NOT mirror their mistake. No action required."),
    ]

    for title, formula, items, action in sections:
        out.append(f"## {title}")
        out.append(f"_Formula: {formula}_")
        out.append("")
        if items:
            for it in items:
                out.append(f"- {it}")
        else:
            out.append("- (empty)")
        out.append("")
        out.append(f"**Action:** {action}")
        out.append("")

    out.append("## Strategic Summary")
    if zones["sweet"]:
        out.append(f"- Sweet-spot anchors ({len(zones['sweet'])}): lead positioning here.")
    else:
        out.append("- No sweet spot detected — your perceived offering does not uniquely cover any named need. Highest priority: close this gap.")
    if zones["opportunity"]:
        out.append(f"- Open opportunities ({len(zones['opportunity'])}): unmet needs neither side covers.")
    if zones["equity_risk"]:
        out.append(f"- Wasted equity ({len(zones['equity_risk'])}): consider cutting or repositioning.")
    if zones["competitor_strength"]:
        out.append(f"- Competitor advantages ({len(zones['competitor_strength'])}): decide catch-up vs concede.")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Run the Urbany-Davis 3-circles diagnostic."
    )
    parser.add_argument("--needs", required=True, help="Customer needs (comma-separated).")
    parser.add_argument("--you", required=True, help="Your offering as customers perceive it.")
    parser.add_argument("--competitor", required=True, help="Competitor offering as customers perceive it.")
    args = parser.parse_args()

    needs = parse_list(args.needs)
    you = parse_list(args.you)
    competitor = parse_list(args.competitor)

    needs_sig = set(needs.keys())
    you_sig = set(you.keys())
    comp_sig = set(competitor.keys())

    zones = {
        "sweet": (needs_sig & you_sig) - comp_sig,
        "surrender": needs_sig & you_sig & comp_sig,
        "equity_risk": you_sig - needs_sig - comp_sig,
        "opportunity": needs_sig - you_sig - comp_sig,
        "competitor_strength": (needs_sig & comp_sig) - you_sig,
        "competitor_waste": comp_sig - needs_sig - you_sig,
    }

    resolved = {
        name: zone_items(sigs, needs, you, competitor)
        for name, sigs in zones.items()
    }
    print(render(resolved))


if __name__ == "__main__":
    main()
