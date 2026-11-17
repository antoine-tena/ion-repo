# ion-repo#T-326 · Elixir read and its pack: mix, Phoenix, Credo, Sobelow
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-313 and ion-repo#T-314 on 25 October 2026, one stack per ticket (kiln score ideas
  of 24 October 2026: Every ecosystem, Stack packs)

Planned in v0.7.22, "Elixir repos, read and packed": A smaller ecosystem, read and packed in one
release: mix and Phoenix, with Credo, Dialyzer, Sobelow and mix_audit as its rules.

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B12** (Elixir's part) Elixir: mix, Phoenix, Credo, Dialyzer, Sobelow.
- [ ] **SP40** Elixir · `MIX-AUDIT`: mix_audit or `mix hex.audit` in CI, `mix.lock` committed. L1 ·
  fix S · adopt.
- [ ] **SP41** Elixir · `CREDO-AND-DIALYZER`: both configured. L1 · fix S · trial.
- [ ] **SP42** Elixir · `SOBELOW`: Sobelow for Phoenix apps. L1 · fix S · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Elixir repos too, each with a passing and a failing example from Elixir.
- [ ] Ten corpus repos of Elixir scored and their findings checked before the pack counts (B24),
  each false alarm fixed in the engine.
