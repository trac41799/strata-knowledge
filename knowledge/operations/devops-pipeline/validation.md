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

# DevOps Pipeline — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. The four key metrics
- Q: Name the four DORA key metrics and state which two measure throughput and which two measure stability.
- bloom: remember
- bank: formative
- A: Deployment frequency and lead time for changes (throughput); change failure rate and time to restore service / MTTR (stability).
- evidence: [S-0162][S-0163]
- topic: operations/devops-pipeline

### F2. Why deployment automation helps
- Q: DORA 2021 found deployment automation improves delivery. Explain the two mechanisms it identifies.
- bloom: understand
- bank: formative
- A: (1) Automated movement from testing to production decreases lead time by enabling faster, more efficient deployments; (2) it reduces the likelihood of deployment errors, which are more common in manual deployments. It also gives immediate feedback on each change.
- evidence: [S-0163]
- topic: operations/devops-pipeline

### F3. Classify a team's delivery
- Q: A team deploys twice a month, has a lead time of two weeks, a change failure rate of 30%, and restores service in two days. Classify them against DORA's 2021 benchmarks and pick the metric that most plausibly improves first with a deployment pipeline.
- bloom: apply
- bank: formative
- A: All four numbers land in or near the low-performer cluster (elite: on-demand deploys, lead time < 1 hour, CFR 0–15%, restore < 1 hour). Deployment frequency and lead time improve first once a pipeline automates integration and deployment, because automation directly shortens the commit-to-production path; CFR and MTTR typically follow once fast feedback and rollback tooling exist.
- evidence: [S-0163]
- topic: operations/devops-pipeline

## Summative (mastery checkpoint)

### S1. Design a pipeline for a checkout service
- Q: Design the pipeline stages for a payment-checkout service that must never exceed a 1% change failure rate. Specify where quality gates and security checks sit, and how promotion through environments is controlled.
- bloom: apply
- bank: summative
- A: Stages per the deployment pipeline pattern: commit (CI build + unit tests), acceptance (integration/e2e against a test environment), capacity (load/soak), manual approval for production, production deployment via blue-green. Quality gates: automated tests must pass per stage; security gates are integrated into every phase, not bolted on at the end (shift-left: security reviews early, per DORA's measured practices). Promotion is configuration management: each environment holds a controlled baseline; only an approved baseline moves to the next environment, with changes tracked and reversible (zero-downtime design incl. database rollback scripts).
- evidence: [S-0164][S-0163][S-0020][S-0022]
- topic: operations/devops-pipeline

### S2. Roll back or ride it out?
- Q: A blue-green release of v2.4 was fully switched to production. Monitoring shows p99 latency up 3x and the change failure rate climbing. You have a database migration in the release. Decide and justify: roll back, and what must hold for the rollback to be safe?
- bloom: analyze
- bank: summative
- A: Roll back by re-routing traffic to the previous environment — that is the point of blue-green (instant rollback). The precondition: the rollback must also undo or tolerate the data migration; if the migration is one-way and non-idempotent, rolling back the app on top of migrated data can make things worse. Zero-downtime release design requires a rollback path for database changes before the release is approved. After recovery, measure time to restore service (MTTR) and treat the incident as data for the next release decision.
- evidence: [S-0164][S-0163]
- topic: operations/devops-pipeline

### S3. Evaluate a delivery doctrine
- Q: "If our dashboards are green and we deploy daily, we are a high-performing team." Evaluate this claim using the DORA evidence and the process view from ISO 12207.
- bloom: evaluate
- bank: summative
- A: Mostly incorrect. Daily deploys alone say nothing about lead time, change failure rate, or restore time — performance is a cluster profile across all four metrics, not deployment frequency alone, and dashboards are not the evidence base. The process view adds: delivery reliability requires the enacted processes (verification, quality assurance, configuration management) around the tooling. High performance is a system property across the 24 capabilities, not a green dashboard.
- evidence: [S-0163][S-0162][S-0020]
- topic: operations/devops-pipeline

## Review (spaced repetition — interleaved with prerequisites)

### R1. Baselines and change control (from configuration-management)
- Q: What is a configuration baseline, and why does controlled change matter when a build moves between environments?
- bloom: remember
- bank: review
- A: A baseline is a formally reviewed, frozen configuration item that subsequent work builds on; CMMI's Configuration Management practice area governs establishing baselines, versioning, and controlling changes to them. Controlled change matters because promotion decisions must be reproducible: if anyone can mutate an environment outside version control, the pipeline cannot reproduce or roll back the state that is in production.
- evidence: [S-0022]
- topic: engineering-process/configuration-management

### R2. Lifecycle processes around delivery (from software-lifecycle)
- Q: ISO/IEC/IEEE 12207:2017 is model-neutral. Why does that matter when a team adopts a deployment pipeline?
- bloom: understand
- bank: review
- A: The standard defines processes (Transition, Operation, Verification, Configuration Management, etc.) without prescribing waterfall, iterative, or agile models. A deployment pipeline enacts those processes inside whatever model the project selected — the pipeline is the mechanism, the standard is the process contract.
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle

### R3. Tailoring for a pipeline team (from software-lifecycle)
- Q: Which ISO 12207 processes would you explicitly tailor in for a small team running a deployment pipeline, and which could be lightened?
- bloom: apply
- bank: review
- A: Keep: requirements, design, implementation, integration, verification, validation, transition, operation, configuration management, risk management, quality assurance. Lighten: heavyweight agreement and information-management artifacts until the product stabilizes. The tailored set must still satisfy process purposes — tailoring is selection, not omission of purpose.
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle
