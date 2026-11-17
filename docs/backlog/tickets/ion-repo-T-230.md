# ion-repo#T-230 · One CI model: every step resolved, injection and privileges on any CI
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Every kind of
  repo, every profile, Mature tools as detectors, Tests), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.21, "One CI model, any workflow": Jobs, steps, triggers and permissions extracted
once; `make test` resolved into what it runs; zizmor and actionlint as detectors; the scored CI
rules read from that model.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C01** A CI model: jobs, steps, commands, triggers, permissions, pinned references, secrets
  used, images. Extracted from every CI format so one rule speaks of all of them (appendix B).
- [ ] **C04** Indirections followed: a step running `make test`, `just check`, `task lint`, `nox`,
  `tox`, `npm run test`, `./gradlew check` or `kiln check` is resolved into what it runs, so
  TESTS-IN-CI knows tests really run (a regex on the workflow today).
- [ ] **C05** PINNED-ACTIONS generalized to every CI's references: GitHub `uses:` by SHA, GitLab
  `include` refs and component versions, CircleCI orbs, Jenkins `@Library`, Buildkite plugins,
  images in `container:`, `services:` and `image:` by digest.
- [ ] **C06** Injection rules for every CI: GitHub's `${{ github.event… }}` in `run:`, GitLab's
  `$CI_COMMIT_MESSAGE` or `$CI_MERGE_REQUEST_TITLE` in `script:`, Azure's
  `$(Build.SourceVersionMessage)`, Jenkins' Groovy-interpolated `sh "…${env.CHANGE_TITLE}"`.
- [ ] **C07** Least privilege for every CI token: GitHub's `permissions:`, GitLab's job token
  allowlist, their Bitbucket and Azure counterparts.
- [ ] **C22** Reusable CI pieces (GitHub reusable workflows, GitLab components, CircleCI orbs)
  followed one level, at their pinned version, with `--online`: a reusable workflow that grants
  `write-all` is the caller's problem too.
- [ ] **D16** GitHub Actions as a kind: `action.yml` valid, a supported `runs.using`, `dist/`
  rebuilt and compared in CI, inputs documented, no `${{ inputs.x }}` inside `run:`.
- [ ] **F04** zizmor for GitHub Actions (template injection, excessive permissions, unpinned uses,
  persisted credentials, cache poisoning, dangerous triggers, impostor commits, known-vulnerable
  actions): a Rust wheel, mapped onto WORKFLOW-INJECTION, PULL-REQUEST-TARGET, PINNED-ACTIONS,
  WORKFLOW-PERMISSIONS and new rules.
- [ ] **F06** actionlint for workflow correctness (expressions, contexts, job dependencies).
- [ ] **TE02** `TESTS-IN-CI` (scored): read from the CI's commands for each component (pytest,
  Vitest, `go test`, `cargo test`, `mvn verify`), on any CI (C), through `make`, `just` and package
  scripts, not a regex for `pytest`.
