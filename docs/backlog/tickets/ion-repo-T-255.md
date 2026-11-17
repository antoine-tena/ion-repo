# ion-repo#T-255 · Background tasks that survive: retries, outbox, idempotence, limits
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Background tasks), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.35, "Background tasks and concurrency": Tasks that retry, time out, take IDs and run
outside the request; increments and locks that survive two requests at once; Celery's settings made
exact.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **BG01** `RETRIES` (draft): Celery tasks set `autoretry_for`, `retry_backoff` and
  `max_retries` (or the same in RQ, Dramatiq, Django 6's tasks). L2 · fix J · trial.
- [ ] **BG02** `OUT-OF-REQUEST` (draft): e-mails, webhooks and slow HTTP calls never sent inside a
  view. L2≈ · fix J · trial.
- [ ] **BG03** `TRANSACTIONAL-OUTBOX` (draft): tasks queued through `transaction.on_commit`, not
  inside an open transaction. L2≈ · fix J · trial.
- [ ] **BG04** `IDEMPOTENT-HANDLER` (draft): tasks guarded by a key or a state check. L2≈ · fix J ·
  assess.
- [ ] **BG05** `TASK-TIME-LIMITS`: hard and soft time limits set. L2 · fix S · adopt.
- [ ] **BG06** `ACKS-LATE`: `task_acks_late` with `task_reject_on_worker_lost` for idempotent tasks.
  L2 · fix S · trial.
- [ ] **BG07** `SAFE-SERIALIZER`: tasks serialized as JSON, never pickle. L2 · fix S · adopt.
