# ion-repo#T-399 · The names ion-repo still keeps from kiln
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-31
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln became ion-repo (31 October 2026); the rename moved the command, the package,
  the plugin, the template's rules, skills, variables and plugin ids, and kept these on purpose

Still named after kiln, each read where it is today: the machine's storage
(`~/.config/kiln/config.toml`, `~/.local/state/kiln/`, `~/.cache/kiln/`), the git config keys
(`kiln.update-check`, `kiln.branch-guard`, `kiln.rtk`, `kiln.report-gaps`), the CI's git note
(`kiln ci: success`), `kiln-waivers.toml` in every repo, kiln-bot (its workflow `kiln-bot.yml`,
its branch `kiln/bot`, `KILN_BOT_TOKEN`), kiln's own CI `kiln.yml`, the images
`docs/assets/kiln-*` and the two recorded demos, which type `kiln` (the alias). Each moves with a
fallback read of the old name, and `ion repo update` converts what a repo carries; the demos are
re-recorded at the next candidate that shows them.
Also `src/kiln/`, the `kiln` alias of `ion-repo` and `kiln_move.py`'s state in `~/.local/state/kiln/`.
- [x] `~/.config/kiln/config.toml` → `~/.config/ion-repo/config.toml`, moved at the first read,
  the old place read by the status line and the hooks until then (2026-11-03).
- [x] `~/.local/state/kiln/` → `~/.local/state/ion-repo/`, merged in at the first session start or
  command, what both hold kept in the new place (2026-11-03).
- [x] `~/.cache/kiln/{ci,update-all,chrome-wsl}` → `~/.cache/ion-repo/`, the local CI's orphan
  worktrees under the old place still removed (2026-11-03).
- [x] git keys `ion-repo.update-check`, `ion-repo.branch-guard`, `ion-repo.rtk`, kiln's still read
  (2026-11-03).
- [x] ion-score first: `WAIVERS_FILE` (`kiln-waivers.toml`, read under both names), `kiln.report-gaps`,
  `~/.cache/kiln/{worktrees,forge}`, `.git/kiln/fix` (ion-score 0.1.2); then `ion repo update`
  renames the file (breaking: the generated tree) (2026-11-03).
