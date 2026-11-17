# ion-repo#T-229 · Compose that survives: restarts, volumes, secrets, scanned and signed images
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Containers), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.20, "Compose files for a small server": What a VPS running compose needs: no engine
socket, databases on localhost, logs rotated, limits and restarts, secrets out of the file, images
scanned and signed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CO23** `RESTART-POLICY`: `restart: unless-stopped` or `always` on long-running services. L1
  · fix S · adopt.
- [ ] **CO24** `NAMED-VOLUMES`: database data in named volumes, never bind-mounted inside the repo.
  L1 · fix S · trial.
- [ ] **CO25** `NO-SECRETS-IN-COMPOSE`: no literal password under `environment:`; `env_file` or
  `secrets:` instead. L1 · fix J · adopt.
- [ ] **CO26** `IMAGES-SCANNED`: built images scanned (Trivy, Grype) in the release workflow. L1 ·
  fix S · trial.
- [ ] **CO27** `IMAGES-SIGNED`: published images signed (cosign) or attested
  (`actions/attest-build-provenance`). L1 · fix S · assess.
- [ ] **CO30** `ROOTLESS-FRIENDLY`: compose files that run under rootless Podman as under Docker
  (`kiln dev` runs Podman). L1 · fix J · assess.
