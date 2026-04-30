#!/usr/bin/env python3
"""
Appium CLI - Interactive mobile app control via command line.

Usage:
    python appium_cli.py start --package com.app --device emulator-5554
    python appium_cli.py --name session1 screenshot --path /tmp/screen.png
    python appium_cli.py --name session1 tap --text "OK"
    python appium_cli.py --name session1 stop

Run with --help for full usage.
"""

import argparse
import json
import os
import subprocess
import sys
import time

SESSION_DIR = "/tmp"


def session_path(name):
    return os.path.join(SESSION_DIR, f"appium_cli_{name}.json")


def save_session(name, data):
    with open(session_path(name), "w") as f:
        json.dump(data, f, indent=2)


def load_session(name):
    path = session_path(name)
    if not os.path.exists(path):
        print(f"ERROR: No session '{name}'. Run 'start' first.")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def get_driver(session):
    """Connect to existing Appium session."""
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from appium.options.ios import XCUITestOptions

    url = session["appium_url"]
    platform = session["platform"]

    if platform == "android":
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.udid = session["device"]
        options.no_reset = True
        # Skip decorative/internal views in accessibility tree → much smaller
        # hierarchy → page_source/find_elements 5-10x faster on heavy RN pages
        # (e.g. hotel detail). Trade-off: some non-important views become invisible.
        options.set_capability("ignoreUnimportantViews", True)
        # Don't set app_package here - it causes instrumentation errors
        # Use activate_app() after session is created instead
    else:
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.udid = session["device"]
        options.no_reset = True

    # Try to reconnect to existing session
    sid = session.get("session_id")
    if sid:
        try:
            driver = webdriver.Remote(url, options=options)
            # Update session id
            session["session_id"] = driver.session_id
            save_session(session["name"], session)
            return driver
        except Exception:
            pass

    driver = webdriver.Remote(url, options=options)
    session["session_id"] = driver.session_id
    save_session(session["name"], session)
    return driver


def find_element(driver, args):
    """Find element with multiple fallback strategies."""
    from appium.webdriver.common.appiumby import AppiumBy

    strategies = []

    if args.id:
        val = args.id
        strategies = [
            (AppiumBy.ID, val),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{val}")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{val}")'),
            (AppiumBy.XPATH, f'//*[@resource-id="{val}" or @content-desc="{val}"]'),
        ]
    elif args.text:
        val = args.text
        strategies = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{val}")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{val}")'),
            (AppiumBy.XPATH, f'//*[@text="{val}"]'),
        ]
    elif args.desc:
        val = args.desc
        strategies = [
            (AppiumBy.ACCESSIBILITY_ID, val),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{val}")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{val}")'),
            (AppiumBy.XPATH, f'//*[@content-desc="{val}"]'),
        ]
    elif getattr(args, "desc_contains", None):
        # Substring match on content-desc — useful when full desc is long/dynamic.
        val = args.desc_contains
        strategies = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{val}")'),
            (AppiumBy.XPATH, f'//*[contains(@content-desc, "{val}")]'),
        ]
    elif getattr(args, "text_contains", None):
        val = args.text_contains
        strategies = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{val}")'),
            (AppiumBy.XPATH, f'//*[contains(@text, "{val}")]'),
        ]
    elif args.xpath:
        strategies = [(AppiumBy.XPATH, args.xpath)]
    elif args.coords:
        return None  # Handled separately with W3C actions
    else:
        print("ERROR: Must provide --id, --text, --desc, --xpath, or --coords")
        sys.exit(1)

    last_err = None
    for by, value in strategies:
        try:
            return driver.find_element(by, value)
        except Exception as e:
            last_err = e
            continue

    raise last_err


