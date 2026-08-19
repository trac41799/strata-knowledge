---
id: security/threat-modeling
title: Threat Modeling
band: B5
track: security
tier: T2
bloom_target: apply
prerequisites: [architecture-design/architectural-styles, systems-software/networking-basics]
related: [security/cryptography-basics, security/web-security]
recommended: [security/secure-sdlc]
status: draft
schema-version: 1
owner: l1-threat-modeling
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0019, S-0237, S-0238, S-0239]
---

# Threat Modeling — validation

## Formative (practice)

### Q1
- Q: Name the six STRIDE threat categories and the security property each one violates.
- bloom: remember
- bank: formative
- A: Spoofing→Authentication, Tampering→Integrity, Repudiation→Non-repudiation, Information disclosure→Confidentiality, Denial of service→Availability, Elevation of privilege→Authorization.
- evidence: [S-0237]
- topic: security/threat-modeling

### Q2
- Q: A bug lets an anonymous user read other users' private messages by guessing message IDs. Which STRIDE categories does this bug instantiate, and which does it not? Explain the distinction.
- bloom: understand
- bank: formative
- A: It instantiates Information disclosure (Confidentiality — data exposed to an unauthorized party). It is not Spoofing (no identity is impersonated — the attacker acts anonymously), not Tampering (no data modified), and not Elevation of privilege in the strict sense unless the read requires higher authorization than the attacker holds; a system where any user may read any message is a disclosure design flaw, not an elevation.
- evidence: [S-0237]
- topic: security/threat-modeling

### Q3
- Q: Given this DFD fragment — [User] --login--> [WebApp] --query--> [Database], with a trust boundary around WebApp+Database — list at least one realistic threat per STRIDE category for the login data flow.
- bloom: apply
- bank: formative
- A: Spoofing: attacker impersonates a user (stolen/guessed credentials, replay). Tampering: login request modified in transit. Repudiation: user denies having logged in without an audit trail. Information disclosure: credentials or session token sniffed on the wire if unencrypted. Denial of service: flooding the login endpoint exhausts resources. Elevation of privilege: attacker uses a flaw in the app or DB to gain admin rights beyond their own.
- evidence: [S-0237]
- topic: security/threat-modeling

## Summative (mastery checkpoint)

### Q4
- Q: Build an attack tree for the goal "steal a session token" with at least two OR branches and one AND node, then state which branch an analyst would choose if each leaf were tagged with an estimated cost.
- bloom: apply
- bank: summative
- A: Root: steal session token. OR branches: (1) intercept in transit — AND(attacker on the path, transport not encrypted); (2) read from storage — AND(gain code execution on client, locate token store); (3) guess/forge it — AND(predictable token generator, compute valid value). Analyst picks the path minimizing total cost subject to feasibility — e.g., sniffing an unencrypted flow may cost ~0 while forging a cryptographic token is infeasible; the cheapest feasible path is the one to mitigate first.
- evidence: [S-0238]
- topic: security/threat-modeling

### Q5
- Q: A team reports "we ran a pentest and found nothing, so we don't need a threat model." Analyze why a clean pentest does not establish that the design has no threats, and what design-time analysis adds.
- bloom: analyze
- bank: summative
- A: A pentest exercises an existing implementation against known attack patterns; it cannot find threats that the design makes possible but that were not probed, and it cannot see threats at all before code exists. Threat modeling examines the design systematically (STRIDE per element, attack trees on goals), so it covers categories a test battery may never reach — e.g., repudiation (no audit trail) or design-level denial of service. The two are complements: model finds what to test; tests validate the model.
- evidence: [S-0237][S-0238]
- topic: security/threat-modeling

### Q6
- Q: Your threat model lists: (a) unauthenticated admin API, (b) server crashes on malformed input, (c) log spam, (d) slow-but-possible brute force on API tokens, (e) insider copying public reports. Rank them for immediate mitigation and justify; state which you would accept with a rationale.
- bloom: evaluate
- bank: summative
- A: Highest risk first: (a) unauthenticated admin API — trivial attack, catastrophic impact → mitigate now. (b) malformed-input crash — easy to exploit remotely, high availability impact → mitigate now. (d) brute force on tokens — credible over time, mitigate (rate limiting) or accept with documented compensating controls. (e) insider copying public data — low impact, accept with rationale (data is public by design). (c) log spam — nuisance, accept and monitor. The ranking uses likelihood × impact; whatever is not mitigated is explicitly rationalized rather than ignored.
- evidence: [S-0237]
- topic: security/threat-modeling

## Review (spaced repetition — interleaved with prerequisites)

### Q7
- Q: Your threat model was reviewed and signed off last quarter; this quarter you added a public file-upload endpoint, moved storage to a new provider, and disabled TLS on an internal link. Which parts of the model are now untrustworthy, and why? (Revisit: what makes a model "living"?)
- bloom: understand
- bank: review
- A: All three changes invalidate parts of the model: the upload endpoint adds new processes/data flows and attack surface (tampering, DoS, EoP vectors), the storage migration changes data stores and trust boundaries (new provider = new trust domain), and disabling TLS turns an internal flow into a sniffing/tampering target. Because security is integrated throughout the lifecycle, the model must be re-examined on design, deployment, or threat-landscape changes — it is a living artifact, not a one-time diagram.
- evidence: [S-0017][S-0237]
- topic: security/threat-modeling

### Q8
- Q: Garlan & Shaw describe pipes-and-filters as a data-flow style (filters connected by pipes, no shared state). Why is a data-flow view of an architecture a natural basis for threat analysis, and what does a filter's black-box boundary correspond to? (Architecture interleave.)
- bloom: apply
- bank: review
- A: A data-flow view exposes exactly the paths along which data — and therefore threats — travel: each pipe is a potential tampering/disclosure point and each filter boundary is where input validation and authorization must be enforced. The filter's interface boundary corresponds to a trust boundary in the DFD: data crossing from an untrusted producer into the filter must be checked at the edge. Architectural style choices (who talks to whom, what crosses boundaries) directly shape the threat surface.
- evidence: [S-0147]
- topic: architecture-design/architectural-styles

### Q9
- Q: IP is a best-effort, connectionless datagram service with no end-to-end delivery guarantees. Using that fact, name at least three STRIDE categories that apply to data sent in plaintext over IP, and the standard transport-layer mitigations. (Networking interleave.)
- bloom: apply
- bank: review
- A: Spoofing (source IP addresses are not authenticated — attacker impersonates a host or injects packets), Tampering (datagrams can be modified or replayed in transit — no integrity mechanism at the IP layer), Information disclosure (payload is readable by anyone on the path), Denial of service (flooding consumes resources). Standard mitigations live in higher layers: TLS (authenticity + integrity + confidentiality), TCP sequence handling, and rate limiting/firewalls for DoS — exactly why threat models treat the network as an untrusted element and draw trust boundaries around endpoints.
- evidence: [S-0088]
- topic: systems-software/networking-basics
