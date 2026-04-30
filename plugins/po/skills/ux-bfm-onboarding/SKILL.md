---
name: ux-bfm-onboarding
description: "Apply the Built For Mars (BFM) onboarding framework — based on 11 real UX case studies (Headspace, Slack, Strava, Trello, YNAB, Chase, Costa, Grok, LinkedIn, Supermarkets, Wise) with 979 annotated slides. Use this skill when: (1) reviewing/auditing an existing onboarding flow, (2) designing a new onboarding flow from scratch, (3) diagnosing high churn or low activation, (4) user asks what's wrong with my onboarding, (5) user asks help me design onboarding for a product."
---

# BFM Onboarding Framework

Built For Mars is a UX case study platform by Peter Ramsey. This skill encodes principles extracted from 979 annotated slides across 11 case studies into a reusable framework for reviewing and designing onboarding flows.

## Two Modes

### Mode 1: REVIEW — Audit an existing flow
Use when the user describes or shares an existing onboarding flow and wants critique.

**Workflow:**
1. Understand the product and user goal
2. Run through the 10-category checklist (below)
3. For each category: ask the diagnostic question, identify findings
4. Output: structured critique with Severity + Recommendation per finding

**Output format:**
```
## Onboarding Review: [Product Name]

### Critical Issues
- **[Category]:** [Finding] → [Recommendation]

### Warnings
- **[Category]:** [Finding] → [Recommendation]

### Passing
- **[Category]:** ✓ [What they do well]

### Priority Actions (top 3)
1. ...
2. ...
3. ...
```

---

### Mode 2: DESIGN — Create a new onboarding flow
Use when the user describes a product and wants help designing onboarding from scratch.

**Workflow:**
1. Ask clarifying questions (if not provided): What is the product? Who is the user? What is the core action? Is it B2B or B2C? Is there a paywall?
2. Run through the 10-category design checklist to build the flow
3. Output: step-by-step onboarding flow with rationale per decision

**Output format:**
```
## Onboarding Design: [Product Name]

### One Thing (core action to protect)
...

### Flow Steps
Step 1: [Screen/Action] — [Why: which BFM principle]
Step 2: ...
...

### Anti-patterns to avoid for this product type
...

### Open questions to validate
...
```

---

## 10-Category Framework

For each category, a reference file with diagnostic questions, anti-patterns, BFM evidence, and red flags is available in `references/`. Load the relevant file when depth is needed.

| # | Category | Key Question | Reference |
|---|----------|-------------|-----------|
| 1 | **Activation & Aha! Moment** | Does the user feel value BEFORE the core product is explained? | `references/01-activation-aha-moment.md` |
| 2 | **Goal-Setting & Goal Gradient** | Does the user OWN their goal, and can they see progress? | `references/02-goal-setting.md` |
| 3 | **Noise & Cognitive Load** | How many onboarding triggers fire simultaneously? | `references/03-noise-cognitive-load.md` |
| 4 | **Celebration & Milestones** | Do celebrations align with what the USER wants, not what you need? | `references/04-celebration-milestones.md` |
| 5 | **Progressive Disclosure** | Are decisions delayed until the user needs to make them? | `references/05-progressive-disclosure.md` |
| 6 | **The One Thing** | Is there a single core action the flow protects above all else? | `references/06-one-thing-focus.md` |
| 7 | **When NOT to Onboard** | Could removing this onboarding improve completion rates? | `references/07-when-not-to-onboard.md` |
| 8 | **AI & Creative Features** | Does the user understand the RANGE of what the feature can do? | `references/08-ai-creative-onboarding.md` |
| 9 | **Intent-Based Onboarding** | Are you responding to user INTENT or just their observable action? | `references/09-intent-based-onboarding.md` |
| 10 | **Transparency & Trust** | Does the user understand what they're getting and why it's valuable? | `references/10-transparency-trust.md` |

---

## Quick Red Flags Checklist

Run through these first — any "yes" is a likely problem:

- [ ] Onboarding celebrates a milestone the user didn't care about (e.g., "You signed up!")
- [ ] Onboarding fires 3+ tooltips/prompts in the first session
- [ ] Goals are pre-selected or labeled ("Basic / Serious / Elite")
- [ ] The "Aha! moment" comes after 3+ screens of explanation
- [ ] A paywall appears before the user has explored the creative range of a feature
- [ ] Sign-up collects data that isn't used to personalize the experience
- [ ] The user can't see how close they are to a reward/milestone
- [ ] A simple, self-evident feature has a multi-step tutorial
- [ ] Onboarding triggers fire even when user is mid-task on something else
- [ ] Template/demo content tries to educate AND demonstrate at the same time
- [ ] UI component used for an educational popup looks like an error (red, warning icon)
- [ ] The "one thing" is unclear — onboarding promotes 3+ different actions equally

---

## When to Load Reference Files

**Always load first:** `references/00-product-types.md` — identifies which product type applies and which 3 categories to prioritise. Saves running all 10 categories when 3 are dominant.

Load a category reference file when:
- A product has a specific issue in that category and you need concrete examples/evidence
- The user asks "why" or "how" for that category
- Designing a flow that involves that category's patterns

Example: If reviewing a fitness app and noticing they pre-select goals → load `references/02-goal-setting.md` for Strava examples and exact anti-pattern explanation.
