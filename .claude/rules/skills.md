---
paths:
  - "plugins/*/skills/**/*"
---

# Skill authoring

Every skill ships as a folder under `plugins/<plugin>/skills/<skill-name>/` with a `SKILL.md` at the root. Additional resources live beside it — they're loaded only when `SKILL.md` points to them, so keep `SKILL.md` lean and offload detail.

## Folder layout

Seen in this repo:

```
skills/<skill-name>/
├── SKILL.md            # required — frontmatter + body
├── references/         # optional — docs loaded on demand (tables, reference material)
├── scripts/            # optional — deterministic helpers (Python) the skill runs via Bash
├── templates/          # optional — files the skill writes into user projects
└── evals/              # optional — eval cases for skill-creator
```

Don't invent new top-level subfolder names. If you have tabular data too big for `SKILL.md`, put it in `references/`.

## Frontmatter

```markdown
---
name: ab-test-designer
description: <one paragraph — what the skill does AND when it should trigger>
---
```

- `name`: kebab-case, matches the folder name and the skill's invocation suffix (`/memory-system:ab-test-designer`).
- `description`: this is the **sole** mechanism Claude uses to decide whether to invoke the skill. Make it pushy and specific about triggers — include both English and Vietnamese phrases when the target user mixes languages (see `learn-coursera` and `coder-memory-store` for examples). Under-triggering is the common failure mode; err on the side of more trigger phrases.

## Body structure

The body of `SKILL.md` is loaded into context when the skill triggers. Three levels of detail available:

1. **SKILL.md body** — always loaded when skill runs. Ideal ≤ 500 lines.
2. **`references/*.md`** — reference with an explicit pointer ("See `references/schema.md` for the full table"). Only loaded when Claude reads the file.
3. **`scripts/*.py`** — executed via Bash; output comes back but the source doesn't have to enter context.

Bias toward scripts for deterministic work (stat tests, regex audits, file transforms) — faster, cheaper, and reproducible. `marketing-toolkit/skills/ab-test-designer/scripts/ab_significance.py` and `seo-onpage-checklist/scripts/seo_audit.py` are the reference patterns.

## Writing style inside skills

- Use imperative voice ("Pick the domain", "Search first, write after") rather than "you should".
- Explain the **why** behind non-obvious rules so Claude can judge edge cases instead of blindly following. All-caps `MUST`/`NEVER` is a last resort when there's a real footgun.
- Avoid `ALWAYS do X` without context — pair it with a short reason.
- Don't duplicate information that belongs in a reference file. Point to the reference.

## Sub-agent / background patterns

Memory skills (`coder-memory-store`, `coder-memory-recall`) run via the Task tool with `subagent_type: "general-purpose"` and `run_in_background: true`. When authoring a skill that does slow I/O (file writes, web fetches, searches) and doesn't need to return data into the main conversation immediately, follow the same pattern. Document it at the top of `SKILL.md` as a **MANDATORY** section so future Claudes don't accidentally run it inline.

If the skill's subagent writes outside the project sandbox (e.g. to `~/.claude/` or a vault path), pre-grant the permission in the plugin's `settings.json` — see `plugins/memory-system/settings.json` for the shape.

## Multi-language triggers

Hung's workflows mix English and Vietnamese. Skills that face him (memory-system, learn-coursera) list Vietnamese trigger phrases in the description. Keep doing this — e.g. `"tìm khoá học về X"`, `"cập nhật kiến thức"`, `"dọn memory"`. It measurably improves auto-trigger rate.

## After editing a skill

- Behavior change or trigger edit → bump the plugin's `plugin.json` `version` and add a CHANGELOG entry.
- Body-only polish with no behavior change → no bump needed.
- Tell the user to `/reload-plugins` if the description changed — the trigger index is rebuilt on reload.
