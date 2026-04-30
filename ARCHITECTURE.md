# Architecture — Maniax Plugin Collection

End-to-end diagram of how tmux team agents work, how memory is stored
and recalled, and how the plugins fit together.

> Last updated: 2026-04-29
> Status: Phase 1 (plugin reorg) + Phase 2 (memory hooks reorg) complete.

---

## 1. Plugin Landscape

```
┌─────────────────────────────────────────────────────────────────────┐
│                      MANIAX PLUGIN COLLECTION                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ROLE PLUGINS (4 agents)        TEAM SCAFFOLDING                     │
│  ┌────────────────────┐         ┌────────────────────────┐          │
│  │  po    → Product   │         │ tmux-team              │          │
│  │  dev   → Developer │         │ └─ create-team skill   │          │
│  │  qc    → QC tester │         │    (scaffolds project) │          │
│  │  cmo   → Marketing │         └────────────────────────┘          │
│  └────────────────────┘                                              │
│                                                                      │
│  KNOWLEDGE PLUGINS (cross-cutting)                                   │
│  ┌─────────────────────────────────┐ ┌────────────────────────┐     │
│  │ second-brain                    │ │ memory-system          │     │
│  │ (ALL brain2 vault interactions) │ │ (project-local tooling)│     │
│  │ • memory-recall (read-only)     │ │ • generate-rules       │     │
│  │ • project-memory-recall         │ │ • init-memory          │     │
│  │ • project-memory-store          │ │ • knowledge-updater    │     │
│  │ • second-brain (mega skill)     │ │ • reorganize           │     │
│  │ • 3 hooks (inject/prompt/store) │ │ • pre-commit-gate hook │     │
│  └─────────────────────────────────┘ └────────────────────────┘     │
│                                                                      │
│  DOMAIN PLUGINS                                                      │
│  ┌────────────────────────────┐ ┌────────────────────────────┐     │
│  │ marketing-toolkit          │ │ learn-coursera             │     │
│  │ (8 marketing skills)       │ │ (Coursera → skill meta)    │     │
│  └────────────────────────────┘ └────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

**Quick reference — which plugin owns what:**

| Concern | Plugin | Skill / Hook |
|---|---|---|
| PO behavior | `po` | po agent + 4 PO skills + 7 UX-BFM skills |
| DEV behavior | `dev` | dev agent + karpathy-guidelines + vercel-react |
| QC behavior | `qc` | qc agent + qc-mobile-testing + qc-web-testing |
| CMO behavior | `cmo` | cmo agent (1150-line strategic persona) |
| Project scaffold | `tmux-team` | create-team skill + templates |
| Universal recall | `second-brain` | memory-recall (read-only) |
| Project memory | `second-brain` | project-memory-recall + project-memory-store |
| Vault hooks | `second-brain` | inject.sh + prompt-reminder.sh + memory_store_reminder.py |
| Project rules | `memory-system` | generate-rules + .claude/rules/ |
| Project auto memory | `memory-system` | init-memory (configures `docs/memory/`) |
| Knowledge sync | `memory-system` | knowledge-updater + pre-commit-gate hook |

---

## 2. Setup Flow — Creating a new tmux team

```
USER terminal
   │
   │ /tmux-team:create-team
   ▼
┌──────────────────────────────────┐
│ create-team skill (in tmux-team) │
│  Asks: project root, team name,  │
│         session name, roles      │
└──────────────┬───────────────────┘
               │
               │ Walks references/templates/, substitutes
               │ {TEAM_NAME}, {SESSION_NAME}, {ROLES}, etc.
               ▼
┌──────────────────────────────────────────┐
│ Project structure scaffolded:            │
│                                          │
│ {project}/                               │
│ ├── .claude/                             │
│ │   ├── hooks/                           │
│ │   │   └── session_start_team_docs.py   │
│ │   └── settings.json                    │
│ └── docs/                                │
│     ├── board/                           │
│     │   ├── backlog.md                   │
│     │   └── sprints/active|archive/      │
│     └── tmux/<team-name>/                │
│         ├── workflow.md                  │
│         └── setup-team.sh (chmod +x)     │
└──────────────────────────────────────────┘
               │
               │ User runs:
               │ bash docs/tmux/<team>/setup-team.sh
               ▼
