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

# Indexing & Storage — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Structure families
- Q: Name three index structure families and one defining property of each.
- bloom: remember
- bank: formative
- A: B-tree family — balanced multiway trees with page-sized nodes, ordered, supporting range scans. LSM tree — batched writes in a memtable cascaded to sorted disk runs via compaction, cheap writes at read-amplification cost. Hash index — near-constant point lookups, no ordering, equality-only.
- evidence: [S-0197][S-0198][S-0128]
- topic: data/indexing-and-storage

### F2. Height as I/O cost
- Q: Why is the B-tree height bound an I/O bound rather than just a CPU bound, and what is the height of a B-tree with n keys and fanout b?
- bloom: understand
- bank: formative
- A: Node size matches the storage page, so each node visit is exactly one page read from buffer pool or disk; with height Θ(log_b n), the number of pages read grows logarithmically in n. A balanced structure is what keeps the bound — one page per level, never more.
- evidence: [S-0200][S-0197]
- topic: data/indexing-and-storage

### F3. Leaf split trace
- Q: A B+ tree leaf holds at most 3 keys and currently contains [3, 5, 8]. Key 1 is inserted. Describe what happens, including what is promoted to the parent.
- bloom: apply
- bank: formative
- A: The full leaf splits into [1, 3] and [5, 8]; the separator key (smallest key of the right child: 5) is promoted to the parent. The tree stays balanced, and all leaves remain at least half full — the invariant that keeps the height logarithmic.
- evidence: [S-0197]
- topic: data/indexing-and-storage

### F4. Write amplification in LSM
- Q: Explain write amplification in an LSM tree: what happens to one logical insert over time, and which two costs follow?
- bloom: understand
- bank: formative
- A: The key moves from the memtable into a sorted run, and each compaction level may rewrite it — so physical bytes written far exceed logical bytes changed (the ratio is write amplification). Costs: flash wear/endurance and compaction CPU/bandwidth. In exchange, ingest writes are sequential and cheap.
- evidence: [S-0198][S-0128]
- topic: data/indexing-and-storage

## Summative (mastery checkpoint)

### S1. Structure selection for a workload
- Q: Workload: 10:1 read:write; 60% point lookups by id, 30% range scans by date, writes are bursty. Choose the primary structure, justify it, and name the tradeoff you accepted.
- bloom: analyze
- bank: summative
- A: B+ tree — it serves both point lookups and ordered range scans and keeps reads fast (one path, low read amplification); the accepted cost is per-write page updates (random I/O and write amplification). An LSM tree would win only if writes dominated and reads were point-heavy (with Bloom filters); it would accept read amplification and compaction cost instead.
- evidence: [S-0199][S-0128]
- topic: data/indexing-and-storage

### S2. Clustered + secondary design
- Q: Schema: orders(id PRIMARY KEY, customer_id, created_at). Design the index set and trace the query "all orders for customer X in July", counting row accesses.
- bloom: apply
- bank: summative
- A: Clustered index on id (the primary key); secondary index on (customer_id, created_at). The query uses the secondary index to find matching row references, then hops to each row through the clustered key — two page accesses per order unless the secondary index covers the needed columns. A leading customer_id keeps the scan targeted; the date filter prunes within it.
- evidence: [S-0199]
- topic: data/indexing-and-storage

### S3. Scan vs buffer pool
- Q: Why does a full table scan thrash a buffer pool even when the pool is large, and which cache design principle does this violate?
- bloom: understand
- bank: summative
- A: A scan touches every page once with no reuse — compulsory misses only, so the replacement policy keeps evicting pages that will never be needed again. The pool only pays off under locality, when the working set fits; scanning has no working set to exploit.
- evidence: [S-0199]
- topic: data/indexing-and-storage

## Review (spaced repetition — interleaved with prerequisites)

### R1. AMAT meets the page read (from memory-hierarchy)
- Q: In AMAT = hit time + miss rate × miss penalty, which term does a database page read most resemble, and how does the buffer pool attack it?
- bloom: understand
- bank: review
- A: A page miss is a miss with a huge penalty (nanoseconds in RAM vs milliseconds on disk). The buffer pool attacks the miss-rate term by keeping the hot working set resident; page-sized B-tree nodes keep the per-operation penalty small by limiting node visits to the height of the tree.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

### R2. Locality decides what caches can do (from memory-hierarchy)
- Q: A workload performs strided, near-random accesses. Why will cache-like designs fail, and which storage choices does that push toward?
- bloom: apply
- bank: review
- A: With no locality the working set exceeds any pool, so capacity misses dominate and hit rate collapses. This pushes toward structures that tolerate random small reads (hash indexes for point lookups) or convert them to sequential work (logs, LSM batching) — caches do not rescue patterns without locality.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

### R3. The primary key as index fodder (from relational-model)
- Q: Why is the primary key the natural clustered index key, and what happens to writes when it is a random UUID instead of a sequential value?
- bloom: understand
- bank: review
- A: Primary keys are unique, non-null, and the most common lookup path, so ordering the table by them pays for the hottest queries. Random UUID inserts scatter across the whole key space, splitting pages everywhere — random I/O and page churn (write amplification) — while sequential keys append at the right edge of the tree.
- evidence: [S-0199]
- topic: data/relational-model
