# SPEC — Strata: Software Engineering Knowledge & Agent Context Layer

**Status:** Draft v0.1 (for review)
**Date:** 2026-08-16
**Author:** Human (reviewer) + AI planning session

---

## 1. Vision

Build a GitHub repository that is simultaneously:

1. **An expert knowledge base** covering software development from the highest abstraction
   levels (system design, architecture, organization) down to the lowest (OS, ISA, hardware),
   grounded in industry standards (SWEBOK, CS2023, ISO, CMMI) and scientifically validated
   learning science, with every claim traceable to an evidence record and a confidence tier.
2. **An agent harness layer** — any coding agent (Claude Code, opencode, Cursor, Codex, etc.)
   pointed at this repo can: (a) **validate** a developer's understanding of any topic against
   the authoritative content, (b) **teach** at the developer's measured level using
   evidence-based techniques, (c) **coach** their journey with retrieval practice, spaced
   review, and calibration.
3. **A journey system** — per-developer learning history, skill matrix, and review schedule
   stored **locally** (private, gitignored), while its **conventions** (schemas, templates,
   protocols) are committed to GitHub so any agent or tool can interoperate.

The repository itself is built cooperatively by a multi-level agent team under **graph
planning** (topological waves over a knowledge DAG), with human review gates.

Codename: **Strata**.

---

## 2. Goals & Non-Goals

### Goals (measurable)

- **G1.** A developer at any level can clone the repo, point any mainstream coding agent at
  it, and within ~5 minutes complete a "validate my understanding of X" session that returns:
  a verdict (correct / partially correct / incorrect), the supporting evidence with tier and
  citations, and a corrective learning path.
- **G2.** Published topics are complete per a strict Definition of Done (see §14 AC2):
  schema-valid, evidence-complete, graph-consistent, with a Bloom-aligned validation pack.
- **G3.** Coverage is continuously audited against SWEBOK v4.0 (18 KAs) and CS2023 (17 KAs)
  and reported as a measurable percentage with a missing-items list.
- **G4.** Journey data is 100% local by default (gitignored), schema-validated, and
  interoperable with any agent that follows the committed conventions.
- **G5.** Frontier/cutting-edge content is always dated, flagged as volatile, and CI raises an
  alert when its review deadline passes.
- **G6.** The structure scales: adding a topic = adding one folder; parallel agents never
  collide; indexes are regenerated deterministically; schema changes are versioned.

### Non-Goals (v1)

- Not an LMS, not a quiz platform, not an IDE plugin. (All can be built later on the data.)
- Not a replacement for the primary sources; it is a curated, mapped, cited layer over them.
- Not a code-generation repo; knowledge artifacts are markdown + machine-readable maps.
- Not a full curriculum for every CS subfield on day one; completeness is operationalized via
  the coverage audit (G3), not by pretense of total coverage.

---

## 3. Personas & Use Cases

| Persona | Level | Primary use cases |
|---|---|---|
| Novice (0–1 yr) | Band B4/B3 (see §6) | Validate basic mental models; follow learning paths; retrieval drills; spaced review |
| Mid (2–5 yr) | B3/B2 | Validate design decisions; close gaps (OS, networking); project review against standards |
| Senior/Staff | B2/B1/B5 | Validate architecture choices; explore frontiers; teach-by-explain-back |
| The Agent | — | Tutor, validator, journey recorder, knowledge contributor (via PRs) |

### Core flows

1. **Validate claim**: developer says "I think X because Y" → agent resolves topic →
   compares against `concept.md` claims → verdict + evidence record + tier + corrective path.
2. **Learn topic**: agent reads `profile.json` + skill matrix → teaches via
   `teaching.md` (worked examples, elaboration prompts) → runs `validation.md` practice
   tests (retrieval practice) → schedules spaced reviews.
3. **Review project**: developer submits a piece of work → agent evaluates against a rubric
   mapped to standards (e.g., ISO 25010 characteristics, SWEBOK testing KA) →
   records `project.reviewed` event.
4. **Plan curriculum**: agent computes a topological path from current mastery to a target
   topic using the knowledge DAG.
5. **Contribute knowledge**: agent proposes corrections/extensions → PR → CI + human gate.

---

## 4. Foundational Evidence (the science the system is built on)

