---
name: learn-coursera
description: "Discover, learn from, and turn Coursera courses into Claude Code skills. Searches Coursera for top courses on any topic (design, SEO, data science, etc.) and recommends professional picks; extracts video transcripts, enriches with actionable notes, evaluates skill-worthiness, builds winning skills with eval benchmarks, and packages them into a plugin. Handles single courses and Professional Certificates. Use whenever user wants to find/search/recommend Coursera courses on a topic, learn a Coursera course, extract transcripts, turn a Coursera course into a skill, or mentions 'I want to learn a new skill', 'find new skill', 'learn something new', 'help me pick up X', 'learn from Coursera', 'find Coursera course on X', 'best Coursera course for X', 'coursera skill', 'coursera transcript'. Also triggers on Vietnamese: 'tôi muốn học kỹ năng mới', 'tìm kỹ năng mới', 'tìm khoá học về X', 'học một cái gì mới', 'hoc khoa hoc', 'lay transcript', 'tao skill tu khoa hoc', 'gợi ý khoá học'."
---

# Learn from Coursera Courses

End-to-end pipeline: **discover → extract → enrich → evaluate → build skills → package plugin**.

## The 5 phases

```
Phase 0 (optional): Search Coursera + recommend courses       ~3-5 min
Phase 1: Extract + enrich transcripts                         ~30-60 min per course
Phase 2: Propose + score candidate skills                     ~5 min
Phase 3: Build winning skills with evals                      ~15-30 min per skill
Phase 4 (optional): Package skills into plugin                ~5 min
```

---

## Phase 0: Discover Courses (search + recommend)

Trigger when user gives a **topic/skill** but no specific course URL. Examples:
- "I want to learn design"
- "Tìm khoá học về SEO"
- "Recommend Coursera courses on data science"
- "Best course for product management"

### Step 1 — Clarify intent

Ask concisely if unclear:
- **Topic** — be specific (e.g., "design" → UX design? graphic design? product design?)
- **Goal** — hobby learning? career pivot? skill for current job?
- **Level** — beginner / intermediate / advanced
- **Time commitment** — casual (1-2h/week) vs intensive (10+ h/week)
- **Credential preference** — any course / Specialization / Professional Certificate / Degree

Don't over-ask. If user gives just "learn design", use defaults (intermediate, moderate, any format) and show results.

### Step 2 — Search Coursera

Navigate + scrape:
```bash
playwright-cli open --browser=chrome "https://www.coursera.org/" --headed
playwright-cli state-load ~/coursera/coursera-auth.json  # if exists

# Search URL pattern:
playwright-cli goto "https://www.coursera.org/search?query=<URL_ENCODED_QUERY>&sortBy=BEST_MATCH"

# Filters via URL params (URL-encode):
#   &productType=Course,Specialization,ProfessionalCertificate
#   &productDifficultyLevel=Beginner,Intermediate,Advanced
#   &language=English
```

Extract results:
```bash
playwright-cli eval "async () => {
  await new Promise(r => setTimeout(r, 3000));
  const cards = document.querySelectorAll('[data-testid=\"search-result-card\"], li.cds-9');
  return Array.from(cards).slice(0, 20).map(c => {
    const titleEl = c.querySelector('h3, [data-testid=\"product-title\"]');
    const linkEl = c.querySelector('a[href*=\"/learn/\"], a[href*=\"/professional-certificates/\"], a[href*=\"/specializations/\"]');
    const partnerEl = c.querySelector('[data-testid=\"partner-name\"], .cds-ProductCard-partnerNames');
    const ratingEl = c.querySelector('[data-testid=\"rating\"], .cds-CommonCard-ratingValue');
    const reviewsEl = c.querySelector('[data-testid=\"reviews-count\"], .cds-RatingStat-meta');
    const metaEl = c.querySelector('[data-testid=\"product-metadata\"], .cds-CommonCard-metadata');
    return {
      title: titleEl?.textContent?.trim(),
      url: linkEl?.href,
      partner: partnerEl?.textContent?.trim(),
      rating: ratingEl?.textContent?.trim(),
      reviews: reviewsEl?.textContent?.trim(),
      meta: metaEl?.textContent?.trim()  // often contains duration + level
    };
  }).filter(x => x.title && x.url);
}"
```

Card selectors change periodically. If the eval returns empty, inspect snapshot to find current selectors:
```bash
playwright-cli snapshot
```

