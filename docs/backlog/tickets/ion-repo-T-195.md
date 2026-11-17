# ion-repo#T-195 · Fixes that close and stay closed: `kiln score --fix`, a fix block per rule
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Rule format v2 and
  authoring, Nothing to do, One measure drives every command), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.10, "`kiln fix`: more gaps closed, faster, from scripts": The code's own rules get
converters, the checks run once with a bisection on red, the options kiln-bot and the skills need; a
fresh `kiln new` repo leaves `kiln fix` nothing to do.

- [ ] **F25** The tool that detected becomes the tool that keeps it closed: `kiln fix` adds its
  config and its CI step when missing (ruff, zizmor, pre-commit).
- [ ] **G08** A `fix` block: a converter, a ruff code, or a written recipe for Claude; `safety =
  "safe" | "unsafe"` as ruff marks its fixes.
- [ ] **K12** `kiln score --fix`: score, fix, score again, in one go.
- [ ] **P02** `kiln fix` on a fresh `kiln new` repo changes nothing; when it does, the template is
  behind the grid.
