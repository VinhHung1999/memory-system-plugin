# QC Mobile Agent - Implementation Plan

## Problem

| Approach | Issue |
|----------|-------|
| Appium (viết script) | Viết mù → chạy → fail → sửa → chạy lại = tốn thời gian |
| mobile-mcp (MCP tools) | Interactive nhưng yếu với Compose UI, custom input fields |

## Solution: Appium CLI + QC Agent

### Core Idea

Tạo `appium_cli.py` - persistent Appium session, agent gọi commands trực tiếp qua Bash:

```bash
python appium_cli.py screenshot
python appium_cli.py list_elements
python appium_cli.py tap --id "com.app:id/btn"
python appium_cli.py type --id "com.app:id/input" --text "hello"
python appium_cli.py swipe up
```

Giống playwright-cli nhưng cho mobile. Agent explore app interactively, thấy kết quả ngay, không cần viết file script.

---

## Files cần tạo

### 1. `appium_cli.py` (Core CLI tool)
```
~/.claude/skills/qc-mobile-testing/scripts/appium_cli.py
```

**Commands:**

| Command | Args | Description |
|---------|------|-------------|
| `start` | `--package <pkg>` `--no-launch` | Start Appium session, launch app |
| `stop` | | Close session |
| `screenshot` | `--path <file>` | Chụp screenshot, save file |
| `list_elements` | `--clickable` `--input` | List UI elements + selectors |
| `page_source` | `--path <file>` | Dump XML page source |
| `tap` | `--id <id>` `--text <text>` `--desc <desc>` `--coords <x,y>` | Tap element |
| `type` | `--id <id>` `--text <text>` `--value <value>` | Type text vào element |
| `swipe` | `<direction>` `--distance <px>` | Swipe up/down/left/right |
| `back` | | Press back |
| `home` | | Press home |
| `wait` | `--id <id>` `--text <text>` `--timeout <s>` | Wait for element xuất hiện |
| `app` | `launch <pkg>` / `terminate <pkg>` / `list` | App lifecycle |
| `scroll_to` | `--text <text>` | UiScrollable.scrollIntoView |
| `clear` | `--id <id>` | Clear input field |
| `long_press` | `--id <id>` `--coords <x,y>` `--duration <ms>` | Long press |
| `info` | | Screen size, orientation, current activity |

**Element finding priority:**
1. `--id` → `AppiumBy.ID` (resource-id)
2. `--text` → `AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("...")'`
3. `--desc` → `AppiumBy.ACCESSIBILITY_ID` (content-desc)
4. `--xpath` → `AppiumBy.XPATH`
5. `--coords x,y` → W3C Actions tap

**Session management (multi-session, multi-device):**
- Mỗi session có `--name` riêng biệt
- `start` lưu session info vào `/tmp/appium_cli_{name}.json`
- Các command sau dùng `--name` để chỉ đúng session
- Không cần giữ process chạy liên tục - mỗi command tự connect/disconnect
- `stop --name` xóa session file
- Nếu không truyền `--name` → dùng "default"

**Multi-device parallel:**
```bash
# 3 QC agents chạy song song trên 3 devices
python appium_cli.py start --name "transfer" --device emulator-5554 --port 4723
python appium_cli.py start --name "login" --device R5CT1234 --port 4724
python appium_cli.py start --name "onboard" --device "iPhone 16 Pro" --port 4725

# Mỗi agent dùng --name để chỉ session của mình
python appium_cli.py --name "transfer" tap --text "Chuyển tiền"
python appium_cli.py --name "login" type --id "email" --value "test@mail.com"
python appium_cli.py --name "onboard" swipe left
```

**Session file format** (`/tmp/appium_cli_{name}.json`):
```json
{
  "name": "transfer",
  "session_id": "abc123",
  "device": "emulator-5554",
  "platform": "android",
  "package": "vn.momo.platform.test",
  "appium_url": "http://localhost:4723",
  "port": 4723
}
```

**Lưu ý:** Mỗi session cần device riêng + port Appium riêng. Không thể 2 session trên cùng 1 device.

