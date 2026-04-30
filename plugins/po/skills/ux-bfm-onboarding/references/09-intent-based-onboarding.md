# Intent-Based Onboarding

## Core Principle
Observable actions are not a reliable proxy for intent. A user who declines notifications does not necessarily never want them — they may want them later, in a more relevant context. A user who sets an aspirational goal during sign-up may not be committed to it. Onboarding that treats signals as permanent commitments creates a personalised experience for a user who no longer exists. Good intent-based onboarding asks the right questions at the right moment and re-asks them when context changes.

## Diagnostic Questions
- Are decisions collected during onboarding used to customise the experience, or just collected and then ignored?
- Does any step in onboarding ask the user to make a commitment they are not yet ready to make?
- Are there moments later in the product where the user's declared intent could be revisited more usefully than it was at sign-up?

## Design Checklist
- Separate exploratory users from ready-to-commit users early, and provide a demo or sandbox path for explorers.
- Do not present aspirational goal questions as binding configuration steps — make clear that these shape the starting point, not a permanent commitment.
- When the user explicitly seeks more information at a decision point ("Linked or unlinked? Learn more"), treat this as a high-intent signal and give a deep, specific answer.
- Re-teach important concepts at the moment the user encounters the relevant situation — not only during sign-up.
- Choose UI components deliberately: an error-style alert for educational content signals danger, not information.

## BFM Evidence

### YNAB — aspirational intent vs. binding configuration
> "It was a single page. It was also out of context and aspirational." (about savings goal selection that silently configures complex budget categories)

### YNAB — lack of context at the decision point
> "By clicking on this link, the user is clearly identifying themselves as someone who doesn't know what to do. They are trying to optimise their decision. So YNAB should list the benefits and differences here, not the features."

### YNAB — commitment required before understanding is possible
> "There wasn't the motivation or context for them to answer these in a complete way."

### YNAB — the downstream cost of uninformed early decisions
> "I didn't have the context or understanding to resolve the problem." (after connecting a bank account and receiving 99+ transactions)

### Strava — declared intent collected and then ignored
> "But instead, they learn this key piece of information [that the user wants to run] ... just to immediately ignore it, and attempt to convert the user with a generic paywall."

### Grok — how user intent can be misread at the exploration stage
> "You have to assume that the user has no context at all." (about a user discovering the Tasks feature for the first time)

## Anti-Pattern
**What goes wrong:** Onboarding collects intent signals (goals, preferences, savings targets) and uses them to configure the product silently. The user does not know what they agreed to, and when the configuration causes problems, they lack the context to fix it.
**Why it happens:** Teams want to personalise quickly and keep onboarding short. Explaining the consequences of each selection would slow the flow, so the explanations are removed.
**BFM Example:** YNAB — the savings goals questionnaire ("Are you saving for any of these?") silently creates budget categories with complex milestone logic (monthly targets, eventual targets, hard deadlines). "None of that logic is mentioned at the point of input. (Because they wanted to keep onboarding simple)." Users who select "Emergency fund" and "Vacation" end up with a budget that auto-prioritises emergency fund funding before vacation — a decision they did not consciously make.

## Diagnostic Questions
- Does any step collect intent or preference data that silently configures the product in a way the user will only discover later?
- Is there a demo or sandbox path for users who want to explore before committing to a configuration?
- Are there UI components (colours, iconography, alert styles) in the onboarding flow that signal the wrong emotional tone?

## Design Checklist
- Show the consequences of intent-collection steps inline: "If you select this, your budget will automatically prioritise it."
- Offer a sandbox or demo environment for users who are not yet ready to configure with real data.
- Re-teach important logistical concepts at the moment they become relevant — after the user has encountered the situation, not before.
- Match UI component choice to the emotional tone of the content: do not use error-style components for educational content.

## Red Flags
- [ ] Intent or preference collected during onboarding silently configures the product in ways not visible to the user on the same screen.
- [ ] There is no demo or sandbox path for users who want to explore without committing real data.
- [ ] A "Learn more" link at a decision point leads to a feature comparison table rather than a consequence explanation.
- [ ] The product uses an error-style visual (red, warning icon) for informational or educational content.
- [ ] Intent signals collected during sign-up (sport, goal, company size) are not referenced at any point in the product after onboarding ends.
