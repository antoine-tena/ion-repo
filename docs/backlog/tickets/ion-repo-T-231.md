# ion-repo#T-231 · The scored CI rules read from the CI model
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (CI/CD), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.21, "One CI model, any workflow": Jobs, steps, triggers and permissions extracted
once; `make test` resolved into what it runs; zizmor and actionlint as detectors; the scored CI
rules read from that model.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CI01** `CI-PRESENT` (scored): "every change is checked before it ships" (decision 6): fast
  checks at each commit and the whole CI before each release, on the forge or on the machine with
  its verdict kept (`kiln ci`), or a CI on every pull request; read from any CI (C) with its
  triggers. With profiles (ion-repo#T-39), company and enterprise ask for CI on every pull request.
- [ ] **CI02** `LINT-IN-CI` (scored): lint commands read per component from any CI, as for
  `TESTS-IN-CI` (TE), through `make`, `just`, `task`, `nox`, `tox` and package scripts.
- [ ] **CI03** `WORKFLOW-INJECTION` (scored): zizmor's template-injection audit (F) instead of one
  regex; an expression passed through `env:` passes.
- [ ] **CI04** `WORKFLOW-PERMISSIONS` (scored): `write-all`, and a job's `contents: write` with no
  step that writes, flagged.
- [ ] **CI05** `PULL-REQUEST-TARGET` (scored): flagged when the workflow checks out or runs the pull
  request's head; `workflow_run` with downloaded artifacts too (zizmor's dangerous-triggers).
