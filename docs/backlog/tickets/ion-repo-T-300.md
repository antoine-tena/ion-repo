# ion-repo#T-300 · Every kind of repo, each with its rules
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every kind of repo, every
  profile, Nothing to do, Application security), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.62, "Every kind of repo": A library, an awesome list, a template, a fork or an
archive each held to what it needs; the kind and what kiln assumed on the report's first lines, with
their evidence.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A39** Forks recognized (an `upstream` remote, or the forge says so): the fork's own changes
  scored apart from upstream's code.
- [ ] **A40** Archived repos (the forge's flag, an "archived" notice in the README) scored only on
  what still matters: secrets, licence.
- [ ] **D01** Kinds recognized: web app (backend, frontend, full stack), API, library (PyPI, npm,
  crates.io, Maven Central…), CLI, desktop, mobile, browser extension, editor extension, GitHub
  Action, Claude Code plugin or MCP server, data science, ML training, data pipeline (dbt, Airflow,
  Dagster), infrastructure, docs site, static site, dotfiles, template, coursework, research
  artefact, game, firmware, hardware, HPC, WordPress, Shopify theme, serverless functions, bot,
  smart contracts, awesome list, single script.
- [ ] **D02** Each kind its rules: a library needs semver, a changelog, typed exports and trusted
  publishing, not health probes; an awesome list needs link checks, not tests (today TESTS-PRESENT
  fails every awesome list).
- [ ] **D03** A repo can be several kinds (a library with a docs site and a CLI): kinds per
  component.
- [ ] **D07** Thresholds that scale: a 200-line script isn't held to a monorepo's architecture
  rules; ratchets on a big repo start from its own numbers.
- [ ] **D11** Kind and profile on the report's first lines with their evidence; `kiln set
  kind=library` exists, is never needed, and each use is a ion-repo#T-38 signal.
- [ ] **D12** The forge's topics and description read with `--online` as hints (`homework`,
  `tutorial`, `template`, `awesome`).
- [ ] **D13** Template repos (`is_template`, `copier.yml`) scored on what they generate: rendered
  with defaults in a sandbox, the result scored. A template's score is its children's.
- [ ] **D14** Tutorials and example repos recognized, so the study and the fleet don't count them
  (a study's exclusions as code).
- [ ] **K14** The integration branch, the main language and the profile detected; the report says
  what it assumed.
- [ ] **AS44** `EXTENSION-PERMISSIONS`: browser extensions ask for the fewest permissions and hosts.
  L1 · fix J · trial.
- [ ] **D17** Static and docs sites read: Hugo (modules at a version), Jekyll (`Gemfile.lock`),
  MkDocs, Docusaurus, Eleventy, Gatsby, Sphinx; the site built in CI, its links checked, its theme
  pinned rather than copied.
- [ ] **FP43** Solidity · `SOLIDITY-CHECKED`: Foundry or Hardhat tests and Slither in CI, the
  compiler version pinned exactly (`pragma solidity 0.8.28;`, not `^`). L1 · fix S · trial.