**Output format:** JSON cho list_elements, plain text cho actions, file path cho screenshot.

### 2. Skill `SKILL.md`
```
~/.claude/skills/qc-mobile-testing/SKILL.md
```

Hướng dẫn agent:
- Cách dùng `appium_cli.py` (commands, args, examples)
- Workflow QC: Start → Explore → QC → Report → Sinh automation script
- Cách ghi exploration log
- Cách handle edge cases (permission, PIN, loading, Compose)
- Format QC report
- Khi nào dùng appium_cli vs mobile-mcp

### 3. References

```
~/.claude/skills/qc-mobile-testing/references/report-template.md
```
- Template QC report: summary, step-by-step, issues, screenshots

```
~/.claude/skills/qc-mobile-testing/references/appium-templates.md  
```
- Code templates cho sinh automation script từ exploration log

### 4. Subagent
```
~/.claude/agents/qc-mobile.md
```
- System prompt cho QC agent
- Skills: `qc-mobile-testing`, `mobile-app-testing`
- Model: sonnet (nhanh, đủ tốt cho QC)
- maxTurns: 80

---

## Workspace Structure

Mọi output nằm gọn trong 1 folder tại nơi user gọi QC:

```
./qc-workspace/                          ← tạo tự động tại working directory (per project)
  .memory/                               ← knowledge base tích lũy cho dự án này
    app-knowledge.md                     ← kiến thức về app (selectors, navigation, edge cases)
  transfer-flow-20260406-1830/           ← mỗi lần QC = 1 folder (flow + timestamp)
    test-cases.md                        ← Step 0: test cases (QC Agent viết, user confirm)
    screenshots/
      step01_home.png
      step02_transfer.png
      step03_phone.png
      error_step05.png
    explore-log.md                       ← ghi liên tục trong quá trình QC
    qc-report.md                         ← kết quả pass/fail
    automation-script.py                 ← bắt buộc, sinh sau khi QC xong
  login-flow-20260406-1835/              ← flow khác chạy song song
    test-cases.md
    screenshots/
    explore-log.md
    qc-report.md
```

### Project Memory (`.memory/`)

Mỗi dự án có memory riêng, tích lũy qua các lần QC:

```markdown
# App Knowledge: MoMo (vn.momo.platform.test)
Last updated: 2026-04-06

## Navigation Structure
- Home không có nút "Chuyển tiền" trực tiếp → vào qua search bar
- Bottom tabs: MoMo, Ưu đãi, Quét QR, Lịch sử GD, Tôi
- Túi Thần Tài: bấm trên home → cần PIN

## Verified Selectors
- Search bar: id="searchBar" (custom Compose)
- Search input: id="input_search" (EditText)
- PIN input: id="input_bottomsheet_password"
- Confirm button: id="com.app:id/confirm"

## Edge Cases
- Mở app → popup "Bundle Load Time" → bấm OK
- Random promo popup → dismiss bằng nút X (label="icon_xbanner_close")
- Xác thực hết hạn banner → bấm X để đóng

## Flows đã test
- [2026-04-06] Chuyển tiền: search → Chuyển tiền MoMo → SĐT → tiền → PIN → thành công
- [2026-04-06] Túi Thần Tài: tap home → PIN → dashboard
```

**QC Agent workflow với memory:**
1. Trước khi explore → đọc `qc-workspace/.memory/app-knowledge.md`
2. Dùng selectors đã verify → skip bước dò tìm
3. Biết trước edge cases → handle nhanh (dismiss popup, etc.)
4. Sau khi QC xong → update memory với kiến thức mới
5. Lần QC sau → nhanh hơn vì đã biết app structure

---

## Workflow khi sử dụng

### Single flow: "QC flow chuyển tiền trên MoMo"

**Step 0: QC Agent viết test cases**

QC Agent phân tích yêu cầu → viết test cases → hỏi user confirm:

