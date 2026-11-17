# ion-repo#T-273 · Docs that tell the truth: README, commands, links, docstrings, context files
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Docs and tracking, AI-assisted development), made
  a ticket on 25 October 2026 at antoine's request

Planned in v0.6.43, "Docs that tell the truth": Every path, command and link that the README and
CLAUDE.md name exists; the map lists every folder; docs that name what is gone are found.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **DT01** `README` (scored): sections that say what it is and how to install, run, test and
  deploy, commands that exist (L3); the bare file isn't enough.
- [ ] **DT02** `WORK-TRACKING` (draft): one backlog file, ordered, with a done log, or the forge's
  issues in use (L6). L0 · fix S · trial.
- [ ] **DT03** `README-COMMANDS`: commands in the README's code blocks exist (scripts, Makefile
  targets, package scripts, `manage.py` commands); `--deep` runs the install ones in a sandbox. L3 ·
  fix J · trial.
- [ ] **DT04** `LINKS-ALIVE`: links and anchors between Markdown files resolve; outside links with
  `--online` (lychee). L3 · fix S · trial.
- [ ] **DT05** `DOCS-BUILD-STRICT`: a docs site builds strictly in CI (`mkdocs build --strict`,
  Sphinx's `-W`). L1 · fix S · trial.
- [ ] **DT06** `DOCSTRINGS-PUBLIC`: public functions of libraries documented (ruff's D1, one
  convention). L4 · ratchet · trial.
- [ ] **DT07** `DOCS-NOT-STALE`: docs naming a function, option, command or file that no longer
  exists. L3 · fix J · trial.
- [ ] **DT08** `API-DOCS-SERVED`: an API with a schema serves its docs in development (Swagger UI,
  Scalar, Ninja's `/docs`). L2 · fix S · trial.
- [ ] **DT09** `MARKDOWN-LINT`: markdownlint or rumdl configured where docs are many. L1 · fix S ·
  assess.
- [ ] **DT10** `GLOSSARY`: a glossary of the domain's words, read by `DOMAIN-VOCABULARY`. L0 · fix J
  · assess.
- [ ] **AI01** `AI-CONTEXT` (scored): from "a file exists" to its quality: under a size budget, its
  map's paths existing, its commands running, nothing contradicting the settings: a script
  removed from `package.json` while CLAUDE.md still says `npm test` fails it (as `agentsgen check`
  does, seen 26 October 2026). L3.
