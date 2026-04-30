# Noise & Cognitive Load

## Core Principle
Noise is anything that distracts the user from their current intent — whether it is a notification, a privacy warning, a modal, or an irrelevant suggestion. Noise accumulates silently: each individual interruption seems minor, so teams do not notice the compound effect until churn data reveals it. The frame effect of early noise can permanently colour a user's perception of the product.

## Diagnostic Questions
- What is the user's intent at this exact step, and does every element on screen serve that intent?
- How many separate interruptions or redirections does a new user encounter before completing their first meaningful action?
- Does any notification or alert shown during onboarding frame the product as a source of risk or anxiety?

## Design Checklist
- Map every step of the new-user journey and count the number of off-path events (modals, notifications, privacy alerts, settings prompts).
- Remove or defer any interruption that does not directly advance the user's current goal.
- Never use a notification or privacy framing during onboarding that creates anxiety ("Your profile fields might be visible").
- Treat the empty state of any feature as an onboarding opportunity — not a generic placeholder.
- If you must show a tip or tutorial, show it exactly when the user encounters the relevant situation, not before.

## Anti-Pattern
**What goes wrong:** The team adds individual notifications, privacy prompts, and feature callouts at separate points in development, each approved in isolation. No one audits the cumulative experience.
**Why it happens:** Product teams measure completion rate of each step, not the total cognitive load of the full flow. Each PM defends their notification as "low friction."
**BFM Example:** LinkedIn — within the first session, a new user is sent to settings to review privacy controls, shown a notification about reorganised notification settings (for an account with no previous settings), directed to a search history page that is empty, and prompted three times to view a marketing notification. "Not only does it add friction into the UX. But it can confuse the messaging and distort the user's priorities."

## BFM Evidence

### LinkedIn — privacy framing creates the wrong mental model
> "i.e., this frames LinkedIn as a tool where you should deeply care about your own privacy."

### LinkedIn — notification about settings that do not exist
> "Reassuring, given that I've only just created an account, and have no previous settings."

### LinkedIn — the notification layer problem
> "Annoyingly, LinkedIn use notifications like this all the time. And they're almost never urgent."

### LinkedIn — noise blocks the milestone moment
> "It quite literally appears on a higher Z-axis than everything else. Not only does it add friction into the UX. But it can confuse the messaging and distort the user's priorities."

### Sainsbury's (Supermarkets) — prompting actions before they are relevant
> "There's not much use in showing me any of this when I'm at home." (referring to the in-store tutorial shown before the user is in a store)

### Sainsbury's (Supermarkets) — explaining failure modes before the user has experienced them
> "I've also never tried this app before, so I've no idea if my internet will be suitable or not. I haven't experienced the pain yet." (about the Wi-Fi prompt)

## What Good Looks Like
Slack hides complexity by not calling a "channel" a channel during setup. The workspace creation asks "What is your team working on?" and creates a channel silently — the user never has to make a structural decision before they are ready. Each complexity is revealed only at the moment it becomes necessary. The result is that onboarding feels effortless, even though Slack is a structurally complex product.

## Red Flags
- [ ] A new user encounters a privacy or security notification before completing their first meaningful action.
- [ ] The first session contains more than two redirections away from the primary onboarding path.
- [ ] Any notification or modal shown during onboarding references a concept the user has not yet encountered (e.g., "previous settings," "search history").
- [ ] Onboarding tips about edge cases (barcode won't scan, Wi-Fi connection) appear before the user has experienced the main flow.
- [ ] An empty state shown to a new user contains only a generic placeholder with no onboarding value.
