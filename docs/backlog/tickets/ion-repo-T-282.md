# ion-repo#T-282 · The forge's settings read: tokens, secrets, alerts, environments, required checks
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (History, forge and registries, Application
  security, Tests, Operations, CI/CD), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.49, "The forge's settings, read": Through the `gh` already logged in: token
permissions, secrets' ages, environments, required checks, alerts left open, update pull requests
ignored.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **M18** GitHub: the default `GITHUB_TOKEN` read-only, "Actions can create pull requests" off,
  allowed actions limited, approval for first-time contributors' workflows, environments with
  reviewers for deploys.
- [ ] **M19** GitHub: secret names and ages (the API gives `updated_at`): unused secrets, secrets
  older than a year (SECRET-ROTATION becomes detectable), long-lived cloud keys where OIDC would do.
- [ ] **M20** GitHub: deploy keys read-only, webhooks with a secret and TLS checking, immutable
  releases, tag rulesets.
- [ ] **M23** Open alerts by age: critical Dependabot or code-scanning alerts open for more than 30
  days.
- [ ] **M24** Update pull requests left open (Dependabot, Renovate) for more than a few weeks: the
  bot is set but ignored, the real gap behind DEPENDENCY-UPDATES.
- [ ] **AS12** `SECRET-ROTATION` (draft): forge secrets older than a year (M). L6 · fix J · trial.
- [ ] **TE29** `TEST-DURATION`: suite time and slowest tests read from the CI's JUnit reports with
  `--online`, as a ratchet. L6 · ratchet · assess.
- [ ] **OP10** `PROTECTED-ENVIRONMENTS`: production jobs run in a forge environment with reviewers
  or branch rules (L6, ion-repo#T-158). L6 · fix J · trial.
- [ ] **CI06** `FAST-CI` (draft): median duration and runs that passed on retry read from the forge
  (L6); caches and concurrency as the static part. L6 · fix J · trial.
- [ ] **CI16** `NO-SELF-HOSTED-ON-PUBLIC`: no self-hosted runner reachable from a public repo's pull
  requests; critical. L1 + L6 · fix J · adopt.
- [ ] **CI21** `REQUIRED-CHECKS`: the integration branch requires the CI's checks (L6, ion-repo#T-158). L6 ·
  fix J · trial.
