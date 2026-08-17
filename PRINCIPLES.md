# PRINCIPLES — the axiomatic basis of Strata

> Every system is designed with a principle (or a theorem). These are Strata's.
> Read this before changing the design: a change that contradicts an axiom is a new
> system, not a modification. A change to a parameter is a tuning.

## The root axiom

**K0 — Knowledge is claims with provenance.**
A knowledge base is not a collection of prose documents; it is a set of claims, each
attached to its evidence, its confidence, and its boundaries. Prose without claim tags is
untestable; tags without records are fabrication. Everything in Strata follows from this.

## Derived axioms

**K1 — Confidence is attached, never implied.**
Every claim carries a tier (`T0`–`T4`) and at least one evidence record (`S-####`). The
grade of the record is fixed by an evidence hierarchy (8 levels, method-based).
`UNVERIFIED` is an explicit state, not a euphemism.
*Enforced by:* concept.md contract, `tools/lint.py` (claim-tag ↔ record bijection),
`evidence/hierarchy.md`.

**K2 — Truth passes through verification before it teaches.**
Content moves `draft → validated → published`. Authors propose; fact-checkers (L2) grade
tiers; humans publish. Nothing that can mislead a learner is published on author authority
alone. *Enforced by:* status machine + `reviewed-by`, human gates in `docs/plan.md`.

**K3 — Context is a scarce resource.**
Agent context windows and human attention are both finite. Information access must be
cost-proportional: resolve via maps (L1), load only the packs in play (L2), fetch deep
artifacts on demand (L3). Never dump the repo. *Enforced by:* `AGENTS.md` §1, generated
`INDEX.md` / `knowledge-graph.yml`, folder-per-topic granularity.

**K4 — Learning is retrieval + spacing, not exposure.**
Rereading feels effective and is not (Dunlosky et al. 2013 — low utility). Every topic
ends in retrieval practice, gets spaced reviews (1/3/7/14/30/60/120 days — Cepeda et al.
2006), interleaves prerequisites (Rohrer & Taylor 2007), and records predicted-vs-actual
calibration (Flavell 1979). *Enforced by:* validation.md contract, review-queue schema,
`AGENTS.md` §3.

**K5 — The learner owns their data; the community owns the conventions.**
Journey data is private by default and stays local (`.journey/`, gitignored). The schemas,
templates, and protocols that make that data portable are public (`journey/`).
*Enforced by:* `.gitignore`, `journey/README.md`, privacy defaults.

**K6 — Convention-as-code; everything generated is reproducible.**
Interfaces are schemas; generated files are tool outputs; drift is a CI failure. If it can
be derived, it is derived. *Enforced by:* `tools/*.py`, CI `git diff --exit-code` gate.

## The structural theorem

**T1 — The knowledge graph is a DAG.**
Topics and prerequisites form a directed acyclic graph; build waves and learning paths are
its topological order. Violating this (cycle, dangling prerequisite) fails CI. Corollary:
every learner at every level can be placed in the graph and given a corrective path.
*Enforced by:* `tools/check-graph.py`.

## Empirical laws the pedagogy is bound to

- Testing effect — Roediger & Karpicke (2006); Dunlosky et al. (2013, HIGH utility)
- Spacing effect — Cepeda et al. (2006)
- Interleaving — Rohrer & Taylor (2007)
- Self-explanation — Chi et al. (1994)
- Worked examples / cognitive load — Sweller & Cooper (1985); Sweller (1988)
- Deliberate practice — Ericsson et al. (1993)
- Metacognitive calibration — Flavell (1979)
- Objectives taxonomy — Bloom (1956); Anderson & Krathwohl (2001)

## Axioms vs parameters

| Axes (fixed) | Parameters (tunable) |
|---|---|
| K0–K6, T1 | 12 tracks, 6-month T4 review cadence, 80% mastery bar, 18-month staleness, review ladder intervals, B0 scope, default Bloom target, seed topic choice |

Parameters can be debated and changed without changing the system. Axioms cannot —
changing one is a redesign.

## Decision trace (examples)

| Decision | Basis | Where enforced |
|---|---|---|
| claim tags `[T0..T4]` + `[S-####]` | K0, K1 | concept.md contract, `lint.py` |
| `review_after` required on T4 | K1 | `lint.py` expiry check |
| `draft → validated → published` | K2 | frontmatter status, plan gates |
| L0→L3 loading protocol | K3 | `AGENTS.md` §1 |
| every topic ships `validation.md` | K4 | lint (published), `new-topic.py` |
| `.journey/` gitignored, `journey/` committed | K5 | `.gitignore`, `journey/README.md` |
| generated files + drift check | K6 | CI workflow |
| waves = topological bands | T1 | `check-graph.py`, plan Phase 3 |
