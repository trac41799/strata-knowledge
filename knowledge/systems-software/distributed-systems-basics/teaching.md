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
sources: [S-0127, S-0128, S-0129]
---

# Distributed Systems Basics — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Enumerate the eight fallacies of distributed computing and the primary sources behind them (Deutsch/Gosling, Sun Microsystems). (evidence: S-0129)
- understand — Explain partial failure, the crash-vs-slow indistinguishability, and why at-least-once/at-most-once are the only raw delivery options. (evidence: S-0128)
- apply — Design a retry-safe RPC or API using idempotency keys, and classify a system's delivery semantics. (evidence: S-0128) — **bloom_target**
- apply — Compute and reason with Lamport logical-clock orderings (happen-before, clock condition). (evidence: S-0127)
- analyze — Given a failure trace (timeout, crash, leader failover), identify which guarantee was violated and the minimal fix. (evidence: S-0128)

## Worked example — an RPC failure and retry trace

System: an order service `O` and a payment service `P`, connected by RPC over HTTP. Client `C` calls `O.place_order()` with a 2-second timeout. Timeline (times illustrative):

1. **t=0.0** — C sends `place_order` to O. The request is processed: an order row is inserted, and O calls `P.charge(card, $50)`.
2. **t=0.3** — P receives the charge, debits the card, and replies OK.
3. **t=0.4** — O crashes before persisting the order row; the network drops O's reply to C.
4. **t=2.0** — C's timeout fires. What does C know? Only "no response within 2 s". The charge may or may not have happened; the order may or may not exist.
5. **t=2.0** — C retries `place_order` (a naive client sends the same request again). O (restarted) inserts a second order row and calls `P.charge` again → the card is charged twice. **This is the double-execution failure of at-least-once.**

Now the fixed design:

6. **Client sends an idempotency key** `k = UUID(unique per logical order)` with every `place_order` call and reuses `k` across retries.
7. **O stores `(k, result)` in a dedup table** keyed by `k`. On retry, O finds `k` already processed: it returns the stored result and does NOT re-call `P.charge`.
8. **P likewise dedups by a charge id** derived from `k`, so even if O crashes between "charge P" and "record result", P returns the first result on the retry instead of debiting twice.

Trace the retry again: at t=2.0 C retries with the same `k`; O's dedup table has no row (O crashed before storing), so O re-calls `P.charge` with the same charge id; P returns the *stored* OK without a second debit; O stores `(k, result)` and replies. The card is charged once — **effectively exactly-once** — while the network remained at-least-once.

Key mental model: **the network can only promise at-least-once or at-most-once; "exactly-once" is an end-to-end property you build with idempotency or deduplication, and it costs stored state.**

## Worked example (mini) — Lamport clock trace

Three processes P1, P2, P3. P1 sends a message to P2 (P1's clock: 1 → carries 1), P2 receives (clock = max(0,1)+1 = 2), then P2 sends to P3 (2), P3 receives (max(0,2)+1 = 3). P3 concurrently did an unrelated event at 1. Conclusion: send→receive chain gives 1 < 2 < 3, consistent with causality; P3's local event at 1 and P1's send at 1 are concurrent and received *some* order (e.g., P3's event 1 then P1's send 1 → in a total order, tie-broken by process id). This is why a total order exists but is arbitrary for concurrent events.

## Elaboration prompts

- Why can't a server, on receiving a request, tell whether it has seen this exact request before — and what state would let it? (evidence: S-0128)
- The fallacies list says "bandwidth is infinite". What would change in an RPC design if bandwidth were truly finite and metered? (evidence: S-0129)
- If logical clocks satisfy C(a) < C(b) whenever a -> b, why are they insufficient to implement "wait until all causally prior events are done"? (evidence: S-0127)
- A single-leader replica acknowledges a write only after syncing to a follower. What does this buy, and what does it cost in latency? (evidence: S-0128)
- Where exactly does the at-least-once assumption enter the idempotency design above — and what breaks if the dedup table itself loses the key before the first result is stored? (evidence: S-0128)

## Common misconceptions

1. **"A distributed system is just a program split across machines."** The split is the problem: with message passing and no shared clock, partial failure, duplicates, and reordering are the default, not exceptions — that is what distinguishes distributed from single-machine (and parallel) programming. (evidence: S-0128)
2. **"Exactly-once delivery exists in the protocol."** No transport can promise it under crash-and-retry; exactly-once is always an end-to-end construction (at-least-once + dedup/idempotency + atomic commit) with stored state and coordination costs. (evidence: S-0128)
3. **"Lamport clocks give me a global timestamp."** They preserve causal ordering only; a greater value does not mean "later in real time", and concurrent events get arbitrary order. (evidence: S-0127)
4. **"A timeout means the server is down — retry is safe / retry is pointless."** Both claims are wrong in general: the only knowledge is "no reply within deadline"; the request may or may not have executed, which is exactly why idempotency matters. (evidence: S-0128)
5. **"Replicas automatically make a system consistent."** Copies must be coordinated; without ordering (consensus) or reconciliation, replicas drift — single-leader replication still needs failover care, and quorums alone give weak guarantees. (evidence: S-0128)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "the network is reliable" is a lie and how a 2-second timeout can turn one payment into two — grade against the RPC/idempotency claims. (evidence: S-0128, S-0129)
2. Why two machines can't just "compare timestamps" to agree on what happened first, and what a counter carried in letters achieves instead — grade against the logical-clock claims. (evidence: S-0127)
3. Why "delivered at least once" plus "doing it twice is harmless" equals "effectively once" — grade against the delivery-semantics claims. (evidence: S-0128)

## Interleaving hooks

- **systems-software/networking-basics (prerequisite):** TCP vs application-level reliability — map the four network hazards to the delivery semantics in this pack (R1, R2 in validation.md).
- **programming/concurrency-primitives (prerequisite):** compare mutex-based coordination over shared memory with message-based coordination across nodes — what assumption (no partial failure of a peer) the single-machine model makes (R3 in validation.md).
- **systems-software/distributed-consensus (recommended follow-on):** everything here — partial failure, retries, ordering — is the vocabulary consensus protocols are built on; revisit this pack when studying Raft's log and quorum intersection.
- **hardware/cache-coherence (cross-track):** both topics are "copies of state that must stay consistent" — cache lines on one chip vs replicas across machines; compare the mechanisms (coherence protocols vs replication/consensus).
