---
id: security/web-security
title: Web Security
band: B4
track: security
tier: T2
bloom_target: apply
prerequisites: [security/authentication-authorization, systems-software/http-basics]
related: [security/threat-modeling, security/secure-sdlc]
recommended: []
status: published
schema-version: 1
owner: l1-web-security
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0023, S-0247, S-0248, S-0249]
---

# Web Security

## Claims

### Standing and the OWASP Top 10

- The OWASP Top 10:2021 is the widely used awareness document on the most critical web application security risks: A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection, A04 Insecure Design, A05 Security Misconfiguration, A06 Vulnerable and Outdated Components, A07 Identification and Authentication Failures, A08 Software and Data Integrity Failures, A09 Security Logging and Monitoring Failures, A10 Server-Side Request Forgery. [T3][S-0247]
- Broken access control is the #1 risk in Top 10:2021, covering improper authorization, IDOR (CWE-639), and cross-site request forgery (CWE-352). [T3][S-0247]
- Injection ranks #3 and spans SQL, NoSQL, OS command, ORM, LDAP, and expression-language injection; cross-site scripting (CWE-79) is mapped under injection. [T3][S-0247]
- Security misconfiguration (A05) — missing or misconfigured hardening settings — is a top-5 risk class. [T3][S-0247]
- SWEBOK v4.0 integrates security across the software lifecycle as a first-class concern via its Software Security knowledge area. [T2][S-0017]
- ISO/IEC 25010:2023 defines the Security quality characteristic with subcharacteristics Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, and Resistance — the goals web defenses serve. [T2][S-0019]

### Injection (SQLi)

- SQL injection occurs when untrusted input is concatenated into a SQL statement: a quote breaks out of the string literal and injected SQL executes with the application's database privileges. [T3][S-0248]
- The primary defense is prepared statements (parameterized queries), which separate SQL structure from data so input cannot alter query structure; stored procedures and allow-list validation are secondary defenses, and escaping is strongly discouraged. [T3][S-0248]

### Cross-site scripting (XSS)

- Cross-site scripting is what RFC 6454 calls leaking an origin's authority to untrusted content: injected script runs in the victim's browser with the full authority of the hosting origin — which is why XSS can read the victim's session cookies. [T2][S-0249]
- Three generally recognized forms exist: reflected XSS (payload echoed from the request), stored XSS (payload persisted server-side, hits every later viewer), and DOM-based XSS (client-side injection into a sink such as innerHTML, no server round-trip). [T3][S-0248]
- XSS prevention is context-aware output encoding — untrusted data must be encoded for the specific rendering context (HTML body, attribute, URL, CSS, JavaScript); DOM sinks need safe assignments such as textContent or Trusted Types. [T3][S-0248]

### Cross-site request forgery (CSRF)

- CSRF exploits ambient authority: browsers attach cookies automatically, and the same-origin policy permits cross-origin requests, so an attacker page can trigger state-changing requests carrying the victim's session — RFC 6454 links the two properties directly. [T2][S-0249]
- CSRF defenses: server-generated synchronizer (anti-CSRF) tokens validated on state-changing requests, SameSite cookie attributes, and care with any credential the browser sends automatically. [T3][S-0248]

### Server-side request forgery (SSRF)

- SSRF is a server fetching a user-supplied URL without validation, letting an attacker reach internal services behind firewalls, VPNs, or network ACLs; it entered the Top 10 in 2021 as A10. [T3][S-0247]
- SSRF mitigation is positive allow-listing of URL scheme, port, and destination plus deny-by-default network segmentation; deny-lists are explicitly rejected because attackers bypass them. [T3][S-0247]

### Same-origin policy

