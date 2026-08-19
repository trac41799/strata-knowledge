---
id: security/authentication-authorization
title: Authentication & Authorization
band: B4
track: security
tier: T2
bloom_target: apply
prerequisites: [security/threat-modeling, security/cryptography-basics]
related: [security/web-security, security/secure-sdlc]
recommended: [security/web-security]
status: draft
schema-version: 1
owner: l1-authentication-authorization
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0019, S-0233, S-0242, S-0243, S-0244, S-0247, S-0248]
---

# Authentication & Authorization — validation

## Formative (practice)

- Q: What are the three classic authentication factor categories, and which category does a TOTP app belong to?
- bloom: remember
- bank: formative
- A: Knowledge, possession, and inherence ("something you know / have / are"); a TOTP app is a possession factor (a multi-factor OTP authenticator in NIST terms).
- evidence: [S-0242]
- topic: security/authentication-authorization

- Q: Why must passwords be stored as salted, slow-hash outputs rather than encrypted?
- bloom: understand
- bank: formative
- A: Storage must resist offline attacks. A one-way KDF with per-user salt and cost factor means a leaked database cannot be decrypted wholesale and each hash must be guessed separately; encryption is reversible, so a leaked key decrypts everything.
- evidence: [S-0242]
- topic: security/authentication-authorization

- Q: What is the difference between authentication and authorization?
- bloom: understand
- bank: formative
- A: Authentication proves identity ("who are you?"); authorization decides what that identity may do ("may you do this?"). They are separate checks: a successful login grants no entitlement by itself, and authorization must never be inferred from authentication.
- evidence: [S-0248]
- topic: security/authentication-authorization

- Q: What must a JWT verifier check before trusting the claims, and what does exp mean?
- bloom: understand
- bank: formative
- A: The verifier must enforce an algorithm allow-list, verify the signature with the correct key (no "alg":"none", no key confusion), match aud, and check exp — the token MUST NOT be accepted at or after its expiration time.
- evidence: [S-0244]
- topic: security/authentication-authorization

## Summative (mastery checkpoint)

- Q: A legacy system stores SHA-256(password) with no salt. Identify the flaws, then specify the replacement storage scheme.
- bloom: apply
- bank: summative
- A: Flaws: fast non-memory-hard hash, no salt — rainbow tables and GPU cracking scale across all users at once. Replacement: per-user random salt (>=32 bits), Argon2id (or scrypt; bcrypt only legacy, work factor >=10) with tuned cost, store salt + hash; never encrypt; add rate limiting on verification.
- evidence: [S-0242][S-0248]
- topic: security/authentication-authorization

- Q: Design the session lifecycle for a web app: identifier generation, cookie attributes, login handling, logout, and inactivity policy.
- bloom: apply
- bank: summative
- A: Generate random IDs with >=64 bits entropy; set HttpOnly + Secure + SameSite (Strict or Lax) on the session cookie; regenerate the ID on login/privilege change (anti-fixation); invalidate server-side on logout; enforce idle timeout (e.g., NIST AAL2: <=1 h inactivity, reauth <=24 h) and terminate the session at the limit.
- evidence: [S-0242][S-0248]
- topic: security/authentication-authorization

- Q: You are choosing between opaque server-side sessions and signed JWTs for a new API. List the decision factors and give a defensible choice.
- bloom: apply
- bank: summative
- A: Factors: revocation (sessions revoke instantly; JWTs only via expiry or deny-lists), state (sessions need server storage; JWTs are stateless), token size/round-trips, leakage surface (bearer tokens must be protected in transit and storage either way), CSRF exposure (cookies need SameSite/tokens; Authorization-header JWTs do not ride cookies). Defensible choices: server-side sessions for classic web apps needing instant logout; short-lived signed JWTs for distributed APIs with a revocation strategy.
- evidence: [S-0244][S-0248]
- topic: security/authentication-authorization

## Review (spaced repetition — interleaved with prerequisites)

- Q: What property does a MAC (e.g., HMAC) provide that encryption alone does not?
- bloom: understand
- bank: review
- A: Integrity plus authenticity: a MAC proves the data was not modified and was produced by a party sharing the key; encryption alone hides content but does not detect modification.
- evidence: [S-0233]
- topic: security/cryptography-basics

- Q: In STRIDE, which threat category violates the authentication property, and what is its classic mitigation family?
- bloom: remember
- bank: review
- A: Spoofing; mitigated by authentication mechanisms (factors, credentials, MFA) that prove identity claims.
- evidence: [S-0237]
- topic: security/threat-modeling

- Q: Why does NIST require reauthentication after inactivity even for sessions that are still valid?
- bloom: understand
- bank: review
- A: A session left idle remains usable by anyone holding the session identifier (e.g., a stolen laptop or session token); reauthentication after the inactivity window bounds the window of misuse and re-proves the claimant controls the authenticators.
- evidence: [S-0242]
- topic: security/authentication-authorization

- Q: Which OAuth grant keeps the user's password away from the third-party client, and where is the access token issued?
- bloom: remember
- bank: review
- A: The authorization code grant: the user authenticates only at the authorization server, and the access token is issued directly to the client at the token endpoint — the client never sees the password.
- evidence: [S-0243]
- topic: security/authentication-authorization
