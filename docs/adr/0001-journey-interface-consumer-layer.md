# ADR 0001 — Journey Interface as a Consumer Layer

- **Status:** Accepted (2026-08-18)
- **Scope change:** adds a UI/UX workstream previously excluded as a non-goal
- **Basis:** PRINCIPLES.md K3 (context is scarce), K5 (learner owns their data), K6 (convention-as-code)

## Context

The journey layer (`.journey/`) and knowledge layer are machine-readable by design.
Learners interact with them only through coding agents (harness layer). There is no
human-facing interface to browse the knowledge graph, run quiz sessions, or visualize
skill-matrix / calibration data. The product owner now requests a complete UI/UX design
workstream for the journey data.

## Decision

Add a **Layer 5 — Journey Interface**: an optional consumer application living in `ui/`
of this repository, governed by the same axioms:

- **K5 (data ownership):** the UI is local-first. It reads `.journey/` from the user's
  machine only; no accounts, no telemetry, no cloud sync. Journey data never leaves the
  machine (unchanged from the data-layer contract).
- **K3 (context is scarce):** the UI is progressive-disclosure by construction — overview
  → maps → topic → deep artifacts, mirroring the harness protocol.
- **K6 (convention-as-code):** the design system is code (CSS custom properties / tokens),
  documented in `docs/design-system/`; the UI consumes the committed schemas
  (`journey/schema/`, `tools/schemas/`) as its data contract, never hardcoded formats.
- The UI is a *consumer*: it never mutates canonical knowledge (PRs only, per AGENTS.md §6)
  and writes only `.journey/` via the event schema.

## Consequences

- `docs/spec.md` gains §5.1; `docs/plan.md` gains Phase 7 (design workstream) and Phase 8
  (implementation).
- New directory: `ui/` (committed) — `ui/explorations/` (design directions),
  later `ui/app/` + `ui/tests/`.
- Non-goal list updated: "not an LMS/quiz platform" remains true of the knowledge layer;
  the UI is a thin, local, optional consumer.
- No change to knowledge/journey schemas or the harness contract.
