# Backlog

Everything left to do on kiln, in a single list ordered by priority. Started on
**2026-10-15**. What is done is in the "✅ Done" section at the bottom; what was turned
down is in [rejected.md](rejected.md). **Nothing else is open.**

North star: **kiln v0.4.0, in English, launched publicly: pleasant for a Claude Code newcomer,
reliable for a team with huge repos** (free mandate given by antoine, 16 October 2026).

---

## How to use (humans and agents)

**A ticket** = a `### T-NN · Title` heading, then five fixed lines, then the details:

    ### T-NN · Short title that says what to achieve
    - **Type**: task
    - **Status**: todo
    - **Opened**: YYYY-MM-DD
    - **Effort**: S · **Owner**: … · **Due**: —
    - **Origin**: where it comes from

    Why, what to do (as a `- [ ]` checklist when there are several steps), where to look.

- **ID** `T-NN`: stable, never reused, quoted as is in commits and branches (tickets opened
  before 16 October 2026 were `AF-NN`, same number). **Next free: T-32.**
- **Type**, one of: `bug` (something is broken); `improvement` (it works, it could work
  better); `idea` (nothing exists yet, to be explored); `task` (work that is neither: a release,
  a decision, a check).
- **Status**, one of: `todo`; `in progress — branch <name>, since YYYY-MM-DD`;
  `blocked — waiting for <who or what>`; `to verify — <where>`.
- **Priority** = the section the ticket lives in; changing it means moving the ticket.
  🔴 critical (now), 🟠 important (before the north star), 🟡 normal, ⚪ background
  (long-running work, debt, ideas still to be explored).
- **Effort**: XS (under an hour), S (half a day), M (one or two days), L (more).
- **Closing a ticket**: remove it from its section and add a line at the top of the "✅ Done"
  log: `- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.
- **Locations quoted are hints, not addresses.**
- Overview: `grep -E '^(## |### T-|- \*\*Status)' docs/backlog/backlog.md`.
- **Good first issues**: keep 3 open on GitHub, reserved for outside contributors (skill
  `base:good-first-issues`); their tickets have **Owner**: `contributor — #NN`.

---

## 🔴 Critical

### T-14 · Promote v0.3.1, the first release on PyPI
- **Type**: task
- **Status**: blocked — waiting for antoine (delete the old token)
- **Opened**: 2026-10-16
- **Effort**: XS · **Owner**: antoine, then Claude · **Due**: —
- **Origin**: promotion of v0.3.0, 16 October 2026

