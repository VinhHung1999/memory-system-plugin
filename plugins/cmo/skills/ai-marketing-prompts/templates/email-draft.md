# Email Draft Prompt Template

From Course 7 M4 m4_06 "Improve your email marketing with AI".

Key insight: start broad, then iterate. Request 4 different personalities, pick closest, then reprompt for variants.

## Full T-C-R-E-I prompt — initial broad round

```
**Task (T):** Draft 4 different versions of a {email_type} email for {campaign_goal}. Each version should have a distinct brand personality so I can pick the one closest to our voice.

**Context (C):**
- Business: {company_description}
- Email type: {acquisition / welcome / newsletter / promotional / retention}
- Audience segment: {segment_description}
- Goal: {specific_outcome — click to landing, buy now, book demo, etc.}
- Offer/hook: {what_they_get}
- Deadline/urgency: {if_any}

**References (R):**
- 4 personality options to try (pick different angles per version):
  1. **Playful** — light humor, casual
  2. **Authoritative** — data-driven, expert tone
  3. **Story-led** — open with narrative/customer moment
  4. **Minimalist** — short, punchy, one-CTA-focus
- Current brand voice baseline: {voice_adjectives}

**Evaluate (E):**
For each version, include a 1-line note on:
- Which subscriber segment it would resonate with most
- Risk (too informal? too corporate? brand-voice mismatch?)

**Iterate (I):**
After I pick a version, I'll reprompt with:
- "Take version {N} and write 2 variants — tighten body, change CTA wording"
- "Write the subject line A/B variants (3 options, clarity > clever)"
- "Shorten by 30% while keeping the hook"
```

## After first round — iteration prompt

```
Based on the 4 versions you just wrote:
- I'm picking version {N} because {reason}
- Take that version and generate 3 subject line A/B variants (30-60 chars, clarity-first)
- Tighten the body by 30% without losing the {key_element}
- Swap the CTA from "{old_CTA}" to be more action-verb-led
```

## Why the 4-personality approach

Generating 4 at once forces AI to diverge. Generating 1 at a time, AI defaults to bland average. The diversity-forcing function is the trick.

## Common failure modes

- **All 4 versions sound the same** → AI defaulted. Re-prompt with stricter personality constraints: "Version 1 MUST be funny, Version 2 MUST open with a data point, Version 3 MUST be a story, Version 4 MUST be under 80 words."
- **Too long** → Explicitly request word count. "Body under 120 words."
- **Generic CTAs** → Provide your CTA style guide or examples of past CTAs that worked.

## Pair with `email-campaign-builder`

For full campaign (segmentation, KPIs, HTML), use `email-campaign-builder` skill.
For quick copy iteration, this skill is faster.
