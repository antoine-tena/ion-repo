# ion-repo#T-402 · A test against the half-renamed forms in the template
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-31
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: session bc540ab5 (kiln becomes ion-repo), 2026-10-31, by /learn:distill

The bulk rename of kiln left `/ion-repo:…`, `.claude/ion-repo` and `ion-repo 0.3` in the template
and the plugin; no test saw them, the first real `ion repo update` did.
- [ ] `test_template.py` refuses, in a render and in `plugins/`: a skill under the catalog's name
  (`/ion-repo:`), a plugin id `ion-repo@ion-repo`, a version of ion-repo below the rename.
- [ ] After any bulk replacement, the same kind of check: what the replacement must never produce.
