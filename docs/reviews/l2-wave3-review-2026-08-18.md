# L2 Wave 3 Review — 2026-08-18

## Summary

Verdicts (23 packs): **pass** — `data/transactions-and-isolation`, `data/distributed-databases`, `quality-testing/software-testing-basics`, `quality-testing/test-design-techniques`, `quality-testing/test-automation`, `quality-testing/code-review`, `quality-testing/performance-engineering`, `security/threat-modeling`, `security/authentication-authorization`, `security/web-security`, `security/secure-sdlc`, `ai-ml/llm-architectures`, `frontiers/agentic-systems`, `frontiers/formal-verification-scale`, `frontiers/post-quantum-cryptography`, `frontiers/zero-knowledge-proofs` (16); **pass-with-fixes** — `data/relational-model`, `data/indexing-and-storage` (2); **fail** — `data/sql-and-query-optimization`, `security/cryptography-basics`, `ai-ml/ml-fundamentals`, `ai-ml/supervised-learning`, `ai-ml/neural-networks` (5). Overall publish recommendation: **DO NOT publish this wave as-is.** The five `fail` packs carry a false T0 topic tier — they tag mathematically-exact definitions/theorems as T0 while citing only practitioner/textbook/observational records (levels 4–7), not proof records (level 1). This is a K1/K2 confidence-integrity violation and is exactly the over-grade L2 exists to catch; the fix is a mechanical tier downgrade + claim re-tag (see Fix list). The two `pass-with-fixes` packs need small edits (a 1NF/2NF over-grade; a B-tree worked-example error). One critical records-hygiene defect: `S-0269` and `S-0272` are the same paper ("Attention Is All You Need", Vaswani 2017) recorded twice. Content and pedagogy across the wave are otherwise of high quality; the five T4 frontier packs show exemplary volatility discipline (dated, `review_after` set, honest `UNVERIFIED` markers).

## data/relational-model

**Verdict: pass-with-fixes**

### Findings

1. `[major]` `knowledge/data/relational-model/concept.md:30` — "First normal form (1NF) requires every attribute value to be atomic…" is tagged `[T0]` but cites only `[S-0183]` (Codd 1972, `practitioner` level 7) and `[S-0199]` (textbook, level 7). No level-1 proof record backs this definitional claim; per hierarchy.md, T0 ← level 1. Fix: re-tag `[T3]`.
2. `[major]` `knowledge/data/relational-model/concept.md:31` — 2NF claim same defect: `[T0][S-0183][S-0199]` with no proof record. Fix: re-tag `[T3]`.
3. `[minor]` `knowledge/data/relational-model/teaching.md:26` — the `**bloom_target**` marker is on the "understand" objective, but frontmatter `bloom_target: apply` (the apply objective is at line 27). Fix: move marker to line 27.

The T0 topic tier is otherwise **correctly** justified by `S-0184` (Bernstein 1976, `proof` level 1): the 3NF synthesis theorem, lossless-join, and BCNF⊂3NF claims (lines 28–29, 32–36) are genuinely proof-backed. F3/S1 model answers spot-checked and correct (candidate keys AB/AC/AD; lossless dependency-preserving decomposition verified).

## data/sql-and-query-optimization

**Verdict: fail**

### Findings

1. `[critical]` `knowledge/data/sql-and-query-optimization/concept.md:6` — topic `tier: T0` is unsupported: the pack contains **no level-1 (proof) record**. Sources are `S-0187` (Selinger 1979, `practitioner` L7), `S-0188` (Leis 2015, `observational` L5), `S-0189` (Graefe 1993, `practitioner` L7), `S-0197` (Comer, L7), `S-0199` (textbook, L7), `S-0194` (SQL-92, L6). Strongest applicable tier is **T1** (from S-0188, level 5).
2. `[critical]` `knowledge/data/sql-and-query-optimization/concept.md:28-30` — nested-loop `|R|*|S|`, sort-merge `O(n log n)`, hash-join `O(|R|+|S|)` complexity bounds are tagged `[T0]` but cite `[S-0189][S-0199]` (survey + textbook, level 7). These are textbook algorithmic facts; per hierarchy they are T3, not T0. Fix: re-tag `[T3]`; drop topic tier to `T1`.

