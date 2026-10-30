# Rejected

Three kinds, not to be confused.

## Ruled out for good

Final decisions: do not propose them again, even if an audit recommends it.

**2026-10-30**, antoine's decision for the launch: no proof on real repos and no study; v0.5.0
launches on kiln's own repos at 100 and the demos already recorded, none re-recorded.
- T-131 · Proof on two real repos, on local copies
- T-132 · The study: a hundred public Django and Nuxt repos scored (and its idea H01, a labelled
  corpus built from it)

**2026-10-24**, antoine's decision with T-177: kiln's own docs are in English only, in no other
language.
- T-164 · French docs brought up to date at the candidate: no French docs left to translate
- T-55 · README in Chinese, Japanese, Spanish and Portuguese: every translation is a copy to keep
  in step at each release

## Declined for now

**2026-10-26**, reopened by antoine's answers (the backlog's decisions of 26 October 2026): T-37
(Docker accepted beside podman) and T-117 (a VS Code extension) are back in the backlog; T-94
(Windows without WSL) stays declined, `kiln score` only says what to do there (T-189).

**2026-10-17**, when the backlog was rewritten from the vision of that day (antoine's request):
kiln keeps a repo up to date with the best practices and easy for Claude to read, Django and
Nuxt first, small structures first. A ticket below comes back when adopters ask for it (an
issue, a report of T-38), or as a rule of the grid once its theme is covered. Its full text is
in the history of `docs/backlog/backlog.md`.

**Building the product rather than keeping the repo up to date**: Claude Code and the
frameworks build features; kiln keeps the repo they live in at the level of the grid.
- T-32 · From idea to live app: every project type deployable from `kiln new`
- T-35 · Living proof: a site and an example app made by kiln, online
- T-62 · `kiln add <feature>`: features on an existing repo, updated like the rest
- T-63, T-64, T-65, T-67, T-68, T-109, T-110, T-111 · Add-ons `auth`, `email`, `payments`,
  `observability`, `i18n`, `storage`, `realtime`, `search` (observability comes back as rules,
  T-141)
- T-66 · Project type `saas`: accounts, billing, mail and admin, ready on day one
- T-112 · GDPR kit: consent, data export and deletion, privacy page (personal data comes back as
  rules, T-141)
- T-88 · A preview environment for each pull request
- T-89 · `kiln secrets`: one place for secrets, synced where they are needed
- T-97 · `kiln dev --share`: a public URL to show the app running on your machine
- T-104 · A custom domain in one command: DNS, HTTPS, checked
- T-108 · An API reference page served by every backend
- T-96 · `kiln new "…"`: the project described in a sentence

**More templates and project types**: Django and Nuxt first, the other templates frozen (T-133).
Scoring other stacks is not ruled out: stack packs after the launch (decision 1 of 24 October
2026, [the kiln score ideas](backlog.md#-kiln-score-the-thesis)).
- T-07 · Better support for Java projects
- T-36 · `kiln new` recommends the stack, the user decides
- T-79, T-80, T-81 · Project types `mcp`, `agent`, `library`
- T-82 · A TypeScript backend: Hono and Drizzle
- T-83 · SvelteKit and React (Vite) fronts
- T-84 · Go and Rust backends
- T-85 · Mobile apps with Expo
- T-115 · Analysis projects: DuckDB, notebooks run in CI

**The comfort of `kiln new` for a newcomer**: the main door is now `kiln score` on the repo
people already have.
- T-40 · kiln tells you what is possible, once, at the right moment
- T-41 · Beginner with nothing to set, expert with everything settable (each finding of
  `kiln score` already says why and the command that fixes or waives it, T-46)
- T-42 · The git flow grows with the size
- T-43 · A skill that helps write a fine README
- T-48 · A devcontainer in every repo, kiln in Codespaces
- T-49 · `kiln bootstrap`: from a bare machine to the first repo (`uvx kiln-cli` needs only uv)
- T-50 · `kiln new` in under 30 seconds, and offline
- T-51 · SQLite first, PostgreSQL when the project grows
- T-56 · A configurator on kiln's site, and a gallery
- T-100 · Every error message links to its page in the docs
- T-120 · `kiln new --like <repo>`
- T-121 · `kiln uninstall`: the machine left as it was (`uvx kiln-cli score` installs nothing)
- T-47 · `kiln eject` (the fixes are plain commits on a branch; back if organisations ask)
- T-94 · Windows without WSL

**Large companies, not at first**: AWS and Moderne serve them; T-39 brings profiles for
associations, companies of about 50 people and universities.
- T-70 · Org profiles: a company's defaults and rules on top of kiln
- T-86 · Monorepos: several services in one repo
- T-114 · Load tests for big services

**Agent features beyond the roadmap**: Claude gets what needs judgment through
`/kiln:modernize` (T-129) and its unattended run (T-74); tokens are not the product.
- T-72 · `/kiln:feature` and `/kiln:fix`
- T-73 · Subagents per stack
- T-75 · `@claude` in pull requests and issues of generated repos
- T-106 · What a feature cost: tokens per ticket and per repo
- T-71 · `kiln mcp` (the `--json` of `kiln score` stays, T-46)

**Versions, delegated to Dependabot and Renovate** (kiln checks they are set, with a cooldown).
- T-61 · `kiln migrate`: framework major upgrades done by Claude Code
- T-113 · `kiln audit --fix`: vulnerable dependencies fixed on a branch

**The vision's ideas in reserve** (17 October 2026), never opened as tickets: far from keeping
small structures' repos up to date; back once the grid holds.
- Living forks: one's changes kept as intentions with their tests, replayed on each upstream
  release (`kiln update` for any open-source software)
- A financial guarantee on merged code: trust sold as an insured product

**Paths the vision dropped on the way** (17 October 2026):
- A "measured harness" (scoring an agent's configuration): a product centred on agents, not
  kiln's subject, and partly Anthropic's ground
- "Dependabot for the Claude Code configuration": Claude Code's `/doctor` has done it since
  July 2026

## Dropped

- **2026-10-22** · Drop the names and conversions from before kiln 0.4.0 (never a ticket, a
  session's own initiative) — declined by antoine: `plugins/base/` still serves the machine's
  status line (`~/.claude/settings.json`), sweep is still at v0.3.4-rc.1 and calls `charte.yml`,
  `test_e2e.py` updates the `kiln-rehearsal` witness frozen at v0.3.3-rc.2, and the 0.4.0 notes
  promise the relays. Back once no repo of the machine is before 0.4.0, the e2e has no 0.3
  witness and the status line points to `plugins/kiln/`; the work is kept in the local tag
  `archive/drop-pre-040-compat` · opened 2026-10-21
- **2026-10-21** · T-05 · Check the first real run of the workflows on GitHub — dropped by
  antoine; the private probe `antoine-tena/kiln-t05-probe` is left as it is · opened 2026-10-15
