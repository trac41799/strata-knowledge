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

# Incident Response

## Claims

- An incident is an event that disrupts or degrades a service; incident response is the organized practice of detecting, responding to, mitigating, and resolving it [T3][S-0167].
- Incident response follows a lifecycle — detection, response, mitigation, resolution, postmortem — and each phase has its own goals, roles, and artifacts [T3][S-0167].
- Detection is the first phase: monitoring and alerting surface service degradation, and the incident record documents how the incident was detected (e.g., "Borgmon detected a high level of HTTP 500s and paged on-call") [T3][S-0167].
- Playbooks — step-by-step response guides for alerts — record the severity and impact of each alert; in SRE practice, every alert gets a corresponding playbook entry [T3][S-0173].
- Severity classification ranks incidents by impact so that response urgency, staffing, and communication scale with the situation; playbooks explain the severity and impact of an alert so responders know what it means [T3][S-0173].
- SRE guidance targets at most two paging events per 8–12 hour on-call shift, so the on-call engineer has time to investigate thoroughly and to conduct postmortems [T3][S-0173].
- Being on-call means being available during a set period and ready to respond to production incidents with appropriate urgency; on-call engineers diagnose, mitigate, fix, or escalate incidents as needed [T3][S-0173].
- During an incident, response teams assign distinct roles: an incident commander holds high-level state and delegates; an ops lead applies operational tools; a communication lead issues periodic updates to the team and stakeholders; a planning role tracks longer-term issues [T3][S-0167].
- The operations team should be the only group modifying the system during an incident [T3][S-0167].
- Escalation widens the response: if you cannot find a solution, involve more of your teammates and seek help quickly — the highest priority is to resolve the issue at hand quickly, and exhaustive root-cause work can wait [T3][S-0167].
- The incident commander keeps a live incident state document (summary, status, command post, current commander); it can be messy but must be functional, and it is retained for postmortem analysis [T3][S-0167].
- A postmortem is a written record of an incident: its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring [T3][S-0167].
- Postmortems are blameless: they focus on process and technology, not people, and assume everyone involved was intelligent, well-intentioned, and making the best choices with the information they had [T3][S-0167].
- Since you cannot "fix" people, blameless postmortems fix the environment: improving system design to avoid entire classes of problems and making the right information easily available [T3][S-0167].
- Postmortem criteria should be defined before incidents occur: user-visible downtime beyond a threshold, data loss, on-call intervention (rollback, rerouting), resolution times above a threshold, and monitoring failures all trigger postmortems; any stakeholder may also request one [T3][S-0167].
- Postmortems are reviewed and published: drafts are shared internally, senior engineers assess completeness, and action items are tracked with owners and typed (mitigate, prevent, process) [T3][S-0167].
- A blameless postmortem culture is the first step in understanding what went wrong — and what went right [T3][S-0167].
- Reliability is a function of mean time to failure (MTTF) and mean time to repair (MTTR); the most relevant metric for evaluating emergency response is how quickly the response team brings the system back to health — the MTTR [T3][S-0167].
- Incident metrics track phases of the response lifecycle separately — mean time to detect (MTTD) versus mean time to repair (MTTR) — so improvement effort can be aimed at detection or at repair [T3][S-0167].
- Playbooks reduce the mean time to repair (MTTR) and the risk of human error during response [T3][S-0173].
- Chaos engineering is the discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions in production [T3][S-0174].
- Chaos experiments are hypothesis-driven: define a measurable steady state, hypothesize it continues, vary real-world events (server crashes, severed network connections, malfunctioning drives), and try to disprove the hypothesis by comparing control and experimental groups [T3][S-0174].
- The harder it is to disrupt the steady state, the more confidence we have in the system's behavior; weaknesses uncovered by experiments become improvement targets before they manifest at scale [T3][S-0174].
- Advanced chaos practice runs experiments in production, automates experiments to run continuously, and minimizes blast radius [T3][S-0174].
- Chaos engineering practice began at Netflix with Chaos Monkey (2011), which randomly terminated production instances to expose resilience weaknesses, later growing into the Simian Army suite of failure-injection tools [T3][S-0174].
- Incident management — incident response processes and postmortems — is part of the SWEBOK v4 Software Engineering Operations Knowledge Area [T2][S-0017].

## Details

- Google's SRE postmortem template anatomy: summary, impact, root causes, trigger, detection, resolution, action items — a structure learners can reuse [T3][S-0167].
- Postmortem action items are tabulated with type (mitigate/prevent/process), owner, bug, and status (DONE/TODO) [T3][S-0167].

## Boundaries / common misunderstandings

- "Postmortem = blame session": a blameless postmortem is the opposite — finger-pointing and shaming destroy the learning culture the postmortem exists to build [T3][S-0167].
- "Mitigation = root-cause fix": during the incident the priority is restoring service quickly; deep root-cause investigation happens after user impact is avoided [T3][S-0167].
- "More responders = faster recovery": ad hoc, uncoordinated response makes incidents worse; role assignment (commander, ops, communications) is what lets a response scale [T3][S-0167].
- "Postmortems are only for failures": they also capture what went right, and any stakeholder can request one for any event [T3][S-0167].
- "Chaos engineering = randomly breaking production": experiments are hypothesis-driven with a defined steady state and a control group, not disruption for its own sake [T3][S-0174].
- "On-call means heroics": on-call is a rotation with defined limits, playbooks, and escalation paths — sustainable practice, not sustained individual overtime [T3][S-0173].

## References (evidence records)

- [S-0017] SWEBOK v4.0 — Software Engineering Operations KA (standard).
- [S-0167] Beyer et al. 2016 — Site Reliability Engineering (O'Reilly).
- [S-0173] Beyer et al. 2018 — The Site Reliability Workbook (O'Reilly).
- [S-0174] Rosenthal & Jones 2017 — Principles of Chaos Engineering.