> Axiomatic basis: `PRINCIPLES.md` — K0 (knowledge is claims with provenance), K1–K6
> (confidence, verification, scarce context, retrieval-based learning, data ownership,
> reproducibility) and theorem T1 (the knowledge graph is a DAG). Every section below
> is a derivation of those axioms; parameters (tracks, cadences, thresholds) are tunable.

The design decisions of this repo are themselves evidence-based. Every principle below maps
to a section of this spec and to an evidence record in `evidence/records/`.

### 4.1 Learning science (cognitive/educational psychology)

| Principle | Evidence | Applied where |
|---|---|---|
| Retrieval practice (testing effect) | Roediger & Karpicke (2006); **Dunlosky et al. (2013) — HIGH utility** | Every topic ships practice tests; sessions start with recall, not reading |
| Distributed practice (spacing) | Cepeda et al. (2006); **Dunlosky et al. (2013) — HIGH** | Spaced review ladder: 1, 3, 7, 14, 30, 60, 120 days; optimal gap ≈ 10–20% of retention interval |
| Interleaved practice | Rohrer & Taylor (2007); **Dunlosky et al. (2013) — MODERATE** | Mixed review sets across prerequisites |
| Elaborative interrogation | **Dunlosky et al. (2013) — MODERATE** | "Why does X work?" prompts in `teaching.md` |
| Self-explanation / Feynman | Chi et al. (1994); **Dunlosky et al. (2013) — MODERATE** | Explain-back prompts; agent grades against concept.md |
| Worked examples + cognitive load | Sweller & Cooper (1985); Sweller (1988) | Novice paths start with worked examples before problems |
| Deliberate practice | Ericsson, Krampe & Tesch-Römer (1993) | Validation items target Bloom level above comfort zone; feedback is immediate |
| Desirable difficulties | Bjork (1994) | Quizzes precede study; review before restudy |
| Skill acquisition stages | Fitts & Posner (1967); Dreyfus & Dreyfus (1980) | Level model for learners (see §6.4) |
| Metacognitive calibration | Flavell (1979) | Journey logs predicted-vs-actual scores; agent reports calibration curves |
| Taxonomy of objectives | Bloom (1956); Anderson & Krathwohl (2001) | Every validation item tagged remember→create; per-topic target level |

### 4.2 Industry standards (codified consensus)

| Standard | Version | Role in repo |
|---|---|---|
| SWEBOK (IEEE CS) | **v4.0, 2024** (v4.0a, Sep 2025) — 18 Knowledge Areas incl. new Architecture, Operations, Security | Primary SE topic spine; coverage audit target |
| CS2023 (ACM/IEEE-CS/AAAI) | Endorsed Jan–Feb 2024 — 17 KAs, competency model | CS-foundations topic spine; coverage audit target |
| ISO/IEC 25010 | **2023** — 9 product quality characteristics (usability→interaction capability; safety added) | Quality/testing track; project-review rubrics |
| ISO/IEC/IEEE 12207 | 2017 — lifecycle processes (superseded by the 2026 revision; claims citing S-0020 are dated to 2017) | Engineering-process track |
| ISO/IEC/IEEE 24765 | 2017 — SE vocabulary | Terminology canonicalization (claim-norming) |
| ISO/IEC/IEEE 42010 | 2022 — architecture description | Architecture track |
| CMMI | **V3.0, Apr 2023** (ISACA) — 31 practice areas (17 core + 14 domain), 8 domains | Engineering-process/maturity track; org-level topics |
| PMBOK | 7th ed., 2021 | Management topics (T2/T3) |
| ACM/IEEE curricula history | CS2013 → CS2023 | Coverage lineage, retired topics |

### 4.3 Evidence hierarchy (adapted from GRADE-style medicine-to-CS mapping)

Claims in the knowledge base are graded by type of support (stored in `evidence/records/`):

1. Formal proof / mathematical derivation
2. Meta-analysis / systematic review
3. Randomized controlled experiment
4. Quasi-experiment / controlled study
5. Large-N observational / correlational / industrial dataset study
6. Codified consensus standard (ISO, IEEE, SWEBOK, CMMI)
7. Practitioner literature / widely adopted patterns (books, industry reports)
8. Anecdote / blog / unreplicated claim

The **evidence tier** (T0–T4, §6.3) is derived from hierarchy level + breadth of acceptance +
currency. A claim must declare `[tier]` + at least one record id. Claims without a record are
forbidden in published content (`UNVERIFIED` is a state, not a tier).

