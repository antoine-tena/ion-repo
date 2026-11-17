# ion-repo#T-209 · One model of the repo: components, roles, one answer for every command
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, One measure drives every
  command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.6, "One answer to "what is this repo"": Score, fix, adopt, dev and check read one
model: components with their roles, so a Django rule never reads `frontend/` and one helper script
doesn't make a repo Python.

- [ ] **A01** One module answers "what is this repo" (`kiln.repo`), replacing `grid/facts.py`,
  `stack.py:detect_stack` and `grid/fix.py:check_commands`; score, fix, adopt, dev, check and update
  all read it.
- [ ] **A02** Components: every folder holding a manifest is one (pyproject.toml, package.json,
  go.mod, Cargo.toml, pom.xml, build.gradle(.kts), *.csproj, composer.json, Gemfile, mix.exs,
  pubspec.yaml, Package.swift, CMakeLists.txt, meson.build, DESCRIPTION, Project.toml, deno.json,
  flake.nix, Chart.yaml, a folder of *.tf), nested under its parent.
- [ ] **A04** A role per component, inferred: backend, frontend, library, CLI, worker, infra, docs,
  mobile, desktop, extension, data/ML, tests, template, fixture, vendored, generated, example. Each
  role turns groups of rules on or off.
- [ ] **A09** `.gitattributes` honoured: `linguist-vendored`, `linguist-generated`,
  `linguist-documentation`, `export-ignore`, conventions many repos already set for GitHub.
- [ ] **A20** A share threshold for languages: one helper script in Python doesn't make a JavaScript
  repo a Python repo (today one `.py` file turns every Python rule on).
- [ ] **A24** Findings per component, paths still relative to the repo: a Django rule never reads
  `frontend/`.
- [ ] **A37** `kiln dev` and `kiln check` read the model: ion-repo#T-159's "checks found beyond the root"
  falls out of it.
- [ ] **P12** `kiln dev`, `kiln doctor` and `kiln check` read the repo model (A).
