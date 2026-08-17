# Strata — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans / subagent-driven development to implement this plan phase-by-phase. Steps use checkbox (`- [ ]`) syntax for tracking. Content-generation tasks are executed by the cooperative agent team (L0–L5) defined in `docs/spec.md` §10; this plan is the L0 playbook.

**Goal:** Build the Strata repository — a standards-grounded, evidence-tiered software engineering knowledge base with validation packs, a local-first journey system, and a progressive-disclosure agent harness — built in topological waves by a cooperative multi-level agent team under human gates.

**Architecture:** Four committed layers (knowledge / validation / journey-conventions / harness) + one gitignored journey data layer + a gitignored agent workspace. The topic inventory forms a DAG (`knowledge-graph.yml`); build and learning both follow topological order. All generated files are deterministic outputs of stdlib-Python tools; CI enforces schema, links, evidence integrity, acyclicity, determinism, and staleness.

**Tech Stack:** Markdown + YAML frontmatter · JSON Schema · JSONL · Python 3 stdlib (no deps) · GitHub Actions · optional codegraph/MCP (phase 6).

**Spec:** `docs/spec.md` (read first; every phase cites its ACs).

---

## Strategy

- **Validation-first**: conventions, schemas, linters, and AGENTS.md exist BEFORE any content. Content that violates them is CI-red by construction.
- **Graph planning**: waves = topological bands of the topic DAG. Agent levels L1→L2→L3→L4 follow in order; L0 orchestrates; human gates at wave boundaries.
- **Vertical slice before breadth**: Phase 2 ships 5 seed topics spanning bands B1→B4 to prove the pipeline end-to-end before mass production.
- **Frequent small commits**: every completed task = one commit, `feat:`/`chore:`/`docs:` style.

---

## Phase 0 — Foundations & Conventions Freeze

**Input:** approved spec. **Output:** repo skeleton, schemas, AGENTS.md, CI, gitignore. **Gate:** human review → conventions frozen (AC2/AC4/AC5 prerequisites).
**Status: COMPLETED 2026-08-16** (tasks 0.1–0.12; tools verified: lint/check-graph/index/coverage exit 0; smoke test confirmed enforcement of claim-tag and prerequisite rules).

- [x] **0.1 Create repo skeleton** — create the layout from spec §11 (`knowledge/`, `evidence/`, `standards/`, `journey/`, `harness/`, `rubrics/`, `tools/`, `docs/adr/`, `.github/workflows/`); write `.gitignore` with `.journey/`, `workspace/`, `__pycache__/`; commit `docs/spec.md` + `docs/plan.md`.
- [x] **0.2 Write `OVERVIEW.md`** — 30-line L0 document: what the repo is, the 4 layers, the 3 core flows (validate/learn/review), how to run sessions with any agent, pointer to harness prompts.
- [x] **0.3 Write `AGENTS.md`** — implement spec §9.2 contract verbatim (orient / validate / teach / record / cite-honestly / contribute / debrief). Committed now so every later session is governed.
- [x] **0.4 Write frontmatter schema** — `tools/schemas/topic.schema.json` implementing spec §6.6 contract (id, band, track, tier, bloom_target, prerequisites, related, status, schema-version, owner, reviewed-by, updated, sources). Also `evidence.schema.json` (§6.7), `rubric.schema.json`.
- [x] **0.5 Write journey schemas** — `journey/schema/`: `profile.schema.json`, `skill-matrix.schema.json`, `review-queue.schema.json`, `session.schema.json`, `event.schema.json` (discriminated union per §8.2), `project-review.schema.json`, `checkpoint.schema.json`.
- [x] **0.6 Write `tools/lint.py`** — stdlib Python: validates frontmatter vs schemas, claim-tag→record integrity, internal link integrity, T4 `review_after` expiry, `updated` staleness (>18 mo). Exit 0/1 only.
- [x] **0.7 Write `tools/check-graph.py`** — builds DAG from `knowledge/**/concept.md` frontmatter; detects cycles; verifies wave monotonicity (spec §10.4); emits `knowledge-graph.yml` (deterministic ordering).
- [x] **0.8 Write `tools/index.py` + `tracks.yml`** — regenerate `INDEX.md` from live content; `tracks.yml` lists the 12 v1 tracks from spec §6.5 with their standard mappings.
- [x] **0.9 Write `tools/coverage.py`** — reads `standards/swebok-map.md` + `cs2023-map.md` (KA + unit lists), diffs against topic inventory, writes `docs/coverage-report.md`.
- [x] **0.10 Write `tools/new-topic.py`** — scaffolds a topic pack skeleton (concept/validation/teaching) from the frozen frontmatter contract.
- [x] **0.11 Write CI** — `.github/workflows/ci.yml`: on PR+schedule run lint → check-graph → index (with `git diff --exit-code`) → coverage → journey-examples schema test. Zero-dependency (`actions/setup-python` + stdlib).
- [x] **0.12 Commit** — `chore: phase 0 foundations`; verify: `python tools/lint.py` exits 0 on empty-but-valid skeleton.

