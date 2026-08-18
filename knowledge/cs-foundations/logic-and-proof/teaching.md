---
id: cs-foundations/logic-and-proof
title: Logic & Proof
band: B3
track: cs-foundations
tier: T0
bloom_target: apply
prerequisites: []
related: [cs-foundations/discrete-mathematics]
recommended: []
status: published
schema-version: 1
owner: l1-logic-and-proof
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0043, S-0044, S-0045]
---

# Logic & Proof — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the soundness and completeness directions for first-order logic and name their sources (Gödel 1930; Gentzen 1935). (evidence: S-0043, S-0044)
- understand — Explain why "valid", "satisfiable", "provable", and "true" are different notions, and why completeness does not yield a decision procedure. (evidence: S-0043)
- apply — Construct natural deduction derivations (∧, →, ∨, ¬ rules with assumption discharge) and induction proofs (base + step) for simple theorems. (evidence: S-0044, S-0045) — **bloom_target**
- analyze — Given a purported proof, locate the invalid step (missing base case, broken inductive step, rule misapplication). (evidence: S-0045, S-0044)
- evaluate — Judge claims like "completeness means proofs are always findable" against the Entscheidungsproblem boundary. (evidence: S-0043)

## Worked example

### Part A — A natural deduction derivation, step by step

Theorem: (A ∧ B) → (B ∧ A). Work backwards from the goal: the outer connective is →, so the last rule will be →-introduction, which needs a derivation of B ∧ A from assumption A ∧ B.

1. **Assume** A ∧ B (goal-directed: we want to prove B ∧ A from it).
2. **∧-elimination** on A ∧ B gives A (rule: from φ ∧ ψ infer φ).
3. **∧-elimination** again gives B (from φ ∧ ψ infer ψ).
4. **∧-introduction** on B and A gives B ∧ A (from φ and ψ infer φ ∧ ψ).
5. **→-introduction** discharges the assumption at step 1, giving (A ∧ B) → (B ∧ A) with no undischarged assumptions — a theorem.

Key mental model: **every connective has an introduction rule (how to prove it) and an elimination rule (how to use it); a proof is built from the conclusion backwards and the assumptions forwards; discharge is what turns "proved under an assumption" into "proved as an implication".**

### Part B — An induction proof, step by step

Theorem: for every n ≥ 1, 1 + 2 + ⋯ + n = n(n+1)/2. The Peano induction axiom says: prove the base case and the uniform step.

1. **Base case (n = 1):** 1 = 1·2/2. The equation holds — check by arithmetic.
2. **Inductive hypothesis:** assume the claim for an arbitrary k: 1 + ⋯ + k = k(k+1)/2. "Arbitrary" matters: k stands for any natural, not a chosen one.
3. **Inductive step:** 1 + ⋯ + k + (k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2 — the claim for k+1, derived purely from the hypothesis and algebra.
4. **Conclusion:** by the induction axiom, ∀n ≥ 1, 1 + 2 + ⋯ + n = n(n+1)/2.

Why both parts? Without the step, the claim holds only for 1. Without the base, the step might hold yet the claim fail everywhere (e.g., the classic all-horses-same-color fallacy passes the step and dies at n = 2 — the step's overlap argument fails exactly there).

## Elaboration prompts

- Why must the inductive step be proved for an *arbitrary* k? What goes wrong if you check it "for a few values"? (evidence: S-0045)
- The completeness theorem says valid and provable coincide. Where in that equivalence does an unsound rule (one that proves an invalid formula) live — and what does it break? (evidence: S-0043)
- Natural deduction has no axiom schemas for ∧ and ∨ — only rules. Why does that make proofs mirror reasoning instead of enumerating formulas? (evidence: S-0044)
- Proof by contradiction and proof by contrapositive both rely on classical ¬¬P ⊢ P. Re-derive both from double-negation elimination. (evidence: S-0044)
- Why does compactness imply that a theorem of first-order logic mentioning infinitely many axioms can be proved from finitely many? (evidence: S-0043)

## Common misconceptions

1. **"Sound and complete are the same property."** They are opposite directions: soundness (provable ⟹ valid) prevents false theorems; completeness (valid ⟹ provable) prevents lost theorems. A system can have one without the other; Gödel's 1930 theorem establishes both for first-order logic. (evidence: S-0043)
2. **"Completeness means every true mathematical statement is provable / provable statements are findable."** Completeness is about validity, not mathematical truth at large, and it asserts existence of proofs, not an algorithm to find them — first-order proof search is undecidable. Both readings fail. (evidence: S-0043)
3. **"Proof by contradiction is universally valid, so it is the strongest strategy."** It is classical-only: it relies on double-negation elimination, unavailable in intuitionistic logic; it is also non-constructive (existence without a witness). And it must never be confused with assuming the conclusion, which is circular and invalid in any system. (evidence: S-0044)
4. **"Checking a few cases proves an induction claim."** Induction is not enumeration: the step must hold for arbitrary k. The all-horses-same-color fallacy shows a step that fails at exactly one value can still look convincing. (evidence: S-0045)
5. **"If a formula is satisfiable it is valid."** Satisfiable = has a model; valid = true in all models. One example (or one satisfying assignment) supports satisfiability only — theoremhood requires validity, and a single countermodel refutes validity. (evidence: S-0043)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "if the machine proves it, it is true" (soundness) and "every true formula has a proof" (completeness) are two different promises, and why a tool could keep one and break the other. Grade against the soundness/completeness claims. (evidence: S-0043)
2. Why proving "one more than k" for every k really does cover every natural — like dominoes where each tile knocks the next and the first one falls. Grade against the induction claims. (evidence: S-0045)
3. Why proving "P implies Q" lets you permanently mark P as an assumption — and why that assumption disappears from the final statement. Grade against the discharge and →-introduction claims. (evidence: S-0044)

## Interleaving hooks

- **cs-foundations/computability (next, dependent):** diagonalization is proof by contradiction aimed at a self-referential construction; the halting proof is the payoff of the strategies learned here. Revisit after computability is mastered.
- **cs-foundations/discrete-mathematics (related):** sets, relations, and functions supply the domain vocabulary for first-order claims; induction over recursively defined structures (lists, trees) is where the two topics meet.
- **cs-foundations/data-structures (dependent):** structural induction is the standard correctness tool for recursive data structures and recursive algorithms.
- **cs-foundations/complexity-theory (related):** truth tables decide propositional validity in 2^n rows — the exponential cliff where decidability ends and complexity begins.
- **systems-software/distributed-consensus (cross-track):** FLP's impossibility argument is a proof by contradiction over runs of a protocol (bivalent configurations) — reconstructing its skeleton is retrieval practice for proof strategies.
