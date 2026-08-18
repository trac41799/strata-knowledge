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

# Observability

## Claims

- The three-pillar model (metrics, logs, traces) is implemented in OpenTelemetry as telemetry signals — traces, metrics, logs, plus baggage — unified by context propagation, a shared mechanism for correlating data across distributed systems [T3][S-0168].
- The signals are designed to complement each other: metrics detect anomalies at scale, logs carry event detail, traces show the path and order of a request; correlation is what ties them into one investigation [T3][S-0168].
- Structured logging: log records carry structured fields (timestamp, severity, body, attributes) plus trace/span correlation fields, so logs can be queried and correlated programmatically instead of grepped as free text [T3][S-0168].
- Metric cardinality is the number of unique attribute combinations reported per metric stream; high-cardinality attributes (user IDs, raw URL paths) drive memory cost and can cause unbounded growth, so the OTel metrics SDK enforces a per-stream cardinality limit (default 2,000 unique attribute combinations, overflow aggregated under `otel.metric.overflow=true`) [T3][S-0168].
- Distributed tracing models a request's path through services as spans linked by shared trace context; OpenTelemetry supports sampling decisions (at span creation and in the Collector) to bound volume and cost while preserving end-to-end traces [T3][S-0168].
- An SLI is a measurable indicator of service behavior (e.g., request latency, availability); an SLO is the target value or range the service aims to meet; an SLA is the contractual agreement with consequences for violation — defined in the SRE book's Service Level Objectives chapter [T3][S-0167].
- Error budgets follow from SLOs: the allowed failure budget (e.g., 0.1% of requests) is spent by incidents, and exhausting it gates releases — making reliability a product decision backed by data [T3][S-0167].
- The four golden signals of monitoring are latency, traffic, errors, and saturation; the SRE book recommends focusing on them for user-facing systems, and latency must be tracked separately for successful and failed requests ("a slow error is even worse than a fast error") [T3][S-0167].
- Monitoring serves three consumers: alerting, dashboards, and retrospective analysis (debugging); dashboards should answer basic questions about the service, typically including the golden signals [T3][S-0167].
- Alerting is for what needs action now — "something is broken, and somebody needs to fix it right now" — and the SRE book's rule-review questions exist to avoid false positives and pager burnout, the core control against alert fatigue [T3][S-0167].
- The RED method monitors, for every service, the request Rate, the Error rate of those requests, and a Duration (latency) distribution — a consistent per-service template that lets operational teams scale ("put people on call for code they didn't write") [T3][S-0169].
- RED is the request-oriented view for services; the USE method (Utilization, Saturation, Errors) is the resource-oriented view for infrastructure — the canonical treatments position the two against each other and against the four golden signals [T3][S-0169][S-0167].
- SLO targets give measurable form to codified quality characteristics: availability is a Reliability subcharacteristic and response latency is a Performance Efficiency (time behaviour) concern in ISO/IEC 25010:2023 [T2][S-0019].
- ISO/IEC/IEEE 12207:2017 defines a Measurement process (Technical Management) and an Operation process (Technical); runtime observability is how those processes are enacted on deployed software [T2][S-0020].
- SWEBOK v4.0 (2024) added Software Engineering Operations as a Knowledge Area and integrates Agile and DevOps across KAs, placing operations and observability inside the codified software engineering body of knowledge [T2][S-0017].

## Details

- Choosing an SLI means deciding what user-visible behavior to measure; the golden signals are defined for user-facing systems precisely because internal resource health is a proxy, not the user experience [T3][S-0167].
- Instrumentation is the foundation: signals must be emitted before any tool can consume them, which is why OpenTelemetry defines APIs/SDKs/OTLP plus the Collector rather than only backends [T3][S-0168].

## Boundaries / common misunderstandings

- "Observability means dashboards": dashboards and alert rules are consumers of telemetry; the observable capability comes from the signals emitted and the questions they can answer — the SRE book frames monitoring as serving alerting, dashboards, and retrospective analysis [T3][S-0167][S-0168].
- "More metrics means more observable": cardinality limits exist because unbounded attribute combinations are a cost and performance hazard — high-cardinality attributes can cause unbounded memory growth, not insight [T3][S-0168].
- "SLO = SLA": an SLO is an internal target with an error budget; an SLA is a contractual commitment with consequences (refunds, credits) — confusing them either overpromises to customers or under-manages internally [T3][S-0167].
- "Uptime is the only SLI that matters": a 99.9% uptime dashboard says nothing about latency or error latency — the golden signals and the success/failure latency distinction exist because user-visible behavior, not resource health, is the product [T3][S-0167].
- "Logs alone are observability": without correlation (trace context, structured fields), logs cannot be traced across services; the signals are designed to be queried together [T3][S-0168].

## References (evidence records)

- [S-0167] Beyer, Jones, Petoff & Murphy 2016 — Site Reliability Engineering (O'Reilly; sre.google).
- [S-0168] OpenTelemetry Specification and Documentation (CNCF, opentelemetry.io).
- [S-0169] Wilkie 2018 — The RED Method: How to Instrument Your Services (Grafana blog).
- [S-0019] ISO/IEC 25010:2023 — Product quality model (standard).
- [S-0020] ISO/IEC/IEEE 12207:2017 — Software life cycle processes (standard).
- [S-0017] SWEBOK v4.0 — Software Engineering Body of Knowledge, Operations KA (standard).
