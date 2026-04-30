# Audience Research Prompt Template

From Course 7 M4 m4_03 "Use AI to understand your audience".

## Full T-C-R-E-I prompt

```
**Task (T):** Analyze the target market for {product_category} and produce a prioritized list of audience segments with pain points, decision criteria, and where they spend time online.

**Context (C):**
- I'm a marketer at {company_name}, a {company_size} {business_type}
- We're exploring / launching {specific_product_or_service}
- Our current audience is {current_audience_description}
- Our goal is {specific_business_goal}
- Region/market: {geography}
- Budget for acquisition: {budget_signal — "tight", "moderate", "generous"}

**References (R):**
- Example of a customer that's a great fit: {describe_one_real_customer}
- Example of a customer that looked right but didn't convert/retain: {describe_one_anti_fit}
- Competitor who serves similar audience: {competitor_name} — their positioning is {how_competitor_positions}

**Evaluate (E):**
Before finalizing, check:
1. Which 2-3 segments have the strongest fit with our product?
2. Which segments are we likely over-estimating? (wishful thinking vs real demand)
3. Any segments you'd flag as risky (regulatory, ethical, sustainability)?

**Iterate (I):**
After delivering initial analysis:
- Deep-dive into the #1 segment with day-in-the-life narrative
- Generate 3 specific marketing angles for that segment
- Suggest 3 channels (not generic "social media" — specific platforms/publications/communities)
```

## How to use

1. Fill the {variables} with your real info
2. Paste into ChatGPT/Claude/Gemini
3. Iterate with the follow-up prompts after initial output

## Expected output structure

- **Audience segment table** with name, size estimate, pain points, decision criteria
- **Prioritization** with rationale
- **Risk flags** per segment
- **Pre-populated follow-up prompts** the AI suggests for deeper dives

## Common failure modes

- **Too generic** → you probably skipped Context. Re-add real customer descriptions.
- **Over-optimistic segments** → Evaluate step missing or ignored. Explicitly ask "which are we over-estimating?"
- **No regulatory flags** → Explicitly add "include any compliance/ethical concerns per segment"
