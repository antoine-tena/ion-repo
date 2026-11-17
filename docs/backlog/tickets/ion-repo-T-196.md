# ion-repo#T-196 · Rules that test themselves: examples in the rule file, `kiln grid new`, `test`, `lint`
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Rule format v2 and
  authoring, Precision and recall, Outputs and integrations), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.11, "Rules that test themselves": Before the grid grows by hundreds of rules: each
rule carries its examples, its rung and its message per place, and `kiln grid new`, `test`, `try`
and `lint` make a rule in minutes.

- [ ] **E01** The ladder: L0 paths and names (microseconds), L1 structured files (TOML, JSON, YAML,
  INI, XML, HCL, Dockerfile, ignore files), L2 syntax patterns, L3 cross-file (imports, calls,
  references), L4 external tools, L5 git history, L6 forge and registry APIs, L7 running the code.
  Each rule declares its rung, each finding says which one found it.
- [ ] **E22** `kiln grid` lints every pattern for catastrophic backtracking when the grid loads.
- [ ] **G01** Examples inside the rule file (`[[examples]]` with `expect` and inline files): the
  grid tests itself, packs ship tested rules, and `tests/test_grid.py` reads them instead of its
  `CASES`.
- [ ] **G02** Several examples per rule, edge cases included; every false positive ever reported
  becomes a `pass` example, so it never comes back.
- [ ] **G07** A `message` per place with placeholders (`{image} is named by tag: pin it as
  {image}@sha256:…`): the finding says what to do right there.
- [ ] **G17** `kiln grid new ID` scaffolds a rule and its examples; `kiln grid test [ID]` runs the
  examples; `kiln grid try ID --on <repo>` runs one rule with its timing.
- [ ] **G18** `kiln grid lint`: patterns that can backtrack, unknown facts, missing examples, stale
  sources, messages too long for a terminal line or for Claude's tokens.
- [ ] **G19** Rule IDs linted: uppercase, three words at most, naming the practice rather than the
  violation.
- [ ] **G21** A hash per rule (content and engine version) for cache keys and for the report's
  `grid_version`.
- [ ] **G25** A rule may carry its own small test repo folder (`rules/<theme>/<ID>/`) when inline
  examples get too big (a whole Django project).
- [ ] **H05** Examples mutated: failing variants generated from each `pass` example (the `USER` line
  removed, a SHA turned into a tag), and the detector must flip.
- [ ] **L20** Messages in English only (decided on 16 October 2026), each finding short enough for
  one terminal line.
