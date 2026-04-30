# Marketing KPI Design Framework — Reference

Comprehensive reference for designing, evaluating, and scaling marketing KPIs at the executive scorecard level. Built from the Coursera courses *Set and Evaluate Winning Marketing KPIs* (Hurix Digital, 2025) and *CMO Excellence* (Module 3).

Load this file when building a scorecard, validating a single KPI, designing a measurement system, or diagnosing a red-zone metric.

---

## Section 1 — The 4-Layer KPI Design Pattern

Every KPI on a board scorecard must trace upward through four layers, in order. If you cannot fill in all four layers for a metric, the metric is not ready for executive reporting.

### Layer 1: Strategic Objective
A clear business outcome — not a marketing activity. Phrased as a result with a number and a deadline.

- BAD: "Run more social media campaigns"
- BAD: "Improve lead quality"
- GOOD: "Increase customer acquisition from organic search by 35 percent in Q2"
- GOOD: "Reduce CAC payback to under 14 months by FY end"
- GOOD: "Lift NRR from 108 to 115 percent in the next 4 quarters"

### Layer 2: Performance Category
The bucket the objective lives in. Categories prevent measurement gaps and stop redundant metrics. Standard buckets:

- Awareness generation
- Lead acquisition
- Conversion optimization
- Customer retention
- Revenue attribution
- Brand health
- Pipeline coverage / sales enablement

### Layer 3: Specific Metric
The exact, named measurement inside the category. Specificity eliminates ambiguity.

- BAD: "Improve lead quality"
- GOOD: "Marketing-qualified leads with score >75, by channel"

### Layer 4: Tracking Mechanism
How and where the metric is collected, calculated, reported. Includes:

- Data source (e.g., GA4, HubSpot, Salesforce, internal data warehouse)
- Calculation formula
- Refresh frequency (weekly is the default for scorecard metrics)
- Owner (single named human)
- Corrective-action trigger (what zone shift triggers what review)

---

### Walkthrough — 3 worked examples

#### Example A: B2B SaaS at Series B
- **Strategic objective**: Reduce CAC payback to under 14 months by FY end.
- **Performance category**: Conversion optimization + revenue attribution.
- **Specific metric**: CAC payback period (months).
- **Tracking mechanism**: Calculated as fully-loaded CAC / (gross-margin-adjusted MRR). Source: Salesforce + finance system. Weekly refresh. Owner: VP Marketing Ops. Trigger: yellow at >15 months, red at >17 months.

#### Example B: E-commerce DTC
- **Strategic objective**: Increase repeat-purchase rate to 35 percent in 12 months.
- **Performance category**: Customer retention.
- **Specific metric**: Day-90 repeat-purchase rate by acquisition cohort.
- **Tracking mechanism**: Cohort table in Shopify + warehouse. Weekly refresh. Owner: Lifecycle Marketing Lead. Trigger: yellow if any cohort drops 3pp WoW; red if 2 consecutive cohorts below target.

#### Example C: 2-sided marketplace
- **Strategic objective**: Improve supply-side liquidity in top 10 metros (defined as >70 percent of demand requests matched within 15 minutes).
- **Performance category**: Awareness generation + lead acquisition (supply side).
- **Specific metric**: Supply-side activation rate (driver/host listings active within 7 days of signup), top 10 metros.
- **Tracking mechanism**: Internal events pipeline. Weekly refresh by metro. Owner: Supply Marketing Lead. Trigger: red if >2 metros below target for 2 weeks.

### Why each layer must trace upward

Skipping a layer creates orphan metrics. A common failure mode: pick the metric first ("everyone tracks CTR, let's track CTR"), then back into a justification. This produces dashboards that measure what's easy, not what's strategic. The 4-layer order — Objective -> Category -> Metric -> Mechanism — forces strategic relevance before measurement convenience.

---

## Section 2 — Activity vs Impact Metrics (the central reframe)