### Step 3 — Rank + filter

Apply these heuristics (in order):

1. **Credentialed product types** — rank `Professional Certificate` > `Specialization` > `Course`. Guided Projects and single courses are OK but lower-priority for career skills.
2. **Partner reputation** — Google, Meta, IBM, Stanford, Microsoft, DeepLearning.AI, Anthropic, University-branded > unknown creators.
3. **Enrollment/review count** — filter out courses with < 5,000 enrollments or < 500 reviews unless it's a new release (<6 months).
4. **Rating** — prefer ≥ 4.5/5. Anything under 4.3 = skip.
5. **Recency** — check if content references outdated tools/frameworks. A "social media marketing 2018" course is probably stale.
6. **Skill-worthy topic match** (using same 5-criteria rubric from Phase 2):
   - Tactical > foundational
   - Specific frameworks > general concepts
   - API/tool-heavy > abstract theory

### Step 4 — Cross-reference with web search

Coursera search alone can be noisy. Supplement:
```bash
# Via WebSearch tool or manual:
"best Coursera course for <topic> 2026 reddit"
"Coursera <topic> Professional Certificate review"
```

Reddit discussions + course-review sites (Class Central) often surface consensus picks. Filter for recent posts (past 12 months).

### Step 5 — Present top 5 recommendations

Show user a ranked table:

```markdown
## Top Coursera courses for "<topic>"

| # | Course | Type | Partner | Rating | Reviews | Duration | Why |
|---|---|---|---|---|---|---|---|
| 1 | Google UX Design | Professional Certificate (7 courses) | Google | 4.8 | 120K+ | ~6 months | Career pivot standard; hiring partner network |
| 2 | Meta Front-End Developer | Professional Certificate | Meta | 4.7 | 45K | ~7 months | Tactical + portfolio-ready |
| 3 | Foundations of User Experience Design | Single Course | Google | 4.8 | 80K | 3 weeks | Sample Course 1 of the certificate — try before committing |
...

## Recommendation

For **career pivot** → **Google UX Design Professional Certificate** (comprehensive, hiring-recognized).
For **quick skill add** → **Foundations of User Experience Design** (3 weeks, free preview).

Which do you want to learn? I'll start extraction + skill-building pipeline.
```

### Step 6 — User picks → continue to Phase 1

Once user picks:
- Confirm URL
- If Professional Certificate, offer "one course at a time" flow
- Jump to Phase 1 Step 2 (setup folders)

### Tips for discovery

