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

# DevOps Pipeline

## Claims

- The deployment pipeline is the automated sequence through which every change travels from commit toward production — canonical stages include commit, acceptance, capacity, manual, and production — with each stage raising confidence that the change is releasable [T3][S-0164].
- The pipeline is a feedback mechanism, not just an automation script: deployment automation gives immediate feedback on each change, which DORA research associates with faster and more reliable delivery [T1][S-0163].
- Continuous integration (integrating, building, and testing every commit) and continuous testing are complementary practices: DORA 2021 found continuous testing a strong predictor of successful continuous delivery — elite performers who meet reliability targets are more likely to use it — and recommends implementing the two together [T1][S-0163].
- Deployment automation — moving software from testing to production automatically — decreases lead time and reduces the deployment errors that are more common in manual deployments [T1][S-0163].
- DORA's continuous-delivery research also measures loosely coupled architecture, trunk-based development, open-source use, monitoring and observability practices, and management of database changes as technical practices of delivery [T1][S-0163].
- Loosely coupled architecture is one of the strongest predictors of successful continuous delivery: teams that can deploy services independently move faster and recover faster from failure [T1][S-0163].
- Accelerate (2018) codifies the DORA research as 24 capabilities in five categories — continuous delivery, architecture, product & process, lean management & monitoring, and culture — that predict delivery performance [T1][S-0162].
- DORA defines four key metrics of software delivery: deployment frequency, lead time for changes, time to restore service (MTTR), and change failure rate — the first two measuring throughput, the last two stability [T1][S-0162][S-0163].
- The metrics benchmark organizations into elite, high, medium, and low performer clusters via cluster analysis, so a team can compare its delivery against an industry dataset [T1][S-0163].
- On the 2021 benchmarks, elite performers deploy on demand (multiple times per day), report lead time for changes under one hour, a change failure rate of 0–15%, and restore service in under one hour; relative to low performers they show ~973x more frequent deployments, ~6,570x faster lead time and recovery, and ~3x lower change failure rate [T1][S-0163].
- Blue-green deployment runs the new version in a parallel environment, validates it there, then switches production traffic to it; rollback is instant re-routing to the previous environment, which stays live [T3][S-0164].
- The blue-green technique originates with Dan North and Jez Humble (c. 2005) during the work that became the Continuous Delivery book [T3][S-0164].
- Zero-downtime release design treats rollback as a first-class requirement — including rolling back database changes — because a release that cannot be undone safely is not a low-risk release [T3][S-0164].
- Deployment and operation are codified lifecycle processes: ISO/IEC/IEEE 12207:2017 includes a Transition process (installing the software and handing it over to operation) and an Operation process that runs it in service [T2][S-0020].
- Promoting builds through environments (dev → test → staging → production) is configuration management in practice: ISO 12207's Configuration Management process and CMMI V3.0's Configuration Management practice area govern baselines, version control, and controlled change — the discipline behind promoting approved baselines [T2][S-0020][S-0022].
- Pipeline security follows from codified process assurance: CMMI V3.0 defines a Security domain with an Ensure Security (ESEC) practice area, making security assurance of organizational processes a codified practice area rather than an add-on [T2][S-0022].
- DORA 2021 measures shift-left security practices — security reviews, integrating security reviews into every phase, and inviting security specialists early — as part of delivery, aligning with the security domain codified in CMMI [T1][S-0163][S-0022].
- SWEBOK v4.0 (2024) added Software Engineering Operations as a Knowledge Area and integrates Agile and DevOps across KAs, placing delivery operations inside the codified software engineering body of knowledge [T2][S-0017].

## Details

- Trunk-based development keeps integration risk low by integrating small batches on a shared mainline instead of long-lived branches [T1][S-0163].
- Automation is the means, not the goal: the 24 capabilities span architecture, culture, and monitoring alongside delivery automation, so high performance is a system property, not a tool purchase [T1][S-0162].

## Boundaries / common misunderstandings

- "DORA metrics measure activity": they measure delivery outcomes — how often, how fast, and how stable delivery is — not activity counts such as commits, lines of code, or story points [T1][S-0163][S-0162].
- "A pipeline is a process": tooling automates steps, but the processes that make delivery reliable — verification, quality assurance, configuration management — are defined and enacted independently of any tool [T2][S-0020].
- "More deployments mean more risk": the elite cluster is simultaneously faster (973x more frequent deploys) and more stable (3x lower change failure rate) than low performers; speed and stability are not traded off [T1][S-0163].
- "Blue-green guarantees zero risk": switching traffic is instant, but data migrations can make rollback unsafe unless the release was designed for it (e.g., rollback scripts for database changes) [T3][S-0164].
- "DevOps is a role or a toolset": the DORA research operationalizes DevOps as measurable capabilities and outcomes, and SWEBOK v4.0 treats it as engineering practice integrated across knowledge areas [T1][S-0162][S-0017].

## References (evidence records)

- [S-0162] Forsgren, Humble & Kim 2018 — Accelerate: The Science of Lean Software and DevOps (IT Revolution Press).
- [S-0163] DORA 2021 — Accelerate State of DevOps Report 2021 (Google Cloud, dora.dev).
- [S-0164] Humble & Farley 2010 — Continuous Delivery (Addison-Wesley).
- [S-0017] SWEBOK v4.0 — Software Engineering Body of Knowledge, Operations KA (standard).
- [S-0020] ISO/IEC/IEEE 12207:2017 — Software life cycle processes (standard).
- [S-0022] CMMI V3.0 — Capability Maturity Model Integration (standard).
