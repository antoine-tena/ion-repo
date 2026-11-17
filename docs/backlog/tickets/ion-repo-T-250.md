# ion-repo#T-250 · The import graph: cycles, feature folders, change coupling
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, History, forge and
  registries, Structure), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.33, "Architecture you can see": An import graph per language: cycles, layers, sealed
domains, god modules, files that always change together.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **E09** Cross-file detectors: every job that tests also lints; every Django app with models
  registers an admin or says why; every route has a test that calls it (routes extracted, tests
  searched).
- [ ] **E10** An import graph per language (Python's `ast`, an ES-module scanner): cycles, layers
  (SEALED-DOMAIN), dead modules, fan-in and fan-out.
- [ ] **M09** Change coupling: files that always change together across folders show a boundary in
  the wrong place.
- [ ] **ST01** `FEATURE-FOLDERS` (draft): layer folders (`models/`, `views/`, `services/`,
  `controllers/`) that each span several domains, found by clustering the import graph. L3≈ · fix J
  · trial.
- [ ] **ST13** `NO-IMPORT-CYCLES`: no cycle between modules or packages. L3 · ratchet · trial.