- **Vietnamese topics** — search in English (Coursera's catalog is mostly English). Translate user's topic: "thiết kế" → "design", "marketing số" → "digital marketing".
- **Very broad topic** — narrow first. "Design" → ask user: UX? UI? graphic? industrial? motion?
- **Very niche topic** — Coursera may not have it. Cross-reference Udemy / YouTube / LinkedIn Learning. If Coursera has nothing good, say so honestly.
- **Free vs paid** — all courses can be audited for free (no certificate, some quizzes locked). Professional Certificates require Coursera Plus ($59/mo) or per-course subscription. Mention this to user.
- **Preview mode** — single courses have "Preview" (free Module 1). Use this to extract a sample before committing to full enrollment.

---

## The remaining phases (extract → build → ship)

---

## Phase 1: Extract & Enrich

### Step 1 — Parse URL + detect course type

User URL patterns:
- Single course: `https://www.coursera.org/learn/<slug>`
- **Professional Certificate** (multi-course): `https://www.coursera.org/professional-certificates/<cert-slug>`
- Google marketing URL: `https://grow.google/certificates/<cert-slug>/`

**If it's a Professional Certificate:** confirm with user — each course needs separate extraction. Expect 3-8 courses per certificate, 30-50 videos each. Offer "one course at a time" flow.

**⚠️ URL slug gotcha:** the URL slug in `/learn/<slug>` often differs from the marketed course title. Example: "Attract and Engage Customers with Digital Marketing" has slug `attract-and-engage-customers` (not `attract-and-engage-customers-with-digital-marketing` which 404s).

**→ Always scrape the certificate landing page first to discover canonical slugs:**
```bash
playwright-cli goto "https://www.coursera.org/professional-certificates/<cert-slug>"
playwright-cli eval "() => Array.from(document.querySelectorAll('a[href*=\"/learn/\"]')).map(a => ({href: a.href, text: a.textContent.trim().substring(0,80)}))"
```

### Step 2 — Setup folders

For single course:
```bash
mkdir -p ~/coursera/<slug>/raw
```

For Professional Certificate (recommend grouping):
```bash
mkdir -p ~/coursera/<cert-slug>/<course-slug>/raw
```

### Step 3 — Open browser + auth

```bash
playwright-cli open --browser=chrome "https://www.coursera.org/" --headed
playwright-cli state-load ~/coursera/coursera-auth.json   # if exists
```

If auth doesn't exist: tell user to log in, then:
```bash
playwright-cli state-save ~/coursera/coursera-auth.json
```

Auth file shared across courses — save once.

### Step 4 — Enroll (IMPORTANT — each course separately)

**⚠️ Non-obvious:** even if user paid for a Professional Certificate, each individual course requires SEPARATE enrollment:

```bash
playwright-cli goto "https://www.coursera.org/learn/<slug>"
```

Then look for `Enroll` button → click → modal appears with `Join Course` button → click.

Use eval to automate:
```js
// Click Enroll (button text starts with "Enroll")
const btns = document.querySelectorAll('button');
for (const b of btns) {
  if (b.textContent.trim().startsWith('Enroll')) { b.click(); break; }
}
// Wait, then click Join Course
setTimeout(() => {
  for (const b of document.querySelectorAll('button')) {
    if (b.textContent.trim() === 'Join Course') { b.click(); break; }
  }
}, 2500);
```

After enrollment: navigate to `/learn/<slug>/home/module/1`. If it redirects back to landing page, enrollment didn't take — retry.

### Step 5 — Discover modules & videos

For each module 1..N:
```bash
playwright-cli goto "https://www.coursera.org/learn/<slug>/home/module/<N>"
playwright-cli eval "async () => {
  await new Promise(r => setTimeout(r, 2500));
  return Array.from(document.querySelectorAll('a[href*=\"/lecture/\"]')).map(a => ({
    href: a.href, text: a.textContent.trim().substring(0, 150)
  }));
}"
```

Iterate modules 1-5 (typical). Module that returns same list as module 1 = doesn't exist (stop).

Save discovery to `_manifest.json` with structure:
```json
{
  "course": "Full course title",
  "slug": "course-slug",
  "modules": [
    {"num": 1, "title": "Module title", "videos": [
      {"id": "abc123", "title": "Video title", "slug": "short-slug", "url": "full lecture URL"}
    ]}
  ]
}
```

### Step 6 — Extract transcripts via bash script

Don't do one-by-one manually. Write a bash script:

```bash
#!/bin/bash
COURSE_DIR="$1"
MANIFEST="$COURSE_DIR/_manifest.json"

EVAL_JS='async () => {
  await new Promise(r => setTimeout(r, 2500));
  const panel = document.querySelector("[role=\"tabpanel\"]");
  if (!panel) return "NO_PANEL";
  const spans = panel.querySelectorAll("span");
  const texts = Array.from(spans).map(s => s.textContent).filter(t => t && t.length > 2
    && !t.includes("Play video") && !t.includes("Language")
    && !t.includes("Interactive Transcript") && !t.includes("navigate through"));
  const deduped = [];
  for (let i = 0; i < texts.length; i += 2) deduped.push(texts[i].replace(/\u200B/g, "").trim());
  return deduped.join(" ");
}'

MODS=$(jq '.modules | length' "$MANIFEST")
for M in $(seq 1 $MODS); do
  COUNT=$(jq ".modules[$((M-1))].videos | length" "$MANIFEST")
  for I in $(seq 0 $((COUNT-1))); do
    URL=$(jq -r ".modules[$((M-1))].videos[$I].url" "$MANIFEST")
    SLUG=$(jq -r ".modules[$((M-1))].videos[$I].slug" "$MANIFEST")
    SEQ=$(printf "%02d" $((I+1)))
    mkdir -p "$COURSE_DIR/raw/module_$M"
    OUT="$COURSE_DIR/raw/module_$M/m${M}_${SEQ}_${SLUG}.txt"
    [ -s "$OUT" ] && continue  # skip if already extracted
    playwright-cli goto "$URL" > /dev/null 2>&1
    sleep 3
    TMPOUT=$(mktemp)
    playwright-cli eval "$EVAL_JS" > "$TMPOUT" 2>&1
    # Extract JSON string between "### Result" and next "###"
    python3 -c "
import re, json
with open('$TMPOUT') as f: content = f.read()
m = re.search(r'### Result\n(.*?)\n### ', content, re.DOTALL)
if m:
    raw = m.group(1).strip()
    try: print(json.loads(raw))
    except: print(raw)
" > "$OUT"
    rm -f "$TMPOUT"
    sleep 1
  done
done
```

Run in **background** for large courses:
```bash
chmod +x /tmp/extract.sh
/tmp/extract.sh "$COURSE_DIR" &   # via Bash tool run_in_background: true
```

**Critical**: `sleep 3` between goto calls — transcript panel is lazy-loaded, needs render time.

### Step 7 — NO_PANEL recovery

If any raw file contains only `NO_PANEL`, the extraction missed. Delete + re-run that specific video:
```bash
rm "$COURSE_DIR/raw/module_X/mX_YY_slug.txt"
# Re-extract that one video manually or via single-video bash invocation
```

### Step 8 — Enrich via parallel subagents (batches)

Spawn 5-8 subagents in parallel, each handling 5-10 videos. Don't do 1-per-subagent (wasteful) or 40-per-subagent (context overflow).

Each subagent prompt:
```
Enrich these N Coursera transcripts.

For each video, read the raw transcript, write enriched .md with EXACT format:

---
name: "<lecture title>"
description: |
  - <actionable bullet 1 — what can be APPLIED, not a recap>
  - <actionable bullet 2>
  - <actionable bullet 3>
  - <actionable bullet 4>
  - <actionable bullet 5 — optional>
---

## Transcript

<full transcript, cleaned: remove "English " prefix, fix typos, preserve content>

Bullets must be ACTIONABLE — what can be APPLIED. Not "lecturer says X" recap.

Base path: <full course path>
Videos:
1. raw/module_1/m1_01_slug.txt → module_1/m1_01_slug.md — "Lecture Title"
2. ...

Write N files. Report "DONE N files" or issues. Under 100 words.
```

Dispatch all batches in parallel in ONE message (multiple `Agent` calls in one response) so they run concurrently.

### Step 9 — Build course README.md

After all enriched .md files exist:
```markdown
---
name: "<course-name>"
description: "<one-line course description>"
---

# <Course Name>

Course X of N in certificate. K video lectures, ~Y hours.

## Module 1: <Title>
- [Lecture title](module_1/m1_01_slug.md) — <one-line actionable takeaway>
- [Lecture title](module_1/m1_02_slug.md) — <takeaway>

## Module 2: <Title>
- ...
```

Use the **first bullet** of each enriched .md's description as the one-line takeaway (it's already actionable).

