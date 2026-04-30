# Product Type Patterns

Different product types have structurally different onboarding challenges. Load this file first when the product type is known — it narrows which of the 10 categories to prioritise.

---

## B2C Consumer Apps (fitness, meditation, habit, entertainment)

**BFM examples:** Headspace, Strava, Duolingo-type

**Dominant challenges:**
- Time-to-value must be seconds, not minutes — user will abandon before the "tutorial" ends
- Goal ownership is critical — pre-selected goals kill retention (Strava: 84% 30-day churn)
- Habit formation requires visible streak/progress mechanics (Goal Gradient Effect)
- Paywall placement must come AFTER the user has experienced creative range

**Priority categories:** 1 (Aha! Moment), 2 (Goal-Setting), 9 (Intent-Based)

**Key pattern:** Give the user the core experience first, sign-up second. Headspace runs a breathing exercise before asking for an account.

**Watch for:** Labels on goal levels ("Casual / Serious / Intense"), pre-selected "recommended" goals, paywall appearing before user has explored what they'd be paying for.

---

## B2B / SaaS Tools (project management, communication, CRM, finance)

**BFM examples:** Trello, Slack, LinkedIn, YNAB

**Dominant challenges:**
- High setup investment required before any value — user must commit time before seeing ROI
- Setup noise is the #1 churn driver (LinkedIn: notifications, prompts, redirects all firing at once)
- Templates must serve the One Thing — not showcase breadth
- Time-to-value is inherently longer; reducing noise buys time

**Priority categories:** 3 (Noise), 6 (One Thing), 5 (Progressive Disclosure)

**Key pattern:** Identify the earliest moment of real value (first board created, first message sent, first budget category filled) and remove everything that doesn't lead directly there.

**Watch for:** Starter templates mixing instruction cards + upsell cards + fake data. Multiple onboarding triggers firing before user completes first core action. Org-structure decisions forced too early (Slack workspace naming).

---

## Finance / Banking / Fintech

**BFM examples:** Chase, Wise, YNAB, Revolut

**Dominant challenges:**
- Trust must be established before any commitment is requested
- Transparency is a competitive differentiator (Wise: show competitor fees, show exact transfer time)
- Dynamic sign-up: detect intent (transfer money vs explore features) and strip friction accordingly
- Celebrations must align with real user goals — opening an account is an obstacle, not an achievement

**Priority categories:** 10 (Transparency), 4 (Celebration), 1 (Aha! Moment)

**Key pattern:** Wise detects that user wants to make a transfer → skips account-setup steps → delivers the transfer → sign-up feels like saving progress, not a gate.

**Watch for:** Celebrating "account opened!" when user wanted to make a payment. Long verification flows before demonstrating any value. Radical transparency opportunities missed (fees, speed, safety).

---

## Loyalty / Rewards / Engagement

**BFM examples:** Costa, Strava

**Dominant challenges:**
- Goal Gradient Effect must be designed deliberately — artificial early progress is legitimate
- Progress visibility is mandatory — empty state ("no rewards yet") destroys motivation
- Flywheel restart after redemption is almost always missed
- Goal labels create identity pressure that backfires when users fail to hit them

**Priority categories:** 2 (Goal-Setting), 4 (Celebration), 1 (Aha! Moment)

**Key pattern:** Give 2 free stamps on day 1 on a 10-stamp card. User is instantly 20% of the way there — Goal Gradient kicks in immediately.

**Watch for:** Showing an empty progress state after redemption. Labeling tiers as identities ("Casual / Serious"). No celebration at the point of earning a reward (only at redemption).

---

## AI Tools / Creative Features

**BFM examples:** Grok

**Dominant challenges:**
- AI interfaces converge → unique capabilities hidden behind identical input fields
- Users need to understand the RANGE of what's possible, not just that it exists
- One use of a feature ≠ understanding — user may have tested it wrong
- Paywalls placed before exploration kill experimentation

**Priority categories:** 8 (AI Onboarding), 1 (Aha! Moment), 9 (Intent-Based)

**Key pattern:** Before the paywall, show the user 3-5 imaginative use cases they haven't thought of. The upsell works when users are excited about ideas they want to try, not when they're rationing their remaining free uses.

**Watch for:** Paywall appearing before user has discovered the feature's creative range. Onboarding stops after the first use. "Pointing and showing" a feature without demonstrating what it can do that the user couldn't do before.

---

## Marketplaces / Two-Sided Platforms

**BFM examples:** (not directly in BFM studies, but principles apply)

**Dominant challenges:**
- Must show supply before asking for demand-side commitment
- Trust gap: new user doesn't know if the platform has what they need
- Sign-up before browsing → high abandon rate

**Priority categories:** 1 (Aha! Moment), 6 (One Thing), 10 (Transparency)

**Key pattern:** The One Thing for a marketplace is not "complete a transaction" — it's "believe that this platform has what I'm looking for." Show the catalogue breadth before asking for account creation.

**Watch for:** Account gate before browsing. Generic "1000s of products" copy vs specific relevant examples. Trust signals missing from the first screen.

---

## Diagnostic: Which type applies?

| Signal | Product Type |
|--------|-------------|
| Core value is habit/routine | B2C Consumer |
| Requires team or workspace setup | B2B SaaS |
| Involves money, verification, trust | Finance/Fintech |
| Has points, streaks, or rewards | Loyalty |
| Has a text input that "does everything" | AI Tool |
| Has buyers and sellers | Marketplace |
