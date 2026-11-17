# ion-repo#T-167 · The branch guard reads the session's folder, not the command's
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: ion-repo#T-05 probe, 2026-10-21

`plugins/kiln/hooks/branch_guard.py` refused `cd <scratch repo> && git commit` on a branch of
another repo with "never commit on develop": it checks the branch of the session's folder and
ignores a leading `cd` (`git -C` got through). It should judge the repo the command runs in.

Seen again by grog (30 October 2026): three refusals over two sessions, one in a throwaway copy
on a `test/…` branch whose commit was refused with "never commit on develop".

Same family, seen on 31 October 2026 (session bc540ab5): `git checkout -b x; git commit` sent as one
command is refused on `main`, since the guard reads the branch before the command runs.
