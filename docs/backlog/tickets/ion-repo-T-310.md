# ion-repo#T-310 · Java and Kotlin read: Maven, Gradle, Spring Boot, the LTS lines
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, API, contracts and typing,
  Supply chain), made a ticket on 25 October 2026 at antoine's request; one stack per ticket from
  the same day (.NET in ion-repo#T-322)

Planned in v0.7.4, "Java and Kotlin repos, read": The road to v0.8.0: every common stack scored and
fixed by script as Django is at v0.5.0, stack by stack (decision 1) in the order the corpus measures
(B01; until it does, the order of the 2025 surveys, Stack Overflow's and GitHub's Octoverse). Two
releases a stack, about what Django and Nuxt each took once the engine is set aside: first what its
repos are made of, read, so that the rules spanning stacks see it; then its pack, counted once ten
corpus repos of it were checked (B24). Each stack's rules are written from the corpus when its turn
comes. First Java and Kotlin: Maven and Gradle read with their wrappers, Spring Boot, Quarkus and
Micronaut recognised: kiln's own frozen Java template held to its stack's rules at last.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B08** Java and Kotlin: Maven (wrapper and checksum), Gradle in its Groovy and Kotlin DSLs
  (wrapper validation, version catalogs, locking, verification metadata), Spring Boot, Quarkus,
  Micronaut, Ktor; Checkstyle, SpotBugs, Error Prone, Spotless, ktlint, detekt; JUnit 5; Java's LTS
  lines. kiln's own frozen Java template would finally be scored.
- [ ] **AT27** `KOTLIN-EXPLICIT-API`: explicit API mode for Kotlin libraries. L1 · fix S · trial.
- [ ] **AT28** `JAVA-NULLNESS`: JSpecify annotations checked by NullAway. L1 · fix J · assess.
- [ ] **SU24** `GRADLE-WRAPPER-VERIFIED`: `distributionSha256Sum` set and the wrapper validated in
  CI. L1 · fix S · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Java and Kotlin repos too, each with a passing and a failing example from Java and Kotlin.
