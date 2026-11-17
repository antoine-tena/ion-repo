# ion-repo#T-259 · Fast back ends: N+1 queries, query counts, indexes, benchmarks
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Performance), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.36, "Fast back ends: caches and queries": Real cache backends with timeouts and
invalidation, N+1 queries and missing indexes found, latency budgets kept in the repo.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PE01** `API-LATENCY` (draft): p95 budgets as k6 thresholds in the repo, or an APM's numbers
  with `--online`. L1≈ · fix J · assess.
- [ ] **PE05** `NO-N-PLUS-ONE`: querysets iterated with related access and no `select_related` or
  `prefetch_related` (L3≈), proven by nplusone in tests (L7). L3≈ · fix J · trial.
- [ ] **PE06** `QUERY-COUNT-TESTS`: list views tested with `django_assert_num_queries` or
  `assertNumQueries`. L2 · fix J · assess.
- [ ] **PE14** `FK-INDEXES`: foreign keys indexed where neither the ORM nor the database does it
  (Prisma's relations on Postgres, raw SQL migrations); Django already does. L2 · fix S · trial.
- [ ] **PE16** `BENCHMARKS`: libraries with hot paths keep benchmarks (pytest-benchmark, Vitest's
  `bench`, `cargo bench`) and a ratchet on them. L1 · fix J · assess.
- [ ] **PE17** `PROFILER-IN-DEV`: a profiler wired in development only (django-silk, pyinstrument's
  middleware). L1 · fix S · assess.
- [ ] **PE19** `COLD-START`: serverless functions' bundle size tracked. L1 · ratchet · assess.
