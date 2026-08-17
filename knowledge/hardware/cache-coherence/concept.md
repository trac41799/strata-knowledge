---
id: hardware/cache-coherence
title: Cache Coherence
band: B1
track: hardware
tier: T0
bloom_target: analyze
prerequisites: [hardware/memory-hierarchy, hardware/cpu-pipelining]
related: [systems-software/virtual-memory]
recommended: []
status: published
schema-version: 1
owner: l1-cache-coherence
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0038, S-0039, S-0040, S-0041]
---

# Cache Coherence

Multiple processors sharing memory each hold private cache copies of the same lines; coherence protocols are the distributed rules that keep those copies consistent.

## 1. The coherence problem

- Caches create multiple copies of one line; without coordination, a core can read a stale copy after another core wrote it [T3][S-0040]
- Coherence = the single-writer/multiple-reader (SWMR) invariant: a line is either cached for reading and writing in exactly one cache, or for reading in zero or more — and reads return the last write [T3][S-0040]
- A coherence protocol is the distributed rule set (cache + memory controllers) that enforces SWMR, propagates writes, and serializes them [T3][S-0040]
- Coherence governs accesses to one location; it says nothing about ordering across different locations [T3][S-0040]

## 2. Coherence vs memory consistency

- Sequential consistency (Lamport 1979): "the result of any execution is the same as if the operations of all the processors were executed in some sequential order, and the operations of each individual processor appear in this sequence in the order specified by its program" [T0][S-0038]
- CRITICAL distinction: a system can be fully coherent (SWMR holds) yet not sequentially consistent — coherence is per-location freshness, consistency is the cross-location ordering contract (SC/TSO/weak) [T3][S-0040]
- ISAs expose different consistency models as part of their contract (x86 TSO vs ARM/POWER weak); coherence hardware is mostly orthogonal to the model software relies on [T3][S-0040]

## 3. Snooping vs directory protocols

- Snooping: every cache watches all transactions on a shared, ordered interconnect and reacts; simple and low-latency, but broadcast traffic does not scale [T3][S-0040]
- Directory: the line's home node tracks sharers and sends point-to-point messages only to them; scales to many cores (CC-NUMA) at the cost of indirection latency and complexity [T3][S-0040]
- Directories were introduced to fix snooping's lack of scalability; the directory serializes requests per line [T3][S-0040]

## 4. MESI states and transitions