```markdown
# Test Cases: Chuyển tiền MoMo

## TC-01: Chuyển tiền thành công (happy path)
- Mở app → navigate đến Chuyển tiền
- Nhập SĐT hợp lệ (0908144825)
- Nhập số tiền (10,000đ)
- Bấm Tiếp tục → xác nhận → nhập PIN
- Expected: Hiện "Giao dịch thành công"

## TC-02: SĐT không hợp lệ
- Nhập SĐT sai format ("123", "abc")
- Expected: Hiện lỗi validation, không cho tiếp tục

## TC-03: Số tiền dưới minimum
- Nhập số tiền 0 hoặc 100
- Expected: Nút Tiếp tục disable hoặc hiện lỗi

## TC-04: Hủy giao dịch
- Điền form → bấm Back
- Expected: Quay về home, không mất tiền
```

→ Lưu vào `qc-workspace/{flow}/test-cases.md`
→ Hỏi user: "Tôi dự định test 4 cases này, OK không?"
→ User confirm / chỉnh sửa → tiếp tục

**Step 1: QC Agent setup session**
```bash
python appium_cli.py start --name "transfer" --package vn.momo.platform.test --device emulator-5554
```

**Step 2: QC Agent gửi subagent (truyền session name)**
```
QC Agent → Subagent: "Dùng session 'transfer'. Screenshot home, 
                      liệt kê các nút liên quan đến chuyển tiền"
  │
  └─ Subagent chạy:
      python appium_cli.py --name "transfer" screenshot --path /tmp/qc/transfer/step01.png
      python appium_cli.py --name "transfer" list_elements --clickable
      → Trả về summary cho QC Agent
```

**Step 3: QC Agent tiếp tục gửi subagent từng bước**
```
QC Agent → Subagent: "Session 'transfer'. Bấm Chuyển tiền, nhập SĐT 0908144825"
  └─ Subagent:
      python appium_cli.py --name "transfer" tap --text "Chuyển tiền"
      python appium_cli.py --name "transfer" type --id "phone_input" --value "0908144825"
      python appium_cli.py --name "transfer" screenshot --path /tmp/qc/transfer/step02.png
      → Trả summary + selectors đã dùng
```

**Step 3: QC Agent tổng hợp → QC Report**

**Step 4: Sinh automation script** từ explore log.

**Step 5: Cập nhật project memory**
- Update `qc-workspace/.memory/app-knowledge.md` với kiến thức mới:
  - Selectors mới phát hiện
  - Navigation paths mới
  - Edge cases mới (popup, dialog, loading)
  - Flow đã test thêm vào danh sách

### Parallel: "QC 3 flow cùng lúc trên 3 devices"

```
User: "QC chuyển tiền trên emulator, login trên device thật, onboarding trên iOS"

QC Agent:
  │
  │ Step 1: Setup 3 sessions
  │ python appium_cli.py start --name "transfer" --device emulator-5554 --port 4723
  │ python appium_cli.py start --name "login" --device R5CT1234 --port 4724
  │ python appium_cli.py start --name "onboard" --device "iPhone 16 Pro" --port 4725
  │
  │ Step 2: Spawn 3 subagents song song (run_in_background=true)
  │
  ├─ Subagent 1: "Session 'transfer'. Test flow chuyển 10k cho SĐT 0908144825"
  │   python appium_cli.py --name "transfer" screenshot ...
  │   python appium_cli.py --name "transfer" tap ...
  │   → Trả summary + explore log
  │
  ├─ Subagent 2: "Session 'login'. Test login với email test@mail.com"
  │   python appium_cli.py --name "login" screenshot ...
  │   python appium_cli.py --name "login" type ...
  │   → Trả summary + explore log
  │
  └─ Subagent 3: "Session 'onboard'. Test onboarding flow mới"
      python appium_cli.py --name "onboard" screenshot ...
      python appium_cli.py --name "onboard" swipe ...
      → Trả summary + explore log

  │ Step 3: Thu thập 3 summaries → sinh QC Report tổng hợp
  │
  │ Step 4: Cleanup
  │ python appium_cli.py stop --name "transfer"
  │ python appium_cli.py stop --name "login"  
  │ python appium_cli.py stop --name "onboard"
```

---

## Context Management: Agent → Subagent Pattern

### Vấn đề

