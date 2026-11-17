# ion-repo#T-374 · Out-of-request work for a project without Celery: [OUT-OF-REQUEST], [OUTBOX], [IDEMPOTENCY]
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: emberstudio session `feat/auth` (accounts copied from annski), 30 October 2026

`django.md` loads [OUT-OF-REQUEST], [OUTBOX], [RETRIES], [ASYNC-HEALTH] and [IDEMPOTENCY] on
every Django repo, and they assume Celery, Redis and an `OutboxEvent` table. emberstudio
(`medium`) has none of them: its account mails (invitation, password reset) could only leave in a
`threading.Thread`, outside any rule, and [IDEMPOTENCY] stayed unapplied. An agent then either
breaks the rule silently or builds a whole Celery stack for three mails.
- [ ] The rules say what a repo without a worker does: a size or a setting (`kiln set
  worker=celery|none`) chooses between the Outbox chain and a lighter path (a mail sent after
  `transaction.on_commit`, a thread for a mail whose timing would reveal an account), written
  as a rule with its limits.
- [ ] [IDEMPOTENCY] says which routes need it when there is no shared cache (payments,
  creations), instead of "every mutation".
- [ ] The Django template offers that path, so the first mail of a project is not improvised.
- [ ] Scheduled work on that same queue (completed 2026-11-02, adoption of annski and booking's
  spec `studio/docs/business/fabrication/reservation.md`): the day-before reminder, the
  anonymisation at the end of retention (ion-repo#T-411). annski's way: tasks published in the
  Outbox inside the caller's transaction (`annski/backend/core/queue.py`), an APScheduler whose
  jobs live in PostgreSQL (`annski/backend/core/scheduler_jobstore.py`), and a heartbeat that the
  container probe reads, so a frozen scheduler is restarted (`annski/backend/core/heartbeat.py`,
  `annski/backend/core/scheduler_health.py`).
