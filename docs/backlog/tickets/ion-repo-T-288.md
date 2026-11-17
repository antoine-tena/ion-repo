# ion-repo#T-288 · Never a crash, whatever the repo
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, The detection engine,
  Precision and recall, Trust, privacy and safety), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.54, "Never a crash, whatever the repo": Static by default, hardened parsers,
linear-time regexes, fuzzed trees, symlinks, untracked and ignored files handled; zero crashes on
the corpus at each candidate.

- [ ] **A27** Outside git, `.gitignore` parsed anyway: `build/`, `target/` and `.venv` stay out
  (only a fixed list is skipped today).
- [ ] **A28** Untracked files scored but marked "untracked": a local `.env` that isn't ignored is a
  real risk, a local experiment isn't the repo.
- [ ] **A32** Symlinks never followed out of the repo, loops cut, case-insensitive file systems
  (macOS, Windows) normalized.
- [ ] **E21** Linear-time regexes (google-re2, or Rust's `regex` through the syntax engine) and a
  time budget per rule: one bad pattern can't hang a run.
- [ ] **E32** Never read `.git/`, virtualenvs or `node_modules` as code, even when they're tracked
  by mistake (that's its own finding).
- [ ] **H06** Property tests (Hypothesis) on every parser (Dockerfile, workflows, compose,
  settings): random input never crashes, and the outcome is deterministic.
- [ ] **H07** A fuzzed tree: deep nesting, Unicode and spaces in paths, symlink loops, empty files,
  100 MB files, invalid UTF-8, CRLF, BOM, case collisions.
- [ ] **H15** A crash budget of zero on the whole corpus at every candidate; a rule that crashes is
  reported with a minimal anonymized tree for `/kiln:report`.
- [ ] **S01** Static by default: no code of the scored repo ever runs (no setup.py, no
  `eslint.config.js`, no `conftest.py`). Scoring an untrusted repo is safe, which the study needs at
  scale.
- [ ] **S02** Hardened parsers: YAML alias bombs, deep nesting, huge JSON, path traversal through
  symlinks, linear-time regexes; limits on file size, file count, time and memory.
