# ion-repo#T-135 · Tests at the lowest token cost, measured on one module first
- **Type**: idea
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 ("the most tests for the fewest tokens"; validation
  step 5)

Asking Claude for every test is the expensive way. On a local copy of the reference repo, its
money module leaves 3 surviving mutants out of 16.
- [ ] mutmut on that module, then Claude writes only the tests that kill the survivors; tokens
  and session time counted; a test is kept only if it passes five times in a row and kills a
  mutant or adds coverage.
- [ ] If the number is net, the recipe joins `/kiln:modernize`: coverage and survivors measured
  by script (mutmut for Python, Stryker for TypeScript), Claude on the holes only, the rest
  thrown away unread; coverage and survivors as ratchets.
