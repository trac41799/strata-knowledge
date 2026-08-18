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

# Observability — teaching

## Learning objectives (Bloom)

By the end of this topic, the learner can:

- remember: name the telemetry signals, the four golden signals, and the SLI/SLO/SLA distinction.
- understand: explain why high cardinality is a memory/performance hazard and how limits + overflow work.
- apply: define SLIs and SLOs for a service and compute error budgets and burn rates.
- apply: instrument a service with RED metrics and write alert rules that respect the SRE alerting philosophy.
- evaluate: judge "we have dashboards/uptime, therefore we are observable" claims against the signals model and SLO practice.

## Worked example

**SLO burn-rate calculation for the checkout API.**

Setup: SLI = share of requests completed successfully; SLO = 99.9% over a 30-day month; budgeted failure = 0.1% of traffic (43.2 minutes of allowed outage if measured in time).

1. Budget in error-rate terms: 0.1% of requests may fail.
2. Incident: 2% of requests fail for 6 hours.
3. Burn rate = actual error rate / budgeted error rate = 2% / 0.1% = 20x. At 20x burn, the whole monthly budget would be consumed in 30 days / 20 = 36 hours.
4. Budget consumed by 6 hours at 20x = 6 / 36 = 16.7%. Remaining: 83.3% of the month's error budget.
5. Decision logic: one such incident is uncomfortable but not budget-exhausting; a release freeze triggers at exhaustion, so the team flags the burn, pages the on-call (alert threshold set so the page fires while action is still possible — e.g., projected exhaustion within hours, not after), and re-evaluates the freeze only if the budget keeps burning.
6. Alert-design lesson: alerting on the burn rate — not on every 5xx — keeps pages rare and actionable, which is exactly the SRE book's anti-fatigue philosophy ("avoid false positives and pager burnout").

What this example teaches: error budgets convert reliability goals into arithmetic; burn rate turns incidents into budget accounting; alerting on burn (not noise) is the operational control for alert fatigue.

## Elaboration prompts

- Why must latency be tracked separately for successful and failed requests? What misleading conclusion does blended latency invite?
- Why does cardinality scale with distinct attribute combinations rather than request volume? Give an attribute that is safe and one that is not.
- RED and USE both describe three letters. What is each "three" a view of, and what does each miss that the other covers?
- Why is an SLA different from an SLO, and what happens if you publish your internal SLO as an SLA?
- In the worked example, why does the alert fire on projected budget exhaustion instead of on the raw error rate?

## Common misconceptions

- "Observability means having dashboards." Dashboards are consumers of telemetry; observability is the property of being able to answer questions from the signals emitted. A dashboard over weak signals is decoration.
- "More metrics/logs = more observability." Unbounded cardinality is a cost and performance hazard (one stream per attribute combination, default cap 2,000), and unsearchable log text is not signal.
- "SLO and SLA are the same thing." SLO is the internal target with an error budget; SLA is the contractual commitment with consequences. Confusing them overpromises externally or under-manages internally.
- "Uptime is the SLI." A 99.9% uptime number says nothing about latency or error latency; the golden signals exist because user-visible behavior is what matters.
- "Page on every anomaly." The SRE alerting philosophy reserves pages for "somebody needs to fix it right now" — alerting on every deviation is how pager burnout (and ignored pages) is manufactured.

## Feynman targets

- Explain to a non-engineer why "we're 99.9% up" and "our users are happy" are not the same statement.
- Explain to a junior developer why adding `user.id` to a metric attribute is dangerous while adding it to a log record is fine.
- Explain to a product manager how an error budget turns the question "should we release?" into arithmetic.

## Interleaving hooks

- devops-pipeline: monitoring/observability is a measured DORA delivery practice; rollback decisions are made on telemetry (review bank R1–R3).
- quality-testing/performance-engineering: load and soak tests define the capacity baselines that capacity-signal alerts compare against.
- architecture-design: loosely coupled services are independently deployable AND independently observable — trace context is what reassembles the request path.
- engineering-process/software-lifecycle: the ISO 12207 Measurement process is what runtime observability enacts; quality characteristics in ISO 25010 are what SLOs quantify.
- security: structured logs and traces feed security review (shift-left practices measured in DORA 2021); cardinality discipline protects log/metric pipelines from abuse.
