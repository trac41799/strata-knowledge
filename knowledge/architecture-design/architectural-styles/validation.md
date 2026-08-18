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

# Architectural Styles — validation

## Formative (practice)

### F1 — remember: style anatomy
- Q: Per Garlan & Shaw, what three kinds of constraints does an architectural style prescribe for its family of architectures?
- bloom: remember
- bank: formative
- A: A vocabulary of component and connector types (e.g., filters and pipes), topological constraints (e.g., the graph must be acyclic), and semantic constraints (e.g., filters cannot share state).
- evidence: [S-0147]
- topic: architecture-design/architectural-styles

### F2 — understand: implicit invocation
- Q: Why does the event-driven (implicit invocation) style decouple a producer from its consumers, and what does the decoupling cost?
- bloom: understand
- bank: formative
- A: A producer announces events without naming consumers; components register handlers that are invoked at runtime, so producers and consumers evolve independently. Cost: runtime indirection, and end-to-end behavior and latency become harder to predict and debug.
- evidence: [S-0147]
- topic: architecture-design/architectural-styles

### F3 — understand: styles and quality attributes
- Q: Why does choosing a style trade quality attributes against each other, and what vocabulary does ISO/IEC 25010 provide for stating the trade?
- bloom: understand
- bank: formative
- A: A style realizes some qualities well and others poorly (e.g., loose coupling aids modifiability but adds indirection that hurts predictable latency). ISO 25010 names nine product quality characteristics (functional suitability, performance efficiency, compatibility, interaction capability, security, safety, reliability, maintainability, flexibility) for stating what is traded.
- evidence: [S-0019]
- topic: architecture-design/architectural-styles

### F4 — apply: classify into a style
- Q: A system ingests a continuous telemetry stream, transforms it (parse, filter, aggregate), and writes results to several sinks; new processing steps must be added without stopping the pipeline. Which style fits, and which of its constraints make it fit?
- bloom: apply
- bank: formative
- A: Pipe-and-filter: filters are incremental stream transformers connected by pipes, and filters do not share state — so a new filter (parse/aggregate) can be inserted into the graph without touching the others. The no-shared-state constraint is what keeps steps independent.
- evidence: [S-0147]
- topic: architecture-design/architectural-styles

## Summative (mastery checkpoint)

### S1 — apply: style selection trace
- Q: An online bookstore: a read-mostly catalog, checkout with two payment providers, and recommendations that should react to orders. Three small teams, an existing relational database, and a three-month deadline — no dedicated operations automation. Which decomposition would you choose, and what quality tradeoff are you accepting?
- bloom: apply
- bank: summative
- A: A modular monolith first: one deployable unit with internally modular boundaries (catalog, checkout, recommendations), payments behind an interface, and event-driven internal notifications for recommendations. Accepted tradeoff: giving up independent deployability and per-service scaling for low operational complexity, in-process consistency, and a fast release — microservices (own processes, distributed data) are not justified for this team size and ops maturity.
- evidence: [S-0148, S-0149]
- topic: architecture-design/architectural-styles

### S2 — apply: classify subsystems
- Q: Classify each subsystem into a style: (a) a Unix-style pipeline that greps, sorts, and uniqs a log stream; (b) a mobile app calling a REST backend that owns the shared database; (c) services that publish OrderPlaced events and handlers that react to them.
- bloom: apply
- bank: summative
- A: (a) pipe-and-filter (stream transformers, no shared state); (b) client-server (servers provide services to clients over a protocol; shared, centralized data); (c) event-driven / implicit invocation (components register handlers for announced events; producers do not name consumers).
- evidence: [S-0147]
- topic: architecture-design/architectural-styles

### S3 — analyze: event-driven vs client-server for order routing
- Q: For a real-time trading platform's order-routing path, compare event-driven and client-server styles: which quality attributes favor each, and where exactly is the tradeoff?
- bloom: analyze
- bank: summative
- A: Event-driven favors modifiability and dynamic integration (new handlers join without changing producers; routing reacts to market events asynchronously) but end-to-end latency and behavior become less predictable and harder to debug. Client-server favors predictable request/response latency and central control over the order book, but the central server is a bottleneck and single point of failure. The tradeoff is performance efficiency and predictability vs modifiability and decoupling — stated per ISO 25010 characteristics.
- evidence: [S-0147, S-0019]
- topic: architecture-design/architectural-styles

## Review (spaced repetition — interleaved with prerequisites)

### R1 — remember: coupling and cohesion
- Q: Define coupling and cohesion and state the design target for each, per SWEBOK.
- bloom: remember
- bank: review
- A: Coupling is the interdependence between modules (minimize across boundaries); cohesion is how strongly the elements inside one module belong together (maximize within modules). Both are evaluated together with complexity.
- evidence: [S-0017]
- topic: architecture-design/modularity

### R2 — apply: find a seam
- Q: A legacy InvoiceProcessor calls a hardcoded TaxCalculator that reads a config file and is impossible to test. Where is the seam, and how do you introduce it?
- bloom: apply
- bank: review
- A: The call site is the enabling point: introduce a TaxCalculator interface, have the existing class implement it, and let InvoiceProcessor receive the calculator — tests then supply a fake without editing the processor's logic.
- evidence: [S-0139]
- topic: architecture-design/modularity

### R3 — apply: microservices claims audit
- Q: A colleague says "we moved to microservices, so we are scalable by definition." What is wrong with the inference, and what does the systematic mapping study say about the evidence?
- bloom: apply
- bank: review
- A: Microservices is a structural style, not a performance guarantee; scalability follows from how the style is realized (state placement, replication, capacity evaluation). The mapping study found scalability and maintenance are the main stated drivers of migration but few studies actually assess whether the benefits materialize — so the claim outruns the evidence.
- evidence: [S-0149, S-0148]
- topic: architecture-design/architectural-styles
