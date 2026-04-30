---
name: qc-web-testing
description: >
  QC web apps using Playwright CLI interactive exploration + automation script generation.
  Agent explores site interactively via playwright-cli, evaluates pass/fail with screenshots,
  generates automation scripts, and maintains project memory. Use this skill whenever the user
  wants to QC a web app, test a flow, run regression tests, or generate automation scripts.
  Triggers on: "QC web", "test web", "kiểm tra web", "test flow web", "chạy regression web",
  "sinh script test web", "web QC", "quality check web".
---

# QC Web Testing

QC web apps through interactive Playwright CLI exploration. Agent controls the browser in real-time, evaluates quality, then generates reusable automation scripts.

## FIRST: Read Project Memory

When this skill loads, IMMEDIATELY read project memory before doing anything else:

```
Read file: ./qc-workspace/.memory/app-knowledge.md
```

If the file exists → you already know this site's navigation, selectors, edge cases. Use this knowledge to skip redundant exploration and go faster.

If the file doesn't exist → this is a new project. You'll build knowledge as you QC.

---

## Prerequisites

`playwright-cli` available on PATH (or fall back to `npx playwright-cli`). Verify with `playwright-cli --version`.

## Subagent Capabilities

The `qc-web` subagent can do the following. Use these to craft your instructions:

### Session Management (you do this directly via Bash, not subagent)
```bash
# Named browser session per flow
playwright-cli -s="s1" open https://app.example.com --persistent
playwright-cli -s="s1" snapshot --filename=/tmp/home.yml
playwright-cli -s="s1" screenshot --filename=/tmp/home.png
playwright-cli -s="s1" close
```

### What You Can Ask the Subagent To Do

| Capability | Instruction Example |
|-----------|---------------------|
| Snapshot | "Snapshot the current page" |
| Screenshot | "Screenshot the current page" |
| Click by ref | "Click element e5 (the Login button)" |
| Fill input | "Fill e3 with 'user@example.com'" |
| Type text | "Type 'hello world'" |
| Press key | "Press Enter" / "Press ArrowDown" |
| Select option | "Select 'option-value' in dropdown e9" |
| Check/uncheck | "Check the checkbox e12" |
| Hover | "Hover over e4" |
| Upload file | "Upload ./document.pdf" |
| Navigate | "Goto https://example.com/login" |
| Back/forward | "Go back" / "Go forward" / "Reload" |
| Wait for text | "Wait until text 'Success' appears" |
| Eval JS | "Eval document.title" |
| Tabs | "Open new tab https://..." / "Select tab 0" |
| Dialog | "Accept dialog" / "Dismiss dialog" |
| Resize | "Resize to 1920x1080" |

### Selector Priority (subagent follows this automatically)
1. ARIA role + accessible name (from snapshot refs like `e5`) — most stable
2. Visible text
3. `data-testid` / `data-test`
4. CSS selector
5. XPath — last resort

Always prefer using **snapshot refs (`e1`, `e2`, ...)** returned by `playwright-cli snapshot` — they are the canonical way to target elements.

---

## Workspace Structure

```
qc-workspace/                          ← created at user's working directory
  .memory/
    app-knowledge.md                   ← accumulated knowledge per project
  flows/                               ← one folder per QC flow
    checkout-flow/
      test-cases.md                    ← Step 0
      explore-log.md                   ← Step 2 (subagent + QC Agent write here)
      qc-report.md                     ← Step 3 (initial QC notes)
      automation-script.py             ← Step 4 (uses playwright python lib)
      screenshots/                     ← exploration screenshots
      snapshots/                       ← .yml snapshots from playwright-cli
      runs/                            ← each ad-hoc script run
        20260407_143022/
          report.html                  ← self-contained HTML (embedded screenshots)
          result.json                  ← machine-readable result
          screenshots/
  regression/                          ← regression runs (run_regression.py)
    20260407_170000/
      summary.html                     ← aggregate report linking per-flow reports
      checkout-flow/
        report.html
        result.json
        screenshots/
      login-flow/
        report.html
        result.json
        screenshots/
  flows.json                           ← optional: default args per flow
```

---

## QC Workflow

**IMPORTANT**: All paths must be **absolute**. At the start, resolve the workspace path from the user's current working directory and use it everywhere (including when calling subagent).

```
WORKSPACE=$(pwd)/qc-workspace
```

