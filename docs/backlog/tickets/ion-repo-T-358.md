# ion-repo#T-358 · The generated flow follows the evidence: trunk-based, pull requests for teams
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q67: "kiln's skills must match the best way of
  working in the world: not MY way, THE way"; Q169), decision 25

DORA's research ties trunk-based development (short branches merged within a day) to delivery
performance, and git-flow's author advises a simpler flow for software delivered continuously,
which a web app is. The generated repos follow antoine's flow today (`develop`, `main`,
`release/**`, merges without pull requests, CI at the release only).
- [ ] New repos: one long-lived branch (`main`), short branches, releases as tags after the whole
  CI; for team profiles (ion-repo#T-39), a pull request and its CI before each merge.
- [ ] Repos of the old flow keep it until they choose; the conversion offered by `kiln update`.
- [ ] kiln's own repo keeps `develop` and `main` while its channels hang on them (ion-repo#T-356).
