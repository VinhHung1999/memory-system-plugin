# Campaign Comparison Prompt Template

From Course 7 M4 m4_05 "Use AI to compare two campaign proposals".

Use when deciding between Campaign A and Campaign B and want a neutral second opinion.

## Full T-C-R-E-I prompt

```
**Task (T):** Evaluate the advantages and disadvantages of Campaign A vs Campaign B. Recommend which to pick OR propose a hybrid/third option if both have fatal flaws.

**Context (C):**
- We need to decide by {deadline}
- Primary goal: {business_goal}
- Budget per campaign: {budget}
- Success metric: {KPI}
- Team capacity: {constraint}
- Campaign A summary: {full_A_description — 3-5 sentences}
- Campaign B summary: {full_B_description — 3-5 sentences}
- Past similar campaign: {relevant_prior_result_if_any}

**References (R):**
- Brand voice: {voice}
- Audience we're targeting: {audience_segment}
- Our biggest fear for this spend: {risk_concern}

**Evaluate (E):**
Structure your comparison as:

| Dimension | Campaign A | Campaign B |
|---|---|---|
| Expected reach | ... | ... |
| Expected conversion | ... | ... |
| Production effort | ... | ... |
| Risk profile | ... | ... |
| Fit with brand voice | ... | ... |
| Measurement clarity | ... | ... |

Then provide:
- **Winner (or Hybrid):** with one-sentence rationale
- **If I'm wrong about assumptions in the recommendation, what would flip it?**
- **What's the minimum spend test to validate the recommendation before going all-in?**

**Iterate (I):**
After initial comparison:
- "Steelman the losing option — what's the strongest case FOR it?"
- "If our budget was cut in half, which would you pick?"
- "Draft a 2-week pilot version of the winning option to derisk"
```

## How to use

Great for: budget allocation, channel A vs B, message framing A vs B, launch timing decisions.

## Expected output structure

- Comparison table
- Winner + rationale
- Assumption flips (fragility check)
- Minimum-cost validation test

## Common failure modes

- **AI sides with whichever option you wrote longer** → write both with equal detail.
- **Wishy-washy "both are good"** → Force a winner. "You MUST pick one or propose a hybrid — no 'it depends'."
- **Misses asymmetric risk** → Explicitly ask about tail risks, not just expected value.
