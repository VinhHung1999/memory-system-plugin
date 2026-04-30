---
name: ux-bfm-teardowns
description: "Apply the Built For Mars (BFM) teardowns framework — based on 8 real UX teardowns (Chatbots, ChatGPT, Reddit, Substack, Ticketmaster, GameStop, Uber Eats Driver, HBO Max). Use this skill when critically analyzing a product's UX, identifying where big products fail users, reviewing AI/conversational interfaces, spotting dark patterns in mainstream apps, or understanding how market power enables bad UX. Trigger on: 'teardown', 'product critique', 'why does X have bad UX', 'analyze this app', 'what's wrong with', 'dark pattern in', 'AI chat interface design', 'monopoly UX'."
---

# BFM Teardowns Framework

8 BFM teardowns reveal how big, successful products fail their users — and why. This skill encodes the recurring patterns.

## How to Use

Identify which teardown pattern applies, load the relevant reference file, and apply the framework.

**Output format:**
```
## Teardown: [Product/Topic]

### The core failure
[Which teardown pattern applies and why this product exemplifies it]

### BFM Evidence
[Verbatim quotes from case studies]

### What good looks like
[The ethical/better alternative]

### Why it persists
[Why the company keeps doing it despite the failure]
```

---

## 5 Teardown Patterns

| # | Pattern | Key Question | Reference |
|---|---------|-------------|-----------|
| 1 | **Monopoly UX** | Is bad UX being sustained by market position rather than failing because of it? | `references/01-monopoly-ux.md` |
| 2 | **Dark Patterns at Scale** | Are manipulative design choices embedded in a mainstream, trusted product? | `references/02-dark-patterns-scale.md` |
| 3 | **AI & Chat Interface Design** | Does the conversational interface hide or reveal capability? Does it set honest expectations? | `references/03-ai-chat-design.md` |
| 4 | **Feature Education Gap** | Do users discover new features through the product — or through external media? | `references/04-feature-education.md` |
| 5 | **Platform Power vs. User Control** | Is the product using platform leverage to restrict user choices rather than improve them? | `references/05-platform-power.md` |

---

## Quick Diagnostic Checklist

- [ ] Product's UX is consistently criticised but market share is unaffected — monopoly insulation
- [ ] Permission prompt has no "decline" button — only "continue" (foot-in-the-door manipulation)
- [ ] New features are announced via press release / YouTube — not discoverable in-app
- [ ] AI/chatbot interface doesn't communicate whether user is talking to a human or bot
- [ ] Suggested prompts/entry points disappear at the moment the user needs them most
- [ ] Third-party apps/integrations shut down without a meaningfully better native replacement
- [ ] Fee or charge revealed only at the final step of a multi-step purchase flow
- [ ] User must navigate to a separate settings screen to say "no" to what should be a binary choice

---

## When to Load Reference Files

**Load `01-monopoly-ux.md`** when analyzing a product with >50% market share or no meaningful competitor — where bad UX persists because switching is difficult.

**Load `02-dark-patterns-scale.md`** when identifying manipulative design in products used by millions — the scale makes the patterns more consequential.

**Load `03-ai-chat-design.md`** when reviewing AI assistants, chatbots, or any conversational interface — including whether the interface honestly communicates its nature.

**Load `04-feature-education.md`** when a product has powerful features that most users never discover — the launch strategy is the design failure.

**Load `05-platform-power.md`** when a company uses its platform position to restrict user access to alternatives or degrade non-preferred surfaces.
