# ion-repo#T-243 · A metrics pass and misspellings, in any language
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Mature tools as detectors),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.30, "Sizes and names, measured in any language": A metrics pass for every language
feeds the size and complexity ratchets; names, cases and misspellings judged from symbol tables.

- [ ] **E13** A metrics pass: lines and logical lines per file and function, cyclomatic and
  cognitive complexity, nesting, parameters, token duplication, comment density, TODOs, for any
  language (lizard's approach), feeding the size and complexity ratchets.
- [ ] **F15** typos (Rust) for misspellings in identifiers and comments, with very few false
  positives.