---

## 5. Architecture Overview

Four layers + one construction machinery:

```
┌──────────────────────────────────────────────────────────────┐
│ LAYER 4  HARNESS   AGENTS.md · OVERVIEW/INDEX · protocol.md  │  ← how ANY agent behaves
│            prompt library · memory rules · codegraph/MCP     │
├──────────────────────────────────────────────────────────────┤
│ LAYER 3  JOURNEY   .journey/ (LOCAL, gitignored)             │  ← per-developer
│            profile · skill matrix · review queue · logs      │
│            + journey/ conventions (COMMITTED: schemas,       │
│              templates, privacy)                             │
├──────────────────────────────────────────────────────────────┤
│ LAYER 2  VALIDATION  per-topic validation.md packs           │  ← proving understanding
│            Bloom-tagged items · spaced review · rubrics      │
│            formative / summative / review banks              │
├──────────────────────────────────────────────────────────────┤
│ LAYER 1  KNOWLEDGE   knowledge/<track>/<topic>/              │  ← the facts
│            concept.md · teaching.md · frontier.md            │
│            evidence/records · standards maps · DAG           │
└──────────────────────────────────────────────────────────────┘
  CONSTRUCTION  Cooperative multi-level agent team + graph planning (→ docs/plan.md)
                CI quality gates · human review gates
```

Layers 1–4 are all committed to GitHub except `.journey/` (private). The construction
machinery (agent team, CI) is itself documented in this spec (§10) and the plan.

### 5.1 Layer 5 — Journey Interface (optional consumer, ADR-0001)

A local-first UI in `ui/` rendering journey + knowledge data. Reads `.journey/` and the
committed maps; writes only `.journey/` via the event schema; never mutates canonical
knowledge. Design system is code (tokens as CSS custom properties), documented in
`docs/design-system/`. Progressive disclosure mirrors the harness protocol (K3). No
accounts, no telemetry (K5). Data contract = committed schemas, never hardcoded formats
(K6).

---

## 6. Layer 1 — Knowledge Base

### 6.1 Knowledge model — four orthogonal axes

Every topic node is positioned on:

- **Axis A — Abstraction band** (the "high→low" vertical):
  - `B6` Enterprise / system-of-systems
  - `B5` System / product (distributed systems, platforms)
  - `B4` Application / component
  - `B3` Module / language
  - `B2` Runtime / OS / platform
  - `B1` ISA / hardware architecture
  - `B0` Microarchitecture / circuits (scope-limited)
- **Axis B — Domain track** (union of SWEBOK KAs and CS2023 KAs, deduplicated; see §6.5).
- **Axis C — Evidence tier** (T0–T4, §6.3).
- **Axis D — Learner depth** (Bloom target level, §7.1).

### 6.2 The knowledge graph (typed, multi-relational)

The graph is a **typed, multi-relational knowledge graph**, not a bare DAG. Only the
`prerequisite` edge type is order-constrained (theorem T1); every other edge type may form
loops because it asserts nothing about learning order.

**Node types**

| Node | Location | Key attributes |
|---|---|---|
| Topic | `knowledge/<track>/<id>/concept.md` | band, tier, bloom_target, status, updated, sources |
| Evidence record | `evidence/records/S-####.md` | type, hierarchy-level, year, venue/standard |
| Standard map | `standards/*-map.md` | KA / PA / characteristic sections |
| Track | `tracks.yml` | title, SWEBOK/CS2023 mappings |
| Rubric | `rubrics/<track>/*.md` | criteria, standards-refs |

**Edge types**

| Edge | Type | Cycle allowed | Meaning | Enforced by |
|---|---|---|---|---|
| `prerequisite` | directed | **NO** | must be mastered first | `check-graph.py` (T1) |
| `recommended` | directed, soft | no (ordering advice) | advised, non-blocking | `check-graph.py` (warning) |
| `related` | undirected | yes | cross-link, no ordering claim | `check-graph.py` (warning) |
| `sources` / `claims-supported` | topic ↔ record | yes | provenance bijection | `lint.py` |
| `replaced-by` | directed, temporal | n/a (retired nodes excluded from active graph) | obsolescence | `lint.py` |

