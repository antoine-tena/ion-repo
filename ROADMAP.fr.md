# Feuille de route

[English](ROADMAP.md)

Où va kiln, et dans quel ordre. Cette page est tirée [du backlog](docs/backlog/backlog.md#-releases),
où chaque ticket ouvert a sa version (les 1 070
[idées de kiln score](docs/backlog/backlog.md#-kiln-score-the-thesis) comprises, devenues des
tickets), et elle
est redessinée à chaque changement du plan. Les numéros sont prévus, pas promis : une version est
arrêtée dès que sa candidate est taguée. Ce qui est déjà sorti est dans le [journal](CHANGELOG.md).

## Comment kiln sort ses versions

- Une version tous les deux jours. Chacune tourne d'abord en candidate sur les repos de kiln :
  24 heures quand elle apporte du neuf, 2 heures quand elle ne fait que corriger, aucune attente
  pour une faille de sécurité.
- En `0.x`, chaque version monte le correctif, changements cassants compris : ils ouvrent la note
  de version, et `kiln update` les convertit dans votre repo. La mineure ne monte qu'à une étape,
  dans la version qui l'atteint : le travail qui y mène sort sous la mineure d'avant, si bien que
  les stacks de la v0.8.0 arrivent en v0.7.x. Le semver strict commence à la 1.0.
- Un seul mainteneur écrit kiln avec Claude Code, environ 25 heures de session par semaine. Les
  dates ci-dessous découlent du plan à ce rythme : des estimations, pas des échéances, et chaque
  version que le plan ne prévoit pas les repousse de deux jours.

## Étapes

| Étape | Ce que ça change pour vous | Prévue |
|---|---|---|
| v0.5.0 | N'importe quel repo Django ou Nuxt, créé par kiln ou non, noté face à la grille en quelques secondes, puis mis à niveau par script partout où un script le peut. Lancement public le mercredi 11 novembre 2026, si la v0.5.0 tient sa barre ; sinon une semaine plus tard. | novembre 2026 |
| v0.6.0 | Claude Code comble seul les écarts qu'un script laisse, chacun prouvé par la note. | décembre 2026 |
| v0.7.0 | Tous les repos d'une organisation (une université, un réseau d'associations, une entreprise de 50 personnes) notés sans les cloner, leurs écarts classés d'un repo à l'autre. | printemps 2027 |
| v0.8.0 | Chaque stack courante notée et corrigée par script : Java et Kotlin, C# et .NET, PHP, C et C++, Go, Rust, Ruby, applications mobiles, jeux, R et Elixir, chacune avec ses frameworks les plus utilisés. | printemps 2027 |
| v0.9.0 | N'importe quelle CI, n'importe quelle machine, n'importe quelle taille : les autres systèmes de CI, ARM, les réseaux coupés d'internet, les monorepos et le million de fichiers. | mi-2027 |
| v1.0.0 | La promesse de stabilité. Le format des règles se fige une fois qu'il a tenu sur les stacks qui font environ 95 % des repos, et chacun peut publier des paquets de règles pour le reste. Semver strict ensuite. | mi-2027 |

Toutes les stacks viennent avant la 1.0, exprès : un format éprouvé sur deux frameworks casserait
à la première stack qui diffère, et la 1.0 promet qu'il ne cassera pas.

## Version par version

Chaque version dans l'ordre où elle sort : ce qu'elle apporte, pourquoi son travail va ensemble,
et ce qu'elle prend du backlog (ses tickets). Le détail est repris tel quel du backlog, tenu en
anglais. Il manque quelque chose, ou vous le voulez plus tôt ?
[Ouvrez une issue](https://github.com/antoine-tena/kiln/issues) : le plan bouge avec ce qu'on lui demande.

<!-- roadmap:start: drawn from docs/backlog/backlog.md by scripts/roadmap.py -->

### v0.4.x · 2 releases

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v0.4.10 | Every gap seen, wherever the code lives | Candidate Tue 27 Oct. The score and the fixes reach what they miss today: GitHub settings, code at the root as well as in `backend/` and `frontend/`, compose services, loose requirements, files read as empty. | fixes as they come |
| v0.4.11 | Never lets it rot, kiln first | Candidate Thu 29 Oct. kiln-bot runs kiln's workflows with write access in other people's repos: each commit it brings is proven first, and kiln's own workflows pass zizmor and carry provenance before anyone runs them. kiln-bot on a test repo is a box of the launch gate (T-03). | 1 ticket |

### v0.5.x · 18 releases

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v0.5.0 | Public launch: the proof and the page | Candidate Sun 1 Nov, promoted Tue 3 Nov. Milestone decided by antoine (16 October 2026), its content defined on 17 October: the version the launch waits for (T-03). The proof (two real repos, a hundred public ones, kiln's own repos at 100) and the page that shows it, the potential line as its demo. | 12 tickets |
| v0.5.1 | Launch week: the rehearsal, and the bugs already known | Candidate Tue 3 Nov. Fixes only from here to the launch; the week absorbs up to three slipped releases. | 6 tickets |
| v0.5.2 | Launch week: what the rehearsal found | Candidate Thu 5 Nov: the fixes of T-142, nothing else. | fixes as they come |
| v0.5.3 | Launch day | Candidate Sat 7 Nov, promoted on Mon 9 Nov by the next candidate: the version strangers install. Gate checked on Mon 9 Nov at 20:00; nothing is promoted on launch day. | 1 ticket |
| v0.5.4 | The first week with strangers | Candidate Mon 9 Nov, promoted after the launch. What the launch brings in (issues, reports, the first gap reports of T-38) comes first; these give way to it. From here each milestone is announced (T-118). | 10 tickets |
| v0.5.5 | A score you can trust: the false alarms of real repos, gone | Strangers' repos hold fixtures, vendored and generated code, templates, READMEs in other languages: each class of false alarm is handled once, in the engine, and stays fixed by a test; the reference repo's score in every note says when the grid moved. | 2 tickets |
| v0.5.6 | Show your score | The image that travels by itself, and anyone's repo scored from its URL: the launch's visitors become its messengers. | 4 tickets |
| v0.5.7 | Claude pays less per session | Context length is the cost (measured on 22 October): skills that run one kiln command, a ladder before writing code, context files kept under a budget, the score shown without Claude asking for it. | 3 tickets |
| v0.5.8 | kiln never makes you wait | The same features, sooner: what was measured slow on 24 October (the suite every release waits for, the session start, `kiln status`, each Bash call, the install), and the score's own start, benchmarked in CI. | 7 tickets |
| v0.5.9 | Updates you take without reading them | Asked at your pace, applied in one step, proven on real upgrade paths, the score before and after shown, Claude told what changed in its rules. | 6 tickets |
| v0.5.10 | `kiln fix`: more gaps closed, faster, from scripts | The code's own rules get converters, the checks run once with a bisection on red, the options kiln-bot and the skills need; a fresh `kiln new` repo leaves `kiln fix` nothing to do. | 4 tickets |
| v0.5.11 | Rules that test themselves | Before the grid grows by hundreds of rules: each rule carries its examples, its rung and its message per place, and `kiln grid new`, `test`, `try` and `lint` make a rule in minutes. | 1 ticket |
| v0.5.12 | Findings where people look | With rules that test themselves (v0.5.11) to build on: in the pull request, the CI's summary and GitHub's code scanning, written without a flag; repo-local rules in the grid's format. | 3 tickets |
| v0.5.13 | The grid grows: the exact rules first, three new themes | T-141 opens here, its other boxes being the theme releases below: the rules a detector decides exactly today, the first rule of `licensing`, `infrastructure` and `data-science`, and the template held to every new rule by its own test. | 4 tickets |
| v0.5.14 | Repos safe to hand to an agent | What Claude Code users need first (17 October): narrow permissions, pinned MCP servers, no secret an agent can read, model calls with limits; plugins and MCP servers scored as a kind of their own. | 3 tickets |
| v0.5.15 | The roadmap Claude reads without exploring | The input of v0.6.0: each gap a context pack with its recipe and its proof, ordered by points per token, cut into batches that fit a session. | 1 ticket |
| v0.5.16 | Tests at the lowest token cost | The other half of v0.6.0: generators that cost no tokens in the template, coverage and surviving mutants measured by script, Claude on the holes only. | 3 tickets |
| v0.5.17 | Strangers' repos run as they are | `kiln dev` brings up any adopted repo without a question, on podman or Docker, whichever the machine has. | 2 tickets |

<details><summary><b>v0.6.x</b> · 66 releases</summary>

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v0.6.0 | Claude closes the gaps alone | Milestone decided by antoine (16 October 2026: Claude does the work in the repo), its content re-scoped to the vision: the roadmap worked unattended within a budget, each pull request kept to its places, the cost of a judgment gap measured, a fix made twice turned into a converter. | 3 tickets |
| v0.6.1 | Less code to carry | The vision's fourth pillar, measured before anything is built: the compressor's dry run, removals proven by types, tests and behaviour, the slimming rules promoted once precise. | 4 tickets |
| v0.6.2 | Claude in the team's flow | A red CI made green on the machine, the roadmap as issues and good first issues, a summary a human reads in their language, a file other agents can read too. | 4 tickets |
| v0.6.3 | The grid kept current: its sources watched | Every week the sources are read, the data bundle refreshed, the rules whose sources moved flagged; each release note carries the grid's diff. | 2 tickets |
| v0.6.4 | `kiln new` fits the person | The quick door and the tailored one share the recap and the machine profile: built together. ⚠ breaking: the size question becomes three questions and `--all-questions` gives way to the tailored mode, both converted by `kiln update`. | 2 tickets |
| v0.6.5 | For more people | Tutorials that keep bringing visitors, the roadmap as a GitHub Project, a page per rule where searches land, the study every quarter, a folder or a zip scored as well as a repo. | 3 tickets |
| v0.6.6 | One answer to "what is this repo" | Score, fix, adopt, dev and check read one model: components with their roles, so a Django rule never reads `frontend/` and one helper script doesn't make a repo Python. | 1 ticket |
| v0.6.7 | Rules per component: versions, tools, evidence | Each fact says where it comes from and how sure it is; rules can say `django >= 4.2` or "your formatter"; a component is scored alone. | 1 ticket |
| v0.6.8 | Rules that say what they mean | Applicability as an expression, several ways to meet one practice, conditions across files, evidence for passes, an honest `unknown`. | 1 ticket |
| v0.6.9 | Code, not text: the syntax engine | Detectors match syntax trees (ast-grep); Django settings, `nuxt.config`, Dockerfiles and tsconfig chains are read as they resolve; the false negatives found on 24 October close. | 1 ticket |
| v0.6.10 | Mature tools as detectors | ruff, shellcheck and their kin mapped onto grid rules, pinned and cached, never downloaded without asking; the faster checkers measured against the ones they would replace. | 2 tickets |
| v0.6.11 | Instant the second time | One listing from git, one matcher for every rule, a cache keyed by blob SHA: a warm run recomputes nothing unchanged, in under 50 ms. | 1 ticket |
| v0.6.12 | Code standards a linter proves | With ruff mapped (v0.6.10), the Python standards it already decides become rules at once, its safe fixes their converters; shell scripts and encodings come with them. | 2 tickets |
| v0.6.13 | Secrets and the settings that leak | The secrets themselves, checksum-verified, and the production settings read as they resolve (v0.6.9): cookies, headers, HTTPS, debug flags, keys in the front. | 2 tickets |
| v0.6.14 | Precision measured on a thousand repos | A labelled corpus re-scored at every candidate, precision and recall per rule as a release gate, new detectors in shadow first; the radar moves on that evidence only. | 2 tickets |
| v0.6.15 | A number that can't lie | Severity orders the gaps, critical findings cap the score at 49 once they are 99 % precise (decision 2), a maybe is never punished, an empty file earns nothing, a report can be verified. | 1 ticket |
| v0.6.16 | Locks and installs you can trust | Every lockfile parsed, one practice checked in every ecosystem, every manifest folder covered by the update bot, installs from the lock in CI and in images. | 1 ticket |
| v0.6.17 | Nothing runs that you didn't pin | Install scripts off, one index, tools and hooks pinned, downloads checked, no token in a committed `.npmrc`, no binary in the tree, an SBOM per release. | 2 tickets |
| v0.6.18 | What is on its way out, and when it breaks | The calendar of what ends (runtimes, frameworks, runners, model IDs), the `hold` rules that detect what is leaving, the converters that move it. | 1 ticket |
| v0.6.19 | Containers built right | Dockerfiles read stage by stage (v0.6.9): the final user, multi-stage builds, secrets at build time, exec form, images by tag and digest everywhere. | 2 tickets |
| v0.6.20 | Compose files for a small server | What a VPS running compose needs: no engine socket, databases on localhost, logs rotated, limits and restarts, secrets out of the file, images scanned and signed. | 2 tickets |
| v0.6.21 | One CI model, any workflow | Jobs, steps, triggers and permissions extracted once; `make test` resolved into what it runs; zizmor and actionlint as detectors; the scored CI rules read from that model. | 2 tickets |
| v0.6.22 | Fast and safe pipelines | Concurrency, caches and retention, supported runners, secrets through `env:`, reusable workflows pinned, provenance on what ships, the same CI on a laptop. | 2 tickets |
| v0.6.23 | Tests that prove something | Tests per component that assert, run shuffled and in parallel, without network or sleep, coverage that only rises; a front with no backend gets its smoke test. | 3 tickets |
| v0.6.24 | Progress, not perfection: no new finding | The score of a change, a comparison with any ref, gates on new findings only, scores kept in git notes and drawn as a curve. | 1 ticket |
| v0.6.25 | One funnel for every repo, new or old | `kiln adopt` as score, lay, fix, roadmap, its result shown before it runs; baselines for the gradual path; the template a repo started from recognised; `kiln new` as the same funnel run on an empty folder. | 1 ticket |
| v0.6.26 | Only what changed, right after each edit | Tests and score rechecked on the changed files only, on save and in Claude Code's edit hook, in milliseconds. | 2 tickets |
| v0.6.27 | The score explained like a senior engineer would | The denominator, the weakest themes, the effort to 100 in session hours, a verdict in plain words, `--explain` with this repo's numbers. | 1 ticket |
| v0.6.28 | A report you can share | Every format a CI or a tool reads, a one-file HTML report, links to each rule's page and to the line on the forge, nothing personal left in it. | 1 ticket |
| v0.6.29 | Code that can be attacked | Injection, unsafe deserialization, weak crypto, open redirects, SSRF and the rest, with taint followed inside a function. | 2 tickets |
| v0.6.30 | Sizes and names, measured in any language | A metrics pass for every language feeds the size and complexity ratchets; names, cases and misspellings judged from symbol tables. | 2 tickets |
| v0.6.31 | Code standards from the syntax tree | What a regex can't tell: modern Vue, explicit imports, floating promises, debug prints, TODOs without a ticket, barrel files, with oxlint or Biome where they decide. | 2 tickets |
| v0.6.32 | API, contracts and typing | The schema committed and checked for breaking changes, front types generated from it, typing read through its inheritance and counted as ratchets. | 3 tickets |
| v0.6.33 | Architecture you can see | An import graph per language: cycles, layers, sealed domains, god modules, files that always change together. | 3 tickets |
| v0.6.34 | Data and migrations | Migrations reversible, safe on a live table, linted in CI, run on the production engine; dumps out of git; invariants held by the database. | 2 tickets |
| v0.6.35 | Background tasks and concurrency | Tasks that retry, time out, take IDs and run outside the request; increments and locks that survive two requests at once; Celery's settings made exact. | 3 tickets |
| v0.6.36 | Fast back ends: caches and queries | Real cache backends with timeouts and invalidation, N+1 queries and missing indexes found, latency budgets kept in the repo. | 2 tickets |
| v0.6.37 | Errors and logs you can follow | Structured logs to stdout, no secret in them and no stack trace shown, errors tracked with their release, a request ID and traces from the front to the back. | 2 tickets |
| v0.6.38 | An accessible front, in every language | Labels, alt texts, focus, contrast and motion checked in templates and by axe; the European Accessibility Act's profile; every locale complete. | 2 tickets |
| v0.6.39 | A fast, SSR-safe front | Hydration and SSR safety, keys and loading states handled, bundle and image budgets, scripts and fonts that don't block, SEO basics. | 2 tickets |
| v0.6.40 | Deploys you can undo | Services and hosts read from every deploy config; health probes that exist, config that fails fast, OIDC instead of keys, rollbacks, certificates renewed. | 2 tickets |
| v0.6.41 | Production watched, backups restored | A runbook whose commands exist, backups with a restore job, uptime and cron checks, alerts on symptoms, metrics kept private. | 2 tickets |
| v0.6.42 | A tree anyone can find their way in | No build output or artefact committed, a complete `.gitignore`, one config per tool, paths every OS accepts, small folders. | 2 tickets |
| v0.6.43 | Docs that tell the truth | Every path, command and link that the README and CLAUDE.md name exists; the map lists every folder; docs that name what is gone are found. | 2 tickets |
| v0.6.44 | Set up in one command | One bootstrap command, tasks named in one place, fast commit hooks, tool versions pinned as in CI, editor settings shared. | 1 ticket |
| v0.6.45 | Personal data, the GDPR way | Personal fields found in the models and kept out of logs, URLs, fixtures and model calls; the inventory and the subprocessors written by script; retention and deletion. | 2 tickets |
| v0.6.46 | Money, time, accounts and mail | Amounts in the smallest unit with their currency, dates in UTC, webhooks verified, cards never on the server, passkeys and rate limits, bulk mail that can be unsubscribed from. | 2 tickets |
| v0.6.47 | History: what every clone carries | Secrets once committed, heavy blobs, locks drifting from their manifests, each blob read once and cached; hotspots open the roadmap. | 1 ticket |
| v0.6.48 | History: how the repo is worked | Commit sizes and messages, merges and branch names, releases and their notes, fixes that come with a test, all read from history. | 2 tickets |
| v0.6.49 | The forge's settings, read | Through the `gh` already logged in: token permissions, secrets' ages, environments, required checks, alerts left open, update pull requests ignored. | 2 tickets |
| v0.6.50 | What you depend on, checked at the registry | Real vulnerabilities in the locked versions, malicious and abandoned packages, typosquats, the provenance of what is published, dependencies' licences, a health card for a new one. | 1 ticket |
| v0.6.51 | `--deep`: the repo's own checks, in a sandbox | Opt-in, in a throwaway copy with the network off: the install from the lock, the tests (flaky, order, network, clock), Django's deploy check, type checkers at their strictest, a clean clone. | 1 ticket |
| v0.6.52 | `--deep`: the app built and probed | Images built and scanned, migrations applied and reversed, the API fuzzed, the front rendered for axe and Lighthouse, the app served and probed, a deployed URL on request. | 1 ticket |
| v0.6.53 | What the grid doesn't know, shown | Every tracked file claimed by a fact or listed, fingerprints as data from Linguist and SchemaStore, the gap reports carrying them, corrections counted as signals. | 1 ticket |
| v0.6.54 | Never a crash, whatever the repo | Static by default, hardened parsers, linear-time regexes, fuzzed trees, symlinks, untracked and ignored files handled; zero crashes on the corpus at each candidate. | 1 ticket |
| v0.6.55 | Python beyond Django | FastAPI, Flask, SQLAlchemy and every packaging tool read; a new stack's rules count only once ten corpus repos of it were checked. | 1 ticket |
| v0.6.56 | JavaScript beyond Nuxt: the fronts | Every JS framework and package manager read; Next.js, React, React Router, Angular, Vue without Nuxt, Svelte and Astro each with its pack, Electron and Tauri locked down. | 2 tickets |
| v0.6.57 | JavaScript beyond Nuxt: the Node back ends | Express, Fastify, NestJS and Hono, the most used back ends after Django's peers, each with its own release's worth of rules rather than a share of the fronts' (framework coverage review of 26 October 2026). | 1 ticket |
| v0.6.58 | Data science repos | The first outside issues came from data repos: notebooks without outputs or secrets, data out of git, seeds and environments locked, models loaded safely. | 2 tickets |
| v0.6.59 | Open source done right | A licence that says the same everywhere, notices kept, contributing, conduct and security policies, issue forms, sponsors, the OpenSSF badge. | 2 tickets |
| v0.6.60 | Libraries and CLIs that publish cleanly | Trusted publishing with attestations, complete metadata, one version source, typed exports, packages that hold what they should and nothing else. | 2 tickets |
| v0.6.61 | Infrastructure as code | Terraform and OpenTofu, Kubernetes and Helm, Ansible: state out of git, versions pinned, buckets private, pods restricted. | 2 tickets |
| v0.6.62 | Every kind of repo | A library, an awesome list, a template, a fork or an archive each held to what it needs; the kind and what kiln assumed on the report's first lines, with their evidence. | 1 ticket |
| v0.6.63 | GitLab too | Universities and companies often run GitLab: its CI read like GitHub's, its settings through `glab`, its merge request widget fed. | 1 ticket |
| v0.6.64 | Profiles read from the repo, never asked | Solo, association, company or university, inferred from signals; criticality raises the bar by itself; moving up applies the new rules as ratchets. | 2 tickets |
| v0.6.65 | Coursework and research | A course's repos scored on what a student can act on, a teacher's guide, research artefacts that can be reproduced and cited. | 1 ticket |

</details>

<details><summary><b>v0.7.x</b> · 23 releases</summary>

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v0.7.0 | A whole organisation's repos | Milestone decided by antoine (16 October 2026: kiln for teams and organisations), re-scoped to the vision's targets: a university, an association network, a 50-person company; large companies come later. Every repo scored remotely without cloning, gaps ranked by how many repos share them. | 2 tickets |
| v0.7.1 | Compliance views | What a company has to show: Scorecard, ASVS, SLSA, CIS, WCAG, the Cyber Resilience Act and the Accessibility Act, each control covered or honestly listed as not checkable. | 1 ticket |
| v0.7.2 | Delivery measured, the organisation's settings read | DORA's four keys from the forge, the bus factor and knowledge islands, two-factor authentication and base permissions, for organisation profiles. | 1 ticket |
| v0.7.3 | The charter and the grid, one engine | Decision 4, before the format freezes: shared detectors first, then the charter as the grid's rules in strict or ratchet regime, its IDs kept as aliases; rule files checked by a published schema. ⚠ breaking: `charter.toml` lists grid rule IDs with their regime, converted by `kiln update`. | 1 ticket |
| v0.7.4 | Java and Kotlin repos, read | The road to v0.8.0: every common stack scored and fixed by script as Django is at v0.5.0, stack by stack (decision 1) in the order the corpus measures (B01; until it does, the order of the 2025 surveys, Stack Overflow's and GitHub's Octoverse). Two releases a stack, about what Django and Nuxt each took once the engine is set aside: first what its repos are made of, read, so that the rules spanning stacks see it; then its pack, counted once ten corpus repos of it were checked (B24). Each stack's rules are written from the corpus when its turn comes. First Java and Kotlin: Maven and Gradle read with their wrappers, Spring Boot, Quarkus and Micronaut recognised: kiln's own frozen Java template held to its stack's rules at last. | 1 ticket |
| v0.7.5 | The Java and Kotlin pack | A supported LTS, a verified wrapper, locked dependencies and a bug finder in the build, then Spring Boot's own rules, counted once ten corpus repos of Java and Kotlin were checked (B24). | 2 tickets |
| v0.7.6 | C# and .NET repos, read | Projects, solutions and central package management read, with nullable references and the supported .NET lines. | 1 ticket |
| v0.7.7 | The C# pack | NuGetAudit, lock files, warnings as errors and a pinned SDK, then the rules of ASP.NET Core and Blazor, counted once ten corpus repos of C# were checked (B24). | 2 tickets |
| v0.7.8 | PHP repos, read | Composer, Laravel, Symfony and WordPress read, with their analysers, formatters, tests and auditor. | 1 ticket |
| v0.7.9 | The PHP pack | Strict types, `composer audit` in CI, a supported PHP and no `phpinfo()` left, then the rules of Laravel, Symfony and WordPress, counted once ten corpus repos of PHP were checked (B24). | 2 tickets |
| v0.7.10 | C and C++ repos, read | CMake, Meson, Bazel, Conan and vcpkg read, with clang-format, clang-tidy, sanitizers and fuzzing. | 1 ticket |
| v0.7.11 | The C and C++ pack | Warnings as errors, sanitizers in CI, clang-tidy, fuzzing for parsers and managed dependencies, counted once ten corpus repos of C and C++ were checked (B24). | 1 ticket |
| v0.7.12 | Go repos, read | go.mod, go.sum and the toolchain read, with golangci-lint, govulncheck, race tests and wrapped errors, `go.sum` held to the rules that span stacks. | 1 ticket |
| v0.7.13 | The Go pack | Go's own rules with their examples and converters, from a tidy `go.mod` to no `panic` in a library, counted once ten corpus repos of Go were checked (B24). | 1 ticket |
| v0.7.14 | Rust repos, read | Cargo, clippy, the edition and `unsafe` read, `Cargo.lock` held to the rules that span stacks. | 1 ticket |
| v0.7.15 | The Rust pack | Rust's own rules, from clippy with warnings as errors to a declared MSRV, counted once ten corpus repos of Rust were checked (B24). | 1 ticket |
| v0.7.16 | Ruby repos, read | Bundler and Rails read, with RuboCop, Sorbet or RBS, RSpec or Minitest and bundler-audit. | 1 ticket |
| v0.7.17 | The Ruby pack | Brakeman and bundler-audit in CI, RuboCop configured, a supported Ruby and no `permit!`, counted once ten corpus repos of Ruby were checked (B24). | 1 ticket |
| v0.7.18 | iOS, Android and Flutter repos, read | SwiftPM, CocoaPods, the Android manifest and Flutter's pubspec read; App Transport Security and exported components checked. | 1 ticket |
| v0.7.19 | The mobile pack | What the stores require and what an app bundle gives away: the privacy manifest, the target SDK, no server secret in the app, signing keys out of git, counted once ten corpus repos of apps were checked (B24). | 1 ticket |
| v0.7.20 | Game repos, read and packed | Unity, Godot, Unreal and Roblox repos read on top of the C# and C++ packs, with Lua and Luau: the engine's version pinned, assets in Git LFS, caches and builds out of git, no store or signing credential committed. | 1 ticket |
| v0.7.21 | R repos, read and packed | R packages and analyses read and packed in one release: DESCRIPTION and renv, lintr, testthat and R CMD check, beyond the notebooks the data science release (v0.6.58) reads. | 1 ticket |
| v0.7.22 | Elixir repos, read and packed | A smaller ecosystem, read and packed in one release: mix and Phoenix, with Credo, Dialyzer, Sobelow and mix_audit as its rules. | 1 ticket |

</details>

<details><summary><b>v0.8.x</b> · 7 releases</summary>

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v0.8.0 | Every common stack scored | Milestone decided by antoine (25 October 2026), reached here: every common stack scored and fixed by script before the format freezes. The rarer languages come as data packs that the community packs of v1.0.0 will extend; then the gate, the corpus re-scored and each stack among those that make 95 % of its repos shown at the level of Django at v0.5.0. | 2 tickets |
| v0.8.1 | The CIs used most after GitHub's and GitLab's | The road to v0.9.0: any CI, any machine, any size, the last before the format freezes. First the CIs used most after GitHub's and GitLab's (v0.6.63), read into the CI model of v0.6.21 with their pinning and their untrusted text (appendix B). | 1 ticket |
| v0.8.2 | Every other CI | Jenkins, Buildkite, Woodpecker, the clouds' own CIs, Tekton and the rest, read the same way. | 1 ticket |
| v0.8.3 | Every machine, every network | macOS and WSL tested beside Linux, ARM64 and musl, air-gapped and corporate networks; native Windows only if T-94 reopens. | 1 ticket |
| v0.8.4 | No Python needed | A single signed binary, `npx kiln-cli score` for JavaScript machines, and the score in a browser if the forges allow it; a language server only if T-117 reopens. | 1 ticket |
| v0.8.5 | Monorepos and big trees | Monorepo tools' project graphs read for components and their links (T-86 staying declined for generating them), rules run in parallel, and a time budget that says what it left out. | 1 ticket |
| v0.8.6 | A million files | Sampling with a stated margin, Rust only where a profile points, then the speed published as uv and ruff publish theirs. | 1 ticket |

</details>

<details><summary><b>v0.9.x</b> · 2 releases</summary>

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v0.9.0 | Any CI, any machine, any size | Milestone decided by antoine (25 October 2026), reached here, the last before the format freezes: the bar of v1.0.0 run as a matrix in kiln's own CI, on GitHub's, GitLab's and one more CI, Linux, macOS and WSL, x86-64 and ARM64, a monorepo and a million files, each scored within its budget. | 1 ticket |
| v0.9.1 | Does the score mean anything? Measured, on every stack | The last proof before the stability promise, now that every stack is scored: ten senior engineers' ranking against kiln's, the score against public repos' incidents, readability against tokens, each published whatever it says. | 1 ticket |

</details>

<details><summary><b>v1.0.x</b> · 1 release</summary>

| Release | What it brings | Why together | Planned work |
|---|---|---|---|
| v1.0.0 | The grid others build on | Milestone decided by antoine (16 October 2026), its bar set on 25 October 2026: the public stability promise, once the rule format has held without breaking on the stacks that make about 95% of the corpus's repos (B01), on GitHub's, GitLab's and one more CI, on Linux, macOS and WSL, and on monorepos, each scored and fixed by script as Django is at v0.5.0; the long tail comes as community packs (T-69). From here, strict semver: breaking → major, `feat` → minor. | 3 tickets |

</details>

<!-- roadmap:end -->
