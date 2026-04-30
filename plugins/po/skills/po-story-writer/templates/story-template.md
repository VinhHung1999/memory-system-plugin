---
story_id: <kebab-case-slug>
epic: <parent epic or "standalone">
priority: P0 | P1 | P2
estimate_hint: S | M | L
---

## User Story

**As a** <specific persona>
**I want** <one primary action, one verb>
**So that** <measurable business value>

## Context

<2–4 lines: why this story exists, link to epic/ticket/incident, current state
of the world. Must be enough that a TL reading this cold understands the
"why" without conversation context.>

## Acceptance Criteria (Gherkin)

**Scenario 1: <golden-path name>**
- Given <initial condition>
- When <action>
- Then <observable, testable outcome>

**Scenario 2: <edge case name>**
- Given <condition>
- When <action>
- Then <outcome>

**Scenario 3: <error case name>**
- Given <condition>
- When <action>
- Then <outcome>

## Out of scope
- <feature deliberately excluded>
- <decision deferred to TL or follow-up story>

## Open questions for TL
- <technical question blocking estimation>
- <or "- None" if truly none>

## INVEST self-check
- [ ] Independent — can ship on its own
- [ ] Negotiable — AC can be refined with TL
- [ ] Valuable — "So that" shows real business value
- [ ] Estimable — enough info for TL to size
- [ ] Small — fits in one sprint (≤5 dev-days)
- [ ] Testable — every AC is measurable/observable