def tap_coords(driver, x, y):
    """Tap at coordinates using W3C Actions."""
    from selenium.webdriver.common.actions import interaction
    from selenium.webdriver.common.actions.action_builder import ActionBuilder
    from selenium.webdriver.common.actions.pointer_input import PointerInput

    finger = PointerInput(interaction.POINTER_TOUCH, "finger")
    action = ActionBuilder(driver, mouse=finger)
    action.pointer_action.move_to_location(int(x), int(y))
    action.pointer_action.pointer_down()
    action.pointer_action.pause(0.1)
    action.pointer_action.pointer_up()
    action.perform()


def parse_coords(coords_str):
    """Parse 'x,y' string into (x, y) tuple."""
    parts = coords_str.split(",")
    if len(parts) != 2:
        print("ERROR: Coords must be 'x,y' format")
        sys.exit(1)
    return int(parts[0].strip()), int(parts[1].strip())


# ---- Commands ----

def cmd_start(args):
    """Start a new Appium session."""
    name = args.name
    device = args.device
    port = args.port
    package = args.package
    platform = args.platform or "android"

    # Auto-detect device if not provided
    if not device:
        if platform == "android":
            result = subprocess.run(
                ["adb", "devices"], capture_output=True, text=True
            )
            lines = [l for l in result.stdout.strip().split("\n")[1:] if l.strip() and "device" in l]
            if lines:
                device = lines[0].split("\t")[0]
            else:
                print("ERROR: No Android device found. Connect a device or start an emulator.")
                sys.exit(1)
        else:
            device = "auto"

    url = f"http://localhost:{port}"

    session = {
        "name": name,
        "session_id": None,
        "device": device,
        "platform": platform,
        "package": package,
        "appium_url": url,
        "port": port,
    }
    save_session(name, session)

    # Connect and optionally launch app
    driver = get_driver(session)

    if package and not args.no_launch:
        if platform == "android":
            driver.activate_app(package)
        else:
            driver.activate_app(package)
        time.sleep(2)

    print(f"OK: Session '{name}' started")
    print(f"  Device: {device}")
    print(f"  Platform: {platform}")
    print(f"  Package: {package or 'none'}")
    print(f"  Appium: {url}")
    print(f"  Session ID: {driver.session_id}")

    driver.quit()


def cmd_stop(args):
    """Stop and clean up session."""
    name = args.name
    path = session_path(name)
    if os.path.exists(path):
        try:
            session = load_session(name)
            driver = get_driver(session)
            driver.quit()
        except Exception:
            pass
        os.remove(path)
        print(f"OK: Session '{name}' stopped")
    else:
        print(f"OK: No session '{name}' to stop")


