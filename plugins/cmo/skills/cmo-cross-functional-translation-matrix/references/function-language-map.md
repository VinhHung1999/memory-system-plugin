# Function Language Map

A per-function reference for translating marketing insights into the KPIs, vocabulary, evidence, and asks each non-marketing executive actually responds to. Used by `scripts/translate_insight.py` and as a credibility check before any cross-functional presentation.

Sources: Coursera CMO Excellence (Hurix Digital, Dec 2025) Modules 2 & 3; McKinsey research on CMO-CEO-CFO alignment; HBR "The CMO and the Future of Marketing" framings.

---

## Finance

The CFO's job is capital allocation under uncertainty. They reward marketers who speak in unit economics, payback, and risk-adjusted return — not impressions or sentiment.

- **KPIs they report on**:
  - CAC (customer acquisition cost, USD per new customer)
  - LTV / CAC ratio (target typically 3x or higher)
  - CAC payback period (months until a customer pays back acquisition cost; target under 18 months for SaaS)
  - Gross margin contribution (percent and absolute USD)
  - Marketing efficiency ratio (new ARR per dollar of marketing spend)
  - Free cash flow impact and burn multiple
  - Forecast accuracy variance (percent vs plan)

- **Language patterns**:
  - "What's the payback?"
  - "Show me the unit economics"
  - "What's the incremental contribution margin?"
  - "How does this move the forecast?"
  - "What's the downside case?"
  - "Cash conversion cycle"

- **Evidence types they trust**:
  - Cohort-level economics (new vs existing, by segment) with statistical confidence
  - Attribution models showing incremental lift, not last-touch
  - Benchmarks vs prior quarter and vs comparable public-company peers
  - Sensitivity analysis showing best/base/worst scenarios
  - Audited finance-system data (NetSuite, Salesforce ARR), not marketing-platform numbers

- **Common asks marketing makes of them**:
  - Incremental budget for a high-LTV segment
  - Reallocation from underperforming channel to a tested one
  - Permission to capitalize a marketing investment (long-term brand build)
  - Approval of a multi-year contract (martech, agency)
  - Hold spend flat while improving efficiency target

- **Common pitfalls**:
  - Leading with brand awareness or impressions instead of revenue impact
  - Citing vanity metrics (followers, MQLs without conversion data)
  - Asking for budget without a payback or break-even date
  - Bringing platform-reported attribution (e.g., Meta-attributed ROAS) without corroboration

---

## Product

The CPO/Head of Product cares about adoption, activation, and the product's ability to drive net revenue retention. Marketing wins their support when an insight unlocks a roadmap priority or de-risks a launch.

- **KPIs they report on**:
  - Activation rate (percent of signups reaching the aha moment within N days)
  - Weekly/Monthly Active Users (WAU/MAU) and DAU/MAU stickiness
  - Feature adoption rate (percent of eligible users using feature X)
  - Net Revenue Retention (NRR target typically 110-130 percent for SaaS)
  - Time-to-value (median days from signup to first business outcome)
  - Expansion revenue per account
  - Churn rate by cohort and feature usage

- **Language patterns**:
  - "What's the user job-to-be-done?"
  - "Where's the activation friction?"
  - "Is this a roadmap commitment or a discovery?"
  - "What's the expansion lever?"
  - "Build vs buy vs partner"
  - "Counter-positioning" / "wedge"

- **Evidence types they trust**:
  - Behavioral cohort data from product analytics (Amplitude, Mixpanel)
  - Qualitative user research with quotes and JTBD framings
  - A/B test results with sample size and lift confidence interval
  - Funnel analysis showing drop-off points
  - Competitive teardowns showing feature gaps tied to deals lost

- **Common asks marketing makes of them**:
  - A roadmap slot for a feature that drives a marketing-defined segment
  - Co-development of a product-led-growth (PLG) motion
  - Launch alignment for a specific GTM moment
  - Tighter activation flow for a high-CAC channel
  - Lifecycle messaging hooks (in-product triggers)

- **Common pitfalls**:
  - Bringing campaign performance instead of user behavior data
  - Asking for a "marketing feature" without a user JTBD
  - Skipping the activation/retention story and jumping to acquisition
  - Demanding roadmap slot without cohort evidence of product-market fit gap

---

## Operations

The COO owns the throughput, cost, and quality of the delivery system. They evaluate marketing through the lens of "can we serve the demand it creates without breaking SLAs or unit cost?"

- **KPIs they report on**:
  - Cost-to-serve per customer or per order
  - Throughput (units/day, tickets/agent, orders/hour)
  - SLA attainment (percent of orders/tickets meeting target)
  - On-time delivery rate
  - Inventory turns and DSO (days sales outstanding)
  - Capacity utilization (percent)
  - Defect rate or first-call resolution

