# ion-repo#T-371 · `/kiln:token`: a paste prompt in kiln's own style
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-29
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: the user, 2026-10-29, after pasting a Cloudflare secret through `wrangler secret
  put` in emberstudio

Today `/kiln:token` hands the user a bare `read -rs -p "<Service> token: " … && echo " ok"`:
nothing shows while pasting, no sign the paste was taken, a flat "ok" at the end. Wrangler's
prompt felt far better: a clear question, a mask once the secret is in, a success line that
names what was saved. The user wants that quality, **without emojis**, in kiln's look: the
stone and fire palette and the marks of `src/kiln/ui.py` (`◆` FIRE for the step, `✓` MOSS for
success, `✗` EMBER for failure, bold titles, dim notes; bare text outside a terminal).

- [ ] A `kiln token <service>` command (or `kiln secret`) that asks for the secret hidden,
  shows a mask (e.g. `••••••` and its length) once pasted, writes `.<service>/token` chmod 600,
  adds `.<service>/` to `.git/info/exclude`, and ends with `✓ Token saved in .<service>/token`.
- [ ] Refuses an empty paste and one with a trailing newline or spaces (trimmed, said so).
- [ ] Works from the user's own terminal, never through Claude Code's `!` (stdin is not a tty):
  says so plainly when stdin is not a terminal.
- [ ] `/kiln:token` gives that command instead of the `read -rs` line.
- [ ] Optional: `--to <command>` pipes the secret into another tool's stdin (`wrangler secret
  put NAME`, `gh secret set NAME`) without writing it to disk.
- [ ] `--generate [LENGTH]`: a secret the app needs (an access code, a signing key) made on the
  machine, stored in `.<service>/`, pushed with `--to`, never shown to Claude. Seen 2026-11-02 on a
  site: a code made by hand with `openssl` + `wrangler secret put`, the user lost, then asking
  "can't you store the code as a token like `.cloudflare`?" (`/learn:distill` of that day).
