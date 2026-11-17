# ion-repo#T-168 · A repo from `kiln new` + `gh repo create --push` has no CI workflow on GitHub
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: ion-repo#T-05 probe, 2026-10-21

After the first push, `ci.yml` was not registered (dispatch answered 404 for minutes); a second
commit touching the file registered it. Reproduce with `kiln publish`, then find out whether it
is GitHub's or kiln's doing.
