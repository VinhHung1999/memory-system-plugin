---
name: marketing-performance-dashboard
description: Pull live marketing performance data from Google Analytics 4 + Google Ads APIs and render a unified dashboard with ROI/ROAS/CTR/CPA metrics, traffic-light alerts (🟢🟡🔴), top/underperformer analysis, and recommended next actions. Handles OAuth setup walkthrough, computes attribution across channels, and compares vs benchmarks + previous period. Use this skill whenever the user wants to review marketing performance, generate a weekly/monthly report, audit campaign efficiency, see what's working vs underperforming across paid + organic channels, or asks "how are my ads doing" — even if they don't mention "dashboard".
---

# Marketing Performance Dashboard

Pulls live data from **Google Analytics 4** + **Google Ads** APIs, computes unified metrics, and renders a stakeholder-ready dashboard. Based on Google's Digital Marketing certificate Courses 5 + 6. **Highest-value skill** in the set because it bridges fragmented tools into one actionable view.

## When this triggers

User wants a marketing snapshot from real live data. Phrasings: "marketing dashboard", "GA report", "weekly report", "Google Ads performance", "how are my ads doing", "last month marketing", "quarterly review", "campaign efficiency audit".

**NOT** the right tool for: drafting campaigns (use `email-campaign-builder` / `google-ads-launch-helper`), A/B testing (use `ab-test-designer`), keyword research (use `social-listening-keywords-builder`).

## Prerequisites (ONE-TIME setup)

This skill requires OAuth credentials for Google APIs. First-run walks user through:

1. Create Google Cloud Project (or use existing)
2. Enable APIs: **Google Analytics Data API** + **Google Ads API**
3. OAuth consent screen config
4. Download `credentials.json`
5. Run `scripts/setup_oauth.sh` → opens browser → user grants access → token saved to `~/.config/marketing-dashboard/token.json`
6. Record GA4 property ID + Google Ads customer ID in `~/.config/marketing-dashboard/config.json`

See `references/oauth-setup-walkthrough.md` for step-by-step with screenshots described.

**If user doesn't have Google Cloud project experience:** walk them through slowly. It's the hardest part of the skill.

## Workflow

1. **Check setup** — if `~/.config/marketing-dashboard/token.json` doesn't exist, walk through OAuth setup first
2. **Get date range** — default last 30 days; can be "last 7 days", "last month", custom range, or period-over-period
3. **Pull GA4 data** — run `scripts/fetch_ga4.py` for sessions, users, conv rate, bounce rate, top pages, top sources
4. **Pull Google Ads data** — run `scripts/fetch_google_ads.py` for impressions, clicks, cost, conversions, per-campaign
5. **Compute metrics** — merge GA4 + Ads → compute ROAS, ROI, CTR, CPA, conv rate per channel
6. **Compare vs benchmarks + previous period** — traffic-light each metric
7. **Render dashboard** — use `templates/dashboard.md.j2` to output markdown (PNG charts optional with matplotlib)
8. **Recommend actions** — for each 🔴 metric, give 1-2 specific fixes from `references/diagnostic-playbook.md`

## Running the scripts

```bash
# One-time setup
bash scripts/setup_oauth.sh

# Weekly pull
python3 scripts/fetch_ga4.py --days 30 > /tmp/ga4_data.json
python3 scripts/fetch_google_ads.py --days 30 > /tmp/ads_data.json
python3 scripts/render_dashboard.py --ga4 /tmp/ga4_data.json --ads /tmp/ads_data.json --out dashboard.md
```

Or combined:
```bash
python3 scripts/dashboard.py --days 30 --out dashboard.md
```

## Requirements

Python packages:
- `google-analytics-data` (GA4 Data API)
- `google-ads` (Google Ads API)
- `google-auth-oauthlib` (OAuth flow)
- `matplotlib` (optional, for PNG charts)
- `jinja2` (templating)

