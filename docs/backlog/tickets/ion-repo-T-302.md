# ion-repo#T-302 · Profiles read from the repo: stages, criticality, team signals
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every kind of repo, every profile, Rule format v2
  and authoring), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.64, "Profiles read from the repo, never asked": Solo, association, company or
university, inferred from signals; criticality raises the bar by itself; moving up applies the new
rules as ratchets.

- [ ] **D05** Stages: prototype, growing, production, maintenance, archived. Rules grow with the
  repo ("the smallest level at creation, and rules that grow with the repo", antoine, 16 October
  2026).
- [ ] **D06** Criticality raises the bar by itself: payments, health or children's data, accounts of
  other people make the stricter profile's rules apply, and the report says why.
- [ ] **D08** Team signals: CODEOWNERS and required reviews only past two regular contributors; the
  bus factor (one person wrote 90 % of the last year) shown to organisation profiles.
- [ ] **G11** Profiles stay a membership list, never weights (decision 2): a rule outside the repo's
  profile is not applicable, so `SLO` asks nothing of a solo repo.
