# ion-repo#T-200 · Repos safe to hand to an agent: permissions, MCP servers, plugins, hooks
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every kind of repo, every profile, AI-assisted
  development), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.14, "Repos safe to hand to an agent": What Claude Code users need first (17
October): narrow permissions, pinned MCP servers, no secret an agent can read, model calls with
limits; plugins and MCP servers scored as a kind of their own.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **D15** Claude Code plugins and MCP servers as a kind: plugin.json valid, skills named as
  their folder, hooks executable, permissions narrow, versions pinned (kiln's own `test_plugins.py`,
  offered to all).
- [ ] **AI02** `AI-CONFIDENTIALITY` (draft): Claude Code's `permissions.deny` covers `.env*`, keys
  and dumps; no real personal data in the fixtures an agent reads (PD). L1 · fix S · trial.
- [ ] **AI03** `AI-ACCOUNTABILITY` (draft): agent-written changes pass the same checks and review:
  hooks or CI enforce the rules, nothing lets an agent merge alone. L1≈ · fix J · assess.
- [ ] **AI04** `AI-FEATURES` (draft): calls to a model's API carry `max_tokens`, a timeout and a
  fallback; evaluations sit in the repo and run in CI (promptfoo, a pytest suite). L2 · fix J ·
  trial.
- [ ] **AI06** `NARROW-PERMISSIONS`: no `Bash(*)`, no `bypassPermissions` default mode, no wildcard
  web access in committed settings. L1 · fix J · adopt.
- [ ] **AI07** `MCP-PINNED`: MCP servers in `.mcp.json` pinned (`npx pkg@x.y.z`, `uvx pkg==x.y.z`,
  an image digest). L1 · fix S · adopt.
- [ ] **AI08** `MCP-NO-LITERAL-SECRETS`: `.mcp.json` passes `${VAR}` references, never tokens;
  critical. L1 · fix J · adopt.
- [ ] **AI09** `PLUGINS-VALID`: skills, agents and commands well formed (name matching the folder, a
  description, the files they cite present), as `test_plugins.py` checks for kiln. L1 · fix J ·
  adopt.
- [ ] **AI10** `HOOKS-SAFE`: hooks in committed settings exist at their paths and download nothing.
  L1 · fix J · adopt.
