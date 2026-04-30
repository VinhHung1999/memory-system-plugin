---
name: cmo-strategic-vision-canvas
description: |
  Score, stress-test, and revise a marketing vision statement against the
  Clarity / Alignment / Actionability rubric. Distinguishes a strategic
  vision (5-10yr north star that guides budget, prioritization, and team
  alignment) from a slogan (motivational but not decision-guiding) and from
  positioning (tactical vs competitors). Runs the "managers in the room"
  check + "compass-vs-poster" test. Use when CMO needs to craft, audit,
  or revise a marketing vision — annual planning, post-pivot, post-funding,
  new-CMO onboarding, or board-prep when leadership cannot articulate the
  marketing north star. Auto-trigger on phrases like "marketing vision",
  "north star", "vision statement", "rewrite our vision", "strategic vision",
  "vision audit", "is our vision strategic", "our marketing mission".
---

# CMO Strategic Vision Canvas

## What this does

Takes a marketing vision statement (or a request to write one) and produces:
1. A scored critique on 3 axes — **Clarity**, **Alignment**, **Actionability** (0-3 each, max 9)
2. Verdict: Strategic vision / Worth-revising / Slogan
3. Stress-test diagnostics: "managers in the room" + "compass-vs-poster"
4. A revision suggestion anchored to the company's mission + customer truth + strategic capability
5. (Optional) A CMO charter reframe for the role positioning

**The core problem this solves:** Most marketing visions are slogans ("be #1 in our category", "delight customers"). They sound aspirational but don't guide budget allocation, kill/scale decisions, or cross-team prioritization. This skill catches that and rewrites the vision so line marketers can actually use it.

## When to invoke this skill

- Annual planning kickoff — "what's our marketing vision for the year?"
- After a strategic pivot — old vision no longer fits
- After a funding round / IPO — vision needs to scale to new ambitions
- New CMO onboarding (first 90 days) — write or rewrite the vision
- Board prep — need to articulate marketing's strategic role
- When line marketers can't agree on what the current vision means
- Asked "is our vision strategic enough?" / "rewrite our vision" / "audit our north star"

**Skip when:**
- Need is positioning vs competitors (use positioning frameworks instead — vision and positioning are different layers)
- Tactical campaign question (use other CMO skills)
- Brand identity / visual brand work (different problem)

## When NOT to use

- Question is about competitive positioning, NOT vision (different framework)
- Question is about brand voice / tone / visual identity
- Tactical / campaign-level decisions
- Already-strong vision being revisited for fun (no scope to improve)

## Workflow

1. **Capture inputs** — get the vision statement (or "no vision yet" → start from blank), plus context: company stage, industry, key customer segment, current strategy.
2. **Score the vision** — `scripts/score_vision.py --vision "<text>" --context "<context>"` produces the 3-axis rubric scores + verdict + stress-test results.
3. **Read the rubric reference** — `references/vision-rubric.md` for axis definitions + Airbnb/Tesla/Unilever benchmark visions to compare against.
4. **Generate revision** — if score < 7/9, use `templates/vision-canvas.md` to rebuild: Mission anchor → Customer truth → Strategic capability → Vision statement → Stress-test answers.
5. **Optional — CMO charter** — `templates/cmo-charter.md` reframes the CMO role positioning (function head → growth architect) to support the vision.

## Running the script

```bash
python3 /Users/phuhung/coursera/.claude/skills/cmo-strategic-vision-canvas/scripts/score_vision.py \
  --vision "We will be the most loved brand in fintech" \
  --context "B2B payments SaaS, 200 employees, $30M ARR, mid-market focus"
```

Output: 3-axis scores (0-3 each) + verdict + stress-test + missing-element flags.

If `python3` crashes with pyexpat error, fall back to `python3.13`.

## Output philosophy

The verdict must answer: **"Can a Marketing Manager use this vision to decide which campaigns to kill and which to scale?"**

If yes → strategic vision.
If only motivates but doesn't guide decisions → slogan, rewrite.
If guides some decisions but ambiguous → worth-revising.

DO NOT produce generic "your vision should be inspiring" advice. The script + rubric force concrete, specific critique tied to whether the vision drives budget/roadmap decisions.

A good revision must explicitly state:
- The MISSION ANCHOR (link to company's broader purpose — what the company exists to do)
- The CUSTOMER TRUTH (the specific buyer reality marketing serves)
- The STRATEGIC CAPABILITY (the unique marketing capability this vision builds toward)
- THE VISION STATEMENT (1-2 sentences passing all 3 stress-tests)
- STRESS-TEST ANSWERS (what would line marketers say it means? what budget decision does it drive?)

## References (load on demand)

- `references/vision-rubric.md` — full Clarity/Alignment/Actionability rubric with scoring guide + benchmark visions (Airbnb, Tesla, Unilever, plus 3 anti-patterns)
- `templates/vision-canvas.md` — fill-in canvas for revision
- `templates/cmo-charter.md` — optional CMO role reframe (folded in from charter-reframe candidate)

## Sources

Built from CMO Excellence (Coursera, Hurix Digital, Dec 2025):
- Module 1 Video: "What Makes a Marketing Vision Strategic?"
- Module 1 Reading: "Crafting a Strategic Marketing Vision"
- Module 1 Video: "The Expanding Role of the CMO in Modern Enterprises"

Augmented with: real examples from Airbnb's COVID-recovery vision, Unilever's Sustainable Living, Tesla's clean-energy mission.
