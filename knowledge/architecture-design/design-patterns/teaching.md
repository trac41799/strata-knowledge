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

# Design Patterns — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — given a design scenario with named variation points, select a GoF pattern and justify it through problem, solution, and consequences ([S-0142]).
- **apply** — assign responsibilities to objects using GRASP (Information Expert, Controller, Low Coupling, High Cohesion) in a small scenario ([S-0143]).
- **analyze** — compare two candidate patterns for the same problem and argue which fits the change requirements ([S-0142]).
- **evaluate** — diagnose pattern misuse/overengineering in a code sample and propose removal or replacement ([S-0142], [S-0144]).
- **understand** — explain the difference between patterns (recurring solutions) and principles (general guidelines) ([S-0144]).

## Worked example — pattern selection for a checkout service

Scenario: a checkout service with three requirements — (a) multiple payment providers, (b) chainable fees/discounts, (c) notifications to subsystems on successful payment.

1. **Name the variation points first** (context): providers change (Stripe/PayPal/BNPL); fee & discount rules combine in new ways; the set of subsystems interested in payments grows. Patterns are only justified by such change requirements.
2. **Requirement (a) — Strategy**: problem — the algorithm (provider protocol) varies; solution — `PaymentStrategy` interface, one class per provider, selected by context; consequences — providers stay independent and replaceable, at the cost of a strategy class per provider.
3. **Requirement (b) — Decorator**: problem — fee/discount combinations multiply as subclasses; solution — wrappers around an `Order` adding fees/discounts; consequences — arbitrary composition without subclass explosion, at the cost of many small objects and harder tracing.
4. **Requirement (c) — Observer**: problem — publisher must not know its subscribers; solution — `PaymentEvent` notification with a registry of subscribers; consequences — decoupling at the cost of notification fan-out and ordering indeterminism.
5. **Check principles** (patterns serve principles): each choice keeps `CheckoutService` closed for modification and open for extension (OCP) and lets policy depend on interfaces (DIP) — if a choice fails the principles, it is probably the wrong pattern ([S-0142], [S-0144]).

## Worked example — diagnosing pattern misuse

A codebase wraps every constructor in a Singleton "because patterns are good," plus a Factory for a class with no subclasses. Analysis: no change requirement (no creation choice, no hidden initialization policy), so the Factory adds pure indirection; the Singleton adds hidden global state and couples every consumer to one instance. Both violate the goal the patterns are supposed to serve. Fix: construct directly, keep the Singleton only where a single-instance policy is actually required, and keep the Factory only where creation is a real variation point ([S-0142]).

## Elaboration prompts

- For Strategy vs Template Method on the same problem: what differs, and how does that difference track the change requirement?
- Why does GoF say to examine "the cause of redesign" before choosing a pattern? Pick a pattern and find the redesign it is meant to prevent.
- GRASP's Controller vs Information Expert can conflict: work through a case where routing (Controller) and data ownership (Expert) pull in different directions.
- Where in a framework you use (or a codebase you know) do you recognize Observer, Decorator, or Adapter, and what does recognizing them tell you about how to use the framework?

## Common misconceptions

- "Patterns are templates to copy": they are descriptions with intent and tradeoffs that must be adapted; copying the structure without the problem yields costs without benefit ([S-0142]).
- "More patterns = better design": every pattern adds indirection; indiscriminate application is overengineering, the failure mode GoF explicitly warns against ([S-0142]).
- "Patterns guarantee quality": patterns and SOLID are heuristics applied to real variation points; rigid application makes designs worse ([S-0144]).
- "GRASP patterns are GoF patterns": GRASP is Larman's nine-principle responsibility-assignment aid with a different purpose and catalog ([S-0143]).
- "Patterns and frameworks are interchangeable": frameworks are reusable implementations that embody patterns; the patterns explain how to use the framework ([S-0142]).

## Feynman targets

- Explain to a colleague why "we used the Strategy pattern" is not a design argument — what must accompany the pattern name.
- Explain why a pattern that "works in the book" can be wrong in your codebase, in terms of variation points.
- Explain what a framework is, using the pattern vocabulary (e.g., "this framework's extension points are Template Method hooks").

## Interleaving hooks

- **architecture-design/modularity**: GRASP re-uses Low Coupling and High Cohesion; Adapter, Facade, and Observer are concrete vehicles for the dependency rules and seams from the modularity pack — re-derive when a pattern is justified from the modularity claims.
- **architecture-design/architectural-styles**: styles (layered, MVC, pipes-and-filters) are patterns at architectural scale — SWEBOK lists MVC among the design patterns and techniques; connect pattern families to the styles pack.
- **programming/programming-paradigms**: GoF patterns presuppose OO mechanisms (polymorphism, inheritance); revisit which pattern features survive in non-OO or functional code.
