# Pricing Architecture & Hidden Fees

## Core Principle
The moment a user sees a price higher than expected — at any point in the checkout — trust erodes and abandonment risk spikes. "Hidden fees" do not need to be dishonest to cause this effect: they only need to be unexpected. The best pricing architecture reveals the total cost progressively and honestly, anchoring the user's mental model at the right level before they reach the final checkout screen. The worst hides fees until the last step, forcing the user to make a new decision at the moment they thought they were done.

## Diagnostic Questions
- What is the price difference between the first price a user sees and the final checkout total?
- At what step do delivery, baggage, seat, or service fees appear?
- Does the user ever need to recalculate or reconsider their decision because of a late-appearing fee?
- Is the per-unit price (per credit, per night, per seat) shown at the point where the comparison is needed?

## Design Checklist
- Show the fully-loaded price (with typical fees) as early as the product/search page where possible
- If fees vary (e.g., baggage by weight), show the range or the minimum clearly — not just the base fare
- Use progressive fee disclosure: show base + most common add-on together, not separately in a late step
- Anchoring works for you if you anchor honestly: show the "without discount" price first, then the discount
- Never reveal a mandatory fee (mandatory booking fee, service charge) for the first time on the final payment screen

## Anti-Pattern
**What goes wrong:** Marketing shows the "from £29" base fare. At checkout: taxes £18, baggage £20, seat selection £10. User who budgeted £30 now faces £77. They abandon and feel deceived — even if every fee is legitimate.
**Why it happens:** Pricing teams optimise the "headline" metric (advertised fare) separately from the "checkout" experience. Nobody owns the gap between them.
**BFM Example (Flights Ch.3):** Airlines show a base fare of £39.99. At checkout, taxes/fees (+£18.50), baggage (+£20.00), and seat selection stack up to £78.49 — nearly double. The decoy/anchor price in search results creates an expectation the checkout cannot meet.

## BFM Evidence

### Flights Ch.3 — fees stack invisibly until checkout
> "Base fare £39.99 | Taxes/fees £18.50 | Baggage +£20.00 | Total £78.49"
> "These all add up to final price" — shown only at checkout, not in search results.

### Flights Ch.3 — "hidden fees" as a named UX failure pattern
> "Hidden Fees: Baggage +£20-40, Seat selection +£5-15, Meal +£5-12, Pet +£50-100"
> "Base fare doesn't include these extras."

### Flights Ch.3 — charm pricing creates false anchors
> "£19.99 vs £20 — Charm pricing makes prices seem lower."
> "Anchoring Bias — First price anchors perception of the discount." (original £200 crossed out, new £100 shown)

The lesson: the first price the user sees sets their reference point for the entire purchase. If you show £49 in search and £87 at checkout, the user doesn't feel they're paying £87 — they feel they've been tricked out of £38.

### Audible — credit pricing requires cross-screen math
> "Buy 3 Credits / £23.99 | Buy 5 Credits / £32.99 — It's intuitively a discount, but not clear by how much. So you'll attempt to work it out."

> "But then you can't compare it directly to the price of actually buying the book, because that's on the previous step."

### WSJ (intro) — confusing subscription pricing as a pattern
> "Why does it take more clicks to subscribe to the WSJ than to open a bank account?"
> "Introductory rates that jump 1000% after 3 months."

The 1000% price jump after the introductory rate is the subscription equivalent of the hidden fee: the user agrees to a price that does not match the long-term cost they are actually committing to.

## What Good Looks Like
A product page that shows the realistic total: "From £39.99 + taxes (~£18) + 1 bag (~£20) = typically £78." The user arrives at checkout already having calibrated their expectation. The confirmed price is not a shock — it's the number they already calculated. Abandonment at the final step drops because there is no new decision to make.

## Red Flags
- [ ] Search/marketing price is more than 20% below typical checkout total
- [ ] Mandatory fees appear for the first time on the final payment screen
- [ ] Per-unit credit pricing requires the user to do division to compare options
- [ ] Introductory subscription rate resets with less than 14 days' notice before the charge
- [ ] "Total" shown before add-ons are selected doesn't include the add-ons users almost always choose
