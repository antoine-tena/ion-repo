# ion-repo#T-335 · Any CI, any machine, any size: the bar's matrix, run
- **Type**: task
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: the bar of v1.0.0 (antoine, 25 October 2026), its CI, machines and sizes made the gate
  of v0.9.0 the same day

Planned in v0.9.0, "Any CI, any machine, any size": Milestone decided by antoine (25 October 2026),
reached here, the last before the format freezes: the bar of v1.0.0 run as a matrix in kiln's own
CI, on GitHub's, GitLab's and one more CI, Linux, macOS and WSL, x86-64 and ARM64, a monorepo and a
million files, each scored within its budget.

The gate of v0.9.0: the milestone is cut only once the matrix is green.

- [ ] A matrix in kiln's own CI (on `release/**`): a sample repo scored on GitHub's CI, GitLab's and
  the one the corpus uses most after them; on Linux, macOS and WSL; on x86-64 and ARM64, glibc and
  musl; offline; a monorepo and a million-file tree, each within its budget.
- [ ] The milestone's note: what each cell measured, and what a cell leaves "unknown".
