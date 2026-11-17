# ion-repo#T-341 · R read and its pack: renv, lintr, testthat, R CMD check
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: stack coverage review of 26 October 2026, at antoine's request ("sois sûr que kiln
  couvre bien tout"): R, at 5 % of the 2025 Stack Overflow survey and common in coursework and
  research, was only a data pack of B14

Planned in v0.7.21, "R repos, read and packed": R packages and analyses read and packed in one
release: DESCRIPTION and renv, lintr, testthat and R CMD check, beyond the notebooks the data
science release (v0.6.58) reads.

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B14** (R's part) R: `DESCRIPTION` and `NAMESPACE`, `renv.lock`, lintr, styler, testthat,
  `R CMD check` in CI (r-lib/actions), Shiny apps; R Markdown and Quarto stay read as notebooks
  (ion-repo#T-292).
- [ ] **SP45** R · `RENV-LOCKED`: `renv.lock` committed for an analysis or an app, restored in CI.
  L0 · fix S · adopt.
- [ ] **SP46** R · `R-CMD-CHECK`: a package passes `R CMD check` in CI without error or warning. L1
  · fix S · adopt.
- [ ] **SP47** R · `LINTR`: lintr configured and run. L1 · fix S · trial.
- [ ] **SP48** R · `NO-SETWD`: no `setwd()` or absolute path in a script; the project's root
  (`here`) instead. L2 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read R
  repos too, each with a passing and a failing example from R.
- [ ] Ten corpus repos of R scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
