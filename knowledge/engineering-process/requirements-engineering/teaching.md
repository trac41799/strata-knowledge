---
id: engineering-process/requirements-engineering
title: Requirements Engineering
band: B5
track: engineering-process
tier: T2
bloom_target: apply
prerequisites: []
related: []
recommended: []
status: published
schema-version: 1
owner: l1-requirements-engineering
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0020, S-0022, S-0073, S-0074, S-0075]
---

# Requirements Engineering — teaching

## Learning objectives (Bloom)

After studying this topic you will be able to:

- (remember) name the four elicitation technique families and the requirements process activities defined in 29148:2018;
- (understand) explain the difference between functional and non-functional requirements, and between verification and validation of requirements;
- (apply) elicit, specify, and validate requirements for a given scenario, applying the 29148 quality characteristics to write unambiguous, verifiable statements; (bloom target)
- (analyze) perform an impact analysis of a requirements change using traceability;
- (evaluate) judge whether a requirements set is good enough to build from, and assess claims about the cost of late defects.

## Worked example — from elicitation to specification

Scenario: a facility-maintenance company wants a field-sales app: technicians
visit clients and record maintenance quotes. "Just build it like our
spreadsheet" is the only brief.

1. **Elicit.** Run two interviews (a technician, a dispatcher) and one
   facilitated workshop with the manager. Findings: technicians work in
   basements with no connectivity; quotes must survive app restarts;
   dispatchers need today's visit list offline; the manager needs a
   "quote accepted" signal for billing. You also prototype a quote screen.
2. **Analyze.** Conflicts: manager wants mandatory client approval codes;
   technicians want to send quotes immediately and collect signatures
   later. Resolution: approval becomes a status, not a gate (offline
   workflow), plus a re-sync rule. Prioritize: offline operation is
   critical; e-mail PDF export is deferred.
3. **Specify.** Apply 29148 characteristics (unambiguous, singular,
   verifiable). Excerpt:

   - FR-12: "The app shall store a quote entered while offline in a local
     queue that survives an application restart. (singular, verifiable)"
   - FR-14: "When connectivity is available, the app shall transmit all
     queued quotes to the server within 60 seconds, resuming an
     interrupted transmission without data loss."
   - NFR-3: "The app shall support full read-write operation with no
     network access for at least 8 hours of continuous use on the
     reference device."
   - FR-18: "A quote shall be marked 'pending approval' until the
     technician records a client signature, regardless of connection
     state."

4. **Validate.** Walk the prototype through the offline scenario with the
   technician (prototype-based validation); review the specification for
   ambiguity; confirm NFR-3's "reference device" is defined so the test
   is feasible.
5. **Trace.** Record FR-12/14/18 and NFR-3 against sources (interview
   notes, workshop minutes) and to the planned tests, so the later change
   "add PDF export of quotes" can be impact-analyzed.

## Elaboration prompts

- Why is "shall" language and a singular focus per requirement worth the
  effort? What breaks downstream when a requirement is ambiguous?
- Why does ISO 12207 put requirements definition into two processes
  (stakeholder needs vs system/software requirements) instead of one?
- How does traceability change the cost of a late requirements change?
- When is a prototype better than an interview for eliciting needs?
- Why can verification pass while validation fails — and which one does
  the customer actually feel?

## Common misconceptions

1. **"Requirements are a list of features written once at the start."**
   RE is iterative and recursive across the life cycle; requirements
   evolve and change management is a core activity [S-0074][S-0073].
2. **"Fast, secure, user-friendly is a fine requirement."** Unverifiable
   and ambiguous language fails the 29148 quality characteristics; every
   requirement must be testable or it cannot be verified [S-0073].
3. **"Verification and validation are the same check."** Verification
   checks the artifact against the spec; validation checks the spec
   against the real need. A beautifully verified wrong product fails
   validation [S-0017][S-0020].
4. **"Traceability is bureaucratic overhead."** Without traceability,
   change impact analysis and completeness checking are guesswork; CMMI
   RDM treats bidirectional traceability as expected practice [S-0022].
5. **"Non-functional requirements are optional polish."** Qualities such
   as performance, security, and safety are requirements and must be
   stated and verified; ISO 25010 gives the vocabulary [S-0019].

## Feynman targets

- Explain to a project manager (2 minutes) why "building the right thing"
  and "building it right" are different risks, and which one
  requirements validation addresses.
- Explain to a junior developer why "the system shall be fast" is not a
  requirement, using the payment-gateway example.
- Explain why finding a requirements defect during operation is
  dramatically more expensive than finding it in elicitation — and why
  the exact multiplier is not the point.

## Interleaving hooks

- engineering-process/software-lifecycle — where requirements processes
  sit in ISO 12207's technical processes; revisit when studying
  Verification/Validation.
- quality-testing/software-testing-basics — acceptance tests are only as
  good as the requirements they trace to; testability is a requirements
  property.
- engineering-process/agile-methods — backlogs and user stories as a
  living requirements set; acceptance criteria as 29148-style quality
  criteria in another form.
- architecture-design/system-design-process — requirements (especially
  quality attributes) drive architecture; architecture choices constrain
  requirements feasibility.
- security/secure-sdlc — security requirements must be elicited and
  specified like any other requirement, not bolted on after design.
