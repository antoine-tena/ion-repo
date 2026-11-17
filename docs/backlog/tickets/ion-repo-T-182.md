# ion-repo#T-182 · `kiln status` in half a second
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: same measurement as ion-repo#T-180, 24 October 2026

`kiln status` takes 1.9 s over 10 repos:
- [ ] 0.36 s to import copier, which `status` never uses: it comes through
  `fleet → adopted → adopted_names → migrations`, which imports it at the top (so does
  `frozen.py`). Imported inside the functions that render; ion-repo#T-178's note that copier is only
  imported by the commands that need it is not true for this path.
- [ ] 0.42 s for `git ls-remote` in `versions.latest_release`, run before the local work: run it
  alongside.
- [ ] ~0.5 s of 23 git calls made one repo after the other: a thread per repo.
- [ ] `kiln update --all` and the other fleet commands get the same import fix for free.
