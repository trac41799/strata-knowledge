---
id: architecture-design/modularity
title: Modularity
band: B4
track: architecture-design
tier: T2
bloom_target: apply
prerequisites: [programming/programming-paradigms]
related: [architecture-design/design-patterns, architecture-design/architectural-styles]
recommended: [architecture-design/design-patterns]
status: published
schema-version: 1
owner: l1-modularity
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0018, S-0137, S-0138, S-0139, S-0144]
---

# Modularity — validation

## Formative (practice)

### F1 — remember: information hiding
- Q: Per Parnas (1972), what should a module hide from the rest of the system, and why does that make change safer?
- bloom: remember
- bank: formative
- A: A module should hide one design decision (format, algorithm, policy) that is difficult or likely to change. Because the decision is invisible outside the module's interface, a change to it affects at most that one module.
- evidence: [S-0137]
- topic: architecture-design/modularity

### F2 — understand: decomposition criteria
- Q: In Parnas's KWIC example, why did two decompositions of the same system differ so much in changeability?
- bloom: understand
- bank: formative
- A: The processing-step decomposition spread each design decision (storage format, algorithm, ordering rule) across several modules, so a change touched many modules. The information-hiding decomposition assigned each decision to exactly one module, so changes stayed confined.
- evidence: [S-0137]
- topic: architecture-design/modularity

### F3 — understand: cohesion vs coupling
- Q: Define coupling and cohesion and state the design target for each.
- bloom: understand
- bank: formative
- A: Coupling is the interdependence between modules (minimize across boundaries); cohesion is how strongly the elements inside one module belong together (maximize within modules). The target is high cohesion and low coupling, evaluated together with complexity.
- evidence: [S-0017]
- topic: architecture-design/modularity

### F4 — apply: classify a design
- Q: A `ReportPrinter` module reads customer data directly from the database, formats it, and emails it. Identify the cohesion and coupling problems and sketch a decomposition.
- bloom: apply
- bank: formative
- A: `ReportPrinter` has low cohesion (data access, formatting, and delivery are three concerns in one module) and high coupling (it depends on the database schema and the mail server internals). Decompose by design decision: a `CustomerSource` module (hides storage), a `ReportFormatter` (hides format), and a `DeliveryChannel` (hides transport), each behind an interface.
- evidence: [S-0017, S-0137]
- topic: architecture-design/modularity

## Summative (mastery checkpoint)

### S1 — apply: Parnas-style decomposition
- Q: A checkout system computes prices (discount rules change quarterly), charges customers (two payment providers), and renders receipts (HTML now, PDF planned). Decompose it into modules that hide likely changes, and justify each boundary.
- bloom: apply
- bank: summative
- A: Modules: `DiscountPolicy` (hides the rules — the quarterly change), `PaymentGateway` interface with one adapter per provider (hides provider protocols — new providers plug in), `ReceiptRenderer` interface with HTML/PDF implementations (hides output formats). Each likely change is confined to one module; interfaces expose only stable contracts (e.g., `total()`, `charge(amount)`, `render(receipt)`).
- evidence: [S-0137, S-0144]
- topic: architecture-design/modularity

### S2 — apply: dependency inversion
- Q: `BillingService` currently calls `PayPalClient.charge()` directly. Redraw the dependencies so `BillingService` does not depend on PayPal, and name what is gained and what is paid.
- bloom: apply
- bank: summative
- A: Introduce `PaymentGateway` with `charge(amount)`; `PayPalClient` implements it; `BillingService` depends only on `PaymentGateway` (supplied via injection). Gain: provider is replaceable without touching `BillingService` (DIP, OCP). Cost: one interface and an injection point — indirection — which is justified by the real variation point (providers change).
- evidence: [S-0144]
- topic: architecture-design/modularity

### S3 — apply: find and use a seam
- Q: A legacy `InvoiceProcessor` calls a hardcoded `TaxCalculator.compute(amount)` that is impossible to test because it reads a config file. Where is the seam, and how do you introduce it?
- bloom: apply
- bank: summative
- A: The call site is the seam's enabling point: introduce a `TaxCalculator` interface, have the existing class implement it, and let `InvoiceProcessor` receive the calculator (constructor or setter). Tests now supply a fake calculator — behavior is altered at the enabling point without editing `InvoiceProcessor`'s logic.
- evidence: [S-0139]
- topic: architecture-design/modularity

## Review (spaced repetition — interleaved with prerequisites)

### R1 — remember: paradigm split
- Q: What distinguishes imperative from declarative programming, and why is encapsulation "a modularity mechanism, not a guarantee of good design"?
- bloom: remember
- bank: review
- A: Imperative describes how (sequenced statements mutating state); declarative describes what (desired result). Encapsulation hides state behind methods, which supports modularity, but hiding internals says nothing about whether the design's boundaries are the right ones.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### R2 — understand: modularity across paradigms
- Q: Why is object-oriented programming only one vehicle for encapsulation and modularity, and what does that imply for module design in a multi-paradigm codebase?
- bloom: understand
- bank: review
- A: Module systems (Rust, OCaml) provide encapsulation without classes, and languages like Python/JS/C++ are multi-paradigm. Modularity is a property of the code's structure (module systems, interfaces), not of the language label, so module boundaries must be designed explicitly in any paradigm.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### R3 — apply: SOLID recap
- Q: A `UserService` validates input, talks to the DB, sends emails, and logs. Which SOLID principle does it violate, and what is the one-line fix?
- bloom: apply
- bank: review
- A: Single Responsibility: it has several reasons to change (validation rules, schema, email format, log format). Fix: split into focused modules/services, each with one axis of change.
- evidence: [S-0144]
- topic: architecture-design/modularity