Install:
```bash
pip install google-analytics-data google-ads google-auth-oauthlib jinja2 matplotlib
```

## Output structure

```markdown
# Marketing Performance Dashboard — {period}

## 🚦 Alerts (this period)
🔴 CPA up 42% vs prior period ($28 → $40)
🟡 Bounce rate 68% (benchmark <55%)
🟢 ROAS 4.2:1 (target 3:1)

## 📊 Topline metrics
| Metric | Actual | Prev period | Benchmark | Status |
|---|---|---|---|---|
| Sessions | 12,450 | 11,200 (+11%) | — | 🟢 |
| Users | 8,320 | 7,800 (+7%) | — | 🟢 |
| Conv rate | 1.8% | 2.1% | 2-5% | 🟡 |
| ROAS (Ads) | 4.2:1 | 3.9:1 | 3:1 | 🟢 |
| CPA (Ads) | $40 | $28 | — | 🔴 |
...

## 🏆 Top performers
- **Brand Search** — ROAS 6.8:1 (32% of total revenue)
- **Organic Search** — 42% of sessions, 2.4% conv

## 🚨 Underperformers + fixes
- **"Summer Sale" Google Ads campaign** — ROAS 1.2:1 (below 3:1 target)
  → Fix: pause the 3 underperforming ad groups with >$20 CPA
  → Fix: move budget to "Brand Search" which has 6.8:1 ROAS
- **Mobile conv rate** — 1.1% vs desktop 3.8%
  → Fix: mobile UX audit (use `seo-onpage-checklist` for technical check)

## 📈 Trend (last 4 weeks, weekly)
Week 1: $8,200 revenue, $1,950 spend, ROAS 4.2
Week 2: $7,800, $2,100, 3.7
Week 3: $9,300, $2,400, 3.9
Week 4: $10,500, $2,200, 4.8 📈

## 🎯 Next 3 experiments
1. Kill "Summer Sale" → reallocate $800/week to Brand Search
2. A/B test mobile checkout simplification (see `ab-test-designer`)
3. Investigate bounce rate spike — landing page issue?
```

## References

- `references/metrics-formulas.md` — ROI, ROAS, CTR, CPA, conv rate + how to merge GA4 + Ads data
- `references/benchmarks.md` — per-vertical benchmarks (e-comm, SaaS, services, nonprofit)
- `references/oauth-setup-walkthrough.md` — step-by-step Google Cloud + OAuth with screenshot-level detail
- `references/diagnostic-playbook.md` — what to do when X metric is below benchmark

## Why this is the highest-value skill

Marketing data lives in 3-5 tools (GA4, Google Ads, Meta Ads, email ESP, maybe Shopify). Every week, stakeholders ask "how are we doing?" — and the answer requires logging into each tool, exporting, combining in spreadsheet, writing narrative. **30-60 minutes of manual work per report.**

This skill collapses that to **30 seconds** + auto-generates stakeholder-ready narrative. And because metrics are computed deterministically from raw API data, reports are reproducible and auditable — no "which CPA did you use" ambiguity.

LLM alone can't do this — it has no API access to your live data. Skill provides the gateway.

## Fallback: no-API mode

If user doesn't want to set up OAuth (or is just exploring), skill has a **no-API mode** that accepts:
- CSV export from Google Ads UI
- CSV export from GA4 UI
- Pasted numbers

And produces the same dashboard. Less automated but works for users who won't set up APIs.

```bash
python3 scripts/dashboard.py --ga4-csv /path/to/ga4.csv --ads-csv /path/to/ads.csv
```

## Output philosophy

Dashboard should pass the "3-minute stakeholder read" test. Structure ensures that:
- 🚦 Alerts at top — headlines that need action
- Topline table — at-a-glance health check
- Top/bottom performers — where to focus attention
- Trend — is it getting better/worse?
- Next experiments — what to do next

No walls of numbers. Every metric has a benchmark + status + optional action. If a stakeholder reads only the first 10 lines, they understand the state.
