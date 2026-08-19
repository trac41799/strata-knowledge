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

# Transactions & Isolation

## Claims

- A transaction groups a set of database operations into one unit: either all take effect or none do; the ACID model — atomicity, consistency, isolation, durability — is the standard framing, implemented in practice by locking, multiversioning, and write-ahead logging [T3][S-0199][S-0193]
- Atomicity and durability are engine-enforced: the DBMS keeps a write-ahead log and forces the commit record to stable storage before acknowledging, so a crash can never lose a committed transaction or expose a partial one [T3][S-0193][S-0199]
- Consistency is an application-level invariant over the data: the DBMS preserves declared constraints (keys, referential integrity) but cannot infer business invariants, so ACID's C holds only relative to what the schema declares [T3][S-0199]
- A schedule is serializable when it is equivalent — for every possible initial state — to some serial execution of the same transactions; serializability is the formal correctness criterion that concurrency control aims at [T0][S-0192]
- Eswaran–Gray–Lorie–Traiger theorem: if every transaction obeys the two-phase rule — no lock is released before every lock it needs has been acquired — and requests are granted compatibly, then every schedule the system executes is serializable [T0][S-0192]
- Two-phase locking therefore splits each transaction into a growing phase (acquire) and a shrinking phase (release); releasing a lock early is exactly what breaks the serializability guarantee [T3][S-0199]
- Locks come in modes (shared/exclusive) and granularities (row, page, table, predicate); coarser granularity costs concurrency, finer granularity costs lock overhead, and intent locks make hierarchical locking safe [T3][S-0193][S-0199]
- Locking concurrency control can deadlock; DBMSs detect deadlock (waits-for graph, timeouts) and resolve it by aborting and restarting a victim [T3][S-0193][S-0199]
- SQL-92 — and every later SQL standard edition — defines four isolation levels, READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, and SERIALIZABLE, by the prohibited phenomena each guarantees against [T2][S-0194]
- The standard's phenomena are P1 (dirty read: reading a value written by an uncommitted transaction), P2 (non-repeatable read: a re-read within a transaction sees a different value), and P3 (phantom: a re-executed predicate query sees rows others inserted or removed) [T2][S-0194]
- Level by level: READ UNCOMMITTED prohibits none of P1–P3, READ COMMITTED prohibits P1, REPEATABLE READ prohibits P1–P2, and SERIALIZABLE prohibits P1–P3 [T2][S-0194]
- Lost update is not part of the SQL-92 taxonomy: the standard does not define it away, which is exactly how an anomaly can slip through levels that still forbid P1–P3 [T2][S-0194]
- In typical implementations the levels map to locking recipes: READ COMMITTED releases read locks at statement end, REPEATABLE READ holds them to transaction end, and SERIALIZABLE additionally takes range/predicate locks to stop phantoms [T3][S-0199]
- Multiversion concurrency control (MVCC) keeps old row versions so readers never block writers: each write creates a new version and each reader sees a consistent snapshot [T3][S-0199]
- Snapshot isolation — the MVCC mode used by several major DBMSs — gives a transaction a stable start-time snapshot and prevents dirty reads, non-repeatable reads, and phantoms for read-only transactions, but it is NOT serializable: write skew and serialization anomalies remain possible [T3][S-0199]
- Two-phase commit (2PC) coordinates atomicity across participants: a prepare phase collects votes, a commit phase broadcasts the decision, and any "no" vote forces abort [T3][S-0193]
- 2PC is blocking: after voting yes a participant cannot unilaterally abort (it might contradict a commit the coordinator decided) nor commit alone (it might violate atomicity), so coordinator failure leaves every yes-voter holding locks until recovery; Gray & Lamport prove commit protocols are consensus problems [T0][S-0203][S-0193]
- Non-blocking atomic commit therefore requires a majority-based consensus protocol such as Paxos Commit, which makes progress while a majority of coordinators are working [T0][S-0203]
- The deeper bound is FLP: in a fully asynchronous model every deterministic consensus protocol can run forever, which is why distributed transaction guarantees ultimately sit on the distributed-consensus limit [T0][S-0034]

## Details

- Write-ahead rule: log records are forced to stable storage before data pages are modified, and a commit is acknowledged only after its commit record is durable; crash recovery then redoes committed work and undoes uncommitted work [T3][S-0193][S-0199]
- 2PC phase by phase: the coordinator asks each participant to prepare; a participant votes yes only after logging its prepared state and holding its locks, and a "no" vote (or timeout) aborts; on unanimous yes the coordinator logs the decision and broadcasts Commit [T3][S-0193]
- A distributed transaction gets atomicity from its commit protocol, but isolation must still be implemented across nodes: 2PC provides no replica consensus or linearizability on its own, and the partition-level consistency/availability tradeoffs apply on top — see systems-software/distributed-consensus and data/distributed-databases [T0][S-0203]

## Boundaries / common misunderstandings

- Isolation levels are a menu of named anomaly permits, not a performance dial: dropping from SERIALIZABLE to READ COMMITTED accepts specific anomalies as a correctness decision, not a free speedup [T2][S-0194]
- "Serializable" is a property of schedules, not of locking: MVCC and optimistic (validation-based) concurrency control also aim at it, and snapshot isolation shows a mechanism can look safe yet permit write skew [T3][S-0199]
- Read-only transactions are not exempt: a read-only transaction under READ COMMITTED still suffers non-repeatable reads; isolation constrains what any transaction can observe, not what it writes [T3][S-0199]
- 2PC is not a consensus protocol for replica agreement: it pins a single decision across participants and blocks on coordinator failure; replacing it with Paxos/Raft-style consensus changes availability, not just implementation style [T0][S-0203]
- MVCC does not mean "no anomalies": it trades blocking for version management, and its classic snapshot isolation still permits write skew — choosing MVCC changes the anomaly menu, it does not remove the need for a serializability argument [T3][S-0199]

## References (evidence records)

- [S-0192] Eswaran, Gray, Lorie & Traiger 1976 — serializability + the 2PL theorem (CACM 19(11)).
- [S-0193] Gray 1978 — Notes on Data Base Operating Systems (LNCS 60): locking, logging, 2PC.
- [S-0194] ISO/IEC 9075:1992 (SQL-92) §4.35 — isolation levels and phenomena P1–P3.
- [S-0199] Silberschatz, Korth & Sudarshan 2020 — Database System Concepts, 7th ed.
- [S-0203] Gray & Lamport 2006 — Consensus on Transaction Commit (ACM TODS 31(1)).
- [S-0034] Fischer, Lynch & Paterson 1985 — FLP impossibility (JACM 32(2)).
