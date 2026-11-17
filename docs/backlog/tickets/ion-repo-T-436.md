# ion-repo#T-436 · The Ion logo and its colours for the whole family
- **Type**: idea
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-11-04
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine, 4 November 2026, after the Ion logo in flight replaced the stone kiln

The banner now shows a blue-violet ion with cyan text, but the rest still speaks stone and fire
(`ion_score.ui`: STONE, FIRE, EMBER, GLOW): they clash beside the logo.
- [ ] The status line's default palette (`plugins/repo/scripts/statusline.py`, `src/ion_repo/statusline.py`).
- [ ] `ion repo doctor`, `fleet`, `release` (and the other `ui.FIRE` titles): the logo's cyan and violet, warnings and errors kept readable.
- [ ] The palette lives in ion-score's `ui`: change it there, then here.
- [ ] The logo for every Ion tool (antoine, 4 November 2026: today only ion-repo shows it; `ion host …`, `ion deal …` show nothing): move `LOGO_PIXELS` and `render_logo()` out of `src/ion_repo/banner.py` into ion-score's `ui`, beside the palette, so each tool draws it from one place; ion-repo's banner keeps only its text.
- [ ] Each tool's banner (`ion`, `ion-host`, `ion-deal`, `ion-words`…) calls it: one ticket per tool in its own backlog, opened once the piece ships in ion-score.
