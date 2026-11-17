# ion-repo#T-272 · The map tells the truth: links, the repo map, entry points, decisions
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, The detection engine, Mature
  tools as detectors, Structure, Code standards, Architecture), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.43, "Docs that tell the truth": Every path, command and link that the README and
CLAUDE.md name exists; the map lists every folder; docs that name what is gone are found.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B20** Markup and assets: Markdown (markdownlint's rules, links), YAML (yamllint), TOML
  (taplo), CSS (stylelint), HTML, SVG (no script inside), images (weight, format), fonts (subset,
  self-hosted).
- [ ] **E27** Docs checked against the tree: every path, command and make target quoted in the
  README and CLAUDE.md exists (REPO-MAP-FRESH, README-COMMANDS-EXIST). A map that lies costs Claude
  more than no map.
- [ ] **F16** lychee for links: relative links and anchors offline, external ones with `--online`,
  cached.
- [ ] **ST02** `REPO-MAP` (scored, "to confirm" today): judged by REPO-MAP-FRESH below, so it stops
  being approximate. L1 · fix J.
- [ ] **ST03** `REPO-MAP-FRESH`: every path the root CLAUDE.md's map names exists, and every
  top-level folder appears in it. L1 · fix J · adopt.
- [ ] **ST22** `ENTRY-POINTS-NAMED`: an app's entry points (`manage.py`, `main.py`,
  `server/index.ts`) where a reader expects them, and named in the map. L0≈ · fix J · assess.
- [ ] **CS14** `DOMAIN-VOCABULARY` (draft): the glossary's words used (a `docs/glossary.md` checked
  against identifiers). L2≈ · fix J · assess.
- [ ] **AR10** `ADR`: decisions recorded (`docs/adr/` or `docs/decisions/`), for company profiles.
  L0 · fix S (folder and template) · assess.
- [ ] **AR11** `ARCHITECTURE-DIAGRAM`: a diagram as code (Mermaid, Structurizr) for repos with
  several services. L1 · fix J · assess.
