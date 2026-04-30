# Feature Education Gap

## Core Principle
A feature that exists but is not discovered is, from the user's perspective, a feature that does not exist. The feature education gap is the distance between what a product can do and what its users know it can do. In simple products, this gap is small — the interface is the map of the capability. In complex products (AI assistants, financial tools, productivity suites), this gap widens with every new release, and closing it requires deliberate in-product design — not press releases, YouTube demos, or help center articles.

## Diagnostic Questions
- What percentage of users have discovered and used your most powerful features?
- How do users typically learn about new features — through the product, or through external media?
- Is there a feature your team is proud of that your users consistently don't know about?
- When a feature is released, is in-product discovery designed before launch — or added as an afterthought?

## Design Checklist
- Design in-product feature discovery before launch, not as a post-launch hotfix
- Entry points for new features should appear in context — at the moment the user has a problem the feature solves
- Contextual prompts are more effective than feature tours: "You can ask me to summarise this" beats "New feature: Summarise"
- Analytics should track feature discovery rate (% of users who have triggered the feature at least once) separately from feature usage rate (how often those users use it)
- Do not assume that power users who share YouTube videos represent the majority of your user base

## Anti-Pattern
**What goes wrong:** A product team builds a genuinely valuable new feature and launches it with a blog post and a YouTube video. Power users adopt it within days. General users never encounter it in the product. 6 months later, user research reveals that 85% of users are unaware the feature exists. The team responds by building another feature.
**Why it happens:** "Launching" a feature means publishing the technical capability. In-product discovery design is treated as a secondary concern — "users can find it in the settings menu." The metrics system counts feature usage, not feature discovery. The gap is invisible.
**BFM Example (ChatGPT o1):** o1's reasoning capability was launched with waves of YouTube videos and developer benchmarks. The in-product discovery mechanism is a model dropdown that most users never interact with. Users who use ChatGPT daily may not know o1 exists, or know what it does differently, months after launch.

## BFM Evidence

### ChatGPT — external education as the primary discovery channel
> "When a new version of ChatGPT is released... there are waves of studio quality videos..."
> Videos: "Building with OpenAI o1," "Coding with OpenAI o1," "Counting with OpenAI o1," "Video Game Coding with OpenAI o1," "Writing Puzzles with OpenAI o1," "Reasoning with OpenAI o1"

Each video is a signal that in-product discovery failed: if the feature were easily discoverable in the product, the YouTube content would not exist at this volume. The videos exist to bridge the gap the product left.

### ChatGPT — the model selector as a feature graveyard
> "Model selector showing: GPT-4o, o1-preview (checked), o1-mini, GPT-4, Temporary Chat"

Five model options in a dropdown, none explained in plain language. A user who doesn't know what "o1-preview" means will never select it — and will never discover that it is meaningfully different from the default. The capability is present; the education is absent.

### ChatGPT — the onboarding paradox
> "Suggested prompts: 'Plan a mental health day' and 'Count the number of in an image'"

These prompts appear on an empty chat screen — when the user has not yet identified what they need. They disappear when the user starts typing — when the user has identified a need but is struggling to articulate it. The timing of the educational prompt is inverted: it arrives early (when the user doesn't need direction) and disappears late (when they do).

### Chatbots — capability ambiguity creates underuse
The BFM chatbots case study documents a parallel failure: users don't know what chatbots can do, so they ask simple questions, get simple answers, and conclude the chatbot is useless. The chatbot may be capable of complex tasks — but the interface suggests "type a question" and the user types the simplest possible question.

Feature education in chatbots is not just about announcing capability — it is about designing the first interaction to demonstrate the level of sophistication the system can handle.

## What Good Looks Like
An in-product feature discovery system where: the first time a user encounters a task that a new feature would improve, the interface proactively surfaces it ("You can ask me to do X — try it"); new model capabilities come with contextual introductions at the point of use, not just at the model selection dropdown; and feature discovery rate is measured and tracked as a separate, first-class metric.

## Red Flags
- [ ] New features announced via blog post / YouTube without a parallel in-product discovery design
- [ ] Feature usage rate tracked but feature discovery rate not tracked
- [ ] Power users are cited as evidence that features are discoverable ("look how many YouTube videos there are")
- [ ] Entry point for a new feature is a settings menu or a dropdown — not a contextual, moment-of-need prompt
- [ ] User research consistently reveals low feature awareness for features the team considers core
