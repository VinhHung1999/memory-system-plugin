# Privacy Guardrails for Marketing AI Prompts

## Why this matters

Public LLMs (ChatGPT free, Gemini, Copilot) may use your prompts for training. Even enterprise tiers may retain data for 30 days. Pasting customer data = potential data breach + GDPR/CCPA violation.

## What NEVER to paste

### Personally Identifiable Information (PII)
- Full names
- Email addresses
- Phone numbers
- Postal addresses
- IP addresses (of individuals)
- National ID / passport / SSN / tax ID

### Financial data
- Credit card numbers (never, ever)
- Bank account info
- Full transaction records with linkable IDs
- Individual revenue figures tied to specific customers

### Health / medical data
- Anything PHI-related (HIPAA risk)
- Symptoms + identifiable info
- Medical conditions tied to individuals

### Proprietary business data
- Customer lists
- Unreleased product specs (competitor risk)
- Pricing strategies
- Legal strategy / M&A info

## What's OK to paste (usually)

### Anonymized feedback
- "User #123 said: 'I love the product but shipping was slow'"
- Survey responses with names/IDs stripped
- Aggregated themes without individual identifiers

### Publicly available content
- Your own blog posts
- Published product descriptions
- Public social media posts (yours or anyone's)

### Generic business context
- "We're a 5-person SaaS startup targeting B2B marketers"
- "Our typical customer spends $2k/year" (aggregate, not individual)
- Industry benchmarks

### Brand voice examples
- Past marketing copy you've published
- Tone samples you've approved for public

## The anonymization checklist

Before pasting survey/review data:

1. **Names** → replace with "User A" "User B" etc.
2. **Email addresses** → strip entirely or replace with "user@example.com"
3. **Phone numbers** → strip
4. **Order IDs** → replace with "ORDER-001" generic IDs
5. **Specific dates** → generalize to "last month" unless dates matter
6. **Company names** (for B2B) → if small market, anonymize; if large market like Google/Meta, public info OK
7. **Specific dollar amounts** tied to individuals → generalize to ranges

## Tiered approach by LLM

| LLM | Recommended for |
|---|---|
| ChatGPT Free | Generic drafting only. Assume your data may be used for training. |
| ChatGPT Plus / Team | Better privacy but still be careful. OK for anonymized data. |
| ChatGPT Enterprise | Contractual data protection. OK for most business data. |
| Claude.ai (Anthropic) | Good privacy posture, no training on user data. |
| Claude Enterprise / API | Best for business data with BAA available. |
| Gemini | Check current terms — varies by tier. |
| Copilot Enterprise | Generally OK for Microsoft-tenant data. |
| Local LLMs (Ollama, etc.) | Best for highly sensitive — data never leaves your machine. |

## When in doubt

1. **Strip + anonymize more than you think necessary**
2. **Don't paste raw CRM exports** — process locally first
3. **For regulated industries** (healthcare, finance, legal): use only enterprise LLMs with signed BAA/DPA or local models
4. **Log what you've pasted** — so if a breach happens, you know what was exposed

## Common pitfalls

- **"It's just for testing"** — your test data still contains PII
- **"I'll delete the chat"** — data may already be logged server-side
- **"The LLM promised it wouldn't train on this"** — check actual TOS, promises vary
- **"It's a competitor, so it's fair game"** — legally it may not be; reputationally always risky

## The 10-second check before pasting

Ask: *"If this paste leaked onto a public Discord tomorrow, would anyone be harmed or embarrassed?"*

If yes → anonymize more or use a safer tier. If no → proceed.
