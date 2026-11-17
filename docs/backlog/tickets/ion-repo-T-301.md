# ion-repo#T-301 · GitLab too: its CI, its forge, its reports
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Outputs and
  integrations, History, forge and registries, CI/CD), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.63, "GitLab too": Universities and companies often run GitLab: its CI read like
GitHub's, its settings through `glab`, its merge request widget fed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C02** GitLab CI: `.gitlab-ci.yml`, `include:` (project, remote, template, component with a
  version), `rules:`, `needs:`, the job token's scope, protected and masked variables.
- [ ] **C09** Forges: GitHub, GitLab (cloud and self-managed), Bitbucket, Azure DevOps, Gitea,
  Forgejo, Codeberg, SourceHut, Gerrit; read from the remote's URL, their folders (`.github/`,
  `.gitlab/`, `.gitea/`, `.forgejo/`, `.azuredevops/`) and conventions (where CODEOWNERS and
  templates live) known.
- [ ] **C21** Self-hosted forges on custom domains recognized by their API's signature (GitLab's
  `/api/v4/version`, Gitea's `/api/v1/version`), with `--online` only.
- [ ] **L03** GitLab: the Code Quality report (merge request widget) and the SAST report format for
  security rules.
- [ ] **M21** GitLab: protected branches and tags, merge request approvals, push rules, secret
  detection, protected and masked variables, the job token's scope.
- [ ] **CI26** `GITLAB-PIPELINE-HYGIENE`: `interruptible`, `timeout`, `rules:` rather than `only`
  and `except`, includes pinned to a commit, protected variables. L1 · fix S · adopt (GitLab).
