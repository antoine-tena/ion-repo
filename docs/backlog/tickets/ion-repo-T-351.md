# ion-repo#T-351 · `kiln dev` runs any repo without being told
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q111: "incredible, but its detection must widen
  so it launches everything without being told"), decision 40

The repos of `kiln adopt` (decision 4) are laid out every way: monorepos, Procfiles, compose
files, `package.json` scripts, Makefiles, Justfiles, devcontainers.
- [ ] Detection from existing work first (doctrine 14): Railpack's and Nixpacks' providers, which
  read how hundreds of stacks start, before any rule of kiln's own.
- [ ] Measured on a corpus of public repos: the share of repos whose servers come up with no question;
  each miss a test.
