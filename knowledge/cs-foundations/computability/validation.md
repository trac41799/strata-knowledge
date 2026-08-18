---
id: cs-foundations/computability
title: Computability
band: B2
track: cs-foundations
tier: T0
bloom_target: understand
prerequisites: [cs-foundations/logic-and-proof]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-computability
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0058, S-0059, S-0060]
---

# Computability — validation

Item anatomy: `Q` · `bloom` · `bank` · `A` · `evidence` · `topic`.

## Formative (practice)

### F1. The Church–Turing thesis
- Q: State the Church–Turing thesis and explain whether it is a theorem or a thesis, and why.
- bloom: remember
- bank: formative
- A: Every function computable by an effective procedure is Turing-computable. It is a thesis, not a theorem: "effective" is informal, so the claim cannot be stated as a mathematical theorem. Confidence comes from the proven equivalence of all formalizations (λ-calculus, μ-recursive functions, register machines, ...) and the absence of counterexamples.
- evidence: [S-0058]
- topic: cs-foundations/computability

### F2. Undecidable does not mean unanswerable
- Q: "The halting problem is undecidable, so nobody can ever know whether a given program halts." Is this a correct consequence? Explain.
- bloom: understand
- bank: formative
- A: No. Undecidability rules out a single uniform algorithm for all machine–input pairs. For any particular program, halting or non-halting can often be proved by hand or by restricted analyses; the theorem says no general decision procedure exists, not that every instance is opaque.
- evidence: [S-0058]
- topic: cs-foundations/computability

### F3. Constructing a reduction
- Q: Let P = {⟨M⟩ : M writes a 1 on its tape at some point during any run}. Show P is undecidable by reducing the halting problem to it.
- bloom: apply
- bank: formative
- A: Given an instance (M, w) of HALT, build M' that ignores its input, runs M on w, and then writes a 1. Then M' writes a 1 on every run iff M halts on w, so ⟨M'⟩ ∈ P iff (M, w) ∈ HALT — a many-one reduction. If P were decidable, HALT would be decidable; contradiction. The reduction preserves the yes/no answer, which is the defining property of ≤m.
- evidence: [S-0060]
- topic: cs-foundations/computability

### F4. Decidable vs recognizable
- Q: A machine accepts every string in L and may loop forever on strings not in L. Which class is L in — decidable or recognizable — and what is missing?
- bloom: understand
- bank: formative
- A: L is Turing-recognizable, not necessarily decidable. What is missing is a "no" verdict: a decider must halt with a definite answer on every input, while a recognizer may run forever on non-members. L is decidable iff such a recognizer exists and a recognizer for its complement also exists.
- evidence: [S-0060]
- topic: cs-foundations/computability

### F5. Rice's theorem scope
- Q: For each property of programs, say whether Rice's theorem makes it undecidable: (a) "halts within 100 steps", (b) "computes a total function", (c) "has exactly 5 states".
- bloom: analyze
- bank: formative
- A: (a) No — a resource bound, not an extensional function property; decided by bounded simulation. (b) Yes — non-trivial semantic property (some functions total, some not). (c) No — a syntactic property. Rice covers only non-trivial properties of the computed function.
- evidence: [S-0059]
- topic: cs-foundations/computability

## Summative (mastery checkpoint)

### S1. The reduction theorem
- Q: Explain why "if A ≤m B and B is decidable, then A is decidable" is true, and state the contrapositive that is used in undecidability proofs.
- bloom: understand
- bank: summative
- A: A ≤m B supplies a computable mapping f preserving yes/no: to decide A, compute f(x) and run B's decider on it. Contrapositive: if A is undecidable and A ≤m B, then B is undecidable — the workhorse of reduction proofs. The direction cannot be reversed: "A ≤m B and A decidable" tells nothing about B.
- evidence: [S-0060]
- topic: cs-foundations/computability

### S2. Undecidability of the empty-language problem
- Q: Prove that E_TM = {⟨M⟩ : M accepts no input} is undecidable.
- bloom: apply
- bank: summative
- A: Two routes. Reduction: given (M, w), build M' that on input x runs M on w and accepts iff M halts; then L(M') = ∅ iff M does not halt on w, so ⟨M'⟩ ∈ E_TM iff (M, w) ∉ HALT — a reduction from the complement of HALT, hence undecidable. Or Rice: "accepts no input" is a non-trivial semantic property (the empty language vs any non-empty one), so Rice's theorem applies directly.
- evidence: [S-0059][S-0060]
- topic: cs-foundations/computability

### S3. Evaluating "static analysis is pointless"
- Q: Evaluate: "Because the halting problem and Rice's theorem are undecidable, static analysis and program verification are pointless."
- bloom: evaluate
- bank: summative
- A: Incorrect. Undecidability constrains uniform algorithms over all programs; it does not forbid per-instance proofs, restricted classes, decidable fragments, or sound approximations. Verification tools prove termination and correctness for the programs they are designed for, accepting incompleteness (some programs unanalyzable) — the same tradeoff the theorems predict. The theorems set the boundary; the engineering lives inside it.
- evidence: [S-0058][S-0059][S-0060]
- topic: cs-foundations/computability

## Review (spaced repetition — interleaved with prerequisites)

### R1. Soundness, completeness, and the Entscheidungsproblem (from logic-and-proof)
- Q: First-order logic is complete (Gödel 1930) yet validity is undecidable (Turing 1936). Explain how both can hold.
- bloom: understand
- bank: review
- A: Completeness says every valid formula has a proof — existence, not findability. Undecidability says no algorithm decides validity for all formulas. A proof may exist and still require unbounded search; the two results live in different quantifiers (∃ proof vs ∃ algorithm).
- evidence: [S-0058]
- topic: cs-foundations/computability

### R2. The diagonalization skeleton
- Q: Lay out the three steps of the diagonalization proof that HALT is undecidable.
- bloom: remember
- bank: review
- A: (1) Assume a decider H for HALT. (2) Build machine D that on input ⟨M⟩ runs H(⟨M, M⟩) and does the opposite — halts if H predicts non-halting, loops if H predicts halting. (3) Run D on ⟨D⟩: D halts iff H says D doesn't halt — a contradiction either way, so H cannot exist. The self-application at step 3 is the diagonal.
- evidence: [S-0058]
- topic: cs-foundations/computability

### R3. Recognizability and complements
- Q: L and its complement are both Turing-recognizable. What follows, and why does the halting problem fail this test?
- bloom: understand
- bank: review
- A: L is decidable: run the two recognizers in parallel (interleaved); one must halt with a verdict. HALT's recognizer (simulate M on w) can certify halting but never certifies non-halting, so its complement is not recognizable — hence HALT is recognizable but not decidable.
- evidence: [S-0060]
- topic: cs-foundations/computability
