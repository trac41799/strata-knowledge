# Strata — Overview

This repository is a knowledge base + agent harness for software engineering,
covering the discipline from high abstraction (system design, architecture,
organization) down to low abstraction (OS, ISA, hardware), grounded in industry
standards (SWEBOK v4.0, CS2023, ISO/IEC 25010, CMMI V3.0) and scientific learning
research.

## The four layers

1. **Knowledge** — `knowledge/<track>/<topic>/`: `concept.md` (validated facts,
   every claim tagged `[Tier]` + `[S-####]` evidence record), `teaching.md`
   (worked examples, misconceptions), `frontier.md` (dated, volatile, T4 only).
2. **Validation** — `validation.md` per topic: Bloom-tagged practice tests,
   mastery checkpoints, spaced-review items. Proving understanding, not claiming it.
3. **Journey** — `.journey/` (LOCAL, gitignored): your profile, skill matrix,
   review queue, event log. Conventions live in `journey/` (committed schemas).
4. **Harness** — `AGENTS.md`, `OVERVIEW.md`, `INDEX.md`, `knowledge-graph.yml`,
   `harness/prompts/`: how any coding agent should behave when pointed here.

## Core flows (with any coding agent)

- **Validate**: "Validate my understanding of <topic>: I think X because Y."
  The agent resolves the topic, compares against `concept.md`, returns a verdict
  with evidence tier + citations + corrective path.
- **Learn**: "Teach me <topic> at my level." The agent reads `.journey/profile.json`
  and skill matrix, uses `teaching.md`, then runs retrieval practice and schedules
  spaced review (1/3/7/14/30/60/120 days).
- **Review**: "Review my project against <rubric>." The agent scores against
  standards-mapped rubrics in `rubrics/` and logs the outcome to your journey.

## How to navigate

- `INDEX.md` — generated index of every topic (L1 map).
- `knowledge-graph.yml` — machine-readable prerequisite DAG (generated).
- `tracks.yml` — the 12 domain tracks and their standard mappings.
- `standards/` — SWEBOK / CS2023 / ISO / CMMI maps; `docs/coverage-report.md` shows
  how much of each standard the knowledge base covers.

## Session recipe (2 minutes)

1. Clone this repo and point your coding agent at it (as your working directory).
2. The agent reads `AGENTS.md` and `OVERVIEW.md` automatically.
3. Paste any prompt from `harness/prompts/` (e.g., `validate-claim.md`).
4. Session events are logged to `.journey/` when you consent. Nothing leaves your machine.

## Status

- v0.1: Phase 0 (conventions frozen) — see `docs/plan.md` for the build roadmap.
