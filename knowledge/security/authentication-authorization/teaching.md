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
status: published
schema-version: 1
owner: l1-authentication-authorization
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0233, S-0242, S-0243, S-0244, S-0247, S-0248]
---

# Authentication & Authorization — teaching

## Learning objectives (Bloom)

By the end of this topic you will be able to:

- **Understand** — explain the authentication/authorization distinction, the factor taxonomy, and why MFA and salted KDF password storage are baseline controls (prereqs: cryptography-basics for hash/KDF mechanics).
- **Apply** — design a password storage scheme, a session lifecycle, and a JWT/OAuth integration with correct verification rules for a concrete web application.
- **Apply** — choose between session cookies, opaque tokens, and signed JWTs for a given API by tracing revocation, state, and leakage trade-offs.

## Worked example: session vs token decision trace

Scenario: "Bookmarks" is a web app (browser client + API) where users log in and read/write their bookmarks. Requirement: logout must take effect immediately; an admin must be able to cut off a compromised account within minutes.

Trace:

1. **Identify the credential options.** (a) Opaque server-side session: random ID (>=64 bits) stored server-side, delivered in an HttpOnly, Secure, SameSite cookie. (b) Signed JWT: claims (sub, exp, scope) signed by the server, carried in an Authorization header. Both are bearer credentials with equal sensitivity in transit.
2. **Trace the hard requirement — revocation.** For (b), a valid JWT is accepted until exp unless the server maintains a deny-list, which reintroduces server-side state and a lookup on every request — the statelessness advantage vanishes exactly when revocation matters. For (a), revocation is deleting the session row: instant, both for logout and for admin cut-off. Choose sessions.
3. **Harden the choice.** Session ID: cryptographically random, >=64 bits entropy. Cookie attributes: HttpOnly (XSS cannot read it), Secure (never over plain HTTP), SameSite=Lax (CSRF defense). Regenerate the ID after login (session fixation). Invalidate server-side on logout and after idle timeout (e.g., 1 h at AAL2).
4. **When would JWT win?** If the API is consumed by many stateless services that cannot share session storage, and revocation is acceptable on the order of token lifetime — short exp (minutes to hours), aud checked per service, algorithm allow-listed, keys pinned. The boundary claim to remember: neither option is "more secure" — they trade revocation and state.

## Elaboration prompts

- Why does SP 800-63B forbid reversible (encrypted) password storage even though encryption "protects" the data? Trace what happens when the key leaks, versus when a salted hash leaks.
- In the OAuth authorization code grant, name each actor and explain why the user's password never crosses the client — and what PKCE protects when the code itself is intercepted.
- Why is "alg":"none" a vulnerability when RFC 7519 *requires* implementations to support it? What does that imply about default configurations of JWT libraries?
- What changes about the threat model between AAL1, AAL2, and AAL3? Pick a product you know and justify which AAL it should target.
- If JWTs are signed, why does RFC 7519 still demand measures (TLS or encryption) for privacy-sensitive claims?

## Common misconceptions

- **"MFA just means 'two passwords'"** — MFA requires factors from different categories (e.g., password + TOTP device), not two instances of the same category; NIST AAL2 demands two *different* authenticator types. Two passwords is one factor twice.
- **"JWT is more secure than sessions, so I should always use it"** — JWT is a format; its security is entirely in the verification. It trades away instant revocation unless you rebuild server-side state. Choose by tracing revocation/state trade-offs, not by vibes.
- **"Hashing with SHA-256 is good enough password storage"** — bare fast hashes (even salted) fall to GPU and rainbow-table economics; the point of a password KDF (Argon2id, scrypt, PBKDF2) is the cost factor that makes each trial expensive, plus memory-hardness against GPU parallelism.
- **"OAuth login = authentication"** — OAuth 2.0 delegates access; how the user authenticates is out of scope. Using OAuth as login without an identity layer leaves identity semantics unstandardized and easy to misuse.
- **"Logging out is enough; nothing else matters"** — a session survives logout unless the server invalidates it; and without idle timeouts a stolen session ID works forever. Cookie hygiene, regeneration, and server-side invalidation are all part of session management.

## Feynman targets

Explain each in plain language, as if to a junior developer who has never seen auth code:

1. Why a leaked password database is still painful with salted Argon2id, and catastrophic with unsalted MD5.
2. Why a JWT verifier needs an algorithm allow-list, and what happens with `alg: none`.
3. The OAuth authorization code + PKCE flow in five steps, naming who trusts whom.
4. Why AAL2 vs AAL3 matters for a banking app vs a news site.

## Interleaving hooks

- **Cryptography basics** — MFA TOTP is a MAC over time steps; JWTs reuse HMAC/RSA signature primitives; Argon2id is a memory-hard KDF. If you cannot explain HMAC or collision resistance, revisit `security/cryptography-basics` first.
- **Threat modeling** — run STRIDE over your auth design: Spoofing (factors, MFA), Tampering (session integrity), Information disclosure (token leakage, logging), Elevation of privilege (authorization checks). Auth choices are the mitigations the threat model demanded.
- **Web security** — the session cookie you design here is the same cookie CSRF attacks abuse; XSS steals the tokens you issue. `security/web-security` assumes you know this material cold.
