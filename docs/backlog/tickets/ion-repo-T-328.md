# ion-repo#T-328 · The C and C++ pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-315 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.11, "The C and C++ pack": Warnings as errors, sanitizers in CI, clang-tidy, fuzzing
for parsers and managed dependencies, counted once ten corpus repos of C and C++ were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP35** C and C++ · `COMPILER-WARNINGS`: `-Wall -Wextra -Werror` (or `/W4 /WX`) in the build.
  L1 · fix S · trial.
- [ ] **SP36** C and C++ · `SANITIZERS-IN-CI`: AddressSanitizer and UndefinedBehaviorSanitizer
  builds in CI. L1 · fix S · trial.
- [ ] **SP37** C and C++ · `CLANG-TIDY`: configured and run. L1 · fix S · trial.
- [ ] **SP38** C and C++ · `FUZZING`: libFuzzer harnesses or OSS-Fuzz for parsers (Scorecard's
  Fuzzing). L1 · fix J · assess.
- [ ] **SP39** C and C++ · `MANAGED-DEPENDENCIES`: vcpkg or Conan manifests rather than copied
  sources. L1 · fix J · trial.
- [ ] Ten corpus repos of C and C++ scored and their findings checked before the pack counts (B24),
  each false alarm fixed in the engine.