def cmd_screenshot(args):
    """Take screenshot and save to file."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        path = args.path or f"/tmp/appium_screenshot_{args.name}.png"
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        driver.save_screenshot(path)
        print(f"OK: Screenshot saved to {path}")
    finally:
        driver.quit()


def cmd_list_elements(args):
    """List UI elements on screen.

    Lists are read live via Appium WebElements, which can go stale on Compose
    UIs that re-render constantly (e.g. MoMo home with animated banners). To
    avoid 'StaleElementReferenceException', each element read is wrapped in
    try/except — stale ones are skipped — and on full failure we retry once.
    """
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.common.exceptions import StaleElementReferenceException

    if args.input:
        xpath = None
        by, sel = AppiumBy.CLASS_NAME, "android.widget.EditText"
    elif args.clickable:
        by, sel = AppiumBy.XPATH, "//*[@clickable='true']"
    else:
        by, sel = AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']"

    def _read_one(el, kind):
        # Each attribute call can throw stale; capture all in one try.
        if kind == "input":
            return {
                "type": "EditText",
                "text": el.text or "",
                "id": el.get_attribute("resource-id") or "",
                "hint": el.get_attribute("hint") or "",
                "coords": f"{el.location['x']},{el.location['y']}",
                "size": f"{el.size['width']}x{el.size['height']}",
                "enabled": el.get_attribute("enabled") == "true",
            }
        return {
            "type": el.get_attribute("className") or "",
            "text": el.text or "",
            "id": el.get_attribute("resource-id") or "",
            "desc": el.get_attribute("content-desc") or "",
            "coords": f"{el.location['x']},{el.location['y']}",
            "size": f"{el.size['width']}x{el.size['height']}",
            "enabled": el.get_attribute("enabled") == "true",
        }

    limit = getattr(args, "limit", None) or 200

    def _scan(driver):
        kind = "input" if args.input else "other"
        out = []
        for el in driver.find_elements(by, sel):
            if len(out) >= limit:
                break
            try:
                out.append(_read_one(el, kind))
            except StaleElementReferenceException:
                continue
            except Exception:
                continue
        return out

    session = load_session(args.name)
    driver = get_driver(session)
    # Cap server-side find time so heavy RN pages don't hang the CLI forever.
    # On big pages (e.g. hotel detail with 500+ views), find_elements can wedge
    # the UiAutomator2 instrumentation; a hard timeout lets us fail fast and
    # fall back to page_source or coordinates.
    try:
        driver.set_page_load_timeout(15)
    except Exception:
        pass
    try:
        elements = _scan(driver)
        # Retry once if everything went stale
        if not elements:
            time.sleep(0.5)
            elements = _scan(driver)
        print(json.dumps(elements, indent=2, ensure_ascii=False))
        print(f"\n# Total: {len(elements)} elements (limit={limit})")
    except Exception as e:
        print(f"ERROR: list_elements failed — page may be too heavy. "
              f"Try --limit smaller, or use page_source / coords. ({type(e).__name__})")
        sys.exit(2)
    finally:
        try:
            driver.quit()
        except Exception:
            pass


def cmd_page_source(args):
    """Dump page source XML."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        source = driver.page_source
        path = args.path or f"/tmp/appium_page_source_{args.name}.xml"
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(source)
        print(f"OK: Page source saved to {path}")
    finally:
        driver.quit()


def cmd_tap(args):
    """Tap an element or coordinates."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        if args.coords:
            x, y = parse_coords(args.coords)
            tap_coords(driver, x, y)
            print(f"OK: Tapped at ({x}, {y})")
        else:
            el = find_element(driver, args)
            el.click()
            selector = args.id or args.text or args.desc or args.xpath
            print(f"OK: Tapped element '{selector}'")
    finally:
        driver.quit()


def cmd_type(args):
    """Type text into an element."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        el = find_element(driver, args)
        if args.clear:
            try:
                el.clear()
            except Exception:
                pass
        selector = args.id or args.text or args.desc or args.xpath
        try:
            el.send_keys(args.value)
        except Exception:
            # Fallback: tap element first, then use ADB keyboard input
            try:
                el.click()
            except Exception:
                pass
            time.sleep(0.5)
            # Use ADB to type (works with Compose UI)
            escaped = args.value.replace(" ", "%s").replace("'", "\\'")
            subprocess.run(
                ["adb", "-s", session["device"], "shell", "input", "text", escaped],
                capture_output=True, text=True, timeout=10
            )
        print(f"OK: Typed '{args.value}' into '{selector}'")
    finally:
        driver.quit()


