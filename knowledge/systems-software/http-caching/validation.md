---
id: systems-software/http-caching
title: HTTP Caching
band: B4
track: systems-software
tier: T2
bloom_target: apply
prerequisites: [systems-software/http-basics]
related: [architecture-design/caching-strategies]
recommended: []
status: published
schema-version: 1
owner: l1-http-caching
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0009, S-0023, S-0024]
---

# HTTP Caching — validation

## Formative (practice)

### Q1
Q: Which single Cache-Control directive truly prevents a response from being stored and reused by any cache?
bloom: remember
bank: formative
A: `no-store`. `no-cache` still allows storage (it only forces revalidation before reuse), and `private` still allows the browser's own cache to store the response.
evidence: [S-0009]

### Q2
Q: A response carries `Cache-Control: max-age=600`, an `Expires` header, and `Date`. In what order does a cache compute the freshness lifetime?
bloom: understand
bank: formative
A: `s-maxage` (if present and the cache is shared) → `max-age` → `Expires` minus `Date` → heuristic freshness. Since `max-age` is present, `Expires` MUST be ignored.
evidence: [S-0009]

### Q3
Q: At 12:00:00 a proxy stores a response with `Date: 12:00:00`, `Age: 0`, `Cache-Control: public, max-age=300`. The proxy forwards it at 12:03:00. What `Age` value must the proxy send, and is the response still fresh?
bloom: apply
bank: formative
A: Age = 180 (3 minutes of resident time added to prior Age 0). Freshness lifetime is 300 s, current age 180 s < 300 s, so it is still fresh and may be served without contacting the origin.
evidence: [S-0009]

### Q4
Q: You run a JSON API keyed by URL whose data changes every 5 minutes and may be cached by CDNs and browsers. Write the Cache-Control header, and state what each directive contributes.
bloom: apply
bank: formative
A: `Cache-Control: public, max-age=300`. `public` allows shared caches (CDN) to store it; `max-age=300` matches the 5-minute data lifetime. No `no-store`, so storage is permitted; no `private`, so shared caches are allowed.
evidence: [S-0009]

## Summative (mastery checkpoint)

### Q5
Q: Trace this sequence hop-by-hop, stating what is on the wire at each step: (1) browser cache miss for GET /report; (2) origin returns 200 with `ETag: "v7"`, `Cache-Control: public, max-age=60`; (3) same browser requests /report again 90 seconds later and the origin still has v7. What does each hop send and receive?
bloom: apply
bank: summative
A: (1) Browser sends plain GET (no conditionals, nothing stored). (2) Origin returns full 200 body + ETag + Cache-Control. (3) The stored copy is stale (90 s > 60 s), so the browser sends `If-None-Match: "v7"`; the origin compares with the strong comparison function, finds a match, and returns `304 Not Modified` with no body; the browser then serves the stored body and refreshes the entry's metadata (freshness restarts per the 304's headers).
evidence: [S-0009][S-0023]

### Q6
Q: An API behind a CDN returns `Cache-Control: private, max-age=60` for all responses. The CDN stores nothing; operations asks why the CDN is "not caching". Explain the behavior, the security rationale, and the exact change that would let the CDN cache (and the risk it introduces).
bloom: analyze
bank: summative
A: `private` restricts storage to the user-agent's cache; shared caches (the CDN) MUST NOT store such responses, so every request still hits the origin. The rationale is that the response may embed user-specific data. Changing to `public` (or `s-maxage`) would enable CDN storage but would also let one user's personalized content be served to others — so `public` is only correct for responses that are truly identical for all users; user-specific data should additionally carry Authorization protection or `private`/`no-store`.
evidence: [S-0009]

### Q7
Q: After a deploy, a CDN serves gzip-compressed HTML to browsers that did not send `Accept-Encoding: gzip`. The origin sends `Vary: Accept-Encoding` on every response. Explain how this bug can happen at the cache even though the origin's headers are correct, and the rule the cache violated.
bloom: analyze
bank: summative
A: The origin negotiated per-request (compressed vs identity) and declared the variation with `Vary: Accept-Encoding`, which makes that header's value part of the cache key. If the cache ignores `Vary` (or serves a stored response without checking the stored header values), it can reuse a gzip variant for a request that cannot decode it — corrupt content. The cache violated the rule that a stored response may only be reused when the current request's values for every `Vary`-listed field match the stored ones.
evidence: [S-0009][S-0023]

## Review (spaced repetition — interleaved with prerequisites)

### Q8
Q: What exactly does the `Age` header measure, and why can a client not compute freshness from its own clock alone?
bloom: understand
bank: review
A: `Age` measures the time since the response was generated or last validated, including time spent inside intermediate caches; it is computed from `Date` and observed response times, not the client's clock. Without it, a client could not know how much of `max-age` was already consumed by intermediate caches. (Prerequisite link: http-basics — response header fields.)
evidence: [S-0009]

### Q9
Q: Which HTTP methods are cacheable by default, and under what conditions may a POST response be stored? When does a client attach `If-None-Match` to a request?
bloom: remember
bank: review
A: GET and HEAD are cacheable by default; a POST response may be cached only with explicit freshness information and a matching `Content-Location`. A client attaches `If-None-Match` when it holds a stored response with an entity-tag and must revalidate it (i.e., the stored entry is stale or the cache uses no-cache). (Prerequisite link: http-basics — methods, conditional request semantics.)
evidence: [S-0009][S-0023]

### Q10
Q: A browser receives `304 Not Modified` for a URL it has never requested before. What should it do, and why?
bloom: apply
bank: review
A: It must treat this as an error (or refetch): a 304 carries no body and only updates an existing stored response's metadata; without a stored entry there is nothing to serve, so the client should issue an unconditional GET. (Prerequisite link: http-basics — status codes.)
evidence: [S-0009][S-0023]
