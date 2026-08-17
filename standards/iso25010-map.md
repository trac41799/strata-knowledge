# ISO/IEC 25010:2023 — Product Quality Model (SQuaRE)

> Second edition (Nov 2023). Product quality model: **9 characteristics** (was 8 in 2011).
> Changes: Safety added; Usability → Interaction Capability; Portability → Flexibility;
> maturity → faultlessness; added subcharacteristics inclusivity, self-descriptiveness,
> user assistance (from accessibility), resistance, scalability. Source: ISO OBP change
> notes + iTeh official preview PDF + arc42 quality model (cross-verified).
> Home tracks: quality-testing (core), security, systems-software, architecture-design.

## Functional Suitability

- `quality-testing/functional-completeness` — functions cover all specified tasks and user objectives
- `quality-testing/functional-correctness` — functions provide accurate results for intended users
- `quality-testing/functional-appropriateness` — functions facilitate accomplishment of specified tasks, no unnecessary steps

## Performance Efficiency

- `quality-testing/time-behavior` — response time and throughput meet requirements
- `quality-testing/resource-utilization` — no more than the specified amount of resources (CPU, memory, storage, network)
- `quality-testing/capacity` — meets maximum limits of product parameters (users, transactions, bandwidth, DB size)

## Compatibility

- `systems-software/co-existence` — performs required functions while sharing common environment/resources with other products
- `systems-software/interoperability` — exchanges information with other products and mutually uses it

## Interaction Capability

- `quality-testing/appropriateness-recognizability` — users can recognize the product as appropriate for their needs
- `quality-testing/learnability` — users learn to use specified functions within a specified time
- `quality-testing/operability` — easy to operate and control
- `quality-testing/user-error-protection` — prevents operation errors
- `quality-testing/inclusivity` — usable by people with diverse characteristics (age, ability, culture, language, gender)
- `quality-testing/user-assistance` — supports users via multiple input/output methods (voice, gaze, touch)
- (also in the standard, not mapped: user engagement, self-descriptiveness)

## Reliability

- `quality-testing/faultlessness` — performs without faults under specified conditions (replaced 2011 "maturity")
- `quality-testing/fault-tolerance` — maintains performance despite faults or intrusions
- `quality-testing/availability` — available when required for use
- `quality-testing/recoverability` — restores state and data after interruption

## Security

- `security/confidentiality` — data accessible only to those authorized
- `security/integrity` — protects against unauthorized modification or destruction
- `security/non-repudiation` — actions can be proven to have taken place
- `security/accountability` — actions can be traced to the responsible entity
- `security/authenticity` — identity can be proven to be the one claimed
- `security/resistance` — sustains operation while under attack from malicious actors (new in 2023)

## Maintainability

- `quality-testing/modularity` — changes in one component have minimal impact on others
- `quality-testing/reusability` — assets can be leveraged across systems and projects
- `quality-testing/analysability` — defects, vulnerabilities and performance issues can be diagnosed efficiently
- `quality-testing/modifiability` — changes can be implemented without unintended side effects
- `quality-testing/testability` — objective, feasible tests can be designed and performed (ISO numbering 3.7.5, under maintainability)

## Flexibility

- `architecture-design/adaptability` — adjusts to different operating environments and configurations
- `architecture-design/installability` — efficient deployment and installation
- `architecture-design/replaceability` — can substitute for another product for the same purpose
- `architecture-design/scalability` — maintains performance and functionality as workloads grow (new in 2023)

## Safety

- `quality-testing/operational-constraint` — prevents operations that could create serious risk
- `quality-testing/risk-identification` — identifies and makes operational risks recognizable
- `quality-testing/fail-safe` — falls back to safe state on failure
- `quality-testing/hazard-warning` — warns users before unsafe actions or conditions
- `quality-testing/safe-integration` — preserves safety when integrated with other components/systems

## Sources

- ISO Online Browsing Platform (official, clauses incl. 3.7.5 testability, 3.8 flexibility, change notes): https://www.iso.org/obp/ui/en/#!iso:std:78176:en
- iTeh official preview PDF of ISO/IEC 25010:2023 (foreword change notes; definitions 3.1–3.4): https://cdn.standards.iteh.ai/samples/78176/13ff8ea97048443f99318920757df124/ISO-IEC-25010-2023.pdf
- arc42 quality model, ISO/IEC 25010 page (full 9-characteristic table; note: it lists testability under flexibility, which contradicts ISO numbering 3.7.5): https://quality.arc42.org/standards/iso-25010
