# ISO/IEC/IEEE 12207:2017 — Software Life Cycle Processes (topic map)

> Verified against the official ISO/IEC/IEEE 12207:2017(E) preview PDF (clause 6 TOC):
> 30 processes in 4 process groups — Agreement (2), Organizational Project-Enabling (6,
> includes Knowledge Management), Technical Management (8, includes Measurement),
> Technical (14, "System/Software requirements definition" per the 2017 text).
> Ids are expected topics for `tools/coverage.py`.

## Agreement Processes

### Acquisition
- `engineering-process/acquisition` — acquisition planning, supplier selection, agreement management

### Supply
- `engineering-process/supply` — proposal response, contract negotiation, product delivery

## Organizational Project-Enabling Processes

### Life Cycle Model Management
- `engineering-process/software-lifecycle` — life cycle model selection, stage definitions
- `engineering-process/process-tailoring` — tailoring the process set to a project

### Infrastructure Management
- `operations/infrastructure-management` — environments, tools, and facilities that support projects

### Portfolio Management
- `engineering-process/portfolio-management` — prioritizing and balancing projects against strategy

### Human Resource Management
- `engineering-process/human-resource-management` — skills, staffing, and personnel development

### Quality Management
- `engineering-process/quality-management` — quality policy, objectives, and continuous improvement

### Knowledge Management
- `engineering-process/knowledge-management` — capturing and sharing organizational knowledge

## Technical Management Processes

### Project Planning
- `engineering-process/project-planning` — work breakdown, schedules, and project plans
- `engineering-process/effort-estimation` — size and effort estimation for software work

### Project Assessment and Control
- `engineering-process/project-control` — progress assessment and corrective action

### Decision Management
- `engineering-process/decision-management` — decision alternatives and trade-offs

### Risk Management
- `engineering-process/risk-management` — risk identification, analysis, and mitigation
- `security/risk-analysis` — security risk assessment of the software system

### Configuration Management
- `engineering-process/configuration-management` — baselines, change, and release control

### Information Management
- `engineering-process/information-management` — information items, records, and retention

### Measurement
- `engineering-process/measurement` — measurement objectives and indicators
- `quality-testing/software-metrics` — quantitative software measurement

### Quality Assurance
- `quality-testing/quality-assurance` — assurance of process and product conformance

## Technical Processes

### Business or Mission Analysis
- `engineering-process/business-analysis` — mission, problem space, and solution concept

### Stakeholder Needs and Requirements Definition
- `engineering-process/requirements-elicitation` — stakeholder needs capture
- `engineering-process/stakeholder-needs` — needs validation and agreement

### System/Software Requirements Definition
- `engineering-process/requirements-specification` — functional and non-functional requirements
- `engineering-process/requirements-engineering` — requirements analysis and management

### Architecture Definition
- `architecture-design/software-architecture` — architectural viewpoints and trade-offs
- `hardware/isa-basics` — platform and instruction-set constraints

### Design Definition
- `architecture-design/design-principles` — modularity, cohesion, coupling
- `architecture-design/detailed-design` — component and interface design

### System Analysis
- `engineering-process/trade-off-analysis` — feasibility, sensitivity, and trade studies

### Implementation
- `programming/coding-practices` — coding standards and construction
- `quality-testing/unit-testing` — unit-level testing

### Integration
- `operations/continuous-integration` — incremental assembly of software items
- `systems-software/component-integration` — integration with platform components

### Verification
- `quality-testing/software-testing-basics` — test levels and strategies
- `quality-testing/verification-techniques` — reviews, inspections, and tests

### Transition
- `operations/deployment-and-rollout` — deployment and user transition
- `operations/release-management` — release preparation and packaging

### Validation
- `quality-testing/acceptance-testing` — acceptance criteria and stakeholder sign-off
- `quality-testing/software-testing-basics` — validation testing

### Operation
- `operations/incident-management` — operation and user support
- `operations/monitoring-and-observability` — runtime monitoring

### Maintenance
- `operations/software-maintenance` — corrective, adaptive, and perfective maintenance
- `operations/change-management` — change request handling

### Disposal
- `operations/system-retirement` — decommissioning and data disposition

## Sources

- https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:12207:ed-1:v1:en (official OBP, clause 6 TOC)
- https://www.normservis.cz/download/view/iec/info_isoiecieee12207%7Bed1.0%7Den.pdf (official 12207:2017(E) preview PDF — TOC verified directly)
- https://en.wikipedia.org/wiki/ISO/IEC_12207 (structure and revision history)
