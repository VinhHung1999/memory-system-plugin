# Transparency & Trust

## Core Principle
Radical transparency — including showing competitor pricing, exact fees, and precise delivery times — is a competitive moat, not a risk. When a product is genuinely better, transparency accelerates trust faster than any marketing claim. Trust built during onboarding compounds: users who trust the product at sign-up are more likely to complete verification, share data, and upgrade.

## Diagnostic Questions
- Is there any information the product withholds during onboarding that, if shown, would increase the user's confidence?
- Does the confirmation or completion message reinforce the specific benefit the user just received, in concrete terms?
- Does the product show competitor pricing or alternatives when it would be to the user's genuine benefit to see them?

## Design Checklist
- Show exact costs, fees, and delivery times before the user commits — not after. Hiding them until checkout creates distrust at the worst possible moment.
- After a key action (first transfer, first booking, first run), send a follow-up message that quantifies the specific value received ("Your transfer arrived in 14 seconds — 3 days faster than a bank transfer").
- When the product is genuinely better than alternatives, show the comparison. Competitors who are afraid to do this signal that they know they are not the best choice.
- Use animated icons and product personality to build emotional connection during low-stakes moments in onboarding — this has brand value independent of direct conversion.
- Detect user intent from sign-up context (referral source, URL parameters, stated purpose) and optimise the entire flow for that intent.

## Anti-Pattern
**What goes wrong:** The product hides fees, limitations, or comparison data until after the user has committed, creating a moment of distrust at the point of confirmation.
**Why it happens:** Teams believe that showing negative information (fees, limitations, competitor prices) will reduce conversion. In transparent markets, the opposite is often true.
**BFM Example:** Slack — during onboarding, subscription pricing is shown per seat without any estimate of the total bill. "During onboarding the plans are framed per seat, without an estimation of the total bill." A shareable invite link can be sent to 400 people, which could create a surprise bill of $8,137.50. The transparency is absent at precisely the moment it would save the user from a costly mistake.

## BFM Evidence

### Wise — radical transparency as a brand position
> "Wise's transparent fee structure reveals hidden fees from competitors — radical transparency in pricing."

### Wise — transparency at the point of decision
> "Real-time fee calculation shows transparency at the point of decision."

### Wise — two-path sign-up based on detected intent
> "Two-tier onboarding: quick transfer OR full account with more features." (detecting whether the user wants to send money now or set up a full account)

### Wise — transparency about delivery timing reinforces post-action value
> "Clear expectations about timing support radical transparency." (transfer status showing estimated delivery time)

### Slack — hiding pricing information that affects commitment decisions
> "During onboarding the plans are framed per seat, without an estimation of the total bill. A link can be shared with up to 400 people. Due today $US8,137.50."

### Strava — opacity about what premium features actually do
> "At times not even explaining what a paywalled feature even does."

## What Good Looks Like
Wise shows a line-by-line fee breakdown before the user enters their card details. It labels the exchange rate as "the real rate" and shows what competitors charge for the same transfer. After the transfer completes, the confirmation email shows the exact delivery speed. The user who might have compared alternatives is now a committed customer — because Wise showed them the comparison first and won it transparently.

## Red Flags
- [ ] Fees, limits, or subscription costs are revealed only after the user has committed to an action (entered card details, invited colleagues, submitted a form).
- [ ] The post-action confirmation message says "success" but does not quantify the specific benefit the user received in concrete terms.
- [ ] The product has a genuine advantage over competitors (speed, price, features) that is not shown to users during onboarding or at the decision point.
- [ ] Subscription pricing is shown per-unit (per seat, per transfer) without any estimate of the realistic total cost to the user.
- [ ] The product detects user intent (from referral, URL, or stated purpose) but does not use that signal to customise the sign-up flow.
