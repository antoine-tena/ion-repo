# ion-repo#T-407 · `ion repo check` is red on ion-repo itself: no `charter.toml`
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: ion-repo#T-393's branch, reproduced on a clean copy of develop (358244a)

In ion-repo's own tree, `ion repo check` (and `--all`) runs the charter step alone, which stops on
"charter: no charter.toml at the root of the repo": no ruff, mypy nor pytest run, the verdict is
red whatever the change. Either ion-repo gets a `charter.toml` of its own (and meets it), or
`check` knows ion-repo's stack (ruff, mypy, pytest) and skips a charter the repo does not declare,
saying so.
