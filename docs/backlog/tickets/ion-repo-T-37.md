# ion-repo#T-37 · Docker or podman: the engine the machine has
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: opened on 16 October 2026, declined on 17 October, reopened by antoine's answers of
  26 October 2026 (Q41: "say podman is highly recommended, but
  not mandatory"), decision 17

Many strangers on macOS have Docker Desktop or OrbStack: refusing them is friction at the first
try. The grid's container rules are engine-neutral already (ion-repo#T-125).
- [ ] `kiln dev`'s backing services and `kiln ci`'s throwaway databases run on podman or Docker,
  whichever the machine has, podman first; `kiln doctor` says podman is recommended, and why
  (rootless, no daemon), without failing on Docker.
