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

# Relational Model — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. Functional dependency
- Q: State the formal definition of a functional dependency X -> Y, and write it down for the FD "Dept -> DeptLoc" in a table of employees.
- bloom: remember
- bank: formative
- A: For every pair of tuples t1, t2 in relation R: if t1[X] = t2[X] then t1[Y] = t2[Y]. For Dept -> DeptLoc: any two employee rows with the same Dept value must have the same DeptLoc value — it is a fact about the dependency set, not about current data contents.
- evidence: [S-0184]
- topic: data/relational-model

### F2. Data independence
- Q: What does "data independence" mean in Codd's 1970 model, and what change in database architecture did it enable?
- bloom: understand
- bank: formative
- A: Users address data by content (relation name + attributes), not by physical position or access path; the system — not the application — chooses how data is stored and found. This freed applications from physical storage structure and made content-addressable, set-at-a-time querying possible.
- evidence: [S-0182]
- topic: data/relational-model

### F3. Candidate keys
- Q: Given R(A, B, C, D) with FDs {AB -> C, C -> D, D -> B}, find all candidate keys and the normal form of R.
- bloom: apply
- bank: formative
- A: Compute closures: AB+ = {A,B,C,D}; AC+ = {A,C,D,B} (C -> D, D -> B); AD+ = {A,D,B,C} (D -> B, AB -> C). So AB, AC, AD are all candidate keys, and every attribute is prime. R is in 3NF (all attributes are key attributes). It is NOT in BCNF: C -> D has determinant C, which is not a superkey. Answer: keys AB/AC/AD; 3NF, not BCNF.
- evidence: [S-0184]
- topic: data/relational-model

### F4. NULL trap
- Q: The query "SELECT * FROM emp WHERE dept = NULL" returns zero rows even though employees without a department exist. Explain exactly why, and give the correct predicate.
- bloom: apply
- bank: formative
- A: NULL is "unknown", not a value. The comparison dept = NULL evaluates to UNKNOWN, and WHERE keeps only rows where the predicate is TRUE — UNKNOWN rows are dropped. Correct predicate: "dept IS NULL". This is three-valued logic (TRUE/FALSE/UNKNOWN), defined by the SQL standard.
- evidence: [S-0194]
- topic: data/relational-model

## Summative (mastery checkpoint)

### S1. Normalize a schema
- Q: Relation R(A, B, C, D) has FDs {A -> B, B -> C, D -> A}. Find the key, identify the anomalies, decompose R to normal form, and verify lossless join and dependency preservation.
- bloom: apply
- bank: summative
- A: Key: D (D+ = {D,A,B,C}). Violations: A -> B and B -> C have non-superkey determinants. Decompose per FD: R1(A,B) [A -> B], R2(B,C) [B -> C], R3(D,A) [D -> A]. Each component's determinant is its key, so all are in BCNF. Lossless: R1 join R2 on B is lossless (B is a key of R2); then join with R3 on A is lossless (A is a key of the join of R1,R2 since A+ = {A,B,C} covers it). Dependencies: every FD appears in a component, so all are preserved.
- evidence: [S-0184][S-0199]
- topic: data/relational-model

### S2. 3NF versus BCNF
- Q: Give a schema where 3NF preserves all FDs but every BCNF decomposition loses one, and explain why that makes 3NF the pragmatic design target.
- bloom: analyze
- bank: summative
- A: R(A, B, C) with FDs {AB -> C, C -> B}. Keys: AB and AC (both attribute sets; C -> B, so AC determines everything). C -> B violates BCNF; the BCNF decomposition splits into (C,B) and (A,C), losing AB -> C (no component contains both A and B). The 3NF decomposition can keep (A,B,C) plus a relation for the violating FD, preserving everything. 3NF guarantees a dependency-preserving lossless schema (Bernstein's theorem); BCNF does not, so 3NF is the standard guaranteed target.
- evidence: [S-0184]
- topic: data/relational-model

### S3. Integrity design
- Q: Design the integrity constraints for two tables — orders(id, customer_id, total) and customers(id, name, country) — and say what each constraint protects against.
- bloom: apply
- bank: summative
- A: customers.id primary key (entity integrity: not null, unique — every customer has one identity); orders.id primary key; orders.customer_id foreign key referencing customers.id with a chosen action (e.g., restrict to prevent deleting a customer who has orders). The FK guarantees referential integrity: no order may reference a nonexistent customer, and no customer row may be deleted while referenced (depending on the action). Also NOT NULL on total if every order has one.
- evidence: [S-0199][S-0194]
- topic: data/relational-model

## Review (spaced repetition — interleaved with prerequisites)

### R1. Relations in set theory
- Q: A mathematical relation is a subset of a Cartesian product. How does Codd's "relation" generalize this, and what does the set view imply about duplicate rows?
- bloom: understand
- bank: review
- A: Codd's relation is a finite set of n-tuples over n domains — i.e., a subset of the Cartesian product D1 x D2 x ... x Dn. Because it is a set, duplicate tuples cannot exist: two rows equal on all attributes are the same element. This is why SQL's duplicate-retaining (bag) semantics is a deviation from the pure model.
- evidence: [S-0182]
- topic: cs-foundations/discrete-mathematics

### R2. BCNF implies 3NF
- Q: Prove, from the definitions only, that every relation in BCNF is in 3NF. Where does the argument use the difference between a superkey and a key attribute?
- bloom: analyze
- bank: review
- A: 3NF permits non-trivial FDs X -> A only when X is a superkey OR A is a key attribute. BCNF requires the stronger condition that every non-trivial FD has X a superkey. Since the BCNF condition implies the 3NF condition for every FD, any BCNF schema satisfies the 3NF condition — so BCNF (subset) 3NF. The slack is exactly the case where a 3NF schema allows a non-superkey determinant whose dependent is a key attribute.
- evidence: [S-0184]
- topic: cs-foundations/discrete-mathematics

### R3. Functions vs functional dependencies
- Q: Contrast a function f: X -> Y in set theory with a functional dependency X -> Y in a relation. What is preserved, and what is different (e.g., partial functions, relation-to-relation mapping)?
- bloom: understand
- bank: review
- A: Both assert determinism: equal inputs give equal outputs. A function maps every element of X to exactly one element of Y; an FD allows some X values to appear with several Y values only if X is not complete — and, unlike a function, an FD is a constraint a relation happens to satisfy (the relation may also hold pairs not covered by the function's domain). FDs constrain the relation's semantics; functions are total mappings. This is why FD closure is studied with inference rules rather than function composition.
- evidence: [S-0184]
- topic: cs-foundations/discrete-mathematics
