---
name: generate-rules
description: "Analyze a project's codebase and generate .claude/rules/ files with path-scoped frontmatter. Use this skill whenever the user asks to create rules, generate rules, set up .claude/rules, organize project instructions, or says things like 'tạo rules', 'viết rules', 'generate rules for this project'. Also trigger when the user mentions their CLAUDE.md is getting too long or wants to split instructions into scoped files."
---

# Generate Rules

Analyze the current project and generate `.claude/rules/` files — modular, path-scoped instruction files that Claude loads only when working with matching files. This saves context window and keeps instructions focused.

## Why path-scoped rules matter

Claude Code loads rules based on file paths being worked on. A rule scoped to `src/services/**/*` only enters context when Claude reads or edits a service file. This means:

- Less noise — Claude sees only what's relevant
- More room — context window isn't wasted on unrelated instructions
- Better compliance — focused rules are easier to follow

Rules **without** a `paths` frontmatter load every session (like CLAUDE.md), so reserve that for truly universal rules.

## The workflow

### Phase 1: Discover the project

Scan the project thoroughly — superficial scanning leads to wrong or shallow rules. Run these in parallel:

1. **Project identity** — Read the project manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `build.gradle`, `Gemfile`, etc.). Note the tech stack, key dependencies, and scripts/commands.
2. **Directory structure** — `ls` the top-level, then recursively explore every major subdirectory. Don't stop at the first level — go 2-3 levels deep to understand the real structure. For example, `src/` might have `components/`, `services/`, `database/` — and each of those has its own internal structure that matters.
3. **Existing instructions** — Read `CLAUDE.md` (project-level and global `~/.claude/CLAUDE.md`) if they exist. These contain rules that may need to be preserved or reorganized.
4. **Existing rules** — Check if `.claude/rules/` already exists. If it does, read all existing rule files to understand what's already covered.
5. **Config files** — Read linter configs (`.eslintrc`, `ruff.toml`, `golangci.yml`), test configs (`jest.config`, `pytest.ini`), CI/CD files (`.github/workflows/`, `Dockerfile`), and build configs (`tsconfig.json`, `vite.config`, `webpack.config`). These reveal conventions and constraints that should become rules.

### Phase 2: Identify domains

Look at the directories, files, and dependencies you discovered and group them into natural domains. A "domain" is a cohesive area of the codebase that has its own conventions, patterns, or gotchas worth documenting.

**How to discover domains — work from the codebase, not from a template:**

1. **Look at top-level directories.** Each distinct directory often maps to a domain. A Go project with `cmd/`, `internal/`, `pkg/` has different domains than a Rails app with `app/models/`, `app/controllers/`, `db/`. Let the project tell you what its domains are.

2. **Look at dependencies and config files.** An ORM dependency suggests a database domain. A test framework suggests testing conventions. A CSS framework or design tokens file suggests a styling domain. CI/CD configs suggest deployment rules.

3. **Look at CLAUDE.md.** If it exists, it often already groups instructions by topic — those topics are your domains.

4. **Merge small domains.** If a domain would produce a rule file with only 1-2 lines, fold it into a related domain or into `general.md`. Only create separate files for domains with enough substance.

**Deciding path scope for each domain:**

- **Always-loaded rules** (no `paths` frontmatter): For universal principles that apply regardless of which file Claude is editing — tech stack, core principles, deploy procedures, git workflow.
- **Path-scoped rules**: For domain-specific conventions. Set paths to match the directories where the domain lives. Use glob patterns that match the actual project structure — don't assume any particular framework layout.

**Example** — the same project concept looks very different across stacks:

A Python FastAPI project might produce: `general.md`, `api.md` (scoped to `app/routers/`), `database.md` (scoped to `app/models/`, `alembic/`), `testing.md` (scoped to `tests/`).

A Go microservice might produce: `general.md`, `handlers.md` (scoped to `internal/handlers/`), `database.md` (scoped to `internal/store/`), `proto.md` (scoped to `proto/`).

A React Native app might produce: `general.md`, `theme.md` (scoped to UI dirs), `navigation.md` (scoped to route dirs), `services.md` (scoped to service dirs).

The point: let the codebase structure drive the domains, not a predefined checklist.

### Phase 3: Verify and write rules

This is the critical step. For each domain you're writing a rule about:

**Deep-read the actual source files before writing anything.** For every fact you put in a rule — a config value, a table name, a function signature, a directory listing — you must have read the source that proves it. Don't infer, don't assume defaults, don't copy from memory. Open the file and check.