Mỗi lần explore 1 screen:
- `screenshot` → image token rất lớn
- `list_elements` → 50-80 elements với text/label/id/coordinates → vài ngàn tokens
- Nhân 10-15 screens trong 1 flow → **context tràn**

### Giải pháp: QC Agent chỉ đạo, Subagent thao tác

```
QC Agent (main) — giữ context nhẹ, chỉ lưu summaries
  │
  ├─ Subagent: "Explore screen Home, tìm nút Chuyển tiền và bấm vào"
  │   → screenshot + list_elements (context nặng, nằm ở subagent)
  │   → Tìm "Chuyển tiền" tại id=xxx → bấm → screenshot verify
  │   → Trả về summary: "Đã bấm Chuyển tiền. Màn hình Transfer có:
  │                       input phone (id=yyy), input amount (id=zzz),
  │                       nút Tiếp tục (id=abc)"
  │
  ├─ Subagent: "Nhập SĐT 0908144825, nhập 10000, bấm Tiếp tục"
  │   → Thực hiện 3 actions → screenshot verify
  │   → Trả về: "Xong. Màn hình xác nhận: Người nhận Nguyễn Văn A,
  │              Số tiền 10,000đ, nút Xác nhận (id=def)"
  │
  ├─ Subagent: "Bấm Xác nhận, nhập PIN 000000"
  │   → Thực hiện → screenshot verify
  │   → Trả về: "Chuyển tiền thành công. Màn hình kết quả hiển thị
  │              'Giao dịch thành công', mã GD: ABC123"
  │
  └─ QC Agent tổng hợp summaries → sinh QC Report
```

### Vai trò

| | QC Agent (main) | Subagent (worker) |
|---|---|---|
| Vai trò | **Bộ não** - quyết định mọi thứ | **Tay chân** - thực thi lệnh |
| Context | Nhẹ - chỉ giữ summaries | Nặng - screenshot + elements |
| Input | Test case từ user | Instruction cụ thể từ QC Agent |
| Output | QC Report | Summary ngắn gọn |
| Lifetime | Toàn bộ QC session | 1 screen hoặc 1 nhóm actions |

### QC Agent quyết định, Subagent thực thi

QC Agent là người **ra mọi quyết định**:
- Phân tích test case → xác định flow cần test
- Quyết định bấm vào đâu, nhập gì, verify cái gì
- Đánh giá pass/fail dựa trên summary từ subagent
- Quyết định bước tiếp theo dựa trên kết quả trước đó

Subagent **chỉ thực thi** lệnh từ QC Agent:
- Nhận instruction cụ thể (VD: "bấm nút có text 'Chuyển tiền'")
- Dùng appium_cli.py để thực hiện
- Screenshot + list elements nếu cần
- Trả về summary kết quả (không quyết định gì)

**Ví dụ thực tế:**

```
QC Agent nhận: "Test flow chuyển tiền 10k cho SĐT 0908144825"
  │
  │ QC Agent suy nghĩ: "Cần mở app → tìm nút chuyển tiền → nhập SĐT → nhập tiền → xác nhận"
  │
  ├─ QC Agent gửi subagent: "Mở app vn.momo.platform.test, screenshot home,
  │                           liệt kê các nút liên quan đến chuyển tiền"
  │   └─ Subagent: thực hiện → trả về "Home có: Nạp/Rút, Nhận tiền, QR Thanh toán, 
  │                                     Ví tiện ích. Không thấy nút Chuyển tiền trực tiếp.
  │                                     Search bar ghi 'Tìm người nhận chuyển khoản'"
  │
  │ QC Agent suy nghĩ: "Không có nút chuyển tiền → thử bấm search bar"
  │
  ├─ QC Agent gửi subagent: "Bấm vào search bar, tìm 'chuyển tiền', 
  │                           báo lại kết quả tìm kiếm"
  │   └─ Subagent: thực hiện → trả về "Tìm thấy dịch vụ 'Chuyển tiền MoMo', 
  │                                     'Chuyển tiền Ngân hàng'. Bấm cái nào?"
  │
  │ QC Agent suy nghĩ: "Chuyển cho SĐT MoMo → chọn 'Chuyển tiền MoMo'"
  │
  ├─ QC Agent gửi subagent: "Bấm 'Chuyển tiền MoMo', nhập SĐT 0908144825,
  │                           nhập số tiền 10000, screenshot kết quả"
  │   └─ Subagent: thực hiện → trả về kết quả
  │
  └─ QC Agent: tổng hợp → sinh QC Report
```

