---
id: quality-testing/quality-models
title: Quality Models
band: B5
track: quality-testing
tier: T2
bloom_target: understand
prerequisites: [engineering-process/requirements-engineering]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-quality-models
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0019, S-0108, S-0109, S-0110]
---

# Quality Models — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. The nine characteristics
- Q: List the nine product quality characteristics of ISO/IEC 25010:2023.
- bloom: remember
- bank: formative
- A: Functional suitability, performance efficiency, compatibility, interaction capability, security, safety, reliability, maintainability, flexibility.
- evidence: [S-0019]
- topic: quality-testing/quality-models

### F2. Two views of quality
- Q: In ISO 25010 terms, what is the difference between product quality and quality in use? Give an example of each.
- bloom: understand
- bank: formative
- A: Product quality concerns properties of the product itself — static and dynamic, e.g., "the checkout flow is modular (maintainability) and responds in 200 ms (performance efficiency)". Quality in use concerns the outcome of interaction — whether specific users achieve specific goals in a specific context, e.g., "customers complete checkout successfully 95% of the time". Product quality enables quality in use but does not guarantee it.
- evidence: [S-0019][S-0110]
- topic: quality-testing/quality-models

### F3. Measure categories
- Q: SQuaRE measurement distinguishes three categories of quality measures. Name them and give one example of each.
- bloom: understand
- bank: formative
- A: Quality measures on internal properties (static attributes of the product — e.g., cyclomatic complexity from code analysis), quality measures on external properties (dynamic behavior of the executing product — e.g., measured response time under load), and quality-in-use measures (outcomes in context — e.g., task completion rate by real users). They measure the product, its behavior, and its outcomes respectively.
- evidence: [S-0110]
- topic: quality-testing/quality-models

### F4. McCall's perspectives
- Q: Under which three perspectives did McCall et al. (1977) organize the quality factors, and which factors sit under each?
- bloom: remember
- bank: formative
- A: Product operation — correctness, reliability, efficiency, integrity, usability. Product revision — maintainability, flexibility, testability. Product transition — portability, reusability, interoperability.
- evidence: [S-0108]
- topic: quality-testing/quality-models

## Summative (mastery checkpoint)

### S1. Classify a quality problem
- Q: A review finds: users can complete checkout, but take unusually long because the multi-step form gives no progress feedback, and a subset of users with screen readers cannot complete it at all. Using ISO 25010:2023, identify the relevant characteristic(s)/subcharacteristic(s) and say which quality view each concern belongs to.
- bloom: understand
- bank: summative
- A: The no-progress-feedback issue is a product-quality concern: interaction capability — operability and self-descriptiveness (the user cannot recognize where they are); the screen-reader issue is interaction capability — inclusivity. The overall effect on completing purchases is a quality-in-use concern: effectiveness (goal achievement). Product quality properties (operability, inclusivity) enable, but do not guarantee, the quality-in-use outcome (effectiveness) in context.
- evidence: [S-0019]
- topic: quality-testing/quality-models

### S2. From requirement to characteristic
- Q: Map each requirement to the ISO 25010:2023 characteristic it belongs to: (a) "the app must keep working during a database outage", (b) "the system must handle 10,000 concurrent users", (c) "the UI must be usable by people with color blindness".
- bloom: apply
- bank: summative
- A: (a) reliability — fault tolerance (maintains performance despite faults; recoverability applies to the restoration after interruption); (b) performance efficiency — capacity (meets maximum limits of product parameters such as users and transactions); (c) interaction capability — inclusivity (usable by people with diverse characteristics). Each maps to a characteristic whose subcharacteristics then guide measures and tests.
- evidence: [S-0019]
- topic: quality-testing/quality-models

### S3. The traceability chain
- Q: Walk the SQuaRE chain from a quality requirement to a verdict, naming each artifact.
- bloom: understand
- bank: summative
- A: (1) Requirement stated in the vocabulary of the quality model: "availability of 99.9% under fault conditions" (reliability — fault tolerance/availability). (2) A quality measure is selected or defined for that characteristic per the measurement framework (25020) — e.g., proportion of time the service is available during fault-injection. (3) The product is evaluated: the measure is collected and compared against the requirement's target. (4) Verdict: requirement satisfied or not. Traceability means each requirement, measure, and evaluation result links through the model.
- evidence: [S-0019][S-0110]
- topic: quality-testing/quality-models

## Review (spaced repetition — interleaved with prerequisites)

### R1. NFRs vs FRs (from requirements-engineering)
- Q: A requirements document says: "The system shall send a receipt email after payment" and "The system shall send it within 30 seconds". Classify each and explain why the second needs a quality model to be useful.
- bloom: understand
- bank: review
- A: The first is a functional requirement (a behavior); the second is a non-functional requirement (a performance constraint). An NFR without a model has no structured home: ISO 25010 locates it under performance efficiency (time behavior), and the quality model then guides which measure (response time) and which evaluation compares the result to the 30-second target.
- evidence: [S-0019]
- topic: engineering-process/requirements-engineering

### R2. Evolution of the model
- Q: What changed in ISO 25010 between the 2011 and 2023 editions, and why does the change matter for quality requirements?
- bloom: understand
- bank: review
- A: 2011 had 8 characteristics (usability, portability); 2023 has 9: safety added, usability renamed interaction capability, portability renamed flexibility, and subcharacteristics added (inclusivity, resistance, scalability). The change matters because requirements vocabulary shifted: a 2023 spec can state safety requirements (fail-safe, hazard warning) and interaction requirements (inclusivity) that the 2011 model could not express directly.
- evidence: [S-0019]
- topic: quality-testing/quality-models

### R3. Writing a measurable NFR (from requirements-engineering)
- Q: Write an NFR for "the service must stay usable during surges" in measurable form, name its ISO 25010 characteristic, and propose one internal, one external, and one quality-in-use measure for it.
- bloom: apply
- bank: review
- A: NFR: "the service shall support 10,000 concurrent users with p95 response time under 300 ms" — characteristic: performance efficiency (capacity, time behavior). Measures: internal — static load/capacity model, resource-utilization review of the design; external — load-test results (throughput, p95 latency under 10,000 users); quality-in-use — user-reported success rate during a real traffic surge (effectiveness in context). The NFR's measurability is what the quality model and measurement framework supply.
- evidence: [S-0019][S-0110]
- topic: engineering-process/requirements-engineering
