---
id: data/sql-and-query-optimization
title: SQL & Query Optimization
band: B4
track: data
tier: T1
bloom_target: apply
prerequisites: [data/relational-model]
related: []
recommended: []
status: draft
schema-version: 1
owner: l1-sql-and-query-optimization
reviewed-by: []
updated: 2026-08-18
sources: [S-0187, S-0188, S-0189, S-0199, S-0197, S-0194]
---

# SQL & Query Optimization

## Claims

- SQL is declarative: a query states the desired result (the "what"), leaving the access strategy and execution order (the "how") to the system; choosing the "how" is the optimizer's job [T3][S-0187][S-0199].
- SQL result semantics are multiset (bag) semantics: without DISTINCT, duplicate rows are retained, and duplicate elimination is an explicit operation — differing from relational algebra's set semantics [T2][S-0194][S-0199].
- SQL implements three-valued logic: comparisons involving NULL yield UNKNOWN, and WHERE keeps only rows where the predicate is TRUE — codified in the SQL standard and a frequent source of "missing rows" bugs [T2][S-0194][S-0199].
- Query processing follows a pipeline: parse and semantic analysis, logical optimization (rewrites such as predicate pushdown and join-order selection), physical planning (access paths, join algorithms), and execution by a tree of operators that pull tuples between nodes [T3][S-0187][S-0189][S-0199].
- Cost-based optimization, introduced with System R, enumerates alternative plans, estimates each plan's cost from catalog statistics (cardinalities, selectivity factors, index fan-out), and picks the cheapest — the architecture still behind mainstream optimizers [T3][S-0187][S-0199].
- Nested-loop join evaluates the join predicate over pairs of tuples from the two inputs: worst case it performs |R|*|S| record comparisons; the block-nested-loop variant reduces I/O by scanning the inner input block-wise [T3][S-0189][S-0199].
- Sort-merge join sorts both inputs on the join key, costing O(|R| log|R| + |S| log|S|) comparisons plus a one-pass merge; it suits large inputs, pre-sorted inputs, and range join predicates [T3][S-0189][S-0199].
- Hash join builds a hash table on one input and probes with the other, achieving roughly O(|R| + |S|) expected work on the join key, with partition-and-spill when it exceeds memory; it wins on equi-joins of large unsorted inputs [T3][S-0189][S-0199].
- No join algorithm dominates: nested loop wins for small inputs, index-nested-loop for selective joins with an index, hash join for large equi-joins, sort-merge when sorted output is wanted — the choice depends on sizes, memory, and available indexes [T3][S-0189][S-0199].
- An index accelerates access to a relation for selective predicates; the optimizer chooses between an index scan and a full table scan from the estimated selectivity — the classic access-path decision formalized in System R [T3][S-0187][S-0197].
- B+-trees support point lookups and range scans with logarithmic page-access cost and are the standard index structure for disk-resident data; clustered indexes keep rows in key order while secondary indexes store key-to-rowid mappings and usually cost an extra lookup [T3][S-0197][S-0199].
- Cardinality estimation — predicting how many rows each operator outputs — is the weakest link of the optimizer: empirical measurement over the JOB benchmark (real-world schema, 113 realistic multi-join queries) shows estimates routinely off by several orders of magnitude, and estimation error is the dominant cause of bad plans, outweighing enumeration and cost-model quality [T1][S-0188].
- The standard estimation assumptions — uniformity of value distributions, independence between attributes, and containment — fail on real data: correlated attributes (e.g., release year and popularity) violate independence and produce wildly wrong selectivity estimates [T1][S-0188].
- Even with perfect cardinality estimates, no tested optimizer reliably found the optimal join order on the benchmark, and bad join orders degrade runtimes by orders of magnitude — join-order selection is inherently hard, not just poorly estimated [T1][S-0188].
- Query plans are inspectable via EXPLAIN-style facilities (operators, access paths, estimated vs actual row counts), which is the primary tool for diagnosing optimizer missteps in practice [T3][S-0199].

## Details

- System R computed join cardinality as the product of relation cardinalities and predicate selectivity factors — the origin of the independence assumption that later studies show to fail [T3][S-0187][S-0188].
- Join-algorithm choice is constrained by predicate shape: hash join requires an equi-join condition, while nested-loop and sort-merge variants also handle inequality joins [T3][S-0189][S-0199].
- Writing to a table costs extra with every index on it (index maintenance), so index selection is a workload-level decision, not a per-query one [T3][S-0197][S-0199].

## Boundaries / common misunderstandings

- "SQL is relational algebra": SQL is declarative with bag semantics, NULL/three-valued logic, duplicate retention, and result ordering (ORDER BY); the set-based equivalence that optimizers exploit holds only after explicit bag-to-set mapping [T2][S-0194][S-0199].
- "The optimizer executes joins in the order you wrote them": join order is chosen by the optimizer from cost estimates; the written order is only the start of the search space [T3][S-0187][S-0199].
- "An index always speeds a query up": for low-selectivity predicates the optimizer correctly prefers a full scan, and every extra index adds write cost [T3][S-0197][S-0199].
- "Cardinality estimates are roughly right": JOB measurements show errors of several orders of magnitude are routine across mainstream systems, and these errors are the main cause of slow queries [T1][S-0188].
- "EXPLAIN shows the best plan": it shows the chosen plan and its estimates; a bad plan usually means bad estimates, and the fix is fresher statistics, query rewriting, or hints — not reading the plan as gospel [T3][S-0199].
- "Bigger hardware fixes slow queries": plan suboptimality is multiplicative (orders of magnitude on benchmark queries), dwarfing linear hardware gains; fixing estimation and planning dominates hardware upgrades [T1][S-0188].

## References (evidence records)

- [S-0187] Selinger, Astrahan, Chamberlin, Lorie & Price 1979 — Access Path Selection in a Relational Database Management System (SIGMOD '79).
- [S-0188] Leis, Gubichev, Mirchev, Boncz, Kemper & Neumann 2015 — How Good Are Query Optimizers, Really? (PVLDB 9(3)).
- [S-0189] Graefe 1993 — Query Evaluation Techniques for Large Databases (ACM Computing Surveys 25(2)).
- [S-0199] Silberschatz, Korth & Sudarshan 2020 — Database System Concepts, 7th ed. (McGraw-Hill).
- [S-0197] Comer 1979 — The Ubiquitous B-Tree (ACM Computing Surveys 11(2)).
- [S-0194] ISO/IEC 9075:1992 — SQL-92 standard.