**The DAG theorem (T1).** `prerequisite` is a strict partial order: "to learn Y you must
have mastered X" is transitive, antisymmetric, irreflexive. A cycle would mean no entry
point exists — nothing can be learned first — a contradiction. Acyclicity is therefore a
semantic invariant of that edge type, verified by CI at every commit. Other edge types are
deliberately unconstrained: richness of association without ordering claims.

**Versioned, not frozen.**

- Any commit may add nodes, re-point edges, or retire topics; CI re-verifies every
  invariant on each commit. History is preserved: nothing is deleted, retirement is a
  status (`retired`), not removal.
- During a session the graph is read-only: hot mutations would bypass verification (K2)
  and break determinism (K6). Contributions go through PRs (AGENTS.md §6).
- The learner's dynamic state is NOT in the graph: it lives in the per-learner overlay
  (`.journey/state/` — skill matrix, review queue, calibration). Shared canonical
  structure vs personal state is the K5 separation.

**Update protocol.** New/retired topic or edge change → PR → CI (schema, links,
acyclicity, determinism) → L2/L4 review → human gate → merge.

**Extension roadmap** (designed for, not built in v1): weighted edges (cost-optimal
paths), bloom-threshold edges (X at `apply` before Y at `analyze`), co-requisite
hyperedges, temporal validity windows, centrality/clustering curation analytics,
semantic/vector search over packs (MCP server).

### 6.3 Evidence tiers (Axis C)

| Tier | Meaning | Example | Handling |
|---|---|---|---|
| `T0` | Formal: proof-verifiable or mathematically exact | Halting problem undecidability; CAP impossibility proof | Highest confidence; cite proof/derivation |
| `T1` | Empirically strong: meta-analysis / RCT / large-N | Testing effect; code-review defect-removal data | Cite record with effect size if available |
| `T2` | Codified consensus: ISO/IEEE/SWEBOK/CMMI | SWEBOK testing KA; ISO 25010 characteristics | Cite standard clause |
| `T3` | Established practice: widely adopted patterns | SOLID, 12-factor, REST conventions | Cite canonical sources; note limits |
| `T4` | Frontier / volatile / not yet consensus | Agentic LLM architectures; WebGPU; post-quantum | MUST have `review_after` date + volatility flag; CI alerts on expiry |

Tier is assigned by **Evidence & Fact-Check agents** (L2), not by authors.
**Topic-level `tier` convention (v1.1):** a topic's tier is the *strongest* tier among its
claims — an upper bound on the confidence available in that pack. Individual claims carry
authoritative per-claim tiers; learner-facing displays and filters may use either, but must
state which.

### 6.4 Learner levels (placement protocol)

Placement combines: (a) self-assessment in `profile.json`, (b) a short adaptive diagnostic
using topic-adjacent validation items, (c) calibration history. Learner stages follow
Fitts & Posner (1967) + Dreyfus (1980): `novice → advanced-beginner → competent → proficient
→ expert`, mapped per track, NOT globally. Teaching adapts:
novice = worked examples first; competent = interleaved mixed review + project rubrics;
expert = explain-back + frontier reading + knowledge contribution.

### 6.5 Tracks (v1) and standards mapping

| Track dir | Covers (source KAs) |
|---|---|
| `cs-foundations` | CS2023: Algorithms, Mathematical foundations, Logic/computation; SWEBOK Computing & Mathematical foundations |
| `programming` | SWEBOK Construction; CS2023: SD Fundamentals, Programming Languages (FPL) |
| `data` | CS2023: Data Management, Data structures; DB theory |
| `architecture-design` | SWEBOK Architecture (new KA), Design, Models & Methods; ISO 42010 |
| `quality-testing` | SWEBOK Quality, Testing; ISO 25010:2023 (9 characteristics) |
| `security` | SWEBOK Security (new KA); CS2023 Security; OWASP (T3) |
| `systems-software` | CS2023: OS, Networking, Parallel & Distributed, Architecture & Organization |
| `hardware` | B1/B0 bands: memory hierarchy, cache coherence, ISA, microarchitecture (scope-limited) |
| `engineering-process` | SWEBOK Process, Management, Economics, Professional Practice; CMMI V3.0; ISO 12207 |
| `operations` | SWEBOK Operations (new KA), CM, Maintenance; DevOps practice (T3) |
| `ai-ml` | CS2023 AI, ML, agents; SWEBOK AI-in-SE notes |
| `frontiers` | Cross-cutting T4: agentic AI engineering, post-quantum crypto, WebGPU, formal verification at scale, ZK proofs |

