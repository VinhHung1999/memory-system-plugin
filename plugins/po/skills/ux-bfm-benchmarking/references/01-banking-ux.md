# Banking UX Benchmarking

## Core Principle
UK banking apps serve the same fundamental tasks — check balance, make payments, manage cards — but the UX quality varies enormously. BFM's banking benchmarks (chapters 7, 8, 9) reveal that the gap between traditional banks and challengers (Monzo, Starling) is not primarily technological — it is a design and product culture difference. Traditional banks add steps; challengers remove them.

## Key Benchmarks

### Transaction Notifications (Chapter 9)
BFM tested the same £1.00 transaction at "Zettle_*Peter Ramsey C" across 6 UK banks. Each bank showed the same transaction; each formatted the notification differently.

**What the data shows:**
> "Transaction notifications from 6 different banks showing same £1.00 transaction at 'Zettle_*Peter Ramsey C' with variations in how each bank formats the notification."

The insight: notification format is a design decision. Every bank receives the same underlying data. The banks that show "Zettle · Coffee shop · £1.00" are making a different design choice than the banks that show "ZETTLE_*PETER RAMSEY C £1.00."

**Best practice:** Clean merchant name, category, amount, and timestamp — all visible at notification level without opening the app.

### Balance Display & Analytics
> "Starling Bank balance screen (Jan 2023) — ending balance £58.69, showing balance trend graph and spending breakdown"
> "Monzo Analytics screen (Dec 2022) — total spend £185, budget £100 with £100 left, showing spending concentration on day 26"

Monzo and Starling expose spending analytics at the balance level — not buried in a separate "analytics" tab. Traditional banks show a number; challengers show context.

> "FlexAccount balance screen — updates after 20 seconds, requires clicking to see payments, doesn't update for pending payments"

Real-time balance with pending transactions visible is now table stakes. A balance that requires a 20-second wait is not just slow — it's a trust problem.

### International Payments (Chapter 7)
> "HSBC international payment — transaction amount (£100 GBP), destination currency (USD 117.34), exchange rate (GBP 1.00 = USD 1.173382)"

HSBC shows the exchange rate and destination amount on the confirmation screen. This is the minimum transparency standard for international payments.

> "Santander international payment form — structured form with 3 steps, requiring beneficiary details (name, address, account number, BIC code, bank details) and payment info"

Santander's international payment requires the full beneficiary address in addition to account number and BIC — more fields than most competitors require for the same task.

**Benchmark standard:** International payment completion in ≤5 screens, with live exchange rate shown before confirmation.

### Card Management (Chapter 8)
BFM's Barclays card management teardown identified:
- "Expired card scenario" — the app does not proactively notify users their card is expiring; users discover expiry at point of purchase
- "Card freezing vs. ordering new card" — the same UI section handles both, creating confusion about which action does what
- "Loading state UX problems" — unclear whether an action (freeze, order) has been submitted or is in progress
- "Virtual card feature discovery" — feature exists but is not surfaced in the card management flow

**Benchmark insight:** Card management flows that distinguish clearly between reversible actions (freeze) and irreversible actions (cancel/replace) reduce support tickets significantly.

### Customer Satisfaction Rankings (Chapter 7)
> "Service quality rankings — surveyed customer likelihood to recommend their personal current account provider. Starling Bank and Monzo tied at #1 (81%), ranging down to Royal Bank of Scotland at #16 (46%)."

The 35-point NPS gap between #1 (Monzo/Starling) and #16 (RBS) is not random. It maps to specific design decisions: notification quality, balance transparency, payment flow length, error recovery design.

## BFM Evidence

### Chapter 9 — the notification test
All 6 banks received the same transaction data. The differences in notification quality are pure design decisions — not technical constraints. The banks with better notifications made a conscious choice to clean up merchant names, add category icons, and format amounts in a human-readable way.

### Chapter 8 — Barclays card UX
> "Virtual card feature discovery" — the feature exists but cannot be found without knowing to look for it.

The pattern: Barclays built a useful feature and put it somewhere users don't naturally navigate. Feature adoption is ~0% because discovery is ~0%.

## What Good Looks Like
**Notifications:** "Deliveroo · Food delivery · -£23.40 · 14:22" — merchant name, category, amount, time. No raw data strings.
**Balance:** Current balance + pending transactions + monthly spend vs. budget — visible on the home screen.
**International payments:** Live exchange rate shown before final confirmation. No more fields than the receiving bank requires.
**Card management:** Freeze (reversible) and replace (irreversible) clearly distinguished, with explicit confirmation for irreversible actions.

## Red Flags
- [ ] Transaction notifications show raw merchant identifiers (e.g., "AMZN MKTP") instead of clean names
- [ ] Balance requires a refresh or additional click to show pending transactions
- [ ] International payment form requires more information than the destination bank mandates
- [ ] Card freeze and card replacement are in the same UI without clear distinction
- [ ] New card features buried in settings rather than surfaced in the relevant flow
