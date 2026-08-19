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

# Authentication & Authorization

## Claims

### What authentication and authorization are

- ISO/IEC 25010:2023 defines Authenticity — "the degree to which the identity of a subject or resource can be proved to be the one claimed" — as a subcharacteristic of the Security quality characteristic; authentication mechanisms serve that goal. [T2][S-0019]
- Authentication and authorization are distinct, sequential checks: authentication proves identity ("who are you?"), authorization decides what that identity may do ("may you do this?"); a successful login grants no entitlement by itself. [T3][S-0248]
- SWEBOK v4.0's Software Security knowledge area places authentication, authorization, and least-privilege access control among the fundamental security concepts engineers apply throughout the lifecycle. [T2][S-0017]

### Authentication factors and MFA

- SP 800-63B builds authentication events from defined authenticator types — memorized secrets, look-up secrets, out-of-band authenticators, single- and multi-factor OTP, cryptographic (software/hardware) authenticators, and biometrics. [T2][S-0242]
- The classic factor taxonomy distinguishes knowledge ("something you know"), possession ("something you have"), and inherence ("something you are") factors; each authenticator type maps to one of these categories. [T3][S-0248]
- Multi-factor authentication requires the successful presentation of two or more distinct factors; NIST's AAL2 demands multi-factor authentication using two different authenticator types. [T2][S-0242]
- AAL3 goes further: authentication SHALL use a hardware-based authenticator plus an authenticator providing phishing (verifier-impersonation) resistance — phishing resistance is recommended at AAL2 and required at AAL3. [T2][S-0242]
- MFA is the baseline mitigation for automated attacks against passwords — credential stuffing, password spraying, and bulk brute force — because possession of the password alone no longer authenticates. [T3][S-0248]

### Password storage

- Verifiers SHALL NOT store passwords as plaintext or as reversible (encrypted) values: SP 800-63B requires storing salted, iteratively hashed verification secrets resistant to offline attack. [T2][S-0242]
- The required scheme is a one-way key derivation function taking password, salt, and cost factor (PBKDF2 is named in the guideline); a memory-hard function SHOULD be used because it raises the cost of each guessing trial. [T2][S-0242]
- Salting makes identical passwords hash differently per user, defeating rainbow tables and batch cracking; NIST requires salts of at least 32 bits, stored alongside the hash. [T2][S-0242]
- OWASP's algorithm ranking for new systems: Argon2id first (winner of the 2015 Password Hashing Competition), scrypt when Argon2 is unavailable, bcrypt only for legacy systems with a work factor of at least 10. [T3][S-0248]
- Password hashing falls under the "never design your own cryptography" rule: custom, fast, or unsalted hashes (bare MD5/SHA-1, home-made KDFs) fall to GPU-accelerated guessing; use standardized, reviewed schemes. [T3][S-0233]

### Session management

- A session ties the authenticated identity to subsequent requests; the session identifier is a bearer credential with the sensitivity of a password and must be unguessable — OWASP requires at least 64 bits of entropy. [T3][S-0248]
- Session cookies must be hardened with attributes: HttpOnly (blocks script access, preventing session-ID theft via XSS), Secure (HTTPS only), and SameSite (Strict or Lax; never None without Secure). [T3][S-0248]
- NIST's reauthentication requirements scale with assurance level: at AAL2 reauthentication SHOULD occur within 24 hours overall and 1 hour of inactivity; at AAL3 within 12 hours overall and 15 minutes of inactivity; the session SHALL terminate when a limit is reached. [T2][S-0242]
- Session identifiers must be regenerated when privilege changes (e.g., after login); failing to do so enables session fixation. [T3][S-0248]
- Logout must invalidate the session server-side; merely clearing the cookie leaves the server-side session alive for anyone holding its identifier. [T3][S-0248]

### Tokens (JWT)

