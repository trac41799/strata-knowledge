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

# SQL & Query Optimization — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. Declarative vs procedural
- Q: State the difference between a declarative and a procedural query, and identify which one SQL is.
- bloom: understand
- bank: formative
- A: A declarative query states the desired result and leaves the strategy to the system; a procedural query (e.g., record-at-a-time navigation, or explicit loops) states the steps. SQL is declarative: the query says what rows are wanted; the optimizer chooses access paths and join order.
- evidence: [S-0187]
- topic: data/sql-and-query-optimization

### F2. Bags vs sets
- Q: A table has two identical rows except for the primary key value. "SELECT dept FROM emp" returns how many rows if the table has 3 employees in dept 'X' and 2 in dept 'Y'? What changes if you add DISTINCT, and why does this difference matter versus relational algebra?
- bloom: understand
- bank: formative
- A: Without DISTINCT: 5 rows (duplicates retained — multiset semantics). With DISTINCT: 2 rows. Relational algebra operates on sets, where duplicates cannot exist at all, so SQL's default behavior is a deviation that makes count(*), aggregates, and optimizer rewrites behave differently than the set algebra would.
- evidence: [S-0194]
- topic: data/sql-and-query-optimization

### F3. Join algorithm choice
- Q: For each situation, name the best join algorithm: (a) 10 rows joined to 10,000 rows with a covering index on the big table; (b) two 1M-row tables, equi-join, no indexes; (c) two huge tables joined on a range predicate where both are pre-sorted.
- bloom: apply
- bank: formative
- A: (a) index-nested-loop join — probe the big table's index once per small row. (b) hash join — linear expected cost without indexes, beats sorting. (c) sort-merge join — inputs already sorted, merge is one pass; hash join cannot handle the range predicate.
- evidence: [S-0189]
- topic: data/sql-and-query-optimization

### F4. Cardinality errors
- Q: The JOB study showed cardinality estimates "off by several orders of magnitude" are routine. What is the primary downstream consequence, and which optimizer component is usually to blame?
- bloom: understand
- bank: formative
- A: Wrong estimates make the optimizer pick a bad join order and access path, turning fast queries into slow ones (order-of-magnitude runtime degradation). Estimation error is the dominant cause — bigger than enumeration or cost-model quality.
- evidence: [S-0188]
- topic: data/sql-and-query-optimization

## Summative (mastery checkpoint)

### S1. Trace a plan
- Q: For "SELECT o.id FROM orders o JOIN customers c ON o.cust_id = c.id WHERE c.country = 'DE' AND o.total > 100", walk the query pipeline from text to execution, naming each stage and one decision the optimizer makes at it.
- bloom: apply
- bank: summative
- A: (1) Parse: build the syntax tree. (2) Semantic analysis: resolve tables/columns, check types. (3) Logical optimization: push the country and total predicates down toward their base tables; choose a join order (e.g., customers first if the country filter is more selective). (4) Physical planning: pick access paths (index scan on customers.country, index scan or seq scan on orders.total) and a join algorithm (index-nested-loop if a useful index exists, else hash join). (5) Execution: a pull-based operator tree (scan -> filter -> join -> project) produces the result rows.
- evidence: [S-0187][S-0199]
- topic: data/sql-and-query-optimization

### S2. Estimate and correct
- Q: customers has 1M rows, country histogram says 2% are 'DE'; orders has 50M rows, 30% pass total > 100; assume every order has a customer. Estimate the intermediate cardinalities and join output. Then state which estimation assumption this math relies on and why it could be badly wrong.
- bloom: apply
- bank: summative
- A: Filtered customers: 1M * 0.02 = 20,000. Filtered orders: 50M * 0.30 = 15M. Join output: 15M * (20,000/1M) = 300,000 rows — this uses the containment assumption (every DE customer is represented in orders) and uniformity. It is badly wrong if DE customers order at a very different rate than others (attribute correlation): real output could be 10x larger or smaller, which flips the optimizer's join-order choice.
- evidence: [S-0187][S-0188]
- topic: data/sql-and-query-optimization

### S3. Diagnose with EXPLAIN
- Q: A query joins two large tables and runs 100x slower than expected. EXPLAIN shows the optimizer chose a nested-loop join with the wrong table as outer, and estimated rows are 10,000x lower than actual rows. Identify the root cause and propose three fixes.
- bloom: analyze
- bank: summative
- A: Root cause: cardinality estimation failure (the 10,000x gap is estimation error, which made the cost model prefer the wrong join order — the exact failure pattern the JOB study found). Fixes: (1) refresh statistics (ANALYZE/VACUUM ANALYZE) so histograms reflect current data; (2) rewrite the query or use join-order hints to force the correct order; (3) add/modify an index so the chosen algorithm can be index-nested-loop instead of block nested loop. Re-check with EXPLAIN ANALYZE that estimated rows now match actual rows.
- evidence: [S-0188][S-0199]
- topic: data/sql-and-query-optimization

### S4. Index decision
- Q: For a table with 100M rows queried by an equality on status (3 distinct values, evenly split) and by a range on created_at, decide between a secondary B+-tree index on status vs on created_at, and say when a full scan is still right.
- bloom: evaluate
- bank: summative
- A: Index on status is nearly useless for selective access: 33M rows pass any equality on it, so the optimizer should choose a full scan (sequential I/O beats index chasing plus heap lookups). Index on created_at supports range scans and is useful when the range is selective. A full scan remains right for low-selectivity predicates, unindexed sort/aggregate passes, and small tables where index overhead exceeds scan cost. The decision is the optimizer's access-path choice informed by selectivity, per the System R cost model.
- evidence: [S-0197][S-0187]
- topic: data/sql-and-query-optimization

## Review (spaced repetition — interleaved with prerequisites)

### R1. Bags vs relational algebra (from relational-model)
- Q: Why can a SQL SELECT return duplicate rows while relational algebra cannot, and what would Codd's algebra require to express "count employees per department"?
- bloom: understand
- bank: review
- A: SQL operates on multisets by default; algebra relations are sets, so duplicates are structurally impossible. In the algebra you would explicitly rename/project and the relation's set nature makes grouping explicit; in SQL, count(*) over grouped rows counts bag occurrences, which is why DISTINCT exists as an explicit bag-to-set operation.
- evidence: [S-0194]
- topic: data/relational-model

### R2. Keys become indexes (from relational-model)
- Q: A normalized schema has FKs everywhere. Why does normalization — which was introduced to remove redundancy — typically create a need for indexes, and which index structure is standard for the job?
- bloom: apply
- bank: review
- A: Normalization splits facts into separate relations, so queries must re-join them on key attributes; joins on FKs are cheap only with an index on the referenced key. The standard structure is the B+-tree, whose logarithmic-height search makes point lookups and range scans on the join key efficient — turning the formal cost of normalization (joins) into a physical access decision.
- evidence: [S-0197]
- topic: data/relational-model

### R3. NULL vs UNKNOWN in predicates (from relational-model)
- Q: The predicate "WHERE total > 100" silently excludes rows where total is NULL. Explain in terms of three-valued logic, and describe how this interacts with the optimizer's row-count estimates for the filter.
- bloom: apply
- bank: review
- A: NULL comparisons evaluate to UNKNOWN; WHERE keeps only TRUE rows, so NULLs are dropped silently. For estimation, the optimizer must know the fraction of NULLs (from statistics) to predict the filter's output; if it assumes no NULLs, the estimate overshoots and the plan for downstream joins can be badly wrong.
- evidence: [S-0194]
- topic: data/relational-model
