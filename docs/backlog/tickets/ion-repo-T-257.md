# ion-repo#T-257 · Concurrency: atomic updates, locks, timeouts, async servers, Celery made exact
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Concurrency, Framework packs), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.35, "Background tasks and concurrency": Tasks that retry, time out, take IDs and run
outside the request; increments and locks that survive two requests at once; Celery's settings made
exact.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CC01** `ATOMIC-INCREMENTS` (draft, Django): `x.n += 1` then `x.save()` becomes `F("n") + 1`.
  L2≈ · fix S · trial.
- [ ] **CC02** `LOCKS` (draft): a read-modify-write inside a transaction uses `select_for_update()`.
  L2≈ · fix J · trial.
- [ ] **CC03** `NO-BLOCKING-IN-ASYNC`: no `time.sleep`, `requests`, sync file or ORM call inside
  `async def` (ruff's ASYNC). L4 · fix J · adopt.
- [ ] **CC04** `TIMEOUTS`: every outgoing HTTP call has a timeout (ruff's S113; fetch with a signal,
  axios with `timeout`). L2 · fix S · adopt.
- [ ] **CC05** `DB-STATEMENT-TIMEOUT`: the database connection sets a statement timeout. L2 · fix S
  · trial.
- [ ] **CC06** `CHECK-THEN-ACT`: `if not exists(): create()` becomes `get_or_create` over a unique
  constraint. L2≈ · fix J · trial.
- [ ] **CC07** `ASGI-SERVER`: an async app served by an ASGI server (Uvicorn, Granian, Hypercorn,
  Daphne). L1 · fix J · adopt.
- [ ] **CC08** `WORKERS-SIZED`: the web server's worker count comes from the environment or the CPU
  count. L1 · fix S · trial.
- [ ] **CC10** `NO-THREADS-IN-REQUESTS`: no thread started inside a request handler. L2≈ · fix J ·
  trial.
- [ ] **FP06** Celery · the BG theme's rules, made exact for Celery's settings (`task_acks_late`,
  `task_time_limit`, the serializer, the beat replica). L1 · fix S · adopt.
