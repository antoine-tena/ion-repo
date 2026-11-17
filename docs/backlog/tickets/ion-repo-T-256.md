# ion-repo#T-256 · Schedulers and workers watched: one scheduler, health, visibility, dead letters
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Background tasks), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.35, "Background tasks and concurrency": Tasks that retry, time out, take IDs and run
outside the request; increments and locks that survive two requests at once; Celery's settings made
exact.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **BG08** `ONE-SCHEDULER`: the beat or scheduler service runs as a single replica. L1 · fix J ·
  adopt.
- [ ] **BG09** `TASKS-TAKE-IDS`: tasks receive identifiers, not model instances. L2≈ · fix J ·
  trial.
- [ ] **BG10** `SCHEDULES-IN-CODE`: periodic jobs declared in code (beat schedule, django-q2), not
  in a host's crontab. L1≈ · fix J · trial.
- [ ] **BG11** `WORKER-HEALTH`: worker services have a health check and a stop grace period. L1 ·
  fix S · trial.
- [ ] **BG12** `VISIBILITY-TIMEOUT`: with a Redis broker, the visibility timeout exceeds the longest
  task. L2 · fix J · trial.
- [ ] **BG13** `DEAD-LETTERS`: failed tasks land where a human sees them. L2≈ · fix J · assess.
