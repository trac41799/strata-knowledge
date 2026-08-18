# L2 Wave 1 Review — 2026-08-18

## Summary

Verdicts: **pass** — cs-foundations/logic-and-proof, cs-foundations/computability, cs-foundations/data-structures, hardware/memory-hierarchy, hardware/isa-basics, engineering-process/professional-ethics, engineering-process/software-lifecycle, quality-testing/quality-models, systems-software/http-basics, programming/programming-paradigms, programming/memory-model-and-pointers (11). **pass-with-fixes** — cs-foundations/discrete-mathematics (one critically wrong model answer), engineering-process/requirements-engineering (29148:2018 characteristics list inaccurate in both concept.md and S-0073), systems-software/networking-basics (untagged NAT claim — a K1 violation). **fail** — none. Overall publish recommendation: **publish all 14 after applying the fixes** below; no pack is technically unsound enough to reject, but the three pass-with-fixes packs and the two cross-cutting currency items (ISO 12207:2026 supersession, multi-tier claim-tag normalization) must be resolved before `status` flips to `validated`. The programming-paradigms T3→T1 tier raise is **justified** (verified below).

## cs-foundations/logic-and-proof

Verdict: **pass** — claims accurate, T0 assignment correct, all records real, validation and teaching exceed AC2.

### Findings

1. [minor] concept.md:23 — the definitional propositional-logic claim is cited to S-0043 (Gödel 1930 completeness paper); basic propositional connectives/validity are elementary formal content, not Gödel's 1930 result. Suggest citing a logic textbook, or restricting S-0043 to the completeness/compactness claims it actually supports.
2. [minor] concept.md:29 — "for first-order validity no such decision procedure exists (Entscheidungsproblem)" is tagged [T0][S-0043] alone; the undecidability of the Entscheidungsproblem is Church/Turing 1936 (S-0058), not Gödel. The cross-reference to computability is correct; add S-0058 to the tag or re-attribute the undecidability half of the claim.

## cs-foundations/computability

Verdict: **pass** — content correct; the T0 (Turing/Rice) vs T3 (Sipser taxonomy) split is disciplined and tier-consistent.

### Findings

1. [minor] concept.md:37 — multi-tier tag `[T0][S-0058][T3][S-0060]` on one claim; a claim should carry a single tier (see Cross-cutting finding 1). Normalize to `[T0][S-0058][S-0060]`.

## cs-foundations/discrete-mathematics

Verdict: **pass-with-fixes** — one critically wrong model answer must be rewritten before publish; everything else is sound.

### Findings

1. [critical] validation.md:87 — the S4 (R(3,3)=6) model answer is logically incorrect and would teach a false proof. The text "If 3 neighbors of v are pairwise adjacent we have a triangle; if not, two of them are adjacent to each other and with v form a triangle" is backwards (if they are *not* pairwise adjacent, some pair is *non-adjacent*, yielding an independent set, not a triangle); the second half ("among 3 mutual non-neighbors, either two are adjacent (no — …)") is self-contradictory. Correct argument: fix v; by pigeonhole ≥3 of the other 5 vertices are all adjacent to v or all non-adjacent; in the adjacent case, either some pair among them is adjacent (triangle with v) or none are (independent set of 3); symmetric in the non-adjacent case. Rewrite this answer.
2. [minor] concept.md:44 — the pigeonhole principle itself is tagged [T0][S-0049] (Ramsey 1930); the principle is Dirichlet's (1834) and predates Ramsey. Line 45 correctly states Ramsey *generalized* it, so cite S-0048 (Rosen) for the basic principle and reserve S-0049 for the Ramsey generalization.
3. [minor] concept.md:9 — `related: []` is not symmetric with logic-and-proof's `related: [cs-foundations/discrete-mathematics]`; `related` is undirected and should be mirrored. See Cross-cutting finding 4.

## cs-foundations/data-structures

