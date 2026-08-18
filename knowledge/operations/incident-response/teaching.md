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

# Incident Response — teaching

## Learning objectives (Bloom)

After this pack the learner can:

- **remember** — state the postmortem definition, the four incident roles, and the definition of chaos engineering (F1–F2, R-items).
- **understand** — explain why postmortems must be blameless, why MTTR is the key emergency-response metric, and how severity shapes staffing (F3–F5).
- **apply (bloom_target)** — staff and run a response for a realistic incident: severity, roles, live incident document, timeline, escalation, postmortem writeup; design a hypothesis-driven chaos experiment.
- **analyze** — critique a postmortem draft for blamelessness and completeness; locate the failure mode in an unmanaged incident.
- **evaluate (stretch)** — judge whether a team's on-call and postmortem practices would sustain learning over time.

## Worked example 1 — incident timeline

Scenario: Acme Checkout (service "checkout") degrades after a deploy. Timeline, recorded in the live incident state document:

| Time | Event | Phase |
|---|---|---|
| 13:50 | Release v2.1.0 deployed (config change: new payment provider routing) | — |
| 14:02 | Alert: error rate >5% for 10 min; on-call paged | Detection |
| 14:05 | On-call acknowledges; declares incident, severity Sev1 (all checkout traffic affected, revenue loss) | Response |
| 14:08 | Commander assigned; ops lead + comms lead named; comms posts first stakeholder update | Response |
| 14:15 | Ops finds all errors are payment-provider timeouts; hypothesis: routing config regression; **no one else modifies the system** | Mitigation |
| 14:22 | Rollback to v2.0.8 (documented runbook); error rate dropping | Mitigation |
| 14:31 | Error rate back to baseline; monitoring shows recovery; incident closed | Resolution |
| 14:45 | Postmortem drafted (impact, trigger, detection, root cause, action items with owners) | Postmortem |

Worked reasoning: the team did not root-cause during the incident — they restored service first. The commander's job was delegation, not debugging. The communication lead's updates prevented stakeholder noise from reaching the ops team.

## Worked example 2 — postmortem writeup (modeled on Google's template)

**Incident #512 — Checkout payment failures (2026-08-19).**
- Summary: checkout error rate >5% for 29 minutes during peak; payment provider timeouts on a share of traffic.
- Impact: ~41k failed checkout attempts, ~12k lost orders, no data loss.
- Trigger: v2.1.0 introduced routing to a new payment provider without feature-flag protection.
- Detection: Borgmon-style error-rate alert paged on-call (manual detection would have been a monitoring failure — itself a postmortem trigger).
- Root causes: config regression (contributed: review gap — routing change not covered by the existing merge gate; runbook gap — rollback path discovered mid-incident).
- Resolution: rollback to v2.0.8; load shed on payment calls; provider routing re-enabled behind a flag.
- Action items (typed, owned, tracked): (1) make payment-provider routing changes merge-blocked review (prevent, owner, bug, TODO); (2) document checkout rollback runbook (process, owner, DONE); (3) add error-rate regression test for provider routing (prevent, owner, bug, TODO); (4) schedule a chaos experiment terminating one payment gateway connection (process, owner, TODO).
- What went right: on-call acknowledged within 3 minutes; no unauthorized changes during the incident.

This writeup is blameless: no person is indicted; every action item fixes the environment.

## Elaboration prompts

- Why must the incident commander NOT be the person debugging? What breaks if the highest-state person is also the most overloaded?
- Why is "the ops team is the only group modifying the system" a rule rather than a suggestion?
- A postmortem's action items are typed mitigate/prevent/process. What happens to a postmortem whose action items are all "mitigate"? Why?
- What does "fix the environment, not the people" mean for a team whose real problem is an undertrained on-call?
- Why does chaos engineering define steady state from *outputs* (error rate, latency) rather than internal attributes? What would happen if the hypothesis were about internals?
- Your alert pages at 3am every night. Is that an on-call problem or an alerting problem? Where does the SRE guidance (max ~2 pages/shift) point you?

## Common misconceptions

1. **"A blameless postmortem means no accountability."** Wrong: blamelessness is about where accountability lands — on processes, tools, and follow-up actions with owners, not on persons. Action items are tracked to completion precisely because the report is accountable.
2. **"Postmortems are paperwork after a failure."** Postmortems are the learning mechanism itself: criteria are set *before* incidents (downtime threshold, data loss, on-call intervention, long resolution, monitoring failure), they capture what went right too, and any stakeholder can request one.
3. **"The incident is over when the service is back up."** Restoration ends mitigation, not the incident: the postmortem and its action items are part of the lifecycle; without them the same class of incident recurs.
4. **"More people and more heroics fix incidents faster."** Uncoordinated response makes incidents spiral (the SRE book's unmanaged-incident portrait); the fix is roles, a live incident document, and escalation — plus preparation and practice, not last-minute heroics.
5. **"Chaos engineering is breaking production to have fun."** It is hypothesis-driven experimentation — steady state, control group, falsification — and advanced practice deliberately minimizes blast radius.

## Feynman targets

- Explain to a non-engineer (e.g., a product manager): what an incident is, why the company does postmortems, and why blaming the on-call is counterproductive.
- Explain to a junior engineer starting on-call: what a playbook is, what they should do in the first 15 minutes of a page, and when to escalate.
- Explain to a skeptical architect: what chaos engineering actually tests, and why the control/experimental group design matters.
- Explain to yourself in one paragraph: the difference between mitigation and root-cause — and when each is the right focus.

## Interleaving hooks

- **operations/observability (prerequisite):** monitoring/alerting feeds detection; "alert on symptoms, not causes" shapes what an incident looks like when it reaches the on-call.
- **operations/devops-pipeline:** deploy frequency and rollback capability decide how many incidents are self-inflicted — reversible releases shrink the mitigation phase.
- **engineering-process/software-lifecycle:** postmortem action items are lifecycle changes (requirements, design, testing); the 100x late-fix cost explains why detection matters.
- **quality-testing (forward link):** chaos experiments are reliability testing in production; error budgets and SLOs decide when to run them.