### Khi nào gọi subagent vs làm trực tiếp

- **Gọi subagent**: Khi cần screenshot + list_elements + phân tích (nặng context)
- **Làm trực tiếp**: Khi chỉ cần action đơn giản không cần xem kết quả chi tiết (VD: bấm back, swipe)

### Implementation trong subagent definition

QC Agent sẽ dùng `Agent` tool để spawn worker subagents. Mỗi worker:
- Nhận instruction cụ thể ("bấm vào X", "nhập Y vào Z") + session name
- Có access đến appium_cli.py qua Bash
- Tự retry cơ bản (wait, scroll, thử lại) trước khi báo lỗi
- Trả về response theo format chuẩn bên dưới

### Subagent response format (BẮT BUỘC)

Subagent **phải trả về đúng format** này để QC Agent parse được:

```
ACTION: tap --text "Chuyển tiền MoMo"
SELECTOR_USED: text="Chuyển tiền MoMo"
ALT_SELECTORS: id=com.app:id/transfer, desc=Transfer
RESULT: OK | FAIL | ERROR
SCREENSHOT: /tmp/qc/step04.png
ELEMENTS_ON_SCREEN:
  - EditText "Nhập số điện thoại" id=com.app:id/phone coords=(200,300)
  - EditText "Số tiền" id=com.app:id/amount coords=(200,450)
  - Button "Tiếp tục" id=com.app:id/next coords=(300,600)
NOTE: (optional) Có permission dialog, đã bấm Allow
```

**Các trường:**

| Trường | Bắt buộc | Mô tả |
|--------|----------|-------|
| ACTION | Yes | Command đã thực thi |
| SELECTOR_USED | Yes | Selector thành công (dùng cho explore log + sinh script) |
| ALT_SELECTORS | No | Các selector khác cũng match (backup cho script) |
| RESULT | Yes | OK, FAIL (element không tìm thấy), ERROR (crash/exception) |
| SCREENSHOT | Yes | Path screenshot sau action |
| ELEMENTS_ON_SCREEN | Yes | Elements trên screen mới (text, id, coords) |
| NOTE | No | Ghi chú đặc biệt (dialog, loading, warning) |

**Khi FAIL/ERROR:**
```
ACTION: tap --text "Chuyển tiền"
SELECTOR_USED: none
RESULT: FAIL
RETRY_LOG:
  - Attempt 1: tap --text "Chuyển tiền" → not found
  - Attempt 2: wait 3s → tap --text "Chuyển tiền" → not found  
  - Attempt 3: scroll down → tap --text "Chuyển tiền" → not found
SCREENSHOT: /tmp/qc/error_step03.png
ELEMENTS_ON_SCREEN:
  - Button "Nạp/Rút" id=com.app:id/topup coords=(152,748)
  - Button "Nhận tiền" id=com.app:id/receive coords=(464,748)
NOTE: Element "Chuyển tiền" không có trên screen hiện tại. Có thể cần scroll thêm hoặc navigate khác.
```

---

## Exploration Log: Sản phẩm phụ của QC

### Explore log KHÔNG phải phase riêng

Explore log được ghi **liên tục** trong quá trình QC. Mỗi lần subagent trả summary, QC Agent vừa đánh giá pass/fail, vừa ghi log. Không có bước explore riêng rồi mới QC.

### Flow ghi log

