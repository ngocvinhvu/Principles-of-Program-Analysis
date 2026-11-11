# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Nature of this directory

This is **not a code repository**. It is not a git repo and has no source code, build system, tests, or linters. It is a research/literature workspace (course "Kỹ thuật phân tích chương trình", Đề tài 5, Chapter 13).

```
papers/          source PDFs (arXiv)
cards/<id>/      Paper Cards from nature-paper-card: source_bundle.json, paper-card.md, audit-report.json
.claude/skills/  project-level nature-skills (copied from github.com/Yuan1z0825/nature-skills)
.venv/           Python venv for skill scripts (PyMuPDF installed)
experiments/     C1′-mini pipeline (doctest items → mutation → setup slice → call trace → contexts → API eval); see experiments/README.md
```

| Paper | Topic | Card |
|---|---|---|
| `2312.15223v2` | Survey: LLMs for Software Engineering | done (review) |
| `2505.13353v5` | Sense and Sensitivity: semantic recall in long-context code understanding (SemTrace) | done (discovery + resource) |
| `2608.21107v1` | Survey: LLMs at the intersection of SE and software security (J@k, E1–E4, G0–G3) | done (review) |
| `2610.30016v2` | Code Comprehensor: hierarchical docs + cross-modal retrieval for large repos | done (methods) |
| `2605.26177` | RepoMirage: repository perturbations for code agents (gap check) | done (resource + discovery) |
| `2409.06338` | Dolce: retrieval vs holistic long-context task classification (gap check) | done (methods + resource) |

Topic decision record (nature-social-science Step 6–8: novelty audit, Reviewer 2, feasibility, Topic Card "C1′-mini", deadline 2026-11-30, model = DeepSeek-V4-Flash via FPT Cloud OpenAI-compatible endpoint, env `LLM_BASE_URL`/`LLM_API_KEY` in `.claude/settings.local.json`; send `"thinking": {"type": "disabled"}` explicitly, thinking is on by default) is in `library/novelty-audit.md`. `papers/2601.03731.pdf` is RepoReason (ACL 2026), the closest prior work; no card yet.

Expanded literature (OpenAlex + Semantic Scholar sweeps, BibTeX) is in `library/expanded-reading.md` and `library/expanded.bib`. The S2 API key is in `.claude/settings.local.json` (`env.S2_API_KEY`), read by `~/.claude/skills/paper-search/scripts/paper_search.py`.

Common theme: LLMs for code/program understanding. Cross-cutting finding from the cards: evaluation weaknesses (shortcut-permitting benchmarks, self-generated test sets, data leakage).

## Working here

- The user writes in Vietnamese; produce notes, cards and summaries in Vietnamese, keeping technical terms in English.
- Quick PDF text: `pdftotext -layout <file> -`, or the Read tool with `pages`.
- Always run skill scripts with `.venv/bin/python`, not system `python3` (system Python lacks PyMuPDF).

## nature-skills

Skills live in `.claude/skills/nature-*`. Each `SKILL.md` is a router: it requires reading its `manifest.yaml` and every `always_load` file before producing output. `nature-shared` is a dependency of other skills, never invoked directly. `nature-proposal-writer` is invoked as `researchwrite`.

Most relevant for this project: `nature-paper-card` (structured deep-reading card), `nature-paper-xray` (deep single-paper comprehension), `nature-reader`, `nature-academic-search`, `nature-ref-verifier`, `nature-social-science` (topic selection / novelty audit), `researchwrite` (proposal), `nature-reviewer`, `nature-writing`, `nature-polishing`, `nature-paper2ppt`.
Need extra setup before use: `nature-downloader` (Node 22+, authenticated Chrome with remote debugging), `nature-literature-pipeline` (cron + messaging platform).

### nature-paper-card workflow (used for `cards/`)

```bash
SKILL=.claude/skills/nature-paper-card
.venv/bin/python $SKILL/scripts/prepare_paper.py papers/<id>.pdf --output cards/<id>/source_bundle.json
# write cards/<id>/paper-card.md (Sections 01–16, per references/card-schema.md)
.venv/bin/python $SKILL/scripts/audit_paper_card.py --card cards/<id>/paper-card.md \
  --bundle cards/<id>/source_bundle.json --locator-mode page-grounded --report cards/<id>/audit-report.json
```

The skill forbids writing replacement extraction/audit scripts or patching the bundled ones during a normal run; audit errors are blockers. `prepare_paper.py` may miss tables (it found none in `2610.30016v2`): check page images manually when the inventory looks incomplete.

## Overlapping custom skills/agents

The user also has their own research skills/agents: `paper-search`, `paper-digest`, `gap-analysis`, `topic-proposal`, `research-pipeline`, `novelty-critic`. These expect notes under `library/notes/`, which does not exist; current reading notes are in `cards/`. They overlap with nature-skills (`paper-digest` ≈ `nature-paper-card`, `topic-proposal` ≈ `researchwrite`), so ask or state which one is being used.