- **Language patterns**:
  - "What's the demand signal?"
  - "Can we scale the supply side?"
  - "What's the unit cost impact?"
  - "Throughput bottleneck"
  - "Capacity plan"
  - "Run rate"

- **Evidence types they trust**:
  - Demand forecast with confidence intervals tied to a campaign curve
  - Time-and-motion studies or cycle-time analyses
  - Process maps showing handoff points and SLA risks
  - Vendor/supplier capacity confirmations
  - Historical demand spikes and their fulfillment outcomes

- **Common asks marketing makes of them**:
  - Co-plan a demand surge (Black Friday, product launch)
  - Adjust SLA tier for a high-LTV segment
  - Add a fulfillment node or partner before a campaign
  - Allow self-serve onboarding to reduce CS load
  - Share demand forecast 60-90 days out

- **Common pitfalls**:
  - Surprising Ops with a demand spike (no lead time)
  - Bringing creative concepts instead of volume forecasts
  - Ignoring the cost-to-serve impact of the targeted segment
  - Promising customers SLAs Ops never agreed to

---

## HR

The CHRO/Head of People cares about engagement, retention, capability, and employer brand. They support marketing when the insight clarifies talent needs, employer brand, or DEI signal.

- **KPIs they report on**:
  - Voluntary attrition rate (percent annualized)
  - Employee Net Promoter Score (eNPS)
  - Time-to-fill and quality-of-hire
  - Engagement survey scores (Glint, Culture Amp)
  - Internal mobility rate
  - Offer acceptance rate
  - Diversity representation at each level

- **Language patterns**:
  - "Talent density"
  - "Employer brand"
  - "Org design"
  - "Capability gap"
  - "Career path"
  - "Span of control"

- **Evidence types they trust**:
  - Engagement-survey verbatims and scores by team
  - Glassdoor/Comparably rating trends
  - Exit-interview themes (anonymized)
  - LinkedIn talent flow data (where hires come from / where leavers go)
  - External labor-market benchmarks (Mercer, Radford)

- **Common asks marketing makes of them**:
  - Co-build employer-brand campaign tied to recruiting funnel
  - Hire net-new marketing capability (e.g., growth, lifecycle)
  - Adjust comp band for hot marketing skill (data, AI, brand)
  - Internal communications support for a rebrand or repositioning
  - DEI alignment on supplier diversity / creator partnerships

- **Common pitfalls**:
  - Treating HR as posting agency instead of strategic talent partner
  - Asking for a hire without a capability gap diagnosis
  - Launching customer-facing brand before internal alignment
  - Ignoring HR data when claiming "culture" benefit of a campaign

---

## Sales

The CRO/Head of Sales lives quarter to quarter on pipeline coverage, conversion, and quota attainment. They listen to marketing when the insight materially moves a forecast number or unblocks a deal.

- **KPIs they report on**:
  - Pipeline coverage (target typically 3-4x quota)
  - Win rate by stage and segment
  - Average deal size (ACV / ASP)
  - Sales cycle length (days from MQL to closed-won)
  - Quota attainment (percent of reps hitting target)
  - Forecast accuracy (commit vs actual)
  - SQL-to-closed-won conversion rate

- **Language patterns**:
  - "Top of funnel" / "bottom of funnel"
  - "Pipeline gen"
  - "Air cover"
  - "Deal velocity"
  - "Commit / best case / pipeline"
  - "Whitespace" / "land and expand"

- **Evidence types they trust**:
  - SQL-to-closed-won conversion by source channel and segment
  - Deal-level win/loss interviews
  - Pipeline contribution by campaign with attribution model disclosed
  - Competitive intel sourced from real deals
  - Account-based scoring with intent signals (6sense, Bombora)

- **Common asks marketing makes of them**:
  - Co-prioritize an ABM target list
  - Adopt a new content asset / playbook in cadences
  - Adjust ICP definition based on win-rate data
  - Provide air cover for an enterprise deal (exec briefing, custom event)
  - Field reps to collect specific qualitative signals

- **Common pitfalls**:
  - Bringing MQL volume instead of pipeline dollars
  - Crediting marketing-touched deals without showing influence model
  - Recommending segment changes that invalidate quota plans mid-quarter
  - Ignoring rep behavior change required to operationalize the insight

---

## Legal

The General Counsel evaluates risk, regulatory exposure, and contractual liability. They support marketing when risks are surfaced early, in their language, with mitigation options — not when they're brought in as last-step approver.

