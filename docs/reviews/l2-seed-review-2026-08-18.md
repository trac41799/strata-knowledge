# L2 Seed Review — 2026-08-18

## Summary

All five seed packs are technically sound and publishable in substance — I found no false or harmful claim, and every worked example and spot-checked model answer I traced is correct (MESI traces, Belady reference-string simulation, two-level page walk, Raft commit-under-leader-change, mark-sweep reachability, Ungar/Hertz-Berger numbers). The blockers are confined to citation integrity and metadata: one wrong DOI (S-0027), two evidence records with empty `claims-supported` (S-0009, S-0042), a frontmatter/references omission (S-0042 missing from consensus validation/teaching), a handful of minor imprecisions/overstatements in distributed-consensus, and an ambiguous vote-arithmetic scenario (consensus F5). Cross-packs are internally consistent (TLB-shootdown and fault-latency-ladder links agree). Verdict list: http-caching **pass** · garbage-collection **pass-with-fixes** · virtual-memory **pass** · distributed-consensus **pass-with-fixes** · cache-coherence **pass**.

## http-caching

Verdict: **pass** — all freshness/validation/directive claims match RFC 9111/9110/5861; validation (10 items, 4 Bloom levels incl. apply) and teaching (1 worked example, 5 misconceptions) exceed AC2.

### Findings

1. [minor] evidence/records/S-0009.md:10 — `claims-supported: []` is empty while concept.md attaches S-0009 to ~20 claims — breaks the `sources`/`claims-supported` bijection; fix: set `claims-supported: [systems-software/http-caching]`.
2. [minor] knowledge/systems-software/http-caching/concept.md:62 — `Vary: *` ("varies on all request header fields") is cited to S-0023 (RFC 9110), but the `*` wildcard semantics live in RFC 9111 §4.1; fix: add S-0009 to this claim's tag (harmless, but provenance should point at the caching RFC).

## garbage-collection

