#!/usr/bin/env python3
"""
Appium Library - Python class for mobile app control via Appium.

Usage:
    import sys
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/qc-mobile-testing/scripts"))
    from appium_lib import AppiumSession

    s = AppiumSession(name="test", package="com.app", device="emulator-5554")
    s.start()
    s.tap(id="searchBar")
    s.type(desc="input_search", value="hello")
    s.screenshot("./screen.png")
    s.stop()
"""

import base64
import html as html_lib
import json
import os
import re
import subprocess
import time
from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ensure_emulator(device, avd_name=None, timeout=120):
    """Check if device is running, start emulator if not."""
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    if device in result.stdout and "device" in result.stdout:
        return True

    if not avd_name:
        result = subprocess.run(
            ["emulator", "-list-avds"], capture_output=True, text=True
        )
        avds = [l for l in result.stdout.strip().split("\n") if l.strip()]
        if not avds:
            raise RuntimeError("No AVD available. Specify avd_name.")
        avd_name = avds[0]

    print(f"Starting emulator: {avd_name}")
    subprocess.Popen(
        ["emulator", "-avd", avd_name, "-no-audio", "-no-window", "-no-snapshot-save"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    subprocess.run(["adb", "wait-for-device"], timeout=timeout, check=True)
    start = time.time()
    while time.time() - start < timeout:
        r = subprocess.run(
            ["adb", "shell", "getprop", "sys.boot_completed"],
            capture_output=True, text=True, timeout=10
        )
        if r.stdout.strip() == "1":
            print("Emulator ready")
            return True
        time.sleep(2)
    raise RuntimeError(f"Emulator did not boot within {timeout}s")


def ensure_appium(port=4723, timeout=30):
    """Check if Appium is running on port, start if not."""
    import http.client
    def check():
        try:
            conn = http.client.HTTPConnection("localhost", port, timeout=2)
            conn.request("GET", "/status")
            resp = conn.getresponse()
            conn.close()
            return resp.status == 200
        except Exception:
            return False

    if check():
        return True

    print(f"Starting Appium server on port {port}")
    subprocess.Popen(
        ["appium", "--port", str(port), "--relaxed-security"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    start = time.time()
    while time.time() - start < timeout:
        if check():
            print("Appium ready")
            return True
        time.sleep(1)
    raise RuntimeError(f"Appium did not start within {timeout}s")


def setup_environment(device, port=4723, avd_name=None):
    """One-call setup: ensure emulator + Appium are running."""
    ensure_emulator(device, avd_name=avd_name)
    ensure_appium(port=port)


class AppiumSession:
    """Persistent Appium session wrapper for mobile app QC."""

    def __init__(self, name="default", package=None, device=None,
                 platform="android", port=4723):
        self.name = name
        self.package = package
        self.device = device
        self.platform = platform
        self.port = port
        self.url = f"http://localhost:{port}"
        self.driver = None

    # ---- Lifecycle ----

    def start(self, launch_app=True, cold_start=True):
        """Start Appium session and optionally launch the app.

        cold_start=True (default): terminate the app first so launch_app brings
        it up from a clean state (Home screen). Without this, activate_app just
        brings the existing process to the foreground — wherever the user left
        it. Set cold_start=False if you want to attach to the current state.
        """
        if self.platform == "android":
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.udid = self.device
            options.no_reset = True
            # Filter unimportant views → faster element queries on heavy RN pages
            options.set_capability("ignoreUnimportantViews", True)
        else:
            options = XCUITestOptions()
            options.platform_name = "iOS"
            options.udid = self.device
            options.no_reset = True

        self.driver = webdriver.Remote(self.url, options=options)

        if self.package and launch_app:
            if cold_start:
                try:
                    self.driver.terminate_app(self.package)
                    time.sleep(1)
                except Exception:
                    pass
            self.driver.activate_app(self.package)
            time.sleep(2)
        return self

    def stop(self):
        """Close the Appium session."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()

    # ---- Element Finding ----

    def find(self, id=None, text=None, desc=None, xpath=None,
             desc_contains=None, text_contains=None):
        """Find element with fallback strategies."""
        strategies = []

        if id:
            strategies = [
                (AppiumBy.ID, id),
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{id}")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{id}")'),
                (AppiumBy.XPATH, f'//*[@resource-id="{id}" or @content-desc="{id}"]'),
            ]
        elif text:
            strategies = [
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
                (AppiumBy.XPATH, f'//*[@text="{text}"]'),
            ]
        elif desc:
            strategies = [
                (AppiumBy.ACCESSIBILITY_ID, desc),
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{desc}")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{desc}")'),
                (AppiumBy.XPATH, f'//*[@content-desc="{desc}"]'),
            ]
        elif desc_contains:
            strategies = [
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{desc_contains}")'),
                (AppiumBy.XPATH, f'//*[contains(@content-desc, "{desc_contains}")]'),
            ]
        elif text_contains:
            strategies = [
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text_contains}")'),
                (AppiumBy.XPATH, f'//*[contains(@text, "{text_contains}")]'),
            ]
        elif xpath:
            strategies = [(AppiumBy.XPATH, xpath)]
        else:
            raise ValueError("Must provide id, text, desc, desc_contains, text_contains, or xpath")

        last_err = None
        for by, value in strategies:
            try:
                return self.driver.find_element(by, value)
            except Exception as e:
                last_err = e
        raise last_err

    # ---- Actions ----

    def tap(self, id=None, text=None, desc=None, xpath=None, coords=None,
            desc_contains=None, text_contains=None):
        """Tap an element or coordinates."""
        if coords:
            x, y = coords if isinstance(coords, tuple) else map(int, coords.split(","))
            self._tap_coords(x, y)
        else:
            el = self.find(id=id, text=text, desc=desc, xpath=xpath,
                           desc_contains=desc_contains, text_contains=text_contains)
            el.click()
        return self

    def _tap_coords(self, x, y):
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        action = ActionBuilder(self.driver, mouse=finger)
        action.pointer_action.move_to_location(int(x), int(y))
        action.pointer_action.pointer_down()
        action.pointer_action.pause(0.1)
        action.pointer_action.pointer_up()
        action.perform()

    def type(self, value, id=None, text=None, desc=None, xpath=None, clear=False):
        """Type text into an element. Falls back to ADB on Compose UI."""
        el = self.find(id=id, text=text, desc=desc, xpath=xpath)
        if clear:
            try:
                el.clear()
            except Exception:
                pass
        try:
            el.send_keys(value)
        except Exception:
            # Compose UI fallback
            try:
                el.click()
            except Exception:
                pass
            time.sleep(0.5)
            escaped = str(value).replace(" ", "%s").replace("'", "\\'")
            subprocess.run(
                ["adb", "-s", self.device, "shell", "input", "text", escaped],
                capture_output=True, text=True, timeout=10
            )
        return self

    def clear(self, id=None, text=None, desc=None, xpath=None):
        el = self.find(id=id, text=text, desc=desc, xpath=xpath)
        el.clear()
        return self

    def swipe(self, direction, distance=None):
        """Swipe up/down/left/right."""
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        cx, cy = w // 2, h // 2
        dist = distance or int(h * 0.3)

        directions = {
            "up":    (cx, cy + dist // 2, cx, cy - dist // 2),
            "down":  (cx, cy - dist // 2, cx, cy + dist // 2),
            "left":  (cx + dist // 2, cy, cx - dist // 2, cy),
            "right": (cx - dist // 2, cy, cx + dist // 2, cy),
        }
        sx, sy, ex, ey = directions[direction]

        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        action = ActionBuilder(self.driver, mouse=finger)
        action.pointer_action.move_to_location(sx, sy)
        action.pointer_action.pointer_down()
        action.pointer_action.pause(0.1)
        action.pointer_action.move_to_location(ex, ey)
        action.pointer_action.pause(0.5)
        action.pointer_action.pointer_up()
        action.perform()
        return self

    def back(self):
        self.driver.back()
        return self

    def home(self):
        if self.platform == "android":
            self.driver.press_keycode(3)
        else:
            self.driver.execute_script("mobile: pressButton", {"name": "home"})
        return self

    def long_press(self, id=None, text=None, desc=None, xpath=None,
                   coords=None, duration=2000):
        if coords:
            x, y = coords if isinstance(coords, tuple) else map(int, coords.split(","))
        else:
            el = self.find(id=id, text=text, desc=desc, xpath=xpath)
            x = el.location["x"] + el.size["width"] // 2
            y = el.location["y"] + el.size["height"] // 2

        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        action = ActionBuilder(self.driver, mouse=finger)
        action.pointer_action.move_to_location(int(x), int(y))
        action.pointer_action.pointer_down()
        action.pointer_action.pause(duration / 1000.0)
        action.pointer_action.pointer_up()
        action.perform()
        return self

    # ---- Wait & Scroll ----

    def wait(self, id=None, text=None, desc=None, timeout=10,
             desc_contains=None, text_contains=None):
        """Wait for element to appear via the same fallback as find()."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                self.find(id=id, text=text, desc=desc,
                          desc_contains=desc_contains, text_contains=text_contains)
                return True
            except Exception:
                time.sleep(0.5)
        sel = id or text or desc or desc_contains or text_contains
        raise TimeoutError(f"Element '{sel}' not found within {timeout}s")

    def scroll_to(self, text, timeout=10):
        """Scroll to find an element with text."""
        self.driver.implicitly_wait(timeout)
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.setMaxSearchSwipes(5)'
                f'.scrollIntoView(new UiSelector().text("{text}"))'
            )
        finally:
            self.driver.implicitly_wait(0)
        return self

    # ---- Inspection ----

    def screenshot(self, path):
        """Save screenshot to file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.driver.save_screenshot(path)
        return path

    def list_elements(self, clickable=False, input_only=False, limit=200):
        """List elements on screen.

        Returns list of dicts with keys: type, text, id, desc, coords ("x,y" string),
        size ("WxH" string). Capped at `limit` to avoid hanging on heavy pages.
        Stale elements are silently skipped.
        """
        from selenium.common.exceptions import StaleElementReferenceException

        if input_only:
            by, sel = AppiumBy.CLASS_NAME, "android.widget.EditText"
            kind = "input"
        elif clickable:
            by, sel = AppiumBy.XPATH, "//*[@clickable='true']"
            kind = "other"
        else:
            by, sel = AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']"
            kind = "other"

        out = []
        for el in self.driver.find_elements(by, sel):
            if len(out) >= limit:
                break
            try:
                if kind == "input":
                    out.append({
                        "type": "EditText",
                        "text": el.text or "",
                        "id": el.get_attribute("resource-id") or "",
                        "hint": el.get_attribute("hint") or "",
                        "coords": f"{el.location['x']},{el.location['y']}",
                        "size": f"{el.size['width']}x{el.size['height']}",
                    })
                else:
                    out.append({
                        "type": el.get_attribute("className") or "",
                        "text": el.text or "",
                        "id": el.get_attribute("resource-id") or "",
                        "desc": el.get_attribute("content-desc") or "",
                        "coords": f"{el.location['x']},{el.location['y']}",
                        "size": f"{el.size['width']}x{el.size['height']}",
                    })
            except (StaleElementReferenceException, Exception):
                continue
        return out

    def page_source(self, path=None):
        source = self.driver.page_source
        if path:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w") as f:
                f.write(source)
        return source

    def info(self):
        size = self.driver.get_window_size()
        return {
            "width": size["width"],
            "height": size["height"],
            "orientation": self.driver.orientation,
            "current_activity": self.driver.current_activity,
            "current_package": self.driver.current_package,
        }

    # ---- App ----

    def launch_app(self, package=None):
        self.driver.activate_app(package or self.package)
        time.sleep(2)
        return self

    def terminate_app(self, package=None):
        self.driver.terminate_app(package or self.package)
        return self


# ============================================================
# REPORTER — generates per-flow HTML reports
# ============================================================

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def _load_template(name):
    """Load a template file from the assets directory."""
    with open(os.path.join(_ASSETS_DIR, name)) as f:
        return f.read()


def _extract_fragment(template, marker_name):
    """Extract a fragment between <!-- {MARKER}_START --> and <!-- {MARKER}_END -->."""
    pattern = rf"<!-- {marker_name}_START -->(.*?)<!-- {marker_name}_END -->"
    match = re.search(pattern, template, re.DOTALL)
    if not match:
        raise ValueError(f"Marker {marker_name} not found in template")
    return match.group(1).strip()


def _strip_fragments(template):
    """Remove all template fragment blocks from the main template."""
    # Remove everything from "<!-- TEMPLATE FRAGMENTS BELOW" onwards
    idx = template.find("<!-- ====")
    if idx != -1:
        # Find the second "<!-- ====" (separator before fragments section)
        idx2 = template.find("<!-- ====", idx)
        if idx2 != -1:
            return template[:idx].rstrip() + "\n"
    return template


def _embed_image(path):
    """Read image file and return base64 data URI."""
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def _esc(text):
    """HTML-escape text."""
    return html_lib.escape(str(text)) if text else ""


def _format_duration(ms):
    """Format milliseconds as human-readable duration."""
    if ms < 1000:
        return f"{ms}ms"
    s = ms / 1000
    if s < 60:
        return f"{s:.1f}s"
    m = int(s // 60)
    s = s % 60
    return f"{m}m {s:.0f}s"


class Reporter:
    """Generates a per-flow HTML report from collected step data."""

    def __init__(self, flow_name, app, device, output_dir,
                 test_case_title=None, test_case_body=None,
                 run_id=None, hero_label=None, flow_desc=None):
        self.flow_name = flow_name
        self.app = app
        self.device = device
        self.output_dir = output_dir
        self.test_case_title = test_case_title or "Untitled test case"
        self.test_case_body = test_case_body or "No description provided."
        self.run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.hero_label = hero_label or "Flow"
        self.flow_desc = flow_desc or ""
        self.steps = []
        self.start_time = datetime.now()
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "screenshots"), exist_ok=True)

    def add_step(self, number, title, description, actions, assert_text,
                 screenshot_path, duration_ms, status="pass"):
        """Add a step. actions = list of dicts: {command, args, result, note}."""
        self.steps.append({
            "number": number,
            "title": title,
            "description": description,
            "actions": actions,
            "assert": assert_text,
            "screenshot": screenshot_path,
            "duration_ms": duration_ms,
            "status": status,
            "error": None,
            "step_time": datetime.now().strftime("%H:%M:%S"),
        })

    def add_failed_step(self, number, title, description, actions,
                        screenshot_path, duration_ms, error, retry_log=None):
        """Add a failed step with error details."""
        self.steps.append({
            "number": number,
            "title": title,
            "description": description,
            "actions": actions or [],
            "assert": None,
            "screenshot": screenshot_path,
            "duration_ms": duration_ms,
            "status": "fail",
            "error": error,
            "retry_log": retry_log or [],
            "step_time": datetime.now().strftime("%H:%M:%S"),
        })

    def _render_actions(self, actions, action_template):
        """Render the actions list HTML."""
        if not actions:
            return '<div style="color: var(--text-dim);">— no actions —</div>'
        rendered = []
        for i, a in enumerate(actions, 1):
            note = ""
            if a.get("note"):
                note = f'<span class="note">// {_esc(a["note"])}</span>'
            html_str = action_template
            html_str = html_str.replace("{{ACTION_NUM}}", str(i))
            html_str = html_str.replace("{{ACTION_CMD}}", _esc(a.get("command", "")))
            html_str = html_str.replace("{{ACTION_ARGS}}", _esc(a.get("args", "")))
            html_str = html_str.replace("{{ACTION_RESULT}}", _esc(a.get("result", "ok")))
            html_str = html_str.replace("{{ACTION_NOTE}}", note)
            rendered.append(html_str)
        return "\n".join(rendered)

    def _render_steps(self, step_template, action_template, assert_template, error_template):
        rendered = []
        for step in self.steps:
            actions_html = self._render_actions(step["actions"], action_template)

            if step["status"] == "fail":
                assert_or_error = error_template.replace(
                    "{{ERROR_TEXT}}", _esc(step.get("error", "Unknown error"))
                )
            else:
                assert_or_error = assert_template.replace(
                    "{{ASSERT_TEXT}}", _esc(step.get("assert") or "verified")
                )

            # Screenshot
            screenshot_path = step.get("screenshot")
            if screenshot_path and os.path.exists(screenshot_path):
                data_uri = _embed_image(screenshot_path)
                screenshot_html = f'<img src="{data_uri}" alt="step {step["number"]}" style="max-width: 100%; max-height: 100%;">'
                screenshot_name = os.path.basename(screenshot_path)
            else:
                screenshot_html = f'<span style="color: var(--text-dim); font-family: var(--mono);">no screenshot</span>'
                screenshot_name = "—"

            num_str = f"{step['number']:02d}"
            html_str = step_template
            html_str = html_str.replace("{{STEP_STATUS}}", step["status"])
            html_str = html_str.replace("{{STEP_NUM}}", num_str)
            html_str = html_str.replace("{{STEP_TITLE}}", _esc(step["title"]))
            html_str = html_str.replace("{{STEP_DESC}}", _esc(step["description"]))
            html_str = html_str.replace("{{STEP_ACTIONS_HTML}}", actions_html)
            html_str = html_str.replace("{{STEP_ASSERT_OR_ERROR}}", assert_or_error)
            html_str = html_str.replace("{{SCREENSHOT_HTML}}", screenshot_html)
            html_str = html_str.replace("{{SCREENSHOT_NAME}}", screenshot_name)
            html_str = html_str.replace("{{STEP_TIME}}", step["step_time"])
            rendered.append(html_str)
        return "\n".join(rendered)

    def _render_timeline(self, segment_template):
        """Render timeline segments based on step durations."""
        if not self.steps:
            return ""
        rendered = []
        for step in self.steps:
            seconds = step["duration_ms"] / 1000
            label = f"{step['number']:02d} · {seconds:.1f}s"
            html_str = segment_template
            html_str = html_str.replace("{{SEGMENT_FLEX}}", f"{seconds:.2f}")
            html_str = html_str.replace("{{SEGMENT_LABEL}}", label)
            rendered.append(html_str)
        return "\n".join(rendered)

    def write(self, filename="report.html"):
        """Generate the HTML report and write to disk. Also writes result.json."""
        template = _load_template("flow-report.html")
        step_template = _extract_fragment(template, "STEP_TEMPLATE")
        action_template = _extract_fragment(template, "ACTION_TEMPLATE")
        assert_template = _extract_fragment(template, "ASSERT_TEMPLATE")
        error_template = _extract_fragment(template, "ERROR_TEMPLATE")
        segment_template = _extract_fragment(template, "TIMELINE_SEGMENT_TEMPLATE")

        # Strip fragment blocks from main template
        main = _strip_fragments(template)

        # Compute stats
        total = len(self.steps)
        passed = sum(1 for s in self.steps if s["status"] == "pass")
        failed = total - passed
        verdict = "PASS" if failed == 0 else "FAIL"
        verdict_class = "pass" if failed == 0 else "fail"
        total_ms = sum(s["duration_ms"] for s in self.steps)
        duration = _format_duration(total_ms)
        asserts_count = sum(1 for s in self.steps if s.get("assert"))

        # Hero name (split first word for em styling)
        words = self.flow_name.split()
        if len(words) >= 2:
            flow_name_html = f"{_esc(' '.join(words[:-1]))}<br><em>{_esc(words[-1])}</em>."
        else:
            flow_name_html = f"<em>{_esc(self.flow_name)}</em>."

        # Summary text
        if verdict == "PASS":
            summary_title = f"Flow <em>verified</em>.<br>Ship with confidence."
            summary_body = (
                f"All {total} steps executed cleanly. The generated automation script "
                f"is ready for inclusion in the next regression run."
            )
        else:
            summary_title = f"Flow <em>broke</em>.<br>Investigate before shipping."
            summary_body = (
                f"{failed} of {total} steps failed. Check the failure detail above and "
                f"the latest UI changes before re-running."
            )

        # Render variable sections
        timeline_html = self._render_timeline(segment_template)
        steps_html = self._render_steps(step_template, action_template, assert_template, error_template)

        # Fill main template
        replacements = {
            "{{FLOW_NAME}}": _esc(self.flow_name),
            "{{FLOW_NAME_HTML}}": flow_name_html,
            "{{APP}}": _esc(self.app),
            "{{DEVICE}}": _esc(self.device),
            "{{RUN_ID}}": _esc(self.run_id),
            "{{START_TIME}}": self.start_time.strftime("%H:%M:%S"),
            "{{HERO_LABEL}}": _esc(self.hero_label),
            "{{FLOW_DESC}}": _esc(self.flow_desc),
            "{{STEPS_PASSED}}": str(passed),
            "{{STEPS_TOTAL}}": str(total),
            "{{VERDICT}}": verdict,
            "{{VERDICT_CLASS}}": verdict_class,
            "{{DURATION}}": duration,
            "{{ASSERTS_COUNT}}": str(asserts_count),
            "{{TEST_CASE_TITLE}}": _esc(self.test_case_title),
            "{{TEST_CASE_BODY}}": self.test_case_body,  # allow HTML for code blocks
            "{{TIMELINE_SEGMENTS}}": timeline_html,
            "{{STEPS_HTML}}": steps_html,
            "{{SUMMARY_TITLE_HTML}}": summary_title,
            "{{SUMMARY_BODY}}": summary_body,
            "{{GENERATED_AT}}": datetime.now().strftime("%Y·%m·%d %H:%M:%S"),
        }
        for k, v in replacements.items():
            main = main.replace(k, v)

        report_path = os.path.join(self.output_dir, filename)
        with open(report_path, "w") as f:
            f.write(main)

        # Also write result.json for regression aggregation
        result = {
            "flow_name": self.flow_name,
            "status": "pass" if verdict == "PASS" else "fail",
            "steps_passed": passed,
            "steps_total": total,
            "duration_s": total_ms / 1000,
            "failure": None,
        }
        for step in self.steps:
            if step["status"] == "fail":
                result["failure"] = {
                    "step_name": f"Step {step['number']:02d} ▸ {step['title']}",
                    "error": step.get("error", "Unknown error"),
                    "selector": "",
                }
                break

        with open(os.path.join(self.output_dir, "result.json"), "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        return os.path.abspath(report_path)


# ============================================================
# REGRESSION REPORTER — generates summary HTML across flows
# ============================================================

class RegressionReporter:
    """Generates a regression summary HTML aggregating multiple flow runs."""

    def __init__(self, output_dir, app, device, run_id=None):
        self.output_dir = output_dir
        self.app = app
        self.device = device
        self.run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.flows = []
        self.start_time = datetime.now()
        os.makedirs(output_dir, exist_ok=True)

    def add_flow(self, name, flow_dir, status, steps_passed, steps_total,
                 duration_s, failure=None, meta=None):
        """Register a flow result. failure = {step_name, error, selector} or None."""
        self.flows.append({
            "name": name,
            "flow_dir": flow_dir,
            "status": status,
            "steps_passed": steps_passed,
            "steps_total": steps_total,
            "duration_s": duration_s,
            "failure": failure,
            "meta": meta or "",
        })

    def add_flow_from_result_json(self, name, flow_dir, result_json_path, meta=None):
        """Load result.json and add the flow."""
        with open(result_json_path) as f:
            data = json.load(f)
        self.add_flow(
            name=name,
            flow_dir=flow_dir,
            status=data["status"],
            steps_passed=data["steps_passed"],
            steps_total=data["steps_total"],
            duration_s=data["duration_s"],
            failure=data.get("failure"),
            meta=meta,
        )

    def _render_step_dots(self, flow, dot_template):
        """Render step dots for a flow's progress bar."""
        rendered = []
        passed = flow["steps_passed"]
        total = flow["steps_total"]
        for i in range(total):
            if i < passed:
                cls = ""  # default = pass
            elif i == passed and flow["status"] == "fail":
                cls = "fail"
            else:
                cls = "skip"
            rendered.append(dot_template.replace("{{DOT_CLASS}}", cls))
        return "\n".join(rendered)

    def _render_flows(self, flow_template, dot_template, failure_template):
        rendered = []
        for i, flow in enumerate(self.flows, 1):
            dots = self._render_step_dots(flow, dot_template)

            failure_html = ""
            if flow.get("failure"):
                f = flow["failure"]
                failure_html = failure_template
                failure_html = failure_html.replace("{{FAILED_STEP_NAME}}", _esc(f.get("step_name", "Unknown step")))
                failure_html = failure_html.replace("{{FAILED_ERROR}}", _esc(f.get("error", "")))
                failure_html = failure_html.replace("{{FAILED_SELECTOR}}",
                    f"selector ▸ {_esc(f.get('selector', '—'))}")

            duration = f"{flow['duration_s']:.1f} seconds"
            status_class = "pass" if flow["status"] == "pass" else "fail"

            html_str = flow_template
            html_str = html_str.replace("{{FLOW_ID}}", f"{i:02d}")
            html_str = html_str.replace("{{FLOW_NAME}}", _esc(flow["name"]))
            html_str = html_str.replace("{{FLOW_META}}", _esc(flow.get("meta", "")))
            html_str = html_str.replace("{{STEP_DOTS}}", dots)
            html_str = html_str.replace("{{FLOW_DIR}}", _esc(flow["flow_dir"]))
            html_str = html_str.replace("{{STEPS_PASSED}}", str(flow["steps_passed"]))
            html_str = html_str.replace("{{STEPS_TOTAL}}", str(flow["steps_total"]))
            html_str = html_str.replace("{{DURATION}}", duration)
            html_str = html_str.replace("{{STATUS}}", flow["status"].upper())
            html_str = html_str.replace("{{STATUS_CLASS}}", status_class)
            html_str = html_str.replace("{{FAILURE_DETAIL}}", failure_html)
            rendered.append(html_str)
        return "\n".join(rendered)

    def write(self, filename="summary.html"):
        template = _load_template("summary-report.html")
        flow_template = _extract_fragment(template, "FLOW_TEMPLATE")
        dot_template = _extract_fragment(template, "STEP_DOT_TEMPLATE")
        failure_template = _extract_fragment(template, "FAILURE_DETAIL_TEMPLATE")
        main = _strip_fragments(template)

        # Stats
        total = len(self.flows)
        passed = sum(1 for f in self.flows if f["status"] == "pass")
        failed = total - passed
        verdict = "PASS" if failed == 0 else "FAIL"
        verdict_class = "pass" if failed == 0 else "fail"
        verdict_desc = "Production ▸ READY" if failed == 0 else "Production ▸ NOT READY"
        total_duration_s = sum(f["duration_s"] for f in self.flows)
        m = int(total_duration_s // 60)
        s = int(total_duration_s % 60)
        total_duration = f"{m}:{s:02d}"

        # Hero title
        if failed == 0:
            hero_title = f"All {total} <em>passed</em>."
            hero_tagline = "Every flow executed cleanly. The build is green and ready to ship."
        elif passed == 0:
            hero_title = f"All <em>broke</em>."
            hero_tagline = "Every flow failed. Likely an environment or critical UI regression."
        else:
            hero_title = f"{passed} passed.<br>{failed} <em>broke</em>."
            hero_tagline = f"{failed} of {total} flows regressed. Investigate before shipping."

        # Recommendation
        if failed == 0:
            rec_title = f"Ship with <em>confidence</em>."
            rec_body = (
                "All regression flows passed. The build can move to production. "
                "Re-run regression after the next deploy to maintain coverage."
            )
            rec_actions = (
                '<a href="#" class="action primary">Promote to staging →</a>'
                '<a href="#" class="action">Re-run regression</a>'
            )
        else:
            failing = [f for f in self.flows if f["status"] == "fail"]
            failing_names = ", ".join(f["name"] for f in failing)
            rec_title = f"Block the release. Fix <em>{_esc(failing[0]['name'].lower())}</em> first."
            rec_body = (
                f"{failed} flow(s) regressed: {_esc(failing_names)}. "
                "Investigate the latest UI changes before re-running regression. "
                "Production deploy should be blocked until all flows pass."
            )
            first_failing = failing[0]["flow_dir"]
            rec_actions = (
                f'<a href="{first_failing}/report.html" class="action primary">Open failing report →</a>'
                '<a href="#" class="action">Re-run regression</a>'
            )

        flows_html = self._render_flows(flow_template, dot_template, failure_template)

        replacements = {
            "{{APP}}": _esc(self.app),
            "{{DEVICE}}": _esc(self.device),
            "{{RUN_ID}}": _esc(self.run_id),
            "{{RUN_DATE}}": self.start_time.strftime("%Y·%m·%d %H:%M"),
            "{{HERO_TITLE_HTML}}": hero_title,
            "{{HERO_TAGLINE}}": hero_tagline,
            "{{VERDICT}}": verdict.title(),
            "{{VERDICT_CLASS}}": verdict_class,
            "{{VERDICT_DESC}}": verdict_desc,
            "{{TOTAL_FLOWS}}": str(total),
            "{{TOTAL_FLOWS_PADDED}}": f"{total:02d}",
            "{{PASSED_COUNT}}": str(passed),
            "{{FAILED_COUNT}}": str(failed),
            "{{TOTAL_DURATION}}": total_duration,
            "{{FLOWS_HTML}}": flows_html,
            "{{RECOMMENDATION_TITLE_HTML}}": rec_title,
            "{{RECOMMENDATION_BODY}}": rec_body,
            "{{RECOMMENDATION_ACTIONS}}": rec_actions,
            "{{GENERATED_AT}}": datetime.now().strftime("%Y·%m·%d %H:%M:%S"),
        }
        for k, v in replacements.items():
            main = main.replace(k, v)

        report_path = os.path.join(self.output_dir, filename)
        with open(report_path, "w") as f:
            f.write(main)

        return os.path.abspath(report_path)
