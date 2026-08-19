---
id: data/indexing-and-storage
title: Indexing & Storage
band: B3
track: data
tier: T0
bloom_target: apply
prerequisites: [data/relational-model, hardware/memory-hierarchy]
related: [data/sql-and-query-optimization, hardware/storage-devices, data/distributed-databases]
recommended: [data/transactions-and-isolation]
status: published
schema-version: 1
owner: l1-indexing-and-storage
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0197, S-0198, S-0199, S-0128, S-0200]
---

# Indexing & Storage — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Enumerate the index structure families (B-tree, LSM, hash) and the storage vocabulary: fanout, memtable, compaction, slotted page, buffer pool, write amplification. (evidence: S-0197, S-0198, S-0199)
- understand — Explain why B-tree height is an I/O bound, why LSM trades read amplification for write cost, and why secondary lookups cost an extra hop. (evidence: S-0200, S-0198, S-0199)
- apply — Trace B+ tree insert/split and LSM write paths, and choose a structure and index set for a given workload. (evidence: S-0197, S-0199) — **bloom_target**
- analyze — Given a workload profile, justify the structure and index choices by the amplification and page-access costs they accept. (evidence: S-0199, S-0128)

## Worked example — B+ tree insert/split trace

Rules: leaves hold at most 3 keys; internal nodes hold at most 2 keys; separator promoted on split = smallest key of the right child.

- **insert 10, 20, 5** → leaf [5, 10, 20]. Height 1 — the root is a leaf.
- **insert 15** → leaf full → split into [5, 10] | [15, 20], promote 15 → root [15], leaves [5, 10] and [15, 20].
- **insert 12** → [5, 10, 12]. No split.
- **insert 25, 30** → right leaf [15, 20, 25] then full → split [15, 20] | [25, 30], promote 25 → root [15, 25].
- **insert 7** → left leaf [5, 7, 10, 12] full → split [5, 7] | [10, 12], promote 10 → root [10, 15, 25] — now 3 keys, over the internal limit of 2.
- **root split** → new root [15]; its children are the internal nodes [10] and [25]; leaves: [5, 7], [10, 12], [15, 20], [25, 30]. Height 2.

Read the result: lookup of 12 reads root → [10] → leaf [10, 12]: 3 page reads for 8 keys, and a lookup never visits more levels than the height. Range [10, 25] walks the leaf chain left to right. Every leaf is at least half full — the invariant that keeps height Θ(log_b n) (S-0200, S-0197).

## Worked example (mini) — the LSM write path

A stream of inserts arrives; the memtable holds ~100 keys. Flush → run R1 (100 sorted keys on disk). More inserts; flush → R2. Background compaction merges R1 and R2 into one sorted run R12, deleting duplicates. Trace costs: a point lookup may probe memtable, then R2, then R1 — up to 3 run reads (read amplification 3). Meanwhile key k was physically written at flush and again at compaction — write amplification ≈ 2 at this level, growing with deeper levels. In exchange, no insert ever caused a random page write. (S-0198, S-0128)

## Elaboration prompts

- The height bound Θ(log_b n) is exact. Why does the fanout b matter more than n for real databases — what changes if keys shrink from 128 bytes to 32? (evidence: S-0200)
- B+ trees keep records only in leaves. What does the internal/leaf split buy for range scans, and what would a pure B-tree cost for the same query? (evidence: S-0197)
- In the LSM mini-example, Bloom filters remove most run probes. Which reads do they *not* help, and why is that acceptable for LSM's target workloads? (evidence: S-0128)
- The secondary index "hop" is one page read per row. When does that stop being an acceptable cost, and what two designs remove it? (evidence: S-0199)
- Write amplification is defined as a ratio. Compare the ratio of a B-tree page update, an LSM flush+compaction, and an append-only log write — which is cheapest and why? (evidence: S-0128)

## Common misconceptions

1. **"B-tree is just a balanced binary tree."** B-trees are multiway: a node holds dozens to hundreds of keys, which is what collapses height to a handful of levels; a binary search tree would need ~30 levels for a billion keys. The "B" never had an agreed meaning. (evidence: S-0197)
2. **"Adding an index always speeds up queries."** Every index must be maintained on every write and consumes storage; low-selectivity predicates and full scans get no benefit, and the planner may ignore a useless index. (evidence: S-0199)
3. **"LSM trees are strictly better than B-trees."** They are better for writes, worse and more variable for reads; read-heavy workloads still favor B-trees, which is why production systems ship both. (evidence: S-0128)
4. **"Write amplification only matters on flash."** It costs CPU and bandwidth everywhere: on HDDs it shows up as extra seeks and transfers, on SSDs it burns endurance — the ratio is a cost, not a durability footnote. (evidence: S-0198)
5. **"A secondary index lookup is free."** It is a table-order-independent structure: every row found costs a hop to the clustered index or heap, two page reads per row unless the index covers the query. (evidence: S-0199)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why finding a record in a table with a billion rows can cost only 4–5 page reads, and why the fanout — not the table size — sets that number — grade against the height claims. (evidence: S-0200)
2. Why a system that "never overwrites, only appends" writes fast but reads slowly, and what the cleanup pass (compaction) does — grade against the LSM and write-amplification claims. (evidence: S-0198)
3. Why a dictionary ordered alphabetically with definitions inline (clustered) differs from an index at the back that points to pages (secondary) — and when you need both — grade against the clustered/secondary claims. (evidence: S-0199)

## Interleaving hooks

- **hardware/memory-hierarchy (prerequisite):** AMAT's miss penalty is the whole reason page-sized nodes exist — review bank items R1/R2 connect the two packs.
- **data/relational-model (prerequisite):** primary keys and uniqueness determine the natural clustered key and its write behavior — R3 in validation.md.
- **data/sql-and-query-optimization (related):** the planner chooses among the index structures this pack describes — revisit index choice when studying join and access-path selection.
- **data/transactions-and-isolation (recommended):** MVCC keeps old versions, so index pages must store version chains; ask how a B+ tree layout accommodates multiple versions of one row under snapshot isolation.
