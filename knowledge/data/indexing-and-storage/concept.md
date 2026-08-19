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
status: draft
schema-version: 1
owner: l1-indexing-and-storage
reviewed-by: []
updated: 2026-08-18
sources: [S-0197, S-0198, S-0199, S-0128, S-0200]
---

# Indexing & Storage

## Claims

- A storage structure is a point on a tradeoff surface, not a universal winner: B-trees, LSM trees, and hash indexes each optimize a different mix of point lookups, range scans, and write cost [T3][S-0199][S-0128]
- A B-tree is a balanced multiway search tree: every node holds at most b keys and b+1 children, and all leaves sit at the same depth; with n keys the height is Θ(log_b n), so every lookup, insert, and delete touches O(log_b n) nodes [T0][S-0200][S-0197]
- B-tree node size is chosen to match the storage page, so one node visit equals one page read; this is what turns the height bound into a real I/O count [T3][S-0197][S-0199]
- Inserting into a full B-tree node splits it into two nodes and pushes the middle key up to the parent; splits propagate upward and can split the root, growing the tree by exactly one level — the tree is always balanced [T3][S-0197][S-0199]
- Deletions that underfill a node are repaired by borrowing from or merging with a sibling, preserving the height bound [T3][S-0197]
- The B+ tree — the standard relational index — keeps all records in leaves, stores keys only in internal nodes, and links leaves in key order, making range scans a sequential leaf walk [T3][S-0197][S-0199]
- With page-sized nodes, fanout reaches hundreds of keys per node, so a few levels (≈4–5) index billions of keys; each level costs one page read [T3][S-0199]
- An LSM tree batches writes in a memory-resident memtable and cascades sorted runs to disk through merge-sort-style compaction, converting random page writes into sequential batch writes [T3][S-0198]
- LSM trades read amplification and space amplification for low write cost: a point lookup may need to check several runs, while writes are cheap — the tradeoff quantified in the original LSM cost analysis [T3][S-0198]
- Bloom filters speed LSM point lookups by testing, cheaply and approximately, whether a run could contain a key, skipping runs that cannot [T3][S-0128]
- Hash indexes give near-constant point lookups but no ordering: they suit equality-only workloads and underpin log-based in-memory engines (Bitcask-style: append to a log, keep a hash map in memory) [T3][S-0128][S-0199]
- A clustered index orders the table's rows by its key, so row data lives in the index leaves and key-ordered access is sequential; a table can have at most one clustered index [T3][S-0199]
- Secondary indexes map keys to row references (primary key or row id), so a secondary lookup costs an extra hop to the row, and scanning a secondary index is not table-ordered [T3][S-0199]
- Tables are stored in fixed-size pages; a slotted-page layout holds a slot array plus variable-length records so records can move within a page without invalidating external references [T3][S-0199]
- The buffer pool caches database pages in memory: the DBMS routes every page request through it and a replacement policy (LRU and variants) evicts pages; the pool hit rate, not raw device speed, determines effective I/O cost [T3][S-0199]
- Database storage exploits the memory hierarchy: hot pages live in the buffer pool while data and log files sit on SSD/HDD, and the nanoseconds-to-milliseconds latency gap is why storage structures are page-oriented rather than pointer-chased — see hardware/memory-hierarchy and hardware/storage-devices [T3][S-0199]
- Write amplification — the ratio of physical bytes written to logical bytes changed — is the central cost of update-heavy designs: LSM compaction rewrites the same data repeatedly and amplifies flash wear, while B-tree updates rewrite only the affected pages [T3][S-0128][S-0198]

## Details

- Index choice by access pattern: point lookups → hash or B-tree; range scans, ORDER BY, and prefix matches → B-tree; insert-heavy append-heavy workloads with cheap writes → LSM; the query planner picks among them from the predicate (see data/sql-and-query-optimization) [T3][S-0199]
- A covering index includes all columns a query needs, eliminating the secondary-index hop entirely [T3][S-0199]
- The write-ahead log is append-only and sequential; LSM's advantage over in-place B-trees is precisely that it makes the data path as sequential as the log [T3][S-0128]

## Boundaries / common misunderstandings

- An index is not a blanket speedup: low-selectivity predicates, full scans, and tiny tables get no benefit, and every index is maintained on every write — more indexes mean slower writes and more storage [T3][S-0199]
- B-trees are not binary trees: a node holds dozens to hundreds of keys, and the "B" never had an agreed-upon meaning [T3][S-0197]
- LSM is not "faster than B-trees": it is faster for writes and usually slower and more variable for reads; read-heavy workloads still favor B-trees, which is why both coexist [T3][S-0128]
- A clustered index does not make every query fast: it orders by exactly one key; lookups on any other column fall back to scans or secondary indexes with the extra hop [T3][S-0199]
- Hash indexes cannot replace ordered structures: without key order there are no range scans, no ORDER BY, no prefix queries, and durability requires an accompanying log [T3][S-0128][S-0199]
- A bigger buffer pool is not automatically faster: scan-heavy workloads with no reuse thrash any pool, because capacity only helps when there is locality to exploit [T3][S-0199]

## References (evidence records)

- [S-0200] Bayer & McCreight 1972 — the original B-tree paper (Acta Informatica 1(3)).
- [S-0197] Comer 1979 — The Ubiquitous B-Tree (ACM Computing Surveys 11(2)).
- [S-0198] O'Neil et al. 1996 — The Log-Structured Merge-Tree (Acta Informatica 33(4)).
- [S-0199] Silberschatz, Korth & Sudarshan 2020 — Database System Concepts, 7th ed.
- [S-0128] Kleppmann 2017 — Designing Data-Intensive Applications, ch. 3 (storage engines).
