---
id: cs-foundations/discrete-mathematics
title: Discrete Mathematics
band: B3
track: cs-foundations
tier: T0
bloom_target: apply
prerequisites: [cs-foundations/logic-and-proof]
related: [cs-foundations/logic-and-proof]
recommended: []
status: published
schema-version: 1
owner: l1-discrete-mathematics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0048, S-0049, S-0045]
---

# Discrete Mathematics — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the definitions of set, relation, equivalence relation, partial order, function, permutation, combination, congruence, and the pigeonhole principle. (evidence: S-0048)
- understand — Explain why an equivalence relation partitions its domain, why induction certifies infinitely many cases from two obligations, and why Ramsey's theorem generalizes the pigeonhole principle. (evidence: S-0048, S-0049, S-0045)
- apply — Count with the product/sum rules and permutation/combination formulas; compute congruence classes and solve CRT systems; run pigeonhole and induction arguments on new problems. (evidence: S-0048, S-0049, S-0045) — **bloom_target**
- analyze — Given a proposed proof or count, identify the missing induction obligation, the invalid counting step, or the misapplied theorem (e.g., functions vs relations, pigeonhole existence claims). (evidence: S-0048, S-0049)
- evaluate — Choose the right combinatorial model (ordered vs unordered, with vs without repetition) and the right proof strategy (direct, induction, contradiction, pigeonhole) for a stated claim. (evidence: S-0048)

## Worked example

### Part A — Induction: the handshake lemma

**Claim.** In any graph, the sum of all vertex degrees is exactly twice the number of edges: Σ deg(v) = 2|E|.

**Proof by induction on the number of edges.**

1. **Base case.** |E| = 0: no edges, every degree is 0, sum is 0 = 2·0 ✓.
2. **Inductive hypothesis.** Suppose the claim holds for every graph with k edges.
3. **Inductive step.** Take any graph G with k + 1 edges. Pick an edge e = {u, v}. Remove it to get G′ with k edges, so by the hypothesis Σ deg'(w) = 2k. Re-adding e increments deg(u) and deg(v) by 1 each, so Σ deg(w) = Σ deg'(w) + 2 = 2k + 2 = 2(k + 1) ✓.
4. **Conclusion.** By the induction axiom, the claim holds for every graph.

**What the two obligations were:** the base case (the claim holds for the smallest structure) and the step P(k) → P(k + 1) (any structure of size k + 1 reduces to size k). Both are required; checking the lemma on three example graphs is not a proof — that is the difference between evidence and a formal argument (the induction axiom makes the leap from "step works" to "all n").

### Part B — Pigeonhole with a modulus

**Claim.** Among any 10 integers, two leave the same remainder modulo 9, hence their difference is divisible by 9.

**Analysis.** Remainders mod 9 are 9 possible values (boxes); 10 integers (objects) must be placed into them, so some box holds ≥ 2: two numbers a, b with a ≡ b (mod 9). Then 9 | (a − b), i.e., a − b is divisible by 9. This is the r = 1 case of Ramsey's theorem — the pigeonhole principle — which Ramsey proved formally in 1930; the counting principle, not luck, is the guarantee.

**Key mental model:** induction = base + step ⇒ all cases; pigeonhole = more objects than classes ⇒ collision; both are existence theorems, and both prove by counting rather than by construction.

## Elaboration prompts

- Why must an equivalence relation be all three of reflexive, symmetric, and transitive? Find a relation that is symmetric and transitive but not reflexive, and explain which partition property fails. (evidence: S-0048)
- Derive C(n, k) from P(n, k) yourself: why does dividing by k! convert an ordered count into an unordered one? (evidence: S-0048)
- Induction, strong induction, and well-ordering are interchangeable — sketch why assuming "all cases below n" is no stronger than ordinary induction. (evidence: S-0048)
- Where does the pigeonhole principle hide in the statement R(2, s) = s of Ramsey theory? Trace the r = 1 case in words. (evidence: S-0049)
- Modular arithmetic treats 0 ≡ 3 ≡ 6 (mod 3) as the same class: which equivalence-relation theorem licenses this, and what would break if congruence were not transitive? (evidence: S-0048)

## Common misconceptions

1. **"Induction = check a few cases."** A finite sample never proves a universal statement — the induction axiom requires the base case plus an arbitrary-k step, and examples cannot substitute for either. (evidence: S-0045)
2. **"A function is any rule that pairs inputs and outputs."** Formally a function must be total and single-valued on its domain; a "function" that returns two values for one input, or none for another, is a relation — this distinction is what makes bijections and inverses well-defined. (evidence: S-0048)
3. **"The pigeonhole principle tells you which box overflows."** It guarantees existence of a crowded box and nothing more; finding the box may require work. Confusing existence with construction leads to wrong proofs. (evidence: S-0049)
4. **"Partial order = total order with missing pairs."** Antisymmetry permits incomparability by design; partial orders model hierarchies (subsets, divisibility) where incomparable elements are expected, and adding all pairs would destroy the structure. (evidence: S-0048)
5. **"a ≡ b (mod m) means a and b are equal."** It is a divisibility statement: m | (a − b). Equality of residue classes, not of integers, is what modular arithmetic reasons about. (evidence: S-0048)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why checking 100 examples of "1 + 2 + … + n = n(n+1)/2" proves nothing, but two small steps (base + step) prove it for every n — grade against the induction claims. (evidence: S-0045)
2. Why 10 people in 9 rooms guarantees two share a room, and why this same one-line idea powers arguments that look very deep (Ramsey theory) — grade against the pigeonhole claims. (evidence: S-0049)
3. Why "same remainder mod 9" groups integers into exactly 9 baskets and why every integer lives in precisely one basket — grade against the equivalence-class claims. (evidence: S-0048)

## Interleaving hooks

- **cs-foundations/logic-and-proof (prerequisite):** induction and pigeonhole proofs are quantified statements — rehearse ∀/∃ order, contraposition, and proof-by-contradiction before applying them here (R1–R3 in validation.md).
- **cs-foundations/data-structures (recommended next):** every complexity argument is a counting argument — hash tables count collisions via the pigeonhole principle, heap proofs run by induction on height. Revisit this pack when studying amortized analysis.
- **cs-foundations/algorithms (related):** binomial coefficients are the arithmetic of recursion trees and dynamic programming; modular arithmetic reappears as hash functions and RSA.
- **data/distributed-databases (later):** congruence classes are the mathematical skeleton of hash-based sharding — the residue classes of this pack are the "buckets" of a distributed table.