```
QC Agent gửi subagent: "Bấm Chuyển tiền"
  └─ Subagent trả: "Đã bấm. Dùng tap --text 'Chuyển tiền'.
                     Màn hình mới có input phone id=com.app:id/phone"

QC Agent làm 2 việc cùng lúc:
  1. QC: Đánh giá PASS ✓ (navigate đúng màn hình)
  2. Ghi explore log:
     ┌─────────────────────────────────────────────┐
     │ Step 3: Bấm Chuyển tiền                     │
     │ Action: tap --text "Chuyển tiền"             │
     │ Selector: text="Chuyển tiền"                 │
     │ Result: OK - Navigated to Transfer screen    │
     │ Screenshot: /tmp/qc/step03.png               │
     │ Elements: input phone (id=com.app:id/phone)  │
     └─────────────────────────────────────────────┘
  3. Quyết định bước tiếp theo
```

### Subagent phải báo lại selector đã dùng

Subagent khi thực thi phải trả về **selector đã dùng thành công**. Đây là thông tin quan trọng nhất cho explore log:

```
Subagent trả về:
  - Action: tap
  - Selector used: --text "Chuyển tiền"  ← CẦN CÁI NÀY
  - Alternative selectors: --id "com.app:id/transfer_btn", --desc "Transfer"
  - Screenshot saved: /tmp/qc/step03.png
  - New screen elements: [phone input id=xxx, amount input id=yyy, ...]
```

### Explore log format

File: `/tmp/qc-explore-{app}-{flow}-{timestamp}.md`

```markdown
# Explore Log: MoMo - Chuyển tiền
Device: emulator-5554
Package: vn.momo.platform.test
Date: 2026-04-06

## Step 1: Launch app
- Command: appium_cli.py start --package vn.momo.platform.test
- Result: OK
- Screenshot: /tmp/qc/step01.png

## Step 2: Navigate home
- Command: appium_cli.py list_elements --clickable
- Key elements:
  - search bar: id=searchBar, label="Tìm người nhận chuyển khoản"
  - Nạp/Rút: label="TopBarIcon/cash_in_out", coords=(152, 748)
  - Nhận tiền: label="TopBarIcon/topbar_myqrcode", coords=(464, 748)
- Note: Không có nút "Chuyển tiền" trực tiếp trên home

## Step 3: Search "chuyển tiền"
- Command: appium_cli.py tap --id "searchBar"
- Command: appium_cli.py type --id "input_search" --value "chuyen tien"
- Selector used: id="input_search" (EditText)
- Result: Tìm thấy "Chuyển tiền MoMo"
- Screenshot: /tmp/qc/step03.png

## Step 4: Tap "Chuyển tiền MoMo"
- Command: appium_cli.py tap --text "Chuyển tiền MoMo"
- Selector used: text="Chuyển tiền MoMo"
- Result: Mở màn hình chuyển tiền
- Screenshot: /tmp/qc/step04.png
- Elements: phone input (id=com.app:id/phone), amount (id=com.app:id/amount)

...
```

### Explore log ghi assert luôn

QC Agent khi đánh giá pass/fail → ghi assert vào explore log ngay:

```markdown
## Step 4: Tap "Chuyển tiền MoMo"
- Command: tap --text "Chuyển tiền MoMo"
- Selector: text="Chuyển tiền MoMo"
- Alt selectors: id=com.app:id/transfer
- Result: OK
- Screenshot: screenshots/step04.png
- Assert: screen contains text "Nhập số điện thoại"    ← QC Agent ghi luôn
- Elements: EditText id=com.app:id/phone, EditText id=com.app:id/amount
```

Assert là **cái mà QC Agent thấy khi verify** → tự nhiên có, không cần bước riêng.

---

## Script Generation (BẮT BUỘC)

### Khi user nói "sinh script"

QC Agent đọc explore log → sinh Appium Python script chuẩn với:
- **Assert** cho mỗi bước (từ explore log)
- **Parameterize** cho data thay đổi (SĐT, số tiền, PIN...)
- **Comment** chỉ ra step nào trong explore log
- **WebDriverWait** cho mỗi element
- **Screenshot** từng bước

### Script output

Lưu tại: `qc-workspace/{flow}/automation-script.py`

