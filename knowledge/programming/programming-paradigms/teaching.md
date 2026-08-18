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

# Programming Paradigms — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember** — name the principal paradigm families and their defining mechanisms (state mutation; objects; pure functions/higher-order functions; facts+rules with unification/resolution) ([S-0098], [S-0100]).
- **understand** — explain why purity means confined, explicit effects rather than "no state", and why encapsulation does not require classes ([S-0098]).
- **apply** — translate an imperative loop into a pure functional expression using map/filter/fold, and classify code snippets by paradigm ([S-0098]).
- **analyze** — argue paradigm fit for a given problem shape and name the concrete tradeoff that decides it ([S-0098], [S-0100]).
- **evaluate** — assess "paradigm X is objectively better" claims against the large-N observational evidence ([S-0099]).

## Worked example 1 — translating imperative to functional

Task: compute the sum of squares of the even numbers in a list.

**Imperative (C-like):**

```c
int total = 0;
for (int i = 0; i < n; i++) {
    if (xs[i] % 2 == 0)
        total += xs[i] * xs[i];
}
```

**Functional (expression, no mutation):**

```text
xs.filter(even).map(x -> x * x).fold(0, (+))
```

**Step-by-step.** (1) `filter(even)` selects the elements that pass the predicate — a new list, the original untouched. (2) `map(x -> x*x)` transforms each element — again a new list. (3) `fold(0, (+))` reduces the list to a single value, threading an accumulator without ever mutating a variable.

**What changed and why it matters.** The imperative version mutates `total` (state changes make behavior depend on execution order). The functional version is an expression: every intermediate is a fresh value, so evaluation order does not matter, the same input always yields the same output (referential transparency), and the three steps can be reasoned about and tested independently. The cost: allocation instead of in-place accumulation — the classic purity-vs-peak-performance tradeoff ([S-0098]).

## Worked example 2 — one task, four paradigms

Task: compute the average of the positive numbers in a list.

| Paradigm | Shape | Mechanism used |
|---|---|---|
| Imperative | `for` loop with `sum`/`count` accumulators | state mutation, sequence |
| OO | object with `add(..)` and `average()` methods | encapsulated state, message passing |
| Functional | `let (s,c) = fold (0,0) (…)`; `average = s/c` | pure function, higher-order fold |
| Logic (Prolog) | `avg(List, A) :- sum(List,S), length(List,N), A is S/N.` | relation + goal-directed deduction |

**Observation.** Same computation, four shapes: imperative mutates, OO hides the mutation in an object, functional makes it a pure expression, logic declares a relation. None is "more powerful"; each maps naturally onto a different problem structure — which is why multi-paradigm languages leave the choice to the programmer ([S-0098], [S-0100]).

## Elaboration prompts

- Why does purity make parallelization easier — and what exactly does the compiler/runtime no longer have to worry about?
- Inheritance is often described as "reuse". Reuse of what, and why does that reuse create the fragile-base-class coupling? When would you prefer composition or delegation?
- In Prolog, the same predicate can be queried "forwards" (given input, find output) and "backwards" (given output, find input). Why does that fall out of resolution, and why is it awkward in imperative languages?
- "Declarative = you don't control performance." Is that true for a Prolog program whose search order you must tune, or for a lazily evaluated Haskell program that you must force at the right points?
- Ray et al. controlled for project size, age, team, and domain. What selection effects remain, and why do they forbid causal conclusions?
- A team standardizes on "functional style in TypeScript". What does that discipline actually require day-to-day, and what part of the language must they police?

## Common misconceptions

1. **"Functional programming bans all state."** It bans *uncontrolled* effects: purity means effects are explicit and typed (monads, effect systems). Even Haskell mutates, inside `ST`/`IO`. [S-0098]
2. **"OOP is the only way to get encapsulation."** Modules (Rust, OCaml, C headers) provide the same information hiding; classes are one vehicle, not the concept. [S-0098]
3. **"Declarative languages leave everything to the machine."** Search order in Prolog and evaluation strategy in FP are programmer-controlled and performance-critical. [S-0100], [S-0098]
4. **"This data proves functional languages have fewer bugs."** The strongest available large-N study finds a significant but *modest* association, with small effects and no causal warrant. [S-0099]
5. **"Logic programming is just expert systems."** It is a general computational model (facts + rules + deduction); its home turf is search-heavy and relational problems, which includes but is not limited to rule engines. [S-0100]
6. **"Every language has exactly one paradigm."** C++ is procedural + OO + generic + functional; JavaScript is prototype-OO + functional; paradigm is a style, not a label. [S-0098]

## Feynman targets

- "Explain to a non-programmer the difference between a recipe that says *how* to cook (imperative) and a restaurant menu that says *what* you want (declarative) — and where the menu still depends on the kitchen." ([S-0098])
- "Explain why replacing a value with its result never changes a pure program, and why that superpower breaks the moment a function touches the outside world."
- "Explain Prolog as answering questions about facts and rules, like a detective — and where the detective's search strategy matters."
- "Explain why 'the data proves language X is better' is a bad argument, using confounding factors as the punchline." ([S-0099])

## Interleaving hooks

- **cs-foundations/logic-and-proof** (prerequisite) — logic programming reuses the prerequisite's logic: Horn clauses, unification, and resolution are deductive inference; revisit proof strategies to predict Prolog's behavior.
- **programming/functions-and-types** — purity, higher-order functions, and parametric polymorphism are the type-system consequences of functional style; the function types in that topic are the FP claims here made concrete.
- **programming/compiler-pipeline** — implementation inheritance compiles to virtual dispatch tables and FP pipelines to closures; paradigm choice changes code generation and inlining behavior.
- **programming/memory-model-and-pointers** — purity's "no aliasing surprises" is exactly what ownership/borrowing formalizes; see that topic for the memory-level version of these tradeoffs.

If the learner places as **novice**, start with Worked example 1 and Feynman target 1 before any quiz; if **competent**, start with a prediction task ("which paradigm would this team choose, and what breaks?"), then use the misconceptions list as a self-check.