**Gate 1 — HUMAN:** review conventions freeze; adjust frontmatter/schemas before any content is written.

---

## Phase 1 — Knowledge Graph Backbone

**Input:** frozen conventions. **Output:** graph skeleton, standards maps, evidence hierarchy. **Gate:** CI green (AC3 plumbing).
**Status: COMPLETED 2026-08-17** (5 L1 research agents produced verified maps; 22 evidence records; 68-topic inventory; 8 waves; coverage 5% baseline).

- [x] **1.1 Standards maps** — write `standards/swebok-map.md` (18 KAs + subtopic lists, from v4.0/v4.0a), `cs2023-map.md` (17 KAs + knowledge units), `iso25010-map.md` (9 characteristics), `cmmi-map.md` (31 practice areas), `iso12207-map.md` (lifecycle processes). Each entry maps to intended topic ids (can be `TBD:<track>/<id>` placeholders that coverage.py reports as gaps — that is by design).
- [x] **1.2 Evidence hierarchy** — write `evidence/hierarchy.md` implementing spec §4.3 (8-level GRADE-style rubric with CS examples).
- [x] **1.3 Seed evidence records** — create records for the 4.1 learning-science papers and 4.2 standards used by the seed slices: Ebbinghaus 1885, Cepeda 2006, Roediger & Karpicke 2006, Dunlosky 2013, Rohrer & Taylor 2007, Chi 1994, Sweller & Cooper 1985, Ericsson 1993, Bjork 1994, Fitts & Posner 1967, Dreyfus 1980, Bloom 1956, Anderson & Krathwohl 2001, Flavell 1979; SWEBOK v4.0, CS2023, ISO 25010:2023, ISO 12207:2017, ISO 42010:2022, CMMI V3.0. IDs `S-0001…`.
- [x] **1.4 Topic inventory (L0 + L1)** — enumerate v1 topics per track (68 ids across bands B1–B6) with prerequisites; run `check-graph.py`; commit `knowledge-graph.yml`. This IS the graph plan; waves derive from it (8 waves).
- [x] **1.5 Coverage baseline** — run `coverage.py`; commit first `docs/coverage-report.md` (16/311 = 5% — honest baseline).

**Gate 2 — HUMAN:** approve topic inventory + wave assignment.

---

## Phase 2 — Vertical Slices (pipeline proof)

**Input:** graph. **Output:** 5 published seed topics spanning bands B1→B4 + first journey records. **Gate:** human (AC1/AC2/AC4 proven on real content).
**Status: COMPLETED 2026-08-18** — 5 L1 agents drafted packs; L2 review by `deepseek/deepseek-v4-pro` (report: `docs/reviews/l2-seed-review-2026-08-18.md`; verdicts pass/pass-with-fixes, all findings applied: S-0027 DOI correction, S-0042 provenance, wording fixes, tier convention documented, validation anatomy normalized); human publish approved. Coverage 16/311 (5%).

Seed topics (one per band, chosen for breadth of techniques):

