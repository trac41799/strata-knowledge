---
id: programming/programming-paradigms
title: Programming Paradigms
band: B3
track: programming
tier: T1
bloom_target: apply
prerequisites: [cs-foundations/logic-and-proof]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-programming-paradigms
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0098, S-0099, S-0100, S-0018]
---

# Programming Paradigms — validation

## Formative (practice)

### F1 — remember: paradigm families
- Q: Name the two principal declarative programming families, and state the imperative/declarative contrast in one sentence each.
- bloom: remember
- bank: formative
- A: Functional and logic programming. Imperative programs say how: sequences of statements that mutate state. Declarative programs say what: the desired result, leaving the mechanism to the language/runtime.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### F2 — understand: purity and mutation
- Q: A colleague says "functional programming means the program never changes any state." Why is that wrong, and what does purity actually require?
- bloom: understand
- bank: formative
- A: Purity means functions have no observable side effects — output depends only on inputs — not that state never changes. Pure-by-default languages confine effects explicitly (monads/effect systems); the program as a whole still performs I/O and mutation, just in a disciplined, visible way.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### F3 — apply: translate imperative to functional
- Q: The imperative loop below computes the sum of squares of the even numbers in a list. Write an equivalent expression using higher-order functions and say what makes it pure. Loop: total = 0; for x in xs: if even(x): total += x*x.
- bloom: apply
- bank: formative
- A: xs.filter(even).map(x -> x*x).fold(0, (+)) — or a fold that combines filter+map. It is pure: no variable is mutated, each step returns a new value, and the same input always yields the same output.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### F4 — apply: classify snippets
- Q: Classify each style: (a) a C loop accumulating into a variable; (b) a class hierarchy with virtual methods; (c) a Prolog rule base queried for answers; (d) a map/filter/reduce pipeline. Name the paradigm family (and subfamily) of each.
- bloom: apply
- bank: formative
- A: (a) imperative (procedural); (b) object-oriented with subtype polymorphism; (c) declarative logic programming (deduction via unification/resolution); (d) declarative functional programming (higher-order functions over data). (a) is "how"; (c) and (d) are "what".
- evidence: [S-0098, S-0100]
- topic: programming/programming-paradigms

## Summative (mastery checkpoint)

### S1 — apply: redesign with immutability
- Q: An imperative function removes duplicates from a list by mutating a buffer in a loop. Produce a pure functional version and state which properties it gains (and what it gives up).
- bloom: apply
- bank: summative
- A: Use a fold accumulating the deduplicated list (e.g., xs.foldLeft(List.empty)((acc, x) => if (acc.contains(x)) acc else x :: acc).reverse). Gains: purity/referential transparency — trivially testable in isolation, no aliasing hazards, safe to parallelize. Gives up: in-place updates and their peak-memory/performance profile for very large lists — a pure version allocates instead of mutating.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### S2 — analyze: paradigm fit
- Q: You must build (i) a rule engine evaluating thousands of business rules, (ii) a GUI framework plugin layer, (iii) a high-throughput data pipeline. For each, argue which paradigm family fits best and name the tradeoff that decides it.
- bloom: analyze
- bank: summative
- A: (i) logic/rule-based declarative — rules map naturally to facts+rules with search; tradeoff: performance opacity and needing to control search order. (ii) OO — plugin layers are polymorphism-heavy (interfaces, virtual dispatch); tradeoff: coupling if implementation inheritance is overused. (iii) functional — pipelines of pure transformations map to map/filter/fold and parallelize safely; tradeoff: allocation overhead and strictness control. Lesson: fit follows the structure of the problem.
- evidence: [S-0098, S-0100]
- topic: programming/programming-paradigms

### S3 — evaluate: the "X is better" claim
- Q: A developer claims: "Functional languages are objectively better — they produce fewer bugs, proven by data." Evaluate this claim against the Ray et al. evidence.
- bloom: evaluate
- bank: summative
- A: Partial-to-weak support. Ray et al. (728 projects, 63M SLOC, 1.5M commits, 17 languages) found language design has a significant but modest association with code quality; after controlling for size, age, team, and domain, typing/paradigm features explain little of the defect variance. The design is observational (selection effects), so causality is not established, and effects are small relative to other factors. Verdict: paradigm choice matters, but "objectively better, proven" overstates the evidence.
- evidence: [S-0099]
- topic: programming/programming-paradigms

### S4 — understand: encapsulation without classes
- Q: Explain how a module system provides encapsulation without classes, and name two properties that OOP's inheritance adds beyond what modules alone provide.
- bloom: understand
- bank: summative
- A: A module hides internals behind an exported interface — callers cannot touch private items — the same information-hiding encapsulation OOP offers. Inheritance additionally provides subtyping (a derived object usable where the base is expected) and implementation reuse; neither is required for encapsulation.
- evidence: [S-0098]
- topic: programming/programming-paradigms

## Review (spaced repetition — interleaved with prerequisites)

### R1 — remember (logic-and-proof): what logic programming builds on
- Q: Logic programming executes by deduction from facts and rules. State what unification and resolution provide in that execution, and why they count as "logic" rather than "control flow".
- bloom: remember
- bank: review
- A: Unification matches terms and binds variables; resolution derives goals from clauses. Together they implement logical inference — execution follows from the logical content, while control (search order) is a separate, explicit concern. That is the premise of declarative logic programming.
- evidence: [S-0100]
- topic: cs-foundations/logic-and-proof

### R2 — understand (programming-paradigms): the paradigm continuum
- Q: Why is "imperative vs declarative" a continuum rather than a partition, and what makes a language "multi-paradigm"?
- bloom: understand
- bank: review
- A: Most languages mix styles: an imperative language can be used in a functional style and vice versa, and even one codebase ranges from explicit loops to expression pipelines. Multi-paradigm means the language supports several families (e.g., C++: procedural + OO + generic + functional idioms), so style is a discipline choice, not a language property.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### R3 — apply (programming-paradigms): paradigm-driven design choices
- Q: A component must (a) allow many interchangeable implementations and (b) forbid callers from mutating internal state. Which paradigm mechanism serves each requirement, and what does each cost?
- bloom: apply
- bank: review
- A: (a) subtype polymorphism (interfaces/virtual dispatch) or generics — cost: indirection or monomorphization; (b) encapsulation (private state + accessors) or immutability (pure data + pure transforms) — cost: protected mutation paths/boilerplate, or allocation instead of in-place change. Both are combinable in multi-paradigm practice.
- evidence: [S-0098]
- topic: programming/programming-paradigms