The most important pattern in this skill: activity metrics measure motion, impact metrics measure business outcomes. Activity metrics get discounted by CFOs and boards. Every activity metric on a scorecard should be paired with — or replaced by — its business-impact twin.

### Activity -> Impact translation table

| Activity metric | Business-impact twin |
|---|---|
| Impressions | Reach within ICP (qualified reach) |
| Click-through rate | Cost per qualified visitor |
| Clicks | Pipeline-attributed clicks (clicks from accounts that convert) |
| Engagement rate | Engaged-to-customer conversion rate |
| MQL count | MQL-to-SQL conversion rate |
| Open rate | Trial conversions from email |
| Sessions | Sessions-to-pipeline ratio |
| Page views | Conversion-rate per landing-page bucket |
| Followers | Engaged-followers-to-customers ratio |
| Likes | Net positive sentiment share |
| Shares | Earned amplification by ICP accounts |
| Brand mentions | Net positive sentiment share |
| Reach | Reach within ICP (qualified reach) |
| Video views | Qualified-view-to-pipeline ratio |
| Subscribers | Subscriber-to-customer conversion rate |
| Bounce rate | Qualified-visitor session quality score |
| Time on page | Read-to-trial conversion rate |
| Email send count | Email-to-trial conversion rate |
| Webinar attendees | Webinar-attendee-to-pipeline conversion rate |
| Whitepaper downloads | Whitepaper-download-to-SQL rate |
| Branded search volume | Branded-search-to-trial rate |
| Social share of voice | Net positive share of voice within ICP |
| Demo requests | Demo-to-closed-won rate |
| Booth scans | Booth-scan-to-pipeline rate |
| App installs | Day-30 retained installs from paid |

### Why activity metrics get discounted by CFOs

**Paragraph 1 — Activity metrics confuse motion with progress.** A team that doubled impressions but did not move pipeline has not earned credit; it has burned money. The CFO sees the activity number as a leading indicator at best, but only if the team also shows the downstream conversion. If the conversion isn't shown, the CFO assumes there is nothing to show — and discounts the spend accordingly.

**Paragraph 2 — Activity metrics are easy to game.** Impressions can be bought. CTR can be juiced by sloppy targeting. Engagement can be inflated by giveaways. Business-impact metrics — CLV, NRR, payback period — are much harder to manipulate without actually moving the business. CFOs and McKinsey-style operators know this and weight metrics by gameability.

**Paragraph 3 — Activity metrics don't translate to capital allocation decisions.** The CFO uses metrics to decide whether to fund the next quarter's marketing budget. "We grew impressions 40 percent" doesn't help — it doesn't tell finance whether to put another $2M into marketing or into R&D. "We grew sourced-pipeline 40 percent and CAC payback dropped from 18 to 14 months" does. The McKinsey reframe: marketing earns budget by proving capital-allocation ROI, not by proving activity output.

---

## Section 3 — Board Metric Library

Each entry: what it measures, formula, target benchmarks by stage, how a CFO interprets it.

### CLV (Customer Lifetime Value)
- **What it measures**: Total margin a customer contributes over their relationship with the company.
- **Formula**: `(Average revenue per customer per period) * (Gross margin %) * (Average customer lifetime in periods)`.
- **Targets by stage**:
  - Seed: track directionally; 3-month proxy.
  - Series A-B: CLV/CAC >= 3.0.
  - Late stage: CLV/CAC >= 5.0; CLV growth YoY >= 15 percent.
- **CFO interpretation**: Direct proxy for unit economics. If CLV is rising and CAC is stable, marketing is creating equity value. If CLV is flat and you're adding customers, you're filling a leaky bucket.

### LTV/CAC ratio
- **What it measures**: Capital efficiency of customer acquisition.
- **Formula**: `LTV / Fully-loaded CAC`.
- **Targets**: 3.0 is the floor for SaaS; <1.0 is unsustainable; >5.0 may signal under-investment in growth.
- **CFO interpretation**: Single best metric for whether to scale spend. Ratio rising -> green-light more spend. Ratio falling -> diagnostic before more spend.

