# ion-repo#T-251 · Architecture you can see: thin views, a service layer, sealed domains
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

- [ ] **AR02** `API-CALLS` (draft, Vue): no `$fetch` or `useFetch` in components outside a
  composable or a service layer. L2 · fix J · trial.
- [ ] **AR03** `THIN-VIEWS` (draft, Django): views under a few dozen lines, without ORM writes. L2≈
  · fix J · trial.
- [ ] **AR04** `THIN-MODEL` (draft, Django): model methods past a few dozen lines flagged. L2≈ · fix
  J · assess.
- [ ] **AR05** `SERVICE-LAYER` (draft): an app whose views write data has a services module. L2≈ ·
  fix J · assess.
- [ ] **AR06** `LAYERED-ARCHITECTURE` (draft): import contracts declared (import-linter,
  dependency-cruiser, eslint-plugin-boundaries) and run in CI. L1 · fix J · trial.
- [ ] **AR07** `SEALED-DOMAIN` (draft): domain packages import no web framework, HTTP client or ORM
  session. L3 · fix J · trial.
- [ ] **AR08** `TWELVE-FACTOR-CONFIG`: config from the environment, one settings tree, no
  per-environment file holding secrets. L2 · fix J · adopt.
- [ ] **AR09** `NO-GOD-MODULES`: no module both large and imported by most of the code. L3 · ratchet
  · assess.
