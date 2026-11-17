# ion-repo#T-180 · The test suite renders each set of answers once, and copier stops asking git per file
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine, 24 October 2026: how to make kiln much faster without changing a single
  feature?

Measured that day on 16 cores: `uv run pytest -q` takes 56 s, every `kiln version cut` waits
for it, and copier's renders are 696 s of the ~900 s the workers spend (77 %). The suite renders
223 times for 164 distinct sets of answers; one render takes 1.0 s alone, 3 to 4 s under the
load of 16 workers.
- [ ] A render cache for the session, keyed by template, `vcs_ref` and answers: each set is
  rendered once, then copied into the test's `tmp_path` (the tests that edit the render keep
  their own copy). 59 renders saved, about a quarter of the render time.
- [ ] Tests that only read the default render share one, per module.
- [ ] Upstream fix in copier: `Worker._sync_git_index_executable_bit` (`copier/_main.py`, 9.18.2)
  runs `git config --type=bool --get core.fileMode` once per rendered file, 62 times per render;
  read once per worker. Measured: 1.01 s → 0.84 s per render (−17 %), which `kiln new` and
  `kiln update` gain too. A pull request to copier, then the version bumped here.
- [ ] Suite time before and after written in the merge commit.