```python
#!/usr/bin/env python3
"""
Auto-generated from explore log
Flow: MoMo - Chuyển tiền
Generated: 2026-04-06
Explore log: qc-workspace/transfer-flow-20260406/explore-log.md
"""

import argparse
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_args():
    parser = argparse.ArgumentParser(description="QC: Chuyển tiền MoMo")
    parser.add_argument("--phone", required=True, help="SĐT người nhận")
    parser.add_argument("--amount", required=True, help="Số tiền")
    parser.add_argument("--pin", required=True, help="Mã PIN")
    parser.add_argument("--device", default="emulator-5554")
    parser.add_argument("--port", type=int, default=4723)
    parser.add_argument("--screenshot-dir", default="./screenshots")
    return parser.parse_args()


def run_test(args):
    os.makedirs(args.screenshot_dir, exist_ok=True)
    
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.udid = args.device
    options.no_reset = True
    driver = webdriver.Remote(f"http://localhost:{args.port}", options=options)
    wait = WebDriverWait(driver, 10)
    results = []

    try:
        # Step 2: Tap search bar (explore: id=searchBar)
        driver.find_element(AppiumBy.ID, "searchBar").click()
        driver.save_screenshot(f"{args.screenshot_dir}/step02.png")

        # Step 3: Type "chuyen tien" (explore: id=input_search)
        search = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "input_search"))
        )
        search.send_keys("chuyen tien")
        driver.save_screenshot(f"{args.screenshot_dir}/step03.png")

        # Step 4: Tap "Chuyển tiền MoMo" (explore: text match)
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Chuyển tiền MoMo")'
        ).click()
        # Assert: screen contains "Nhập số điện thoại" (from explore log step 4)
        assert wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Nhập số điện thoại")'))
        ), "FAIL Step 4: Expected 'Nhập số điện thoại' on Transfer screen"
        results.append(("Step 4: Navigate to Transfer", "PASS"))
        driver.save_screenshot(f"{args.screenshot_dir}/step04.png")

        # Step 5: Enter phone number (explore: id=com.app:id/phone)
        phone_input = driver.find_element(AppiumBy.ID, "com.app:id/phone")
        phone_input.send_keys(args.phone)  # ← parameterized
        driver.save_screenshot(f"{args.screenshot_dir}/step05.png")

        # Step 6: Enter amount (explore: id=com.app:id/amount)
        amount_input = driver.find_element(AppiumBy.ID, "com.app:id/amount")
        amount_input.send_keys(args.amount)  # ← parameterized
        driver.save_screenshot(f"{args.screenshot_dir}/step06.png")

        # Step 7: Tap "Tiếp tục" (explore: id=com.app:id/next)
        driver.find_element(AppiumBy.ID, "com.app:id/next").click()
        # Assert: confirmation screen shows phone + amount
        assert wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{args.phone}")'))
        ), f"FAIL Step 7: Expected phone {args.phone} on confirmation screen"
        results.append(("Step 7: Confirmation screen", "PASS"))
        driver.save_screenshot(f"{args.screenshot_dir}/step07.png")

        # Step 8: Confirm + Enter PIN (explore: PIN input)
        driver.find_element(AppiumBy.ID, "com.app:id/confirm").click()
        pin_input = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "input_bottomsheet_password"))
        )
        pin_input.send_keys(args.pin)  # ← parameterized
        
        # Assert: "Giao dịch thành công" (from explore log step 8)
        assert wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("thành công")'))
        ), "FAIL Step 8: Expected 'Giao dịch thành công'"
        results.append(("Step 8: Transfer success", "PASS"))
        driver.save_screenshot(f"{args.screenshot_dir}/step08_success.png")

    except AssertionError as e:
        results.append((str(e).split(":")[0], "FAIL"))
        driver.save_screenshot(f"{args.screenshot_dir}/failure.png")
        raise
    except Exception as e:
        results.append(("Unexpected error", "ERROR"))
        driver.save_screenshot(f"{args.screenshot_dir}/error.png")
        raise
    finally:
        # Print results summary
        print("\n=== Test Results ===")
        for step, status in results:
            print(f"  [{status}] {step}")
        print(f"  Screenshots: {args.screenshot_dir}/")
        driver.quit()


if __name__ == "__main__":
    args = parse_args()
    run_test(args)
```

