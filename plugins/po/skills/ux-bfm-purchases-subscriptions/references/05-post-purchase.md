# Post-Purchase Confirmation

## Core Principle
The moment after payment is a peak anxiety moment, not a relaxation moment. The user has just transferred money and received nothing tangible yet. Post-purchase confirmation must immediately: (1) confirm the exact transaction, (2) set clear expectations about what happens next and when, and (3) give the user something to do. A generic "Thank you for your order!" fails all three. The best confirmation screens close the anxiety loop and open the next engagement loop.

## Diagnostic Questions
- Does the confirmation screen show the exact item purchased, the total paid, and the estimated delivery/delivery date?
- Is the next action the user should take clearly specified? (Download app, track order, set up account)
- Does the confirmation email arrive within 60 seconds?
- What does the user do in the 24 hours after purchase — is there a designed next step?

## Design Checklist
- Confirmation must show: item with image, quantity, price paid, reference number, and expected delivery/access timeline
- Provide a single clear next action: "Track your order", "Download your audiobook", "Set up your account"
- Send confirmation email within 60 seconds — include all the above plus support contact
- Order tracking, where relevant, should be proactive (push notification when status changes) not reactive (user must check)
- Upsell at the confirmation step must be relevant and light — not a full product catalogue

## Anti-Pattern
**What goes wrong:** Confirmation page shows "Order #849201 placed! Thank you." The user has no idea when it arrives, where to find their receipt, or what to do next. They email support 24 hours later to ask if the order went through. Support ticket is a failure of the confirmation UX, not a customer service issue.
**Why it happens:** The confirmation page is treated as the end of the purchase funnel. The team that owns conversion doesn't own the post-purchase experience. Nobody designed the 24-48 hours after payment.
**BFM Example (Audible):** After purchase, the user sees "Success! Thank you! Your title is being delivered to your Library. This may take a few minutes — refresh your Library if you don't see it." The positive signal is there, but "a few minutes" is vague, "refresh your Library" puts the burden on the user, and there's no notification mechanism. The user who doesn't know where the Library is has no clear next step.

## BFM Evidence

### Audible — post-purchase confirmation with residual friction
> "Success! Thank you! Your title is being delivered to your Library. This may take a few minutes — refresh your Library if you don't see it. | View in Library [button]"

The confirmation exists and is positive. But "a few minutes" is non-specific, "refresh" puts action burden on the user, and there's no push notification for when delivery completes. A user who purchased on mobile and put their phone down will miss the delivery moment entirely.

### Zara — post-purchase tracking as anxiety reducer
> "Order tracking dashboard | Package status | Estimated delivery date — Real-time updates reduce purchase anxiety."
> "Returns policy page | Exchange information | Timeframe details — Clear policy information increases purchase confidence."

Post-purchase anxiety in e-commerce is primarily about: did it ship, when does it arrive, can I return it? Proactive tracking (push when shipped, push when out for delivery, push when delivered) eliminates support tickets for all three.

### Flights Ch.3 — confirmation as the start of the next commitment
> "Booking confirmation | Ref: BK45892 | Passenger: John Smith | Total: £87.99 | 'Booking confirmed!'"
> "Email template | Booking details | Confirmation number | 'Download boarding pass' button — Confirmation email with clear next steps."
> "Mobile notification | 'Flight booked successfully' | LTN → FCO, Dec 5 | 'View details' button"

The flight confirmation model is well-understood: reference number, passenger details, route, total, and the immediate next action (download boarding pass). Every element of this is a lesson in confirmation UX: specific, actionable, and complete.

### Flights Ch.3 — sunk cost psychology after purchase
> "Sunk Cost Fallacy — You're more likely to continue spending because you've already invested money."

The post-purchase period is when upsell is most powerful — not because users are irrational, but because they have already committed to the goal (the trip, the audiobook, the meal). A seat upgrade offer shown 30 minutes after booking converts better than the same offer shown before payment, because the decision to travel is already made.

## What Good Looks Like
A confirmation screen that shows: item image + name, quantity, price paid, reference number, estimated delivery, and one CTA ("Track my order" / "Start listening" / "Download boarding pass"). Followed within 60 seconds by a confirmation email with all the same information plus support contact. Followed, if relevant, by a proactive status notification when the next milestone is reached.

## Red Flags
- [ ] Confirmation screen has no estimated delivery/access time
- [ ] Confirmation email takes more than 5 minutes to arrive
- [ ] No proactive status updates — user must check manually
- [ ] Confirmation screen has no clear next action
- [ ] "Thank you" is the primary message — specific transaction details are secondary or absent