- A JWT is a compact, URL-safe claims format: a JSON payload carried inside a JWS (signed) or JWE (encrypted) structure; the common signed-only form is tamper-evident but not confidential. [T2][S-0244]
- Registered claims (iss, sub, aud, exp, nbf, iat, jti) standardize validation: a token MUST NOT be accepted at or after exp, and a receiver MUST identify itself in aud or reject the token. [T2][S-0244]
- RFC 7519 makes "none" a mandatory-to-implement algorithm and requires rejecting JWTs whose algorithms are not understood or acceptable — verification must therefore enforce an explicit algorithm allow-list and reject unsigned tokens. [T2][S-0244]
- Real-world JWT failures are verification failures: accepting "alg":"none" lets anyone forge tokens, and key/algorithm confusion (e.g., an HS256 MAC keyed with the issuer's public key) forges tokens in the issuer's name. [T3][S-0248]
- RFC 7519's trust rule: JWT contents cannot be relied on in a trust decision unless they are cryptographically secured and bound to the decision context — the verification, not the format, is the security control. [T2][S-0244]

### OAuth 2.0

- OAuth 2.0 is an authorization framework: a third-party client obtains limited access to an HTTP service on behalf of the resource owner, without the client ever holding the owner's credentials. [T2][S-0243]
- OAuth defines four roles (resource owner, client, authorization server, resource server) and four grant types: authorization code, implicit, resource owner password credentials, and client credentials. [T2][S-0243]
- In the authorization code grant, the resource owner authenticates only at the authorization server; the code travels through the user-agent, and the access token is issued directly to the client at the token endpoint. [T2][S-0243]
- How the resource owner authenticates is explicitly beyond OAuth's scope — OAuth is delegation, not a user-authentication standard, which is why identity frameworks build an authentication layer on top of it. [T2][S-0243]
- Access tokens carry a specific scope and lifetime and are usually opaque to the client; refresh tokens are credentials for obtaining new access tokens and are never sent to resource servers. [T2][S-0243]
- In the implicit grant the access token is delivered directly to the browser and the authorization server does not authenticate the client; RFC 6749 flags its security implications — the authorization code grant is preferred. [T2][S-0243]
- Public clients (SPAs, native apps) using the authorization code grant should add PKCE, which binds the code to the client and defeats authorization-code interception. [T3][S-0248]
- OAuth endpoints transmit credentials, so the authorization server MUST require TLS on the authorization endpoint. [T2][S-0243]

### Authorization models

- RBAC assigns permissions to roles and users to roles, making roles the unit of administration; ABAC evaluates subject/resource/environment attributes against policies, trading administrative simplicity for expressiveness. [T3][S-0248]
- Access control should be deny-by-default and enforced server-side on every request, including object-level checks — failing these enables Insecure Direct Object Reference (IDOR) patterns. [T3][S-0248]
- Least privilege — granting each subject only the permissions necessary for its function — limits the blast radius of any single compromised account. [T2][S-0017]

## Details

AAL ladder in practice: AAL1 accepts a single factor (e.g., password). AAL2 requires two different authenticator types (e.g., password + TOTP app) and periodic reauthentication. AAL3 adds a hardware-based, phishing-resistant authenticator (e.g., FIDO2 security key) and shorter reauthentication windows. The levels are a contract between the application's risk appetite and the strength of the authentication event.

OAuth authorization-code + PKCE trace: (A) client redirects the user to the authorization server with client_id, redirect_uri, state, code_challenge; (B) the user authenticates at the authorization server — the client never sees the password; (C) the server redirects back with an authorization code; (D) the client exchanges code + code_verifier at the token endpoint for an access token (and refresh token); (E) the client calls the resource server with the access token. PKCE binds the code to the client that started the flow, so an intercepted code cannot be redeemed by an attacker.

Password-storage trace: on registration, generate a per-user random salt (>=32 bits, preferably 16 bytes) and store Argon2id(password, salt, memory/cost parameters); on login, recompute and compare. Slow, salted, one-way hashing means a leaked database does not directly reveal passwords, and each user's hash must be attacked separately.

## Boundaries / common misunderstandings

- "JWT is inherently more secure than server-side sessions" — JWT is a claims format, not a security level: an accepted-but-unverified JWT is trivially forgeable, and a bearer JWT needs the same protection as any credential; sessions and stateless JWTs differ in revocation, state, and storage, not in intrinsic security. [T3][S-0248]
- "Encrypting passwords is as good as hashing them" — reversible storage is forbidden by NIST guidance: if the encryption key leaks, every password decrypts, while salted one-way KDFs remain one-way. [T2][S-0242]
- "MFA makes phishing impossible" — MFA resists credential-only attacks; phishing-resistant authenticators (hardware-bound, verifier-impersonation resistant) are the stronger class NIST separates out at AAL3. [T2][S-0242]
- "Using OAuth to log users in means OAuth is an authentication protocol" — OAuth standardizes delegation of access; how the user authenticates is out of scope, so identity semantics require an identity layer such as OpenID Connect. [T2][S-0243]
- "A signed JWT is encrypted" — base64url is not encryption: claims are readable by anyone who decodes the payload, and RFC 7519 requires encryption or TLS for privacy-sensitive claims. [T2][S-0244]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — software security fundamentals: authentication, authorization, least privilege.
- S-0019 — ISO/IEC 25010:2023 — Security quality characteristic; Authenticity subcharacteristic.
- S-0233 — Katz & Lindell, Introduction to Modern Cryptography, 3rd ed. (2020) — practice rules: standardized, reviewed mechanisms.
- S-0242 — NIST SP 800-63B-4 (2025) — authenticator types, MFA/AALs, password storage, session reauthentication.
- S-0243 — RFC 6749 (2012) — OAuth 2.0 roles, grants, token semantics.
- S-0244 — RFC 7519 (2015) — JWT format, claims, validation and trust rules.
- S-0247 — OWASP Top 10:2021 — A07 Identification and Authentication Failures.
- S-0248 — OWASP Cheat Sheet Series — MFA, Password Storage, Session Management, JWT, OAuth2, Authorization sheets.
