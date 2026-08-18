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

# Computability — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the Church–Turing thesis, the halting problem, Rice's theorem, and the decidable/recognizable definitions with their sources (Turing 1936; Rice 1953). (evidence: S-0058, S-0059)
- understand — Explain why undecidability constrains uniform algorithms rather than individual instances, and why "recognizable but not decidable" is possible. (evidence: S-0058, S-0060) — **bloom_target**
- apply — Construct many-one reductions (e.g., from HALT to other problems) and classify properties under Rice's theorem. (evidence: S-0060, S-0059)
- analyze — Given a proposed analyzer or a property, determine which theorem (Turing, Rice, none) governs it and why. (evidence: S-0058, S-0059)
- evaluate — Judge claims like "undecidable means verification is pointless" against the model-restriction argument. (evidence: S-0058, S-0060)

## Worked example

### Part A — The diagonalization proof, step by step

Claim: no Turing machine decides HALT = {⟨M, w⟩ : M halts on input w}.

1. **Assume the opposite.** Suppose a decider H exists: H(⟨M, w⟩) accepts iff M halts on w, and H itself always halts.
2. **Build D from H.** D takes an encoding ⟨M⟩ and runs H on the diagonal pair ⟨M, M⟩ (the same machine fed itself). D then does the opposite of H's verdict: if H accepts (predicted halting), D loops forever; if H rejects (predicted non-halting), D halts. Everything D does is computable given H, so D is a legitimate machine.
3. **Run D on its own encoding ⟨D⟩.** This is the diagonal step — the machine is fed itself:
   - If D halts on ⟨D⟩, then H(⟨D, D⟩) accepted, so D was built to loop — contradiction.
   - If D loops on ⟨D⟩, then H(⟨D, D⟩) rejected, so D was built to halt — contradiction.
4. **Conclusion.** Both cases contradict the assumed behavior of H, so H does not exist: HALT is undecidable. The proof uses only logical vocabulary from the logic-and-proof topic (assumption, case analysis, contradiction) plus the one trick — self-application.

Key mental model: **a decider for "does this machine halt?" would have to answer about a machine built to invert that very answer — the decider's verdict and the machine's behavior chase each other around the diagonal.**

### Part B — A many-one reduction, step by step

Claim: the empty-language problem E_TM = {⟨M⟩ : M accepts no input} is undecidable.

1. **Choose the source problem.** HALT is known undecidable; reduce HALT ≤m E_TM.
2. **Design the mapping.** Given an instance (M, w), construct a machine M' that: ignores its own input x, runs M on w, and accepts iff M halts. M' is built from M and w by a computable construction (inserting w as a constant and wrapping M) — the mapping is computable.
3. **Check the yes/no preservation.**
   - If M halts on w: M' accepts every input, so L(M') ≠ ∅ — ⟨M'⟩ ∉ E_TM.
   - If M does not halt on w: M' never accepts anything, so L(M') = ∅ — ⟨M'⟩ ∈ E_TM.
   So (M, w) ∈ HALT iff ⟨M'⟩ ∉ E_TM — yes/no flips, but uniformly: this is still a valid many-one reduction (to the complement), and it transfers undecidability.
4. **Conclude.** If E_TM were decidable, HALT would be decidable through the mapping; contradiction. (Rice's theorem gives the same result in one line: "accepts no input" is a non-trivial semantic property.)

## Elaboration prompts

- Why must the machine built in a reduction be *computably constructible* from the source instance — what breaks if the construction itself needs the decision we lack? (evidence: S-0060)
- The Church–Turing thesis is unprovable, yet every formalization converges on the same class. What does that convergence tell you about "effective computation" as a concept? (evidence: S-0058)
- HALT is recognizable; its complement is not. Why is that asymmetry exactly the difference between "can certify yes" and "can certify both"? (evidence: S-0060)
- Rice's theorem is about the function computed, not the program. Where does "halts within 100 steps" escape the theorem — and what does that tell you about the boundary between semantics and resources? (evidence: S-0059)
- Turing's Entscheidungsproblem result answers a question posed by Hilbert in 1928. Why is "validity of first-order formulas" a computation problem at all — what does Gödel's completeness have to do with the encoding? (evidence: S-0058)

## Common misconceptions

1. **"Undecidable means we can never know whether any program halts."** Wrong scope: undecidability kills a single uniform algorithm over all program–input pairs; individual instances are routinely resolved (proofs, tests, restricted analyses). The theorem's boundary is "one procedure for everything", not "nothing is knowable". (evidence: S-0058)
2. **"The Church–Turing thesis was proven by Turing's paper."** Turing's paper gives the model and the analysis; the thesis itself is unprovable because "effective" is informal. What is proven is the equivalence of the formal models and the undecidability results built on them. (evidence: S-0058)
3. **"Rice's theorem means every property of programs is undecidable."** Only non-trivial *semantic* properties — those determined by input/output behavior — are covered. Syntax checks, type checking, size bounds, and bounded simulation are decidable. The theorem has precise scope: index sets. (evidence: S-0059)
4. **"Recognizable is just a slower decidable."** A recognizer may never answer "no" — it can run forever on non-members. Decidability requires terminating verdicts in both directions; "decidable iff recognizable and co-recognizable" is the exact relationship. (evidence: S-0060)
5. **"If A ≤m B and A is decidable, then B is decidable."** Reversed direction — invalid. Reductions transfer decidability upward (B decidable ⟹ A decidable) and undecidability downward (A undecidable ⟹ B undecidable). The mapping runs from A to B; properties travel the other way. (evidence: S-0060)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "there is no single recipe that reads any program and always says whether it finishes" is different from "we can never tell whether a particular program finishes" — like a referee who can decide any one match but no rulebook covers every match ever. Grade against the halting claims. (evidence: S-0058)
2. Why a machine that "does the opposite of what the analyzer predicts" defeats any analyzer — and why feeding it itself is the one move that makes the trap close. Grade against the diagonalization claims. (evidence: S-0058)
3. Why "this program computes the same function as that one" is unanswerable in general, while "this program has fewer than 100 lines" is trivially answerable — the difference between what a program *does* and what it *is*. Grade against the Rice claims. (evidence: S-0059)

## Interleaving hooks

- **cs-foundations/logic-and-proof (prerequisite):** rehearse proof by contradiction and case analysis — the diagonalization proof is a structured application of both (R1 in validation.md). Gödel's completeness frames what the Entscheidungsproblem is asking.
- **cs-foundations/complexity-theory (next):** decidability is the "can it be computed at all?" question; complexity is "how much resource?" — reductions reappear there as NP-completeness machinery.
- **cs-foundations/discrete-mathematics (related):** encodings and countability: the set of all programs is countable, the set of all functions is not — the pigeonhole behind "most functions are uncomputable".
- **frontiers/formal-verification-scale (dependent):** verified compilers and proof assistants live inside the boundary — sound, incomplete systems that prove real programs correct while sidestepping undecidability by restriction.
- **systems-software/distributed-consensus (cross-track):** FLP's impossibility is a halting-problem cousin in an asynchronous model; like HALT it is a liveness/model result, not a statement that consensus "can't work in practice" — comparing the two theorems is retrieval practice for both.
