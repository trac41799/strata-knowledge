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

# Computability

## Claims

- A Turing machine is a formal computing device: an infinite tape of symbols, a finite-state control, and a read/write head moving left or right according to a finite transition table; it computes a partial function from input strings to output strings [T0][S-0058].
- Turing (1936) introduced the machines as a model of what a human "computer" (clerk) does when carrying out an algorithm, arguing the model captures every computation a human could perform — the defining analysis of effective computation [T0][S-0058].
- A universal Turing machine is a single machine that, given the encoding of any other machine together with an input, simulates it; this self-description of machines as data is the theoretical basis of stored-program computers [T0][S-0058].
- The Church–Turing thesis states that every function computable by an effective procedure is Turing-computable; it is a thesis about the meaning of "effective" rather than a theorem, but every proposed formalization (λ-calculus, μ-recursive functions, register machines, cellular automata) has been shown equivalent to Turing machines, and no counterexample is known [T0][S-0058].
- The halting problem — "does machine M halt on input w?" — is undecidable: no Turing machine decides it; the diagonalization argument assumes a decider H, builds a machine D that does the opposite of H's verdict on ⟨D, D⟩, and derives a contradiction [T0][S-0058].
- The Entscheidungsproblem — deciding whether a first-order formula is valid — is also undecidable: Turing's application of the halting problem shows no algorithm decides first-order validity, answering Hilbert's decision problem negatively [T0][S-0058].
- Undecidability is a statement about decision procedures over all instances: for any particular program one can often prove halting or non-halting; the theorem rules out a single uniform algorithm that works for every program–input pair [T0][S-0058].
- Many-one reducibility: A ≤m B when a computable function maps every instance of A to an instance of B preserving the yes/no answer; if A ≤m B and B is decidable then A is decidable — so an undecidable A forces B undecidable [T3][S-0060].
- The halting problem is m-complete for the recognizable languages: every Turing-recognizable language reduces many-one to it; reduction chains from the halting problem are the standard method for proving other problems undecidable [T3][S-0060].
- Reductions order problems by relative hardness: A ≤m B says B is at least as hard as A; undecidability propagates along the direction of the reduction, which is why reduction proofs are one-way [T3][S-0060].
- Rice's theorem (1953): every non-trivial property of the function computed by a program — a property true of some partial computable functions and false of others, depending only on input/output behavior — is undecidable given the program text [T0][S-0059].
- Rice's theorem covers semantic properties only: syntactic, structural, or resource properties (e.g., "has fewer than 100 instructions", "halts within 100 steps") are not function properties and are not covered; bounded-resource properties can be decided by bounded simulation [T0][S-0059].
- Everyday program questions are Rice properties: "computes a total function", "halts on every input", "outputs 7 on input 3" are non-trivial semantic properties, hence undecidable — no general analyzer can answer them from source alone [T0][S-0059].
- Decidable vs recognizable: a language is decidable when some Turing machine halts with yes/no on every input; it is Turing-recognizable when a machine halts with yes exactly on the members and may run forever on non-members [T3][S-0060].
- A language is decidable iff both it and its complement are recognizable; the halting problem is recognizable (simulate the machine) but not decidable, so its complement is not recognizable — the canonical asymmetry [T0][S-0058][S-0060].
- Recognizability is one-sided verification: a recognizer can certify "yes" answers but gives no verdict on "no"; decidability requires both directions at once [T3][S-0060].
- Every finite language is decidable (a machine can hardcode its instances); undecidability bites only on infinite instance classes — the distinction behind restricting analyses to finite or bounded inputs [T3][S-0060].

## Details

- Decision problems are framed as languages: an encoding scheme (e.g., ⟨M, w⟩) turns each problem instance into a string, and decidability is membership in the corresponding language; this encoding step is what makes universality and diagonalization possible [T0][S-0058].
- The taxonomy is standard course content: decidable ⊂ recognizable, and a language is decidable exactly when it and its complement are both recognizable; the halting problem separates the classes [T3][S-0060].

## Boundaries / common misunderstandings

- "Undecidable" is not "unsolvable in practice, always": decidability is a property of a decision problem over an infinite instance class; restricting the class (finite inputs, resource-bounded programs, decidable fragments) restores decidability — which is exactly what practical analyses and verifiers do [T3][S-0060].
- Halting problem nuance: the theorem says no single algorithm decides HALT for all machine–input pairs; it does not say individual halting questions are unanswerable, nor that programs can never be verified — per-instance termination proofs exist for most real programs [T0][S-0058].
- Rice's theorem does not make all program analysis impossible: it applies to index sets (extensional function properties); syntax checks, type checking, and bounded simulation fall outside its scope [T0][S-0059].
- The Church–Turing thesis is not a theorem that was "proven": "effective" is informal, so the thesis cannot be stated as a mathematical theorem; its acceptance rests on the equivalence of all formalizations and the absence of counterexamples [T0][S-0058].
- Recognizable does not equal decidable: a recognizer may loop forever on non-members, so a recognizer is strictly weaker than a decider; "decidable iff recognizable and co-recognizable" is the precise relationship [T3][S-0060].

## References (evidence records)

- [S-0058] Turing 1936 — On Computable Numbers (Proc. LMS s2-42).
- [S-0059] Rice 1953 — Classes of Recursively Enumerable Sets (Trans. AMS 74).
- [S-0060] Sipser 2013 — Introduction to the Theory of Computation, 3rd ed. (Cengage).
