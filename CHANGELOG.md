# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
