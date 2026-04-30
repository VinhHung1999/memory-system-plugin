# Edge Cases Checklist

When clarifying with the user, you will never think of every edge case on
your own. Use this checklist as a prompt bank. Skim the section matching the
request's domain, pick 3-5 questions most likely to reveal undefined behavior,
and ask them.

These questions are phrased as what to **ask the user**, not what to assume.

---

## Data & state

- What happens with an **empty** result set? (zero items, no search hits, no history)
- What happens when data is **loading**? (spinner, skeleton, optimistic UI?)
- What happens when loading **fails**? (timeout, 500 error, network gone)
- What happens with a **partial** load? (got first page, fetching more fails)
- What's the **maximum** the user can create / upload / list before we paginate or reject?
- What about **very long strings / large files / huge numbers**? Specific limit?
- What happens with **special characters / emojis / RTL text** in input fields?
- What about **duplicate** entries? Prevent, warn, or allow silently?
- Is the data **case-sensitive**? (email, username, search query)
- What happens if the data is **stale** (cached, user offline for a week)?

---

## Authentication, authorization, permissions

- Who is **allowed** to perform this action? Owner, admin, member, guest, system?
- What happens if a **logged-out** user tries? (redirect to login? preserve intent?)
- What happens if a user is **logged in but not authorized**? (403? hidden UI? empty state?)
- What if the user's **session expires** mid-action?
- What about **impersonation** / admin-acting-as-user?
- Can the **permission be revoked mid-use**? What happens to the current session?
- Are there **IP / device / geo restrictions**?
- Does this touch **PII / payment / health** data? Compliance review needed?
- Is there a **rate limit** per user? Per IP? Per API key?
- What about **abuse** (fake invites, spam, scraping)?

---

## Network & offline

- What happens if the request **times out**? (Retry? How many times? With backoff?)
- What about **slow networks** (3G, spotty WiFi)? Should UI show partial state?
- What if the user is **fully offline**? (Queue action? Error? Local-only mode?)
- What about **request retries** — is the action idempotent?
- Can this action be **cancelled** mid-flight?
- What happens when the **server is down** for maintenance? (Graceful degradation?)

---

## Concurrency

- What if **two users act on the same resource simultaneously**? (Last-write-wins, optimistic lock, merge?)
- What if the **same user acts on two devices**? (e.g. adding to cart on phone + laptop)
- What if an action is **triggered twice** (double-click, double-tap)?
- What about **race conditions** in multi-step flows? (User clicks back during a save)
- If the operation is **async** (e.g. job queued), what does the user see? (Progress? Fire-and-forget? Undo window?)

---

## Time & scheduling

- What **timezone** are timestamps in? User's local, server UTC, other?
- What about **daylight saving time** transitions?
- What's the **granularity** — seconds, minutes, days?
- If scheduling future events, what's the **max future date** allowed?
- What happens around **midnight / end-of-month** for recurring events?
- Do **past dates** make sense? (e.g. back-dating a journal entry, yes; back-dating a calendar reminder, no)

---

## Internationalization

- Which **languages / locales** must this support at launch?
- What about **RTL languages** (Arabic, Hebrew)?
- How do **currencies** format? (₫ vs $ vs €, comma vs dot, code vs symbol)
- Are there **region-specific features or blocks**? (e.g. feature X only for VN)

---

## Accessibility

- Is this usable with **keyboard only** (no mouse)?
- Is it **screen-reader friendly** (labels, ARIA, focus order)?
- Does it meet **WCAG contrast** requirements? (AA at minimum)
- What about **users with motor disabilities** — is the tap target big enough? Timing generous?

---

## Mobile-specific

- **Portrait vs landscape** — does it work both?
- What happens on **small screens** (iPhone SE) vs large (iPad)?
- **Interrupted by a call / notification** mid-action?
- **Background / foreground** transitions — state preserved?
- **Deep links** — what if someone opens a deep link without an account? Without the required permission?
- **Platform differences** — does iOS behavior need to match Android exactly, or are minor differences OK?

---

## Money & transactions

- What's the **currency**? How many decimal places?
- What if a **refund** is needed — partial, full, what triggers it?
- What about **tax, fees, discounts** — how are they computed, displayed, logged?
- **Rounding rules** — half-up, banker's, truncate?
- What happens if the **payment fails mid-transaction**?
- Is there an **idempotency key** for retries?
- What **audit trail** is required? (compliance, dispute resolution)

---

## Content & user-generated data

- Can users **delete / edit** after posting? Is it soft-delete or hard?
- Is there a **moderation** step? Pre- or post-publish?
- What about **reporting / flagging** by other users?
- **Profanity / blocked-word filter**?
- What about **links / images / videos** in user content — are they allowed?
  scanned? transcoded?
- What's the **retention policy**? Deleted after 30 days? Kept forever?

---

## Business logic gotchas

- What happens when a **user's account is suspended / deleted** mid-flow?
- What about **sub-accounts / workspaces / organizations**? Does action scope correctly?
- Are there **feature flags** in play? What if flag flips mid-session?
- **Trial vs paid** — does this action behave differently for free-tier users?
- **Deprecation** — is there an older version of this action we need to support?

---

## Observability & debugging

- What **events / logs / metrics** should this action emit?
- What should go in an **audit trail**? (who, what, when, from where)
- What **error codes / messages** should be user-facing vs engineer-facing?
- Should failures **alert** someone (on-call)? Which severity?

---

## How to use this list

1. Read the user's request. Identify 2-3 most likely domains from above
   (auth + data + network is the most common combo).
2. Pick 3-5 questions per domain — the ones most likely to reveal undefined
   behavior given the specific request.
3. Batch them into max 3 questions per turn when asking the user.
4. After user answers, scan again — did their answer surface a *new* edge
   case? Ask it next round.
5. Stop when: every scenario has a defined outcome, or the user says "we'll
   handle edge case X in a follow-up story" (which you then write in "Out of
   scope").
