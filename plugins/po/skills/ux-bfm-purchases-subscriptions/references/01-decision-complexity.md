# Decision Complexity at Checkout

## Core Principle
A purchase decision is a moment of maximum cognitive load. The user must evaluate price, compare options, recall their budget, and commit to a financial action — all simultaneously. Every additional option, every hidden piece of information, every click required to compare choices adds to this load and increases abandonment probability. The goal is to reduce the decision to its simplest possible form at the moment of payment.

## Diagnostic Questions
- How many payment options does the user face at the point of purchase?
- Is the information needed to make a decision (credit renew date, price per unit, delivery cost) visible without clicking to another screen?
- Does the user have to mentally calculate or compare prices across screens to make a decision?
- What is the mobile abandonment rate vs desktop? (Higher mobile = checkout friction)

## Design Checklist
- Present one recommended payment path — not three equal options
- All information needed to choose (credit cost, wait time, book price) must be visible on the same screen
- Avoid requiring users to navigate to another screen to find critical information, then return
- On mobile: one primary action per screen, address auto-complete, minimal required fields
- If multiple payment methods exist, use progressive disclosure: show the default, reveal alternatives on tap

## Anti-Pattern
**What goes wrong:** Product adds more payment flexibility (credits, bulk credits, direct purchase, discount) without restructuring how these options are presented. The user must work out the math themselves — across multiple modals — before they can make a confident decision.
**Why it happens:** Each payment option was added separately to serve a segment. Nobody redesigned the decision architecture after adding the third option.
**BFM Example (Audible):** At the point of purchase, users face three simultaneous payment paths: wait for credit renewal (but the date is hidden in a different modal), buy extra credits (but the per-unit cost requires mental math across screens), or buy the book directly. None of the information needed to compare these options appears on the same screen.

## BFM Evidence

### Audible — critical information hidden behind a click
> "Nowhere on this step can you see when your credits renew. Instead, it's hidden in here... along with the actual cost of a credit."

> "So, whilst trying to weigh up the options, you need to click... to learn that it's £9.99 for 1."

### Audible — price comparison forced across screens
> "But then you can't compare it directly to the price of actually buying the book, because that's on the previous step."

> "You probably need to work out roughly how many days [until renewal] is. (i.e., are you prepared to wait)."

### Audible — three options, none clearly recommended
The options are:
- Wait for credit (date unknown without clicking away)
- Buy more credits (price unknown without clicking away)
- Buy direct for £7.99 (visible)

The result: a motivated user still has to make 2 extra clicks and mental calculations before they can confidently pick any option.

### Delta (intro) — mobile abandonment is the headline metric
> "91% of mobile users abandon their cart when booking flights (vs. 65–75% eCommerce average)."

> "These lousy mobile experiences are a big part of the problem."

The mobile purchase decision is harder than desktop because screen space forces sequential information — what the user needs to compare is never visible simultaneously.

### Flights Ch.3 — too many choices causes paralysis
> "The Paradox of Choice — Too many similar options causes decision paralysis."

When flight results show 20+ similar options with marginal price differences, users freeze. The fix is not more information — it is curation: surface 3 options with clear differentiation (cheapest, fastest, best value).

## What Good Looks Like
A single checkout screen where the user sees: the item, the price, their available credits/balance, the alternative price, and a single recommended CTA — without leaving the screen. Like a well-designed confirmation dialog: all the information you need to say yes or no, in one place.

## Red Flags
- [ ] User must click to another screen to get information needed to make the current decision
- [ ] Three or more payment options with no recommended path
- [ ] Mobile cart abandonment rate is >20% higher than desktop
- [ ] Credit balance, renewal date, or discount percentage not shown on the purchase screen
- [ ] User must perform mental arithmetic to compare options