### Step 0: Write Test Cases
Before exploring, write test cases and save to `$WORKSPACE/flows/{flow}/test-cases.md`. Ask user to confirm before proceeding.

As you explore in Step 2, come back and **annotate the test case with any element uniqueness gotchas you discover** — ambiguous button labels, recurring popups (cookie banners, newsletter modals), conditional screens, cached state (logged-in session, saved cart) that alters flow, etc. Test cases aren't just a to-do list; they're the spec the script will encode. Gotchas noted here save script iterations later.

### Step 1: Setup

1. Create workspace: `mkdir -p $WORKSPACE/flows/{flow}/screenshots $WORKSPACE/flows/{flow}/snapshots`
2. Check `playwright-cli` is available.
3. **Cold-start the browser before exploring** — close any existing session, launch fresh without cached state. This is critical: if you explore from a warm state (already logged in, cookie banners already dismissed, cart already populated), your script will later fail on a cold launch because it won't see the cookie banner / login wall / empty-cart state you accidentally skipped. Explore the site from the same state the script will face in production:
```bash
playwright-cli -s="{flow}" close 2>/dev/null || true
playwright-cli -s="{flow}" delete-data 2>/dev/null || true
```
4. Start CLI session:
```bash
playwright-cli -s="{flow}" open {url}
```
Use `--persistent` only if the flow explicitly needs a saved profile (e.g. testing signed-in state).

### Step 2: Explore + QC
Use **`qc-web` subagent** (via Agent tool with `subagent_type: "qc-web"`) for page interaction to avoid context overflow.

**How to call**:
```
Agent tool:
  subagent_type: "qc-web"
  prompt: "Session name: {name}. Workspace: {workspace_path}. Task: {instruction}"
```

**Example**:
```
Agent tool:
  subagent_type: "qc-web"
  prompt: "Session name: checkout. Workspace: ./qc-workspace/flows/checkout-flow/.
           Task: Click vào search bar, tìm 'laptop', bấm vào kết quả đầu tiên"
```
Subagent tự biết dùng `snapshot` để tìm ref, tự chụp screenshot khi xong. Không cần chỉ chi tiết từng command.

**Subagent returns** structured response with every action listed:
```
ACTIONS:
1. `click e5` → OK (role=searchbox name="Search")
   alt: css="input[name='q']"
2. `fill e5 "laptop"` → OK
3. `press Enter` → OK
4. `click e12` → OK (role=link name="Dell XPS 13")

RESULT: OK
SNAPSHOT: qc-workspace/flows/{flow}/snapshots/step01.yml
SCREENSHOT: qc-workspace/flows/{flow}/screenshots/step01.png
ELEMENTS_ON_PAGE:
  - searchbox "Search" e5
  - button "Cart" e8
  - link "Dell XPS 13" e12
NOTE: Cookie banner appeared, dismissed via click e2 ("Accept all")
```

**Subagent appends raw data to explore log automatically** (ACTIONS, selectors, snapshot, screenshot, elements). QC Agent only needs to add the **assert** after verifying.

**After EACH subagent response**, you (main agent):
1. Read the screenshot with Read tool to verify visually
2. Evaluate pass/fail
3. **Append assert to explore log** (`$WORKSPACE/flows/{flow}/explore-log.md`) — what you verified from screenshot
4. Decide next step

**When calling subagent**, always include:
- Session name
- Workspace path
- **Explore log path** + current step number/title
- Task instruction

**Subagent retry policy**: Built into `qc-web` agent — wait 3s → re-snapshot (refs may have changed) → retry → try alt selector (role/text/css) → report FAIL with RETRY_LOG.

### Step 3: QC Report
Write `qc-workspace/flows/{flow}/qc-report.md` with pass/fail per test case, screenshots, issues found.

### Step 4: Generate Automation Script
Read explore log → generate `$WORKSPACE/flows/{flow}/automation-script.py` using the `playwright` Python library (sync API):
- `BrowserSession` → page wrapper (goto/click/fill/wait/screenshot)
- `Reporter` → HTML report generator (auto-styled, embedded screenshots)
- `setup_environment()` → ensures playwright browsers installed

See `references/playwright-templates.md` for the full template.

**After generating, RUN the script immediately to verify it works** — do not hand a script back to the user unverified. Scripts run **much faster** than human exploration, so timing bugs only show up at runtime:

```bash
playwright-cli -s="{flow}" close 2>/dev/null || true   # cold state, same as prod
python $WORKSPACE/flows/{flow}/automation-script.py --url {url} --user test@mail.com
```

