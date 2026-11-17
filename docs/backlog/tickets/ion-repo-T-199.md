# ion-repo#T-199 · Three new themes open: licensing, infrastructure, data science
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Git and versions, Licensing, Infrastructure as
  code, Data science), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.13, "The grid grows: the exact rules first, three new themes": ion-repo#T-141 opens here, its
other boxes being the theme releases below: the rules a detector decides exactly today, the first
rule of `licensing`, `infrastructure` and `data-science`, and the template held to every new rule by
its own test.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **GV13** `NO-CONFLICT-MARKERS`: no `<<<<<<<`, `=======` or `>>>>>>>` line in tracked text,
  docs that teach git aside. L2 · fix J · adopt.
- [ ] **LI01** `LICENSE-FILE`: a licence file whose text matches an SPDX licence (matched as
  licensee does), or "all rights reserved" stated for private work. L1 · fix J · adopt (open
  source).
- [ ] **IN02** `TF-REMOTE-STATE`: no `*.tfstate` committed (state holds secrets), a remote backend
  declared; critical when state is tracked. L0 · fix J · adopt.
- [ ] **DS01** `MODEL-TRACED` (trial, v0.4.6): moves here from data-migrations; promoted once its
  precision is measured on data repos.
