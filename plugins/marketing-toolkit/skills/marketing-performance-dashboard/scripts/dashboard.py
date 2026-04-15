#!/usr/bin/env python3
"""
Marketing Performance Dashboard — pulls GA4 + Google Ads, renders markdown report.

Usage:
    # Live mode (requires OAuth setup)
    python3 dashboard.py --days 30 --out dashboard.md

    # CSV mode (manual export)
    python3 dashboard.py --ga4-csv ga4.csv --ads-csv ads.csv --out dashboard.md

    # Pasted-numbers mode (for quick exploration)
    python3 dashboard.py --totals sessions=12450,users=8320,conversions=155,ad_cost=5200,ad_revenue=21840 --out dashboard.md

Supports period-over-period comparison with --compare-days N (default: same as --days).
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_DIR = Path(os.path.expanduser("~/.config/marketing-dashboard"))
TOKEN_PATH = CONFIG_DIR / "token.json"
CONFIG_PATH = CONFIG_DIR / "config.json"


BENCHMARKS = {
    "conversion_rate": (0.02, 0.05),   # 2-5%
    "bounce_rate": (0.40, 0.55),       # <55% good
    "roas": (3.0, 3.0),                 # 3:1 break-even-plus
    "roi": (0, 0),                      # flex
    "ctr": (0.02, 0.05),                # 2-5%
}


def fetch_ga4_live(property_id, days):
    """Pull GA4 data via API. Requires OAuth token."""
    try:
        from google.oauth2.credentials import Credentials
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
    except ImportError:
        raise RuntimeError("Missing `google-analytics-data`. Install: pip install google-analytics-data")

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    client = BetaAnalyticsDataClient(credentials=creds)

    end = datetime.now().date()
    start = end - timedelta(days=days)
    prev_start = start - timedelta(days=days)
    prev_end = start - timedelta(days=1)

    def _fetch(start_date, end_date):
        req = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date=str(start_date), end_date=str(end_date))],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers"),
                Metric(name="conversions"),
                Metric(name="bounceRate"),
                Metric(name="screenPageViews"),
            ],
        )
        resp = client.run_report(req)
        row = resp.rows[0] if resp.rows else None
        if not row:
            return {"sessions": 0, "users": 0, "conversions": 0, "bounce_rate": 0, "pageviews": 0}
        return {
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "conversions": int(row.metric_values[2].value),
            "bounce_rate": float(row.metric_values[3].value),
            "pageviews": int(row.metric_values[4].value),
        }

    return {
        "current": _fetch(start, end),
        "previous": _fetch(prev_start, prev_end),
    }


def fetch_ads_live(customer_id, developer_token, login_customer_id, days):
    """Pull Google Ads data via GAQL."""
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        raise RuntimeError("Missing `google-ads`. Install: pip install google-ads")

    # Client needs a google-ads.yaml or config dict
    config = {
        "developer_token": developer_token,
        "use_proto_plus": True,
    }
    if login_customer_id and login_customer_id != "PASTE_MANAGER_ACCOUNT_ID_IF_MCC":
        config["login_customer_id"] = login_customer_id
    # OAuth creds
    with open(TOKEN_PATH) as f:
        token = json.load(f)
    config["refresh_token"] = token["refresh_token"]
    config["client_id"] = token["client_id"]
    config["client_secret"] = token["client_secret"]

    client = GoogleAdsClient.load_from_dict(config)
    ga_service = client.get_service("GoogleAdsService")

    def _fetch(range_str):
        query = f"""
            SELECT
              metrics.impressions,
              metrics.clicks,
              metrics.cost_micros,
              metrics.conversions,
              metrics.conversions_value
            FROM campaign
            WHERE segments.date DURING {range_str}
        """
        stream = ga_service.search_stream(customer_id=customer_id, query=query)
        totals = {"impressions": 0, "clicks": 0, "cost": 0, "conversions": 0, "conv_value": 0}
        for batch in stream:
            for row in batch.results:
                totals["impressions"] += row.metrics.impressions
                totals["clicks"] += row.metrics.clicks
                totals["cost"] += row.metrics.cost_micros / 1_000_000
                totals["conversions"] += row.metrics.conversions
                totals["conv_value"] += row.metrics.conversions_value
        return totals

    if days == 7:
        current_range, prev_range = "LAST_7_DAYS", "LAST_14_DAYS"
    elif days == 30:
        current_range, prev_range = "LAST_30_DAYS", "LAST_BUSINESS_WEEK"
    else:
        end = datetime.now().date()
        start = end - timedelta(days=days)
        prev_start = start - timedelta(days=days)
        prev_end = start - timedelta(days=1)
        current_range = f"'{start}' AND '{end}'"
        prev_range = f"'{prev_start}' AND '{prev_end}'"

    return {
        "current": _fetch(current_range),
        "previous": _fetch(prev_range),
    }


def parse_csv(path, type_):
    """Parse GA4 or Ads CSV export. Very lenient on column names."""
    with open(path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return {}
    # Sum numeric columns
    totals = {}
    for row in rows:
        for k, v in row.items():
            try:
                n = float(v.replace(",", "").replace("$", "").replace("%", ""))
                totals[k.lower().strip()] = totals.get(k.lower().strip(), 0) + n
            except (ValueError, AttributeError):
                pass
    return totals


def parse_totals(arg):
    """Parse '--totals key=value,key=value,...'."""
    d = {}
    for pair in arg.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            d[k.strip()] = float(v.strip())
    return d


def compute_metrics(ga4_cur, ga4_prev, ads_cur, ads_prev):
    def safe_div(a, b):
        return (a / b) if b else 0.0

    def metrics_one_period(ga4, ads):
        sessions = ga4.get("sessions", 0)
        users = ga4.get("users", 0)
        conversions = ga4.get("conversions", 0)
        bounce = ga4.get("bounce_rate", 0)

        impressions = ads.get("impressions", 0)
        clicks = ads.get("clicks", 0)
        cost = ads.get("cost", 0)
        ads_conversions = ads.get("conversions", 0)
        revenue = ads.get("conv_value", 0)

        return {
            "sessions": sessions,
            "users": users,
            "conversions": conversions,
            "conversion_rate": safe_div(conversions, sessions),
            "bounce_rate": bounce,
            "impressions": impressions,
            "clicks": clicks,
            "cost": cost,
            "ads_conversions": ads_conversions,
            "revenue": revenue,
            "ctr": safe_div(clicks, impressions),
            "cpc": safe_div(cost, clicks),
            "cpa": safe_div(cost, ads_conversions),
            "roas": safe_div(revenue, cost),
            "roi": safe_div(revenue - cost, cost) if cost else 0,
        }

    return {
        "current": metrics_one_period(ga4_cur, ads_cur),
        "previous": metrics_one_period(ga4_prev, ads_prev),
    }


def traffic_light(metric, value, reverse=False):
    bm = BENCHMARKS.get(metric)
    if not bm or value == 0:
        return "⚪"
    low, high = bm
    if reverse:
        if value <= high: return "🟢"
        if value <= high * 1.25: return "🟡"
        return "🔴"
    else:
        if value >= low: return "🟢"
        if value >= low * 0.8: return "🟡"
        return "🔴"


def pct_change(cur, prev):
    if not prev: return "N/A"
    change = (cur - prev) / prev * 100
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.1f}%"


def format_dashboard(metrics, period_label):
    cur = metrics["current"]
    prev = metrics["previous"]

    out = []
    out.append(f"# Marketing Performance Dashboard — {period_label}\n")

    # Alerts
    alerts = []
    if cur["roas"] < 3.0 and cur["cost"] > 0:
        alerts.append(f"🔴 ROAS {cur['roas']:.1f}:1 (benchmark 3:1)")
    if cur["cpa"] > prev["cpa"] * 1.3 and prev["cpa"] > 0:
        alerts.append(f"🔴 CPA up {pct_change(cur['cpa'], prev['cpa'])} vs prior period (${prev['cpa']:.0f} → ${cur['cpa']:.0f})")
    if cur["bounce_rate"] > 0.55:
        alerts.append(f"🟡 Bounce rate {cur['bounce_rate']*100:.0f}% (benchmark <55%)")
    if cur["conversion_rate"] < 0.02 and cur["sessions"] > 100:
        alerts.append(f"🟡 Conversion rate {cur['conversion_rate']*100:.2f}% (benchmark 2-5%)")

    if alerts:
        out.append("## 🚦 Alerts\n")
        for a in alerts:
            out.append(a)
        out.append("")
    else:
        out.append("## 🚦 All metrics healthy\n")

    # Topline table
    out.append("## 📊 Topline metrics\n")
    out.append("| Metric | Actual | vs prev | Benchmark | Status |")
    out.append("|---|---|---|---|---|")

    def row(label, metric, fmt, bm_str, reverse=False):
        val = cur[metric]
        prev_val = prev[metric]
        if fmt == "pct": val_s, prev_s = f"{val*100:.2f}%", f"{prev_val*100:.2f}%"
        elif fmt == "money": val_s, prev_s = f"${val:,.0f}", f"${prev_val:,.0f}"
        elif fmt == "ratio": val_s, prev_s = f"{val:.1f}:1", f"{prev_val:.1f}:1"
        else: val_s, prev_s = f"{int(val):,}", f"{int(prev_val):,}"
        tl = traffic_light(metric, val, reverse=reverse)
        out.append(f"| {label} | {val_s} | {pct_change(val, prev_val)} | {bm_str} | {tl} |")

    row("Sessions", "sessions", "int", "—")
    row("Users", "users", "int", "—")
    row("Conv rate", "conversion_rate", "pct", "2-5%")
    row("Bounce rate", "bounce_rate", "pct", "<55%", reverse=True)
    if cur["cost"] > 0:
        row("Ad spend", "cost", "money", "—")
        row("Ad revenue", "revenue", "money", "—")
        row("ROAS", "roas", "ratio", "3:1")
        row("CTR", "ctr", "pct", "2-5%")
        row("CPA", "cpa", "money", "—")
    out.append("")

    # Recommendations
    out.append("## 🎯 Next 3 experiments\n")
    recs = []
    if cur["roas"] < 3.0 and cur["cost"] > 0:
        recs.append("Review campaigns with ROAS <3:1 — pause or shift budget to top performers.")
    if cur["conversion_rate"] < 0.02:
        recs.append("Audit landing page match to ad/campaign intent; test single-CTA simplification.")
    if cur["bounce_rate"] > 0.6:
        recs.append("Investigate top-bounce pages in GA4 — is content or load time the issue?")
    if not recs:
        recs = [
            "Scale top-performing campaign budgets by +20% (watch ROAS).",
            "Test send-time variation on highest-engagement channel.",
            "Deep-dive mobile-specific performance (bounce / conv rate by device).",
        ]
    for i, r in enumerate(recs[:3], 1):
        out.append(f"{i}. {r}")
    out.append("")

    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--ga4-csv")
    p.add_argument("--ads-csv")
    p.add_argument("--totals", help="Pasted-numbers mode: 'sessions=X,users=Y,...'")
    p.add_argument("--out", default="-")
    args = p.parse_args()

    if args.totals:
        # Pasted-numbers mode
        t = parse_totals(args.totals)
        ga4_cur = {"sessions": t.get("sessions", 0), "users": t.get("users", 0), "conversions": t.get("conversions", 0), "bounce_rate": t.get("bounce_rate", 0) / (100 if t.get("bounce_rate", 0) > 1 else 1), "pageviews": 0}
        ga4_prev = {k: 0 for k in ga4_cur}
        ads_cur = {"impressions": t.get("impressions", 0), "clicks": t.get("clicks", 0), "cost": t.get("ad_cost", t.get("cost", 0)), "conversions": t.get("conversions", 0), "conv_value": t.get("ad_revenue", t.get("revenue", 0))}
        ads_prev = {k: 0 for k in ads_cur}
        period = "pasted totals"
    elif args.ga4_csv or args.ads_csv:
        ga4_cur = parse_csv(args.ga4_csv, "ga4") if args.ga4_csv else {}
        ads_cur = parse_csv(args.ads_csv, "ads") if args.ads_csv else {}
        ga4_prev = {}
        ads_prev = {}
        period = "CSV import"
    else:
        # Live mode
        if not CONFIG_PATH.exists():
            print(f"ERROR: config not found at {CONFIG_PATH}")
            print("Run scripts/setup_oauth.sh first.")
            sys.exit(2)
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        print(f"Pulling GA4 + Ads data for last {args.days} days...", file=sys.stderr)
        try:
            ga4 = fetch_ga4_live(config["ga4_property_id"], args.days)
            ga4_cur, ga4_prev = ga4["current"], ga4["previous"]
        except Exception as e:
            print(f"WARN: GA4 fetch failed: {e}", file=sys.stderr)
            ga4_cur = ga4_prev = {}
        try:
            ads = fetch_ads_live(
                config["google_ads_customer_id"],
                config["google_ads_developer_token"],
                config.get("google_ads_login_customer_id"),
                args.days,
            )
            ads_cur, ads_prev = ads["current"], ads["previous"]
        except Exception as e:
            print(f"WARN: Ads fetch failed: {e}", file=sys.stderr)
            ads_cur = ads_prev = {}
        period = f"last {args.days} days"

    metrics = compute_metrics(ga4_cur, ga4_prev, ads_cur, ads_prev)
    report = format_dashboard(metrics, period)

    if args.out == "-":
        print(report)
    else:
        with open(args.out, "w") as f:
            f.write(report)
        print(f"Dashboard written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