### NRR (Net Revenue Retention)
- **What it measures**: Revenue from existing customers, including expansion/upsell minus churn/downgrades.
- **Formula**: `(Starting ARR + Expansion - Downgrade - Churn) / Starting ARR`, rolling 12-month basis, no new logos.
- **Targets**:
  - Seed/A: 100-110 percent.
  - Series B-C: 110-120 percent.
  - Late stage: 120+ percent for top quartile SaaS.
- **CFO interpretation**: The "best growth metric" for SaaS. >120 percent NRR means existing customers fund growth even with zero new logos. <100 percent means you cannot grow without ever-increasing acquisition spend.

### Gross Retention
- **What it measures**: Pure retention without expansion.
- **Formula**: `(Starting ARR - Churn - Downgrade) / Starting ARR`.
- **Targets**: 90 percent floor for SaaS; 95 percent is good; 98 percent is best-in-class.
- **CFO interpretation**: Quality of the customer base. Strong NRR with weak gross retention means a few accounts are masking a churn problem.

### Churn Rate (logo + revenue)
- **What it measures**: Two flavors — logos lost (count) and revenue lost (dollars).
- **Formula**: Logo churn = `Lost customers / starting customers`. Revenue churn = `Lost MRR / starting MRR`.
- **Targets**: Logo churn 5-7 percent annual for SMB SaaS; <3 percent for enterprise. Revenue churn should track logo churn but lower if losing small accounts.
- **CFO interpretation**: Survival rate. High churn invalidates any acquisition story.

### Market Share / Share of Wallet
- **What it measures**: Your slice of the addressable market.
- **Formula**: `Your revenue / Total category revenue` (if known) or `Your customers / Total category customers`.
- **Targets**: Stage-dependent, but board cares about *direction* — gaining share or losing share.
- **CFO interpretation**: Share gain in flat market = winning; share loss in growing market = hidden problem masked by tide.

### NPS / Customer Advocacy
- **What it measures**: Likelihood of recommendation as proxy for advocacy.
- **Formula**: Promoters (9-10) minus Detractors (0-6) as a percentage.
- **Targets**: 30+ is decent SaaS; 50+ is excellent; 70+ is best-in-class consumer brands.
- **CFO interpretation**: Leading indicator for retention and viral acquisition. Standalone NPS is not actionable — pair with onboarding-completion or feature-adoption metric.

### Brand Health Score
- **What it measures**: Composite of awareness, consideration, preference, advocacy in the target market.
- **Formula**: Weighted survey index (typical: 30 percent awareness + 20 percent consideration + 30 percent preference + 20 percent NPS).
- **Targets**: Year-over-year improvement of 5-10 percent is realistic; baseline first.
- **CFO interpretation**: Long-term moat indicator. Hard to game, expensive to move, slow to change. Useful for the long view; not for weekly review.

### Share of Voice
- **What it measures**: Your share of category conversation in earned + paid media.
- **Formula**: `Mentions of your brand / Mentions of all brands in category`, weighted by sentiment.
- **Targets**: SoV > market share is leading-indicator territory; SoV < market share is concerning.
- **CFO interpretation**: Predictive of share gain in 12-24 months when paired with positive sentiment.

### Pipeline Coverage Ratio
- **What it measures**: How much pipeline marketing has built relative to revenue target.
- **Formula**: `Open pipeline / Quarterly revenue target`.
- **Targets**: 3x is the SaaS standard; <3x signals upcoming revenue miss; >5x signals possible bloat.
- **CFO interpretation**: Single best leading indicator for next-quarter revenue. The CFO will ask for this every Monday.

### CAC Payback Period
- **What it measures**: How many months to recover acquisition cost via gross-margin-adjusted MRR.
- **Formula**: `Fully-loaded CAC / (ARPA * gross margin %)`, in months.
- **Targets**: 12-18 months is healthy SaaS; under 12 is excellent; over 24 is unsustainable.
- **CFO interpretation**: Cash-efficiency metric. Shorter payback means you can self-fund growth. The CFO cares about this almost as much as NRR.