v2 (deferred, mapped but not built): `hci-ux`, `graphics`, `parallel-computing` split, `games`.

Coverage audit (`tools/coverage.py`) compares topic inventory against every SWEBOK KA +
CS2023 KA and produces `docs/coverage-report.md` with % and missing items. **G3 is satisfied
by the report existing and being truthful, not by 100%.**

### 6.6 Topic pack anatomy (one folder per topic)

```
knowledge/<track>/<topic-id>/
├── concept.md      # THE validated knowledge: claims with [Tier]+[record-id] tags
├── validation.md   # Layer 2: quiz banks, exercises, rubric hooks (see §7)
├── teaching.md     # learning objectives, worked examples, elaboration prompts,
│                   #   common misconceptions, Feynman targets
└── frontier.md     # OPTIONAL (T4 only): dated, volatile-flagged, review_after
```

**Frontmatter contract** (every md; validated by CI):

```yaml
---
id: systems-software/virtual-memory
title: Virtual Memory & Paging
band: B2            # abstraction axis
track: systems-software
tier: T1            # evidence axis
bloom_target: apply # learner axis
prerequisites: [hardware/memory-hierarchy, hardware/isa-basics, systems-software/processes]
recommended: [systems-software/containers-isolation]
related: [hardware/cache-coherence, systems-software/containers-isolation]
status: published   # draft | validated | published | retired
schema-version: 1
owner: <agent-id>   # build-time
reviewed-by: [<agent-id>]
updated: 2026-08-16
sources: [S-0012, S-0047]   # evidence record ids
---
```

### 6.7 Evidence records

`evidence/records/<id>.md` — one per source (paper, standard clause, book):

```yaml
---
id: S-0047
type: meta-analysis | rct | quasi | observational | standard | practitioner
title: ...
authors: ...
year: 2006
venue/standard: ...
doi/url: ...
claims-supported: [os/virtual-memory, hw/memory-hierarchy]
hierarchy-level: 2
---
```

`evidence/hierarchy.md` documents the grading rubric (a.k.a. §4.3). `tools/lint.py` enforces:
every `[T*]` claim tag in `concept.md` maps to a record id present in `evidence/records/`.

---

## 7. Layer 2 — Validation

Proving understanding, not claiming it. Three banks per topic in `validation.md`:

| Bank | Purpose | Technique |
|---|---|---|
| **Formative** | Practice during study | Retrieval practice (Roediger & Karpicke 2006), immediate feedback |
| **Summative** | Topic mastery checkpoint | ≥80% correct on items at `bloom_target` level |
| **Review** | Spaced repetition | Mixed interleaved items from prerequisites + this topic, on due dates |

Item anatomy: `Q: <question>` · `bloom: <level>` · `bank: formative|summative|review` ·
`A: <model answer>` · `evidence: [S-####]` · `topic: <topic id>` (**required** on every
item — machines use it to assemble interleaved sets) · `distractors:` (optional; only for
multiple-choice style items).
`topic:` values must be clean topic ids (no parentheticals). A pack's frontmatter `sources`
lists the records backing the pack's own claims; review items may cite records from other
packs for interleaved prerequisites without listing them in `sources`.
Claim lines carry exactly ONE tier tag (the strongest applicable tier); additional record
refs follow the tier tag: `[T1][S-0037][S-0036]`.

Bloom targets (Anderson & Krathwohl 2001): `remember → understand → apply → analyze →
evaluate → create`. Per-topic default progression: concept quiz = understand; exercises =
apply; design scenarios = analyze/evaluate; capstone prompts = create.

Project-based validation: `rubrics/` per track map artifacts to standards (e.g., a system
design review rubric references ISO 25010 performance/scalability characteristics + SWEBOK
architecture KA). Agent scores with evidence pointers; outcome stored in journey.

---

## 8. Layer 3 — Journey (local data, committed conventions)

### 8.1 Split

| Committed (`journey/`) | Local only (`.journey/`, gitignored) |
|---|---|
| `README.md` — how to log, privacy rules | `profile.json` — alias, level per track |
| `schema/*.schema.json` — validation schemas | `state/skill-matrix.json` — per-topic proficiency |
| `templates/*.md` — session, checkpoint | `state/review-queue.json` — due items (spaced ladder) |
| `privacy.md` — defaults & opt-in sharing | `logs/YYYY-MM-DD-*.jsonl` — append-only event log |
| `examples/` — redacted sample records | `artifacts/` — projects, explain-backs, code |

