# L2 Wave 2 Review — 2026-08-18

## Summary

Verdicts: os-processes **pass**; os-scheduling **pass** (T0 raise correct); distributed-systems-basics **pass-with-fixes** (provenance bijection gap; frontmatter tier understated vs T0 Lamport claim); parallel-programming **pass-with-fixes** (frontmatter tier understated vs T0 Amdahl/Gustafson claims; S-0039/S-0103/S-0104 provenance bijection gap); containers-isolation **pass** (T2 raise correct); caching-strategies **pass** (T1 raise correct; NSDI figures web-verified); modularity **pass-with-fixes** (minor tier-convention); design-patterns **pass-with-fixes** (minor tier-convention); architectural-styles **pass-with-fixes** (frontmatter tier T2 vs T1 SMS claim); system-design-process **pass**; devops-pipeline **pass-with-fixes** (frontmatter tier T3 vs T1 DORA claims; numbers verified); observability **pass-with-fixes** (minor tier-convention); incident-response **pass-with-fixes** (minor tier-convention + one provenance-precision item); software-maintenance **pass-with-fixes** (S-0178 tier/record reconciliation). All three tier raises (os-scheduling T0, containers T2, caching T1) are **correct**. No pack fails on content accuracy, provenance existence, or pedagogy; every pack meets AC2 (≥6 Bloom items, ≥3 levels incl. bloom_target, canonical anatomy, clean topic ids, ≥1 worked example, ≥3 misconceptions). **Overall recommendation: do not block the wave — publish after the fix list below**; the material items are (1) two provenance-bijection gaps and (2) a systemic "topic tier = strongest claim tier" convention that was applied to three packs but not to eight others, requiring uniform application or a spec clarification.

## systems-software/os-processes

Verdict: **pass**

### Findings
1. [minor] `knowledge/systems-software/os-processes/concept.md:36` — fork/exec claim cites S-0112 (Ritchie & Thompson 1974) as a single mechanism; the claim is accurate, but "returning 0 in the child and the child's PID in the parent" is a POSIX behavior detail beyond what the 1974 paper documents. Suggested fix: keep S-0112 for the fork/exec *separation* claim and co-cite S-0032 for the return-value detail, or drop the detail.
2. [minor] `knowledge/systems-software/os-processes/concept.md:43` — the address-space/TLB-switch claim is tagged `[T3][S-0032]`; S-0032 is a textbook (level 7) so T3 is correct, but the TLB consequence is only lightly covered by S-0032's record text (which focuses on paging/VM). Suggested fix: acceptable as-is; optional co-cite of a virtual-memory record.

## systems-software/os-scheduling

Verdict: **pass** (T0 raise validated)

### Findings
1. [minor] `knowledge/systems-software/os-scheduling/concept.md:54` — the boundary claim "under overload EDF typically misses many deadlines" is tagged `[T0][S-0118]`. Liu & Layland prove optimality *within* the model; the overload-behavior statement is a known consequence, not part of the proof. Suggested fix: re-tag the overload clause T3 (or split the sentence) and keep the model-scope statement at T0.
2. [minor] `knowledge/systems-software/os-scheduling/concept.md:49` — CFS is correctly tagged T3 ("established practice"), a good contrast against the T0 proofs. No change needed; noted for accuracy.

T0 raise is correct: S-0117 (Smith 1956), S-0119 (Schrage 1968), S-0118 (Liu & Layland 1973) are all `type: proof`, `hierarchy-level: 1`, and the SJF/SRTF/EDF/RM claims are accurately stated formal results.

## systems-software/distributed-systems-basics

Verdict: **pass-with-fixes**

