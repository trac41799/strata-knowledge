---
id: quality-testing/performance-engineering
title: Performance Engineering
band: B4
track: quality-testing
tier: T1
bloom_target: apply
prerequisites: [quality-testing/quality-models, systems-software/os-scheduling]
related: []
recommended: []
status: draft
schema-version: 1
owner: l1-performance-engineering
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0019, S-0110, S-0227, S-0228, S-0229]
---

# Performance Engineering — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Latency numbers recall
- Q: Give the order of magnitude (ns/µs/ms) of: L1 cache reference, main memory reference, same-datacenter round trip, disk seek, and a cross-continent round trip.
- bloom: remember
- bank: formative
- A: L1 ~0.5 ns; main memory ~100 ns; same-datacenter round trip ~0.5 ms; disk seek ~10 ms; cross-continent (CA→NL→CA) ~150 ms. These are order-of-magnitude heuristics for circa-2007–2013 hardware, for back-of-the-envelope estimates — not laws and not today's exact figures.
- evidence: [S-0228]
- topic: quality-testing/performance-engineering

### F2. Why the mean lies
- Q: A service reports "average latency 180 ms" and p99 1.2 s. Explain why the average misrepresents user experience, and state which measurement the SLO should be written against.
- bloom: understand
- bank: formative
- A: The distribution is long-tailed: 99% of requests are fast, so the mean is pulled low while 1% of users experience >1.2 s. User-perceived latency tracks the tail, not the mean; with fan-out, the tail dominates end-to-end. The SLO should be written against high percentiles (p99/p99.9), per the tail-at-scale evidence.
- evidence: [S-0227]
- topic: quality-testing/performance-engineering

### F3. Fan-out amplification
- Q: A query fans out to 50 independent components, each with a 1% chance of taking p99-class latency. Compute the probability that at least one component is slow, and state the design implication.
- bloom: understand
- bank: formative
- A: P(any slow) = 1 − (0.99)^50 ≈ 39%. End-to-end latency is set by the slowest component, so even rare tails are very likely to appear in fan-out queries. Implication: tail tolerance (hedged/tied requests, partitioning) must be designed in — the mean and even a clean p50 do not describe the system the user experiences.
- evidence: [S-0227]
- topic: quality-testing/performance-engineering

### F4. Back-of-the-envelope design choice
- Q: A page needs 20 thumbnail images, each a 256 KB disk read (10 ms seek + read time at ~30 MB/s). Estimate the serial design and a parallel-read design, and name the lever each represents.
- bloom: apply
- bank: formative
- A: Serial: 20 × (10 ms + 256 KB/30 MB/s ≈ 8.5 ms) ≈ 20 × 18.5 ms ≈ 370 ms. Parallel: one seek + one 256 KB read ≈ 18.5 ms (ignoring variance, realistically higher). The lever is parallelization (plus caching/pre-computation of thumbnails as alternates). Back-of-the-envelope with the latency numbers separates the designs before any code is written — measurement-first applied at design time.
- evidence: [S-0228]
- topic: quality-testing/performance-engineering

## Summative (mastery checkpoint)

### S1. p99 analysis + optimization trace
- Q: A checkout endpoint shows: p50 45 ms, p90 90 ms, p99 1,100 ms, mean 180 ms; the 1% slowest requests correlate with DB connection-reuse failures. Fan-out is 10 (10 sub-queries). Build the optimization trace: state the problem in percentiles, compute the fan-out exposure, pick a lever, and specify how you would verify the fix.
- bloom: apply
- bank: summative
- A: Problem: the tail (1,100 ms at p99) is 24x the p50 — the mean hides it; 1% of requests suffer connection-reuse failures. Fan-out exposure: 1 − (0.99)^10 ≈ 9.6% chance a checkout hits at least one slow sub-query. Lever: fix the DB connection-reuse failure (variance source) first — this targets the distribution's tail directly rather than the common case; as a complementary tail-tolerant measure, hedge the slowest sub-query class if failures persist. Verification: profile (sampling profiler) to confirm the hot path; re-measure the full percentile distribution (p50/p90/p99) under load, not just the mean, and compare against the budget (e.g., p99 < 300 ms). Any fix that does not move the p99 is not a fix for this problem.
- evidence: [S-0227][S-0229]
- topic: quality-testing/performance-engineering

