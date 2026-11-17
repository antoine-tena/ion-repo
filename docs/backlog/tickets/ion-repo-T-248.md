# ion-repo#T-248 · Strict typing everywhere: libraries, annotations, TypeScript options, problem details
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (API, contracts and typing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.32, "API, contracts and typing": The schema committed and checked for breaking
changes, front types generated from it, typing read through its inheritance and counted as ratchets.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AT10** `PY-TYPED`: a typed Python library ships `py.typed`. L0 · fix S · adopt.
- [ ] **AT11** `ANNOTATIONS-COVERAGE`: the share of fully annotated functions, a ratchet (ruff's ANN
  counts). L4 · ratchet · trial.
- [ ] **AT12** `NO-EXPLICIT-ANY` (Python): `Any` counted (ANN401), as NO-ANY does for TS. L4 ·
  ratchet · trial.
- [ ] **AT13** `TS-UNCHECKED-INDEX`: `noUncheckedIndexedAccess` on. L1 · fix S · trial.
- [ ] **AT14** `TS-EXACT-OPTIONAL`: `exactOptionalPropertyTypes` on. L1 · fix J · assess.
- [ ] **AT15** `TS-VERBATIM-MODULES`: `verbatimModuleSyntax` on. L1 · fix S · assess.
- [ ] **AT16** `DJANGO-STUBS`: django-stubs and its mypy plugin whenever mypy checks Django code. L1
  · fix S · adopt.
- [ ] **AT17** `PROBLEM-DETAILS`: API errors as RFC 9457 problem details. L2≈ · fix J · assess.
- [ ] **AT18** `API-VERSIONED`: public APIs carry a version, in the path or a header. L2≈ · fix J ·
  assess.
