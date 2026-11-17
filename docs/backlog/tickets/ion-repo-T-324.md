# ion-repo#T-324 · Ruby read: Bundler, Rails, RuboCop, bundler-audit
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-312 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem, API, contracts and typing)

Planned in v0.7.16, "Ruby repos, read": Bundler and Rails read, with RuboCop, Sorbet or RBS, RSpec
or Minitest and bundler-audit.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B11** Ruby: Bundler, Rails (credentials, `force_ssl`, Brakeman), RuboCop, Sorbet or RBS,
  RSpec or Minitest, bundler-audit.
- [ ] **F10** (Ruby's part) bundler-audit.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Ruby repos too, each with a passing and a failing example from Ruby.
