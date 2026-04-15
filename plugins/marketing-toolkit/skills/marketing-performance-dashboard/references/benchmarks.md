# Marketing Performance Benchmarks

Ranges for traffic-light coloring. "Good" = above midpoint for that metric.

## Universal benchmarks

| Metric | Floor | Good | Stretch |
|---|---|---|---|
| Conversion rate | 1% | 2-5% | 5%+ |
| Bounce rate | - | 40-55% | <40% |
| CTR (search ads) | 2% | 3-6% | 8%+ |
| CTR (display) | 0.5% | 0.8-1.5% | 2%+ |
| CPA | varies | industry | - |
| ROAS (blended) | 2:1 | 3-5:1 | 6:1+ |
| ROI (blended) | 100% | 200-400% | 500%+ |

## By vertical

### E-commerce
- Conversion rate: 1.5-3%
- Bounce rate: 40-50%
- Cart abandonment: 65-75% typical (not a bug)
- ROAS: 4:1 target, 6:1+ great
- AOV: vertical-specific

### SaaS (trial → paid)
- Conversion rate: 1-3% (visit → trial), 15-25% (trial → paid)
- LTV:CAC: 3:1 sustainable, 5:1+ strong
- Payback period: <12 months good, <6 months great

### Services / local
- Conversion rate: 2-5% (form submit)
- Cost per lead: industry-varies ($20-300)
- Appointment rate: 30-50% of leads
- Close rate: 25-50% of appointments

### Nonprofit
- Conversion rate (donation): 0.5-2%
- Avg donation: vertical-varies
- Acquisition cost per donor: $20-60

### Content / media
- Bounce rate: 60-80% (normal for content)
- Pages/session: 1.5-3
- Time on page: 90s+ good
- Return visitor rate: 30%+ is healthy

## By traffic source (GA4 channel groups)

| Source | Typical conv rate | Typical cost |
|---|---|---|
| Direct | 2-5% | 0 |
| Organic Search | 2-4% | 0 (content cost) |
| Organic Social | 0.5-1.5% | 0 (content cost) |
| Paid Search | 2-5% | CPC-based |
| Paid Social | 0.8-2% | CPC-based |
| Email | 3-8% | minimal |
| Referral | 1-3% | 0 |

Email consistently has the highest conversion rate of any channel.

## Traffic-light thresholds (what the skill uses)

```python
# 🟢 = above floor of "good" range
# 🟡 = within 20% below floor
# 🔴 = more than 20% below floor
```

For example, conversion rate good range is 2-5%:
- 🟢: ≥2%
- 🟡: 1.6-2%
- 🔴: <1.6%

For "lower is better" metrics (bounce, CPA, unsub):
- 🟢: at or below target ceiling
- 🟡: 20% above ceiling
- 🔴: 25%+ above ceiling

## Period-over-period interpretation

Raw delta isn't enough. Look at:

- **Sustained trend** (3+ periods same direction) = real change
- **Single-period spike** = noise until confirmed next period
- **>30% change** = investigate for tracking issues (might be a bug, not real)

## Seasonality warning

Always compare like-for-like:
- Monday vs Monday (not Monday vs Sunday)
- Week 1 of month vs Week 1 of previous month
- December vs December (not November — holiday bias)
- Post-Black-Friday vs pre-Black-Friday is not a valid comparison

If seasonal, use year-over-year instead of period-over-period.

## When benchmarks mislead

- **New business**: benchmarks are based on mature businesses. Don't demoralize yourself with 42:1 email ROI if you have 100 subscribers.
- **Regulated industries** (healthcare, legal): often lower conversion, don't compare to e-commerce.
- **Very high AOV** (luxury, B2B enterprise): conversion rates below benchmarks are fine — revenue/visitor is the better metric.
- **Audience-specific brands**: if your audience is tiny-but-loyal, engagement rates may dwarf conversion rates. Pick metrics that match your stage.
