# ion-repo#T-192 · The score in Claude Code's session, context files under a budget
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Nothing to do, AI-assisted development), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.5.7, "Claude pays less per session": Context length is the cost (measured on 22
October): skills that run one kiln command, a ladder before writing code, context files kept under a
budget, the score shown without Claude asking for it.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **K17** Claude Code does the work: the plugin's session start shows the score in one line
  (cached), the status line shows it, the edit hook keeps it. The user only reads.
- [ ] **AI05** `CONTEXT-BUDGET`: CLAUDE.md, the rules it loads and the skills' descriptions under a
  token budget (context length is the cost, measured on 22 October 2026). L1 · ratchet · trial.
