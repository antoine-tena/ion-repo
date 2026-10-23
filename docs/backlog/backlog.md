# Backlog

Everything left to do on kiln, in a single list ordered by priority. Started on
**2026-10-15**, rewritten on **2026-10-17** from the vision of that day (`docs/vision/`;
the measures of the two real repos stay private, see "Repos d'entraînement" in `CLAUDE.md`). Closed tickets are in
[done.md](done.md), what was turned down in [rejected.md](rejected.md); how to write a ticket:
[README.md](README.md). **Nothing else is open.**

North star: **kiln v0.5.0, launched publicly on Wednesday 11 November 2026: any Django or Nuxt
repo scored in seconds against a sourced grid of today's best practices, brought up to it by
script, the rest handed to Claude Code as a short list** (vision of 17 October 2026: "kiln
keeps a repo up to date with the best of the world, and easy for Claude to read").

**Next free: T-166.**

---

## 🚀 Releases

A candidate every two days, about 4 of its 7 session-hours planned, the rest margin. v0.4.0 to
v0.4.4 went out a week ahead of the first plan (v0.4.4 promoted on Wed 21 Oct instead of a
candidate on Wed 28 Oct): the week won goes to the releases below, and v0.5.0 keeps its date.
The launch date is fixed (T-03); the version it waits for is v0.5.0.

### Shipped: v0.4.0 to v0.4.4
- v0.4.0 · kiln speaks English: promoted on Mon 19 Oct, the milestone decided by antoine
  (⚠ breaking, all converted by `kiln update`).
- v0.4.1 · The grid, as data: `kiln grid`, 105 drafts from the reference repo.
- v0.4.2 · Any repo scored against the best, in seconds: T-125, T-46, T-157.
- v0.4.3 · What a script can fix, fixed by script: T-126, T-127, T-128.
- v0.4.4 · The rest handed to Claude: T-129, T-161, and most of T-130 (the template's gaps
  closed), promoted on Wed 21 Oct. T-130's proof and T-90 slipped to v0.4.5.

### v0.4.5 · kiln and its repos at 100 on their own grid
Candidate Fri 23 Oct. A tool that grades other repos must score 100 itself, visibly, before
anyone else runs it; T-160 removes the last gap of a fresh repo.
- T-130 · Generated repos pass the whole grid: the proof left (S)
- T-90 · kiln passes its own grid: pinned actions, least privilege, provenance, Scorecard (M)
- T-160 · A front with no backend ships a smoke test (M)
- Its notes credit the outside fixes merged on 23 Oct: `kiln dev` sees IPv6 servers (#54),
  `kiln check` without `backend/.env.example` (#55), no pre-commit hook without its config (#56),
  each line ending `(#n, thanks @NathanBarrachin)`.

### v0.4.6 · Every gap seen, wherever the code lives
Candidate Sun 25 Oct. The score and the fixes reach what they miss today: GitHub settings,
`backend/` and `frontend/` folders, compose services, loose requirements; the reference repo's
score proves it in each note.
- T-159 · What T-126 to T-128 left: compose hardening, pyproject from requirements, `kiln update` (M)
- T-158 · `kiln score` reads the GitHub settings when `gh` is logged in (S)
- T-134 · The reference repo's score in every release note (S)

### v0.4.7 · Never lets it rot, and the grid learns
Candidate Tue 27 Oct. Updates go down by themselves, gaps come back up with consent.
- T-59 · kiln-bot: the grid's fixes as a weekly pull request (L)
- T-38 · What the grid does not know, reported with consent (M)

### v0.4.8 · Data projects done right
Candidate Thu 29 Oct. The two issues of kiln's first outside reporter (#43, #44) closed before
the launch: a Streamlit or Dash project deploys where it can run, and its models stay tied to
their code.
- T-155 · A Streamlit or Dash front gets a deployment that fits, or none is assumed (M)
- T-156 · Committed trained models tied to the code that made them (M)

### v0.5.0 · Public launch: the proof and the page
Candidate Sun 1 Nov, promoted Tue 3 Nov. Milestone decided by antoine (16 October 2026), its
content defined on 17 October: the version the launch waits for (T-03).
- T-131 · Proof on two real repos, on local copies (M)
- T-132 · The study: a hundred public Django and Nuxt repos scored (M)
- T-30 · README and English docs for strangers, with the demo (L)
- T-33 · One promise everywhere: tagline, About, PyPI, social preview (S)
- T-119 · GitHub Sponsors and `FUNDING.yml` (XS)
- T-154 · Show your score: a badge other repos display (S)

### v0.5.1 · Launch week: a stranger's first ten minutes, rehearsed
Candidate Tue 3 Nov. Fixes only from here to the launch; the week absorbs up to three slipped
releases.
- T-142 · Launch rehearsal: a stranger's first ten minutes, replayed (M)
- T-53 · Readable by Claude, measured: the A/B test (M) — only if the budget allows; its number
  joins the launch article only if it is net
- T-145 · A public benchmark: Claude Code with and without kiln (L) — same condition, after T-53

### v0.5.2 · Launch week: what the rehearsal found
Candidate Thu 5 Nov: the fixes of T-142, nothing else.

### v0.5.3 · Launch day
Candidate Sat 7 Nov, promoted on Mon 9 Nov by the next candidate: the version strangers
install. Gate checked on Mon 9 Nov at 20:00; nothing is promoted on launch day.
- T-03 · Public launch: Wednesday 11 November 2026, 16:00 Paris, every forum at once (M)

### v0.5.4 · The first week with strangers
Candidate Mon 9 Nov, promoted after the launch. What the launch brings in (issues, reports)
comes first; these tickets give way to it.
- T-45 · Update reminders at the pace you choose (S)
- T-107 · After an update, Claude is told what changed in its rules (S)
- T-118 · Each promoted release announced on Bluesky and dev.to (S)
- T-98 · Tab completion for zsh and fish (S) (good first issue)
- T-116 · An accessible CLI: `NO_COLOR`, `--plain` (S) (good first issue)
- T-10 · Interface polish (S)
- T-99 · `kiln doctor --fix` (S)
- T-153 · `statusline.ci locale`: a French value left in generated repos (S)

### v0.5.5 · Findings where people look, upgrades proven
- T-91 · Findings where people look: SARIF in pull requests and code scanning (M)
- T-54 · Every candidate proven on real upgrade paths (M)
- T-77 · Tests in seconds after each edit: only those the change touches (M)
- T-144 · Checks as fast as they are precise: oxlint, TypeScript 7, ty or pyrefly, measured (M)

### v0.5.6 · The grid grows, and stays current
- T-141 · Grid v2: the themes after the launch (L)
- T-140 · The grid kept current: its sources watched every week (M)

### v0.5.7 · For more people
- T-55 · README in Chinese, Japanese, Spanish and Portuguese (S)
- T-57 · A tutorial series: bring a Django repo up to date in an afternoon (M)
- T-58 · A public roadmap on GitHub Projects (M)

### v0.6.0 · Claude closes the gaps alone
Milestone decided by antoine (16 October 2026: Claude does the work in the repo), its content
re-scoped to the vision: the roadmap worked unattended within a budget, and only the tests that
matter written by Claude.
- T-74 · The roadmap worked unattended: one gap, one pull request (L)
- T-76 · `kiln ci --fix`: a red CI made green by Claude Code, locally (M)
- T-135 · Tests at the lowest token cost, measured on one module first (M)
- T-136 · Test generators that cost no tokens, in the template (M)
- T-137 · Claude invents, the script repeats: a fix made twice becomes a converter (M)

### v0.6.1 · Less code to carry
The vision's fourth pillar, a lead: measured before anything is built.
- T-138 · Less code to carry, measured first: the compressor's dry run (M)
- T-139 · The compressor: removals proven by types, tests and behaviour (L)

### v0.7.0 · A whole organisation's repos
Milestone decided by antoine (16 October 2026: kiln for teams and organisations), re-scoped to
the vision's targets: a university, an association network, a 50-person company; large
companies come later.
- T-39 · Profiles of structure: the rules that fit an association, a company, a university (L)
- T-87 · Fleet view: every repo of an organisation scored, without cloning (M)

### v1.0.0 · The grid others build on
Milestone decided by antoine (16 October 2026): the public stability promise, before others
build on kiln. From here, strict semver: breaking → major, `feat` → minor.
- T-69 · Community grid packs from any git repo (L)
- T-122 · `kiln version` proposes 1.0.0 (S)

## 🔴 Critical

## 🟠 Important

### T-163 · Skills call one kiln command, the backlog first
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: antoine, 21 October 2026, after T-162: "skills should use one command line at most"

A skill that runs git, gh and file reads step by step pays each step in tokens and leaves every
output in the conversation, re-read by each later message; a kiln command does the mechanics in
one call and answers in a few lines. The backlog first: one full read costs about 20k tokens
here and 36k in the reference repo, and Claude read it nearly 500 times in three weeks.
- [ ] `kiln backlog next`, `show T-NN`, `add`, `start`, `done`: one ticket in or out, never the
  whole file; `/kiln:backlog` calls them and nothing else.
- [ ] Then the mechanical skills, one command each (`merge`, `cleanup`, `worktree`, `update`);
  a skill keeps only what needs judgment.
- [ ] `test_plugins.py`: one shell command per skill at most, the skills that need judgment over
  several commands (`review`, `release`, `contribution`) listed with their reason.

### T-164 · French docs brought up to date at the candidate
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: antoine, 21 October 2026, after T-162: the docs in two languages, kept up to date in
  every branch, make about a quarter of kiln's file edits

Branches update the English docs only (`README.md`, `docs/reference.md`); the candidate
(`/kiln:release`, before `-rc.1`) translates in one pass what changed since the last version
into `README.fr.md` and `docs/reference.fr.md`.
- [ ] `test_docs.py`: the checks between the two languages run at the release only (`kiln
  version cut`), the English ones on every merge.
- [ ] `/kiln:release`: the translation step, from the English diff since the last tag.
- [ ] `CLAUDE.md` ("a change updates the docs in its branch"): English in the branch, French at
  the candidate.

### T-165 · Write less code, measured: a ladder before writing
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: the most-starred token savers, 21 October 2026: ponytail (a skill, about 45 % fewer
  tokens and more risky logic tested, by its maintainer's own benchmark)

Before writing, Claude climbs a ladder and stops at the first rung that works: does this code
need to exist, does the repo already have it, the standard library, an installed dependency, a
few lines; never cut: validation at the boundaries, security, data loss, accessibility, a test
for each risky logic. Same pillar as T-138 and T-139, which remove code that exists; this one
keeps it from being written.
- [ ] A few lines in `template/.claude/rules/kiln/` (they are read at every message).
- [ ] Measured before it stays, with T-53's method: the same tasks with and without, tokens,
  lines written, tests, bugs caught; dropped if it does not win.

### T-159 · What T-126 to T-128 left: compose hardening, pyproject from requirements, `kiln update`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: left from T-126, T-127 and T-128 (2026-10-20)

- [ ] Compose services `read_only`, `cap_drop: [ALL]`, `no-new-privileges`, kept only where the
  service still starts (needs the containers run: `podman compose up` on a copy).
- [ ] `requirements*.txt` to `pyproject.toml` and `uv.lock` (today: the loose file becomes its
  `.in` and uv compiles exact versions, which keeps images and scripts working).
- [ ] In a kiln repo, `kiln update` runs the same converters after the template.
- [ ] Images: a converter commit that touches a `Dockerfile` builds it when podman or docker is
  there (today: left to the repo's CI).
- [ ] The repo's checks found beyond its root: `check_commands` reads only the root manifests,
  so a repo with `backend/` and `frontend/` (most of the training fleet, 20 October 2026) gets
  every commit marked "unverified" although it has tests; look one folder down, and run a
  Django project's tests through `manage.py` when its settings start without secrets.


### T-158 · `kiln score` reads the GitHub settings when `gh` is logged in
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: left from T-46 (2026-10-20)

Branch protection or rulesets on the integration branch, secret scanning and push protection,
Dependabot alerts: read through `gh api` when logged in, left out of the count otherwise (never a
failure for lack of a token).

### T-130 · Generated repos pass the whole grid
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 ("bring kiln's Django + Nuxt template to the top of the
  grid"); two of the reference repo's gaps came from kiln itself

Fixing the grid in kiln fixes it everywhere at once; a kiln repo below 100 would make the whole
pitch hollow.
- [ ] `kiln new` Django + Nuxt, at each size: 100 on the rules that apply; the end-to-end tests
  fail when a template change lowers it.
- [x] The template's gaps closed (from the 17 October audit: actions by SHA, cooldown,
  Debian 13, read-only containers): shipped in v0.4.4.
- [ ] `kiln update` takes an older generated repo to 100 (the converters of T-126).
- [ ] The frozen templates (T-133) measured, their score in the docs.

### T-90 · kiln passes its own grid: pinned actions, least privilege, provenance, Scorecard
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026: a tool that rewrites
  other people's repos must pass its own grid, visibly

- [ ] Third-party actions pinned by SHA in kiln's workflows and actions; `permissions:` minimal
  everywhere; zizmor in kiln's CI.
- [ ] Build provenance attested on each GitHub Release (`actions/attest-build-provenance`);
  PyPI keeps its token (antoine's preference for a key over a manual setting, 16 October 2026).
- [ ] The OpenSSF Scorecard workflow and its badge.
- [ ] `kiln score` on kiln itself in its CI: 100 on the universal rules.

### T-59 · kiln-bot: the grid's fixes as a weekly pull request
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026 ("Never lets it rot"); rewritten 17 October 2026
  (vision, step 5: continuous)

"Dependabot for your methods" is only true if the fixes come by themselves. `kiln fix` needs no
token, so it runs in CI for free on any public repo.
- [ ] A reusable workflow (and a composite action) on a weekly schedule: `kiln score`,
  `kiln fix` (and `kiln update` in a kiln repo), one pull request kept up to date, with the
  score before and after and the why of each commit; nothing when nothing changed.
- [ ] The score and its delta commented on each pull request, optional.
- [ ] Set up in one copy-paste in any repo; the docs say the catch: a pull request opened with
  `GITHUB_TOKEN` does not start the CI, and which token or app to use instead.
- [ ] In generated repos: `kiln set update_bot=weekly|monthly|off`.

### T-38 · What the grid does not know, reported with consent
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: antoine, 16 October 2026 (adopters should tell kiln what it lacks); issue #42;
  rewritten 17 October 2026 (vision: updates go down, gaps come up, every install is a sensor)

- [ ] `kiln score` ends with what it met and the grid does not cover ("Django + django-q:
  scheduler not covered by the grid") and the rules that misfired (a waiver renewed again, a
  finding marked wrong).
- [ ] One question, once per repo: "Tell kiln? It opens an issue with this line only." Never
  code, paths, internal names or secrets: the user sees exactly what leaves, and says yes.
- [ ] One issue per gap, not one per user: the signature is looked up among open `grid-gap`
  issues first, and gets a 👍 when it exists; through `/kiln:report` with `gh`, or a prefilled
  issue link without it.
- [ ] A count is a signal, never a decision: a practice enters the grid by the doctrine
  (maturity, sources), otherwise fake reports could poison it; the most reported gaps become
  tickets first. Closes #42.

### T-134 · The reference repo's score in every release note
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 (the reference repo as training ground: its score
  measured at each kiln release)

- [ ] `kiln version` runs `kiln score --json` on the reference repo (read-only, its path in a
  machine setting) and on a local copy after `kiln fix`, and writes one line in the release
  entry, such as "Reference repo: 58 → 61, and 74 with `kiln fix`".
- [ ] A drop stops the candidate until it is explained.

### T-131 · Proof on two real repos, on local copies
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude, antoine for the message to the university team · **Due**: —
- **Origin**: vision of 17 October 2026 (validation plan, step 3; two real repos measured)

- [ ] The reference repo (18 of the 31 reference practices applied on 17 October) and a
  university repo built by students since 2023 (an ordinary repo: no CI, no lock, containers
  running as root), each copied locally: `kiln score`, `kiln fix`, their own checks green,
  `kiln score` again, the length of the roadmap.
- [ ] Nothing written or pushed in either original.
- [ ] Results anonymized in `docs/proof/` (no name, no path, nothing that identifies a project);
  the README quotes the before and after.
- [ ] The university project's team gets what the 17 October measurement found in its repo,
  privately, before any number about it is published (`urgent.md`); until then, the launch
  quotes the reference repo only.

### T-132 · The study: a hundred public Django and Nuxt repos scored
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 (validation steps 1 and 4: the pain on more than two
  repos, then a number to publish); the launch article

- [ ] The selection kept in the script, so anyone can rerun it: about 70 Django and 30 Nuxt
  public repos pushed in the last 90 days, at least 50 stars, no forks, templates or tutorials.
- [ ] Shallow clones in a temporary folder, `kiln score --json --offline` and
  `kiln fix --dry-run`, then the aggregate: median per pillar, most-missed practices, what a
  script closes, the distribution as a chart.
- [ ] `docs/study/2026-11-django-nuxt.md` with the method; aggregate only, no repo scored by
  name.
- [ ] The headline the article and Show HN can use, whatever it turns out to be: "the median
  Django repo applies X % of today's reference practices; a script brings it to Y %, without
  AI, in Z seconds".

### T-30 · README and English docs for strangers, with the demo
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: T-03 prerequisites; issues #37 and #38; rewritten 17 October 2026 for the vision

- [x] Today's README brought to the level of the best (20 October 2026, branch
  `docs/showcase`), after measuring the READMEs of 70 repos of 10,000 stars or more (uv, ruff,
  Bun, ripgrep, fzf, mise, Claude Code…): the pixel kiln on top, one promise, three badges that
  measure something (beyond five, popular npm packages get fewer downloads: Trockman et al.,
  ICSE 2018), a recorded demo first, plain bullets, the words of a visitor, a comparison where
  the others win rows too; the help screen, the rule list and the update note moved to the
  reference. `tests/test_docs.py` now fails on the marks readers take for AI writing (em dashes,
  list items opened in bold or by an emoji, sales words), on a README whose images or links
  would break on PyPI, and on a demo that types what kiln no longer offers.
- [x] Demo recorded with vhs (`docs/assets/kiln-new.tape`, `scripts/demo_shell.sh`): `kiln new`,
  its three questions, then `kiln check` on the new repo; replayed before each candidate.
- [ ] v0.5.0 first screen: the promise (T-33), `uvx kiln-cli score`, then the study's chart as
  the hero, as uv and ruff open on one benchmark chart: light and dark, a caption with the exact
  conditions, a link to the script that reruns it (T-131, T-132); then how it works in five
  steps (score, fix, roadmap for Claude, verified by the script, continuous), the grid, and
  "Built for Claude Code; the score and the fixes need no AI at all".
- [ ] A second tape: `kiln score` on a public example repo (never a team's project shown at
  fault), `kiln fix`, the score again, the kiln-bot pull request; its first frame says what it
  shows, as animations stay paused for those who ask for less motion.
- [ ] Docs in English in `docs/`: getting started, score, fix, modernize, the grid (one page per
  theme generated from the rule files: the Technology Radar that applies itself), update,
  charter, plugins, workflows, versions. `README.fr.md` shrinks to a French summary pointing
  there. Closes #37 and #38 (another good first issue opened instead).
- [ ] A comparison page, facts only: what Dependabot and Renovate, Copier and cruft,
  sp-repo-review, OpenRewrite, AWS Transform and Claude Code's `/doctor` do, and what kiln adds
  (from the vision's market table); the r/Python Showcase format asks for it (T-03).
- [ ] `kiln new` second: "Starting a repo? It starts at 100."
- [ ] The default branch becomes `main` with v0.5.0, so the repo page and `claude plugin
  marketplace add` show what `uvx kiln-cli` installs; pull requests still go to `develop`
  (CONTRIBUTING).

### T-33 · One promise everywhere: tagline, About, PyPI, social preview
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude, antoine for the social preview upload · **Due**: —
- **Origin**: positioning, 16 October 2026; rewritten 17 October 2026 from the vision's
  taglines

"Start every project like a senior engineer would" sold `kiln new`; the vision sells keeping any
repo up to date. The same words in the README hero, the GitHub About (search results, link
previews), the PyPI summary and the launch titles.
- [x] Today's promise, the same everywhere, chosen by antoine on 20 October 2026 from the
  former ones ("Repos Claude Code can work in safely, kept up to date." was too bare): "Claude
  Code's workshop", then "Start every new project, and rescue every old one, like a senior
  engineer would — even if you're not one.", and under it "Make Claude Code build
  production-grade repos, bring yours up to that grade, and keep them that way." An old repo to
  bring up counts as much as a new one. In the README, the PyPI summary (`pyproject.toml`), the
  GitHub About and the social preview drawn by `scripts/screenshots.py`.
- [ ] Decided by Claude (17 October 2026), from the vision's taglines, reworded on 20 October:
  **"Dependabot for engineering practices."** ("your methods" reads as class methods to an
  English-speaking developer), then "kiln keeps your repo up to date with the best of the world
  (methods, structure, tools, containers, security, code standards) and easy for Claude to
  read." The analogy explains the job in four words, as "A cat(1) clone with wings" (bat) or "A
  smarter cd command" (zoxide) do; "the best" alone would read as an opinion. Shown to antoine
  first, with today's line beside it: he keeps "Claude Code's workshop" and the senior engineer
  line (20 October 2026), and decides whether the analogy joins them or replaces them.
- [ ] Right under it, the proof in numbers (T-131, T-132) and the one line
  `uvx kiln-cli score`.
- [ ] GitHub About and topics (best-practices, modernization, code-quality, technical-debt next
  to claude-code, django, nuxt), PyPI summary; the social preview (1280×640) redone with the new
  line, uploaded by antoine (no API): https://github.com/antoine-tena/kiln/settings (Social
  preview).
- [ ] The social preview redrawn with the v0.5.0 promise (`scripts/screenshots.py`, then
  `scripts/social_preview.py`), then a box in `urgent.md` asking antoine to upload it again
  (no API takes it): https://github.com/antoine-tena/kiln/settings, "Social preview", "Edit".
  Today's image was uploaded by antoine on 20 October 2026.

### T-154 · Show your score: a badge other repos display
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: README study, 20 October 2026; after T-46

The image that travels by itself: GitHub's code search finds the Ruff badge in about 7,800
READMEs, OpenSSF Scorecard's in about 25,000, github-readme-stats cards in about 247,000. A score
is a badge that measures something, the kind a study of 294,941 npm packages found reliable and
lasting (Trockman et al., ICSE 2018), whose authors ask for badges of "conformance to coding
standards".
- [ ] `kiln score --badge`: the Markdown of a shields.io endpoint badge, its JSON kept up to date
  by kiln-bot (T-59) or the CI.
- [ ] A "Show your score" section in the README, as Ruff has; kiln's own badge on top (T-90).
- [ ] The `kiln score` output made to be screenshotted: the score large, the kiln, 80 columns.

### T-119 · GitHub Sponsors and `FUNDING.yml`
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: XS · **Owner**: antoine for the Sponsors profile, Claude for the file · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026

- [ ] Sponsors profile: https://github.com/sponsors/accounts ; `.github/FUNDING.yml` and a line
  in the README, in place before the launch.

### T-142 · Launch rehearsal: a stranger's first ten minutes, replayed
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: 2026-11-09
- **Origin**: launch planned on 17 October 2026 (T-03)

- [ ] On fresh GitHub-hosted runners (Ubuntu, macOS) and in a clean container: the README's
  commands copied as they are, `uvx kiln-cli score` from an empty cache on three public repos of
  the study, `kiln fix --dry-run` then `kiln fix`, kiln-bot on a throwaway repo; the time of
  each step.
- [ ] Every stumble fixed in v0.5.1 to v0.5.3, never on the day.
- [ ] The texts of T-03 checked against each forum's rules.

### T-03 · Public launch: Wednesday 11 November 2026, 16:00 Paris, every forum at once
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-15
- **Effort**: M · **Owner**: antoine for Hacker News and Reddit, Claude for the rest ·
  **Due**: 2026-11-11
- **Origin**: GitHub showcase, 15 October 2026; date and gate fixed on 17 October 2026 at
  antoine's request ("a date when I publish on every forum at once, only after a version you
  define")

One launch, everywhere the same afternoon: stars come in a burst, and the launch happens once.
Nothing is posted on a forum before it (T-118 starts after).

**The version it waits for: v0.5.0**, and what it has to prove:
- [ ] `kiln-cli` 0.5.0 or later promoted on PyPI; `uvx kiln-cli score` works from an empty
  cache on Linux and macOS, on a repo kiln never saw (T-142).
- [ ] `kiln score` deterministic, offline, without a token, under 5 seconds on a 50,000-line
  repo (T-46); `kiln fix` closes every scriptable gap of the two local copies, their checks
  still green (T-126 to T-128, T-131); kiln-bot runs on a test repo (T-59).
- [ ] The study published (T-132); the README's first screen and the docs done, the demo
  recorded from the released version (T-30, T-33).
- [ ] kiln passes its own grid, its CI green on `main` (T-90).
- [ ] No open 🔴 ticket.
- [ ] The Hacker News title, text and every answer written by antoine, by hand: HN's
  guidelines say "Please don't put generated text in HN posts" and, for comments, "Don't
  post generated text or AI-edited text"; Claude hands over raw facts only (numbers, links).
  No upvotes asked, no booster comments from friends.
- [ ] Gate checked on **Monday 9 November at 20:00**. One box empty: the launch moves to
  **Wednesday 18 November**, same hour, gate on Monday 16 November. The date moves, never the
  gate.

**Why this date.** Reaching v0.5.0 takes about 27 session-hours, seven releases at the two-day
cadence (candidate on Sunday 1 November, promoted on Tuesday 3); the week from 3 to 9 November
absorbs up to three slipped releases and rehearses the launch. A Wednesday: Hacker News readers
are there from Tuesday to Thursday, and 11 November is a public holiday in France, so antoine is
free to post at 16:00 and answer until midnight. A week after the US midterm elections
(3 November), two after GitHub Universe (28 and 29 October). The Pro quota restarts on Tuesday
10 November at 8:00: the launch day and the days after have a whole week for fixes and answers.
16:00 in Paris is 10:00 in New York and 7:00 in San Francisco: Europe still at work, the US
East Coast in its morning, the West Coast waking up.

**The day** (Paris time; every text written the week before, each in its forum's format):
- [ ] 15:30: last check, `uvx kiln-cli score` on a fresh clone of a public repo; README and
  links.
- [ ] 16:00: Show HN, by antoine: https://news.ycombinator.com/submit (rules:
  https://news.ycombinator.com/showhn.html). Suggested title: "Show HN: Kiln – Dependabot for
  your methods, not just your versions". Then antoine's first comment: why, how it works, the
  method of the study.
- [ ] 16:05: the study as a dev.to article and a Bluesky thread, posted by Claude (`.devto/`,
  `.bluesky/`), saying the text is written with Claude where the platform asks.
- [ ] 16:15 to 17:15, a quarter of an hour apart (identical posts at once trip Reddit's spam
  filters), by antoine: https://www.reddit.com/r/ClaudeAI/submit,
  https://www.reddit.com/r/ClaudeCode/submit, https://www.reddit.com/r/django/submit,
  https://www.reddit.com/r/Python/submit (its "Showcase" format: what it does, target audience,
  comparison), https://www.reddit.com/r/Nuxt/submit.
- [ ] The same day, by Claude: awesome-claude-code, through its issue form only, one
  recommendation: https://github.com/hesreallyhim/awesome-claude-code/issues/new/choose
- [ ] Until midnight: every comment answered by antoine, with facts from the study, never an
  argument over taste; pull requests through `/kiln:contribution`; three good first issues open
  (T-98, T-116, a grid rule to add) by `/kiln:good-first-issues`.
- [ ] A week later, with the first numbers: Anthropic's plugin directory,
  https://clau.de/plugin-directory-submission
- [ ] Never: asking for votes, posting from several accounts, the same text twice without a
  canonical URL.

### T-53 · Readable by Claude, measured: the A/B test
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
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

### T-167 · The branch guard reads the session's folder, not the command's
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: T-05 probe, 2026-10-21

`plugins/kiln/hooks/branch_guard.py` refused `cd <scratch repo> && git commit` on a branch of
another repo with "never commit on develop": it checks the branch of the session's folder and
ignores a leading `cd` (`git -C` got through). It should judge the repo the command runs in.

### T-168 · A repo from `kiln new` + `gh repo create --push` has no CI workflow on GitHub
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: T-05 probe, 2026-10-21

After the first push, `ci.yml` was not registered (dispatch answered 404 for minutes); a second
commit touching the file registered it. Reproduce with `kiln publish`, then find out whether it
is GitHub's or kiln's doing.

## 🟡 Normal

### T-160 · A front with no backend ships a smoke test
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: training on the fleet (2026-10-20): a new `none` + Nuxt, Next or Astro project
  misses TESTS-PRESENT, the only gap left on a fresh repo (`test_template.py` exempts it)

Its only code is constants: a test of them would be filler. The test worth having is a smoke
test of the built site, the home page carrying the site title, through `node --test` (no
dependency): Astro's `dist/index.html`, Next's prerendered `.next/server/app/index.html`, Nuxt
prerendering `/` or its server started. Run after `build` in `ci.yml` and in `kiln check`; then
drop the exemption.

### T-155 · A Streamlit or Dash front gets a deployment that fits, or none is assumed
- **Type**: bug
- **Status**: in progress
- **Opened**: 2026-10-20
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: issue #43 (darnak69, 16 October 2026)

- [x] `frontend_deploy=vercel` refused for Streamlit and Dash (they need a long-running
  Python server with websockets).
- [x] With no deployment set, nothing generated cites `deploy.yml` or `scripts/ops/deploy-*.sh`
  (comment of `ci.yml`; the `release` skill ends at the tag when nothing deploys).
- [ ] A target that fits: `vps` (podman + Caddy) opened to the front image, with a
  `/_stcore/health` probe (already in `compose.yaml`; the `uv` image is already pinned by
  digest). Closes #43.

### T-156 · Committed trained models tied to the code that made them
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: issue #44 (darnak69, 16 October 2026)

For `backend=data`: a manifest next to each committed model (hash of the training code, seed,
dataset version, metrics) written by the training command; a check that the hash still matches
the code, or the commit says why; a test template asserting the committed model's metrics stay
above the recorded ones. Goes in the grid as a rule with its sources (T-123 doctrine), not
only in the template. Closes #44.

### T-153 · `statusline.ci locale`: a French value left in generated repos
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: the README's recorded demo (20 October 2026) shows `git config statusline.ci locale`

kiln moved to English in 0.4.0, but `apply_statusline_settings` (`src/kiln/statusline.py`) still
writes `locale` for a CI run on the machine, read by the status line script, the session start
hook and `/kiln:merge`. Write `local`, keep reading `locale` (hooks and status line are read from
the main tree by open sessions), convert existing repos in `kiln update`.

### T-45 · Update reminders at the pace you choose
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: antoine, 16 October 2026

Asking at every release annoys; letting users skip releases is worse in 0.x (each patch can
break, skipped conversions pile up). So space the question, never the updates.
- [ ] `kiln set update-reminders=each|daily|weekly` (machine setting, default `weekly`: kiln
  ships a release every two days, antoine's call of 17 October 2026); when accepted, the repo
  goes to the latest release in one step, with one short note per release crossed, breaking
  changes first.
- [ ] A release that changes nothing for this repo (its stack untouched, plugins only) is
  applied without a question at the next `kiln update`, never counted as a reminder.
- [ ] From 1.0 (strict semver): `update-level=patch|minor|all` to follow only some releases.

### T-107 · After an update, Claude is told what changed in its rules
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026; the grid changes at every release

A session opened before an update keeps working by the old rules.
- [ ] The session-start hook says, once, the rules added or changed by the last update (from
  the release notes and the grid's `since`), in three lines at most.

### T-118 · Each promoted release announced on Bluesky and dev.to
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026; accounts ready (T-03)

Every release is a reason to be seen again, from the launch on: nothing before it, so the
launch lands as one wave.
- [ ] At promotion, a short post written from the release notes (what a user notices, one
  link), posted from `.bluesky/` and `.devto/`; skipped for a release with nothing visible.

### T-91 · Findings where people look: SARIF in pull requests and code scanning
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 for the grid

- [ ] `kiln score --sarif`, uploaded by kiln-bot (T-59) and the charter workflow: findings in
  the pull request diff and in GitHub code scanning.
- [ ] Repo-local rules in the grid's format (`.kiln/grid/`), tested like kiln's; a rule that
  proves useful is proposed to kiln by `/kiln:report`.

### T-54 · Every candidate proven on real upgrade paths
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; the nightly end-to-end run exists since v0.3.4

The promise "kept up to date for as long as the project lives" rests on `kiln update` from any
old release.
- [ ] Repos generated by each of the last five releases updated to the candidate: checks green,
  no conflict marker, a score never lower; a candidate is not promoted otherwise (`kiln version`
  reads the result).
- [ ] The hooks, skills and status line run against the current and the previous Claude Code
  release; `claude plugin eval` suites for the main skills.

### T-77 · Tests in seconds after each edit: only those the change touches
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; complements T-27 (doctrine 11: only recheck what
  changed)

Claude Code learns from fast feedback; a full suite after each edit is too slow on big repos.
- [ ] `kiln test --changed`: pytest-testmon, `vitest related`; the full suite stays in
  `kiln check` and CI.
- [ ] Offered to Claude as the default test command in the generated rules.

### T-144 · Checks as fast as they are precise: oxlint, TypeScript 7, ty or pyrefly, measured
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-18
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026, doctrine 11 ("the fastest, at equal precision"; on the
  reference repo: ruff 0.4 s, the charter 1.1 s, mypy 22.6 s, eslint 42.3 s)

A slow check ends up not being run, and the time goes into the tools, not into kiln's code.
- [ ] Each candidate measured on a local copy of the reference repo against the tool it would
  replace, for time and for what it finds: oxlint next to eslint (2.7 s, fewer rules, weak on Vue
  templates), TypeScript 7's native compiler for the type check, ty or pyrefly next to mypy on
  Django code.
- [ ] Each one a grid rule (T-123): `trial` in the template only when it finds at least what the
  old tool found on the rules it covers, `assess` otherwise; the measurement kept as its source.
- [ ] kiln's own rules written as ast-grep patterns where a pattern can say them; Rust only where
  a measurement shows kiln's code is the slow part.

### T-141 · Grid v2: the themes after the launch
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 (the 23 themes); T-52, T-78, T-92, T-93, T-101, T-102,
  T-103 and T-105 merged here, as rules

- [ ] Tests: property tests, mutation testing, API fuzzing, end-to-end journeys (with T-136).
- [ ] Data and migrations: migrations linted before merge (django-migration-linter, squawk),
  seed data, anonymised dumps.
- [ ] Front, accessibility and performance: axe checks, Lighthouse budgets, Core Web Vitals.
- [ ] Operations and observability: backups with a tested restore, health checks, alerts on
  symptoms; OpenTelemetry and SLO by profile (T-39).
- [ ] Git and docs: issue and pull request templates, CODEOWNERS, a licence and the
  dependencies' licences checked, release notes written from the commits.
- [ ] AI-assisted development: `AGENTS.md` for every agent, the context loaded at session start
  measured and capped, MCP servers pinned, narrow permissions, a tool that reads code symbol
  by symbol (Serena, an LSP) so a file's size matters less.
- [ ] Business domain, as universal rules with project settings: money in cents, dates stored
  in UTC, personal data out of the logs.

### T-140 · The grid kept current: its sources watched every week
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 ("keeping this grid up to date for the whole world is
  permanent work: that is where the value is, and what an agent alone does not do")

- [ ] A weekly job in kiln: endoflife.date, the release notes of the tools the grid names, the
  OSV advisories, the Technology Radar when a volume comes out; flagged: rules whose sources are
  more than six months old, end-of-life dates crossed, release candidates turned stable.
- [ ] One pull request to kiln with the proposed level changes and their sources, decided by the
  doctrine (maturity, sources), never by a count.

### T-55 · README in Chinese, Japanese, Spanish and Portuguese
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026

A large share of the stars on developer tools come from Chinese, Japanese and Brazilian
communities, who share translated READMEs widely.
- [ ] `README.zh-CN.md`, `README.ja.md`, `README.es.md`, `README.pt-BR.md`, linked from the
  language line of the README.
- [ ] A check at release time: same sections and same commands as `README.md`, otherwise the
  release lists which translation is behind.

### T-57 · A tutorial series: bring a Django repo up to date in an afternoon
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 for the vision

Tutorials keep bringing visitors long after a launch; a series also tests the path for real.
- [ ] Five parts in `docs/tutorials/`, published on dev.to (`.devto/`), on a public sample repo:
  the score, the fixes, the roadmap with Claude Code, kiln-bot, staying there.
- [ ] Each part replayed at each minor release by a script; a broken step is a bug.

### T-58 · A public roadmap on GitHub Projects
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026

Contributors and users want to see where kiln goes and to weigh in, without reading a Markdown
file.
- [ ] `docs/backlog/backlog.md` published one way to a GitHub Project (one card per ticket,
  release as a field) by a workflow at each push on `develop`.
- [ ] Discussions (already enabled) with categories: ideas, the grid (a rule to add or to
  challenge), show and tell, questions; linked from the README and from `/kiln:report`.

### T-74 · The roadmap worked unattended: one gap, one pull request
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 (v0.6.0: Claude closes
  the gaps alone)

- [ ] Headless Claude Code takes the roadmap of T-129 item by item, each in its own worktree,
  and opens a pull request when the checks pass and the gap has left the score; it never
  merges.
- [ ] A budget per item and per night in session time, said before it starts and kept within
  the Pro quota; one item at a time (no fleet); a report in the morning.

### T-76 · `kiln ci --fix`: a red CI made green by Claude Code, locally
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; builds on `kiln ci`

- [ ] Reads the failed job (GitHub logs or local replay), runs headless Claude Code on a work
  branch with the failure as the prompt, replays the job until green or the budget is spent.
- [ ] Never touches a test to make it pass without saying so in the commit message.

### T-135 · Tests at the lowest token cost, measured on one module first
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 ("the most tests for the fewest tokens"; validation
  step 5)

Asking Claude for every test is the expensive way. On a local copy of the reference repo, its
money module leaves 3 surviving mutants out of 16.
- [ ] mutmut on that module, then Claude writes only the tests that kill the survivors; tokens
  and session time counted; a test is kept only if it passes five times in a row and kills a
  mutant or adds coverage.
- [ ] If the number is net, the recipe joins `/kiln:modernize`: coverage and survivors measured
  by script (mutmut for Python, Stryker for TypeScript), Claude on the holes only, the rest
  thrown away unread; coverage and survivors as ratchets.

### T-136 · Test generators that cost no tokens, in the template
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 (generators without a model first)

- [ ] Schemathesis on the Django Ninja API, Hypothesis for the pure computations (prices,
  dates) with CrossHair as its engine, snapshot tests to freeze behaviour before a modernization, the Playwright recorder for
  the Nuxt journeys; each wired in the template and in `kiln check`, and each a rule of the grid
  (T-141).

### T-137 · Claude invents, the script repeats: a fix made twice becomes a converter
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026 (doctrine 6)

- [ ] From the log of `/kiln:modernize` (T-129): a rule fixed the same way twice, in one repo or
  across repos (with consent, the circuit of T-38), is proposed as a converter; Claude writes it
  with its tests, a cost paid once per rule instead of once per repo.

### T-39 · Profiles of structure: the rules that fit an association, a company, a university
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: "the smallest level at creation, and rules that grow with the repo" (antoine,
  16 October 2026); rewritten 17 October 2026 from the vision (doctrine 1: one way per stack
  and per size of structure; risk 4: "the best depends on the context")

- [ ] Profiles: solo or association, a company of about 50 people, a university (student
  projects, labs), large companies later; each rule of the grid says which it fits.
- [ ] The profile read from the repo's answers, otherwise suggested from signals (contributors
  in the last 90 days, a deployment, several services), never imposed: `kiln set profile=…`.
- [ ] Moving to a bigger profile applies the new rules as ratchets on the existing code, never a
  wall of errors.
- [ ] The sizes of `kiln new` (spark, ember, flame, blaze) map onto the profiles.

### T-87 · Fleet view: every repo of an organisation scored, without cloning
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 (the vision's targets: a
  university whose student teams change every year, an association network)

- [ ] `kiln status --org <name>`: through the GitHub API, each repo's score, its lag behind the
  grid, its CI and its open security alerts.
- [ ] An HTML report, also produced weekly by a workflow in the organisation's `.github` repo.

### T-122 · `kiln version` proposes 1.0.0
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: milestones decided by antoine, 16 October 2026 (v0.5.0, v0.6.0, v0.7.0, v1.0.0)

In 0.x, `kiln version --minor` only moves to the next minor (`release.py`): nothing proposes
leaving 0.x.
- [ ] `kiln version --stable` proposes `1.0.0` from any 0.x release, says what changes from then
  on (strict semver, breaking → major) and refuses without a `## v1.0.0` note that states the
  promise (what is public API, the grid format included; how long a major is supported).
- [ ] `kiln version` reads the milestones of `docs/backlog/` and says "the next release is the
  v0.6.0 milestone" instead of proposing a patch.

## ⚪ Background — long-running work, debt and ideas

### T-98 · Tab completion for zsh and fish
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: a contributor (good first issue at the launch) · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026; follows T-20 (bash)

zsh is the default shell on macOS: most newcomers there get no completion today.
- [ ] `kiln completion zsh` and `kiln completion fish`, built from the parser like bash; the
  README line for each.

### T-116 · An accessible CLI: `NO_COLOR`, `--plain`, screen readers, CI logs
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: a contributor (good first issue at the launch) · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026

- [ ] `NO_COLOR` and `--plain` respected everywhere (no spinner, no box drawing, words instead
  of symbols); tested like the output outside a terminal.

### T-10 · Interface polish
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-15
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: interface redesign, 15 October 2026

- [ ] `kiln check`: the step title and the `✓` line say the same thing (one command per step).

### T-99 · `kiln doctor --fix`: the fixes applied, not just printed
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026

- [ ] Each problem `kiln doctor` finds and can fix safely (pre-commit missing, plugin not
  installed, outdated kiln) is fixed after one confirmation; the others keep their command and
  direct link.
### T-138 · Less code to carry, measured first: the compressor's dry run
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026, fourth pillar ("slim down", a lead): writing code
  costs almost nothing now, its mass is the problem

- [ ] `kiln score` gains the slimming pillar: unused dependencies (deptry, knip), dead code
  (vulture), measured on the reference repo and on the study's repos.
- [ ] The upkeep ahead, next to it: how many dependency releases the repo will absorb in a year,
  how many breaking, which ends of life are coming (libyear measures the lag behind; this
  measures what is coming), and how much removing the unused dependencies lowers it.
- [ ] The number decides the rest: "−22 % of lines, −9 dependencies, same behaviour" is worth
  building; a few percent is not.

### T-139 · The compressor: removals proven by types, tests and behaviour
- **Type**: idea
- **Status**: in progress — started before T-138's number, at antoine's request (21 October
  2026); the compressor's own dry run gives that number. Merged into develop on 22 October
  2026: `kiln fix --rule DEAD-CODE` and `--rule UNUSED-DEPENDENCIES`, proven by the type
  checker and the tests; the behaviour comparison and the dependency replacement remain
- **Opened**: 2026-10-17
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026, fourth pillar

No open tool removes existing code with a proof.
- [ ] `kiln fix` removes what T-138 found, each removal proven in steps (type checker, then
  tests, then behaviour compared); an unproven removal is not applied. Type first, compress
  after.
- [x] Never rewritten: cryptography, parsers, time zones, Unicode.
- [ ] Replacing a dependency by the part actually used comes second, after measurements: the
  most striking, and the riskiest.

### T-145 · A public benchmark: Claude Code with and without kiln
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-18
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: vision of 17 October 2026, ideas in reserve ("a public benchmark, Claude Code with
  and without kiln, that could serve as proof"); widened on 21 October 2026 at antoine's
  request: the tokens kiln saves, shown each session

T-53 measures one hypothesis (small files); this one measures the whole promise. Only rtk's
savings are measured live (`rtk gain`); the rest (repo map, skills, charter) can only be
estimated, and an estimate is credible only from a published A/B run.
- [ ] The same tasks given to headless Claude Code (`claude -p`, its usage read per run) on
  local copies of the training repos, with and without kiln, then before and after `kiln fix`
  and `/kiln:modernize`, several runs each: tokens, turns, red CIs, rules broken, tasks done;
  its cost on the Pro quota said before it runs, stopped at the budget.
- [ ] Published with its method and script whatever the result; after T-53, which sets the
  method. If the number is net, it joins the README and the launch (T-03).
- [ ] Status line: rtk's savings since the session started (measured, cached), and the
  benchmark's figure marked `≈` with a link to its method; tokens, never dollars (a Pro plan
  pays no tokens).

### T-69 · Community grid packs from any git repo
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026: the community modules
  of v1.0.0 are grid packs

An ecosystem is what turns a tool into a project people star and contribute to.
- [ ] `kiln grid add github:someone/kiln-grid-fastapi`: rules for a stack or a domain kiln does
  not cover, in the format of T-123, scored like kiln's own, with a trust prompt that shows what
  their detectors and fixers run.
- [ ] An index of reviewed packs in kiln; an author kit (template, contract tests, a workflow
  that tests the pack against each kiln release).
