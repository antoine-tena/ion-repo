# ion-repo#T-213 · Mature tools as detectors: ruff and shellcheck, pinned and deduplicated
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, The detection engine, Mature
  tools as detectors), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.10, "Mature tools as detectors": ruff, shellcheck and their kin mapped onto grid
rules, pinned and cached, never downloaded without asking; the faster checkers measured against the
ones they would replace.

- [ ] **B15** Shell and PowerShell as real code: shellcheck, shfmt, `set -euo pipefail`, bats;
  PSScriptAnalyzer and Pester.
- [ ] **E02** The default run is L0 to L3 plus the L4 tools shipped as wheels: offline, nothing of
  the repo executed. `--online` adds L6, `--history` L5, `--deep` L7 in a sandbox.
- [ ] **F01** A `tool` detector kind: run a tool with machine output (JSON, SARIF), map each result
  to a rule and a place. The tool comes from the repo's environment, PATH or kiln's bundle; it is
  never downloaded without `--online`.
- [ ] **F02** ruff as the Python engine wherever it has the rule: DTZ (naive datetimes), E722 (bare
  except), PGH003 and PGH004 (blanket ignores), S608 (SQL by strings), S602 to S607 (shell), S301
  and S506 (unsafe loads), S113 (no timeout), B006 (mutable defaults), T20 (print), C901, PLR2004
  (magic values), UP (modern Python at the `requires-python` target), DJ, ASYNC, PTH, ERA. Exact,
  string-aware, and its safe fixes become free converters.
- [ ] **F03** kiln's reference ruff selection run even on repos without a ruff config (isolated,
  kiln's own config), beside the repo's: "your linter says" and "the grid says" kept apart.
- [ ] **F05** shellcheck (the `shellcheck-py` wheel) on shell scripts and on the `run:` blocks of
  workflows.
- [ ] **F21** Every tool pinned by version and hash, its output cached by the hash of its inputs; a
  tool update is a grid change and its precision is measured again.
- [ ] **F22** Several tools on one line deduplicated: ruff's S608 and another tool on the same SQL
  string make one finding with both as evidence.
- [ ] **F23** A missing tool never fails a rule: "unknown: install kiln's tools extra, or run with
  `--deep`".
- [ ] **F24** A `kiln-cli[tools]` extra bringing the tools that ship as wheels in one install.
