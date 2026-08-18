---
id: architecture-design/architectural-styles
title: Architectural Styles
band: B5
track: architecture-design
tier: T1
bloom_target: apply
prerequisites: [architecture-design/modularity]
related: [architecture-design/design-patterns, architecture-design/system-design-process]
recommended: [architecture-design/system-design-process]
status: published
schema-version: 1
owner: l1-architectural-styles
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0018, S-0019, S-0147, S-0148, S-0149]
---

# Architectural Styles — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — classify a described system into an architectural style (layered, client-server, peer-to-peer, event-driven, pipe-and-filter, microservices/monolith) and justify the classification with the style's constraints ([S-0147]).
- **apply** — choose a style for a given set of requirements and constraints, naming the quality-attribute tradeoff being accepted ([S-0017], [S-0019]).
- **analyze** — compare two candidate styles on the same problem and state, per ISO 25010 characteristic, what each one buys and costs ([S-0019], [S-0147]).
- **evaluate** — judge whether a claimed benefit (e.g., "microservices make us scalable") is supported by evidence, using the systematic mapping study as a benchmark for what is known ([S-0149]).

## Worked example 1 — style selection trace (food-delivery platform)

Problem: a food-delivery company has 30k orders/day, spikey demand around lunch, a 20-person engineering org split into 3 feature teams, no dedicated ops team, and a legacy order database. Goals: ship a new payment provider in 2 weeks, survive a 5x lunch spike, keep the existing DB.

Trace:

1. **List candidate styles.** Monolith (single deployable unit), modular monolith (one unit, module boundaries), microservices (independent processes), event-driven (decoupled event exchange), client-server (API front vs backend).
2. **Match constraints to styles.** Team autonomy: 3 teams → they need separable work units (Parnas criterion from the modularity pack). Ops maturity: no dedicated ops → few moving parts. Spike: must scale the order-ingestion path specifically. Legacy DB: cannot be re-architected in 2 weeks.
3. **Tradeoff matrix (per ISO 25010 characteristics):** microservices buys modifiability (independent deployment) and fault isolation, but costs performance efficiency (network hops), reliability (distributed consistency), and operational complexity — which this org cannot carry ([S-0148]). Event-driven edges (order events → kitchen, rider dispatch, analytics) buy modifiability for new consumers at the cost of harder end-to-end reasoning ([S-0147]).
4. **Decision:** modular monolith with an event-driven edge and the database behind a module interface. Rationale: modifiability (new payment provider = new adapter behind an interface), performance efficiency (in-process calls on the critical path), and capacity (ingestion path can be replicated; queue absorbs the spike). Microservices deferred until team size and ops automation justify the distributed-systems costs — the style is a decision, not a trend ([S-0148]).

## Worked example 2 — style mix, not style monoculture

An e-commerce system: a layered core (presentation → application → domain → infrastructure), a client-server split between the mobile app and the API, an event-driven edge (OrderPlaced events feed recommendations and analytics), and a nightly batch pipeline in pipe-and-filter style (extract → transform → load). Trace which concern each style serves and where the seams between styles sit — mixing styles is normal ([S-0147]).

## Elaboration prompts

- Why does "vocabulary of components and connectors" make a style a family of architectures rather than a specific design? Give two architectures that are both layered but differ in structure.
- For the trading-platform comparison in validation item S3, which quality attribute would you accept degrading, and why?
- Where does the pipe-and-filter "no shared state" constraint show up in the modularity pack's information-hiding ideas?
- Under what conditions does the microservices-vs-monolith decision actually change the answer for a team you know?

## Common misconceptions

- "Microservices guarantee scalability": the style is a structural commitment; the systematic mapping study shows few studies even assess whether migration benefits materialize ([S-0149]).
- "One style per system": systems routinely combine styles — layered cores with event-driven edges are normal ([S-0147]).
- "Event-driven decoupling is free": indirection costs latency and end-to-end predictability ([S-0147]).
- "Microservices are inherently more modular": distribution adds consistency and ops complexity without improving boundaries; boundaries are designed, not granted ([S-0148]).
- "The style name determines quality": quality emerges from realization (tactics, allocation, infrastructure), not from the label ([S-0017]).

## Feynman targets

- Explain to a non-technical stakeholder why "we use microservices" is a claim about structure, not a promise about speed or scale.
- Explain why a pipeline of `grep | sort | uniq` and a data-processing cluster are the same style.
- Explain why choosing a style is like choosing a dialect: the vocabulary and grammar are fixed, but what you say with them is up to you.

## Interleaving hooks

- **architecture-design/modularity (prerequisite):** styles are module-boundary policies at system scale — the seam concept becomes the port/adapter boundary in style-level designs; Parnas's change-confinement criterion is the reason style selection matters.
- **architecture-design/design-patterns:** patterns (Adapter, Observer, Strategy) are the in-style mechanisms that realize a style's tradeoffs — continue there.
- **architecture-design/system-design-process (recommended):** style selection is the first decision evaluated in tradeoff analysis — the next pack shows how the chosen style is documented (views) and evaluated (ATAM).
