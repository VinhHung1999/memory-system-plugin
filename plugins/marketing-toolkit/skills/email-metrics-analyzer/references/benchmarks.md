# Email Benchmarks — Universal + Vertical + Type

Same as `email-campaign-builder/references/benchmarks.md` but focused on evaluation context.

## Universal

| Metric | Benchmark | Traffic light threshold |
|---|---|---|
| Open rate | 20-25% | 🟢 ≥20%, 🟡 16-20%, 🔴 <16% |
| CTOR | 10-15% | 🟢 ≥10%, 🟡 8-10%, 🔴 <8% |
| CTR | 2-5% | 🟢 ≥2%, 🟡 1.6-2%, 🔴 <1.6% |
| Conversion rate | 1-5% | 🟢 ≥1%, 🟡 0.8-1%, 🔴 <0.8% |
| Unsub rate | <0.5% | 🟢 <0.5%, 🟡 0.5-0.75%, 🔴 >0.75% |
| Complaint rate | <0.1% | 🟢 <0.1%, 🟡 0.1-0.15%, 🔴 >0.15% |
| Bounce rate | <2% | 🟢 <2%, 🟡 2-3%, 🔴 >3% |
| ROI | 42:1 | 🟢 ≥42, 🟡 34-42, 🔴 <34 |

## By vertical

Use `--vertical=X` flag:

### ecommerce
- Open: 18-22% (slightly below universal due to promotional heaviness)
- CTR: 2.0-3.5%
- Conv: 1-3%
- ROI: 45:1

### saas / b2b
- Open: 22-28% (smaller list, higher relevance)
- CTR: 2.5-4%
- ROI: 30-50:1 (harder to measure precisely)

### nonprofit
- Open: 25-30%
- CTR: 3-5%
- Donation conv: 0.5-2%

### media / content
- Open: 25-30%
- CTR: 4-8%

## By email type (for single-type analysis)

| Type | Open (typical) | CTR (typical) |
|---|---|---|
| Welcome | 45-60% | 10-15% |
| Promotional | 15-25% | 2-4% |
| Newsletter | 22-28% | 3-6% |
| Retention (win-back) | 20-35% | 5-10% |
| Acquisition | 12-20% | 1-3% |

## When to override defaults

- **Mixed-type campaigns:** use universal benchmarks
- **Single-type analysis:** use type-specific (welcome shouldn't be compared to promo benchmarks)
- **New list (<1000):** benchmarks are less reliable; focus on trends, not absolute values
- **Transactional (order confirms, receipts):** skip this analyzer — transactional benchmarks are totally different (open 40-60%, not marketing)

## Red flags regardless of benchmarks

- Bounce rate >5% → list quality problem
- Complaint rate >0.1% → permission/consent issue
- Unsub rate >2% → cadence too high OR content mismatch
- Open rate drop >20% week-over-week → deliverability incident (check sender reputation, DNS, ISP blocks)