### Step 10 — Close browser

```bash
playwright-cli close
```

---

## Phase 2: Propose + Score Candidate Skills

After extraction, always run this analysis — prevents creating "fake skills" that LLM already handles.

### Step 1 — Propose 3-5 candidates

Read README.md + scan module titles + first-bullet summaries. Identify:
- **Name** (slug-style)
- **Scope** (1 sentence)
- **Sources** (which lectures feed it)

### Step 2 — Score each candidate (5 criteria)

| Criterion | Scoring |
|---|---|
| **Novelty** — Does LLM already know this? | −3 (common knowledge) to +3 (proprietary/niche framework) |
| **Specificity** — Opinionated vs generic? | 0 (generic) to +3 (specific decision tree, framework, checklist) |
| **Executable** — Can bundle script/template/API? | 0 (markdown only) to +3 (Python script + API + templates) |
| **Substantial** — Enough depth in course? | −1 (1-2 videos) to +2 (full module of tactical content) |
| **Transfer test** — With-skill output clearly better? | 0 (no difference) to +3 (dramatic quality/speed gain) |

**Verdict thresholds:**
- **≥ 8** → Strong create
- **5-7** → Worth creating if bundle is realistic
- **2-4** → Marginal, probably fold into another skill
- **< 2** → DO NOT create — it's a fake skill

### Step 3 — Typical patterns by course level

- **Intro/foundational courses** (usually Course 1 of a certificate) → rarely skill-worthy. Covers general concepts LLMs already know. Expect scores -3 to +2.
- **Tactical/applied courses** (Courses 2-4 of a certificate) → best candidates. Score +5 to +10 typical.
- **Soft-skills courses** (portfolio, interview prep) → almost never skill-worthy.
- **Data/measurement courses** → always high-score because of API integration + deterministic metrics.