1. Script writes `runs/{timestamp}/report.html` + `result.json` automatically
2. If PASS → open the HTML report to verify
3. If FAIL → read `failure.png` + error, fix script, run again
4. Script is only complete when it runs successfully from **cold state**

**Common script-vs-exploration gaps to look for when debugging a failed run:**
- **Cookie / GDPR banners, newsletter popups, "app install" interstitials** — appear only on cold start, not during warm exploration. Dismiss them right after `page.goto()`.
- **Skeleton loaders / lazy-loaded content** — script clicks before the element is attached. Replace bare `time.sleep` with `page.wait_for_selector(...)` or `expect(locator).to_be_visible()` for the specific element you need next.
- **Cached auth / localStorage state from previous runs** — exploration left you logged in, your script assumes anonymous. Make state changes idempotent (`if already_logged_in: skip_login`) so the script works whether the state already matches or not.
- **A/B test variants, feature flags** — the page you explored may differ from what the script sees. Pin the variant via cookie/query-string if possible.
- **Dynamic refs** — `e5` from exploration is NOT stable across runs. The script must use role/text/testid selectors, never raw snapshot refs.

The generated `report.html` is a self-contained file with embedded screenshots, ready to share with the team.

### Step 5: Update Project Memory

Write/update `qc-workspace/.memory/README.md` with new selectors, navigation paths, recurring popups (cookie banners, modals), known bugs, auth flows, feature flags, and anything else discovered that would save a future session from rediscovering it.

**The continuous-improvement loop**: before writing new things, scan each step's `### Friction` section in the explore log. Every friction note is a signal that the current memory is missing something — an unknown popup, an unreliable selector, a hidden wait condition. Harvest those into the memory so the next session avoids the same time-wasters. Over many flows, this compounds: session 1 might hit 10 friction points, session 5 should hit maybe 1-2. If session N still hits the same friction as session N-1, the memory harvest step was skipped. **Track this deliberately** — the goal isn't "the test passed", it's "each session is faster than the last".

**Format rule**: Keep `README.md` as the single entry point. When it grows beyond ~200 lines, split it by topic into sibling files (e.g. `.memory/popups.md`, `.memory/selectors.md`, `.memory/bugs.md`, `.memory/auth.md`) and leave concise `[Topic →](file.md)` references in the README. Never let a single memory file sprawl past 200 lines — future agents only skim, and anything buried deep gets lost.

### Step 6: Send Verdict & Handoff

**Only after Steps 4 and 5 are complete** — do NOT send verdict before the automation script exists and runs clean.

**Pass:**
```bash
tm-send DEV "[PASSED: <story_id>] All scenarios green on <browser>. Automation script at qc-workspace/flows/{flow}/automation-script.py."
tm-send PO  "[DONE: <story_id>] Ready to demo."
tm-send CMO "[DONE: <story_id>] <one-line user-facing summary for GTM>."
```

