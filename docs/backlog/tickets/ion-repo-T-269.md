# ion-repo#T-269 · Production watched: SLOs, alerts on symptoms, private metrics, dashboards
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Observability), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.41, "Production watched, backups restored": A runbook whose commands exist, backups
with a restore job, uptime and cron checks, alerts on symptoms, metrics kept private.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OB03** `SLO` (draft): objectives as code (OpenSLO, Sloth, Pyrra). L1 · fix J · assess.
- [ ] **OB04** `ALERT-ON-SYMPTOMS` (draft): alert rules on error rates and latency rather than CPU,
  read from Prometheus rule files. L2≈ · fix J · assess.
- [ ] **OB05** `METRICS-PRIVATE`: a `/metrics` endpoint behind authentication or on an internal
  port. L2 · fix J · trial.
- [ ] **OB08** `DASHBOARDS-AS-CODE`: dashboards committed (Grafana JSON, Grafonnet, Perses). L0 ·
  fix J · assess.
- [ ] **OB10** `QUIET-HEALTH-LOGS`: health checks left out of access logs. L2 · fix S · assess.
- [ ] **OB11** `TRACE-SAMPLING`: a sampling ratio set from the environment. L2 · fix S · assess.
- [ ] **OB12** `LOG-RETENTION`: retention set in the log stack, with `RETENTION` (PD). L1 · fix S ·
  assess.
