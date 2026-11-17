# ion-repo#T-244 · Sizes and names measured: files, functions, complexity, naming
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.30, "Sizes and names, measured in any language": A metrics pass for every language
feeds the size and complexity ratchets; names, cases and misspellings judged from symbol tables.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS01** `FILE-SIZE` (draft): lines per file from the index, generated code and migrations
  aside, a ratchet from today's numbers. L0 · ratchet · trial.
- [ ] **CS02** `FUNCTION-SIZE` (draft): function length from syntax trees in any language (ruff's
  PLR0915 for Python). L2 · ratchet · trial.
- [ ] **CS03** `CASE` (draft): symbols cased as their language wants (pep8-naming through ruff's N8,
  typescript-eslint's naming convention), from symbol tables. L2 · fix J · trial.
- [ ] **CS04** `BOOLEANS` (draft): names of `bool`-typed values start with is, has, can or should
  (Python annotations, TS types). L2 · fix J · assess.
- [ ] **CS05** `GENERIC-NAMES` (draft): identifiers from a deny-list (`data`, `res`, `tmp`, `obj`,
  `val`, `info`, `item`, `stuff`, `foo`), one list per human language. L2≈ · fix J · trial.
- [ ] **CS08** `ONE-CLASS` (draft): one public class per file in Python and TS. L2 · fix J · assess.
- [ ] **CS28** `COMPLEXITY`: cognitive complexity under about 15 per function. L2 · ratchet · trial.
- [ ] **CS30** `NESTING-DEPTH`: four levels of nesting at most. L2 · ratchet · trial.
- [ ] **CS33** `NAMES-WITH-UNITS`: durations, sizes and amounts named with their unit
  (`timeout_seconds`, `size_bytes`). L2≈ · fix J · assess.
- [ ] **CS34** `FILE-NAMES-CASE`: file names in the language's convention (snake_case.py,
  PascalCase.vue components, kebab-case routes). L0 · fix J · trial.
- [ ] **CS45** `TYPOS`: no common misspelling in identifiers and comments (the typos dictionary). L4
  · fix S · trial.
