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

# Programming Paradigms

## Claims

### Classification: imperative vs declarative

- A programming paradigm is a family of styles for organizing computation; the most general split is imperative ("how": sequenced statements that change state) versus declarative ("what": describing the desired result), and the split is a stylistic continuum, not a formal taxonomy. [T3][S-0098]
- Imperative programming computes by executing statements that mutate state — assignment, loops, procedure calls — and is the dominant style of C, Pascal, and most systems languages. [T3][S-0098]
- Declarative programming expresses the desired result and leaves the mechanism to the language/runtime; functional and logic programming are its two principal families. [T3][S-0098]
- CS2023 treats paradigms as core curriculum: its renamed Foundations of Programming Languages (FPL) knowledge area is focused on programming-language paradigms and concepts, and includes both functional and logic programming as core topics. [T2][S-0018]

### Object-oriented programming

- Object-oriented programming organizes state and behavior into objects — encapsulated state accessed through methods — and is characterized by encapsulation, inheritance (or delegation), and polymorphism. [T3][S-0098]
- Encapsulation hides an object's internal state behind its interface, restricting mutation to its methods; it is a modularity mechanism, not a guarantee of good design. [T3][S-0098]
- Inheritance supports code reuse and subtyping, but implementation inheritance couples subclasses to parent internals — the well-known source of breakage when the parent class changes (fragile base class). [T3][S-0098]
- Polymorphism lets one interface serve many implementations: subtype polymorphism (inheritance + virtual dispatch), parametric polymorphism (generics), and ad-hoc polymorphism (overloading). [T3][S-0098]
- Encapsulation and modularity do not require classes: module systems (Rust, OCaml) provide them without inheritance, so OOP is one vehicle for these properties, not the only one. [T3][S-0098]

### Functional programming

- Functional programming computes by evaluating functions, emphasizing pure functions — output depends only on input, with no observable side effects — and immutable data. [T3][S-0098]
- Purity yields referential transparency: an expression can be replaced by its value without changing program behavior, enabling equational reasoning, easier testing, and safe parallelization. [T3][S-0098]
- Higher-order functions — functions that take or return functions, such as map/filter/fold — abstract common iteration patterns out of hand-written loops. [T3][S-0098]
- Pure-by-default languages make effects explicit and disciplined (monads, effect systems) rather than impossible; evaluation strategy (strict vs lazy) is a separate axis with real performance consequences. [T3][S-0098]

### Logic programming

- Logic programming computes by deduction: a program is a set of facts and rules (Horn clauses), and execution is goal-directed inference using unification and resolution, as embodied by Prolog. [T3][S-0100]
- Prolog predicates are relations, not functions: they can be queried in several directions, and nondeterminism (backtracking over alternatives) is a defining mechanism. [T3][S-0100]
- Logic programming fits symbolic/declarative domains — search, parsing, rule and constraint systems — and its main costs are opaque performance and the need to control search order explicitly. [T3][S-0100]

### Paradigm tradeoffs & empirical evidence

- Paradigms are not ordered by expressiveness: imperative, OO, functional, and logic styles can express the same computations, and mainstream languages (C++, Python, JavaScript, Scala, Rust) are multi-paradigm in practice. [T3][S-0098]
- Large-N observational evidence (728 GitHub projects, 63M SLOC, 1.5M commits, 17 languages) found language choice has a significant but modest association with code quality: after controlling for project size, age, team, and domain, typing and paradigm features explain only a small share of defect differences. [T1][S-0099]
- The same evidence does not support "paradigm X is objectively better" claims: effect sizes are small and the design is observational (selection effects), so paradigm choice is a tradeoff of fit, ecosystem, and team skill, not a universal ranking. [T1][S-0099]

### Multi-paradigm practice

- In multi-paradigm languages, style is a matter of discipline: the same language can be used in OO, functional, or imperative style, so "which paradigm a codebase uses" is a decision the team makes. [T3][S-0098]
- Practical paradigm adoption follows fit — functional idioms for data pipelines and concurrency, OO for UI frameworks, logic for rule engines — making multi-paradigm fluency a practical skill. [T3][S-0098]

## Boundaries / common misunderstandings

- "Functional programming means no mutation anywhere": purity means mutation and effects are explicit and confined (e.g., Haskell's IO/ST), not that state does not exist. [T3][S-0098]
- "OOP equals classes": prototype-based OO (JavaScript, Self) exists, and encapsulation exists without classes via modules. [T3][S-0098]
- "Declarative means the language does all the work": the programmer still controls the algorithm and its complexity — Prolog search order and FP evaluation strategy shape performance. [T3][S-0098]
- "Python/JavaScript/Rust are functional languages": they support functional idioms but are not pure; purity is a property of code, not a language label. [T3][S-0098]
- "The better paradigm wins by data": the strongest large-N evidence shows language/paradigm effects on quality are modest relative to other factors such as team, domain, and process. [T1][S-0099]

## References (evidence records)

- S-0018 — CS2023, FPL knowledge area (T2)
- S-0098 — Scott, Programming Language Pragmatics, 4th ed. (T3)
- S-0099 — Ray et al., FSE 2014 / CACM 2017 (T1)
- S-0100 — Clocksin & Mellish, Programming in Prolog, 5th ed. (T3)
