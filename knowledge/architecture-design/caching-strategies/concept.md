---
id: architecture-design/caching-strategies
title: Caching Strategies
band: B4
track: architecture-design
tier: T1
bloom_target: apply
prerequisites: [systems-software/http-caching]
related: [systems-software/http-caching]
recommended: []
status: published
schema-version: 1
owner: l1-caching-strategies
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0009, S-0157, S-0158, S-0159]
---

# Caching Strategies

## Claims

### Placement: client, proxy, server

- RFC 9111 distinguishes private caches (single user, e.g., the browser cache) from shared caches (serving many users, e.g., proxies and CDNs); directives such as private and s-maxage have different semantics for each. [T2][S-0009]
- A shared cache must not store a response to a request carrying Authorization unless the response explicitly permits it (public, must-revalidate, or s-maxage). [T2][S-0009]
- Server-side caches sit in front of the data store: reads are served from the cache and only misses fall through to the store; distributed caches (e.g., Redis, memcached) provide a shared tier across application instances at the cost of a network round-trip per access, while in-process caches avoid the round trip but duplicate data per instance. [T3][S-0157]

### Cache-aside and read-through

- Cache-aside (lazy loading): on a read the application checks the cache; on a miss it loads the value from the data store, stores it in the cache, and returns it — the application owns the cache-orchestration flow. [T3][S-0157]
- Read-through: the cache itself loads a missing value from the data store on a miss, so the application only calls the cache and the loading logic moves into the cache layer. [T3][S-0157]
- On a miss, the first read pays the data-store latency plus the cache-population write, so the miss path is the dominant read-latency risk in cache-aside and read-through designs. [T3][S-0157]

### Write strategies

- Write-through updates the data store and the cache in the same write operation, so readers see the new value immediately after a successful write; it costs write latency and can cache data that is never read. [T3][S-0157]
- Write-behind (write-back) acknowledges the write at the cache and flushes to the data store asynchronously, maximizing write throughput at the cost of short-term inconsistency and a data-loss window if the cache fails before flushing. [T3][S-0157]
- Hazelcast's guidance reserves write-behind for cases where performance considerations outweigh short-term consistency, because asynchronous propagation is harder to reason about and to recover from. [T3][S-0157]
- Read-through and write-through compose: writes keep the cache current while reads miss-populate, yielding read-your-writes behavior through a single read path. [T3][S-0157]

### TTL and invalidation

- TTL bounds how long an entry is served before it expires: in HTTP, max-age fixes the freshness lifetime and stale entries must be revalidated before reuse; in key-value caches, an expired key is deleted and treated as a miss. [T2][S-0009][S-0159]
- Invalidation-based coherence: on a write, delete the cached value rather than set it, so the next read rebuilds fresh data — the approach Facebook's memcache uses; it keeps data fresher than TTL alone but requires the write path to know about the cache. [T1][S-0158]
- A stale set is a real failure mode of set-on-write caching: concurrent, reordered updates can install an outdated value in the cache; memcache leases detect and reject such writes by validating the lease token at set time. [T1][S-0158]
- In HTTP, servers declare freshness and validation policy declaratively (Cache-Control, ETag), so HTTP caches need no write-path integration; application caches must implement invalidation themselves. [T2][S-0009]

### Cache stampede / thundering herd

- A thundering herd occurs when a key with heavy read activity is invalidated or expires: many concurrent reads miss and all fall through to the more costly data store. [T1][S-0158]
- Facebook's leases mitigate thundering herds: a memcached server issues a lease token for a key at a regulated rate (by default once per 10 seconds), and other clients are told to wait briefly instead of hitting the store, so the store receives roughly one rebuild per period. [T1][S-0158]
- In Facebook's evaluation, leases reduced the peak database query rate for a contended key from roughly 17,000/s to 1,300/s. [T1][S-0158]
- Refresh-ahead is a pattern-level alternative: the cache refreshes (typically hot) entries shortly before they expire, so reads never wait on a miss. [T3][S-0157]

### Consistency

- Caching strategies span a consistency spectrum: cache-aside with TTL gives bounded staleness; write-through gives read-your-writes; write-behind gives delayed visibility plus a loss window — choosing a strategy is choosing a point on this spectrum. [T3][S-0157]
- Distributed-cache consistency has an additional failure mode: concurrent readers and reordered writes can leave an old value in the cache (stale sets), so consistency is a property of the whole read/write path, not of the cache server alone. [T1][S-0158]

### Distributed cache practice

- Redis supports per-key TTL (EXPIRE), a maxmemory limit, and eviction via maxmemory-policy: noeviction (the default; writes error when full), allkeys-lru/lfu/random (any key), or volatile-lru/lfu/ttl (keys with a TTL only). [T3][S-0159]
- volatile-* eviction policies behave like noeviction if no keys carry an expiration — a cache using volatile policies must set TTLs on its entries or writes will fail under memory pressure. [T3][S-0159]
- Facebook's memcache fleet serves billions of requests per second and holds trillions of items: keys are partitioned across servers (consistent hashing), hot data is replicated within pools, and high-churn and low-churn keys are placed in separate pools so one workload's evictions do not displace another's entries. [T1][S-0158]
- Memcached is populated on demand (demand fill): values are set when a miss occurs rather than preloaded, so its hit behavior depends entirely on read patterns and eviction. [T1][S-0158]

### Hit-ratio economics

- Cache effectiveness is measured by hit ratio (reads served from cache); because only misses reach the data store, origin load is proportional to the miss rate — a hit-ratio drop from 99% to 98% doubles miss traffic and therefore doubles store load. [T3][S-0157]
- The design goal of a cache tier is load reduction on the data store: Facebook's memcache added leases, pools, and replication explicitly to reduce backing-store query load, and measured the payoff (17,000/s to 1,300/s on a contended key). [T1][S-0158]

## Boundaries / common misunderstandings

- "Write-back is always faster": write-behind accelerates only the write path, not reads; it adds inconsistency windows and a data-loss risk, so it is a targeted trade, not a general speed-up. [T3][S-0157]
- "TTL keeps the cache fresh": TTL only bounds staleness — an entry can be served long after the source changed; freshness on writes requires invalidation. [T1][S-0158]
- "The cache can be treated as authoritative": every pattern here (except write-through at write time) can serve data the store has changed; the store remains the source of truth. [T3][S-0157]
- "Eviction policy is an afterthought": mixing high-churn and low-churn data in one cache pool lets one workload's evictions destroy another's hit ratio — pool/policy design is part of cache design. [T1][S-0158]
- "HTTP caching and application caching are the same game": HTTP caches are declarative (the origin controls freshness via headers) with no write-path integration; application caches are imperative and need application-managed invalidation. [T2][S-0009]
- "A stampede is just a slow first read": at scale, synchronized rebuild of a hot key is an availability event for the store — leases and refresh-ahead exist precisely because it is not. [T1][S-0158]

## References (evidence records)

- S-0009 — RFC 9111: HTTP Caching (IETF, 2022): private/shared cache placement, freshness/TTL, Authorization rule. (T2)
- S-0157 — Hazelcast, "A Hitchhiker's Guide to Caching Patterns" (2026): cache-aside, read-through, write-through, write-behind, refresh-ahead trade-offs. (T3)
- S-0158 — Nishtala et al., "Scaling Memcache at Facebook" (NSDI 2013): thundering herd, leases, stale sets, invalidation, pools. (T1)
- S-0159 — Redis eviction policy documentation (2026): maxmemory-policy, noeviction default, volatile/allkeys policies. (T3)