### 8.2 Event taxonomy (JSONL, one object per line, schema-validated)

```
session.started|completed     session.schema.json
claim.submitted|verdict        claim schema (verdict: correct|partial|incorrect + evidence link)
quiz.attempted                 (quiz_id, bank, scores per bloom level)
review.due|completed           (spacing ladder bookkeeping)
elaboration.submitted          (explain-back, agent feedback)
project.submitted|reviewed     (rubric scores vs standards map)
matrix.updated                 (skill deltas)
calibration.updated            (predicted vs actual → calibration curve)
reflection.logged              (free text, metacognitive prompts)
```

Verdict vocabulary is intentionally split across artifacts: claims use
`correct|partial|incorrect`; checkpoints and project reviews use `pass|partial|fail`.
Event `payload` shapes are documented in `journey/README.md` (known contracts).

### 8.3 Privacy defaults

- No PII; pseudonymous alias; all data local; nothing leaves the machine without explicit
  opt-in (e.g., sharing an anonymized summary).
- Agents MUST NOT log raw conversation content; only structured events.
- `.gitignore` contains `.journey/` from day one; CI never touches it.

---

## 9. Layer 4 — Harness (agent-facing)

### 9.1 Progressive disclosure protocol (cognitive-load-motivated, Sweller 1988)

```
L0  README.md + OVERVIEW.md      — what this is, when to use, session recipes
L1  INDEX.md + knowledge-graph.yml + tracks.yml — navigation; load on demand only
L2  topic pack (concept/validation/teaching)     — loaded when a topic is relevant
L3  evidence records, rubrics, frontier notes    — loaded on demand
```

Rule for agents: **never dump the repo into context**; resolve via the graph, load L2
only for the topics in play. This keeps context budgets flat as the repo grows.

### 9.2 AGENTS.md contract (root, agents.md-compliant)

Mandatory behaviors for any coding agent pointed at this repo:

1. **Orient**: read `OVERVIEW.md` first, then `INDEX.md`/`knowledge-graph.yml` to locate
   topics. Never read `knowledge/` wholesale.
2. **Validate**: resolve the learner's claim to topic → compare against `concept.md` claims →
   verdict + evidence tier + record citations + corrected mental model → suggest
   `validation.md` items + schedule review.
3. **Teach**: place learner via `.journey/profile.json` + matrix (if present) → honor Bloom
   target → worked examples before problems for novices → end with retrieval practice.
4. **Record**: if the user consents, append structured events to `.journey/logs/` per the
   committed schemas. Never log raw chat; never invent events.
5. **Cite honestly**: only `evidence/records/` ids; `T4` content flagged volatile and dated;
   unknown → answer `UNVERIFIED` explicitly, never fabricate.
6. **Contribute**: corrections/expansions go through PRs (draft → CI → human gate), not
   silent rewrites of published content.
7. **Debrief**: at session end, update skill matrix + review queue + calibration.

### 9.3 Prompt library (`harness/prompts/`)

Copy-paste recipes making the harness agent-agnostic:

```
validate-claim.md    teach-topic.md      quiz-me.md         plan-curriculum.md
review-project.md    explain-back.md     update-journey.md  mentor-debrief.md
research-frontier.md audit-knowledge.md  session-kickoff.md
```

Each prompt is a self-contained template with placeholders (`<topic>`, `<level>`) and the
exact AGENTS.md clauses it activates. `harness/protocol.md` explains the protocol in prose;
`harness/memory.md` documents how agents with persistent memory (e.g., Claude Code memory)
should store durable facts (→ knowledge base PRs) vs session facts (→ `.journey/`).

### 9.4 Optional machinery (phase 6)

- `codegraph` index (`.codegraph/`) for cross-reference navigation (see AGENTS.md note).
- An MCP server (`tools/mcp-server/`) exposing: topic lookup, claim verification, quiz
  retrieval, journey append. Strictly optional; the markdown contract is the baseline.

---

## 10. Cooperative Multi-Level Agent Team (construction machinery)

### 10.1 Levels

