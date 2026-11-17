# ion-repo#T-368 · Recorded demos replayed by a test: an output that changed fails until re-recorded
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-27
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: review of similar public projects, 26 October 2026
  (`BhodiSea/next-expo-supabase-agent-harness`, whose test runs its tape's commands)

Planned in v0.5.4, "The first week with strangers". `test_docs.py` already fails on a demo that
types what kiln no longer offers; it doesn't see a demo whose output changed.
- [ ] The commands of `kiln-new.tape` run in `scripts/demo_shell.sh`'s shell, their output
  compared with a text kept next to the tape; a difference fails until the GIF is re-recorded
  and the text refreshed.
- [ ] `kiln-rescue.tape`'s commands that need no network and no Claude, the same way.
