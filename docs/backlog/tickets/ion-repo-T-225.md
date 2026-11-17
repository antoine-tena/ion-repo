# ion-repo#T-225 · What is on its way out: support calendars, hold rules and their converters
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Rule format v2 and authoring, Scoring model v2, A
  grid that stays current, Supply chain, CI/CD), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.18, "What is on its way out, and when it breaks": The calendar of what ends
(runtimes, frameworks, runners, model IDs), the `hold` rules that detect what is leaving, the
converters that move it.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **G13** `switch_when` made checkable (`django supports python 3.15`, from PyPI classifiers or
  endoflife data): kiln says by itself when it is time.
- [ ] **I10** `grid_version` in every report and badge; `kiln score --grid 0.4.5` re-scores with an
  older grid (bundled history) to compare like with like.
- [ ] **I22** Upcoming deadlines in the score's margin: "Node 22 reaches its end on 30 April 2027,
  in 188 days" (see `--calendar`, Q).
- [ ] **Q04** `hold` rules detect what is on its way out: Travis CI, Pipenv, Rye, `setup.py
  install`, `pytz`, `nose`, `distutils`, Python 2 idioms, TSLint, create-react-app, Vue 2, Nuxt 2,
  AngularJS, `node-sass`, `request`, `moment`, compose's `version:`, `docker-compose` v1, `apt-key`,
  `::set-output`, retired runner images.
- [ ] **Q05** A converter for each `hold` rule a script can close: `pytz` to `zoneinfo`,
  `::set-output` to `$GITHUB_OUTPUT`, compose's `version:` removed, `docker-compose` to `docker
  compose`.
- [ ] **Q13** `kiln score --calendar`: what will break and when (Node 22 ends on 30 April 2027, 188
  days from today; a runner image retired; a framework's support ending), the maintenance load the
  vision wanted to measure.
- [ ] **Q14** Rules retire too: a practice everyone now meets by default (a framework made it the
  default) leaves the score, kept as history.
- [ ] **Q15** A framework on `hold` (AngularJS, Vue 2, create-react-app…) gets the successor its
  maintainers name, with the source, never one of kiln's taste; the move sized in session hours;
  the roadmap splits it into steps the score proves (the old framework's last line first, a test
  net around the behaviour, then route by route behind the same URLs, the strangler fig), never a
  rewrite in one go; one finding in the score, never a collapse. A living framework (Django,
  Flask, Express) never goes on `hold` for being less used than another (the doctrine, 12).
- [ ] **SU05** `SUPPORTED-RUNTIMES` (scored): every runtime endoflife.date knows; an app judged on
  what it runs, a library's support floor shown as information.
- [ ] **SU19** `NO-DEPRECATED-PACKAGES`: a bundled list (`request`, `node-sass`, `tslint`, `moment`,
  `pytz`, `nose`, `six`, backports past their Python), joined with NO-OBSOLETE-BACKPORTS. L1 · fix S
  where a converter exists · adopt.
- [ ] **SU27** `SUPPORTED-FRAMEWORKS`: Django, Vue, Nuxt, Angular, Rails, Laravel, Spring Boot and
  the rest on a supported line (Vue 2 and Nuxt 2 are past their end). L1 with data · fix J · adopt.
- [ ] **SU30** `RUNTIME-NOT-LAGGING`: the runtime within its two newest supported lines, beyond "not
  past its end". L1 · fix S · trial.
- [ ] **CI13** `NO-DEPRECATED-COMMANDS`: no `::set-output` or `::save-state`; `$GITHUB_OUTPUT` and
  `$GITHUB_STATE`. L2 · fix S · adopt.
