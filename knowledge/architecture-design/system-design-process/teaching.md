---
id: architecture-design/system-design-process
title: System Design Process
band: B5
track: architecture-design
tier: T2
bloom_target: analyze
prerequisites: [architecture-design/architectural-styles, engineering-process/requirements-engineering]
related: [engineering-process/software-lifecycle, quality-testing/quality-models]
recommended: [quality-testing/quality-models]
status: published
schema-version: 1
owner: l1-system-design-process
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0018, S-0019, S-0020, S-0021, S-0152, S-0153, S-0154]
---

# System Design Process — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **understand** — explain the requirements → architecture → design flow and why it iterates, per SWEBOK and ISO 12207 ([S-0017], [S-0020]).
- **apply** — produce an architecture description for a described system: stakeholders, concerns, viewpoints, views, and correspondences, per ISO/IEC/IEEE 42010 ([S-0021]).
- **analyze** — given requirements and constraints, choose an architecture and style, justify the choice with the tradeoffs accepted, and identify what must be evaluated before committing ([S-0019], [S-0152]).
- **analyze** — run an ATAM-style evaluation on an architecture description: quality-attribute goals, scenarios, sensitivity points, tradeoff points, risks ([S-0152]).
- **evaluate** — judge whether documented rationale is adequate to support future change ([S-0153], [S-0154]).

## Worked example 1 — a 42010 architecture description walkthrough (e-commerce checkout)

System: a checkout service that computes totals, takes payment (two providers), and emits OrderPlaced events. Goal: show the shape of an architecture description, not its final content.

1. **Stakeholders and concerns.** Shoppers (response time), finance (correct totals, audit trail), operators (availability at peak, capacity), payment team (provider replaceability), developers (modifiability of pricing rules).
2. **Pick viewpoints (42010).** A *context viewpoint* (system boundary, external interfaces), a *functional viewpoint* (components, data flow), a *deployment viewpoint* (processes, state, capacity), each documented as a viewpoint with conventions ([S-0021]).
3. **Produce the views.** Context view: checkout ↔ payment providers, catalog, orders DB. Functional view: CartService → PricingEngine → PaymentGateway (interface; one adapter per provider) → OrderEmitter; OrderEmitter publishes to the event bus. Deployment view: two stateless checkout replicas behind a load balancer, one orders DB, one Kafka cluster.
4. **Record decisions and rationale.** "Pricing rules live in PricingEngine behind an interface because tax rules change quarterly (change confinement)." Rationale is part of the architecture, per Perry & Wolf's elements/form/rationale model ([S-0154]).
5. **Evaluate with ATAM-lite.** Utility tree with two scenarios: "1,000 checkouts/min at month-end with 99.95% availability" (performance + availability) and "add a third payment provider in two weeks" (modifiability). Analysis: PaymentGateway adapter is a tradeoff point (provider independence vs. adapter code to maintain); the single orders DB is a sensitivity point for both capacity and availability; a Kafka outage is a risk for order completion ([S-0152]).
6. **Iterate.** The evaluation surfaces that checkout must not depend on Kafka being up for the synchronous path — the design is revised so OrderPlaced is published after commit. The loop closes back into architecture ([S-0017], [S-0020]).

## Worked example 2 — the flow, traced with feedback

Requirements: "5,000 concurrent users, 99.9% availability, pricing changeable weekly." Architecture: stateless API layer, order state in the DB, event bus to downstream. Design: services, repositories, schemas. Trace two feedback loops: (1) design reveals the DB cannot take the peak → architecture adds a queue and worker pool; (2) operations reports a month-end batch that starves the API → capacity requirement is restated, and the architecture's resource allocation is revised. Each loop re-enters earlier activities — the flow is iterative by construction ([S-0020]).

## Elaboration prompts

- Why does 42010 define viewpoint conventions *before* views exist? What goes wrong when a team draws diagrams without viewpoints?
- In worked example 1, which view would an auditor care about, and which would a new developer care about — and what happens if the two views contradict each other?
- Why is "evaluate before implement" a risk-management move rather than a formality? What does ATAM's stakeholder-driven utility tree buy that a checklist cannot?
- When is a tradeoff point *not* worth resolving? (Hint: think about which quality attribute is actually under contract.)

## Common misconceptions

- "A diagram is the architecture": views are a representation; the architecture includes decisions and rationale, and 42010 separates the architecture from its description ([S-0021], [S-0154]).
- "One view is enough": stakeholder concerns differ, so multiple viewpoints and correspondences are required ([S-0021]).
- "Evaluation tests functional correctness": ATAM analyzes quality attributes, not correctness — verification and testing own correctness ([S-0152]).
- "Design is a single upfront phase": requirements, architecture, and design iterate with feedback from implementation and operation ([S-0017], [S-0020]).
- "Scalability is a tuning problem": capacity follows from structural decisions made during architecture definition — it is a requirement to evaluate, per 12207 and ISO 25010's capacity subcharacteristic ([S-0020], [S-0019]).

## Feynman targets

- Explain to a product manager why "the architecture is the decisions, the diagrams are just the minutes of the meeting."
- Explain why the same floor plan (views) does not equal the building (architecture), using a house blueprint analogy.
- Explain how you would convince a team to spend a week evaluating an architecture before writing code — in terms of what it prevents.

## Interleaving hooks

- **architecture-design/architectural-styles (prerequisite):** style selection is the first candidate-architecture decision that tradeoff analysis evaluates — reuse the style-tradeoff matrix here.
- **engineering-process/requirements-engineering (prerequisite):** NFRs become the quality-attribute scenarios in evaluation; traceability links requirements → architecture → tests.
- **engineering-process/software-lifecycle (related):** architecture definition and design definition are lifecycle technical processes — this pack is their content.
- **quality-testing/quality-models (recommended):** ISO 25010's nine characteristics are the vocabulary for both stating quality requirements and scoring tradeoffs.
