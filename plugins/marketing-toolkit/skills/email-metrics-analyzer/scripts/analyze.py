#!/usr/bin/env python3
"""
Email campaign metrics analyzer.

Usage:
    python3 analyze.py data.csv
    python3 analyze.py data.csv --vertical=ecommerce
    python3 analyze.py data.csv --json > out.json

CSV column name variants accepted (case-insensitive):
    sent, recipients, emails_sent
    delivered
    opened, opens, unique_opens
    clicked, clicks, unique_clicks
    unsubscribed, unsubs
    bounced, bounces, hard_bounces
    complained, complaints, spam_reports
    conversions, conversion, converted
    revenue, sales
    spend, cost
    name, campaign_id, campaign
    date, send_date, sent_date
"""
import sys
import csv
import os
import json
import argparse
from collections import defaultdict

try:
    import pandas as pd
except ImportError:
    print("ERROR: missing dependency `pandas`. Install with:")
    print("  pip install pandas")
    print("Or use python3.13 if python3 has broken deps.")
    sys.exit(1)


COL_VARIANTS = {
    "sent": ["sent", "recipients", "emails_sent", "total_sent"],
    "delivered": ["delivered"],
    "opened": ["opened", "opens", "unique_opens", "open"],
    "clicked": ["clicked", "clicks", "unique_clicks", "click"],
    "unsubscribed": ["unsubscribed", "unsubs", "unsubscribe"],
    "bounced": ["bounced", "bounces", "hard_bounces", "bounce"],
    "complained": ["complained", "complaints", "spam_reports", "complaint"],
    "conversions": ["conversions", "conversion", "converted"],
    "revenue": ["revenue", "sales"],
    "spend": ["spend", "cost"],
    "name": ["name", "campaign_id", "campaign", "subject"],
    "date": ["date", "send_date", "sent_date"],
}


BENCHMARKS = {
    "universal": {
        "open_rate": (0.20, 0.25),
        "ctor": (0.10, 0.15),
        "ctr": (0.02, 0.05),
        "conversion_rate": (0.01, 0.05),
        "unsub_rate": (0, 0.005),
        "complaint_rate": (0, 0.001),
        "bounce_rate": (0, 0.02),
        "roi": (42, 42),
    },
    "ecommerce": {"open_rate": (0.18, 0.22), "ctr": (0.020, 0.035), "conversion_rate": (0.01, 0.03), "roi": (45, 45)},
    "saas": {"open_rate": (0.22, 0.28), "ctr": (0.025, 0.04), "roi": (30, 50)},
    "nonprofit": {"open_rate": (0.25, 0.30), "ctr": (0.03, 0.05)},
    "media": {"open_rate": (0.25, 0.30), "ctr": (0.04, 0.08)},
}


def find_col(df, key):
    """Case-insensitive column match with variants."""
    lower = {c.lower().strip(): c for c in df.columns}
    for v in COL_VARIANTS[key]:
        if v in lower:
            return lower[v]
    return None


def safe_div(a, b):
    return (a / b) if b else 0.0


def compute_metrics(row):
    sent = row.get("sent", 0) or 0
    delivered = row.get("delivered") or (sent - (row.get("bounced") or 0))
    opened = row.get("opened", 0) or 0
    clicked = row.get("clicked", 0) or 0
    unsubs = row.get("unsubscribed", 0) or 0
    bounced = row.get("bounced", 0) or 0
    complained = row.get("complained", 0) or 0
    conversions = row.get("conversions", 0) or 0
    revenue = row.get("revenue", 0) or 0
    spend = row.get("spend", 0) or 0

    return {
        "open_rate": safe_div(opened, delivered),
        "ctor": safe_div(clicked, opened),
        "ctr": safe_div(clicked, delivered),
        "conversion_rate": safe_div(conversions, clicked),
        "unsub_rate": safe_div(unsubs, delivered),
        "complaint_rate": safe_div(complained, delivered),
        "bounce_rate": safe_div(bounced, sent),
        "roi": safe_div(revenue - spend, spend) if spend else None,
    }


