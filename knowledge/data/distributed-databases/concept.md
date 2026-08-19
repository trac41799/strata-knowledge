---
id: data/distributed-databases
title: Distributed Databases
band: B5
track: data
tier: T0
bloom_target: apply
prerequisites: [data/transactions-and-isolation, systems-software/distributed-systems-basics]
related: [systems-software/distributed-consensus, data/sql-and-query-optimization, data/indexing-and-storage]
recommended: []
status: draft
schema-version: 1
owner: l1-distributed-databases
reviewed-by: []
updated: 2026-08-18
sources: [S-0018, S-0034, S-0035, S-0128, S-0202, S-0203, S-0204]
---

# Distributed Databases

## Claims

- A distributed database presents a single logical database over data stored at multiple sites; the field decomposes into data distribution (partitioning), replication, distributed query processing, and distributed transaction management [T3][S-0202].
- Distributed databases and cloud computing form a knowledge unit of the CS2023 Data Management KA, covering distributed storage, distributed query processing, and the distributed transaction model [T2][S-0018].
- Partitioning (sharding) splits a dataset across nodes such that each record is owned by exactly one node; queries are routed only to nodes holding relevant partitions [T3][S-0128].
- Hash partitioning spreads writes evenly across shards but destroys ordered access, while range partitioning keeps keys ordered for range scans but concentrates hot keys into single shards [T3][S-0128].
- The partition key determines colocation: records sharing a key land on the same node, enabling single-partition transactions and joins; a poor key choice forces every related query across shards [T3][S-0128].
- A transaction touching multiple partitions requires cross-node coordination, so distributed databases push users toward keys that colocate related data and keep transactions single-partition [T3][S-0128].
- Replication models fall into single-leader, multi-leader, and leaderless (quorum) replication, trading write throughput, failure tolerance, and consistency [T3][S-0128].
- Atomic consistency (linearizability) and availability cannot both be guaranteed during a network partition (CAP); when no partition occurs, both can hold [T0][S-0035].
- Leader-based strong consistency acknowledges a write only after it is durably stored (e.g., on a quorum of followers), trading latency for the guarantee that acknowledged writes survive failover [T3][S-0128].
- Eventual consistency guarantees that replicas converge once writes stop; until then, reads may return stale data and the system stays available [T3][S-0128].
- Quorum-based leaderless replication uses overlapping read/write quorums (W + R > N) to trade consistency for latency; an acknowledged write is read by the next read only if quorums intersect [T3][S-0128].
- Read replicas scale read throughput by spreading reads across followers; writes still pass through the leader, and asynchronous replication means a read can return data older than the last acknowledged write [T3][S-0128].
- Two-phase commit (2PC) coordinates an atomic all-or-nothing outcome across participants: a prepare phase collects votes, a commit phase broadcasts the decision, and any "no" vote forces abort [T3][S-0128].
- Two-phase commit is blocking: if the coordinator fails after a participant has voted yes, that participant cannot safely decide alone and must wait for recovery; Gray & Lamport prove commit protocols are consensus problems, so non-blocking atomic commit requires a consensus-based protocol such as Paxos Commit [T0][S-0203][S-0034].
- Spanner, Google's globally distributed database, runs two-phase commit over Paxos-replicated shard groups — mitigating 2PC's availability problem because each group tolerates minority failures — and uses the TrueTime clock to achieve external consistency (stronger than linearizability) at global scale [T1][S-0204].
- Distributed query processing decomposes a query into sub-queries executed at the sites holding the relevant partitions and combines partial results; join strategies such as partition join and semijoin reduce the data shipped between sites [T3][S-0202].
- NewSQL systems aim to keep the relational model and ACID transactions while scaling horizontally, in contrast to NoSQL systems that trade schema or transactional guarantees for scale-out [T3][S-0202].
- NoSQL systems (key-value, document, wide-column) typically offer flexible schemas, easier scale-out, and weaker or absent transaction guarantees; the choice is workload-driven, not ideological [T3][S-0128].
- Partitioning and replication are orthogonal: each partition is independently replicated, so a sharded, replicated database is simultaneously horizontally partitioned and fault-tolerant [T3][S-0128].

## Details

- Typical design flow for a sharded system: choose the partition key from the dominant query pattern, then replicate each partition for fault tolerance and read scaling — order matters because the partition key fixes colocation and the replication factor fixes durability [T3][S-0128].
- Conflict resolution under eventual consistency uses pragmatic rules (e.g., last-writer-wins by timestamp, or merge functions); applications that cannot tolerate lost updates must either use strong consistency or detect and reconcile conflicts themselves [T3][S-0128].

## Boundaries / common misunderstandings

- Eventual consistency is not "eventually correct": it is a convergence guarantee — replicas converge to the same value — but the converged value may be wrong from the application's viewpoint when concurrent writes conflict (e.g., last-writer-wins can silently discard an update) [T3][S-0128].
- CAP is not "choose any two of three": partition tolerance is a failure-mode assumption (the network may lose messages), not a property you select; the theorem says during a partition you must choose between atomic consistency and availability [T0][S-0035].
- Two-phase commit is not a fault-tolerant consensus protocol: it guarantees atomicity only while the coordinator lives; its blocking failure mode is exactly what consensus-based log replication (Paxos, Raft) eliminates [T0][S-0203].
- Read replicas do not scale writes: adding followers increases read capacity while writes are still serialized through the leader or quorum and then replicated [T3][S-0128].
- More shards do not automatically mean more speed: cross-shard queries, joins, and transactions get slower as data spreads, and cross-shard secondary indexes must be maintained explicitly [T3][S-0128].
- NewSQL does not repeal CAP or FLP: Spanner's guarantees rest on engineered infrastructure — bounded clock uncertainty (TrueTime) and Paxos replication — costs that plain 2PC systems do not pay [T1][S-0204].

## References (evidence records)

- [S-0018] ACM/IEEE-CS/AAAI CS2023 — Data Management KA (distributed databases/cloud computing).
- [S-0034] Fischer, Lynch & Paterson 1985 — FLP impossibility (JACM 32(2)).
- [S-0035] Gilbert & Lynch 2002 — CAP theorem proof (SIGACT News 33(2)).
- [S-0128] Kleppmann 2017 — Designing Data-Intensive Applications (O'Reilly).
- [S-0202] Özsu & Valduriez 2020 — Principles of Distributed Database Systems, 4th ed. (Springer).
- [S-0203] Gray & Lamport 2006 — Consensus on Transaction Commit (ACM TODS 31(1)).
- [S-0204] Corbett et al. 2012 — Spanner: Google's Globally-Distributed Database (OSDI'12).
