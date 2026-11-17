# ion-repo#T-417 · One file for the stack's versions, checked in pre-commit and CI
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `annski/scripts/ci/check_versions.py`

annski writes every version of its stack (Python, Node, PostgreSQL, Redis, images) in
`annski/docs/exploitation/versions.md`, and `annski/scripts/ci/check_versions.py` fails when a
Containerfile, the compose files, CI or `engines` drift from it. A charter check of the same kind
for every generated repo. Score side: ion-repo#T-210.