`v0.3.1` is promoted and `kiln-cli 0.3.1` is on PyPI (16 October 2026); `v0.3.2-rc.2` is the
candidate followed by annway, sweep and vision.
- [x] Cut `v0.3.2-rc.1`, then `-rc.2` (tests independent of the machine's git config); the
  `CHANGELOG.md` entry credits #39 (@SakarPaisen). `kiln update --all` done.
- [x] Promote `v0.3.1`, `pypi` run green, `uvx --from kiln-cli==0.3.1 kiln` works on an empty
  uv cache.
- [x] README (English and French): `uv tool install kiln-cli` as the main install.
- [x] Token scoped to `kiln-cli` in `.pypi/token`, `PYPI_TOKEN` secret updated (16 October
  2026); first used by the promotion of `v0.3.2` (16 October 2026): `kiln-cli 0.3.2` is on
  PyPI. `v0.3.3-rc.2` is now the candidate followed by annway, sweep and vision.
- [ ] antoine deletes the old account-wide token on https://pypi.org/manage/account/token/

### T-22 · Release v0.3.4 (first-run fixes) and promote v0.3.3
- **Type**: task
- **Status**: in progress — branch fix/first-run, since 2026-10-16
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

A newcomer could not get through `kiln new`: owner `antoine-tena` offered by default (taken
silently outside a terminal), immediate failure without `gh`, generated README installing kiln
from git. v0.3.4 fixes the first run; its candidate makes v0.3.3 ready for promotion.
- [x] Template never newer than the installed tool (migrations live in the tool).
- [x] Owner from the machine settings or the gh account; GitHub optional; `kiln publish`.
- [x] `secrets.yml`: gitleaks without the organisation licence of gitleaks-action.
- [x] CLI imports on demand (0.5 s → 0.12 s); T-09.
- [x] End-to-end tests (`pytest -m e2e`): every framework generated, installed, checked; a
  project of the previous releases updated without conflict. CI: release branches, nightly.
- [ ] Cut `v0.3.4-rc.1`, promote `v0.3.3` (PyPI, GitHub Release), `kiln update --all`.

### T-23 · kiln in English (v0.4.0)
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: T-06 and T-13 merged here; plan accepted by antoine, 16 October 2026

Main obstacle to adoption outside France and to the Claude Code directories. Decisions
(antoine, 16 October 2026): the command and the plugins in English only; generated
instructions in English for every project, the project's language only rules what is human
(conversation, comments, commits, docs, UI texts); every rename at once, converted by
`kiln update`; v0.4.0 is the milestone.
- [ ] Command: messages, help, `kiln set` keys; English command and option names
  (`contrat` → `contract`, `--poste` → `--global`, `ci --sauter` → `--skip`…), old ones
  accepted and flagged until the next minor.
- [ ] `copier.yml`: English questions and keys (`envergure` → `size`, `proprietaire` →
  `owner`…), values (`aucun` → `none`…); `language` asked at `kiln new` (en, fr), per-use
  overrides by `kiln set` (comments, commits, docs, tickets, UI).
- [ ] Rule engine `charte` → `charter` (`charter.toml`, English sections, keys and rule IDs);
  `charte`, `charte.toml` and the old IDs still read, so annski (adopted, no update) keeps
  working.
- [ ] Workflows: English names and inputs; the old files stay as relays for `@develop` users.
- [ ] `kiln update` converts a v0.3 project: answers, `charte.toml`, waivers, rule IDs quoted
  in the code, project additions to the old `CLAUDE.md` files carried over.
- [ ] Changelog translated; README, CONTRIBUTING, kiln's own `CLAUDE.md` in English.

## 🟠 Important

### T-03 · Launch kiln publicly, then list it in the Claude Code directories
- **Type**: task
- **Status**: blocked — waiting for T-23 to T-26 and T-30
- **Opened**: 2026-10-15
- **Effort**: S · **Owner**: antoine · **Due**: —
- **Origin**: GitHub showcase, 15 October 2026; "Claude Code's workshop" positioning,
  16 October 2026

antoine's goal: lots of stars. Directories take projects that already have users: the launch
comes first. Hacker News and Reddit: posted by antoine (no API for HN, Reddit vets new apps),
Claude drafts the texts. Elsewhere, Claude posts directly on antoine's accounts, with no review
(antoine's call, 16 October 2026), saying the text is written with Claude where the platform
asks, then gives the links.
- [x] Accounts with an API key, ready (16 October 2026): dev.to (`.devto/`, user
  `antoine-tena`) and Bluesky (`.bluesky/`, `antoine-tena.bsky.social`, app password).
- [ ] On launch day: article on dev.to, post on Bluesky (Mastodon dropped, antoine's call,
  16 October 2026).
- [ ] A demo of `kiln new` at the top of the README (GIF or asciinema, issue #38).
- [ ] Show HN (https://news.ycombinator.com/submit), suggested title "Show HN: Kiln – make
  Claude Code build production-grade repos, and keep them that way".
- [ ] r/ClaudeAI (https://www.reddit.com/r/ClaudeAI/submit) and r/ClaudeCode
  (https://www.reddit.com/r/ClaudeCode/submit).
- [ ] awesome-claude-code (55,000 ★): not before **29 October 2026** (repo at least 14 days
  old, or 100 ★), one recommendation at a time, **through the issue form only** (no PR):
  https://github.com/hesreallyhim/awesome-claude-code/issues/new/choose
- [ ] Anthropic's official directory (claude-plugins-official, loaded by default in Claude
  Code): https://clau.de/plugin-directory-submission — after T-06, French plugins are
  unlikely to get in.

### T-24 · Generated instructions in `.claude/rules/kiln/`, by path and by size
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

A `spark` script got the same ~400-line charter as a `blaze` service, loaded in every session
(OpenTelemetry, SLO, CSP, feature flags…); the size only chose podman. Claude Code now loads
`.claude/rules/*.md` at start, or only when a matching file is touched (`paths:` front matter),
and advises CLAUDE.md files under 200 lines.
- [ ] kiln-owned rules in `.claude/rules/kiln/` (regenerated by `kiln update`, never edited:
  deviations through `kiln waive`), one file per topic, scoped by path (`backend/**`…).
- [ ] The size chooses the rules: `spark` the essentials, `blaze` everything.
- [ ] The root `CLAUDE.md` belongs to the project (generated once): what Claude cannot guess.
- [ ] The size also tunes CI jobs and GitHub protections.

### T-25 · Plugin `kiln` with English skills, released with kiln
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

Public users of the catalogue got `develop` live, and skills are called `/base:fusion`.
- [ ] `base` → `kiln` (`/kiln:worktree`, `/kiln:merge`, `/kiln:release`, `/kiln:cleanup`…),
  `pile-django` → `django`, `pile-nuxt` → `nuxt`, `vps-podman` → `vps`; `renames` map in
  `marketplace.json` so Claude Code migrates existing installs.
- [ ] Plugin versions = kiln version, bumped by the release; generated repos pin the
  catalogue to `main` (`ref`), the released state.
- [ ] Hooks and skills in English; git config keys in English, old ones still read.

### T-26 · A friendlier `kiln new`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

About fifteen Copier questions today. Target: name, what you are building (the stack
follows), size, language; everything else by default or by option. Ends on what to do next
(`cd my-app`, `kiln dev`, `claude`, a first prompt to try) and how to get Claude Code.

### T-30 · README, English reference in `docs/`, demo of `kiln new`
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: T-03 prerequisites; issues #37 and #38

README rewritten around a 60-second start and an animated demo; full reference in `docs/`
(getting started, commands, charter, plugins, workflows, versions) instead of `README.fr.md`.

### T-12 · Homebrew formula in an `antoine-tena/homebrew-kiln` tap
- **Type**: improvement
- **Status**: blocked — waiting for demand (an issue asking for it) or homebrew-core notability
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: distribution, 16 October 2026

`brew install antoine-tena/kiln/kiln` for macOS and Linux, formula updated on each
promotion. Not now (antoine, 16 October 2026): kiln needs uv anyway, so
`uv tool install kiln-cli` covers its users, and a formula lists ~30 dependencies to keep up
to date. The tap https://github.com/antoine-tena/homebrew-kiln is created to keep the name
(README only, issues off). The official homebrew-core requires an already known project.

### T-04 · Decide whether annski quotes kiln's workflows at a tag
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-15
- **Effort**: XS · **Owner**: antoine · **Due**: —
- **Origin**: move to semver, 15 October 2026

annski is adopted (no template) and quotes the workflows at `@develop`: it gets everything that
lands on `develop`, before any candidate. Pinning it to a tag (`@v0.3.0`) would protect it, at
the cost of a manual update on each release. The user's condition: never break annski.

## 🟡 Normal

### T-27 · The edit hook checks only the edited file
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: free mandate (teams with huge repos), 16 October 2026

`controle-fichier.py` runs the whole charter after every edit: on a big repo, seconds per
edit. The hook runs the bans on the edited file only; ratchets and floors run at commit and in
CI.

### T-28 · Quiet session hook outside kiln repos
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

In any repo, at each session, the hook creates `.claude/kiln`, writes to `.git/info/exclude`
and offers to adopt kiln: the shortest way to get a public plugin uninstalled. Outside kiln
repos: nothing. Adoption on request only (`kiln adopt`, `/kiln:adopt`). The goodwill score of
`relances.py` goes; a plain backoff for update reminders stays.

### T-29 · GitHub Release at each promotion, `kiln version` does the mechanical steps
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

A release is a dozen manual steps and no GitHub Release (what watchers and the repo page
show). `pypi.yml` also creates the GitHub Release from the changelog entry; `kiln version`
cuts a candidate (branch, number, changelog skeleton, tag) and promotes one.

### T-31 · Neutral defaults instead of AnnSki's
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: free mandate, 16 October 2026

Europe/Paris in the rules, `.fr` domains, Java package `fr.<name>`, GDPR wording: a time zone
answer (default from the machine), `example.com` placeholders, a Java package derived from the
owner (existing projects keep `fr.<name>`).

### T-05 · Check the first real run of the workflows on GitHub
- **Type**: task
- **Status**: blocked — waiting for GitHub billing (CI stopped)
- **Opened**: 2026-10-15
- **Effort**: XS · **Owner**: Claude · **Due**: —
- **Origin**: actions at the workflow's commit, 15 October 2026

kiln's workflows clone kiln at `job.workflow_sha` (an April 2026 property, unknown to
actionlint) with a fallback to `develop`. On the first run, check that the version taken is the
tag's, and that `.kiln` is removed before the project's checks.

### T-07 · Better support for Java projects
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-15
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: handover of the kiln1 session, 15 October 2026
- [ ] Maven dependency audit in CI (`securite.yml`).
- [ ] `kiln update` bumps the versions in `pom.xml` (today only Dependabot does).
- [ ] `kiln ci` replays `maven.yml`.

## ⚪ Background — long-running work, debt and ideas

### T-08 · Copier migrations for breaking releases
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-15
- **Effort**: M · **Owner**: Claude · **Due**: —
- **Origin**: move to semver, 15 October 2026

In 0.x, any release can break (patch-first numbering, CLAUDE.md "Versions"). Copier can run a migration when a version is crossed
(`_migrations` in `copier.yml`), but `kiln update` runs Copier with `unsafe=False`, so they do
not run: today a migration lives in kiln's Python code, after Copier (see `src/kiln/backlog.py`
for `docs/a-faire/` → `docs/backlog/`). Watch out: Copier deletes a file the template no longer
has even when the repo edited it; its content is still in the last commit.

### T-10 · Interface polish
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-15
- **Effort**: S · **Owner**: Claude · **Due**: —
- **Origin**: interface redesign, 15 October 2026
- [ ] `kiln check`: the step title and the `✓` line say the same thing (one command per step).
- Bash completion moved to T-20.

---

## ✅ Done

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
  annway, sweep and vision moved to `v0.3.1-rc.1` (`kiln update --all`) · opened 2026-10-15
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
  (`feat/semver`); candidate `v0.3.0-rc.1` adopted by annway, sweep and vision; gitleaks and
  `workflow_call` brought up from annway into the template (`feat/secrets-scan`).
- **2026-10-15** · Interface (banner, welcome screen, spinner, summary), `kiln doctor`, prefixed
  output of `kiln dev`, debt (typed status line and `charte`), command tests and pytest-xdist,
  English GitHub showcase.
