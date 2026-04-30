# Marketing Metrics Formulas

Unified across GA4 + Google Ads + CRM data.

## Top-line metrics (from GA4)

| Metric | Formula | What it tells you |
|---|---|---|
| **Sessions** | Total visits | Raw traffic volume |
| **Users** | Unique visitors | Audience size |
| **Conversion rate** | conversions / sessions | How well site converts traffic |
| **Bounce rate** | single-page sessions / total sessions | Landing page relevance |
| **Pages/session** | pageviews / sessions | Engagement depth |
| **Avg session duration** | total session time / sessions | Engagement time |

## Paid media metrics (from Google Ads)

| Metric | Formula | What it tells you |
|---|---|---|
| **CTR** | clicks / impressions | Ad creative + targeting quality |
| **CPC** | cost / clicks | Auction pressure |
| **CPM** | cost / (impressions/1000) | Reach efficiency |
| **CVR** | conversions / clicks | Landing page match + offer |
| **CPA** | cost / conversions | Cost per customer/lead |
| **ROAS** | revenue / spend | Return for every $1 spent |
| **ROI** | (revenue - spend) / spend × 100 | Net profitability |

## Merged metrics (GA4 + Ads + CRM)

Need data from multiple sources.

### Channel attribution

- **Organic sessions**: from GA4 with `sessionDefaultChannelGroup = Organic Search`
- **Paid sessions**: Organic Search + Paid Search + Paid Social
- **% of sessions from paid**: paid / total
- **Blended ROAS**: total revenue / total paid spend (merges all paid channels)

### Customer Acquisition Cost (CAC)

```
CAC = total sales + marketing spend / new customers acquired
```

- Total spend includes paid ads + tooling + % of team cost if attributable
- New customers from CRM
- CAC is more complete than CPA (CPA = ad cost only)

### Lifetime Value to CAC ratio (LTV:CAC)

```
LTV:CAC = avg customer lifetime value / CAC
```

- 3:1 is the "sustainable growth" benchmark
- Below 1:1 = losing money per customer
- Above 5:1 = might be under-investing in acquisition

### Marketing-attributable revenue

```
Marketing revenue = revenue from {marketing-attributed channels}
                  = (organic sessions × conv rate × AOV)
                  + (paid channel revenue, from Ads)
                  + (email channel revenue, from ESP)
```

### Conversion funnel metrics

```
Stage 1: Awareness (impressions)
Stage 2: Interest (clicks, sessions)
Stage 3: Consideration (pageviews per session, time on site)
Stage 4: Intent (add-to-cart, form start)
Stage 5: Conversion (purchase, signup)
Stage 6: Loyalty (repeat purchase, retention)

Funnel conversion rate = each stage / previous stage
```

Where each leak happens tells you what to fix.

## Attribution models (GA4 default)

GA4 uses **data-driven attribution** by default (post-2023). Key models:

| Model | How it assigns credit |
|---|---|
| **Last click** | 100% to last click before conversion |
| **First click** | 100% to first touchpoint |
| **Linear** | Equal credit across all touchpoints |
| **Time decay** | More recent touchpoints get more credit |
| **Position-based** | 40% first + 40% last + 20% middle |
| **Data-driven** | ML model trained on your data |

Default is data-driven, which usually gives best attribution but requires enough conversions to train (10+/day).

## Common calculation gotchas

1. **"Conversion" definition drift**: GA4 conversions ≠ Ads conversions. GA4 counts events; Ads counts what you told it to count. Can differ 20%+.

2. **Attribution window**: Ads default 30-day click, 1-day view. Conversions that happen on day 31 don't show. Adjust if your cycle is longer.

3. **Double-counting**: If both GA4 and Ads report "conversion", make sure you're not summing. One view per metric.

4. **Revenue vs gross margin**: ROAS uses revenue; ROI uses profit. Don't confuse. A 5:1 ROAS can still lose money if margin is 20%.

5. **Currency**: GA4 revenue might be in USD, Ads cost in VND. Normalize.

6. **Segmentation**: Aggregate numbers hide everything. Always segment by device, channel, campaign for actionable insight.
