# 💡 kiln score: the thesis

> Written on 24 October 2026 at antoine's request: "if you wanted to improve `kiln score` as much
> as possible, how would you do it? It should adapt to every environment in the world, detect
> absolutely everything, leave the user nothing to do, be ultra fast and ultra powerful. `kiln
> score` is the base of everything: through it `kiln adopt` knows what to improve in a repo, and
> `kiln new` aims to meet every rule of `kiln score`. Add and change whatever you want, but code
> nothing." Nothing was coded; each idea got its release on 25 October 2026, then became a box
> of a ticket the same day.

**1,070 ideas**: 433 on the engine and the product (sections A to V), and 637 on rules (31 themes
and packs): 520 new rules, 98 drafts or trials given a detector, 19 scored rules made sharper. They
are tickets now, in the sections above: ion-repo#T-186 to ion-repo#T-319, plus boxes added to the existing tickets
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

## Part I · The thesis

### What kiln score is for

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

### Where it stands (measured on 24 October 2026)

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
- **GitHub Actions only** for CI rules; forge settings aren't read (ion-repo#T-158).
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
  to kiln as issues, with the user's yes (ion-repo#T-38, `gap_report.py`). The repo is then scored on
  universal rules only.

### The twelve moves

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

### Decisions (24 October 2026)

antoine left the six choices this file raised to Claude ("decide yourself"). Each is recorded
with its reason; the ideas below follow them.

1. **Every stack scored; the templates stay frozen.** `kiln adopt` promises to bring any repo up,
   and a Go or Java repo scored on the 14 universal rules and those of its tools gets a hollow
   number. Generating keeps ion-repo#T-133's line (Django and Nuxt first, the other templates frozen;
   `rejected.md` now says "templates"); scoring opens stack by stack after the launch, in the
   order the corpus and ion-repo#T-38's gap reports show, each pack with its facts, rules, examples and
   measured precision.
2. **Equal weights stay; critical findings cap the score.** The number keeps meaning "the share
   of the rules that apply, met" (ion-repo#T-46): weights would be numbers to defend, and would shift
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
   data-migrations) join `THEMES`, each with its first rule, in ion-repo#T-141. Developer experience goes
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
   (ion-repo#T-39), company and enterprise ask for CI on every pull request, where integration breaks
   between people.

Ideas that brush a declined ticket carry ⚠ and its number (ion-repo#T-94 Windows without WSL, ion-repo#T-48
devcontainers, ion-repo#T-86 monorepos, ion-repo#T-71 `kiln mcp`): those stay declined until someone reopens them,
as antoine reopened ion-repo#T-117, the editor extension, on 26 October 2026.

### Order of battle

Every idea is a box of a ticket listed under its release in [🚀 Releases](#-releases)
(25 October 2026, at antoine's request: everything a ticket, in its place). The plan in short:

| Releases | From these ideas | Why then |
|---|---|---|
| v0.4.10 to v0.5.0, before the launch | what their tickets already do (ion-repo#T-158's GitHub settings, ion-repo#T-159's containers run on a copy, kiln-bot, the study as the first corpus, kiln's repos at 100) and three small ones: the two silent passes (A30, A31) and the potential line (I07) | the launch's releases are full: a new idea there would push the gate |
| v0.5.4 to v0.5.16 | what strangers meet first (K), the false alarms (A, E, H), the badge (L), speed, updates, `kiln fix`, rules that test themselves (G), the outputs where people look (L), the exact rules and the AI rules (Part III), the roadmap as context packs (O), tests at the lowest cost | the launch brings repos nobody here has seen, and v0.6.0 needs the roadmap and the tests |
| v0.6.0 | O: the unattended run's scope guard, its labels and its costs | the milestone |
| v0.6.1 to v0.6.11 | slimming, the grid's weekly watch, the repo model (A), rule format v2 (E, G), the syntax engine, mature tools (F), the cache (J) | the engine every later rule stands on |
| v0.6.12 to v0.6.61 | the rule themes one by one, each after the rung it needs; between them the corpus and the critical cap (H, I), locks and registries, history and the forge (M), `--deep` (N), what the grid doesn't know (U), Python and JavaScript beyond Django and Nuxt (B, FP) | a rule enters once its detector's rung exists and the corpus can measure it |
| v0.6.62 to v0.7.3 | kinds and profiles (D), GitLab (C), coursework, the fleet (K, P), compliance views (R), the charter as the grid's rules (decision 4) | a university or an association network scores every repo |
| v0.7.4 to v0.8.0 | the other ecosystems, two releases a stack (B, SP), the long tail as data packs, the gate measured on the corpus | the format has to hold on every common stack before it freezes, in the order the corpus measures |
| v0.8.1 to v0.9.0 | every CI and machine (C, K), monorepos and huge trees (J), the bar's matrix run | and on every CI, machine and size |
| v0.9.1 | the score itself measured on every stack (T) | the last proof before the promise |
| v1.0.0 | packs (R, ion-repo#T-69), the published JSON schema, every executable thing pinned | the format is the public API; the long tail comes as packs |

Among the ecosystems, generic Python and JS/TS come first (v0.6.55 to v0.6.57); the order of the
others is a guess until the corpus measures it (B01).

## Appendices

### A · Ecosystem matrix

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

### B · CI matrix

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

### C · OpenSSF Scorecard and the grid

Scorecard grades the same things from outside; kiln would answer each check, or say why not.
ion-repo#T-90 asks kiln to pass Scorecard itself.

| Scorecard check | Grid rule today | From this file |
|---|---|---|
| Binary-Artifacts | none | `NO-BINARY-ARTIFACTS` (SU) |
| Branch-Protection | none | `NO-FORCE-PUSH-ON-MAIN`, `REQUIRED-CHECKS` (L6, ion-repo#T-158) |
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
| Webhooks | none | the forge's webhooks with a secret (L6, ion-repo#T-158) |

### D · Data to bundle or read

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
