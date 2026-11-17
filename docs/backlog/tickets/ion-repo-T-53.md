# ion-repo#T-53 · Readable by Claude, measured: the A/B test
- **Type**: idea
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 (vision, validation
  step 2: the small-files hypothesis is not proven)

The third pillar rests on a hypothesis: many small, well-named files save tokens. A simple model
favours 15 files of 100 lines over 5 of 300 or 100 of 15; the only measurement found (Sonar,
660 runs with Claude Code) gives 7 to 8 % fewer tokens for clean code; no study compares the
layouts directly.
- [ ] Ten identical tasks on one feature of a local copy of the reference repo, split into small
  files and left as it is, run headless (`claude -p`), three runs each: tokens, turns, files
  read, success.
- [ ] Its cost on the Pro quota said before it runs (about sixty runs: a few session-hours),
  stopped at the budget.
- [ ] The result published either way; the readability rules of the grid follow it (a rule the
  measurement does not support goes back to `assess`).
