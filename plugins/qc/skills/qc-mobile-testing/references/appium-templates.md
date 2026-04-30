# Automation Script Template

Scripts use `AppiumSession` (driver wrapper) + `Reporter` (HTML report generator) from `appium_lib.py`.

## Template

```python
#!/usr/bin/env python3
"""
Auto-generated from explore log.
Flow: {flow_name}
App: {package}
"""

import argparse
import os
import sys
import time
from datetime import datetime

# Import appium_lib from skill directory
sys.path.insert(0, os.path.expanduser("~/.claude/skills/qc-mobile-testing/scripts"))
from appium_lib import AppiumSession, setup_environment, Reporter


def parse_args():
    p = argparse.ArgumentParser(description="{flow description}")
    # Test data params (parameterize from explore log)
    p.add_argument("--phone", required=True)
    p.add_argument("--amount", required=True)
    # Standard params (all generated scripts share these)
    p.add_argument("--device", default="emulator-5554")
    p.add_argument("--port", type=int, default=4723)
    p.add_argument("--avd", default=None)
    p.add_argument("--reset", action="store_true", help="Clear app data before run")
    p.add_argument("--output-dir", default=None,
                   help="Where to write report.html + result.json (default: ./runs/{timestamp})")
    return p.parse_args()


def dismiss_optional(s, **selector):
    """Try to tap an element; ignore if not present."""
    try:
        s.tap(**selector)
        time.sleep(1)
    except Exception:
        pass


def main():
    args = parse_args()

    # Resolve output dir (default: ./runs/{timestamp})
    if args.output_dir is None:
        args.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "runs",
            datetime.now().strftime("%Y%m%d_%H%M%S"),
        )
    os.makedirs(args.output_dir, exist_ok=True)
    screenshots_dir = os.path.join(args.output_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Setup reporter
    reporter = Reporter(
        flow_name="{Flow Name}",
        app="{package}",
        device=args.device,
        output_dir=args.output_dir,
        test_case_title="TC-01 ▸ {test case title}",
        test_case_body="{test case description with <code>HTML</code>}",
        hero_label="Flow",
        flow_desc="{One-sentence summary of what this flow tests}",
    )

    # Setup environment (reproducible state)
    setup_environment(device=args.device, port=args.port, avd_name=args.avd)
    if args.reset:
        import subprocess
        subprocess.run(
            ["adb", "-s", args.device, "shell", "pm", "clear", "{package}"],
            capture_output=True, timeout=10,
        )

    s = AppiumSession(
        name="{flow}-regression",
        package="{package}",
        device=args.device,
        port=args.port,
    )

    try:
        s.start()
        time.sleep(3)
        dismiss_optional(s, text="OK")  # known launch popup if any

        # === Step 1 ===
        step_start = time.time()
        try:
            s.tap(id="searchBar")
            s.type(desc="input_search", value="...")
            s.tap(text="...")
            s.wait(text="...", timeout=10)
            screenshot = os.path.join(screenshots_dir, "step01.png")
            s.screenshot(screenshot)
            reporter.add_step(
                number=1,
                title="Step 1 title",
                description="Brief description of what this step does.",
                actions=[
                    {"command": "tap", "args": '--id "searchBar"', "result": "ok"},
                    {"command": "type", "args": '--desc "input_search" --value "..."',
                     "result": "ok", "note": "adb fallback"},
                    {"command": "tap", "args": '--text "..."', "result": "ok"},
                ],
                assert_text='screen.contains("...")',
                screenshot_path=screenshot,
                duration_ms=int((time.time() - step_start) * 1000),
                status="pass",
            )
        except Exception as e:
            screenshot = os.path.join(screenshots_dir, "step01_fail.png")
            try:
                s.screenshot(screenshot)
            except Exception:
                pass
            reporter.add_failed_step(
                number=1,
                title="Step 1 title",
                description="Brief description.",
                actions=[],
                screenshot_path=screenshot,
                duration_ms=int((time.time() - step_start) * 1000),
                error=str(e),
            )
            raise

        # === Step 2, 3, ... === (repeat the pattern)

    finally:
        try:
            s.stop()
        except Exception:
            pass

        # Write HTML report + result.json
        report_path = reporter.write()
        print(f"\n  Report: {report_path}")

        # Console summary
        passed = sum(1 for s in reporter.steps if s["status"] == "pass")
        total = len(reporter.steps)
        print(f"  Result: {passed}/{total} steps passed")

        if passed < total:
            sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Full Example: MoMo Transfer Flow

```python
#!/usr/bin/env python3
"""
Auto-generated from explore log.
Flow: MoMo - Chuyển tiền
App: vn.momo.platform.test
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/.claude/skills/qc-mobile-testing/scripts"))
from appium_lib import AppiumSession, setup_environment, Reporter


def parse_args():
    p = argparse.ArgumentParser(description="MoMo Transfer QC")
    p.add_argument("--phone", required=True)
    p.add_argument("--amount", required=True)
    p.add_argument("--device", default="emulator-5554")
    p.add_argument("--port", type=int, default=4723)
    p.add_argument("--avd", default=None)
    p.add_argument("--reset", action="store_true")
    p.add_argument("--output-dir", default=None)
    return p.parse_args()


def dismiss_optional(s, **selector):
    try:
        s.tap(**selector)
        time.sleep(1)
    except Exception:
        pass


def main():
    args = parse_args()

    if args.output_dir is None:
        args.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "runs", datetime.now().strftime("%Y%m%d_%H%M%S"),
        )
    os.makedirs(args.output_dir, exist_ok=True)
    screenshots = os.path.join(args.output_dir, "screenshots")
    os.makedirs(screenshots, exist_ok=True)

    reporter = Reporter(
        flow_name="Transfer Flow",
        app="vn.momo.platform.test",
        device=args.device,
        output_dir=args.output_dir,
        test_case_title="TC-01 ▸ Happy path peer-to-peer transfer",
        test_case_body=(
            f"Open MoMo, search <code>chuyen tien</code>, navigate to transfer screen, "
            f"enter phone <code>{args.phone}</code> and amount <code>{args.amount}đ</code>, "
            f"then tap <code>Chuyển tiền</code>."
        ),
        hero_label="Flow ▸ Transfer",
        flow_desc="Five steps. Full peer-to-peer money transfer journey from search to confirmation.",
    )

    setup_environment(device=args.device, port=args.port, avd_name=args.avd)
    if args.reset:
        subprocess.run(
            ["adb", "-s", args.device, "shell", "pm", "clear", "vn.momo.platform.test"],
            capture_output=True, timeout=10,
        )

    s = AppiumSession(
        name="transfer-regression",
        package="vn.momo.platform.test",
        device=args.device,
        port=args.port,
    )

    failed_early = False

    try:
        s.start()
        time.sleep(3)
        dismiss_optional(s, text="OK")  # Bundle Load Time popup

        # Step 1: Search Chuyển tiền
        t = time.time()
        s.tap(id="searchBar")
        s.type(desc="input_search", value="chuyen tien")
        s.tap(text="Chuyển tiền")
        s.wait(text="Nhập SĐT/STK", timeout=10)
        path = os.path.join(screenshots, "step01.png")
        s.screenshot(path)
        reporter.add_step(
            number=1,
            title="Open search and find Chuyển tiền",
            description="Tap search bar, type keyword, select result from autocomplete.",
            actions=[
                {"command": "tap", "args": '--id "searchBar"', "result": "ok"},
                {"command": "type", "args": '--desc "input_search" --value "chuyen tien"',
                 "result": "ok", "note": "adb fallback"},
                {"command": "tap", "args": '--text "Chuyển tiền"', "result": "ok"},
                {"command": "wait", "args": '--text "Nhập SĐT/STK" --timeout 10', "result": "ok"},
            ],
            assert_text='screen.contains("Nhập SĐT/STK")',
            screenshot_path=path,
            duration_ms=int((time.time() - t) * 1000),
            status="pass",
        )
        dismiss_optional(s, text="Đã hiểu")  # New UI popup

        # Step 2: Enter phone
        t = time.time()
        s.tap(id="search_input_home_p2p")
        time.sleep(1)
        dismiss_optional(s, text="Bỏ qua")  # Permission popup
        s.type(xpath="//android.widget.EditText", value=args.phone)
        s.wait(text=args.phone, timeout=10)
        path = os.path.join(screenshots, "step02.png")
        s.screenshot(path)
        reporter.add_step(
            number=2,
            title="Enter recipient phone number",
            description="Tap phone field, dismiss permission popup, type phone number.",
            actions=[
                {"command": "tap", "args": '--id "search_input_home_p2p"', "result": "ok"},
                {"command": "tap", "args": '--text "Bỏ qua"', "result": "ok",
                 "note": "permission popup"},
                {"command": "type", "args": f'--xpath "//EditText" --value "{args.phone}"',
                 "result": "ok"},
            ],
            assert_text=f'screen.contains("{args.phone}")',
            screenshot_path=path,
            duration_ms=int((time.time() - t) * 1000),
            status="pass",
        )

        # Step 3: Select contact
        t = time.time()
        s.tap(text=args.phone)
        s.wait(text="0đ", timeout=10)
        path = os.path.join(screenshots, "step03.png")
        s.screenshot(path)
        reporter.add_step(
            number=3,
            title="Select contact",
            description="Tap the matching contact in the search results.",
            actions=[
                {"command": "tap", "args": f'--text "{args.phone}"', "result": "ok"},
                {"command": "wait", "args": '--text "0đ" --timeout 10', "result": "ok"},
            ],
            assert_text='amount_screen.loaded',
            screenshot_path=path,
            duration_ms=int((time.time() - t) * 1000),
            status="pass",
        )

        # Step 4: Enter amount
        t = time.time()
        subprocess.run(["adb", "-s", args.device, "shell", "input", "text", args.amount],
                       capture_output=True, timeout=10)
        time.sleep(1)
        path = os.path.join(screenshots, "step04.png")
        s.screenshot(path)
        reporter.add_step(
            number=4,
            title="Enter transfer amount",
            description="Type amount via ADB (Compose UI requires ADB fallback).",
            actions=[
                {"command": "adb", "args": f'shell input text "{args.amount}"', "result": "ok"},
            ],
            assert_text=f'amount_field == "{args.amount}đ"',
            screenshot_path=path,
            duration_ms=int((time.time() - t) * 1000),
            status="pass",
        )

        # Step 5: Tap transfer button
        t = time.time()
        s.tap(text="Chuyển tiền")
        time.sleep(3)
        path = os.path.join(screenshots, "step05.png")
        s.screenshot(path)
        reporter.add_step(
            number=5,
            title="Tap the transfer button",
            description="Trigger the final transfer action.",
            actions=[
                {"command": "tap", "args": '--text "Chuyển tiền"', "result": "ok"},
            ],
            assert_text='confirmation_dialog.visible',
            screenshot_path=path,
            duration_ms=int((time.time() - t) * 1000),
            status="pass",
        )

    except Exception as e:
        failed_early = True
        print(f"FAIL: {e}")
        # Add a failed step entry if we have one in progress
        try:
            err_path = os.path.join(screenshots, "failure.png")
            s.screenshot(err_path)
        except Exception:
            err_path = None
        reporter.add_failed_step(
            number=len(reporter.steps) + 1,
            title="Unhandled exception",
            description="Test execution stopped due to an unhandled error.",
            actions=[],
            screenshot_path=err_path,
            duration_ms=0,
            error=str(e),
        )

    finally:
        try:
            s.stop()
        except Exception:
            pass

        report_path = reporter.write()
        print(f"\n  Report: {report_path}")
        passed = sum(1 for st in reporter.steps if st["status"] == "pass")
        total = len(reporter.steps)
        print(f"  Result: {passed}/{total} steps passed")

        if passed < total:
            sys.exit(1)


if __name__ == "__main__":
    main()
```

### How to run

```bash
# Run a single flow (writes report to ./runs/{timestamp}/)
python automation-script.py --phone 0908144830 --amount 10000

# With clean state
python automation-script.py --phone 0908144830 --amount 10000 --reset

# As part of regression (output-dir is set by run_regression.py)
python automation-script.py --phone 0908144830 --amount 10000 \
    --output-dir /path/to/regression/{ts}/transfer-flow/
```

---

## Reporter API

```python
from appium_lib import Reporter

reporter = Reporter(
    flow_name="Transfer Flow",
    app="vn.momo.platform.test",
    device="emulator-5554",
    output_dir="./runs/20260407_143022",
    test_case_title="TC-01 ▸ Happy path",
    test_case_body="Description with <code>HTML</code> allowed.",
    hero_label="Flow ▸ Transfer",
    flow_desc="One sentence summary.",
)

# Pass step
reporter.add_step(
    number=1,
    title="Step title",
    description="What this step does.",
    actions=[
        {"command": "tap", "args": '--id "btn"', "result": "ok"},
        {"command": "type", "args": '--id "input" --value "x"', "result": "ok",
         "note": "optional inline note"},
    ],
    assert_text='screen.contains("Success")',
    screenshot_path="./screenshots/step01.png",
    duration_ms=2300,
    status="pass",
)

# Failed step
reporter.add_failed_step(
    number=2,
    title="Step that broke",
    description="...",
    actions=[...],
    screenshot_path="./screenshots/step02_fail.png",
    duration_ms=10000,
    error="NoSuchElementException: Element 'X' not found",
)

# Write HTML + result.json
reporter.write()  # writes report.html and result.json into output_dir
```

## Rules

1. **Use `Reporter` for HTML output** — don't write inline HTML
2. **Use `setup_environment()`** at the start to ensure emulator + Appium running
3. **Wrap each step in `try/except`** so failures are captured properly
4. **Screenshot at the end of each step** (after the action completes)
5. **`--output-dir`** is the standard arg — `run_regression.py` uses it to point at regression folders
6. **Always call `reporter.write()` in `finally`** so the report is generated even on failure
7. **Parameterize variable data** (phone, amount, etc.) as argparse args