Validation (11 items, ≥3 Bloom levels, clean topic ids) and teaching (worked example + 5 misconceptions) are sound. No other substantive errors.

## data/transactions-and-isolation

**Verdict: pass**

### Findings

None blocking. T0 correctly backed by `S-0192` (Eswaran-Gray-Lorie-Traiger 2PL theorem, `proof` L1), `S-0203` (Gray & Lamport, `proof` L1), `S-0034` (FLP, `proof` L1). ACID/SQL-92/P1–P3/SI-write-skew claims correctly T3/T2. S1 (write-skew) and the four-lens worked example are correct. Cross-pack 2PC-blocking phrasing matches `data/distributed-databases` (both cite S-0203, both T0).

## data/indexing-and-storage

**Verdict: pass-with-fixes**

### Findings

1. `[major]` `knowledge/data/indexing-and-storage/teaching.md:39` — root-split trace error: after promoting 15 out of root `[10,15,25]`, the right child is `[25]`, but the line reads "children are the internal nodes [10] and [15, 25]". `[15,25]` is wrong (a 2-key internal node would need 3 children). Fix: `[15, 25]` → `[25]`.

T0 is **correctly** justified by `S-0200` (Bayer & McCreight 1972, `proof` L1 — the height bound Θ(log n) is proven there). F3 (B+ split, promote 5) and the LSM/amplification claims are correct.

## data/distributed-databases

**Verdict: pass**

### Findings

None blocking. T0 correctly backed by `S-0035` (CAP proof, L1), `S-0034` (FLP, L1), `S-0203` (Gray & Lamport, L1). Spanner `[T1][S-0204]` (observational L5) correct; DDIA/Özsu claims T3 correct. CAP "not choose-two-of-three" and "2PC is not consensus" boundaries correctly T0. S-0278-adjacent cross-links sound.

## quality-testing/software-testing-basics

**Verdict: pass**

### Findings

None blocking. T1 (raised) correctly justified by `S-0208` (Inozemtseva & Holmes, `observational` L5). TDD quality claims are honestly downgraded to T3 with explicit "no verified controlled study" wording (concept.md:33) — exemplary honesty. SWEBOK claims T2 correct. Validation 11 items, ≥3 Bloom levels, clean.

## quality-testing/test-design-techniques

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/quality-testing/test-design-techniques/validation.md:21-28` — uses flat `- Q:` bullets without `### F#.` item headings (unlike most packs). Schema-valid (Q/bloom/bank/A/evidence/topic all present); cosmetic inconsistency only.
2. `[minor]` `knowledge/quality-testing/test-design-techniques/teaching.md:27` — uses `apply (target)` instead of the `**bloom_target**` convention; learning objectives lack `(evidence: …)` tags. Cosmetic.

T1 correctly justified by `S-0214` (systematic-review L2), `S-0212` (NIST observational L5), `S-0213` (quasi-experiment L4). NIST 65–97% / 4–6-way figures correct.

## quality-testing/test-automation

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/quality-testing/test-automation/validation.md:21-28` — same flat-bullet format divergence (no `### F#.` headings). Cosmetic.
2. `[minor]` `knowledge/quality-testing/test-automation/teaching.md:27` — `apply (target)` instead of `**bloom_target**`.

T1 (raised) correctly justified by `S-0217`/`S-0218`/`S-0219` (observational L5). Flakiness statistics (1.5%, 84%, 4.56% of 1.6M ≈ 73k, 2–16%) cross-check against the records and are correct.

## quality-testing/code-review

**Verdict: pass**

### Findings

None blocking. T1 correctly justified by `S-0222`/`S-0224` (observational L5) and `S-0223` (Fagan 1976, `observational` L5). Fagan 20% productivity / 10x–25x cost-escalation figures are single-company industrial data and are correctly not over-claimed; the pack presents them as Fagan's reported numbers. 66–150% files-known and 14.7–19.8 h medians correct. Validation 11 items, ≥3 Bloom levels, clean.

## quality-testing/performance-engineering

**Verdict: pass**

### Findings