### Step 4 — Save candidates (DON'T build immediately)

Write `SKILL_CANDIDATES.md` in the course folder with:
- All candidates + scores + rationale
- Top 2-3 picks with detailed spec (inputs, outputs, bundle assets, SKILL.md outline, open questions)
- User's priority picks marked

This creates a queue. Build later after all courses are extracted.

### Step 5 — For multi-course certificates: accumulate across courses

After each course, update a master `SKILL_CANDIDATES_MASTER.md` at the certificate root. Track:
- Top N picks across ALL courses
- Synergy map (which skills compose into a pipeline)
- Revised build order (easy→hard: markdown-only first, OAuth-requiring last)

---

## Phase 3: Build Winning Skills

Only build skills that scored ≥5. Each skill follows the same loop.

### Per-skill loop

1. **Create dirs**: `~/.claude/skills/<name>/{scripts,references,templates}` + workspace dir `~/.claude/skills/<name>-workspace/iteration-1/`

2. **Write SKILL.md** — YAML frontmatter (name + triggering description, "pushy" style) + body:
   - When it triggers
   - Workflow steps
   - When NOT to use
   - Running scripts
   - Output philosophy
   - References list

3. **Write script(s)** in `scripts/` — prefer deterministic Python:
   - Self-contained (minimal deps)
   - Standalone CLI (argparse)
   - Known macOS gotcha: **Python 3.14 pyexpat bug** — test with `python3.13` fallback
   - Argparse `%` char escape: avoid `%` in help strings (crashes 3.14) — use `"percent"` instead

4. **Write references** in `references/` — deep-dive docs loaded on demand:
   - Benchmarks / formulas / thresholds
   - Playbooks for diagnostic flows
   - Tool-specific syntax (per-vendor)
   - Compliance / privacy guardrails
   - Keep each ~200-400 lines, include table of contents if larger

5. **Write templates** in `templates/` — ready-to-paste files (HTML, CSV, MD prompts)

6. **Smoke test the script** — run locally, verify output shape

7. **Set up evals** — create `evals/evals.json`:
   ```json
   {"skill_name": "<name>", "evals": [
     {"id": 0, "name": "typical-task", "prompt": "...", "expected_output": "..."},
     {"id": 1, "name": "vague-prompt", "prompt": "...", "expected_output": "..."},
     {"id": 2, "name": "edge-case", "prompt": "...", "expected_output": "..."}
   ]}
   ```

   3 evals cover: (a) typical happy-path, (b) vague prompt testing disambiguation, (c) edge case / domain-specific gotcha.

8. **Dispatch 6 eval subagents in parallel** — 3 test cases × (with-skill, baseline without):
   - With-skill: point subagent at `~/.claude/skills/<name>/`, instruct to read SKILL.md first
   - Baseline: explicitly say "do NOT use any skill from ~/.claude/skills/"
   - Save outputs to `<name>-workspace/iteration-1/eval-<N>-<name>/{with_skill,without_skill}/outputs/response.md`

9. **Write benchmark.md** when all 6 complete:
   - Evaluation criteria (4-7 assertions per eval type)
   - Per-eval with-skill vs baseline comparison table
   - Pass-rate summary
   - Observations (what skill won on, what baseline matched, any bugs found)
   - Recommendation (ship / iterate)

10. **Fix bugs caught by evals** — evaluation subagents often find real bugs (e.g., script crashes, missing references). Fix immediately before shipping.

### Target benchmark results

A good skill hits:
- **Pass rate: 85-95% with skill, 30-55% baseline** (delta +30-60 percentage points)
- **Output quality**: with-skill is either much more structured OR has novel insights baseline missed

If with-skill pass rate < 75% or baseline > 70%, the skill design is off. Consider:
- SKILL.md description too vague → subagents didn't know when to invoke
- Script not adding real value → LLM could compute inline
- References not applied → subagent didn't know to read them

---

## Phase 4 (optional): Package skills into plugin

When 5+ skills exist on one topic, package as a Claude Code plugin for distribution.

### Structure

```
<repo>/
├── .claude-plugin/
│   └── marketplace.json          ← lists all plugins
└── plugins/
    └── <plugin-name>/
        ├── .claude-plugin/
        │   └── plugin.json       ← name, version, description, author, license
        ├── README.md             ← list skills + benchmarks + install
        └── skills/
            ├── skill-1/          ← copied from ~/.claude/skills/
            ├── skill-2/
            └── ...
```

