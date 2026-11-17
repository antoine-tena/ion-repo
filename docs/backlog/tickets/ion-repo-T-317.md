# ion-repo#T-317 · Monorepos and big trees: project graphs, rules in parallel, a time budget
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Speed), made a
  ticket on 25 October 2026 at antoine's request; the million files split off the same day (ion-repo#T-334)

Planned in v0.8.5, "Monorepos and big trees": Monorepo tools' project graphs read for components and
their links (ion-repo#T-86 staying declined for generating them), rules run in parallel, and a time budget
that says what it left out.

- [ ] **C19** Monorepo tools' project graphs (Nx, Turborepo, Bazel, Pants, Rush, Moon) read for
  components and their links ⚠ ion-repo#T-86 (declined) is about generating monorepos; scoring them is
  another matter.
- [ ] **J09** Rules in parallel: threads for I/O-bound rules, processes on big repos; free-threaded
  Python 3.14 measured.
- [ ] **J17** A time budget (`--budget 2s`): rules by value per cost, and what didn't run is said
  ("not checked: budget").
