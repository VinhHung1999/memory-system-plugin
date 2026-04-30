# Expectation Setting

## Core Principle
Users form an expectation the moment they take an action. When the outcome matches that expectation, the interaction is invisible. When it doesn't, the gap between expectation and reality is experienced as frustration — and the larger the gap, the greater the frustration. Chatbot UX fails primarily because the entry point (a chat widget that looks like messaging a human) sets an expectation that the interface cannot fulfill.

## Diagnostic Questions
- What does the user expect to happen when they press this button, and does the actual outcome match?
- Is the CTA or entry point honest about what type of interaction the user is entering — human, bot, or hybrid?
- When the outcome might disappoint (long wait, no human, limited capability), is that communicated before or after the user commits?

## Design Checklist
- Match the visual design of the entry point to the actual experience (a chat widget implies human conversation; a form implies routing)
- Disclose wait times, bot vs human status, and routing logic before the user begins, not after they are stuck
- If a decision tree may redirect users to a help article, warn them upfront rather than surprising them mid-flow
- CTA labels should describe the outcome, not just the action ("Start a chat with a real advisor" vs "Chat with us")
- For chatbots, establish the capability boundary early: "I can help with X and Y. For anything else, I'll connect you to the team."

## Anti-Pattern
**What goes wrong:** A company labels a button "Chat with us," but clicking it enters a decision tree that may or may not produce a human, depending on answers to automated questions. Users who expected a human feel deceived.
**Why it happens:** Customer support teams design each step of the chatbot flow individually. No one owns the gap between the entry point expectation and the eventual outcome. The CTA is written by marketing, the decision tree by ops.
**BFM Example:** Revolut — a user asked the chatbot "How do I downgrade my plan?" and was shown entirely unrelated prompts (French IBAN, overdraft, statements). The chatbot then offered "How do I upgrade my plan?" as the closest match — the opposite of what was requested. The user could not be certain whether typing a new message would lose all context already given.

## BFM Evidence
### Chatbots — action-expectation alignment is foundational
> "Being confident in the outcome of an action, is a core UX principle. It's what makes a button comfortable to click on. It's why you don't panic about using a teapot."

### Chatbots — the widget used to set an honest expectation
> "For a long time the chat widget existed as a tool to enable seamless conversation. And importantly, the user could be confident that their message would eventually reach a human."

### Chatbots — blurring human and bot boundaries creates suspicion
> "We've blurred the lines between genuine human interaction, chatbots and AI. Sometimes companies even leverage this ambiguity. Objectively to look at, you could assume that you're speaking to a live chat specialist called Ruby. But as soon as you reply... she immediately turns into Frank, who then posts a templated message. It's too quick to have ever been typed. So is Frank real? All it does is make me suspicious."

### Chatbots — the core failure: users cannot be certain of the outcome
> "This forces the user to make a decision: do they select the most related available prompt? (And hope it pushes them in the right direction). Or type something new, and possibly lose any context they've already given to the assistant? Neither of these are comfortable, because the user cannot be certain of the outcome."

### Chatbots — Starling does it right
> "And more importantly, they don't use chatbots as gatekeepers. Instead, they give you clear context about what is happening. This is the simplicity and human touch that we're all craving."

### Flights — insider blind spots create expectation gaps
> "Review manipulation — social proof anchored to lower scores increases perceived value." (The designer knows what an 8.2/10 means; the user doesn't know the benchmark distribution.)

## What Good Looks Like
Starling Bank — a single, clearly labeled "Live chat" button with the description "The quickest way to get an answer." Within one minute, a named human ("Emma") confirms the connection and says "Hi Peter, you're through to Emma." The outcome matched the expectation set at the entry point exactly.

## Red Flags
- [ ] The CTA says "Chat with us" but the flow begins with an automated decision tree, not a human
- [ ] Bot vs human status is not disclosed before the user begins typing
- [ ] Wait time for a human agent is not shown — user does not know if they are wasting their time
- [ ] Switching topics mid-bot-flow would cause the user to lose all previously given context
- [ ] The entry point widget looks like a messaging app but behaves like a form