None blocking. T1 correctly justified by `S-0227` (Tail at Scale, `observational` L5) and `S-0229` (Knuth 1971, `observational` L5). **Focus point (6) — Knuth for a T1 measurement-first claim is FAIR:** it is a genuine empirical study (level 5) and the pack honestly dates it to 1971 ("measured in 1971 and the standing default"). Latency numbers correctly tagged T3 (`S-0228` practitioner L7) as era-specific. Fan-out math and hedged-request figures (1800→74 ms, +2%) correct.

## security/cryptography-basics

**Verdict: fail**

### Findings

1. `[critical]` `knowledge/security/cryptography-basics/concept.md:6` — topic `tier: T0` unsupported: no level-1 record. Sources are `S-0232` (FIPS 197, L6), `S-0233` (Katz & Lindell, `practitioner` L7), `S-0234` (SP 800-175B, L6), `S-0017`/`S-0019` (standards L6). Strongest applicable tier is **T2**.
2. `[critical]` `knowledge/security/cryptography-basics/concept.md:53` — the Diffie-Hellman algebraic identity `(g^a)^b = g^(ab)` is tagged `[T0]` but cites only `[S-0233]` (textbook, level 7). The identity is mathematically-exact *content*, but the citation is not proof-level. Fix: re-tag `[T3]`, or add a proof-level record (Diffie–Hellman 1976).
3. `[minor]` `knowledge/security/cryptography-basics/teaching.md:25-28` — learning objectives use `[T2][S-…]` inline tags rather than `(evidence: …)`; no `**bloom_target**` marker (frontmatter `apply`). Cosmetic.

Content is otherwise accurate (AES, HMAC, GCM, birthday bound, DH trace p=23 all correct; Q4 model answer verified numerically).

## security/threat-modeling

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/security/threat-modeling/teaching.md:25-28` — no `**bloom_target**` marker (frontmatter `apply`). Cosmetic.

T2 correct (SWEBOK/ISO level-6). STRIDE mapping and MITRE ATT&CK "14 tactics" correct. Attack-tree AND/OR semantics correct.

## security/authentication-authorization

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/security/authentication-authorization/teaching.md:25-27` — no `**bloom_target**` marker; objectives listed as Understand/Apply only (no remember/analyze/evaluate). Validation pack still spans remember/understand/apply, so AC2 is met.

**Focus point (2) — the T2 revert is CORRECT:** the pack cites RFC 6749, RFC 7519, NIST SP 800-63B-4, SWEBOK, ISO 25010 — all level-6 codified-consensus standards. T2 (not T3) is the right topic tier. Web-verified: SP 800-63B-4 reauthentication values (AAL2 = 24 h overall / 1 h inactivity; AAL3 = 12 h / 15 min) in concept.md:49 are **correct** against the current final (the old 12 h/30 min figures belong to 63B-3, not -4).

## security/web-security

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/security/web-security/teaching.md:25-27` — no `**bloom_target**` marker. Cosmetic.

**Focus point (2) — T2 revert CORRECT:** RFC 6454, RFC 9110, SWEBOK, ISO 25010 (level 6) → T2. OWASP Top 10:2021 list (A01–A10), IDOR/CWE-639, CSRF/CWE-352, XSS/CWE-79 mapping, origin (scheme,host,port) all correct.

## security/secure-sdlc

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/security/secure-sdlc/concept.md:26` — cites `S-0020` (ISO 12207:2017) without noting its supersession by the 2026 revision; the record itself flags it and the claim is dated to 2017, so this is acceptable but a one-line "superseded by 12207:2026" note would be more honest.

T2 correct (SSDF SP 800-218 L6, SWEBOK L6, ISO 12207 L6). SAMM "5 functions / 15 practices / levels 0–3" and CVE/CNAs correct. Cross-pack with threat-modeling (both "security integrated throughout lifecycle") is consistent.

## ai-ml/ml-fundamentals

**Verdict: fail**

### Findings

1. `[critical]` `knowledge/ai-ml/ml-fundamentals/concept.md:6` — topic `tier: T0` unsupported: no level-1 record. Sources: `S-0018` (CS2023 L6), `S-0257` (Kohavi, `quasi-experiment` L4), `S-0258` (Kaufman, `observational` L5), `S-0259` (Saito & Rehmsmeier, `observational` L5). Strongest applicable tier is **T1**.
2. `[critical]` `knowledge/ai-ml/ml-fundamentals/concept.md:40-43` — precision/recall/ROC-AUC/PRC-baseline claims tagged `[T0]` cite only `[S-0259]` (observational L5). These are definitions/derivations, but the citation is not proof-level. Fix: re-tag `[T1]` (matching S-0259 level 5).