Verdict: **pass-with-fixes** — mechanism, generational, RC-cycle, and Hertz-Berger claims all verified correct (5x/3x/2x/70%/paging and "up to 9% faster" confirmed against the OOPSLA'05 paper); one records-level citation error (S-0027 DOI) must be fixed before publish.

### Findings

1. [major] evidence/records/S-0027.md:8 — DOI is wrong: `10.1145/1103845.1094836` should be `10.1145/1094811.1094836` (verified via Semantic Scholar / ACM); content of the record is accurate, but a bad DOI fails citation integrity (K2); fix: correct the DOI.
2. [minor] knowledge/programming/garbage-collection/concept.md:6 — frontmatter `tier: T1` while the dominant claim tier is T3 (S-0028 practitioner handbook; only lines 39 and 61–62 are T1) — tier-axis semantics ambiguous (strongest vs dominant claim); see Cross-cutting #1.
3. [minor] knowledge/programming/garbage-collection/concept.md:57 — "ZGC/Shenandoah (OpenJDK) target pause times of roughly 10 ms or less" is a reasonable T3 summary but undersells ZGC's current sub-millisecond goal; fix: soften to "on the order of tens of ms or less, down to sub-ms in recent ZGC".

## virtual-memory

Verdict: **pass** — address-translation, TLB, demand-paging, replacement (Belady, stack property), working-set/thrashing, COW, and mmap claims all correct; Belady DOI and Silberschatz 10th-ed ISBN verified; validation (11 items, 4 Bloom levels incl. apply) and teaching (2 worked examples, 6 misconceptions) exceed AC2.

### Findings

1. [minor] knowledge/systems-software/virtual-memory/concept.md:6 — `tier: T1` with a dominant T3 claim set (S-0032 textbook) plus one T0 claim (Belady, line 44) — same tier-axis ambiguity; see Cross-cutting #1.

## distributed-consensus

Verdict: **pass-with-fixes** — FLP/CAP/Paxos/Raft/PBFT statements are accurate (FLP DOI and venue verified); several small provenance and wording fixes needed before publish.

### Findings

1. [minor] evidence/records/S-0042.md:10 — `claims-supported: []` empty though concept.md cites S-0042 on Paxos claims (lines 31–33); fix: set `claims-supported: [systems-software/distributed-consensus]`.
2. [minor] knowledge/systems-software/distributed-consensus/concept.md:57-60 — References section omits S-0042 despite it being in frontmatter `sources` and cited on lines 31–33; fix: add the S-0042 reference line.
3. [minor] knowledge/systems-software/distributed-consensus/validation.md:16 and teaching.md:16 — `sources` lists only 4 records (S-0034…S-0037), omitting S-0042 present in concept.md:16; fix: add S-0042 to both frontmatter blocks.
4. [minor] knowledge/systems-software/distributed-consensus/concept.md:24 — Byzantine fault model ("node may behave arbitrarily") is cited to S-0037 (PBFT); the model is formally defined by Lamport/Shostak/Pease 1982 (The Byzantine Generals Problem), and the definition itself is T0 not T1; fix: add a Lamport-1982 record and re-tier, or reword to "…the failure class PBFT tolerates [T1][S-0037]".
5. [minor] knowledge/systems-software/distributed-consensus/concept.md:52 — "leader-based predecessors such as Viewstamped Replication and ZooKeeper" conflates a protocol (VR, Oki & Liskov 1988) with a service (ZooKeeper, built on ZAB) and mislabels ZooKeeper a "predecessor" of Raft; fix: drop ZooKeeper or reword to "VR and ZAB (ZooKeeper)".
6. [minor] knowledge/systems-software/distributed-consensus/concept.md:40 — "anchoring most later BFT designs (including blockchain BFT)" is a retrospective overstatement not established by PBFT's 1999 evaluation; fix: soften to "influencing later BFT designs".
7. [minor] knowledge/systems-software/distributed-consensus/concept.md:29 — "in the partially synchronous model any two of the three properties can be achieved" is a loose summary of Gilbert & Lynch; their nuance is that C+A becomes achievable under bounded-time assumptions; fix: reword to reflect that partial synchrony relaxes the tradeoff rather than guaranteeing arbitrary pairs.
8. [minor] knowledge/systems-software/distributed-consensus/validation.md:57-61 — F5 scenario arithmetic is inconsistent ("each receives exactly 2 votes" yet "the fifth server voted for one of them already", which would give 3 = majority); the conclusion (no majority → randomized timeouts) is correct but the premise should be cleaned up; fix: state votes explicitly (e.g., 2-2-1 with the last voter already committed).

## cache-coherence

Verdict: **pass** — SWMR/SC-vs-coherence/MESI/MOESI/MESIF/invalidate-vs-update/store-buffer/false-sharing claims all correct (Sorin/Hill/Wood DOI verified verbatim; MESIF technical report confirmed real); validation (11 items, 5 Bloom levels incl. analyze) and teaching (2 worked examples, 5 misconceptions) exceed AC2.

### Findings

1. [minor] knowledge/hardware/cache-coherence/concept.md:6 — `tier: T1` with a T0 claim (SC definition, line 32) and dominant T3 claim set (S-0040) — same tier-axis ambiguity; see Cross-cutting #1.

## Records audit

| record id | verdict | notes |
|---|---|---|
| S-0009 | minor-fix | RFC 9111 real & correct; `claims-supported` empty. |
| S-0023 | ok | RFC 9110 real & correct. |
| S-0024 | ok | RFC 5861 real; correctly noted as incorporated into RFC 9111. |
| S-0026 | ok | Ungar 1984 verified — 13%→1.5% (8×) and 1.7× match the paper verbatim. |
| S-0027 | **doi-wrong** | Hertz & Berger 2005 real, numbers verified; DOI `1103845` must be `1094811`. |
| S-0028 | ok | Jones/Hosking/Moss 2nd ed. 2023 verified — ISBN 978-1-032-21803-8 and DOI 10.1201/9781003276142 correct. |
| S-0030 | ok | Belady/Nelson/Shedler 1969 verified — CACM 12(6):349–353, DOI 10.1145/363011.363155. |
| S-0031 | ok | Denning 1968 working-set paper real & canonical; DOI 10.1145/363095.363141 plausible (UNVERIFIED precision). |
| S-0032 | ok | Silberschatz/Galvin/Gagne 10th ed. 2018 verified — ISBN 978-1-119-43925-7 correct. |
| S-0034 | ok | FLP 1985 verified — JACM 32(2):374–382, DOI 10.1145/3149.214121. |
| S-0035 | ok | Gilbert & Lynch 2002 SIGACT News 33(2) real & canonical (UNVERIFIED DOI precision). |
| S-0036 | ok | Raft, USENIX ATC '14 real & correct. |
| S-0037 | ok | PBFT, OSDI '99 real & correct. |
| S-0038 | ok | Lamport 1979 SC paper real & correct. |
| S-0039 | ok | Torrellas/Lam/Hennessy 1994 real & correct. |
| S-0040 | ok | Sorin/Hill/Wood 2011 verified — DOI 10.2200/S00346ED1V01Y201104CAC016 matches verbatim. |
| S-0041 | ok | Goodman & Hum 2009 MESIF Auckland TR verified real; QPI-derivation claim matches the paper. |
| S-0042 | minor-fix | Lamport "Paxos Made Simple" 2001 real (UNVERIFIED DOI precision); `claims-supported` empty. |

## Cross-cutting findings

1. **Tier-axis semantics ambiguous.** http-caching declares T2 (matches its dominant/only tier), but GC/VM/consensus/coherence declare T1 while their claim sets span T0 (FLP/CAP/SC/Belady proofs) through T3 (practitioner/textbook) — so `tier` is currently "strongest" in some packs and "dominant" in others. This affects topic-inventory.yml ordering and any tier-filtering. Fix: document one convention in spec §6.3 (recommend "highest tier among published claims", which would make distributed-consensus T0), then reconcile frontmatter + inventory.
2. **Validation item anatomy is not uniform.** Only cache-coherence emits `distractors`; only GC/VM/consensus/coherence emit `topic`; http-caching emits neither — yet spec §7 lists both in the item anatomy. Fix: standardize fields (and decide whether `distractors` is required for all banks, especially formative).
3. **No substantive inter-pack contradictions found.** VM↔coherence TLB-shootdown framing, VM↔GC fault-latency ladder (~5–6 orders of magnitude), and consensus↔http-caching (different layers) are all consistent.
4. **Provenance bijection under-enforced.** Two cited records (S-0009, S-0042) carry empty `claims-supported`; `tools/lint.py` should verify the reverse direction (every record cited by a topic lists that topic), per spec §6.7/hierarchy.md.

## Fix list

1. Fix S-0027 DOI: `10.1145/1103845.1094836` → `10.1145/1094811.1094836`.
2. Set `claims-supported: [systems-software/http-caching]` on S-0009 and `claims-supported: [systems-software/distributed-consensus]` on S-0042.
3. Add S-0042 to distributed-consensus validation.md and teaching.md `sources`, and to concept.md References section.
4. Document tier-axis semantics (strongest vs dominant) in spec §6.3 and reconcile frontmatter + docs/topic-inventory.yml.
5. Reword consensus concept.md lines 24, 29, 40, 52 (Byzantine-model provenance, CAP "any two", "blockchain BFT anchoring", "ZooKeeper as predecessor").
6. Fix F5 vote arithmetic in consensus validation.md (lines 57–61).
7. Uniformly apply `distractors`/`topic` fields across validation packs.