### Findings
1. [major] `knowledge/systems-software/distributed-systems-basics/concept.md:16` — frontmatter `sources: [S-0127, S-0128, S-0129]` omits S-0018, which is cited on the claim at `:27` ("codified curriculum knowledge units in the CS2023 Parallel & Distributed Computing KA [T2][S-0018]"). Spec §7 requires frontmatter `sources` to list every record backing the pack's own claims. Suggested fix: add S-0018 to `sources`.
2. [major] `evidence/records/S-0018.md:11` — `claims-supported` lists ten topics but omits `systems-software/distributed-systems-basics`, breaking the provenance bijection (§6.2/§6.7) for the claim at `concept.md:27`. Suggested fix: add the topic to S-0018's `claims-supported`.
3. [major] `knowledge/systems-software/distributed-systems-basics/concept.md:6` — frontmatter `tier: T2`, but the pack carries T0 claims (Lamport clocks, `concept.md:55-58,75`, backed by S-0127 `type: proof`, `hierarchy-level: 1`). Topic tier must equal the strongest claim tier (§6.3), so it should be **T0**. Suggested fix: raise frontmatter tier to T0, or reclassify the Lamport claims.
4. [minor] `knowledge/systems-software/distributed-systems-basics/concept.md:27` — the claim asserts the CS2023 "Parallel & Distributed Computing" KA specifically; S-0018's record text names "Systems Fundamentals" and 17 KAs but not the PDC KA. Suggested fix: note the PDC KA in S-0018, or soften the claim.

## systems-software/parallel-programming

Verdict: **pass-with-fixes**

### Findings
1. [major] `knowledge/systems-software/parallel-programming/concept.md:6` — frontmatter `tier: T1`, but the pack carries T0 claims (Amdahl's law `:32-34`, Gustafson's law `:35-36,53`, backed by S-0132/S-0133 `type: proof`, `hierarchy-level: 1`, whose record text explicitly says "Basis for the T0 … claims"). Topic tier must be **T0**. Suggested fix: raise frontmatter to T0, or downgrade the two laws + re-type the records to T1 (L2 decision; the proof records favor T0).
2. [major] `knowledge/systems-software/parallel-programming/concept.md:16` — frontmatter `sources: [S-0132, S-0133, S-0134]` omits S-0039, S-0103, S-0104, all cited on the pack's own claims (`:40-44,55-56`). Suggested fix: add the three ids to `sources`.
3. [major] `evidence/records/S-0039.md:10`, `S-0103.md:9`, `S-0104.md:9` — `claims-supported` omit `systems-software/parallel-programming` (they list `hardware/cache-coherence` and `programming/memory-model-and-pointers` only), breaking the bijection for claims at `concept.md:40-44,55-56`. Suggested fix: add the topic to each record's `claims-supported`.
4. [minor] `knowledge/systems-software/parallel-programming/concept.md:34` — "the Amdahl bound is exact — no schedule … can beat …" is a faithful statement of the algebraic bound given the fixed-size assumption (already stated at `:33`); accurate. No change.

## systems-software/containers-isolation

Verdict: **pass** (T2 raise validated)

### Findings
1. [minor] `evidence/records/S-0122.md:9` — OCI specs are typed `standard`/`hierarchy-level: 6`. OCI is a de-facto industry spec rather than an ISO/IEEE codified standard; this is defensible (hierarchy.md itself lists RFC 9111 under level 6), but it is a judgment call. Suggested fix: acceptable; optionally note "de-facto standard" in the record.

T2 raise is correct: NIST SP 800-190 (S-0124, `type: standard`, level 6) and CS2023 (S-0018, level 6) independently anchor T2, independent of the OCI classification. NIST claims (`concept.md:58-65`) accurately reflect SP 800-190's lifecycle model and shared-kernel risk framing.

## architecture-design/caching-strategies

Verdict: **pass** (T1 raise validated)

