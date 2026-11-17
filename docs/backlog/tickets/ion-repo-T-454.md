# ion-repo#T-454 · `ion repo score --roadmap --write` writes into the backlog folder
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-17
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: ion-repo#T-453, 17 November 2026: the backlog became a folder, ion-score still
  writes the single file

`ion repo score --roadmap --write` (ion-score's `roadmap.py`, `BACKLOG = docs/backlog/backlog.md`)
refuses a repo whose backlog is a folder ("no docs/backlog/backlog.md"), and `/repo:modernize`
closes the tickets it wrote. The fix lives in ion-score, in its own session.
- [ ] ion-score writes one file per item in `docs/backlog/tickets/` and moves the index's
  `Next free` on (the format of ion-repo's `template/docs/backlog/how-to.md.jinja`), a single
  `backlog.md` still written as before.
- [ ] ion-repo's dependency on ion-score raised to that release; `docs/reference.md` and
  `.fr.md` say where `--write` puts the tickets.
