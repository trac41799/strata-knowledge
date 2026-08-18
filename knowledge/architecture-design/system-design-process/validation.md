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

# System Design Process — validation

## Formative (practice)

### F1 — remember: 42010 vocabulary
- Q: In ISO/IEC/IEEE 42010, what is the relationship between a viewpoint, a view, and a concern?
- bloom: remember
- bank: formative
- A: A viewpoint specifies the conventions for constructing, using, and analyzing views to address a set of related concerns; a view is a work product expressing the architecture from the perspective of the system concerns addressed by that viewpoint.
- evidence: [S-0021]
- topic: architecture-design/system-design-process

### F2 — understand: why the loop
- Q: Why is requirements → architecture → design a loop rather than a one-way flow?
- bloom: understand
- bank: formative
- A: Elaborating the architecture exposes missing or conflicting requirements, and detailed design or construction reveals constraints that force rework of earlier decisions; the lifecycle processes are applied iteratively, with feedback from each activity revising the earlier ones.
- evidence: [S-0017, S-0020]
- topic: architecture-design/system-design-process

### F3 — understand: why multiple views
- Q: Why does 42010 require multiple views rather than one all-purpose architecture diagram?
- bloom: understand
- bank: formative
- A: Different stakeholders have different concerns (end users, developers, operators, acquirers), and no single view can express all of them; a set of viewpoints plus correspondences between their views keeps each view focused and the description consistent.
- evidence: [S-0021]
- topic: architecture-design/system-design-process

### F4 — apply: plan an architecture description
- Q: A team must document the architecture of a payroll system. Name the stakeholders and their concerns, and pick two viewpoints whose views you would produce.
- bloom: apply
- bank: formative
- A: Stakeholders: payroll staff (functional workflow, response time), finance/auditors (correctness, compliance evidence), IT operators (availability, capacity at month-end), developers (modifiability of tax rules). Views: e.g., a functional/logical view (components, data flow) for users and developers, and a deployment view (nodes, state, capacity) for operators; each defined by a viewpoint that states its conventions.
- evidence: [S-0021]
- topic: architecture-design/system-design-process

## Summative (mastery checkpoint)

### S1 — analyze: choose an architecture under constraints
- Q: Requirements: 50k monthly users growing 5x/year, 99.95% availability, four-developer team with no operations automation, six-month deadline, legacy relational database. Which architecture and style would you propose, which quality attributes are in tension, and what would you evaluate before committing?
- bloom: analyze
- bank: summative
- A: A layered modular monolith on managed infrastructure (client-server toward users), with the database behind a module boundary: it meets the deadline and team size, keeps ops simple, and the growth path is to split along module boundaries later. Tension: modifiability and speed to market vs the independent scalability and fault isolation of microservices — which this team cannot operate. Before committing, evaluate capacity (month-end batch, 5x growth), availability, and modifiability as scenarios (ATAM-style), and confirm the legacy DB can be isolated behind an interface.
- evidence: [S-0017, S-0019, S-0152]
- topic: architecture-design/system-design-process

### S2 — analyze: find tradeoffs in an architecture description
- Q: An order service keeps state in a local database and calls payments over HTTP; a Kafka event bus publishes OrderPlaced to an inventory service; the deployment is a single region. Given goals of performance, modifiability, and availability, identify the sensitivity points, tradeoff points, and risks in this architecture.
- bloom: analyze
- bank: summative
- A: Sensitivity points: the HTTP payment call (its latency and timeout dominate order latency); the single-region deployment (drives availability); the local order database (defines the consistency and replication story). Tradeoff point: event-driven order fulfillment buys modifiability (new consumers subscribe) at the cost of end-to-end latency and delivery guarantees. Risks: payment provider latency spikes violate the latency goal; a region outage violates availability; a schema change to the order DB couples the team that owns it to every consumer.
- evidence: [S-0152, S-0021]
- topic: architecture-design/system-design-process

### S3 — analyze: capacity as an architectural decision
- Q: Why must capacity be analyzed during architecture definition rather than treated as a tuning problem? Name the structural facts that determine scaling behavior, and the standards vocabulary for stating the requirement.
- bloom: analyze
- bank: summative
- A: Scaling follows from structure — where state lives (stateless services can replicate; local DBs cannot), what can be partitioned or replicated, where queues and bottlenecks sit — so an architecture that cannot scale cannot be tuned into one that can. ISO 25010 names capacity as a performance-efficiency subcharacteristic (alongside time behaviour and resource utilization), and ISO 12207's architecture definition process assesses candidate architectures against such requirements before selecting one.
- evidence: [S-0019, S-0020]
- topic: architecture-design/system-design-process

## Review (spaced repetition — interleaved with prerequisites)

### R1 — understand: style selection recap
- Q: Why does choosing an architectural style constrain the design space, and what are the three kinds of constraints a style prescribes?
- bloom: understand
- bank: review
- A: A style defines a family of architectures, so choosing it commits the team to its constraints. The constraints are the component/connector vocabulary, topological constraints, and semantic constraints (e.g., filters cannot share state in pipe-and-filter).
- evidence: [S-0147]
- topic: architecture-design/architectural-styles

### R2 — apply: requirements quality recap
- Q: A capacity requirement ("the system must handle 5,000 concurrent users") is a non-functional requirement — why must it be stated as a verifiable requirement, and which ISO 25010 characteristic names it?
- bloom: apply
- bank: review
- A: Non-functional (quality) requirements are real requirements: unverifiable NFRs cannot drive or validate the architecture. The characteristic is performance efficiency, with capacity as a subcharacteristic; a verifiable statement fixes the resource, the scenario, and the measurement.
- evidence: [S-0073, S-0019]
- topic: engineering-process/requirements-engineering

### R3 — remember: rationale in architecture
- Q: In Perry & Wolf's model, what does the rationale component capture, and why does that make design decisions part of the architecture itself?
- bloom: remember
- bank: review
- A: Rationale captures the motivation for the choice of architectural style, elements, and form — the design decisions and their justification are first-class parts of the architecture, so future changes can be judged against why earlier ones were made.
- evidence: [S-0154]
- topic: architecture-design/system-design-process
