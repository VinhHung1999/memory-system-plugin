---
name: ux-bfm-purchases-subscriptions
description: "Apply the Built For Mars (BFM) purchases & subscriptions framework — based on 8 real UX case studies (Audible, Dominos, Flights Ch.3, Hellofresh, Netflix, Zara, Delta, WSJ). Use this skill when asked about: checkout friction, purchase abandonment, subscription conversion, pricing display, hidden fees, trust at payment, free trial design, post-purchase UX. Trigger on phrases like 'users abandon cart', 'checkout friction', 'low purchase conversion', 'subscription signup', 'pricing page', 'free trial', 'add-on fees', 'mobile purchase'."
---

# BFM Purchases & Subscriptions Framework

8 BFM case studies reveal why users abandon at checkout and what converts them. This skill encodes those mechanisms.

## How to Use

Identify which purchase failure category applies, load the relevant reference file, and apply the framework.

**Output format:**
```
## Purchase Analysis: [Topic]

### Why users are dropping off
[Which purchase failure mechanism applies and why]

### BFM Evidence
[Verbatim quotes from case studies]

### Recommendation
[Concrete, actionable change]

### Watch out for
[Common mistake — the dark-pattern version of this fix]
```

---

## 5 Purchase Failure Categories

| # | Category | Key Question | Reference |
|---|----------|-------------|-----------|
| 1 | **Decision Complexity at Checkout** | Are too many options / hidden information causing abandonment? | `references/01-decision-complexity.md` |
| 2 | **Pricing Architecture & Hidden Fees** | Does the total price reveal itself too late? | `references/02-pricing-hidden-fees.md` |
| 3 | **Trust & Purchase Anxiety** | Does the user feel safe handing over their money right now? | `references/03-trust-purchase-anxiety.md` |
| 4 | **Subscription Model Design** | Is the trial/subscription framing working against conversion? | `references/04-subscription-design.md` |
| 5 | **Post-Purchase Confirmation** | Does the experience close well — or leave users anxious after paying? | `references/05-post-purchase.md` |

---

## Quick Diagnostic Checklist

- [ ] Checkout presents 3+ competing payment options without clear guidance on which to choose
- [ ] Final price is significantly higher than the price shown on the product page
- [ ] Add-on fees (baggage, seat, delivery) revealed only at the last step
- [ ] No security indicators, reviews, or return policy visible at the payment step
- [ ] Free trial requires credit card with no pre-announcement of charge date
- [ ] Subscription page lists features, not personal ROI ("what you'll save/gain")
- [ ] Post-purchase confirmation is a generic "thank you" with no next step
- [ ] Mobile checkout requires more than 3 form fields on one screen

---

## When to Load Reference Files

**Load `01-decision-complexity.md`** when users abandon mid-checkout, when payment options are confusing, or when cognitive load at point of purchase is high.

**Load `02-pricing-hidden-fees.md`** when total price is revealed late, when add-ons stack at checkout, or when price shown in search differs from final price.

**Load `03-trust-purchase-anxiety.md`** when conversion rate is low despite good product, or when users get to payment and stop.

**Load `04-subscription-design.md`** when designing free trials, subscription paywalls, or plan selection pages.

**Load `05-post-purchase.md`** when return rate is high, when users contact support after purchase, or when post-purchase NPS is low.