| Topic id | Band | Tier | Why this seed |
|---|---|---|---|
| `systems-software/http-caching` | B4 | T2/T3 | universally-known; tests validation-pack design |
| `programming/garbage-collection` | B3 | T1/T2 | strong empirical + consensus mix |
| `systems-software/virtual-memory` | B2 | T1 | textbook consensus + measurable facts |
| `systems-software/distributed-consensus` | B5 | T1/T2 | CAP/BFT proofs (T0 claims inside) |
| `hardware/cache-coherence` | B1 | T1/T2 | high→low sweep anchor; ties to memory hierarchy |

- [ ] **2.1 Draft packs (L1 research agents, one per topic)** — produce concept.md with claim-level `[Tier]+[S-id]` tags, teaching.md draft, validation.md item seed list, from primary sources only.
- [ ] **2.2 Evidence review (L2)** — verify every claim↔record mapping; reassign tiers where unsupported; produce adversarial review notes per pack.
- [ ] **2.3 Pedagogy pass (L3)** — Bloom targets, ≥6 items per validation.md spanning ≥3 Bloom levels incl. `bloom_target` (AC2), misconception lists, spacing schedule initialization (ladder 1/3/7/14/30/60/120 — Cepeda 2006).
- [ ] **2.4 Integration (L4)** — cross-link topics (`related`), run all tools, fix drift.
- [ ] **2.5 Human publish** — human reviews each pack; `status: validated → published`.
- [ ] **2.6 Journey dry run (L3 + human)** — a human does one real "validate → learn → quiz" session per seed topic using the harness; agent logs events to `.journey/`; validate examples against schemas; redact → `journey/examples/`.

**Gate 3 — HUMAN:** approve pipeline; sign off on quality of the 5 packs; freeze pack-quality expectations.

---

## Phase 3 — Wave-Based Parallel Build

**Input:** approved pipeline + graph. **Output:** published topic packs for waves 1–3 (≈ 20–30 topics). **Gate:** per-wave human approval (AC6).

Execution loop per wave (L0 dispatches; all artifacts through workspace/claims ownership):

- [ ] **3.W.1 Dispatch (L0)** — assign topic folders to L1 agents (one owner per folder); wave = topological band from `knowledge-graph.yml`.
- [ ] **3.W.2 Draft (L1)** — per topic: concept/teaching/validation drafts from sources.
- [ ] **3.W.3 Validate (L2)** — evidence integrity + tier + currency; notes; `status: draft → validated`.
- [ ] **3.W.4 Pedagogy (L3)** — finish validation packs + spacing + misconceptions; lags one wave behind L1.
- [ ] **3.W.5 Integrate (L4)** — cross-links, index/map regen, full tool run (lint/check-graph/diff).
- [ ] **3.W.6 QA (L5)** — coverage report refresh; tier-distribution report; release notes.
- [ ] **3.W.7 Human publish gate** — approve batch; `status: published`.
- [ ] **3.W.8 Wave parallel-safety test (AC6)** — verify no file collisions occurred (git log + workspace claims audit); fix protocol if any.

Wave 1 priority (fills coverage + high learner demand): `cs-foundations` core units, `programming` fundamentals, `data` core, `quality-testing` core, `security` core.
Wave 2: `systems-software` core (OS/networking/distributed), `architecture-design` core, `operations` core.
Wave 3: `engineering-process` core (CMMI/12207), `hardware` core, `ai-ml` core, first `frontiers` T4 packs.

---

## Phase 4 — Journey System Completion

**Input:** conventions + real session data from Phase 2.6. **Output:** full journey UX (AC4).

- [ ] **4.1 Templates** — `journey/templates/session.md`, `checkpoint.md`, `weekly-debrief.md`, `curriculum-plan.md` (topological path from matrix to target).
- [ ] **4.2 Review-queue logic** — document + implement `tools/review-due.py`: reads `state/review-queue.json`, emits due items by ladder date; agent runs it at session start (spaced repetition engine v1 — SM-2 optional v2).
- [ ] **4.3 Calibration reports** — `tools/calibrate.py`: predicted vs actual per topic; writes `state/calibration.json`; harness uses it to tune teaching level (spec §6.4).
- [ ] **4.4 Privacy doc** — `journey/privacy.md` (spec §8.3): defaults, opt-ins, redaction rules, example anonymization procedure.
- [ ] **4.5 Examples refresh** — re-run 2.6 with new templates; commit redacted examples; CI validates.

