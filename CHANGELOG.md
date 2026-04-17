# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [memory-system 1.10.5] — 2026-04-17

### Changed
- `prompt-reminder.sh` (UserPromptSubmit) now emits a short `systemMessage` — a dimmed one-line banner so the user can see the hook firing. `additionalContext` to Claude is unchanged.

[memory-system 1.10.5]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/memory-system-v1.10.5

## [memory-system 1.10.4 / second-brain 1.0.1] — 2026-04-17

### Changed
- **Date-bucketed `raw/` inbox** across both plugins.
  - `memory-system`: `coder-memory-store` now writes to `brain2/raw/<YYYY-MM-DD>/code-knowledge/<domain>/<bugs|patterns>/<slug>.md` instead of `brain2/raw/code-knowledge/...`. `coder-memory-recall` grep paths widened to `raw/*/code-knowledge/` so it finds files regardless of which day they were staged. Storage-layout diagrams, skill descriptions, hook context messages (`inject.sh`), and `memory_store_reminder.py` reason string all updated to reflect the new path.
  - `second-brain`: `ingest` workflow now stashes raw sources under `brain2/raw/<today>/...` using `date +%F`. Conversational ingest goes to `brain2/raw/<YYYY-MM-DD>/conversations/<topic>.md`. `raw/assets/`, `raw/notion/`, and `raw/clippings/` remain flat (user-managed). Layout diagrams in `references/conventions.md` and `assets/CLAUDE.md.template` updated.
- Rationale: daily ingests group together so Hung can scan a single "inbox of 2026-04-17" at promotion time instead of one giant flat folder.

### Migration
- Existing files under `brain2/raw/code-knowledge/` should be moved into a `raw/<date>/code-knowledge/` folder matching each file's `created:` frontmatter. New writes always use today's bucket.

[memory-system 1.10.4 / second-brain 1.0.1]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/memory-system-v1.10.4

## [1.5.0] — 2026-04-14

### Added
- **2-level memory hierarchy**: `~/.claude/memory/<domain>/<category>/<file>.md`
  - Level 1 (domain): self-discovered, dynamic (e.g., `frontend-patterns/`, `blockchain-patterns/`)
  - Level 2 (category): 5 defaults (`bugs/`, `patterns/`, `decisions/`, `procedures/`, `structure/`) + extensible when defaults don't fit
- **`/memory-system:reorganize`** — new skill that migrates legacy flat files into the 2-level structure. Threshold-aware (skips domains with ≤ 3 files).
- **Tie-breaker priority** when insight fits multiple categories: bugs > decisions > procedures > structure > patterns
- **Flat/sub threshold**: domains with ≤ 3 files stay flat; > 3 files use 2-level. Keeps small domains simple.

### Changed
- `coder-memory-store` workflow now picks domain AND category (2 decisions instead of 1)
- `coder-memory-recall` searches narrow to `<domain>/<category>/` first, widens progressively
- Both INDEX.md levels maintained — category lists entries, domain lists categories + highlights

[1.5.0]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/v1.5.0

## [1.4.0] — 2026-04-14

### Changed
- **Less spammy memory reminder**: Tuned Stop hook defaults from 3/3/disabled to 5/8/10:
  - `REMIND_EVERY_N_STOPS`: 3 → 5 (fires every 5th turn instead of every 3rd)
  - `MIN_TOOL_CALLS`: 3 → 8 (requires a truly substantial 5-turn window)
  - `COOLDOWN_MINUTES`: disabled → 10 (no back-to-back reminders within 10 min)
- Result: typical coding session sees ~1-2 reminders per hour instead of many.

[1.4.0]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/v1.4.0

## [1.3.0] — 2026-04-14

### Added
- **Pre-granted permissions** in plugin `settings.json` for `~/.claude/memory/**` (Write, Edit, Read, Bash mkdir/ls/grep). Subagents no longer hit permission prompts when writing memory files.
- `coder-memory-store` and `coder-memory-recall` now use `run_in_background: true` for their Task subagent calls — main conversation doesn't block on memory operations.

### Fixed
- Memory writes from subagents previously failed with permission errors because subagents are sandboxed to project scope. Now explicitly granted.

[1.3.0]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/v1.3.0

## [1.2.0] — 2026-04-14

### Changed
- **Relaxed anti-fragmentation rule**: `coder-memory-store` now prefers creating a new domain folder over dumping into `universal-patterns/` — even for the first insight in that domain. This prevents `universal-patterns/` from becoming a junk drawer.
- Clearer rule: `universal-patterns/` is reserved for genuinely cross-cutting concerns (exponential backoff, retry logic, etc.), not "unclear" insights.

[1.2.0]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/v1.2.0

## [1.1.0] — 2026-04-14

### Changed
- **Dynamic folder auto-discovery**: removed hardcoded keyword routing tables in `coder-memory-store` and `coder-memory-recall`. Claude now picks or creates folders by scanning existing ones and matching content semantically.
- **Anti-fragmentation rule**: single insight → `universal-patterns/` until 2-3 related ones justify a new domain folder.
- `knowledge-updater` delegates memory routing to `coder-memory-store` instead of duplicating the table.

### Added
- `inject.sh` auto-creates `~/.claude/memory/` on first run — zero setup for new users.
- `LICENSE` (MIT), `CHANGELOG.md`, README badges.

### Fixed
- Author URL and homepage URL in `plugin.json` (now points to the actual GitHub account).

### Removed
- Old memory files (episodic/, procedural/, semantic/) that shipped accidentally with the plugin.

[1.1.0]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/v1.1.0

## [1.0.0] — 2026-04-14

### Added
- **5 skills** for the 4-tier memory/knowledge system:
  - `generate-rules` — analyze codebase and generate `.claude/rules/` with path-scoped frontmatter
  - `init-memory` — set up `.claude/memory/` and configure auto memory per project
  - `coder-memory-store` — save universal patterns to `~/.claude/memory/<domain>/`
  - `coder-memory-recall` — retrieve patterns from universal memory
  - `knowledge-updater` — route recent changes to the right knowledge store
- **3 hooks** that integrate with Claude Code lifecycle:
  - `inject.sh` — SessionStart/PostCompact/PreToolUse:Read → inject Universal Memory index with colored output, auto-discovers topic folders
  - `pre-commit-gate.sh` — PreToolUse:Bash → block `git commit`/`push` until `/knowledge-updater` has run
  - `memory_store_reminder.py` — Stop → counter-based reminder (every 3rd turn, ≥3 tool calls)
- **Default settings** — `autoMemoryEnabled: true`
- **Marketplace** `maniax` — ready for future plugins

[1.0.0]: https://github.com/VinhHung1999/memory-system-plugin/releases/tag/v1.0.0
