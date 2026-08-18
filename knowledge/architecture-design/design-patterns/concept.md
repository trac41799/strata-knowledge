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

# Design Patterns

## Claims

- A design pattern is a named, reusable solution to a recurring design problem in a context: it describes the problem, the structure of the solution (elements, relationships, responsibilities), and the consequences of applying it. [T3][S-0142]
- The four essential elements of a pattern (GoF): the pattern name (a vocabulary term), the problem (when to apply it), the solution (structure of participants and responsibilities), and the consequences (the tradeoffs of the design). [T3][S-0142]
- A pattern is a description of a solution to be adapted, not a finished design that transforms directly into code: applying a pattern always requires working out the specifics of the situation. [T3][S-0142]
- SWEBOK v4's Design KA treats design patterns and techniques — including the GoF catalog, MVC, and SOLID-based design principles — as core design knowledge. [T2][S-0017]
- The GoF catalog documents 23 object-oriented patterns, classified by purpose into three families: creational (object creation), structural (class/object composition), and behavioral (interaction and responsibility distribution). [T3][S-0142]
- The creational family (5 patterns: Abstract Factory, Builder, Factory Method, Prototype, Singleton) decouples a system from how its objects are created and composed. [T3][S-0142]
- The structural family (7 patterns: Adapter, Composite, Decorator, Facade, Proxy, ...) composes classes and objects into larger structures while keeping those structures flexible. [T3][S-0142]
- The behavioral family (11 patterns: Observer, Strategy, Template Method, Command, Iterator, ...) assigns responsibilities and manages communication between objects. [T3][S-0142]
- The GoF catalog targets the object-oriented paradigm: patterns are described in terms of classes, objects, inheritance, and polymorphism, and presuppose the OO mechanisms that make them expressible. [T3][S-0142]
- Selecting a pattern requires matching problem context and consequences, not the pattern name: GoF's selection guidance is to consider how patterns solve design problems, examine the causes of redesign, and study each candidate's consequences. [T3][S-0142]
- "Design patterns should not be applied indiscriminately": patterns buy flexibility and variability by adding indirection, which can complicate a design and cost performance — they are justified where the variation point exists. [T3][S-0142]
- A pattern's consequences are part of the pattern: choosing a pattern means accepting its tradeoffs (e.g., Observer's notification cost, Singleton's global state), and those tradeoffs are the selection criteria. [T3][S-0142]
- Design principles are general guidelines; patterns are concrete recurring solutions: in Martin's principles-first view, patterns serve principles such as SOLID, which constrain when and how a pattern is applied. [T3][S-0144]
- Indiscriminate pattern use is a recognized failure mode (overengineering): flexibility bought by indirection with no corresponding change requirement makes a design harder to understand and modify. [T3][S-0142]
- GRASP (General Responsibility Assignment Software Patterns, Larman) is a learning aid of nine patterns/principles for assigning responsibilities to objects: Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Pure Fabrication, Indirection, Protected Variations. [T3][S-0143]
- GRASP complements rather than replaces the GoF catalog: GoF documents solution structures; GRASP answers which object should hold which responsibility. [T3][S-0143]
- GRASP carries modularity into object design: Low Coupling and High Cohesion appear as responsibility-assignment principles, connecting module-level design to object-level design. [T3][S-0143]
- Patterns provide a shared vocabulary: naming a solution (Observer, Strategy, Facade) lets designers communicate structure and tradeoffs at a higher level than code. [T3][S-0142]
- Patterns and frameworks are different reuse mechanisms: a framework is a set of cooperating classes embodying a reusable design, and knowing the patterns behind a framework is how you use and extend it. [T3][S-0142]
- The GoF catalog is a starting vocabulary, not the whole discipline: adjacent catalogs (e.g., GRASP for responsibility assignment) cover problems the 23 patterns do not address. [T3][S-0143]

## Boundaries / common misunderstandings

- "Patterns are templates to copy": a pattern is a description with intent and tradeoffs that must be adapted; mechanically copying a pattern's structure without its problem yields the costs without the benefit. [T3][S-0142]
- "More patterns means better design": every pattern adds indirection; pattern use is justified by matching variation points and change requirements, and over-application is overengineering. [T3][S-0142]
- "The pattern name decides the design": choosing by name or symptom (e.g., "I need a Singleton") skips the context and consequence check that GoF's selection guidance requires. [T3][S-0142]
- "Patterns guarantee quality": patterns and principles are heuristics; quality comes from applying them to real variation points, and rigid application (pattern or SOLID) can make designs worse. [T3][S-0144]
- "GRASP patterns are GoF patterns": GRASP is Larman's nine-principle responsibility-assignment learning aid — a different catalog with a different purpose than GoF's 23 patterns. [T3][S-0143]
- "Patterns solve the same problem as frameworks": patterns are design descriptions; frameworks are reusable implementations — a framework may embody several patterns, and the patterns explain how to use it. [T3][S-0142]

## References (evidence records)

- S-0017 SWEBOK v4.0 (Design KA: design patterns and techniques) — T2
- S-0142 Gamma, Helm, Johnson & Vlissides 1994, Design Patterns (GoF) — T3
- S-0143 Larman 2002, Applying UML and Patterns (GRASP) — T3
- S-0144 Martin 2000, Design Principles and Design Patterns — T3
