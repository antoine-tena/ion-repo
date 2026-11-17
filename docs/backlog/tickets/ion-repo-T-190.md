# ion-repo#T-190 · False alarms gone: templates, fixtures, vendored and generated code left out
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every forge, CI, host and
  machine, The detection engine, Precision and recall), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.5, "A score you can trust: the false alarms of real repos, gone": Strangers' repos
hold fixtures, vendored and generated code, templates, READMEs in other languages: each class of
false alarm is handled once, in the engine, and stays fixed by a test; the reference repo's score in
every note says when the grid moved.

- [ ] **A05** Templates recognized and kept out of the repo's own stack: `copier.yml`,
  `cookiecutter.json`, `{{ }}` in paths, `.jinja`, `.j2`, `.tmpl` suffixes. kiln's `template/` stops
  making kiln a Django + Nuxt repo.
- [ ] **A06** Fixtures and test data kept out of code rules (`tests/fixtures/`, `testdata/`,
  `__snapshots__/`, `cassettes/`, `*.golden`), still read by the secret rules.
- [ ] **A07** Vendored code recognized (`vendor/`, `third_party/`, `external/`, submodules,
  `*.min.js` in static folders): scored on its own rules (pinned, known vulnerabilities, licence
  kept), never as the repo's code.
- [ ] **A08** Generated code recognized (`@generated`, `DO NOT EDIT`, Go's `Code generated … DO NOT
  EDIT.`, `*.pb.go`, `*_pb2.py`, `*.gen.ts`, OpenAPI clients, Django migrations for size rules):
  left out of style and size rules.
- [ ] **C17** Any human language in the repo: a README found as `LISEZMOI.md` or `README.zh-CN.md`;
  generic-name lists per language (`donnees`, `truc`, `datos`, `daten`); typography that isn't a bug
  (French non-breaking spaces, the doctrine's ruff example); identifiers in any script.
- [ ] **E05** Until the syntax engine lands, `regex` gets `in = "code" | "comments" | "strings" |
  "any"`, from Python's `tokenize` (stdlib) and a small JS/TS tokenizer: the false positives seen on
  kiln vanish with no new dependency.
- [ ] **E06** Path classes instead of hand-written globs: `where = ["code"]`, `["tests"]`,
  `["config"]`, `["docs"]`, `["ci"]`, `["containers"]`, from the model; generated, vendored,
  fixtures and templates left out by default.
- [ ] CI steps that hide their commands followed one level: `npm test` or `make check` read in
  `package.json`'s scripts or the Makefile, a reusable workflow of another repo read at its pinned
  ref (`--online`); until then, a step kiln can't follow leaves the rule `unknown`, never a gap
  (a JavaScript library whose `npm test` runs xo, 26 October 2026).
- [ ] **E07** A policy per rule for tests: `in_tests = "skip" | "lower" | "same"` (SQL built in a
  test is noise; a naive datetime in a test can hide a bug).
- [ ] **H08** Known false-positive classes handled once, in the engine: tests, fixtures, templates,
  examples, code blocks in docs (a README showing the bad way), `.example` files, vendored and
  generated code, migrations, documented sample keys, localhost URLs.
- [ ] **H10** Known false positives closed too: `requires-python = ">=3.9"` read as running 3.9 (a
  library's floor, not its runtime); an app with an empty `models.py`, or one under `tests/`, asked
  for migrations; a lone `.go` file in `docs/` announcing "Go: not covered".
- [ ] **H17** A regression suite of real false positives: each one reported gets a minimal repo in
  `tests/` that must pass forever.
