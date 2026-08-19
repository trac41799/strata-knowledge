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

# SQL & Query Optimization — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Name the stages of the query pipeline and the three join families (nested loop, hash, sort-merge) with their asymptotic costs. (evidence: S-0187, S-0189)
- understand — Explain why SQL is declarative, how bag semantics and NULL/three-valued logic deviate from relational algebra, and why cardinality estimation is the optimizer's weak link. (evidence: S-0194, S-0188) — **bloom_target**
- apply — Trace a SQL query through parse, optimization, and execution; estimate intermediate cardinalities; choose a join algorithm and access path for a given workload; diagnose a slow plan from EXPLAIN output. (evidence: S-0187, S-0189, S-0188, S-0199)
- evaluate — Compare alternative plans for a query (index vs scan, join order, join algorithm) given sizes and statistics, and justify the decision. (evidence: S-0187, S-0199)

## Worked example

### Part A — Trace a query plan end to end

Query: `SELECT o.order_id FROM orders o JOIN customers c ON o.cust_id = c.id WHERE c.country = 'DE' AND o.total > 100`.

Step 1 — Parse + semantics. Tables resolve, columns type-check, the FK direction (orders.cust_id -> customers.id) is recognized.

Step 2 — Logical optimization. Predicate pushdown moves `c.country = 'DE'` to a scan of customers and `o.total > 100` to a scan of orders, so filters run before the join. Join-order search: `(orders x customers)` vs `(customers x orders)` — the optimizer prefers the smaller filtered input as the outer (driving) side.

Step 3 — Physical planning with statistics: customers = 1M rows, 2% in DE (histogram) -> 20k rows; orders = 50M, 30% pass total > 100 -> 15M rows. Access paths: index scan on customers(country) (selective, 20k/1M = 2%), vs full scan on orders — or index on orders(total) if it exists. Join: with the DE filter driving, index-nested-loop (20k probes of the customers/orders index) beats hash join (build 15M-row table, probe 20k).

Step 4 — Execution. The executor pulls: Scan(customers, index on country) -> Filter(country='DE') -> [NestedLoop Join: for each outer row, probe orders index for cust_id and total>100] -> Project(order_id). Cost estimate for the plan: ~20k index probes + 15M-row scan — versus a hash join that must build the whole 15M filtered orders table.

Step 5 — The failure mode. If the histogram is stale (say 'DE' is really 40%, not 2%), the optimizer believes the filter passes 20k rows when it passes 400k — the cost model then picks hash join or a bad order, and the query runs 10-100x slower than the optimal plan. EXPLAIN ANALYZE shows "estimated rows = 20,000, actual rows = 400,000" — the diagnosis is estimation failure, and the fix is fresh statistics (or a rewritten predicate), not new hardware. (evidence: S-0187, S-0188, S-0199)

### Part B — Choose the join algorithm

Same tables, but now the query joins on the FK with no useful index and both inputs must be fully read: block-nested-loop does |B_orders| * |B_customers| page transfers; sort-merge sorts both (O(50M log 50M) comparisons) then merges; hash join builds a hash table on the smaller input (customers, 1M rows — fits memory) and probes with 50M rows: ~linear expected cost, the winner here. General rule from the survey: hash join for large equi-joins, index-nested-loop for selective index-backed joins, sort-merge for sorted/range joins. (evidence: S-0189)

## Elaboration prompts

- SQL says "what", not "how" — yet every database runs one concrete "how". Where exactly in the pipeline does the choice happen, and what information does the optimizer use? (evidence: S-0187)
- Why can two SQL queries that are logically identical (different join order written by the user) perform completely differently? What does that say about the optimizer's search space? (evidence: S-0187, S-0188)
- The JOB study separated estimation, enumeration, and cost modeling. Which component dominated the outcome, and why does that change where you invest effort as an engineer? (evidence: S-0188)
- Why is an index on a column with 3 distinct values nearly useless, while the same index shape on a high-cardinality column is essential? Trace the selectivity math. (evidence: S-0197)
- Bag semantics makes count(*) and DISTINCT behave differently from the relational algebra. Find one query where treating SQL as set semantics silently changes the result. (evidence: S-0194)

## Common misconceptions

1. **"SQL is relational algebra."** SQL is declarative with bag semantics, NULL/three-valued logic, duplicate retention, and ORDER BY — the pure algebra is set-based with two-valued logic; the standard-required behavior is the multiset behavior. (evidence: S-0194, S-0199)
2. **"The optimizer runs my join order."** Join order and access paths are the optimizer's choice from cost estimates; the written order is only the seed of the search. (evidence: S-0187)
3. **"Add an index and every query speeds up."** For low selectivity the optimizer correctly prefers a full scan, and each index adds write cost — index selection is workload-level, not per-query. (evidence: S-0197, S-0199)
4. **"The optimizer's row estimates are roughly accurate."** On the JOB benchmark, errors of several orders of magnitude are routine and are the dominant cause of slow queries — estimates are the weak link, not the cost model. (evidence: S-0188)
5. **"Faster hardware fixes slow queries."** Bad join orders multiply runtime by orders of magnitude, dwarfing linear hardware gains; fixing statistics and plans dominates hardware spend. (evidence: S-0188)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. How a SELECT statement becomes an execution plan, in five sentences, using "the database is the boss of the how". Grade against the pipeline claims. (evidence: S-0187, S-0199)
2. Why "the database guessed 20,000 rows but got 400,000" explains a 100x slowdown. Grade against the cardinality-estimation claims. (evidence: S-0188)
3. The difference between a sorted-merge marriage of two phone books and a hash-table marriage, and when each is better. Grade against the join-algorithm claims. (evidence: S-0189)

## Interleaving hooks

- **data/relational-model (prerequisite):** joins re-assemble what normalization split; bag vs set semantics and NULL are the deviations from the algebra — revisit R1–R3 in validation.md.
- **data/indexing-and-storage (recommended chain):** B+-trees, clustered vs secondary indexes, and buffer pools are the physical substrate every plan cost model assumes.
- **data/transactions-and-isolation (cross-link):** plan choice interacts with locking (locks per row/operator), and long-running bad plans collide with isolation more often than fast ones.
- **cs-foundations/complexity-theory (cross-link):** join costs are the complexity classes (|R|*|S| vs |R|+|S|) applied to real systems — hash join is the "hash table beats sort" moment at scale.
- **cs-foundations/probability-statistics (cross-link):** selectivity estimation is applied statistics — histograms, independence assumptions, and correlation are exactly the topics that fail on real data (S-0188).
