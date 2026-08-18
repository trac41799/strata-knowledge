---
id: operations/software-maintenance
title: Software Maintenance
band: B4
track: operations
tier: T1
bloom_target: apply
prerequisites: [engineering-process/software-lifecycle]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-software-maintenance
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0020, S-0177, S-0178, S-0179]
---

# Software Maintenance

## Claims

- Software maintenance is the modification of a software product after delivery to correct faults, improve performance or other attributes, or adapt it to a changed environment [T2][S-0017][S-0020].
- ISO 12207 defines Maintenance as one of the technical processes of the software life cycle, spanning the operation and maintenance phase after delivery [T2][S-0020].
- SWEBOK v4 classifies maintenance into four types: corrective (fixing defects), adaptive (adapting to the environment), perfective (enhancing attributes), and preventive (preventing future issues) [T2][S-0017].
- Corrective maintenance fixes residual faults discovered after delivery — errors in design, logic, or code that prevent the software from meeting its specification [T2][S-0017].
- Adaptive maintenance modifies software to keep pace with a changing environment, for example upgrades to an operating system, hardware, or third-party dependencies [T2][S-0017].
- Perfective maintenance provides enhancements for users and improves performance, maintainability, or other software attributes [T2][S-0017].
- Preventive maintenance detects and corrects latent faults before they manifest as failures — proactive, risk-reducing maintenance [T2][S-0017].
- Maintenance commonly occupies over half of the total lifecycle costs of a software system, so design-for-maintainability is a first-order economic decision [T2][S-0017].
- A survey of 487 data processing organizations (Lientz & Swanson 1980) found that most maintenance requests — about 55% — were new requirements rather than corrections, and that most (at least half) of maintenance effort was perfective [T1][S-0179].
- Maintenance is therefore mostly evolution of functionality and adaptation to the environment, not repair: "bug fixing" is the minority share of maintenance work [T1][S-0179].
- Lehman's laws of software evolution describe regularities observed in the long-term evolution of large software systems, grounded in a longitudinal study of IBM's OS/360 [T1][S-0177].
- Lehman distinguished S-programs (spec-driven, fully verifiable), P-programs (problem-driven), and E-programs (embedded in the real world); the evolution laws concern E-programs, which must evolve because the world changes around them [T1][S-0177].
- The laws set down by 1980 include continuing change (an E-type program must be continually adapted or it becomes progressively less satisfactory), increasing complexity (complexity increases unless work is done to maintain or reduce it), and conservation of familiarity (excessive growth erodes the mastery needed to change a system) [T1][S-0177].
- Later work extended the laws to eight, adding continuing growth, declining quality, and feedback-system regularities [T1][S-0177].
- The technical debt metaphor was coined by Ward Cunningham (OOPSLA 1992): shipping first-time code is like going into debt — a little debt speeds development so long as it is paid back promptly with a rewrite [T3][S-0178].
- Unrepaid debt accrues interest: every minute spent on not-quite-right code counts as interest on that debt, and entire engineering organizations can be brought to a standstill under the debt load of an unconsolidated implementation [T3][S-0178].
- Technical debt is repaid by refactoring — restructuring code to reflect knowledge gained during the project; the metaphor is also a tool for explaining engineering trade-offs to management [T3][S-0178].
- Refactoring — restructuring existing code to improve its design — is itself a maintenance activity and the standard mechanism for repaying technical debt [T3][S-0178].

## Details

- Maintenance is change-driven: requests for modification enter a managed process of analysis, implementation, and regression verification before release [T2][S-0017].
- Understanding existing code is the precondition for any safe maintenance change; comprehension work precedes modification [T2][S-0017].

## Boundaries / common misunderstandings

- "Maintenance = bug fixing": most maintenance effort is perfective and adaptive — enhancements and environment adaptation — with corrections the minority [T1][S-0179].
- "Maintenance is the cheap tail of the lifecycle": maintenance commonly exceeds half of lifecycle costs; deferring it does not remove the cost, it moves it [T2][S-0017].
- "Lehman's laws say every program must rot": the laws are empirical regularities observed in large E-type systems, not inevitabilities — the complexity law explicitly describes work done to reduce complexity as part of evolution [T1][S-0177].
- "All technical debt is a mistake": Cunningham's framing treats a little debt as a deliberate accelerator, provided it is repaid promptly with a rewrite [T3][S-0178].
- "Preventive maintenance is just extra testing": it is proactive detection and correction of latent faults before they become failures, classified separately from the other types [T2][S-0017].

## References (evidence records)

- [S-0017] SWEBOK v4.0 — Software Maintenance KA (standard).
- [S-0020] ISO/IEC/IEEE 12207:2017 — Software life cycle processes, Maintenance technical process (standard).
- [S-0177] Lehman 1980 — Programs, Life Cycles, and Laws of Software Evolution (Proc. IEEE).
- [S-0178] Cunningham 1992 — The WyCash Portfolio Management System (OOPSLA '92).
- [S-0179] Lientz & Swanson 1980 — Software Maintenance Management (Addison-Wesley).
