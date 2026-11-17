# ion-repo#T-227 · Dockerfiles that behave: build secrets, signals, pipefail, one process
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Containers), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.19, "Containers built right": Dockerfiles read stage by stage (v0.6.9): the final
user, multi-stage builds, secrets at build time, exec form, images by tag and digest everywhere.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CO11** `BUILD-SECRETS`: secrets through `--mount=type=secret`, never `ARG` or `ENV`
  (BuildKit's `SecretsUsedInArgOrEnv` check). L2 · fix J · adopt.
- [ ] **CO12** `EXEC-FORM`: `CMD` and `ENTRYPOINT` in JSON form so signals reach the process
  (BuildKit's `JSONArgsRecommended`). L2 · fix S · adopt.
- [ ] **CO13** `PIPEFAIL`: `SHELL [..., "-o", "pipefail", "-c"]` before a `RUN` with a pipe
  (DL4006). L2 · fix S · adopt.
- [ ] **CO14** `INIT-PROCESS`: `init: true` or tini where the main process doesn't reap its
  children. L2≈ · fix S · assess.
- [ ] **CO15** `OCI-LABELS`: `org.opencontainers.image.source`, `revision` and `licenses` on
  published images. L2 · fix S · trial.
- [ ] **CO28** `HADOLINT-CLEAN`: hadolint passes, as a mapped tool (F). L4 · fix J · trial.
- [ ] **CO29** `ONE-PROCESS`: no supervisord or `&` chain running several services in one container.
  L2 · fix J · trial.
