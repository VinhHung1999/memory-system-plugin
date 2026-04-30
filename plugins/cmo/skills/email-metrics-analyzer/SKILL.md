---
name: email-metrics-analyzer
description: Analyze email campaign data (CSV) and generate a stakeholder-ready performance report. Computes 9 standard email marketing metrics (open rate, click-to-open, CTR, unsubscribe, complaint, conversion, forward, list growth, bounce, ROI), compares each against industry benchmarks with traffic-light alerts (🟢/🟡/🔴), and produces a 4-pillar report (concise, visual, engaging, show growth). Use this skill whenever the user has email campaign data (CSV/spreadsheet) and wants to analyze performance, calculate metrics, generate a monthly/weekly email report, evaluate ROI, diagnose poor performance, or compare campaigns — even if they don't use the word "analyze".
---

# Email Metrics Analyzer

Takes raw email campaign data and produces a reproducible, benchmark-calibrated performance report. Built on Google's Digital Marketing certificate Course 4 Module 4: the 9-metric framework, the data → metrics → KPIs → reports pyramid, and the 4-pillar report framework.

## When this triggers

User has email sends data (a CSV, spreadsheet, or pasted numbers) and wants to know how campaigns performed. They may phrase it as: "analyze my email campaign", "how did last month's newsletter do", "calculate my open rate", "is my email ROI good", "which campaign performed best", or simply paste numbers and ask "is this good?"

**NOT** the right tool for: live API pulls (use `marketing-performance-dashboard` for that), A/B statistical significance (use `ab-test-designer`), drafting emails (use `email-campaign-builder`).

## Input formats

### CSV (preferred)
Required columns (column names are flexible — script detects common variants):
- `campaign_id` or `name` — identifier
- `date` or `send_date` — when sent
- `sent` or `recipients` — total sent
- `delivered` (optional — defaults to `sent - bounced`)
- `opened` — unique opens
- `clicked` — unique clicks
- `unsubscribed` — count
- `bounced` (optional)
- `complained` (optional — spam reports)
- `conversions` (optional)
- `revenue` (optional — for ROI)
- `spend` (optional — for ROI)

### Pasted numbers
Can also accept a free-form description like "I sent 10,000 emails, 2,200 opened, 400 clicked, 30 unsubscribed, 50 conversions, $3,000 revenue, $80 spend". Script parses + computes.

## Workflow

1. **Get the data** — CSV path, or ask user to paste/describe the numbers
2. **Run analysis** — `python3 scripts/analyze.py <csv-path>` OR compute inline if free-form
3. **Compute 9 metrics** per campaign (see `references/metrics-formulas.md`)
4. **Compare vs benchmarks** — each metric gets a traffic-light (🟢 above benchmark, 🟡 within 20% below, 🔴 >20% below)
5. **Generate 4-pillar report**:
   - **Concise** — 1-page exec summary
   - **Visual** — ASCII bars or Markdown tables (PNG charts if matplotlib installed)
   - **Engaging** — opens with top win or top concern
   - **Show growth** — period-over-period comparison if data spans multiple periods
6. **Recommend next actions** — 3 specific experiments to run based on weakest metric

## Why benchmarks matter

Raw metrics are meaningless without context. "25% open rate" is excellent for e-commerce promotional but mediocre for a welcome email (should be 50%+). This skill tags every metric with **type-appropriate benchmark** so users immediately know "good" vs "bad" without memorizing ranges. Pulled from `references/benchmarks.md`.

## Running the analysis script

```bash
python3 scripts/analyze.py /path/to/email-data.csv
# or
python3 scripts/analyze.py /path/to/email-data.csv --vertical=saas  # pick benchmark set
python3 scripts/analyze.py /path/to/email-data.csv --period-over-period  # compare last N vs previous N
```

Outputs:
- Markdown report to stdout
- Optional PNG chart (`--chart`) if matplotlib installed
- Optional JSON (`--json`) for programmatic consumption

Script is standalone — only requires `pandas`. `matplotlib` is optional for charts.

## Report structure (4-pillar)

```
# Email Performance Report — {period}

## 🎯 Headline
[1 sentence: top win OR top concern]

## 🚦 This period at a glance
| Metric | Actual | Benchmark | Status |
|---|---|---|---|
| Open rate | 23.4% | 20-25% | 🟢 |
| CTR | 2.1% | 2-5% | 🟡 |
| ...
| ROI | 28:1 | 42:1 | 🔴 |

## 📈 Trend (vs last period)
- Open rate: +2.1pp (improvement)
- Unsubscribes: +0.3pp (concern)
- ...

## 🏆 Top performer
Campaign X: [why it won]

## 🚨 Underperformer + fix
Campaign Y: [why it lost, specific fix]

## 🎯 Next 3 experiments
1. A/B test {weakest_metric_lever}
2. Audit {secondary_metric}
3. Segment {subsegment}

## Appendix: full per-campaign table
[...]
```

## References

- `references/metrics-formulas.md` — all 9 formulas + what each tells you
- `references/benchmarks.md` — universal + per-vertical + per-email-type benchmarks
- `references/diagnostic-playbook.md` — "what to do if X metric is below benchmark" guide

## Output philosophy

The report should pass the "stakeholder read in 2 minutes" test. That means:
- Headline up top (1 sentence)
- Traffic lights instead of dense tables for the overview
- One concrete recommendation per underperformer (not "consider improving")
- Full detail in appendix for whoever wants to dig in

Don't pad the report with filler. If only 2 campaigns, don't invent insights about "trend". If one metric is clearly the problem, lead with it.
