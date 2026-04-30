---
name: qc-mobile-testing
description: >
  QC mobile apps using Appium CLI interactive exploration + automation script generation.
  Supports Android and iOS. Agent explores app interactively via appium_cli.py, evaluates
  pass/fail with screenshots, generates automation scripts, and maintains project memory.
  Use this skill whenever the user wants to QC a mobile app, test a flow, run regression
  tests, or generate automation scripts. Triggers on: "QC app", "test mobile", "kiểm tra app",
  "test flow", "chạy regression", "sinh script test", "mobile QC", "quality check".
---

# QC Mobile Testing

QC mobile apps through interactive Appium CLI exploration. Agent controls the app in real-time, evaluates quality, then generates reusable automation scripts.

## FIRST: Read Project Memory

When this skill loads, IMMEDIATELY read project memory before doing anything else:

```
Read file: ./qc-workspace/.memory/app-knowledge.md
```

If the file exists → you already know this app's navigation, selectors, edge cases. Use this knowledge to skip redundant exploration and go faster.

If the file doesn't exist → this is a new project. You'll build knowledge as you QC.

---

## Prerequisites

Appium server running + device/emulator connected. Check with `~/.claude/skills/mobile-app-testing/scripts/env_check.py --fix-hints`.

## Subagent Capabilities

The `qc-mobile` subagent can do the following. Use these to craft your instructions:

### Session Management (you do this directly via Bash, not subagent)
```bash
CLI=~/.claude/skills/qc-mobile-testing/scripts/appium_cli.py
# IMPORTANT: --name is a global flag, must come BEFORE the subcommand
python $CLI --name "s1" start --package com.app --device emulator-5554 --port 4723
python $CLI --name "s1" stop
python $CLI --name "s1" screenshot --output /tmp/home.png
```

### What You Can Ask the Subagent To Do

| Capability | Instruction Example |
|-----------|---------------------|
| Screenshot | "Screenshot the current screen" |
| List elements | "List all clickable elements" / "List input fields" |
| Tap by text | "Tap the button with text 'Chuyển tiền'" |
| Tap by ID | "Tap element with id 'com.app:id/btn'" |
| Tap by coords | "Tap at coordinates (500, 800)" |
| Type text | "Type '0908144825' into the phone input field" |
| Clear + type | "Clear the input field and type 'hello'" |
| Swipe | "Swipe up" / "Swipe left" |
| Back | "Press back button" |
| Scroll to text | "Scroll down until you find 'Settings'" |
| Wait for element | "Wait up to 15 seconds for text 'Success' to appear" |
| Long press | "Long press at (300, 400) for 3 seconds" |
| Launch app | "Launch app com.other.app" |
| Get screen info | "Get screen size and orientation" |

### Selector Priority (subagent follows this automatically)
1. resource-id — most stable
2. text — readable
3. content-desc / accessibility ID — accessible
4. xpath — last resort, fragile
5. coordinates — fallback for custom Compose UI

---

## Workspace Structure

```
qc-workspace/                          ← created at user's working directory
  .memory/
    app-knowledge.md                   ← accumulated knowledge per project
  flows/                               ← one folder per QC flow
    transfer-flow/
      test-cases.md                    ← Step 0
      explore-log.md                   ← Step 2 (subagent + QC Agent write here)
      qc-report.md                     ← Step 3 (initial QC notes)
      automation-script.py             ← Step 4 (uses appium_lib)
      screenshots/                     ← exploration screenshots
      runs/                            ← each ad-hoc script run
        20260407_143022/
          report.html                  ← self-contained HTML (embedded screenshots)
          result.json                  ← machine-readable result
          screenshots/
  regression/                          ← regression runs (run_regression.py)
    20260407_170000/
      summary.html                     ← aggregate report linking per-flow reports
      transfer-flow/
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

As you explore in Step 2, come back and **annotate the test case with any element uniqueness gotchas you discover** — ambiguous button labels, recurring popups, conditional screens, cached state that alters flow, etc. Test cases aren't just a to-do list; they're the spec the script will encode. Gotchas noted here save script iterations later.

### Step 1: Setup

1. Create workspace: `mkdir -p $WORKSPACE/flows/{flow}/screenshots`
2. Check infrastructure (emulator + Appium server). See `references/setup-guide.md` if not running.
3. **Cold-start the app before exploring** — kill whatever state the app is in, then launch fresh. This is critical: if you explore from a warm state (already navigated somewhere, popups already dismissed, destination already picked), your script will later fail on a cold launch because it won't see the Bundle Load popup / KYC overlays / cached state you accidentally skipped. Explore the app from the same state the script will face in production:
```bash
adb -s {device} shell am force-stop {pkg}
```
4. Start CLI session:
```bash
CLI=~/.claude/skills/qc-mobile-testing/scripts/appium_cli.py
python $CLI --name "{flow}" start --package {pkg} --device {device} --port 4723
```

### Step 2: Explore + QC
Use **`qc-mobile` subagent** (via Agent tool with `subagent_type: "qc-mobile"`) for screen interaction to avoid context overflow.

**How to call**:
```
Agent tool:
  subagent_type: "qc-mobile"
  prompt: "Session name: {name}. Workspace: {workspace_path}. Task: {instruction}"