| Level | Role | Produces | Gate |
|---|---|---|---|
| L0 | **Orchestrator/Planner** | wave plans, task graph, merge decisions | works with human |
| L1 | **Domain Research agents** (per track) | draft topic packs from primary sources | L2 review |
| L2 | **Evidence & Fact-Check agents** | tier assignment, citation integrity, currency, adversarial claim review | L4 + human for T0/T1 |
| L3 | **Pedagogy agents** | Bloom objectives, validation packs, spacing schedules, misconception lists | L2 cross-check |
| L4 | **Integration agents** | graph coherence, cross-links, index regeneration, linters | CI + human |
| L5 | **QA/Consolidation agents** | coverage audits, schema/link/tier audits, release notes | human |

### 10.2 Cooperation protocol

- **Ownership**: one agent owns a topic folder at a time (claim file in `workspace/claims/`).
- **Handoff**: every artifact carries `owner`/`reviewed-by` + handoff note; L2 approval flips
  `status: draft → validated`; human approval flips `validated → published` (per wave).
- **Workspace**: `workspace/` (gitignored) holds agent scratch; only `knowledge/`,
  `evidence/`, `journey/`, `harness/`, `docs/`, `tools/` are committed.
- **Conflict**: two agents never edit the same file; L0 resolves conflicts via the graph.
- **Determinism**: all generated files (indexes, maps) are produced by `tools/*.py`; CI
  fails on drift (`git diff --exit-code` after regen).

### 10.3 Human gates

1. Spec & plan approval (this document set) — *current checkpoint*.
2. Conventions freeze (Phase 0 output) — frontmatter, schemas, AGENTS.md.
3. Seed slices approval (Phase 2) — pipeline proven end-to-end.
4. Per-wave publish approvals.
5. Pilot feedback loop (Phase 6).

### 10.4 Graph planning = build waves

The topic DAG is topologically sorted; **wave k** contains topics whose prerequisites are
all in waves `< k`. L1 agents fan out per wave; L2 validates within the wave; L3 lags one
wave behind; L4 integrates at wave boundaries. CI checks: wave assignment is monotone
(a topic in wave k must not depend on wave > k). Parallelism scales with wave width.

---

## 11. Repository Layout (target)

```
/
├── AGENTS.md                 # harness contract (any agent)
├── README.md                 # entry + session recipes
├── OVERVIEW.md               # progressive disclosure L0
├── INDEX.md                  # L1: everything at a glance (auto-generated)
├── knowledge-graph.yml       # L1: machine-readable DAG (auto-generated)
├── tracks.yml                # L1: track definitions (hand-maintained)
├── knowledge/<track>/<topic>/…   # L2: topic packs
├── evidence/
│   ├── hierarchy.md          # evidence grading rubric
│   └── records/<id>.md       # source records
├── standards/                # SWEBOK/CS2023/ISO/CMMI maps + clause pointers
│   ├── swebok-map.md  cs2023-map.md  iso25010-map.md  cmmi-map.md  iso12207-map.md
├── journey/                  # L3 conventions (COMMITTED)
│   ├── README.md  privacy.md  schema/*.schema.json  templates/  examples/
├── .journey/                 # L3 data (LOCAL, gitignored)
│   ├── profile.json  state/  logs/  artifacts/
├── harness/
│   ├── protocol.md  memory.md  prompts/*.md
├── rubrics/<track>/*.md      # project-review rubrics mapped to standards
├── tools/                    # python stdlib only
│   ├── lint.py  index.py  check-graph.py  coverage.py  new-topic.py  regen-ci.sh
├── workspace/                # agent scratch (gitignored)
├── docs/
│   ├── spec.md  plan.md  adr/  coverage-report.md  changelog.md
├── .github/workflows/ci.yml
└── .gitignore                # .journey/, workspace/, *.tmp…
```

---

## 12. Tooling & CI (quality gates)

| Gate | Tool | Fails when |
|---|---|---|
| Frontmatter schema | `tools/lint.py` + JSON Schema | malformed/missing fields |
| Claim→evidence integrity | `tools/lint.py` | `[T*]` tag without record id |
| Link integrity | `tools/lint.py` | broken internal links |
| Graph acyclicity + wave monotonicity | `tools/check-graph.py` | cycles / backward wave deps |
| Index determinism | `tools/index.py` + `git diff --exit-code` | generated files drifted |
| Coverage | `tools/coverage.py` → `docs/coverage-report.md` | report out of date |
| Staleness | `tools/lint.py` | T4 `review_after` expired; topic `updated` > 18 mo |
| Journey conventions | schema tests on `journey/examples/` | examples invalid |
| Tier distribution | `docs/coverage-report.md` | unpublished-tier gaps reported |

