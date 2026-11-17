# ion-repo#T-201 · Apps that call a model: keys server-side, current models, validated outputs
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (AI-assisted development), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.5.14, "Repos safe to hand to an agent": What Claude Code users need first (17
October): narrow permissions, pinned MCP servers, no secret an agent can read, model calls with
limits; plugins and MCP servers scored as a kind of their own.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AI11** `AGENTS-MD-POINTER`: where a team uses other agents, `AGENTS.md` points to CLAUDE.md
  rather than holding a second truth. L0 · fix S · assess.
- [ ] **AI12** `LLM-KEYS-SERVER-SIDE`: no model provider's key reachable from front code or a public
  env prefix; critical. L2 · fix J · adopt.
- [ ] **AI13** `LLM-MODELS-CURRENT`: model IDs not retired, from a bundled calendar like the
  runtimes'. L2 · fix S · trial.
- [ ] **AI14** `LLM-OUTPUT-VALIDATED`: structured outputs parsed by a schema (tool use, JSON schema)
  before use. L2≈ · fix J · trial.
- [ ] **AI15** `PROMPTS-AS-FILES`: prompts versioned as files, reviewable, not scattered strings.
  L2≈ · fix J · assess.
- [ ] **AI16** `TOOLS-LEAST-PRIVILEGE`: an agent fed untrusted content gets read-only tools, its
  input delimited. L2≈ · fix J · assess.
- [ ] **AI18** `PROMPT-CACHING`: long static system prompts marked for caching (`cache_control` on
  Anthropic's API). L2 · fix S · assess.