**Bounce (stop at Step 3 — don't write automation script for a failing feature):**
```bash
tm-send DEV "[BOUNCED: <story_id>] Scenario X failed. See card notes for repro."
```

**Blocked (ambiguous AC):**
```bash
tm-send PO "[QC_BLOCKED: <story_id>] Scenario X unclear. Need: <specific question>."
```

**Root cause in bounce notes:** Never guess. If you can't pinpoint from logs/console output, write `Root cause: unknown — needs DevTools investigation by DEV.`

---

## Explore Log Format

Write to `$WORKSPACE/flows/{flow}/explore-log.md` (same folder as test-cases, screenshots, report).

Each step can have **multiple actions**. Every action must have **exact CLI command with stable selector** (role/text/testid, NOT raw ref) so the script can be generated without guessing.

```markdown
## Step N: [Description]

### Actions:
1. `click e5` → OK  (role=searchbox name="Search")
2. `fill e5 "laptop"` → OK
3. `press Enter` → OK
4. `click e12` → OK  (role=link name="Dell XPS 13")

### Stable selectors (for script gen):
- Search bar: `role=searchbox[name="Search"]`
- Search input: same element — fill after click
- First result: `role=link[name="Dell XPS 13"]`

### Alt selectors:
- Search bar: `css=input[name="q"]`
- First result: `css=[data-testid="product-card"]:first-child a`

### Selector uniqueness notes (CRITICAL for script gen)
When multiple elements share a role/text, record the **minimum discriminator** the script needs to pick the right one. Without this, the generated script will grab the first match (often the wrong one) and fail. Two common traps:

- **Repeated role+name** — a page with multiple "Add to cart" buttons (one per product card). Use `get_by_role('button', name='Add to cart').nth(0)` only if the order is stable; otherwise scope via the parent product card (`locator('[data-testid=card-123]').get_by_role('button', name='Add to cart')`).
- **Text appears in multiple places** — e.g. "Submit" appears both as a section heading and a button. Always scope by role (`get_by_role('button', name='Submit')`).

Format your note as a rule the script can encode:

```markdown
- "<ambiguous selector>" matches N elements. Target is the only one under "<parent discriminator>" — scope by that in the script.
- "<ambiguous text>" appears twice on <page> (heading + button). Use `get_by_role('button', name=...)`.
```

This is the #1 cause of script gen wasting iterations. Cost 10 seconds to write now, saves 2 failed script runs later.

### Result: OK
### Snapshot: snapshots/step01_search_results.yml
### Screenshot: screenshots/step01_search_results.png
### Assert: Search results page loaded, shows "Dell XPS 13" as first result
### Elements on new page:
- searchbox "Search" (still present, populated with "laptop")
- link "Dell XPS 13" (first result)
- link "MacBook Pro" (second result)
- button "Add to cart" × 10 (one per card)
### Note: Cookie banner appeared on first load, dismissed via `click` on "Accept all"
```

**Why exact commands matter**: The generated script maps directly from these commands. "click search bar" is ambiguous — `get_by_role('searchbox', name='Search')` is precise and reproducible. Raw `e5` refs are NOT reproducible across runs.

---

## Regression Suite

When user asks to run regression ("chạy regression", "production checklist"):

```bash
python ~/.claude/skills/qc-web-testing/scripts/run_regression.py \
    --workspace ./qc-workspace
```

The script:
1. Finds all `qc-workspace/flows/*/automation-script.py`
2. Creates `qc-workspace/regression/{timestamp}/`
3. For each flow: runs `python automation-script.py --output-dir regression/{timestamp}/{flow}/`
4. Each script writes its own `report.html` + `result.json`
5. Aggregates all results into `regression/{timestamp}/summary.html`
6. Auto-opens summary in browser

**Optional**: Create `qc-workspace/flows.json` to specify default args per flow:
```json
{
  "checkout-flow": {"url": "https://shop.example.com", "user": "test@mail.com"},
  "login-flow":    {"url": "https://app.example.com", "email": "test@mail.com", "password": "abc123"}
}
```

---

## When to Read Screenshots

Not every subagent response needs a screenshot review. Only read when:
- **After navigation** — verify landed on correct page
- **After form submit** — verify success/error message
- **When subagent reports FAIL** — understand what went wrong
- **Final step of test case** — verify end state

Skip reading for: dismiss popup, go back, scroll, intermediate steps.

## Edge Cases

The `qc-web` subagent handles edge cases automatically (cookie banners, auth walls, dynamic content, iframes). If it encounters something it can't handle, it reports FAIL with details. You decide what to do next based on the report and project memory.

## Verdict & Handoff

After all test cases complete, send the verdict via `tm-send` (no `--to` flag):

**Pass:**
```bash
tm-send DEV "[PASSED: <story_id>] All scenarios green on <browser/device>. Evidence at <path>."
tm-send PO  "[DONE: <story_id>] Ready to demo."
tm-send CMO "[DONE: <story_id>] <one-line user-facing summary for GTM>."
```

**Bounce:**
```bash
tm-send DEV "[BOUNCED: <story_id>] Scenario X failed. See card notes for repro."
```

**Blocked (ambiguous AC):**
```bash
tm-send PO "[QC_BLOCKED: <story_id>] Scenario X unclear. Need: <specific question>."
```

### Root cause in bounce notes

**Never guess** root cause without concrete evidence (console log line, stack trace, exact error message). If you can't pinpoint it from logs/console output:

```
Root cause: unknown — needs DevTools / log investigation by DEV.
Hypothesis: (leave blank or "none")
```

A wrong hypothesis misleads DEV and wastes time. "Unknown" is more honest and more useful.

---

## Reference Files

- `references/setup-guide.md` — Playwright CLI setup
- `references/report-template.md` — QC report template
- `references/playwright-templates.md` — Automation script generation templates