- An origin is the triple (scheme, host, port): https://example.com, its default port, and every path form one origin; changing any component changes the origin. [T2][S-0249]
- The same-origin policy lets same-origin content interact freely while restricting cross-origin interaction: reading another origin's information is generally forbidden, but sending requests to it is permitted. [T2][S-0249]
- Cross-origin reads are possible only when the resource opts in (e.g., via CORS); the send-permitted/read-forbidden asymmetry is exactly why CSRF exists. [T2][S-0249]
- Cookies predate the origin model and are scoped by host/domain rather than by origin — a unit-of-isolation divergence RFC 6454 flags as a source of vulnerabilities. [T2][S-0249]
- Because cookies are not origin-scoped, they must be hardened with Secure, HttpOnly, and SameSite attributes; the browser will not do it for you. [T3][S-0248]

### HTTP authentication framing

- HTTP defines its own challenge-response authentication framework — 401 responses and the WWW-Authenticate and Authorization header fields — separate from application-level mechanisms; most web applications layer cookies and bearer tokens on top. [T2][S-0023]

### Security headers and TLS

- Content-Security-Policy lets the server declare what the page may load; it defends against XSS by restricting inline scripts, remote scripts, and dynamic evaluation (eval) — as defense in depth, not a substitute for output encoding. [T3][S-0248]
- HTTP Strict Transport Security (Strict-Transport-Security) forces browsers to refuse plaintext HTTP and upgrade to HTTPS for the declared domain; includeSubDomains and the preload list extend coverage — and preload is deliberately hard to undo. [T3][S-0248]
- TLS in the web context protects the confidentiality and integrity of data in transit between browser and server; HTTPS is necessary but not sufficient — every application-level risk in this pack still applies over TLS. [T3][S-0248]

## Details

SQLi trace: the query `SELECT * FROM users WHERE name = '` + input + `'` becomes two statements when input is `' OR '1'='1` — the quote closes the literal and the injected predicate always matches, returning all rows. Parameterized queries send the statement skeleton and the values separately, so the value can never be parsed as SQL structure.

CSRF trace: the victim is logged into bank.example (session cookie). attacker.example serves a page with `<img src="https://bank.example/transfer?to=attacker&amount=1000">` or an auto-submitting form. The browser attaches the bank cookie automatically (cookie, not origin, scoped), the same-origin policy does not block the *request* (it blocks reading the response), and the transfer executes. Mitigation: synchronizer token embedded in the form and checked server-side — the attacker page cannot read the token, so it cannot forge the request.

SSRF trace: a "fetch this URL" feature with input `http://169.254.169.254/latest/meta-data/` reaches the cloud metadata service — an internal address the app would never legitimately call. The allow-list fix rejects non-allow-listed schemes, hosts, and ports before fetching.

## Boundaries / common misunderstandings

- "HTTPS means the site is secure" — TLS protects data in transit; the application still ships injection, XSS, broken access control, and every other risk in this pack over that encrypted pipe. [T3][S-0248]
- "CSP alone fixes XSS" — OWASP's XSS guidance lists sole reliance on CSP as an anti-pattern; CSP is defense in depth on top of context-aware output encoding. [T3][S-0248]
- "The same-origin policy stops cross-origin requests" — it blocks cross-origin *reads*; cross-origin *sends* are permitted, which is precisely the property CSRF exploits. [T2][S-0249]
- "Input filtering ('block <, >, quotes') prevents XSS" — encoding depends on the rendering context; blacklisting characters fails across attribute, JavaScript, URL, and CSS contexts and against alternate encodings. [T3][S-0248]
- "Injection is only about user form input" — any untrusted data reaching a context (uploaded files, third-party APIs, config values, URLs) can carry payloads; the discipline is separating data from structure everywhere. [T3][S-0248]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — software security as lifecycle-integrated concern.
- S-0019 — ISO/IEC 25010:2023 — Security quality characteristic and subcharacteristics.
- S-0023 — RFC 9110 (2022) — HTTP semantics; challenge-response authentication framework.
- S-0247 — OWASP Top 10:2021 — A01 (CSRF), A03 (injection, XSS), A05, A10 (SSRF).
- S-0248 — OWASP Cheat Sheet Series — SQLi, XSS, DOM XSS, CSRF, CSP, HSTS, cookie/session sheets.
- S-0249 — RFC 6454 (2011) — origin concept, same-origin policy, CSRF/XSS linkage.