### Findings
1. [minor] `knowledge/architecture-design/caching-strategies/concept.md:65` — "Facebook's memcache fleet serves billions of requests per second and holds trillions of items" is accurate (web-verified against the NSDI paper's own phrasing). No change.

T1 raise is correct: S-0158 (Nishtala et al., NSDI 2013) is `type: observational`, `hierarchy-level: 5` → T1. The lease/thundering-herd/stale-set claims (`concept.md:45-46,51-53,59,65-66,71`) faithfully reproduce the paper, and the headline figure "17,000/s → 1,300/s" was web-verified against the paper text ("Without leases … 17K/s. With leases … 1.3K/s") and the "once per 10 seconds per key" lease rate.

## architecture-design/modularity

Verdict: **pass-with-fixes**

### Findings
1. [minor] `knowledge/architecture-design/modularity/concept.md:6` — frontmatter `tier: T3`, but the pack carries T2 claims (SWEBOK/CS2023: coupling/cohesion/separation-of-concerns at `:23,29-34,58`). Under the strict §6.3 rule the topic tier should be T2. Suggested fix: see Cross-cutting finding (tier convention); either raise to T2 or document the "substantive-tier vs framing-tier" convention.
2. [minor] `knowledge/architecture-design/modularity/teaching.md:30` lists an **evaluate** learning objective, but `validation.md` spans only remember/understand/apply (no evaluate item). AC2 is still met (≥3 levels incl. bloom_target "apply"). Suggested fix: add one evaluate-tagged review/summative item, or drop the evaluate objective.

## architecture-design/design-patterns

Verdict: **pass-with-fixes**

### Findings
1. [minor] `knowledge/architecture-design/design-patterns/concept.md:6` — frontmatter `tier: T3` vs a T2 claim (SWEBOK at `:26`). Same convention issue as modularity. Suggested fix: see Cross-cutting.
2. [minor] `knowledge/architecture-design/design-patterns/teaching.md:27-28` list **analyze**/**evaluate** objectives, but `validation.md` tops out at apply. AC2 met; optional alignment. Suggested fix: add an analyze/evaluate item (e.g., compare two candidate patterns).

## architecture-design/architectural-styles

Verdict: **pass-with-fixes**

### Findings
1. [major] `knowledge/architecture-design/architectural-styles/concept.md:6` — frontmatter `tier: T2`, but the pack carries a T1 claim (`concept.md:61`, "a systematic mapping study … found … few studies actually assess whether the benefits materialize [T1][S-0149]"). Topic tier must equal strongest claim tier → **T1**. Suggested fix: raise frontmatter to T1.
2. [minor] `evidence/records/S-0149.md:7` — records "January 2025" for IST vol. 177; the article appeared online October 2024 (web-verified via ResearchGate: "October 2024; Information and Software Technology 177(5):107590"). Authors, journal, volume, and article number are correct. Suggested fix: note "online October 2024, in-press January 2025".
3. Focus point 4 resolved: the T1 tag on the SMS claim **is correct**. S-0149 is `type: systematic-review`, `hierarchy-level: 2` (systematic mapping study = secondary/literature evidence → T1 per hierarchy.md). The claim is a faithful, correctly-hedged *meta-statement about the evidence base* ("drivers stated but benefits rarely assessed"), used to rebut the "microservices guarantee scalability" misconception — not an empirical measurement of microservices itself. The SMS wording (`concept.md:61`) matches the record's abstract.

## architecture-design/system-design-process

Verdict: **pass**

### Findings
1. [minor] `knowledge/architecture-design/system-design-process/concept.md:45` — ATAM stakeholder list ("managers, developers, maintainers, testers, reusers, end users, and customers") is plausible but is a specific enumeration not reproduced verbatim in S-0152's record text; mark UNVERIFIED as to the exact list, not the ATAM concept. Suggested fix: acceptable; optionally soften to "a representative set of stakeholders".

## operations/devops-pipeline

Verdict: **pass-with-fixes**

### Findings
1. [major] `knowledge/operations/devops-pipeline/concept.md:6` — frontmatter `tier: T3`, but the pack's core empirical content is T1 (DORA/Accelerate claims at `:24-32,39,44-45,49,51,53`, backed by S-0162/S-0163 `type: observational`, level 5). Topic tier must equal strongest claim tier → **T1**. Suggested fix: raise frontmatter to T1.
2. [minor] `knowledge/operations/devops-pipeline/concept.md:25` — "elite performers who meet reliability targets are 3.7x more likely to use [continuous testing]" — the 3.7× factor was not independently re-confirmed in this review; the continuous-testing-as-predictor claim is plausible but the exact multiplier is UNVERIFIED. Suggested fix: verify the 3.7× figure against the 2021 report or drop the multiplier.
3. Focus point 3 resolved: the elite-benchmark claim (`concept.md:32`) is **verified** — the DORA 2021 headline figures (973× more frequent deploys, 6570× faster lead time, 6570× faster recovery, 3× lower change failure rate, lead time <1 hour) are confirmed by Google Cloud's own DORA 2021 announcement. The mean-CFR detail (7.5% vs 23%) is consistent with the 2021 report but not independently re-confirmed here; the range "0–15%" is correct.

## operations/observability

Verdict: **pass-with-fixes**

### Findings
1. [minor] `knowledge/operations/observability/concept.md:6` — frontmatter `tier: T3` vs T2 claims (ISO 25010 at `:35`, ISO 12207 at `:36`, SWEBOK at `:37`). Same convention issue. Suggested fix: see Cross-cutting.
2. [minor] `knowledge/operations/observability/concept.md:26` — the OTel cardinality default "2,000 unique attribute combinations, overflow under `otel.metric.overflow=true`" is reproduced accurately from S-0168. No change.

## operations/incident-response

Verdict: **pass-with-fixes**

### Findings
1. [minor] `knowledge/operations/incident-response/concept.md:6` — frontmatter `tier: T3` vs a T2 claim (SWEBOK Operations KA at `:48`). Same convention issue. Suggested fix: see Cross-cutting.
2. [minor] `knowledge/operations/incident-response/concept.md:28` — "at most two paging events per 8–12 hour on-call shift" is cited to S-0167 (the 2016 SRE book). This guidance is more commonly attributed to the SRE Workbook (S-0173, "Being On-Call"); the SRE book's Monitoring chapter covers alert fatigue but the specific "two pages/shift" figure is UNVERIFIED as to exact source. Suggested fix: verify and co-cite S-0173 if that is the origin.
3. Focus point 5 resolved: S-0167/S-0173 overlap is **not a defect**. S-0167 (`claims-supported: [incident-response, observability]`) is a legitimate shared record; observability uses it for SLO/error-budget/golden-signals/alerting (ch. 4, 6), incident-response for lifecycle/roles/postmortem/MTTR/on-call — distinct, non-contradictory claims. S-0173 (Workbook) is correctly confined to on-call/playbook/severity/MTTR claims.

## operations/software-maintenance

Verdict: **pass-with-fixes**

### Findings
1. [major] `knowledge/operations/software-maintenance/concept.md:37-40` + `evidence/records/S-0178.md:3-4,9` — technical-debt claims tagged `[T3]` are backed by a record typed `anecdote`/`hierarchy-level: 8`. Focus point 2 resolved: **T3 is acceptable and must NOT be downgraded to T4** — the metaphor is 30 years canonical (high breadth of acceptance + currency), which per hierarchy.md's "hierarchy level + breadth of acceptance + currency" rule justifies T3; T4 (volatile/not-yet-consensus + `review_after`) would be wrong. However, the record's `type`/`hierarchy-level` fields are internally inconsistent with T3 (level 8 maps to no T3 line in the mapping table). Suggested fix: re-type S-0178 to `practitioner`/`hierarchy-level: 7` with a note ("primary source for the coinage; status since elevated to established practice"), or add an explicit cross-reference to a level-7 source (e.g., SWEBOK's technical-debt coverage) so the T3 claim is not a lone level-8 anchor.
2. [minor] `evidence/records/S-0177.md:9` — Lehman 1980 typed `observational`/level 5 (large-N); the underlying study is a longitudinal single-system (OS/360) investigation, arguably level 4 rather than level 5. The topic's T1 is independently anchored by S-0179 (Lientz & Swanson, 487 orgs, level 5), so the T1 topic tier stands regardless. Suggested fix: acceptable; optionally re-level S-0177 to 4 (still T1) for precision.

## Records audit

| record | verdict | notes |
|---|---|---|
| S-0112 | pass | Ritchie & Thompson 1974; practitioner/7; supports os-processes. Accurate. |
| S-0113 | pass | Love 2010; practitioner/7; task/CLONE_VM claims accurate. |
| S-0117 | pass | Smith 1956; proof/1; SJF optimality accurate. T0 correct. |
| S-0118 | pass | Liu & Layland 1973; proof/1; EDF/RM accurate. T0 correct. |
| S-0119 | pass | Schrage 1968; proof/1; SRTF optimality accurate. T0 correct. |
| S-0122 | pass (minor) | OCI specs; standard/6 → T2; de-facto vs ISO judgment call, acceptable. |
| S-0123 | pass | man-pages/kernel docs; practitioner/7; namespace/cgroup/chroot/pivot_root/overlayfs accurate. |
| S-0124 | pass | NIST SP 800-190; standard/6 → T2; lifecycle model accurate. |
| S-0127 | pass | Lamport 1978; proof/1; happened-before/clock condition accurate. T0 correct. |
| S-0128 | pass | Kleppmann DDIA; practitioner/7; failure/RPC/exactly-once accurate. |
| S-0129 | pass | Fallacies; practitioner/7; attribution (Deutsch 1994, Gosling ~1997) accurate. |
| S-0132 | pass | Amdahl 1967; proof/1; bound accurate. T0 correct (see frontmatter finding). |
| S-0133 | pass | Gustafson 1988; proof/1; scaled law accurate. T0 correct (see frontmatter finding). |
| S-0134 | pass | H&P 6e; practitioner/7; taxonomy/DLP-TLP/GPU claims accurate. |
| S-0137 | pass | Parnas 1972; practitioner/7; decomposition/information-hiding accurate. |
| S-0138 | pass | Conway 1968; practitioner/7; law accurately quoted; Datamation 14(4) vs (5) noted and reconciled. |
| S-0139 | pass | Feathers 2004; practitioner/7; seam definition accurate. |
| S-0142 | pass | GoF 1994; practitioner/7; 4 elements/23 patterns/5-7-11 families accurate. |
| S-0143 | pass | Larman 2002; practitioner/7; GRASP nine patterns accurate. |
| S-0144 | pass | Martin 2000; practitioner/7; SOLID + Feathers acronym attribution accurate. |
| S-0147 | pass | Garlan & Shaw 1994; practitioner/7; style definition accurate. |
| S-0148 | pass | Lewis & Fowler 2014; practitioner/7; microservices definition/characteristics accurate. |
| S-0149 | pass (minor) | Martínez Saucedo et al. 2025; systematic-review/2 → T1; web-verified (IST 177:107590); date should note Oct 2024 online. |
| S-0152 | pass | ATAM 2000; practitioner/7; sensitivity/tradeoff/risks accurate. |
| S-0153 | pass | Kruchten 4+1; practitioner/7; views accurate. |
| S-0154 | pass | Perry & Wolf 1992; practitioner/7; elements/form/rationale accurate. |
| S-0157 | pass | Hazelcast; practitioner/7; pattern taxonomy accurate. |
| S-0158 | pass | NSDI 2013; observational/5 → T1; 17K→1.3K and lease rate **web-verified**. |
| S-0159 | pass | Redis eviction; practitioner/7; maxmemory-policy/noeviction accurate. |
| S-0162 | pass | Accelerate 2018; observational/5 → T1; 4 metrics/24 capabilities accurate. |
| S-0163 | pass | DORA 2021; observational/5 → T1; 973×/6570×/3× **web-verified**; 7.5%/23% means plausible, not re-confirmed. |
| S-0164 | pass | Continuous Delivery 2010; practitioner/7; pipeline stages/blue-green attribution accurate. |
| S-0167 | pass | SRE book 2016; practitioner/7; shared incident-response+observability; accurate. |
| S-0168 | pass | OpenTelemetry; practitioner/7; signals/cardinality 2000 accurate. |
| S-0169 | pass | RED method; practitioner/7; RED/USE contrast accurate. |
| S-0173 | pass | SRE Workbook 2018; practitioner/7; on-call/playbook/MTTR accurate. |
| S-0174 | pass | Principles of Chaos 2017; practitioner/7; steady-state/control-group accurate. |
| S-0177 | pass (minor) | Lehman 1980; observational/5; level-5 vs level-4 judgment call (still T1). |
| S-0178 | pass-with-fix | Cunningham 1992; anecdote/8 backing T3 claims — T3 acceptable, but re-type to practitioner/7 (see finding). |
| S-0179 | pass | Lientz & Swanson 1980; observational/5; 487 orgs/55%/≥50% perfective accurate. |

Reused records (S-0032, S-0018, S-0009, S-0103, S-0104, S-0039, S-0017, S-0019, S-0020, S-0021, S-0022, S-0023) all exist, are correctly typed, and support their claims. Two bijection gaps: S-0018 (missing distributed-systems-basics), S-0039/S-0103/S-0104 (missing parallel-programming).

## Cross-cutting findings

1. **Tier-convention application is inconsistent.** The "topic tier = strongest claim tier" rule (§6.3 v1.1) was applied to exactly three packs (os-scheduling→T0, containers→T2, caching→T1) but not to eight others whose strongest claim outranks their frontmatter: distributed-systems-basics (T0 Lamport), parallel-programming (T0 Amdahl/Gustafson), architectural-styles (T1 SMS), devops-pipeline (T1 DORA), and modularity/design-patterns/observability/incident-response (T2 SWEBOK/ISO framing vs T3). Recommended resolution: either (a) apply the rule uniformly (raise all eight), or (b) amend §6.3 to distinguish "substantive claim tier" from "standard-membership framing tier" so peripheral T2 framing claims do not drive the topic tier — then document which interpretation was used and apply it consistently.
2. **Provenance bijection must be kept bidirectional.** Two packs cite records whose `claims-supported` does not list the pack, and whose frontmatter `sources` omits the record. Fix both directions in lockstep (see fix list). This is the highest-priority correctness issue.
3. **Cross-pack consistency is otherwise sound.** os-processes↔os-scheduling↔virtual-memory, containers↔virtual-memory, caching↔http-caching, observability↔incident-response, and software-maintenance↔software-lifecycle links are coherent; prerequisites resolve; interleaving hooks and review-bank `topic:` ids are clean and reference existing packs. The S-0167 shared record is used for disjoint claim sets.
4. **Single-tier-per-claim rule is satisfied** across all 14 packs — every claim line carries exactly one tier tag; multi-record claims correctly use the form `[T*][S-a][S-b]`.
5. **All 14 packs meet AC2** (≥6 Bloom-tagged items, ≥3 Bloom levels including `bloom_target`, canonical Q/bloom/bank/A/evidence/topic anatomy, clean topic ids, ≥1 worked example, ≥3 misconceptions). Model answers spot-checked for os-scheduling (SJF/RR/EDF arithmetic) and parallel-programming (Amdahl/Gustafson arithmetic) are numerically correct.

## Fix list

1. Add `S-0018` to frontmatter `sources` of `systems-software/distributed-systems-basics/concept.md` and add `systems-software/distributed-systems-basics` to `S-0018.md` `claims-supported`.
2. Add `S-0039, S-0103, S-0104` to frontmatter `sources` of `systems-software/parallel-programming/concept.md`, and add `systems-software/parallel-programming` to the `claims-supported` of `S-0039.md`, `S-0103.md`, `S-0104.md`.
3. Reconcile frontmatter `tier` for the eight packs flagged in Cross-cutting #1 (raise to the strongest claim tier, or amend §6.3 and apply the chosen interpretation uniformly). Highest-impact: parallel-programming→T0, distributed-systems-basics→T0, architectural-styles→T1, devops-pipeline→T1.
4. Re-type `S-0178.md` to `practitioner`/`hierarchy-level: 7` (or add a level-7 co-cite) so its T3 technical-debt claims are not anchored to a lone level-8 anecdote; retain the "coined by Cunningham 1992" fact.
5. Verify-or-drop the "3.7× continuous testing" multiplier in `devops-pipeline/concept.md:25`, and confirm the S-0163 mean-CFR figures (7.5%/23%) or mark the detail UNVERIFIED.
6. Confirm the "two paging events/shift" source in `incident-response/concept.md:28` and co-cite S-0173 if the Workbook is the origin.
7. Note S-0149's October-2024-online date; re-tag or split the "EDF under overload" clause in `os-scheduling/concept.md:54`.
8. Optional: add analyze/evaluate-tagged validation items to modularity and design-patterns to match their teaching objectives.
