---
id: data/transactions-and-isolation
title: Transactions & Isolation
band: B4
track: data
tier: T0
bloom_target: apply
prerequisites: [data/relational-model]
related: [systems-software/distributed-consensus, data/distributed-databases]
recommended: []
status: draft
schema-version: 1
owner: l1-transactions-and-isolation
reviewed-by: []
updated: 2026-08-18
sources: [S-0192, S-0193, S-0194, S-0199, S-0203, S-0034]
---

# Transactions & Isolation — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Isolation level taxonomy
- Q: Name the four SQL isolation levels and, for each, which of the phenomena P1, P2, P3 it must exclude.
- bloom: remember
- bank: formative
- A: READ UNCOMMITTED (excludes none of P1–P3), READ COMMITTED (P1), REPEATABLE READ (P1–P2), SERIALIZABLE (P1–P3). The level names are defined by these exclusions, nothing more.
- evidence: [S-0194]
- topic: data/transactions-and-isolation

### F2. The three phenomena
- Q: In one sentence each, state P1 (dirty read), P2 (non-repeatable read), and P3 (phantom), and which party — reader or writer — causes each.
- bloom: understand
- bank: formative
- A: P1 — a reader sees a value written by a transaction that later aborts (the writer's uncommitted state leaks). P2 — a value changes between two reads inside one transaction because another transaction committed (the reader's snapshot moves). P3 — a predicate query returns different row sets across executions because another transaction inserted or deleted matching rows and committed (row locks can't lock rows that don't exist yet).
- evidence: [S-0194]
- topic: data/transactions-and-isolation

### F3. Anomaly classification
- Q: T1 reads balance = 500. T2 subtracts 100 and commits. T1 re-reads balance = 400 and its checksum logic breaks. Which anomaly is this, and what is the minimum isolation level that prevents it?
- bloom: apply
- bank: formative
- A: Non-repeatable read (P2): the value changed between two reads inside T1 because T2 committed. READ COMMITTED only excludes P1, so REPEATABLE READ (or SERIALIZABLE) is the minimum level that prevents it.
- evidence: [S-0194]
- topic: data/transactions-and-isolation

### F4. Isolation level choice
- Q: An analytics job reads the accounts table twice and must see identical rows; a comment feed tolerates new comments appearing between page loads. Choose an isolation level for each and justify.
- bloom: apply
- bank: formative
- A: Analytics needs REPEATABLE READ (stable re-reads; P2 excluded) — READ COMMITTED would let the second pass differ. The comment feed can run READ COMMITTED: its named anomaly (non-repeatable reads) is business-tolerable. The choice must name the accepted anomaly, not just pick a level.
- evidence: [S-0199]
- topic: data/transactions-and-isolation

## Summative (mastery checkpoint)

### S1. Write skew under snapshot isolation
- Q: Two doctors; invariant "at least one doctor is on call". T1 reads both on-call flags (1,1), then sets A off-call. T2 reads both (1,1), then sets B off-call. Both commit. Why does snapshot isolation allow this, and what would prevent it?
- bloom: analyze
- bank: summative
- A: Each transaction reads the same start-time snapshot (both on call) and the writes touch disjoint rows, so MVCC's conflict check sees no conflict and both commit — yet the combined outcome (nobody on call) is not serializable: no serial execution produces both flips. Prevention: serializable isolation, explicit locks on the scanned rows (SELECT ... FOR UPDATE), or application-level retry when the snapshot version changes. The lesson: SI's guarantee set is not serializability.
- evidence: [S-0199]
- topic: data/transactions-and-isolation

### S2. 2PC blocking trace
- Q: Coordinator C crashes after participants P1 and P2 have voted yes, before sending Commit. Can either participant decide alone? Name the failure mode and say whether safety or liveness is lost.
- bloom: apply
- bank: summative
- A: No — committing alone could break atomicity if the other aborts; aborting alone could contradict a commit C had already decided. Both hold locks and wait for C to recover: this is blocking. Safety (agreement on commit/abort) is preserved; liveness (progress) is lost. Gray & Lamport show commit is a consensus problem, so non-blocking commit needs a majority-based protocol (e.g., Paxos Commit).
- evidence: [S-0203]
- topic: data/transactions-and-isolation

### S3. Two-phase rule mechanics
- Q: State the two-phase rule and explain why obeying it yields serializable schedules; what exactly goes wrong if a transaction releases a lock before acquiring all the locks it needs?
- bloom: understand
- bank: summative
- A: Rule — no lock released before every lock the transaction requires has been acquired. With compatible granting, every schedule is then serializable (Eswaran–Gray–Lorie–Traiger). Early release lets other transactions read data that is still being modified (uncommitted reads and cascading dependences), producing schedules with no serial equivalent.
- evidence: [S-0192]
- topic: data/transactions-and-isolation

## Review (spaced repetition — interleaved with prerequisites)

### R1. Constraints define "consistency" (from relational-model)
- Q: Why must a primary key be unique and non-null, and how does that constraint shape what ACID's "C" can mean?
- bloom: understand
- bank: review
- A: Uniqueness and nullability are declared constraints the engine enforces mechanically. ACID's consistency is therefore only guaranteed relative to declared schema constraints — business invariants (e.g., "balance never negative") are enforced by the engine only if declared (CHECK) and otherwise are the application's job. A transaction layer cannot invent invariants the schema never declared.
- evidence: [S-0199]
- topic: data/relational-model

### R2. Enforced vs application invariants (from relational-model)
- Q: Given customers(id PRIMARY KEY, name, balance) and orders(id, customer_id REFERENCES customers), which invariants does the DBMS enforce and which does it not — and which of the not-enforced ones can a transaction still not rescue?
- bloom: apply
- bank: review
- A: Enforced: primary-key uniqueness, foreign-key referential integrity. Not enforced: balance >= 0 (a business invariant) unless declared as a CHECK constraint. Transactions preserve consistency only within declared constraints — concurrent schedules can still violate an undeclared invariant (that is precisely what write-skew and lost-update scenarios demonstrate), so the invariant must be declared or checked by the application.
- evidence: [S-0199]
- topic: data/relational-model
