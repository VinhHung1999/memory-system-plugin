# Google Ads Experiments — Step-by-Step

From Course 5 Module 3 m3_04 "Perform A/B tests in Google Ads".

## Setup flow

1. **Navigate**: Google Ads → left rail → **Campaigns** → **All campaigns** → scroll down to **Experiments** tab
2. **Click "+"** to create a new experiment
3. **Name the experiment** — descriptive: "2026-05 Shorter-headlines test"
4. **Choose scope**:
   - All campaigns in account
   - Specific campaigns (recommended for focused tests)
5. **Pick edit type**:
   - **Headlines** — test different headline copy
   - **Final URL** — test different landing pages
   - **Call to action** (CTA) — test different CTA text
   - **Ad copy variations** — broader ad experimentation
6. **Set variant** — make ONE change (e.g., new headline for variant B)
7. **Choose split** — default 50/50 is the correct choice
8. **Set duration**:
   - Start date: immediately or scheduled
   - End date: based on sample size calculation
   - Minimum recommended: 2 weeks (catches day-of-week effects)
   - Maximum: 4 weeks (novelty effect dampens; keep runs short)

## During the experiment

- Monitor for **Sample Ratio Mismatch (SRM)**: if split drifts away from 50/50 by >2%, something is technically broken — investigate tracking.
- **Don't peek daily**. Decide duration upfront, check at midpoint + end only.
- **Don't make other campaign changes** (bid changes, ad copy edits) during the experiment — confounds results.

## After: reading the results

Google Ads Experiments dashboard shows:
- **CTR** per variant
- **Conversion rate** per variant
- **CPC / CPA**
- **Conversions** absolute count
- **Statistical significance flag** (Google's built-in — their threshold is typically 95%)

Cross-check Google's significance flag with your own calculation (`ab_significance.py`) because:
- Google may use different stat tests
- Google shows significance on a per-metric basis, not per-business-outcome

## Experimentation strategy

**What to test first** (highest impact, in order):
1. **Headlines** — biggest CTR lever, easiest to test
2. **Landing page** — biggest conversion rate lever
3. **CTA text** — moderate CTR + conversion impact
4. **Call extensions / sitelinks** — incremental click volume
5. **Display images** (for Display campaigns)
6. **Keywords** — test match types (broad vs phrase)
7. **Bidding strategy** — Manual CPC vs Target CPA vs Target ROAS

**Don't test**:
- Minor copy tweaks ("Buy now" vs "Shop now") unless you have huge volume
- Multiple things at once — can't attribute
- Things you can change unilaterally without evidence

## Common Google Ads Experiment types

### Responsive Search Ads (RSA) variation
Google mixes headlines/descriptions automatically. Better than classic A/B for most cases. Use experiment to test a different mix strategy or disable certain combinations.

### Campaign Drafts
For larger structural changes (new bid strategy, new keyword set), create a draft of the campaign, apply the experiment → run at split traffic → promote if wins.

### Video ad A/B (YouTube campaigns)
Test different opening hooks (first 5 seconds). Skip rate drops massively if opening is wrong.

## When Google Ads Experiments aren't enough

- Testing things OUTSIDE Google Ads (landing page changes) → use Google Optimize (deprecated 2023) or GA4 + third-party tool (Optimizely, VWO, Google Analytics 4 experiments)
- Testing email subject lines → use ESP's built-in A/B feature (Mailchimp, HubSpot)
- Testing app onboarding → Firebase A/B Testing

For all these, the same stat framework applies — only the setup tool changes.
