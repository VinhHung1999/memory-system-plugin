# Upstream Thinking

## Core Principle
Downstream UX solves problems after they happen — better complaint flows, cancellation-rate dashboards, refund modals. Upstream UX prevents problems before they happen — nudges at the moment of decision, contextual cues that change behaviour in the moment, CTA labels that carry moral weight. The same design budget spent upstream produces orders of magnitude more impact than spent downstream.

## Diagnostic Questions
- At what moment in this flow does the problematic behaviour first become possible, and what is the user's mindset at that exact moment?
- Is the warning, nudge, or deterrent placed before the decision or after the consequence?
- Does the current CTA label communicate the commitment the user is actually making?

## Design Checklist
- Map the moment of decision (accept order, cancel delivery, click "Chat") and intervene there — not after the outcome
- Use contextual, empathetic messaging that acknowledges the user's situation rather than issuing a generic warning
- Personalise the stakes: name the person affected, show the relationship, make the impact concrete
- Replace generic CTA labels with commitment language that activates responsibility ("I will deliver this" instead of "Confirm")
- Surface nudges that teach the correct behaviour before the first session — not after a pattern of bad behaviour has formed
- For chatbots, set the expectation before the user types their first message, not after the decision tree fails them

## Anti-Pattern
**What goes wrong:** A platform detects that a driver has a high cancellation rate and displays a dashboard warning. The warning is shown after the pattern has already formed, uses abstract metrics ("your rate is above average"), and offers no deterrent or guidance at the actual moment of cancellation.
**Why it happens:** Analytics teams measure outcomes. Product teams build features against those metrics. The feedback loop runs weeks behind the behaviour it is trying to change.
**BFM Example:** Uber Eats — drivers who check a receipt timestamp know that old orders are unlikely to result in a tip, so they cancel. Uber's response was a cancellation-rate warning banner shown after the fact. It is "about as downstream as you could possibly be. The driver has already been labelled." No intervention occurs at the moment of cancellation, and the cancel CTA simply reads "Don't want trip."

## BFM Evidence
### Uber Eats — downstream labelling vs upstream intervention
> "In a very weak attempt to stop drivers from doing this, Uber track their cancellation rate. But from a UX perspective, this is about as downstream as you could possibly be. The driver has already been labelled. It's hard to encourage an emotional reaction to this datapoint. It's faceless and detached. And without any deterrent."

### Uber Eats — the cancel moment is the intervention opportunity
> "Think about the moment of cancelling an order. Do you care that 'holly_r' will need to wait a bit longer? Probably not. But you might if Uber leaned into the psychology of this moment. Holly is a real person."

### Uber Eats — CTA labels carry moral weight
> "Or even better, lean into the driver being somewhat responsible for this delivery. i.e., by experimenting with different CTA labels. [e.g., 'I will deliver this' instead of 'Confirm']"

### Uber Eats — contextual empathy changes behaviour
> "But contextual and empathetic messaging can help to encourage specific behaviour. And as a strategy, upstream thinking invites you to get curious about the role of product psychology in avoiding problems."

### Uber Eats — nudge at the right moment
> "After a few minutes of waiting it should nudge the user. Teach them how they can get more opportunities. [e.g., 'Nearby area is busy — Waiting in busy areas can boost the chances of being matched with an order by 35%']"

### Chatbots — the entry point CTA is upstream of the frustration
> "Being confident in the outcome of an action, is a core UX principle. It's what makes a button comfortable to click on." [When the CTA label is honest about what happens next, the frustration downstream never occurs.]

## What Good Looks Like
The cancel modal that reads: "You're Holly's food delivery hero, are you sure you need to cancel?" with Peter's (driver) and Holly's (customer) avatars connected by a dotted line. Combined with the companion modal "You okay, bro?" offering: "I've lost my keys / My maps aren't working / Food isn't ready yet." This addresses both deliberate and accidental non-delivery at exactly the right moment, with empathy rather than surveillance.

## Red Flags
- [ ] Warnings or deterrents appear after the problematic action is already complete
- [ ] Cancellation or abandonment copy uses generic labels ("Don't want trip", "Maybe Later") with no consequence framing
- [ ] Driver/user education happens only during initial onboarding, not contextually during sessions
- [ ] A dashboard metric tracks bad behaviour without triggering any in-session intervention
- [ ] The CTA for a significant commitment uses action language ("Confirm") rather than responsibility language ("I will do X")
