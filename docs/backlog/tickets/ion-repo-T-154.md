# ion-repo#T-154 · Show your score: a badge other repos display
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: README study, 20 October 2026; after ion-repo#T-46

The image that travels by itself: GitHub's code search finds the Ruff badge in about 7,800
READMEs, OpenSSF Scorecard's in about 25,000, github-readme-stats cards in about 247,000. A score
is a badge that measures something, the kind a study of 294,941 npm packages found reliable and
lasting (Trockman et al., ICSE 2018), whose authors ask for badges of "conformance to coding
standards".
- [ ] `kiln score --badge`: the Markdown of a shields.io endpoint badge, its JSON kept up to date
  by kiln-bot (ion-repo#T-59) or the CI.
- [ ] A "Show your score" section in the README, as Ruff has; kiln's own badge on top (ion-repo#T-90).
- [ ] The `kiln score` output made to be screenshotted: the score large, the kiln, 80 columns.

From the kiln score ideas of 24 October 2026:
- [ ] **L07** A live badge: kiln-bot publishes a shields.io endpoint JSON (Pages or a gist) instead
  of a number frozen in the README (ion-repo#T-154).
