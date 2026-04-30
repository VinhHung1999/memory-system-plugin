# Email Compliance One-pager

## CAN-SPAM (US)

Required in every marketing email:
1. **Accurate sender info** — "From" name matches your business
2. **Honest subject line** — don't misrepresent email contents
3. **Physical address** — a real mailing address in the footer
4. **Unsubscribe link** — clear, prominent, honored within 10 days
5. **Identify as ad** — if the email is promotional, make that clear

## GDPR (EU)

Required before you can email any EU resident:
1. **Explicit opt-in** — checkbox must be unchecked by default; no "by continuing you agree…" dark patterns
2. **Purpose specification** — state WHY you're collecting email + what you'll send
3. **Data processing lawfulness** — legitimate interest OR consent (consent is safer for marketing)
4. **Right to access** — users can request what you have on them
5. **Right to erasure** — users can request deletion; honor within 30 days
6. **Data Protection Officer** — required for large organizations or high-risk processing
7. **Breach notification** — report data breaches within 72 hours

## CASL (Canada)

Required before you can email Canadian residents:
1. **Express consent** — opt-in (not opt-out)
2. **Implied consent** exists for 2 years after business relationship (existing customer), 6 months after purchase
3. **Sender identification** — name, mailing address, phone OR email
4. **Unsubscribe mechanism** — must work for 60 days after email sent

## Vietnam (Decree 91/2020)

1. **Opt-in required** — explicit consent before first send
2. **Unsubscribe required** — must be honored within 24 hours
3. **Timing restrictions** — no marketing emails 22:00-06:00
4. **Registration** — commercial emailers must register with MIC (Ministry of Information and Communications)

## Universal best practices

1. **Double opt-in** — send a confirmation email after signup; only email confirmed addresses. Higher quality list, lower spam rates, defensible consent record.
2. **Preference center** — let users pick frequency/topics instead of only offering "unsubscribe". Reduces churn.
3. **List hygiene** — remove hard bounces immediately; sunset inactive subscribers after 6-12 months.
4. **Authentication** — set up SPF, DKIM, DMARC on your sending domain. Without these, you'll land in spam for Gmail/Outlook.
5. **Mobile-friendly** — 60%+ of email opens are mobile. Test every send on phone.

## Red-flag patterns

- Buying email lists (GDPR/CAN-SPAM violation)
- Scraping websites for emails (same)
- "You are receiving this because…" without actual consent record
- Unsubscribe links that don't work, require login, or delay > 10 days
- Physical address = PO box in another country
- No sender authentication (SPF/DKIM/DMARC)
- Re-importing unsubscribes ("maybe they'll engage this time")

The cost of violations: CAN-SPAM fines can be $50,120 per email. GDPR fines can be €20M or 4% of global revenue. Compliance is not optional.