Content is accurate and the validation (Q4 confusion-matrix arithmetic verified) and teaching are strong. The Kohavi/Kaufman T1 claims are correctly backed.

## ai-ml/supervised-learning

**Verdict: fail**

### Findings

1. `[critical]` `knowledge/ai-ml/supervised-learning/concept.md:6` — topic `tier: T0` unsupported: no level-1 record. Sources include `S-0262`/`S-0263`/`S-0264` (all `quasi-experiment` L4), `S-0257` (L4), `S-0259` (L5), `S-0268` (Goodfellow, `practitioner` L7). Strongest applicable tier is **T1**.
2. `[critical]` `knowledge/ai-ml/supervised-learning/concept.md:32-34` — "MSE/cross-entropy convex for linear models", "GD converges for convex losses", "mini-batch SGD unbiased in expectation" are tagged `[T0]` citing only `[S-0268]` (textbook, L7). Genuinely T0-worthy *content*, but not proof-cited. Fix: re-tag `[T3]`.
3. `[minor]` `knowledge/ai-ml/supervised-learning/concept.md:26-27` — SVM and decision-trees tagged `[T3]` but their records (S-0264, S-0262) are level 4 (→ T1). Under-grade, conservative direction; inconsistent with the record levels.

## ai-ml/neural-networks

**Verdict: fail**

### Findings

1. `[critical]` `knowledge/ai-ml/neural-networks/concept.md:6` — topic `tier: T0` unsupported: no level-1 record. Sources: `S-0267` (Rumelhart 1986, `quasi-experiment` L4), `S-0268` (Goodfellow, L7), `S-0269` (Vaswani 2017, `quasi-experiment` L4), `S-0257` (L4). Strongest applicable tier is **T1**.
2. `[critical]` `knowledge/ai-ml/neural-networks/concept.md:25,26,31,36,41,43` — perceptron-linear-separability, universal-approximation, activation definitions, backprop chain-rule, vanishing/exploding mechanism, and RNN-BPTT claims are tagged `[T0]` but cite `[S-0267]` (L4) and `[S-0268]` (L7). The backprop chain-rule is a genuine derivation, but Rumelhart 1986 is classified `quasi-experiment` by the same author — an internal contradiction. Fix: re-tag to T1 (S-0267) / T3 (S-0268), drop topic tier to T1.

Q4 backprop hand-computation (w1=0.2, w2=0.5 → deltas and updated weights) spot-checked and arithmetically correct.

## ai-ml/llm-architectures

**Verdict: pass**

### Findings

1. `[minor]` `knowledge/ai-ml/llm-architectures/concept.md:27,29` — scaled-dot-product formula and O(n²) attention cost tagged `[T0]` but cite `[S-0272]` (Vaswani, `quasi-experiment` L4). Should be `[T1]`. Does not change the topic tier (T4 by frontier subject).

Otherwise exemplary T4 discipline: `review_after: 2027-02-17` in all three files, a `Volatility notes` section with honest `UNVERIFIED` markers (post-training recipes, quantization, frontier safety), claims current to 2025–2026 (Gemini 1.5, DeepSeek-R1). Chinchilla 20 tokens/param and InstructGPT 85% / 41%→21% figures correct.

## frontiers/agentic-systems

**Verdict: pass**

### Findings

None blocking. T4 with `review_after: 2027-02-17` in all three files; settled results (ReAct, SWE-bench, RAG) correctly T1, volatile practice (tools, workflows, memory, multi-agent) correctly T4. Honest `UNVERIFIED` markers (prompt injection, agent evals). `S-0278` shared-record use is sane (claims-supported lists both `ai-ml/llm-architectures` and `frontiers/agentic-systems`).

## frontiers/formal-verification-scale

**Verdict: pass**

### Findings

