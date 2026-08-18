---
id: operations/devops-pipeline
title: DevOps Pipeline
band: B5
track: operations
tier: T1
bloom_target: apply
prerequisites: [engineering-process/configuration-management, engineering-process/software-lifecycle]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-devops-pipeline
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0020, S-0022, S-0162, S-0163, S-0164]
---

# DevOps Pipeline — teaching

## Learning objectives (Bloom)

By the end of this topic, the learner can:

- remember: name the four DORA key metrics and the canonical pipeline stages.
- understand: explain why deployment automation and continuous integration reduce lead time and errors (DORA evidence).
- apply: design a pipeline with quality/security gates and controlled environment promotion for a given service.
- apply: decide between rollback and ride-out using blue-green mechanics and the change-failure/restore metrics.
- evaluate: judge delivery claims ("we deploy daily → we are elite") against the DORA cluster benchmarks and the ISO 12207 process view.

## Worked example

**Release v2.3.0 of the payments API, with a failure and a rollback decision.**

Setup: pipeline stages commit → build → acceptance → capacity → production (blue-green). Environment promotion is baseline-controlled (staging baseline "v2.3.0-candidate").

1. Commit: CI builds, unit tests pass in 6 minutes.
2. Acceptance: e2e suite runs against the test environment; the payments e2e flakes twice and fails. Decision: the gate fails — do not promote. Team fixes a race in the test fixture, re-runs, green. (Fix was in the harness, not the product — the gate still caught a real signal: the suite was not stable enough to trust.)
3. Capacity: load test shows p99 under 300 ms at 2x peak. Green.
4. Manual approval: release manager checks the migration plan (v2 migration with rollback script) and approves.
5. Production: v2.3.0 deploys to the green environment; database migration v2 runs; traffic switches 100% to green at 14:02.
6. 14:17: golden-signal-style monitoring shows p99 latency 3x above baseline and errors climbing. Change failure rate is clearly heading out of the 0–15% band.
7. Decision — roll back: re-route traffic to blue (still running v2.2.0) at 14:19. MTTR measured: 17 minutes. Migration rollback script reverts data to v2-compatible state; no data loss because the rollback path was designed before release.
8. Retrospective: root cause was a query pattern the capacity test did not exercise at production cardinality. Actions: extend capacity suite, add the query pattern to acceptance, and for the next release phase the traffic switch in 10% increments instead of 100% (incremental rollout) so the failure would have been caught before full switch.

What this example teaches: gates exist to fail early; blue-green makes rollback a routing decision, not a rebuild; the rollback safety of data migrations is a release precondition; the metrics (MTTR, CFR) are measured outcomes of this run, feeding the next decision.

## Elaboration prompts

- Why is change failure rate a *stability* metric and lead time a *throughput* metric? What happens if you only optimize one of the two?
- DORA found elite teams both faster AND more stable. What mechanisms could explain the absence of a speed/stability trade-off?
- Why does the pipeline concept require "software is releasable at every stage"? What breaks if the pipeline ends in a manual, unscripted production step?
- Why is promoting a build between environments a configuration-management act rather than a copy operation?
- In the worked example, why was the harness fix not wasted effort? What did the failure teach before production?

## Common misconceptions

- "CI/CD is a set of tools you buy." The pipeline is a feedback and risk-management design; DORA treats automation as one capability among 24 spanning architecture, culture, and monitoring.
- "More deployments = more risk." The 2021 elite cluster deploys ~973x more often than low performers while failing ~3x less often; automation and small batches are how they square the circle.
- "Blue-green = guaranteed zero downtime / zero risk." Traffic switch is instant, but a release with a one-way data migration may be impossible to roll back safely — zero-downtime design must cover the data.
- "DORA metrics are for performance review of individuals." They measure delivery outcomes of a system/process, not individual activity; using them to rank individuals misreads what they measure.
- "Rollback means redeploying the old version." In blue-green it means re-routing traffic to the environment that never stopped running; a redeploy is slower and riskier than a routing flip.

## Feynman targets

- Explain to a product manager why "deploys every day" is not proof of a high-performing team, using the four metrics and the elite benchmarks.
- Explain to a non-engineer how blue-green deployment makes undoing a release cheap, and when it does not.
- Explain to a junior engineer why a pipeline stage that never fails is a useless gate.

## Interleaving hooks

- configuration-management: baselines and change control are the discipline behind environment promotion (R1 in the review bank).
- software-lifecycle: Transition and Operation processes are what the pipeline enacts in ISO 12207 terms (R2/R3).
- quality-testing/test-automation: automated tests are the pipeline's gates; continuous testing is a measured DORA practice.
- security/secure-sdlc: shift-left security practices are measured in DORA 2021 and codified in CMMI's Security domain.
- observability: monitoring and observability practices are a DORA delivery practice; golden signals feed the rollback decision (worked example, step 6).
