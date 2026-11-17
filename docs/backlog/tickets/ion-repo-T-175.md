# ion-repo#T-175 · `kiln fix` runs the checks once, then bisects on red
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

Today the whole test suite runs after each converter: ten rules, ten runs, which kiln-bot pays
in CI minutes (ion-repo#T-59).
- [ ] Every converter applied, one commit each, then the checks once; when red, a bisection
  over the commits finds the culprit, which alone is undone.
- [ ] The network lookups (commit SHAs, image digests) resolved in parallel before the
  converters start.
- [ ] The time saved measured on the two training copies, written in the release note.