How deep to go per domain:
- **Schema/data layer**: Read the actual schema definition file, migration files, and model files. Get real table names, column names, types, version numbers.
- **Styling/theme**: Read every file in the theme/design-token directory. Get real color values, spacing values, typography scales, export names.
- **Routing/navigation**: `ls` every level of the route directory. Read layout files to understand nesting, middleware, guards.
- **Services/business logic**: `ls` the directory, then read the index/barrel file (if any) and skim each service file to understand its API — exported functions, key patterns.
- **Config/build**: Read the actual config files (`tsconfig.json`, `eslintrc`, `Dockerfile`, etc.) to extract real settings and constraints.
- **Tests**: Read the test config and a few representative test files to understand the testing patterns used (framework, assertion style, mocking approach).

**Write each rule file** with this format:

```markdown
---
paths:
  - "relevant/directory/**/*"
---

# Domain Name

[Concise, verified content]
```

Guidelines for rule content:

- **Be concise** — rules should be scannable, not essays. Use tables, bullet points, code blocks.
- **Be accurate** — every value, path, and name must come from reading the actual codebase.
- **Be actionable** — tell Claude what to do, not just what exists. "Use `get_db()` from `app/deps.py`" is better than "There is a database dependency injection module".
- **Include import/usage patterns** — show how to use things correctly, since wrong usage is a common source of errors.
- **Skip the obvious** — don't document things Claude can figure out from reading the code. Focus on conventions, gotchas, and decisions that aren't self-evident.
- **Match the project's language** — if the project is in Go, show Go code blocks. If Python, show Python. Don't mix.

### Phase 4: Update CLAUDE.md

Add a rules reference table to CLAUDE.md (or create one if it doesn't exist). The table should be a quick index showing which rule files exist and what they cover:

```markdown
## Rules

Detailed rules are in `.claude/rules/`:

| Rule file    | Scope                         | What                              |
| ------------ | ----------------------------- | --------------------------------- |
| `general.md` | Always                        | Tech stack, principles            |
| `theme.md`   | `src/components/`, `src/app/` | Design system, colors, typography |
| ...          | ...                           | ...                               |
```

If CLAUDE.md already has rule references, update the table rather than duplicating it. If CLAUDE.md has inline rules that are now covered by rule files, remove the inline versions to avoid duplication.

### Phase 5: Generate codebase overview

Create a `CODEBASE.md` file in the project root — a human-readable map of the entire source code. This file helps new developers (or the project owner returning after a break) quickly understand what's where and how things connect.

The overview should include:
- **Tech stack summary** — languages, frameworks, key dependencies, with versions
- **Directory map** — annotated tree showing what each directory contains and its purpose. Go 2-3 levels deep for important directories, 1 level for obvious ones.
- **Architecture overview** — how the major pieces connect (e.g., "Frontend calls Backend API via /api proxy, Auth service issues JWT tokens consumed by Backend")
- **Key files** — a short table of the most important files a developer should read first to understand the project (entry points, config, schema definitions, main business logic)
- **Data flow** — how data moves through the system (e.g., "User input → API route → Graph pipeline → Engine calculation → LLM interpretation → SSE stream back to client")
- **Development commands** — how to run, test, lint, build, deploy

Keep it factual and concise — this is a reference map, not documentation. Every claim must come from files you actually read during the earlier phases. Use the project's own terminology.

### Phase 6: Present the summary

After generating all rules and the codebase overview, present a summary to the user:

- List of rule files created (with path scoping info)
- Any decisions you made (e.g., "Merged state management into general.md since there's only Zustand with one store")
- Anything you weren't sure about and left out
- Mention that `CODEBASE.md` was created for onboarding reference

## Important principles

- **Don't over-generate.** A small project might only need 2-3 rule files. Don't create 10 nearly-empty files just because you can.
- **Don't duplicate CLAUDE.md.** Rules should complement CLAUDE.md, not repeat it. CLAUDE.md stays as the high-level overview; rules handle domain-specific detail.
- **Preserve existing rules.** If `.claude/rules/` already has files, update them rather than replacing. Read them first to understand what's there.
- **Path globs should be precise.** `src/services/**/*` is better than `src/**/*` for a services-only rule. Over-broad paths defeat the purpose of scoping.
- **When in doubt, leave it out.** A rule that's wrong or misleading is worse than no rule at all. If you can't verify something from the codebase, don't include it.
