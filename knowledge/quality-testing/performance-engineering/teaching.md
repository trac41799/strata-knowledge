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
status: published
schema-version: 1
owner: l1-performance-engineering
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0110, S-0227, S-0228, S-0229]
---

# Performance Engineering — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Recite the order-of-magnitude latency numbers and the percentile vocabulary (p50/p99/p99.9, tail, fan-out). (evidence: S-0228, S-0227)
- understand — Explain why the mean hides the tail, why fan-out amplifies rare slowness, and why measurement-first is the empirical baseline for optimization. (evidence: S-0227, S-0229)
- apply — Produce a p99 analysis and optimization trace: locate the tail in a latency histogram, compute fan-out exposure, pick a lever, and specify the verification. (evidence: S-0227, S-0228) — **bloom_target**
- analyze — Diagnose load-test results (queueing vs compute, variance vs mean) and map symptoms to levers and OS-level causes. (evidence: S-0227)
- evaluate — Judge optimization proposals ("add threads", "micro-optimize X", "buy faster hardware") against measurement-first and tail-tolerance evidence. (evidence: S-0229, S-0227)

## Worked example — p99 analysis + optimization trace

Scenario: checkout endpoint; latency histogram (ms): p50 45, p90 90, p99 1,100, mean 180. The 1% slowest requests correlate with DB connection-reuse failures; each checkout fans out to 10 sub-queries.

1. **State the problem in percentiles, not means.** The mean (180 ms) hides that 1% of users wait 1.1 s — 24x the median. The tail-at-scale evidence says user-perceived latency tracks the tail, so the SLO candidate is p99 < 300 ms, and the working problem is the 1,100 ms tail.
2. **Quantify the fan-out exposure.** 10 sub-queries, each slow 1% of the time: P(any slow) = 1 − (0.99)^10 ≈ 9.6%. Even a "rare" tail appears in ~1 in 10 checkouts — end-to-end latency is set by the slowest component. This justifies treating the tail as a first-class design problem, not an anomaly.
3. **Find the variance source with a profiler.** Run a sampling profiler under load (low overhead, statistical attribution — instrumentation would add exact counters at chosen call sites but distort timing and costs more setup). The profile shows the slow requests are blocked on connection-reuse failures, not compute: CPU is idle while threads wait — a queueing/variance problem, not a speed problem. (Technique note: sampling vs instrumentation is practice-level knowledge; the evidence at hand establishes that runtime concentrates measurably, which is what makes the profile decisive.)
4. **Pick a lever, guided by measurement.** Fix the variance source (connection reuse) — targeting the tail directly. Complementary tail tolerance if failures persist: hedge the slowest sub-query class (send a second request after a small delay, use the first response) — the measured precedent is p99.9 dropping from 1,800 ms to 74 ms at +2% load. Caching/pre-computation applies only if the back-of-the-envelope says repeated work dominates — here it does not.
5. **Verify against the budget.** Re-run the load test and check the percentile distribution, not the mean: pass = p99 within budget at target load, with utilization within the quality-model targets. A change that moves p50 but not p99 did not fix this problem.

The reusable trace: percentiles → fan-out exposure → profile to find the variance source → lever chosen by measurement → verify against the budget.

## Worked example (mini) — back-of-the-envelope design estimate

Thumbnail page, 30 images, 256 KB each, ~30 MB/s read, 10 ms seeks. Serial: 30 × (10 + 8.5) ms ≈ 560 ms. Parallel: ~18 ms (ignoring variance; realistically 30–60 ms). The estimate alone separates the designs — and shows why caching (already-rendered thumbnails), pre-computation, and parallelization are the first levers to consider. Same method, one order of magnitude down: a fan-out service that issues dozens of 1 MB RPCs per user request is already lousy on paper.

## Elaboration prompts

- Why is the *mean* the metric that survives in dashboards despite the evidence against it — and what dashboard change makes the tail visible? (evidence: S-0227)
- Fan-out of 100 at 1% gives 63% exposure; fan-out of 10 at 1% gives ~9.6%. Where is the crossover where "rare" stops being rare, and how does that change what you optimize? (evidence: S-0227)
- Hedged requests buy 24x tail improvement at 2% load in the measured example — what other costs (besides load) does hedging introduce, and how would you bound them? (evidence: S-0227)
- Amdahl's law (Amdahl 1967) bounds parallel speedup by the serial fraction: how does the fan-out exposure interact with Amdahl when the serial fraction is the *variance* rather than the work? (pointer: S-0132, teaching-level)
- Knuth measured 70% of runtime in single loops in 1971 programs — what could make that concentration weaker in modern systems, and why is it still the default assumption? (evidence: S-0229)
- A performance budget says "p99 < 300 ms at 2x load" — trace the requirement through the quality model to the load test and back to the SLO. Where do the measures get defined, and who decides the thresholds? (evidence: S-0019, S-0110)

## Common misconceptions

1. **"Average latency is the performance of the system."** The mean hides the tail; users experience the tail, and fan-out makes rare slowness common (63% at 100 components × 1%). (evidence: S-0227)
2. **"Optimize the code you think is slow."** Runtime concentrates in a small fraction of code — measured in 1971 and the standing default — so unmeasured optimization is a lottery. Profile first. (evidence: S-0229)
3. **"More parallelism always helps."** The levers (parallelization included) change the dominant cost only when measurement says the cost is there; queueing/variance — not thread count — usually dominates latency at scale. (evidence: S-0227, S-0229)
4. **"The latency numbers are physical constants."** They are order-of-magnitude, era-dependent heuristics (2007–2013 hardware) for estimation, not specification values. (evidence: S-0228)
5. **"Faster hardware / more machines fixes it."** Latency variability is inherent at scale (background activity, failures, scheduling); responsive services tolerate the tail instead of eliminating it. (evidence: S-0227)
6. **"Load testing is optional performance work."** Performance testing is part of the testing discipline (SWEBOK specialized testing), and its verdict is only decidable against a numeric budget from the quality model. (evidence: S-0017, S-0019)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "the average wait at the bank is 3 minutes" doesn't describe the queue when one teller is on break — and what number you would actually want. (grade against the tail/percentile claims: S-0227)
2. Why a chef who spends 10 minutes polishing the salad tongs while the grill is on fire is optimizing the wrong thing — and what you'd measure first. (grade against the measurement-first claims: S-0229)
3. Why "one slow car in a convoy of 100" makes the whole convoy slow — and what a convoy designer does about it. (grade against the fan-out/tail-tolerance claims: S-0227)

## Interleaving hooks

- **quality-testing/quality-models (prerequisite):** performance budgets are the SQuaRE requirement→measure chain applied to the performance-efficiency characteristic — R1 in validation.md reviews the model; the budget question "who decides thresholds" is a quality-requirements question.
- **systems-software/os-scheduling (prerequisite):** response-time variance has an OS-level source — scheduling delays and context-switch overhead — R2 in validation.md interleaves it; ask which scheduler choices a latency SLO implies (quantum size, priorities, isolation).
- **systems-software/parallel-programming (related, via S-0132):** Amdahl's law bounds what parallelization can buy — combine it with the fan-out math to separate "speedup from work-parallelism" from "speedup from variance-tolerance".
- **operations/observability (related):** the percentile vocabulary here is the latency distribution RED/USE methods monitor — a performance budget is only enforceable when the pipeline can report p99/p99.9 under load.
- **quality-testing/software-testing-basics (related):** load testing reuses the testing machinery (oracles, test levels): the oracle for a load test is the numeric budget, exactly as the oracle is the decidable expectation in unit tests.