Verdict: **pass** — operation costs, amortized/universal-hashing analysis, and model answers (heap trace, probe counts, universal hashing) all checked correct.

### Findings

1. [minor] concept.md:51,56,63 — multi-tier tags (`[T3][S-0055][T0][S-0053]`, `[T0][S-0053][T0][S-0054]`) violate single-tier-per-claim; normalize (Cross-cutting finding 1).

## hardware/memory-hierarchy

Verdict: **pass** — numbers and AMAT exercises verified correct.

### Findings

1. [minor] concept.md:52 (and S-0063 body) — "Cortex-A8 class, 4 GHz" mis-attributes the source: H&P 6e's worked example is a generic "4.0 GHz CPU" (with Intel Core i7 context for the 4-cycle L1); "Cortex-A8" is the 5th-edition example. The numeric values (4-cycle L1, DDR4-2400 ≈40 ns ≈160 cy, ≈200 cy miss penalty) match H&P 6e exactly — fix only the processor label in both the record and the claim.
2. [minor] concept.md:6 — topic `tier: T2` is driven solely by the CS2023 curriculum claim (line 39); every technical claim is T3. Correct per §6.3 (topic tier = strongest claim), but the T2 does not reflect technical confidence — note this in the pack or consider T3 with the curriculum claim re-tiered.

## hardware/isa-basics

Verdict: **pass** — decode examples (0xFF830293), ABI register mapping, and consistency-model content all verified correct.

### Findings

1. [minor] concept.md:53 — "16 GPRs, rax-r15" is imprecise: the 16 are rax, rbx, rcx, rdx, rsi, rdi, rbp, rsp, r8-r15. "rax-r15" omits rsi/rdi/rbp/rsp ordering; reword.
2. [minor] teaching.md:46 — `lea rax, [rdi + rdi*4]` computes ×5, not ×4; the worked example flags it with "?" but should read `lea rax, [rdi*4]` (or a shift). Fix to avoid teaching a wrong instruction.
3. [minor] validation.md:109,117,125 — review-item `topic` field uses a non-canonical id with a parenthetical ("hardware/isa-basics (interleaves hardware/memory-hierarchy)"); `topic` should be a clean id (Cross-cutting finding 3).

## engineering-process/requirements-engineering

Verdict: **pass-with-fixes** — one major inaccuracy in a codified-standard claim (propagated into the evidence record).

### Findings

