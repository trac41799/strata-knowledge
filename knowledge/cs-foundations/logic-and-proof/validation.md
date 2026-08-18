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

# Logic & Proof — validation

Item anatomy: `Q` · `bloom` · `bank` · `A` · `evidence` · `topic`.

## Formative (practice)

### F1. Soundness and completeness directions
- Q: State the two directions of the soundness/completeness pair for first-order logic, and which one Gödel's 1930 theorem proves.
- bloom: remember
- bank: formative
- A: Soundness: every provable formula is valid (⊢ φ implies ⊨ φ). Completeness: every valid formula is provable (⊨ φ implies ⊢ φ). Gödel 1930 proved the completeness direction; soundness is checked directly on the axioms and rules.
- evidence: [S-0043]
- topic: cs-foundations/logic-and-proof

### F2. Why completeness is not a decision procedure
- Q: Explain why the completeness theorem does not give an algorithm for deciding whether a first-order formula is valid.
- bloom: understand
- bank: formative
- A: Completeness asserts existence of a proof for every valid formula; it says nothing about how to find it. Naive proof search cannot decide validity: the search space is unbounded and (as shown in the computability topic) first-order validity is undecidable — the Entscheidungsproblem has no algorithmic solution.
- evidence: [S-0043]
- topic: cs-foundations/logic-and-proof

### F3. Natural deduction derivation
- Q: Derive (A ∧ B) → (B ∧ A) in natural deduction, naming each rule and assumption discharge.
- bloom: apply
- bank: formative
- A: 1. Assume A ∧ B. 2. ∧-elimination gives A. 3. ∧-elimination gives B. 4. ∧-introduction on B and A gives B ∧ A. 5. →-introduction discharges assumption 1, yielding (A ∧ B) → (B ∧ A). The derivation has no undischarged assumptions, so the formula is a theorem.
- evidence: [S-0044]
- topic: cs-foundations/logic-and-proof

### F4. Induction proof
- Q: Prove by mathematical induction that for every n ≥ 1, 1 + 2 + ⋯ + n = n(n+1)/2. Name base case and inductive step.
- bloom: apply
- bank: formative
- A: Base (n = 1): 1 = 1·2/2. Step: assume 1 + ⋯ + k = k(k+1)/2; then 1 + ⋯ + k + (k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2, the formula for k+1. The induction axiom (Peano) licenses ∀n P(n).
- evidence: [S-0045]
- topic: cs-foundations/logic-and-proof

### F5. Diagnosing a flawed induction
- Q: A proof claims to show by induction that "in any group of n horses, all horses have the same color": base n = 1 trivial; step: remove one horse, the rest match, remove another, the rest match, so all n match. For which n does the step fail, and why?
- bloom: analyze
- bank: formative
- A: The step fails for n = 2: after removing one horse the remaining group of 1 trivially matches; removing the other leaves a different group of 1. The two sub-groups share no horse, so no overlap forces the two horses to match. This is the missing-overlap fallacy — a valid-looking step that breaks at exactly one value; induction's step must hold for every k.
- evidence: [S-0045]
- topic: cs-foundations/logic-and-proof

## Summative (mastery checkpoint)

### S1. Contrapositive derivation
- Q: Derive (A → B) → (¬B → ¬A) in natural deduction, and state which inference is classical (not intuitionistic).
- bloom: apply
- bank: summative
- A: Assume A → B, then assume ¬B, then assume A; modus ponens gives B, contradicting ¬B, so ¬A by ¬-introduction; discharge ¬B by →-introduction giving ¬B → ¬A; discharge A → B giving (A → B) → (¬B → ¬A). The ¬-introduction step is intuitionistically valid; the contrapositive as stated needs only ¬-introduction, but the reverse direction (¬B → ¬A) ⊢ (A → B) is classical.
- evidence: [S-0044]
- topic: cs-foundations/logic-and-proof

### S2. Evaluating "completeness means we can find proofs"
- Q: Evaluate the claim: "Gödel's completeness theorem guarantees that a software tool can always find a proof of a valid formula, so theorem proving is just engineering."
- bloom: evaluate
- bank: summative
- A: Incorrect. Completeness guarantees existence of a derivation for every valid formula but gives no effective method to find one; first-order validity and proof search are undecidable (Entscheidungsproblem). Real provers therefore restrict to decidable fragments, heuristics, or interactive guidance — the theorem sets a boundary, not a workaround.
- evidence: [S-0043]
- topic: cs-foundations/logic-and-proof

### S3. Soundness's role
- Q: A proof assistant's rule set is sound but incomplete for its target logic. Why is that an acceptable (and typical) state for a tool, while an unsound rule set is fatal?
- bloom: understand
- bank: summative
- A: Soundness means everything the tool proves is genuinely valid — certified results are trustworthy, which is the tool's contract. Incompleteness only means some valid formulas remain unproved (a known limitation users work around). One unsound rule could certify a false theorem, and no completeness elsewhere repairs that breach.
- evidence: [S-0043]
- topic: cs-foundations/logic-and-proof

## Review (spaced repetition — interleaved with related topics)

### R1. Translation to first-order logic (interleaved with cs-foundations/discrete-mathematics)
- Q: Translate "every set has a subset that is not equal to it" into first-order logic and negate the formula.
- bloom: understand
- bank: review
- A: ∀S ∃T (T ⊆ S ∧ T ≠ S), with ⊆ definable as ∀x (x ∈ T → x ∈ S). Negation: ∃S ∀T (T ⊄ S ∨ T = S). Exercises quantifier scope, the point where propositional logic is insufficient.
- evidence: [S-0043]
- topic: cs-foundations/logic-and-proof

### R2. The induction axiom
- Q: State the induction axiom of Peano arithmetic and say which of base case or step it forces you to prove.
- bloom: remember
- bank: review
- A: If P holds of the first element and P(k) implies P(k+1) for every k, then P holds of every natural number. The axiom requires both: the base case (P of the first element) and the uniform step (P(k) → P(k+1) for arbitrary k).
- evidence: [S-0045]
- topic: cs-foundations/logic-and-proof

### R3. Valid vs satisfiable
- Q: A formula is true under some assignments and false under others. Which statuses does it have — valid, satisfiable, neither, both?
- bloom: understand
- bank: review
- A: Satisfiable (true under at least one assignment) but not valid (not true under all). Validity implies satisfiability; the converse fails — a common trap when conflating "has a model" with "is a theorem".
- evidence: [S-0043]
- topic: cs-foundations/logic-and-proof
