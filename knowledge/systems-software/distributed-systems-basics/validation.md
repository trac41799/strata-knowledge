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

# Distributed Systems Basics — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Fallacies recall
- Q: List the first four fallacies of distributed computing and the design habit each one warns against.
- bloom: remember
- bank: formative
- A: (1) The network is reliable — assume packet loss and timeouts; (2) latency is zero — budget for real round-trip times; (3) bandwidth is infinite — respect finite capacity; (4) the network is secure — threat-model the wire. The habit: design for the worst case, not the happy path.
- evidence: [S-0129]
- topic: systems-software/distributed-systems-basics

### F2. Partial failure explanations
- Q: A client sends a request and receives nothing within its timeout. Enumerate the distinct explanations, and state which one the client cannot rule out.
- bloom: understand
- bank: formative
- A: (a) request lost; (b) server crashed before processing; (c) server processed but crashed before replying; (d) reply lost; (e) server is slow. The client cannot distinguish a dead server from a slow one — only "no response within the deadline" is certain, so retry behavior must assume the request may have been executed.
- evidence: [S-0128]
- topic: systems-software/distributed-systems-basics

### F3. Retry-safe API design
- Q: You expose POST /charge with automatic retry on timeout. Charging is not idempotent. Design the smallest change that makes retries safe, and name the delivery semantics your design implements.
- bloom: apply
- bank: formative
- A: Require a client-generated idempotency key per charge; the server stores the key with the result and returns the stored result on duplicate keys, and the client must reuse the same key across retries of the same logical operation. The transport is at-least-once (retries until ack), but the stored-key dedup makes the effect exactly-once for a well-behaved client.
- evidence: [S-0128]
- topic: systems-software/distributed-systems-basics

### F4. Logical clock direction
- Q: Events a and b have logical clock values C(a) = 5 and C(b) = 9. Does a necessarily happened-before b? Answer and explain what the clock condition actually guarantees.
- bloom: understand
- bank: formative
- A: No. The clock condition is one-way: a -> b implies C(a) < C(b); the converse does not hold because concurrent events receive an arbitrary order. Without knowing the causal chain (program order, send/receive pairs), a smaller timestamp proves nothing.
- evidence: [S-0127]
- topic: systems-software/distributed-systems-basics

## Summative (mastery checkpoint)

### S1. Delivery semantics for a job queue
- Q: A job queue has consumer C. Publisher P retries a publish until acknowledged; C acknowledges after completing the job. Classify the delivery semantics on each leg (P to queue, queue to C) and explain what guarantee the system as a whole gives if the job is "write a row with this UUID".
- bloom: apply
- bank: summative
- A: P to queue: at-least-once (retries may duplicate the message in the queue). Queue to C: at-least-once if C acks after processing (a crash between processing and ack re-delivers). So duplicates can occur at both legs. If the row write is idempotent by UUID (insert-on-conflict-update), the end-to-end effect is exactly-once even though delivery is not — exactly-once is an end-to-end property built from at-least-once plus idempotence, not a transport guarantee.
- evidence: [S-0128]
- topic: systems-software/distributed-systems-basics

### S2. Leader-replication failure trace
- Q: A single-leader replicated counter: client sends inc() to the leader; the leader applies it, acknowledges, then crashes before replicating. A failover promotes a follower. What does the client observe next, and what is the consistency consequence?
- bloom: analyze
- bank: summative
- A: The client observes a lost increment: the new leader's value predates the acknowledged write. The acknowledgment was a lie from the consistency standpoint — the write was never durably replicated. Consequence: acknowledged-write-lost, a classic at-least-once/durability gap. Standard fixes: replicate to a quorum (or synchronously to followers) before acknowledging, or accept the semantic and reconcile (e.g., idempotent compensating operations).
- evidence: [S-0128]
- topic: systems-software/distributed-systems-basics

## Review (spaced repetition — interleaved with prerequisites)

### R1. TCP and the request/response gap (from networking-basics)
- Q: TCP guarantees an in-order, lossless byte stream over a connection. A client sends one request and awaits one reply on a TCP connection. Why must the client still implement timeouts and retries?
- bloom: understand
- bank: review
- A: TCP's guarantees hold only while the connection exists and only for bytes in the stream. The server can crash, the connection can break mid-request, and the reply can arrive after the client gave up — TCP never promises that a request was processed or that a reply will come. Transport reliability is not application-level delivery.
- evidence: [S-0088]
- topic: systems-software/networking-basics

### R2. Network hazards map to semantics (from networking-basics)
- Q: Name the four packet-level hazards of an unreliable network, and for each give the application-layer consequence a distributed-system designer must handle.
- bloom: understand
- bank: review
- A: Loss (message never arrives — timeouts, retries, at-least-once risk), duplication (same message twice — idempotency/dedup), reordering (messages arrive out of order — sequence numbers or total order), delay (arbitrary latency — timeout false positives, the slow-vs-dead problem). Every delivery-semantics design (at-least-once, at-most-once) is a decision about how to absorb these four.
- evidence: [S-0088]
- topic: systems-software/networking-basics

### R3. Shared-memory vs message passing (from concurrency-primitives)
- Q: On one machine, two threads coordinate via a mutex over shared memory. Across machines, nodes coordinate via message passing. State the failure-handling assumption each model makes and why the distributed version cannot rely on the first model's guarantees.
- bloom: understand
- bank: review
- A: The shared-memory model assumes a coherent view of memory and that coordination happens synchronously within the machine (no machine-level partial failure of one thread). Message passing assumes communication is the only coupling and that any message may be lost, delayed, or duplicated and any node may fail mid-operation — so coordination must tolerate partial failure, which mutual exclusion alone does not.
- evidence: [S-0128]
- topic: systems-software/distributed-systems-basics