### S2. Diagnosing a load-test result
- Q: Load testing at 2x peak shows: p50 stable at 60 ms, p99 degrades from 200 ms to 1,400 ms as the run progresses, and CPU is at 30% while the thread pool is saturated. Diagnose the bottleneck class and map it to a lever.
- bloom: analyze
- bank: summative
- A: Saturation of a resource (thread pool) with idle CPU indicates queueing/contention, not compute: requests queue behind blocked threads, so latency variance explodes (p99 7x worse) while CPU stays low. The lever is not more compute — it is reducing blocking (async/batching of the blocked I/O), bounding queue depth, or load-shedding — measured with the percentile distribution, not the mean. This is the variance-dominates picture of tail latency: the p50 hides the queue.
- evidence: [S-0227][S-0228]
- topic: quality-testing/performance-engineering

### S3. Evaluating an optimization claim
- Q: A colleague proposes: "add a thread pool of 200 threads — more parallelism always helps — and let's micro-optimize the string concatenation in the logging path." Evaluate both parts against the evidence.
- bloom: evaluate
- bank: summative
- A: Both parts fail measurement-first. (1) The empirical concentration finding (Knuth) says runtime lives in a small fraction of code — optimizing the logging path without a profile is a lottery, the exact premature-optimization pattern; the profiler decides. (2) Blindly adding threads ignores that latency at scale is dominated by variance and queueing, not thread count — the correct move is to measure (percentiles under load), find the variance source (blocked I/O, contention), and only then choose a lever (async, batching, hedging), verifying against the p99/p99.9 budget.
- evidence: [S-0229][S-0227]
- topic: quality-testing/performance-engineering

### S4. Budget construction
- Q: A product owner says "make it fast" and rejects a numeric target. Construct a performance budget from the quality model, state what the load test must check, and justify why a number beats a word.
- bloom: analyze
- bank: summative
- A: Translate "fast" into the performance-efficiency characteristic (time behavior, resource utilization, capacity): e.g., p50 < 100 ms, p99 < 300 ms at 2x peak load, CPU < 70% utilization. Per SQuaRE, the requirement is linked to measures so the load test checks measured values against them — the budget is a measurable quality requirement. A number beats a word because verification (load test pass/fail), regression detection, and the variance/p99 behavior can only be checked against a defined target — and SWEBOK's testing KA places that check (performance testing) inside the testing discipline.
- evidence: [S-0019][S-0110][S-0017]
- topic: quality-testing/performance-engineering

## Review (spaced repetition — interleaved with prerequisites)

### R1. Performance efficiency as a quality characteristic (from quality-models)
- Q: A stakeholder requests "good performance." Using the quality model, decompose the request into characteristics and state how quality in use is measured differently from product performance.
- bloom: understand
- bank: review
- A: Product quality: performance efficiency decomposes into time behavior, resource utilization, and capacity — measurable on the product (latency percentiles, CPU, throughput). Quality in use: efficiency is the user's time/effort per achieved outcome, measured in context of use, and product performance enables it without guaranteeing it. "Good performance" must be decomposed into characteristics + measures per the SQuaRE chain before it is testable.
- evidence: [S-0019][S-0110]
- topic: quality-testing/quality-models

### R2. Scheduling and latency variance (from os-scheduling)
- Q: A latency-sensitive service shares a host with batch jobs. Using the scheduling concepts, explain why response-time variance grows and name two scheduler-level remedies.
- bloom: understand
- bank: review
- A: Interactive and batch work compete for the CPU; batch bursts delay ready processes, inflating response time and its variance (the tail). Remedies: a small round-robin quantum bounds response time but tiny quanta multiply context-switch overhead; priority/MLFQ schemes boost interactive (I/O-bound) processes; or isolate workloads (cgroups/schedulers) so batch work cannot push the interactive tail. The point: response-time variance has an OS-level source — performance engineering and scheduling meet here.
- evidence: [S-0032]
- topic: systems-software/os-scheduling

### R3. Measurement before change (this topic)
- Q: A team rewrites a hot function based on "everyone knows it's slow," without a profile. Evaluate the move and describe the minimal measurement that would justify it.
- bloom: evaluate
- bank: review
- A: The move is unjustified: the empirical concentration finding says most code is rarely executed — the rewrite may target dead weight while the real hot spot sits elsewhere. Minimal justification: a sampling-profiler trace showing the function's share of runtime (plus percentile latency data if the goal is responsiveness), then the rewrite, then a re-measure against the budget. Optimization without measurement is the premature-optimization pattern, whatever the intent.
- evidence: [S-0229]
- topic: quality-testing/performance-engineering
