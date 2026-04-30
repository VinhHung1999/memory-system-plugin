---
name: ux-bfm-psychology
description: "Apply the Built For Mars product psychology framework — extracted from 11 real case studies (Chatbots, Dominos, Flights, HelloFresh, Monzo Perks, Netflix Ads, Nike, Robinhood, Uber Eats, Chase, Headspace) with 800+ annotated slides. Use this skill when: (1) reviewing why users ignore features or resist paying, (2) designing pricing pages or paywalls, (3) understanding dark patterns and ethical alternatives, (4) improving referral or reward mechanics, (5) making personalization actually feel personal, (6) designing CTAs and conversion flows."
---

# BFM Product Psychology Framework

Built For Mars case studies reveal the psychological mechanisms behind user behaviour — why people pay, ignore, cancel, refer, or get frustrated. This skill encodes those mechanisms into an actionable framework.

## How to Use

Given a product question, identify the relevant psychological mechanism(s) and load the corresponding reference file.

**Output format:**
```
## Psychology Analysis: [Topic]

### Mechanism at play
[Which psychological principle applies and why]

### BFM Evidence
[Verbatim quotes from case studies]

### Recommendation
[Concrete, actionable change]

### Watch out for
[Common mistake or dark-pattern version of this]
```

---

## 8 Psychology Categories

| # | Category | Key Question | Reference |
|---|----------|-------------|-----------|
| 1 | **Dark Patterns & Deceptive Design** | Is this persuasion or manipulation? | `references/01-dark-patterns.md` |
| 2 | **Pricing Psychology & Decoy Effect** | How do users perceive value and price? | `references/02-pricing-psychology.md` |
| 3 | **Variable Rewards & Referrals** | What makes a reward loop viral? | `references/03-variable-rewards.md` |
| 4 | **Personalization** | Does the experience feel genuinely personal? | `references/04-personalization.md` |
| 5 | **Expectation Setting** | Do users know what will happen next? | `references/05-expectation-setting.md` |
| 6 | **Feature Perception & Value Anchoring** | Why are users ignoring your best features? | `references/06-feature-perception.md` |
| 7 | **Upstream Thinking & Prevention** | Are you solving problems before they happen? | `references/07-upstream-thinking.md` |
| 8 | **Emotional Design & Moments** | Do users feel something at key moments? | `references/08-emotional-design.md` |

---

## Quick Diagnostic Checklist

- [ ] Pricing page uses only one plan tier (no anchor/decoy)
- [ ] Referral reward is fixed and predictable — no surprise/variable element
- [ ] "Personalised" content is the same for all users with same basic attribute
- [ ] Chatbot/AI flow creates ambiguity about whether user is talking to human
- [ ] Feature announced without showing user the specific value they'll receive
- [ ] CTA label describes the action ("Submit") not the outcome ("Get my report")
- [ ] Paywall appears before user has experienced the value being sold
- [ ] User has to discover they were overcharged rather than being shown proactively
- [ ] Celebration fires at a company milestone, not a user milestone

---

## When to Load Reference Files

Load reference file when:
- User asks "why aren't users paying/upgrading/referring?"
- Reviewing a specific UI pattern (pricing table, reward flow, chatbot)
- Designing a psychological nudge and need BFM precedent

**Load `01-dark-patterns.md`** when evaluating if a design is manipulative vs persuasive.
**Load `02-pricing-psychology.md`** when designing pricing pages, paywalls, or subscription tiers.
**Load `03-variable-rewards.md`** when building referral programs or gamification.
**Load `04-personalization.md`** when personalisation feels hollow or fake.
**Load `05-expectation-setting.md`** when users feel surprised, confused, or misled mid-flow.
**Load `06-feature-perception.md`** when users ignore features that exist and work.
**Load `07-upstream-thinking.md`** when solving for downstream problems (refunds, cancellations, complaints).
**Load `08-emotional-design.md`** when moments feel flat, generic, or miss the user emotional state.
