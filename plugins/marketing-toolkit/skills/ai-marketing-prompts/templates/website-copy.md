# Website Copy A/B Variants Prompt Template

From Course 7 M4 m4_07 "Brainstorm website copy ideas with AI".

Use for landing page hero, CTA copy, value-prop sections, feature descriptions.

## Full T-C-R-E-I prompt

```
**Task (T):** Given my current {page_section} copy, produce 2 additional versions so all 3 can be A/B tested. Each version should test a different hypothesis about what will convert better.

**Context (C):**
- Page: {page_url_or_description}
- Section: {hero / CTA / value-prop / testimonial-section / feature-list}
- Current copy (Version A):
  ```
  {paste_current_copy}
  ```
- Goal of this section: {get_click / generate_lead / reduce_bounce / increase_understanding}
- Target audience: {segment}
- Current metric: {current_CTR_or_conv_rate_if_known}

**References (R):**
- Brand voice: {adjectives}
- Competitor doing this well: {competitor_example_text}
- Style constraint: {must_include / must_avoid}

**Evaluate (E):**
For each new version (B and C), state:
- **Hypothesis** — what user-behavior theory you're testing (e.g., "shorter beats longer for mobile scanners")
- **Expected winner** and your confidence (high/medium/low)
- **Risk** — what could make this version LOSE to A

Make the 3 versions genuinely different, not tiny wording tweaks.

**Iterate (I):**
After the 3 versions:
- "Pick the one you think most likely to win. Generate 2 micro-variants (wordier + punchier)."
- "Add preheader text / subheadline to each version"
- "Generate button copy options for each (3 per version)"
```

## Example hypotheses to test

Pick ≥ 2 different hypotheses across your 3 variants:
- **Length**: long-form with detail vs short direct punch
- **Tone**: emotional/aspirational vs factual/functional
- **Outcome framing**: "Save X" vs "Avoid Y" (gain vs loss)
- **Specificity**: concrete number vs general benefit
- **Social proof position**: above-the-fold vs below
- **CTA verb**: "Start" vs "Get" vs "Try" vs "See"

## Common failure modes

- **All 3 versions sound the same** → No genuine hypothesis difference. Force explicit divergence.
- **Lost the brand voice** → Voice example wasn't concrete enough. Paste 2-3 actual past headlines as reference.
- **Too meta/salesy** → "Limit each version to language a real person would use on a call with a friend."

## After A/B testing

Pair with `ab-test-designer` skill:
1. Run sample-size calc to determine test duration
2. Use `ab_significance.py` to evaluate results
3. Ship the winning variant