None blocking. T4 with `review_after: 2027-02-17`. Settled foundational claims correctly split from volatile tooling: undecidability `[T0][S-0058]` (Turing 1936, `proof` L1) and seL4 `[T0][S-0282]` (Klein et al., `proof` L1) are **correctly** proof-backed — the model the ai-ml T0 packs should have followed. seL4 ~8,700 LOC C + ~600 asm figures correct; AWS TLA+ (DynamoDB/S3 since 2011) correct.

## frontiers/post-quantum-cryptography

**Verdict: pass**

### Findings

None blocking. T4 with `review_after: 2027-02-17`. Shor's algorithm `[T0][S-0287]` (Shor 1997, `proof` L1) correctly proof-backed. FIPS 203/204/205 (Aug 13, 2024) and IR 8547 draft 2030/2035 dates correct; hybrid (X25519MLKEM768, RFC 9794) claims current and honestly dated. Grover/Regev/quantum-hardware correctly marked `UNVERIFIED`.

## frontiers/zero-knowledge-proofs

**Verdict: pass**

### Findings

1. `[minor]` `evidence/records/S-0294.md` vs `knowledge/frontiers/zero-knowledge-proofs/concept.md:37-39` — PLONK is classified `proof` L1, but its claims are tagged `[T1]`. Conservative under-grade; either downgrade the record (ePrint preprint, not peer-reviewed) or upgrade the claims.

**Focus point — S-0292 venue correction CONFIRMED:** web-verified, the journal version is SIAM J. Computing 18(1):186–208 (1989), conference version STOC 1985 — not JACM. The record's note is correct. GMR/FS `[T0]` claims correctly proof-backed (`proof` L1). Q6 Fiat-Shamir trace (n=35, s=4, r=11 → x=16, y=9, verify 9²≡x·v) spot-checked and correct.

## Records audit

