# Diagnostic Playbook — What to do when a metric is 🔴

## Low conversion rate (<1%)

**Root causes in order of likelihood:**
1. Landing page mismatch — ad/campaign promises X, page delivers Y
2. Too much checkout friction (form fields, account creation)
3. Wrong audience — traffic is coming but not ICP
4. Offer is weak

**Diagnostic steps:**
1. Load the primary landing page yourself — does it match what the ad/campaign says?
2. Audit checkout flow on mobile — count fields, time it
3. Run traffic source breakdown — is low conv from one channel dragging average down?
4. Check top-bounce pages — is there a specific page causing the drop?

## High bounce rate (>60%)

**Root causes:**
1. Page takes too long to load (>3s)
2. Mobile UX broken
3. Misleading ad or meta description → visitor thought they'd find X, found Y
4. Blog/content page (bounce rate is naturally high; not always a problem)

**Diagnostic steps:**
1. Run PageSpeed Insights on top-bounce pages
2. Test mobile rendering in Chrome DevTools mobile emulator
3. Cross-reference top-bounce pages with top paid-traffic landing pages
4. Segment: is bounce rate high across all pages, or concentrated?

## Low ROAS (<2:1)

**Root causes:**
1. Bidding too high — paying more than customers are worth
2. Audience targeting too broad — hitting non-buyers
3. Attribution bug — conversions happening but not credited to Ads
4. Wrong conversion event — tracking "view page" instead of "purchase"

**Diagnostic steps:**
1. In Ads: break down ROAS by campaign → kill bottom 20%
2. Check audience segments — negative keyword list, audience exclusions
3. Verify conversion tracking is firing correctly (Google Tag Assistant)
4. Compare GA4-reported revenue to Ads-reported revenue — mismatch = attribution issue

## High CPA (up from baseline)

**Root causes:**
1. Competition increased (auction pressure)
2. Quality Score dropped (ad relevance issue)
3. Conversion rate dropped → denominator shrinking
4. Keyword bid creep

**Diagnostic steps:**
1. Check Quality Score per keyword in Ads (Quality Score column)
2. Review search terms report → irrelevant terms to add as negatives
3. Seasonality check — are competitors bidding higher right now?
4. A/B test new ad creative → often refreshes Quality Score

## Low CTR on ads (<1% for Search, <0.3% for Display)

**Root causes:**
1. Ad copy generic
2. Keyword-to-ad match weak
3. Ad extensions missing (sitelinks, callouts)
4. Wrong match types → targeting irrelevant searches

**Diagnostic steps:**
1. Run search terms report → audit match relevance
2. Add sitelinks + callout extensions
3. Include target keyword in headline 1
4. Use Responsive Search Ads with 15 headline variants for Google to pick best

## Traffic dropping month-over-month

**Root causes:**
1. SEO issue — ranking dropped
2. Ad budget cut / paused
3. Seasonality (check previous year)
4. Technical issue (site down, tracking broken)

**Diagnostic steps:**
1. Check Search Console for impression/position drops
2. Verify tracking still firing (GA real-time)
3. Check for manual actions (Search Console → Security & Manual Actions)
4. Look at previous year — is this seasonal?

## No organic traffic growth

**Root causes:**
1. Content not indexed
2. No internal linking
3. Weak on-page SEO
4. Low-authority domain (needs backlinks)

**Diagnostic steps:**
1. Check Search Console Coverage → how many pages indexed?
2. Run `seo-onpage-checklist` on top pages
3. Audit site structure — are pages <4 clicks from home?
4. Review backlink profile (Ahrefs, SEMrush free tiers)

## High paid spend with low revenue

**Root causes:**
1. Wrong KPIs (optimizing for clicks not conversions)
2. Budget allocated to wrong campaigns
3. Tracking broken (conversions not reporting back to Ads)

**Diagnostic steps:**
1. Verify conversion tracking in Ads (View conversions column per keyword)
2. Campaign-level ROAS breakdown → kill bottom performers
3. Use Target ROAS or Target CPA smart bidding instead of Manual CPC

## Great blended metrics but specific campaign tanks

Aggregate looks fine; one big loser hides in the average. Always segment by:
- Campaign
- Ad group
- Device
- Day of week (weekend vs weekday)
- Audience segment

The weakest segment often has outsized impact if it's the highest spend.

## When to stop optimizing and invest more

- All channels at 🟢
- ROAS >5:1 for 3+ months
- CPA stable or dropping
- Conv rate steady

At this point: scale. Increase budget by +20% per month while monitoring. Spending too little is leaving revenue on the table.
