# ion-repo#T-153 · `statusline.ci locale`: a French value left in generated repos
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: the README's recorded demo (20 October 2026) shows `git config statusline.ci locale`

kiln moved to English in 0.4.0, but `apply_statusline_settings` (`src/kiln/statusline.py`) still
writes `locale` for a CI run on the machine, read by the status line script, the session start
hook and `/kiln:merge`. Write `local`, keep reading `locale` (hooks and status line are read from
the main tree by open sessions), convert existing repos in `kiln update`.