### Revenue contribution from marketing
- **What it measures**: ARR / pipeline directly attributable to marketing.
- **Formula**: `Marketing-sourced ARR / Total new ARR` (and pipeline equivalent).
- **Targets**: 30-50 percent for inbound-led SaaS; 10-25 percent for sales-led; varies wildly.
- **CFO interpretation**: Marketing's ROI proof. Track multi-touch and last-touch in parallel; never report only one.

---

## Section 4 — The 4-Pillar Scaling Framework

(Source: CMO Excellence Module 3, "Scaling Marketing Impact Across the Enterprise.")

When marketing scales beyond the founder/early-CMO stage, four pillars become non-negotiable.

### Pillar 1 — Aligned Measurement
Every campaign has a clear line of sight to a business outcome (pipeline contribution, retention uplift, margin expansion). No campaign launches without an explicit pre-stated business outcome and the metric that will measure it. This is the antidote to "we doubled campaign budget but sales growth hasn't moved an inch."

### Pillar 2 — Scaled Customer Insights
Move beyond "which campaigns perform" to "why and how customer needs are shifting across markets and segments." Insights are systematized — recurring research cadence, segment-level dashboards, voice-of-customer pipeline — so the team can pivot to long-term value drivers, not just short-term performance signals.

### Pillar 3 — Resource Orchestration
At scale, the question is not "do we have a good campaign" but "are we deploying the right mix of channels, budgets, and teams to maximize impact across the portfolio?" This balances global brand consistency with local market flexibility. Portfolio-level mix is a CMO decision, not a channel-team decision.

### Pillar 4 — Executive Storytelling
Translate marketing results into the language of growth, risk, and shareholder value. Boards don't speak campaign — they speak ARR, churn, share gain, payback period. The SaaS CMO who tied each marketing dollar to pipeline, ARR growth, and reduced churn earned greater budget approvals, tighter sales alignment, and a stronger voice in corporate strategy. Same data, different frame.

---

## Section 5 — Traffic-Light Zoning Rules

### Thresholds (default)
For "higher is better" metrics, variance vs target:
- **Green**: variance >= -5 percent (within 5 percent of target, or exceeding).
- **Yellow**: variance between -5 and -15 percent.
- **Red**: variance < -15 percent.

For "lower is better" metrics (CAC payback, churn, cost per acquisition), invert the sign before zoning.

### Why "everything yellow" means targets are wrong
If 100 percent of your KPIs are yellow, the targets themselves are miscalibrated. Yellow is supposed to be the diagnose-and-prep zone — not the resting state. When everything sits there, you have lost the signal.

### Calibration check
- If no metric is *ever* red across multiple quarters: you're not stretching. Reset 1-2 stretch targets.
- If no metric is *ever* green: targets are unrealistic, the team will lose trust in the scorecard.
- A healthy scorecard has 1-2 metrics in red, 2-4 in yellow, the rest in green at any given week.

### Cadence rules
- **Weekly review** is the default scorecard cadence. Daily is too noisy (overreaction to fluctuation); monthly is too late (you miss the corrective window).
- Daily dashboards exist for in-quarter operators; weekly is for the CMO + leads.
- Quarterly is for board narrative, not for action.

---

## Section 6 — Root-Cause Detective Method

The 4-step diagnostic flow when a KPI goes red.

### Step 1 — Gather evidence (don't assume)
List what you have, flag what's missing. Standard evidence dimensions:
- Channel-level breakdown (e.g., Google vs Bing vs LinkedIn)
- Campaign-level breakdown (e.g., demo-request vs free-trial)
- Segment breakdown (SMB vs Mid vs Enterprise)
- Time-series trend (declining how long? when did it start?)
- External events (competitor launches, market shifts, seasonality)
- Funnel decomposition (top-funnel volume vs mid-funnel conversion vs bottom-funnel close)
- Data validation (have we confirmed tracking, attribution, calculation?)

