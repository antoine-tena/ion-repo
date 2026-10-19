# What's new in kiln

One entry per release, the most recent first: `## vX.Y.Z — date`, then one line per visible
change (`- …`), breaking changes first (`**Breaking**`). `kiln update` shows the entries of the
releases a project crosses; `kiln version cut` drafts the entry of the release it cuts, on the
`release/vX.Y.Z` branch, rewritten before its first candidate. Names are those of their release:
entries before v0.4.0 quote kiln's former French names.

## v0.4.0 — 2026-10-19
- **Breaking**: kiln speaks English. `kiln update` converts a generated project in one go, and the names of 0.3 are still read until the next minor.
- **Breaking**: the template's questions are in English (`size`, `name`, `owner`, `team`, `project_type`…); `kiln update` hands Copier the new names and still reads the old answers.
- **Breaking**: the charter is in English: `charte.toml` becomes `charter.toml` (bans, ratchets, floors) and rules take English identifiers. `kiln update` rewrites the file with its budgets and the project's own rules, and the rule identifiers cited in waivers and in the code; an adopted repo keeps its `charte.toml`, read under its French names, and `charte` stays an alias of the `charter` command.
- **Breaking**: commands and options in English: `contrat` → `contract`, `set --poste` → `set --global`, `ci --sauter/--sans-pousser/--garder/--statut` → `--skip/--no-push/--keep/--status`; the old names still work, with a warning.
- **Breaking**: kiln's instructions for Claude move to `.claude/rules/kiln/`: the project and charter rules always loaded, each stack's rules only when Claude touches its files, production and browser security rules from the `ember` size on. The root `CLAUDE.md` now belongs to the project; `kiln update` carries over what the project added to the old one.
- **Breaking**: plugins renamed: `base`, `pile-django`, `pile-nuxt`, `vps-podman` become `kiln`, `django`, `nuxt`, `vps`, with English skill names (`/kiln:merge`, `/kiln:release`, `/kiln:cleanup`, `/kiln:review`, `/kiln:update`, `/kiln:adopt`, `/kiln:report`…). The catalogue moves existing installs to the new names, and the former hook and status line paths keep working.
- **Breaking**: reusable workflows `charter.yml`, `security.yml` and `api-contract.yml`, with English inputs; `charte.yml`, `securite.yml` and `contrat-api.yml` stay as relays, and the old inputs are still accepted. The `kiln ci` note starts with `kiln ci: success` or `kiln ci: failure`; notes of 0.3 are still read.
- **Breaking**: machine settings and status line styles in English (`channel=internal`, `plain`, `band`, `classic`…); the old keys and values are still read in `config.toml` and accepted by `kiln set`.
- `kiln new` in three questions (what you build, the size, the team's language), then the next steps; `--all-questions` for the whole questionnaire.
- Generated code, comments, scripts and workflows in English; what users read (pages, messages, README) follows the project's language.
- The hook after each edit checks the edited file alone (`charter file`, about 0.15 s), and says how to waive a rule; ratchets and floors run at commit and in CI.
- At session start, kiln's logo shows the new release and its main changes above a shorter update question.
- `kiln version cut` and `kiln version promote`: kiln's own release in two commands, with a GitHub Release for each promoted version.
- Only a release of kiln updates a repo: a kiln installed from a checkout ahead of its tag (or with changes, or from a branch) is refused by `kiln update`, `new` and `adopt`, with the command that installs the release, instead of mixing its code with an older template. `kiln --version` says what is installed, not what the checkout became since, and the session start replaces such a tool by the release.
- `kiln update --rehearse` plays the update on a throwaway clone with its checks and only reports, the repo untouched; `kiln update --all --rehearse` does it for every repo.
- At session start, Claude is told when the last CI of the integration branch is red, to say so before any new work.
- `/kiln:merge` runs the repo's checks before merging and reads GitHub's verdict on the merge.
- `kiln update` opens a ticket for what only the team can complete after an update (`After updating:` in a commit), and a backlog ticket can be reserved for one GitHub account.
- `kiln version cut` waits for GitHub's CI of the release branch and tags only on green; `kiln version` and `promote` hold back a candidate whose CI is not green; a fix of a candidate bumps the plugins it touches.

## v0.3.4 — 2026-10-16
- The template is never newer than the installed tool: `kiln update` applies the installed kiln release (conversions from one release to the next live in the tool), refuses to take a repo back to a release older than its own, and says when a newer release is out.
- `kiln new` without `gh`, or outside a terminal without a login, creates the project locally, and `kiln publish` creates the GitHub repository afterwards. The default owner comes from the machine's settings or from the account logged in to gh; a project without a team has neither CODEOWNERS nor a "Team" section.
- The generated CI looks for secrets through the `secrets.yml` workflow (gitleaks pinned and verified, without the license gitleaks-action requires for an organization); `kiln ci` replays it with the machine's gitleaks.
- `kiln` answers in 0.12 s instead of 0.5 s (commands imported on demand); the generated README installs kiln from PyPI.
- Reliability: end-to-end tests (each framework generated, installed and checked; a project of the previous releases updated without conflict), run on every release branch; kiln's CI on macOS too.

## v0.3.3 — 2026-10-16
- `kiln completion bash`: completion script drawn from kiln's commands and options, enabled by `eval "$(kiln completion bash)"` in `~/.bashrc` (#41, thanks @HarshRajSinghania).
- `good-first-issues` skill: keeps a few beginner issues open on GitHub, drawn from the backlog and reserved for outside contributors.
- Fixes: `kiln update` no longer stops on a conflict in `ci.yml` after a release is promoted (only the `@<tag>` of kiln's workflows differed); `base:worktree` no longer trips on a repo without a `.env` file; updating a kiln installed from a folder also removes the former `kiln` tool.

## v0.3.2 — 2026-10-16
- `kiln adopt` makes an existing repo follow kiln, without regenerating it; the `adoption` skill sorts out with the user what the charter finds there, and the session start offers it in a repo of one's own that does not follow kiln yet.
- Charter waivers in `kiln-waivers.toml`, with a reason and a deadline that grows at each renewal: `kiln waive` adds, renews or lists them, `kiln update` spares frozen files and says what it would have changed, `kiln status` counts each repo's.
- `relecture` skill: a branch's commits and diff reviewed and tidied before the merge (`fusion` runs it), the whole repo before a release (`version` runs it); the `garde-branche` hook refuses a commit message signed by Claude.
- kiln's questions at session start follow a common policy: each "no" spaces out the next one, each "yes" brings it closer.
- `kiln --version` (#39, thanks @SakarPaisen, first outside contribution).
- Fixes: `kiln update --all` says "GitHub unreachable" in one line instead of a Python traceback, and a failed run no longer blocks the next one with a worktree left empty.

## v0.3.1 — 2026-10-16
- **Breaking**: work tracking moves to English, `docs/a-faire/` becomes `docs/backlog/` (tickets `T-NN`, skill `base:backlog` instead of `base:a-faire`); `kiln update` moves the old folder.
- Numbering like Claude Code: in 0.x, each release bumps the patch, breaking ones included; the minor only moves for a milestone (`kiln version --minor`). A release is promoted as soon as the next one is ready as a candidate, without a waiting period.
- kiln installs from PyPI: package `kiln-cli` (the command stays `kiln`), published at the tag of each promoted release; `kiln doctor` and `maj-kiln` offer the update that way.
- New skills: `report-to-kiln` (a defect of kiln met in a repo becomes an issue or a PR, posted only with the user's consent), `token` (a service's token in `.<service>/`, pasted without showing), `contribution` (handling an outside contributor's PR).
- The generated CI runs gitleaks and can be called by other workflows (`workflow_call`).
- Status line: four styles in kiln's colours, in English (`kiln set statusline=…`), session name, RAM and busy cores.
- Fixes: `kiln doctor` offers the update at the release's tag, `kiln status` template column wide enough.

## v0.3.0 — 2026-10-15
- First published release. Semver in 0.x: a release first comes out as a candidate (`-rc.N`) for machines on the `interne` channel, then is promoted when the next one is ready and it has held for three days; `kiln version` says where the candidates stand.
- Projects quote kiln's workflows at the exact tag they start from; `kiln update` moves it forward and shows what is new in each release crossed. The session-start hook offers the tool, then the repo, at each release.
- `kiln status` says which release each repo starts from (`f611f82 → v0.3.0`); `kiln set canal=interne` (machine setting) follows the candidates.
- New interface: laughing kiln as a banner, sectioned welcome screen, spinner and duration for each external command, boxed recap of the steps; no colour outside a terminal, `KILN_VERBOSE=1` for the full output.
- `kiln doctor`: diagnosis of the machine and the repo, each problem with the command that fixes it.
- `kiln dev`: servers' output interleaved, prefixed by service in colour.
- `kiln update --all` merges each repo whose checks pass directly, without a PR.
- Java backend (Maven), `maj-kiln` skill, `.claude/kiln` link to the plugin, machine settings through `kiln set`.
