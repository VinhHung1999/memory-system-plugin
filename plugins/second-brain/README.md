# 🧠 second-brain — Claude Code Plugin

An LLM-maintained personal knowledge wiki for your Obsidian vault.

Instead of re-deriving knowledge via RAG on every query, the LLM
incrementally compiles knowledge into a persistent, cross-linked wiki of
markdown files — so each question makes the next cheaper.

## What it does

Seven operations exposed via `/second-brain <op>` or natural phrasing:

| Op      | Purpose                                                    |
| ------- | ---------------------------------------------------------- |
| `init`  | One-time vault scaffold (idempotent)                       |
| `ingest`| Read a source, extract knowledge, file it into the wiki    |
| `query` | Answer from the wiki, with wikilink citations              |
| `lint`  | Audit wiki health — broken links, orphans, contradictions  |
| `note`  | One discrete note file at `wiki/notes/<slug>.md`           |
| `dump`  | Timestamped brain-dump in today's journal                  |
| `task`  | Add/move a kanban task (Todo/Doing/Review/Done)            |

Ingest/query/lint are heavyweight (touch many pages). Note/dump/task are
fire-and-forget capture.

## Setup

1. Install the plugin:

   ```
   /plugin install second-brain
   ```

2. Point the skill at your Obsidian vault via an env var (add to
   `~/.zshrc` or `~/.bashrc`):

   ```bash
   export SECOND_BRAIN_VAULT="/absolute/path/to/your/brain2"
   ```

   The vault folder can be named anything — `brain2` is just the
   convention used in docs.

3. Initialize the vault (creates `CLAUDE.md`, `log.md`, `wiki/wiki.md`,
   `wiki/overview.md`, `raw/assets/`):

   ```bash
   bash <skill-dir>/scripts/init.sh
   ```

   Or just say "init my second brain" and the skill will run it.

4. (Optional) For semantic search: install
   [`qmd`](https://github.com/anthropics/qmd) and index the `wiki/` folder
   as collection `brain2`. Ingest auto-reindexes.

## Triggers

**English:** *"ingest this article into my second brain"*, *"what does my
wiki say about X"*, *"lint my wiki"*, *"note quantum-computing:"*, *"brain
dump"*, *"add task [work] finish PR review"*.

**Vietnamese:** *"ghi chú ..."*, *"dump vào não"*, *"kiểm tra wiki"*, *"xài
second brain để ..."*, *"ghi lại ý"*, *"làm xong task ..."*.

## Philosophy

- **Knowledge should compound.** Don't just answer and let the answer
  disappear — file insights back so the next question benefits.
- **Folder-note MOCs.** Each folder has a file named after it, acting as
  the folder's table of contents. Wikilinks are bare slugs.
- **Contradictions are features.** When a new source contradicts existing
  wiki content, flag it in an `## Open questions` section — never
  silently overwrite.
- **Quality-first, never batch.** One source at a time with discussion,
  unless explicitly asked to batch.

## License

MIT
