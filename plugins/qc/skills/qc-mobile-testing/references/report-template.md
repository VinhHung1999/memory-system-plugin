# QC Report Template

## Single Flow Report

```markdown
# QC Report: [App Name] - [Flow Name]

**Date**: YYYY-MM-DD HH:MM
**Device**: [device ID / model]
**App**: [package name] v[version if known]
**Session**: [session name]

## Summary

| Metric | Value |
|--------|-------|
| Test Cases | N |
| Passed | N |
| Failed | N |
| Total Steps | N |
| Duration | Nm Ns |
| Overall | PASS / FAIL |

## Test Results

### TC-01: [Test Case Name] — PASS

| Step | Action | Expected | Actual | Status |
|------|--------|----------|--------|--------|
| 1 | Open app | Home screen | Home screen displayed | PASS |
| 2 | Tap "Transfer" | Transfer screen | Transfer screen loaded | PASS |
| 3 | Enter phone | Phone shown in field | "0908144825" displayed | PASS |

**Screenshots**: step01.png, step02.png, step03.png

### TC-02: [Test Case Name] — FAIL

| Step | Action | Expected | Actual | Status |
|------|--------|----------|--------|--------|
| 1 | Enter invalid phone "123" | Error message | No error shown | FAIL |

**Screenshots**: tc02_step01.png
**Issue**: No validation for short phone numbers

## Issues Found

| # | Severity | Description | Screenshot |
|---|----------|-------------|------------|
| 1 | HIGH | No phone validation for short numbers | tc02_step01.png |
| 2 | LOW | Loading spinner shows for 5s on slow network | step04.png |

## Notes
- [Observations about UI quality, performance, accessibility]
- [Edge cases encountered]
```

## Regression Report

```markdown
# Regression Report

**Date**: YYYY-MM-DD HH:MM
**Device**: [device]
**App**: [package] v[version]

## Summary

| # | Flow | Status | Duration | Script |
|---|------|--------|----------|--------|
| 1 | Transfer | PASS | 45s | transfer-flow/automation-script.py |
| 2 | Login | PASS | 30s | login-flow/automation-script.py |
| 3 | Onboarding | FAIL | 25s | onboarding-flow/automation-script.py |

**Total**: 2/3 PASS (66.7%)
**Production Ready**: NO

## Failed Tests

### 3. Onboarding
- **Failed at**: Step 5 - Assert "Welcome screen"
- **Error**: Element not found after 10s timeout
- **Screenshot**: regression-screenshots/onboarding_fail.png
- **Possible cause**: UI changed after latest deploy

## Recommendation
- Fix onboarding before release
- Rerun regression after fix
```
