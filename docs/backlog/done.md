# Done

The closed tickets of kiln, most recent first, one line each:
`- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.

- **2026-10-26** · T-172 · The checks of `kiln fix` told apart, timed out, their log kept for Claude — `grid/checks.py`: each check run once before the first converter, a missing tool (with its install), a check already red and a timeout told apart in the summary, the green ones judging and named in each commit; a 10-minute timeout per check; checks one folder down, Django's `manage.py test`, yarn and bun, `typecheck`; a reverted converter's log kept in the git folder and its gap handed to `kiln score --roadmap` (feat/fix-checks) · opened 2026-10-24
- **2026-10-26** · T-185 · `kiln dev` in an adopted repo with a compose file offers its services — a repo kiln's stack does not serve, whose compose file runs its own services while kiln would run its `package.json` scripts, is offered the compose services in podman or the scripts on the machine, the answer remembered; outside a terminal a note points to `--containers` (feat/dev-compose-services) · opened 2026-10-24
- **2026-10-26** · T-166 · An adopted repo whose code is not in `backend/` or `frontend/` gets its stack too — `backend_dir` and `frontend_dir` in the answers (written by `kiln adopt`, kept only when not the default): CI, hooks, Claude rules, charter, Dependabot, `kiln check`, `kiln dev`, `kiln install` and `kiln contract` follow the code to the root; a generated repo renders byte for byte as before; tested for each stack at the root and for an adopted Vite app through `kiln update`; closes the rest of #59 (feat/code-at-root) · opened 2026-10-24
- **2026-10-26** · T-186 · Binary and non-UTF-8 files read right, GitHub settings read through `gh` — a non-UTF-8 source decoded (BOM, cp1252, latin-1) and listed, binary and minified files left out of the code rules (A30, A31); the GitHub settings of T-158 (M16 without required pull requests nor signatures, kiln's way merging straight into develop; M17; M29 cached a day; S09 the token stays gh's) (feat/score-reads-right) · opened 2026-10-25
- **2026-10-26** · T-158 · `kiln score` reads the GitHub settings when `gh` is logged in — the GitHub settings read through `gh` when it is logged in with admin rights (`grid/forge.py`), five rules (PROTECTED-BRANCH, FORGE-SECRET-SCANNING, DEPENDABOT-ALERTS, PRIVATE-VULN-REPORTING, CODE-SCANNING in trial), each gap with its settings page; unknown without access, never a failure; never read in CI, so a setting's detail stays on the owner's machine; `glab` and `tea` left to T-301 and T-316 (feat/score-reads-right) · opened 2026-10-20
- **2026-10-26** · T-342 · Not using an agent is not a fault: agent files out of the score — `AI-CONTEXT` an `assess` rule shown as advice, out of the score, to a repo worked with an agent (fact `agent`: a `.claude/`, `.cursor/`, `.codex/` or `.gemini/` folder); `REPO-MAP` reads `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md` too; kiln stays at 100 (feat/agent-files-unscored) · opened 2026-10-26
- **2026-10-26** · T-343 · Two habits for every repo: reproduce first, a direct link for every online step — the template's `project.md` gets **[REPRODUCE-FIRST]** and **[DIRECT-LINKS]**; Claude's trailers a machine setting, `kiln set ai_trailers=disclose|never`, asked at the first `kiln install` ("choose for me": disclose), `never` empties Claude Code's `attribution` and the branch guard refuses Claude's co-author trailer; antoine's machine on `never` (feat/two-habits) · opened 2026-10-26
- **2026-10-26** · T-362 · `kiln doctor` calls kiln's own repo "not a kiln repo" — kiln's checkout (its `copier.yml`, `template/` and the `kiln-cli` package) reported as the template's source; a stranger's repo still warned (fix/doctor-kiln-repo) · opened 2026-10-26
- **2026-10-26** · T-361 · `kiln ci` speaks French in one reason — the reason of a job with services of its own in English, the one French string left in what the user reads (the others convert old files) (fix/ci-english) · opened 2026-10-26
- **2026-10-24** · T-38 · What the grid does not know, reported with consent — `kiln score` names the known packages no rule covers and the rules waived again and again; in a terminal it offers to tell kiln with the exact lines that leave, one issue per gap or a 👍, a prefilled link without `gh`, "never" per repo; closes #42 (feat/grid-gaps) · opened 2026-10-16
- **2026-10-24** · T-156 · Committed trained models tied to the code that made them — `pipeline/models.py` in the data stack writes a manifest (code hash, seed, dataset, metrics), `tests/test_models.py` fails on stale code or lower metrics, grid rule `MODEL-TRACED` (trial); closes #44 (feat/traced-models) · opened 2026-10-20
- **2026-10-24** · T-155 · A Streamlit or Dash front gets a deployment that fits — `deploy=vps` for a dashboard alone: its image behind Caddy, websockets, `/_stcore/health`, `deploy-frontend.sh`, no database; the Django deployment renders as before; closes #43 (feat/vps-front) · opened 2026-10-20
- **2026-10-22** · T-12 · Homebrew formula in the `antoine-tena/kiln-homebrew` tap — `brew install antoine-tena/kiln/kiln`; `scripts/homebrew_formula.py` writes it from `uv.lock` and the wheel on PyPI (wheels only, each pinned by its hash), `pypi.yml` pushes it at each promoted tag with the deploy key `HOMEBREW_TAP_KEY`, a tool from the tap is told `brew upgrade kiln` (feat/t12-homebrew) · opened 2026-10-16
- **2026-10-21** · T-162 · Save tokens without limiting Claude — compaction at 400k by default (`compact_window`, the `autoCompactWindow` setting, `claude --autocompact 1M` lifts it), status line in tokens, red once the cache has expired, `/clear` suggested after a merge, skill descriptions under 300 characters; claude.ai connectors left to each person; turned down: a smaller model or effort, a compaction at 200k, one session at a time, a release a week (feat/token-savings) · opened 2026-10-21
- **2026-10-21** · T-129 · What needs judgment goes to Claude — `kiln score --roadmap` (sure gaps first, then the smallest, places and proof; approximate ones "to confirm"), `--write` (backlog tickets, once each), `--rule ID` (fails while open), a false positive dismissed by a waiver on its path (grid IDs accepted by the charter), skill `/kiln:modernize` (tests first, one commit per gap, the rule ID in its body for T-137) (feat/roadmap) · opened 2026-10-17
- **2026-10-21** · T-161 · Install kiln on the whole machine, in one command — `kiln install` outside a repo (or `--machine`): the CLI as a uv tool, the catalogue and `kiln@kiln` at user scope, the machine settings, only what is missing; `kiln doctor` points to it (feat/install-machine) · opened 2026-10-21
- **2026-10-20** · T-126, T-127, T-128 · `kiln fix` and its first 14 converters — one commit per rule on `kiln/fix-<date>`, checks before and after, red undone, `--dry-run`, `--rule`; supply chain and CI, Python, containers and runtimes; the university copy went from 35 to 61; leftovers in T-159 (feat/kiln-fix) · opened 2026-10-17
- **2026-10-20** · T-157 · #45 and #46 credited in the v0.4.2 notes (release/v0.4.2) · opened 2026-10-20
- **2026-10-20** · T-46 · `kiln score` — any repo against the 40 scored rules: score out of 100 and per pillar, three gaps first, waivers apart, uncovered stacks listed, `--all`, `--json` (schema 1), `--badge`, `--online`; about 1 s on the reference repo; GitHub settings left to T-158 (feat/kiln-score) · opened 2026-10-16
- **2026-10-20** · T-125 · Grid v1 — 40 scored rules (nine drafts promoted, 25 new), each sourced and dated, with a passing and a failing example, run on local copies of both training repos: rules that can flag wrongly launch `review` or `ratchet`; 1.0 s on the reference repo (feat/grid-v1) · opened 2026-10-17
- **2026-10-19** · T-143 · Decide the name before the launch — antoine keeps **kiln**, after
  the facts of `docs/vision/nom.md` (Kiln-AI, two agent tools of the same name, `kiln` taken on
  PyPI and npm); the package stays `kiln-cli` · opened 2026-10-18
- **2026-10-19** · T-14 · Delete the old PyPI token — done by antoine: only the `kiln-cli`
  token scoped to the project remains, the one `pypi.yml` publishes with · opened 2026-10-16
- **2026-10-19** · T-124 · The reference repo's rules sorted on the two axes — its 108 named
  rules and 15 backend pillars, plus what lives outside its charter (operations, structure,
  tracking), read only and anonymized, merged where they repeat into 105 draft rules
  (`level = "assess"`, out of the score): each with theme, scope, regime, profiles, whether a
  script can detect and fix it, and the kiln charter rule that enforces it; `kiln grid` shows
  adopt and trial by default (feat/grid-reference) · opened 2026-10-17
- **2026-10-19** · T-133 · The other templates frozen while Django and Nuxt reach the top —
  said in both READMEs and at the end of `kiln new` for another stack; the end-to-end matrix
  keeps them all (docs/frozen-stacks) · opened 2026-10-17
- **2026-10-19** · T-146 · kiln moves the workflows' tag forward in adopted repos —
  `kiln update` (and `--all`, `--rehearse`) in an adopted repo moves only the
  `antoine-tena/kiln/...@ref` references to the latest public release, after checking each
  input against the workflow at that tag; `kiln adopt` does it at adoption, `kiln status` shows
  the quoted tag (feat/adopted-tag) · opened 2026-10-19
- **2026-10-19** · T-123 · The grid as data: one small file per rule, on two axes —
  `src/kiln/grid/` (format, closed lists, validation, facts of a repo, declarative detectors and
  Python checks, `kiln grid`), six `adopt` rules with sources checked on 19 October; each rule
  needs a passing and a failing example (feat/grid-data) · opened 2026-10-17
- **2026-10-19** · T-152 · A private repo's CI runs on the machine — answer `ci_runner`
  (`local` by default, `github` for a public repo, picked from the visibility by `kiln update`),
  `ci.yml` without push triggers, `/kiln:merge` runs `kiln ci`, the status line and the session
  start read its git note; antoine's GitHub free plan kept running out of minutes
  (feat/local-ci-private) · opened 2026-10-19
- **2026-10-19** · T-147 · One answer to "which kiln version" — only a release updates a repo,
  the package records the commit it is built from, `--version` says what is installed; antoine's
  machine on `v0.4.0-rc.2` from GitHub; annway's update rehearsed green with it
  (fix/version-truth) · opened 2026-10-19
- **2026-10-19** · T-151 · The checks run before every merge into `develop` — `/kiln:merge`
  runs the repo's checks first and reads GitHub's verdict after; antoine's global instructions
  say so, skill names of 0.4 there too (fix/version-truth) · opened 2026-10-19
- **2026-10-19** · T-150 · `kiln update` rehearsed on a copy first — `kiln update --rehearse`
  (and `--all --rehearse`); the public fixture `antoine-tena/kiln-rehearsal` (Java, v0.3.3-rc.2,
  lived in) rehearsed then updated by the end-to-end tests (fix/version-truth) · opened 2026-10-19
- **2026-10-19** · T-149 · A red check stops the release — `cut` waits for GitHub's CI of the
  release branch and tags only on green; `kiln version` and `promote` hold back a red
  candidate; the session start tells Claude of a red integration branch (fix/version-truth) ·
  opened 2026-10-19
- **2026-10-19** · T-148 · End-to-end tests take the user's path — every release since v0.3.0
  updated through a tool installed by uv, the template at GitHub's address (`insteadOf`); Java
  updated; 0.4 tags rendered under their names; tests out of the machine's Copier cache
  (fix/version-truth) · opened 2026-10-19
- **2026-10-19** · T-04 · Decide whether the adopted repo quotes kiln's workflows at a tag —
  antoine: at a tag. The reference repo quotes `@v0.3.4` (inputs and charter checked
  compatible), the tag moved by hand until T-146 · opened 2026-10-15
- **2026-10-19** · T-23 · Finish kiln in English: the changelog, then the candidate — every
  `CHANGELOG.md` entry in English, the v0.4.0 note with its breaking changes first;
  `v0.4.0-rc.1` cut with `kiln version cut`, `v0.3.4` promoted with `kiln version promote`
  (PyPI, GitHub Release); #36 closed (docs/changelog-en, release/v0.4.0) · opened 2026-10-16
- **2026-10-19** · T-29 · A release in two commands, announced on GitHub — `kiln version cut`
  (release branch in its worktree, changelog entry drafted from the commits, breaking first,
  numbers of the package and of the changed plugins; once the draft is rewritten: checks, tag
  `-rc.N`), `kiln version promote` (tag on the last candidate, `main`, `develop`), the GitHub
  Release made by `pypi.yml`, the plan's open tickets in `kiln version`, `/kiln:release` calls
  them (feat/release-commands) · opened 2026-10-16
- **2026-10-19** · T-27 · The edit hook checks only the edited file — `charter file <path>`:
  the bans on that file alone, in about 0.15 s; ratchets, floors, repo-wide bans and local
  rules left to the commit and CI; the report says how to waive (feat/edit-hook-one-file) ·
  opened 2026-10-16
- **2026-10-18** · Backlog checked against the vision of 17 October 2026 — three tickets
  (T-143 the name, T-144 faster checks, T-145 the benchmark), details added to T-123, T-125,
  T-129, T-30, T-135, T-136, T-138 and T-141; two ideas in reserve declined for now
  ([rejected.md](rejected.md)) (docs/backlog-vision-gaps)
- **2026-10-17** · Backlog rewritten from the vision of 17 October 2026 — kiln keeps repos up to
  date with the best practices and easy for Claude to read, Django and Nuxt first; efforts in
  Claude Code session time on the Pro plan; plan dated up to the launch of v0.5.0 on
  11 November 2026 (T-03); 55 tickets declined for now ([rejected.md](rejected.md)), 20 new
  (T-123 to T-142) (docs/backlog-vision)
- **2026-10-17** · T-52, T-78, T-92, T-93, T-101, T-102, T-103, T-105 · `AGENTS.md`, context
  budget, front tests, database safety, repo hygiene, licences, release notes, backups — merged
  into T-141, as rules of the grid · opened 2026-10-16
- **2026-10-17** · T-95 · `kiln why` and `/kiln:onboard` — `kiln why` merged into T-123
  (`kiln grid RULE-ID`), `/kiln:onboard` declined · opened 2026-10-16
- **2026-10-17** · T-60 · `kiln update --dry-run` and `--undo` — merged into T-126 (`kiln fix
  --dry-run`, the fixes on a branch of their own) · opened 2026-10-16
- **2026-10-17** · T-34 · A second door: kiln for the repo you already have — merged into T-46
  (`uvx kiln-cli score` is that door) and T-30 · opened 2026-10-16
- **2026-10-17** · T-44 · `/kiln:backlog plan` — plan mode puts every ticket in a named release,
  new tickets placed anywhere (feat/backlog-plan, feat/backlog-plan-all); reading the plan from
  `kiln version` moved to T-29 · opened 2026-10-16
- **2026-10-17** · T-31 · Neutral defaults instead of a real project's — time zone from the
  machine, `example.com` placeholders, the Java package asked (feat/template-en) · opened
  2026-10-16
- **2026-10-17** · T-28 · Quiet session hook outside kiln repos — no adoption offer, no
  `.claude/kiln` link, a plain backoff for update reminders (feat/plugin-kiln) · opened
  2026-10-16
- **2026-10-17** · T-25 · Plugin `kiln` with English skills — plugins `kiln`, `django`,
  `nuxt`, `vps` with a `renames` map, English skills and hooks, generated repos on the
  catalogue's `main` (feat/plugin-kiln); plugin versions bumped by the release moved to T-29 ·
  opened 2026-10-16
- **2026-10-17** · T-24 · Generated instructions in `.claude/rules/kiln/`, by path and by size —
  one file per topic, stack rules loaded only on their files, the root `CLAUDE.md` owned by the
  project (feat/template-en) · opened 2026-10-16
- **2026-10-17** · T-22 · Release v0.3.4 and promote v0.3.3 — `v0.3.4-rc.1` cut and `v0.3.3`
  promoted on 16 October (fix/first-run); `v0.3.4` is promoted by the v0.4.0 candidate (T-23) ·
  opened 2026-10-16
- **2026-10-17** · T-08 · Copier migrations for breaking releases — done another way: the
  conversions live in the tool (`migrations.py`, `renames.py`), run by `kiln update` after
  Copier (v0.3.4, feat/template-en) · opened 2026-10-15
- **2026-10-16** · T-26 · A friendlier `kiln new` — three questions (what you are building, size, language), the rest by default or option, `--all-questions` for the whole questionnaire; ends on the next steps and a first prompt (feat/cli-en) · opened 2026-10-16
- **2026-10-16** · T-09 · Tests running in the main tree during a merge — `.claude/worktrees/` in kiln's `.gitignore`, so a template copied from a dirty tree never sees the nested worktrees (fix/first-run) · opened 2026-10-15
- **2026-10-16** · T-06, T-13 · Translation and project language — merged into T-23 · opened 2026-10-15
- **2026-10-16** · T-21 · Credit #41 in the notes of the next release — line in the `v0.3.3` entry of `CHANGELOG.md` (release/v0.3.3) · opened 2026-10-16
- **2026-10-16** · T-20 · Bash completion (`kiln completion bash`) — PR #41 by @HarshRajSinghania, fixed up and merged, issue #40 closed · opened 2026-10-16
- **2026-10-16** · T-18 · Promoting a release makes `kiln update` conflict on `ci.yml` — cause confirmed (Copier's old render takes the promoted tag from `git describe`); the three-way merge is redone with the project's tag, reproduced in a test (fix/conflit-promotion) · opened 2026-10-16
- **2026-10-16** · T-19 · kiln has no pre-push hook — `.pre-commit-config.yaml` (ruff at commit, mypy before push), set by `kiln install` (chore/pre-push-kiln) · opened 2026-10-16
- **2026-10-16** · T-16 · A failed `kiln update --all` leaves a worktree that blocks the next
  run — a worktree with no change and no commit of its own is removed after the failure and
  before the next run; one with work in it is kept and named (`fix/update-reseau`) · opened 2026-10-16
- **2026-10-16** · T-15 · `kiln update --all` crashes with a Python traceback when GitHub is
  unreachable — Copier's git failure becomes one line in the summary, "GitHub injoignable"
  when the network is down (`fix/update-reseau`) · opened 2026-10-16
- **2026-10-16** · T-11 · Publish kiln on PyPI as `kiln-cli` — distribution and `kiln-cli`
  command, install source and update through PyPI, `pypi.yml` on the promotion tag, README;
  the first upload is checked by T-14 · opened 2026-10-16

- **2026-10-16** · T-01 · Promote v0.3.0, the first public release — `v0.3.1-rc.1` cut, then
  `v0.3.0` tagged on the commit of `v0.3.0-rc.1`, merged into `main`, back into `develop`;
  the internal repos moved to `v0.3.1-rc.1` (`kiln update --all`) · opened 2026-10-15
- **2026-10-16** · T-02 · Review PR #39 (`kiln --version`) from an outside contributor —
  reviewed with the new skill `base:contribution`, version computed only on demand (commit
  pushed on top of the contributor's), merged (`b71f91a`), issue #35 closed; credit to add to
  the next changelog entry (T-01) · opened 2026-10-15
- **2026-10-16** · Backlog in English: `docs/a-faire/` becomes `docs/backlog/` (`backlog.md`,
  `rejected.md`, `urgent.md`), `T-NN` tickets with a type and an opening date, skill
  `base:backlog`, status line reading both formats, old trackers converted by `kiln update`
  (`feat/backlog`).
- **2026-10-16** · "Claude Code's workshop" positioning: tagline "Make Claude Code build
  production-grade repos — and keep them that way." (README, `pyproject.toml`, `CLAUDE.md`,
  welcome subtitle), GitHub repo description and topics (`docs/positionnement`).
- **2026-10-15** · Semver in 0.x, candidates (`-rc.N`) and promotion, `interne` channel,
  `kiln version`, workflows quoted at the exact tag, actions at the workflow's commit
  (`feat/semver`); candidate `v0.3.0-rc.1` adopted by the internal repos; gitleaks and
  `workflow_call` brought up from an internal repo into the template (`feat/secrets-scan`).
- **2026-10-15** · Interface (banner, welcome screen, spinner, summary), `kiln doctor`, prefixed
  output of `kiln dev`, debt (typed status line and `charte`), command tests and pytest-xdist,
  English GitHub showcase.
