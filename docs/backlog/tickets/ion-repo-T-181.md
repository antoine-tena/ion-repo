# ion-repo#T-181 · The session start does not wait for GitHub
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: same measurement as ion-repo#T-180, 24 October 2026

`plugins/kiln/hooks/session_start.py` takes 1.3 s at every session start, almost all of it in
one network call, `gh run list --branch develop --limit 20` (1.5 s, the red CI check), made in
sequence. Off the `beta` channel, `git ls-remote` of the update check comes on top of it.
- [ ] The CI verdict read from a cache refreshed in the background (as the status line already
  does with `Popen`), with a short lifetime; the first session of the day may say nothing.
- [ ] Otherwise, at least the network calls run at the same time, not one after the other.
- [ ] Same messages, same cases: `tests/test_session_start.py` unchanged.
