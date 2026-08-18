---
id: systems-software/distributed-systems-basics
title: Distributed Systems Basics
band: B5
track: systems-software
tier: T0
bloom_target: apply
prerequisites: [systems-software/networking-basics, programming/concurrency-primitives]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-distributed-systems-basics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0018, S-0127, S-0128, S-0129]
---

# Distributed Systems Basics

## Claims

### What a distributed system is

- A distributed system is a set of independent machines connected by a network that cooperate by passing messages; there is no shared memory and no shared clock, and each machine has only a partial view of the system state [T3][S-0128].
- The defining difficulty of distributed systems is partial failure: at any moment some nodes may be slow or dead while others work normally, and the system as a whole must stay correct [T3][S-0128].
- Distributed-systems fundamentals (system models, RPC, time and clocks, fault tolerance) are codified curriculum knowledge units in the CS2023 Parallel & Distributed Computing knowledge area [T2][S-0018].

### The fallacies of distributed computing

- The eight fallacies of distributed computing (Deutsch, Gosling, Sun Microsystems) enumerate the assumptions beginners make that are always false: the network is reliable; latency is zero; bandwidth is infinite; the network is secure; topology does not change; there is one administrator; transport cost is zero; the network is homogeneous [T3][S-0129].
- Each fallacy names a failure mode the design must absorb: for example, "the network is reliable" fails on packet loss, and "the network is homogeneous" fails when one component speaks a different protocol or version [T3][S-0129].

### Partial failure

- A client cannot tell a crashed server from a slow one: after a timeout, the only reliable statement is "no response within the deadline", never "the server is dead" [T3][S-0128].
- The network can lose, duplicate, reorder, and arbitrarily delay packets; even a reliable transport (TCP) only guarantees delivery and ordering of an established byte stream, so request/response interactions still face timeouts and retries [T3][S-0128].
- Physical clocks on different machines drift and their synchronization is approximate, so wall-clock timestamps cannot be used to order events across nodes [T3][S-0128].

### RPC and idempotency

- Remote procedure call (RPC) makes a call to a remote service look like a local function call; the abstraction leaks, because timeouts, retries, duplicated execution, and partial failure become visible to the caller [T3][S-0128].
- A retried request may execute twice: the reply may have been lost after the server already processed the request, so retrying is safe only if the operation is idempotent or deduplicated [T3][S-0128].
- An operation is idempotent if performing it once has the same effect as performing it many times; assigning each request a unique idempotency key lets the server drop duplicates, which is the standard retry-safety mechanism [T3][S-0128].

### Delivery semantics and exactly-once

- At-least-once: the sender retries until it receives an acknowledgment, so every message is delivered, but a message may be delivered more than once [T3][S-0128].
- At-most-once: the sender gives up or never retries, so no message is ever duplicated, but messages may be lost [T3][S-0128].
- Exactly-once delivery cannot be guaranteed by a transport or messaging layer alone: when senders can crash and retry and networks can duplicate, a receiver cannot distinguish a retried message from a new one without extra state [T3][S-0128].
- Exactly-once is achieved end-to-end, not per hop: at-least-once delivery combined with deduplication or idempotent operations and atomic commit yields exactly-once effects for well-behaved operations [T3][S-0128].

### Time and ordering

- Lamport (1978) defines the happened-before partial order: within one process events are ordered by program order, a send happens before the matching receive, and the relation is transitive [T0][S-0127].
- A logical clock assigns each event a counter value such that a -> b implies C(a) < C(b); the algorithm increments the counter per event, carries the value in messages, and takes the max on receive [T0][S-0127].
- Lamport extends the partial order to an arbitrary total order by breaking ties with process identifiers, which suffices to run a replicated state machine (the total order is the log) [T0][S-0127].
- A larger logical-clock value does NOT imply a later event: concurrent events receive an arbitrary order, so the implication runs only one way (causality implies ordering, not the converse) [T0][S-0127].

### Replication basics

- Replication keeps copies of the same data on several nodes; the benefits are higher availability, lower read latency, and higher read throughput, at the cost of keeping copies consistent [T3][S-0128].
- Single-leader replication: one node (the leader) accepts writes and ships them to followers; followers serve reads and can take over only after the leader fails and a failover is coordinated [T3][S-0128].
- Quorum-based schemes make an operation require a subset (quorum) of nodes to agree; quorum arithmetic and the consensus protocols built on majorities (Raft, Paxos) are treated in systems-software/distributed-consensus [T3][S-0128].

## Details

- Timeouts are the only general failure-detection mechanism in an asynchronous network; choosing them is a tradeoff between false positives (aborting slow-but-healthy operations) and false negatives (waiting on dead nodes) [T3][S-0128].
- A distributed system need not be exotic: any client/server deployment over a network, message queue, or multi-node database already exhibits partial failure, retries, and the ordering problems above [T3][S-0128].

## Boundaries / common misunderstandings

- Distributed computing is not parallel computing: parallel programming runs cooperating threads sharing memory on one machine to cut latency or raise throughput; distributed systems span independent machines with message passing, where the hard problems are failure and coordination, not raw speedup [T3][S-0128].
- Exactly-once is not a magic transport property: products advertised as exactly-once still implement at-least-once plus deduplication or idempotent, atomic commit — the guarantee is end-to-end and costs coordination [T3][S-0128].
- Logical clocks are not synchronized wall clocks: Lamport timestamps only preserve causal ordering and give no information about real time [T0][S-0127].
- A majority of replicas alone does not give linearizable consistency or a total order; quorum read/write gives weaker guarantees unless a consensus protocol (Raft/Paxos) orders the log — that distinction belongs to systems-software/distributed-consensus [T3][S-0128].
- The fallacies are not historical trivia: each one still maps to a real incident class (dropped packets, high tail latency, MTU/version mismatch, security breaches) [T3][S-0129].

## References (evidence records)

- [S-0127] Lamport 1978 — Time, Clocks, and the Ordering of Events in a Distributed System (CACM 21(7)).
- [S-0128] Kleppmann 2017 — Designing Data-Intensive Applications (O'Reilly).
- [S-0129] Deutsch & Gosling (Sun Microsystems) — The Eight Fallacies of Distributed Computing.
- [S-0018] ACM/IEEE-CS/AAAI 2024 — CS2023 (Parallel & Distributed Computing KA), cited on one claim.
