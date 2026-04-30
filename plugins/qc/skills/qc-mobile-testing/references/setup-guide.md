# Infrastructure Setup Guide

## Check Prerequisites
```bash
python ~/.claude/skills/mobile-app-testing/scripts/env_check.py --fix-hints
```

## Start Emulator (if not running)
```bash
adb devices  # check if device listed
# If no device:
emulator -avd Pixel_7_API_34 -no-audio -no-window &
adb wait-for-device
# Wait for boot
while [ "$(adb shell getprop sys.boot_completed 2>/dev/null)" != "1" ]; do sleep 2; done
echo "Emulator ready"
```

## Start Appium Server (if not running)
```bash
curl -s http://localhost:4723/status  # check if running
# If no response:
appium --port 4723 --relaxed-security &
# Wait until ready
while ! curl -s http://localhost:4723/status > /dev/null 2>&1; do sleep 1; done
echo "Appium ready"
```

## Port Forwarding (if app connects to local services)
```bash
adb reverse tcp:8081 tcp:8081
adb reverse tcp:8181 tcp:8181
```

## Multiple Devices
Each device needs a separate Appium port:
```bash
appium --port 4723 --relaxed-security &  # device 1
appium --port 4724 --relaxed-security &  # device 2
```
