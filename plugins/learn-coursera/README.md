# 🎓 learn-coursera — Claude Code Plugin

A meta-skill for turning Coursera courses into Claude Code skills.

## What it does

5-phase pipeline:

1. **Discovery** — search Coursera for top professional courses on any topic and recommend picks.
2. **Extract + Enrich** — scrape video transcripts via Playwright, then enrich them into actionable engineer-facing notes.
3. **Propose + Score** — apply a 5-criteria rubric (novelty, specificity, executable, substantial, transfer test) to identify skill-worthy modules.
4. **Build** — scaffold winning skills with `/skill-creator`, including eval benchmarks (with-skill vs baseline).
5. **Package** — bundle skills into a Claude Code plugin with marketplace registration.

Handles single courses and full Professional Certificates.

## Triggers

English: *"find Coursera course on X"*, *"I want to learn new skill"*, *"turn this course into a skill"*, *"extract transcripts"*, *"best Coursera course for X"*.

Vietnamese: *"tôi muốn học kỹ năng mới"*, *"tìm kỹ năng mới"*, *"tìm khoá học về X"*, *"học một cái gì mới"*, *"lấy transcript"*, *"tạo skill từ khoá học"*, *"gợi ý khoá học"*.

## Proof

Built the sibling [`marketing-toolkit`](../marketing-toolkit) plugin (8 skills, 93% avg pass rate vs 48% baseline) from Google's Digital Marketing & E-commerce Certificate (7 courses, 267 videos) using this exact pipeline.

## Installation

```
/plugin install learn-coursera
```

## License

MIT
