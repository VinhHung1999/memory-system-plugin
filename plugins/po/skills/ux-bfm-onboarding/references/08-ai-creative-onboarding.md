# AI & Creative Feature Onboarding

## Core Principle
Creative and AI features converge on a single open-ended text input, which hides unique capabilities from users who do not know what to type. Pointing at the feature ("Analyse Docs") is not enough — users need to understand the range of what the feature can do before they can use it well. A paywall or task limit that activates during exploration kills experimentation and forces users to think small.

## Diagnostic Questions
- Does the user understand the RANGE of what this feature can do, or just the fact that it exists?
- Is there anything in this feature's entry point that gives the user a concrete, memorable example of a use case they had not thought of?
- If the user tries the feature once and uses it poorly, does the product help them use it better on the second attempt?

## Design Checklist
- Surface rotating examples of what users can achieve with the feature — not generic descriptions, but specific, visceral prompts that spark ideas.
- Make examples context-sensitive: if the user has uploaded a CSV, suggest CSV-specific queries; if they uploaded a PDF, suggest document-specific ones.
- Do not stop onboarding after first use. The first use is often exploratory and under-informed — the second use is where the real learning happens.
- Avoid paywalls or limits that activate during early exploration. If a user hits a limit while still discovering the feature, they disengage before committing.
- For features the user stumbles across (not actively sought), pair the feature discovery with inspiration — not just a description of what it does.

## Anti-Pattern
**What goes wrong:** The product shows a feature entry point (button, empty state) with a generic label and an open text field. Users who do not already know what to type are left to guess.
**Why it happens:** The team assumes the feature's value is self-evident once the user sees the input. The onboarding is designed for users who already have a use case in mind.
**BFM Example:** Grok — the "Analyse Docs" entry point shows an open text field with no examples. "The problem isn't that people can't think of anything to enter. It's that they're having to guess at how to use it effectively. They don't know all the things that it could do."

## BFM Evidence

### Grok — the convergence problem for AI interfaces
> "You'll have noticed that most AI apps are converging on a similar interface. Which makes it more challenging to introduce new features."

### Grok — the real problem with open input fields
> "The problem isn't that people can't think of anything to enter. It's that they're having to guess at how to use it effectively. They don't know all the things that it could do."

### Grok — rotating examples reframe how users think about the tool
> "Grok should give rotating examples to demonstrate the types of query that people can make. This reframes how people think about the tool. It gives them something visceral to remember."

### Grok — indirect value of inspiration even without immediate action
> "Even if they don't do this action right away, they're more likely to associate value to Grok because of it."

### Grok — the three-stage framework for creative feature onboarding
> "1. If you're directly encouraging someone to try a feature ... then you should explain the limitations (and benefits) in that moment. 2. If it's a feature that the user stumbles across for the first time ... you need to explain how it works and inspire them to use it better."

### Grok — the importance of the strategic thinking moment
> "It's important to identify the moment that users will be working on the task ... and help them to practically do that thing. This is where the strategic thinking is happening."

## What Good Looks Like
When a user uploads a spreadsheet to an AI tool, the interface immediately surfaces three rotating example queries tailored to spreadsheet files: "What's my average customer value?", "Which days do I get the most subscribers?", "Which ad campaign did the best?" The user reads these, thinks "I could use it to analyse my sales data," and submits a query they would not have thought of independently. Even if they do not click an example, their mental model of the feature has expanded.

## Red Flags
- [ ] The AI feature entry point shows only an open text field with a placeholder like "Ask anything" and no contextual examples.
- [ ] Example prompts shown are generic across all file types or contexts rather than tailored to what the user has just uploaded.
- [ ] The user hits a paywall or usage limit while still in the exploratory phase of first use.
- [ ] After the user's first (likely under-informed) use of the feature, the product provides no nudge or guidance toward a better second use.
- [ ] The feature's empty state only describes what the feature is ("Schedule a task to automate any prompt") without helping the user think of a task to try.