- **KPIs they report on**:
  - Open regulatory matters and litigation count
  - Contract cycle time (days)
  - Privacy/data-subject request response time
  - Compliance-training completion rate
  - Vendor-risk-assessment throughput
  - Number of high-severity incidents per quarter

- **Language patterns**:
  - "Material risk"
  - "Defensible position"
  - "Privilege" / "work product"
  - "Indemnification" / "limitation of liability"
  - "Regulatory exposure"
  - "Reasonable basis" (FTC standard for claims)

- **Evidence types they trust**:
  - Documented consent flows and audit trail
  - Substantiation files for advertising claims (FTC reasonable-basis docs)
  - Data-flow maps showing where PII moves and is stored
  - Vendor contracts with DPA (data processing addendum) and SCCs
  - Regulator guidance citations (FTC, CCPA, GDPR, HIPAA, TCPA)

- **Common asks marketing makes of them**:
  - Pre-clear a campaign claim or testimonial format
  - Approve a new vendor / DPA review
  - Update privacy notice for a new data use
  - Define consent mechanism for a new geo (EU, California, Quebec)
  - Sign-off on influencer or affiliate disclosure language

- **Common pitfalls**:
  - Dropping a campaign on Legal 48 hours before launch
  - Asking "is this OK?" instead of presenting the risk and mitigation
  - Hiding edge cases (minors, healthcare data, EU residents)
  - Treating Legal as a blocker to route around — they remember

---

## IT

The CIO/CTO/Head of Engineering owns systems uptime, integration architecture, security posture, and engineering capacity. They evaluate marketing requests against system risk and engineering opportunity cost.

- **KPIs they report on**:
  - System uptime / availability (percent, e.g., 99.9)
  - Mean time to recovery (MTTR)
  - Change failure rate (DORA metric)
  - Security incidents per quarter
  - Engineering capacity utilization
  - Tech-debt ratio
  - API latency (p50/p95/p99 milliseconds)

- **Language patterns**:
  - "Single source of truth"
  - "API-first" / "event-driven"
  - "Tech stack rationalization"
  - "Identity and access management (IAM)"
  - "Data residency"
  - "Throughput / latency / availability"

- **Evidence types they trust**:
  - Architecture diagrams showing data flow and integration points
  - Vendor SOC 2 Type II reports and pen-test summaries
  - Load-test results and capacity projections
  - API documentation and rate-limit specs
  - Total cost of ownership (TCO) over 3-year horizon

- **Common asks marketing makes of them**:
  - Integrate a new martech tool (CDP, ESP, attribution platform)
  - Stand up a customer-data warehouse view
  - Provide engineering capacity for a marketing-site migration
  - Implement consent management or identity resolution
  - Expose an API for personalization at the edge

- **Common pitfalls**:
  - Buying SaaS without IT review (shadow IT)
  - Ignoring data-residency and security review timelines
  - Treating IT as ticket-takers instead of architecture partners
  - Underestimating integration cost and ongoing maintenance burden

---

## Customer Success

The CCO/Head of CS owns retention, expansion, and the experience post-sale. They support marketing when an insight reduces churn risk, surfaces expansion signal, or arms the CSM team with a better narrative.

- **KPIs they report on**:
  - Gross Revenue Retention (GRR) and Net Revenue Retention (NRR)
  - Logo churn rate (percent of accounts lost)
  - Expansion ARR per account (dollars and percent)
  - CSAT and NPS by segment
  - Time-to-value (TTV) and time-to-first-value (TTFV)
  - Health-score distribution (red/yellow/green percent)
  - QBR completion and adoption-plan attainment

- **Language patterns**:
  - "Health score"
  - "Expansion play"
  - "Churn risk signal"
  - "Renewal motion"
  - "Adoption plan"
  - "Voice of customer (VoC)"

- **Evidence types they trust**:
  - Health-score breakdowns by segment and lifecycle stage
  - Verbatim VoC feedback (interviews, surveys, ticket themes)
  - Cohort retention curves segmented by acquisition source
  - Renewal forecast tied to specific account-level signals
  - QBR notes and customer maturity assessments

- **Common asks marketing makes of them**:
  - Co-build a customer-advocacy program (references, case studies)
  - Identify expansion-ready accounts for an upsell campaign
  - Share VoC themes to inform messaging or roadmap
  - Coordinate a re-onboarding sequence for at-risk accounts
  - Align lifecycle-marketing triggers with CS playbooks

- **Common pitfalls**:
  - Treating CS as a content-source instead of a strategic partner
  - Launching upsell campaigns without CS coordination (annoys customers)
  - Ignoring health-score data when defining ideal customer profile
  - Promising customer outcomes the CS team can't operationally deliver
