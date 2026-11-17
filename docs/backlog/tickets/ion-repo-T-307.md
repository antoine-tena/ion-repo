# ion-repo#T-307 · The charter and the grid, one engine
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Rule format v2 and authoring, One measure drives
  every command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.7.3, "The charter and the grid, one engine": Decision 4, before the format freezes:
shared detectors first, then the charter as the grid's rules in strict or ratchet regime, its IDs
kept as aliases; rule files checked by a published schema. ⚠ breaking: `charter.toml` lists grid
rule IDs with their regime, converted by `kiln update`.

- [ ] **G09** `related`, `supersedes` and `aliases`: old IDs answered forever, the stable-ID promise
  of v1.0.
- [ ] **G16** A published JSON Schema for rule files: editors check a rule as it is typed (taplo, VS
  Code).
- [ ] **P11** The charter and the grid as one engine (decision 4): shared detectors first, a test
  that makes a rule and its charter twin agree on the examples; at v1.0.0 a rule written once in the
  grid, `charter.toml` listing rule IDs with their regime and budget, the charter's IDs kept as
  aliases.
