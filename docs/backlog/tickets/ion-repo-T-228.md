# ion-repo#T-228 · Compose for a small server: hardening, no socket, logs and limits
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Containers), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.20, "Compose files for a small server": What a VPS running compose needs: no engine
socket, databases on localhost, logs rotated, limits and restarts, secrets out of the file, images
scanned and signed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CO02** `HARDENED-CONTAINERS` (scored): also read in Kubernetes manifests and Helm values
  (`securityContext`, see IN).
- [ ] **CO16** `COMPOSE-NO-VERSION`: no top-level `version:`, obsolete in the Compose Specification.
  L1 · fix S · adopt.
- [ ] **CO17** `COMPOSE-HEALTHY-DEPENDS`: `depends_on` with `condition: service_healthy` on
  databases. L1 · fix S · adopt.
- [ ] **CO18** `NO-DOCKER-SOCKET`: no `/var/run/docker.sock` mounted, except read-only into a
  declared proxy with its reason; critical. L1 · fix J · adopt.
- [ ] **CO19** `NO-PRIVILEGED`: no `privileged`, `network_mode: host`, `pid: host` or added
  `SYS_ADMIN`, beside `HARDENED-CONTAINERS`. L1 · fix J · adopt.
- [ ] **CO21** `LOG-ROTATION`: `max-size` and `max-file` on the logging driver (json-file grows
  without end by default). L1 · fix S · adopt.
- [ ] **CO22** `RESOURCE-LIMITS`: memory and CPU limits per service. L1 · fix S · trial.