**Gate 4 — HUMAN:** journey UX usable; conventions complete.

---

## Phase 5 — Harness Polish

- [ ] **5.1 Prompt library** — all 11 prompts from spec §9.3, each self-contained with placeholders + protocol pointers; test each against a live agent session (dry run with sample claims).
- [ ] **5.2 `harness/protocol.md` + `memory.md`** — prose protocol; memory rules (durable facts → PRs, session facts → `.journey/`).
- [ ] **5.3 Rubrics** — `rubrics/` per track: e.g., `rubrics/system-design.md` (ISO 25010 + SWEBOK architecture), `rubrics/code-review.md` (SWEBOK construction/testing), `rubrics/security-review.md` (SWEBOK security + OWASP T3).
- [ ] **5.4 Optional machinery** — `.codegraph/` init (if desired); `tools/mcp-server/` stub (topic lookup + claim verify + quiz retrieve + journey append), documented in `harness/memory.md`.
- [ ] **5.5 AGENTS.md v2** — fold in lessons from all dry runs; re-verify every clause with a clean-context agent.

**Gate 5 — HUMAN:** harness demonstrated on 3 different agents (e.g., opencode, Claude Code, Cursor).

---

## Phase 6 — QA, Coverage Audit & Pilot

- [ ] **6.1 Full audit (L5)** — lint/check-graph/coverage/index-drift all green; `docs/coverage-report.md` refreshed; tier audit (no UNVERIFIED in published; T4 expiry list clean).
- [ ] **6.2 Pilot** — one volunteer developer at a chosen level runs AC1/AC4/AC7 scripts end-to-end over 2 weeks; agent records journey; debrief.
- [ ] **6.3 Fix loop** — implement pilot findings as PRs; update spec/plan/ADR as needed.
- [ ] **6.4 Release** — tag v1.0; changelog; `docs/adr/` decisions recorded (licensing, journey location, naming — per spec §15).

**Final gate — HUMAN:** acceptance criteria AC1–AC7 checked off.

---

## Team Manifest (cooperation protocol, spec §10.2)

- One owner per file; claim via `workspace/claims/<topic-id>.json`.
- Handoff = frontmatter `owner`/`reviewed-by` + notes; no oral lore — everything in files.
- L2 is the only tier-assigner; L0 the only merger; humans the only publishers.
- Generated files are sacred: never hand-edit `knowledge-graph.yml`/`INDEX.md`; always via tools.
- Cite only `evidence/records/`; never fabricate; never silently rewrite published content.

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Content volume overwhelms quality | Wave caps (≈10 topics/wave); L2 adversarial review; publish gates |
| Agent context bloat on large repo | Progressive disclosure enforced in AGENTS.md + CI checks on INDEX size |
| Fabricated citations | L2 + CI claim→record integrity; UNVERIFIED state |
| Schema drift | schema-version in frontmatter; CI; ADRs for changes |
| Stale frontier content misleads | T4 `review_after` CI expiry; 6-month default |
| Colliding parallel agents | ownership claims + folder-per-topic + deterministic regen |
| Learning-science misuse (e.g., cramming schedules) | ladder + interleaving built into validation.md templates; L3 owns pedagogy |

## Milestones & Timebox (agent-days, indicative)

| Milestone | Phase | Timebox |
|---|---|---|
| M0 Conventions frozen | 0 | 1–2 d + human |
| M1 Graph + maps | 1 | 1–2 d |
| M2 Seed slices published | 2 | 5–7 d |
| M3 Waves 1–3 | 3 | 3–4 wks |
| M4 Journey complete | 4 | 3–5 d |
| M5 Harness proven | 5 | 3–5 d |
| M6 Audit + pilot + v1.0 | 6 | 1–2 wks |

---

## Execution Handoff

Plan complete and saved to `docs/plan.md`. Two execution options when the human approves Gate 1:

1. **Subagent-Driven (recommended)** — dispatch fresh subagents per phase/task with L0 orchestration, human review between phases.
2. **Inline Execution** — execute in-session with checkpoint reviews per gate.

Awaiting: spec §15 open decisions + Gate 1 approval.