def traffic_light(metric, value, benchmarks):
    """Return 🟢/🟡/🔴 icon based on benchmark range."""
    if value is None:
        return "⚪"
    bm = benchmarks.get(metric)
    if bm is None:
        return "⚪"
    low, high = bm

    # For "lower is better" metrics
    if metric in ("unsub_rate", "complaint_rate", "bounce_rate"):
        if value <= high: return "🟢"
        if value <= high * 1.5: return "🟡"
        return "🔴"

    # For "higher is better" metrics
    if value >= low: return "🟢"
    if value >= low * 0.8: return "🟡"
    return "🔴"


def fmt_pct(v, digits=2):
    if v is None: return "N/A"
    return f"{v*100:.{digits}f}%"


def fmt_ratio(v, digits=1):
    if v is None: return "N/A"
    return f"{v:.{digits}f}:1"


def analyze(csv_path, vertical="universal"):
    df = pd.read_csv(csv_path)
    # Normalize column names
    rename_map = {}
    for k in COL_VARIANTS:
        c = find_col(df, k)
        if c and c != k:
            rename_map[c] = k
    df = df.rename(columns=rename_map)

    # Fill missing numeric cols with 0
    for k in ["sent", "delivered", "opened", "clicked", "unsubscribed", "bounced", "complained", "conversions", "revenue", "spend"]:
        if k not in df.columns:
            df[k] = 0
        else:
            df[k] = pd.to_numeric(df[k], errors="coerce").fillna(0)

    # Compute per-campaign metrics
    rows = df.to_dict("records")
    for r in rows:
        r["metrics"] = compute_metrics(r)

    # Aggregate totals
    total = {k: df[k].sum() for k in ["sent", "delivered", "opened", "clicked", "unsubscribed", "bounced", "complained", "conversions", "revenue", "spend"]}
    if total["delivered"] == 0:
        total["delivered"] = total["sent"] - total["bounced"]
    overall = compute_metrics(total)

    # Merge benchmark set
    benchmarks = {**BENCHMARKS["universal"], **BENCHMARKS.get(vertical, {})}

    return {"campaigns": rows, "total": total, "overall": overall, "benchmarks": benchmarks, "vertical": vertical}


