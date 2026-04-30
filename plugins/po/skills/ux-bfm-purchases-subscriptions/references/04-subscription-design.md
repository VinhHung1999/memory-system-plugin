# Subscription Model Design

## Core Principle
Subscription conversion fails when the user cannot answer two questions: "What am I getting?" and "What happens if I stop?" The best subscription funnels address both before asking for payment. Free trials work when: (1) the trial delivers real value the user can feel, (2) the charge date is pre-announced with enough time to decide, and (3) the downgrade/cancel path is visible and low-friction. Subscription design that obscures any of these creates short-term conversion but long-term distrust and cancellation.

## Diagnostic Questions
- Does the subscription page show personal ROI ("you'll save £14 on this order") or feature lists ("unlimited access")?
- Is the trial end date and charge amount shown at the moment of trial signup — not just in an email?
- How many clicks does it take to cancel? (Benchmark: should match signup steps)
- Is there a pause or downgrade option, or only a binary subscribe/cancel choice?

## Design Checklist
- Show the specific personal value the subscription delivers — not a generic feature list
- If a trial is offered, show the exact charge date and amount at the moment of signup (not buried in terms)
- Send a reminder notification 2-3 days before the trial ends — proactively, not reactively
- Cancel flow should be no more complex than signup flow
- Offer pause/downgrade before the hard cancel option
- Plan comparison should highlight what the user loses by choosing the lower tier — not just what they gain by upgrading

## Anti-Pattern
**What goes wrong:** Subscription page lists 8 features. User signs up for trial, forgets, gets charged. Contacts support to cancel. Support is hard to reach. User does a chargeback. Brand gets a fraudulent transaction dispute. Trust destroyed, subscriber lost, payment processor relationship damaged.
**Why it happens:** Conversion team optimises trial signup rate. They remove friction (including the friction that would have filtered out uncommitted users). The downstream effects (involuntary churn, support load, chargebacks) belong to a different team.
**BFM Example (Hellofresh):** Subscription meal kit model — the trial converts users who experience the product, but retention depends on managing the "too many boxes" and "I'm going on holiday" moments. Offering a pause option at the moment the user tries to cancel is worth more than any win-back campaign.

## BFM Evidence

### Netflix — tier structure shapes subscription perception
> "When there's only three options, most of the prices are above £10 per month. And so it doesn't feel unreasonable to spend above £10 on Netflix."
> "It cannibalised the more expensive tiers. i.e., whilst the basic plan grew in popularity... something about the value proposition had made the premium plans less popular."

The lesson: subscription tier design is not just about price — it's about what each tier makes the others feel like. Adding a cheap tier can make the mid-tier feel inadequate.

### Strava — transparent trial timeline as conversion AND retention
> "Today: Unlock subscription features. 2 Days before: Get a reminder about when your trial will end. In 30 days: You'll be charged the subscription amount. Cancel at least 24 hours before."

This timeline serves two purposes: it reduces post-trial chargeback risk (user can't claim surprise) and it builds trust with users who are on the fence (they feel in control). Transparent trials convert better long-term because they self-select committed users.

### Audible — subscription pricing confusion at point of purchase
> "CURRENT MEMBERSHIP: Premium Plus — £4.99/mo for 3 months then £9.99/mo after. ✓ 1 credit a month."
> "Buy 1 Credit / £9.99 | Buy 3 Credits / £23.99 | Buy 5 Credits / £32.99"

The subscription creates confusion at the purchase moment: the user is a subscriber but cannot easily understand how much more credits cost, when their included credit arrives, or whether it's better to buy now or wait. The subscription model is not simplified at the point of use.

### WSJ (intro) — subscription plan confusion as a named failure
> "Three pain points in subscription journalism UX — confusing plans, introductory rates that jump 1000% after 3 months, and cancellation nightmares."
> "Why does it take more clicks to subscribe to the WSJ than to open a bank account?"

The pattern: subscription complexity that makes the user feel trapped — even before they've committed. If cancellation is perceived as hard before signup, conversion drops. If it's actually hard after signup, churn spikes at the charge renewal date.

## What Good Looks Like
A subscription signup that takes 60 seconds, shows the exact charge date, delivers real value in the trial, sends a clear reminder before charging, and makes cancellation a single screen with a pause option. The user who cancels after 3 months is less valuable than the user who pauses and comes back — and they cost the same to acquire.

## Red Flags
- [ ] Subscription page shows feature list, not personal ROI specific to the user's situation
- [ ] Trial end date not shown at the moment of signup
- [ ] No reminder notification 2-3 days before trial ends
- [ ] Cancel path requires more steps than signup
- [ ] No pause or downgrade option — only binary subscribe/cancel
- [ ] Introductory price resets without 14+ days advance notice
