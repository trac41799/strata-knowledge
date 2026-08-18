---
id: quality-testing/quality-models
title: Quality Models
band: B5
track: quality-testing
tier: T2
bloom_target: understand
prerequisites: [engineering-process/requirements-engineering]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-quality-models
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0019, S-0108, S-0109, S-0110]
---

# Quality Models — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — List the nine ISO 25010:2023 product quality characteristics and the five quality-in-use characteristics; name McCall's three perspectives. (evidence: S-0019, S-0108)
- understand — Explain the distinction between product quality and quality in use, between internal, external, and quality-in-use measures, and the requirement-measure-evaluation traceability chain. (evidence: S-0019, S-0110) — **bloom_target**
- apply — Map a requirements statement or a user complaint to the correct characteristic and subcharacteristic, and propose a measure for it. (evidence: S-0019, S-0110)
- analyze — Decompose a quality problem into product-quality properties vs quality-in-use outcomes and identify where measurement must happen. (evidence: S-0019, S-0110)

## Worked example

### Part A — Quality model as diagnostic vocabulary (ISO 25010:2023)

Context: a rideshare app's product team collects complaints after a big release: (1) "app crashes when the driver calls mid-ride"; (2) "night mode is unreadable"; (3) "the rating screen takes 8 seconds to open"; (4) "passengers who don't speak English can't get help".

Step 1 — Map each complaint to the product quality model:
- (1) reliability — faultlessness (performs without faults) and fault tolerance (maintains performance despite the call); also compatibility — co-existence (shares the environment with the phone call).
- (2) interaction capability — operability/self-descriptiveness (screen readable under the selected mode).
- (3) performance efficiency — time behavior (response time).
- (4) interaction capability — inclusivity (usable by people with diverse language characteristics) and user assistance.

Step 2 — Separate product quality from quality in use. Product quality says *properties* of the app are wrong (crash rate, latency, contrast). Quality in use asks *outcomes*: "can a passenger still complete the trip successfully during a call?" (effectiveness), "how long does a driver spend fighting the app?" (efficiency), "do users trust the app after crashes?" (satisfaction). The fix list changes depending on which question you answer — which is exactly why the model separates the two views.

Step 3 — Choose measures per the measurement framework (ISO 25020:2019). Internal measures: static analysis of the call-handling code path; complexity of the rating screen. External measures: crash rate during injected in-call state; p95 latency of the rating screen under load. Quality-in-use measures: task success rate of the help flow for non-English users in a usability lab (test environment designed for the intended users, since the product is not yet released).

Step 4 — Write the quality requirements with traceability: "reliability — faultlessness: crash rate < 0.1% during in-call sessions, measured by (external) crash-rate metric, target verified in evaluation before release." Each requirement names its characteristic, its measure, and its verdict criterion.

### Part B — Reading a historical model (McCall 1977)

Same app through McCall's lens: the crash-during-call complaint is product operation — reliability (and integrity, if data was corrupted); the slow rating screen is efficiency; the night-mode problem is usability. The maintainer's viewpoint (product revision — maintainability, flexibility, testability) asks how cheaply the team can fix these. McCall's contribution is that every factor carries criteria and metrics: "reliability" is not a vibe, it maps to error-frequency metrics. The vocabulary is older and coarser than ISO 25010, but the skeleton — factors decomposed into measurable criteria — is the direct ancestor of the ISO model.

## Elaboration prompts

- Why did ISO 25010:2023 add safety as a ninth characteristic and rename usability and portability? What new requirements does that vocabulary make expressible? (evidence: S-0019)
- A product passes every internal and external measure yet users still fail in the field. Which quality view was never measured, and why can the other two not substitute for it? (evidence: S-0110)
- Trace a single requirement from a requirements document through the quality model to an evaluation verdict — where does each SQuaRE division (2501n, 2502n, 2503n, 2504n) sit in that chain? (evidence: S-0019, S-0110)
- McCall's factors and ISO 25010's characteristics both decompose quality — what did the 25 years between them add besides vocabulary? (evidence: S-0108, S-0019)
- Which quality-in-use characteristic would you sacrifice to satisfy a product-quality requirement, and who decides? What does that say about what a quality model cannot do? (evidence: S-0019)

## Common misconceptions

1. **"Quality in use is just user satisfaction."** Satisfaction is one of five quality-in-use characteristics — effectiveness, efficiency, freedom from risk, and context coverage are separate dimensions. (evidence: S-0019)
2. **"ISO 25010 is a checklist you score once."** It is a specification and evaluation scheme: characteristics express requirements, measures quantify them, evaluation judges them — a single composite score is not its purpose. (evidence: S-0019, S-0110)
3. **"Static-analysis metrics prove quality."** Internal and external measures indicate quality in use only indirectly; outcomes must be measured in context (or in a faithful test environment with intended users). (evidence: S-0110)
4. **"McCall/Boehm are alternative modern quality standards."** They are the historical precursors from 1977/1978 whose decomposition pattern ISO 9126 and SQuaRE standardized; current practice uses ISO 25010. (evidence: S-0108, S-0109, S-0019)
5. **"The model tells you which trade-off to make."** The model names the dimensions (e.g., security vs interaction capability); resolving conflicts between characteristics remains an engineering and product decision. (evidence: S-0019)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. The difference between "the product is well built" and "the product works for its users" — with one example where they diverge. Grade against the two-views claims. (evidence: S-0019, S-0110)
2. Why "the code is clean" (internal measure) is not the same as "users finish their task" (quality-in-use measure), and what you must actually measure to know the second. Grade against the measure-category claims. (evidence: S-0110)
3. How a 1977 report from the US Air Force still shapes how we talk about software quality today. Grade against the McCall/Boehm claims. (evidence: S-0108, S-0109)

## Interleaving hooks

- **engineering-process/requirements-engineering (prerequisite):** NFRs are the raw material; the quality model is their vocabulary — revisit R1, R3 in validation.md.
- **engineering-process/software-lifecycle (related):** the characteristics a lifecycle must verify (esp. safety) come from this model; verification/validation processes are where measures get collected.
- **quality-testing/software-testing-basics (related):** test strategies map to characteristics — fault-injection for reliability, load testing for performance efficiency, accessibility review for inclusivity.
- **quality-testing/software-metrics (recommended chain):** internal/external/quality-in-use measure categories are the formal home of the metrics this topic introduces.
- **security/risk-analysis (cross-track):** security as a product quality characteristic (confidentiality, integrity, resistance) links the quality model to threat-driven security work.
