---
id: architecture-design/design-patterns
title: Design Patterns
band: B4
track: architecture-design
tier: T2
bloom_target: apply
prerequisites: [architecture-design/modularity]
related: [architecture-design/architectural-styles]
recommended: []
status: published
schema-version: 1
owner: l1-design-patterns
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0142, S-0143, S-0144]
---

# Design Patterns — validation

## Formative (practice)

### F1 — remember: essential elements
- Q: What are the four essential elements of a design pattern, per the GoF book?
- bloom: remember
- bank: formative
- A: Pattern name, problem (when to apply), solution (structure of participants and responsibilities), and consequences (tradeoffs).
- evidence: [S-0142]
- topic: architecture-design/design-patterns

### F2 — understand: pattern vs template
- Q: Why is a design pattern "not a finished design that transforms directly into code"?
- bloom: understand
- bank: formative
- A: A pattern describes a solution to be adapted to a context: it names participants, responsibilities, and interactions, but the concrete classes, algorithms, and tradeoff decisions must be worked out per situation. Copying the shape without the problem yields the pattern's costs without its benefit.
- evidence: [S-0142]
- topic: architecture-design/design-patterns

### F3 — understand: GoF families
- Q: What three families classify the GoF catalog, and what does each family change or manage?
- bloom: understand
- bank: formative
- A: Creational (object creation), structural (composition of classes/objects), behavioral (interaction and responsibility distribution). Family tells you what kind of design decision the pattern encapsulates.
- evidence: [S-0142]
- topic: architecture-design/design-patterns

### F4 — apply: classify patterns
- Q: Classify each into a GoF family: Factory Method, Adapter, Observer, Decorator, Singleton.
- bloom: apply
- bank: formative
- A: Factory Method and Singleton — creational; Adapter and Decorator — structural; Observer — behavioral.
- evidence: [S-0142]
- topic: architecture-design/design-patterns

## Summative (mastery checkpoint)

### S1 — apply: pattern selection scenario
- Q: A checkout service must support (a) several payment providers, (b) a chain of optional fees/discounts applied to an order, (c) notifying multiple subsystems when a payment succeeds. Propose a pattern per requirement and justify each with its consequences.
- bloom: apply
- bank: summative
- A: (a) Strategy — select a provider algorithm at runtime; consequence: provider families stay independent and replaceable. (b) Decorator — wrap an order to add fees/discounts compositionally; consequence: unlimited combination without subclass explosion, at the cost of many small objects. (c) Observer — subscribers register for payment events; consequence: publishers stay decoupled from subscribers, at the cost of notification fan-out and ordering indeterminism. Each is justified by a real variation point (providers change, fee rules combine, subsystems evolve).
- evidence: [S-0142]
- topic: architecture-design/design-patterns

### S2 — apply: GRASP responsibility assignment
- Q: In a point-of-sale scenario, who should know the sale total (Information Expert), who should route commands from the UI (Controller), and why does assigning these keep coupling low?
- bloom: apply
- bank: summative
- A: The `Sale` object is the Information Expert for the total (it holds the line items). A `ProcessSaleHandler` (or similar) is the Controller: it receives UI events and delegates to domain objects. Assigning responsibilities to the objects that already hold the needed data avoids handing data around, which keeps coupling low and cohesion high.
- evidence: [S-0143]
- topic: architecture-design/design-patterns

### S3 — apply: detect misuse
- Q: A codebase wraps every class constructor in a Singleton "because patterns are good" and adds a Factory for a fixed class with no subclasses. Diagnose and propose the fix.
- bloom: apply
- bank: summative
- A: This is indiscriminate pattern use: the Singleton adds hidden global state and the Factory adds indirection with no variation point (no subclassing, no creation choice). Fix: drop both, construct objects directly; keep the patterns only where a change requirement exists (GoF: do not apply indiscriminately; Martin: patterns serve principles).
- evidence: [S-0142, S-0144]
- topic: architecture-design/design-patterns

## Review (spaced repetition — interleaved with prerequisites)

### R1 — remember: information hiding
- Q: What should a module hide from the rest of the system, and what is the consequence for change?
- bloom: remember
- bank: review
- A: One design decision that is difficult or likely to change (format, algorithm, policy). Because it is invisible outside the interface, a change affects at most that one module.
- evidence: [S-0137]
- topic: architecture-design/modularity

### R2 — understand: cohesion and coupling
- Q: Define coupling and cohesion, and state the target of module design for each.
- bloom: understand
- bank: review
- A: Coupling is interdependence between modules (minimize across boundaries); cohesion is how strongly elements within one module belong together (maximize within). Target: high cohesion, low coupling, evaluated together with complexity.
- evidence: [S-0017]
- topic: architecture-design/modularity

### R3 — apply: dependency inversion recap
- Q: `OrderService` calls `SmtpMailer.send()` directly. How do you invert the dependency, and what do you gain?
- bloom: apply
- bank: review
- A: Introduce a `Mailer` interface; `SmtpMailer` implements it; `OrderService` depends on the interface via injection. Gain: mail transport is replaceable without editing `OrderService` — the policy no longer depends on the detail.
- evidence: [S-0144]
- topic: architecture-design/modularity
