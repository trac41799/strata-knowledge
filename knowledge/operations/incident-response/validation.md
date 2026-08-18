---
id: operations/incident-response
title: Incident Response
band: B5
track: operations
tier: T2
bloom_target: apply
prerequisites: [operations/observability]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-incident-response
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0167, S-0173, S-0174]
---

# Incident Response — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. Postmortem definition
- Q: What is a postmortem, and what five things must it record?
- bloom: remember
- bank: formative
- A: A postmortem is a written record of an incident: its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent it recurring — plus how it was detected.
- evidence: [S-0167]
- topic: operations/incident-response

### F2. Chaos engineering definition
- Q: State the definition of chaos engineering in one sentence.
- bloom: remember
- bank: formative
- A: The discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions in production.
- evidence: [S-0174]
- topic: operations/incident-response

### F3. Why blameless
- Q: A postmortem says "the on-call engineer made a bad decision under pressure." Why is that framing wrong, and what should the postmortem do instead?
- bloom: understand
- bank: formative
- A: Blameless postmortems focus on process and technology, not people; they assume everyone was intelligent, well-intentioned, and made the best choices with the information they had. The report should fix the environment — system design, information availability, tooling — because you cannot "fix" people.
- evidence: [S-0167]
- topic: operations/incident-response

### F4. Severity drives staffing
- Q: A Sev1 and a Sev3 alert both page. What does severity classification determine about the response, and where is severity recorded?
- bloom: understand
- bank: formative
- A: Severity ranks impact and determines response urgency, staffing, and communication scope. Playbooks record the severity and impact of each alert so a responder knows what it means before acting.
- evidence: [S-0173]
- topic: operations/incident-response

### F5. MTTR framing
- Q: Why does SRE practice treat MTTR as the most relevant emergency-response metric, and what is it a function of alongside?
- bloom: understand
- bank: formative
- A: Reliability is a function of mean time to failure (MTTF) and mean time to repair (MTTR); MTTR — how quickly the response team brings the system back to health — directly measures emergency response effectiveness.
- evidence: [S-0167]
- topic: operations/incident-response

## Summative (mastery checkpoint)

### S1. Staff and run a response
- Q: At 14:02 an alert fires: checkout-service error rate exceeds 5% for the past 10 minutes; a config change shipped at 13:50; the primary on-call is mid-debug; a VP asks for updates every 5 minutes; two engineers start making changes independently. Staff the incident and produce the first 30 minutes of a live incident state document.
- bloom: apply
- bank: summative
- A: Declare the incident and assign roles: incident commander (holds state, delegates, keeps the incident document with summary/status/command post/commander), ops lead (only the ops team modifies the system — halt the two independent change-makers), communication lead (periodic updates to the VP and stakeholders, keeps the document accurate), planning (tracks divergences, files bugs). First document entries: summary (checkout-service error rate >5%, suspected config change at 13:50), status active, severity per impact, timeline of alerts/actions, current hypothesis, next check-in time. Escalate to the change owner if the config hypothesis stalls; restore service before root-causing.
- evidence: [S-0167][S-0173]
- topic: operations/incident-response

### S2. Critique a postmortem
- Q: A postmortem draft contains: "Engineer A was careless deploying without review; fix: write Engineer A up." Identify why this fails as a postmortem and rewrite the offending sections to the SRE standard.
- bloom: analyze
- bank: summative
- A: It fails the blameless test: it indicts a person instead of the process and proposes a people-fix, not an environment-fix. Rewrite: contributing factors — deploy proceeded without review because the review requirement was not enforced by the pipeline (process); the rollback path was undocumented, slowing mitigation (documentation); action items typed mitigate/prevent/process with owners — e.g., "make review a merge-blocking check (prevent, owner, bug, TODO)" and "document rollback runbook (process, owner, DONE)". Include impact, trigger, detection, resolution.
- evidence: [S-0167]
- topic: operations/incident-response

### S3. Design a chaos experiment
- Q: Design a chaos experiment for a payment API whose SLO is 99.9% availability. Specify steady state, hypothesis, variables, control vs experimental group, and how you would disprove the hypothesis — then say why running it in production is the advanced practice.
- bloom: apply
- bank: summative
- A: Steady state: measurable output — e.g., payment API error rate and p99 latency over a 15-minute window. Hypothesis: steady state continues when one of three API nodes is terminated. Variable: terminate one node (real-world event). Experimental group: API serving synthetic load during termination; control: identical API without termination. Disprove by comparing steady state between groups; the harder the disruption, the more confidence. Advanced practice runs such experiments in production (with minimized blast radius) because only production conditions produce trustworthy evidence; automate to run continuously.
- evidence: [S-0174]
- topic: operations/incident-response

## Review (spaced repetition — interleaved with prerequisites)

### R1. What pipelines are for (from devops-pipeline)
- Q: What is the purpose of a continuous integration / continuous delivery pipeline, and why is it a precondition for safe frequent releases?
- bloom: understand
- bank: review
- A: A pipeline automates build, test, and deployment stages so every change is verified before it reaches production; automation makes release repeatable, fast, and reversible — the precondition for the high-frequency releases incident response must cope with.
- evidence: [S-0017][S-0020]
- topic: operations/devops-pipeline

### R2. Reversibility under fire
- Q: Why must a deployment be reversible (rollback-capable) before a team can safely operate high release frequency?
- bloom: apply
- bank: review
- A: When a release degrades the service, the fastest mitigation is often a rollback; if rollback is untested or manual, time-to-repair stretches and incident risk rises. Reversibility converts deployment failures from incidents into routine reverts.
- evidence: [S-0167]
- topic: operations/devops-pipeline

### R3. Monitoring vs alerting boundary (from devops-pipeline)
- Q: Distinguish monitoring from alerting, and say what an alert must contain to be actionable for an on-call engineer.
- bloom: understand
- bank: review
- A: Monitoring collects and displays signals; alerting decides when a signal requires human attention. An actionable alert is tied to a playbook entry that explains the severity and impact of the alert and gives debugging/mitigation steps.
- evidence: [S-0173]
- topic: operations/devops-pipeline
