---
id: data/relational-model
title: Relational Model
band: B4
track: data
tier: T0
bloom_target: apply
prerequisites: [cs-foundations/discrete-mathematics, cs-foundations/logic-and-proof]
related: []
recommended: []
status: draft
schema-version: 1
owner: l1-relational-model
reviewed-by: []
updated: 2026-08-18
sources: [S-0182, S-0183, S-0184, S-0199, S-0194, S-0018]
---

# Relational Model — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the definition of a relation, a functional dependency, and each normal form 1NF–3NF/BCNF. (evidence: S-0182, S-0183, S-0184)
- understand — Explain data independence, why update anomalies arise from redundancy, and how SQL deviates from the pure model (bags, NULL, three-valued logic). (evidence: S-0182, S-0199, S-0194)
- apply — Given a schema and its FD set, find candidate keys, determine the normal form, decompose to 3NF/BCNF, and verify lossless join and dependency preservation. (evidence: S-0184, S-0199) — **bloom_target**
- analyze — Prove normal-form containment (BCNF implies 3NF) and explain why 3NF guarantees dependency preservation while BCNF does not. (evidence: S-0184)

## Worked example

### Part A — Find the problem: a table with redundancy

Context: `EMP(EmpID, EmpName, Dept, DeptLoc, ProjID, Hours)` with FDs `{EmpID -> EmpName, EmpID -> Dept, Dept -> DeptLoc, EmpID+ProjID -> Hours}`. A salesperson appears in many project rows.

Step 1 — Find the key. Closure of {EmpID, ProjID}: EmpID determines EmpName, Dept, DeptLoc; together with ProjID determines Hours. No proper subset determines the rest (EmpID alone does not give Hours). So the key is (EmpID, ProjID).

Step 2 — Predict the anomalies (before normalizing):
- Insertion: we cannot record a new employee who has no project yet (a NULL in the key is forbidden by entity integrity).
- Modification: an employee's DeptLoc is stored once per project row — changing the office requires updating every row (redundant copies of Dept -> DeptLoc).
- Deletion: deleting the last project row deletes the employee's department information too.

Step 3 — Check the normal forms. 1NF: all attributes atomic. 2NF: EmpID -> EmpName is a partial dependency (EmpID is a proper subset of the key) — violates 2NF. 3NF: EmpID -> Dept -> DeptLoc is a transitive dependency — violates 3NF. BCNF: EmpID -> Dept is a non-trivial FD whose determinant is not a superkey — violates BCNF.

Step 4 — Decompose along the violating dependencies:
- `EMP_BASE(EmpID, EmpName, Dept)` from EmpID -> EmpName, EmpID -> Dept.
- `DEPT(Dept, DeptLoc)` from Dept -> DeptLoc (separating the transitive chain).
- `ASSIGN(EmpID, ProjID, Hours)` keeps the key and the key-dependent attribute.

Step 5 — Verify the decomposition formally:
- Dependency preservation: every original FD appears in some component.
- Lossless join: ASSIGN join EMP_BASE on EmpID is lossless (EmpID is a key of EMP_BASE); the result joins DEPT on Dept losslessly (Dept is a key of DEPT). Global join = original data, no spurious tuples.
- Normal form: each component has a single-key dependency structure — all in BCNF.

### Part B — The trade-off, made visible

The same facts, denormalized: a read-heavy dashboard that always shows employee + department together now needs a join (ASSIGN x EMP_BASE x DEPT). The designer can keep a denormalized reporting table — accepting update anomalies — when reads dominate writes. Normalization is the formal guarantee; the engineering choice is separate. (evidence: S-0199)

## Elaboration prompts

- Why did Codd's 1970 paper describe data independence as a requirement, not an optimization? What could users NOT do in navigational systems that the relational model makes possible? (evidence: S-0182)
- The 3NF definition has two clauses ("X is a superkey OR A is a key attribute"). Build a schema that satisfies 3NF only through the second clause, and show which anomaly remains — that is exactly what BCNF removes. (evidence: S-0184)
- Bernstein's synthesis theorem says dependency-preserving lossless 3NF decomposition always exists. Why does the same guarantee fail for BCNF? Where does the proof rely on key attributes? (evidence: S-0184)
- SQL keeps duplicates unless DISTINCT is written. Translate "set semantics" into a SQL query that eliminates duplicates, and explain what the optimizer must do differently for bag vs set queries. (evidence: S-0194, S-0199)
- Entity integrity forbids NULL in keys, yet SQL allows composite keys with NULL parts. What does that inconsistency imply about "SQL = relational model"? (evidence: S-0194)

## Common misconceptions

1. **"A primary key makes a table normalized."** The key is 1NF-ish structure; 2NF/3NF/BCNF are separate properties of the FD set (partial and transitive dependencies), and a table with a key can still violate all of them. (evidence: S-0183, S-0199)
2. **"3NF is about splitting tables until nothing can be split."** Normal form is a property of dependency structure — no non-superkey determinants — and membership is relative to the stated FD set, not to how many pieces the schema has. (evidence: S-0184)
3. **"NULL is just another value like 0 or ''."** NULL is "unknown" in SQL: comparisons with NULL yield UNKNOWN, WHERE drops UNKNOWN rows, and `WHERE x = NULL` is a classic bug; `IS NULL` is the correct predicate. (evidence: S-0194)
4. **"Normalization is always the right design."** It trades update anomalies for join cost; read-heavy workloads legitimately denormalize or add materialized summaries. (evidence: S-0199)
5. **"SQL and the relational model are the same thing."** SQL has bag semantics, NULL with three-valued logic, and result ordering — deviations Codd later criticized; the algebra is set-based with two-valued logic. (evidence: S-0194, S-0199)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. What a relation is, and why "no duplicate rows" follows from it being a set. Grade against the definition claims. (evidence: S-0182)
2. Why storing one fact in several rows causes the "delete one thing and lose another" bug, and how splitting tables fixes it. Grade against the normalization claims. (evidence: S-0199, S-0184)
3. Why `WHERE dept = NULL` finds nothing, and what "unknown" means in a WHERE clause. Grade against the NULL/three-valued-logic claims. (evidence: S-0194)

## Interleaving hooks

- **cs-foundations/discrete-mathematics (prerequisite):** relations as subsets of Cartesian products, functions vs FDs — revisit R1–R3 in validation.md.
- **cs-foundations/logic-and-proof (prerequisite):** FD inference and the proof that BCNF implies 3NF are small deductive arguments; the closure computation is a fixed-point exercise.
- **data/sql-and-query-optimization (next topic):** every join in a query is a re-assembly of what normalization split apart — the cost of normalization shows up in the next pack.
- **data/indexing-and-storage (recommended chain):** keys become unique indexes; FKs become indexes chosen for join acceleration.
- **data/transactions-and-isolation (cross-link):** integrity constraints interact with concurrency (FK checks, unique violations under isolation levels).
