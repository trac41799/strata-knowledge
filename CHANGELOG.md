# Changelog

All notable changes to Strata are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); the project is pre-1.0.

## [Unreleased]

- Wave 4: remaining 12 topic scaffolds (cs-foundations, programming, engineering-process,
  hardware leftovers).
- Journey Interface implementation (see `docs/plan-ui.md`).

## [0.3.0] — 2026-08-18

- **Wave 3 published**: 23 packs (data ×5, quality-testing ×5, security ×5, ai-ml ×4,
  frontiers ×4) — 56/68 topics published, ~200 evidence records.
- L2 review by `deepseek/deepseek-v4-pro` (`docs/reviews/l2-wave3-review-2026-08-18.md`):
  systematic T0 over-grading corrected (record-tier rule), Vaswani duplicate record
  consolidated, B-tree teaching bug fixed.
- Dry run (user-POV harness test): AC4 passed; AC1 enabled — 11 harness prompts shipped,
  per-type event payload constraints, `tools/validate-journey.py`.
- Repo published to GitHub (`trac41799/strata-knowledge`, public); open-source standards
  applied (LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, CITATION, PR
  template).

## [0.2.0] — 2026-08-18

- **Waves 1–2 published**: 28 packs (CS foundations, programming, hardware, engineering,
  networking, architecture, operations).
- L2 reviews archived (`docs/reviews/l2-wave1-review-2026-08-18.md`,
  `l2-wave2-review-2026-08-18.md`); uniform tier rule (spec §6.3), single-tier-per-claim
  lint rule, ISO 12207:2026 supersession noted.
- **Phase 7 (ADR-0001)**: Journey Interface design — 3 directions + vision critiques,
  hybrid design system (`ui/design-system/` + `docs/design-system/`), UI spec
  (`docs/spec-ui.md`, AC-UI-01..12), TDD plan (`docs/plan-ui.md`).

## [0.1.0] — 2026-08-16/17

- **Phase 0**: conventions freeze — schemas, `tools/*.py` pipeline (lint, graph, index,
  coverage, new-topic, import-inventory), CI, AGENTS.md, PRINCIPLES.md.
- **Phase 1**: knowledge graph backbone — standards maps (SWEBOK v4.0 18 KAs, CS2023 17
  KAs, ISO 25010:2023, CMMI V3.0, ISO 12207:2017), evidence hierarchy, 22 seed records,
  68-topic inventory, 8 waves.
- **Phase 2**: 5 vertical seed slices published (http-caching, garbage-collection,
  virtual-memory, distributed-consensus, cache-coherence) after deepseek-v4-pro L2 review.
