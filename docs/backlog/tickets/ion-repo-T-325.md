# ion-repo#T-325 · The Ruby pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-313 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.17, "The Ruby pack": Brakeman and bundler-audit in CI, RuboCop configured, a
supported Ruby and no `permit!`, counted once ten corpus repos of Ruby were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP26** Ruby · `BUNDLER-AUDIT` and `BRAKEMAN`: both in CI for Rails apps, `Gemfile.lock`
  committed. L1 · fix S · adopt.
- [ ] **SP27** Ruby · `RUBOCOP`: RuboCop or Standard configured. L1 · fix S · adopt.
- [ ] **SP28** Ruby · `RUBY-SUPPORTED`: `.ruby-version` on a supported line. L1 · fix S · adopt.
- [ ] **SP29** Ruby · `RAILS-STRONG-PARAMS`: no `permit!`. L2 · fix J · adopt.
- [ ] Ten corpus repos of Ruby scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
- [ ] **FP36** Rails · `RAILS-STRONG-MIGRATIONS`: the strong_migrations gem, so a migration that
  would lock a live table is stopped. L1 · fix S · trial.
- [ ] **AS01** (Rails' part) `SECRETS`: `config/master.key` and `config/credentials/*.key` never
  committed. L0 · fix J · adopt.
