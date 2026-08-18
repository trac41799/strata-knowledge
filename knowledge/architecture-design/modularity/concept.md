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

# Modularity

## Claims

- Modularity is the decomposition of a system into distinct modules with well-defined interfaces, so each module can be developed, understood, changed, and reused with only limited knowledge of the others; SWEBOK v4's Design KA treats modularization and information hiding as core design concepts. [T2][S-0017]
- The criteria used to decompose a system into modules — not the module boundaries themselves — determine how well the system supports change: Parnas (1972) argued decomposition should follow "difficult design decisions" and "design decisions which are likely to change." [T3][S-0137]
- Information hiding: each module should be designed to hide one design decision from the rest of the system, so that a change to that decision affects at most one module; the module interface should expose only the stable contract the others need. [T3][S-0137]
- Parnas demonstrated the criterion with two decompositions of the same system, a KWIC index producer: one decomposed by processing steps, one by hidden design decisions (storage format, algorithm, ordering rule) — the information-hiding decomposition confined each likely change to a single module. [T3][S-0137]
- A module is characterized by the design decision it hides: interfaces stay free of hidden information, and other modules depend only on the interface, not on the hidden choice. [T3][S-0137]
- The practical benefits Parnas listed for decomposition — parallel development by separate groups with little communication, changeability, independent compilation, and comprehensibility — are what a decomposition is evaluated against; module count is not among the criteria. [T3][S-0137]
- Coupling measures the interdependence between modules — how much one depends on another's internals or behavior; designs aim to minimize coupling across module boundaries. [T2][S-0017]
- Cohesion measures how strongly the elements inside one module belong together — how much they serve a single purpose; designs aim to maximize cohesion within modules. [T2][S-0017]
- SWEBOK's evaluation of design quality uses metrics such as coupling, cohesion, and complexity; these metrics, not module counts, are the quantitative indicators of modularity. [T2][S-0017]
- CS2023's Software Engineering KA includes separation of concerns, information hiding, and coupling and cohesion among the system design principles, and identifies "identifying component boundaries and dependencies" as a core design competency. [T2][S-0018]
- Separation of concerns decomposes a system so that each concern (persistence, presentation, business rules, ...) is addressed in its own module with minimal overlap; it is a design principle distinct from, but supporting, information hiding. [T2][S-0018]
- SWEBOK's basic design concepts — abstraction, encapsulation, modularization, and information hiding — are the vocabulary with which modular designs are described and reviewed. [T2][S-0017]
- SOLID is an acronym (coined by Michael Feathers, around 2004) for five object-oriented design principles set out by Robert C. Martin in 2000: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. [T3][S-0144]
- The Single Responsibility Principle: a module or class should have one reason to change — a responsibility is an axis of change. [T3][S-0144]
- The Open-Closed Principle: modules should be open for extension but closed for modification — behavior is added without editing existing code, typically through polymorphism. [T3][S-0144]
- The Liskov Substitution Principle: subtypes must be substitutable for their base types without altering the correctness of the program. [T3][S-0144]
- The Interface Segregation Principle: clients should not be forced to depend on interfaces they do not use. [T3][S-0144]
- The Dependency Inversion Principle: high-level policy modules should not depend on low-level detail modules; both should depend on abstractions, and abstractions should not depend on details. [T3][S-0144]
- SOLID is practice-level guidance for managing dependencies and change, not a formal law: the principles are widely adopted conventions with known limits and tradeoffs. [T3][S-0144]
- Dependency direction is a design decision: in conventional layering, dependencies point from stable policy toward changeable detail, so that replacing a detail (database, vendor SDK, file format) does not force changes in the policy that uses it. [T3][S-0144]
- DIP "inverts" the naive direction: instead of high-level code calling low-level concrete classes, both depend on an interface, making the detail replaceable without touching the policy. [T3][S-0144]
- Inverting a dependency introduces indirection — an interface plus an injection point — which is the cost paid for the policy's stability; DIP is a recommendation to apply where the variation point is real. [T3][S-0144]
- Conway's law (Conway, 1968): organizations that design systems are constrained to produce designs that are copies of their communication structures. [T3][S-0138]
- Conway presented the law as an empirical constraint observed in the systems his committees designed: the design's structure follows the organization's communication structure, and the constraint is not easily avoided. [T3][S-0138]
- Conway's law is descriptive, not prescriptive: it predicts that coupling between teams shows up as coupling between modules; it does not itself prescribe team structure. [T3][S-0138]
- A seam is a place where you can alter program behavior without editing the code in that place; each seam has an enabling point where the choice between behaviors is made. [T3][S-0139]
- Seams are deliberately introduced at module boundaries: a module whose dependencies all sit behind interfaces has a seam at every dependency, which is what makes the module testable and replaceable in isolation. [T3][S-0139]
- Seams are the mechanism for safe change in legacy code: you open seams to sense and separate behavior before changing it, and you use them to gradually displace behavior. [T3][S-0139]

## Boundaries / common misunderstandings

- "More modules means more modular": module count alone says nothing about modularity; what matters is which design decisions each module hides and whether likely changes stay confined to single modules. [T3][S-0137]
- "Information hiding equals private fields": language visibility is one enforcement mechanism; information hiding is the design decision to keep a module's secrets (format, algorithm, policy) out of its interface — private fields enforce it, they do not define it. [T3][S-0137]
- "SOLID is law": the SOLID principles are heuristics; they can conflict and are context-dependent, and applying them rigidly can over-engineer a design. [T3][S-0144]
- "Conway's law tells you to reorganize teams": the law is a descriptive claim about a constraint; using it prescriptively is an organizational strategy beyond what the 1968 paper states. [T3][S-0138]
- "Less coupling is always better": coupling is evaluated together with cohesion and complexity, and decoupling always costs indirection, so the target is a balance, not a minimum. [T2][S-0017]
- "A seam is a testing hack": seams are the general mechanism for changing behavior through a boundary without editing in place; tests are one consumer, but any behavior substitution (plugins, dependency injection, configuration) uses seams. [T3][S-0139]

## References (evidence records)

- S-0017 SWEBOK v4.0 (Design KA: design concepts, patterns and techniques, design-quality metrics) — T2
- S-0018 CS2023 (Software Engineering KA: design principles, component boundaries) — T2
- S-0137 Parnas 1972, CACM — decomposition criteria and information hiding — T3
- S-0138 Conway 1968, Datamation — Conway's law — T3
- S-0139 Feathers 2004, Working Effectively with Legacy Code — seams — T3
- S-0144 Martin 2000, Design Principles and Design Patterns — SOLID, DIP — T3
