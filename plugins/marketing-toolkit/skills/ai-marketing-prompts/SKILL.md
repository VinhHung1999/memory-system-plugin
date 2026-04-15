---
name: ai-marketing-prompts
description: Craft high-quality AI/LLM prompts for marketing tasks using the T-C-R-E-I framework (Task, Context, References, Evaluate, Iterate) from Google's Digital Marketing certificate. Provides 7 battle-tested prompt templates for common marketing jobs - audience research, strategy ideation, campaign comparison, email copy, website copy, clustering customer feedback, and LinkedIn announcement drafts. Use this skill whenever the user wants to write a prompt for ChatGPT/Claude/Gemini, improve an existing AI prompt, use AI for marketing work (audience research, copywriting, strategy, survey analysis), or is frustrated that AI output isn't useful — even if they don't mention "prompt".
---

# AI Marketing Prompts (T-C-R-E-I Framework)

Turns fuzzy marketing questions into structured prompts that actually work. Based on Course 7 Module 4 of Google's Digital Marketing certificate — the T-C-R-E-I framework + 7 concrete prompt recipes. Mnemonic: **"Thoughtfully Create Really Excellent Inputs."**

## When this triggers

User is about to use an LLM (ChatGPT, Claude, Gemini, Copilot) for a marketing task and wants the output to be good on the first try. Phrasings: "help me write a prompt", "how should I ask AI", "my AI output is generic", "improve this prompt", "use AI to [do marketing task]".

**NOT** the right tool for: general prompt engineering for non-marketing (code, research, etc.), building agents with tools, or explaining what AI can do.

## The T-C-R-E-I framework

Every good prompt has 5 parts:

| | Stand for | What to include |
|---|---|---|
| **T** | Task | One clear verb sentence — what exactly do you want? |
| **C** | Context | Who you are, what the business is, what's at stake |
| **R** | References | Examples of what good looks like (voice samples, past wins, style guides) |
| **E** | Evaluate | Ask the AI to critique its own output before presenting it |
| **I** | Iterate | Plan to refine — first output is a draft, not a deliverable |

### Example — weak vs T-C-R-E-I

**Weak:** "Write an Instagram caption for my plant shop."

**T-C-R-E-I:**
> **Task:** Write 3 Instagram caption options (120-180 chars each) announcing the restock of our rare Philodendron White Princess.
>
> **Context:** I'm a 2-person rare houseplant shop (PlantCo) serving home gardeners 25-45. Brand voice is friendly, educational, earnest — we avoid hype words and exclamation points. Past captions performed well when they led with a species fact or a plant-care insight.
>
> **References:** Voice example — "Repotting season is here. A quick tip: most houseplants want their new pot just 1 inch wider than the old one. Going bigger = soggy roots."
>
> **Evaluate:** After drafting, flag which caption is most on-voice, which would likely get the most saves, and which if any feel off-brand or hype-y.
>
> **Iterate:** Then generate 2 more versions of the strongest one with slightly different opening hooks.

Better output on first try, every time.

## Workflow

1. **Identify task type** — match to one of the 7 recipes in `references/` (or say "custom" if it doesn't match)
2. **Gather T-C-R-E-I inputs** — ask user concisely for each of the 5 parts (or infer from context)
3. **Build the prompt** — fill the matching template
4. **Present the prompt** — clean, ready to paste into ChatGPT/Claude/Gemini
5. **Offer to run it** — if the user wants, execute the prompt inline (Claude Code environment) or remind them how to iterate

## The 7 recipes

From Course 7 Module 4 lectures m4_02..m4_07:

1. **Audience research** — `templates/audience-research.md`
2. **Marketing strategy ideation** — `templates/strategy-ideation.md`
3. **Compare two campaigns** — `templates/campaign-comparison.md`
4. **Email marketing drafts** — `templates/email-draft.md`
5. **Website copy variants** — `templates/website-copy.md`
6. **Cluster customer feedback (surveys, reviews)** — `templates/cluster-feedback.md`
7. **LinkedIn / social announcement** — `templates/linkedin-announcement.md`

Each template has:
- T (task phrasing)
- C slots to fill (your context)
- R slots (where to paste your examples/voice samples)
- E (self-critique instruction)
- I (follow-up prompts to run)

## Why T-C-R-E-I matters

Most "AI doesn't help my marketing" complaints trace to a missing T-C-R-E-I element:
- **Missing T** — vague task ("help me with marketing") → generic output
- **Missing C** — no audience/voice context → off-brand output
- **Missing R** — no examples → AI defaults to average-internet-style
- **Missing E** — no self-critique → AI confidently delivers weak output
- **Missing I** — expecting one-shot perfection → frustration when it's not

The framework forces discipline. It also works across ChatGPT, Claude, Gemini, Copilot — not tool-specific.

## References

- `references/common-mistakes.md` — anti-patterns in marketing AI prompts with fixes
- `references/voice-extraction-guide.md` — how to describe brand voice in a way AI can apply
- `references/privacy-guardrails.md` — what NOT to paste into public LLMs (customer data, proprietary strategy)

## Output philosophy

The skill produces a **ready-to-paste prompt**, not marketing content. Never confuse the two. When the user asks "write me marketing copy", the right move is:
1. Use `ai-marketing-prompts` to craft the prompt
2. Either run it here OR hand the prompt to the user for their preferred LLM

This skill's job is to make the NEXT call (to an LLM) produce great output. It's a meta-skill.

## Iteration examples

First pass might produce "3 OK captions". Good iteration prompts:
- "Pick the strongest. Now write 2 variants that go harder on the educational angle."
- "All 3 feel too similar. Give me 3 more with 3 different opening hook types: question, stat, BTS story."
- "These are too long. Cut each to under 80 words while preserving the voice."

Teach users to expect 2-3 iterations as normal, not failure.
