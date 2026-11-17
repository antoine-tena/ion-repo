# ion-repo#T-139 · The compressor: removals proven by types, tests and behaviour
- **Type**: idea
- **Priority**: ⚪ background
- **Status**: in progress — started before ion-repo#T-138's number, at antoine's request (21 October
  2026); the compressor's own dry run gives that number. Merged into develop on 22 October
  2026: `kiln fix --rule DEAD-CODE` and `--rule UNUSED-DEPENDENCIES`, proven by the type
  checker and the tests; the behaviour comparison and the dependency replacement remain
- **Opened**: 2026-10-17
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026, fourth pillar

No open tool removes existing code with a proof.
- [ ] `kiln fix` removes what ion-repo#T-138 found, each removal proven in steps (type checker, then
  tests, then behaviour compared); an unproven removal is not applied. Type first, compress
  after.
- [x] Never rewritten: cryptography, parsers, time zones, Unicode.
- [ ] Replacing a dependency by the part actually used comes second, after measurements: the
  most striking, and the riskiest.