### Steps

1. `mkdir -p <repo>/plugins/<plugin-name>/skills`
2. `cp -R ~/.claude/skills/<skill>/ <repo>/plugins/<plugin-name>/skills/` for each skill
3. Write `<repo>/plugins/<plugin-name>/.claude-plugin/plugin.json` with metadata
4. Write `<repo>/plugins/<plugin-name>/README.md` with skill table + benchmark summary + install guide
5. Update `<repo>/.claude-plugin/marketplace.json` — add entry to "plugins" array
6. Validate JSON: `python3 -c "import json; json.load(open('X.json')); print('valid')"`

Users can then `/plugin install <plugin-name>` to get the full set.

---

## File structure

```
~/coursera/<cert-slug>/                 # Professional Certificate root
  SKILL_CANDIDATES_MASTER.md            # Cross-course candidate tracker
  <course1-slug>/
    _manifest.json                      # Video metadata (id, title, slug, url)
    README.md                           # Enriched course index
    SKILL_CANDIDATES.md                 # Per-course candidate analysis
    raw/module_1/m1_01_slug.txt         # Raw transcripts
    module_1/m1_01_slug.md              # Enriched (frontmatter + transcript)
    module_1/m1_02_slug.md
    ...
  <course2-slug>/
    ...

~/.claude/skills/<skill-name>/          # Built skills (installed locally)
  SKILL.md
  scripts/*.py
  references/*.md
  templates/*.html|.txt|.md
  evals/evals.json

~/.claude/skills/<skill-name>-workspace/ # Eval workspaces
  iteration-1/
    eval-0-<name>/{with_skill,without_skill}/outputs/response.md
    benchmark.md
```

---

## Common gotchas (from real runs)

### Extraction phase

- **Python 3.14 pyexpat bug** on some macOS installs → scripts crash with `Symbol not found: _XML_SetAllocTrackerActivationThreshold`. **Fallback**: invoke scripts with `python3.13` instead of `python3`.
- **Auth state expired mid-session** → browser redirects to login. Re-login and `state-save` again.
- **Course slug mismatch** → marketed title ≠ URL slug. Always scrape certificate page to find canonical slug.
- **Each certificate course needs separate Enroll + Join Course click** — paying for certificate doesn't auto-enroll individual courses.
- **`[MUSIC]` transcripts** — some intro/outro videos have no real transcript, just music cues. Placeholder the enrichment.

### Enrichment phase

- **Subagent batch size**: 5-10 per subagent is optimal. Smaller = too many API calls. Larger = context overflow.
- **"Description must be actionable"** — repeat this 3 times in the subagent prompt. LLMs default to recap.

### Skill-building phase

- **Fake skill trap**: if scoring < 2, the skill adds no value. Don't build for completeness. Skip honestly.
- **Argparse `%` escape**: `%` in help strings crashes Python 3.14. Use `"percent"` instead.
- **OAuth-heavy skills**: always include a CSV/pasted-numbers fallback mode so users can try without setup.
- **Traffic-light output (🟢🟡🔴)**: stakeholders don't read tables, they scan. Use this pattern for any reporting skill.

### Eval phase

- **Baseline must explicitly avoid the skill**: "Do NOT use any skill from ~/.claude/skills/" in the prompt. Otherwise subagent may invoke it anyway.
- **Eval subagents catch real bugs** — they test the skill from fresh context, often hit issues you missed. Fix before shipping.

---

## Troubleshooting quick reference

| Problem | Fix |
|---|---|
| Empty transcript / NO_PANEL | `playwright-cli reload`, `sleep 3`, retry. If persists, video has no transcript (rare). |
| Duplicate text in output | `i+=2` dedup in extraction JS — Coursera renders each line in 2 spans. Already handled in Step 6 script. |
| Auth expired | Delete `~/coursera/coursera-auth.json`, restart from Step 3. |
| Module locked (Preview mode) | Ask user to start free trial OR extract only Module 1 (free preview). |
| "Enroll" button doesn't appear | User already enrolled — skip to Step 5 directly. |
| All videos return same transcript | Browser session stale. Close + reopen. |
| Script crashes `pyexpat` error | Use `python3.13` instead of `python3`. |
| Subagent returns "DONE" but files missing | Check permissions. Sometimes `Write` works but `Bash mkdir` denied — use Write directly (it creates parent dirs). |