1. [major] concept.md:44 (and S-0073 body) — the ISO/IEC/IEEE 29148:2018 characteristics enumeration is inaccurate. Verified against the standard text: individual-requirement characteristics (§5.2.5) are necessary, appropriate (implementation-free), unambiguous, complete, singular, feasible, verifiable, correct, conforming; set-of-requirements characteristics (§5.2.6) are complete, consistent, feasible, comprehensible. The pack adds "traceable" to the set list (it is not a §5.2.6 set characteristic) and omits "conforming" from the individual list. Correct both concept.md:44 and the S-0073 description.
2. [minor] concept.md:62 (and S-0075 body) — the "roughly 5x for smaller systems" figure is attributed to S-0075 (Boehm & Basili 2001), whose own text states only the 100x (large-system) finding; the 5:1 ratio is from related literature (Boehm's earlier work), not the 2001 article. The hedging is honest; soften the attribution or cite the 5x source separately.
3. [minor] concept.md:55 — "traceability is a characteristic of a good set of requirements in 29148:2018" inherits the same mis-attribution as Finding 1 (traceability is a requirement *attribute*/individual characteristic in 29148, not a §5.2.6 set characteristic).

## engineering-process/professional-ethics

Verdict: **pass** — ACM/IEEE code content and Therac-25 claims verified accurate.

### Findings

1. [minor] S-0080 record — `type: observational` conflicts with `hierarchy-level: 7`; the Therac-25 is a documented case-study/investigation (practitioner level), not a large-N observational study. The concept correctly tags it T3, but the record's `type` should be `practitioner` (or a `case-study` type) for internal consistency.

## engineering-process/software-lifecycle

Verdict: **pass** — Royce/boehm/IID/Therac-25 content accurate and properly dated to ISO 12207:2017; currency caveat below.

### Findings

1. [minor] concept.md:24,34,37,42,47,51 — all ISO 12207 claims are explicitly dated "2017" and are accurate for 2017, but ISO/IEC/IEEE 12207:2026 (published 2026-04-15, board approval 2026-02-12) supersedes 2017. S-0020 carries no supersession note, and the 2026 edition harmonizes with 15288:2015 and renames a requirements process — re-check "30 processes / 4 categories" and "System/Software Requirements Definition" against 2026 before publish (Cross-cutting finding 2).

## quality-testing/quality-models

Verdict: **pass** — 25010:2023 characteristics/subcharacteristics and McCall/Boehm lineage verified correct.

### Findings

1. [minor] concept.md:35,48 — multi-tier tags (`[T3][S-0108][S-0109][T2][S-0019]`) violate single-tier-per-claim; normalize (Cross-cutting finding 1).

## systems-software/networking-basics

Verdict: **pass-with-fixes** — one untagged factual claim is a K1 violation for published content.

### Findings

1. [major] concept.md:78 — the NAT paragraph ("NAT … rewrites addresses/ports at a gateway … breaks IP's end-to-end transparency") is a factual claim with no evidence record, explicitly flagged "not yet claim-covered". This violates K0/K1 for publishable concept content ("prose without claim tags is untestable"; AC5 forbids unprovenanced claims). The honest flag is better than silent prose but insufficient for `validated`. Fix: add a record for NAT (RFC 3022, or RFC 2663) and tag the claim, or reduce the paragraph to a non-claim "Extension (not covered here)" pointer with a citation.
2. [minor] concept.md:60 (and validation.md:95) — "TCP reserves ports 0–255 as well-known (RFC 1122 §4.2.2.1)" is accurate to RFC 1122 but dated against IANA's current 0–1023 well-known / 1024–49151 registered convention; add a one-line currency note so learners do not misread the range.

## systems-software/http-basics

Verdict: **pass** — methods/status/negotiation/version semantics verified against RFC 9110/9112/9113/9114; caching boundary correctly deferred to http-caching (S-0009/RFC 9111).

### Findings

1. [minor] validation.md:104,112 (and teaching.md:34) — review items Q10/Q11 and the worked example cite S-0089/S-0088 (networking-basics records) that are not listed in this pack's `sources` frontmatter. Decide and document whether interleaved records must appear in `sources` (Cross-cutting finding 3).

## programming/programming-paradigms

Verdict: **pass** — **tier raise validated as justified.** S-0099 (Ray et al.) is a real large-N observational study: verified "728 projects, 63 million SLOC, 29,000 authors, 1.5 million commits, 17 languages" (CACM 2017 abstract). The record is hierarchy-level 5 → T1 (correct per hierarchy.md), and the three T1 claims (concept.md:54,55,68) faithfully report the study's "significant but modest" association, small effect sizes, and observational/no-causal-warrant limits. Paradigm-classification claims are correctly left at T3 (Scott PLP). Topic tier = strongest = T1, per §6.3. No substantive findings.

### Findings

1. [minor] S-0099 record title renders the venue as "Github" (lowercase h); cosmetic — "GitHub".

## programming/memory-model-and-pointers

Verdict: **pass** — C17 clause numbers, data-race/UB definitions, and Rust ownership rules verified correct; Wang et al. SOSP 2013 (S-0104) accurately characterized.

### Findings

1. [minor] validation.md:96,112 (and teaching.md:89) — R1/R3 cite S-0063/S-0032 (memory-hierarchy / virtual-memory records) not listed in this pack's `sources`; same interleaving-record question as Cross-cutting finding 3.

## Records audit

| record | verdict | notes |
|---|---|---|
| S-0043 Gödel 1930 | pass | completeness/compactness provenance correct; DOI 10.1007/BF01696781 plausible |
| S-0044 Gentzen 1935 | pass | ND/sequent/Hauptsatz correct; DOI 10.1007/BF01201353 plausible |
| S-0045 Peano 1889 | pass | shared record, well-formed |
| S-0048 Rosen 8e | pass | correct edition/year |
| S-0049 Ramsey 1930 | pass | correct; see discrete-mathematics Finding 2 re pigeonhole attribution |
| S-0053 Tarjan 1985 | pass | DOI 10.1137/0606031 correct |
| S-0054 Carter & Wegman 1979 | pass | DOI correct |
| S-0055 Knuth TAOCP v3 | pass | 2nd ed. 1998 correct |
| S-0058 Turing 1936 | pass | DOI 10.1112/plms/s2-42.1.230 correct |
| S-0059 Rice 1953 | pass | correct |
| S-0060 Sipser 3e | pass | correct |
| S-0063 H&P 6e | pass-with-fix | numbers correct; "Cortex-A8" label mis-attributed (memory-hierarchy Finding 1) |
| S-0064 COD RISC-V 2e | pass | correct |
| S-0065 Denning 1980 | pass | distinct from S-0031 (Denning 1968); no conflict |
| S-0068 RISC-V ISA | pass | 40 instr / 6 formats / x0 correct |
| S-0069 Patterson & Ditzel 1980 | pass | DOI 10.1145/641914.641917 correct |
| S-0070 SysV AMD64 psABI | pass | de-facto standard, well-formed |
| S-0073 ISO 29148:2018 | pass-with-fix | **characteristics list inaccurate** (requirements-engineering Finding 1); standard itself real |
| S-0074 Nuseibeh & Easterbrook 2000 | pass | DOI 10.1145/336512.336523 correct |
| S-0075 Boehm & Basili 2001 | pass | **citation real** (IEEE Computer 34(1):135-137, Jan 2001); DOI 10.1109/2.962984 exists but is omitted — add it; "5x" figure over-attributed (minor) |
| S-0078 ACM Code 2018 | pass | adoption date/sections correct |
| S-0079 IEEE Code 2020 | pass | 10 tenets / 3 commitments correct |
| S-0080 Leveson & Turner 1993 | pass-with-fix | real (IEEE Computer 26(7)); `type: observational` vs `hierarchy-level: 7` mismatch |
| S-0083 Royce 1970 | pass | correct |
| S-0084 Boehm 1986 | pass | correct |
| S-0085 Larman & Basili 2003 | pass | correct |
| S-0088 RFC 1122 | pass | ports 0-255 claim accurate to source |
| S-0089 RFC 1034 | pass | correct |
| S-0090 RFC 4291 | pass | correct |
| S-0093/94/95 RFC 9112/13/14 | pass | correct |
| S-0098 Scott PLP 4e | pass | correct |
| S-0099 Ray et al. | pass | **verified** 728 projects / 63M SLOC / 17 languages; level 5 → T1 correct |
| S-0100 Prolog (Clocksin & Mellish) | pass | correct |
| S-0103 ISO C17 | pass | correctly notes C23 (9899:2024) supersession |
| S-0104 Wang et al. SOSP 2013 | pass | real; level 5 → T1 correct |
| S-0105 Rust Book 2e | pass | correct |
| S-0108 McCall 1977 | pass | correct |
| S-0109 Boehm 1978 | pass | correct |
| S-0110 ISO 25020:2019 | pass | correct |
| S-0017/18/19/22/23, S-0009, S-0031, S-0032, S-0040 (shared) | pass | well-formed; S-0020 lacks 12207:2026 supersession note (below) |

## Cross-cutting findings

1. **[minor, systematic]** Multi-tier claim tags. Several claims carry two tier tags (e.g., computability:37 `[T0][S-0058][T3][S-0060]`; data-structures:51,56,63; quality-models:35,48; software-lifecycle:51). hierarchy.md states "a claim citing multiple records takes the strongest applicable level for its tier" — i.e., one tier per claim. Normalize to a single tier + multiple records (e.g., `[T0][S-0058][S-0060]`). Verify lint.py tolerates the current form; if it does, tighten it.

2. **[major, currency]** ISO/IEC/IEEE 12207:2026 supersedes 2017 (published 2026-04-15). S-0020 has no supersession note; the packs' claims are correctly dated "2017" but the 2026 edition harmonizes the process model with 15288:2015 and renames a requirements process. Add a supersession note to S-0020 and re-check the "30 processes / 4 categories" and "System/Software Requirements Definition" claims (software-lifecycle, requirements-engineering) against 2026 before publish. (spec.md §4.2 also still lists 2017 — out of scope here but note for L0.)

3. **[minor]** Interleaved-record provenance. Review items and worked examples frequently cite records not listed in the pack's `sources` (http-basics → S-0088/S-0089; memory-model → S-0063/S-0032; professional-ethics → S-0073). This is reasonable for interleaving, but the convention should be decided and documented: either add the cited records to `sources`, or state that `sources` covers only the pack's own claims. Also standardize the review-item `topic` field to clean ids (isa-basics uses parentheticals).

4. **[minor]** `related`/`recommended` frontmatter is under-populated relative to teaching.md interleaving hooks, and `related` is not symmetric (logic-and-proof ↔ discrete-mathematics is one-directional). Populate/mirror these fields so the knowledge graph reflects the prose.

5. **[minor]** Untagged lead-in prose. Several concept.md files open with untagged factual summary paragraphs (e.g., memory-hierarchy:21, isa-basics:21). These are borderline summaries rather than testable claims, but the NAT case (networking-basics:78) shows the risk. Adopt a convention: lead-ins must be pure orientation (no novel factual assertions), or be tagged like every other claim.

## Fix list

Ordered, minimal edits (only for pass-with-fixes/cross-cutting; do not touch published content without a PR):

1. discrete-mathematics/validation.md:87 — rewrite the S4 R(3,3)=6 model answer to the correct pigeonhole argument.
2. requirements-engineering/concept.md:44 and evidence/records/S-0073.md — correct the 29148:2018 characteristics lists (individual: +conforming; set: remove "traceable", keep complete/consistent/feasible/comprehensible).
3. systems-software/networking-basics/concept.md:78 — add an RFC 3022 (or RFC 2663) record and tag the NAT claim, or reduce to a non-claim extension pointer.
4. evidence/records/S-0075.md — add `doi: 10.1109/2.962984`; soften/relocate the "5x" figure attribution.
5. evidence/records/S-0020.md — add a supersession note (ISO/IEC/IEEE 12207:2026, 2026-04-15); re-check software-lifecycle/requirements-engineering 12207 claims.
6. evidence/records/S-0063.md and hardware/memory-hierarchy/concept.md:52 — replace "Cortex-A8 class" with the correct 6e example label (4.0 GHz CPU / Intel Core i7 context).
7. evidence/records/S-0080.md — set `type: practitioner` (or add a case-study type).
8. Normalize all multi-tier claim tags to single-tier + multiple records (computability, data-structures, quality-models, software-lifecycle).
9. hardware/isa-basics — fix "rax-r15" wording (concept.md:53) and the `lea` typo (teaching.md:46); clean review-item `topic` ids.
10. cs-foundations/discrete-mathematics — re-cite the pigeonhole principle (concept.md:44) to S-0048; mirror `related` with logic-and-proof.
11. Decide + document the interleaved-record `sources` convention (Cross-cutting 3) and populate `related`/`recommended` (Cross-cutting 4).
12. hardware/memory-hierarchy — add a one-line note that T2 reflects only the CS2023 curriculum claim.