| record | verdict | notes |
|---|---|---|
| S-0182 Codd 1970 | OK | practitioner L7 → T3; DOI correct |
| S-0183 Codd 1972 | OK | practitioner L7; used for T0 1NF/2NF claims → over-grade (see relational) |
| S-0184 Bernstein 1976 | OK | proof L1; typed correctly; TODS 1(4):277-298 correct |
| S-0187 Selinger 1979 | OK | practitioner L7 → T3 |
| S-0188 Leis 2015 | OK | observational L5 → T1; JOB 113 queries correct |
| S-0189 Graefe 1993 | OK | practitioner L7 → T3 |
| S-0192 Eswaran et al. 1976 | OK | proof L1 → T0 (2PL theorem) |
| S-0193 Gray 1978 | OK | practitioner L7 → T3 |
| S-0194 SQL-92 | OK | standard L6 → T2 |
| S-0197 Comer 1979 | OK | practitioner L7 → T3 |
| S-0198 O'Neil LSM 1996 | OK | practitioner L7 → T3 |
| S-0199 Silberschatz 2020 | OK | practitioner L7 → T3 |
| S-0200 Bayer & McCreight 1972 | OK | **focus (5): proof L1 justified** — peer-reviewed journal, height bound proven |
| S-0202 Özsu & Valduriez 2020 | OK | practitioner L7 → T3 |
| S-0203 Gray & Lamport 2006 | OK | proof L1 → T0 |
| S-0204 Spanner 2012 | OK | observational L5 → T1 |
| S-0207 Cohn 2009 | OK | practitioner L7 → T3 |
| S-0208 Inozemtseva & Holmes 2014 | OK | observational L5 → T1 |
| S-0209 Beck 2002 | OK | practitioner L7 → T3 |
| S-0212 Kuhn et al. 2004 | OK | observational L5 → T1; NIST figures correct |
| S-0213 Andrews et al. 2005 | OK | quasi-experiment L4 → T1 |
| S-0214 Papadakis et al. 2018 | OK | systematic-review L2 → T1 |
| S-0217 Luo et al. 2014 | OK | observational L5 → T1 |
| S-0218 Micco 2017 | OK | observational L5 → T1 |
| S-0219 Memon et al. 2017 | OK | observational L5 → T1 |
| S-0220 Jest docs | OK | practitioner L7 → T3; year 2014 = first release |
| S-0222 Bacchelli & Bird 2013 | OK | observational L5 → T1 |
| S-0223 Fagan 1976 | OK | observational L5 → T1 (single-company, but industrial data) |
| S-0224 Rigby & Bird 2013 | OK | observational L5 → T1 |
| S-0227 Tail at Scale 2013 | OK | observational L5 → T1 |
| S-0228 Dean 2007 | OK | practitioner L7 → T3 |
| S-0229 Knuth 1971 | OK | **focus (6): observational L5 → T1 is fair**; honestly dated |
| S-0232 FIPS 197 | OK | standard L6 → T2 |
| S-0233 Katz & Lindell 2020 | OK | practitioner L7 → T3 |
| S-0234 SP 800-175B | OK | standard L6 → T2 |
| S-0237 Kohnfelder & Garg 1999 | OK | practitioner L7 → T3 |
| S-0238 Schneier 1999 | OK | practitioner L7 → T3 |
| S-0239 MITRE ATT&CK | OK | practitioner L7 → T3 |
| S-0242 SP 800-63B-4 | OK | standard L6 → T2; reauth values web-verified correct |
| S-0243 RFC 6749 | OK | standard L6 → T2 |
| S-0244 RFC 7519 | OK | standard L6 → T2; "none" mandatory-to-implement correct (Sec. 8) |
| S-0247 OWASP Top 10 2021 | OK | practitioner L7 → T3 |
| S-0248 OWASP Cheat Sheets | OK | practitioner L7 → T3 |
| S-0249 RFC 6454 | OK | standard L6 → T2 |
| S-0252 NIST SSDF 800-218 | OK | standard L6 → T2 |
| S-0253 OWASP SAMM v2 | OK | practitioner L7 → T3 |
| S-0254 CVE Program | OK | practitioner L7 → T3 |
| S-0257 Kohavi 1995 | OK | quasi-experiment L4 → T1 |
| S-0258 Kaufman 2012 | OK | observational L5 → T1 |
| S-0259 Saito & Rehmsmeier 2015 | OK | observational L5 → T1; used for T0 → over-grade |
| S-0262 Breiman 2001 | OK | quasi-experiment L4 → T1 |
| S-0263 Friedman 2001 | OK | quasi-experiment L4 → T1 |
| S-0264 Cortes & Vapnik 1995 | OK | quasi-experiment L4 → T1 |
| S-0267 Rumelhart 1986 | OK | quasi-experiment L4 → T1; used for T0 → over-grade |
| S-0268 Goodfellow 2016 | OK | practitioner L7 → T3; used for T0 → over-grade |
| S-0269 Vaswani 2017 | **DUPLICATE** | identical to S-0272 ("Attention Is All You Need"). Consolidate |
| S-0272 Vaswani 2017 | **DUPLICATE** | identical to S-0269. Consolidate into one record, claims-supported = [neural-networks, llm-architectures] |
| S-0273 Hoffmann 2022 | OK | observational L5 → T1 |
| S-0274 Ouyang 2022 | OK | quasi-experiment L4 → T1 |
| S-0277 Yao 2023 (ReAct) | OK | quasi-experiment L4 → T1 |
| S-0278 Lewis 2020 (RAG) | OK | shared correctly (llm-architectures + agentic-systems) |
| S-0279 Anthropic 2024 | OK | practitioner L7 → T4 (volatile frontier guidance) |
| S-0280 SWE-bench 2024 | OK | quasi-experiment L4 → T1 |
| S-0282 seL4 2014 | OK | proof L1 → T0 (correctly used) |
| S-0283 AWS TLA+ 2015 | OK | observational L5 → T1 |
| S-0284 Woodcock 2009 | OK | systematic-review L2 → T1 |
| S-0287 Shor 1997 | OK | proof L1 → T0 (correctly used) |
| S-0288 FIPS 203 | OK | standard L6 → T2 |
| S-0291 IR 8547 | OK | standard L6 → T4 (draft, volatile — correct) |
| S-0292 GMR 1989 | OK | proof L1; **venue web-verified**: SIAM J. Comput 18(1), not JACM |
| S-0293 Fiat-Shamir 1987 | OK | proof L1 → T0 |
| S-0294 PLONK 2019 | OK (minor) | proof L1 vs T1 claims mismatch (conservative); ePrint not peer-reviewed |

