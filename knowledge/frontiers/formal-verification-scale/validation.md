---
id: frontiers/formal-verification-scale
title: Formal Verification at Scale
band: B5
track: frontiers
tier: T4
bloom_target: understand
prerequisites: [cs-foundations/computability, cs-foundations/complexity-theory]
related: []
recommended: []
status: draft
schema-version: 1
owner: l1-formal-verification-scale
reviewed-by: []
updated: 2026-08-18
sources: [S-0282, S-0283, S-0284, S-0058]
review_after: 2027-02-17
---

# Formal Verification at Scale — validation

## Formative (practice)

### Q1
- Q: Name the three main families of formal verification and the artifact each one works on.
- bloom: remember
- bank: formative
- A: Model checking — exhaustive exploration of a finite-state model against temporal properties; theorem proving with proof assistants — machine-checked logical derivation over a formal specification; automated reasoning with SAT/SMT-style decision procedures — deciding satisfiability in decidable theories for program analysis. The families differ in what is exhaustive (model checking), deductive (theorem proving), or decidable (SMT).
- evidence: [S-0284]
- topic: frontiers/formal-verification-scale

### Q2
- Q: Why is "state explosion" the central scalability barrier for verification? Give the mechanism in one sentence.
- bloom: understand
- bank: formative
- A: The state space of a system with n interacting components can grow exponentially in n, so exhaustively exploring it becomes infeasible as the system scales — long before the system itself is large.
- evidence: [S-0284]
- topic: frontiers/formal-verification-scale

### Q3
- Q: What does "functional correctness" mean in the seL4 proof, and what lies outside its original scope?
- bloom: understand
- bank: formative
- A: It means the C implementation always behaves exactly as its abstract specification prescribes — it will never crash and never perform an unsafe operation, and its behavior is predictable in every situation. Outside the original scope: correctness of the compiler, assembly code, and hardware (assumed correct; the compiler gap was later closed by a binary-correctness proof).
- evidence: [S-0282]
- topic: frontiers/formal-verification-scale

### Q4
- Q: Which company verifies critical system designs with TLA+, since when, and on which services did it start?
- bloom: remember
- bank: formative
- A: Amazon Web Services, since 2011, using TLA+ specifications checked with the TLC model checker (design-level, "exhaustively testable pseudo-code"), beginning with DynamoDB and S3.
- evidence: [S-0283]
- topic: frontiers/formal-verification-scale

## Summative (mastery checkpoint)

### Q5
- Q: Distinguish model checking, theorem proving, and SMT-based analysis along the axes: what is exhaustive, what is deductive, what is decidable?
- bloom: understand
- bank: summative
- A: Model checking is exhaustive: it explores all reachable states of a finite model and is complete for that model, but suffers state explosion. Theorem proving is deductive: properties are derived step by step in a logic with every step machine-checked, which is expressive but needs human-supplied structure (specifications, invariants). SMT-based analysis is decidable: it decides satisfiability in specific restricted theories, giving fast automation at the price of limited expressiveness; undecidability is why there is no universal verifier covering everything.
- evidence: [S-0284][S-0058]
- topic: frontiers/formal-verification-scale

### Q6
- Q: You must verify a distributed leader-election protocol for a safety-critical product. Sketch the verification plan: which family, what artifact, what properties, and one pitfall.
- bloom: apply
- bank: summative
- A: Design-level: write a TLA+ (or equivalent) model of the design — processes, messages, failure assumptions; express safety properties (exactly one leader; validity) and liveness; run a model checker (e.g., TLC) over bounded configurations. Pitfall: the model is an abstraction — "all models are wrong, some are useful" — so validate the abstraction against the real protocol, and remember state explosion limits the configurations you can check.
- evidence: [S-0283][S-0284]
- topic: frontiers/formal-verification-scale

### Q7
- Q: A colleague says: "We formally verified the kernel, so it is bug-free." Assess the claim: what is true, what is assumed, what is missing?
- bloom: evaluate
- bank: summative
- A: True: the implementation is machine-checked to match its specification, covering functional correctness and (for seL4) integrity, noninterference, and binary correctness. Assumed: correctness of the hardware and originally the compiler/assembly. Missing: the specification itself could be wrong or incomplete, and the surrounding system (drivers, applications) is unverified. "Bug-free" therefore holds only relative to the specification and the assumptions — a strong but bounded guarantee.
- evidence: [S-0282]
- topic: frontiers/formal-verification-scale

### Q8
- Q: Compare where verification pays off: a banking web API vs an OS kernel. Where does the ROI justify it and why?
- bloom: evaluate
- bank: summative
- A: Kernel: failures are catastrophic, concurrency/interaction complexity defeats testing, and a verified kernel is reused by everything above it — seL4 is the precedent. Banking API: bugs are costly but often caught by testing and review at lower cost; verification pays there only for protocol-level invariants (e.g., ledger consistency), where design-level TLA+ like AWS uses gives pre-production guarantees on subtle concurrency bugs. The established pattern: verification pays where failure is extreme or where subtle design bugs evade every other technique.
- evidence: [S-0283][S-0282][S-0284]
- topic: frontiers/formal-verification-scale

## Review (spaced repetition — interleaved with prerequisites)

### Q9
- Q: Why can there be no algorithm that verifies arbitrary programs against arbitrary properties? State the theorem and its consequence for verification practice.
- bloom: understand
- bank: review
- A: The halting problem is undecidable (Turing, 1936): no algorithm decides whether an arbitrary program halts; a general program verifier would decide such undecidable properties. Consequence: verification must restrict scope — finite models, decidable fragments, or machine-checked proofs with human-supplied structure.
- evidence: [S-0058]
- topic: cs-foundations/computability

### Q10
- Q: Connect complexity theory to verification: why does state explosion make model checking scale poorly, and what does that imply about verification of large systems?
- bloom: analyze
- bank: review
- A: The state space grows exponentially with the number of components, and finite-state model checking must explore it; the decision problem is decidable but expensive, so exhaustive checking works only on bounded configurations. Implication: verification of large systems needs abstraction, symbolic techniques, or a restriction of the claim (component-level, design-level), rather than naive full-state exploration.
- evidence: [S-0284][S-0058]
- topic: cs-foundations/complexity-theory