- MESI stable states: M = only copy, dirty (memory stale); E = only copy, clean; S = clean, copies may exist elsewhere; I = invalid [T3][S-0040]
- Local read: hit in M/E/S changes nothing; miss in I fetches the line — to E if sole sharer, else S [T3][S-0040]
- Local write: E/M hit → M silently (no traffic); S hit → upgrade (invalidate all other copies) → M; I miss → fetch-for-ownership (invalidate others) → M [T3][S-0040]
- Remote read of an M line: owner supplies data and writes back, line drops to S; remote write/invalidate: any state → I (write-back if M) [T3][S-0040]
- Eviction: M writes back then I; E/S can be dropped silently in snooping systems (directories require explicit PutS) [T3][S-0040]
- MOESI adds O (Owned): a dirty line that is also shared — the owner responds to misses without a write-back, memory stays stale (AMD; the primer's reference family) [T3][S-0040]
- MESIF adds F (Forward): exactly one sharer is designated responder for read requests, enabling a two-hop cache-to-cache response on point-to-point interconnects (Intel QPI) [T3][S-0041]
- MESI is a design space, not one standard: state sets, upgrade transactions, and eviction rules vary across implementations (MSI/MESI/MOESI/MESIF; write-once, Berkeley, Firefly, Dragon families) [T3][S-0040]

## 5. Invalidate vs update

- Write-invalidate: on a write, other copies are invalidated; their next read misses and refetches — traffic once per sharer per write [T3][S-0040]
- Write-update: the new value is broadcast to all sharers on every write — traffic scales with sharers × writes [T3][S-0040]
- Invalidation dominates in practice: update burns bandwidth on hot lines because traffic is proportional to sharers × writes [T3][S-0040]

## 6. Write/store buffers and ordering

- Store buffers let stores retire before draining to the cache hierarchy; local loads forward from the buffer, so a core sees its own store before other cores do [T3][S-0040]
- Buffering + forwarding enables store→load reordering as observed by other cores: two cores each storing a flag then loading the other's can both observe the old value — a result SC forbids [T3][S-0040]
- x86 is TSO-style: loads not reordered with loads, stores not reordered with older loads or other stores, but loads may pass older stores (store-buffer bypass) [T3][S-0040]
- ARM/POWER are weaker: no default ordering between independent accesses — order comes from explicit fences or acquire/release; a consistency fact, not a coherence failure [T3][S-0040]

## 7. False sharing

- False sharing: different processors access different words of one line; coherence transfers the whole line on each conflicting write though no data is actually shared [T1][S-0039]
- Measured in shared-memory workloads: coherence misses split into true- and false-sharing misses; false sharing grows with block size, flattening the miss-rate improvement larger blocks give uniprocessors — padding/alignment mitigates it [T1][S-0039]

## 8. Coherence in NUMA and scaling

- Coherence traffic (invalidations, forwards, write-backs) grows with core count × sharing frequency; snooping's broadcast model is capped at roughly a busload of processors [T3][S-0040]
- CC-NUMA distributes directories and home nodes; remote-node coherence operations cost far more than local ones, so data placement and sharing patterns dominate performance [T3][S-0040]

## 9. Protocol correctness

- Correctness = SWMR under all interleavings; real protocols add transient states (transitions are not atomic) and a serialization point (bus order or directory) for concurrent requests to one line [T3][S-0040]
- Protocols are specified as state/transition tables and validated with formal methods / model checking — the norm for complex directory protocols [T3][S-0040]

## Details — canonical MESI per-line transitions

| Event \ current state | M | E | S | I |
|---|---|---|---|---|
| local read hit | M | E | S | — |
| local write hit | M | E→M (silent) | S→M (invalidate others) | — |
| read miss (fetch) | — | — | — | E if sole sharer, else S |
| write miss (fetch + invalidate) | — | — | — | M |
| remote read (snoop) | S (+ write-back) | S | S (supply data) | — |
| remote write / invalidate | I (+ write-back) | I | I | — |

## Boundaries / common misunderstandings

- Coherence ≠ consistency: coherent memory can still reorder accesses; SC is an ordering contract over all locations, and few real ISAs deliver it [T3][S-0040][S-0038]
- MESI is a family, not one protocol: canonical tables differ from real products in upgrades, transient states, and evictions — and the state set is extended (MOESI's O, MESIF's F) [T3][S-0040][S-0041]
- x86 is not sequentially consistent: it is TSO; ARM/POWER are weaker still — "it runs on x86" is not an SC guarantee [T3][S-0040]
- Coherence does not fix races or provide atomicity: locks and atomics are a separate layer; coherent hardware still interleaves unsynchronized accesses as the consistency model allows [T3][S-0040]
- False sharing is a performance artifact, not a correctness bug or data race: no word is actually shared, yet lines bounce between caches [T1][S-0039]
- Store buffers do not break coherence — they relax ordering: SWMR still holds because coherence operates per line, while ordering concerns the access sequence cores observe [T3][S-0040]

## References (evidence records)

- S-0038 — Lamport (1979), IEEE Trans. Computers C-28(9):690-691 — sequential consistency
- S-0039 — Torrellas, Lam & Hennessy (1994), IEEE Trans. Computers 43(6):651-663 — false sharing
- S-0040 — Sorin, Hill & Wood (2011), Morgan & Claypool — coherence & consistency primer
- S-0041 — Goodman & Hum (2009), U. Auckland TR — MESIF protocol
