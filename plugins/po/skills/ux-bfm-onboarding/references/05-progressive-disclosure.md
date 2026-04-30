# Progressive Disclosure

## Core Principle
Smart defaults should teach users how to use a product without requiring explicit instruction — the interface itself makes the correct choice obvious before the user has to think. Revealing complexity too early creates Decision Fatigue and causes bad defaults that are hard to reverse later. Hiding complexity completely (rather than deferring it) trades a good short-term completion rate for a poor long-term experience.

## Diagnostic Questions
- Are there decisions in this flow that could be made correctly by a smart default, instead of requiring user input?
- Is any decision presented to the user before they have the context to make it well?
- Are there downstream consequences of early decisions that the user is not warned about?

## Design Checklist
- Use smart defaults that encode product best practices, so users who accept them end up in a good state.
- Defer structural or configuration decisions until the user has used the product enough to understand what they are deciding.
- When a user explicitly seeks more information ("Learn more to help you decide"), treat that as high-intent — give them a deep, specific answer.
- Warn users at decision points about irreversible or high-impact consequences.
- Present complex choices as intent-framed questions ("What is your team working on?") rather than structural-framed questions ("Create your first channel").

## Anti-Pattern
**What goes wrong:** A complex decision is presented early in onboarding without explaining the downstream consequences, so users pick an option that creates problems they cannot fix later without expert knowledge.
**Why it happens:** The product team wants to personalise the experience quickly, so they collect configuration data upfront — but they simplify the UI at the expense of the context the user needs.
**BFM Example:** YNAB — the "Linked vs. Unlinked" bank account decision is presented as a simple two-option screen. Choosing "Linked" imports 99+ transactions immediately. "I didn't have the context or understanding to resolve the problem." The decision point says "Learn more to help you decide" — but the help screen lists features, not consequences.

## BFM Evidence

### Slack — intent-framed channel creation hides complexity
> "But notice that it's framed to be about your intentions. They don't even mention channels."

### Slack — smart defaults teach without instructing
> "Whilst creating a workspace, you'll notice that your dashboard builds around you in real time. i.e., you're being incrementally exposed to key items, in real time."

### Slack — the cost of hiding complexity entirely
> "The lack of context, onboarding, or even the awareness of complexity breeds inefficiency and noise."

### YNAB — the "help" screen explains features, not consequences
> "So YNAB should list the benefits and differences here, not the features. For example, nothing here explains the consequences of this decision."

### YNAB — aspirational questions answered without context
> "It was a single page. It was also out of context and aspirational." (about savings goal selection that silently creates budget categories with complex milestone logic)

### Strava — decision fatigue from repeated vague paywalls
> "'Our best' / 'So much more' / 'Subscriber-only features' / 'Deepest look' — which they follow up with another vague full screen prompt."

## What Good Looks Like
Slack's workspace creation asks "What is your company or team called?" and auto-generates a workspace URL from the answer. It asks "What are you working on right now?" and creates a channel named after the answer — without ever mentioning channels. The user enters the product with a sensible structure already in place, built from their own words. The complexity of channel organisation is revealed only when the user actively tries to add more channels.

## Red Flags
- [ ] A high-consequence decision (data import, billing cycle, notification permissions) is presented before the user has used the product at all.
- [ ] The "learn more" or "help" link at a decision point shows a feature comparison table instead of a consequence explanation.
- [ ] Accepting the default option at any decision point during onboarding creates a state that is difficult to correct without knowing how the system works.
- [ ] The onboarding questionnaire collects personalisation data that silently configures the product in ways the user will only discover later.
- [ ] Complex vocabulary is used at decision points without a plain-language explanation in the same view.
