# ion-repo#T-357 · Every agent, or none: the instructions laid for the agent the person uses
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q22: "anyone using an AI should be able to use
  it, even without AI: ask at install which AI CLI, CLAUDE.md for Claude, otherwise AGENTS.md";
  Q72: "yes, with everything"; Q83), decision 26

Being tied to one agent is how kiln could be made useless by an agent's next release (Q190).
AGENTS.md is read by most agents; Claude Code reads CLAUDE.md, which can import it.
- [ ] `kiln install` asks once which agent the person uses (Claude Code, Codex, Cursor, Gemini CLI,
  Copilot, several, none); `kiln new` and `kiln adopt` lay `AGENTS.md` with the rules, and a short
  `CLAUDE.md` that imports it for Claude Code users.
- [ ] What only Claude Code has (skills, hooks, the status line) stays in its plugins; the
  others get the same rules as text.
- [ ] Without an agent: `kiln score`, `kiln fix` and the roadmap written for a person (the
  checklist of ion-repo#T-129 in plain words).
