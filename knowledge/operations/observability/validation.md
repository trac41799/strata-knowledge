---
id: operations/observability
title: Observability
band: B5
track: operations
tier: T2
bloom_target: apply
prerequisites: [operations/devops-pipeline]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-observability
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0020, S-0167, S-0168, S-0169]
---

# Observability — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. The three pillars
- Q: Name the three telemetry pillars (signals) and state, in one sentence each, what question each answers best.
- bloom: remember
- bank: formative
- A: Metrics — aggregated counts/values over time, best for detecting anomalies at scale ("is something wrong?"); logs — discrete event records, best for detail ("what exactly happened?"); traces — request paths across services, best for localization ("which component failed, in what order?"). In OpenTelemetry they are signals unified by context propagation.
- evidence: [S-0168]
- topic: operations/observability

### F2. Why cardinality is a hazard
- Q: Why can logging a user ID as a metric attribute cause unbounded memory growth, and what does the OTel metrics SDK do about it?
- bloom: understand
- bank: formative
- A: The SDK keeps a separate aggregation state (data point) per unique attribute combination, so cost scales with the number of distinct combinations, not request volume; user IDs produce one stream per user. The SDK enforces a per-stream cardinality limit (default 2,000 unique attribute combinations) and aggregates overflow under the `otel.metric.overflow=true` attribute instead of dropping data outright.
- evidence: [S-0168]
- topic: operations/observability

### F3. Set an SLO with an error budget
- Q: A payment API must be available 99.9% of a 30-day month. Define the SLI, the SLO, and the monthly error budget in minutes.
- bloom: apply
- bank: formative
- A: SLI: share of valid requests successfully completed (or service availability over the window); SLO: >= 99.9% over the month; budget: 0.1% of the window = 30d * 24h * 60min * 0.001 = 43.2 minutes of allowed failure. Incidents consume the budget; exhausting it should gate further releases.
- evidence: [S-0167]
- topic: operations/observability

## Summative (mastery checkpoint)

### S1. Instrument a checkout service
- Q: A checkout service has 8,000 req/min peak and a 3-tier backend. Specify: (a) the RED metrics to expose per service, (b) two cardinality rules for their attributes, (c) three alert rules written under the SRE alerting philosophy.
- bloom: apply
- bank: summative
- A: (a) Rate (requests/sec), Errors (failed requests/sec), Duration (latency histogram) per service; (b) never attach user IDs or raw URL paths as attributes (each unique combination is a new stream); keep attributes to a bounded set such as service, route template, status class, version; (c) alerts must be actionable and rare: e.g., page when error rate exceeds budget burn for the SLI (not on every error), page on p99 latency above the SLO threshold sustained for a few minutes, page on traffic collapse (sudden drop in rate) — each with a runbook; avoid per-instance noise alerts that cause pager burnout.
- evidence: [S-0169][S-0168][S-0167]
- topic: operations/observability

### S2. Burn-rate analysis
- Q: Your SLO is 99.9% availability over 30 days. An incident runs 6 hours at a 2% error rate. Compute the burn rate and the fraction of the error budget consumed, and decide whether releases should stop.
- bloom: analyze
- bank: summative
- A: Budgeted error rate = 0.1%; burn rate = 2% / 0.1% = 20x. At 20x burn the budget lasts 30d / 20 = 36 hours; 6 hours consumes 6/36 = 16.7% of the budget. Decision: releases continue is defensible but risky — two more incidents of similar size exhaust the budget. SRE practice gates releases on budget exhaustion (and pages well before it), so the correct action is: alert on projected exhaustion, keep releases running only if the remaining budget is judged sufficient, and re-evaluate after each incident.
- evidence: [S-0167]
- topic: operations/observability

### S3. Evaluate an observability claim
- Q: "We have dashboards showing 99.9% uptime for every service, so we are fully observable." Evaluate this statement.
- bloom: evaluate
- bank: summative
- A: Incorrect on both counts. Dashboards are consumers of telemetry, not the definition of observability — the capability is set by the signals emitted and the questions they can answer. Uptime alone is a weak SLI: it says nothing about latency (or error latency), so a slow degraded service can look "100% up". Observable systems expose structured logs, metrics with controlled cardinality, and traces with correlation, and their alerts follow the SLO/error-budget model rather than raw uptime.
- evidence: [S-0167][S-0168]
- topic: operations/observability

## Review (spaced repetition — interleaved with prerequisites)

### R1. The four DORA metrics (from devops-pipeline)
- Q: Name the four DORA key metrics and which pair measures throughput versus stability.
- bloom: remember
- bank: review
- A: Deployment frequency and lead time for changes (throughput); change failure rate and time to restore service / MTTR (stability).
- evidence: [S-0162]
- topic: operations/devops-pipeline

### R2. Monitoring as a delivery practice (from devops-pipeline)
- Q: DORA 2021 lists monitoring and observability practices among the technical practices of continuous delivery. Why does that belong in a pipeline topic?
- bloom: understand
- bank: review
- A: The pipeline's feedback loop only closes if changes are observed in production: deployment automation gives immediate feedback on each change, and monitoring/observability practices are what make the feedback visible. Release decisions (rollback vs ride-out) are made on telemetry, not on assumptions.
- evidence: [S-0163]
- topic: operations/devops-pipeline

### R3. Rollback decisions (from devops-pipeline)
- Q: In a blue-green deployment, why is rollback a routing decision, and what precondition makes it safe?
- bloom: apply
- bank: review
- A: The previous environment stays live, so rollback = re-routing traffic to it. The precondition is that the release's data migration can also be rolled back (zero-downtime design): an app rolled back on top of an irreversible migration is still broken.
- evidence: [S-0164]
- topic: operations/devops-pipeline
