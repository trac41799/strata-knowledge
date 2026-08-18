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

# Caching Strategies — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember** — name cache-aside, read-through, write-through, and write-behind, and recall Redis maxmemory-policy groups and the noeviction default ([S-0157], [S-0159]).
- **understand** — explain where cache-aside vs read-through loading logic lives, and why TTL alone gives only bounded staleness ([S-0157], [S-0158]).
- **apply** — choose a pattern set (read path, write path, TTL, invalidation, eviction) for a given workload and trace its behavior on a read/write sequence ([S-0157], [S-0159]).
- **apply** — apply stampede mitigations (leases, refresh-ahead) to a hot-key timeline ([S-0158]).
- **analyze** — position strategies on the consistency spectrum and argue the store-load economics of a hit-ratio change.

## Worked example — decision trace for a product catalog service

Requirements: 5,000 reads/s of catalog items; 5 writes/s via an admin tool; a "new product" must be visible within ~60 s; a 10x read spike is expected during a sale; the database must never see >2,000 qps.

1. **Read path: cache-aside.** Reads check the Redis cache; on miss, load from the store, populate, return. The loading logic lives in the application ([S-0157]).
2. **TTL: 60 s.** Bounds staleness: even a missed invalidation disappears within a minute ([S-0159], [S-0009]).
3. **Write path: invalidate-on-write.** Admin update → write the store, delete the cache key. The next read repopulates; readers may see a brief miss right after a write, which is acceptable ([S-0158]).
4. **Hot key: sale product.** At sale launch, one product key gets most reads; when its entry expires, thousands of readers could stampede the store. Mitigation: refresh-ahead for known hot keys (recompute before expiry) or a single-flight/lease-style rebuild so only one request rebuilds ([S-0157], [S-0158]). With a lease token rate-limited to once per 10 s, the store sees ~1 rebuild per 10 s instead of thousands (Facebook: 17,000/s → 1,300/s) ([S-0158]).
5. **Rejected options.** Write-through: write rate is 5/s; paying write latency and caching unread data buys nothing. Write-behind: any loss window on writes is unacceptable for catalog data ([S-0157]).
6. **Config.** Redis: maxmemory set; eviction allkeys-lru (pure cache — every key is safe to evict) or volatile-lru with TTL on every entry; note volatile-* behaves like noeviction if keys lack TTLs ([S-0159]).

## Elaboration prompts

- Why is "delete on write" safer than "set on write" under concurrency? (Two writers, reordered → stale set; leases exist because of this.) [S-0158]
- If cache-aside leaves the store as the source of truth, what happens to correctness when a background job updates the store without touching the cache?
- Why does the read path in read-through still pay a miss cost even though "the cache handles everything"?
- At what write rate does write-through stop being silly? At what durability requirement does write-back become unacceptable? (Work the trade with numbers.)
- Facebook rate-limits lease tokens per key: what breaks if the rate is 0 (no tokens) or infinite?
- Your hit ratio is 95% and the store is at 90% CPU: which lever matters — the ratio or the store's headroom? [S-0157]

## Common misconceptions

1. **"Write-back is always faster."** It speeds only the write path; reads are unaffected, consistency is delayed, and a cache failure before flush loses data. It is a targeted trade, not a general speed-up. [S-0157]
2. **"TTL keeps data fresh."** TTL bounds staleness; the entry is served until expiry regardless of source changes. Freshness on writes requires invalidation. [S-0158]
3. **"Invalidation is trivial — just update the cache on write."** Concurrent reordered writes create stale sets (an old value installed last); production systems add lease tokens to detect them. [S-0158]
4. **"Cache everything, eviction will sort it out."** Eviction policy and pool separation are design decisions: mixing high-churn and low-churn keys lets one workload evict the other's hot data. [S-0158]
5. **"maxmemory-policy volatile-ttl is a safe default."** volatile-* policies evict nothing if no keys carry TTLs (behave like noeviction → writes fail); every cache key must have a TTL for volatile policies to work. [S-0159]
6. **"HTTP caching and app caching are the same."** HTTP caches are declarative and need no write-path integration; application caches are imperative and require the application to implement invalidation. [S-0009]

## Feynman targets

- "Explain to a new hire why a 99% hit ratio is different from a 98% hit ratio, using store load" ([S-0157]).
- "Explain what a thundering herd is and how a rate-limited token fixes it — in two minutes, without the word 'lease'" ([S-0158]).
- "Explain when you would refuse to use write-behind, and why" ([S-0157]).
- "Explain the difference between TTL and invalidation using a newspaper: one says when the paper is thrown away, the other says when it's pulled from shelves."

## Interleaving hooks

- **systems-software/http-caching** — the declarative counterpart: freshness (max-age), validators (ETag/If-None-Match), and shared-vs-private placement are the HTTP-native answers to TTL/invalidation/placement questions ([S-0009]).
- **systems-software/virtual-memory** — the TLB is a hardware cache-aside with hardware-managed misses; hit-ratio economics repeat at every level of the memory hierarchy.
- **hardware/memory-hierarchy** — cache placement, block size, and eviction policy analogies transfer directly (LRU, clock, polluting a cache with cold data).
- **systems-software/distributed-systems-basics** — a distributed cache is a partitioned system: consistent hashing, replication, and failure modes apply to the cache tier too ([S-0158]).
