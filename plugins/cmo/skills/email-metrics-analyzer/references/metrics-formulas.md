# 9 Email Metrics — Formulas + What Each Tells You

From Course 4 Module 4 (m4_04..m4_06).

| # | Metric | Formula | What it tells you |
|---|---|---|---|
| 1 | **Open rate** | opens / delivered | Subject line effectiveness + sender reputation |
| 2 | **Click-to-open (CTOR)** | clicks / opens | Body content quality — of those who opened, how many engaged |
| 3 | **Click-through rate (CTR)** | clicks / delivered | Overall email effectiveness (combines subject + body) |
| 4 | **Conversion rate** | conversions / clicks | Landing page + offer quality |
| 5 | **Unsubscribe rate** | unsubs / delivered | Content relevance + cadence |
| 6 | **Complaint rate** | spam reports / delivered | Permission issue (should be <0.1%) |
| 7 | **Forward rate** | forwards / delivered | Content virality / shareability |
| 8 | **List growth rate** | (new − unsubs − bounces) / total | List health |
| 9 | **Bounce rate** | bounces / sent | List hygiene (hard) + temporary issues (soft) |
| 10 | **ROI** | (revenue − spend) / spend × 100 | Program-level financial justification |

## The data pyramid (m4_02)

```
          Reports (for stakeholders)
            ↑
          KPIs (3-5 critical ones)
            ↑
          Metrics (9 above + context)
            ↑
          Raw data (sends, opens, clicks, purchases)
```

Don't skip levels. A metric without raw data is untrustworthy. A KPI without metrics is vanity. A report without KPIs is prose.

## Which to make KPIs?

Depends on goal:
- **Acquisition/lead gen goal:** Open rate, CTR, conversion rate, list growth
- **E-commerce revenue goal:** CTR, conversion rate, ROI, AOV
- **Retention goal:** Open rate of retention emails, reactivation rate
- **Health check:** Bounce rate, complaint rate, unsub rate

Pick 3-5 max. 10 KPIs = 0 focus.

## Common calculation gotchas

1. **Open rate denominator should be DELIVERED, not sent.** Bounced emails can't open. If you divide by sent, you understate performance.

2. **Unique vs total opens/clicks.** Always use unique for benchmark comparisons. ESPs sometimes report total; divide by `n_recipients_with_at_least_1_open` not by total open events.

3. **Conversion rate base.** Can be conversions/clicks (CTR-conv) OR conversions/delivered (overall). Both valid, but be consistent. Industry usually uses conversions/clicks.

4. **ROI excludes labor.** "Spend" here means direct send cost (ESP fees, ad spend for list-building). Labor/agency fees are separate.

5. **Bounce types matter.** Hard bounces (invalid address) = remove immediately. Soft bounces (full inbox, server down) = retry, remove after 3-5 failures.
