# ion-repo#T-178 · A lighter install: copier's dependencies trimmed, not fetched later
- **Type**: idea
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine, 24 October 2026: should kiln download its packages bit by bit to stay light?

Measured that day: the installed tool weighs 26 MB, kiln itself 1.4 MB; the rest comes from
copier (pygments 5 MB, pydantic-core 5 MB, wcwidth 3.5 MB, yaml 2.8 MB, prompt_toolkit…).
`kiln --version` answers in 0.2 s, copier is imported only by the commands that need it, and
the heavy pieces (Playwright's Chromium, serena, context7, each stack's toolchain) are already
fetched on first use. Lazy-downloading copier was ruled out: a `kiln new` or `kiln update` that
fails offline, versions no longer pinned by one `uv tool install`, a slower first command.
- [ ] See which of copier's dependencies kiln's paths actually load (`-X importtime` on
  `kiln new`, `kiln update`), and whether any can be dropped or made optional upstream.
- [ ] Only worth doing if the gain is real (several MB or a visible install time); otherwise
  close it as measured.
