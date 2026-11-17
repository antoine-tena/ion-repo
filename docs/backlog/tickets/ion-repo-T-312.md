# ion-repo#T-312 · PHP read: Composer, Laravel, Symfony, WordPress
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, API, contracts and typing), made
  a ticket on 25 October 2026 at antoine's request; one stack per ticket from the same day (Ruby in
  ion-repo#T-324)

Planned in v0.7.8, "PHP repos, read": Composer, Laravel, Symfony and WordPress read, with their
analysers, formatters, tests and auditor.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B10** PHP: Composer, Laravel, Symfony, WordPress (themes, plugins, wp-config), PHPStan or
  Psalm, PHP-CS-Fixer, PHPUnit or Pest, `composer audit`.
- [ ] **F10** (PHP's part) `composer audit`.
- [ ] **AT26** `PHPSTAN-LEVEL`: PHPStan at level 6 or higher, or Psalm's equivalent. L1 · ratchet ·
  trial.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read PHP
  repos too, each with a passing and a failing example from PHP.
