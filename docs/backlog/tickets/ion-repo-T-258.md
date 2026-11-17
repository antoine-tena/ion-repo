# ion-repo#T-258 · Caches that invalidate and stay private
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Cache), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.36, "Fast back ends: caches and queries": Real cache backends with timeouts and
invalidation, N+1 queries and missing indexes found, latency budgets kept in the repo.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CA01** `CACHE-TAGS` (draft): invalidation by tags or versioned keys, never by guessing. L2≈
  · fix J · assess.
- [ ] **CA02** `CACHE-STAMPEDE` (draft): expensive recomputations protected (a lock, early refresh,
  jitter). L2≈ · fix J · assess.
- [ ] **CA03** `PROD-CACHE-BACKEND`: the production cache isn't `LocMemCache` or a dummy backend. L2
  · fix J · adopt.
- [ ] **CA04** `EXPLICIT-TIMEOUTS`: every `cache.set` gives a timeout. L2 · fix J · trial.
- [ ] **CA05** `IMMUTABLE-ASSETS`: hashed static assets served with `immutable` and a long max-age
  (Caddy, nginx, Nuxt's `routeRules`). L1 · fix S · trial.
- [ ] **CA06** `PRIVATE-RESPONSES`: authenticated responses are `private` or `no-store`; shared
  caches vary on authentication. L2≈ · fix J · trial.
- [ ] **CA07** `REDIS-EVICTION`: Redis runs with `maxmemory` and the eviction policy its use needs
  (a cache evicts, a broker never does). L1 · fix S · trial.