### Chạy script

```bash
# Chạy với data cụ thể
python automation-script.py --phone 0908144825 --amount 10000 --pin 000000

# Chạy trên device khác
python automation-script.py --phone 0908144825 --amount 10000 --pin 000000 \
    --device R5CT1234 --port 4724

# Chạy với screenshot dir riêng
python automation-script.py --phone 0908144825 --amount 10000 --pin 000000 \
    --screenshot-dir ./regression-test-01/
```

### Script generation rules

QC Agent khi sinh script phải:
1. **Mỗi step có comment** chỉ ra explore log step tương ứng
2. **Assert từ explore log** - không tự nghĩ assert mới
3. **Parameterize data** - SĐT, số tiền, PIN, email... thành args
4. **Giữ nguyên selector** đã thành công trong explore (SELECTOR_USED)
5. **WebDriverWait** cho mọi element (không hardcode sleep)
6. **Screenshot mỗi bước** + screenshot khi fail
7. **Print results summary** cuối script

---

## Tính năng riêng: Regression Suite (khi user yêu cầu)

User nói: "chạy regression" / "chạy tất cả scripts" / "checklist production"

QC Agent tìm tất cả `automation-script.py` trong workspace → chạy tuần tự hoặc song song → sinh regression report.

### Workspace structure sau nhiều lần QC

```
qc-workspace/
  .memory/
    app-knowledge.md
  transfer-flow-20260406/
    automation-script.py       ← script 1
  login-flow-20260407/
    automation-script.py       ← script 2
  onboarding-flow-20260408/
    automation-script.py       ← script 3
  regression-20260410/         ← regression run output
    results.md
    screenshots/
```

### Chạy regression

```bash
# QC Agent tự tìm tất cả scripts và chạy
find qc-workspace/ -name "automation-script.py" -not -path "*/regression-*"

# Chạy từng script
python qc-workspace/transfer-flow-20260406/automation-script.py --phone 0908144825 --amount 10000 --pin 000000
python qc-workspace/login-flow-20260407/automation-script.py --email test@mail.com --password abc123
python qc-workspace/onboarding-flow-20260408/automation-script.py
```

### Regression Report

Lưu tại: `qc-workspace/regression-{date}/results.md`

```markdown
# Regression Report
Date: 2026-04-10
Device: emulator-5554
App: vn.momo.platform.test v5.06

## Summary
| # | Flow | Status | Duration |
|---|------|--------|----------|
| 1 | Chuyển tiền | PASS | 45s |
| 2 | Login | PASS | 30s |
| 3 | Onboarding | FAIL | 25s |

Total: 2/3 PASS (66.7%)
Production ready: NO

## Failed Tests

### 3. Onboarding
- Failed at: Step 5 - Assert "Welcome screen"
- Error: Element not found after 10s timeout
- Screenshot: screenshots/onboarding_fail.png
- Possible cause: UI changed after latest deploy

## Recommendation
- Fix onboarding flow trước khi release
- Rerun regression sau khi fix
```

### Khi nào chạy regression

- **Chỉ khi user yêu cầu** - không tự động
- User nói: "chạy regression", "kiểm tra production", "chạy tất cả test", "production checklist"
- QC Agent tìm scripts → chạy → report → báo user pass/fail

---

## So sánh

| | mobile-mcp | appium_cli | Viết Appium script |
|---|---|---|---|
| Interactive | Yes | Yes | No |
| Compose UI | Weak | Strong | Strong |
| Input fields | Weak | Strong | Strong |
| UiScrollable | No | Yes | Yes |
| WebDriverWait | No | Yes | Yes |
| Setup | 0 (MCP) | Cần Appium server | Cần Appium server |
| Reusable script | No | No | Yes |

---

## Prerequisites

- Android SDK + ADB
- Appium server (`npm install -g appium`)
- UiAutomator2 driver (`appium driver install uiautomator2`)
- `appium-python-client` (`pip install Appium-Python-Client`)
- Emulator/device đang chạy

(Kiểm tra bằng `~/.claude/skills/mobile-app-testing/scripts/env_check.py`)