def cmd_clear(args):
    """Clear an input field."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        el = find_element(driver, args)
        el.clear()
        selector = args.id or args.text or args.desc or args.xpath
        print(f"OK: Cleared '{selector}'")
    finally:
        driver.quit()


def cmd_swipe(args):
    """Swipe on screen."""
    from selenium.webdriver.common.actions import interaction
    from selenium.webdriver.common.actions.action_builder import ActionBuilder
    from selenium.webdriver.common.actions.pointer_input import PointerInput

    session = load_session(args.name)
    driver = get_driver(session)
    try:
        size = driver.get_window_size()
        w, h = size["width"], size["height"]
        cx, cy = w // 2, h // 2
        dist = args.distance or int(h * 0.3)

        directions = {
            "up":    (cx, cy + dist // 2, cx, cy - dist // 2),
            "down":  (cx, cy - dist // 2, cx, cy + dist // 2),
            "left":  (cx + dist // 2, cy, cx - dist // 2, cy),
            "right": (cx - dist // 2, cy, cx + dist // 2, cy),
        }

        if args.direction not in directions:
            print(f"ERROR: Direction must be up/down/left/right")
            sys.exit(1)

        sx, sy, ex, ey = directions[args.direction]

        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        action = ActionBuilder(driver, mouse=finger)
        action.pointer_action.move_to_location(sx, sy)
        action.pointer_action.pointer_down()
        action.pointer_action.pause(0.1)
        action.pointer_action.move_to_location(ex, ey)
        action.pointer_action.pause(0.5)
        action.pointer_action.pointer_up()
        action.perform()

        print(f"OK: Swiped {args.direction} ({sx},{sy}) → ({ex},{ey})")
    finally:
        driver.quit()


def cmd_back(args):
    """Press back button."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        driver.back()
        print("OK: Pressed BACK")
    finally:
        driver.quit()


def cmd_home(args):
    """Press home button."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        if session["platform"] == "android":
            driver.press_keycode(3)  # KEYCODE_HOME
        else:
            driver.execute_script("mobile: pressButton", {"name": "home"})
        print("OK: Pressed HOME")
    finally:
        driver.quit()


def cmd_wait(args):
    """Wait for element to appear."""
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    session = load_session(args.name)
    driver = get_driver(session)
    timeout = args.timeout or 10
    try:
        tc = getattr(args, "text_contains", None)
        dc = getattr(args, "desc_contains", None)
        if args.id:
            locator = (AppiumBy.ID, args.id)
        elif args.text:
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{args.text}")')
        elif args.desc:
            locator = (AppiumBy.ACCESSIBILITY_ID, args.desc)
        elif tc:
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{tc}")')
        elif dc:
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{dc}")')
        else:
            print("ERROR: Must provide --id, --text, --desc, --text-contains, or --desc-contains")
            sys.exit(1)

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        selector = args.id or args.text or args.desc or tc or dc
        print(f"OK: Element '{selector}' found within {timeout}s")
    except Exception:
        selector = args.id or args.text or args.desc or tc or dc
        print(f"FAIL: Element '{selector}' not found after {timeout}s")
        sys.exit(1)
    finally:
        driver.quit()


def cmd_is_enabled(args):
    """Check if an element is enabled (not greyed out / disabled)."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        el = find_element(driver, args)
        enabled = el.get_attribute("enabled") == "true"
        print(f"{'OK' if enabled else 'DISABLED'}: enabled={enabled}")
        if not enabled:
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: element not found ({type(e).__name__})")
        sys.exit(2)
    finally:
        driver.quit()


def cmd_scroll_to(args):
    """Scroll to find element by text (UiScrollable)."""
    from appium.webdriver.common.appiumby import AppiumBy

    session = load_session(args.name)
    driver = get_driver(session)
    timeout = getattr(args, 'timeout', 10) or 10
    # Set implicit wait as timeout for UiScrollable
    driver.implicitly_wait(timeout)
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.setMaxSearchSwipes(5)'
            f'.scrollIntoView(new UiSelector().text("{args.text}"))'
        )
        print(f"OK: Scrolled to '{args.text}'")
    except Exception:
        print(f"FAIL: Could not scroll to '{args.text}' (max 5 swipes, {timeout}s timeout)")
        sys.exit(1)
    finally:
        driver.implicitly_wait(0)
        driver.quit()


