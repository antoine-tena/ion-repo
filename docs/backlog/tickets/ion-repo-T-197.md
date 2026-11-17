# ion-repo#T-197 · Findings in the pull request: locations, fingerprints, annotations, summaries
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Nothing to do, Outputs and
  integrations, Trust, privacy and safety), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.12, "Findings where people look": With rules that test themselves (v0.5.11) to build
on: in the pull request, the CI's summary and GitHub's code scanning, written without a flag;
repo-local rules in the grid's format.

- [ ] **E23** Locations with line, column and end (SARIF regions), with a snippet, redacted for
  secrets.
- [ ] **E24** A fingerprint per finding (rule, path, normalized snippet, like SARIF's
  `partialFingerprints`): a finding keeps its identity when lines move, so waivers and baselines
  survive edits.
- [ ] **K08** CI detected (`GITHUB_ACTIONS`, `GITLAB_CI`, `CI`): annotations, SARIF and a job
  summary written without a flag, colours off outside a terminal (ion-repo#T-116).
- [ ] **K18** Nothing written in the repo by default (as today); `--output` writes a report when
  asked.
- [ ] **L05** A Markdown summary for pull request comments and `$GITHUB_STEP_SUMMARY`.
- [ ] **L10** GitHub check runs with annotations, sent in batches of 50.
- [ ] **S03** Secrets never printed: snippets redacted (`ghp_****abcd`) in every output (terminal,
  JSON, SARIF, HTML, comments).