```

**Example**:
```
Agent tool:
  subagent_type: "qc-mobile"
  prompt: "Session name: transfer. Workspace: ./qc-workspace/transfer-flow-20260406/.
           Task: Tap vào search bar, tìm 'chuyển tiền', bấm vào kết quả Chuyển tiền"
```
Subagent tự biết dùng `list_elements` để tìm selector, tự chụp screenshot khi xong. Không cần chỉ chi tiết từng command.

**Subagent returns** structured response with every action listed:
```
ACTIONS:
1. `tap --id "searchBar"` → OK (selector: xpath //*[@resource-id="searchBar"])
   alt: coords=(504,584)
2. `type --desc "input_search" --value "chuyen tien"` → OK (ADB fallback)
   alt: coords=(208,191)
3. `tap --text "Chuyển tiền"` → OK (selector: text="Chuyển tiền")
   alt: desc="text_miniapp_Chuyển tiền"

RESULT: OK
SCREENSHOT: qc-workspace/flows/{flow}/screenshots/step01.png
ELEMENTS_ON_SCREEN:
  - search_input_home_p2p "Nhập SĐT/STK" coords=(96,352)
  - Ví MoMo tab
  - Ngân hàng tab
NOTE: PIN dialog appeared, dismissed via tap --desc "btn_close"
```

**Subagent appends raw data to explore log automatically** (ACTIONS, selectors, screenshot, elements). QC Agent only needs to add the **assert** after verifying.

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

**Subagent retry policy**: Built into `qc-mobile` agent — wait 3s → retry → scroll → try alt selector → report FAIL with RETRY_LOG.

### Step 3: QC Report
Write `qc-workspace/flows/{flow}/qc-report.md` with pass/fail per test case, screenshots, issues found.

### Step 4: Generate Automation Script
Read explore log → generate `$WORKSPACE/flows/{flow}/automation-script.py` using `appium_lib`:
- `AppiumSession` → driver wrapper (tap/type/swipe/wait/screenshot)
- `Reporter` → HTML report generator (auto-styled, embedded screenshots)
- `setup_environment()` → ensures emulator + Appium server running

See `references/appium-templates.md` for the full template + working MoMo example.

**After generating, RUN the script immediately to verify it works** — do not hand a script back to the user unverified. Scripts run **much faster** than human exploration, so timing bugs only show up at runtime:

```bash
adb -s {device} shell am force-stop {pkg}   # cold state, same as prod
python $WORKSPACE/flows/{flow}/automation-script.py --phone 0908144825 --amount 10000
```

1. Script writes `runs/{timestamp}/report.html` + `result.json` automatically
2. If PASS → open the HTML report to verify
3. If FAIL → read `failure.png` + error, fix script, run again
4. Script is only complete when it runs successfully from **cold state**

**Common script-vs-exploration gaps to look for when debugging a failed run:**
- **Launch popups** (Bundle Load Time, welcome banners, "What's new" sheets) — appear only on cold start, not during warm exploration. Dismiss with `dismiss_optional(s, text="OK")` right after `s.start()`.
- **Skeleton loaders / async content** — script taps before the UI finishes loading. Replace bare `time.sleep` with `s.wait(text="...")` for the specific element you need next.
- **Cached state from previous runs** — exploration left the app on screen X, your script assumes it starts on home. Make state changes idempotent (`try: find(target) except: do_change`) so the script works whether the state already matches or not.
- **KYC / notification overlays** — these popups appear on many screens and block CTAs invisibly. Call `dismiss_kyc_popup()` before every primary-CTA tap.
- **Wait fallback coverage** — if `s.wait(id="X")` fails but `s.tap(id="X")` works, the lib's wait doesn't yet have the same 4-tier fallback as find(); add the id to a wait via text/desc if needed.

The generated `report.html` is a self-contained file with embedded screenshots, ready to share with the team.

### Step 5: Update Project Memory
Write/update `qc-workspace/.memory/README.md` with new selectors, navigation paths, recurring popups, known bugs, miniapp packages, transaction thresholds, and anything else discovered that would save a future session from rediscovering it.

**The continuous-improvement loop**: before writing new things, scan each step's `### Friction` section in the explore log. Every friction note is a signal that the current memory is missing something — an unknown popup, an unreliable selector, a hidden wait condition. Harvest those into the memory so the next session avoids the same time-wasters. Over many flows, this compounds: session 1 might hit 10 friction points, session 5 should hit maybe 1-2. If session N still hits the same friction as session N-1, the memory harvest step was skipped. **Track this deliberately** — the goal isn't "the test passed", it's "each session is faster than the last".

**Format rule**: Keep `README.md` as the single entry point. When it grows beyond ~200 lines, split it by topic into sibling files (e.g. `.memory/popups.md`, `.memory/selectors.md`, `.memory/bugs.md`, `.memory/transactions.md`) and leave concise `[Topic →](file.md)` references in the README. Never let a single memory file sprawl past 200 lines — future agents only skim, and anything buried deep gets lost.

### Step 6: Send Verdict & Handoff

**Only after Steps 4 and 5 are complete** — do NOT send verdict before the automation script exists and runs clean.

**Pass:**
```bash
tm-send DEV "[PASSED: <story_id>] All scenarios green on <device>. Automation script at qc-workspace/flows/{flow}/automation-script.py."
tm-send PO  "[DONE: <story_id>] Ready to demo."
tm-send CMO "[DONE: <story_id>] <one-line user-facing summary for GTM>."
```

**Bounce** (stop at Step 3 — don't write automation script for a failing feature):
```bash
tm-send DEV "[BOUNCED: <story_id>] Scenario X failed on <device>. See card notes for repro."
```

**Root cause in bounce notes — never guess:**
If you can't pinpoint root cause from crash log / Logcat / exact error:
```
Root cause: unknown — needs device log / Logcat investigation by DEV.
Hypothesis: (leave blank or "none")
```
A wrong hypothesis misleads DEV and wastes time. "Unknown" is more honest and more useful.

**Blocked (ambiguous AC):**
```bash
tm-send PO "[QC_BLOCKED: <story_id>] Scenario X unclear. Need: <specific question>."
```

---

## Explore Log Format

Write to `$WORKSPACE/flows/{flow}/explore-log.md` (same folder as test-cases, screenshots, report).

Each step can have **multiple actions**. Every action must have **exact CLI command with selector** so the script can be generated without guessing.

```markdown
## Step N: [Description]

### Actions:
1. `tap --id "searchBar"` → OK
2. `type --desc "input_search" --value "chuyen tien"` → OK (ADB fallback)
3. `tap --text "Chuyển tiền"` → OK

### Selectors used:
- Search bar: xpath `//*[@resource-id="searchBar"]` (ID fallback)
- Search input: desc="input_search" (Compose, needs ADB type)
- Result item: text="Chuyển tiền"

### Alt selectors:
- Search bar: coords=(504,584)
- Result item: desc="text_miniapp_Chuyển tiền"

### Selector uniqueness notes (CRITICAL for script gen)
When multiple elements share a prefix/text, record the **minimum discriminator** the script needs to pick the right one. Without this, the generated script will grab the first match (often the wrong one) and fail. Two common traps:

- **Shared container prefix** — many touchables share a long `desc` prefix (e.g., a framework-generated path) but only one is the actual target. Find the substring that appears ONLY on the target, and note it.
- **Ambiguous text on popups** — the same button label (e.g. confirmation text) often appears as both a title `TextView` and a button label `TextView`. Use an `id`/`desc` selector on the button itself, never a plain `--text`.

Format your note as a rule the script can encode:

```markdown
- "<ambiguous selector>" matches N elements. Target is the only one with "<discriminator>" — filter by that in the script.
- "<ambiguous text>" appears twice on <screen> (title + button). Use <unique id/desc> for the button.
```

This is the #1 cause of script gen wasting iterations. Cost 10 seconds to write now, saves 2 failed script runs later.

### Result: OK
### Screenshot: screenshots/step01_transfer_screen.png
### Assert: Chuyển tiền screen loaded, shows "Nhập SĐT/STK tại đây"
### Elements on new screen:
- search_input_home_p2p: "Nhập SĐT/STK tại đây" coords=(96,352)
- Ví MoMo khác tab
- Ngân hàng tab
- Lê Thanh (recent contact)
### Note: 2 PIN dialogs appeared, dismissed via tap --desc "btn_close"
```

**Why exact commands matter**: The generated script maps directly from these commands. "tap search bar" is ambiguous — `tap --id "searchBar"` is precise and reproducible.

---

## Regression Suite

When user asks to run regression ("chạy regression", "production checklist"):

```bash
python ~/.claude/skills/qc-mobile-testing/scripts/run_regression.py \
    --workspace ./qc-workspace \
    --device emulator-5554
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
  "transfer-flow": {"phone": "0908144825", "amount": "10000"},
  "login-flow":    {"email": "test@mail.com", "password": "abc123"}
}
```

---

## When to Read Screenshots

Not every subagent response needs a screenshot review. Only read when:
- **After navigation** — verify landed on correct screen
- **After form submit** — verify success/error message
- **When subagent reports FAIL** — understand what went wrong
- **Final step of test case** — verify end state

Skip reading for: dismiss popup, press back, swipe, intermediate steps.

## Edge Cases

The `qc-mobile` subagent handles edge cases automatically (Compose UI fallbacks, permission dialogs, popups, etc.). If it encounters something it can't handle, it reports FAIL with details. You decide what to do next based on the report and project memory.

## Reference Files

- `references/setup-guide.md` — Emulator + Appium server setup
- `references/report-template.md` — QC report template
- `references/appium-templates.md` — Automation script generation templates
