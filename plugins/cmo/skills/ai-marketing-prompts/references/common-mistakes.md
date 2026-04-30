# Common Mistakes in Marketing AI Prompts

## 1. Asking for "a marketing plan" with no context

**Bad:** "Give me a marketing plan for my startup."

**Why:** AI has no idea of industry, audience, budget, stage. Output is a generic template that's useless.

**Fix:** Add all T-C-R-E-I elements. Paste real info.

## 2. Missing brand voice examples

**Bad:** "Write in a friendly voice."

**Why:** "Friendly" means different things (casual/warm/joking/inclusive/etc.). AI defaults to generic friendly.

**Fix:** Paste 2-3 real examples of past copy that hit the voice. "Match this tone: {example}."

## 3. Accepting the first output

**Bad:** Copy first version, paste into email, send.

**Why:** First output is always ~70% of best output. AI has no iteration signal unless you give it one.

**Fix:** Always do at least 1 iteration. "What would you improve about your own output?" OR "Rewrite the weakest section."

## 4. Not asking for self-critique

**Bad:** "Write 3 taglines."

**Why:** AI generates 3, all sound equally good because there's no evaluation pressure.

**Fix:** Add the E in T-C-R-E-I. "Rank these by which I should ship first + why. Flag any weaknesses."

## 5. Vague audience descriptions

**Bad:** "Target: small business owners."

**Why:** Small business owner in SaaS B2B is nothing like small business owner in local services. Generic targeting = generic output.

**Fix:** Specific persona: "B2B SaaS founders at 5-20 person teams, typically technical, skeptical of marketing-ese, read Hacker News."

## 6. Over-constraining early

**Bad:** Giving 20 rules before asking for draft.

**Why:** AI tries to satisfy all rules simultaneously → mediocre output that passes rules but has no spark.

**Fix:** Start broad (few rules) → iterate to tighten. "First pass: prioritize {goal}. Later passes will enforce other constraints."

## 7. Privacy violations

**Bad:** Pasting customer names + emails + order IDs.

**Why:** Public LLMs may use your prompts for training. You've leaked customer data.

**Fix:** Anonymize before pasting. "Customer X said..." "Order ID abc123." See `privacy-guardrails.md`.

## 8. One-prompt, one-output thinking

**Bad:** "Write my full 6-month marketing strategy."

**Why:** AI tries to generate one massive output, everything is shallow.

**Fix:** Break into stages. "First, pick the #1 channel. Then we'll deep-dive that channel. Then we'll add secondary channels."

## 9. Not using references (the R in T-C-R-E-I)

**Bad:** "Write in our style."

**Why:** AI has no clue what your style is.

**Fix:** Paste 2-3 actual past samples + explicitly note what makes them on-brand.

## 10. Treating AI output as truth

**Bad:** AI says "Instagram is best for B2B SaaS" → you believe it.

**Why:** AI is trained on general internet text. May be wrong for your specific context or outdated.

**Fix:** Treat AI output as a strong first draft. Validate claims against real data. When AI gives statistics, ask for sources (or check yourself).

## 11. Expecting the LLM to "just know"

**Bad:** "You know what I mean."

**Why:** It doesn't. Prior conversation turns don't carry over unless you're in a session/thread.

**Fix:** Re-include relevant context every time you start a new task. It's cheap.

## 12. Using AI for the wrong tasks

AI is GREAT for: ideation, rewriting, clustering, summarization, structured reformatting.
AI is MEDIOCRE for: factual research (check sources), real-time data (outdated), highly creative/original breakthrough ideas.
AI is BAD for: decisions requiring specialized expertise (legal, medical, heavy regulatory), sensitive situations requiring empathy + nuance.

Don't force AI into the wrong jobs.
