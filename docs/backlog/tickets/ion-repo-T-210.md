# ion-repo#T-210 · Facts per component: versions, runtimes, tools, evidence, `--facts`
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.7, "Rules per component: versions, tools, evidence": Each fact says where it comes
from and how sure it is; rules can say `django >= 4.2` or "your formatter"; a component is scored
alone.

- [ ] **A03** Workspaces group components: uv workspaces, pnpm-workspace.yaml, npm, Yarn and Bun
  workspaces, Cargo workspaces, go.work, Maven modules, Gradle settings, Nx, Turborepo, Lerna, Rush,
  Bazel's MODULE.bazel, Pants, Moon.
- [ ] **A10** Every fact carries its evidence (`django 5.2 · backend/uv.lock:412`) and a confidence
  (certain from a lock, likely from an import, possible from a file name).
- [ ] **A11** Versions in facts, from the lock first, the manifest's constraint next: rules can say
  `django >= 4.2`, `vue < 3`, `node 20`.
- [ ] **A13** Runtime versions gathered from every place that names one (.python-version,
  requires-python, .tool-versions, mise.toml, runtime.txt, .nvmrc, .node-version, engines, Volta,
  packageManager, Dockerfile FROM, CI matrices, global.json, rust-toolchain.toml, go.mod's `go` and
  `toolchain`), and their disagreements reported.
- [ ] **A14** Tools per component: which linter, formatter, type checker, test runner, bundler and
  task runner, from config files and dev dependencies; rules then speak of "your formatter",
  whichever it is.
- [ ] **A19** Facts declared as data (`facts/*.toml`: file patterns, dependency names, content
  signatures), tested like rules: a new ecosystem is a data change, not code.
- [ ] **A21** `kiln score --facts`: the model as a tree (components, roles, versions, tools,
  services) with its evidence, in JSON too. The first thing to read when a rule misapplies.
- [ ] **A22** `kiln score --why-applies RULE`: the facts that made a rule apply here.
- [ ] **A25** The repo's score aggregates its components' (weighted by code size); each component
  scorable alone (`kiln score backend/`).
- [ ] **A36** A correction exists when detection is wrong (`kiln set components.ignore=…`), is never
  needed, and each use is a signal for ion-repo#T-38.
