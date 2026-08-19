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
status: published
schema-version: 1
owner: l1-threat-modeling
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0237, S-0238, S-0239]
---

# Threat Modeling — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: name the six STRIDE categories with their property mapping, the AND/OR semantics of attack trees, and the DFD element types. [T3][S-0237][S-0238]
- **understand**: explain why threat modeling happens at design time, what threat/vulnerability/attack mean, and why the model must be maintained as the system evolves. [T3][S-0237]
- **apply**: run a STRIDE-per-element pass over a small system's DFD and construct an attack tree for a stated goal with cost-tagged leaves. [T3][S-0237][S-0238] **bloom_target**
- **analyze**: compare design-time methods (STRIDE, attack trees) with observation-based knowledge (MITRE ATT&CK) and identify which threats each method will and will not surface. [T3][S-0237][S-0239]

## Worked example — STRIDE walkthrough on a file-upload service

Setup: "DropBox-lite". Users upload files over HTTPS to a web app; files are stored in object storage; metadata lives in a database. DFD: [User] --HTTPS--> [WebApp] --storage API--> [ObjectStore]; [WebApp] --SQL--> [DB]; trust boundary around WebApp + DB + ObjectStore.

1. **Draw the DFD and mark trust boundaries.** The boundary encloses WebApp, DB, and ObjectStore; the User is outside. Every flow crossing the boundary (the HTTPS upload, the storage API call, the SQL query) is an attack surface. [S-0237]
2. **STRIDE per element.** 
   - Spoofing: fake users, fake storage service (DNS/cert spoofing) → mitigate with TLS client/server authn, signed responses.
   - Tampering: file content modified in flight or in store → mitigate with TLS + content hashes/checksums verified on download.
   - Repudiation: user denies uploading a malicious file; admin denies deleting files → mitigate with append-only audit log (who did what, when).
   - Information disclosure: files accessible by guessing URLs; DB leak via SQL injection → mitigate with per-user authorization checks, parameterized queries, encryption at rest.
   - Denial of service: giant uploads, slowloris, storage exhaustion → mitigate with size limits, rate limits, quotas.
   - Elevation of privilege: path traversal in filenames, upload to a directory served as static content (arbitrary code execution) → mitigate with generated storage keys (never user-controlled paths) and no executable content in served directories. [S-0237]
3. **Risk-rank and decide.** (Path traversal → arbitrary code execution) and (unauthenticated read of other users' files) are high likelihood × high impact → fix now. Audit-logging gaps are high impact but lower urgency → schedule. Exotic DoS vectors are rationalized (accepted with monitoring) rather than silently dropped. [S-0237]
4. **Keep it alive.** Adding a sharing feature, moving storage to a new provider, or enabling a public API invalidates parts of this model — re-run the pass on each change. [S-0017]

Mini attack tree (for "obtain another user's file"): root = read victim's file. OR: (A) guess/shared URL — AND(URL predictable, no access check); (B) steal session — AND(obtain token, token not bound to device); (C) exploit upload path — AND(path traversal bug, uploaded file served). Leaves cost-tagged (A: ~0 if predictable; B: moderate; C: high skill). Analysts mitigate the cheapest feasible path first — here (A) via unguessable keys + access checks. [S-0238]

## Elaboration prompts

- Why is threat identification "the first step" of proactive security analysis — what does it make possible that testing later cannot? [T3][S-0237]
- The STRIDE property mapping is a table, not an algorithm: why does mapping each threat to the property it violates help choose mitigations? [T3][S-0237]
- Attack trees support AND/OR composition — when would the same physical step appear in two different branches, and why does that matter for mitigation? [T3][S-0238]
- ATT&CK is built from real-world observations — what systematic blind spot does that give it, and what blind spot does STRIDE have that ATT&CK does not? [T3][S-0239]
- "Accept with rationale" is an explicit outcome — what discipline does documenting accepted threats impose on the team? [T3][S-0237]

## Common misconceptions

1. **"Threat modeling is a one-time diagram."** The model is a living artifact: security is integrated throughout the lifecycle, so design, deployment, and threat-landscape changes all force re-examination. [T2][S-0017]
2. **"A pentest or scanner replaces it."** Those operate on existing implementations; threat modeling operates on the design before code exists and covers whole categories (repudiation, design-level DoS) that scanners don't address. [T3][S-0237]
3. **"Every identified threat must be mitigated."** The point is prioritization: mitigate high-risk threats, accept low-risk ones — but explicitly, with a rationale, never silently. [T3][S-0237]
4. **"Threat modeling is about external hackers only."** The definition is broader: any potential occurrence, malicious or otherwise, with an undesirable effect — insiders, accidents, and misconfigurations count. [T3][S-0237]
5. **"STRIDE is the only method" / "ATT&CK replaces STRIDE."** STRIDE is design-time and design-driven; ATT&CK is observation-driven and adversary-grounded. Each has blind spots; they are complements. [T3][S-0237][S-0239]

## Feynman targets

Explain in plain language a non-engineer could follow:

- Why you draw the plumbing of a system before looking for burglars, and why the drawing must be redrawn when you move rooms.
- How an attacker's "plan" can be drawn as a tree of choices, and why you defend by cutting the cheapest branches.
- Why knowing how burglars actually operate (from case files) and knowing how your building is laid out are two different tools you need together.

## Interleaving hooks

- **architecture-design/architectural-styles (prerequisite)**: the DFD is the data-flow view of the architecture; style choices (who may talk to whom, shared state or not) determine the trust boundaries you draw.
- **systems-software/networking-basics (prerequisite)**: IP's best-effort model makes the network an untrusted element — every on-the-wire flow is a spoofing/tampering/disclosure surface, which is why TLS lives at the endpoints.
- **security/cryptography-basics (related)**: mitigations are built from crypto primitives — authentication, integrity, and confidentiality map 1:1 to the properties STRIDE threats violate.
- **security/secure-sdlc (next topic, recommended)**: the threat model is the input that turns security requirements into secure design, testing (attack cases), and operations runbooks.