def format_report(result):
    out = []
    vertical = result["vertical"]
    overall = result["overall"]
    benchmarks = result["benchmarks"]
    n = len(result["campaigns"])

    # Headline
    worst_metric, worst_val, worst_light = None, None, None
    for m, v in overall.items():
        tl = traffic_light(m, v, benchmarks)
        if tl == "🔴":
            worst_metric, worst_val, worst_light = m, v, tl
            break
    best_metric = None
    for m, v in overall.items():
        if traffic_light(m, v, benchmarks) == "🟢":
            best_metric = m
            break

    out.append(f"# Email Performance Report ({n} campaign{'s' if n != 1 else ''}, vertical: {vertical})\n")
    if worst_metric:
        out.append(f"## 🚨 Headline: {worst_metric.replace('_', ' ').title()} is underperforming ({fmt_pct(worst_val)}) — needs attention.\n")
    elif best_metric:
        out.append(f"## 🎉 Headline: All metrics in healthy range. Top strength: {best_metric.replace('_', ' ').title()}.\n")
    else:
        out.append("## Headline: Data analyzed — see metrics below.\n")

    # At-a-glance table
    out.append("## 🚦 This period at a glance\n")
    out.append("| Metric | Actual | Benchmark | Status |")
    out.append("|---|---|---|---|")
    metric_labels = [
        ("open_rate", "Open rate", "pct"),
        ("ctor", "Click-to-open", "pct"),
        ("ctr", "Click-through", "pct"),
        ("conversion_rate", "Conversion rate", "pct"),
        ("unsub_rate", "Unsubscribe rate", "pct"),
        ("complaint_rate", "Complaint rate", "pct"),
        ("bounce_rate", "Bounce rate", "pct"),
        ("roi", "ROI", "ratio"),
    ]
    for key, label, fmt in metric_labels:
        v = overall.get(key)
        tl = traffic_light(key, v, benchmarks)
        bm = benchmarks.get(key)
        if bm:
            low, high = bm
            if key == "roi":
                bm_str = f"{low:.0f}:1"
            elif key in ("unsub_rate", "complaint_rate", "bounce_rate"):
                bm_str = f"<{high*100:.1f}%"
            else:
                bm_str = f"{low*100:.0f}-{high*100:.0f}%"
        else:
            bm_str = "—"
        val_str = fmt_ratio(v) if fmt == "ratio" else fmt_pct(v)
        out.append(f"| {label} | {val_str} | {bm_str} | {tl} |")
    out.append("")

    # Top/bottom per-campaign (if >1)
    if n > 1:
        sorted_by_open = sorted(result["campaigns"], key=lambda r: r["metrics"]["open_rate"], reverse=True)
        out.append("## 🏆 Top performer (by open rate)")
        r = sorted_by_open[0]
        name = r.get("name", f"Campaign {r.get('campaign_id', '?')}")
        out.append(f"- **{name}** — open {fmt_pct(r['metrics']['open_rate'])}, CTR {fmt_pct(r['metrics']['ctr'])}\n")

        out.append("## 🚨 Underperformer (by open rate)")
        r = sorted_by_open[-1]
        name = r.get("name", f"Campaign {r.get('campaign_id', '?')}")
        out.append(f"- **{name}** — open {fmt_pct(r['metrics']['open_rate'])}, CTR {fmt_pct(r['metrics']['ctr'])}")
        out.append("  - Fix: rework subject line (biggest open-rate lever); re-check list hygiene for hard bounces.\n")

    # Recommendations
    out.append("## 🎯 Next 3 experiments")
    if overall.get("open_rate", 0) < benchmarks.get("open_rate", (0, 0))[0] * 0.8:
        out.append("1. **A/B test 3 subject line variants** — clarity-first, personalization, and curiosity hooks.")
        out.append("2. **List hygiene audit** — remove hard bounces + 180-day dormant subscribers.")
        out.append("3. **Sender reputation check** — verify SPF/DKIM/DMARC + check spam placement in mail-tester.com.")
    elif overall.get("ctr", 0) < benchmarks.get("ctr", (0, 0))[0] * 0.8:
        out.append("1. **Simplify primary CTA** — one button, above the fold, action-verb copy.")
        out.append("2. **Test preview text** — first 40 chars determine mobile open intent.")
        out.append("3. **Segment by engagement** — send high-frequency to engaged, reduce cadence for mid-tier.")
    elif overall.get("conversion_rate", 0) < benchmarks.get("conversion_rate", (0, 0))[0] * 0.8:
        out.append("1. **Audit landing page match** — does it deliver what the email promised?")
        out.append("2. **Reduce checkout friction** — test guest checkout, fewer form fields.")
        out.append("3. **A/B test offer** — discount amount vs. free shipping vs. bundle.")
    else:
        out.append("1. **Segment top performers** — find what's working and scale it.")
        out.append("2. **Experiment with send time** — test ±3h from current best slot.")
        out.append("3. **Introduce new content format** — video CTA, interactive element, UGC feature.")
    out.append("")

    # Per-campaign appendix
    out.append("## Appendix: Per-campaign detail\n")
    out.append("| Campaign | Sent | Open | CTR | Conv | Unsub |")
    out.append("|---|---|---|---|---|---|")
    for r in result["campaigns"]:
        m = r["metrics"]
        name = r.get("name", "?")
        out.append(f"| {name} | {int(r.get('sent', 0))} | {fmt_pct(m['open_rate'], 1)} | {fmt_pct(m['ctr'], 2)} | {fmt_pct(m['conversion_rate'], 1)} | {fmt_pct(m['unsub_rate'], 2)} |")

    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv", help="Path to CSV with email campaign data")
    p.add_argument("--vertical", default="universal", choices=list(BENCHMARKS.keys()))
    p.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    args = p.parse_args()

    if not os.path.exists(args.csv):
        print(f"ERROR: file not found: {args.csv}")
        sys.exit(2)

    result = analyze(args.csv, args.vertical)

    if args.json:
        # Make JSON-serializable
        slim = {
            "vertical": result["vertical"],
            "total": {k: float(v) for k, v in result["total"].items()},
            "overall": {k: (float(v) if v is not None else None) for k, v in result["overall"].items()},
            "benchmarks": {k: list(v) for k, v in result["benchmarks"].items()},
            "campaign_count": len(result["campaigns"]),
        }
        print(json.dumps(slim, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