┌──────────────────────────────────────────────┐
│ tmux session created with N panes:           │
│                                              │
│ [PO]  [DEV]  [QC]  [CMO]                     │
│   │     │     │     │                        │
│   │ Each pane runs:                          │
│   │ claude --model opus --agent <role>       │
│   │ + sets pane @role_name option            │
│   ▼                                          │
│ Per-pane: SessionStart hook fires            │
└──────────────────────────────────────────────┘
```

---

## 3. Runtime Flow — Agent boots up (PO pane example)

```
┌───────────────────────────────────────────────────────┐
│  claude --agent po --model opus                       │
│  ─────────────────────────────────                    │
│  STEP 1: Load PO agent system prompt from po plugin   │
│          (po.md = Pure PO behavior + skills routing   │
│          + project memory section + quality gate)     │
└───────────────────────┬───────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────┐
│  SessionStart hooks fire (parallel):                  │
│                                                       │
│  Project hook (session_start_team_docs.py):           │
│  ├─ Detects role from @role_name = "PO"               │
│  ├─ Detects team from @team_name                      │
│  └─ Injects via additionalContext:                    │
│     • workflow.md (team-specific operations)          │
│     • Active sprint (docs/board/sprints/active/...)   │
│     • Backlog (docs/board/backlog.md, PO/SM only)     │
│                                                       │
│  Plugin hook (inject.sh from second-brain):           │
│  └─ Injects via additionalContext:                    │
│     • Brain2 wiki sections summary                    │
│     • Skills list (memory-recall, project-memory-*,   │
│       second-brain mega)                              │
│     • When-to-use guide                               │
└───────────────────────┬───────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────┐
│  PO agent ready — sees:                               │
│  ✓ Own behavior (pure PO from po plugin)              │
│  ✓ Team workflow (this team's tm-send rules)          │
│  ✓ Current sprint state                               │
│  ✓ Product backlog                                    │
│  ✓ Brain2 wiki landscape + skill pointers             │
└───────────────────────────────────────────────────────┘
```

---

## 4. Memory Tiers

```
┌──────────────────────────────────────────────────────────────────────┐
│                            MEMORY TIERS                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  TIER 1: WORK ARTIFACTS (project)                                    │
│  ────────────────────────────────────                                │
│   docs/board/backlog.md           ← PO writes/updates                │
│   docs/board/sprints/active/*.md  ← PO+DEV+QC update                 │
│                                                                      │
│  TIER 2: PROJECT MEMORY (brain2/wiki/projects/<X>/memory/)           │
│  ─────────────────────────────────────────────────────               │
│   po.md     ← PO appends                                             │
│   dev.md    ← DEV appends                                            │
│   qc.md     ← QC appends                                             │
│   cmo.md    ← CMO appends                                            │
│   shared.md ← Any role appends (cross-cutting)                       │
│                                                                      │
│  TIER 3: UNIVERSAL CODE-KNOWLEDGE (brain2/wiki/code-knowledge/)      │
│  ──────────────────────────────────────────────────────              │
│   <domain>/{bugs,patterns}/  ← READ-ONLY (160 entries curated)       │
│   (universal store retired — no new writes; recall still works)      │
│                                                                      │
│  TIER 4: CONVERSATION (Claude Code built-in)                         │
│  ───────────────────────────────────────────                         │
│   Auto memory ~/.claude/memory/ + transcript (in-session)            │
└──────────────────────────────────────────────────────────────────────┘
```

**Rule of thumb — which tier for which info:**

| Info | Tier | How |
|---|---|---|
| Backlog item, sprint task | 1 | Edit `docs/board/*` directly |
| Stakeholder pattern, decision rationale | 2 | `/second-brain:project-memory-store role=<role> project=<name>` |
| Architecture decision per project | 2 | Same as above (role=dev) |
| Flaky test pattern per project | 2 | Same as above (role=qc) |
| Universal coding lesson (rare now) | 3 | Read-only — recall via `/second-brain:memory-recall` |
| Today's task state | 4 | Auto memory (no action) |

---

## 5. Memory Recall Flow

```
USER prompt: "đó giờ mình có làm cái nào như vậy chưa?"
                              │
                              ▼
        ┌─────────────────────────────────┐
        │  Agent reads UserPromptSubmit   │
        │  hook context:                  │
        │  "Recall when project mentioned │
        │   / unfamiliar / explicit ask"  │
        └────────────┬────────────────────┘
                     │
                     │ Matches signal: explicit ask
                     ▼
        ┌─────────────────────────────────┐
        │  Agent invokes:                 │
        │  /second-brain:                 │
        │  project-memory-recall          │
        │  role=<own> project=<name>      │
        │  + query                        │
        └────────────┬────────────────────┘
                     │
                     │ Skill SKILL.md instructs:
                     │ MANDATORY use Task tool background
                     ▼
        ┌─────────────────────────────────┐
        │  Background sub-agent:          │
        │  • Classify query shape         │
        │  • Smart route:                 │
        │    - Direct project? Read       │
        │    - Concept? qmd vsearch       │
        │    - Keyword? grep              │
        │  • Filter to memory/<role>.md   │
        │    + memory/shared.md           │
        │  • Return top 3-5 hits          │
        └────────────┬────────────────────┘
                     │
                     ▼
        Agent uses results, replies to user
```

**Recall triggers (priority order):**
1. ⭐ User explicitly asks ("có làm cái này chưa?", "have we done X?", "--recall")
2. Project name mentioned + suspect prior context exists
3. Genuinely unfamiliar domain (use judgment, lower reliability)

**Default: skip recall.** Most prompts don't need it.

---

## 6. Memory Capture Flow — Observation-Driven Pipeline

Active store has been **retired**. Agents no longer pre-judge what's worth
storing in the moment. Instead, every turn is captured cheaply by a Stop
hook, and a nightly dream skill digests the day's observations.

```
DURING DAY (cheap, dumb, programmatic)
─────────────────────────────────────
Agent finishes turn → Claude Code fires Stop hook
                            │
                            ▼
              ┌─────────────────────────────┐
              │ observation_logger.py        │
              │ (Python script — no LLM)     │
              ├─────────────────────────────┤
              │ 1. Find observation.md       │
              │    walking up from cwd to    │
              │    project root              │
              │ 2. Auto-create with header   │
              │    if missing                │
              │ 3. Read transcript JSONL     │
              │ 4. Extract last user msg     │
              │    + assistant response      │
              │    + tool call summaries     │
              │ 5. Format markdown:          │
              │    ## YYYY-MM-DD HH:MM       │
              │    [role: po] (from tmux)    │
              │    **User:** ...             │
              │    **Assistant:** ...        │
              │    <details>tool calls...    │
              │ 6. Append to observation.md  │
              └─────────────┬───────────────┘
                            │
                            ▼
            workspace/observation.md grows by 1 entry

AT 2 AM (smart, slow, LLM-driven — PLANNED)
────────────────────────────────────────────
        ┌────────────────────────────────────┐
        │ dream skill reads:                 │
        │  • Today's observation.md          │
        │  • Existing wiki/projects/<X>/     │
        │    memory/<role>.md (per role)     │
        ├────────────────────────────────────┤
        │ Per cluster of related entries:    │
        │  1. EXTRACT — quality gate check;  │
        │     if pass, append insight to     │
        │     memory/<role>.md               │
        │  2. CONSOLIDATE — detect dupes vs  │
        │     existing memory; merge/skip    │
        │  3. ANNOTATE — mark stale entries  │
        │  4. FLAG — suggest contradictions  │
        │     for manual review              │
        ├────────────────────────────────────┤
        │ Output:                            │
        │  • Updated wiki/projects/<X>/      │
        │    memory/<role>.md                │
        │  • Daily report wiki/.dream/       │
        │    <YYYY-MM-DD>.md                 │
        │  • Archive observation.md →        │
        │    .observations/<YYYY-MM-DD>.md   │
        │  • Fresh observation.md tomorrow   │
        └────────────────────────────────────┘
```

**Per-role insight types** (what dream extracts):

| Role | Examples |
|---|---|
| PO | Stakeholder pattern · Past decision + rationale · Recurring scope shifts · Acceptance bar · Dropped features + why |
| DEV | Architecture decision + rationale · Hard-won bug fix · Codebase invariants · Library version pins + why · Perf gotchas |
| QC | Flaky test area + cause · Edge case caught real bug · Regression patterns · Test data quirks · Browser/device gotchas |
| CMO | Channel ROI · Pricing-signal pattern · Positioning iterations + what failed · Competitive reactions · Campaign learnings |

**Why this design:**
- Capture is cheap: append-only file write, no LLM, no agent decision
- Judgment is sparse: dream runs once per day, has full context to decide
- Failure-safe: if dream misses an insight, it's still in observation.md (replayable)
- Opt-out: delete observation.md + add to .gitignore

---

## 7. Cleanup Flow (Future — AutoDream pattern)

```
       Wiki grows over time
                │
                ▼
        ┌─────────────────────────────────┐
        │  Hung invokes (future):         │
        │  /second-brain:                 │
        │  project-memory-dream           │
        │  project=<name> [role=<role>]   │
        └────────────┬────────────────────┘
                     │
                     │ AutoDream pattern:
                     ▼
        ┌─────────────────────────────────┐
        │  Per role file:                 │
        │  • PRUNE outdated entries       │
        │  • MERGE duplicates             │
        │  • REFRESH stale specifics      │
        │  Output: dream report + diff    │
        └────────────┬────────────────────┘
                     │
                     │ Default --dry-run
                     ▼
        Hung reviews → --apply → wiki updated
```

Status: **deferred** (design note saved at
`brain2/raw/2026-04-29/code-knowledge/claude-code/patterns/auto-dream-for-project-memory.md`).

---

## 8. End-to-End Big Picture

```
        USER
         │
         ▼
    [tmux session]
         │
    ┌────┴────┬────┬────┐
    ▼         ▼    ▼    ▼
   [PO]    [DEV] [QC] [CMO]
    │        │    │    │
    │ tm-send between panes (when needed)
    │
    ├─→ Reads: docs/board/* (sprint+backlog) — Tier 1
    ├─→ Reads: docs/tmux/<team>/workflow.md (team rules)
    ├─→ Reads: brain2/wiki/projects/<X>/memory/<role>.md (own past)
    ├─→ Recalls via /second-brain:project-memory-recall (smart query)
    ├─→ Stores via /second-brain:project-memory-store (append wiki direct)
    └─→ Future: cleanup via /second-brain:project-memory-dream
```

---

## Key Design Decisions Made

| Decision | Why |
|---|---|
| Subagent format (`claude --agent po`) instead of plain prompts in tmux panes | Each role's behavior is universal (lives in plugin), team-specific layer comes from project workflow.md — clean separation |
| Project memory writes DIRECTLY to wiki (no raw inbox) | Scope already bounded (project + role), no human curation needed; reduces friction |
| Universal coder-memory STORE retired (recall kept read-only) | Most lessons are project-specific; universal store added noise without proportional value |
| All vault hooks/skills consolidated to second-brain plugin | Plugin organization should mirror data domain — 1 plugin per concern |
| Hook reminders are signal-based, default-skip | "Non-trivial" is vague; explicit user ask is the most reliable trigger |
| Quality gate (3 questions) lives in agent prompt, not hook | Strict gate at decision point > nag at end of turn |
| `tmux-team` plugin scaffolds, doesn't own role behavior | Team setup is project-specific; role behavior is universal — different lifecycles |

---

## Plugin Versions (current)

| Plugin | Version | Notes |
|---|---|---|
| marketplace.json (root) | 3.0.0 | After observation-driven pipeline shift |
| second-brain | 3.0.0 | Active store retired; observation_logger Stop hook |
| memory-system | 1.11.0 | After moving vault skills out |
| po | 0.4.0 | Capture section now points to observation log |
| dev | 0.1.0 | Same |
| qc | 0.1.0 | Same |
| cmo | 0.1.0 | Same |
| tmux-team | 0.1.0 | 4-role default |
| marketing-toolkit | 1.0.0 | Untouched |
| learn-coursera | 1.0.0 | Untouched |
