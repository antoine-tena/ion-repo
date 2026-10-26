# Backlog

Everything left to do on kiln, in a single list ordered by priority. Started on
**2026-10-15**, rewritten on **2026-10-17** from the vision of that day (the measures of the two
real repos stay private, see "Repos d'entraînement" in `CLAUDE.md`). Below the tickets: the
[🧭 Vision](#-vision) that orders them, then the [💡 kiln score thesis](#-kiln-score-the-thesis)
that T-186 to T-319 came from. Closed tickets are in [done.md](done.md), what was turned down in
[rejected.md](rejected.md); how to write a ticket: [📖 How to use](#-how-to-use-humans-and-agents).
**Nothing else is open.**

North star: **kiln v0.5.0, launched publicly on Wednesday 11 November 2026: any Django or Nuxt
repo scored in seconds against a sourced grid of today's best practices, brought up to it by
script, the rest handed to Claude Code as a short list** (vision of 17 October 2026: "kiln
keeps a repo up to date with the best of the world, and easy for Claude to read").

**Next free: T-364.**

---

## 🚀 Releases

A candidate every two days, about 4 of its 7 session-hours planned, the rest margin. v0.4.0 to
v0.4.5 went out a week ahead of the first plan: the week won goes to the releases below, and v0.5.0
keeps its date (the launch, T-03). Every open ticket has its release and is listed under it, the
1,070 [kiln score ideas](#-kiln-score-the-thesis) included: each became a box of a ticket (T-186 to
T-319, or the existing ticket it extended) in the release it was planned in (antoine, 25 October
2026: everything a ticket, in one format, in its place). A milestone takes its minor in the release
that reaches it, so the work leading to it carries the minor before: every common stack is v0.7.x,
and v0.8.0 is the release where the last one is scored. Each stack gets two releases, about what
Django and Nuxt each took once the engine is set aside, and its pack holds the rules of its most
used frameworks as well as its language's (framework coverage review of 26 October 2026: Spring
Boot, ASP.NET Core, Laravel, Rails; the Node back ends a release of their own). The stacks come in
the order of the 2025 surveys until the corpus measures its own, and games and R have a release each
(stack coverage review of the same day). From v0.5.4 on, releases carry no date: at this pace v0.6.0
lands in early December 2026, v0.7.0 in mid-April 2027, v0.8.0 at the start of June, v0.9.0 and
v1.0.0 in mid-June 2027. These are consequences of the plan rather than promises, and each release
the launch adds pushes them by two days. The public view of this plan is
[`ROADMAP.md`](../../ROADMAP.md), drawn from this section by `scripts/roadmap.py`.

### Shipped: v0.4.0 to v0.4.9
- v0.4.0 · kiln speaks English: promoted on Mon 19 Oct, the milestone decided by antoine
  (⚠ breaking, all converted by `kiln update`).
- v0.4.1 · The grid, as data: `kiln grid`, 105 drafts from the reference repo.
- v0.4.2 · Any repo scored against the best, in seconds: T-125, T-46, T-157.
- v0.4.3 · What a script can fix, fixed by script: T-126, T-127, T-128.
- v0.4.4 · The rest handed to Claude: T-129, T-161, and most of T-130 (the template's gaps
  closed), promoted on Wed 21 Oct.
- v0.4.5 · Cheaper sessions, CI only at the release: promoted on Fri 23 Oct, with the outside
  fixes #54 to #56 (thanks @NathanBarrachin). Its planned theme slipped: T-90's rest moved to
  v0.4.11, T-130's proof to v0.5.0, T-160 to v0.6.23.
- v0.4.6 · Every issue closed, adoption at full strength: promoted on Mon 26 Oct (urgent, on
  antoine's request: no repo of the code folder runs candidates since they all follow `beta`),
  `kiln adopt` at the level of `kiln new`, #42 to #44 and #58 to #60.
- v0.4.7 to v0.4.9 · pnpm 11 in repos kiln did not make: promoted on Mon 26 Oct, three fixes
  outside the plan (a front without a lockfile, build scripts `allowBuilds` does not list, in
  `kiln install` then in `kiln ci` and the workflows); the planned releases moved by three numbers.

### v0.4.10 · Every gap seen, wherever the code lives
Candidate Tue 27 Oct. The score and the fixes reach what they miss today: GitHub settings, code at
the root as well as in `backend/` and `frontend/`, compose services, loose requirements, files read
as empty.
- T-159 · What T-126 to T-128 left: compose hardening, pyproject from requirements, `kiln update` (M)
- T-158 · `kiln score` reads the GitHub settings when `gh` is logged in (S)
- T-166 · An adopted repo whose code is not in `backend/` or `frontend/` gets its stack too (M)
- T-185 · `kiln dev` in an adopted repo with a compose file offers its services (S)
- T-172 · The checks of `kiln fix` told apart, timed out, their log kept for Claude (S)
- T-173 · More converters: the CI and the supply chain (M)
- T-186 · Binary and non-UTF-8 files read right, GitHub settings read through `gh` (M)
- T-362 · `kiln doctor` calls kiln's own repo "not a kiln repo" (XS)
- T-342 · Not using an agent is not a fault: agent files out of the score (S)
- T-343 · Two habits for every repo: reproduce first, a direct link for every online step (XS)

### v0.4.11 · Never lets it rot, kiln first
Candidate Thu 29 Oct. kiln-bot runs kiln's workflows with write access in other people's repos: each
commit it brings is proven first, and kiln's own workflows pass zizmor and carry provenance before
anyone runs them. kiln-bot on a test repo is a box of the launch gate (T-03).
- T-170 · `kiln fix` proves each commit: its rule closed, no other rule broken (M)
- T-171 · `kiln fix` works in a throwaway worktree, never in the user's tree (S)
- T-59 · kiln-bot: the grid's fixes as a weekly pull request (L)
- T-90 · kiln passes its own grid: zizmor, provenance and Scorecard left (M)
- T-187 · `kiln fix` shows the points each commit won (S)
- T-344 · `/kiln:pause`: a session named and its place kept, listed at the next start (S)

### v0.5.0 · Public launch: the proof and the page
Candidate Sun 1 Nov, promoted Tue 3 Nov. Milestone decided by antoine (16 October 2026), its content
defined on 17 October: the version the launch waits for (T-03). The proof (two real repos, a hundred
public ones, kiln's own repos at 100) and the page that shows it, the potential line as its demo.
- T-131 · Proof on two real repos, on local copies (M)
- T-132 · The study: a hundred public Django and Nuxt repos scored (M)
- T-130 · Generated repos pass the whole grid: the proof left (S)
- T-30 · README and English docs for strangers, with the demo (L)
- T-177 · kiln's own docs in English only (M)
- T-33 · One promise everywhere: tagline, About, PyPI, social preview (S)
- T-119 · GitHub Sponsors and `FUNDING.yml` (XS)
- T-188 · The potential on every run, the frozen templates scored, an honest comparison (M)
- T-360 · The plan renumbered: a minor every ten releases or so (S)
- T-345 · The licence: `MIT OR Apache-2.0`, the template's output free of attribution (S)
- T-346 · "The kiln standard": the grid's public name (S)
- T-347 · A mascot and a logo, still and animated (S) — once antoine has chosen the mascot; not a
  box of the gate

### v0.5.1 · Launch week: the rehearsal, and the bugs already known
Candidate Tue 3 Nov. Fixes only from here to the launch; the week absorbs up to three slipped
releases.
- T-142 · Launch rehearsal: a stranger's first ten minutes, replayed (M)
- T-167 · The branch guard reads the session's folder, not the command's (S)
- T-168 · A repo from `kiln new` + `gh repo create --push` has no CI workflow on GitHub (S)
- T-179 · A new Django repo's tests start without warnings (S)
- T-53 · Readable by Claude, measured: the A/B test (M) — run once, before the launch (antoine,
  26 October 2026); its number joins the launch article only if it is net
- T-145 · A public benchmark: Claude Code with and without kiln (L) — same condition, after T-53

### v0.5.2 · Launch week: what the rehearsal found
Candidate Thu 5 Nov: the fixes of T-142, nothing else.

### v0.5.3 · Launch day
Candidate Sat 7 Nov, promoted on Mon 9 Nov by the next candidate: the version strangers install.
Gate checked on Mon 9 Nov at 20:00; nothing is promoted on launch day.
- T-03 · Public launch: Wednesday 11 November 2026, 16:00 Paris, every forum at once (M)

### v0.5.4 · The first week with strangers
Candidate Mon 9 Nov, promoted after the launch. What the launch brings in (issues, reports, the
first gap reports of T-38) comes first; these give way to it. From here each milestone is
announced (T-118).
- T-118 · Each milestone announced on Bluesky, dev.to, X and Mastodon (S)
- T-153 · `statusline.ci locale`: a French value left in generated repos (S)
- T-10 · Interface polish (S)
- T-99 · `kiln doctor --fix` (S)
- T-98 · Tab completion for zsh and fish (S) (good first issue)
- T-116 · An accessible CLI: `NO_COLOR`, `--plain` (S) (good first issue)
- T-189 · A stranger's first run: no install, never a crash, the next step printed (M)
- T-348 · Opt-in telemetry: which commands run, and how they end (M)
- T-349 · A daily digest mail: issues, pull requests, discussions, gap reports (S)
- T-350 · Launch metrics kept in kiln-private (S) — from launch day: GitHub keeps traffic 14 days

### v0.5.5 · A score you can trust: the false alarms of real repos, gone
Strangers' repos hold fixtures, vendored and generated code, templates, READMEs in other languages:
each class of false alarm is handled once, in the engine, and stays fixed by a test; the reference
repo's score in every note says when the grid moved.
- T-134 · The reference repo's score in every release note (S)
- T-190 · False alarms gone: templates, fixtures, vendored and generated code left out (L)

### v0.5.6 · Show your score
The image that travels by itself, and anyone's repo scored from its URL: the launch's visitors
become its messengers.
- T-154 · Show your score: a badge other repos display (S)
- T-191 · Any repo scored from its URL, a percentile, a Marketplace action (M)
- T-352 · The score as a page: Markdown and Mermaid charts (S)
- T-353 · A leaderboard of the best-scored public repos (S)

### v0.5.7 · Claude pays less per session
Context length is the cost (measured on 22 October): skills that run one kiln command, a ladder
before writing code, context files kept under a budget, the score shown without Claude asking for
it.
- T-163 · Skills call one kiln command, the backlog first (L)
- T-165 · Write less code, measured: a ladder before writing (M)
- T-192 · The score in Claude Code's session, context files under a budget (S)

### v0.5.8 · kiln never makes you wait
The same features, sooner: what was measured slow on 24 October (the suite every release waits for,
the session start, `kiln status`, each Bash call, the install), and the score's own start,
benchmarked in CI.
- T-180 · The test suite renders each set of answers once, copier stops asking git per file (M)
- T-181 · The session start does not wait for GitHub (S)
- T-182 · `kiln status` in half a second (S)
- T-183 · One hook per Bash call instead of two (S)
- T-178 · A lighter install: copier's dependencies trimmed, not fetched later (S)
- T-193 · `kiln score` benchmarked: a startup budget, a lean path, slow candidates stopped (M)
- T-354 · Fast CI: the generated test suites in parallel (M)

### v0.5.9 · Updates you take without reading them
Asked at your pace, applied in one step, proven on real upgrade paths, the score before and after
shown, Claude told what changed in its rules.
- T-45 · Update reminders at the pace you choose (S)
- T-107 · After an update, Claude is told what changed in its rules (S)
- T-54 · Every candidate proven on real upgrade paths (M)
- T-194 · Updates that announce their rules and show the score before and after (M)
- T-355 · The repo's update offered outside Claude Code too (S)
- T-356 · Strangers may follow the candidates; kiln's `develop` gets a channel of its own (S)

### v0.5.10 · `kiln fix`: more gaps closed, faster, from scripts
The code's own rules get converters, the checks run once with a bisection on red, the options
kiln-bot and the skills need; a fresh `kiln new` repo leaves `kiln fix` nothing to do.
- T-174 · More converters: the code (M)
- T-175 · `kiln fix` runs the checks once, then bisects on red (M)
- T-176 · `kiln fix` options: several rules, `--skip`, `--json`, `--pr`, `--dry-run --verify` (M)
- T-195 · Fixes that close and stay closed: `kiln score --fix`, a fix block per rule (M)

### v0.5.11 · Rules that test themselves
Before the grid grows by hundreds of rules: each rule carries its examples, its rung and its message
per place, and `kiln grid new`, `test`, `try` and `lint` make a rule in minutes.
- T-196 · Rules that test themselves: examples in the rule file, `kiln grid new`, `test`, `lint` (L)

### v0.5.12 · Findings where people look
With rules that test themselves (v0.5.11) to build on: in the pull request, the CI's summary and
GitHub's code scanning, written without a flag; repo-local rules in the grid's format.
- T-91 · Findings where people look: SARIF in pull requests and code scanning (M)
- T-197 · Findings in the pull request: locations, fingerprints, annotations, summaries (L)
- T-117 · A VS Code extension (L), reopened on 26 October 2026

### v0.5.13 · The grid grows: the exact rules first, three new themes
T-141 opens here, its other boxes being the theme releases below: the rules a detector decides
exactly today, the first rule of `licensing`, `infrastructure` and `data-science`, and the template
held to every new rule by its own test.
- T-141 · Grid v2: the themes after the launch (L)
- T-198 · The exact rules first, and the template held to each new rule (L)
- T-199 · Three new themes open: licensing, infrastructure, data science (M)
- T-363 · New tools found the week they come out, assessed before recommended (M)

### v0.5.14 · Repos safe to hand to an agent
What Claude Code users need first (17 October): narrow permissions, pinned MCP servers, no secret an
agent can read, model calls with limits; plugins and MCP servers scored as a kind of their own.
- T-200 · Repos safe to hand to an agent: permissions, MCP servers, plugins, hooks (L)
- T-201 · Apps that call a model: keys server-side, current models, validated outputs (L)

### v0.5.15 · The roadmap Claude reads without exploring
The input of v0.6.0: each gap a context pack with its recipe and its proof, ordered by points per
token, cut into batches that fit a session.
- T-202 · The roadmap as context packs: estimated, ordered, batched, budgeted (L)

### v0.5.16 · Tests at the lowest token cost
The other half of v0.6.0: generators that cost no tokens in the template, coverage and surviving
mutants measured by script, Claude on the holes only.
- T-135 · Tests at the lowest token cost, measured on one module first (M)
- T-136 · Test generators that cost no tokens, in the template (M)
- T-203 · Tests that cost no tokens: properties, mutants, API fuzzing, journeys as rules (M)

### v0.5.17 · Strangers' repos run as they are
`kiln dev` brings up any adopted repo without a question, on podman or Docker, whichever the
machine has.
- T-351 · `kiln dev` runs any repo without being told (L)
- T-37 · Docker or podman: the engine the machine has (M), reopened on 26 October 2026

### v0.6.0 · Claude closes the gaps alone
Milestone decided by antoine (16 October 2026: Claude does the work in the repo), its content
re-scoped to the vision: the roadmap worked unattended within a budget, each pull request kept to
its places, the cost of a judgment gap measured, a fix made twice turned into a converter.
- T-74 · The roadmap worked unattended: one gap, one pull request (L)
- T-137 · Claude invents, the script repeats: a fix made twice becomes a converter (M)
- T-204 · The unattended run kept to its places, its verdicts fed back (S)

### v0.6.1 · Less code to carry
The vision's fourth pillar, measured before anything is built: the compressor's dry run, removals
proven by types, tests and behaviour, the slimming rules promoted once precise.
- T-138 · Less code to carry, measured first: the compressor's dry run (M)
- T-139 · The compressor: removals proven by types, tests and behaviour (L)
- T-205 · The slimming rules: dead code, unused dependencies, duplication, a dependency budget (M)
- T-359 · kiln's own engines weighed against existing tools: keep, wrap or replace (M)

### v0.6.2 · Claude in the team's flow
A red CI made green on the machine, the roadmap as issues and good first issues, a summary a human
reads in their language, a file other agents can read too.
- T-76 · `kiln ci --fix`: a red CI made green by Claude Code, locally (M)
- T-206 · The roadmap where the team works: issues, good first issues, other agents (M)
- T-357 · Every agent, or none: the instructions laid for the agent the person uses (L)
- T-358 · The generated flow follows the evidence: trunk-based, pull requests for teams (L)

### v0.6.3 · The grid kept current: its sources watched
Every week the sources are read, the data bundle refreshed, the rules whose sources moved flagged;
each release note carries the grid's diff.
- T-140 · The grid kept current: its sources watched every week (M)
- T-207 · The grid's data dated at each release: end of life, grid diff, consistency, proposals (L)

### v0.6.4 · `kiln new` fits the person
The quick door and the tailored one share the recap and the machine profile: built together.
⚠ breaking: the size question becomes three questions and `--all-questions` gives way to the
tailored mode, both converted by `kiln update`.
- T-169 · `kiln new` asks about your situation, not about tools (L)
- T-184 · `kiln new` tailored: it starts from what you know, then what the project needs (L)

### v0.6.5 · For more people
Tutorials that keep bringing visitors, the roadmap as a GitHub Project, a page per rule where
searches land, the study every quarter, a folder or a zip scored as well as a repo.
- T-57 · A tutorial series: bring a Django repo up to date in an afternoon (M)
- T-58 · A public roadmap on GitHub Projects (M)
- T-208 · A page per rule, and the study every quarter (M)

### v0.6.6 · One answer to "what is this repo"
Score, fix, adopt, dev and check read one model: components with their roles, so a Django rule never
reads `frontend/` and one helper script doesn't make a repo Python.
- T-209 · One model of the repo: components, roles, one answer for every command (L)

### v0.6.7 · Rules per component: versions, tools, evidence
Each fact says where it comes from and how sure it is; rules can say `django >= 4.2` or "your
formatter"; a component is scored alone.
- T-210 · Facts per component: versions, runtimes, tools, evidence, `--facts` (L)

### v0.6.8 · Rules that say what they mean
Applicability as an expression, several ways to meet one practice, conditions across files, evidence
for passes, an honest `unknown`.
- T-211 · Rules that say what they mean: applicability as an expression, `any_of`, `unknown` (L)

### v0.6.9 · Code, not text: the syntax engine
Detectors match syntax trees (ast-grep); Django settings, `nuxt.config`, Dockerfiles and tsconfig
chains are read as they resolve; the false negatives found on 24 October close.
- T-212 · The syntax engine: ast-grep, one parse per file, settings and configs resolved (L)

### v0.6.10 · Mature tools as detectors
ruff, shellcheck and their kin mapped onto grid rules, pinned and cached, never downloaded without
asking; the faster checkers measured against the ones they would replace.
- T-144 · Checks as fast as they are precise: oxlint, TypeScript 7, ty or pyrefly, measured (M)
- T-213 · Mature tools as detectors: ruff and shellcheck, pinned and deduplicated (L)

### v0.6.11 · Instant the second time
One listing from git, one matcher for every rule, a cache keyed by blob SHA: a warm run recomputes
nothing unchanged, in under 50 ms.
- T-214 · Instant the second time: one listing, one index, a cache by blob SHA (L)

### v0.6.12 · Code standards a linter proves
With ruff mapped (v0.6.10), the Python standards it already decides become rules at once, its safe
fixes their converters; shell scripts and encodings come with them.
- T-215 · Python standards ruff already decides: modern syntax, formatting, linting (L)
- T-216 · Error handling, shell scripts and encodings, decided by tools (L)

### v0.6.13 · Secrets and the settings that leak
The secrets themselves, checksum-verified, and the production settings read as they resolve
(v0.6.9): cookies, headers, HTTPS, debug flags, keys in the front.
- T-217 · Secrets in the tree cap the score; session cookies, headers, CSRF (L)
- T-218 · Settings that leak: CORS, passwords, HTTPS, front secrets, debug modes (L)

### v0.6.14 · Precision measured on a thousand repos
A labelled corpus re-scored at every candidate, precision and recall per rule as a release gate, new
detectors in shadow first; the radar moves on that evidence only.
- T-219 · The corpus: precision and recall per rule at every candidate (L)
- T-220 · A quality sheet in every release note (S)

### v0.6.15 · A number that can't lie
Severity orders the gaps, critical findings cap the score at 49 once they are 99 % precise (decision
2), a maybe is never punished, an empty file earns nothing, a report can be verified.
- T-221 · A number that can't lie: severity, the critical cap, confidence, anti-gaming (L)

### v0.6.16 · Locks and installs you can trust
Every lockfile parsed, one practice checked in every ecosystem, every manifest folder covered by the
update bot, installs from the lock in CI and in images.
- T-222 · Locks and installs you can trust: every lockfile, frozen installs, pinned runtimes (L)

### v0.6.17 · Nothing runs that you didn't pin
Install scripts off, one index, tools and hooks pinned, downloads checked, no token in a committed
`.npmrc`, no binary in the tree, an SBOM per release.
- T-223 · Nothing runs unpinned: install scripts, indexes, git dependencies, tools (L)
- T-224 · Nothing downloaded blind: curl pipes, checksums, binaries, tokens in config (M)

### v0.6.18 · What is on its way out, and when it breaks
The calendar of what ends (runtimes, frameworks, runners, model IDs), the `hold` rules that detect
what is leaving, the converters that move it.
- T-225 · What is on its way out: support calendars, hold rules and their converters (L)

### v0.6.19 · Containers built right
Dockerfiles read stage by stage (v0.6.9): the final user, multi-stage builds, secrets at build time,
exec form, images by tag and digest everywhere.
- T-226 · Dockerfiles built right: digests, base images, non-root, stages (L)
- T-227 · Dockerfiles that behave: build secrets, signals, pipefail, one process (L)

### v0.6.20 · Compose files for a small server
What a VPS running compose needs: no engine socket, databases on localhost, logs rotated, limits and
restarts, secrets out of the file, images scanned and signed.
- T-228 · Compose for a small server: hardening, no socket, logs and limits (L)
- T-229 · Compose that survives: restarts, volumes, secrets, scanned and signed images (M)

### v0.6.21 · One CI model, any workflow
Jobs, steps, triggers and permissions extracted once; `make test` resolved into what it runs; zizmor
and actionlint as detectors; the scored CI rules read from that model.
- T-230 · One CI model: every step resolved, injection and privileges on any CI (L)
- T-231 · The scored CI rules read from the CI model (M)

### v0.6.22 · Fast and safe pipelines
Concurrency, caches and retention, supported runners, secrets through `env:`, reusable workflows
pinned, provenance on what ships, the same CI on a laptop.
- T-232 · Fast pipelines: concurrency, caches, runners, actionlint, zizmor (L)
- T-233 · Safe pipelines: secrets through `env`, pinned reusable workflows, provenance (L)

### v0.6.23 · Tests that prove something
Tests per component that assert, run shuffled and in parallel, without network or sleep, coverage
that only rises; a front with no backend gets its smoke test.
- T-160 · A front with no backend ships a smoke test (M)
- T-234 · Tests counted right: presence, clock, network, coverage, strict pytest (L)
- T-235 · Tests that prove something: no sleeps, random order, assertions, names (L)

### v0.6.24 · Progress, not perfection: no new finding
The score of a change, a comparison with any ref, gates on new findings only, scores kept in git
notes and drawn as a curve.
- T-236 · No new finding: history, the score of a change, `--compare`, PR comments (L)

### v0.6.25 · One funnel for every repo, new or old
`kiln adopt` as score, lay, fix, roadmap, its result shown before it runs; baselines for the gradual
path; the template a repo started from recognised; `kiln new` as the same funnel run on an empty
folder.
- T-237 · One funnel for every repo: baselines, `kiln adopt` scored before and after (M)

### v0.6.26 · Only what changed, right after each edit
Tests and score rechecked on the changed files only, on save and in Claude Code's edit hook, in
milliseconds.
- T-77 · Tests in seconds after each edit: only those the change touches (M)
- T-238 · Only what changed: `--changed`, `--watch`, the edit hook (M)

### v0.6.27 · The score explained like a senior engineer would
The denominator, the weakest themes, the effort to 100 in session hours, a verdict in plain words,
`--explain` with this repo's numbers.
- T-239 · The score explained like a senior engineer would (L)

### v0.6.28 · A report you can share
Every format a CI or a tool reads, a one-file HTML report, links to each rule's page and to the line
on the forge, nothing personal left in it.
- T-240 · A report you can share: every format, HTML, `--quiet`, `--porcelain` (L)

### v0.6.29 · Code that can be attacked
Injection, unsafe deserialization, weak crypto, open redirects, SSRF and the rest, with taint
followed inside a function.
- T-241 · Code that can be attacked: taint, permissions, uploads, injections, crypto (L)
- T-242 · Code that can be attacked: redirects, SSRF, paths, escaping, JWT, SAST (L)

### v0.6.30 · Sizes and names, measured in any language
A metrics pass for every language feeds the size and complexity ratchets; names, cases and
misspellings judged from symbol tables.
- T-243 · A metrics pass and misspellings, in any language (S)
- T-244 · Sizes and names measured: files, functions, complexity, naming (L)

### v0.6.31 · Code standards from the syntax tree
What a regex can't tell: modern Vue, explicit imports, floating promises, debug prints, TODOs
without a ticket, barrel files, with oxlint or Biome where they decide.
- T-245 · oxlint or Biome mapped, barrel files counted (S)
- T-246 · TypeScript and Vue standards from the syntax tree (L)

### v0.6.32 · API, contracts and typing
The schema committed and checked for breaking changes, front types generated from it, typing read
through its inheritance and counted as ratchets.
- T-247 · API contracts: the schema committed and frozen, typed routes, pagination (L)
- T-248 · Strict typing everywhere: libraries, annotations, TypeScript options, problem details (L)
- T-249 · Clients and schemas generated, not copied: OpenAPI lint, GraphQL, Protobuf, settings (L)

### v0.6.33 · Architecture you can see
An import graph per language: cycles, layers, sealed domains, god modules, files that always change
together.
- T-250 · The import graph: cycles, feature folders, change coupling (M)
- T-251 · Architecture you can see: thin views, a service layer, sealed domains (L)
- T-252 · Boundaries between front, back and services: stores, async, one database each (L)

### v0.6.34 · Data and migrations
Migrations reversible, safe on a live table, linted in CI, run on the production engine; dumps out
of git; invariants held by the database.
- T-253 · Migrations safe and reversible, linted in CI (L)
- T-254 · Data modelled right: constraints, public IDs, connections, seeds, the real engine in tests
  (L)

### v0.6.35 · Background tasks and concurrency
Tasks that retry, time out, take IDs and run outside the request; increments and locks that survive
two requests at once; Celery's settings made exact.
- T-255 · Background tasks that survive: retries, outbox, idempotence, limits (L)
- T-256 · Schedulers and workers watched: one scheduler, health, visibility, dead letters (M)
- T-257 · Concurrency: atomic updates, locks, timeouts, async servers, Celery made exact (L)

### v0.6.36 · Fast back ends: caches and queries
Real cache backends with timeouts and invalidation, N+1 queries and missing indexes found, latency
budgets kept in the repo.
- T-258 · Caches that invalidate and stay private (L)
- T-259 · Fast back ends: N+1 queries, query counts, indexes, benchmarks (L)

### v0.6.37 · Errors and logs you can follow
Structured logs to stdout, no secret in them and no stack trace shown, errors tracked with their
release, a request ID and traces from the front to the back.
- T-260 · Errors and logs you can follow (L)
- T-261 · Requests traced: request IDs, OpenTelemetry, front errors, an audit trail (M)

### v0.6.38 · An accessible front, in every language
Labels, alt texts, focus, contrast and motion checked in templates and by axe; the European
Accessibility Act's profile; every locale complete.
- T-262 · An accessible front: names, alt text, focus, motion, ARIA (L)
- T-263 · Accessible and translated: headings, contrast, the EU Accessibility Act, i18n keys (L)

### v0.6.39 · A fast, SSR-safe front
Hydration and SSR safety, keys and loading states handled, bundle and image budgets, scripts and
fonts that don't block, SEO basics.
- T-264 · A fast front: Core Web Vitals, budgets, images, fonts, lazy loading (L)
- T-265 · A front that renders safely: UI states, SSR and hydration, SEO, error pages (L)

### v0.6.40 · Deploys you can undo
Services and hosts read from every deploy config; health probes that exist, config that fails fast,
OIDC instead of keys, rollbacks, certificates renewed.
- T-266 · Where it deploys: services and deploy configs read, compression, static files (M)
- T-267 · Deploys you can undo: health probes, config that fails fast, OIDC, graceful shutdown (L)

### v0.6.41 · Production watched, backups restored
A runbook whose commands exist, backups with a restore job, uptime and cron checks, alerts on
symptoms, metrics kept private.
- T-268 · Production that holds: backups restored, runbooks, uptime, recovery targets (L)
- T-269 · Production watched: SLOs, alerts on symptoms, private metrics, dashboards (L)

### v0.6.42 · A tree anyone can find their way in
No build output or artefact committed, a complete `.gitignore`, one config per tool, paths every OS
accepts, small folders.
- T-270 · A tidy tree: the root, the layout, one config per tool, small folders (L)
- T-271 · A tree that checks out anywhere: marked files, no build output, line endings, paths (L)

### v0.6.43 · Docs that tell the truth
Every path, command and link that the README and CLAUDE.md name exists; the map lists every folder;
docs that name what is gone are found.
- T-272 · The map tells the truth: links, the repo map, entry points, decisions (L)
- T-273 · Docs that tell the truth: README, commands, links, docstrings, context files (L)

### v0.6.44 · Set up in one command
One bootstrap command, tasks named in one place, fast commit hooks, tool versions pinned as in CI,
editor settings shared.
- T-274 · Set up in one command: pre-commit, editor files, a task runner, tool versions (L)

### v0.6.45 · Personal data, the GDPR way
Personal fields found in the models and kept out of logs, URLs, fixtures and model calls; the
inventory and the subprocessors written by script; retention and deletion.
- T-275 · Sensitive data found by itself, encrypted, isolated per tenant (M)
- T-276 · Personal data the GDPR way (L)

### v0.6.46 · Money, time, accounts and mail
Amounts in the smallest unit with their currency, dates in UTC, webhooks verified, cards never on
the server, passkeys and rate limits, bulk mail that can be unsubscribed from.
- T-277 · Money, payments and webhooks done right, accounts protected (L)
- T-278 · People's data as given: phones, names, dates, invoices, mail that arrives (L)

### v0.6.47 · History: what every clone carries
Secrets once committed, heavy blobs, locks drifting from their manifests, each blob read once and
cached; hotspots open the roadmap.
- T-279 · History: secrets ever committed, heavy blobs, hotspots (L)

### v0.6.48 · History: how the repo is worked
Commit sizes and messages, merges and branch names, releases and their notes, fixes that come with a
test, all read from history.
- T-280 · History: commit habits, signatures, release rhythm, regression tests (L)
- T-281 · Git and versions rules from history: commits, branches, releases, tags (L)

### v0.6.49 · The forge's settings, read
Through the `gh` already logged in: token permissions, secrets' ages, environments, required checks,
alerts left open, update pull requests ignored.
- T-282 · The forge's settings read: tokens, secrets, alerts, environments, required checks (L)
- T-283 · Repo hygiene on the forge: submodules, CODEOWNERS, force pushes, stale branches (M)

### v0.6.50 · What you depend on, checked at the registry
Real vulnerabilities in the locked versions, malicious and abandoned packages, typosquats, the
provenance of what is published, dependencies' licences, a health card for a new one.
- T-284 · What you depend on, checked at the registry: vulnerabilities, malware, licences (L)

### v0.6.51 · `--deep`: the repo's own checks, in a sandbox
Opt-in, in a throwaway copy with the network off: the install from the lock, the tests (flaky,
order, network, clock), Django's deploy check, type checkers at their strictest, a clean clone.
- T-285 · `--deep`: the repo's own checks in a sandbox (L)

### v0.6.52 · `--deep`: the app built and probed
Images built and scanned, migrations applied and reversed, the API fuzzed, the front rendered for
axe and Lighthouse, the app served and probed, a deployed URL on request.
- T-286 · `--deep`: the app built, served and probed (L)

### v0.6.53 · What the grid doesn't know, shown
Every tracked file claimed by a fact or listed, fingerprints as data from Linguist and SchemaStore,
the gap reports carrying them, corrections counted as signals.
- T-287 · What the grid doesn't know, shown: every file claimed (L)

### v0.6.54 · Never a crash, whatever the repo
Static by default, hardened parsers, linear-time regexes, fuzzed trees, symlinks, untracked and
ignored files handled; zero crashes on the corpus at each candidate.
- T-288 · Never a crash, whatever the repo (L)

### v0.6.55 · Python beyond Django
FastAPI, Flask, SQLAlchemy and every packaging tool read; a new stack's rules count only once ten
corpus repos of it were checked.
- T-289 · Python beyond Django: every packaging tool, FastAPI and Flask (L)

### v0.6.56 · JavaScript beyond Nuxt: the fronts
Every JS framework and package manager read; Next.js, React, React Router, Angular, Vue without
Nuxt, Svelte and Astro each with its pack, Electron and Tauri locked down.
- T-290 · JavaScript beyond Nuxt: every framework and package manager (M)
- T-291 · Framework packs: Next.js, React, Angular, Svelte, Astro (L)

### v0.6.57 · JavaScript beyond Nuxt: the Node back ends
Express, Fastify, NestJS and Hono, the most used back ends after Django's peers, each with its own
release's worth of rules rather than a share of the fronts' (framework coverage review of 26 October
2026).
- T-336 · Node back ends: Express, Fastify, NestJS, Hono (L)

### v0.6.58 · Data science repos
The first outside issues came from data repos: notebooks without outputs or secrets, data out of
git, seeds and environments locked, models loaded safely.
- T-292 · Data science repos: notebooks, data out of git, seeds, locked environments (L)
- T-293 · Data science repos: pipelines, model loading, experiments, Streamlit (L)

### v0.6.59 · Open source done right
A licence that says the same everywhere, notices kept, contributing, conduct and security policies,
issue forms, sponsors, the OpenSSF badge.
- T-294 · Licences right: files, manifests, notices, assets, community health (L)
- T-295 · Open source done right: contributing, conduct, security policy, issue forms (L)

### v0.6.60 · Libraries and CLIs that publish cleanly
Trusted publishing with attestations, complete metadata, one version source, typed exports, packages
that hold what they should and nothing else.
- T-296 · Packages published cleanly: trusted publishing, attestations, contents (L)
- T-297 · Packages that behave: typed exports, engines, one version source, CLIs (M)

### v0.6.61 · Infrastructure as code
Terraform and OpenTofu, Kubernetes and Helm, Ansible: state out of git, versions pinned, buckets
private, pods restricted.
- T-298 · Infrastructure as code: Terraform locked, scanned, private, encrypted (L)
- T-299 · Kubernetes, Helm and Ansible by the book (L)

### v0.6.62 · Every kind of repo
A library, an awesome list, a template, a fork or an archive each held to what it needs; the kind
and what kiln assumed on the report's first lines, with their evidence.
- T-300 · Every kind of repo, each with its rules (L)

### v0.6.63 · GitLab too
Universities and companies often run GitLab: its CI read like GitHub's, its settings through `glab`,
its merge request widget fed.
- T-301 · GitLab too: its CI, its forge, its reports (M)

### v0.6.64 · Profiles read from the repo, never asked
Solo, association, company or university, inferred from signals; criticality raises the bar by
itself; moving up applies the new rules as ratchets.
- T-39 · Profiles of structure: the rules that fit an association, a company, a university (L)
- T-302 · Profiles read from the repo: stages, criticality, team signals (M)

### v0.6.65 · Coursework and research
A course's repos scored on what a student can act on, a teacher's guide, research artefacts that can
be reproduced and cited.
- T-303 · Coursework and research repos (M)

### v0.7.0 · A whole organisation's repos
Milestone decided by antoine (16 October 2026: kiln for teams and organisations), re-scoped to the
vision's targets: a university, an association network, a 50-person company; large companies come
later. Every repo scored remotely without cloning, gaps ranked by how many repos share them.
- T-87 · Fleet view: every repo of an organisation scored, without cloning (M)
- T-304 · A whole organisation's repos: CSV, local scores, organisation packs (M)

### v0.7.1 · Compliance views
What a company has to show: Scorecard, ASVS, SLSA, CIS, WCAG, the Cyber Resilience Act and the
Accessibility Act, each control covered or honestly listed as not checkable.
- T-305 · Compliance views: Scorecard, ASVS, SLSA, the CRA and the EAA (L)

### v0.7.2 · Delivery measured, the organisation's settings read
DORA's four keys from the forge, the bus factor and knowledge islands, two-factor authentication and
base permissions, for organisation profiles.
- T-306 · Delivery measured, the organisation's settings read (M)

### v0.7.3 · The charter and the grid, one engine
Decision 4, before the format freezes: shared detectors first, then the charter as the grid's rules
in strict or ratchet regime, its IDs kept as aliases; rule files checked by a published schema.
⚠ breaking: `charter.toml` lists grid rule IDs with their regime, converted by `kiln update`.
- T-307 · The charter and the grid, one engine (M)

### v0.7.4 · Java and Kotlin repos, read
The road to v0.8.0: every common stack scored and fixed by script as Django is at v0.5.0, stack by
stack (decision 1) in the order the corpus measures (B01; until it does, the order of the 2025
surveys, Stack Overflow's and GitHub's Octoverse). Two releases a stack, about what Django and Nuxt
each took once the engine is set aside: first what its repos are made of, read, so that the rules
spanning stacks see it; then its pack, counted once ten corpus repos of it were checked (B24). Each
stack's rules are written from the corpus when its turn comes. First Java and Kotlin: Maven and
Gradle read with their wrappers, Spring Boot, Quarkus and Micronaut recognised: kiln's own frozen
Java template held to its stack's rules at last.
- T-310 · Java and Kotlin read: Maven, Gradle, Spring Boot, the LTS lines (L)

### v0.7.5 · The Java and Kotlin pack
A supported LTS, a verified wrapper, locked dependencies and a bug finder in the build, then Spring
Boot's own rules, counted once ten corpus repos of Java and Kotlin were checked (B24).
- T-311 · The Java and Kotlin pack (L)
- T-337 · The Spring Boot pack (M)

### v0.7.6 · C# and .NET repos, read
Projects, solutions and central package management read, with nullable references and the supported
.NET lines.
- T-322 · C# and .NET read: projects, central packages, nullable, supported lines (L)

### v0.7.7 · The C# pack
NuGetAudit, lock files, warnings as errors and a pinned SDK, then the rules of ASP.NET Core and
Blazor, counted once ten corpus repos of C# were checked (B24).
- T-323 · The C# pack (L)
- T-338 · The ASP.NET Core and Blazor pack (M)

### v0.7.8 · PHP repos, read
Composer, Laravel, Symfony and WordPress read, with their analysers, formatters, tests and auditor.
- T-312 · PHP read: Composer, Laravel, Symfony, WordPress (L)

### v0.7.9 · The PHP pack
Strict types, `composer audit` in CI, a supported PHP and no `phpinfo()` left, then the rules of
Laravel, Symfony and WordPress, counted once ten corpus repos of PHP were checked (B24).
- T-313 · The PHP pack (L)
- T-339 · The Laravel, Symfony and WordPress pack (M)

### v0.7.10 · C and C++ repos, read
CMake, Meson, Bazel, Conan and vcpkg read, with clang-format, clang-tidy, sanitizers and fuzzing.
- T-327 · C and C++ read: CMake, Meson, Bazel, Conan, vcpkg (L)

### v0.7.11 · The C and C++ pack
Warnings as errors, sanitizers in CI, clang-tidy, fuzzing for parsers and managed dependencies,
counted once ten corpus repos of C and C++ were checked (B24).
- T-328 · The C and C++ pack (L)

### v0.7.12 · Go repos, read
go.mod, go.sum and the toolchain read, with golangci-lint, govulncheck, race tests and wrapped
errors, `go.sum` held to the rules that span stacks.
- T-308 · Go read: modules, toolchains, race tests, errors (L)

### v0.7.13 · The Go pack
Go's own rules with their examples and converters, from a tidy `go.mod` to no `panic` in a library,
counted once ten corpus repos of Go were checked (B24).
- T-309 · The Go pack (L)

### v0.7.14 · Rust repos, read
Cargo, clippy, the edition and `unsafe` read, `Cargo.lock` held to the rules that span stacks.
- T-320 · Rust read: Cargo, clippy, editions, `unsafe`, locks (L)

### v0.7.15 · The Rust pack
Rust's own rules, from clippy with warnings as errors to a declared MSRV, counted once ten corpus
repos of Rust were checked (B24).
- T-321 · The Rust pack (L)

### v0.7.16 · Ruby repos, read
Bundler and Rails read, with RuboCop, Sorbet or RBS, RSpec or Minitest and bundler-audit.
- T-324 · Ruby read: Bundler, Rails, RuboCop, bundler-audit (L)

### v0.7.17 · The Ruby pack
Brakeman and bundler-audit in CI, RuboCop configured, a supported Ruby and no `permit!`, counted
once ten corpus repos of Ruby were checked (B24).
- T-325 · The Ruby pack (L)

### v0.7.18 · iOS, Android and Flutter repos, read
SwiftPM, CocoaPods, the Android manifest and Flutter's pubspec read; App Transport Security and
exported components checked.
- T-314 · iOS, Android and Flutter read: SwiftPM, the manifest, pubspec (L)

### v0.7.19 · The mobile pack
What the stores require and what an app bundle gives away: the privacy manifest, the target SDK, no
server secret in the app, signing keys out of git, counted once ten corpus repos of apps were
checked (B24).
- T-315 · The mobile pack (L)

### v0.7.20 · Game repos, read and packed
Unity, Godot, Unreal and Roblox repos read on top of the C# and C++ packs, with Lua and Luau: the
engine's version pinned, assets in Git LFS, caches and builds out of git, no store or signing
credential committed.
- T-340 · Game repos: Unity, Godot, Unreal, Roblox, Lua (L)

### v0.7.21 · R repos, read and packed
R packages and analyses read and packed in one release: DESCRIPTION and renv, lintr, testthat and R
CMD check, beyond the notebooks the data science release (v0.6.58) reads.
- T-341 · R read and its pack: renv, lintr, testthat, R CMD check (L)

### v0.7.22 · Elixir repos, read and packed
A smaller ecosystem, read and packed in one release: mix and Phoenix, with Credo, Dialyzer, Sobelow
and mix_audit as its rules.
- T-326 · Elixir read and its pack: mix, Phoenix, Credo, Sobelow (L)

### v0.8.0 · Every common stack scored
Milestone decided by antoine (25 October 2026), reached here: every common stack scored and fixed by
script before the format freezes. The rarer languages come as data packs that the community packs of
v1.0.0 will extend; then the gate, the corpus re-scored and each stack among those that make 95 % of
its repos shown at the level of Django at v0.5.0.
- T-329 · The long tail as data packs (M)
- T-330 · Every common stack scored, measured: the corpus's 95 % (M)

### v0.8.1 · The CIs used most after GitHub's and GitLab's
The road to v0.9.0: any CI, any machine, any size, the last before the format freezes. First the CIs
used most after GitHub's and GitLab's (v0.6.63), read into the CI model of v0.6.21 with their
pinning and their untrusted text (appendix B).
- T-316 · The CIs used most after GitHub's and GitLab's: Forgejo, Bitbucket, Azure, CircleCI (L)

### v0.8.2 · Every other CI
Jenkins, Buildkite, Woodpecker, the clouds' own CIs, Tekton and the rest, read the same way.
- T-331 · Every other CI read: Jenkins, Buildkite, Woodpecker, the clouds', Tekton (L)

### v0.8.3 · Every machine, every network
macOS and WSL tested beside Linux, ARM64 and musl, air-gapped and corporate networks; native Windows
only if T-94 reopens.
- T-332 · Every machine and every network: macOS, WSL, ARM64, musl, offline, proxies (L)

### v0.8.4 · No Python needed
A single signed binary, `npx kiln-cli score` for JavaScript machines, and the score in a browser if
the forges allow it; a language server only if T-117 reopens.
- T-333 · No Python needed: a signed binary, npx, the browser (L)

### v0.8.5 · Monorepos and big trees
Monorepo tools' project graphs read for components and their links (T-86 staying declined for
generating them), rules run in parallel, and a time budget that says what it left out.
- T-317 · Monorepos and big trees: project graphs, rules in parallel, a time budget (L)

### v0.8.6 · A million files
Sampling with a stated margin, Rust only where a profile points, then the speed published as uv and
ruff publish theirs.
- T-334 · A million files: sampling, Rust where a profile points, the speed published (L)

### v0.9.0 · Any CI, any machine, any size
Milestone decided by antoine (25 October 2026), reached here, the last before the format freezes:
the bar of v1.0.0 run as a matrix in kiln's own CI, on GitHub's, GitLab's and one more CI, Linux,
macOS and WSL, x86-64 and ARM64, a monorepo and a million files, each scored within its budget.
- T-335 · Any CI, any machine, any size: the bar's matrix, run (M)

### v0.9.1 · Does the score mean anything? Measured, on every stack
The last proof before the stability promise, now that every stack is scored: ten senior engineers'
ranking against kiln's, the score against public repos' incidents, readability against tokens, each
published whatever it says.
- T-318 · Does the score mean anything? Seniors, incidents and tokens, measured (M)

### v1.0.0 · The grid others build on
Milestone decided by antoine (16 October 2026), its bar set on 25 October 2026: the public stability
promise, once the rule format has held without breaking on the stacks that make about 95% of the
corpus's repos (B01), on GitHub's, GitLab's and one more CI, on Linux, macOS and WSL, and on
monorepos, each scored and fixed by script as Django is at v0.5.0; the long tail comes as community
packs (T-69). From here, strict semver: breaking → major, `feat` → minor.
- T-69 · Community grid packs from any git repo (L)
- T-122 · `kiln version` proposes 1.0.0 (S)
- T-319 · The grid others build on: the JSON schema, packs indexed, everything pinned (M)

## 🔴 Critical

## 🟠 Important

### T-362 · `kiln doctor` calls kiln's own repo "not a kiln repo"
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: XS · **Owner**: — · **Due**: before the v0.4.10 candidate (Tue 27 Oct)
- **Origin**: antoine's `kiln doctor` run in kiln, 26 October 2026

`_template` in `src/kiln/doctor.py` warns when `.copier-answers.yml` and the charter are missing,
which is true of kiln itself, the source of the template: a false alarm in the repo antoine
works in most.
- [ ] kiln's own checkout (its `copier.yml` and `template/`) recognized and reported as such, with
  a test; a stranger's repo still gets the warning.

### T-342 · Not using an agent is not a fault: agent files out of the score
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: before the v0.4.10 candidate (Tue 27 Oct)
- **Origin**: antoine's answers of 26 October 2026 (Q42: a developer without Claude must not be
  marked down), decisions 10 and 16 of 26 October

A stranger who codes without an agent must not lose points for it, and the repos known for their
quality (the calibration, T-132) mostly have no agent file. The vision's market section has the
evidence: ETH Zurich finds context files don't raise success and cost 20 to 23 % more tokens.
- [ ] `AI-CONTEXT` out of the score (`assess`), its advice still shown to a repo that uses an
  agent (a `.claude/`, `.cursor/`, `.codex/` or `.gemini/` folder).
- [ ] `REPO-MAP` also reads the map from `README.md`, `CONTRIBUTING.md` and `ARCHITECTURE.md`: a
  map is a human practice first (matklad's ARCHITECTURE.md, 2021).
- [ ] The rules' examples in `tests/test_grid.py` follow; kiln's own score stays at 100.

### T-343 · Two habits for every repo: reproduce first, a direct link for every online step
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q93: which generic parts of his global
  instructions should every repo get? "find them yourself"), decision 35

- [ ] The template's `project.md` gets **[REPRODUCE-FIRST]** (a bug is reproduced, by a failing
  test or a command, before it is fixed; a diagnosis, one's own or another session's, is checked
  on a copy first) and **[DIRECT-LINKS]** (a step asked of a human online comes with its direct
  link, as precise as possible, never a menu path).
- [ ] The commit trailer rule ("never `Co-Authored-By: Claude`") is antoine's taste, not the
  world's way (Q67): it becomes a setting asked at install, "choose for me" meaning disclosure,
  as the AI policies of several large open-source projects now ask; antoine's machine keeps
  "never".
- Not generated, antoine's own: one session at a time, no fleet of subagents, CI only at the
  release, the language of his replies.

### T-345 · The licence: `MIT OR Apache-2.0`, the template's output free of attribution
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: before the v0.5.0 candidate (Sun 1 Nov)
- **Origin**: antoine's answers of 26 October 2026 (Q76: "Apache 2.0 then, I want the best licence
  possible"), decision 28

Apache-2.0 brings a patent grant MIT lacks; offered side by side with MIT, as uv does
(https://docs.astral.sh/uv/reference/policies/license/), it keeps MIT's reach (GPLv2 projects
can take MIT code, not Apache-2.0 code). The cheapest moment is before the launch, while few
outside contributors have code in kiln. antoine said yes to the pair (26 October, follow-up).
- [ ] The three outside authors of kiln's code (@NathanBarrachin: #33, #45, #46, #54 to #56;
  @HarshRajSinghania: #41; @SakarPaisen: #39) are not asked (antoine, 26 October 2026): their
  contributions stay under MIT, as they were given, which the pair allows; `LICENSE-MIT` keeps
  their notice and `CONTRIBUTING.md` says new contributions come under the pair.
- [ ] `LICENSE-MIT`, `LICENSE-APACHE`, `license = "MIT OR Apache-2.0"` in `pyproject.toml` (PEP
  639), the READMEs' licence lines, `CONTRIBUTING.md` (contributions under the same terms).
- [ ] What `kiln new` and `kiln adopt` lay in a repo is the user's: the template's files under
  MIT-0 (no notice to keep), said in the README, so a generated repo carries no kiln licence.

### T-360 · The plan renumbered: a minor every ten releases or so
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: before the v0.5.0 candidate (Sun 1 Nov)
- **Origin**: antoine's yes to decision 23 of 26 October 2026 (Q58: "I don't want too many p in
  vN.m.p")

Long runs of patches (v0.5.17, v0.6.23) are what antoine does not want; uv and ruff move the minor
every few weeks, each minor a themed group holding its breaking changes.
- [ ] `## 🚀 Releases` regrouped into minors of about ten releases, each named for its theme, the
  launch staying v0.5.0; the big milestones (Claude alone, teams, every stack, any CI, 1.0) keep
  their order and get their new numbers.
- [ ] `ROADMAP.md`'s two hand-written milestone tables, `.claude/rules/releases.md`, the vision's
  dates and the tickets' "Planned in" lines follow; `scripts/roadmap.py` rerun.

### T-346 · "The kiln standard": the grid's public name
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: before the v0.5.0 candidate (Sun 1 Nov)
- **Origin**: antoine's answers of 26 October 2026 (Q24, Q176: "standard is the clearest"),
  decision 5

"Grid" says nothing to a stranger; "standard" says what v1.0 promises, the standard others build
on. `kiln score` keeps its name: it scores a repo against the standard (Q113).
- [ ] Every text a user reads says "the kiln standard": READMEs, reference, `kiln score`'s report,
  the rule pages, ROADMAP.md, the launch texts.
- [ ] `kiln standard [RULE-ID]`, with `kiln grid` kept as an alias (cited by older docs and
  skills).
- [ ] The code keeps `grid` (`src/kiln/grid/`), one line in the repo map of `CLAUDE.md` saying so.

### T-177 · kiln's own docs in English only
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: — · **Due**: before the v0.5.0 candidate (Sun 1 Nov)
- **Origin**: antoine, 24 October 2026: several languages, or English only? Answer: English
  only for kiln itself. The public it wants (stars, Hacker News, outside contributors) reads
  English, as with uv, ruff and Bun; the parity between languages doubles every doc change
  (`test_docs.py`, `kiln version cut`; 91 commits touched the French files in October) on a Pro
  plan; and the English reference, the one strangers read, is the one behind (3,510 words
  against 6,072 in French on 24 Oct). antoine reads the docs through Claude, in French, as the
  language rule of 21 Oct already has it.

Not touched: the language of the generated repos (`kiln set language_*`, the `copier.yml`
questions), a feature for French associations and universities (v0.7.0). The French vision
moved into this file, in English, on 24 Oct.
- [ ] Bring `docs/reference.md` up to `docs/reference.fr.md`: every section, command, option,
  setting and example the French one has and the English one lacks, written for strangers.
- [ ] Remove `README.fr.md`, `docs/reference.fr.md` and `ROADMAP.fr.md` (with `scripts/roadmap.py`'s
  French output), and the language line linking them from
  `README.md` and `docs/reference.md`; `CONTRIBUTING.md` no longer asks for both languages.
- [ ] `tests/test_docs.py`: `READMES` and `REFERENCES` down to the English files, the parity test
  between languages removed; `tests/test_plugins.py` follows.
- [ ] `src/kiln/shipping.py`: `DOCS_BY_LANGUAGE` down to the English pair, so `kiln version cut`
  asks for the English README or reference to change (or `<!-- readme: unchanged, why -->`).
- [ ] `CLAUDE.md` (map of the repo, "Le README, entièrement à jour", "Contrôles") and the
  `tout-a-jour` memory: one language for kiln's docs.
- T-164 (French docs translated at the candidate) and T-55 (README in Chinese, Japanese,
  Spanish, Portuguese) ruled out by antoine on 24 Oct (`rejected.md`); T-30 keeps no French
  summary.

### T-166 · An adopted repo whose code is not in `backend/` or `frontend/` gets its stack too
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: issue #59 (antoine, 23 October 2026), what v0.4.6 left

`kiln adopt` lays the common part only when the framework lives elsewhere (a Vite app at the
root, `manage.py` at the root): the template's stack files assume `backend/` and `frontend/`.
- [ ] Where the backend and the front live recorded in the answers (`frontend_dir = "."`), read
  by the template (CI, rules, charter, dependabot) and by `kiln check` and `kiln dev`.
- [ ] Tested for each stack at the root, and for the same repo after `kiln update`.

### T-185 · `kiln dev` in an adopted repo with a compose file offers its services
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: issue #59 (antoine, 23 October 2026): `kiln dev` ran `npm run dev` and
  `npm run server` while the repo's `compose.yaml` had a `web` and a `server` service

- [ ] When a compose file names services that `kiln dev` would also run from `package.json`, the
  menu offers the compose services (as `--containers` does in a generated repo).


### T-163 · Skills call one kiln command, the backlog first
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: antoine, 21 October 2026, after T-162: "skills should use one command line at most"

A skill that runs git, gh and file reads step by step pays each step in tokens and leaves every
output in the conversation, re-read by each later message; a kiln command does the mechanics in
one call and answers in a few lines. The backlog first: one full read costs about 20k tokens
here and 36k in the reference repo, and Claude read it nearly 500 times in three weeks.
- [ ] `kiln backlog next`, `show T-NN`, `add`, `start`, `done`: one ticket in or out, never the
  whole file; `/kiln:backlog` calls them and nothing else.
- [ ] The backlog condensed to what Claude needs (antoine, 26 October 2026: "only for Claude,
  optimize it to the max"): the thesis and appendices whose ideas are all tickets archived, each
  ticket's why in a few lines; tokens measured before and after.
- [ ] Then the mechanical skills, one command each (`merge`, `cleanup`, `worktree`, `update`);
  a skill keeps only what needs judgment.
- [ ] `test_plugins.py`: one shell command per skill at most, the skills that need judgment over
  several commands (`review`, `release`, `contribution`) listed with their reason.

### T-165 · Write less code, measured: a ladder before writing
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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

From the kiln score ideas of 24 October 2026:
- [ ] **N03** Containers started read-only with every capability dropped: a service that still
  starts gets the hardening from `kiln fix` (what T-159 needs).


### T-170 · `kiln fix` proves each commit: its rule closed, no other rule broken
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

`fix.py` promises "with proof", but `_apply` commits as soon as the converter leaves a diff:
it never runs the rule's detector again. kiln-bot (T-59) cannot open pull requests on
strangers' repos until each commit is proven.
- [ ] After each converter, the rule's detector runs again: `fixed` when it passes, `partial`
  when it still fails (the diff is kept, the rest goes to `kiln score --roadmap`), `unchanged`
  when nothing moved.
- [ ] The whole grid compared before and after each commit: a converter that turns another rule
  red (`add_ci` writing an unpinned action, say) is undone and reported.
- [ ] Any exception from a converter is caught, not only `OSError`, `ValueError` and
  `KilnError`: today a `KeyError` or a `yaml.YAMLError` stops the run halfway with a dirty tree
  on the `kiln/fix-…` branch. Tree reset, outcome `unchanged (converter bug)`.
- [ ] A test over every `FIXERS` entry: a second run of the converter changes nothing
  (idempotence).
- [ ] A converter that turns the repo's own tests red leaves the batch: kept on a branch of its
  own with its log and handed to Claude (`/kiln:modernize`), never merged red, never dropped
  silently (decision 21 of 26 October 2026).
- [ ] The summary gives the points each rule brought, not only the score before and after.

### T-171 · `kiln fix` works in a throwaway worktree, never in the user's tree
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

`kiln fix` runs `git switch -c kiln/fix-<date>` in the user's tree, against kiln's own rule (one
worktree per branch, no switch in the main tree): a second run the same day fails on the
existing branch, and a crash leaves the user on a half-done branch.
- [ ] The converters run in a temporary worktree, as `--dry-run` already does; only the branch
  remains, the user's tree is never touched.
- [ ] A dirty tree is no longer refused (the worktree starts from the last commit, said in
  one line).
- [ ] A branch name already taken gets a suffix (`kiln/fix-2026-10-24-2`), or the existing
  branch is updated when it holds only `kiln fix` commits (what kiln-bot needs, T-59).

### T-172 · The checks of `kiln fix` told apart, timed out, their log kept for Claude
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

`run_checks` answers yes or no: no check found, a tool missing and a repo already red before
the run all end up as "unverified", and a reverted converter vanishes without a trace. Goes with
the last box of T-159 (checks found beyond the root).
- [ ] Three cases told apart in the summary: no check found, tool missing (which one, how to
  install it), already red before `kiln fix` (which command).
- [ ] A timeout on each check (a `pytest` waiting for an absent database hangs `kiln fix` today).
- [ ] The output of the check that failed is kept: a reverted converter becomes an entry of
  `kiln score --roadmap`, with the log, for Claude to finish by hand.
- [ ] `yarn` and `bun` recognised besides `npm` and `pnpm`; `typecheck` run when `package.json`
  declares it.

### T-173 · More converters: the CI and the supply chain
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026; 26 `adopt` rules have a
  detector but no converter

The north star says "brought up to it by script": these `adopt` rules are closed by a script
without judgment. Each one with its passing and failing case in `tests/test_fix.py`.
- [ ] WORKFLOW-INJECTION: `${{ github.event… }}` inside a `run:` moved to an `env:` variable
  (what zizmor's fix does).
- [ ] VULNERABILITY-AUDIT: a `pip-audit` or `npm audit` step added to the existing CI.
- [ ] LINT-IN-CI and TESTS-IN-CI: the missing step added to an existing CI (`add_ci` only
  writes one when there is none).
- [ ] NO-TRACKED-ENV: `git rm --cached .env`, the file added to `.gitignore`, a
  `.env.example` with the keys and no values.
- [ ] Ordered by how often the two training repos miss them (measures in `kiln-private`, never
  quoted here).


### T-158 · `kiln score` reads the GitHub settings when `gh` is logged in
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: left from T-46 (2026-10-20)

Branch protection or rulesets on the integration branch, secret scanning and push protection,
Dependabot alerts: read through `gh api` when logged in, left out of the count otherwise (never a
failure for lack of a token).
- [ ] Shown in full on the owner's machine only; what leaves it (the badge, a gap report to kiln,
  the CI summary of a public repo) carries the score and the rule IDs alone, never a setting's
  detail (antoine's question of 26 October 2026, decision 37).

From the kiln score ideas of 24 October 2026:
- [ ] **M15** Forge settings read through the CLI already logged in (`gh`, `glab`, `tea`); a token
  is never asked for (T-158, generalized).

### T-130 · Generated repos pass the whole grid
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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

From the kiln score ideas of 24 October 2026:
- [ ] **P01** `kiln new` proven at 100: every combination of answers (stack, size, options)
  generated and scored at each candidate; a template change that lowers any of them fails (T-130's
  matrix).
- [ ] **T07** kiln, its generated repos and the reference repo at 100, visibly (T-90, T-130, T-134).

### T-90 · kiln passes its own grid: pinned actions, least privilege, provenance, Scorecard
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026: a tool that rewrites
  other people's repos must pass its own grid, visibly

- [x] Third-party actions pinned by SHA in kiln's workflows and actions, their exact version in
  a comment, moved by Dependabot (composite actions included); `permissions: contents: read` on
  every workflow that sets none (23 October 2026, branch `chore/modernize-score`).
- [ ] zizmor in kiln's CI.
- [ ] Build provenance attested on each GitHub Release (`actions/attest-build-provenance`);
  PyPI keeps its token (antoine's preference for a key over a manual setting, 16 October 2026).
- [ ] The OpenSSF Scorecard workflow and its badge.
- [x] `kiln score` on kiln itself in its CI: 100 on every rule (32 of 32, from 77), the release
  CI fails below; the grid's Python rules no longer flag the examples kept in strings (23 October
  2026, branch `chore/modernize-score`).

From the kiln score ideas of 24 October 2026:
- [x] **P14** kiln's own score at 100 gates its release (done on the branch `chore/modernize-score`,
  24 October 2026). (T-90)
- [ ] **S07** Signed releases and data bundles (Sigstore, PyPI attestations; T-90's provenance).

### T-59 · kiln-bot: the grid's fixes as a weekly pull request
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
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

From the kiln score ideas of 24 October 2026:
- [ ] **K19** kiln-bot (T-59) as the effortless default for any public repo: one copy-paste, a
  weekly pull request with the score and `kiln fix`'s commits.
- [ ] **P16** kiln-bot (T-59) posts the delta on each pull request and opens the weekly fix pull
  request.

### T-134 · The reference repo's score in every release note
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (the reference repo as training ground: its score
  measured at each kiln release)

- [ ] `kiln version` runs `kiln score --json` on the reference repo (read-only, its path in a
  machine setting) and on a local copy after `kiln fix`, and writes one line in the release
  entry, such as "Reference repo: 58 → 61, and 74 with `kiln fix`".
- [ ] A drop stops the candidate until it is explained.

From the kiln score ideas of 24 October 2026:
- [ ] **P15** The reference repo's score and its potential after `kiln fix` in every release note
  (T-134).

### T-131 · Proof on two real repos, on local copies
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (validation plan, step 3; two real repos measured)

- [ ] The reference repo (18 of the 31 reference practices applied on 17 October) and a
  university repo built by students since 2023 (an ordinary repo: no CI, no lock, containers
  running as root), each copied locally: `kiln score`, `kiln fix`, their own checks green,
  `kiln score` again, the length of the roadmap.
- [ ] Nothing written or pushed in either original.
- [ ] Results anonymized in `docs/proof/` (no name, no path, nothing that identifies a project);
  the README quotes the before and after.
- [ ] The university repo stays a private test (antoine, 26 October 2026: never cited by kiln,
  not even in aggregate): the launch quotes the reference repo only. One day kiln runs on it and
  its teacher gets a pull request, by antoine's hand.

### T-132 · The study: a hundred public Django and Nuxt repos scored
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (validation steps 1 and 4: the pain on more than two
  repos, then a number to publish); the launch article

- [ ] The selection kept in the script, so anyone can rerun it: about 70 Django and 30 Nuxt
  public repos pushed in the last 90 days, at least 50 stars, no forks, templates or tutorials.
- [ ] Shallow clones in a temporary folder, `kiln score --json --offline` and
  `kiln fix --dry-run`, then the aggregate: median per pillar, most-missed practices, what a
  script closes, the distribution as a chart.
- [ ] **Calibration first** (decision 10 of 26 October): before the hundred, repos known for their
  quality: uv, ruff, Django, FastAPI, Nuxt, and Django apps such as Zulip, NetBox, Saleor,
  Paperless-ngx, Healthchecks and Baserow (Django + Nuxt). Every point they lose is a gap their
  maintainers would recognize, with its source, or a defect of the standard (rule, detector or
  scope) fixed before the launch.
- [ ] `docs/study/2026-11-django-nuxt.md` with the method; the reference repos named with their
  score, the hundred as aggregates, never a list of the worst (decision 11).
- [ ] A vulnerability found (a secret, a dangerous workflow) is reported privately to its
  project (its SECURITY.md or GitHub's private reporting), never in the article nor in a public
  pull request before the fix; the credit in the published advisory is the publicity
  (decision 12).
- [ ] The headline the article and Show HN can use, whatever it turns out to be: "the median
  Django repo applies X % of today's reference practices; a script brings it to Y %, without
  AI, in Z seconds".

From the kiln score ideas of 24 October 2026:
- [ ] **H01** A labelled corpus: T-132's hundred repos as its first version, then 1,000 and 10,000
  public repos sampled by language, size and age, each pinned to a commit, every finding labelled
  true or false.

### T-30 · README and English docs for strangers, with the demo
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
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
- [x] A second tape (24 October 2026, `docs/assets/kiln-rescue.tape`): on the public
  `antoine-tena/kiln-demo-legacy`, a Django app kept deliberately outdated (never a team's
  project shown at fault), `kiln score` 23, `kiln adopt` 39, `kiln fix` 65, the roadmap, a real
  Claude Code on `/kiln:modernize` as a time-lapse (about ten minutes), `kiln score` 100. The
  `kiln new` tape now ends on `kiln score` at 100/100.
- [ ] The kiln-bot pull request in the rescue tape, once kiln-bot exists (T-59).
- [ ] Docs in English in `docs/`: getting started, score, fix, modernize, the grid (one page per
  theme generated from the rule files: the Technology Radar that applies itself), update,
  charter, plugins, workflows, versions, in English only (T-177). Closes #37 and #38 (another
  good first issue opened instead).
- [ ] A comparison page, facts only: what Dependabot and Renovate, Copier and cruft,
  sp-repo-review, OpenRewrite, AWS Transform and Claude Code's `/doctor` do, and what kiln adds
  (from the vision's market table); the r/Python Showcase format asks for it (T-03).
- [ ] `kiln new` second: "Starting a repo? It starts at 100."
- [ ] From the decisions of 26 October 2026: `kiln score` first, then `kiln adopt`, then `kiln new`
  (decision 4); "the kiln standard" (T-346); no Ubuntu image; one line each for `kiln check`,
  `kiln ci` and `kiln score` (decision 40); the review gap as the sourced why (decision 8); the
  score in Lighthouse's bands (decision 6); `uvx` first.
- [ ] The default branch becomes `main` with v0.5.0, so the repo page and `claude plugin
  marketplace add` show what `uvx kiln-cli` installs; pull requests still go to `develop`
  (CONTRIBUTING).

### T-33 · One promise everywhere: tagline, About, PyPI, social preview
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
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
- [ ] The promise covers the trio, `kiln score` first (decision 4 of 26 October): antoine loves
  "Make Claude Code build production-grade repos, and keep them that way" but finds it too much
  about `kiln new`. Draft: "Make any repo production-grade: score it, raise it, keep it there."
- [x] Declined by antoine on 26 October 2026 (Q10), as a title and as a tagline: the analogy
  proposed by Claude on 17 October 2026, reworded on 20 October: **"Dependabot for engineering
  practices."** ("your methods" reads as class methods to an
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
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
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

From the kiln score ideas of 24 October 2026:
- [ ] **L07** A live badge: kiln-bot publishes a shields.io endpoint JSON (Pages or a gist) instead
  of a number frozen in the README (T-154).

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
- **Effort**: M · **Owner**: @antoine-tena · **Due**: 2026-11-09
- **Origin**: launch planned on 17 October 2026 (T-03)

- [ ] On fresh GitHub-hosted runners (Ubuntu, macOS) and in a clean container: the README's
  commands copied as they are, `uvx kiln-cli score` from an empty cache on three public repos of
  the study and three of other stacks (Go, Rust, a JavaScript library), their first screen read
  for anything false, `kiln fix --dry-run` then `kiln fix`, kiln-bot on a throwaway repo; the time
  of each step.
- [ ] First with the people around antoine who already use kiln (about ten, four often), each
  on a repo of their own; then the runners.
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

**Awaiting antoine's decision** (26 October 2026, decision 1): Hacker News restricts Show HN from
new accounts since March 2026 (https://news.ycombinator.com/showlim) and antoine has no HN
account and no Reddit karma. Proposal: 11 November for the forums that need no history (dev.to,
Bluesky, X, Mastodon, LinkedIn, the university mail, awesome-claude-code), HN and Reddit on the
first Wednesday his accounts are accepted, at the latest v0.6.0. Either way, both accounts are
opened at once and used for real, never about kiln (`urgent.md`).

**The version it waits for: v0.5.0**, and what it has to prove:
- [ ] `kiln-cli` 0.5.0 or later promoted on PyPI; `uvx kiln-cli score` works from an empty
  cache on Linux and macOS, on a repo kiln never saw (T-142).
- [ ] `kiln score` deterministic, offline, without a token, under 5 seconds on a 50,000-line
  repo (T-46); `kiln fix` closes every scriptable gap of the two local copies, their checks
  still green (T-126 to T-128, T-131); kiln-bot runs on a test repo (T-59).
- [ ] `kiln score` on ten known public repos of other stacks (Go, Rust, Ruby, Java, PHP,
  TypeScript) says nothing false about tests, CI and linters, and names at the top the language it
  doesn't score yet: a launch's visitors run it on their own repos, not on Django ones. Measured on
  26 October 2026: 8 false alarms in 6 of 10 such repos (no tests found in a Rust and a Ruby repo,
  no linter in CI where clippy, golangci-lint and RuboCop ran), fixed the same day; one class left,
  a linter run by `npm test`'s script, for T-190.
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
  https://news.ycombinator.com/showhn.html). The title is antoine's (he
  declined the Dependabot one on 26 October), `kiln score` first. Then antoine's first comment: why, how it works, the
  method of the study.
- [ ] 16:05: the study as a dev.to article and a thread on Bluesky, X and Mastodon, posted by
  Claude (`.devto/`, `.bluesky/`, `.x/`, `.mastodon/`), the AI disclosure only where the platform
  asks (decision 3).
- [ ] The same day, by antoine: a LinkedIn post written by Claude, and a mail to his university's
  students; Discussions' categories ready (T-58).
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
- [ ] A week later, with the first numbers: Anthropic's plugin directory, one plugin, `kiln`
  (decision 27): https://clau.de/plugin-directory-submission
- [ ] Never: asking for votes, posting from several accounts, the same text twice without a
  canonical URL.

### T-53 · Readable by Claude, measured: the A/B test
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: T-05 probe, 2026-10-21

`plugins/kiln/hooks/branch_guard.py` refused `cd <scratch repo> && git commit` on a branch of
another repo with "never commit on develop": it checks the branch of the session's folder and
ignores a leading `cd` (`git -C` got through). It should judge the repo the command runs in.

### T-168 · A repo from `kiln new` + `gh repo create --push` has no CI workflow on GitHub
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: T-05 probe, 2026-10-21

After the first push, `ci.yml` was not registered (dispatch answered 404 for minutes); a second
commit touching the file registered it. Reproduce with `kiln publish`, then find out whether it
is GitHub's or kiln's doing.

### T-186 · Binary and non-UTF-8 files read right, GitHub settings read through `gh`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, History, forge and
  registries, Trust, privacy and safety), made a ticket on 25 October 2026 at antoine's request

Planned in v0.4.10, "Every gap seen, wherever the code lives": Candidate Tue 27 Oct. The score and
the fixes reach what they miss today: GitHub settings, code at the root as well as in `backend/` and
`frontend/`, compose services, loose requirements, files read as empty.

- [ ] **A30** Binary files skipped on a NUL byte in their first 8 KB; minified files (lines over
  1,000 characters) skipped by code rules but counted.
- [ ] **A31** A non-UTF-8 source decoded (BOM, then cp1252 or latin-1) and reported; never read as
  empty, which passes every regex rule today.
- [ ] **M16** GitHub: rulesets or branch protection on the integration branch (pull requests
  required, checks required, no force push, no deletion), signatures required, linear history when
  the repo merges that way.
- [ ] **M17** GitHub: secret scanning and push protection, Dependabot alerts and security updates,
  code scanning, private vulnerability reporting.
- [ ] **M29** All of it cached and rate-limited, with "unknown: log in with gh to check" without
  access. Never a failure for lack of a token.
- [ ] **S09** Forge tokens borrowed from `gh` or `glab`, never stored, never printed.

### T-187 · `kiln fix` shows the points each commit won
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One measure drives every command), made a ticket
  on 25 October 2026 at antoine's request

Planned in v0.4.11, "Never lets it rot, kiln first": Candidate Thu 29 Oct. kiln-bot runs kiln's
workflows with write access in other people's repos: each commit it brings is proven first, and
kiln's own workflows pass zizmor and carry provenance before anyone runs them. kiln-bot on a test
repo is a box of the launch gate (T-03).

- [ ] **P09** `kiln fix` reports the points each commit won.

### T-188 · The potential on every run, the frozen templates scored, an honest comparison
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, One measure drives every
  command, Docs, teaching and reach), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.0, "Public launch: the proof and the page": Candidate Sun 1 Nov, promoted Tue 3 Nov.
Milestone decided by antoine (16 October 2026), its content defined on 17 October: the version the
launch waits for (T-03). The proof (two real repos, a hundred public ones, kiln's own repos at 100)
and the page that shows it, the potential line as its demo.

- [ ] **I07** The potential on every run: "58 now · 74 after `kiln fix` (no token, about 2 minutes)
  · 100 after the roadmap (12 items, about 3 hours of Claude Code)".
- [ ] **P18** The frozen templates (T-133) scored at each candidate too: frozen doesn't mean
  rotting, and their score goes in the docs.
- [ ] **V04** An honest comparison page: kiln score beside OpenSSF Scorecard, SonarQube, Codacy,
  DeepSource, Snyk, repolinter and the CHAOSS metrics; what each sees and what kiln adds (practices,
  fixes, Claude).
- [ ] **V07** `kiln score` in the README demo's first ten seconds: the number, the potential, `kiln
  fix`, the number again.

## 🟡 Normal

### T-344 · `/kiln:pause`: a session named and its place kept, listed at the next start
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q6: he puts the computer to sleep with several
  sessions open, then no longer knows which one to resume)

- [ ] First, what Claude Code already gives (`/rename`, the `--resume` picker, its session
  titles): kiln adds only what they lack (doctrine 14).
- [ ] `/kiln:pause`, one kiln command (T-163), a few seconds: the session named (repo, branch,
  task in a few words), where it stopped and the next step written to
  `~/.local/state/kiln/sessions/<session id>.json`.
- [ ] At the next session start, in any repo, the paused sessions listed: name, age, next step,
  `claude --resume <id>`; a resumed or merged one leaves the list.

### T-347 · A mascot and a logo, still and animated
- **Type**: idea
- **Status**: blocked — waiting for antoine's choice of mascot
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q28: "a static logo and a dynamic one, I'd love
  it; maybe a small animal, Claude has its crab"), decision 9

The stone-and-fire palette stays. Claude's proposal: a fire salamander, the creature legend puts
in the fire of a kiln. Once chosen:
- [ ] A still logo (SVG, the README, the social preview, the favicon of the docs site) and an
  animated one (the banner of `kiln new`, the GIFs), drawn by `scripts/screenshots.py` like the
  other images.

### T-348 · Opt-in telemetry: which commands run, and how they end
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q96: "yes, we need telemetry!"), reversing
  S05; decision 19

Which commands strangers run, and where they fail, decides what to merge or drop (T-10). Go chose
opt-in after its 2023 debate, and HN's readers judge a launch on it: opt-in it is.
- [ ] Asked once, at install or at the first command, answer "no" by default; `kiln set
  telemetry=on|off`; `KILN_NO_TELEMETRY=1` and CI (`CI=true`) never send.
- [ ] Sent: kiln's version, the command, its outcome and duration, the OS family, the stack; never
  a path, a repo name, a file's content, an identity. A page of the reference lists every field.
- [ ] An existing service with an EU region and a free tier (to choose with sources), no server
  of kiln's (decision 20).

### T-349 · A daily digest mail: issues, pull requests, discussions, gap reports
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q45: "a recap mail would be great; even better,
  a free agent that only receives PRs and issues and mails me an ultra simple recap"), decision 19

- [ ] A scheduled workflow of kiln's repo (free on a public repo), once a day: what opened, what
  waits for antoine, the gap reports (T-38), each in one line with its link; nothing sent on an
  empty day.
- [ ] Written by script first (no tokens); a model's summary only if the script's is not clear
  enough, through a free tier (GitHub Models).
- [ ] The mail account through `/kiln:token` (`.mail/`), the address antoine gives.

### T-350 · Launch metrics kept in kiln-private
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: launch week
- **Origin**: antoine's answers of 26 October 2026 (Q138: "in kiln-private, that would be
  incredible"), decision 31

GitHub keeps a repo's traffic (views, clones, referrers) for 14 days only: what the launch week
brings is lost unless saved.
- [ ] Once a week from the launch, into `kiln-private`: stars, forks, PyPI downloads, GitHub
  traffic and referrers, repos showing the badge (T-154), gap reports (T-38), telemetry's counts
  (T-348).
- [ ] The launch texts, contacts and the questions file live there too, never in kiln.

### T-351 · `kiln dev` runs any repo without being told
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q111: "incredible, but its detection must widen
  so it launches everything without being told"), decision 40

The repos of `kiln adopt` (decision 4) are laid out every way: monorepos, Procfiles, compose
files, `package.json` scripts, Makefiles, Justfiles, devcontainers.
- [ ] Detection from existing work first (doctrine 14): Railpack's and Nixpacks' providers, which
  read how hundreds of stacks start, before any rule of kiln's own.
- [ ] Measured on the corpus (T-132): the share of repos whose servers come up with no question;
  each miss a test.

### T-352 · The score as a page: Markdown and Mermaid charts
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q26: "as visual and colourful as possible: the
  terminal first, then a button that generates lots of visuals in a .md, in Mermaid"), decision 6

- [ ] `kiln score --report`: a Markdown file of Mermaid charts (pillars, themes, gaps by effort,
  the score's history from the git notes), rendered as is by GitHub and GitLab.
- [ ] The terminal shows the number in Lighthouse's bands (0-49 red, 50-89 orange, 90-100 green).

### T-354 · Fast CI: the generated test suites in parallel
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q85: "CI is always the longest, but it matters a
  lot: as complete and fast as possible"; Q112: the reference repo's `kiln ci`, 25 min 59 s of
  which pytest 1,497 s), decision 33

- [ ] The Django template runs pytest across cores (pytest-xdist), with the test settings that cost
  nothing in safety (a fast password hasher, emails in memory); TE19 `PARALLEL-TESTS` promoted.
- [ ] Measured on a copy of the reference repo, before and after; the job's duration in `kiln ci`'s
  verdict.
- [ ] What `kiln ci` does not replay yet, said on 26 October: the end-to-end job (its own
  services), the `infra` and `sbom` workflows.

### T-355 · The repo's update offered outside Claude Code too
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q94: "I'd like kiln's update offers to happen
  without Claude Code too"), decision 35

The tool's own update is offered after a command typed in a terminal, but never to a checkout
like antoine's, which is why he hasn't seen it. The repo's `kiln update` is offered only in a
Claude session.
- [ ] A kiln command typed in a terminal, in a repo behind the latest release, ends by offering
  `kiln update`, at the pace of `update-reminders` (T-45); a yes runs it on a branch and merges it
  when the checks pass, a conflict sends the user to `/kiln:update`.

### T-356 · Strangers may follow the candidates; kiln's `develop` gets a channel of its own
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q119: "yes, they can use the beta too"; Q131),
  decision 35

`develop` takes merges checked by linters only (CI runs at the release): a stranger should get
early releases that passed the whole CI, which the candidates are.
- [ ] `beta` = the candidates, open to anyone (today's `internal`); kiln's own development, the
  editable checkout, moves to `edge`; `kiln update` converts the setting.
- [ ] The reference and `kiln set channel=…`'s help say what each channel gets and risks.

### T-357 · Every agent, or none: the instructions laid for the agent the person uses
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q22: "anyone using an AI should be able to use
  it, even without AI: ask at install which AI CLI, CLAUDE.md for Claude, otherwise AGENTS.md";
  Q72: "yes, with everything"; Q83), decision 26

Being tied to one agent is how kiln could be made useless by an agent's next release (Q190).
AGENTS.md is read by most agents; Claude Code reads CLAUDE.md, which can import it.
- [ ] `kiln install` asks once which agent the person uses (Claude Code, Codex, Cursor, Gemini CLI,
  Copilot, several, none); `kiln new` and `kiln adopt` lay `AGENTS.md` with the rules, and a short
  `CLAUDE.md` that imports it for Claude Code users.
- [ ] What only Claude Code has (skills, hooks, the status line) stays in its plugins; the
  others get the same rules as text.
- [ ] Without an agent: `kiln score`, `kiln fix` and the roadmap written for a person (the
  checklist of T-129 in plain words).

### T-358 · The generated flow follows the evidence: trunk-based, pull requests for teams
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q67: "kiln's skills must match the best way of
  working in the world: not MY way, THE way"; Q169), decision 25

DORA's research ties trunk-based development (short branches merged within a day) to delivery
performance, and git-flow's author advises a simpler flow for software delivered continuously,
which a web app is. The generated repos follow antoine's flow today (`develop`, `main`,
`release/**`, merges without pull requests, CI at the release only).
- [ ] New repos: one long-lived branch (`main`), short branches, releases as tags after the whole
  CI; for team profiles (T-39), a pull request and its CI before each merge.
- [ ] Repos of the old flow keep it until they choose; the conversion offered by `kiln update`.
- [ ] kiln's own repo keeps `develop` and `main` while its channels hang on them (T-356).

### T-359 · kiln's own engines weighed against existing tools: keep, wrap or replace
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q5: "kiln must use as many tools as possible
  that use no tokens, the fastest; invent no tool: go find existing repos on GitHub"), doctrine 14

- [ ] Each engine of kiln's own (`kiln dev`'s process runner, `kiln ci`'s replay, the charter's
  checks, the grid's detectors, `kiln fix`'s converters) set against the maintained tools doing
  the same (process-compose, act, ast-grep, Semgrep, OpenRewrite…): speed, precision, licence,
  upkeep, measured.
- [ ] Kept only where kiln's is better or nothing exists; otherwise wrapped or replaced, one
  ticket each.

### T-37 · Docker or podman: the engine the machine has
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: opened on 16 October 2026, declined on 17 October, reopened by antoine's answers of
  26 October 2026 (Q41: "say podman is highly recommended, but
  not mandatory"), decision 17

Many strangers on macOS have Docker Desktop or OrbStack: refusing them is friction at the first
try. The grid's container rules are engine-neutral already (T-125).
- [ ] `kiln dev`'s backing services and `kiln ci`'s throwaway databases run on podman or Docker,
  whichever the machine has, podman first; `kiln doctor` says podman is recommended, and why
  (rootless, no daemon), without failing on Docker.

### T-117 · A VS Code extension
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: opened on 16 October 2026, declined on 17 October, reopened by antoine's answers of
  26 October 2026 (Q100: "oh yes, that could be good, unless it's
  paid"; Q96: people who can't use a terminal), decision 38

Publishing is free (the VS Code Marketplace and Open VSX, which Cursor and VSCodium read).
- [ ] The score and the findings in the editor, from `kiln score --json` and the SARIF of T-91: a
  finding on its line, its why and its fix one click away; no logic of its own.

### T-174 · More converters: the code
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

The second half of T-173: rules on the code itself, each change proven by the repo's tests.
- [ ] NOQA-CODES and TYPE-IGNORE-CODES: ruff or mypy run, the code of each error read and
  written into the bare comment.
- [ ] JS-LINTER: a minimal flat ESLint config, as `add_ruff` does for Python.
- [ ] HEALTH-PROBES: a `HEALTHCHECK` in the `Dockerfile` when the port and the route are
  obvious, left to judgment otherwise.
- [ ] BARE-EXCEPT: `except:` → `except Exception:`, kept only when the tests stay green.

### T-175 · `kiln fix` runs the checks once, then bisects on red
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

Today the whole test suite runs after each converter: ten rules, ten runs, which kiln-bot pays
in CI minutes (T-59).
- [ ] Every converter applied, one commit each, then the checks once; when red, a bisection
  over the commits finds the culprit, which alone is undone.
- [ ] The network lookups (commit SHAs, image digests) resolved in parallel before the
  converters start.
- [ ] The time saved measured on the two training copies, written in the release note.

### T-176 · `kiln fix` options: several rules, `--skip`, `--json`, `--pr`, `--dry-run --verify`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

- [ ] `--rule` takes several rules; `--skip RULE` leaves some out.
- [ ] `--json`: the outcomes for the CI and the skills (`/kiln:modernize`, kiln-bot).
- [ ] `--pr`: the branch pushed and a pull request opened with the score before and after and
  the why of each commit (the base kiln-bot reuses, T-59).
- [ ] `--dry-run --verify`: the checks run on the throwaway copy too.
- [ ] The references in both languages and the README updated with the options
  (`tests/test_docs.py`).

### T-169 · `kiln new` asks about your situation, not about tools
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: antoine, 24 October 2026: "what should `kiln new` ask to fit the user best?"

Ask only what kiln cannot guess and what really changes the repo, worded the way a senior
engineer would ask a beginner: who uses it, what happens if it breaks, never "Django or
FastAPI?". Today: what you build, the size ("How hot does this one burn?"), the language; the
description defaults to `"{{ title }}."`, so `CLAUDE.md`, the README and the north star start
empty for Claude.
- [ ] "What is it for, in one sentence?" (free text, Enter skips): fills `description`, and the
  north star when `--goal` is not given. The most useful line for Claude per keystroke.
- [ ] The size deduced from three concrete questions instead of the four notches: who uses it
  (me / people I know / the public), who works on it (alone / two or three / several teams), if
  it breaks (nothing serious / annoying / money or data lost); kiln then says "→ Flame".
  `--size` still answers directly.
- [ ] Open source or private: chooses `ci_runner` (GitHub, free for a public repo, else `kiln
  ci`), the licence, the contributor files; today deduced from the visibility, private by
  default.
- [ ] (Only with its effects) what the project handles: user accounts, payments, personal data.
  The template has none of it today (no auth, no privacy rules, no link to the `stripe` plugin):
  the question comes with what it changes (`.claude/rules/kiln/`, `stripe` plugin, grid rules of
  that domain), or not at all.
- [ ] Asked once per machine, not per project (`machine.py`, `kiln set` outside a repo): the
  language, and "Are you a developer?", which sets how much Claude explains and how many
  technical choices it leaves to the user (the promise: "even if you're not one").
- [ ] A recap before generating: type, size, stack, podman, CI, language as deduced, "Enter to
  generate, a number to change": the user sees what was chosen for them.
- [ ] A folder that already holds code: `kiln new` offers `kiln adopt` instead.
- [ ] Not asked, as today: deployment ("None for now", `kiln set deploy=…` later), stack details,
  podman, serena, time zone, `compact_window`, status line, owner and team.
- [ ] `tests/test_questions.py`, the references (both languages), and the demo
  (`docs/assets/kiln-new.tape`) re-recorded.
- [ ] Built with T-184 (the tailored door): one recap, one machine profile for both.

### T-184 · `kiln new` tailored: it starts from what you know, then what the project needs
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine, 24 October 2026: "kiln new should offer two modes: one like today, and
  another with a ton of questions where the user ticks the languages they use most, the same
  for frameworks".

Two doors at the start of `kiln new`: "Quick: 3 questions, kiln picks the rest" (default, made
better by T-169) and "Tailored: your profile, your project, every setting (~5 min)", which
replaces `--all-questions` (today Copier's raw questionnaire). Rule for every question: its
answer changes a generated file, or it is written into a "Project context" section of
`CLAUDE.md`; none is lost. Each question says what it changes, takes "I don't know" (kiln's
default and its reason), and each section can be skipped ("later").

Stage 1, on what the template already has (this ticket's effort):
- [ ] The profile, about the person, kept on the machine (`~/.config/kiln/config.toml`,
  `machine.py`), never in `.copier-answers.yml` (a team repo is not one person's habits):
  languages, then the frameworks of the ticked languages, then databases, JS package manager,
  container engine; three levels per box (know well / a little / want to learn). Filled once,
  used by every `kiln new`, the quick one too; changed by `kiln set profile`.
- [ ] Asked once at install (`kiln install`), at `kiln new` only if never answered (antoine,
  26 October 2026, Q53); with the agent the person uses (T-357) and the profile of structure
  (T-39).
- [ ] Pre-ticked from the repos of the code directory (`fleet.py`): "3 Django repos, 1 Nuxt".
- [ ] "Is this to ship or to learn?": ship recommends within what you know well (React, not
  Vue → Next.js); learn picks a "want to learn" box and makes the Claude rules teach (explain
  each choice, propose before doing).
- [ ] The profile written for Claude too: "knows Python well, new to TypeScript: detail the
  front, be brief on the back".
- [ ] Tools kiln does not generate stay tickable (Go, Rust, PHP, Ruby, C#, Kotlin, Svelte,
  Angular…): "Go: no template yet, report it?", counted with consent like T-38's gap reports,
  to choose the next stacks on facts.
- [ ] Sections: you (ship or learn, developer or not, Claude's autonomy, languages of talk, code
  and commits); the project (purpose in one sentence, type, lifetime); people (who uses it, how
  many in a year, who works on it: the size deduced, not asked); risks (cost of an outage, who is
  told, personal data, money); the stack recommended with its reason and alternatives, the last
  word to the user; operations (where it runs, monthly budget, domain, backups); openness
  (public or private, licence, outside contributions → contributor files, `good-first-issues`);
  kiln's settings (podman, serena, `compact_window`, CI runner, status line, time zone), each
  shown with kiln's choice and why.
- [ ] A numbered recap with the tree about to be generated: Enter generates, a number changes it.
- [ ] Checkboxes in the terminal (questionary or a small menu of ours), with a "1,3,5" fallback
  outside a terminal; a draft kept on Ctrl-C and offered back.
- [ ] `tests/test_questions.py`, the references (both languages), a demo of the profile and the
  recommendation for the README.

Later stages, each its own ticket when planned:
- Stage 2, the features: accounts, emails, payments (the `stripe` plugin), uploads, several
  languages, realtime, search, PWA, accessibility, admin; one at a time, the most ticked first.
  Until one exists, its question only feeds the project context of `CLAUDE.md`.
- Stage 3, the stacks the "not yet" boxes ask for most (Go, Rust, Hono, SvelteKit, Expo…).
- Around: `kiln new --answers <file>` replayed without asking, a team profile exported,
  `kiln new --like <repo>`, `kiln new "<one sentence>"` pre-filling the tailored mode, a local
  form (`kiln new --web`), later an online configurator printing the command.
- Watch: every stack × size × feature must render and pass its checks (`test_template.py`), a
  cost paid at each release; a stack kiln generates but `kiln score` does not grade is said so in
  the recommendation.

### T-179 · A new Django repo's tests start without warnings
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: recording the `kiln new` demo (24 October 2026): `kiln check --all --tests` on a
  fresh Django + Nuxt repo passes with 6 warnings

`UserWarning: No directory at: …/backend/staticfiles/`, raised by WhiteNoise's middleware
(`django/core/handlers/base.py:63`) in each test that builds a request: `STATIC_ROOT` does not
exist before `collectstatic`. A repo kiln has just made should run its tests clean; settle it in
the template (the test settings, or the folder created), not by silencing the warning.

### T-160 · A front with no backend ships a smoke test
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: training on the fleet (2026-10-20): a new `none` + Nuxt, Next or Astro project
  misses TESTS-PRESENT, the only gap left on a fresh repo (`test_template.py` exempts it)

Its only code is constants: a test of them would be filler. The test worth having is a smoke
test of the built site, the home page carrying the site title, through `node --test` (no
dependency): Astro's `dist/index.html`, Next's prerendered `.next/server/app/index.html`, Nuxt
prerendering `/` or its server started. Run after `build` in `ci.yml` and in `kiln check`; then
drop the exemption.

### T-153 · `statusline.ci locale`: a French value left in generated repos
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: the README's recorded demo (20 October 2026) shows `git config statusline.ci locale`

kiln moved to English in 0.4.0, but `apply_statusline_settings` (`src/kiln/statusline.py`) still
writes `locale` for a CI run on the machine, read by the status line script, the session start
hook and `/kiln:merge`. Write `local`, keep reading `locale` (hooks and status line are read from
the main tree by open sessions), convert existing repos in `kiln update`.

### T-45 · Update reminders at the pace you choose
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026; the grid changes at every release

A session opened before an update keeps working by the old rules.
- [ ] The session-start hook says, once, the rules added or changed by the last update (from
  the release notes and the grid's `since`), in three lines at most.

### T-118 · Each milestone announced on Bluesky, dev.to, X and Mastodon
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026; accounts ready (T-03)

A milestone is a reason to be seen again, from the launch on: nothing before it, so the launch
lands as one wave. Only milestones (a new minor) are announced: a post every two days would be
noise (antoine, 26 October 2026, Q131; decision 41); the patch releases go out with their notes.
- [ ] At a milestone's promotion, a short post written from the release notes (what a user
  notices, one link), posted from `.bluesky/`, `.devto/`, `.x/` and `.mastodon/`.
- [ ] The X and Mastodon accounts opened by antoine in kiln's name (`urgent.md`), their tokens
  through `/kiln:token`; Mastodon on an instance for open-source projects.
- [ ] Nothing says "written with Claude" unless the platform asks (decision 3).

### T-91 · Findings where people look: SARIF in pull requests and code scanning
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 for the grid

- [ ] `kiln score --sarif`, uploaded by kiln-bot (T-59) and the charter workflow: findings in
  the pull request diff and in GitHub code scanning.
- [ ] Repo-local rules in the grid's format (`.kiln/grid/`), tested like kiln's; a rule that
  proves useful is proposed to kiln by `/kiln:report`.

From the kiln score ideas of 24 October 2026:
- [ ] **L02** Complete SARIF 2.1.0: rules with `helpUri` to their page, regions,
  `partialFingerprints`, `fixes` for scripted fixes, waivers as `suppressions` with their reason
  (T-91).
- [ ] **R01** Repo-local rules in `.kiln/grid/` (T-91), in the same format, their examples run by
  `kiln grid test`.

### T-54 · Every candidate proven on real upgrade paths
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; the nightly end-to-end run exists since v0.3.4

The promise "kept up to date for as long as the project lives" rests on `kiln update` from any
old release.
- [ ] Repos generated by each of the last five releases updated to the candidate: checks green,
  no conflict marker, a score never lower; a candidate is not promoted otherwise (`kiln version`
  reads the result).
- [ ] The hooks, skills and status line run against the current and the previous Claude Code
  release; `claude plugin eval` suites for the main skills.

### T-180 · The test suite renders each set of answers once, and copier stops asking git per file
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine, 24 October 2026: how to make kiln much faster without changing a single
  feature?

Measured that day on 16 cores: `uv run pytest -q` takes 56 s, every `kiln version cut` waits
for it, and copier's renders are 696 s of the ~900 s the workers spend (77 %). The suite renders
223 times for 164 distinct sets of answers; one render takes 1.0 s alone, 3 to 4 s under the
load of 16 workers.
- [ ] A render cache for the session, keyed by template, `vcs_ref` and answers: each set is
  rendered once, then copied into the test's `tmp_path` (the tests that edit the render keep
  their own copy). 59 renders saved, about a quarter of the render time.
- [ ] Tests that only read the default render share one, per module.
- [ ] Upstream fix in copier: `Worker._sync_git_index_executable_bit` (`copier/_main.py`, 9.18.2)
  runs `git config --type=bool --get core.fileMode` once per rendered file, 62 times per render;
  read once per worker. Measured: 1.01 s → 0.84 s per render (−17 %), which `kiln new` and
  `kiln update` gain too. A pull request to copier, then the version bumped here.
- [ ] Suite time before and after written in the merge commit.

### T-181 · The session start does not wait for GitHub
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: same measurement as T-180, 24 October 2026

`plugins/kiln/hooks/session_start.py` takes 1.3 s at every session start, almost all of it in
one network call, `gh run list --branch develop --limit 20` (1.5 s, the red CI check), made in
sequence. Off the `beta` channel, `git ls-remote` of the update check comes on top of it.
- [ ] The CI verdict read from a cache refreshed in the background (as the status line already
  does with `Popen`), with a short lifetime; the first session of the day may say nothing.
- [ ] Otherwise, at least the network calls run at the same time, not one after the other.
- [ ] Same messages, same cases: `tests/test_session_start.py` unchanged.

### T-182 · `kiln status` in half a second
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: same measurement as T-180, 24 October 2026

`kiln status` takes 1.9 s over 10 repos:
- [ ] 0.36 s to import copier, which `status` never uses: it comes through
  `fleet → adopted → adopted_names → migrations`, which imports it at the top (so does
  `frozen.py`). Imported inside the functions that render; T-178's note that copier is only
  imported by the commands that need it is not true for this path.
- [ ] 0.42 s for `git ls-remote` in `versions.latest_release`, run before the local work: run it
  alongside.
- [ ] ~0.5 s of 23 git calls made one repo after the other: a thread per repo.
- [ ] `kiln update --all` and the other fleet commands get the same import fix for free.

### T-183 · One hook per Bash call instead of two
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: same measurement as T-180, 24 October 2026

Every Bash call of Claude Code waits for two Python processes in a row: `branch_guard.py`
(45 ms) then `rtk.py` (100 ms: two `git config`, then `rtk hook claude`), about 150 ms paid
hundreds of times a session.
- [ ] One `PreToolUse` hook for Bash doing both: one Python start, the git config read once.
  Expected gain 30 to 40 ms per call, measured before and after.
- [ ] The old script names stay as relays: open sessions call the hooks in the main tree
  (`CLAUDE.md`, "Contrôles"), and `tests/test_plugins.py` checks the relays.
- [ ] Left as they are, measured that day: the status line (140 ms, 16 commands in sequence,
  never blocks Claude), `check_file.py` (70 ms), the CLI start (120 ms), `kiln score` (0.4 s),
  `kiln check` (0.8 s), `charter` (0.6 s).

### T-77 · Tests in seconds after each edit: only those the change touches
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (the 23 themes); T-52, T-78, T-92, T-93, T-101, T-102,
  T-103 and T-105 merged here, as rules

Planned box by box: the three new themes in v0.5.13, every other box with its theme's release
in [🚀 Releases](#-releases), as the ideas that carry it.

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
- [ ] Three new themes, each entering `THEMES` with its first rule: `licensing`,
  `infrastructure`, `data-science` (`MODEL-TRACED` moves there); decision 3 of 24 October
  2026 in the [kiln score ideas](#-kiln-score-the-thesis).

### T-140 · The grid kept current: its sources watched every week
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 ("keeping this grid up to date for the whole world is
  permanent work: that is where the value is, and what an agent alone does not do")

- [ ] A weekly job in kiln: endoflife.date, the release notes of the tools the grid names, the
  OSV advisories, the Technology Radar when a volume comes out; flagged: rules whose sources are
  more than six months old, end-of-life dates crossed, release candidates turned stable.
- [ ] One pull request to kiln with the proposed level changes and their sources, decided by the
  doctrine (maturity, sources), never by a count.

From the kiln score ideas of 24 October 2026:
- [ ] **Q02** The weekly watch (T-140) refreshes the bundle and flags the rules whose sources
  changed.
- [ ] **Q16** A rule whose sources nobody re-read for a year leaves the score, back to assess,
  until someone does: the watch (Q02) flags what moved, this catches what nobody looked at, so
  the grid's breadth can't rot silently and a pack nobody keeps goes quiet rather than wrong.

### T-363 · New tools found the week they come out, assessed before recommended
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine, 26 October 2026 ("a technology watch, so that as soon as a tool comes out
  kiln knows"): T-140 watches the tools the grid already names; this finds the ones it doesn't

- [ ] Collection by script, no tokens, once a week: the lines added to the stacks' `awesome-*`
  lists (a diff of their README: curated already), the newsletters' feeds (PyCoder's Weekly,
  Django News, JavaScript Weekly, Vue and Nuxt news), Show HN above a points threshold through
  the Algolia API, the packages whose dependents grow fastest on ecosyste.ms, and the unknown
  packages several gap reports name (T-38). Proven libraries only (`feedparser`, `httpx`, a git
  diff): no crawler of kiln's own.
- [ ] A deterministic filter: already seen (a state file), no stack of kiln's, no licence, no
  release in a year; what is left is a short list, about 5 to 15 a week.
- [ ] A scheduled workflow of kiln's repo (free on a public repo, like T-349) opens or updates one
  issue per week, `Watch, week N`, one line per candidate with its sources; nothing on an empty
  week.
- [ ] Judgment by Claude on that list only, in a normal session (a step of `/kiln:backlog`, or a
  skill of its own): replaces a tool of the grid, completes one, or nothing; a yes becomes a
  ticket or a pull request that adds the rule at `assess`, its sources attached.
- [ ] Known the week it comes out, recommended only on evidence: a new tool enters at `assess`
  and moves to `trial` then `adopt` through T-140's doctrine (maturity, sources, G12's
  `level_history`), never because it is new.

### T-57 · A tutorial series: bring a Django repo up to date in an afternoon
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 for the vision

Tutorials keep bringing visitors long after a launch; a series also tests the path for real.
- [ ] Five parts in `docs/tutorials/`, published on dev.to (`.devto/`), on a public sample repo:
  the score, the fixes, the roadmap with Claude Code, kiln-bot, staying there.
- [ ] Each part replayed at each minor release by a script; a broken step is a bug.

### T-58 · A public roadmap on GitHub Projects
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026

Contributors and users want to see where kiln goes and to weigh in, without reading a Markdown
file.
- [x] `ROADMAP.md` and `ROADMAP.fr.md`, linked from the READMEs: the milestones by hand, the
  releases drawn from `## 🚀 Releases` by `scripts/roadmap.py`, held to it by `tests/test_docs.py`
  (25 October 2026).
- [ ] `docs/backlog/backlog.md` published one way to a GitHub Project (one card per ticket,
  release as a field) by a workflow at each push on `develop`.
- [ ] Discussions (already enabled) with categories: ideas, the grid (a rule to add or to
  challenge), show and tell, questions; linked from the README and from `/kiln:report`.

### T-74 · The roadmap worked unattended: one gap, one pull request
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; builds on `kiln ci`

- [ ] Reads the failed job (GitHub logs or local replay), runs headless Claude Code on a work
  branch with the failure as the prompt, replays the job until green or the budget is spent.
- [ ] Never touches a test to make it pass without saying so in the commit message.

### T-135 · Tests at the lowest token cost, measured on one module first
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (generators without a model first)

- [ ] Schemathesis on the Django Ninja API, Hypothesis for the pure computations (prices,
  dates) with CrossHair as its engine, snapshot tests to freeze behaviour before a modernization, the Playwright recorder for
  the Nuxt journeys; each wired in the template and in `kiln check`, and each a rule of the grid
  (T-141).

### T-137 · Claude invents, the script repeats: a fix made twice becomes a converter
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (doctrine 6)

- [ ] From the log of `/kiln:modernize` (T-129): a rule fixed the same way twice, in one repo or
  across repos (with consent, the circuit of T-38), is proposed as a converter; Claude writes it
  with its tests, a cost paid once per rule instead of once per repo.

From the kiln score ideas of 24 October 2026:
- [ ] **O17** After a modernize session, the points won, tokens spent and items left logged per
  rule: the cost of a judgment gap measured, not guessed (input of T-137 and of the effort
  estimates).

### T-39 · Profiles of structure: the rules that fit an association, a company, a university
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: "the smallest level at creation, and rules that grow with the repo" (antoine,
  16 October 2026); rewritten 17 October 2026 from the vision (doctrine 1: one way per stack
  and per size of structure; risk 4: "the best depends on the context")

- [ ] Profiles: solo or association, a company of about 50 people, a university (student
  projects, labs), large companies later; each rule of the grid says which it fits.
- [ ] More of them (decision 18 of 26 October 2026): student project, teacher, startup, small
  company, freelance delivery (the score as the delivery's certificate), open-source project,
  personal project.
- [ ] The profile read from the repo's answers, otherwise suggested from signals (contributors
  in the last 90 days, a deployment, several services), never imposed: `kiln set profile=…`.
- [ ] Moving to a bigger profile applies the new rules as ratchets on the existing code, never a
  wall of errors.
- [ ] The sizes of `kiln new` (spark, ember, flame, blaze) map onto the profiles.

From the kiln score ideas of 24 October 2026:
- [ ] **A18** Team facts from history: contributors in the last 90 days, commit rhythm, age, last
  activity, code size by language; inputs of the profile (T-39) and of the kind (D).
- [ ] **D04** The profile (T-39) inferred from signals, never asked: owner (person or organisation),
  contributors in 90 days, a deployment, personal data handled, licence, stars, a security policy.

### T-87 · Fleet view: every repo of an organisation scored, without cloning
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 (the vision's targets: a
  university whose student teams change every year, an association network)

- [ ] `kiln status --org <name>`: through the GitHub API, each repo's score, its lag behind the
  grid, its CI and its open security alerts.
- [ ] An HTML report, also produced weekly by a workflow in the organisation's `.github` repo.

From the kiln score ideas of 24 October 2026:
- [ ] **K05** Remote scoring without a clone for L0 and L1 rules: the Git Trees API lists every path
  in one call for most repos, then a few config files are fetched. Seconds, for T-87's fleet view.
- [ ] **P17** The fleet (T-87) scores an organisation's repos remotely (K) and ranks gaps by how
  many repos share them: one fix in kiln helps them all.

### T-122 · `kiln version` proposes 1.0.0
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: milestones decided by antoine, 16 October 2026 (v0.5.0, v0.6.0, v0.7.0, v1.0.0)

In 0.x, `kiln version --minor` only moves to the next minor (`release.py`): nothing proposes
leaving 0.x.
- [ ] `kiln version --stable` proposes `1.0.0` from any 0.x release, says what changes from then
  on (strict semver, breaking → major) and refuses without a `## v1.0.0` note that states the
  promise (what is public API, the grid format included; how long a major is supported).
- [ ] `kiln version` reads the milestones of `docs/backlog/` and says "the next release is the
  v0.6.0 milestone" instead of proposing a patch.

### T-189 · A stranger's first run: no install, never a crash, the next step printed
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every forge, CI, host and
  machine, Nothing to do), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.4, "The first week with strangers": Candidate Mon 9 Nov, promoted after the launch.
What the launch brings in (issues, reports, the first gap reports of T-38) comes first; these give
way to it. From here each milestone is announced (T-118).

- [ ] On Windows without WSL, `kiln score` says what to do (WSL and its link) instead of a
  traceback; T-94 stays declined (decision 38 of 26 October 2026).
- [ ] **A29** Shallow clones, sparse checkouts, partial clones, worktrees, bare repos and submodules
  handled; what wasn't checked out is said, never guessed.
- [ ] **C20** The integration branch read from the remote's HEAD (main, master, develop, trunk),
  never assumed.
- [ ] **K01** One command, no install: `uvx kiln-cli score`. Documented beside it: `pipx run
  --python 3.14 kiln-cli score` (an older Python fails on PEP 758 syntax), Homebrew, a container
  image pinned by digest.
- [ ] **K10** Never a crash: a broken file is a finding, a rule that throws is reported as a kiln
  bug (with `/kiln:report`'s hint), and the run goes on.
- [ ] **K11** The next step always printed as one command: "`kiln fix` closes 5 of these 9 gaps, on
  a branch, no token".
- [ ] **K20** On a machine, `kiln install` (T-161) is the only setup; in a repo, there is none.

### T-190 · False alarms gone: templates, fixtures, vendored and generated code left out
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every forge, CI, host and
  machine, The detection engine, Precision and recall), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.5, "A score you can trust: the false alarms of real repos, gone": Strangers' repos
hold fixtures, vendored and generated code, templates, READMEs in other languages: each class of
false alarm is handled once, in the engine, and stays fixed by a test; the reference repo's score in
every note says when the grid moved.

- [ ] **A05** Templates recognized and kept out of the repo's own stack: `copier.yml`,
  `cookiecutter.json`, `{{ }}` in paths, `.jinja`, `.j2`, `.tmpl` suffixes. kiln's `template/` stops
  making kiln a Django + Nuxt repo.
- [ ] **A06** Fixtures and test data kept out of code rules (`tests/fixtures/`, `testdata/`,
  `__snapshots__/`, `cassettes/`, `*.golden`), still read by the secret rules.
- [ ] **A07** Vendored code recognized (`vendor/`, `third_party/`, `external/`, submodules,
  `*.min.js` in static folders): scored on its own rules (pinned, known vulnerabilities, licence
  kept), never as the repo's code.
- [ ] **A08** Generated code recognized (`@generated`, `DO NOT EDIT`, Go's `Code generated … DO NOT
  EDIT.`, `*.pb.go`, `*_pb2.py`, `*.gen.ts`, OpenAPI clients, Django migrations for size rules):
  left out of style and size rules.
- [ ] **C17** Any human language in the repo: a README found as `LISEZMOI.md` or `README.zh-CN.md`;
  generic-name lists per language (`donnees`, `truc`, `datos`, `daten`); typography that isn't a bug
  (French non-breaking spaces, the doctrine's ruff example); identifiers in any script.
- [ ] **E05** Until the syntax engine lands, `regex` gets `in = "code" | "comments" | "strings" |
  "any"`, from Python's `tokenize` (stdlib) and a small JS/TS tokenizer: the false positives seen on
  kiln vanish with no new dependency.
- [ ] **E06** Path classes instead of hand-written globs: `where = ["code"]`, `["tests"]`,
  `["config"]`, `["docs"]`, `["ci"]`, `["containers"]`, from the model; generated, vendored,
  fixtures and templates left out by default.
- [ ] CI steps that hide their commands followed one level: `npm test` or `make check` read in
  `package.json`'s scripts or the Makefile, a reusable workflow of another repo read at its pinned
  ref (`--online`); until then, a step kiln can't follow leaves the rule `unknown`, never a gap
  (a JavaScript library whose `npm test` runs xo, 26 October 2026).
- [ ] **E07** A policy per rule for tests: `in_tests = "skip" | "lower" | "same"` (SQL built in a
  test is noise; a naive datetime in a test can hide a bug).
- [ ] **H08** Known false-positive classes handled once, in the engine: tests, fixtures, templates,
  examples, code blocks in docs (a README showing the bad way), `.example` files, vendored and
  generated code, migrations, documented sample keys, localhost URLs.
- [ ] **H10** Known false positives closed too: `requires-python = ">=3.9"` read as running 3.9 (a
  library's floor, not its runtime); an app with an empty `models.py`, or one under `tests/`, asked
  for migrations; a lone `.go` file in `docs/` announcing "Go: not covered".
- [ ] **H17** A regression suite of real false positives: each one reported gets a minimal repo in
  `tests/` that must pass forever.

### T-191 · Any repo scored from its URL, a percentile, a Marketplace action
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, Nothing to do, Docs, teaching
  and reach), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.6, "Show your score": The image that travels by itself, and anyone's repo scored
from its URL: the launch's visitors become its messengers.

- [ ] **I09** A percentile against the study's distribution, bundled: "better than 82 % of public
  Django repos" (aggregates only, no repo named).
- [ ] **K04** Any repo by URL: `kiln score github:owner/repo`, `kiln score https://gitlab.com/…`. A
  shallow clone in the cache, scored, deleted; private repos through `gh` or `glab`'s login.
- [ ] **V03** A "kiln score" action on the GitHub Marketplace and a GitLab CI component.
- [ ] **V06** An opt-in showcase of repos at 100, never a ranking of other people's repos by name.

### T-192 · The score in Claude Code's session, context files under a budget
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Nothing to do, AI-assisted development), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.5.7, "Claude pays less per session": Context length is the cost (measured on 22
October): skills that run one kiln command, a ladder before writing code, context files kept under a
budget, the score shown without Claude asking for it.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **K17** Claude Code does the work: the plugin's session start shows the score in one line
  (cached), the status line shows it, the edit hook keeps it. The user only reads.
- [ ] **AI05** `CONTEXT-BUDGET`: CLAUDE.md, the rules it loads and the skills' descriptions under a
  token budget (context length is the cost, measured on 22 October 2026). L1 · ratchet · trial.

### T-193 · `kiln score` benchmarked: a startup budget, a lean path, slow candidates stopped
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Speed), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.8, "kiln never makes you wait": The same features, sooner: what was measured slow on
24 October (the suite every release waits for, the session start, `kiln status`, each Bash call, the
install), and the score's own start, benchmarked in CI.

- [ ] **J01** Measure first: `kiln score --profile` (time per phase: listing, model, each rule,
  output; the ten slowest rules) and a benchmark suite (an empty repo, kiln, a copy of the reference
  repo, a 50,000-file monorepo, a synthetic million-file tree) in CI, with thresholds.
- [ ] **J02** Startup measured (`-X importtime`) and budgeted (80 ms to the first line): `urllib`
  imported only for `--online` (60 ms today), copier and Jinja never imported by `score`.
- [ ] **J03** A lean path: the score's dependencies kept minimal, so `uvx kiln-cli score` downloads
  little on a first run; the template's dependencies only for `new`, `adopt` and `update`.
- [ ] **J21** A candidate more than 10 % slower on the suite waits for an explanation.

### T-194 · Updates that announce their rules and show the score before and after
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, Nothing to do, One measure
  drives every command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.9, "Updates you take without reading them": Asked at your pace, applied in one step,
proven on real upgrade paths, the score before and after shown, Claude told what changed in its
rules.

- [ ] **I11** New `adopt` rules announced one release ahead ("counts from v0.5.7: you meet it", or
  "you will lose 2 points: `kiln fix` closes it"): no score drops overnight.
- [ ] **K16** Offline on a plane: all but `--online` works; the data's date shown, with "12 new
  rules since your version" when the tool is old (`tool_update.py`).
- [ ] **P08** `kiln update` shows the score before and after, and the grid changes that touch this
  repo; a lower score stops the update unless the grid explains it.

### T-195 · Fixes that close and stay closed: `kiln score --fix`, a fix block per rule
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Rule format v2 and
  authoring, Nothing to do, One measure drives every command), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.10, "`kiln fix`: more gaps closed, faster, from scripts": The code's own rules get
converters, the checks run once with a bisection on red, the options kiln-bot and the skills need; a
fresh `kiln new` repo leaves `kiln fix` nothing to do.

- [ ] **F25** The tool that detected becomes the tool that keeps it closed: `kiln fix` adds its
  config and its CI step when missing (ruff, zizmor, pre-commit).
- [ ] **G08** A `fix` block: a converter, a ruff code, or a written recipe for Claude; `safety =
  "safe" | "unsafe"` as ruff marks its fixes.
- [ ] **K12** `kiln score --fix`: score, fix, score again, in one go.
- [ ] **P02** `kiln fix` on a fresh `kiln new` repo changes nothing; when it does, the template is
  behind the grid.

### T-196 · Rules that test themselves: examples in the rule file, `kiln grid new`, `test`, `lint`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Rule format v2 and
  authoring, Precision and recall, Outputs and integrations), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.11, "Rules that test themselves": Before the grid grows by hundreds of rules: each
rule carries its examples, its rung and its message per place, and `kiln grid new`, `test`, `try`
and `lint` make a rule in minutes.

- [ ] **E01** The ladder: L0 paths and names (microseconds), L1 structured files (TOML, JSON, YAML,
  INI, XML, HCL, Dockerfile, ignore files), L2 syntax patterns, L3 cross-file (imports, calls,
  references), L4 external tools, L5 git history, L6 forge and registry APIs, L7 running the code.
  Each rule declares its rung, each finding says which one found it.
- [ ] **E22** `kiln grid` lints every pattern for catastrophic backtracking when the grid loads.
- [ ] **G01** Examples inside the rule file (`[[examples]]` with `expect` and inline files): the
  grid tests itself, packs ship tested rules, and `tests/test_grid.py` reads them instead of its
  `CASES`.
- [ ] **G02** Several examples per rule, edge cases included; every false positive ever reported
  becomes a `pass` example, so it never comes back.
- [ ] **G07** A `message` per place with placeholders (`{image} is named by tag: pin it as
  {image}@sha256:…`): the finding says what to do right there.
- [ ] **G17** `kiln grid new ID` scaffolds a rule and its examples; `kiln grid test [ID]` runs the
  examples; `kiln grid try ID --on <repo>` runs one rule with its timing.
- [ ] **G18** `kiln grid lint`: patterns that can backtrack, unknown facts, missing examples, stale
  sources, messages too long for a terminal line or for Claude's tokens.
- [ ] **G19** Rule IDs linted: uppercase, three words at most, naming the practice rather than the
  violation.
- [ ] **G21** A hash per rule (content and engine version) for cache keys and for the report's
  `grid_version`.
- [ ] **G25** A rule may carry its own small test repo folder (`rules/<theme>/<ID>/`) when inline
  examples get too big (a whole Django project).
- [ ] **H05** Examples mutated: failing variants generated from each `pass` example (the `USER` line
  removed, a SHA turned into a tag), and the detector must flip.
- [ ] **L20** Messages in English only (decided on 16 October 2026), each finding short enough for
  one terminal line.

### T-197 · Findings in the pull request: locations, fingerprints, annotations, summaries
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Nothing to do, Outputs and
  integrations, Trust, privacy and safety), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.12, "Findings where people look": With rules that test themselves (v0.5.11) to build
on: in the pull request, the CI's summary and GitHub's code scanning, written without a flag;
repo-local rules in the grid's format.

- [ ] **E23** Locations with line, column and end (SARIF regions), with a snippet, redacted for
  secrets.
- [ ] **E24** A fingerprint per finding (rule, path, normalized snippet, like SARIF's
  `partialFingerprints`): a finding keeps its identity when lines move, so waivers and baselines
  survive edits.
- [ ] **K08** CI detected (`GITHUB_ACTIONS`, `GITLAB_CI`, `CI`): annotations, SARIF and a job
  summary written without a flag, colours off outside a terminal (T-116).
- [ ] **K18** Nothing written in the repo by default (as today); `--output` writes a report when
  asked.
- [ ] **L05** A Markdown summary for pull request comments and `$GITHUB_STEP_SUMMARY`.
- [ ] **L10** GitHub check runs with annotations, sent in batches of 50.
- [ ] **S03** Secrets never printed: snippets redacted (`ghp_****abcd`) in every output (terminal,
  JSON, SARIF, HTML, comments).

### T-198 · The exact rules first, and the template held to each new rule
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Nothing to do, One measure drives every command,
  Code standards, Architecture, Application security, Front, accessibility and i18n, Containers,
  CI/CD), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.13, "The grid grows: the exact rules first, three new themes": T-141 opens here, its
other boxes being the theme releases below: the rules a detector decides exactly today, the first
rule of `licensing`, `infrastructure` and `data-science`, and the template held to every new rule by
its own test.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **K13** A repo generated by kiln scoring under 100 says it: kiln's bug, reported with consent
  ([REPORT-TO-KILN]).
- [ ] **P04** Each `adopt` rule names the template files that meet it (`met_by_template = […]`):
  `kiln grid` says "kiln new does this for you".
- [ ] **P05** Grid first: a new rule makes the template's test fail until the template meets it,
  test-driven development for the template.
- [ ] **CS18** `NO-DEBUGGER`: no `breakpoint()`, `pdb.set_trace()`, `debugger;`, `binding.pry` or
  `dd()`. L2 · fix S · adopt.
- [ ] **AR01** `NO-SIGNALS` (draft, Django): `@receiver` and model signals' `.connect(`; the charter
  already bans them. L2 · fix J · adopt.
- [ ] **AS32** `NO-MASS-ASSIGNMENT`: no `fields = "__all__"` in ModelForms or serializers. L2 · fix
  J · adopt.
- [ ] **FA05** `HTML-LANG`: `lang` on `<html>` (Nuxt's `app.head.htmlAttrs`, `index.html`, the base
  template). L2 · fix S · adopt.
- [ ] **FA19** `VUE-V-FOR-KEY`: `:key` on every `v-for`. L2 · fix J · adopt.
- [ ] **CO04** `DOCKERIGNORE`: beside each build context, excluding `.git`, `.env*`, `node_modules`
  and caches. L1 · fix S · adopt.
- [ ] **CO20** `PORTS-ON-LOCALHOST`: databases and internal services published on `127.0.0.1` only
  (Docker's published ports bypass ufw's rules). L1 · fix S · adopt.
- [ ] **CI08** `CI-TIMEOUTS`: `timeout-minutes` on every job (the default is 360). L1 · fix S ·
  adopt.
- [ ] **CI10** `NO-PERSISTED-CREDENTIALS`: `actions/checkout` with `persist-credentials: false`
  (zizmor's artipacked). L1 · fix S · adopt.

### T-199 · Three new themes open: licensing, infrastructure, data science
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Git and versions, Licensing, Infrastructure as
  code, Data science), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.13, "The grid grows: the exact rules first, three new themes": T-141 opens here, its
other boxes being the theme releases below: the rules a detector decides exactly today, the first
rule of `licensing`, `infrastructure` and `data-science`, and the template held to every new rule by
its own test.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **GV13** `NO-CONFLICT-MARKERS`: no `<<<<<<<`, `=======` or `>>>>>>>` line in tracked text,
  docs that teach git aside. L2 · fix J · adopt.
- [ ] **LI01** `LICENSE-FILE`: a licence file whose text matches an SPDX licence (matched as
  licensee does), or "all rights reserved" stated for private work. L1 · fix J · adopt (open
  source).
- [ ] **IN02** `TF-REMOTE-STATE`: no `*.tfstate` committed (state holds secrets), a remote backend
  declared; critical when state is tracked. L0 · fix J · adopt.
- [ ] **DS01** `MODEL-TRACED` (trial, v0.4.6): moves here from data-migrations; promoted once its
  precision is measured on data repos.

### T-200 · Repos safe to hand to an agent: permissions, MCP servers, plugins, hooks
- **Type**: improvement
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

### T-201 · Apps that call a model: keys server-side, current models, validated outputs
- **Type**: improvement
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

### T-202 · The roadmap as context packs: estimated, ordered, batched, budgeted
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Outputs and integrations, The roadmap for
  Claude), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.15, "The roadmap Claude reads without exploring": The input of v0.6.0: each gap a
context pack with its recipe and its proof, ordered by points per token, cut into batches that fit a
session.

- [ ] **L18** `--for-claude`: the roadmap's context packs, token-counted, nothing decorative.
- [ ] **O01** A context pack per gap: the rule (why, recipe, a passing example), the places with
  five lines around each, the repo's own passing example when one exists ("this repo already does it
  right in `x.py`"), the proof command. Claude opens nothing else.
- [ ] **O02** Tokens and effort estimated per item; items ordered by points gained per token.
- [ ] **O03** Dependencies between items (tests before a refactor, types before the compressor, the
  lock before the audit) give a topological order.
- [ ] **O04** Batches: one rule with many places split into chunks of under an hour of session each.
- [ ] **O06** Risk tags: config only, pure refactor, behaviour change, product decision (the skill
  already stops on the last).
- [ ] **O07** Recipes as data for every judgment rule, so two sessions fix a gap the same way (and
  T-137 can turn the recipe into a converter).
- [ ] **O09** `--roadmap --budget 2h`: the best set of items for one session (a knapsack on points
  and effort).
- [ ] **O10** `--roadmap --json` with the packs inline: `/kiln:modernize` reads one document and
  explores nothing.

### T-203 · Tests that cost no tokens: properties, mutants, API fuzzing, journeys as rules
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The roadmap for Claude, Tests), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.5.16, "Tests at the lowest token cost": The other half of v0.6.0: generators that cost
no tokens in the template, coverage and surviving mutants measured by script, Claude on the holes
only.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **O08** Each place's coverage (from `--deep` or a committed report): untested places get
  "write a characterization test first".
- [ ] **TE05** `PROPERTY-TESTS` (draft): Hypothesis or fast-check where parsers, serializers or
  money code live, found by paths and names. L1≈ · fix J · assess.
- [ ] **TE06** `MUTATION-TESTS` (draft): mutmut, cosmic-ray or Stryker configured and scheduled. L1
  · fix J · assess.
- [ ] **TE07** `API-FUZZING` (draft): Schemathesis run against the committed OpenAPI schema. L1 ·
  fix S · trial.
- [ ] **TE08** `E2E-JOURNEYS` (draft): Playwright present, its specs naming the journeys the docs
  list. L1≈ · fix J · trial.

### T-204 · The unattended run kept to its places, its verdicts fed back
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The roadmap for Claude), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.0, "Claude closes the gaps alone": Milestone decided by antoine (16 October 2026:
Claude does the work in the repo), its content re-scoped to the vision: the roadmap worked
unattended within a budget, each pull request kept to its places, the cost of a judgment gap
measured, a fix made twice turned into a converter.

- [ ] **O11** A scope guard: a modernize commit that touches files beyond its places and their tests
  is flagged before it merges.
- [ ] **O12** Confirmations and dismissals of "to confirm" places fed back as labels (H), with
  consent.

### T-205 · The slimming rules: dead code, unused dependencies, duplication, a dependency budget
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Code standards, Supply
  chain), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.1, "Less code to carry": The vision's fourth pillar, measured before anything is
built: the compressor's dry run, removals proven by types, tests and behaviour, the slimming rules
promoted once precise.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F13** deptry and knip (unused and missing dependencies) and vulture (dead code), already
  used by the compressor: their findings feed UNUSED-DEPENDENCIES and DEAD-CODE once their precision
  is measured.
- [ ] **CS09** `DEAD-CODE` (trial): vulture and knip, promoted once their precision is measured on
  the corpus. L4≈ · fix S (the compressor) · trial.
- [ ] **CS31** `DUPLICATION`: no duplicated block over about 50 tokens across files (the charter's
  `identical-copies`, generalized). L3 · ratchet · trial.
- [ ] **SU02** `UNUSED-DEPENDENCIES` (trial): deptry and knip, promoted once precise. L4≈ · fix S ·
  trial.
- [ ] **SU17** `DEPENDENCY-BUDGET`: the count of transitive dependencies tracked as a ratchet (the
  slimming pillar). L1 · ratchet · trial.

### T-206 · The roadmap where the team works: issues, good first issues, other agents
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The roadmap for Claude), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.2, "Claude in the team's flow": A red CI made green on the machine, the roadmap as
issues and good first issues, a summary a human reads in their language, a file other agents can
read too.

- [ ] **O13** The roadmap as GitHub or GitLab issues (`--write-issues`, labelled by rule), not only
  backlog tickets.
- [ ] **O14** Good first issues from the roadmap on open-source repos: small, well-placed items
  tagged for `/kiln:good-first-issues`.
- [ ] **O15** A one-line summary per item for the human, in the user's language when Claude speaks
  to them.
- [ ] **O16** A roadmap file other agents can read too (AGENTS.md style), with T-357 (every
  agent, decision 26 of 26 October).

### T-207 · The grid's data dated at each release: end of life, grid diff, consistency, proposals
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Rule format v2 and authoring, A
  grid that stays current), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.3, "The grid kept current: its sources watched": Every week the sources are read,
the data bundle refreshed, the rules whose sources moved flagged; each release note carries the
grid's diff.

- [ ] **B22** End of life for every product endoflife.date covers (runtimes, frameworks, databases,
  distributions, Kubernetes, CI runners), bundled at each release, refreshed by `--online`.
- [ ] **G12** `level_history`: when and why the rule moved on the radar, with the evidence
  (precision, sources). An auditable radar.
- [ ] **Q01** A data bundle per release, dated and shown by `kiln score --version`: end-of-life
  dates, deprecated and malicious packages, retired CI runners and commands, retired LLM model IDs,
  provider secret patterns.
- [ ] **Q06** A grid diff in each release note: rules added, promoted, demoted, retired.
- [ ] **Q10** A consistency check: no two rules contradict (examples cross-run: a pass example of
  one never fails another).
- [ ] **Q11** A `grid-proposal` issue template (a practice with its sources), triaged by the
  doctrine.
- [ ] **Q12** The decision behind each rule kept with it (why adopt, why now), like an architecture
  decision record.

### T-208 · A page per rule, and the study every quarter
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Rule format v2 and authoring, Nothing to do,
  Docs, teaching and reach), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.5, "For more people": Tutorials that keep bringing visitors, the roadmap as a GitHub
Project, a page per rule where searches land, the study every quarter, a folder or a zip scored as
well as a repo.

- [ ] **G15** A Markdown page per rule beside its file (why, bad and good code, the fix,
  references), as ruff documents its rules; `kiln grid ID --doc` shows it, the site publishes it.
- [ ] **K07** No config, no question, no `kiln adopt` needed to score; a plain folder, a zip or a
  tarball scored too.
- [ ] **V01** A web page per rule generated from its file (why, bad and good, the fix, sources,
  prevalence, precision, standards): the pages people land on when they search "pin GitHub Actions",
  one way to get known.
- [ ] **V02** The study (T-132) repeated every quarter: "the state of Django and Nuxt repos".

### T-209 · One model of the repo: components, roles, one answer for every command
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, One measure drives every
  command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.6, "One answer to "what is this repo"": Score, fix, adopt, dev and check read one
model: components with their roles, so a Django rule never reads `frontend/` and one helper script
doesn't make a repo Python.

- [ ] **A01** One module answers "what is this repo" (`kiln.repo`), replacing `grid/facts.py`,
  `stack.py:detect_stack` and `grid/fix.py:check_commands`; score, fix, adopt, dev, check and update
  all read it.
- [ ] **A02** Components: every folder holding a manifest is one (pyproject.toml, package.json,
  go.mod, Cargo.toml, pom.xml, build.gradle(.kts), *.csproj, composer.json, Gemfile, mix.exs,
  pubspec.yaml, Package.swift, CMakeLists.txt, meson.build, DESCRIPTION, Project.toml, deno.json,
  flake.nix, Chart.yaml, a folder of *.tf), nested under its parent.
- [ ] **A04** A role per component, inferred: backend, frontend, library, CLI, worker, infra, docs,
  mobile, desktop, extension, data/ML, tests, template, fixture, vendored, generated, example. Each
  role turns groups of rules on or off.
- [ ] **A09** `.gitattributes` honoured: `linguist-vendored`, `linguist-generated`,
  `linguist-documentation`, `export-ignore`, conventions many repos already set for GitHub.
- [ ] **A20** A share threshold for languages: one helper script in Python doesn't make a JavaScript
  repo a Python repo (today one `.py` file turns every Python rule on).
- [ ] **A24** Findings per component, paths still relative to the repo: a Django rule never reads
  `frontend/`.
- [ ] **A37** `kiln dev` and `kiln check` read the model: T-159's "checks found beyond the root"
  falls out of it.
- [ ] **P12** `kiln dev`, `kiln doctor` and `kiln check` read the repo model (A).

### T-210 · Facts per component: versions, runtimes, tools, evidence, `--facts`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.7, "Rules per component: versions, tools, evidence": Each fact says where it comes
from and how sure it is; rules can say `django >= 4.2` or "your formatter"; a component is scored
alone.

- [ ] **A03** Workspaces group components: uv workspaces, pnpm-workspace.yaml, npm, Yarn and Bun
  workspaces, Cargo workspaces, go.work, Maven modules, Gradle settings, Nx, Turborepo, Lerna, Rush,
  Bazel's MODULE.bazel, Pants, Moon.
- [ ] **A10** Every fact carries its evidence (`django 5.2 · backend/uv.lock:412`) and a confidence
  (certain from a lock, likely from an import, possible from a file name).
- [ ] **A11** Versions in facts, from the lock first, the manifest's constraint next: rules can say
  `django >= 4.2`, `vue < 3`, `node 20`.
- [ ] **A13** Runtime versions gathered from every place that names one (.python-version,
  requires-python, .tool-versions, mise.toml, runtime.txt, .nvmrc, .node-version, engines, Volta,
  packageManager, Dockerfile FROM, CI matrices, global.json, rust-toolchain.toml, go.mod's `go` and
  `toolchain`), and their disagreements reported.
- [ ] **A14** Tools per component: which linter, formatter, type checker, test runner, bundler and
  task runner, from config files and dev dependencies; rules then speak of "your formatter",
  whichever it is.
- [ ] **A19** Facts declared as data (`facts/*.toml`: file patterns, dependency names, content
  signatures), tested like rules: a new ecosystem is a data change, not code.
- [ ] **A21** `kiln score --facts`: the model as a tree (components, roles, versions, tools,
  services) with its evidence, in JSON too. The first thing to read when a rule misapplies.
- [ ] **A22** `kiln score --why-applies RULE`: the facts that made a rule apply here.
- [ ] **A25** The repo's score aggregates its components' (weighted by code size); each component
  scorable alone (`kiln score backend/`).
- [ ] **A36** A correction exists when detection is wrong (`kiln set components.ignore=…`), is never
  needed, and each use is a signal for T-38.

### T-211 · Rules that say what they mean: applicability as an expression, `any_of`, `unknown`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, The detection engine, Rule
  format v2 and authoring), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.8, "Rules that say what they mean": Applicability as an expression, several ways to
meet one practice, conditions across files, evidence for passes, an honest `unknown`.

- [ ] **A23** Applicability as an expression over the model (`component.role == "backend" and django
  >= 4.2`) instead of the flat `applies` list.
- [ ] **E08** Combinators (`all`, `any`, `not`) and conditions ("if a Dockerfile `EXPOSE`s a port,
  compose or the Dockerfile has a health check").
- [ ] **E18** Equivalence lists as data (Python linters: ruff, flake8, pylint; dependency bots:
  Dependabot, Renovate…): a practice met by any, with "met; kiln recommends ruff" as a gentle
  `trial` note.
- [ ] **E19** Evidence for passes too: "met by `renovate.json`", "met: `USER app` in the final stage
  of `Dockerfile`". `--all` says why each rule passed.
- [ ] **E20** A third outcome, `unknown`: the detector couldn't decide (a config written as code, a
  tool missing, a file too big). Listed apart, never a pass, never a fail.
- [ ] **E33** A rule's condition can read the model (`component.frameworks.django.version`), so
  Django 4.2 and 5.2 can have different detectors.
- [ ] **E34** Inline justifications in the charter's style (`# kiln: allow NAIVE-DATETIMES,
  reason`): counted, shown, gone when the code they sit on goes.
- [ ] **E35** A detector can ask for several files at once (compose, Dockerfile and CI together):
  the engine hands it the set, each file read once.
- [ ] **G03** `applies` as an expression over the repo model (A).
- [ ] **G04** `any_of`: the ways one practice can be met, each with its own detector.
- [ ] **G20** One practice, several languages, one ID: `[detector.python]`, `[detector.typescript]`,
  `[detector.java]`.
- [ ] **G24** Typed settings with defaults, for project data only (time zone, currency, integration
  branch): never a knob that weakens a rule (doctrine 1).

### T-212 · The syntax engine: ast-grep, one parse per file, settings and configs resolved
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Precision and recall,
  Speed), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.9, "Code, not text: the syntax engine": Detectors match syntax trees (ast-grep);
Django settings, `nuxt.config`, Dockerfiles and tsconfig chains are read as they resolve; the false
negatives found on 24 October close.

- [ ] **E03** A `syntax` detector kind on ast-grep (Rust, tree-sitter, YAML rules with `pattern`,
  `inside`, `has`, `not`, `constraints`): declarative like today's regexes, matching code instead of
  text (doctrine 11, T-144).
- [ ] **E04** One parse per file, shared by every syntax rule, the tree cached by blob SHA.
- [ ] **E12** Symbol tables per language (functions, classes, variables, booleans, constants) from
  tree-sitter queries: CASE, BOOLEANS, GENERIC-NAMES and ONE-CLASS for every language.
- [ ] **E14** Config resolved rather than grepped: tsconfig `extends` chains (local files and
  package presets), ruff's `extend`, ESLint flat configs read as syntax (never executed), mypy,
  pyright, pytest and coverage settings wherever they live.
- [ ] **E15** Django settings evaluated statically: the module found (`manage.py`, `wsgi.py`,
  `asgi.py`, `DJANGO_SETTINGS_MODULE`), `from .base import *` followed, plain assignments and
  `env("X", default=…)` read. `DEBUG = env.bool("DEBUG", default=True)` becomes a finding; it is
  invisible today.
- [ ] **E16** `nuxt.config` read as syntax: `runtimeConfig` (secrets under `public`), `routeRules`,
  the Nitro preset, `devtools`, modules, `ssr`, `sourcemap`.
- [ ] **E17** Dockerfiles parsed per stage: the final stage's `USER`, `ARG` defaults resolved inside
  `FROM` (a `$` image is skipped today, a false negative), heredocs, `--mount` options.
- [ ] **H09** Known false negatives (from reading the code on 24 October) closed one by one: `FROM
  $IMAGE` skipped; the file's last `USER` read instead of the final stage's; `permissions:
  write-all` passes WORKFLOW-PERMISSIONS; a tsconfig strict through a local `extends` fails
  STRICT-TS; a linter config anywhere (even under `template/`) passes PYTHON-LINTER for the whole
  repo; compose, Kubernetes and CI images escape IMAGES-BY-DIGEST.
- [ ] **J16** The syntax engine runs all syntax rules of a language in one native pass (`ast-grep
  scan` over a rules folder), in parallel.

### T-213 · Mature tools as detectors: ruff and shellcheck, pinned and deduplicated
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, The detection engine, Mature
  tools as detectors), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.10, "Mature tools as detectors": ruff, shellcheck and their kin mapped onto grid
rules, pinned and cached, never downloaded without asking; the faster checkers measured against the
ones they would replace.

- [ ] **B15** Shell and PowerShell as real code: shellcheck, shfmt, `set -euo pipefail`, bats;
  PSScriptAnalyzer and Pester.
- [ ] **E02** The default run is L0 to L3 plus the L4 tools shipped as wheels: offline, nothing of
  the repo executed. `--online` adds L6, `--history` L5, `--deep` L7 in a sandbox.
- [ ] **F01** A `tool` detector kind: run a tool with machine output (JSON, SARIF), map each result
  to a rule and a place. The tool comes from the repo's environment, PATH or kiln's bundle; it is
  never downloaded without `--online`.
- [ ] **F02** ruff as the Python engine wherever it has the rule: DTZ (naive datetimes), E722 (bare
  except), PGH003 and PGH004 (blanket ignores), S608 (SQL by strings), S602 to S607 (shell), S301
  and S506 (unsafe loads), S113 (no timeout), B006 (mutable defaults), T20 (print), C901, PLR2004
  (magic values), UP (modern Python at the `requires-python` target), DJ, ASYNC, PTH, ERA. Exact,
  string-aware, and its safe fixes become free converters.
- [ ] **F03** kiln's reference ruff selection run even on repos without a ruff config (isolated,
  kiln's own config), beside the repo's: "your linter says" and "the grid says" kept apart.
- [ ] **F05** shellcheck (the `shellcheck-py` wheel) on shell scripts and on the `run:` blocks of
  workflows.
- [ ] **F21** Every tool pinned by version and hash, its output cached by the hash of its inputs; a
  tool update is a grid change and its precision is measured again.
- [ ] **F22** Several tools on one line deduplicated: ruff's S608 and another tool on the same SQL
  string make one finding with both as evidence.
- [ ] **F23** A missing tool never fails a rule: "unknown: install kiln's tools extra, or run with
  `--deep`".
- [ ] **F24** A `kiln-cli[tools]` extra bringing the tools that ship as wheels in one install.

### T-214 · Instant the second time: one listing, one index, a cache by blob SHA
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Rule format v2 and
  authoring, Speed), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.11, "Instant the second time": One listing from git, one matcher for every rule, a
cache keyed by blob SHA: a warm run recomputes nothing unchanged, in under 50 ms.

- [ ] **A34** The model cached by the blob SHAs of the manifests: every kiln command reuses it in
  milliseconds.
- [ ] **G22** `inputs` declared per rule (the path classes it reads): the incremental engine knows
  what to recompute.
- [ ] **J04** One listing (`git ls-files -s` gives each tracked file's blob SHA for free); contents
  through `git cat-file --batch` when the tree is clean, from disk otherwise.
- [ ] **J05** A file-to-rules index built once, every rule's globs merged into one matcher: today
  each rule walks every file with its own patterns.
- [ ] **J06** Only the files some applicable rule needs are read; sizes from `git cat-file
  --batch-check` skip the huge ones before reading.
- [ ] **J07** YAML through libyaml's `CSafeLoader` when present, several times faster than the
  pure-Python loader.
- [ ] **J08** All text rules for one file type in a single scan (a combined automaton: a regex set,
  or Hyperscan where a measurement says so).
- [ ] **J10** A cache keyed by blob SHA, rule hash and engine version in `~/.cache/kiln/score/`: a
  warm run recomputes nothing unchanged, in under 50 ms.
- [ ] **J22** The repo and CI models cached across commands (score, fix, dev, check) and across
  runs.
- [ ] **J25** The grid compiled once into one index (each rule's `applies`, inputs and detector),
  at build or on the first run: a run parses only the rules whose facts the repo has, and a test
  proves a Django repo loads no Go rule. Measured on 26 October 2026: 138 rules parsed one by one
  in 30 ms (0.22 ms each), so the plan's 800 or so would cost about 170 ms on every run; budget:
  under 30 ms whatever the grid's size.

### T-215 · Python standards ruff already decides: modern syntax, formatting, linting
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.12, "Code standards a linter proves": With ruff mapped (v0.6.10), the Python
standards it already decides become rules at once, its safe fixes their converters; shell scripts
and encodings come with them.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS06** `MODERN-PYTHON` (draft): ruff's UP rules at the `requires-python` target; ruff's
  fixes are the converter. L4 · fix S · adopt.
- [ ] **CS11** `RETURN-VALUES` (draft): functions that return a value on some paths and nothing on
  others (ruff's RET503). L4 · fix J · trial.
- [ ] **CS13** `NO-MAGIC-VALUES` (draft): ruff's PLR2004 and its JS counterpart. L4 · fix J · trial.
- [ ] **CS15** `FORMATTER`: a formatter configured for each language, as `PYTHON-LINTER` and
  `JS-LINTER` ask a linter (ruff format or Black, Prettier or Biome, gofmt, rustfmt, Spotless,
  `dotnet format`, RuboCop, PHP-CS-Fixer). L1 · fix S · adopt.
- [ ] **CS16** `FORMATTED`: the code really is formatted (`ruff format --check` and the other
  formatters shipped as wheels). L4 · fix S · adopt.
- [ ] **CS17** `LINTER-CLEAN`: the repo's own linter config passes, or its error count only goes
  down. L4 · ratchet · trial.
- [ ] **CS21** `NO-COMMENTED-CODE`: no code left commented out (ruff's ERA001). L4 · fix S · trial.
- [ ] **CS22** `NO-MUTABLE-DEFAULTS` (Python): ruff's B006. L4 · fix S · adopt.
- [ ] **CS23** `NO-STAR-IMPORTS` (Python): F403, settings modules aside. L4 · fix J · adopt.

### T-216 · Error handling, shell scripts and encodings, decided by tools
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.12, "Code standards a linter proves": With ruff mapped (v0.6.10), the Python
standards it already decides become rules at once, its safe fixes their converters; shell scripts
and encodings come with them.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS24** `NO-SILENT-EXCEPT`: no `except Exception: pass` or empty `catch {}` (S110, BLE001,
  no-empty), beyond `BARE-EXCEPT`. L4 · fix J · adopt.
- [ ] **CS25** `EXCEPTION-CHAINING`: `raise … from err` inside `except` (B904). L4 · fix S · adopt.
- [ ] **CS26** `NO-ASSERT-FOR-CHECKS`: no `assert` doing validation in shipped Python (S101); `-O`
  removes them. L4 · fix J · trial.
- [ ] **CS27** `PATHLIB`: `pathlib` rather than `os.path` (ruff's PTH). L4 · fix S · trial.
- [ ] **CS29** `PARAMETER-COUNT`: five parameters at most, keyword-only past that (PLR0913). L4 ·
  fix J · trial.
- [ ] **CS40** `SHELL-STRICT-MODE`: shell scripts start with `set -euo pipefail`, or say why not. L1
  · fix S · adopt.
- [ ] **CS41** `SHELLCHECK-CLEAN`: shellcheck passes on every script. L4 · fix J · adopt.
- [ ] **CS42** `UTF8-SOURCES`: text files in UTF-8 without a BOM. L1 · fix S · adopt.
- [ ] **CS43** `NO-MIXED-INDENTATION`: tabs and spaces never mixed in one file. L1 · fix S · adopt.

### T-217 · Secrets in the tree cap the score; session cookies, headers, CSRF
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Application security), made
  a ticket on 25 October 2026 at antoine's request

Planned in v0.6.13, "Secrets and the settings that leak": The secrets themselves, checksum-verified,
and the production settings read as they resolve (v0.6.9): cookies, headers, HTTPS, debug flags,
keys in the front.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **E28** A secrets engine: provider patterns (gitleaks' rules as data), checksum-verified
  tokens (GitHub's `ghp_` and `github_pat_` tokens carry a CRC32, so zero false positives), entropy
  last; documented sample keys and placeholders (`AKIAIOSFODNN7EXAMPLE`, `changeme`, `<your-token>`)
  left out.
- [ ] **AS01** `SECRETS` (draft): the secrets themselves in tracked files (provider patterns,
  checksum-verified tokens, entropy last), where `SECRET-SCAN` checks that a scan runs and
  `NO-TRACKED-ENV` that no `.env` is tracked; critical: it caps the score at 49. L2 · fix J (rotate,
  then remove) · adopt.
- [ ] **AS02** `SESSION-COOKIES` (draft, Django): `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
  `SESSION_COOKIE_HTTPONLY` and `SAMESITE` in the production settings, evaluated statically. L2 ·
  fix S · adopt.
- [ ] **AS03** `SECURITY-HEADERS` (draft): HSTS of a year or more, `nosniff`, frames denied, a
  referrer policy; in Django's settings, the reverse proxy (Caddy, nginx) or Nuxt (nuxt-security).
  L2 · fix S · adopt.
- [ ] **AS04** `CSP-NONCE` (draft): a Content Security Policy with nonces (Django 6.0's built-in
  CSP, django-csp, nuxt-security), no `unsafe-inline` for scripts. L2 · fix J · trial.
- [ ] **AS05** `CONSTANT-TIME` (draft): secrets compared with `hmac.compare_digest` or
  `crypto.timingSafeEqual`, never `==` on names like token, signature or digest; the charter's ban
  promoted. L2 · fix S · adopt.
- [ ] **AS09** `SUBRESOURCE-INTEGRITY` (draft): `<script>` and `<link>` from another origin carry
  `integrity`. L2 · fix S (hash computed online) · adopt.
- [ ] **AS20** `NO-HARDCODED-PASSWORDS`: S105 to S107 and their JS counterparts. L4 · fix J · adopt.
- [ ] **AS21** `TLS-VERIFIED`: no `verify=False`, `rejectUnauthorized: false`,
  `NODE_TLS_REJECT_UNAUTHORIZED=0` or `InsecureSkipVerify: true`. L2 · fix S · adopt.
- [ ] **AS22** `CSRF-ON`: CSRF middleware on; `@csrf_exempt` only with a justification marker. L2 ·
  fix J · adopt.

### T-218 · Settings that leak: CORS, passwords, HTTPS, front secrets, debug modes
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Application security), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.13, "Secrets and the settings that leak": The secrets themselves, checksum-verified,
and the production settings read as they resolve (v0.6.9): cookies, headers, HTTPS, debug flags,
keys in the front.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS23** `CORS-STRICT`: no allow-all origins with credentials (`CORS_ALLOW_ALL_ORIGINS`,
  `Access-Control-Allow-Origin: *`). L2 · fix J · adopt.
- [ ] **AS24** `PASSWORD-HASHING`: Argon2 or the framework's default first, never MD5, SHA-1 or
  unsalted hashers. L2 · fix S · adopt.
- [ ] **AS25** `PASSWORD-VALIDATORS`: `AUTH_PASSWORD_VALIDATORS` set, or a passkey-first login. L2 ·
  fix S · adopt.
- [ ] **AS35** `HTTPS-ONLY`: `SECURE_SSL_REDIRECT`, Caddy's automatic HTTPS, `force_ssl`. L2 · fix S
  · adopt.
- [ ] **AS36** `NO-SECRETS-IN-FRONT`: no secret-looking key under Nuxt's `runtimeConfig.public`,
  `NUXT_PUBLIC_*`, `VITE_*` or `NEXT_PUBLIC_*`. L2 · fix J · adopt.
- [ ] **AS49** `BAAS-ACCESS-RULES`: Firebase's `firestore.rules`, `storage.rules` and
  `database.rules.json` never open to everyone (`allow read, write: if true`, or the test mode's
  `request.time <` date left in), and every Supabase table of an exposed schema under row-level
  security in its migrations, the `service_role` key never in front code; the anon key is public
  by design, so these rules are the only lock (170 generated apps found readable and writable by
  anyone in 2025, CVE-2025-48757). L1 · fix J · adopt.
- [ ] **AS37** `PRIVATE-SOURCEMAPS`: production source maps not served publicly. L2 · fix S · trial.
- [ ] **AS38** `DEV-TOOLS-DEV-ONLY`: debug toolbars and devtools only in development settings and
  dependency groups. L2 · fix S · adopt.
- [ ] **AS39** `SECURITY-TXT`: production web apps serve `/.well-known/security.txt` (RFC 9116). L0
  · fix S · trial.
- [ ] **AS45** `FRAMEWORK-DEBUG-OFF`: `DJANGO-DEBUG-OFF` for the other frameworks: Laravel's
  `APP_DEBUG`, Rails' `consider_all_requests_local`, Flask's `debug=True`, Spring's Actuator
  exposing more than health and info. L2 · fix S · adopt.

### T-219 · The corpus: precision and recall per rule at every candidate
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every ecosystem, Rule
  format v2 and authoring, Precision and recall, A grid that stays current), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.14, "Precision measured on a thousand repos": A labelled corpus re-scored at every
candidate, precision and recall per rule as a release gate, new detectors in shadow first; the radar
moves on that evidence only.

- [ ] **A35** A corpus for the model itself: 500 real trees (paths and manifests) with their
  expected model; each fact's precision tracked like a rule's.
- [ ] **B01** The order of ecosystems set by the corpus (share of repos, share of code), never
  assumed; Django and Nuxt stay the reference.
- [ ] **G14** `precision` and `prevalence` written by the calibration job (H), shown in `kiln grid
  ID` and on the rule's page.
- [ ] **G23** `shadow = true`: a new detector runs and records on the corpus and on beta machines
  without showing, for one release, before it counts.
- [ ] **H02** Labels from Claude in batches (20 places per rule, "to confirm"), spot-checked by
  antoine, stored by fingerprint; only aggregates in public, anything that names a project in
  `kiln-private`.
- [ ] **H03** Precision and recall per rule at every candidate; a strict rule under 99 % precision,
  or any drop, stops the candidate (`kiln version cut`).
- [ ] **H04** Differential tests against reference tools (zizmor, Scorecard, gitleaks, ruff): each
  disagreement triaged into a kiln bug or a documented difference.
- [ ] **H12** Inline markers and waivers counted per rule across the corpus: the most-waived rules
  are examined first.
- [ ] **H14** Recall measured with seeded faults: secrets, unpinned images, root containers planted
  in copies of corpus repos must all be found.
- [ ] **H19** The corpus's labels versioned with the grid, so a rule's precision history is a plot,
  not a memory.
- [ ] **H20** A rule that flags more than half of the corpus is looked at twice: either the practice
  is rare (say so) or the detector is wrong.
- [ ] **Q03** Radar moves on evidence only: assess to trial needs a detector and examples; trial to
  adopt needs 99 % precision on the corpus (strict rules) and fresh sources; adopt to hold when the
  practice is superseded.

### T-220 · A quality sheet in every release note
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Measuring kiln score itself), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.14, "Precision measured on a thousand repos": A labelled corpus re-scored at every
candidate, precision and recall per rule as a release gate, new detectors in shadow first; the radar
moves on that evidence only.

- [ ] **T01** A quality sheet in each release note: scored rules, rules with a detector, median
  precision, recall on seeded faults, speed on the suite, crashes on the corpus.

### T-221 · A number that can't lie: severity, the critical cap, confidence, anti-gaming
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Rule format v2 and
  authoring, Precision and recall, Scoring model v2, Trust, privacy and safety), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.15, "A number that can't lie": Severity orders the gaps, critical findings cap the
score at 49 once they are 99 % precise (decision 2), a maybe is never punished, an empty file earns
nothing, a report can be verified.

- [ ] **E26** Approximate detectors return candidates with a confidence: the roadmap sends the
  uncertain ones to Claude "to confirm" and the certain ones as gaps.
- [ ] **G05** `severity` (critical, high, medium, low, info), apart from `regime` (how it is
  enforced) and `level` (the radar).
- [ ] **H13** A confidence per finding (the rule's precision times its context: test file,
  generated, comment), shown as "certain" or "likely".
- [ ] **H18** Precision shown to users ("this rule is 99.4 % precise on 1,000 repos"): trust earned
  with numbers.
- [ ] **I01** A severity on each rule (critical, high, medium, low) that orders the gaps and marks
  the critical ones; it never weighs the number (decision 2).
- [ ] **I02** Critical findings cap the score at 49 (decision 2), each critical rule proven at 99 %
  precision first: a committed secret, `DEBUG = True` in production settings, `pull_request_target`
  checking out the pull request's code, the engine's socket mounted in a container. A repo that
  leaks its keys can't show 90.
- [ ] **I03** Progress shown per place, never as partial credit: "`IMAGES-BY-DIGEST`: 37 of 40
  pinned" beside the rule, so every fix shows while the number keeps meaning rules met (decision 2).
- [ ] **I04** Approximate findings not counted until Claude or the user confirms them: the score
  never punishes a maybe.
- [ ] **I14** Anti-gaming: presence rules check content (a README with install and usage, a
  SECURITY.md with a contact, tests that assert, CI that runs on pull requests and pushes). An empty
  file earns nothing.
- [ ] **S06** Reproducible: the report carries kiln's version, the grid's hash, the data's date and
  the commit; `kiln score --verify report.json` runs again and compares.

### T-222 · Locks and installs you can trust: every lockfile, frozen installs, pinned runtimes
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every ecosystem, Every
  forge, CI, host and machine, The detection engine, Supply chain), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.16, "Locks and installs you can trust": Every lockfile parsed, one practice checked
in every ecosystem, every manifest folder covered by the update bot, installs from the lock in CI
and in images.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A12** A parser per lockfile (uv.lock, poetry.lock, pdm.lock, Pipfile.lock, pylock.toml,
  hashed requirements, pnpm-lock.yaml, package-lock.json v1 to v3, yarn.lock classic and Berry,
  bun.lock, Cargo.lock, go.sum, composer.lock, Gemfile.lock, mix.lock, pubspec.lock,
  packages.lock.json, gradle.lockfile, Package.resolved, renv.lock, Manifest.toml, flake.lock,
  .terraform.lock.hcl): exact versions and the whole tree, transitives included.
- [ ] **B21** One practice, many ecosystems, one ID: `LOCKED-DEPENDENCIES`, `FROZEN-INSTALL-IN-CI`
  or `NO-INSTALL-SCRIPTS` carry a detector per ecosystem, so "universal" rules really are.
- [ ] **C10** Every dependency bot recognized and held to the same settings: Dependabot (every
  ecosystem folder covered, cooldown, groups), Renovate (every config place, `minimumReleaseAge`,
  presets), GitLab's dependency scanning, Snyk, Mend, Depfu.
- [ ] **E31** Freshness of generated files without running anything: the lock against its manifest,
  the committed OpenAPI schema against the routes it names, an action's `dist/` against its sources
  (approximate; `--deep` proves).
- [ ] **SU06** `DEPENDENCY-UPDATES` (scored): every manifest folder covered by the bot's config, not
  merely "a config exists".
- [ ] **SU07** `LOCK-IN-SYNC`: every dependency of the manifest is in the lock's root with a
  matching constraint. L1 · fix S · adopt.
- [ ] **SU08** `FROZEN-INSTALL-IN-CI`: CI installs from the lock (`uv sync --locked`, `npm ci`,
  `pnpm install --frozen-lockfile`, `cargo build --locked`, `bundle install` frozen). L1 · fix S ·
  adopt.
- [ ] **SU09** `FROZEN-INSTALL-IN-IMAGES`: Dockerfiles install from the lock too. L1 · fix S ·
  adopt.
- [ ] **SU25** `RUNTIME-PINNED`: one runtime version named consistently in `.python-version` or
  `.nvmrc`, in CI and in images. L1 · fix S · adopt.
- [ ] **SU26** `PACKAGE-MANAGER-PINNED`: `packageManager` in package.json (corepack), uv's
  `required-version`. L1 · fix S · adopt.
- [ ] **SU31** `COOLDOWN-EVERYWHERE`: `UPDATE-COOLDOWN` also met where the package manager has one
  (pnpm's `minimumReleaseAge`, uv's `exclude-newer`), not only in the bot. L1 · fix S · trial.
- [ ] **SU32** `DEPENDABOT-GROUPED`: updates grouped to keep the noise down. L1 · fix S · trial.

### T-223 · Nothing runs unpinned: install scripts, indexes, git dependencies, tools
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Supply chain), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.17, "Nothing runs that you didn't pin": Install scripts off, one index, tools and
hooks pinned, downloads checked, no token in a committed `.npmrc`, no binary in the tree, an SBOM
per release.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SU01** `SBOM` (draft): an SBOM (CycloneDX or SPDX) made in the release workflow (syft,
  cdxgen, the package manager). L1 · fix S · trial.
- [ ] **SU10** `NO-INSTALL-SCRIPTS`: npm lifecycle scripts off by default (`ignore-scripts`, pnpm's
  `onlyBuiltDependencies` allowlist, Bun's trusted dependencies); the 2025 npm worms spread through
  install scripts. L1 · fix S · adopt.
- [ ] **SU11** `ONE-INDEX`: Python packages from one index, no `--extra-index-url` (dependency
  confusion); uv's pinned indexes for private packages. L1 · fix S · adopt.
- [ ] **SU12** `GIT-DEPS-PINNED`: dependencies fetched from git pinned to a commit, never a branch.
  L1 · fix S (online) · adopt.
- [ ] **SU18** `NO-DUPLICATE-MAJORS`: one package in several major versions in a JS lock. L1 · fix S
  (dedupe) · trial.
- [ ] **SU20** `PINNED-PRE-COMMIT`: pre-commit hooks pinned by commit (`autoupdate --freeze`). L1 ·
  fix S · adopt.
- [ ] **SU21** `PINNED-TOOLS`: tools run through `npx`, `uvx`, `pipx run` or `go run` in CI and
  scripts carry a version. L1 · fix S · adopt.

### T-224 · Nothing downloaded blind: curl pipes, checksums, binaries, tokens in config
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Supply chain), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.17, "Nothing runs that you didn't pin": Install scripts off, one index, tools and
hooks pinned, downloads checked, no token in a committed `.npmrc`, no binary in the tree, an SBOM
per release.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SU22** `NO-CURL-PIPE-SHELL`: no `curl … | sh` in Dockerfiles, CI or setup scripts: download,
  verify, then run. L1 · fix J · adopt (review in READMEs).
- [ ] **SU23** `CHECKSUMS-FOR-DOWNLOADS`: binaries fetched in Dockerfiles and CI checked against a
  SHA-256. L1≈ · fix S (online) · trial.
- [ ] **SU29** `VENDORED-JS-VULNERABILITIES`: front-end libraries copied into static folders
  (jQuery, Bootstrap, Moment and the rest) matched against retire.js's signatures. L1 · fix J ·
  adopt.
- [ ] **SU34** `NO-HTTP-INDEXES`: package indexes and registries over HTTPS only (`.npmrc`,
  `pip.conf`, `uv.toml`, Maven's `settings.xml`). L1 · fix S · adopt.
- [ ] **SU35** `NO-TOKENS-IN-NPMRC`: no auth token in a committed `.npmrc` or `.pypirc`. L1 · fix J
  · adopt, critical.
- [ ] **SU36** `NO-BINARY-ARTIFACTS`: no executable, `.jar`, `.class`, `.dll` or wheel committed
  outside declared fixtures (Scorecard's Binary-Artifacts). L0 · fix J · adopt.

### T-225 · What is on its way out: support calendars, hold rules and their converters
- **Type**: improvement
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

### T-226 · Dockerfiles built right: digests, base images, non-root, stages
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Mature tools
  as detectors, Supply chain, Containers), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.19, "Containers built right": Dockerfiles read stage by stage (v0.6.9): the final
user, multi-stage builds, secrets at build time, exec form, images by tag and digest everywhere.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C12** Neutral to container engines (Docker, Podman, Buildah, Kaniko, BuildKit): `# syntax=`,
  `--mount=type=secret` and `type=cache`, Bake files, devcontainer.json read.
- [ ] **F08** hadolint's most useful checks rewritten on the parsed Dockerfile (latest tag, root
  user, pipefail, apt hygiene, `ADD` of a URL, exec form) rather than shipping a Haskell binary.
- [ ] **SU04** `IMAGES-BY-DIGEST` (scored): extended to compose, Kubernetes, Helm values and CI
  images, with `ARG` defaults resolved.
- [ ] **SU28** `SUPPORTED-BASE-IMAGES`: Alpine, Debian, Ubuntu and language images on supported
  versions (CURRENT-DEBIAN generalized). L1 · fix S · adopt.
- [ ] **CO01** `NON-ROOT-CONTAINERS` (scored): the final stage's `USER`, not the file's last one; a
  numeric UID so Kubernetes' `runAsNonRoot` can check it; compose's `user:` counted.
- [ ] **CO03** `CURRENT-DEBIAN` (scored): folded into `SUPPORTED-BASE-IMAGES` (SU), the Debian line
  read from the tag or the digest, Alpine and Ubuntu too.
- [ ] **CO05** `MULTI-STAGE`: compilers and dev dependencies left in a builder stage. L2 · fix J ·
  trial.
- [ ] **CO06** `MINIMAL-FINAL-STAGE`: a slim or distroless final image, no shell where none is
  needed. L2 · fix J · trial.
- [ ] **CO07** `TAG-AND-DIGEST`: `image:tag@sha256:…`, the tag kept for humans and update bots. L2 ·
  fix S · adopt.
- [ ] **CO08** `COPY-NOT-ADD`: `COPY` rather than `ADD`, never `ADD` of a URL (hadolint's DL3020).
  L2 · fix S · adopt.
- [ ] **CO09** `APT-HYGIENE`: `--no-install-recommends`, lists removed or a cache mount (DL3015,
  DL3009). L2 · fix S · adopt.
- [ ] **CO10** `CACHE-MOUNTS`: `RUN --mount=type=cache` for uv, pnpm, pip and apt. L2 · fix S ·
  trial.

### T-227 · Dockerfiles that behave: build secrets, signals, pipefail, one process
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Containers), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.19, "Containers built right": Dockerfiles read stage by stage (v0.6.9): the final
user, multi-stage builds, secrets at build time, exec form, images by tag and digest everywhere.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CO11** `BUILD-SECRETS`: secrets through `--mount=type=secret`, never `ARG` or `ENV`
  (BuildKit's `SecretsUsedInArgOrEnv` check). L2 · fix J · adopt.
- [ ] **CO12** `EXEC-FORM`: `CMD` and `ENTRYPOINT` in JSON form so signals reach the process
  (BuildKit's `JSONArgsRecommended`). L2 · fix S · adopt.
- [ ] **CO13** `PIPEFAIL`: `SHELL [..., "-o", "pipefail", "-c"]` before a `RUN` with a pipe
  (DL4006). L2 · fix S · adopt.
- [ ] **CO14** `INIT-PROCESS`: `init: true` or tini where the main process doesn't reap its
  children. L2≈ · fix S · assess.
- [ ] **CO15** `OCI-LABELS`: `org.opencontainers.image.source`, `revision` and `licenses` on
  published images. L2 · fix S · trial.
- [ ] **CO28** `HADOLINT-CLEAN`: hadolint passes, as a mapped tool (F). L4 · fix J · trial.
- [ ] **CO29** `ONE-PROCESS`: no supervisord or `&` chain running several services in one container.
  L2 · fix J · trial.

### T-228 · Compose for a small server: hardening, no socket, logs and limits
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Containers), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.20, "Compose files for a small server": What a VPS running compose needs: no engine
socket, databases on localhost, logs rotated, limits and restarts, secrets out of the file, images
scanned and signed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CO02** `HARDENED-CONTAINERS` (scored): also read in Kubernetes manifests and Helm values
  (`securityContext`, see IN).
- [ ] **CO16** `COMPOSE-NO-VERSION`: no top-level `version:`, obsolete in the Compose Specification.
  L1 · fix S · adopt.
- [ ] **CO17** `COMPOSE-HEALTHY-DEPENDS`: `depends_on` with `condition: service_healthy` on
  databases. L1 · fix S · adopt.
- [ ] **CO18** `NO-DOCKER-SOCKET`: no `/var/run/docker.sock` mounted, except read-only into a
  declared proxy with its reason; critical. L1 · fix J · adopt.
- [ ] **CO19** `NO-PRIVILEGED`: no `privileged`, `network_mode: host`, `pid: host` or added
  `SYS_ADMIN`, beside `HARDENED-CONTAINERS`. L1 · fix J · adopt.
- [ ] **CO21** `LOG-ROTATION`: `max-size` and `max-file` on the logging driver (json-file grows
  without end by default). L1 · fix S · adopt.
- [ ] **CO22** `RESOURCE-LIMITS`: memory and CPU limits per service. L1 · fix S · trial.

### T-229 · Compose that survives: restarts, volumes, secrets, scanned and signed images
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Containers), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.20, "Compose files for a small server": What a VPS running compose needs: no engine
socket, databases on localhost, logs rotated, limits and restarts, secrets out of the file, images
scanned and signed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CO23** `RESTART-POLICY`: `restart: unless-stopped` or `always` on long-running services. L1
  · fix S · adopt.
- [ ] **CO24** `NAMED-VOLUMES`: database data in named volumes, never bind-mounted inside the repo.
  L1 · fix S · trial.
- [ ] **CO25** `NO-SECRETS-IN-COMPOSE`: no literal password under `environment:`; `env_file` or
  `secrets:` instead. L1 · fix J · adopt.
- [ ] **CO26** `IMAGES-SCANNED`: built images scanned (Trivy, Grype) in the release workflow. L1 ·
  fix S · trial.
- [ ] **CO27** `IMAGES-SIGNED`: published images signed (cosign) or attested
  (`actions/attest-build-provenance`). L1 · fix S · assess.
- [ ] **CO30** `ROOTLESS-FRIENDLY`: compose files that run under rootless Podman as under Docker
  (`kiln dev` runs Podman). L1 · fix J · assess.

### T-230 · One CI model: every step resolved, injection and privileges on any CI
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Every kind of
  repo, every profile, Mature tools as detectors, Tests), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.21, "One CI model, any workflow": Jobs, steps, triggers and permissions extracted
once; `make test` resolved into what it runs; zizmor and actionlint as detectors; the scored CI
rules read from that model.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C01** A CI model: jobs, steps, commands, triggers, permissions, pinned references, secrets
  used, images. Extracted from every CI format so one rule speaks of all of them (appendix B).
- [ ] **C04** Indirections followed: a step running `make test`, `just check`, `task lint`, `nox`,
  `tox`, `npm run test`, `./gradlew check` or `kiln check` is resolved into what it runs, so
  TESTS-IN-CI knows tests really run (a regex on the workflow today).
- [ ] **C05** PINNED-ACTIONS generalized to every CI's references: GitHub `uses:` by SHA, GitLab
  `include` refs and component versions, CircleCI orbs, Jenkins `@Library`, Buildkite plugins,
  images in `container:`, `services:` and `image:` by digest.
- [ ] **C06** Injection rules for every CI: GitHub's `${{ github.event… }}` in `run:`, GitLab's
  `$CI_COMMIT_MESSAGE` or `$CI_MERGE_REQUEST_TITLE` in `script:`, Azure's
  `$(Build.SourceVersionMessage)`, Jenkins' Groovy-interpolated `sh "…${env.CHANGE_TITLE}"`.
- [ ] **C07** Least privilege for every CI token: GitHub's `permissions:`, GitLab's job token
  allowlist, their Bitbucket and Azure counterparts.
- [ ] **C22** Reusable CI pieces (GitHub reusable workflows, GitLab components, CircleCI orbs)
  followed one level, at their pinned version, with `--online`: a reusable workflow that grants
  `write-all` is the caller's problem too.
- [ ] **D16** GitHub Actions as a kind: `action.yml` valid, a supported `runs.using`, `dist/`
  rebuilt and compared in CI, inputs documented, no `${{ inputs.x }}` inside `run:`.
- [ ] **F04** zizmor for GitHub Actions (template injection, excessive permissions, unpinned uses,
  persisted credentials, cache poisoning, dangerous triggers, impostor commits, known-vulnerable
  actions): a Rust wheel, mapped onto WORKFLOW-INJECTION, PULL-REQUEST-TARGET, PINNED-ACTIONS,
  WORKFLOW-PERMISSIONS and new rules.
- [ ] **F06** actionlint for workflow correctness (expressions, contexts, job dependencies).
- [ ] **TE02** `TESTS-IN-CI` (scored): read from the CI's commands for each component (pytest,
  Vitest, `go test`, `cargo test`, `mvn verify`), on any CI (C), through `make`, `just` and package
  scripts, not a regex for `pytest`.

### T-231 · The scored CI rules read from the CI model
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (CI/CD), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.21, "One CI model, any workflow": Jobs, steps, triggers and permissions extracted
once; `make test` resolved into what it runs; zizmor and actionlint as detectors; the scored CI
rules read from that model.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CI01** `CI-PRESENT` (scored): "every change is checked before it ships" (decision 6): fast
  checks at each commit and the whole CI before each release, on the forge or on the machine with
  its verdict kept (`kiln ci`), or a CI on every pull request; read from any CI (C) with its
  triggers. With profiles (T-39), company and enterprise ask for CI on every pull request.
- [ ] **CI02** `LINT-IN-CI` (scored): lint commands read per component from any CI, as for
  `TESTS-IN-CI` (TE), through `make`, `just`, `task`, `nox`, `tox` and package scripts.
- [ ] **CI03** `WORKFLOW-INJECTION` (scored): zizmor's template-injection audit (F) instead of one
  regex; an expression passed through `env:` passes.
- [ ] **CI04** `WORKFLOW-PERMISSIONS` (scored): `write-all`, and a job's `contents: write` with no
  step that writes, flagged.
- [ ] **CI05** `PULL-REQUEST-TARGET` (scored): flagged when the workflow checks out or runs the pull
  request's head; `workflow_run` with downloaded artifacts too (zizmor's dangerous-triggers).

### T-232 · Fast pipelines: concurrency, caches, runners, actionlint, zizmor
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (CI/CD), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.22, "Fast and safe pipelines": Concurrency, caches and retention, supported runners,
secrets through `env:`, reusable workflows pinned, provenance on what ships, the same CI on a
laptop.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CI07** `CI-CONCURRENCY`: `concurrency:` with `cancel-in-progress` on pull-request runs. L1 ·
  fix S · adopt.
- [ ] **CI09** `CI-CACHES`: dependency caches on (setup-uv's `enable-cache`, setup-node's `cache`).
  L1 · fix S · adopt.
- [ ] **CI11** `ARTIFACT-RETENTION`: `retention-days` on uploaded artifacts. L1 · fix S · trial.
- [ ] **CI12** `SUPPORTED-RUNNERS`: no runner image GitHub has retired (`ubuntu-20.04` in 2025,
  older macOS ones), a calendar like the runtimes'. L1 · fix S · adopt.
- [ ] **CI14** `ACTIONLINT`: actionlint passes (expressions, types, the shellcheck it embeds). L4 ·
  fix J · adopt.
- [ ] **CI15** `ZIZMOR-CLEAN`: zizmor's audits pass, run by kiln or in CI. L4 · fix J · trial.
- [ ] **CI17** `CACHE-POISONING`: release workflows restore no cache that pull requests can write
  (zizmor's cache-poisoning). L4 · fix J · trial.

### T-233 · Safe pipelines: secrets through `env`, pinned reusable workflows, provenance
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (CI/CD), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.22, "Fast and safe pipelines": Concurrency, caches and retention, supported runners,
secrets through `env:`, reusable workflows pinned, provenance on what ships, the same CI on a
laptop.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CI18** `SECRETS-THROUGH-ENV`: `${{ secrets.X }}` passed through `env:`, never inlined in
  `run:`. L2 · fix S · adopt.
- [ ] **CI19** `REUSABLE-WORKFLOWS-PINNED`: `uses: org/repo/.github/workflows/x.yml@<sha>`
  (`PINNED-ACTIONS` extended); kiln's own workflows, cited by tag and moved by `kiln update`, stay
  one accepted way. L1 · fix S · adopt.
- [ ] **CI20** `ACTIONS-UPDATED`: the `github-actions` ecosystem in the update bot's config
  (`DEPENDENCY-UPDATES` per ecosystem). L1 · fix S · adopt.
- [ ] **CI22** `MATRIX-COVERS-SUPPORT`: a library's CI matrix covers the versions it claims
  (`requires-python`, `engines`). L1 · fix S · trial.
- [ ] **CI23** `PROVENANCE`: release artifacts attested (`actions/attest-build-provenance`, PyPI's
  attestations); T-90 asks it of kiln. L1 · fix S · trial.
- [ ] **CI24** `BUILD-ONCE`: the artifact deployed is the one tested (an image promoted by digest),
  never rebuilt per environment. L2≈ · fix J · assess.
- [ ] **CI25** `CI-REPLAYABLE`: the CI's commands run on a laptop too (`kiln ci`, `make ci`, `just
  ci`). L1≈ · fix J · trial.

### T-234 · Tests counted right: presence, clock, network, coverage, strict pytest
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Tests), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.23, "Tests that prove something": Tests per component that assert, run shuffled and
in parallel, without network or sleep, coverage that only rises; a front with no backend gets its
smoke test.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **TE01** `TESTS-PRESENT` (scored): per component, and a test file that collects nothing
  doesn't count (pytest's `--collect-only` with `--deep`).
- [ ] **TE03** `CLOCK` (draft): tests calling `now()`, `date.today()` or `Date.now()` with no
  time-machine, freezegun or `vi.useFakeTimers` in reach. L3≈ · fix J · trial.
- [ ] **TE04** `NO-NETWORK` (draft): sockets blocked in tests (pytest-socket's `--disable-socket`,
  msw with `onUnhandledRequest: "error"`, nock's `disableNetConnect`). L1 · fix S · trial.
- [ ] **TE09** `PERMISSION-TESTS` (draft): each protected route (from the URL conf or Ninja's
  routers) has a test that calls it anonymously. L3≈ · fix J · trial.
- [ ] **TE11** `COVERAGE-MEASURED`: coverage with branches (`[tool.coverage.run] branch = true`,
  Vitest's coverage provider). L1 · fix S · adopt.
- [ ] **TE12** `COVERAGE-FLOOR`: a floor that only rises (`fail_under`, Vitest's thresholds with
  `autoUpdate`). L1 · ratchet · trial.
- [ ] **TE13** `DIFF-COVERAGE`: changed lines covered in pull requests (diff-cover). L1 · fix S ·
  assess.
- [ ] **TE14** `PYTEST-STRICT`: `--strict-markers`, `--strict-config`, `xfail_strict = true`,
  warnings as errors with a named allow-list. L1 · fix S · adopt.
- [ ] **TE15** `NO-FOCUSED-TESTS`: no `.only`, `fit` or `fdescribe` committed. L2 · fix S · adopt.
- [ ] **TE16** `NO-SKIPPED-TESTS`: every `skip` and `xfail` gives a reason, and their count only
  goes down. L2 · ratchet · trial.

### T-235 · Tests that prove something: no sleeps, random order, assertions, names
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Tests), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.23, "Tests that prove something": Tests per component that assert, run shuffled and
in parallel, without network or sleep, coverage that only rises; a front with no backend gets its
smoke test.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **TE17** `NO-SLEEP-IN-TESTS`: no `time.sleep` or `setTimeout` waits; a frozen clock or polling
  instead. L2 · fix J · trial.
- [ ] **TE18** `RANDOM-ORDER`: tests run shuffled (pytest-randomly, Vitest's `sequence.shuffle`) so
  hidden coupling shows. L1 · fix S · trial.
- [ ] **TE19** `PARALLEL-TESTS`: pytest-xdist or the runner's workers, for suites over a minute. L1
  · fix S · trial.
- [ ] **TE20** `ASSERTIONS-PRESENT`: no test without an assertion (`expect-expect` for Vitest and
  Jest, a syntax check for pytest). L2 · fix J · trial.
- [ ] **TE21** `FACTORIES`: factory_boy, model-bakery or fishery rather than big JSON fixtures. L1≈
  · fix J · assess.
- [ ] **TE24** `TESTS-TYPE-CHECKED`: tests not excluded from the type checker. L1 · fix S · trial.
- [ ] **TE25** `TEST-NAMES`: names that state the behaviour (`test_refuses_expired_token`), never
  `test_1` or `test_view`. L2≈ · fix J · assess.
- [ ] **TE26** `SNAPSHOTS-IN-CHECK`: obsolete snapshots fail in CI (`--ci`), snapshot files stay
  small. L1 · fix S · assess.
- [ ] **TE27** `CONTRACT-TESTS`: consumer-driven contracts (Pact) between the services of one
  organisation. L1 · fix J · assess.
- [ ] **TE28** `LOAD-SCENARIO`: a k6 or Locust scenario kept in the repo of an app with an SLO. L0 ·
  fix J · assess.

### T-236 · No new finding: history, the score of a change, `--compare`, PR comments
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, Speed, Nothing to do, Outputs
  and integrations, History, forge and registries, One measure drives every command), made a ticket
  on 25 October 2026 at antoine's request

Planned in v0.6.24, "Progress, not perfection: no new finding": The score of a change, a comparison
with any ref, gates on new findings only, scores kept in git notes and drawn as a curve.

- [ ] **I12** `kiln score --history`: the score at each tag or merge (cheap with the cache), drawn
  as a curve; "41 to 78 since adoption".
- [ ] **I13** The score of a change: "this branch takes the score from 74 to 76; 1 new finding, 3
  fixed". The gate is "no new finding", never an absolute number.
- [ ] **J23** `--first` for hooks: stop at the first critical finding.
- [ ] **K09** Exit code 0 by default, since it is a measure; gates are explicit: `--fail-under 80`,
  `--fail-on critical`, `--no-new` against a baseline or the integration branch.
- [ ] **L08** `--compare <ref or report.json>`: new, fixed and still-open findings, the delta, the
  rules that started or stopped applying.
- [ ] **L09** Pull request comments by the action: the delta, new findings as review comments on the
  diff's lines, fixed ones thanked.
- [ ] **L11** Scores kept in git notes (`refs/notes/kiln-score`), as `kiln ci` keeps its verdicts:
  history for free, travelling with the repo when pushed.
- [ ] **M30** `--at <ref>`: the repo scored as it was at a tag or a commit (a throwaway worktree,
  cached).
- [ ] **P10** `kiln check` includes "no new finding against the integration branch".

### T-237 · One funnel for every repo: baselines, `kiln adopt` scored before and after
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, The detection engine, One
  measure drives every command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.25, "One funnel for every repo, new or old": `kiln adopt` as score, lay, fix,
roadmap, its result shown before it runs; baselines for the gradual path; the template a repo
started from recognised; `kiln new` as the same funnel run on an empty folder.

- [ ] **A38** The template a repo started from, fingerprinted (kiln, cookiecutter-django,
  create-next-app, `nuxi init`, `rails new`, Spring Initializr, the Laravel installer): what that
  template changed since can be compared.
- [ ] **E25** Baselines: `kiln score --baseline` records today's findings, and from then on only new
  ones fail a gate. The progressive path of doctrine 9 for any repo, not only kiln's.
- [ ] **P03** The radical form: `kiln new` as an empty folder, then `kiln adopt`, then `kiln fix`.
  The template and the converters can't drift apart.
- [ ] **P06** `kiln adopt` as a funnel: score before, lay files, `kiln fix`, score after, roadmap
  tickets; each step a commit on its branch.
- [ ] **P07** `kiln adopt --dry-run` shows the score it would reach.

### T-238 · Only what changed: `--changed`, `--watch`, the edit hook
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Speed), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.26, "Only what changed, right after each edit": Tests and score rechecked on the
changed files only, on save and in Claude Code's edit hook, in milliseconds.

- [ ] **J11** `--changed`: only files changed since the merge base, and the repo-level rules whose
  inputs changed, are checked again.
- [ ] **J12** `--watch`: re-score on save (watchfiles, Rust), the changed file only.
- [ ] **J13** The Claude Code edit hook re-scores the edited file in milliseconds and tells Claude
  only what is new; one engine with the charter's `check_file.py`.

### T-239 · The score explained like a senior engineer would
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Rule format v2 and authoring, Scoring model v2,
  Nothing to do), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.27, "The score explained like a senior engineer would": The denominator, the weakest
themes, the effort to 100 in session hours, a verdict in plain words, `--explain` with this repo's
numbers.

- [ ] **G06** `effort` per place and per rule, in session minutes, and `impact`: the roadmap's order
  and the effort-to-100 estimate come from them.
- [ ] **I05** Scores per component and per theme, under the five pillars; under each pillar, its
  weakest themes (decision 5).
- [ ] **I06** The denominator explained: "31 rules apply: Python, Django, Docker, GitHub Actions"; a
  new Dockerfile says "5 more rules apply now, 2 met".
- [ ] **I08** Effort to 100 from the rules' effort estimates, in session hours, the backlog's unit.
- [ ] **I16** Remediation time in hours per rule and in total: a debt figure for practices.
- [ ] **I17** `kiln score --explain`: the formula with this repo's numbers in it.
- [ ] **I18** One function computes the score everywhere (CLI, badge, bot, fleet, HTML), with golden
  tests.
- [ ] **I19** The score model versioned (`score_model` in the JSON); a change re-scores the
  reference repos and the release note says its effect.
- [ ] **I20** "Rules met" stays on the first line (24 of 31): plainer than a percentage for a
  newcomer.
- [ ] **I21** A verdict in plain words generated from the findings, no model needed: "well tested,
  but the supply chain is open: unpinned actions and images, no update bot".
- [ ] **K15** Explanations a newcomer understands (one sentence, no jargon) and `--explain` for the
  details: "like a senior engineer would, even if you're not one".

### T-240 · A report you can share: every format, HTML, `--quiet`, `--porcelain`
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Outputs and integrations, Trust, privacy and
  safety), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.28, "A report you can share": Every format a CI or a tool reads, a one-file HTML
report, links to each rule's page and to the line on the forge, nothing personal left in it.

- [ ] **L01** `--format`: text, json, sarif, junit, markdown, html, csv, gitlab-codequality,
  github-annotations, checkstyle.
- [ ] **L04** JUnit XML, each rule a test case, for Jenkins, Azure and any CI's test tab.
- [ ] **L06** A self-contained HTML report in one file: the score, the pillars with their weakest
  themes, findings with snippets, filters, the potential bar, the history curve.
- [ ] **L14** `--quiet` (the number only) and `--porcelain` (stable lines for scripts).
- [ ] **L15** `kiln grid --json`: the whole catalogue for other tools.
- [ ] **L17** `--open`: the HTML report in the browser.
- [ ] **L19** The report's absolute `root` left out by default: it names the user's home when
  shared.
- [ ] **L21** A finding links to its rule's page and to the line on the forge when the remote is
  known (`https://github.com/o/r/blob/<sha>/path#L12`).
- [ ] **S04** Shareable reports: no absolute paths, user names or e-mail addresses.

### T-241 · Code that can be attacked: taint, permissions, uploads, injections, crypto
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Application security), made
  a ticket on 25 October 2026 at antoine's request

Planned in v0.6.29, "Code that can be attacked": Injection, unsafe deserialization, weak crypto,
open redirects, SSRF and the rest, with taint followed inside a function.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **E11** Taint inside one function: a request value (`request.GET`, `request.data`, route
  parameters, `req.query`) reaching a sink (`execute`, `os.system`, `open`, `redirect`,
  `subprocess`, `eval`) without a known sanitizer.
- [ ] **AS06** `EXPLICIT-PERMISSIONS` (draft): every route states its authentication (Ninja's
  `auth=`, DRF's `permission_classes`), and the default isn't `AllowAny`. L2 · fix J · adopt.
- [ ] **AS07** `PUBLIC-ROUTES` (draft): public routes listed in one place, everything else
  authenticated by default. L2≈ · fix J · trial.
- [ ] **AS08** `UPLOADS` (draft): uploads validated (size limits, type by content, storage outside
  the web root, random names). L2≈ · fix J · trial.
- [ ] **AS13** `VALIDATE-AT-BOUNDARIES` (draft): request data parsed by a schema before use. L2≈ ·
  fix J · trial.
- [ ] **AS14** `NO-EVAL`: no `eval`, `exec`, `new Function` or string `setTimeout`. L2 · fix J ·
  adopt.
- [ ] **AS15** `NO-SHELL-INJECTION`: no `shell=True` or `os.system` on non-literal input, no
  `child_process.exec` with template strings (S602 to S605). L2 · fix J · adopt.
- [ ] **AS16** `NO-UNSAFE-DESERIALIZATION`: no pickle, marshal, `yaml.load`, `ObjectInputStream` or
  `unserialize` on outside data (S301, S506). L2 · fix S (`yaml.safe_load`) · adopt.
- [ ] **AS17** `NO-XXE`: XML parsed with defusedxml or safe defaults (S313 to S320). L4 · fix S ·
  adopt.
- [ ] **AS18** `NO-WEAK-CRYPTO`: no MD5 or SHA-1 for security, no DES, RC4 or ECB (S324, S303 to
  S305). L4 · fix J · adopt.
- [ ] **AS48** `NO-SQL-INJECTION`: no query built from a variable by concatenation, `%` or an
  f-string: `raw`, `extra` and `RawSQL` of Django, `text` of SQLAlchemy, a DB-API `execute`; each
  stack's pack adds its own APIs (T-336, T-337, T-338, T-339). L2 · fix J · adopt.

### T-242 · Code that can be attacked: redirects, SSRF, paths, escaping, JWT, SAST
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Application security), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.29, "Code that can be attacked": Injection, unsafe deserialization, weak crypto,
open redirects, SSRF and the rest, with taint followed inside a function.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS19** `SECURE-RANDOM`: tokens from `secrets` or `crypto.randomUUID`, never `random` or
  `Math.random` (S311). L2 · fix S · adopt.
- [ ] **AS29** `NO-OPEN-REDIRECT`: redirects to a request value checked
  (`url_has_allowed_host_and_scheme`). L2 · fix J · adopt.
- [ ] **AS30** `NO-SSRF`: outgoing requests to user-given URLs pass an allowlist. L2≈ · fix J ·
  trial.
- [ ] **AS31** `NO-PATH-TRAVERSAL`: files opened from request values resolved and confined. L2≈ ·
  fix J · trial.
- [ ] **AS33** `AUTOESCAPE`: no `|safe`, `mark_safe`, `{% autoescape off %}`, `v-html` or
  `dangerouslySetInnerHTML` on variables (with NO-V-HTML). L2 · fix J · adopt.
- [ ] **AS34** `JWT-SAFE`: algorithms pinned (never `none`), signature and expiry checked. L2 · fix
  J · adopt.
- [ ] **AS40** `SAST-IN-CI`: CodeQL, semgrep or the language's security linter in CI. L1 · fix S ·
  adopt.
- [ ] **AS46** `GRAPHQL-LIMITS`: depth and cost limits, introspection off in production. L2≈ · fix J
  · trial.
- [ ] **AS47** `EXPRESS-HARDENED`: Helmet or equivalent headers, `x-powered-by` off. L2 · fix S ·
  trial.

### T-243 · A metrics pass and misspellings, in any language
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Mature tools as detectors),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.30, "Sizes and names, measured in any language": A metrics pass for every language
feeds the size and complexity ratchets; names, cases and misspellings judged from symbol tables.

- [ ] **E13** A metrics pass: lines and logical lines per file and function, cyclomatic and
  cognitive complexity, nesting, parameters, token duplication, comment density, TODOs, for any
  language (lizard's approach), feeding the size and complexity ratchets.
- [ ] **F15** typos (Rust) for misspellings in identifiers and comments, with very few false
  positives.

### T-244 · Sizes and names measured: files, functions, complexity, naming
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.30, "Sizes and names, measured in any language": A metrics pass for every language
feeds the size and complexity ratchets; names, cases and misspellings judged from symbol tables.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS01** `FILE-SIZE` (draft): lines per file from the index, generated code and migrations
  aside, a ratchet from today's numbers. L0 · ratchet · trial.
- [ ] **CS02** `FUNCTION-SIZE` (draft): function length from syntax trees in any language (ruff's
  PLR0915 for Python). L2 · ratchet · trial.
- [ ] **CS03** `CASE` (draft): symbols cased as their language wants (pep8-naming through ruff's N8,
  typescript-eslint's naming convention), from symbol tables. L2 · fix J · trial.
- [ ] **CS04** `BOOLEANS` (draft): names of `bool`-typed values start with is, has, can or should
  (Python annotations, TS types). L2 · fix J · assess.
- [ ] **CS05** `GENERIC-NAMES` (draft): identifiers from a deny-list (`data`, `res`, `tmp`, `obj`,
  `val`, `info`, `item`, `stuff`, `foo`), one list per human language. L2≈ · fix J · trial.
- [ ] **CS08** `ONE-CLASS` (draft): one public class per file in Python and TS. L2 · fix J · assess.
- [ ] **CS28** `COMPLEXITY`: cognitive complexity under about 15 per function. L2 · ratchet · trial.
- [ ] **CS30** `NESTING-DEPTH`: four levels of nesting at most. L2 · ratchet · trial.
- [ ] **CS33** `NAMES-WITH-UNITS`: durations, sizes and amounts named with their unit
  (`timeout_seconds`, `size_bytes`). L2≈ · fix J · assess.
- [ ] **CS34** `FILE-NAMES-CASE`: file names in the language's convention (snake_case.py,
  PascalCase.vue components, kebab-case routes). L0 · fix J · trial.
- [ ] **CS45** `TYPOS`: no common misspelling in identifiers and comments (the typos dictionary). L4
  · fix S · trial.

### T-245 · oxlint or Biome mapped, barrel files counted
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Structure), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.31, "Code standards from the syntax tree": What a regex can't tell: modern Vue,
explicit imports, floating promises, debug prints, TODOs without a ticket, barrel files, with oxlint
or Biome where they decide.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F07** oxlint or Biome for JS/TS rules (no-eval, eqeqeq, no-debugger, accessibility) as
  native binaries (T-144 measures them).
- [ ] **ST12** `NO-BARREL-FILES`: no `index.ts` re-exporting a whole folder (slower bundles and
  tests, one more hop for Claude). L2 · fix J · assess.

### T-246 · TypeScript and Vue standards from the syntax tree
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.31, "Code standards from the syntax tree": What a regex can't tell: modern Vue,
explicit imports, floating promises, debug prints, TODOs without a ticket, barrel files, with oxlint
or Biome where they decide.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS07** `MODERN-VUE` (draft): `<script setup>`, no Options API in new files, `defineModel`,
  no `this.$`. L2 · fix J · trial.
- [ ] **CS10** `EXPLICIT-IMPORTS` (draft, Nuxt): auto-imported composables used without an import,
  counted. L2 · fix S · assess.
- [ ] **CS12** `ASYNC-AWAIT` (draft, TS): `.then()` chains where `await` reads better; floating
  promises with `--deep`, since they need types. L2 · fix J · assess.
- [ ] **CS19** `NO-PRINT-DEBUG`: no `print()` or `console.log` in shipped code (ruff's T20,
  no-console), command-line tools aside. L2 · fix J · adopt.
- [ ] **CS20** `TODO-WITH-TICKET`: each TODO or FIXME cites a ticket (`T-12`, `#123`); the backlog
  is the only list. L2 · ratchet · trial.
- [ ] **CS32** `NO-GLOBAL-MUTATION`: no `global` statements, no module-level state changed by
  functions. L2 · fix J · trial.
- [ ] **CS35** `VUE-MULTI-WORD-COMPONENTS`: component names of two words or more (Vue's style guide,
  essential). L0 · fix J · adopt.
- [ ] **CS36** `TS-NO-NON-NULL-ASSERTION`: `!` assertions counted. L2 · ratchet · trial.
- [ ] **CS37** `TS-NO-ENUMS`: `as const` unions rather than `enum` (erasable syntax, which Node's
  type stripping runs). L2 · fix S · assess.
- [ ] **CS38** `ESM`: `"type": "module"` and no `require()` in TypeScript. L1 · fix J · trial.
- [ ] **CS39** `NO-VAR` and `STRICT-EQUALITY` (JS): `let` and `const`, `===`. L2 · fix S · adopt.
- [ ] **CS44** `NO-NESTED-TERNARY`. L2 · fix J · trial.

### T-247 · API contracts: the schema committed and frozen, typed routes, pagination
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (API, contracts and typing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.32, "API, contracts and typing": The schema committed and checked for breaking
changes, front types generated from it, typing read through its inheritance and counted as ratchets.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AT01** `OPENAPI-IN-REPO` (draft): the API's schema committed (`openapi.json` or `.yaml`)
  when an API framework is present (Django Ninja, DRF, FastAPI, NestJS). L0 · fix J · trial.
- [ ] **AT02** `FROZEN-CONTRACT` (draft): CI compares the schema with the integration branch's
  (oasdiff's breaking-change check). L1 · fix S (the CI step) · trial.
- [ ] **AT03** `CONTRACT-DRIFT` (draft): front types generated from the committed schema
  (openapi-typescript or the like) with a script to regenerate them; `--deep` proves there's no
  drift. L1 · fix J · trial.
- [ ] **AT04** `TYPED-API` (draft, Ninja): every route has typed input and output schemas. L2 · fix
  J · trial.
- [ ] **AT05** `PAGINATION` (draft): list endpoints paginated (`@paginate`, DRF's
  `DEFAULT_PAGINATION_CLASS`). L2 · fix J · trial.
- [ ] **AT06** `DEPRECATION-HEADERS` (draft): deprecated routes send `Deprecation` (RFC 9745) and
  `Sunset` (RFC 8594). L2≈ · fix J · assess.
- [ ] **AT07** `IDEMPOTENCY` (draft): payment and creation endpoints accept an `Idempotency-Key`.
  L2≈ · fix J · assess.
- [ ] **AT08** `STRICT-TYPING` and `STRICT-TS` (scored): config read with its inheritance (`extends`
  chains, `[tool.mypy]` anywhere), not by one regex.
- [ ] **AT09** `TYPE-CHECK-IN-CI`: a type checker runs in CI (mypy, pyright, ty or pyrefly; tsc,
  vue-tsc or `nuxi typecheck`). L1 · fix S · adopt.

### T-248 · Strict typing everywhere: libraries, annotations, TypeScript options, problem details
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (API, contracts and typing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.32, "API, contracts and typing": The schema committed and checked for breaking
changes, front types generated from it, typing read through its inheritance and counted as ratchets.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AT10** `PY-TYPED`: a typed Python library ships `py.typed`. L0 · fix S · adopt.
- [ ] **AT11** `ANNOTATIONS-COVERAGE`: the share of fully annotated functions, a ratchet (ruff's ANN
  counts). L4 · ratchet · trial.
- [ ] **AT12** `NO-EXPLICIT-ANY` (Python): `Any` counted (ANN401), as NO-ANY does for TS. L4 ·
  ratchet · trial.
- [ ] **AT13** `TS-UNCHECKED-INDEX`: `noUncheckedIndexedAccess` on. L1 · fix S · trial.
- [ ] **AT14** `TS-EXACT-OPTIONAL`: `exactOptionalPropertyTypes` on. L1 · fix J · assess.
- [ ] **AT15** `TS-VERBATIM-MODULES`: `verbatimModuleSyntax` on. L1 · fix S · assess.
- [ ] **AT16** `DJANGO-STUBS`: django-stubs and its mypy plugin whenever mypy checks Django code. L1
  · fix S · adopt.
- [ ] **AT17** `PROBLEM-DETAILS`: API errors as RFC 9457 problem details. L2≈ · fix J · assess.
- [ ] **AT18** `API-VERSIONED`: public APIs carry a version, in the path or a header. L2≈ · fix J ·
  assess.

### T-249 · Clients and schemas generated, not copied: OpenAPI lint, GraphQL, Protobuf, settings
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (API, contracts and typing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.32, "API, contracts and typing": The schema committed and checked for breaking
changes, front types generated from it, typing read through its inheritance and counted as ratchets.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AT19** `OPENAPI-LINT`: the committed schema passes Spectral or Redocly's lint. L4 · fix J ·
  trial.
- [ ] **AT20** `GENERATED-CLIENT`: the front reaches the API through generated types, never
  hand-copied ones. L2≈ · fix J · trial.
- [ ] **AT21** `TYPED-PROPS`: `defineProps<…>()` and `defineEmits<…>()` typed. L2 · fix J · adopt.
- [ ] **AT22** `RUNTIME-SCHEMAS`: outside data parsed by a schema library (Pydantic, Zod, Valibot)
  at the edge. L2≈ · fix J · trial.
- [ ] **AT23** `GRAPHQL-SCHEMA`: the GraphQL schema committed and checked for breaking changes. L1 ·
  fix J · trial.
- [ ] **AT24** `PROTO-LINT`: `buf lint` and `buf breaking` for Protobuf APIs. L1 · fix S · trial.
- [ ] **AT29** `SETTINGS-TYPED`: application settings parsed into a typed object (pydantic-settings,
  a schema-checked runtime config). L2≈ · fix J · trial.

### T-250 · The import graph: cycles, feature folders, change coupling
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, History, forge and
  registries, Structure), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.33, "Architecture you can see": An import graph per language: cycles, layers, sealed
domains, god modules, files that always change together.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **E09** Cross-file detectors: every job that tests also lints; every Django app with models
  registers an admin or says why; every route has a test that calls it (routes extracted, tests
  searched).
- [ ] **E10** An import graph per language (Python's `ast`, an ES-module scanner): cycles, layers
  (SEALED-DOMAIN), dead modules, fan-in and fan-out.
- [ ] **M09** Change coupling: files that always change together across folders show a boundary in
  the wrong place.
- [ ] **ST01** `FEATURE-FOLDERS` (draft): layer folders (`models/`, `views/`, `services/`,
  `controllers/`) that each span several domains, found by clustering the import graph. L3≈ · fix J
  · trial.
- [ ] **ST13** `NO-IMPORT-CYCLES`: no cycle between modules or packages. L3 · ratchet · trial.

### T-251 · Architecture you can see: thin views, a service layer, sealed domains
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Architecture), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.33, "Architecture you can see": An import graph per language: cycles, layers, sealed
domains, god modules, files that always change together.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AR02** `API-CALLS` (draft, Vue): no `$fetch` or `useFetch` in components outside a
  composable or a service layer. L2 · fix J · trial.
- [ ] **AR03** `THIN-VIEWS` (draft, Django): views under a few dozen lines, without ORM writes. L2≈
  · fix J · trial.
- [ ] **AR04** `THIN-MODEL` (draft, Django): model methods past a few dozen lines flagged. L2≈ · fix
  J · assess.
- [ ] **AR05** `SERVICE-LAYER` (draft): an app whose views write data has a services module. L2≈ ·
  fix J · assess.
- [ ] **AR06** `LAYERED-ARCHITECTURE` (draft): import contracts declared (import-linter,
  dependency-cruiser, eslint-plugin-boundaries) and run in CI. L1 · fix J · trial.
- [ ] **AR07** `SEALED-DOMAIN` (draft): domain packages import no web framework, HTTP client or ORM
  session. L3 · fix J · trial.
- [ ] **AR08** `TWELVE-FACTOR-CONFIG`: config from the environment, one settings tree, no
  per-environment file holding secrets. L2 · fix J · adopt.
- [ ] **AR09** `NO-GOD-MODULES`: no module both large and imported by most of the code. L3 · ratchet
  · assess.

### T-252 · Boundaries between front, back and services: stores, async, one database each
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Architecture), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.33, "Architecture you can see": An import graph per language: cycles, layers, sealed
domains, god modules, files that always change together.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AR12** `STATE-IN-STORES` (Vue): shared state in Pinia stores, not module-level `reactive()`
  singletons. L2 · fix J · trial.
- [ ] **AR13** `NUXT-SERVER-THIN`: `server/api` handlers delegate to services. L2≈ · fix J · assess.
- [ ] **AR14** `ONE-DB-PER-SERVICE`: two services don't share one database's tables (compose and
  settings read together). L1≈ · fix J · assess.
- [ ] **AR15** `ASYNC-BOUNDARY` (Django): async views never call the sync ORM without
  `sync_to_async`. L2 · fix J · adopt.
- [ ] **AR16** `DEPENDENCY-DIRECTION`: stable packages don't depend on volatile ones (fan-in and
  fan-out). L3 · ratchet · assess.
- [ ] **AR17** `NO-CIRCULAR-APPS` (Django): no import cycle between apps. L3 · fix J · trial.
- [ ] **AR18** `FLAGS-IN-ONE-PLACE`: feature flags read through one module or library, not scattered
  `if settings.X`. L2≈ · fix J · assess.

### T-253 · Migrations safe and reversible, linted in CI
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Mature tools as detectors, Data
  and migrations), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.34, "Data and migrations": Migrations reversible, safe on a live table, linted in
CI, run on the production engine; dumps out of git; invariants held by the database.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B16** SQL as code: sqlfluff, squawk for Postgres migrations, dbt projects.
- [ ] **F18** squawk and django-migration-linter for migrations, sqlfluff for SQL.
- [ ] **DM01** `MIGRATIONS` (scored): apps with an empty `models.py`, and apps under `tests/`, no
  longer asked for migrations.
- [ ] **DM02** `COMMON-FIELDS` (draft, Django): models inherit a base carrying `created_at` and
  `updated_at`. L2 · fix J · trial.
- [ ] **DM03** `INDEXES` (draft, Postgres): fields filtered or ordered on in querysets have an
  index. L3≈ · fix J · assess.
- [ ] **DM04** `TRANSACTIONS` (draft): views writing several rows do it in `transaction.atomic` (or
  `ATOMIC_REQUESTS`). L2≈ · fix J · trial.
- [ ] **DM05** `USE-TZ` (Django): `USE_TZ = True`. L2 · fix S · adopt.
- [ ] **DM06** `REVERSIBLE-MIGRATIONS`: `RunPython` with `reverse_code`, `RunSQL` with
  `reverse_sql`. L2 · fix J · adopt.
- [ ] **DM07** `SAFE-MIGRATIONS`: no NOT NULL column added without a default to an existing table;
  indexes built concurrently on Postgres (`AddIndexConcurrently`, `atomic = False`). L2≈ · fix J ·
  trial.
- [ ] **DM08** `SCHEMA-AND-DATA-APART`: data migrations (`RunPython`) in their own files. L2 · fix J
  · trial.
- [ ] **DM09** `MIGRATION-LINT-IN-CI`: django-migration-linter or squawk in CI. L1 · fix S · trial.
- [ ] **DM10** `MIGRATION-NAMES`: no `00xx_auto_<date>`: a migration's name says what it changes. L0
  · fix J · trial.

### T-254 · Data modelled right: constraints, public IDs, connections, seeds, the real engine in tests
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Data and migrations, Tests), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.34, "Data and migrations": Migrations reversible, safe on a live table, linted in
CI, run on the production engine; dumps out of git; invariants held by the database.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **DM11** `SQUASH-WHEN-LONG`: an app past about 100 migrations gets them squashed. L0 · fix J ·
  assess.
- [ ] **DM12** `ALEMBIC-ONE-HEAD`: a single head in Alembic's history. L2 · fix J · adopt.
- [ ] **DM13** `NO-DUMPS`: no `.sql`, `.dump` or `.sqlite3` holding real data committed. L0 · fix S
  (untracked) · adopt.
- [ ] **DM14** `DB-CONSTRAINTS`: invariants enforced by the database (`UniqueConstraint`,
  `CheckConstraint`), not only in code. L2≈ · fix J · trial.
- [ ] **DM15** `PUBLIC-IDS`: public identifiers that aren't sequential integers (UUIDv7, ULID), so
  nobody can enumerate them. L2≈ · fix J · assess.
- [ ] **DM16** `CONN-REUSE` (Django): `CONN_MAX_AGE` and `CONN_HEALTH_CHECKS` set, or a pooler. L2 ·
  fix S · trial.
- [ ] **DM17** `SUPPORTED-DATABASES`: Postgres, MySQL, Redis and MongoDB versions in compose and
  manifests still supported. L1 · fix S · adopt.
- [ ] **DM18** `ORM-MIGRATIONS-COMMITTED` (JS, Ruby): Prisma, Drizzle, Knex, TypeORM and Rails
  migrations (and `schema.rb`) committed. L0 · fix J · adopt.
- [ ] **DM19** `SEED-DATA`: a seed command or fixtures with fake data for local development. L0≈ ·
  fix J · trial.
- [ ] **DM20** `QUERIES-OUT-OF-VIEWS`: raw SQL lives in a query module, not in views. L2 · fix J ·
  assess.
- [ ] **TE22** `PROD-ENGINE-IN-TESTS`: tests run on the production database engine (a Postgres
  service in CI, Testcontainers), not SQLite. L1 · fix J · trial.
- [ ] **TE23** `MIGRATIONS-CHECKED`: `makemigrations --check --dry-run` in CI, and a migration from
  an empty database. L1 · fix S · adopt.

### T-255 · Background tasks that survive: retries, outbox, idempotence, limits
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Background tasks), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.35, "Background tasks and concurrency": Tasks that retry, time out, take IDs and run
outside the request; increments and locks that survive two requests at once; Celery's settings made
exact.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **BG01** `RETRIES` (draft): Celery tasks set `autoretry_for`, `retry_backoff` and
  `max_retries` (or the same in RQ, Dramatiq, Django 6's tasks). L2 · fix J · trial.
- [ ] **BG02** `OUT-OF-REQUEST` (draft): e-mails, webhooks and slow HTTP calls never sent inside a
  view. L2≈ · fix J · trial.
- [ ] **BG03** `TRANSACTIONAL-OUTBOX` (draft): tasks queued through `transaction.on_commit`, not
  inside an open transaction. L2≈ · fix J · trial.
- [ ] **BG04** `IDEMPOTENT-HANDLER` (draft): tasks guarded by a key or a state check. L2≈ · fix J ·
  assess.
- [ ] **BG05** `TASK-TIME-LIMITS`: hard and soft time limits set. L2 · fix S · adopt.
- [ ] **BG06** `ACKS-LATE`: `task_acks_late` with `task_reject_on_worker_lost` for idempotent tasks.
  L2 · fix S · trial.
- [ ] **BG07** `SAFE-SERIALIZER`: tasks serialized as JSON, never pickle. L2 · fix S · adopt.

### T-256 · Schedulers and workers watched: one scheduler, health, visibility, dead letters
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Background tasks), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.35, "Background tasks and concurrency": Tasks that retry, time out, take IDs and run
outside the request; increments and locks that survive two requests at once; Celery's settings made
exact.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **BG08** `ONE-SCHEDULER`: the beat or scheduler service runs as a single replica. L1 · fix J ·
  adopt.
- [ ] **BG09** `TASKS-TAKE-IDS`: tasks receive identifiers, not model instances. L2≈ · fix J ·
  trial.
- [ ] **BG10** `SCHEDULES-IN-CODE`: periodic jobs declared in code (beat schedule, django-q2), not
  in a host's crontab. L1≈ · fix J · trial.
- [ ] **BG11** `WORKER-HEALTH`: worker services have a health check and a stop grace period. L1 ·
  fix S · trial.
- [ ] **BG12** `VISIBILITY-TIMEOUT`: with a Redis broker, the visibility timeout exceeds the longest
  task. L2 · fix J · trial.
- [ ] **BG13** `DEAD-LETTERS`: failed tasks land where a human sees them. L2≈ · fix J · assess.

### T-257 · Concurrency: atomic updates, locks, timeouts, async servers, Celery made exact
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Concurrency, Framework packs), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.35, "Background tasks and concurrency": Tasks that retry, time out, take IDs and run
outside the request; increments and locks that survive two requests at once; Celery's settings made
exact.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CC01** `ATOMIC-INCREMENTS` (draft, Django): `x.n += 1` then `x.save()` becomes `F("n") + 1`.
  L2≈ · fix S · trial.
- [ ] **CC02** `LOCKS` (draft): a read-modify-write inside a transaction uses `select_for_update()`.
  L2≈ · fix J · trial.
- [ ] **CC03** `NO-BLOCKING-IN-ASYNC`: no `time.sleep`, `requests`, sync file or ORM call inside
  `async def` (ruff's ASYNC). L4 · fix J · adopt.
- [ ] **CC04** `TIMEOUTS`: every outgoing HTTP call has a timeout (ruff's S113; fetch with a signal,
  axios with `timeout`). L2 · fix S · adopt.
- [ ] **CC05** `DB-STATEMENT-TIMEOUT`: the database connection sets a statement timeout. L2 · fix S
  · trial.
- [ ] **CC06** `CHECK-THEN-ACT`: `if not exists(): create()` becomes `get_or_create` over a unique
  constraint. L2≈ · fix J · trial.
- [ ] **CC07** `ASGI-SERVER`: an async app served by an ASGI server (Uvicorn, Granian, Hypercorn,
  Daphne). L1 · fix J · adopt.
- [ ] **CC08** `WORKERS-SIZED`: the web server's worker count comes from the environment or the CPU
  count. L1 · fix S · trial.
- [ ] **CC10** `NO-THREADS-IN-REQUESTS`: no thread started inside a request handler. L2≈ · fix J ·
  trial.
- [ ] **FP06** Celery · the BG theme's rules, made exact for Celery's settings (`task_acks_late`,
  `task_time_limit`, the serializer, the beat replica). L1 · fix S · adopt.

### T-258 · Caches that invalidate and stay private
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Cache), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.36, "Fast back ends: caches and queries": Real cache backends with timeouts and
invalidation, N+1 queries and missing indexes found, latency budgets kept in the repo.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CA01** `CACHE-TAGS` (draft): invalidation by tags or versioned keys, never by guessing. L2≈
  · fix J · assess.
- [ ] **CA02** `CACHE-STAMPEDE` (draft): expensive recomputations protected (a lock, early refresh,
  jitter). L2≈ · fix J · assess.
- [ ] **CA03** `PROD-CACHE-BACKEND`: the production cache isn't `LocMemCache` or a dummy backend. L2
  · fix J · adopt.
- [ ] **CA04** `EXPLICIT-TIMEOUTS`: every `cache.set` gives a timeout. L2 · fix J · trial.
- [ ] **CA05** `IMMUTABLE-ASSETS`: hashed static assets served with `immutable` and a long max-age
  (Caddy, nginx, Nuxt's `routeRules`). L1 · fix S · trial.
- [ ] **CA06** `PRIVATE-RESPONSES`: authenticated responses are `private` or `no-store`; shared
  caches vary on authentication. L2≈ · fix J · trial.
- [ ] **CA07** `REDIS-EVICTION`: Redis runs with `maxmemory` and the eviction policy its use needs
  (a cache evicts, a broker never does). L1 · fix S · trial.

### T-259 · Fast back ends: N+1 queries, query counts, indexes, benchmarks
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Performance), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.36, "Fast back ends: caches and queries": Real cache backends with timeouts and
invalidation, N+1 queries and missing indexes found, latency budgets kept in the repo.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PE01** `API-LATENCY` (draft): p95 budgets as k6 thresholds in the repo, or an APM's numbers
  with `--online`. L1≈ · fix J · assess.
- [ ] **PE05** `NO-N-PLUS-ONE`: querysets iterated with related access and no `select_related` or
  `prefetch_related` (L3≈), proven by nplusone in tests (L7). L3≈ · fix J · trial.
- [ ] **PE06** `QUERY-COUNT-TESTS`: list views tested with `django_assert_num_queries` or
  `assertNumQueries`. L2 · fix J · assess.
- [ ] **PE14** `FK-INDEXES`: foreign keys indexed where neither the ORM nor the database does it
  (Prisma's relations on Postgres, raw SQL migrations); Django already does. L2 · fix S · trial.
- [ ] **PE16** `BENCHMARKS`: libraries with hot paths keep benchmarks (pytest-benchmark, Vitest's
  `bench`, `cargo bench`) and a ratchet on them. L1 · fix J · assess.
- [ ] **PE17** `PROFILER-IN-DEV`: a profiler wired in development only (django-silk, pyinstrument's
  middleware). L1 · fix S · assess.
- [ ] **PE19** `COLD-START`: serverless functions' bundle size tracked. L1 · ratchet · assess.

### T-260 · Errors and logs you can follow
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Errors and logs), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.37, "Errors and logs you can follow": Structured logs to stdout, no secret in them
and no stack trace shown, errors tracked with their release, a request ID and traces from the front
to the back.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **EL01** `STRUCTURED-LOGGING` (draft): structlog or a JSON formatter configured; the charter's
  `logging` ban promoted. L1 · fix J · trial.
- [ ] **EL02** `DOMAIN-ERRORS` (draft): an exception hierarchy per domain, mapped to HTTP in one
  place. L2≈ · fix J · assess.
- [ ] **EL03** `ERROR-TRACKING`: Sentry, GlitchTip, Rollbar or Honeybadger configured, for
  production profiles. L1 · fix J · trial.
- [ ] **EL04** `NO-PII-TO-TRACKER`: `send_default_pii=False` and scrubbing configured. L2 · fix S ·
  adopt.
- [ ] **EL05** `LOGS-TO-STDOUT`: in containers, logs go to stdout, no file handler. L2 · fix J ·
  adopt.
- [ ] **EL06** `LOG-LEVEL-FROM-ENV`. L2 · fix S · trial.
- [ ] **EL07** `LOG-EXCEPTIONS-WITH-TRACE`: `logger.exception` in handlers rather than
  `logger.error(str(e))` (TRY400). L4 · fix S · adopt.
- [ ] **EL08** `LAZY-LOG-FORMAT`: no f-strings in log calls (G004); key-value pairs with structlog.
  L4 · fix S · trial.
- [ ] **EL09** `NO-SECRETS-IN-LOGS`: no `password`, `token`, `secret` or `authorization` values
  passed to a log call. L2 · fix J · adopt.
- [ ] **EL10** `NO-STACK-TRACES-SHOWN`: production error pages hide internals (Django's `DEBUG`,
  Express's `NODE_ENV`, Nuxt's error page, Spring's `include-stacktrace`). L2 · fix J · adopt.
- [ ] **EL11** `UNHANDLED-REJECTIONS` (Node): a process-level handler that logs and exits. L2 · fix
  J · trial.

### T-261 · Requests traced: request IDs, OpenTelemetry, front errors, an audit trail
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Observability), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.37, "Errors and logs you can follow": Structured logs to stdout, no secret in them
and no stack trace shown, errors tracked with their release, a request ID and traces from the front
to the back.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OB01** `REQUEST-ID` (draft): a request-ID middleware (django-guid, asgi-correlation-id) with
  the ID in the log format and the response headers. L2 · fix S · trial.
- [ ] **OB02** `OPENTELEMETRY` (draft): the OpenTelemetry SDK configured from `OTEL_*` variables,
  the framework and HTTP clients instrumented, `traceparent` forwarded from the front. L2 · fix S ·
  trial.
- [ ] **OB06** `FRONT-ERRORS-CAPTURED`: browser errors reported (Sentry for Vue and Nuxt), source
  maps uploaded privately. L1 · fix S · trial.
- [ ] **OB07** `RELEASE-IN-EVENTS`: errors and traces carry the release (the commit SHA), so a
  regression points to a deploy. L2 · fix S · trial.
- [ ] **OB09** `AUDIT-TRAIL`: security-relevant actions (login, role change, export, deletion)
  written to an append-only log. L2≈ · fix J · trial.

### T-262 · An accessible front: names, alt text, focus, motion, ARIA
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Front, accessibility and i18n), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.38, "An accessible front, in every language": Labels, alt texts, focus, contrast and
motion checked in templates and by axe; the European Accessibility Act's profile; every locale
complete.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FA01** `ACCESSIBILITY` (draft): labels and accessible names checked in templates by
  eslint-plugin-vuejs-accessibility or jsx-a11y, run as mapped tools (F). L2 · fix J · adopt.
- [ ] **FA02** `AUTOMATED-ACCESSIBILITY` (draft): axe in Playwright tests (`@axe-core/playwright`)
  or pa11y-ci on the main pages. L1 · fix S · trial.
- [ ] **FA06** `IMG-ALT`: every image has `alt`, empty for decoration. L2 · fix J · adopt.
- [ ] **FA07** `CLICKABLE-ELEMENTS`: no click handler on a `div` or `span` without a role and a
  keyboard handler: a button or a link instead. L2 · fix J · adopt.
- [ ] **FA08** `FOCUS-VISIBLE`: no `outline: none` or `outline-0` without a `:focus-visible` style.
  L2 · fix J · adopt.
- [ ] **FA09** `REDUCED-MOTION`: animations respect `prefers-reduced-motion` (Tailwind's
  `motion-safe:`). L2 · fix S · trial.
- [ ] **FA10** `VIEWPORT-META`: `width=device-width`, never `user-scalable=no` or `maximum-scale=1`.
  L2 · fix S · adopt.
- [ ] **FA11** `NO-AUTOPLAY`: no media that plays sound by itself. L2 · fix S · adopt.
- [ ] **FA12** `SKIP-LINK`: a skip-to-content link in layouts. L2≈ · fix S · trial.
- [ ] **FA13** `ARIA-VALID`: ARIA roles and attributes valid and not redundant. L2 · fix J · adopt.

### T-263 · Accessible and translated: headings, contrast, the EU Accessibility Act, i18n keys
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Front, accessibility and i18n), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.38, "An accessible front, in every language": Labels, alt texts, focus, contrast and
motion checked in templates and by axe; the European Accessibility Act's profile; every locale
complete.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FA14** `HEADINGS-ORDER`: one `h1` per page, no skipped level. L3≈ · fix J · trial.
- [ ] **FA15** `FORM-AUTOCOMPLETE`: `autocomplete` on identity and address fields (WCAG 2.2, 1.3.5).
  L2 · fix S · trial.
- [ ] **FA16** `TOUCH-TARGETS`: targets of 24 by 24 CSS pixels at least (WCAG 2.2, 2.5.8), read from
  utility classes. L3≈ · fix J · assess.
- [ ] **FA17** `COLOR-CONTRAST`: the theme's text and background pairs computed from its tokens; axe
  for the rendered rest. L3≈ · fix J · trial.
- [ ] **FA18** `EU-ACCESSIBILITY-ACT`: for businesses selling to consumers in the EU, the European
  Accessibility Act applies since 28 June 2025: in that profile the accessibility rules move to
  `adopt`, and an accessibility statement exists. L0 · fix J · adopt (profile).
- [ ] **FA27** `I18N-KEYS-COMPLETE`: every locale has every key and no key is unused
  (vue-i18n-extract, `makemessages` compared). L3 · fix S · adopt.
- [ ] **FA28** `I18N-NO-BARE-TEXT`: user-facing text in templates goes through the i18n layer once
  one is configured (`@intlify/vue-i18n/no-raw-text`). L2 · ratchet · trial.
- [ ] **FA29** `LOCALE-FORMATTING`: dates, numbers and currencies through `Intl` or the framework's
  filters, never concatenated by hand. L2≈ · fix J · assess.
- [ ] **FA30** `RTL-READY`: logical CSS properties once a right-to-left locale is configured. L2 ·
  fix S · assess.

### T-264 · A fast front: Core Web Vitals, budgets, images, fonts, lazy loading
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Performance), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.39, "A fast, SSR-safe front": Hydration and SSR safety, keys and loading states
handled, bundle and image budgets, scripts and fonts that don't block, SEO basics.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PE02** `CORE-WEB-VITALS` (draft): Lighthouse CI with assertions (`lighthouserc`); field data
  from the Chrome UX Report's API with `--online`. L1 · fix S · trial.
- [ ] **PE03** `JS-BUDGET` (draft): size-limit or bundle budgets checked at build. L1 · fix S ·
  trial.
- [ ] **PE04** `MODERN-IMAGES` (draft): committed JPEG and PNG over about 200 KB listed with their
  savings; `@nuxt/image` or `<picture>` present; `width`, `height` and `loading="lazy"` set below
  the fold. L2 · fix S (conversion) · trial.
- [ ] **PE09** `NO-SYNC-SCRIPTS`: third-party scripts `async` or `defer`, or loaded through Nuxt
  Scripts. L2 · fix S · adopt.
- [ ] **PE10** `FONT-LOADING`: `font-display` set, fonts subset and preloaded (`@nuxt/fonts` does
  all three). L2 · fix S · trial.
- [ ] **PE11** `TREE-SHAKEN-IMPORTS`: no whole-library imports (`import _ from "lodash"`, `import *
  as icons`). L2 · fix S · adopt.
- [ ] **PE12** `HEAVY-DEPENDENCIES`: moment, full lodash or `core-js` for modern targets, listed
  with lighter options (with `NO-DEPRECATED-PACKAGES`). L1 · fix J · trial.
- [ ] **PE13** `LAZY-COMPONENTS`: heavy components and routes loaded on demand
  (`defineAsyncComponent`, Nuxt's `Lazy` prefix, `React.lazy`). L2≈ · fix J · assess.
- [ ] **PE15** `CACHEABLE-PUBLIC-PAGES`: anonymous pages cacheable (Nuxt's `routeRules` with `swr`
  or `isr`, `Cache-Control` on public views). L2≈ · fix J · trial.

### T-265 · A front that renders safely: UI states, SSR and hydration, SEO, error pages
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Front, accessibility and i18n), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.39, "A fast, SSR-safe front": Hydration and SSR safety, keys and loading states
handled, bundle and image budgets, scripts and fonts that don't block, SEO basics.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FA03** `UI-STATES` (draft): results of `useFetch` and `useAsyncData` whose `status` and
  `error` the template never reads. L2 · fix J · trial.
- [ ] **FA04** `UTILITY-CSS-FIRST` (draft): Tailwind or UnoCSS configured; `<style scoped>` blocks
  counted as a ratchet. L1 · ratchet · trial.
- [ ] **FA20** `VUE-NO-V-IF-WITH-V-FOR`. L2 · fix J · adopt.
- [ ] **FA21** `SSR-SAFE`: no `window`, `document` or `localStorage` at setup outside `onMounted`,
  `import.meta.client` or `<ClientOnly>`. L2 · fix J · adopt.
- [ ] **FA22** `HYDRATION-SAFE`: no `Math.random()`, `Date.now()` or locale formatting rendered on
  both sides without a stable value (`useState`, `useId`). L2≈ · fix J · trial.
- [ ] **FA23** `SEO-BASICS`: title, description, canonical URL, `robots.txt` and a sitemap on public
  sites (`useSeoMeta`, `@nuxtjs/sitemap`). L2 · fix S · trial.
- [ ] **FA24** `SOCIAL-CARDS`: Open Graph title and image on the pages people share. L2 · fix S ·
  assess.
- [ ] **FA25** `CSS-LINT`: Stylelint where CSS is written by hand. L1 · fix S · trial.
- [ ] **FA26** `ERROR-PAGES`: designed 404 and 500 pages (Nuxt's `error.vue`, Django's `404.html`
  and `500.html`). L0 · fix S · trial.
- [ ] **FA31** `WEB-MANIFEST`: icons and a web manifest for installable apps. L0 · fix S · assess.

### T-266 · Where it deploys: services and deploy configs read, compression, static files
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every forge, CI, host and
  machine, Performance), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.40, "Deploys you can undo": Services and hosts read from every deploy config; health
probes that exist, config that fails fast, OIDC instead of keys, rollbacks, certificates renewed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A15** Services read from compose, Kubernetes, Procfile, fly.toml, render.yaml, app.json,
  vercel.json, netlify.toml, wrangler.toml, serverless.yml: databases, caches, queues, search,
  object storage, with their versions.
- [ ] **A16** Where it deploys (a VPS by script, Fly, Render, Railway, Heroku, Vercel, Netlify,
  Cloudflare, Cloud Run, AWS, Azure, Kubernetes, GitHub Pages), which switches the operations rules
  on.
- [ ] **C11** Deploy configs read: Dockerfile, Containerfile, compose, Kubernetes manifests (any
  YAML with `apiVersion` and `kind`), Helm, Kustomize, Skaffold, Tilt, Nomad, systemd units,
  Caddyfile, nginx, Traefik, Fly, Render, Railway, Heroku, Vercel, Netlify, Cloudflare, Firebase,
  App Engine, Serverless, SAM.
- [ ] **PE07** `COMPRESSION`: responses compressed (Caddy's `encode zstd gzip`, nginx's `gzip on`,
  the platform's). L1 · fix S · adopt.
- [ ] **PE08** `STATIC-BY-PROXY`: static files hashed and served by the proxy, WhiteNoise or a CDN
  (`ManifestStaticFilesStorage`), never by the framework's dev server. L2 · fix S · adopt.

### T-267 · Deploys you can undo: health probes, config that fails fast, OIDC, graceful shutdown
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Operations), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.40, "Deploys you can undo": Services and hosts read from every deploy config; health
probes that exist, config that fails fast, OIDC instead of keys, rollbacks, certificates renewed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OP01** `HEALTH-PROBES` (scored): beyond a `HEALTHCHECK` line: the endpoint exists in the
  code, liveness and readiness told apart, compose and Kubernetes probes read.
- [ ] **OP04** `REVERSIBLE-DEPLOYMENT` (draft): images deployed by immutable tag or digest, a
  rollback script or workflow present. L1≈ · fix J · trial.
- [ ] **OP07** `ENV-EXAMPLE-COMPLETE`: every variable the code reads (`os.environ`, `env()`,
  `process.env`, `useRuntimeConfig`) is in `.env.example`, and none there is stale. L3 · fix S ·
  adopt.
- [ ] **OP08** `FAIL-FAST-CONFIG`: a missing required setting stops the start (no silent default for
  `SECRET_KEY` or `DATABASE_URL`): what `DJANGO-SECRET-KEY` and `DJANGO-ALLOWED-HOSTS` ask of
  Django, for every stack. L2 · fix J · adopt.
- [ ] **OP09** `DEPLOY-FROM-CI`: production deployed by a workflow from a commit, not from a laptop.
  L1 · fix J · trial.
- [ ] **OP11** `OIDC-TO-CLOUD`: cloud credentials through OIDC federation (`id-token: write`), no
  long-lived keys in secrets. L1 · fix J · adopt.
- [ ] **OP12** `ENCRYPTED-SECRETS`: secrets committed only encrypted (sops with age, git-crypt,
  Ansible Vault). L1 · fix J · trial.
- [ ] **OP14** `GRACEFUL-SHUTDOWN`: SIGTERM handled, a stop grace period longer than the longest
  request or task. L2 · fix S · trial.
- [ ] **OP15** `UTC-SERVERS`: containers and servers run in UTC, no `TZ` set to a local zone (with
  `TIME-ZONE`). L1 · fix S · trial.
- [ ] **OP20** `AUTOMATIC-TLS`: certificates renewed by themselves (Caddy, cert-manager, the
  platform's). L1 · fix S · adopt.

### T-268 · Production that holds: backups restored, runbooks, uptime, recovery targets
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Operations), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.41, "Production watched, backups restored": A runbook whose commands exist, backups
with a restore job, uptime and cron checks, alerts on symptoms, metrics kept private.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OP02** `ASYNC-HEALTH` (draft): workers and the scheduler report health (a Celery ping, a
  heartbeat file probed by compose). L2≈ · fix J · trial.
- [ ] **OP03** `TESTED-BACKUPS` (draft): a backup job in code (pg_dump, restic, borg) with a
  scheduled restore job beside it. L1≈ · fix J · trial.
- [ ] **OP05** `FEATURE-FLAGS` (draft): a flags library or module present where risky changes ship.
  L1≈ · fix J · assess.
- [ ] **OP06** `TESTED-SELF-HEALING` (draft): restart policies plus a script that exercises a known
  failure. L1≈ · fix J · assess.
- [ ] **OP13** `RUNBOOK`: deploy, rollback, restore and rotate written down (`docs/runbook.md`),
  with commands that exist. L1 · fix J · trial.
- [ ] **OP16** `UPTIME-CHECKS`: an outside check declared (Uptime Kuma, Gatus, a cron monitor) for
  production profiles. L1≈ · fix J · assess.
- [ ] **OP17** `CRON-MONITORED`: scheduled jobs ping a dead man's switch. L2≈ · fix J · assess.
- [ ] **OP18** `RECOVERY-TARGETS`: RPO and RTO stated in the runbook, the backup schedule matching
  them. L1≈ · fix J · assess.
- [ ] **OP19** `HOSTS-AS-CODE`: servers configured by code (Ansible, cloud-init, NixOS), not by
  hand. L0 · fix J · trial.
- [ ] **OP22** `STAGING-LIKE-PROD`: staging differs from production by values only. L1≈ · fix J ·
  assess.
- [ ] **OP23** `COST-GUARDS`: budgets and alerts declared with the cloud resources. L1 · fix J ·
  assess.
- [ ] **OP24** `DATA-RESIDENCY`: regions in the IaC and settings inside the EU for profiles that
  promise it. L1 · fix J · assess.

### T-269 · Production watched: SLOs, alerts on symptoms, private metrics, dashboards
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Observability), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.41, "Production watched, backups restored": A runbook whose commands exist, backups
with a restore job, uptime and cron checks, alerts on symptoms, metrics kept private.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OB03** `SLO` (draft): objectives as code (OpenSLO, Sloth, Pyrra). L1 · fix J · assess.
- [ ] **OB04** `ALERT-ON-SYMPTOMS` (draft): alert rules on error rates and latency rather than CPU,
  read from Prometheus rule files. L2≈ · fix J · assess.
- [ ] **OB05** `METRICS-PRIVATE`: a `/metrics` endpoint behind authentication or on an internal
  port. L2 · fix J · trial.
- [ ] **OB08** `DASHBOARDS-AS-CODE`: dashboards committed (Grafana JSON, Grafonnet, Perses). L0 ·
  fix J · assess.
- [ ] **OB10** `QUIET-HEALTH-LOGS`: health checks left out of access logs. L2 · fix S · assess.
- [ ] **OB11** `TRACE-SAMPLING`: a sampling ratio set from the environment. L2 · fix S · assess.
- [ ] **OB12** `LOG-RETENTION`: retention set in the log stack, with `RETENTION` (PD). L1 · fix S ·
  assess.

### T-270 · A tidy tree: the root, the layout, one config per tool, small folders
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Every forge, CI, host and
  machine, The detection engine, Structure), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.42, "A tree anyone can find their way in": No build output or artefact committed, a
complete `.gitignore`, one config per tool, paths every OS accepts, small folders.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B19** Every config file kiln recognizes validated against its JSON Schema from the
  SchemaStore catalogue: typos and deprecated keys found in hundreds of tools' files, for free.
- [ ] **C13** Rules that know operating systems: CRLF and `.gitattributes`, paths Windows refuses,
  case collisions that break macOS, a setup documented only as a `.sh` script.
- [ ] **E29** Artefacts that should never be committed, by name and content: `.pyc`,
  `node_modules/`, `dist/`, `.DS_Store`, `*.log`, `*.sqlite3`, `*.tfstate`, `id_rsa`, `*.pem`,
  `*.p12`, `*.keystore`, `.ipynb_checkpoints`, coverage reports, virtualenvs.
- [ ] **E30** `.gitignore` compared with github/gitignore's templates for the ecosystems present:
  what's missing is a scripted fix.
- [ ] **ST04** `ROOT-TIDY`: about 25 entries at most at the root; scripts in `scripts/`, docs in
  `docs/`. L0 · fix J · trial.
- [ ] **ST05** `SRC-LAYOUT`: a Python library's package under `src/`, as PyPA recommends. L0 · fix J
  · trial.
- [ ] **ST06** `ONE-CONFIG-PER-TOOL`: a tool configured in one place (ruff in `pyproject.toml` and
  in `ruff.toml` is two truths). L1 · fix S · adopt.
- [ ] **ST07** `CONFIG-IN-PYPROJECT`: Python tools' settings gathered in `pyproject.toml`
  (setup.cfg, tox.ini, .coveragerc, pytest.ini, mypy.ini merged in). L1 · fix S · trial.
- [ ] **ST08** `NO-NESTED-REPOS`: no `.git` inside the tree except declared submodules. L0 · fix J ·
  adopt.
- [ ] **ST09** `SHALLOW-TREE`: code no deeper than about six folders. L0 · ratchet · assess.
- [ ] **ST10** `SMALL-FOLDERS`: no code folder with more than about 50 files (assets, data,
  migrations aside). L0 · ratchet · assess.
- [ ] **ST11** `NO-GRAB-BAG-FILES`: no `utils.py`, `helpers.ts`, `misc.py` or `common.js` past about
  200 lines; the name says nothing of what's inside. L0 · fix J · trial.

### T-271 · A tree that checks out anywhere: marked files, no build output, line endings, paths
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Structure, Git and versions), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.42, "A tree anyone can find their way in": No build output or artefact committed, a
complete `.gitignore`, one config per tool, paths every OS accepts, small folders.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **ST14** `WORKSPACE-DECLARED`: more than two components of one ecosystem are declared in a
  workspace (uv, pnpm). L1 · fix S · trial.
- [ ] **ST15** `GENERATED-MARKED`: generated files marked (`linguist-generated` or a header) so
  tools and Claude skip them. L1 · fix S · adopt.
- [ ] **ST16** `VENDORED-MARKED`: vendored code marked `linguist-vendored`. L1 · fix S · adopt.
- [ ] **ST17** `NO-BUILD-OUTPUT`: no `dist/`, `build/`, `.nuxt/`, `.output/`, `.next/`, `target/` or
  `*.egg-info` committed. L0 · fix S (untracked and ignored) · adopt.
- [ ] **ST18** `GITIGNORE-COMPLETE`: `.gitignore` covers the ecosystems present (virtualenvs,
  `node_modules`, caches, `.env`, coverage). L1 · fix S · adopt.
- [ ] **ST19** `EDITORCONFIG`: an `.editorconfig` consistent with the formatters. L0 · fix S ·
  trial.
- [ ] **ST20** `LINE-ENDINGS`: `.gitattributes` with `* text=auto eol=lf`. L1 · fix S · trial.
- [ ] **ST21** `ONE-TEST-LAYOUT`: tests either beside the code or in a mirrored tree, one convention
  per component. L0≈ · fix J · assess.
- [ ] **GV14** `NO-CASE-COLLISIONS`: no two paths that differ only by case (they break checkouts on
  macOS and Windows). L0 · fix J · adopt.
- [ ] **GV15** `PORTABLE-PATHS`: no name Windows refuses (`CON`, `aux.py`, a trailing dot or space,
  `:*?"<>|`). L0 · fix J · adopt.

### T-272 · The map tells the truth: links, the repo map, entry points, decisions
- **Type**: improvement
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

### T-273 · Docs that tell the truth: README, commands, links, docstrings, context files
- **Type**: improvement
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
  map's paths existing, its commands running, nothing contradicting the settings. L3.

### T-274 · Set up in one command: pre-commit, editor files, a task runner, tool versions
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Operations,
  Developer experience), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.44, "Set up in one command": One bootstrap command, tasks named in one place, fast
commit hooks, tool versions pinned as in CI, editor settings shared.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C08** Pre-commit frameworks read (pre-commit, lefthook, Husky, lint-staged): checks before a
  commit, never counted as CI.
- [ ] **C16** Editor and environment files read: `.editorconfig`, `.vscode/` (recommended
  extensions, settings with personal paths), `.idea/` (workspace files committed), devcontainers,
  Gitpod, Codespaces, mise and asdf, direnv's `.envrc` (secrets in it), Nix dev shells, flox.
- [ ] **OP21** `ONE-COMMAND-LOCAL`: the whole stack runs locally with one command (`kiln dev`,
  compose, `Procfile.dev`). L0 · fix S · adopt.
- [ ] **DX01** `ONE-COMMAND-SETUP`: one documented bootstrap command (`make setup`, `just setup`,
  `uv sync` with `pnpm install`). L1 · fix S · adopt.
- [ ] **DX02** `TASK-RUNNER`: common tasks named in one place (Makefile, justfile, package scripts,
  poe), and the README cites them. L1 · fix S · trial.
- [ ] **DX03** `PRE-COMMIT-FAST`: commit hooks run in seconds (ruff at commit, type checks and tests
  elsewhere). L1≈ · fix J · trial.
- [ ] **DX04** `TOOL-VERSIONS-PINNED`: tool versions in `mise.toml` or `.tool-versions`, the same as
  in CI. L1 · fix S · trial.
- [ ] **DX05** `NO-GLOBAL-INSTALLS`: tools run from the project (`uvx`, `pnpm dlx`, versioned
  `npx`), never `sudo pip install` or `npm -g` in the docs. L2 · fix J · trial.
- [ ] **DX06** `EDITOR-SETTINGS-SHARED`: recommended extensions and format-on-save shared, personal
  settings ignored. L0 · fix S · assess.
- [ ] **DX08** `DEVCONTAINER` ⚠ T-48 (declined): a dev container for teams that want one, at `hold`
  while T-48 stands. L0 · hold.

### T-275 · Sensitive data found by itself, encrypted, isolated per tenant
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Application security),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.45, "Personal data, the GDPR way": Personal fields found in the models and kept out
of logs, URLs, fixtures and model calls; the inventory and the subprocessors written by script;
retention and deletion.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A17** Domain facts from code and dependencies: money (Decimal fields named price, Stripe),
  personal data (user models, e-mail fields), uploads, e-mail sending, payments, LLM calls (the
  anthropic and openai SDKs). They switch on MONEY, PERSONAL-DATA, AI-FEATURES and their kin without
  a question.
- [ ] **AS10** `ENCRYPTION` (draft): sensitive fields encrypted at rest. L2≈ · fix J · assess.
- [ ] **AS11** `ROW-LEVEL-SECURITY` (draft, Postgres): RLS policies in migrations for multi-tenant
  tables. L2≈ · fix J · assess.

### T-276 · Personal data the GDPR way
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Personal data, AI-assisted development), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.45, "Personal data, the GDPR way": Personal fields found in the models and kept out
of logs, URLs, fixtures and model calls; the inventory and the subprocessors written by script;
retention and deletion.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PD01** `PERSONAL-DATA` (draft): fields holding personal data (e-mail, phone, address, birth
  date, IBAN, IP) marked as the charter marks them; unmarked ones listed. L2 · fix J · trial.
- [ ] **PD02** `PII-INVENTORY`: an inventory of personal-data fields written from the models
  (`docs/personal-data.md`) and kept current by a script. L2 · fix S · trial.
- [ ] **PD03** `NO-REAL-PII-IN-FIXTURES`: fixtures and seeds hold fake data (real-looking e-mails on
  real domains, phone numbers flagged). L2 · fix J · adopt.
- [ ] **PD04** `NO-PII-IN-URLS`: no e-mail or name in query strings. L2≈ · fix J · trial.
- [ ] **PD05** `NO-PII-IN-LOGS`: personal fields passed to log calls (the charter's ban, promoted).
  L2 · fix J · adopt.
- [ ] **PD06** `RETENTION`: a job deletes or anonymizes data past its retention period. L2≈ · fix J
  · assess.
- [ ] **PD07** `DATA-EXPORT` and `ACCOUNT-DELETION`: users can get and delete their data (GDPR
  articles 15, 17 and 20), for profiles holding accounts in the EU. L2≈ · fix J · assess.
- [ ] **PD08** `CONSENT-BEFORE-TRACKING`: analytics and trackers load after consent, or are
  cookieless (Plausible, Matomo set so). L2 · fix J · trial.
- [ ] **PD09** `SELF-HOSTED-FONTS`: no fonts from Google's CDN (a German court awarded damages over
  it under the GDPR in 2022); `@nuxt/fonts` or local files. L2 · fix S · adopt (EU).
- [ ] **PD10** `SUBPROCESSORS-LISTED`: the third parties receiving data (Sentry, Stripe, a mail
  provider) listed from dependencies and settings, ready for the privacy policy. L1 · fix S ·
  assess.
- [ ] **PD11** `MINIMIZATION`: personal fields read nowhere flagged for removal. L3≈ · fix J ·
  assess.
- [ ] **AI17** `PII-TO-LLM`: personal fields sent to a model's API flagged (PD). L3≈ · fix J ·
  trial.

### T-277 · Money, payments and webhooks done right, accounts protected
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Application security, Business domain), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.46, "Money, time, accounts and mail": Amounts in the smallest unit with their
currency, dates in UTC, webhooks verified, cards never on the server, passkeys and rate limits, bulk
mail that can be unsubscribed from.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS26** `PASSKEYS`: WebAuthn offered for accounts (allauth's MFA, SimpleWebAuthn). L2≈ · fix
  J · assess.
- [ ] **AS27** `ADMIN-MFA`: the admin asks for a second factor. L2≈ · fix J · trial.
- [ ] **AS28** `RATE-LIMITS`: login, password reset and the API rate-limited, in the app or the
  proxy. L2≈ · fix J · trial.
- [ ] **BD01** `MONEY` (draft): `FloatField`, `float` or JS `number` arithmetic on names like price,
  amount, total, fee or balance; integers of the smallest unit stay the grid's way. L2≈ · fix J ·
  trial.
- [ ] **BD02** `TIME-ZONE` (draft): naive datetimes, `TIME_ZONE` set, calendar computations through
  `zoneinfo` (with `NAIVE-DATETIMES` and `USE-TZ`). L2 · fix J · trial.
- [ ] **BD03** `WEBHOOKS-VERIFIED`: incoming webhooks check their signature (Stripe's
  `construct_event`, GitHub's `X-Hub-Signature-256` compared in constant time). L2 · fix J · adopt.
- [ ] **BD04** `WEBHOOKS-DEDUPLICATED`: events stored by ID before they're handled. L2≈ · fix J ·
  trial.
- [ ] **BD05** `PAYMENTS-BY-PROVIDER`: card numbers never reach the server (Checkout or Elements),
  no `card_number` field anywhere; critical. L2 · fix J · adopt.
- [ ] **BD06** `CURRENCY-WITH-AMOUNT`: every amount carries its ISO 4217 currency. L2≈ · fix J ·
  assess.
- [ ] **BD07** `EXPLICIT-ROUNDING`: the rounding mode stated wherever amounts are divided (taxes,
  splits). L2≈ · fix J · trial.
- [ ] **BD08** `EMAILS-CASE-INSENSITIVE`: e-mail uniqueness ignores case (a `Lower()` unique
  constraint, `citext`). L2 · fix J · trial.

### T-278 · People's data as given: phones, names, dates, invoices, mail that arrives
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Business domain), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.46, "Money, time, accounts and mail": Amounts in the smallest unit with their
currency, dates in UTC, webhooks verified, cards never on the server, passkeys and rate limits, bulk
mail that can be unsubscribed from.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **BD09** `PHONES-E164`: phone numbers stored in E.164 (phonenumbers, libphonenumber). L2≈ ·
  fix J · assess.
- [ ] **BD10** `NAMES-AS-GIVEN`: no forced first and last name split, no ASCII-only or short-capped
  names. L2≈ · fix J · assess.
- [ ] **BD11** `DATES-NOT-DATETIMES`: birthdays and due dates stored as dates. L2≈ · fix J · assess.
- [ ] **BD12** `INVOICE-NUMBERING`: invoice numbers in one continuous chronological sequence where
  the law asks for it (France among others), taken inside a transaction. L2≈ · fix J · assess.
- [ ] **BD13** `TAX-RATES-AS-DATA`: VAT rates and thresholds held as dated data, not in code. L2≈ ·
  fix J · assess.
- [ ] **BD14** `ONE-CLICK-UNSUBSCRIBE`: bulk mail with `List-Unsubscribe` and one-click unsubscribe
  (RFC 8058, required by Gmail and Yahoo for bulk senders since 2024). L2≈ · fix J · trial.
- [ ] **BD15** `MAIL-AUTHENTICATED`: SPF, DKIM and DMARC for the sending domain, checked in DNS with
  `--online`. L6 · fix J · trial.

### T-279 · History: secrets ever committed, heavy blobs, hotspots
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Speed, History, forge and
  registries, The roadmap for Claude, Git and versions), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.47, "History: what every clone carries": Secrets once committed, heavy blobs, locks
drifting from their manifests, each blob read once and cached; hotspots open the roadmap.

The six drafts are questions about history: `--history` (M) gives them detectors.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A33** Git LFS patterns known: a binary tracked by LFS is fine, the same binary outside it is
  a finding.
- [ ] **J24** History scans incremental: each commit's blobs scanned once, ever (the cache knows
  them by SHA), so `--history` costs seconds after the first run.
- [ ] **M01** Secrets ever committed, scanned through history (each blob once, cached): a key
  removed but never rotated is still a key.
- [ ] **M02** Heavy blobs in history, which every clone carries forever: git-filter-repo or LFS
  suggested.
- [ ] **M08** Hotspots: churn times complexity per file (Adam Tornhill's method). The roadmap opens
  hotspots first, since that is where the next bug will be.
- [ ] **M12** A lock changed without its manifest, or the reverse, in history: drift caught at its
  source.
- [ ] **O05** Hotspots first among equals (M): the places that change most are fixed first.
- [ ] **GV10** `NO-SECRETS-IN-HISTORY`: secret patterns searched in every reachable blob, not only
  the tree; critical. The fix rotates first; history is rewritten only on the user's decision. L5 ·
  fix J · adopt.
- [ ] **GV11** `NO-LARGE-BLOBS`: no blob over about 5 MB in history outside LFS. L5 · fix J · adopt.
- [ ] **GV12** `LFS-FOR-BINARIES`: large binary assets tracked by LFS or stored elsewhere. L0 · fix
  J · trial.

### T-280 · History: commit habits, signatures, release rhythm, regression tests
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (History, forge and registries, Tests), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.48, "History: how the repo is worked": Commit sizes and messages, merges and branch
names, releases and their notes, fixes that come with a test, all read from history.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **M03** Commit habits over the last 90 days (Conventional Commits share, size distribution):
  SMALL-COMMITS and a commit-message rule promoted on facts.
- [ ] **M04** Signed commits and tags (GPG, SSH, gitsign), as a share.
- [ ] **M05** Direct commits on the integration branch (first-parent commits that aren't merges):
  NO-COMMIT-ON-INTEGRATION from history.
- [ ] **M06** Merge style (MERGE-COMMITS) and branch names (BRANCH-NAMES) from history.
- [ ] **M07** Release rhythm from tags: the last release's age, semver tags, a changelog entry per
  tag (RELEASE-NOTES).
- [ ] **M11** `fix:` commits that come with a test change (REGRESSION-TEST from history).
- [ ] **TE10** `REGRESSION-TEST` (draft): `fix:` commits of the last hundred that touch no test,
  with `--history`. L5 · ratchet · trial.

### T-281 · Git and versions rules from history: commits, branches, releases, tags
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Git and versions, Community), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.48, "History: how the repo is worked": Commit sizes and messages, merges and branch
names, releases and their notes, fixes that come with a test, all read from history.

The six drafts are questions about history: `--history` (M) gives them detectors.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **GV01** `SMALL-COMMITS` (draft): median size of the last hundred non-merge commits, and the
  share of subjects in the Conventional Commits form. L5 · ratchet · trial.
- [ ] **GV02** `BRANCH-NAMES` (draft): merged branches' names, from merge subjects or the forge,
  carry a type prefix. L5 · fix J · trial.
- [ ] **GV03** `MERGE-COMMITS` (draft): merges kept on the integration branch, visible in history,
  where the profile asks for them. L5 · fix J · assess.
- [ ] **GV04** `NO-COMMIT-ON-INTEGRATION` (draft): non-merge commits made straight on the
  integration branch, bots aside; branch protection with `--online`. L5 · ratchet · trial.
- [ ] **GV05** `RELEASE-NOTES` (draft): each release tag has its CHANGELOG entry or forge release,
  breaking changes first. L5 · fix J · trial.
- [ ] **GV06** `RELEASES-FROM-MAIN` (draft): release tags reachable from main, deploy workflows
  triggered by tags. L5 · fix J · trial.
- [ ] **GV07** `CHANGELOG`: a `CHANGELOG.md` in the Keep a Changelog shape, or generated
  (release-please, git-cliff). L0 · fix S · trial.
- [ ] **GV08** `SEMVER-TAGS`: release tags parse as versions and only go up. L5 · fix J · trial.
- [ ] **GV09** `SIGNED-TAGS`: release tags signed (SSH or GPG), verified with `--online`. L5 · fix J
  · assess.
- [ ] **GV16** `BLAME-IGNORE-REVS`: mass-reformatting commits listed in `.git-blame-ignore-revs`. L5
  · fix S · trial.
- [ ] **CM08** `MAINTAINED`: commits or releases in the last 90 days, or the README says the project
  is finished or archived (Scorecard's Maintained). L5 · fix J · trial.

### T-282 · The forge's settings read: tokens, secrets, alerts, environments, required checks
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (History, forge and registries, Application
  security, Tests, Operations, CI/CD), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.49, "The forge's settings, read": Through the `gh` already logged in: token
permissions, secrets' ages, environments, required checks, alerts left open, update pull requests
ignored.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **M18** GitHub: the default `GITHUB_TOKEN` read-only, "Actions can create pull requests" off,
  allowed actions limited, approval for first-time contributors' workflows, environments with
  reviewers for deploys.
- [ ] **M19** GitHub: secret names and ages (the API gives `updated_at`): unused secrets, secrets
  older than a year (SECRET-ROTATION becomes detectable), long-lived cloud keys where OIDC would do.
- [ ] **M20** GitHub: deploy keys read-only, webhooks with a secret and TLS checking, immutable
  releases, tag rulesets.
- [ ] **M23** Open alerts by age: critical Dependabot or code-scanning alerts open for more than 30
  days.
- [ ] **M24** Update pull requests left open (Dependabot, Renovate) for more than a few weeks: the
  bot is set but ignored, the real gap behind DEPENDENCY-UPDATES.
- [ ] **AS12** `SECRET-ROTATION` (draft): forge secrets older than a year (M). L6 · fix J · trial.
- [ ] **TE29** `TEST-DURATION`: suite time and slowest tests read from the CI's JUnit reports with
  `--online`, as a ratchet. L6 · ratchet · assess.
- [ ] **OP10** `PROTECTED-ENVIRONMENTS`: production jobs run in a forge environment with reviewers
  or branch rules (L6, T-158). L6 · fix J · trial.
- [ ] **CI06** `FAST-CI` (draft): median duration and runs that passed on retry read from the forge
  (L6); caches and concurrency as the static part. L6 · fix J · trial.
- [ ] **CI16** `NO-SELF-HOSTED-ON-PUBLIC`: no self-hosted runner reachable from a public repo's pull
  requests; critical. L1 + L6 · fix J · adopt.
- [ ] **CI21** `REQUIRED-CHECKS`: the integration branch requires the CI's checks (L6, T-158). L6 ·
  fix J · trial.

### T-283 · Repo hygiene on the forge: submodules, CODEOWNERS, force pushes, stale branches
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Git and versions), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.49, "The forge's settings, read": Through the `gh` already logged in: token
permissions, secrets' ages, environments, required checks, alerts left open, update pull requests
ignored.

The six drafts are questions about history: `--history` (M) gives them detectors.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **GV17** `SUBMODULES-SANE`: submodules over HTTPS, pinned to commits their remote still has.
  L1 + L6 · fix J · trial.
- [ ] **GV18** `CODEOWNERS-VALID`: paths that exist and owners that exist (L6), for team profiles.
  L1 · fix J · trial.
- [ ] **GV19** `NO-FORCE-PUSH-ON-MAIN`: force pushes and deletions blocked on the release and
  integration branches (L6, T-158). L6 · fix J · adopt.
- [ ] **GV20** `STALE-BRANCHES`: branches merged long ago and still on the remote (`/kiln:cleanup`,
  for the forge). L6 · fix S · assess.

### T-284 · What you depend on, checked at the registry: vulnerabilities, malware, licences
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Speed, History, forge
  and registries, Supply chain, Licensing), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.50, "What you depend on, checked at the registry": Real vulnerabilities in the
locked versions, malicious and abandoned packages, typosquats, the provenance of what is published,
dependencies' licences, a health card for a new one.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F09** osv-scanner, or OSV's batch API, for real vulnerability counts in the locked versions.
  VULNERABILITY-AUDIT checks today that an audit runs, not what it would find.
- [ ] **J19** `--online` calls in parallel, cached a day with ETags (endoflife.date, OSV, forge
  APIs), batched (OSV's `querybatch` takes hundreds of packages at once).
- [ ] **M26** Registries: trusted publishing and attestations on PyPI (PEP 740) and npm
  (provenance), checked on the published files.
- [ ] **M27** Registries: each dependency's health (last release, deprecated flag, yanked versions,
  archived source, a single maintainer) for ABANDONED-DEPENDENCIES.
- [ ] **M28** Registries: typosquat suspects (one edit from a popular name, few downloads) and known
  malicious packages (OSV's `MAL-` advisories).
- [ ] **SU03** `NEW-DEPENDENCY` (draft): a dependency added on a branch gets a health card in the
  pull request (maintainers, age, downloads, licence, install scripts). L6 · fix J · trial.
- [ ] **SU13** `MALICIOUS-PACKAGES`: no dependency known to be malicious (OSV's `MAL-`). L1 with
  data · fix J · adopt, critical.
- [ ] **SU14** `KNOWN-VULNERABILITIES`: no known critical or high vulnerability in the locked
  versions (OSV's batch query, or a cached database offline). L6 · fix S (bump within range) ·
  adopt.
- [ ] **SU15** `ABANDONED-DEPENDENCIES`: no dependency deprecated, yanked, archived, or three years
  without a release with open security issues. L6 · fix J · trial.
- [ ] **SU16** `TYPOSQUAT-SUSPECTS`: dependencies one edit from a popular name, with few downloads.
  L6 · fix J · trial.
- [ ] **SU37** `REPRODUCIBLE-LOCK`: the lock still resolves today (no yanked version, no dead URL),
  with `--online`. L6 · fix S · trial.
- [ ] **LI04** `DEPENDENCY-LICENSES`: licences of the locked dependencies compatible with the
  project's and its profile (no AGPL in a closed service without a decision), from the registries
  (L6) or a bundled cache. L6 · fix J · trial.

### T-285 · `--deep`: the repo's own checks in a sandbox
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Deep checks, opt-in
  and sandboxed, Trust, privacy and safety, Developer experience), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.51, "`--deep`: the repo's own checks, in a sandbox": Opt-in, in a throwaway copy
with the network off: the install from the lock, the tests (flaky, order, network, clock), Django's
deploy check, type checkers at their strictest, a clean clone.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F14** Type checkers as ratchet metrics in `--deep` (mypy, pyright, ty or pyrefly once
  mature, tsc, vue-tsc): the error count at strict settings.
- [ ] **N01** `--deep` runs in a throwaway copy, in a container when an engine is there, network off
  unless a step needs it, within a time budget; never in the user's tree.
- [ ] **N04** An install from the lock that works (`uv sync --locked`, `pnpm install
  --frozen-lockfile`): LOCK-IN-SYNC proven.
- [ ] **N05** Tests run: pass rate, duration, the slowest, the flaky (failures run again), order
  dependence (random order), network use (sockets blocked: NO-NETWORK proven), clock dependence (a
  shifted fake clock: CLOCK proven).
- [ ] **N06** Coverage measured (lines and branches) and mutation testing on a sample (mutmut,
  Stryker): the tests theme's ratchets fed with real numbers.
- [ ] **N07** Django's own `manage.py check --deploy` against the production settings: HSTS, SSL
  redirect, secure cookies, `DEBUG`, `SECRET_KEY`'s strength, `ALLOWED_HOSTS`, X-Frame-Options.
  Official checks, mapped onto grid rules.
- [ ] **N08** `manage.py makemigrations --check --dry-run`: models and migrations in sync.
- [ ] **N15** Type checkers and the repo's linters at their strictest: error counts as ratchets.
- [ ] **N16** The app's start-up time and memory, as ratchets.
- [ ] **N17** Deep results cached by commit and marked "measured at <commit>"; kiln-bot's weekly run
  uses `--deep` in CI, where running code is normal.
- [ ] **S08** Network calls listed before they start, as the fixers' `network` flag does, and only
  with `--online` or `--deep`.
- [ ] **DX07** `CLEAN-CLONE-WORKS`: a fresh clone installs and passes its checks with the documented
  commands (`--deep`, in a sandbox). L7 · fix J · trial.

### T-286 · `--deep`: the app built, served and probed
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Deep checks, opt-in and sandboxed, Performance),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.52, "`--deep`: the app built and probed": Images built and scanned, migrations
applied and reversed, the API fuzzed, the front rendered for axe and Lighthouse, the app served and
probed, a deployed URL on request.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **N02** Images built: size, final user, a shell or not, packages with known vulnerabilities
  (trivy or grype on the image), the health check passing.
- [ ] **N09** Migrations applied to a fresh Postgres container, then reversed; their SQL linted by
  squawk (through `sqlmigrate`).
- [ ] **N10** The OpenAPI schema generated and compared with the committed one (CONTRACT-DRIFT),
  then a short Schemathesis run (API-FUZZING).
- [ ] **N11** The front built: bundle sizes (JS-BUDGET), `nuxi typecheck`, pages rendered by
  Playwright for axe (ACCESSIBILITY) and for Lighthouse's lab metrics (CORE-WEB-VITALS).
- [ ] **N12** The app served locally and probed: security headers, cookie flags, CORS, error pages
  leaking a stack trace, `/admin` exposed, directory listings, server banners.
- [ ] **N13** A deployed URL scored too (`--url https://…`, opt-in): TLS, headers, `security.txt`,
  redirects; the production that the repo describes.
- [ ] **N14** N+1 queries caught while the tests run (nplusone, django-zeal), query counts per view.
- [ ] **N18** The backup script run against a throwaway database and restored (TESTED-BACKUPS
  proven) for repos whose scripts kiln knows.
- [ ] **N19** `kiln dev`'s own launch reused as a probe: if the stack starts with `kiln dev`, its
  servers are probed while they run, with no second setup.
- [ ] **PE18** `IMAGE-SIZE-BUDGET`: the final container image's size tracked; `--deep` builds it. L7
  · ratchet · assess.

### T-287 · What the grid doesn't know, shown: every file claimed
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every ecosystem, Precision
  and recall, A grid that stays current, Trust, privacy and safety, Measuring kiln score itself,
  What the grid doesn't know), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.53, "What the grid doesn't know, shown": Every tracked file claimed by a fact or
listed, fingerprints as data from Linguist and SchemaStore, the gap reports carrying them,
corrections counted as signals.

- [ ] **A26** Language by content when the extension lies: shebangs, `.h` (C, C++ or Objective-C),
  `.m` (Objective-C or MATLAB), `.pl`, `.v`, `.ts` (TypeScript or Qt translations), with Linguist's
  heuristics as data.
- [ ] **B25** A stack the grid doesn't cover yet is scored on the universal rules and told which
  pack would cover it, and how many corpus repos share it: a reason to write the pack.
- [ ] **H11** Waivers as signals beyond renewals (reported since v0.4.6): "false positive" in a
  reason, or one rule waived across many repos of a fleet, flags the rule for review.
- [ ] **Q07** A coverage map, themes by ecosystems with the number of scored rules in each cell,
  holes visible (`kiln grid --coverage`).
- [ ] **S05** No silent telemetry: T-38's report, with consent and the exact lines shown, as
  v0.4.6 does, and the opt-in counts of T-348 (antoine reversed "no telemetry, ever" on
  26 October 2026); every later signal (U) goes through one of the two.
- [ ] **T02** User effort measured: manual corrections needed per 100 corpus repos for a right score
  (target 0).
- [ ] **T03** The unclaimed-file rate on the corpus (target under 1 % outside docs and assets).
- [ ] **U01** Every tracked file claimed by a fact (code, a known tool's config, docs, asset, data);
  the rest listed as "kiln doesn't know these", with counts.
- [ ] **U02** A fingerprint library as data, seeded from GitHub Linguist (languages, vendored and
  generated patterns), the SchemaStore catalogue (config names to tools), github/gitignore,
  endoflife.date's products, Renovate's managers (⚠ AGPL: facts only, no code), Dependabot's and
  OSV's ecosystems, the pre-commit hooks index (appendix D).
- [ ] **U03** `NOTABLE_PACKAGES` (28 names in `score.py` today) grown into data: the top packages of
  each registry with what they are, so the gap report names what matters ("celery: background tasks,
  4 drafts, 0 scored") and still never a private name.
- [ ] **U04** Practices found but unclassified (a `scripts/backup.sh`, a `docs/runbook.md`, a
  `chaos/` folder), named so the grid can learn them.
- [ ] **U05** T-38's report (v0.4.6: stacks, notable packages, misfiring rules) also carries the
  kinds of unclaimed files (a config's name, never a path) and the corrections users made; the most
  reported become tickets first, counted by `/kiln:backlog`.

### T-288 · Never a crash, whatever the repo
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, The detection engine,
  Precision and recall, Trust, privacy and safety), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.54, "Never a crash, whatever the repo": Static by default, hardened parsers,
linear-time regexes, fuzzed trees, symlinks, untracked and ignored files handled; zero crashes on
the corpus at each candidate.

- [ ] **A27** Outside git, `.gitignore` parsed anyway: `build/`, `target/` and `.venv` stay out
  (only a fixed list is skipped today).
- [ ] **A28** Untracked files scored but marked "untracked": a local `.env` that isn't ignored is a
  real risk, a local experiment isn't the repo.
- [ ] **A32** Symlinks never followed out of the repo, loops cut, case-insensitive file systems
  (macOS, Windows) normalized.
- [ ] **E21** Linear-time regexes (google-re2, or Rust's `regex` through the syntax engine) and a
  time budget per rule: one bad pattern can't hang a run.
- [ ] **E32** Never read `.git/`, virtualenvs or `node_modules` as code, even when they're tracked
  by mistake (that's its own finding).
- [ ] **H06** Property tests (Hypothesis) on every parser (Dockerfile, workflows, compose,
  settings): random input never crashes, and the outcome is deterministic.
- [ ] **H07** A fuzzed tree: deep nesting, Unicode and spaces in paths, symlink loops, empty files,
  100 MB files, invalid UTF-8, CRLF, BOM, case collisions.
- [ ] **H15** A crash budget of zero on the whole corpus at every candidate; a rule that crashes is
  reported with a minimal anonymized tree for `/kiln:report`.
- [ ] **S01** Static by default: no code of the scored repo ever runs (no setup.py, no
  `eslint.config.js`, no `conftest.py`). Scoring an untrusted repo is safe, which the study needs at
  scale.
- [ ] **S02** Hardened parsers: YAML alias bombs, deep nesting, huge JSON, path traversal through
  symlinks, linear-time regexes; limits on file size, file count, time and memory.

### T-289 · Python beyond Django: every packaging tool, FastAPI and Flask
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Framework packs), made a ticket
  on 25 October 2026 at antoine's request

Planned in v0.6.55, "Python beyond Django": FastAPI, Flask, SQLAlchemy and every packaging tool
read; a new stack's rules count only once ten corpus repos of it were checked.

The `NOTABLE_PACKAGES` of `score.py` already name what the gap report sees; a pack turns one of them
into rules.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B02** Python beyond Django: Flask, FastAPI, Litestar, Starlette, aiohttp, Pyramid;
  SQLAlchemy and Alembic; Pydantic 1 to 2; Celery, RQ, Dramatiq, Huey, django-q2; each with a pack
  of rules (rule ideas, FP).
- [ ] **B03** Every Python packaging tool read: uv, Poetry, PDM, Hatch, pip-tools
  (`requirements.in`), Pipenv, Conda (environment.yml, conda-lock), Rye (`hold`, to uv), setup.py
  and setup.cfg (`hold`, to PEP 621), PEP 735 dependency groups, PEP 751 `pylock.toml`, PEP 723
  inline script metadata.
- [ ] **B24** A new ecosystem's rules count only after ten public repos of that stack in the corpus
  were scored and their findings checked: precision first.
- [ ] **FP01** FastAPI · `FASTAPI-RESPONSE-MODELS`: every route declares its response model. L2 ·
  fix J · adopt.
- [ ] **FP02** FastAPI · `FASTAPI-LIFESPAN`: `lifespan` rather than the deprecated `on_event`. L2 ·
  fix S · adopt.
- [ ] **FP03** FastAPI · `FASTAPI-AUTH-DEPENDENCIES`: protected routes through security
  dependencies, set on the router rather than route by route. L2 · fix J · trial.
- [ ] **FP04** FastAPI · `FASTAPI-DOCS-IN-PROD`: `/docs` and `/openapi.json` off or protected in
  production for private APIs. L2 · fix J · trial.
- [ ] **FP05** Flask · `FLASK-APP-FACTORY`: a `create_app` factory, the secret key from the
  environment, CSRF protection on forms (Flask-WTF). L2 · fix J · trial.
- [ ] **FP20** Pydantic · `PYDANTIC-V2`: Pydantic 2 rather than 1, which is no longer developed
  (`bump-pydantic` migrates). L1 · fix S · adopt.
- [ ] **AS23** (FastAPI's part) `CORS-STRICT`: `CORSMiddleware` never with `allow_origins=["*"]` and
  `allow_credentials=True` together. L2 · fix S · adopt.

### T-290 · JavaScript beyond Nuxt: every framework and package manager
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Application security), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.56, "JavaScript beyond Nuxt: the fronts": Every JS framework and package manager
read; Next.js, React, React Router, Angular, Vue without Nuxt, Svelte and Astro each with its pack,
Electron and Tauri locked down.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B04** JavaScript and TypeScript beyond Nuxt: Next.js, React Router 7, Astro, SvelteKit,
  SolidStart, Angular, Vite with React or Vue, Express, Fastify, NestJS, Hono, Koa, Electron, Tauri,
  React Native and Expo.
- [ ] **B05** Every JS package manager read: npm, Yarn classic and Berry (PnP, `.yarnrc.yml`), pnpm,
  Bun, Deno (deno.json, deno.lock, JSR), corepack's `packageManager`.
- [ ] **AS43** `ELECTRON-SAFE`: `contextIsolation` on, `nodeIntegration` off, `sandbox` on. L2 · fix
  S · adopt.
- [ ] **FP27** Tauri · `TAURI-CAPABILITIES`: the capabilities of Tauri 2 grant each window only the
  commands it uses, and a CSP is set. L1 · fix J · adopt.

### T-291 · Framework packs: Next.js, React, Angular, Svelte, Astro
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Framework packs), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.56, "JavaScript beyond Nuxt: the fronts": Every JS framework and package manager
read; Next.js, React, React Router, Angular, Vue without Nuxt, Svelte and Astro each with its pack,
Electron and Tauri locked down.

The `NOTABLE_PACKAGES` of `score.py` already name what the gap report sees; a pack turns one of them
into rules.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FP07** Next.js · `NEXT-SERVER-ONLY`: secrets and database access in `server-only` modules,
  never imported by a `"use client"` file. L2 · fix J · adopt.
- [ ] **FP08** Next.js · `NEXT-AUTH-IN-DATA-LAYER`: authorization checked where data is read, not
  only in middleware (CVE-2025-29927 let a header skip middleware). L2≈ · fix J · adopt.
- [ ] **FP09** React · `REACT-HOOKS-RULES`: eslint-plugin-react-hooks on (`rules-of-hooks`,
  `exhaustive-deps`). L1 · fix S · adopt.
- [ ] **FP10** React · `REACT-KEYS`: keys on list items (`jsx-key`). L2 · fix J · adopt.
- [ ] **FP11** Angular · `ANGULAR-STRICT`: `strict` and `strictTemplates` on. L1 · fix S · adopt.
- [ ] **FP12** Angular · `ANGULAR-NO-SANITIZER-BYPASS`: `bypassSecurityTrust*` counted, each with
  its reason. L2 · fix J · adopt.
- [ ] **FP13** Angular · `MODERN-ANGULAR`: standalone components, signals and the built-in control
  flow; Angular's own schematics migrate. L2 · fix S · trial.
- [ ] **FP14** Svelte · `SVELTE-RUNES`: Svelte 5 runes in new files (`npx sv migrate svelte-5` for
  the rest). L2 · fix S · trial.
- [ ] **FP15** SvelteKit · `SVELTEKIT-CSRF`: `csrf.checkOrigin` never turned off. L1 · fix S ·
  adopt.
- [ ] **FP21** Next.js · `NEXT-SERVER-ACTIONS-AUTH`: every Server Action checks authorization and
  validates its input, since each one is a public endpoint. L2≈ · fix J · adopt.
- [ ] **FP22** React Router · `ROUTER-LOADER-AUTH`: the loaders and actions of React Router 7
  (formerly Remix) check authorization themselves, like the data layer of Next.js. L2≈ · fix J ·
  trial.
- [ ] **FP23** Astro · `ASTRO-CHECK`: `astro check` in CI. L1 · fix S · adopt.
- [ ] **AS33** (Svelte's part) `AUTOESCAPE`: `{@html}` on variables, like `v-html`. L2 · fix J ·
  adopt.
- [ ] **AS36** (SvelteKit's and Astro's part) `NO-SECRETS-IN-FRONT`: their `PUBLIC_*` variables too.
  L2 · fix J · adopt.
- [ ] Vue's rules (`VUE-MULTI-WORD-COMPONENTS`, `API-CALLS`, `STATE-IN-STORES` and the rest) read a
  Vite + Vue repo as they read Nuxt, each with a passing and a failing example without Nuxt.

### T-336 · Node back ends: Express, Fastify, NestJS, Hono
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-291 by the framework coverage review of 26 October 2026, at antoine's
  request (the most used frameworks of the 2025 surveys checked against the plan): the Node back
  ends get their own release instead of a share of the fronts'

Planned in v0.6.57, "JavaScript beyond Nuxt: the Node back ends": Express, Fastify, NestJS and Hono,
the most used back ends after Django's peers, each with its own release's worth of rules rather than
a share of the fronts' (framework coverage review of 26 October 2026).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FP16** Express · `EXPRESS-5`: Express 5, whose router passes rejected promises to the error
  handler. L1 · fix J · trial.
- [ ] **FP17** NestJS · `NEST-VALIDATION-PIPE`: a global `ValidationPipe` with `whitelist` and
  `forbidNonWhitelisted`. L2 · fix S · adopt.
- [ ] **FP18** NestJS · `NEST-GUARD-BY-DEFAULT`: a global authentication guard, public routes marked
  one by one. L2 · fix J · trial.
- [ ] **FP24** Express · `EXPRESS-TRUST-PROXY`: `trust proxy` set to the proxies in front when the
  app runs behind one, so `req.ip` and rate limits see the real client. L2≈ · fix J · trial.
- [ ] **FP25** Fastify · `FASTIFY-SCHEMAS`: a schema on every route's body, query and response, in
  JSON Schema or through a type provider (TypeBox, Zod). L2 · fix J · adopt.
- [ ] **FP26** Hono · `HONO-VALIDATOR`: request input through a validator (`@hono/zod-validator`,
  `@hono/standard-validator`). L2 · fix J · trial.
- [ ] **AS48** (the Node ORMs' part) `NO-SQL-INJECTION`: `$queryRawUnsafe` and `$executeRawUnsafe`
  of Prisma, `raw` of Knex, `query` of TypeORM and `sql.raw` of Drizzle never built from a variable.
  L2 · fix J · adopt.

### T-292 · Data science repos: notebooks, data out of git, seeds, locked environments
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Data science), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.58, "Data science repos": The first outside issues came from data repos: notebooks
without outputs or secrets, data out of git, seeds and environments locked, models loaded safely.

The first data repos came through issues (#43, #44): v0.4.6 deploys a Streamlit or Dash front
(T-155) and adds `MODEL-TRACED` (T-156). This theme gathers what such repos need.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B18** Notebooks as code: `.ipynb` parsed (cells, outputs, execution order), Quarto and R
  Markdown read, Shiny apps recognised next to Streamlit and Dash.
- [ ] **DS02** `NOTEBOOK-OUTPUTS-CLEAN`: notebooks committed without outputs or execution counts
  (nbstripout, or Jupytext pairs). L1 · fix S · adopt.
- [ ] **DS03** `NOTEBOOKS-PAIRED`: notebooks paired with a `.py` file (Jupytext's percent format) so
  diffs and reviews work. L1 · fix S · trial.
- [ ] **DS04** `NOTEBOOK-SECRETS`: no token in a cell or an output; `SECRETS` reads a `.ipynb` as
  cells, not as one JSON string. L2 · fix J · adopt.
- [ ] **DS05** `NO-ABSOLUTE-PATHS`: no `/home/…`, `C:\Users\…` or `/content/drive` path in code or
  notebooks. L2 · fix J · adopt.
- [ ] **DS06** `DATA-OUT-OF-GIT`: datasets over a few MB kept out of git (DVC, LFS, a bucket),
  described by a pointer. L0 · fix J · adopt.
- [ ] **DS07** `SEEDS-SET`: random seeds fixed where results are reported
  (`numpy.random.default_rng(seed)`, `torch.manual_seed`). L2≈ · fix J · trial.
- [ ] **DS08** `ENVIRONMENT-LOCKED`: the analysis environment locked (uv, conda-lock, pixi, renv).
  L1 · fix S · adopt.

### T-293 · Data science repos: pipelines, model loading, experiments, Streamlit
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Data science, Framework packs), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.58, "Data science repos": The first outside issues came from data repos: notebooks
without outputs or secrets, data out of git, seeds and environments locked, models loaded safely.

The first data repos came through issues (#43, #44): v0.4.6 deploys a Streamlit or Dash front
(T-155) and adds `MODEL-TRACED` (T-156). This theme gathers what such repos need.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **DS09** `PIPELINE-DECLARED`: steps declared (DVC stages, Snakemake, a Makefile), not
  notebooks run by hand in order. L0 · fix J · trial.
- [ ] **DS10** `STREAMLIT-SECRETS-IGNORED`: `.streamlit/secrets.toml` ignored and untracked;
  critical when tracked. L0 · fix S · adopt.
- [ ] **DS11** `NOTEBOOKS-RUN-IN-CI`: notebooks that are part of the deliverable executed in CI
  (nbmake, papermill). L1 · fix S · trial.
- [ ] **DS12** `SAFE-MODEL-LOADING`: no `pickle.load` or `torch.load(..., weights_only=False)` on
  downloaded files, nor `trust_remote_code=True` (Hugging Face) without a pinned revision;
  safetensors or ONNX for models from outside. L2 · fix S · adopt.
- [ ] **DS13** `EXPERIMENTS-TRACKED`: runs logged with their commit (MLflow, a results file). L1≈ ·
  fix J · assess.
- [ ] **DS14** `DATA-SCHEMA`: input tables validated by a schema (pandera, Great Expectations,
  Pydantic). L2≈ · fix J · assess.
- [ ] **FP19** Streamlit and Dash · the DS theme's rules plus `STREAMLIT-SECRETS-IGNORED`, and the
  deploy of v0.4.6 checked (a health route, a non-root image). L1 · fix S · trial.
- [ ] **FP38** Gradio · `GRADIO-SHARE-OFF`: no `launch(share=True)` in committed code, which opens
  the app to the whole Internet through a public link. L2 · fix S · adopt.

### T-294 · Licences right: files, manifests, notices, assets, community health
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, History, forge and
  registries, Licensing), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.59, "Open source done right": A licence that says the same everywhere, notices kept,
contributing, conduct and security policies, issue forms, sponsors, the OpenSSF badge.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F17** The REUSE tool and a licence detector in licensee's manner for the licensing theme.
- [ ] **M25** Community health from the forge (README, licence, conduct, contributing, templates)
  and maintainers' responsiveness (median first response), for open-source profiles.
- [ ] **LI02** `LICENSE-DECLARED`: the manifest's licence as an SPDX expression (`license = "MIT"`
  with PEP 639, package.json's `license`). L1 · fix S · adopt.
- [ ] **LI03** `LICENSE-CONSISTENT`: the file, the manifests and the README say the same licence. L1
  · fix J · adopt.
- [ ] **LI05** `THIRD-PARTY-NOTICES`: vendored code keeps its licence and notice. L1 · fix J ·
  adopt.
- [ ] **LI06** `ASSETS-LICENSED`: fonts, images and icons committed with their licence or source (a
  font's OFL file). L0≈ · fix J · trial.
- [ ] **LI07** `SPDX-HEADERS`: REUSE-compliant headers or a `REUSE.toml`, for projects that want
  them. L1 · fix S · assess.
- [ ] **LI08** `SIGN-OFF`: contributions under a DCO sign-off or a CLA, for profiles that need one.
  L5 · fix J · assess.

### T-295 · Open source done right: contributing, conduct, security policy, issue forms
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Community), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.59, "Open source done right": A licence that says the same everywhere, notices kept,
contributing, conduct and security policies, issue forms, sponsors, the OpenSSF badge.

For the open-source profile; kiln's own vitrine (CONTRIBUTING, Code of Conduct, SECURITY, templates,
FUNDING with T-119) is the reference example.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CM01** `CONTRIBUTING`: setup, tests and the pull-request flow written down. L0 · fix S ·
  adopt (open source).
- [ ] **CM02** `CODE-OF-CONDUCT`: the Contributor Covenant or an equivalent, with a contact. L0 ·
  fix S · adopt (open source).
- [ ] **CM03** `SECURITY-POLICY`: `SECURITY.md` with a private reporting channel; private
  vulnerability reporting on (L6). L0 · fix S · adopt.
- [ ] **CM04** `ISSUE-FORMS`: issue forms for bugs and requests, a pull-request template. L0 · fix S
  · trial.
- [ ] **CM05** `FUNDING`: `FUNDING.yml` when the maintainers accept sponsors. L0 · fix S · assess.
- [ ] **CM06** `GOOD-FIRST-ISSUES`: a few labelled issues open (L6, `/kiln:good-first-issues`). L6 ·
  fix J · assess.
- [ ] **CM07** `RESPONSE-TIME`: median time to a first answer on issues and pull requests (L6). L6 ·
  ratchet · assess.
- [ ] **CM10** `OPENSSF-BADGE`: the OpenSSF Best Practices badge, read with `--online`. L6 · fix J ·
  assess.

### T-296 · Packages published cleanly: trusted publishing, attestations, contents
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Packaging and publishing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.60, "Libraries and CLIs that publish cleanly": Trusted publishing with attestations,
complete metadata, one version source, typed exports, packages that hold what they should and
nothing else.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PK01** `TRUSTED-PUBLISHING`: PyPI and npm publish through OIDC trusted publishing, no
  long-lived token. L1 · fix S · adopt.
- [ ] **PK02** `ATTESTATIONS`: PyPI attestations (PEP 740) and npm provenance on published packages.
  L1 · fix S · trial.
- [ ] **PK03** `RELEASE-WORKFLOW`: publishing only from CI, on a tag, in a protected environment. L1
  · fix S · adopt.
- [ ] **PK04** `NPM-FILES-ALLOWLIST`: `files` in package.json so nothing private ships (`npm pack
  --dry-run` with `--deep`). L1 · fix S · adopt.
- [ ] **PK05** `PYPROJECT-METADATA`: `[project]` with name, version source, `requires-python`,
  licence expression, readme and URLs. L1 · fix S · adopt.
- [ ] **PK06** `NO-SETUP-PY`: a PEP 517 backend declared in `pyproject.toml`; `setup.py` kept only
  for C extensions. L1 · fix J · trial.
- [ ] **PK07** `PACKAGE-CONTENTS`: the sdist holds the tests and the licence, the wheel holds
  neither tests nor secrets (`--deep` builds both). L7 · fix J · trial.

### T-297 · Packages that behave: typed exports, engines, one version source, CLIs
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Packaging and publishing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.60, "Libraries and CLIs that publish cleanly": Trusted publishing with attestations,
complete metadata, one version source, typed exports, packages that hold what they should and
nothing else.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PK08** `TYPED-EXPORTS`: package.json `exports` with `types` conditions; publint and
  arethetypeswrong clean. L4 · fix J · trial.
- [ ] **PK09** `ENGINES-DECLARED`: `engines.node` and `requires-python` set and matching the CI
  matrix. L1 · fix S · adopt.
- [ ] **PK10** `VERSION-SINGLE-SOURCE`: the version in one place, the manifest or the tag
  (hatch-vcs, setuptools-scm). L1 · fix J · trial.
- [ ] **PK11** `CLI-ENTRY-POINTS`: command-line tools declared in `[project.scripts]` or `bin`, with
  `--version` and `--help` that work (L7). L1 · fix S · trial.
- [ ] **PK12** `DEPRECATION-POLICY`: a deprecation warns for at least one release before the removal
  (`DeprecationWarning`), and the docs say so. L2≈ · fix J · assess.
- [ ] **PK13** `REPRODUCIBLE-BUILD`: `SOURCE_DATE_EPOCH` honoured; two builds give the same hash
  (`--deep`). L7 · fix J · assess.

### T-298 · Infrastructure as code: Terraform locked, scanned, private, encrypted
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Mature tools as detectors,
  Infrastructure as code), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.61, "Infrastructure as code": Terraform and OpenTofu, Kubernetes and Helm, Ansible:
state out of git, versions pinned, buckets private, pods restricted.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B17** Infrastructure as code: Terraform and OpenTofu, Pulumi, CDK, CloudFormation, Bicep,
  Ansible, Helm, Kustomize, Nix (rule ideas, IN).
- [ ] **F11** trivy's config mode or checkov for Terraform, Kubernetes, Helm and Dockerfiles, mapped
  onto the containers and infrastructure rules.
- [ ] **F12** kube-linter or kubeconform for Kubernetes manifests.
- [ ] **IN01** `TF-LOCK`: `.terraform.lock.hcl` committed. L0 · fix S · adopt.
- [ ] **IN03** `TF-VERSIONS-PINNED`: `required_version` and provider constraints set; registry
  modules pinned to versions, git modules to commits. L1 · fix S · adopt.
- [ ] **IN04** `TF-CHECKED`: `fmt -check`, `validate` and tflint in CI (Terraform or OpenTofu). L1 ·
  fix S · trial.
- [ ] **IN05** `IAC-SCANNED`: checkov, Trivy's config scan or KICS in CI. L1 · fix S · trial.
- [ ] **IN06** `NO-PUBLIC-BUCKETS`: storage buckets private unless declared public with a reason;
  public access blocked by default. L1 · fix J · adopt.
- [ ] **IN07** `ENCRYPTED-AT-REST`: databases, volumes and buckets encrypted in the IaC. L1 · fix S
  · trial.
- [ ] **IN08** `K8S-SECURITY-CONTEXT`: `runAsNonRoot`, `readOnlyRootFilesystem`,
  `allowPrivilegeEscalation: false`, capabilities dropped (the restricted Pod Security Standard). L1
  · fix S · adopt.
- [ ] **IN09** `K8S-RESOURCES`: memory requests and limits, CPU requests. L1 · fix S · adopt.

### T-299 · Kubernetes, Helm and Ansible by the book
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Infrastructure as code), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.61, "Infrastructure as code": Terraform and OpenTofu, Kubernetes and Helm, Ansible:
state out of git, versions pinned, buckets private, pods restricted.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **IN10** `K8S-PROBES`: readiness and liveness probes on different endpoints. L1 · fix S ·
  adopt.
- [ ] **IN11** `K8S-NO-LATEST`: no `:latest` or untagged image (`IMAGES-BY-DIGEST` reads manifests
  too). L1 · fix S · adopt.
- [ ] **IN12** `K8S-NETWORK-POLICIES`: a default-deny NetworkPolicy per namespace. L1 · fix J ·
  trial.
- [ ] **IN13** `K8S-SECRETS-EXTERNAL`: no Secret manifest holding real data; External Secrets,
  Sealed Secrets or sops instead. L1 · fix J · adopt.
- [ ] **IN14** `K8S-SUPPORTED-APIS`: no API version Kubernetes has removed (`extensions/v1beta1`,
  `policy/v1beta1`), from pluto's data. L1 · fix S · adopt.
- [ ] **IN15** `HELM-CHARTS`: `values.schema.json` present, `Chart.lock` committed. L0 · fix J ·
  trial.
- [ ] **IN16** `ANSIBLE-LINT`: ansible-lint clean, secrets in Vault rather than plain variables. L4
  · fix J · trial.
- [ ] **IN17** `IAC-TAGS`: resources tagged with an owner and a cost centre, for company profiles.
  L1 · fix S · assess.

### T-300 · Every kind of repo, each with its rules
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every kind of repo, every
  profile, Nothing to do, Application security), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.62, "Every kind of repo": A library, an awesome list, a template, a fork or an
archive each held to what it needs; the kind and what kiln assumed on the report's first lines, with
their evidence.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A39** Forks recognized (an `upstream` remote, or the forge says so): the fork's own changes
  scored apart from upstream's code.
- [ ] **A40** Archived repos (the forge's flag, an "archived" notice in the README) scored only on
  what still matters: secrets, licence.
- [ ] **D01** Kinds recognized: web app (backend, frontend, full stack), API, library (PyPI, npm,
  crates.io, Maven Central…), CLI, desktop, mobile, browser extension, editor extension, GitHub
  Action, Claude Code plugin or MCP server, data science, ML training, data pipeline (dbt, Airflow,
  Dagster), infrastructure, docs site, static site, dotfiles, template, coursework, research
  artefact, game, firmware, hardware, HPC, WordPress, Shopify theme, serverless functions, bot,
  smart contracts, awesome list, single script.
- [ ] **D02** Each kind its rules: a library needs semver, a changelog, typed exports and trusted
  publishing, not health probes; an awesome list needs link checks, not tests (today TESTS-PRESENT
  fails every awesome list).
- [ ] **D03** A repo can be several kinds (a library with a docs site and a CLI): kinds per
  component.
- [ ] **D07** Thresholds that scale: a 200-line script isn't held to a monorepo's architecture
  rules; ratchets on a big repo start from its own numbers.
- [ ] **D11** Kind and profile on the report's first lines with their evidence; `kiln set
  kind=library` exists, is never needed, and each use is a T-38 signal.
- [ ] **D12** The forge's topics and description read with `--online` as hints (`homework`,
  `tutorial`, `template`, `awesome`).
- [ ] **D13** Template repos (`is_template`, `copier.yml`) scored on what they generate: rendered
  with defaults in a sandbox, the result scored. A template's score is its children's.
- [ ] **D14** Tutorials and example repos recognized, so the study and the fleet don't count them
  (T-132's exclusions as code).
- [ ] **K14** The integration branch, the main language and the profile detected; the report says
  what it assumed.
- [ ] **AS44** `EXTENSION-PERMISSIONS`: browser extensions ask for the fewest permissions and hosts.
  L1 · fix J · trial.
- [ ] **D17** Static and docs sites read: Hugo (modules at a version), Jekyll (`Gemfile.lock`),
  MkDocs, Docusaurus, Eleventy, Gatsby, Sphinx; the site built in CI, its links checked, its theme
  pinned rather than copied.
- [ ] **FP43** Solidity · `SOLIDITY-CHECKED`: Foundry or Hardhat tests and Slither in CI, the
  compiler version pinned exactly (`pragma solidity 0.8.28;`, not `^`). L1 · fix S · trial.

### T-301 · GitLab too: its CI, its forge, its reports
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Outputs and
  integrations, History, forge and registries, CI/CD), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.6.63, "GitLab too": Universities and companies often run GitLab: its CI read like
GitHub's, its settings through `glab`, its merge request widget fed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C02** GitLab CI: `.gitlab-ci.yml`, `include:` (project, remote, template, component with a
  version), `rules:`, `needs:`, the job token's scope, protected and masked variables.
- [ ] **C09** Forges: GitHub, GitLab (cloud and self-managed), Bitbucket, Azure DevOps, Gitea,
  Forgejo, Codeberg, SourceHut, Gerrit; read from the remote's URL, their folders (`.github/`,
  `.gitlab/`, `.gitea/`, `.forgejo/`, `.azuredevops/`) and conventions (where CODEOWNERS and
  templates live) known.
- [ ] **C21** Self-hosted forges on custom domains recognized by their API's signature (GitLab's
  `/api/v4/version`, Gitea's `/api/v1/version`), with `--online` only.
- [ ] **L03** GitLab: the Code Quality report (merge request widget) and the SAST report format for
  security rules.
- [ ] **M21** GitLab: protected branches and tags, merge request approvals, push rules, secret
  detection, protected and masked variables, the job token's scope.
- [ ] **CI26** `GITLAB-PIPELINE-HYGIENE`: `interruptible`, `timeout`, `rules:` rather than `only`
  and `except`, includes pinned to a commit, protected variables. L1 · fix S · adopt (GitLab).

### T-302 · Profiles read from the repo: stages, criticality, team signals
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every kind of repo, every profile, Rule format v2
  and authoring), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.64, "Profiles read from the repo, never asked": Solo, association, company or
university, inferred from signals; criticality raises the bar by itself; moving up applies the new
rules as ratchets.

- [ ] **D05** Stages: prototype, growing, production, maintenance, archived. Rules grow with the
  repo ("the smallest level at creation, and rules that grow with the repo", antoine, 16 October
  2026).
- [ ] **D06** Criticality raises the bar by itself: payments, health or children's data, accounts of
  other people make the stricter profile's rules apply, and the report says why.
- [ ] **D08** Team signals: CODEOWNERS and required reviews only past two regular contributors; the
  bus factor (one person wrote 90 % of the last year) shown to organisation profiles.
- [ ] **G11** Profiles stay a membership list, never weights (decision 2): a rule outside the repo's
  profile is not applicable, so `SLO` asks nothing of a solo repo.

### T-303 · Coursework and research repos
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every kind of repo, every profile, Docs, teaching
  and reach, Community), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.65, "Coursework and research": A course's repos scored on what a student can act on,
a teacher's guide, research artefacts that can be reproduced and cited.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **D09** Coursework: a course's repos (many, small, short-lived, one template) scored on what a
  student can act on; a teacher scores the class (fleet, CSV). The v0.7.0 university target.
- [ ] **D10** Research artefacts: CITATION.cff, a pinned environment, data availability, a DOI, "how
  to reproduce the figures"; the artefact badges of ACM and the big conferences as rules.
- [ ] **V05** A teacher's guide: a class's repos scored each week, a rubric per theme.
- [ ] **CM09** `CITATION`: `CITATION.cff` for research software (the university profile). L0 · fix S
  · trial.

## ⚪ Background — long-running work, debt and ideas

### T-353 · A leaderboard of the best-scored public repos
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q99: "I find it cool, to see whether big repos
  already do this or if it's frowned upon"), decision 38

Public rankings by a quality score exist and are welcome when they celebrate (best-of-python
ranks projects by a project-quality score; Scorecard publishes every repo's checks); shaming the
worst is what is frowned upon.
- [ ] A page of the best-scored public repos by stack, from the corpus and the badges (T-154),
  top only, a repo removed on its maintainers' request; built after T-191.

### T-178 · A lighter install: copier's dependencies trimmed, not fetched later
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine, 24 October 2026: should kiln download its packages bit by bit to stay light?

Measured that day: the installed tool weighs 26 MB, kiln itself 1.4 MB; the rest comes from
copier (pygments 5 MB, pydantic-core 5 MB, wcwidth 3.5 MB, yaml 2.8 MB, prompt_toolkit…).
`kiln --version` answers in 0.2 s, copier is imported only by the commands that need it, and
the heavy pieces (Playwright's Chromium, serena, context7, each stack's toolchain) are already
fetched on first use. Lazy-downloading copier was ruled out: a `kiln new` or `kiln update` that
fails offline, versions no longer pinned by one `uv tool install`, a slower first command.
- [ ] See which of copier's dependencies kiln's paths actually load (`-X importtime` on
  `kiln new`, `kiln update`), and whether any can be dropped or made optional upstream.
- [ ] Only worth doing if the gain is real (several MB or a visible install time); otherwise
  close it as measured.

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
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: interface redesign, 15 October 2026

- [ ] `kiln check`: the step title and the `✓` line say the same thing (one command per step).

### T-99 · `kiln doctor --fix`: the fixes applied, not just printed
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026

- [ ] Each problem `kiln doctor` finds and can fix safely (pre-commit missing, plugin not
  installed, outdated kiln) is fixed after one confirmation; the others keep their command and
  direct link.
### T-138 · Less code to carry, measured first: the compressor's dry run
- **Type**: idea
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026, fourth pillar ("slim down", a lead): writing code
  costs almost nothing now, its mass is the problem

- [ ] `kiln score` gains the slimming pillar: unused dependencies (deptry, knip), dead code
  (vulture), measured on the reference repo and on the study's repos.
- [ ] The upkeep ahead, next to it: how many dependency releases the repo will absorb in a year,
  how many breaking, which ends of life are coming (libyear measures the lag behind; this
  measures what is coming), and how much removing the unused dependencies lowers it.
- [ ] The number decides the rest: "−22 % of lines, −9 dependencies, same behaviour" is worth
  building; a few percent is not.

From the kiln score ideas of 24 October 2026:
- [ ] **M10** Code untouched for years and imported by nothing: candidates for the compressor
  (T-138).

### T-139 · The compressor: removals proven by types, tests and behaviour
- **Type**: idea
- **Status**: in progress — started before T-138's number, at antoine's request (21 October
  2026); the compressor's own dry run gives that number. Merged into develop on 22 October
  2026: `kiln fix --rule DEAD-CODE` and `--rule UNUSED-DEPENDENCIES`, proven by the type
  checker and the tests; the behaviour comparison and the dependency replacement remain
- **Opened**: 2026-10-17
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
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
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026: the community modules
  of v1.0.0 are grid packs

An ecosystem is what turns a tool into a project people star and contribute to.
- [ ] `kiln grid add github:someone/kiln-grid-fastapi`: rules for a stack or a domain kiln does
  not cover, in the format of T-123, scored like kiln's own, with a trust prompt that shows what
  their detectors and fixers run.
- [ ] An index of reviewed packs in kiln; an author kit (template, contract tests, a workflow
  that tests the pack against each kiln release).

From the kiln score ideas of 24 October 2026:
- [ ] **B23** Ecosystem packs written as data and proven by examples, so the community (T-69) adds
  one without touching kiln's code.
- [ ] **R02** Packs from any git repo (T-69), pinned by SHA, behind a trust prompt that shows what
  their detectors run; declarative detectors only unless trusted (a Python check is code execution).

### T-304 · A whole organisation's repos: CSV, local scores, organisation packs
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Outputs and integrations, One measure drives
  every command, Packs, local rules, standards), made a ticket on 25 October 2026 at antoine's
  request

Planned in v0.7.0, "A whole organisation's repos": Milestone decided by antoine (16 October 2026:
kiln for teams and organisations), re-scoped to the vision's targets: a university, an association
network, a 50-person company; large companies come later. Every repo scored remotely without
cloning, gaps ranked by how many repos share them.

- [ ] **L16** CSV across many repos (`kiln status --csv`): a teacher grading a class, an association
  checking its repos.
- [ ] **P13** `kiln status` shows each local repo's score and the grid version it was scored with.
- [ ] **R03** Organisation packs for the v0.7.0 targets: a university's rules for student repos, an
  association network's.

### T-305 · Compliance views: Scorecard, ASVS, SLSA, the CRA and the EAA
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Rule format v2 and
  authoring, A grid that stays current, Packs, local rules, standards), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.7.1, "Compliance views": What a company has to show: Scorecard, ASVS, SLSA, CIS, WCAG,
the Cyber Resilience Act and the Accessibility Act, each control covered or honestly listed as not
checkable.

- [ ] **F19** OpenSSF Scorecard's checks redone locally where possible (they need its API
  otherwise): "kiln score covers Scorecard" is a claim worth making (appendix C).
- [ ] **F20** Semgrep-compatible rules ⚠ licences first: the Semgrep registry's rules have their own
  licence, the opengrep engine is LGPL. kiln's own rules stay in ast-grep.
- [ ] **G10** A `standards` table: CWE, OWASP Top 10 and ASVS, OpenSSF Scorecard, SLSA, NIST SSDF,
  CIS benchmarks, WCAG, the EU Cyber Resilience Act, twelve-factor.
- [ ] **Q08** Standards coverage: the share of Scorecard, ASVS level 1, CIS Docker, SLSA build level
  2 and WCAG AA controls that a grid rule covers.
- [ ] **R06** Compliance views (`kiln score --standard scorecard | asvs-l1 | slsa | cis-docker |
  owasp-top10 | wcag-aa | cra | gdpr`): what passes, what fails, and what can't be checked
  statically, honestly listed.
- [ ] **R07** EU Cyber Resilience Act readiness for companies selling software in Europe (reporting
  duties from September 2026, the rest from December 2027): SBOM, a vulnerability policy, security
  updates, a contact.
- [ ] **R08** European Accessibility Act (applied since June 2025): the front-accessibility rules as
  a company's evidence.
- [ ] **R09** The OpenSSF Best Practices badge's questionnaire pre-filled from the findings.
- [ ] **R10** Each security rule traced to its OWASP cheat sheet, so a reviewer can follow every
  rule to its source.

### T-306 · Delivery measured, the organisation's settings read
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, History, forge and registries),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.7.2, "Delivery measured, the organisation's settings read": DORA's four keys from the
forge, the bus factor and knowledge islands, two-factor authentication and base permissions, for
organisation profiles.

- [ ] **I15** A delivery score apart, for organisation profiles with `--online`: DORA's four keys
  from the forge (deploy frequency from releases, lead time from merge times, change failure rate
  from reverts and hotfixes, time to restore from incident issues).
- [ ] **M13** Reverts and hotfixes per month: the change failure rate.
- [ ] **M14** Bus factor and knowledge islands, for organisation profiles.
- [ ] **M22** Organisations: two-factor authentication required, base permissions, SSO (organisation
  profiles).

### T-307 · The charter and the grid, one engine
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Rule format v2 and authoring, One measure drives
  every command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.7.3, "The charter and the grid, one engine": Decision 4, before the format freezes:
shared detectors first, then the charter as the grid's rules in strict or ratchet regime, its IDs
kept as aliases; rule files checked by a published schema. ⚠ breaking: `charter.toml` lists grid
rule IDs with their regime, converted by `kiln update`.

- [ ] **G09** `related`, `supersedes` and `aliases`: old IDs answered forever, the stable-ID promise
  of v1.0.
- [ ] **G16** A published JSON Schema for rule files: editors check a rule as it is typed (taplo, VS
  Code).
- [ ] **P11** The charter and the grid as one engine (decision 4): shared detectors first, a test
  that makes a rule and its charter twin agree on the examples; at v1.0.0 a rule written once in the
  grid, `charter.toml` listing rule IDs with their regime and budget, the charter's IDs kept as
  aliases.

### T-310 · Java and Kotlin read: Maven, Gradle, Spring Boot, the LTS lines
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, API, contracts and typing,
  Supply chain), made a ticket on 25 October 2026 at antoine's request; one stack per ticket from
  the same day (.NET in T-322)

Planned in v0.7.4, "Java and Kotlin repos, read": The road to v0.8.0: every common stack scored and
fixed by script as Django is at v0.5.0, stack by stack (decision 1) in the order the corpus measures
(B01; until it does, the order of the 2025 surveys, Stack Overflow's and GitHub's Octoverse). Two
releases a stack, about what Django and Nuxt each took once the engine is set aside: first what its
repos are made of, read, so that the rules spanning stacks see it; then its pack, counted once ten
corpus repos of it were checked (B24). Each stack's rules are written from the corpus when its turn
comes. First Java and Kotlin: Maven and Gradle read with their wrappers, Spring Boot, Quarkus and
Micronaut recognised: kiln's own frozen Java template held to its stack's rules at last.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B08** Java and Kotlin: Maven (wrapper and checksum), Gradle in its Groovy and Kotlin DSLs
  (wrapper validation, version catalogs, locking, verification metadata), Spring Boot, Quarkus,
  Micronaut, Ktor; Checkstyle, SpotBugs, Error Prone, Spotless, ktlint, detekt; JUnit 5; Java's LTS
  lines. kiln's own frozen Java template would finally be scored.
- [ ] **AT27** `KOTLIN-EXPLICIT-API`: explicit API mode for Kotlin libraries. L1 · fix S · trial.
- [ ] **AT28** `JAVA-NULLNESS`: JSpecify annotations checked by NullAway. L1 · fix J · assess.
- [ ] **SU24** `GRADLE-WRAPPER-VERIFIED`: `distributionSha256Sum` set and the wrapper validated in
  CI. L1 · fix S · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Java and Kotlin repos too, each with a passing and a failing example from Java and Kotlin.

### T-311 · The Java and Kotlin pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (C# in T-323)

Planned in v0.7.5, "The Java and Kotlin pack": A supported LTS, a verified wrapper, locked
dependencies and a bug finder in the build, then Spring Boot's own rules, counted once ten corpus
repos of Java and Kotlin were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP13** Java and Kotlin · `JAVA-LTS`: a supported LTS (17, 21, 25) in the toolchain's config.
  L1 · fix S · adopt.
- [ ] **SP14** Java and Kotlin · `WRAPPER-COMMITTED`: Gradle or Maven wrapper committed with its
  checksum. L1 · fix S · adopt.
- [ ] **SP15** Java and Kotlin · `DEPENDENCY-LOCKING`: Gradle's dependency locking, or Maven plugins
  and versions pinned and checked by the enforcer. L1 · fix S · trial.
- [ ] **SP16** Java and Kotlin · `BUG-FINDER`: Error Prone or SpotBugs in the build; detekt and
  ktlint for Kotlin. L1 · fix S · trial.
- [ ] Ten corpus repos of Java and Kotlin scored and their findings checked before the pack counts
  (B24), each false alarm fixed in the engine.

### T-337 · The Spring Boot pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: framework coverage review of 26 October 2026 at antoine's request: the most used
  frameworks of the 2025 surveys checked against the plan; the pack of its language held only the
  language's rules

Planned in v0.7.5, "The Java and Kotlin pack": A supported LTS, a verified wrapper, locked
dependencies and a bug finder in the build, then Spring Boot's own rules, counted once ten corpus
repos of Java and Kotlin were checked (B24).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FP29** Spring Boot · `SPRING-DDL-AUTO`: `spring.jpa.hibernate.ddl-auto` never `update`,
  `create` or `create-drop` outside development; the schema moved by Flyway or Liquibase. L1 · fix J
  · adopt.
- [ ] **FP30** Spring Boot · `SPRING-OPEN-IN-VIEW-OFF`: `spring.jpa.open-in-view=false`, so no query
  runs while the view renders. L1 · fix S · trial.
- [ ] **FP31** Spring Boot · `SPRING-VALIDATION`: `@Valid` or `@Validated` on every request body. L2
  · fix J · adopt.
- [ ] **FP32** Spring Boot · `SPRING-CONSTRUCTOR-INJECTION`: dependencies through the constructor,
  no `@Autowired` field. L2 · fix J · trial.
- [ ] **AS20** (Spring's part) `NO-HARDCODED-PASSWORDS`: no password, key or token in
  `application.yml` or `application.properties`, `${…}` placeholders from the environment instead.
  L1 · fix J · adopt.
- [ ] **AS22** (Spring Security's part) `CSRF-ON`: `csrf` disabled only on a stateless API, with a
  justification marker. L2 · fix J · adopt.
- [ ] **AS48** (Spring's part) `NO-SQL-INJECTION`: `createNativeQuery`, `JdbcTemplate` and
  `@Query(nativeQuery = true)` never built by concatenation. L2 · fix J · adopt.
- [ ] **DM18** (Flyway's and Liquibase's part) `ORM-MIGRATIONS-COMMITTED`: their migrations
  committed. L0 · fix J · adopt.
- [ ] Ten corpus repos of Spring Boot scored and their findings checked before the pack counts
  (B24), each false alarm fixed in the engine.

### T-322 · C# and .NET read: projects, central packages, nullable, supported lines
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-310 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem, API, contracts and typing, Supply chain)

Planned in v0.7.6, "C# and .NET repos, read": Projects, solutions and central package management
read, with nullable references and the supported .NET lines.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B09** C# and .NET: .csproj, .sln and .slnx, central package management,
  `packages.lock.json`, `<Nullable>enable`, analyzers, `dotnet format`, `global.json`, supported
  .NET lines. ASP.NET Core (`Program.cs`, minimal APIs or controllers), Blazor Server and
  WebAssembly, EF Core, user secrets. Visual Basic and F# projects read alike; WPF, WinForms and
  .NET MAUI recognised.
- [ ] **AT25** `CSHARP-NULLABLE`: `<Nullable>enable</Nullable>` in every project. L1 · fix S ·
  adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read C#
  repos too, each with a passing and a failing example from C#.

### T-323 · The C# pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-311 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.7, "The C# pack": NuGetAudit, lock files, warnings as errors and a pinned SDK, then
the rules of ASP.NET Core and Blazor, counted once ten corpus repos of C# were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP17** C# · `CENTRAL-PACKAGES`: `Directory.Packages.props` and lock files
  (`RestorePackagesWithLockFile`). L1 · fix S · trial.
- [ ] **SP18** C# · `NUGET-AUDIT`: NuGetAudit on, transitive packages included, high findings as
  errors. L1 · fix S · adopt.
- [ ] **SP19** C# · `WARNINGS-AS-ERRORS`: `TreatWarningsAsErrors` and a current `AnalysisLevel` in
  `Directory.Build.props`. L1 · fix S · trial.
- [ ] **SP20** C# · `DOTNET-SUPPORTED`: the target framework on a supported .NET release. L1 · fix S
  · adopt.
- [ ] **SP21** C# · `GLOBAL-JSON`: the SDK pinned in `global.json` with a `rollForward` policy. L1 ·
  fix S · trial.
- [ ] Ten corpus repos of C# scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.

### T-338 · The ASP.NET Core and Blazor pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: framework coverage review of 26 October 2026 at antoine's request: the most used
  frameworks of the 2025 surveys checked against the plan; the pack of its language held only the
  language's rules

Planned in v0.7.7, "The C# pack": NuGetAudit, lock files, warnings as errors and a pinned SDK, then
the rules of ASP.NET Core and Blazor, counted once ten corpus repos of C# were checked (B24).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS07** (ASP.NET Core's part) `PUBLIC-ROUTES`: a fallback authorization policy that requires
  an authenticated user, every `[AllowAnonymous]` deliberate. L2 · fix J · adopt.
- [ ] **AS22** (ASP.NET Core's part) `CSRF-ON`: antiforgery on for forms and Blazor, each
  `[IgnoreAntiforgeryToken]` with a justification marker. L2 · fix J · adopt.
- [ ] **AS20** (ASP.NET Core's part) `NO-HARDCODED-PASSWORDS`: no password in a connection string of
  `appsettings*.json`; user secrets in development, the environment or a vault in production. L1 ·
  fix J · adopt.
- [ ] **AS45** (ASP.NET Core's part) `FRAMEWORK-DEBUG-OFF`: `UseDeveloperExceptionPage` only in the
  Development environment. L2 · fix S · adopt.
- [ ] **AS35** (ASP.NET Core's part) `HTTPS-ONLY`: `UseHttpsRedirection` and `UseHsts` outside
  development. L2 · fix S · adopt.
- [ ] **AS36** (Blazor's part) `NO-SECRETS-IN-FRONT`: nothing secret in the
  `wwwroot/appsettings*.json` of a Blazor WebAssembly client, which every visitor downloads. L1 ·
  fix J · adopt.
- [ ] **AS48** (EF Core's part) `NO-SQL-INJECTION`: `FromSqlRaw` and `ExecuteSqlRaw` never given an
  interpolated string (`FromSql` takes one safely). L2 · fix S · adopt.
- [ ] **DM18** (EF Core's part) `ORM-MIGRATIONS-COMMITTED`: EF Core migrations committed. L0 · fix J
  · adopt.
- [ ] Ten corpus repos of ASP.NET Core and Blazor scored and their findings checked before the pack
  counts (B24), each false alarm fixed in the engine.

### T-312 · PHP read: Composer, Laravel, Symfony, WordPress
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, API, contracts and typing), made
  a ticket on 25 October 2026 at antoine's request; one stack per ticket from the same day (Ruby in
  T-324)

Planned in v0.7.8, "PHP repos, read": Composer, Laravel, Symfony and WordPress read, with their
analysers, formatters, tests and auditor.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B10** PHP: Composer, Laravel, Symfony, WordPress (themes, plugins, wp-config), PHPStan or
  Psalm, PHP-CS-Fixer, PHPUnit or Pest, `composer audit`.
- [ ] **F10** (PHP's part) `composer audit`.
- [ ] **AT26** `PHPSTAN-LEVEL`: PHPStan at level 6 or higher, or Psalm's equivalent. L1 · ratchet ·
  trial.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read PHP
  repos too, each with a passing and a failing example from PHP.

### T-313 · The PHP pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (Ruby in T-325, Elixir in T-326)

Planned in v0.7.9, "The PHP pack": Strict types, `composer audit` in CI, a supported PHP and no
`phpinfo()` left, then the rules of Laravel, Symfony and WordPress, counted once ten corpus repos of
PHP were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP22** PHP · `COMPOSER-AUDIT`: `composer audit` in CI, `composer.lock` committed for
  applications. L1 · fix S · adopt.
- [ ] **SP23** PHP · `STRICT-TYPES`: `declare(strict_types=1);` in every file. L2 · fix S · adopt.
- [ ] **SP24** PHP · `PHP-SUPPORTED`: `require.php` on a supported PHP line. L1 · fix S · adopt.
- [ ] **SP25** PHP · `NO-PHPINFO`: no `phpinfo()` reachable. L2 · fix S · adopt.
- [ ] Ten corpus repos of PHP scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.

### T-339 · The Laravel, Symfony and WordPress pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: framework coverage review of 26 October 2026 at antoine's request: the most used
  frameworks of the 2025 surveys checked against the plan; the pack of its language held only the
  language's rules

Planned in v0.7.9, "The PHP pack": Strict types, `composer audit` in CI, a supported PHP and no
`phpinfo()` left, then the rules of Laravel, Symfony and WordPress, counted once ten corpus repos of
PHP were checked (B24).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS32** (Laravel's part) `NO-MASS-ASSIGNMENT`: no `$guarded = []` nor `Model::unguard()`, a
  `$fillable` list instead. L2 · fix J · adopt.
- [ ] **FP33** Laravel · `LARAVEL-ENV-IN-CONFIG`: `env()` called only in `config/`, which
  `config:cache` would otherwise break; `.env` untracked and `.env.example` committed. L2 · fix J ·
  adopt.
- [ ] **AT26** (Laravel's part) `PHPSTAN-LEVEL`: Larastan loaded, so PHPStan understands facades and
  Eloquent. L1 · fix S · trial.
- [ ] **AS22** (Laravel's part) `CSRF-ON`: each route left out of CSRF checks
  (`validateCsrfTokens(except: …)`) with a justification marker. L2 · fix J · adopt.
- [ ] **AS48** (the part of Laravel, Doctrine and WordPress) `NO-SQL-INJECTION`: `whereRaw`,
  `DB::raw`, DQL and `$wpdb->query` never built from a variable, `$wpdb->prepare` for WordPress. L2
  · fix J · adopt.
- [ ] **AS01** (Symfony's part) `SECRETS`: a real `APP_SECRET` never in a committed `.env`,
  Symfony's secrets vault or the environment instead. L1 · fix J · adopt.
- [ ] **AS45** (the part of Symfony and WordPress) `FRAMEWORK-DEBUG-OFF`: `APP_ENV=prod` with
  `APP_DEBUG=0`, `WP_DEBUG` and `WP_DEBUG_DISPLAY` off in production. L2 · fix S · adopt.
- [ ] **FP34** WordPress · `WP-NONCES`: every admin, AJAX and REST handler checks a nonce and a
  capability (`check_ajax_referer`, `current_user_can`, a `permission_callback`). L2 · fix J ·
  adopt.
- [ ] **FP35** WordPress · `WP-CODING-STANDARDS`: PHPCS with the WordPress Coding Standards in CI,
  whose sniffs check escaping and sanitizing. L1 · fix S · adopt.
- [ ] Ten corpus repos of Laravel, Symfony and WordPress scored and their findings checked before
  the pack counts (B24), each false alarm fixed in the engine.

### T-327 · C and C++ read: CMake, Meson, Bazel, Conan, vcpkg
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-314 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem)

Planned in v0.7.10, "C and C++ repos, read": CMake, Meson, Bazel, Conan and vcpkg read, with
clang-format, clang-tidy, sanitizers and fuzzing.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B13** C and C++: CMake, Meson, Bazel, Conan and vcpkg manifests, clang-format, clang-tidy,
  sanitizers and fuzzing in CI, warnings as errors. Firmware too: PlatformIO, Arduino, ESP-IDF and
  Zephyr projects, their board and toolchain pinned.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read C
  and C++ repos too, each with a passing and a failing example from C and C++.

### T-328 · The C and C++ pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-315 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.11, "The C and C++ pack": Warnings as errors, sanitizers in CI, clang-tidy, fuzzing
for parsers and managed dependencies, counted once ten corpus repos of C and C++ were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP35** C and C++ · `COMPILER-WARNINGS`: `-Wall -Wextra -Werror` (or `/W4 /WX`) in the build.
  L1 · fix S · trial.
- [ ] **SP36** C and C++ · `SANITIZERS-IN-CI`: AddressSanitizer and UndefinedBehaviorSanitizer
  builds in CI. L1 · fix S · trial.
- [ ] **SP37** C and C++ · `CLANG-TIDY`: configured and run. L1 · fix S · trial.
- [ ] **SP38** C and C++ · `FUZZING`: libFuzzer harnesses or OSS-Fuzz for parsers (Scorecard's
  Fuzzing). L1 · fix J · assess.
- [ ] **SP39** C and C++ · `MANAGED-DEPENDENCIES`: vcpkg or Conan manifests rather than copied
  sources. L1 · fix J · trial.
- [ ] Ten corpus repos of C and C++ scored and their findings checked before the pack counts (B24),
  each false alarm fixed in the engine.

### T-308 · Go read: modules, toolchains, race tests, errors
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Mature tools as detectors,
  Concurrency, Errors and logs, Supply chain), made a ticket on 25 October 2026 at antoine's
  request; one stack per ticket from the same day (Rust in T-320)

Planned in v0.7.12, "Go repos, read": go.mod, go.sum and the toolchain read, with golangci-lint,
govulncheck, race tests and wrapped errors, `go.sum` held to the rules that span stacks.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B06** Go: go.mod and go.sum, the `go` and `toolchain` directives, golangci-lint, gofmt,
  govulncheck, `go vet`, `-race` in CI, vendoring. Gin, Echo, Fiber and chi recognised.
- [ ] **F10** govulncheck for Go (reachable vulnerabilities only); cargo-deny, `composer audit` and
  bundler-audit come with their stacks (T-320, T-312, T-324).
- [ ] **CC09** `GO-RACE`: `go test -race` in CI. L1 · fix S · adopt.
- [ ] **EL12** `GO-ERROR-WRAPPING`: `fmt.Errorf("…: %w", err)`. L2 · fix J · trial.
- [ ] **SU33** `LOCKS-COMMITTED`: `go.sum` committed (`Cargo.lock` comes with Rust, T-320). L0 · fix
  J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read Go
  repos too, each with a passing and a failing example from Go.

### T-309 · The Go pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (Rust in T-321)

Planned in v0.7.13, "The Go pack": Go's own rules with their examples and converters, from a tidy
`go.mod` to no `panic` in a library, counted once ten corpus repos of Go were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP01** Go · `GO-MOD-TIDY`: `go mod tidy` would change nothing. L4 · fix S · adopt.
- [ ] **SP02** Go · `GO-LINT`: `go vet` and golangci-lint (its v2 config) in CI. L1 · fix S · adopt.
- [ ] **SP03** Go · `GOVULNCHECK`: govulncheck in CI, which reports only the vulnerable code a
  program reaches. L1 · fix S · adopt.
- [ ] **SP04** Go · `GO-TOOLCHAIN-SUPPORTED`: the `go` directive and `toolchain` on one of the two
  supported releases. L1 · fix S · adopt.
- [ ] **SP05** Go · `GO-CONTEXT-FIRST`: `context.Context` as first parameter, never stored in a
  struct. L2 · fix J · trial.
- [ ] **SP06** Go · `GO-NO-PANIC-IN-LIBS`: no `panic` on a library's ordinary paths. L2 · fix J ·
  trial.
- [ ] Ten corpus repos of Go scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
- [ ] **FP28** Go · `GO-HTTP-TIMEOUTS`: an `http.Server` with `ReadHeaderTimeout`, never a bare
  `http.ListenAndServe` in a server (gosec G112, G114). L2 · fix J · adopt.

### T-320 · Rust read: Cargo, clippy, editions, `unsafe`, locks
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-308 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem, Mature tools as detectors, Concurrency, Supply chain)

Planned in v0.7.14, "Rust repos, read": Cargo, clippy, the edition and `unsafe` read, `Cargo.lock`
held to the rules that span stacks.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B07** Rust: Cargo.lock committed, clippy, rustfmt, cargo-deny or cargo-audit,
  `rust-version`, the edition, `unsafe` justified, cargo-semver-checks for libraries. Axum and Actix
  Web recognised.
- [ ] **F10** (Rust's part) cargo-deny for Rust.
- [ ] **CC11** `RUST-NO-STATIC-MUT`: no `static mut`. L2 · fix J · adopt.
- [ ] **SU33** (Rust's part) `LOCKS-COMMITTED`: `Cargo.lock` committed. L0 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Rust repos too, each with a passing and a failing example from Rust.

### T-321 · The Rust pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-309 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.15, "The Rust pack": Rust's own rules, from clippy with warnings as errors to a
declared MSRV, counted once ten corpus repos of Rust were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP07** Rust · `CLIPPY-CLEAN`: clippy with warnings as errors in CI, a `[lints]` table in
  `Cargo.toml`. L1 · fix S · adopt.
- [ ] **SP08** Rust · `CARGO-DENY`: cargo-deny (advisories, licences, bans, sources) or cargo-audit
  in CI. L1 · fix S · adopt.
- [ ] **SP09** Rust · `RUST-EDITION-CURRENT`: edition 2024 (stable since Rust 1.85, February 2025).
  L1 · fix J · trial.
- [ ] **SP10** Rust · `RUST-MSRV`: `rust-version` declared and tested. L1 · fix S · trial.
- [ ] **SP11** Rust · `UNSAFE-JUSTIFIED`: every `unsafe` block with a `// SAFETY:` comment (clippy's
  `undocumented_unsafe_blocks`). L2 · fix J · adopt.
- [ ] **SP12** Rust · `NO-UNWRAP-IN-LIBS`: `unwrap` and `expect` counted in library code (clippy's
  `unwrap_used`). L2 · ratchet · trial.
- [ ] Ten corpus repos of Rust scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.

### T-324 · Ruby read: Bundler, Rails, RuboCop, bundler-audit
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-312 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem, API, contracts and typing)

Planned in v0.7.16, "Ruby repos, read": Bundler and Rails read, with RuboCop, Sorbet or RBS, RSpec
or Minitest and bundler-audit.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B11** Ruby: Bundler, Rails (credentials, `force_ssl`, Brakeman), RuboCop, Sorbet or RBS,
  RSpec or Minitest, bundler-audit.
- [ ] **F10** (Ruby's part) bundler-audit.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Ruby repos too, each with a passing and a failing example from Ruby.

### T-325 · The Ruby pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-313 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.17, "The Ruby pack": Brakeman and bundler-audit in CI, RuboCop configured, a
supported Ruby and no `permit!`, counted once ten corpus repos of Ruby were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP26** Ruby · `BUNDLER-AUDIT` and `BRAKEMAN`: both in CI for Rails apps, `Gemfile.lock`
  committed. L1 · fix S · adopt.
- [ ] **SP27** Ruby · `RUBOCOP`: RuboCop or Standard configured. L1 · fix S · adopt.
- [ ] **SP28** Ruby · `RUBY-SUPPORTED`: `.ruby-version` on a supported line. L1 · fix S · adopt.
- [ ] **SP29** Ruby · `RAILS-STRONG-PARAMS`: no `permit!`. L2 · fix J · adopt.
- [ ] Ten corpus repos of Ruby scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
- [ ] **FP36** Rails · `RAILS-STRONG-MIGRATIONS`: the strong_migrations gem, so a migration that
  would lock a live table is stopped. L1 · fix S · trial.
- [ ] **AS01** (Rails' part) `SECRETS`: `config/master.key` and `config/credentials/*.key` never
  committed. L0 · fix J · adopt.

### T-314 · iOS, Android and Flutter read: SwiftPM, the manifest, pubspec
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Application security), made a
  ticket on 25 October 2026 at antoine's request; one stack per ticket from the same day (Elixir in
  T-326, C and C++ in T-327, the long tail in T-329)

Planned in v0.7.18, "iOS, Android and Flutter repos, read": SwiftPM, CocoaPods, the Android manifest
and Flutter's pubspec read; App Transport Security and exported components checked.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B12** Swift (SwiftPM, CocoaPods, SwiftLint), Android (manifest, R8), Dart and Flutter
  (pubspec, analysis_options); React Native and Expo (`app.json`, `app.config.*`, `eas.json`);
  Kotlin Multiplatform, Ionic and Capacitor, .NET MAUI's mobile targets; Elixir's part is in T-326.
- [ ] **AS41** `ANDROID-MANIFEST`: not debuggable, no cleartext traffic, backups off, every
  component's `exported` explicit. L1 · fix S · adopt.
- [ ] **AS42** `IOS-ATS`: App Transport Security left on. L1 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Swift, Android and Flutter repos too, each with a passing and a failing example from Swift,
  Android and Flutter.

### T-315 · The mobile pack
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (C and C++ in T-328)

Planned in v0.7.19, "The mobile pack": What the stores require and what an app bundle gives away:
the privacy manifest, the target SDK, no server secret in the app, signing keys out of git, counted
once ten corpus repos of apps were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP30** Mobile · `IOS-PRIVACY-MANIFEST`: `PrivacyInfo.xcprivacy` declaring the
  required-reason APIs (required by Apple since May 2024). L1 · fix J · adopt.
- [ ] **SP31** Mobile · `ANDROID-TARGET-SDK`: `targetSdkVersion` meets Google Play's current
  requirement, from a dated calendar. L1 · fix S · adopt.
- [ ] **SP32** Mobile · `NO-SERVER-SECRETS-IN-APP`: nothing secret in an app bundle (everything in
  it is public); client keys restricted instead. L2 · fix J · adopt.
- [ ] **SP33** Mobile · `SIGNING-OUT-OF-GIT`: no keystore, `.p12` or provisioning profile committed.
  L0 · fix J · adopt.
- [ ] **SP34** Mobile · `FLUTTER-STRICT`: `analysis_options.yaml` with the strict modes. L1 · fix S
  · trial.
- [ ] Ten corpus repos of apps (iOS, Android, Flutter) scored and their findings checked before the
  pack counts (B24), each false alarm fixed in the engine.
- [ ] **FP37** Expo · `EXPO-SDK-SUPPORTED`: one of the Expo SDKs still supported. L1 · fix J ·
  adopt.
- [ ] **AS36** (Expo's part) `NO-SECRETS-IN-FRONT`: `EXPO_PUBLIC_*` variables too, compiled into the
  app. L2 · fix J · adopt.

### T-340 · Game repos: Unity, Godot, Unreal, Roblox, Lua
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: stack coverage review of 26 October 2026, at antoine's request ("sois sûr que kiln
  couvre bien tout"): Lua at 9 % of the 2025 Stack Overflow survey and game repos had two boxes in
  T-300, nothing that read them

Planned in v0.7.20, "Game repos, read and packed": Unity, Godot, Unreal and Roblox repos read on top
of the C# and C++ packs, with Lua and Luau: the engine's version pinned, assets in Git LFS, caches
and builds out of git, no store or signing credential committed.

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B14** (Lua's part) Game repos read: Unity (`ProjectSettings/ProjectVersion.txt`,
  `Packages/manifest.json` and its lock), Godot (`project.godot`, GDScript with gdtoolkit's gdlint
  and gdformat, its C# projects), Unreal (`.uproject`, `.uplugin`, `Source/`, `Config/`), Roblox
  (Rojo's `default.project.json`, Wally, Rokit or Aftman), LÖVE; Lua and Luau with selene or
  luacheck, StyLua, Luau's type checker, busted, LuaRocks' rockspecs.
- [ ] **FP39** Unity · `UNITY-REPO`: `.meta` files committed with their assets, `Library/`, `Temp/`
  and builds ignored, large binaries in Git LFS. L0 · fix S · adopt.
- [ ] **FP40** Godot · `GODOT-REPO`: `.godot/` ignored, no signing credentials in
  `export_presets.cfg`. L0 · fix S · adopt.
- [ ] **SP43** Games · `ENGINE-VERSION-PINNED`: the engine's version recorded in the repo (Unity's
  `ProjectVersion.txt`, Godot's `config/features`, Unreal's `EngineAssociation`) and the same in
  CI. L0 · fix J · adopt.
- [ ] **FP41** Unreal · `UNREAL-REPO`: `Binaries/`, `Intermediate/`, `Saved/` and
  `DerivedDataCache/` ignored, `.uasset` and `.umap` in Git LFS. L0 · fix S · adopt.
- [ ] **FP42** Roblox · `LUAU-STRICT`: `--!strict` in Luau modules, selene and StyLua in CI. L1 ·
  fix S · trial.
- [ ] **SP44** Lua · `LUA-LINT`: selene or luacheck and StyLua in CI. L1 · fix S · trial.
- [ ] **AS01** (games' part) `SECRETS`: no keystore, `.p12`, Steamworks or store credential
  committed. L0 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  game repos too, each with a passing and a failing example from Unity, Godot or Lua.
- [ ] Ten corpus repos of games scored and their findings checked before the pack counts (B24),
  each false alarm fixed in the engine.

### T-341 · R read and its pack: renv, lintr, testthat, R CMD check
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: stack coverage review of 26 October 2026, at antoine's request ("sois sûr que kiln
  couvre bien tout"): R, at 5 % of the 2025 Stack Overflow survey and common in coursework and
  research, was only a data pack of B14

Planned in v0.7.21, "R repos, read and packed": R packages and analyses read and packed in one
release: DESCRIPTION and renv, lintr, testthat and R CMD check, beyond the notebooks the data
science release (v0.6.58) reads.

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B14** (R's part) R: `DESCRIPTION` and `NAMESPACE`, `renv.lock`, lintr, styler, testthat,
  `R CMD check` in CI (r-lib/actions), Shiny apps; R Markdown and Quarto stay read as notebooks
  (T-292).
- [ ] **SP45** R · `RENV-LOCKED`: `renv.lock` committed for an analysis or an app, restored in CI.
  L0 · fix S · adopt.
- [ ] **SP46** R · `R-CMD-CHECK`: a package passes `R CMD check` in CI without error or warning. L1
  · fix S · adopt.
- [ ] **SP47** R · `LINTR`: lintr configured and run. L1 · fix S · trial.
- [ ] **SP48** R · `NO-SETWD`: no `setwd()` or absolute path in a script; the project's root
  (`here`) instead. L2 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read R
  repos too, each with a passing and a failing example from R.
- [ ] Ten corpus repos of R scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.

### T-326 · Elixir read and its pack: mix, Phoenix, Credo, Sobelow
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-313 and T-314 on 25 October 2026, one stack per ticket (kiln score ideas
  of 24 October 2026: Every ecosystem, Stack packs)

Planned in v0.7.22, "Elixir repos, read and packed": A smaller ecosystem, read and packed in one
release: mix and Phoenix, with Credo, Dialyzer, Sobelow and mix_audit as its rules.

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B12** (Elixir's part) Elixir: mix, Phoenix, Credo, Dialyzer, Sobelow.
- [ ] **SP40** Elixir · `MIX-AUDIT`: mix_audit or `mix hex.audit` in CI, `mix.lock` committed. L1 ·
  fix S · adopt.
- [ ] **SP41** Elixir · `CREDO-AND-DIALYZER`: both configured. L1 · fix S · trial.
- [ ] **SP42** Elixir · `SOBELOW`: Sobelow for Phoenix apps. L1 · fix S · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Elixir repos too, each with a passing and a failing example from Elixir.
- [ ] Ten corpus repos of Elixir scored and their findings checked before the pack counts (B24),
  each false alarm fixed in the engine.

### T-329 · The long tail as data packs
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: split from T-314 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem)

Planned in v0.8.0, "Every common stack scored": Milestone decided by antoine (25 October 2026),
reached here: every common stack scored and fixed by script before the format freezes. The rarer
languages come as data packs that the community packs of v1.0.0 will extend; then the gate, the
corpus re-scored and each stack among those that make 95 % of its repos shown at the level of Django
at v0.5.0.

Below the stacks that make 95 % of the corpus's repos: each language's facts as data (manifests,
locks, tools), read by the rules that span stacks, and a pack of its own only once the corpus or a
community pack (T-69) asks for one.

- [ ] **B14** The long tail as data packs: Scala (sbt, Mill), Haskell, OCaml, Clojure, Erlang, F#,
  Julia, Perl, Zig, Nim, Fortran (fpm), MATLAB, Solidity (its rules in T-300); R has its release
  (T-341), Lua comes with the games (T-340).

### T-330 · Every common stack scored, measured: the corpus's 95 %
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: the bar of v1.0.0 (antoine, 25 October 2026), its stacks made the gate of v0.8.0 the
  same day, when each stack got its releases

Planned in v0.8.0, "Every common stack scored": Milestone decided by antoine (25 October 2026),
reached here: every common stack scored and fixed by script before the format freezes. The rarer
languages come as data packs that the community packs of v1.0.0 will extend; then the gate, the
corpus re-scored and each stack among those that make 95 % of its repos shown at the level of Django
at v0.5.0.

The gate of v0.8.0, as T-03 is the launch's: the milestone is cut only once these hold.

- [ ] The corpus re-scored (T-219): the share of its repos, and of its code, whose stacks each have
  a pack (B01); 95 % or more, otherwise the missing stack gets its releases before v0.8.0.
- [ ] Each of those packs at the level of Django at v0.5.0: its facts, its rules with their
  examples, its converters, its precision on ten corpus repos (B24, H03), no strict rule under 99 %.
- [ ] Every change the stacks forced on the rule format listed with its conversion: the evidence
  that the format can freeze.
- [ ] The milestone's note: the stacks and their precision, the order the corpus gave, what is left
  to community packs (T-69).

### T-316 · The CIs used most after GitHub's and GitLab's: Forgejo, Bitbucket, Azure, CircleCI
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Nothing to do,
  Outputs and integrations), made a ticket on 25 October 2026 at antoine's request; cut in four the
  same day (T-331 to T-333)

Planned in v0.8.1, "The CIs used most after GitHub's and GitLab's": The road to v0.9.0: any CI, any
machine, any size, the last before the format freezes. First the CIs used most after GitHub's and
GitLab's (v0.6.63), read into the CI model of v0.6.21 with their pinning and their untrusted text
(appendix B).

- [ ] **C03** The CIs used most after GitHub's and GitLab's, read into the CI model (T-230): Forgejo
  and Gitea Actions (GitHub's format), Bitbucket Pipelines, Azure Pipelines, CircleCI (orbs pinned);
  the others in T-331.
- [ ] Each one's pinning and untrusted text (appendix B) checked by the CI rules that already read
  GitHub's, with an example per CI.

### T-331 · Every other CI read: Jenkins, Buildkite, Woodpecker, the clouds', Tekton
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-316 on 25 October 2026 (kiln score ideas of 24 October 2026: Every forge,
  CI, host and machine)

Planned in v0.8.2, "Every other CI": Jenkins, Buildkite, Woodpecker, the clouds' own CIs, Tekton and
the rest, read the same way.

- [ ] **C03** (the others) Jenkins (Jenkinsfile, shared libraries pinned), Buildkite, Woodpecker and
  Drone, SourceHut, TeamCity, AppVeyor, Travis (`hold`), Google Cloud Build, AWS CodeBuild, Tekton,
  Argo Workflows, Dagger, Earthly.
- [ ] The same CI rules on each of them, with an example per CI.

### T-332 · Every machine and every network: macOS, WSL, ARM64, musl, offline, proxies
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-316 on 25 October 2026 (kiln score ideas of 24 October 2026: Every forge,
  CI, host and machine)

Planned in v0.8.3, "Every machine, every network": macOS and WSL tested beside Linux, ARM64 and
musl, air-gapped and corporate networks; native Windows only if T-94 reopens.

- [ ] **C14** kiln score runs on Linux, macOS, WSL and native Windows (it is Python and git) ⚠ T-94
  declined Windows without WSL for kiln as a whole; the score alone may cost little, tested in CI if
  taken.
- [ ] **C15** x86-64 and ARM64 (Apple Silicon, Graviton, Raspberry Pi), glibc and musl (Alpine):
  every bundled tool shipped as a wheel for each, or its rules say "unknown" there.
- [ ] **C18** Air-gapped and corporate networks: offline by default; `--online` honours
  `HTTPS_PROXY` and custom certificate authorities (`SSL_CERT_FILE`); the data bundle downloadable
  as one file (`--data bundle.tar.zst`).

### T-333 · No Python needed: a signed binary, npx, the browser
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-316 on 25 October 2026 (kiln score ideas of 24 October 2026: Every forge,
  CI, host and machine, Outputs and integrations)

Planned in v0.8.4, "No Python needed": A single signed binary, `npx kiln-cli score` for JavaScript
machines, and the score in a browser if the forges allow it; a language server only if T-117
reopens.

- [ ] **K02** A single signed binary for machines without Python or uv (PyApp, which bootstraps
  through uv, or a frozen build), on each GitHub release.
- [ ] **K03** `npx kiln-cli score` for JavaScript-only machines: a small npm package that runs the
  binary.
- [ ] **K06** In the browser with Pyodide, on a tarball fetched from the forge's API, no server at
  all; to verify (CORS on the tarball endpoints).
- [ ] **L12** A language server: diagnostics for place rules in any editor, code actions for
  scripted fixes ⚠ T-117 (a VS Code extension) is declined for now; a language server serves every
  editor at once, only if adopters ask.

### T-317 · Monorepos and big trees: project graphs, rules in parallel, a time budget
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Speed), made a
  ticket on 25 October 2026 at antoine's request; the million files split off the same day (T-334)

Planned in v0.8.5, "Monorepos and big trees": Monorepo tools' project graphs read for components and
their links (T-86 staying declined for generating them), rules run in parallel, and a time budget
that says what it left out.

- [ ] **C19** Monorepo tools' project graphs (Nx, Turborepo, Bazel, Pants, Rush, Moon) read for
  components and their links ⚠ T-86 (declined) is about generating monorepos; scoring them is
  another matter.
- [ ] **J09** Rules in parallel: threads for I/O-bound rules, processes on big repos; free-threaded
  Python 3.14 measured.
- [ ] **J17** A time budget (`--budget 2s`): rules by value per cost, and what didn't run is said
  ("not checked: budget").

### T-334 · A million files: sampling, Rust where a profile points, the speed published
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from T-317 on 25 October 2026 (kiln score ideas of 24 October 2026: Speed)

Planned in v0.8.6, "A million files": Sampling with a stated margin, Rust only where a profile
points, then the speed published as uv and ruff publish theirs.

- [ ] **J14** A resident process only if measurements demand it, as language servers do; never by
  default.
- [ ] **J15** Rust only where a profile points: the walker, glob matching and the multi-pattern scan
  are the candidates (a `kiln-core` wheel through PyO3), or ripgrep's engine through `rg --json`
  when installed.
- [ ] **J18** Metrics sampled on huge repos with a stated margin (sizes, complexity); security rules
  always exhaustive.
- [ ] **J20** Speed published as uv and ruff publish theirs: "0.3 s on Django's own repo, 4 s on a
  million files". Speed is part of the pitch.

### T-335 · Any CI, any machine, any size: the bar's matrix, run
- **Type**: task
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: the bar of v1.0.0 (antoine, 25 October 2026), its CI, machines and sizes made the gate
  of v0.9.0 the same day

Planned in v0.9.0, "Any CI, any machine, any size": Milestone decided by antoine (25 October 2026),
reached here, the last before the format freezes: the bar of v1.0.0 run as a matrix in kiln's own
CI, on GitHub's, GitLab's and one more CI, Linux, macOS and WSL, x86-64 and ARM64, a monorepo and a
million files, each scored within its budget.

The gate of v0.9.0: the milestone is cut only once the matrix is green.

- [ ] A matrix in kiln's own CI (on `release/**`): a sample repo scored on GitHub's CI, GitLab's and
  the one the corpus uses most after them; on Linux, macOS and WSL; on x86-64 and ARM64, glibc and
  musl; offline; a monorepo and a million-file tree, each within its budget.
- [ ] The milestone's note: what each cell measured, and what a cell leaves "unknown".

### T-318 · Does the score mean anything? Seniors, incidents and tokens, measured
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Precision and recall, A grid that stays current,
  Measuring kiln score itself, What the grid doesn't know), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.9.1, "Does the score mean anything? Measured, on every stack": The last proof before
the stability promise, now that every stack is scored: ten senior engineers' ranking against kiln's,
the score against public repos' incidents, readability against tokens, each published whatever it
says.

- [ ] **H16** Seniors' agreement: ten senior engineers rank twenty repos, and kiln's order must
  agree with theirs (Kendall's tau of 0.7 or more). "Like a senior engineer would", measured.
- [ ] **Q09** A radar fed by the corpus: tools rising quarter after quarter become `assess`
  candidates, tools falling become `hold` candidates.
- [ ] **T04** Seniors' agreement (H) measured again each quarter.
- [ ] **T05** Does the score predict anything? Public repos' advisories and incidents against their
  score at the time: evidence for the launch's claim, or a humbling result to publish anyway.
- [ ] **T06** Does readability lower Claude's tokens? T-53's A/B test run again with the readability
  pillar's score as the variable.
- [ ] **U06** Suggestions from the corpus ("repos like yours, Django with Celery and Nuxt, usually
  also have X"): association rules mined from the corpus as `assess` candidates, never findings.

### T-319 · The grid others build on: the JSON schema, packs indexed, everything pinned
- **Type**: improvement
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Outputs and integrations, Packs, local rules,
  standards, Trust, privacy and safety), made a ticket on 25 October 2026 at antoine's request

Planned in v1.0.0, "The grid others build on": Milestone decided by antoine (16 October 2026), its
bar set on 25 October 2026: the public stability promise, once the rule format has held without
breaking on the stacks that make about 95% of the corpus's repos (B01), on GitHub's, GitLab's and
one more CI, on Linux, macOS and WSL, and on monorepos, each scored and fixed by script as Django is
at v0.5.0; the long tail comes as community packs (T-69). From here, strict semver: breaking →
major, `feat` → minor.

- [ ] **L13** The `--json` schema published (`schema.json`), versioned with a changelog, stable at
  v1.0.
- [ ] **R04** Community packs for stacks kiln won't template: FastAPI, Rails, Laravel, Spring Boot,
  Go services.
- [ ] **R05** An index of reviewed packs with their precision on the corpus.
- [ ] **S10** Every executable thing kiln runs pinned and hashed: packs (R) and tools (F).

---

## 📖 How to use (humans and agents)

Next to this file: [done.md](done.md), the closed tickets, one line each, most recent first
(written by `/kiln:backlog done`), [rejected.md](rejected.md), what was turned down, dropped or
ruled out for good, and [urgent.md](urgent.md), what only a human on the team can
do (access, payment, decision), one checkbox per action (counted by the status line).

An audit writes its dated report next to these files (`audit-<topic>-YYYY-MM-DD.md`) while it
runs, copies its open findings into this file (with a pointer to their lines), then moves to `docs/_archive/YYYY-MM-DD-topic/`. Archives **can be read, but everything in them
is old and must be checked** against the current code; they are never edited.

**A ticket** = a `### T-NN · Title` heading, then five fixed lines, then the details:

    ### T-NN · Short title that says what to achieve
    - **Type**: task
    - **Status**: todo
    - **Opened**: YYYY-MM-DD
    - **Effort**: S · **Owner**: … · **Due**: —
    - **Origin**: where it comes from

    Why, what to do (as a `- [ ]` checklist when there are several steps), where to look.

- **ID** `T-NN`: stable, never reused, quoted as is in commits and branches (tickets opened
  before 16 October 2026 were `AF-NN`, same number). The next free one is at the top of this file
  (`Next free: T-NN`).
- **Type**, one of: `bug` (something is broken); `improvement` (it works, it could work
  better); `idea` (nothing exists yet, to be explored); `task` (work that is neither: a release,
  a decision, a check).
- **Status**, one of: `todo`; `in progress — branch <name>, since YYYY-MM-DD`;
  `blocked — waiting for <who or what>`; `to verify — <where>`.
- **Priority** = the section the ticket lives in; changing it means moving the ticket.
  🔴 critical (now), 🟠 important (before the north star), 🟡 normal, ⚪ background
  (long-running work, debt, ideas still to be explored).
- **Effort**, in Claude Code session time on the Pro plan kiln is built with: XS under
  15 minutes, S about half an hour, M about an hour, L two to three hours (split it when it can
  be split). Measured on kiln: on 16 October 2026, 9.3 session-hours shipped four promotions and
  the move to English (about 8,000 lines changed): some twenty times faster than the former
  estimates in human time.
- **Budget**: the Pro quota restarts every Tuesday at 8:00 (Paris). It lasted 42 session-hours
  the week of 6 October and 33 the week of 13 October (limit reached on Friday at 14:03), all
  projects together; a 5-hour window runs out after 2 to 3.5 hours of work. kiln plans on
  25 session-hours a week, about 7 per release, spread over the week (about 5 a day, all
  projects): spent by Friday, it leaves the Saturday and Monday releases without budget. No
  fleet of subagents, no headless run without a budget said beforehand.
- **Releases**: the `## 🚀 Releases` section at the top places every open ticket and every
  kiln score idea in a planned release (`/kiln:backlog plan`); numbers are planned, not promised,
  until the candidate is cut.
- **Closing a ticket**: remove it from its section and add a line at the top of
  [done.md](done.md): `- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.
- **Details in archived audits**: when a ticket quotes lines of `docs/_archive/`, the original
  finding is there in full; it is old, check it against the current code.
- **Locations quoted are hints, not addresses.**
- Overview: `grep -E '^(## |### T-|- \*\*Status)' docs/backlog/backlog.md`.

---

## 🧭 Vision

Why the tickets above exist and how they are judged. Drafted in French on 17 October 2026 from a
long research conversation, two real repos measured that day (the reference repo and a
university repo; the details stay private, see "Repos d'entraînement" in `CLAUDE.md`) and web
research; moved here and condensed on 24 October 2026. What the vision planned became tickets
(the grid as data T-123, `kiln score` T-46, `kiln fix` T-126 to T-128, the roadmap T-129, gap
reports T-38, profiles T-39, the A/B test T-53, the study T-132, tests at the lowest cost T-135
and T-136, the compressor T-138 and T-139, the benchmark T-145); its ideas in reserve and the
paths it dropped are in [rejected.md](rejected.md).

### In one sentence

**kiln keeps a repo up to date with the best of the world (methods, structure, tools,
containers, security, code standards) and easy for Claude to read.** Version numbers matter, but
Dependabot and Renovate already handle them: kiln does the rest. It picks the best tools and
methods, checks they work together, and moves every repo to the next release (the Ubuntu image
stays out of public texts: too abstract, decision 5 of 26 October). The goal: kiln becomes the
reference tool for this problem, measured by adoption (stars, installs), and never something
the next release of an agent makes useless (antoine, 26 October 2026): agent-neutral, scripted,
sourced.

### The problem

1. **The world moves faster than repos.** uv replaced pip, ruff replaced flake8, black and
   isort; containers went rootless, dependency cooldowns appeared in 2025, passkeys took over.
   Nobody tells a repo that a better method exists.
2. **Existing tools stop at versions** (Dependabot, Renovate) **or serve large companies** (AWS
   Transform, Moderne).
3. **Agent-written code speeds up debt.** 90 % of professional developers use an agent every
   week, and about 47 % of their code is written entirely by one (JetBrains, 2026); refactoring
   fell from 21 % of changed lines in 2022 to 3.8 % in 2026 (GitClear).
4. **Nobody has time to review everything.** Code output per developer doubled, reviewers only
   grew 1.5× (CMU and Stanford, 196,000 PRs); PRs with a real human comment fell from 39 % to
   21 %, median review time rose 441 % (Faros); 96 % of developers don't fully trust generated
   code but only 48 % always check it; teams *feel* 20 % faster while being 19 % slower
   (LinearB). Hence "nothing without proof".
5. **Small structures have nobody to keep watch**: an association, a 50-person company, a
   university course whose student team changes every year.
6. **Repos are not laid out for an agent to read.** Every badly split or badly named file is paid
   in tokens, re-reads and mistakes.

### The five pillars

1. **Methods and tools up to date**: a reference grid kept current and applied to the repo
   (tooling, supply chain, containers and operations, tests, application security,
   observability and delivery).
2. **Code standards**: naming, typing, sizes and the rest, enforced rather than advised, in three
   regimes (strict, ratchet, review); the reference repo's charter is the starting base.
3. **Readable by Claude**: a folder per feature, a file per idea (about 50 to 300 lines), names
   that serve as a table of contents, few levels of indirection, the repo map in `CLAUDE.md`,
   tools that read function by function (Serena, LSP). The small-files hypothesis is not proven
   yet (T-53).
4. **Slim down** (a lead): remove unused dependencies and code with a proof that behaviour does
   not change (T-138, T-139). Writing code costs almost nothing now; its mass is the problem.
   The true measure is the surface to review, not the line count; typing helps (the cheapest
   proof, and it removes defensive code): type first, compress after.
5. **Versions**: delegated to Dependabot or Renovate; kiln checks they are set, with a cooldown.

### For whom, and where it starts

- **First** small structures without a platform team: associations, companies of about
  50 people, startups, universities (students, teachers, labs), freelancers, and people who
  build with an agent without knowing how to code: they should code well without knowing it.
  They come to learn to run a project, or to bring an old repo up (`kiln adopt`). **Not at
  first** large companies: AWS and Moderne serve them.
- **Django and Nuxt first**, the reference repo's stacks, brought to the top of the grid; each
  stack counts alone (a Django repo with a React front still gets the Django profile). The
  reference repo is the training ground (its score at every release, T-134); the university repo
  and other ordinary repos are the test for repos kiln did not create, always on local copies.
- **The other templates are frozen** (T-133): generated and tested, no new grid work for them;
  scoring opens stack by stack after the launch (decision 1 of the
  [kiln score ideas](#-kiln-score-the-thesis)).

### The doctrine

There is one way to code, run a repo and run a project: the one kiln holds to be the best
possible, and it is followed. The reference repo's charter is the starting base; after that, the
reference is what comes out in the world, sorted by these principles. gofmt ("nobody's favourite
style, everyone's favourite tool"), Black, Prettier and Rails won this way; create-react-app,
frozen then abandoned in 2025, shows what happens when the one way stops moving.

1. **One way per profile.** For each stack and size of structure, kiln picks one way and holds
   it: an association does not need a large company's SLOs. Where the community is split at
   equal quality, the other way is accepted, never scored down (podman recommended, Docker
   accepted: decision 17 of 26 October). kiln's way is the world's best, not its author's.
2. **The best, not the newest.** A practice enters only once mature (maintained, adopted,
   compatible with the rest of the stack), through four levels: assess, trial, adopt, hold.
3. **Every rule has its why, source and date.** Sources weigh in this order: official docs and
   maintainers' release notes; security advisories (OWASP, OpenSSF, CVE); measured studies;
   adoption data; blogs.
4. **Every rule sits on two axes**: its theme and its scope (universal, language, framework,
   tool, business domain, project). A universal rule may take a project setting: "store dates in
   UTC" is universal, "Europe/Paris" is the project's.
5. **The script first, Claude next.** Whatever a program can check or fix, a program does: exact,
   reproducible, no tokens. Claude gets only what needs judgment, with the exact place and the
   rule; it never walks the repo looking for problems.
6. **Claude invents, the script repeats.** A fix Claude makes twice the same way becomes a rule
   or a converter (T-137): paid once per rule, not once per repo.
7. **A vague rule is worse than none.** A rule that flags wrongly costs tokens and trust; it goes
   strict only once its false positives are under control.
8. **Nothing without proof**: tests, types and CI green, measured before and after.
9. **Explicit exceptions, a gradual path**: a waiver is dated and justified (`kiln waive`); an
   existing repo converges by ratchets, without breaking everything at once.
10. **Readable by Claude** (pillar 3).
11. **The fastest, at equal precision.** A slow check stops being run: the fastest tools among
    those precise and mature enough, only what changed rechecked (cache, changed files,
    parallelism), our own rules declarative for a fast engine such as ast-grep; Rust of our own
    only where a measurement shows our code is the slow part (T-144).
12. **A living choice is never a finding.** The one way governs how a stack is run, never which
    living stack a repo picked: a Django repo is held to Django at its best, never told to become
    FastAPI, since each fits its own job (`kiln new` picks one per job: Django for a full app,
    FastAPI for an API alone). A choice becomes a finding only on dated, sourced facts: its line
    is past its end (`SUPPORTED-FRAMEWORKS`), its maintainers deprecated it and name a successor
    (the `hold` rules), or it is abandoned with open advisories (`ABANDONED-DEPENDENCIES`). kiln
    then names the successor its maintainers name, never one of its own taste, and splits the
    move into steps the score proves, never a rewrite in one go (T-225; antoine's question of
    26 October 2026).
13. **Breadth costs data, not weight.** `kiln new` keeps few complete stacks (decision 1); the
    grid reads every stack, and a stack is mostly facts for the rules that span stacks (about
    four planned rules in five on 26 October 2026; 5 of the grid's 138 rules belong to a
    framework), its own rules a thin layer, its mature tools (Brakeman, Sobelow, SpotBugs…) run
    rather than rewritten. A repo loads only its stacks' rules (T-214), and a rule nobody re-read
    for a year leaves the score (T-140): a pack nobody keeps goes quiet rather than wrong.
14. **No tool invented.** As many tools as possible that spend no tokens, the fastest, and
    existing ones: where a maintained open-source tool does the job, kiln runs it; kiln's own
    code is the glue, the standard and what nobody else does (antoine, 26 October 2026: "invent no
    tool, go find existing repos on GitHub"; T-359).

### How it works: the script finds, Claude judges

Not everything can be checked by a program (whether a name says what it holds, whether an
architecture fits the domain; Rice's theorem), and handing everything to Claude would cost a
fortune: reading the reference repo's Python once (48,616 lines outside tests) is about
500,000 tokens. So five steps, most of them free:
1. **Deterministic audit, no tokens** (`kiln score`): scripts, linters and public APIs measure the
   repo against the grid; a score per pillar and the list of gaps, each with its why, for whom
   and its effort.
2. **Mechanical fixes, no tokens** (`kiln fix`, `kiln update`'s conversions), on a branch.
3. **A roadmap for Claude, targeted tokens** (`kiln score --roadmap`, `/kiln:modernize`): only
   what needs judgment (split a 3,000-line file, rename with meaning, write tests, strict
   typing), each item with its place, rule and why. Most of an agent's tokens go into
   exploring; the roadmap removes that: Claude pays to think, not to search.
4. **Checked by the script** (`kiln score --rule`): a gap is closed only when it leaves the
   measure and tests, types and CI stay green.
5. **Continuously**: each release updates the grid and `kiln update` brings the repos to it,
   candidates first on the `internal` channel.

A repo kiln did not create gets `kiln adopt`, then a test net freezing today's behaviour before
any modernization.

**The circuit.** Updates go down through `kiln update`; gaps come up: where kiln runs, the score
notices what the grid does not know and the rules that get in the way wrongly, and Claude drafts
the report to kiln (T-38). Its rules: never without consent (the user sees exactly what leaves);
anonymised (no code, paths, internal names or secrets, only the gap's signature); one issue per
gap, not per user (a further report adds a voice), a PR only when the fix is obvious and local,
any outside PR through `/kiln:contribution`; a signal, not a decision (the doctrine decides, so
the grid cannot be poisoned by fake reports); the most frequent gaps become tickets first.

**Tests, the most for the fewest tokens**: generators without a model first (Schemathesis,
Hypothesis and CrossHair, snapshots, the Playwright recorder: T-136), holes measured by coverage
and mutation (mutmut, Stryker), Claude on the holes only, a test kept only if it passes five
times and kills a mutant or adds coverage, then ratchets (T-135). Meta's mutation-guided ACH saw
73 % of its generated tests accepted; CoverUp reaches 89 % line and branch coverage on its
benchmark. No tool lifts the last limit: a generated test checks what the code *does*, not what
it *should* do, which is why property tests and killed mutants are worth more than coverage.

### The market (October 2026)

| Player | What it does | What it lacks for our target |
|---|---|---|
| Dependabot, Renovate | Versions, optional cooldown | Neither methods nor standards |
| Copier, cruft (and Renovate's Copier manager) | Template updates | No grid, no method conversions |
| AWS Transform "Continuous Modernization" (preview since 17 June 2026) | Debt, end-of-life dependencies, outdated frameworks across thousands of repos | Large companies, AWS ecosystem |
| Moderne / OpenRewrite ($30M raised) | Recipe migrations, paid multi-repo | Large companies, Java first |
| GitHub Copilot app modernization | Java and .NET upgrades | Two ecosystems |
| Claude Code (`/doctor`, `/skill-doctor`, `claude-code-setup`) | Health of the Claude configuration | Not the rest of the repo |
| sp-repo-review (Scientific Python) | A checklist of scientific Python practices | Checks without applying |
| libyear, depwatch | Dependency lag | Versions only |
| deptry, FawltyDeps, knip, vulture | Unused dependencies and code | Detection only |
| ponytail | Tells agents to write less code | At writing time, not on existing code |
| ECC, Superpowers | Configuration packs for agents | Frozen at install |
| Thoughtworks Technology Radar | Opinions twice a year | Not executable |

**What is missing**: an open, free tool with a grid of methods and standards kept current,
applied with proof to small structures' repos, making them readable by Claude.

**What protects us** is where the big players cannot go, because of their own interests:
Anthropic (outside Claude Code, tedious stack by stack, and a script spends no tokens; only the
Claude configuration's health is its ground), Dependabot and Renovate (their job is raising
versions), AWS, Moderne and GitHub (they sell to large companies: an association never calls
their sales team), hosts (they host, they don't maintain code), funded startups (small
structures don't pay). A chore everyone suffers and nobody wants to own, as with Stripe and
payments; the demand is measured (the university repo). The real risk is a funded startup on the
same angle: speed and open source answer it, and a big player more often buys than rebuilds
(OpenAI bought Astral in March 2026, Anthropic Bun's team in December 2025).

**What makes a tool break out.** uv was no new idea (Poetry, pip-tools, pipx, pyenv, rye): it won
on execution (10 to 100× faster, one tool instead of several, `uv pip` adoptable without
migrating, ruff's credibility), and speed changed habits. The Claude Code projects that exploded
in 2026 share a one-line install, a number in the tagline and a pain felt in the first session.
For kiln: unify scattered tools (Dependabot, linters, templates, checkers like sp-repo-review)
and show a striking number, a before and after score. Distribution weighs as much as the idea
(ECC broke out after a hackathon win, Superpowers on its author's name): hence the launch (T-03).

**What Claude users need** (17 October 2026; JetBrains' survey the soundest source): Claude Code
is used at work by 39 % of professional developers; the needs, strongest first: checking agents'
code; controlling tokens (the category with the most stars: ponytail, cc-switch, caveman, rtk,
headroom); imposing a method (Superpowers, ECC, though ETH Zurich finds context files don't raise
success and cost 20 to 23 % more tokens); securing the agent chain (Clinejection, 1,184 malicious
skills on ClawHub, a quarter of MCP servers unpinned, mods not sandboxed); stability and the
freedom to pick one's agent (AGENTS.md in 60,000+ projects, SKILL.md read by 32+ tools, paths
that differ); understanding and remembering. The grid takes from it: pin MCP servers, avoid
broad permissions, keep context files short and hand-written, keep repos readable by any agent.
The background trend is harness engineering (OpenAI, February 2026): a harness improved from
measurements gains 7 points of success and saves 12 % of tokens.

### Decisions of 26 October 2026

antoine answered 220 questions offline (the file names people and private repos: it lives in
`kiln-private`). Below, what changes; where he wrote "decide", Claude settled it, with the
reason. T-342 to T-358 come from here; "Q" numbers are the file's.

**Launch (T-03).**
1. Hacker News restricts Show HN from new accounts since March 2026
   (https://news.ycombinator.com/showlim: "take some time to get to know the community",
   criteria vague on purpose), and antoine has no HN account and no Reddit karma (Q11, Q12).
   Proposed to him, his call (the date is his): 11 November stays for what needs no history
   (dev.to, Bluesky, X, Mastodon, LinkedIn, a mail to his university's students,
   awesome-claude-code); HN and Reddit on the first Wednesday his accounts are accepted, at the
   latest v0.6.0 (early December, a stronger story); both accounts opened at once and used for
   real, never about kiln. Moving everything to v1.0 (Q8) is advised against: seven months without
   strangers' repos to calibrate on, and the name left to whoever ships first.
2. The HN title stays antoine's (he dislikes "Dependabot for your methods"), `kiln score` first.
   LinkedIn: a post the day kiln takes off, written by Claude, posted by antoine. About ten
   people around antoine use kiln, four of them often: T-142 starts with them.
3. Claude never adds "written with Claude" on its own (Q129: "never"); where a platform asks
   (dev.to's AI disclosure tier) the true answer is given, or the post is not made. HN stays
   antoine's words only. The video is silent.

**Promise and README (T-30, T-33).**
4. `kiln score` first, then `adopt` and `new`, which stand on it (Q20, Q21, Q192): the trio is the
   promise. Draft tagline: "Make any repo production-grade: score it, raise it, keep it there".
   antoine wants the best README in the world.
5. The Ubuntu image goes from public texts (too abstract). The grid is called **the kiln
   standard** wherever a user reads it (T-346). The standard is the grid, not the score:
   `kiln score` keeps its name, beside `kiln check` and `kiln ci` (Q113, antoine is fine with
   the three).
6. The score: a number out of 100 in Lighthouse's bands (0-49 red, 50-89 orange, 90-100 green;
   the cap at 49 lands in red by construction), no letter; colourful in the terminal, a Markdown
   page of Mermaid charts on request (T-352).
7. English only for kiln's own docs: T-177 stands (Q27, "do as you like").
8. A sourced why for the README: output per developer doubled while reviewers grew 1.5× (CMU and
   Stanford, in the sources below); "right first costs fewer tokens than refactoring later" only
   with a measure (T-145), otherwise left out.
9. A logo, still and animated, and a mascot to discuss (T-347).

**The study (T-131, T-132).**
10. Calibration before conclusions: a standard that finds nothing well made is worthless
    (antoine, Q30). Repos known for their quality are scored before the launch; every point they
    lose is a gap their maintainers would recognize, with its source, or a defect fixed first.
11. Scores are reproducible by anyone (as with Scorecard or best-of-python): the article names the
    reference repos and gives the hundred as aggregates, never a list of the worst.
12. A vulnerability found is reported privately (the project's SECURITY.md, GitHub's private
    reporting), never as a public PR first; the credit in the published advisory is the
    publicity antoine wants (Q31). Other PRs: a few, by hand, where CONTRIBUTING welcomes them,
    never in bulk.
13. The university repo is never cited by kiln, not even as aggregates (Q34; one day kiln runs on
    it and a PR goes to its teacher). The association's site is never named (Q35).
14. T-53 before the launch, run once; T-145 matters.

**The standard and the score.**
15. The six decisions of 24 October stand, re-read; the cap at 49 too (SSL Labs' logic: a tracked
    `.env` is an incident, not a style point).
16. Not using an agent is not a fault (Q42, T-342).
17. One recommended way per profile, and an accepted other where the community is split at equal
    quality (Q40, Q41: podman recommended, Docker accepted). Every question kiln asks offers
    "I don't know: choose for me", the recommended answer.
18. Tools move from trial to adopt on Claude's call, with sources (Q43). More profiles (T-39):
    student project, teacher, startup, small company, freelance delivery, open-source project,
    personal project.
19. Telemetry: S05 ("no telemetry, ever") reversed by antoine (Q96): opt-in, anonymous,
    documented (T-348). Gap reports, issues and PRs reach him as a daily mail (T-349).

**kiln fix and kiln-bot (T-59, T-170).**
20. kiln-bot is a workflow each repo installs (free, no server); a hosted App later if kiln grows,
    the association's server lending a little meanwhile. It never breaks production: each commit
    proven (T-170), the PR a proposal the repo's CI judges.
21. `kiln fix --pr` allowed. A fix that turns the repo's tests red leaves the batch, kept on its own
    branch with its log and handed to Claude: never merged red, never dropped silently.

**kiln new and adopt (T-169, T-184, T-188).**
22. Two doors, quick or tailored; the long questionnaire (the machine profile) is asked once at
    install, and at `kiln new` only if never answered. Three concrete questions replace the
    sizes. The frozen templates stay offered, marked frozen with their score; FastAPI at the
    launch: "not yet, report it".

**Plan to 1.0.**
23. Numbering (Q58): antoine wants small patch numbers. antoine said yes the same day to a minor
    every ten releases or so, each a themed milestone holding its breaking changes, as uv and
    ruff do; the plan is renumbered by T-360.
24. The best on every stack (Q59, unchanged); someone antoine knows waits for GitLab; the
    compressor uses proven tools only (vulture, knip), Q62.

**Claude Code, agents, plugins.**
25. kiln's way is the world's best, not antoine's (Q67): the generated flow follows the evidence
    (T-358). Its tools too: token-free, the fastest, existing ones first (Q5, doctrine 14,
    T-359). His own habits (one session, no subagents, CI only at the release) stay his; the
    first two are not generated (checked).
26. Every agent, and none (Q22, Q72, T-357); Claude Code first at the launch, where the audience
    is.
27. The plugin directory lists one plugin, `kiln`; the stack plugins come with `kiln new` and
    `kiln adopt`. Serena stays opt-in (it is), context7 stays (current library docs serve "the most
    up to date"), rtk stays on. Pro plan only.

**Community and money.**
28. Free forever; Sponsors still to open (T-119); no maintainer rights to anyone; Discussions are
    enabled, their categories in T-58. Licence `MIT OR Apache-2.0` (T-345): antoine asked for
    Apache-2.0 as "the best"; the pair keeps Apache's patent grant and MIT's reach, as uv does;
    he said yes to it.
29. Contact: security through GitHub's private reporting (SECURITY.md has it); companies through
    antoine's GitHub and LinkedIn. A kiln page on the association's site is declined (it would
    name it): GitHub Pages, with the docs site after the launch. The site is static (docs, rule
    pages, the leaderboard drawn at build): Pages serves it from the repo, built by a workflow,
    with no other account; Vercel, antoine's first idea, only if a server part comes (T-348's
    collector).
30. antoine can take about 50 issues or PRs a day; each is answered in its own language.

**Way of working.**
31. The backlog is for Claude alone (Q82, Q214): condensed (T-163). It stays in `docs/backlog/`
    (ripgrep skips dot-folders by default; contributors and good first issues read it), with
    `ROADMAP.md` as the human view; launch texts, contacts and metrics go to `kiln-private`
    (T-350). The plan stays public (contributors, trust, building in public); antoine may still
    ask for it private (Q138).
32. Estimates are ceilings: antoine always goes faster (Q84).
33. CI only at the release stays (nothing slipped through, Q86), as complete and fast as possible
    (Q85, T-354).
34. annway stays off limits, its copy `annway-copie` may serve kiln (the Java pack, T-310); kiln
    trains on sweep and polytech-vision up to 100, in their own sessions (Q91, Q92).
35. Two habits of antoine's global instructions go to every repo (T-343). The repo's update is
    offered outside Claude Code too (T-355); strangers may follow the candidates (T-356). A
    session paused in seconds is found again at the next start (Q6, T-344). The session messages
    stay as they are (Q7): the logo only comes with an update on offer, as a message that costs
    no tokens.
36. The questions file: offered again before big milestones, not every time.

**Security, ideas, commands.**
37. What `kiln score` reads from GitHub's settings stays on the owner's machine; what leaves it
    (badge, report to kiln, a public CI summary) carries the score and rule IDs alone (T-158).
38. Score by URL (T-191); a leaderboard of the best only (T-353); the VS Code extension reopened
    (T-117, free on the Marketplace and Open VSX); Windows without WSL stays declined (T-94), but
    `kiln score` says what to do there instead of failing (T-189); a teacher is ready to try the
    teacher mode (T-87).
39. A quiet launch: same plan, measure, ask the testers, fix the first minute, launch again at the
    next milestone. A loud one: the digest, Discussions, a pinned issue of known problems.
40. `kiln check` (seconds, while coding), `kiln ci` (the whole CI on the machine, before a
    release) and `kiln score` (the repo against the standard), one line each in the README and
    `--help` (T-30): antoine did not know the first two apart (Q113). Merging two waits for
    telemetry (T-10). `kiln dev` must run any repo without being told (Q111, T-351).
41. Waivers keep their expiry (already by tiers); reminders weekly, security at once (T-45).
    Announcements: milestones only, on Bluesky, dev.to, X and Mastodon (T-118); no newsletter
    before 1,000 stars.

**Technical choices** left to "the best in the world" (Q145 to Q180): the standard settles them
rule by rule with dated sources. Held today: Django Ninja for new apps (DRF scored fairly); Celery
until Django 6's `django.tasks` has a mature production backend; Tailwind with tokens (Nuxt UI
weighed as a rule); pnpm; Vitest and Playwright; coverage as a ratchet with profile floors
(Google's 60, 75, 90 %); mutation tests at the release on critical code; strict types for new code,
a ratchet for old; 300 lines a file, strict when new, a ratchet when adopted; no `utils` nor
`helpers`; showcase files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY) for public repos only, none
generated today (with the community rules, CM); pre-commit kept; Conventional Commits; semver
after 1.0; `uvx` first; kiln's CLI in English until 1.0; Django with HTMX as a later frozen template.

### Risks and open questions

1. The giants hold the top of the market (AWS made the same promise in June, for large
   companies).
2. The grid is endless work: the starting scope keeps it tractable, the gap circuit feeds it.
3. Agents make applying a change easy for everyone: the value is in the choice and the proof.
4. "The best" depends on the context: profiles of structure (T-39).
5. Old repos without tests break when modernized blind: a test net first.
6. Upkeep tools earn few stars (deptry about 1,000): a striking number is needed (T-132, T-145).
7. The small-files hypothesis is not proven (T-53).
8. Gap reports raise privacy, noise and grid poisoning: the circuit's rules above.

### Sources

- Market and usage: [JetBrains, agent adoption 2026](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/) ·
  [GitClear (LeadDev)](https://leaddev.com/ai/code-maintainability-plummets-in-the-ai-coding-era) ·
  [the review bottleneck in numbers](https://www.flowverify.co/blog/ai-code-review-bottleneck-2026-data) ·
  [CMU and Stanford](https://www.matthewswong.com/en/blog/ai-code-review-bottleneck-cmu-stanford-silent-approvals/) ·
  [Pragmatic Engineer, AI tooling 2026](https://newsletter.pragmaticengineer.com/p/ai-tooling-2026) ·
  [Claude Code repos by stars](https://githublb.vercel.app/topic/claude-code) ·
  [agent configuration exposures](https://arxiv.org/abs/2609.07360) ·
  [mods not sandboxed](https://www.dsebastien.net/2026-10-04-claude-code-mods-claude-code-is-now-programmable-and-mods-arent-sandboxed/) ·
  [skill portability](https://codemyspec.com/blog/skill-portability) ·
  [harness engineering](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) ·
  [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850)
- Modernization: [AWS Transform](https://aws.amazon.com/blogs/migration-and-modernization/aws-transform-from-migration-to-continuous-modernization/) ·
  [Moderne raises $30M](https://refreshmiami.com/news/moderne-raises-30m-to-continue-driving-mass-scale-code-modernization/) ·
  [OpenRewrite and Moderne](https://moderne.ai/blog/overview-of-openrewrite-and-moderne) ·
  [Copilot modernization](https://theaieconomy.substack.com/p/github-copilot-modernizes-java-dotnet) ·
  [Renovate's Copier manager](https://docs.renovatebot.com/modules/manager/copier/) ·
  [Technology Radar](https://www.thoughtworks.com/radar) ·
  [`/doctor`](https://improveandrepeat.com/2026/10/keep-your-claude-code-configuration-healthy/) ·
  [`/skill-doctor`](https://www.implicator.ai/anthropic-claude-code-skill-doctor-context-audit/) ·
  [OpenAI acquires Astral](https://simonwillison.net/2026/Mar/19/openai-acquiring-astral)
- Readability: [Sonar's study](https://www.developersdigest.tech/blog/code-cleanliness-affects-ai-coding-agents) ·
  [ETH Zurich, AGENTS.md](https://iclr.cc/virtual/2026/10021142) ·
  [vertical slices and AI](https://jeremydmiller.com/2026/06/04/the-codebase-is-the-prompt-wolverine-vertical-slices-and-ai-assisted-development/) ·
  [an agent-friendly codebase](https://deska.dev/blog/agent-friendly-codebase)
- Slimming: [Meta's SCARF](https://engineering.fb.com/2023/10/24/developer-tools/automating-dead-code-cleanup/) ·
  [TRIM](https://arxiv.org/abs/2607.18161) ·
  ["Software Supply Chains are Dead"](https://arxiv.org/abs/2607.13021) ·
  [Lexo](https://arxiv.org/abs/2510.14522) ·
  [build once, maintain forever](https://expressionsofchange.org/build-once-maintain-forever)
- Tests: [CoverUp](https://dl.acm.org/doi/10.1145/3729398) ·
  [Meta, mutation-guided tests](https://arxiv.org/pdf/2501.12862) ·
  [`hypothesis write`](https://hypothesis.readthedocs.io/en/latest/ghostwriter.html) ·
  [a study of Hypothesis' tests](https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf) ·
  [hypothesis-crosshair](https://github.com/pschanely/hypothesis-crosshair) ·
  [Pynguin](https://arxiv.org/pdf/2007.14049) ·
  [Keploy](https://keploy.io/docs/concepts/what-is-keploy.md)
- Neighbouring tools: [sp-repo-review](https://pypi.org/project/sp-repo-review) ·
  [libyear](https://www.npmjs.com/package/libyear) ·
  [deptry](https://github.com/osprey-oss/deptry) ·
  [FawltyDeps](https://github.com/tweag/FawltyDeps) ·
  [ponytail](https://www.mindstudio.ai/blog/ponytail-ai-coding-minimalism-plugin)

---

## 💡 kiln score: the thesis

> Written on 24 October 2026 at antoine's request: "if you wanted to improve `kiln score` as much
> as possible, how would you do it? It should adapt to every environment in the world, detect
> absolutely everything, leave the user nothing to do, be ultra fast and ultra powerful. `kiln
> score` is the base of everything: through it `kiln adopt` knows what to improve in a repo, and
> `kiln new` aims to meet every rule of `kiln score`. Add and change whatever you want, but code
> nothing." Nothing was coded; each idea got its release on 25 October 2026, then became a box
> of a ticket the same day.

**1,070 ideas**: 433 on the engine and the product (sections A to V), and 637 on rules (31 themes
and packs): 520 new rules, 98 drafts or trials given a detector, 19 scored rules made sharper. They
are tickets now, in the sections above: T-186 to T-319, plus boxes added to the existing tickets
they extended (under "From the kiln score ideas of 24 October 2026"). Each box keeps its ID
(`- [ ] **A30** …`), so a search for `**A30**` finds it; what stays here is the thesis that
orders them and the reference tables to build from.

**How to read it.**
- The vision still decides ([the vision](#-vision)): one way per profile, the best
  and not the newest, the script first and Claude next, a rule that flags wrongly is worse than
  none, nothing without proof.
- An ID's letters name its section: one letter for the engine and the product, two for a rule
  theme or a pack (table below). A ticket's `Origin` lists the sections of its boxes.
- Rule boxes use a short notation after their description: the detector's rung (`L0` to `L7`,
  section E; `≈` when the detector is approximate and Claude confirms), `fix S` when a converter
  can close the gap or `fix J` when it takes judgment, then the radar level it would enter at.
- ⚠ marks an idea that brushes a declined ticket or a licence to check. The six choices these
  ideas raised are decided below.
- Locations quoted are hints, measured on `develop` at `7685fe6`.

| Engine and product | Rule themes and packs |
|---|---|
| A one model of the repo · B every ecosystem · C every forge, CI, host and machine · D every kind of repo, every profile · E the detection engine · F mature tools as detectors · G rule format v2 and authoring · H precision and recall · I scoring model v2 · J speed · K nothing to do · L outputs and integrations · M history, forge and registries · N deep checks, opt-in and sandboxed · O the roadmap for Claude · P one measure drives every command · Q a grid that stays current · R packs, local rules, standards · S trust, privacy and safety · T measuring kiln score itself · U what the grid doesn't know · V docs, teaching and reach | ST structure · CS code standards · AT API, contracts and typing · AR architecture · DM data and migrations · BG background tasks · CC concurrency · CA cache · EL errors and logs · AS application security · PD personal data · SU supply chain · TE tests · PE performance · FA front, accessibility and i18n · CO containers · OP operations · OB observability · CI CI/CD · GV Git and versions · DT docs and tracking · AI AI-assisted development · BD business domain · LI licensing · IN infrastructure as code · DS data science · DX developer experience · PK packaging and publishing · CM community · SP stack packs · FP framework packs |

### Part I · The thesis

#### What kiln score is for

Every other command serves the measure:
- `kiln new` makes a repo born at 100 on every rule that applies to it;
- `kiln adopt` lays what the score finds missing, then hands the rest to `kiln fix` and the roadmap;
- `kiln fix` closes what a script can, and `kiln score --rule` proves each one closed;
- `--roadmap` and `/kiln:modernize` hand Claude the places, never the search;
- `kiln update` keeps the score, kiln-bot posts it, the fleet view and the badge show it.

So the score's quality bounds the quality of everything kiln does. Six properties, each with a
measure, so that "better" is a number rather than a feeling:

| Property | What it means | Measured by | Target |
|---|---|---|---|
| Universal | Any repo: any language, structure, forge, CI, OS, size, human language | stacks named right per component on a 10,000-repo corpus | 99 % |
| Exhaustive | Every practice of the grid detected, every theme × ecosystem covered | adopt rules with a detector; tracked files no fact explains | 100 %; under 1 % |
| Effortless | No install, no config, no question, no token, no false positive to dismiss | steps from "never heard of kiln" to a score; manual corrections per 100 repos | one command; 0 |
| Fast | Instant on a laptop repo, seconds on a monorepo, milliseconds after an edit | a benchmark suite in CI | under 0.3 s cold on 1,000 files, 50 ms warm, 10 s on 1 M files |
| Powerful | Precise, explained, actionable, provable | precision per rule on a labelled corpus; gaps with a fix or a roadmap item | 99 % for strict rules; 100 % |
| Honest | Same commit and same grid give the same score; a change says whether the repo or the grid moved | `--verify`, the delta report | always |

#### Where it stands (measured on 24 October 2026)

- **138 rules**: 40 `adopt` (scored), 3 `trial`, 95 `assess` drafts. **97 rules have no detector.**
- **41 detectors**: 24 regex, 7 file, 10 Python checks. The `toml`, `json` and `yaml` kinds exist,
  no rule uses them.
- **10 facts** (`python`, `uv`, `django`, `javascript`, `typescript`, `pnpm`, `nuxt`, `vue`,
  `github-actions`, `containers`), repo-wide, without version, place or evidence. kiln itself is
  read as a Django + Nuxt repo because `template/` holds one: rules of stacks it doesn't have
  apply to it.
- **Regexes read raw text**: strings, comments and fixtures count. On kiln, `NOQA-CODES`,
  `TYPE-IGNORE-CODES` and `SQL-PARAMETERS` flag `tests/test_grid.py`, where the rules' own failing
  examples live.
- **A file that isn't UTF-8 reads as empty** (`Repo.text`): every regex rule passes it silently.
- **Three answers to "what is this repo"**: `grid/facts.py` (score, fix), `stack.py:detect_stack`
  (adopt, dev, check; markers in `backend/` and `frontend/`), `grid/fix.py:check_commands` (fix).
  They already disagree: `stack.py` knows a Vite + React front since today, the grid's facts don't.
- **Every rule weighs the same**: a committed `.env` costs as much as a missing README, and no
  finding caps the score.
- **GitHub Actions only** for CI rules; forge settings aren't read (T-158).
- **End-of-life data** for Python and Node only, bundled; `--online` refreshes those two.
- **Outputs**: terminal, JSON (schema 1), a static badge. No SARIF, HTML, delta or history.
- **Speed**: 0.56 s on kiln (666 files), about 1 s on the reference repo, no cache. Importing the
  score module takes 0.14 s, 0.06 s of it for `urllib`, used only by `--online`.
- **Python 3.14 required** (the code uses PEP 758's `except A, B:`): `uvx` brings it; `pipx run`
  or `pip` on an older Python fail.
- **Rule examples live in `tests/test_grid.py`** (`CASES`), not in the rule files: a pack author
  can't ship them.
- **What the grid doesn't know** is named: stacks (Go, Rust, Java…), 28 notable packages it doesn't
  cover (Celery, FastAPI, React…), rules waived again and again. Since v0.4.6 these lines can go
  to kiln as issues, with the user's yes (T-38, `gap_report.py`). The repo is then scored on
  universal rules only.

#### The twelve moves

1. **One model of the repo** (A). Components, not a repo: every folder with a manifest is a
   component with its ecosystem, frameworks and versions (from the lock), its role (backend,
   frontend, library, CLI, infra, docs, tests, template, fixture, vendored, generated, example),
   its tools and its evidence. Rules apply per component. Score, fix, adopt, dev, check and update
   read the same model: one answer to "what is this repo".
2. **Code, not text** (E). Detectors match syntax trees (ast-grep on tree-sitter, one parse per
   file shared by every rule), tell strings from code and tests from shipped code, and resolve
   what a regex can't: `ARG` defaults in a `FROM`, a tsconfig's `extends` chain, Django settings
   split across modules.
3. **A ladder of detectors, cheapest first** (E, F, M, N): L0 paths, L1 structured config, L2
   syntax, L3 cross-file, L4 external tools, L5 git history, L6 forge and registry APIs, L7 running
   the code. The default stays static and offline; `--online`, `--history` and `--deep` climb.
   Each finding says which rung found it.
4. **Mature tools as detectors** (F): ruff, zizmor, shellcheck, osv-scanner, gitleaks' patterns…
   mapped onto grid rules. kiln doesn't rewrite what a mature tool does better: it chooses,
   configures, maps and explains.
5. **Rules v2** (G): examples inside the rule file, applicability as an expression over the model,
   several ways to meet one practice, a severity, a message per place, the fix, the standards it
   maps to, its measured precision.
6. **Scoring v2** (I): equal weights kept, critical findings that cap the score, progress shown
   per place, the potential (after `kiln fix`, after the roadmap), a percentile against the
   study, and a delta that says whether the repo or the grid moved.
7. **Incremental and parallel** (J): a cache keyed by the blob SHAs git already knows, `--changed`,
   `--watch`, the Claude Code hook re-scoring only what was edited; Rust only where a profile
   points.
8. **Nothing to do** (K): `uvx kiln-cli score` or a single binary, any repo URL scored without
   cloning by hand, CI detected and fed (SARIF, annotations, job summary) without a flag, no
   config, no question, never a crash.
9. **The repo as it lives** (M): its history (secrets once committed, heavy blobs, hotspots), its
   forge settings, its registries, the advisories, the end-of-life calendar of every product.
10. **A grid that learns** (H, Q, U): a labelled corpus re-scored at every candidate, precision
    per rule as a release gate, files no fact explains turned into signals, sources watched.
11. **One measure drives everything** (P): `kiln new` proven at 100 by a matrix test, `kiln adopt`
    as score, lay, fix, roadmap; `kiln update` never lowers the score silently; the charter and
    the grid one engine.
12. **Explained like a senior engineer would** (L, O, V): each gap with its why, risk, effort, fix,
    proof, source and date; a page per rule; the roadmap as context packs Claude reads without
    exploring.

#### Decisions (24 October 2026)

antoine left the six choices this file raised to Claude ("decide yourself"). Each is recorded
with its reason; the ideas below follow them.

1. **Every stack scored; the templates stay frozen.** `kiln adopt` promises to bring any repo up,
   and a Go or Java repo scored on the 14 universal rules and those of its tools gets a hollow
   number. Generating keeps T-133's line (Django and Nuxt first, the other templates frozen;
   `rejected.md` now says "templates"); scoring opens stack by stack after the launch, in the
   order the corpus and T-38's gap reports show, each pack with its facts, rules, examples and
   measured precision.
2. **Equal weights stay; critical findings cap the score.** The number keeps meaning "the share
   of the rules that apply, met" (T-46): weights would be numbers to defend, and would shift
   every score as the grid grows. A short closed list of critical rules (a secret in the tree or
   its history, a tracked `.env` or Terraform state, the Docker socket mounted, a malicious
   package, a self-hosted runner open to public pull requests, card numbers on the server, a
   model provider's key in the front) caps the score at 49 and opens the report, the way SSL
   Labs caps a grade; the report shows both ("49, capped: `.env` tracked; 90 without it"). A rule
   is marked critical only once its precision reaches 99 % on the corpus. Severity orders the
   gaps; it never weighs the number.
3. **Three new themes, three folded.** `licensing` (a legal concern no theme holds, Scorecard's
   License check), `infrastructure` (Terraform and Kubernetes, apart from containers) and
   `data-science` (the first outside issues were data repos, and `MODEL-TRACED` sits badly in
   data-migrations) join `THEMES`, each with its first rule, in T-141. Developer experience goes
   to `structure` and `docs-tracking`, packaging to `supply-chain` and `ci-cd`, community to
   `docs-tracking`: a dozen presence checks each don't earn a line in `kiln grid`.
4. **The charter and the grid become one engine by v1.0.0, without breaking.** First one
   detector per practice: a grid rule linked to a charter rule runs the same check, and a test
   makes both agree on the rule's examples. Then, with the rule format v2 frozen at v1.0.0, the
   charter is the grid's rules in strict or ratchet regime, run at commit and in CI; the
   charter's rule IDs live on as aliases (`renames.py`). Two engines drift, and v1.0.0 should
   freeze one format, not two.
5. **No report families.** A third classification beside pillars and themes would confuse. The
   five pillars stay the report's frame (the vision's words, the README's images); under each,
   the report names its weakest themes ("methods 80 · weakest: app-security 55, tests 60").
6. **`CI-PRESENT` says what kiln does.** The template itself runs GitHub's CI only on
   `release/**`, or on the machine with `kiln ci` (its verdict kept as a git note): a detector
   reading triggers would fail every generated repo, and `kiln new` must meet the grid. The rule
   becomes "every change is checked before it ships": fast checks at each commit, the whole CI
   before each release; a CI on every pull request is the other accepted way. With profiles
   (T-39), company and enterprise ask for CI on every pull request, where integration breaks
   between people.

Ideas that brush a declined ticket carry ⚠ and its number (T-94 Windows without WSL, T-48
devcontainers, T-86 monorepos, T-71 `kiln mcp`): those stay declined until someone reopens them,
as antoine reopened T-117, the editor extension, on 26 October 2026.

#### Order of battle

Every idea is a box of a ticket listed under its release in [🚀 Releases](#-releases)
(25 October 2026, at antoine's request: everything a ticket, in its place). The plan in short:

| Releases | From these ideas | Why then |
|---|---|---|
| v0.4.10 to v0.5.0, before the launch | what their tickets already do (T-158's GitHub settings, T-159's containers run on a copy, kiln-bot, the study as the first corpus, kiln's repos at 100) and three small ones: the two silent passes (A30, A31) and the potential line (I07) | the launch's releases are full: a new idea there would push the gate |
| v0.5.4 to v0.5.16 | what strangers meet first (K), the false alarms (A, E, H), the badge (L), speed, updates, `kiln fix`, rules that test themselves (G), the outputs where people look (L), the exact rules and the AI rules (Part III), the roadmap as context packs (O), tests at the lowest cost | the launch brings repos nobody here has seen, and v0.6.0 needs the roadmap and the tests |
| v0.6.0 | O: the unattended run's scope guard, its labels and its costs | the milestone |
| v0.6.1 to v0.6.11 | slimming, the grid's weekly watch, the repo model (A), rule format v2 (E, G), the syntax engine, mature tools (F), the cache (J) | the engine every later rule stands on |
| v0.6.12 to v0.6.61 | the rule themes one by one, each after the rung it needs; between them the corpus and the critical cap (H, I), locks and registries, history and the forge (M), `--deep` (N), what the grid doesn't know (U), Python and JavaScript beyond Django and Nuxt (B, FP) | a rule enters once its detector's rung exists and the corpus can measure it |
| v0.6.62 to v0.7.3 | kinds and profiles (D), GitLab (C), coursework, the fleet (K, P), compliance views (R), the charter as the grid's rules (decision 4) | a university or an association network scores every repo |
| v0.7.4 to v0.8.0 | the other ecosystems, two releases a stack (B, SP), the long tail as data packs, the gate measured on the corpus | the format has to hold on every common stack before it freezes, in the order the corpus measures |
| v0.8.1 to v0.9.0 | every CI and machine (C, K), monorepos and huge trees (J), the bar's matrix run | and on every CI, machine and size |
| v0.9.1 | the score itself measured on every stack (T) | the last proof before the promise |
| v1.0.0 | packs (R, T-69), the published JSON schema, every executable thing pinned | the format is the public API; the long tail comes as packs |

Among the ecosystems, generic Python and JS/TS come first (v0.6.55 to v0.6.57); the order of the
others is a guess until the corpus measures it (B01).

### Appendices

#### A · Ecosystem matrix

What a pack reads and runs, ecosystem by ecosystem. "To verify" marks a cell to check before
the pack is built.

| Ecosystem | Manifests | Locks | Lint | Format | Types | Tests | Audit |
|---|---|---|---|---|---|---|---|
| Python | `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg`, `Pipfile` | `uv.lock`, `poetry.lock`, `pdm.lock`, `Pipfile.lock`, `pylock.toml` (PEP 751), hashed requirements | ruff | ruff format, Black | mypy, pyright, ty, pyrefly | pytest | pip-audit, osv-scanner |
| JavaScript, TypeScript | `package.json` | `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lock` | ESLint, oxlint, Biome | Prettier, Biome | tsc, vue-tsc | Vitest, Jest, Playwright | `pnpm audit`, `npm audit`, osv-scanner |
| Go | `go.mod` | `go.sum` | `go vet`, golangci-lint | gofmt, gofumpt | the compiler | `go test` | govulncheck |
| Rust | `Cargo.toml` | `Cargo.lock` | clippy | rustfmt | the compiler | `cargo test`, nextest | cargo-audit, cargo-deny |
| Java | `pom.xml`, `build.gradle(.kts)` | `gradle.lockfile` when locking is on; none for Maven | Error Prone, SpotBugs, PMD, Checkstyle | google-java-format, Spotless | the compiler, NullAway | JUnit 5 | OWASP Dependency-Check, osv-scanner |
| Kotlin | `build.gradle.kts` | `gradle.lockfile` | detekt, ktlint | ktlint, ktfmt | the compiler | JUnit 5, Kotest | osv-scanner |
| C# | `*.csproj`, `Directory.Packages.props` | `packages.lock.json` when enabled | .NET analyzers | `dotnet format` | nullable reference types | xUnit, NUnit, MSTest | NuGetAudit |
| PHP | `composer.json` | `composer.lock` | PHPStan, Psalm | PHP-CS-Fixer, Pint | PHPStan, Psalm | PHPUnit, Pest | `composer audit` |
| Ruby | `Gemfile`, `*.gemspec` | `Gemfile.lock` | RuboCop | RuboCop, Standard | Sorbet, Steep | RSpec, Minitest | bundler-audit |
| Swift | `Package.swift` | `Package.resolved` | SwiftLint | swift-format | the compiler | XCTest, Swift Testing | to verify |
| Dart, Flutter | `pubspec.yaml` | `pubspec.lock` | `dart analyze` | `dart format` | the analyzer | `flutter test` | osv-scanner (to verify) |
| Elixir | `mix.exs` | `mix.lock` | Credo | `mix format` | Dialyzer | ExUnit | mix_audit, `mix hex.audit` |
| C, C++ | `CMakeLists.txt`, `meson.build`, `vcpkg.json`, `conanfile.*` | `conan.lock`, vcpkg's baseline | clang-tidy | clang-format | the compiler | CTest, GoogleTest, Catch2 | to verify |
| R | `DESCRIPTION` | `renv.lock` | lintr | styler | none | testthat | to verify |
| Shell | none | none | shellcheck | shfmt | none | bats | none |
| Terraform, OpenTofu | `*.tf` | `.terraform.lock.hcl` | tflint | `fmt` | `validate` | `terraform test` | checkov, Trivy |
| Containers | `Dockerfile`, `Containerfile`, compose files | digests | hadolint, BuildKit's checks | none | none | container-structure-test | Trivy, Grype |
| Helm | `Chart.yaml` | `Chart.lock` | `helm lint`, kube-linter | none | `values.schema.json` | helm-unittest | checkov, Trivy |

#### B · CI matrix

Where each CI keeps its files, how a step is pinned, and where outside text gets into a script.

| CI | Files | Pinning | Untrusted text |
|---|---|---|---|
| GitHub Actions | `.github/workflows/*.yml`, `action.yml` | `uses: owner/repo@<40-hex SHA>`, images by digest | `${{ github.event.* }}` titles, bodies and branch names, `github.head_ref`, expanded into `run:` |
| Forgejo, Gitea Actions | `.forgejo/workflows/`, `.gitea/workflows/` | as GitHub's (`uses:` may be a full URL) | as GitHub's |
| GitLab CI | `.gitlab-ci.yml`, its `include:` files, CI/CD components | `include:` of a project at a commit, components at a version or SHA, images by digest | `$CI_COMMIT_MESSAGE` or `$CI_MERGE_REQUEST_TITLE` passed to `eval` or a generated script; `$[[ inputs ]]` interpolation (to verify) |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` | pipes at a version, images by digest | to verify |
| Azure Pipelines | `azure-pipelines.yml`, templates | tasks by major version only (`Task@2`), templates by `ref` | `$(…)` macros expanded before the shell runs (to verify) |
| CircleCI | `.circleci/config.yml` | orbs `ns/orb@x.y.z`, images by digest | `<< pipeline.git.branch >>` parameters expanded into commands (to verify) |
| Jenkins | `Jenkinsfile` | `@Library('lib@<sha>')` | Groovy interpolation of parameters and branch names inside `sh "…"` |
| Woodpecker | `.woodpecker.yml`, `.woodpecker/*.yaml` | plugin images by digest | to verify |
| Buildkite | `.buildkite/pipeline.yml` | plugins at a version or a commit | to verify |
| Google Cloud Build | `cloudbuild.yaml` | builder images by digest | substitutions such as `$BRANCH_NAME` (to verify) |
| AWS CodeBuild | `buildspec.yml` | images by digest | to verify |
| Tekton | `Task` and `Pipeline` manifests | bundles and images by digest | params expanded into `script` (to verify) |

#### C · OpenSSF Scorecard and the grid

Scorecard grades the same things from outside; kiln would answer each check, or say why not.
T-90 asks kiln to pass Scorecard itself.

| Scorecard check | Grid rule today | From this file |
|---|---|---|
| Binary-Artifacts | none | `NO-BINARY-ARTIFACTS` (SU) |
| Branch-Protection | none | `NO-FORCE-PUSH-ON-MAIN`, `REQUIRED-CHECKS` (L6, T-158) |
| CI-Tests | `TESTS-IN-CI` | pull requests' checks read from the forge (L6) |
| CII-Best-Practices | none | `OPENSSF-BADGE` (CM) |
| Code-Review | none | `NO-COMMIT-ON-INTEGRATION` from history, reviews read from the forge (L6) |
| Contributors | none | none: not a practice a repo chooses |
| Dangerous-Workflow | `WORKFLOW-INJECTION`, `PULL-REQUEST-TARGET` | zizmor's audits (F) |
| Dependency-Update-Tool | `DEPENDENCY-UPDATES` | every manifest folder covered |
| Fuzzing | `API-FUZZING` (draft) | `PROPERTY-TESTS`, `FUZZING` (SP) |
| License | none | `LICENSE-FILE`, `LICENSE-DECLARED` (LI) |
| Maintained | none | `MAINTAINED` (CM) |
| Packaging | none | `RELEASE-WORKFLOW`, `TRUSTED-PUBLISHING` (PK) |
| Pinned-Dependencies | `PINNED-ACTIONS`, `IMAGES-BY-DIGEST`, `LOCKED-DEPENDENCIES` | `PINNED-TOOLS`, `NO-CURL-PIPE-SHELL`, `FROZEN-INSTALL-IN-CI` |
| SAST | none | `SAST-IN-CI` (AS) |
| SBOM | `SBOM` (draft) | its detector |
| Security-Policy | none | `SECURITY-POLICY` (CM) |
| Signed-Releases | none | `ATTESTATIONS`, `IMAGES-SIGNED`, `PROVENANCE` |
| Token-Permissions | `WORKFLOW-PERMISSIONS` | `write-all` and job-level writes |
| Vulnerabilities | `VULNERABILITY-AUDIT` (an audit step exists) | `KNOWN-VULNERABILITIES` (the locked versions themselves) |
| Webhooks | none | the forge's webhooks with a secret (L6, T-158) |

#### D · Data to bundle or read

Each source with its licence where it is sure; "to check" before anything is bundled.

| Source | What it gives | Licence | How kiln would use it |
|---|---|---|---|
| GitHub Linguist | languages, extensions, vendored and generated patterns | MIT | bundled, refreshed each release |
| SchemaStore | config file names mapped to tools, their JSON schemas | Apache-2.0 | a bundled subset |
| github/gitignore | ignore patterns per ecosystem | CC0-1.0 | bundled |
| endoflife.date | release cycles and end dates of runtimes, frameworks, images and OSes | MIT | a bundled snapshot, `--online` refreshes it |
| OSV.dev | advisories and malicious packages (`MAL-`) per ecosystem | per source: to check | `--online` batch queries, a cached slice offline |
| gitleaks | secret patterns | MIT | patterns adapted, attributed |
| retire.js | signatures of vulnerable front-end libraries | Apache-2.0 | bundled |
| OpenSSF Scorecard | checks and their documentation | Apache-2.0 | the mapping of appendix C, no code |
| zizmor | GitHub Actions audits | MIT | run as a tool (F) |
| Renovate | which files of which manager hold dependencies | AGPL-3.0 | facts only, no code copied |
| OWASP Cheat Sheet Series | the why of the security rules | CC BY-SA 4.0 | cited as sources, quoted with attribution |
| SPDX License List | licence identifiers and texts | to check | identifiers bundled |
| Registries' download counts | the most used packages, to grow `NOTABLE_PACKAGES` | each API's terms: to check | `--online`, cached |
| Chrome UX Report | field Core Web Vitals | API terms: to check | `--online` |