Reused records (`S-0017`, `S-0018`, `S-0019`, `S-0020`, `S-0023`, `S-0034`, `S-0035`, `S-0036`, `S-0058`, `S-0110`, `S-0128`, `S-0139`): all consistent with their `hierarchy-level` and `claims-supported` fields; no conflicts detected.

## Cross-cutting findings

1. **`[critical]` Systematic T0 over-grading.** Five packs tag mathematically-exact definitions/theorems as T0 while citing only practitioner/textbook/observational records (levels 4–7): `sql-and-query-optimization`, `cryptography-basics`, `ml-fundamentals`, `supervised-learning`, `neural-networks`. The published precedent (`cs-foundations/logic-and-proof`) and hierarchy.md both require T0 ← level-1 proof records. The authors themselves classified the cited records (Rumelhart L4, Goodfellow L7, Saito L5, Graefe L7, Katz&Lindell L7) below level 1 — an internal contradiction. This is the single most important finding of the wave.
2. **`[critical]` Duplicate evidence record.** `S-0269` and `S-0272` are the same paper (Vaswani et al. 2017, "Attention Is All You Need", arXiv:1706.03762, NeurIPS 2017). Must be consolidated — the shared-record pattern (correctly used for S-0278, S-0203, S-0034) was violated here.
3. **`[major]` INDEX.md tiers are now wrong** (`INDEX.md` shows T0 for the five packs above). Regenerate after tier fixes (`tools/index.py`); per spec §6.3 the inventory must be synced when a pack's tier changes.
4. **`[minor]` `bloom_target` marker discipline.** Eight packs omit or misplace the `**bloom_target**` marker in `teaching.md` (crypto, threat-modeling, auth, web-security, secure-sdlc, ml-fundamentals, supervised, neural use `[Tier][S-…]` inline tags instead). Frontmatter `bloom_target` is correct everywhere; the teaching-file marker is inconsistent.
5. **`[minor]` validation.md format divergence.** `test-design-techniques` and `test-automation` use flat `- Q:` bullets without `### F#.` item headings; all other packs use headings. Both schema-valid; normalize for consistency.
6. **`[minor]` Under-grades (conservative).** SVM (S-0264 L4) tagged T3 in supervised-learning; PLONK (S-0294 L1) tagged T1 in ZK. Not misleading, but inconsistent with the record levels and the "strongest applicable level" rule.

## Fix list

1. **Downgrade five topics and re-tag their T0 claims** (mechanical, but L2 must re-verify after):
   - `data/sql-and-query-optimization`: tier T0 → **T1** (all three files); concept.md:28-30 `[T0]` → `[T3]`.
   - `security/cryptography-basics`: tier T0 → **T2**; concept.md:53 `[T0]` → `[T3]`.
   - `ai-ml/ml-fundamentals`: tier T0 → **T1**; concept.md:40-43 `[T0]` → `[T1]`.
   - `ai-ml/supervised-learning`: tier T0 → **T1**; concept.md:32-34 `[T0]` → `[T3]`.
   - `ai-ml/neural-networks`: tier T0 → **T1**; concept.md:25,26,31,36,41,43 `[T0]` → `[T1]`/`[T3]` per record.
2. **Consolidate duplicate record** `S-0269`/`S-0272` (Vaswani 2017) into one id; set `claims-supported: [ai-ml/neural-networks, ai-ml/llm-architectures]`; update both packs' citations and `sources`.
3. `data/relational-model`: concept.md:30-31 re-tag 1NF/2NF `[T0]` → `[T3]`; teaching.md:26 move `**bloom_target**` to the apply objective.
4. `data/indexing-and-storage`: teaching.md:39 fix `[15, 25]` → `[25]`.
5. Regenerate `INDEX.md` (`tools/index.py`) after steps 1–3 so the tier inventory is synced.
6. Add missing `**bloom_target**` markers in the eight teaching.md files (crypto, threat-modeling, auth, web-security, secure-sdlc, ml-fundamentals, supervised, neural).
7. (Optional) Normalize validation.md item-heading format across the two divergent packs; re-tag the conservative under-grades (SVM → T1, PLONK → T0) for full consistency.
