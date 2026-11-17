# ion-repo#T-366 · The session's place kept before compaction, a pause offered near the usage limit
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-27
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: review of similar public projects, 26 October 2026 (`tillmeier/claude-code-guardrails`'s
  compaction handoff, `asiagenawi/claude-powernap`, `wrg32786/aigent-os`)

Planned in v0.6.0, "Claude closes the gaps alone": an unattended run has to outlive a compaction
and the 5-hour window. `kiln pause` only runs when someone asks for it.
- [ ] A `PreCompact` hook writes what `kiln pause` keeps (branch, ticket, where it stopped, next
  step) and `SessionStart` with the `compact` matcher hands it back to Claude.
- [ ] Near the end of the usage window (about 90 %, or sooner when the burn rate projects the
  limit within minutes, read from what the status line already knows), Claude is told to finish
  its step and run `kiln pause`.
- [ ] Measured before shipping: the work kept across a compaction, with and without the hook, on
  one real session.
