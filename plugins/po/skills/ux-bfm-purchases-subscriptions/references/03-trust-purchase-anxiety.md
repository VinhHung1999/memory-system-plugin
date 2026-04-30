# Trust & Purchase Anxiety

## Core Principle
Purchase anxiety peaks at the payment step — the moment when the user must hand over money for something they haven't yet received. This anxiety is amplified by: unfamiliar brands, inconsistent product information, unclear return policies, and absence of social proof. Reducing this anxiety is not about reassurance copy ("safe and secure!") — it is about removing the specific uncertainty the user has at that moment. The right trust signal addresses the specific fear.

## Diagnostic Questions
- What specific fear does the user have at the payment step? (Will it fit? Is this legit? Can I return it? Will it arrive?)
- Is the return policy visible without leaving the checkout flow?
- Is the price shown on the product page the same as the price shown at checkout?
- Does the product information (size, colour, spec) stay consistent across the purchase journey?

## Design Checklist
- Show return/refund policy at the checkout step — not just on a separate "Returns" page
- Security indicators (padlock, payment logos, verification badges) should appear at the payment entry step
- Reviews and ratings relevant to the specific product should be visible before the purchase — not only on the product page
- Product information (price, description, size options) must be consistent across search, product page, and checkout
- Order summary at checkout should show exactly what was selected — with images — so the user can confirm before paying

## Anti-Pattern
**What goes wrong:** Trust signals (reviews, return policy, security badges) are present somewhere on the site — but not at the checkout step. The user reaches payment, their anxiety peaks, and they can't see the reassurance they need without abandoning the checkout to go look for it.
**Why it happens:** Trust signals are added to the product page and marketing, but the checkout is treated as a "conversion funnel" — stripped of everything except the payment form to reduce "distractions." This removes exactly the signals users need most at that moment.
**BFM Example (Zara):** Navigation reorganises every few hours (causing users to get lost), prices drift across search results and product pages, and the low-contrast video background makes key information unreadable. By the time a motivated user reaches checkout, their confidence in the product and brand has already been eroded by inconsistency.

## BFM Evidence

### Zara — inconsistency creates anxiety before checkout
> "Navigation reorganizes every few hours — user gets lost."
> "Prices drift in search results — shows different values."
> "Product information inconsistencies across pages."

The trust failure starts before checkout. A user who sees different prices for the same item across two pages cannot trust the final checkout total.

### Zara — Airbnb as the trust benchmark
> "Split view comparing Zara and Airbnb checkout experiences. Airbnb's approach to building trust and reducing anxiety."
> "Multiple verification steps increase confidence."
> "Host profile with reviews and ratings | Verified badge | Response rate shown — Social proof reduces purchase anxiety."

Airbnb's model: the buyer has more information about what they're buying than Zara provides for a £50 dress. Photo gallery, host reviews, verified status, response rate — all visible before payment.

### Zara — specific trust mechanics that reduce anxiety
> "Saved items reduce purchase friction." (Wishlist)
> "Real-time [order tracking] updates reduce purchase anxiety."
> "Clear policy information increases purchase confidence." (Returns)
> "Security indicators build trust." (Padlock, payment logos)

The lesson: trust is not one thing — it's a stack of specific signals, each addressing a different fear. The user asking "will this fit?" needs the size guide. The user asking "can I return it?" needs the returns policy. Neither is helped by a generic "Shop with confidence" badge.

### WSJ (intro) — subscription trust failure
> "I support paying for journalism, but why does the experience have to be so uncomfortable?"

Trust at the subscription paywall is a distinct form of anxiety: the user is committing to a recurring charge, not a one-time purchase. The comfort they need is: "I know exactly what I'm paying, when it starts, how much it will be in 3 months, and how easy it is to cancel." WSJ's pattern — confusing plans, 1000% price jump after intro, cancellation nightmares — destroys trust at every point.

## What Good Looks Like
A checkout where the user can answer "yes" to all of these without leaving the page:
- Is this the right item/size/colour? (order summary with image)
- What will this cost, total? (fully-loaded price)
- Can I return it if it doesn't work? (return policy visible)
- Is this payment secure? (security indicators)
- Have other people bought this and been happy? (reviews)

## Red Flags
- [ ] Return/refund policy is only on a dedicated "Returns" page, not visible in checkout
- [ ] Price shown in search differs from price shown in checkout (even by delivery costs)
- [ ] Product page has no reviews, or reviews are not product-specific
- [ ] Security indicators absent from the payment form step
- [ ] Navigation or product information has changed between sessions (consistency failure)
