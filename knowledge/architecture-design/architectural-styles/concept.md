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

# Architectural Styles

## Claims

### Styles as decision vocabulary

- An architectural style defines a family of architectures: it prescribes a vocabulary of components and connectors (e.g., filters and pipes), topological constraints (e.g., the graph must be acyclic), and semantic constraints (e.g., filters cannot share state); an architecture is an instance of a style when it obeys those constraints. [T3][S-0147]
- Because a style constrains the form and structure of a family of instances, choosing a style is choosing a bundle of design decisions; Garlan & Shaw argue that recognizing common patterns lets new systems be built as variations on known families, and that selecting an appropriate architecture is crucial to a system's success. [T3][S-0147]
- SWEBOK v4's Software Architecture KA treats architectural styles and patterns as core architecture-design content — including layered, event-driven, and microservices styles — alongside architecture representation (views such as 4+1 and the C4 model) and quality-attribute design. [T2][S-0017]
- Styles are the vocabulary in which architectural decisions are stated and communicated: SWEBOK frames architectural design as transforming requirements into an architecture by making design decisions, and styles/patterns are the named alternatives among which those decisions choose. [T2][S-0017]
- SWEBOK's Architecture KA covers quality-attribute design — how to realize quality requirements such as performance, availability, security, and maintainability through architecture — which is how a chosen style is turned into measured qualities. [T2][S-0017]

### Styles

- Layered style: the system is organized into layers, each layer exporting services used by the layer above and using services of the layer below (e.g., the OSI reference model); layering supports portability, information hiding, and divide-and-conquer development, at the cost of indirection and constraints on how layers may interact. [T3][S-0147]
- Client-server style: processing is partitioned into servers that provide services and clients that consume them over a network protocol; the style supports shared, centralized data and independent evolution of clients and servers, but the server can become a bottleneck and a single point of failure. [T3][S-0147]
- Peer-to-peer style: processing elements act as symmetric peers that both provide and consume services without a central coordinator; the style avoids a central bottleneck and single point of failure, at the cost of coordination complexity (discovery, consistency, security). [T3][S-0147]
- Event-driven (implicit invocation) style: components interact by announcing events at runtime, and components can register handlers for events; a producer does not name its consumers, so components evolve and integrate independently, but end-to-end behavior becomes harder to predict and debug. [T3][S-0147]
- Pipe-and-filter style: components are filters that transform an input data stream into an output stream, connected by pipes; the family is a graph of incremental stream transformers, and filters do not share state, which makes filters simple, reusable, and replaceable, while the style fits stream processing better than interactive, stateful applications. [T3][S-0147]
- Microservices (Lewis & Fowler, 2014): an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API; services are built around business capabilities and are independently deployable. [T3][S-0148]
- Microservices' common characteristics include decentralized governance and data management, smart endpoints with dumb pipes (domain logic in the services, simple messaging between them), infrastructure automation, and design for failure; the style presumes operational automation such as continuous delivery and monitoring. [T3][S-0148]
- The monolith is the contrasting option: an application deployed as a single unit that communicates internally via in-process calls; Lewis & Fowler present the choice as a tradeoff — independent deployment and team autonomy against the costs of distribution (network latency, data consistency, operational complexity). [T3][S-0148]
- Microservices are a decomposition vehicle, not a guarantee of modularity: the style changes the deployment and independence unit, while module-boundary quality (information hiding, cohesion) still has to be designed within and across services. [T3][S-0148]

### Quality attributes and tradeoffs

- ISO/IEC 25010:2023 defines nine product quality characteristics — functional suitability, performance efficiency, compatibility, interaction capability, security, safety, reliability, maintainability, flexibility — and architectural styles realize different mixes of them, so choosing a style is choosing which qualities to favor. [T2][S-0019]
- Style choice trades quality attributes against each other: for example, loose coupling (event-driven, pipe-and-filter) buys component independence and modifiability but adds runtime indirection and makes performance and end-to-end behavior harder to predict than with direct-call styles. [T3][S-0147]
- CS2023's Software Engineering KA includes architectural design — styles, views, and architecture description — among the core software development competencies. [T2][S-0018]

## Details

A style is a template for structure, not a structure itself. The same style
name covers infinitely many architectures that share component/connector
vocabulary and constraints. Real systems commonly combine styles: e.g., a
layered core with an event-driven edge and a client-server UI. When comparing
styles, the question is which quality attributes the stakeholders care about —
the style that maximizes modifiability is rarely the one that minimizes
latency.

## Boundaries / common misunderstandings

- "Microservices guarantee scalability": microservices is a structural style, not a performance outcome — a systematic mapping study of monolith-to-microservices migration found scalability and maintenance are the main stated drivers of migration but few studies actually assess whether the benefits materialize. [T1][S-0149]
- "One style must rule the whole system": styles describe families of architectures; mixing styles (a layered core with event-driven edges) is a design decision, not a violation. [T3][S-0147]
- "Event-driven is always better because it decouples": implicit invocation buys independence but adds runtime indirection and makes end-to-end behavior and latency harder to predict. [T3][S-0147]
- "Microservices = distributed = automatically modular": distribution adds network calls, consistency, and operations complexity without improving module boundaries — boundaries still have to be designed. [T3][S-0148]
- "The style label determines quality": a style constrains the family of architectures, but quality emerges from how the style is realized; the same style can yield excellent or poor performance, availability, or maintainability. [T2][S-0017]

## References (evidence records)

- S-0017 SWEBOK v4.0 (Software Architecture KA: styles and patterns, representation, quality-attribute design) — T2
- S-0018 CS2023 (Software Engineering KA: architectural design competencies) — T2
- S-0019 ISO/IEC 25010:2023 (product quality characteristics; basis of quality tradeoffs) — T2
- S-0147 Garlan & Shaw 1994, CMU-CS-94-166 — style families: pipes-and-filters, implicit invocation, layered, client-server, peer-to-peer — T3
- S-0148 Lewis & Fowler 2014, Microservices (martinfowler.com) — microservices definition and tradeoffs — T3
- S-0149 Martínez Saucedo et al. 2025, Information and Software Technology 177 — systematic mapping study of monolith-to-microservices migration — T1