Python 3 stdlib only (zero-dependency CI). GitHub Actions runs all gates on PR + schedule.

---

## 13. Non-Functional Requirements

- **Scalable**: folder-per-topic; parallel agent safety; deterministic regen; progressive
  disclosure keeps agent context flat; graph-based dispatch scales with topic count.
- **Maintainable**: schemas-as-code, CI gates, templates (`tools/new-topic.py`), ADRs for
  structural decisions, changelog, ownership metadata.
- **Portable**: baseline = markdown + YAML frontmatter + JSON Schema + JSONL + stdlib Python;
  no proprietary runtime; works with any mainstream coding agent.
- **Honest**: tier discipline; UNVERIFIED is a state; staleness alerts; no fabricated
  citations (L2 enforced, CI enforced).
- **Private**: journey local by default; documented opt-ins; CI never touches `.journey/`.
- **Licensing**: knowledge content under CC-BY-4.0 (attribution, open), tooling under MIT;
  evidence records keep original source licenses/attribution. *(Open decision §14.3)*

---

## 14. Acceptance Criteria

- **AC1** (G1): A fresh clone + one mainstream coding agent + one pasted prompt from
  `harness/prompts/validate-claim.md` yields a verdict with evidence tier + citations +
  corrective path, in a single session.
- **AC2** (G2): 100% of `status: published` topics pass: schema, links, claim→evidence,
  prerequisites resolvable, `validation.md` with ≥6 Bloom-tagged items spanning ≥3 Bloom
  levels including `bloom_target`, `teaching.md` with ≥1 worked example + ≥3 misconception
  corrections.
- **AC3** (G3): `docs/coverage-report.md` exists, CI-green, lists % and missing items vs
  SWEBOK v4 (18 KAs) and CS2023 (17 KAs).
- **AC4** (G4): agent writes a full session (`session.completed`, `quiz.attempted`,
  `matrix.updated`) to `.journey/`; all lines validate against committed schemas;
  `git status` shows `.journey/` untracked; conventions documented in `journey/README.md`.
- **AC5** (G5): every T4 artifact has `review_after`; CI turns red on expiry; `UNVERIFIED`
  never appears in published content.
- **AC6**: Two agents can work on two topic folders in the same wave without file conflicts
  (workspace protocol) — verified in Phase 3 dry run.
- **AC7** (pilot, G1): one developer completes validate → learn → project-review; their
  calibration data (predicted vs actual) is logged and summarized by the agent.

---

## 15. Open Decisions (resolved 2026-08-16)

1. **Language**: English-only — **RESOLVED: English-only**. (Schema allows `lang` later.)
2. **License**: CC-BY-4.0 knowledge + MIT tooling — **RESOLVED: adopted**; formalized in `LICENSE` files at v1.0 (plan 6.4).
3. **Scope of low end**: — **RESOLVED: stop at ISA/cache coherence; B0 microarchitecture scope-limited**.
4. **Track priority order** — **RESOLVED: follow the recommended wave order** (§6.5 / plan Phase 3).
5. **Journey location**: — **RESOLVED: repo-local `.journey/`** (gitignored).
6. **Naming**: — **RESOLVED: codename "Strata" kept**.
7. **Review cadence for frontier**: — **RESOLVED: 6 months default**.
8. **Public repo?** — **RESOLVED: yes, public** → `journey/examples/` must remain fully synthetic/redacted (CI-validated, enforced by `tools/lint.py`).

All decisions are recorded in `docs/adr/` at release time (plan 6.4).

---

## 16. Definition of Done (spec level)

- [ ] All open decisions §15 resolved or explicitly deferred with defaults.
- [ ] `docs/plan.md` approved; phases map 1:1 to acceptance criteria AC1–AC7.
- [ ] Phase 0 freezes: frontmatter spec, schemas, AGENTS.md, .gitignore, CI skeleton.
- [ ] Phase 2 seed slices demonstrate the full pipeline (draft → validate → publish → journey).
- [ ] Coverage report green after first full wave.
