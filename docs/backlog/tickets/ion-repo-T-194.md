# ion-repo#T-194 · Updates that announce their rules and show the score before and after
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, Nothing to do, One measure
  drives every command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.9, "Updates you take without reading them": Asked at your pace, applied in one step,
proven on real upgrade paths, the score before and after shown, Claude told what changed in its
rules.

- [ ] **I11** New `adopt` rules announced one release ahead ("counts from v0.5.7: you meet it", or
  "you will lose 2 points: `kiln fix` closes it"): no score drops overnight.
- [ ] **K16** Offline on a plane: all but `--online` works; the data's date shown, with "12 new
  rules since your version" when the tool is old (`tool_update.py`).
- [ ] **P08** `kiln update` shows the score before and after, and the grid changes that touch this
  repo; a lower score stops the update unless the grid explains it.
