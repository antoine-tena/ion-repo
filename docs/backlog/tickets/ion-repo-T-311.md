# ion-repo#T-311 · The Java and Kotlin pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (C# in ion-repo#T-323)

Planned in v0.7.5, "The Java and Kotlin pack": A supported LTS, a verified wrapper, locked
dependencies and a bug finder in the build, then Spring Boot's own rules, counted once ten corpus
repos of Java and Kotlin were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP13** Java and Kotlin · `JAVA-LTS`: a supported LTS (17, 21, 25) in the toolchain's config.
  L1 · fix S · adopt.
- [ ] **SP14** Java and Kotlin · `WRAPPER-COMMITTED`: Gradle or Maven wrapper committed with its
  checksum. L1 · fix S · adopt.
- [ ] **SP15** Java and Kotlin · `DEPENDENCY-LOCKING`: Gradle's dependency locking, or Maven plugins
  and versions pinned and checked by the enforcer. L1 · fix S · trial.
- [ ] **SP16** Java and Kotlin · `BUG-FINDER`: Error Prone or SpotBugs in the build; detekt and
  ktlint for Kotlin. L1 · fix S · trial.
- [ ] Ten corpus repos of Java and Kotlin scored and their findings checked before the pack counts
  (B24), each false alarm fixed in the engine.
