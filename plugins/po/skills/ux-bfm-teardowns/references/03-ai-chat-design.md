# AI & Chat Interface Design

## Core Principle
Chat interfaces create unique UX problems that traditional UI patterns cannot solve. Unlike button-driven interfaces, a chat interface must communicate capability through language alone — there are no visible menu items, no feature discovery through browsing. The harder the underlying AI becomes, the more important it is to make the surface feel simpler, not just capable. And any conversational interface must answer one question before the user engages: "Am I talking to a human or a machine?" Ambiguity here is not neutral — it is manipulative.

## Diagnostic Questions
- When a user opens the chat interface, do they know what it can do? Do they know what it can't?
- Does the interface indicate whether the user is talking to an AI, a human, or a hybrid?
- As new model capabilities are added, does the interface get easier to use — or just more powerful?
- Are entry points (suggested prompts, example queries) visible when the user needs them most?

## Design Checklist
- Suggested prompts / entry points must remain visible as the user begins composing — not disappear the moment they start typing
- New AI capabilities must be discoverable in-product, not only via external announcements
- If a chatbot can escalate to a human, this transition must be explicitly indicated — not hidden in language style changes
- The interface should constrain visible options to what the model can actually do — not imply unlimited capability that produces poor responses
- Model selection (GPT-4o vs o1) must be explained in plain language, not technical model names

## Anti-Pattern
**What goes wrong:** AI product adds new model capability (GPT-o1, Claude 3.5, etc.). The capability is announced via press release, YouTube demos, and tech press. The majority of existing users never learn the feature exists through the product itself. Feature adoption is driven by external media, not in-product discovery. The user's mental model of the product's capability lags months behind the actual capability.
**Why it happens:** AI companies' culture prioritises research publication and model benchmarking over UX. "We released it" means "we wrote the blog post" — not "users found it."
**BFM Example (ChatGPT o1):** When o1-preview launched, waves of YouTube videos ("Coding with OpenAI o1," "Reasoning with OpenAI o1") appeared before most users encountered the feature in-product. The model selector in the ChatGPT interface shows technical names (o1-preview, o1-mini, GPT-4, Temporary Chat) with no plain-language explanation of what each does differently.

## BFM Evidence

### ChatGPT — complexity-simplicity tension
> "...it gets harder to squeeze traditional UX principles into a simple chat interface like this."

> "As the underlying technology gets more complicated... [the interface must still feel simple]"

The challenge: a chat interface that was designed for GPT-3 is now housing GPT-4o, o1-preview, o1-mini, and function-calling. The surface hasn't changed; the capability has multiplied. The result is a product where most users use a fraction of the available functionality.

### ChatGPT — suggested prompts disappear at the wrong moment
> "Suggested prompts: 'Plan a mental health day' and 'Count the number of in an image'"

BFM's observation: these entry points appear when the chat is empty — exactly when they are least useful (the user has no context for them). At the moment a user is struggling to articulate a complex request (exactly when a suggestion would help), the prompts are gone — they've disappeared as the user started typing.

### ChatGPT — feature education via YouTube, not product
> "When a new version of ChatGPT is released... there are waves of studio quality videos..."
> "Coding with OpenAI o1 (586K views), Counting with OpenAI o1 (53K views)..."

The external education volume dwarfs any in-product feature introduction. A new user who never watches YouTube will discover o1 by accidentally selecting it from the model dropdown — if they ever notice the dropdown exists.

### Chatbots — human/AI ambiguity as a design failure (and dark pattern)
The BFM chatbots case study identifies the core ambiguity problem: when a chatbot uses human-sounding language, adopts a persona name, and does not clearly indicate it is automated, users who believe they are talking to a human make different (and sometimes consequential) decisions. This is not a neutral UX choice — it is expectation manipulation.

The ethical design requirement: state clearly at the start of any chatbot conversation that the user is interacting with an automated system. A chatbot that doesn't do this is not just confusing — it is deceptive.

## What Good Looks Like
A chat interface that: shows its capability through progressively helpful suggestions as the user's query develops (not just on an empty screen); explains model differences in human terms ("faster and cheaper" vs. "thinks longer for harder problems"); clearly identifies when responses are AI-generated vs. human-escalated; and introduces new features through in-product discovery moments ("try asking me to...") rather than press releases.

## Red Flags
- [ ] Suggested prompts visible only on empty chat — disappear when user starts typing
- [ ] Model selector uses technical names (GPT-4o, o1-mini) with no plain-language differentiation
- [ ] New features announced via blog post / YouTube before in-product discovery is designed
- [ ] Chatbot persona has a human name and uses first-person language without clear AI disclosure
- [ ] User cannot tell from the interface whether they are talking to an AI or a human agent
