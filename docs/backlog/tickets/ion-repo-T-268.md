# ion-repo#T-268 · Production that holds: backups restored, runbooks, uptime, recovery targets
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Operations), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.41, "Production watched, backups restored": A runbook whose commands exist, backups
with a restore job, uptime and cron checks, alerts on symptoms, metrics kept private.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OP02** `ASYNC-HEALTH` (draft): workers and the scheduler report health (a Celery ping, a
  heartbeat file probed by compose). L2≈ · fix J · trial.
- [ ] **OP03** `TESTED-BACKUPS` (draft): a backup job in code (pg_dump, restic, borg) with a
  scheduled restore job beside it. L1≈ · fix J · trial.
- [ ] **OP05** `FEATURE-FLAGS` (draft): a flags library or module present where risky changes ship.
  L1≈ · fix J · assess.
- [ ] **OP06** `TESTED-SELF-HEALING` (draft): restart policies plus a script that exercises a known
  failure. L1≈ · fix J · assess.
- [ ] **OP13** `RUNBOOK`: deploy, rollback, restore and rotate written down (`docs/runbook.md`),
  with commands that exist. L1 · fix J · trial.
- [ ] **OP16** `UPTIME-CHECKS`: an outside check declared (Uptime Kuma, Gatus, a cron monitor) for
  production profiles. L1≈ · fix J · assess.
- [ ] **OP17** `CRON-MONITORED`: scheduled jobs ping a dead man's switch. L2≈ · fix J · assess.
- [ ] **OP18** `RECOVERY-TARGETS`: RPO and RTO stated in the runbook, the backup schedule matching
  them. L1≈ · fix J · assess.
- [ ] **OP19** `HOSTS-AS-CODE`: servers configured by code (Ansible, cloud-init, NixOS), not by
  hand. L0 · fix J · trial.
- [ ] **OP22** `STAGING-LIKE-PROD`: staging differs from production by values only. L1≈ · fix J ·
  assess.
- [ ] **OP23** `COST-GUARDS`: budgets and alerts declared with the cloud resources. L1 · fix J ·
  assess.
- [ ] **OP24** `DATA-RESIDENCY`: regions in the IaC and settings inside the EU for profiles that
  promise it. L1 · fix J · assess.
