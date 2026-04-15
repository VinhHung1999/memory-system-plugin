# Diagnostic Playbook: What to Do When a Metric is Below Benchmark

## Open rate below benchmark

**Root causes (in order of likelihood):**
1. Subject line weak
2. From-name not recognized
3. Deliverability issue (landing in spam)
4. List quality poor (dormant/bought list)

**Diagnostic steps:**
1. A/B test 3 subject lines (clarity, personalization, curiosity)
2. Check from-name matches brand
3. Run mail-tester.com score — should be 8+/10
4. Verify SPF/DKIM/DMARC pass
5. Sunset subscribers who haven't opened in 180 days

## CTOR below benchmark

**Root causes:**
1. Body doesn't deliver on subject line promise
2. Too many CTAs (reader paralyzed)
3. Copy too long
4. Mobile render broken

**Diagnostic steps:**
1. Does subject promise match body intro? (rewrite if gap)
2. Count CTAs — should be 1 primary + max 2 secondary
3. Test mobile render in Litmus or Email on Acid
4. Measure body length — <300 words for promos, <600 for newsletters

## CTR below benchmark (but CTOR OK)

This means subject is weak (low opens cap clicks). Focus on open rate first.

## Conversion rate below benchmark

**Root causes:**
1. Landing page mismatch
2. Checkout friction
3. Offer weak
4. Wrong audience (segmentation problem)

**Diagnostic steps:**
1. Does landing page headline match email CTA? (rewrite if gap)
2. Count form fields — <5 ideal
3. Test offer variations (% off, $ off, free shipping, bundle)
4. Check segment size + match — small tight segment > big broad one

## Unsub rate above benchmark

**Root causes:**
1. Cadence too high
2. Content irrelevant to segment
3. Promotional heaviness

**Diagnostic steps:**
1. Audit send frequency — <2/week for e-comm, <4/week for media
2. Survey unsubscribers (1 question: "what didn't work?")
3. Check ratio of promo vs value content — 1 promo per 3-4 value emails

## Complaint rate above benchmark

**THIS IS SERIOUS.** >0.1% triggers ESP warnings, >0.3% triggers blocking.

**Root causes:**
1. Permission issue — bought list, scraped list, pre-ticked opt-in
2. Misleading subject line (clickbait)
3. Hard to unsubscribe

**Immediate actions:**
1. Pause all sends
2. Audit opt-in flow — require double opt-in going forward
3. Verify unsubscribe link works + honored within 10 days
4. Suppress anyone who complained (never email again)
5. Warm up sender reputation (send to most-engaged only for 2 weeks)

## Bounce rate above benchmark

**Hard bounces >0.5%:**
- Immediate list purge — remove hard bounces permanently
- Audit signup flow — use email validation (Kickbox, NeverBounce) before adding to list
- If bought list, the list is the problem

**Soft bounces >3%:**
- Temporary — usually resolves
- Investigate if persists: ESP IP blocked? Receiver (Gmail/Outlook) throttling?

## ROI below 42:1

**This is a strategic metric, not a send-level one.** Root causes span the whole program:
- Lead quality (acquisition channel)
- Conversion rate (landing page + offer)
- AOV (pricing + cross-sell)
- Retention (CLV ceiling)

**Diagnostic:** run full funnel audit — where's the biggest leak? Often the email is fine; the problem is upstream (bad list) or downstream (bad offer).

## Everything above benchmark

Congrats. Now consider:
- Increase send frequency modestly (+1 send/week, watch unsub rate)
- Scale acquisition (invest more in top lead source)
- Test new formats (video, interactive, personalization depth)
- Document what's working for team knowledge
