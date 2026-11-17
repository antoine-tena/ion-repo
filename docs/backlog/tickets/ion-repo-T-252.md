# ion-repo#T-252 · Boundaries between front, back and services: stores, async, one database each
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Architecture), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.33, "Architecture you can see": An import graph per language: cycles, layers, sealed
domains, god modules, files that always change together.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AR12** `STATE-IN-STORES` (Vue): shared state in Pinia stores, not module-level `reactive()`
  singletons. L2 · fix J · trial.
- [ ] **AR13** `NUXT-SERVER-THIN`: `server/api` handlers delegate to services. L2≈ · fix J · assess.
- [ ] **AR14** `ONE-DB-PER-SERVICE`: two services don't share one database's tables (compose and
  settings read together). L1≈ · fix J · assess.
- [ ] **AR15** `ASYNC-BOUNDARY` (Django): async views never call the sync ORM without
  `sync_to_async`. L2 · fix J · adopt.
- [ ] **AR16** `DEPENDENCY-DIRECTION`: stable packages don't depend on volatile ones (fan-in and
  fan-out). L3 · ratchet · assess.
- [ ] **AR17** `NO-CIRCULAR-APPS` (Django): no import cycle between apps. L3 · fix J · trial.
- [ ] **AR18** `FLAGS-IN-ONE-PLACE`: feature flags read through one module or library, not scattered
  `if settings.X`. L2≈ · fix J · assess.
