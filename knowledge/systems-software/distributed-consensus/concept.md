---
id: systems-software/distributed-consensus
title: Distributed Consensus
band: B5
track: systems-software
tier: T0
bloom_target: analyze
prerequisites: [systems-software/distributed-systems-basics]
related: [data/distributed-databases, systems-software/networking-basics]
recommended: [data/distributed-databases]
status: published
schema-version: 1
owner: l1-distributed-consensus
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0034, S-0035, S-0036, S-0037, S-0042]
---

# Distributed Consensus

## Claims

- The consensus problem: each process proposes a value; all non-faulty processes must agree on the same value, and the agreed value must be one that was proposed. In an asynchronous system this cannot be guaranteed with termination even for a single faulty process [T0][S-0034].
- Failure models (crash): a process simply stops and never resumes — the model FLP's impossibility is stated for [T0][S-0034].
- Failure models (Byzantine): a node may behave arbitrarily (lie, equivocate, send conflicting messages) due to bugs or attacks — the failure class PBFT is designed to tolerate [T1][S-0037].
- FLP theorem (Fischer, Lynch & Paterson 1985): in a totally asynchronous model of computation (no bound on processing speed or message delay), every deterministic consensus protocol has the possibility of nontermination, even with only one faulty process; by contrast, solutions are known for the synchronous case [T0][S-0034].
- FLP is a liveness impossibility, not a safety one: a protocol can preserve agreement (safety) while being unable to guarantee progress [T0][S-0034].
- FLP does not declare consensus impossible in practice: the paper itself points to refined models with realistic timing assumptions (eventual synchrony, failure detectors) or relaxed requirements (e.g., termination under specific conditions) [T0][S-0034].
- CAP theorem (Gilbert & Lynch 2002, formalizing Brewer's 2000 PODC conjecture): in the asynchronous network model it is impossible to simultaneously guarantee atomic (linearizable) consistency, availability (every request received by a non-faulty node must result in a response), and partition tolerance (the network may lose arbitrarily many messages) [T0][S-0035].
- CAP's tradeoff is model-dependent: in the partially synchronous model the impossibility relaxes — under bounded-time assumptions, consistency and availability become simultaneously achievable while the network is stable; the unconditional "any two of three" reading holds only in the asynchronous model [T0][S-0035].
- CAP's definitions bound its scope: consistency means atomic consistency (linearizability), and availability carries no time bound in the asynchronous model; the theorem does not directly constrain weaker consistency models or time-bounded availability [T0][S-0035].
- Quorums and majority: with n = 2f+1 servers, f failures can be tolerated (five servers tolerate two failures); any two majorities intersect in at least one server, and that intersection is the foundation of safety in majority-based protocols like Paxos and Raft [T3][S-0042].
- Paxos (Lamport 1998, "The Part-Time Parliament"; simplified in 2001, "Paxos Made Simple") is the foundational practical consensus protocol: it combines a two-phase protocol for basic consensus (prepare/promise, then accept) with a separate leader-election mechanism, which is orthogonal to core consensus [T3][S-0042].
- Paxos has proven correctness, supports membership changes, and is efficient in the normal case, but it is exceptionally difficult to understand; the Raft paper reports that few researchers feel comfortable with it and that practical systems typically diverge from the published algorithm [T3][S-0042][S-0036].
- Raft (Ongaro & Ousterhout 2014) is a consensus algorithm for managing a replicated log, equivalent to (multi-)Paxos in results and efficiency; it decomposes consensus into leader election, log replication, and safety, concentrating functionality in a strong leader to reduce mechanism [T3][S-0036].
- Leader election in Raft: time is divided into terms with monotonically increasing numbers; a follower that hears nothing within an election timeout becomes a candidate and requests votes; randomized timeouts make split votes rare; a candidate wins only with a majority of votes for its term [T3][S-0036].
- Log replication in Raft: the leader appends client commands to its log and sends AppendEntries RPCs; an entry is committed once a majority of servers have stored it, then applied to the state machine in log order; the Leader Append-Only, Log Matching, Leader Completeness, and State Machine Safety properties prevent divergent logs [T3][S-0036].
- Safety vs liveness: safety means "nothing bad ever happens" (e.g., agreement — no two servers apply different commands at the same log index); liveness means "something good eventually happens" (e.g., termination) [T0][S-0034].
- Raft guarantees safety under all non-Byzantine conditions — delays, partitions, packet loss, duplication, reordering — while liveness holds only while a majority of servers can communicate with each other and with clients; timing affects availability, never consistency [T3][S-0036].
- Raft's failure model is crash-stop with recovery: servers fail by stopping and may later restart from stable storage; Raft is not designed for Byzantine behavior [T3][S-0036].
- Byzantine fault tolerance: PBFT (Castro & Liskov 1999) was the first replication algorithm to make BFT practical — it works in asynchronous systems like the Internet and tolerates up to f Byzantine-faulty replicas with n = 3f + 1 replicas, using pre-prepare, prepare, and commit phases with message authentication [T1][S-0037].
- PBFT's experimental evaluation demonstrated near-production performance, making Byzantine consensus feasible for real services and influencing later BFT designs [T1][S-0037].

## Details

- Typical deployment pattern: consensus runs a replicated state machine — a log of commands applied in the same order on every replica; Raft orders the log, distributed databases then layer transactions over it [T3][S-0036].
- The FLP "window of vulnerability" reappears in every practical protocol: Raft's liveness depends on a majority being able to communicate within election timeouts — under a permanent partition, progress (not safety) is lost [T3][S-0036].

## Boundaries / common misunderstandings

- CAP is not "pick any 2 of 3 at all times": partition tolerance is a failure-mode assumption (the network may lose messages), not a property you choose; the theorem says that during a partition you cannot keep both atomic consistency and availability — when no partition occurs, both can hold [T0][S-0035].
- FLP assumes asynchrony: "consensus is impossible" is only true in the totally asynchronous model with crash-prone processes; synchronous and partially synchronous models admit solutions [T0][S-0034].
- Raft and Paxos are not Byzantine-tolerant: they assume servers fail by stopping; a single malicious or arbitrarily buggy node lies outside their guarantees — BFT protocols need 3f+1 replicas rather than 2f+1 [T1][S-0037][S-0036].
- Raft is not the only practical consensus protocol: Paxos and leader-based alternatives such as Viewstamped Replication (Oki & Liskov 1988) and ZAB (ZooKeeper's consensus protocol) offer different structure and tradeoffs [T3][S-0036].
- A leader cannot safely commit by acting alone: commit requires a majority; an entry committed without a majority quorum can be lost when a new leader is elected [T3][S-0036].

## References (evidence records)

- [S-0034] Fischer, Lynch & Paterson 1985 — FLP impossibility (JACM 32(2)).
- [S-0035] Gilbert & Lynch 2002 — CAP theorem proof (SIGACT News 33(2)).
- [S-0036] Ongaro & Ousterhout 2014 — Raft (USENIX ATC '14).
- [S-0037] Castro & Liskov 1999 — PBFT (OSDI '99).
- [S-0042] Lamport 2001 — Paxos Made Simple (SIGACT News 32(4)).
