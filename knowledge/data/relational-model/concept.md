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

# Relational Model

## Claims

- The relational model, introduced by Codd (1970), organizes data as a collection of time-varying relations: each relation is a finite set of n-tuples, and each tuple is an ordered list of values drawn from the corresponding domains (sets of atomic values) [T3][S-0182].
- The model's core design move is data independence: users address data by content (relation and attribute names), never by physical position or access path, shifting responsibility for storage and efficient access to the data system [T3][S-0182][S-0199].
- Every relation has a key — a set of attributes whose values uniquely identify each tuple — and keys give the model its identity and update semantics [T3][S-0182][S-0199].
- Codd's 1970 paper defined the fundamental operations — selection, projection, and joins (the join expressed as natural composition of relations) — as set-at-a-time operations over relations [T3][S-0182].
- The relational algebra (selection, projection, join, set union/intersection/difference, renaming, division) is closed: every operation takes relations as input and yields a relation, so algebra expressions compose into nested query trees [T3][S-0199][S-0182].
- A functional dependency (FD) X -> Y holds in a relation when every two tuples equal on X are equal on Y; FDs are the formal language in which keys and normal forms are defined [T0][S-0184][S-0199].
- Candidate keys are the minimal attribute sets functionally determining the whole relation; a designer's chosen candidate key is the primary key, and normalization analyzes how non-key attributes depend on candidate keys [T0][S-0183][S-0184].
- First normal form (1NF) requires every attribute value to be atomic — a single value from its domain, not a set or nested structure; all higher normal forms presuppose 1NF [T3][S-0183][S-0199].
- Second normal form (2NF) eliminates partial dependencies: every non-key attribute depends on the whole candidate key, not on a proper subset of a composite key [T3][S-0183][S-0199].
- Third normal form (3NF) eliminates transitive dependencies: no non-key attribute depends on another non-key attribute (equivalently, every non-trivial FD X -> A has X a superkey or A a key attribute) [T0][S-0183][S-0184].
- Boyce-Codd normal form (BCNF) strengthens 3NF: every non-trivial FD must have a superkey as determinant; a relation in BCNF is automatically in 3NF, and BCNF removes the residual anomalies that non-superkey determinants permitted in 3NF [T0][S-0184][S-0199].
- Bernstein (1976) proved that any set of functional dependencies can be synthesized into a 3NF schema that preserves all dependencies and has the lossless-join property — the formal guarantee behind the standard design procedure [T0][S-0184].
- Decomposing by splitting off violating FDs is lossless for the join but is not guaranteed to preserve every FD: dependency preservation is a theorem with conditions, not a free property, which is the formal core of the 3NF-versus-BCNF trade-off [T0][S-0184][S-0199].
- The normal forms are strictly increasing in strength: 1NF (subset) 2NF (subset) 3NF (subset) BCNF — each admits a proper subset of the schemas of the previous [T0][S-0184][S-0199].
- Normalization eliminates update anomalies — insertion (cannot record a fact without another), deletion (removing one fact loses another), modification (redundant copies of a fact must be changed together) — which are the concrete symptoms of redundancy [T3][S-0199].
- The model includes integrity constraints: entity integrity (key attributes are never missing) and referential integrity (a foreign-key value must match an existing referenced key), enforced by the database [T3][S-0199].
- The international SQL standard implements the model's core notions — tables, keys, constraints, joins — but deviates from the pure model: multisets instead of sets, NULL, duplicate rows, and result ordering [T2][S-0194][S-0199].
- Missing values (NULL) are an SQL-era extension absent from Codd's 1970 formulation: SQL-92 defines NULL with three-valued logic (TRUE / FALSE / UNKNOWN), and predicates involving NULL evaluate to UNKNOWN rather than FALSE [T2][S-0194][S-0199].
- CS2023's Data Management knowledge area requires the relational model — relations, keys, functional dependencies, and normalization — as core material for computing graduates [T2][S-0018].

## Details

- Codd motivated the model by the weaknesses of the then-dominant navigational (record-at-a-time) systems, whose pointer-based access tied users to physical structure; the relational model is content-addressable and set-at-a-time [T3][S-0182].
- Referential integrity is enforced via foreign-key declarations; SQL-92 defines the enforcement actions (restrict, cascade, set null) as options of the referential constraint [T2][S-0194][S-0199].
- Normal-form membership is a property of a schema together with the set of functional dependencies assumed to hold: changing the FD set changes the normal form, so normalization analysis must start from a stated dependency set [T0][S-0184][S-0199].

## Boundaries / common misunderstandings

- "SQL is the relational model": SQL queries run over multisets with NULL and three-valued logic, while relational algebra operates on sets with two-valued logic; SQL is a derivative/superset of the algebra, not the algebra itself [T2][S-0194][S-0199].
- "A table with a primary key is normalized": keys alone give 1NF; eliminating partial and transitive dependencies (2NF, 3NF, BCNF) is a separate formal analysis of the FD set [T3][S-0183][S-0199].
- "Normalization means splitting tables until they cannot be split": the formal target is dependency structure — no non-superkey determinants — not decomposition for its own sake; beyond BCNF, 4NF/5NF target different dependency classes (multivalued dependencies, join dependencies) [T0][S-0184][S-0199].
- "NULL means the same as zero or empty string": in SQL semantics NULL denotes unknown; comparisons with NULL yield UNKNOWN, which filters rows out of WHERE results — the classic "WHERE x = NULL" trap [T2][S-0194].
- "A normalized schema is always better": normalization removes update anomalies at the cost of extra joins; for read-dominated workloads, deliberate denormalization or materialized summaries are a legitimate engineering trade [T3][S-0199].

## References (evidence records)

- [S-0182] Codd 1970 — A Relational Model of Data for Large Shared Data Banks (CACM 13(6)).
- [S-0183] Codd 1972 — Further Normalization of the Data Base Relational Model (Courant Symposia 6, Prentice-Hall).
- [S-0184] Bernstein 1976 — Synthesizing Third Normal Form Relations from Functional Dependencies (ACM TODS 1(4)).
- [S-0199] Silberschatz, Korth & Sudarshan 2020 — Database System Concepts, 7th ed. (McGraw-Hill).
- [S-0194] ISO/IEC 9075:1992 — SQL-92 standard.
- [S-0018] ACM/IEEE-CS/AAAI 2024 — CS2023.