def cmd_long_press(args):
    """Long press on element or coordinates."""
    from selenium.webdriver.common.actions import interaction
    from selenium.webdriver.common.actions.action_builder import ActionBuilder
    from selenium.webdriver.common.actions.pointer_input import PointerInput

    session = load_session(args.name)
    driver = get_driver(session)
    duration = (args.duration or 2000) / 1000.0
    try:
        if args.coords:
            x, y = parse_coords(args.coords)
        else:
            el = find_element(driver, args)
            x = el.location["x"] + el.size["width"] // 2
            y = el.location["y"] + el.size["height"] // 2

        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        action = ActionBuilder(driver, mouse=finger)
        action.pointer_action.move_to_location(x, y)
        action.pointer_action.pointer_down()
        action.pointer_action.pause(duration)
        action.pointer_action.pointer_up()
        action.perform()

        print(f"OK: Long pressed at ({x}, {y}) for {duration}s")
    finally:
        driver.quit()


def cmd_app(args):
    """App lifecycle: launch, terminate, list."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        if args.action == "launch":
            driver.activate_app(args.package)
            time.sleep(2)
            print(f"OK: Launched {args.package}")
        elif args.action == "terminate":
            driver.terminate_app(args.package)
            print(f"OK: Terminated {args.package}")
        elif args.action == "list":
            # List running apps via adb
            result = subprocess.run(
                ["adb", "-s", session["device"], "shell", "pm", "list", "packages", "-3"],
                capture_output=True, text=True
            )
            for line in result.stdout.strip().split("\n"):
                if line.startswith("package:"):
                    print(line[8:])
    finally:
        driver.quit()


def cmd_info(args):
    """Get screen info: size, orientation, activity."""
    session = load_session(args.name)
    driver = get_driver(session)
    try:
        size = driver.get_window_size()
        orientation = driver.orientation
        try:
            activity = driver.current_activity
            package = driver.current_package
        except Exception:
            activity = "unknown"
            package = "unknown"

        info = {
            "screen_width": size["width"],
            "screen_height": size["height"],
            "orientation": orientation,
            "current_activity": activity,
            "current_package": package,
            "device": session["device"],
            "platform": session["platform"],
            "session_name": session["name"],
        }
        print(json.dumps(info, indent=2))
    finally:
        driver.quit()


# ---- Argument Parser ----

def build_parser():
    parser = argparse.ArgumentParser(
        description="Appium CLI - Interactive mobile app control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--name", default="default", help="Session name (default: 'default')")

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # start
    p = sub.add_parser("start", help="Start Appium session")
    p.add_argument("--package", help="App package/bundle ID")
    p.add_argument("--device", help="Device ID (auto-detect if omitted)")
    p.add_argument("--platform", choices=["android", "ios"], help="Platform (default: android)")
    p.add_argument("--port", type=int, default=4723, help="Appium port (default: 4723)")
    p.add_argument("--no-launch", action="store_true", help="Don't launch the app")

    # stop
    sub.add_parser("stop", help="Stop session")

    # screenshot
    p = sub.add_parser("screenshot", help="Take screenshot")
    p.add_argument("--path", "--output", "-o", dest="path",
                   help="Save path (default: /tmp/appium_screenshot_{name}.png)")

    # list_elements
    p = sub.add_parser("list_elements", help="List UI elements")
    p.add_argument("--clickable", action="store_true", help="Only clickable elements")
    p.add_argument("--input", action="store_true", help="Only input fields")
    p.add_argument("--limit", type=int, default=200, help="Cap result count (default 200)")

    # page_source
    p = sub.add_parser("page_source", help="Dump page source XML")
    p.add_argument("--path", help="Save path")

    # tap
    p = sub.add_parser("tap", help="Tap element or coordinates")
    p.add_argument("--id", help="Resource ID")
    p.add_argument("--text", help="Text content")
    p.add_argument("--desc", help="Content description / accessibility ID")
    p.add_argument("--desc-contains", help="Substring match on content-desc")
    p.add_argument("--text-contains", help="Substring match on text")
    p.add_argument("--xpath", help="XPath")
    p.add_argument("--coords", help="Coordinates 'x,y'")

    # type
    p = sub.add_parser("type", help="Type text into element")
    p.add_argument("--id", help="Resource ID")
    p.add_argument("--text", help="Text content to find element")
    p.add_argument("--desc", help="Content description")
    p.add_argument("--desc-contains", help="Substring match on content-desc")
    p.add_argument("--text-contains", help="Substring match on text")
    p.add_argument("--xpath", help="XPath")
    p.add_argument("--value", required=True, help="Text to type")
    p.add_argument("--clear", action="store_true", help="Clear field before typing")

    # clear
    p = sub.add_parser("clear", help="Clear input field")
    p.add_argument("--id", help="Resource ID")
    p.add_argument("--text", help="Text content")
    p.add_argument("--desc", help="Content description")
    p.add_argument("--desc-contains", help="Substring match on content-desc")
    p.add_argument("--text-contains", help="Substring match on text")
    p.add_argument("--xpath", help="XPath")

    # swipe
    p = sub.add_parser("swipe", help="Swipe on screen")
    p.add_argument("direction", choices=["up", "down", "left", "right"])
    p.add_argument("--distance", type=int, help="Swipe distance in pixels")

    # back
    sub.add_parser("back", help="Press BACK")

    # home
    sub.add_parser("home", help="Press HOME")

    # wait
    p = sub.add_parser("wait", help="Wait for element")
    p.add_argument("--id", help="Resource ID")
    p.add_argument("--text", help="Text content")
    p.add_argument("--desc", help="Content description")
    p.add_argument("--desc-contains", help="Substring match on content-desc")
    p.add_argument("--text-contains", help="Substring match on text")
    p.add_argument("--timeout", type=int, default=10, help="Timeout seconds (default: 10)")

    # is_enabled
    p = sub.add_parser("is_enabled", help="Check if element is enabled (exit 0 if enabled, 1 if disabled, 2 if not found)")
    p.add_argument("--id", help="Resource ID")
    p.add_argument("--text", help="Text content")
    p.add_argument("--desc", help="Content description")
    p.add_argument("--desc-contains", help="Substring match on content-desc")
    p.add_argument("--text-contains", help="Substring match on text")
    p.add_argument("--xpath", help="XPath")

    # scroll_to
    p = sub.add_parser("scroll_to", help="Scroll to find text")
    p.add_argument("--text", required=True, help="Text to scroll to")
    p.add_argument("--timeout", type=int, default=10, help="Timeout seconds (default: 10)")

    # long_press
    p = sub.add_parser("long_press", help="Long press")
    p.add_argument("--id", help="Resource ID")
    p.add_argument("--text", help="Text content")
    p.add_argument("--desc", help="Content description")
    p.add_argument("--desc-contains", help="Substring match on content-desc")
    p.add_argument("--text-contains", help="Substring match on text")
    p.add_argument("--xpath", help="XPath")
    p.add_argument("--coords", help="Coordinates 'x,y'")
    p.add_argument("--duration", type=int, default=2000, help="Duration ms (default: 2000)")

    # app
    p = sub.add_parser("app", help="App lifecycle")
    p.add_argument("action", choices=["launch", "terminate", "list"])
    p.add_argument("--package", help="Package name (for launch/terminate)")

    # info
    sub.add_parser("info", help="Screen and device info")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "start": cmd_start,
        "stop": cmd_stop,
        "screenshot": cmd_screenshot,
        "list_elements": cmd_list_elements,
        "page_source": cmd_page_source,
        "tap": cmd_tap,
        "type": cmd_type,
        "clear": cmd_clear,
        "swipe": cmd_swipe,
        "back": cmd_back,
        "home": cmd_home,
        "wait": cmd_wait,
        "is_enabled": cmd_is_enabled,
        "scroll_to": cmd_scroll_to,
        "long_press": cmd_long_press,
        "app": cmd_app,
        "info": cmd_info,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
