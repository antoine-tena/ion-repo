# ion-repo#T-337 · The Spring Boot pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: framework coverage review of 26 October 2026 at antoine's request: the most used
  frameworks of the 2025 surveys checked against the plan; the pack of its language held only the
  language's rules

Planned in v0.7.5, "The Java and Kotlin pack": A supported LTS, a verified wrapper, locked
dependencies and a bug finder in the build, then Spring Boot's own rules, counted once ten corpus
repos of Java and Kotlin were checked (B24).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FP29** Spring Boot · `SPRING-DDL-AUTO`: `spring.jpa.hibernate.ddl-auto` never `update`,
  `create` or `create-drop` outside development; the schema moved by Flyway or Liquibase. L1 · fix J
  · adopt.
- [ ] **FP30** Spring Boot · `SPRING-OPEN-IN-VIEW-OFF`: `spring.jpa.open-in-view=false`, so no query
  runs while the view renders. L1 · fix S · trial.
- [ ] **FP31** Spring Boot · `SPRING-VALIDATION`: `@Valid` or `@Validated` on every request body. L2
  · fix J · adopt.
- [ ] **FP32** Spring Boot · `SPRING-CONSTRUCTOR-INJECTION`: dependencies through the constructor,
  no `@Autowired` field. L2 · fix J · trial.
- [ ] **AS20** (Spring's part) `NO-HARDCODED-PASSWORDS`: no password, key or token in
  `application.yml` or `application.properties`, `${…}` placeholders from the environment instead.
  L1 · fix J · adopt.
- [ ] **AS22** (Spring Security's part) `CSRF-ON`: `csrf` disabled only on a stateless API, with a
  justification marker. L2 · fix J · adopt.
- [ ] **AS48** (Spring's part) `NO-SQL-INJECTION`: `createNativeQuery`, `JdbcTemplate` and
  `@Query(nativeQuery = true)` never built by concatenation. L2 · fix J · adopt.
- [ ] **DM18** (Flyway's and Liquibase's part) `ORM-MIGRATIONS-COMMITTED`: their migrations
  committed. L0 · fix J · adopt.
- [ ] Ten corpus repos of Spring Boot scored and their findings checked before the pack counts
  (B24), each false alarm fixed in the engine.
