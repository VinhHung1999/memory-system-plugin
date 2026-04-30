# When Not to Onboard

## Core Principle
The best onboarding is sometimes no onboarding. When a feature is self-evident or low-risk, adding a tutorial creates friction, signals that the product is hard to use, and can distract from the core action. The question is not "should we explain this?" but "will the user be worse off if we don't?"

## Diagnostic Questions
- If we removed this tutorial or prompt, how many users would fail to complete the action it covers?
- Is this feature low-risk and self-evident, or does failure have a meaningful cost to the user?
- Does the onboarding for this feature exist because users need it, or because someone on the team wanted to promote it?

## Design Checklist
- Apply the Reverse Prototype test: remove the onboarding for a feature, observe the abandon rate, and only add it back if the data warrants it.
- Do not onboard features that users can discover and use correctly without instruction.
- Do not onboard features whose failure is low-stakes and immediately recoverable.
- When standard metrics (completion rate, drop-off) show no problem, also check for unnecessary onboarding — users who complete the flow despite the tutorial, not because of it.
- Reserve onboarding for high-stakes decisions (irreversible choices, high-cost errors) or features with non-obvious capabilities.

## Anti-Pattern
**What goes wrong:** A product adds a tutorial for a feature that users can figure out on their own, creating friction and signalling complexity where none exists.
**Why it happens:** Teams default to explaining features because it feels safer. No one gets blamed for explaining too much — only for not explaining enough.
**BFM Example:** Sainsbury's (Supermarkets) — the SmartShop app shows a multi-screen tutorial for barcode scanning before the user has even entered the store. "There's not much use in showing me any of this when I'm at home." The tutorial ends by prompting the user to scan their first item — when they are still standing at the front of the store with nothing in their hands.

## BFM Evidence

### Supermarkets — when self-evident features need no explanation
> "Take the 'scan and go' technology in supermarkets, for example. This is true of onboarding. Often, the best education is to put it in user's hands."

### Supermarkets — tutorial timing destroys its usefulness
> "There's not much use in showing me any of this when I'm at home." (about the in-store scanning tutorial)

### Supermarkets — tutorial ending with an impossible prompt
> "Weirder still ... this tutorial ends by asking you to scan your first item. But the timing is all wrong, because I'm probably still standing at the front of the store."

### Grok — when contextual discovery replaces onboarding
> "Before I get into that, it'll be useful to demonstrate when new functionality doesn't need onboarding."

### Grok — self-evident features at the right moment
> "With this example, the outcome isn't reliant on the user knowing how it works in advance. It's located in the right place to be discovered, at the right time."

### Supermarkets — pre-emptive explanation of failure modes
> "They'll also tell you what to do if a barcode won't scan. Which should just be explained when it happens."

## What Good Looks Like
Waitrose's scan-and-go opens directly to the camera without a tutorial. When a scan fails, it shows the error in context with the manual barcode entry option surfaced at that moment — not in a pre-emptive tutorial nobody reads. The product teaches through the experience of using it, reserving explicit instruction for the one moment it is genuinely needed.

## Red Flags
- [ ] The product shows a tutorial for a feature that involves pointing a camera at something — an action that requires no explanation.
- [ ] Onboarding tips for edge cases ("what to do if this fails") appear before the user has attempted the main action.
- [ ] The tutorial contains a call-to-action ("scan your first item") that the user cannot fulfill in their current context.
- [ ] Standard funnel metrics look healthy, but the tutorial has never been tested in a removed state.
- [ ] Tutorial content is shown at a time or location when the user cannot act on the information.
