# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