### Step 2 — Break the aggregate
Channel-average masks underperformers. Run breakdowns until you find concentration.

Classic example from the Module 2 lecture: Paid search aggregate conversion rate is 2.1 percent vs 3.5 percent target (red). But:
- Google Search: 1.4 percent
- Bing: 3.8 percent

And inside Google Search:
- demo-request campaign: 1.2 percent
- free-trial campaign: 3.6 percent

The aggregate problem is actually one campaign on one channel. The fix is targeted, not broad.

### Step 3 — Identify pattern
- **Concentrated underperformance**: a specific channel/campaign/segment is dragging the aggregate. Most common pattern.
- **Broad decline**: everything is dropping uniformly. Suggests systemic cause: tracking break, attribution change, macro shift, org-wide execution slip.
- **Cyclical/seasonal**: matches a known cycle. Compare same-period YoY before treating as a problem.

### Step 4 — Conclude root cause vs symptom
The board confuses these. The CMO must not.

- **Symptom**: "Paid search conversion is dropping."
- **Concentration**: "Google Ads campaign 'demo-request' is at 1.4 percent vs benchmark 3.5 percent."
- **Cause**: "Competitor outbid us on top keyword starting June 12."

Symptom-treatment failure modes (3 examples):
1. **Symptom: "MQLs are down."** Symptom-treatment: launch a new lead-gen campaign. Cause: a tracking pixel broke 3 weeks ago. Real fix: reinstall pixel, no new campaign needed.
2. **Symptom: "Paid social ROI is down."** Symptom-treatment: cut the entire paid social budget. Cause: one of three campaigns (Reels) has a creative-fatigue issue, the other two are healthy. Real fix: refresh Reels creative, do not cut Stories or Feed.
3. **Symptom: "Email conversion is down."** Symptom-treatment: rewrite subject lines. Cause: the post-click landing page changed and broke mobile checkout 8 days ago. Real fix: roll back landing-page change.

### Common patterns to watch for
- **Channel-average masking**: aggregate looks fine, one sub-channel is on fire.
- **Segment-mix shift**: ICP shifted underneath you (e.g., enterprise share dropped, SMB grew, blended numbers changed).
- **Attribution model drift**: a measurement change altered the apparent performance without anything changing in reality.
- **Competitor action**: bid wars, copycat creative, announcement timing.
- **Seasonality / macro**: same period last year may show the same pattern.

---

## Section 7 — KPI Hygiene Checklist

Run this checklist quarterly (and before any board prep).

### Orphan metrics (no objective)
A metric on the dashboard with no traceable strategic objective. Either:
- assign it to an existing objective, OR
- delete it.

Don't keep it "because it's interesting." Interesting != strategic.

### Stale metrics (no longer relevant)
A metric that was strategic 18 months ago but no longer maps to current business priorities. Common after a strategy pivot, a re-org, or a market shift. Audit quarterly.

### Vanity metrics (not actionable)
A metric that goes up or down but the team has no specific corrective lever. NPS in isolation, brand health in isolation, follower count, share of voice without sentiment. Either pair with an actionable companion metric or remove from the board scorecard (keep on internal dashboards if directionally useful).

### Duplicate metrics (measuring same thing twice)
Two metrics that move together, measure the same underlying phenomenon, and confuse the readout. Example: "Marketing-sourced pipeline" + "MQL volume * average deal size" — pick one. Duplicate metrics burn board attention.

---

## Quick reference — when to use which mode

| Need | Mode | Script |
|---|---|---|
| Build scorecard from raw metrics | BUILD | `scripts/build_scorecard.py` |
| Check if a single metric belongs on the scorecard | VALIDATE | `scripts/validate_kpi.py` |
| Diagnose a red-zone metric | DIAGNOSE | `scripts/diagnose_red_zone.py` |
| 1-page board format | template | `templates/board-scorecard.md` |
| Recurring weekly review | template | `templates/weekly-kpi-review.md` |
