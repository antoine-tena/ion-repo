# kiln score: the idea backlog

> Written on 24 October 2026 at antoine's request: "if you wanted to improve `kiln score` as much
> as possible, how would you do it? It should adapt to every environment in the world, detect
> absolutely everything, leave the user nothing to do, be ultra fast and ultra powerful. `kiln
> score` is the base of everything: through it `kiln adopt` knows what to improve in a repo, and
> `kiln new` aims to meet every rule of `kiln score`. Add and change whatever you want, but code
> nothing." Nothing here is coded or planned yet.

**1,070 ideas**: 433 on the engine and the product (Part II, sections A to V), and 637 on rules (Part III, 31 themes and packs): 520 new rules, 98 drafts or trials given a detector, 19 scored rules made sharper.

**How to read it.**
- These are ideas, not tickets. One becomes a ticket of [backlog.md](backlog.md) when it is
  planned (`/kiln:backlog`), its `Origin` quoting `backlog-kiln-score.md <ID>`, and its box here
  is ticked with the ticket's number.
- The vision still decides ([docs/vision/](../vision/README.md)): one way per profile, the best
  and not the newest, the script first and Claude next, a rule that flags wrongly is worse than
  none, nothing without proof.
- Part I is the thesis (what to aim at, where it stands, the big moves, the order). Part II holds
  the engine and product ideas, one letter per section (`A01`…). Part III holds rule ideas, two
  letters per theme (`SU07`…). The appendices are reference tables to build from.
- Rule ideas use a short notation after their description: the detector's rung (`L0` to `L7`,
  section E; `≈` when the detector is approximate and Claude confirms), `fix S` when a converter
  can close the gap or `fix J` when it takes judgment, then the radar level it would enter at.
- ⚠ marks an idea that brushes a declined ticket or a licence to check. The six choices this
  file raised are decided in Part I.
- Locations quoted are hints, measured on `develop` at `7685fe6`.

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

Ideas that brush a declined ticket carry ⚠ and its number (T-94 Windows without WSL, T-117 an
editor extension, T-48 devcontainers, T-86 monorepos, T-71 `kiln mcp`): those stay declined
until someone reopens them.

### Order of battle

Inside the plan of [backlog.md](backlog.md) as it stands tonight (v0.4.6 is today's candidate;
about 7 session-hours a release, 4 of them planned; the launch on 11 November waits for v0.5.0,
and from v0.5.1 to the launch only fixes go in):

| Release | From this file | Why then |
|---|---|---|
| v0.4.7 "every gap seen, wherever the code lives" | A: components and their roles, folders left out (template, fixtures, vendored, generated, examples), facts per component, the UTF-8 silent pass; with T-166, one answer to "what is this repo" | kiln reads itself as Django + Nuxt: T-132's study would count stacks that aren't there |
| v0.4.8 "never lets it rot" | P: `kiln update` and kiln-bot never lower the score silently; I: the delta that says whether the repo or the grid moved | kiln-bot's weekly pull request (T-59) needs a delta to show |
| v0.5.0 "the proof and the page" | H: precision sampled on T-132's corpus, Python rules made code-aware (stdlib `tokenize`), the rules' own examples out of their reach; I: the critical cap and the potential line | the study publishes numbers: they must be right, and "58 now, 74 after `kiln fix`" is the demo |
| v0.5.4 "the first week with strangers" | K: what strangers hit first (Python 3.14 needed, a crash on an odd repo, a flag to find); U: the first gap reports read | the launch brings repos nobody here has seen |
| v0.5.5 "findings where people look" | L: SARIF with T-91, annotations, job summary; J: the cache and `--changed` beside T-77 | people run it in CI and on bigger repos |
| v0.5.6 "the grid grows, and stays current" | Part III with T-141: the exact rules promoted first (`USE-TZ`, `NO-MASS-ASSIGNMENT`, `PORTS-ON-LOCALHOST`, `DOCKERIGNORE`, `CI-TIMEOUTS`, `NO-DEBUGGER`, `NO-CONFLICT-MARKERS`, `VUE-V-FOR-KEY`, `HTML-LANG`, `NO-SIGNALS`, `SESSION-COOKIES`, `NO-PERSISTED-CREDENTIALS`); Q with T-140; C: GitLab CI | the grid grows on what the corpus measured, never the week of the launch |
| v0.6.0 "Claude closes the gaps alone" | O: context packs, effort and token estimates, ordered gaps | the roadmap becomes the whole input of an unattended run |
| v0.6.1 "less code to carry" | the slimming rules (`DEPENDENCY-BUDGET`, `DUPLICATION`, `DEAD-CODE`, `UNUSED-DEPENDENCIES`) proven by the compressor | T-138 measures first |
| v0.7.0 "a whole organisation's repos" | D, P, K: kinds, profiles, remote scoring without cloning | a university or an association network scores every repo |
| v1.0.0 "the grid others build on" | G frozen (rule format v2), the charter run as the grid's rules (decision 4), R: packs and repo-local rules | the format is the public API |

Ecosystems after the launch, in the order the corpus measures rather than assumes: generic Python
and JS/TS first, then whichever of Go, Java and Kotlin, C#, PHP, Ruby or Rust the corpus shows.

## Part II · The engine and the product

### A · One model of the repo

- [ ] **A01** One module answers "what is this repo" (`kiln.repo`), replacing `grid/facts.py`, `stack.py:detect_stack` and `grid/fix.py:check_commands`; score, fix, adopt, dev, check and update all read it.
- [ ] **A02** Components: every folder holding a manifest is one (pyproject.toml, package.json, go.mod, Cargo.toml, pom.xml, build.gradle(.kts), *.csproj, composer.json, Gemfile, mix.exs, pubspec.yaml, Package.swift, CMakeLists.txt, meson.build, DESCRIPTION, Project.toml, deno.json, flake.nix, Chart.yaml, a folder of *.tf), nested under its parent.
- [ ] **A03** Workspaces group components: uv workspaces, pnpm-workspace.yaml, npm, Yarn and Bun workspaces, Cargo workspaces, go.work, Maven modules, Gradle settings, Nx, Turborepo, Lerna, Rush, Bazel's MODULE.bazel, Pants, Moon.
- [ ] **A04** A role per component, inferred: backend, frontend, library, CLI, worker, infra, docs, mobile, desktop, extension, data/ML, tests, template, fixture, vendored, generated, example. Each role turns groups of rules on or off.
- [ ] **A05** Templates recognized and kept out of the repo's own stack: `copier.yml`, `cookiecutter.json`, `{{ }}` in paths, `.jinja`, `.j2`, `.tmpl` suffixes. kiln's `template/` stops making kiln a Django + Nuxt repo.
- [ ] **A06** Fixtures and test data kept out of code rules (`tests/fixtures/`, `testdata/`, `__snapshots__/`, `cassettes/`, `*.golden`), still read by the secret rules.
- [ ] **A07** Vendored code recognized (`vendor/`, `third_party/`, `external/`, submodules, `*.min.js` in static folders): scored on its own rules (pinned, known vulnerabilities, licence kept), never as the repo's code.
- [ ] **A08** Generated code recognized (`@generated`, `DO NOT EDIT`, Go's `Code generated … DO NOT EDIT.`, `*.pb.go`, `*_pb2.py`, `*.gen.ts`, OpenAPI clients, Django migrations for size rules): left out of style and size rules.
- [ ] **A09** `.gitattributes` honoured: `linguist-vendored`, `linguist-generated`, `linguist-documentation`, `export-ignore`, conventions many repos already set for GitHub.
- [ ] **A10** Every fact carries its evidence (`django 5.2 · backend/uv.lock:412`) and a confidence (certain from a lock, likely from an import, possible from a file name).
- [ ] **A11** Versions in facts, from the lock first, the manifest's constraint next: rules can say `django >= 4.2`, `vue < 3`, `node 20`.
- [ ] **A12** A parser per lockfile (uv.lock, poetry.lock, pdm.lock, Pipfile.lock, pylock.toml, hashed requirements, pnpm-lock.yaml, package-lock.json v1 to v3, yarn.lock classic and Berry, bun.lock, Cargo.lock, go.sum, composer.lock, Gemfile.lock, mix.lock, pubspec.lock, packages.lock.json, gradle.lockfile, Package.resolved, renv.lock, Manifest.toml, flake.lock, .terraform.lock.hcl): exact versions and the whole tree, transitives included.
- [ ] **A13** Runtime versions gathered from every place that names one (.python-version, requires-python, .tool-versions, mise.toml, runtime.txt, .nvmrc, .node-version, engines, Volta, packageManager, Dockerfile FROM, CI matrices, global.json, rust-toolchain.toml, go.mod's `go` and `toolchain`), and their disagreements reported.
- [ ] **A14** Tools per component: which linter, formatter, type checker, test runner, bundler and task runner, from config files and dev dependencies; rules then speak of "your formatter", whichever it is.
- [ ] **A15** Services read from compose, Kubernetes, Procfile, fly.toml, render.yaml, app.json, vercel.json, netlify.toml, wrangler.toml, serverless.yml: databases, caches, queues, search, object storage, with their versions.
- [ ] **A16** Where it deploys (a VPS by script, Fly, Render, Railway, Heroku, Vercel, Netlify, Cloudflare, Cloud Run, AWS, Azure, Kubernetes, GitHub Pages), which switches the operations rules on.
- [ ] **A17** Domain facts from code and dependencies: money (Decimal fields named price, Stripe), personal data (user models, e-mail fields), uploads, e-mail sending, payments, LLM calls (the anthropic and openai SDKs). They switch on MONEY, PERSONAL-DATA, AI-FEATURES and their kin without a question.
- [ ] **A18** Team facts from history: contributors in the last 90 days, commit rhythm, age, last activity, code size by language; inputs of the profile (T-39) and of the kind (D).
- [ ] **A19** Facts declared as data (`facts/*.toml`: file patterns, dependency names, content signatures), tested like rules: a new ecosystem is a data change, not code.
- [ ] **A20** A share threshold for languages: one helper script in Python doesn't make a JavaScript repo a Python repo (today one `.py` file turns every Python rule on).
- [ ] **A21** `kiln score --facts`: the model as a tree (components, roles, versions, tools, services) with its evidence, in JSON too. The first thing to read when a rule misapplies.
- [ ] **A22** `kiln score --why-applies RULE`: the facts that made a rule apply here.
- [ ] **A23** Applicability as an expression over the model (`component.role == "backend" and django >= 4.2`) instead of the flat `applies` list.
- [ ] **A24** Findings per component, paths still relative to the repo: a Django rule never reads `frontend/`.
- [ ] **A25** The repo's score aggregates its components' (weighted by code size); each component scorable alone (`kiln score backend/`).
- [ ] **A26** Language by content when the extension lies: shebangs, `.h` (C, C++ or Objective-C), `.m` (Objective-C or MATLAB), `.pl`, `.v`, `.ts` (TypeScript or Qt translations), with Linguist's heuristics as data.
- [ ] **A27** Outside git, `.gitignore` parsed anyway: `build/`, `target/` and `.venv` stay out (only a fixed list is skipped today).
- [ ] **A28** Untracked files scored but marked "untracked": a local `.env` that isn't ignored is a real risk, a local experiment isn't the repo.
- [ ] **A29** Shallow clones, sparse checkouts, partial clones, worktrees, bare repos and submodules handled; what wasn't checked out is said, never guessed.
- [ ] **A30** Binary files skipped on a NUL byte in their first 8 KB; minified files (lines over 1,000 characters) skipped by code rules but counted.
- [ ] **A31** A non-UTF-8 source decoded (BOM, then cp1252 or latin-1) and reported; never read as empty, which passes every regex rule today.
- [ ] **A32** Symlinks never followed out of the repo, loops cut, case-insensitive file systems (macOS, Windows) normalized.
- [ ] **A33** Git LFS patterns known: a binary tracked by LFS is fine, the same binary outside it is a finding.
- [ ] **A34** The model cached by the blob SHAs of the manifests: every kiln command reuses it in milliseconds.
- [ ] **A35** A corpus for the model itself: 500 real trees (paths and manifests) with their expected model; each fact's precision tracked like a rule's.
- [ ] **A36** A correction exists when detection is wrong (`kiln set components.ignore=…`), is never needed, and each use is a signal for T-38.
- [ ] **A37** `kiln dev` and `kiln check` read the model: T-159's "checks found beyond the root" falls out of it.
- [ ] **A38** The template a repo started from, fingerprinted (kiln, cookiecutter-django, create-next-app, `nuxi init`, `rails new`, Spring Initializr, the Laravel installer): what that template changed since can be compared.
- [ ] **A39** Forks recognized (an `upstream` remote, or the forge says so): the fork's own changes scored apart from upstream's code.
- [ ] **A40** Archived repos (the forge's flag, an "archived" notice in the README) scored only on what still matters: secrets, licence.

### B · Every ecosystem

- [ ] **B01** The order of ecosystems set by the corpus (share of repos, share of code), never assumed; Django and Nuxt stay the reference.
- [ ] **B02** Python beyond Django: Flask, FastAPI, Litestar, Starlette, aiohttp, Pyramid; SQLAlchemy and Alembic; Pydantic 1 to 2; Celery, RQ, Dramatiq, Huey, django-q2; each with a pack of rules (Part III, FP).
- [ ] **B03** Every Python packaging tool read: uv, Poetry, PDM, Hatch, pip-tools (`requirements.in`), Pipenv, Conda (environment.yml, conda-lock), Rye (`hold`, to uv), setup.py and setup.cfg (`hold`, to PEP 621), PEP 735 dependency groups, PEP 751 `pylock.toml`, PEP 723 inline script metadata.
- [ ] **B04** JavaScript and TypeScript beyond Nuxt: Next.js, React Router 7, Astro, SvelteKit, SolidStart, Angular, Vite with React or Vue, Express, Fastify, NestJS, Hono, Koa, Electron, Tauri, React Native and Expo.
- [ ] **B05** Every JS package manager read: npm, Yarn classic and Berry (PnP, `.yarnrc.yml`), pnpm, Bun, Deno (deno.json, deno.lock, JSR), corepack's `packageManager`.
- [ ] **B06** Go: go.mod and go.sum, the `go` and `toolchain` directives, golangci-lint, gofmt, govulncheck, `go vet`, `-race` in CI, vendoring.
- [ ] **B07** Rust: Cargo.lock committed, clippy, rustfmt, cargo-deny or cargo-audit, `rust-version`, the edition, `unsafe` justified, cargo-semver-checks for libraries.
- [ ] **B08** Java and Kotlin: Maven (wrapper and checksum), Gradle (wrapper validation, version catalogs, locking, verification metadata), Spring Boot, Quarkus, Micronaut; Checkstyle, SpotBugs, Error Prone, Spotless, ktlint, detekt; JUnit 5; Java's LTS lines. kiln's own frozen Java template would finally be scored.
- [ ] **B09** C# and .NET: .csproj, .sln and .slnx, central package management, `packages.lock.json`, `<Nullable>enable`, analyzers, `dotnet format`, `global.json`, supported .NET lines.
- [ ] **B10** PHP: Composer, Laravel, Symfony, WordPress (themes, plugins, wp-config), PHPStan or Psalm, PHP-CS-Fixer, PHPUnit or Pest, `composer audit`.
- [ ] **B11** Ruby: Bundler, Rails (credentials, `force_ssl`, Brakeman), RuboCop, Sorbet or RBS, RSpec or Minitest, bundler-audit.
- [ ] **B12** Elixir (mix, Phoenix, Credo, Dialyzer, Sobelow), Swift (SwiftPM, CocoaPods, SwiftLint), Android (manifest, R8), Dart and Flutter (pubspec, analysis_options).
- [ ] **B13** C and C++: CMake, Meson, Bazel, Conan and vcpkg manifests, clang-format, clang-tidy, sanitizers and fuzzing in CI, warnings as errors.
- [ ] **B14** The long tail as data packs: Scala, Haskell, OCaml, Clojure, Erlang, F#, Julia, R (DESCRIPTION, renv, lintr, testthat), Perl, Lua, Zig, Nim, Fortran (fpm), MATLAB.
- [ ] **B15** Shell and PowerShell as real code: shellcheck, shfmt, `set -euo pipefail`, bats; PSScriptAnalyzer.
- [ ] **B16** SQL as code: sqlfluff, squawk for Postgres migrations, dbt projects.
- [ ] **B17** Infrastructure as code: Terraform and OpenTofu, Pulumi, CDK, CloudFormation, Bicep, Ansible, Helm, Kustomize, Nix (Part III, IN).
- [ ] **B18** Notebooks as code: `.ipynb` parsed (cells, outputs, execution order), Quarto and R Markdown read.
- [ ] **B19** Every config file kiln recognizes validated against its JSON Schema from the SchemaStore catalogue: typos and deprecated keys found in hundreds of tools' files, for free.
- [ ] **B20** Markup and assets: Markdown (markdownlint's rules, links), YAML (yamllint), TOML (taplo), CSS (stylelint), HTML, SVG (no script inside), images (weight, format), fonts (subset, self-hosted).
- [ ] **B21** One practice, many ecosystems, one ID: `LOCKED-DEPENDENCIES`, `FROZEN-INSTALL-IN-CI` or `NO-INSTALL-SCRIPTS` carry a detector per ecosystem, so "universal" rules really are.
- [ ] **B22** End of life for every product endoflife.date covers (runtimes, frameworks, databases, distributions, Kubernetes, CI runners), bundled at each release, refreshed by `--online`.
- [ ] **B23** Ecosystem packs written as data and proven by examples, so the community (T-69) adds one without touching kiln's code.
- [ ] **B24** A new ecosystem's rules count only after ten public repos of that stack in the corpus were scored and their findings checked: precision first.
- [ ] **B25** A stack the grid doesn't cover yet is scored on the universal rules and told which pack would cover it, and how many corpus repos share it: a reason to write the pack.

### C · Every forge, CI, host and machine

- [ ] **C01** A CI model: jobs, steps, commands, triggers, permissions, pinned references, secrets used, images. Extracted from every CI format so one rule speaks of all of them (appendix B).
- [ ] **C02** GitLab CI: `.gitlab-ci.yml`, `include:` (project, remote, template, component with a version), `rules:`, `needs:`, the job token's scope, protected and masked variables.
- [ ] **C03** The other CIs read: Bitbucket Pipelines, Azure Pipelines, CircleCI (orbs pinned), Jenkins (Jenkinsfile, shared libraries pinned), Buildkite, Woodpecker and Drone, Forgejo and Gitea Actions, SourceHut, TeamCity, AppVeyor, Travis (`hold`), Google Cloud Build, AWS CodeBuild, Tekton, Argo Workflows, Dagger, Earthly.
- [ ] **C04** Indirections followed: a step running `make test`, `just check`, `task lint`, `nox`, `tox`, `npm run test`, `./gradlew check` or `kiln check` is resolved into what it runs, so TESTS-IN-CI knows tests really run (a regex on the workflow today).
- [ ] **C05** PINNED-ACTIONS generalized to every CI's references: GitHub `uses:` by SHA, GitLab `include` refs and component versions, CircleCI orbs, Jenkins `@Library`, Buildkite plugins, images in `container:`, `services:` and `image:` by digest.
- [ ] **C06** Injection rules for every CI: GitHub's `${{ github.event… }}` in `run:`, GitLab's `$CI_COMMIT_MESSAGE` or `$CI_MERGE_REQUEST_TITLE` in `script:`, Azure's `$(Build.SourceVersionMessage)`, Jenkins' Groovy-interpolated `sh "…${env.CHANGE_TITLE}"`.
- [ ] **C07** Least privilege for every CI token: GitHub's `permissions:`, GitLab's job token allowlist, their Bitbucket and Azure counterparts.
- [ ] **C08** Pre-commit frameworks read (pre-commit, lefthook, Husky, lint-staged): checks before a commit, never counted as CI.
- [ ] **C09** Forges: GitHub, GitLab (cloud and self-managed), Bitbucket, Azure DevOps, Gitea, Forgejo, Codeberg, SourceHut, Gerrit; read from the remote's URL, their folders (`.github/`, `.gitlab/`, `.gitea/`, `.forgejo/`, `.azuredevops/`) and conventions (where CODEOWNERS and templates live) known.
- [ ] **C10** Every dependency bot recognized and held to the same settings: Dependabot (every ecosystem folder covered, cooldown, groups), Renovate (every config place, `minimumReleaseAge`, presets), GitLab's dependency scanning, Snyk, Mend, Depfu.
- [ ] **C11** Deploy configs read: Dockerfile, Containerfile, compose, Kubernetes manifests (any YAML with `apiVersion` and `kind`), Helm, Kustomize, Skaffold, Tilt, Nomad, systemd units, Caddyfile, nginx, Traefik, Fly, Render, Railway, Heroku, Vercel, Netlify, Cloudflare, Firebase, App Engine, Serverless, SAM.
- [ ] **C12** Neutral to container engines (Docker, Podman, Buildah, Kaniko, BuildKit): `# syntax=`, `--mount=type=secret` and `type=cache`, Bake files, devcontainer.json read.
- [ ] **C13** Rules that know operating systems: CRLF and `.gitattributes`, paths Windows refuses, case collisions that break macOS, a setup documented only as a `.sh` script.
- [ ] **C14** kiln score runs on Linux, macOS, WSL and native Windows (it is Python and git) ⚠ T-94 declined Windows without WSL for kiln as a whole; the score alone may cost little, tested in CI if taken.
- [ ] **C15** x86-64 and ARM64 (Apple Silicon, Graviton, Raspberry Pi), glibc and musl (Alpine): every bundled tool shipped as a wheel for each, or its rules say "unknown" there.
- [ ] **C16** Editor and environment files read: `.editorconfig`, `.vscode/` (recommended extensions, settings with personal paths), `.idea/` (workspace files committed), devcontainers, Gitpod, Codespaces, mise and asdf, direnv's `.envrc` (secrets in it), Nix dev shells, flox.
- [ ] **C17** Any human language in the repo: a README found as `LISEZMOI.md` or `README.zh-CN.md`; generic-name lists per language (`donnees`, `truc`, `datos`, `daten`); typography that isn't a bug (French non-breaking spaces, the doctrine's ruff example); identifiers in any script.
- [ ] **C18** Air-gapped and corporate networks: offline by default; `--online` honours `HTTPS_PROXY` and custom certificate authorities (`SSL_CERT_FILE`); the data bundle downloadable as one file (`--data bundle.tar.zst`).
- [ ] **C19** Monorepo tools' project graphs (Nx, Turborepo, Bazel, Pants, Rush, Moon) read for components and their links ⚠ T-86 (declined) is about generating monorepos; scoring them is another matter.
- [ ] **C20** The integration branch read from the remote's HEAD (main, master, develop, trunk), never assumed.
- [ ] **C21** Self-hosted forges on custom domains recognized by their API's signature (GitLab's `/api/v4/version`, Gitea's `/api/v1/version`), with `--online` only.
- [ ] **C22** Reusable CI pieces (GitHub reusable workflows, GitLab components, CircleCI orbs) followed one level, at their pinned version, with `--online`: a reusable workflow that grants `write-all` is the caller's problem too.

### D · Every kind of repo, every profile

- [ ] **D01** Kinds recognized: web app (backend, frontend, full stack), API, library (PyPI, npm, crates.io, Maven Central…), CLI, desktop, mobile, browser extension, editor extension, GitHub Action, Claude Code plugin or MCP server, data science, ML training, data pipeline (dbt, Airflow, Dagster), infrastructure, docs site, static site, dotfiles, template, coursework, research artefact, game, firmware, hardware, HPC, WordPress, Shopify theme, serverless functions, bot, smart contracts, awesome list, single script.
- [ ] **D02** Each kind its rules: a library needs semver, a changelog, typed exports and trusted publishing, not health probes; an awesome list needs link checks, not tests (today TESTS-PRESENT fails every awesome list).
- [ ] **D03** A repo can be several kinds (a library with a docs site and a CLI): kinds per component.
- [ ] **D04** The profile (T-39) inferred from signals, never asked: owner (person or organisation), contributors in 90 days, a deployment, personal data handled, licence, stars, a security policy.
- [ ] **D05** Stages: prototype, growing, production, maintenance, archived. Rules grow with the repo ("the smallest level at creation, and rules that grow with the repo", antoine, 16 October 2026).
- [ ] **D06** Criticality raises the bar by itself: payments, health or children's data, accounts of other people make the stricter profile's rules apply, and the report says why.
- [ ] **D07** Thresholds that scale: a 200-line script isn't held to a monorepo's architecture rules; ratchets on a big repo start from its own numbers.
- [ ] **D08** Team signals: CODEOWNERS and required reviews only past two regular contributors; the bus factor (one person wrote 90 % of the last year) shown to organisation profiles.
- [ ] **D09** Coursework: a course's repos (many, small, short-lived, one template) scored on what a student can act on; a teacher scores the class (fleet, CSV). The v0.7.0 university target.
- [ ] **D10** Research artefacts: CITATION.cff, a pinned environment, data availability, a DOI, "how to reproduce the figures"; the artefact badges of ACM and the big conferences as rules.
- [ ] **D11** Kind and profile on the report's first lines with their evidence; `kiln set kind=library` exists, is never needed, and each use is a T-38 signal.
- [ ] **D12** The forge's topics and description read with `--online` as hints (`homework`, `tutorial`, `template`, `awesome`).
- [ ] **D13** Template repos (`is_template`, `copier.yml`) scored on what they generate: rendered with defaults in a sandbox, the result scored. A template's score is its children's.
- [ ] **D14** Tutorials and example repos recognized, so the study and the fleet don't count them (T-132's exclusions as code).
- [ ] **D15** Claude Code plugins and MCP servers as a kind: plugin.json valid, skills named as their folder, hooks executable, permissions narrow, versions pinned (kiln's own `test_plugins.py`, offered to all).
- [ ] **D16** GitHub Actions as a kind: `action.yml` valid, a supported `runs.using`, `dist/` rebuilt and compared in CI, inputs documented, no `${{ inputs.x }}` inside `run:`.

### E · The detection engine

- [ ] **E01** The ladder: L0 paths and names (microseconds), L1 structured files (TOML, JSON, YAML, INI, XML, HCL, Dockerfile, ignore files), L2 syntax patterns, L3 cross-file (imports, calls, references), L4 external tools, L5 git history, L6 forge and registry APIs, L7 running the code. Each rule declares its rung, each finding says which one found it.
- [ ] **E02** The default run is L0 to L3 plus the L4 tools shipped as wheels: offline, nothing of the repo executed. `--online` adds L6, `--history` L5, `--deep` L7 in a sandbox.
- [ ] **E03** A `syntax` detector kind on ast-grep (Rust, tree-sitter, YAML rules with `pattern`, `inside`, `has`, `not`, `constraints`): declarative like today's regexes, matching code instead of text (doctrine 11, T-144).
- [ ] **E04** One parse per file, shared by every syntax rule, the tree cached by blob SHA.
- [ ] **E05** Until the syntax engine lands, `regex` gets `in = "code" | "comments" | "strings" | "any"`, from Python's `tokenize` (stdlib) and a small JS/TS tokenizer: the false positives seen on kiln vanish with no new dependency.
- [ ] **E06** Path classes instead of hand-written globs: `where = ["code"]`, `["tests"]`, `["config"]`, `["docs"]`, `["ci"]`, `["containers"]`, from the model; generated, vendored, fixtures and templates left out by default.
- [ ] **E07** A policy per rule for tests: `in_tests = "skip" | "lower" | "same"` (SQL built in a test is noise; a naive datetime in a test can hide a bug).
- [ ] **E08** Combinators (`all`, `any`, `not`) and conditions ("if a Dockerfile `EXPOSE`s a port, compose or the Dockerfile has a health check").
- [ ] **E09** Cross-file detectors: every job that tests also lints; every Django app with models registers an admin or says why; every route has a test that calls it (routes extracted, tests searched).
- [ ] **E10** An import graph per language (Python's `ast`, an ES-module scanner): cycles, layers (SEALED-DOMAIN), dead modules, fan-in and fan-out.
- [ ] **E11** Taint inside one function: a request value (`request.GET`, `request.data`, route parameters, `req.query`) reaching a sink (`execute`, `os.system`, `open`, `redirect`, `subprocess`, `eval`) without a known sanitizer.
- [ ] **E12** Symbol tables per language (functions, classes, variables, booleans, constants) from tree-sitter queries: CASE, BOOLEANS, GENERIC-NAMES and ONE-CLASS for every language.
- [ ] **E13** A metrics pass: lines and logical lines per file and function, cyclomatic and cognitive complexity, nesting, parameters, token duplication, comment density, TODOs, for any language (lizard's approach), feeding the size and complexity ratchets.
- [ ] **E14** Config resolved rather than grepped: tsconfig `extends` chains (local files and package presets), ruff's `extend`, ESLint flat configs read as syntax (never executed), mypy, pyright, pytest and coverage settings wherever they live.
- [ ] **E15** Django settings evaluated statically: the module found (`manage.py`, `wsgi.py`, `asgi.py`, `DJANGO_SETTINGS_MODULE`), `from .base import *` followed, plain assignments and `env("X", default=…)` read. `DEBUG = env.bool("DEBUG", default=True)` becomes a finding; it is invisible today.
- [ ] **E16** `nuxt.config` read as syntax: `runtimeConfig` (secrets under `public`), `routeRules`, the Nitro preset, `devtools`, modules, `ssr`, `sourcemap`.
- [ ] **E17** Dockerfiles parsed per stage: the final stage's `USER`, `ARG` defaults resolved inside `FROM` (a `$` image is skipped today, a false negative), heredocs, `--mount` options.
- [ ] **E18** Equivalence lists as data (Python linters: ruff, flake8, pylint; dependency bots: Dependabot, Renovate…): a practice met by any, with "met; kiln recommends ruff" as a gentle `trial` note.
- [ ] **E19** Evidence for passes too: "met by `renovate.json`", "met: `USER app` in the final stage of `Dockerfile`". `--all` says why each rule passed.
- [ ] **E20** A third outcome, `unknown`: the detector couldn't decide (a config written as code, a tool missing, a file too big). Listed apart, never a pass, never a fail.
- [ ] **E21** Linear-time regexes (google-re2, or Rust's `regex` through the syntax engine) and a time budget per rule: one bad pattern can't hang a run.
- [ ] **E22** `kiln grid` lints every pattern for catastrophic backtracking when the grid loads.
- [ ] **E23** Locations with line, column and end (SARIF regions), with a snippet, redacted for secrets.
- [ ] **E24** A fingerprint per finding (rule, path, normalized snippet, like SARIF's `partialFingerprints`): a finding keeps its identity when lines move, so waivers and baselines survive edits.
- [ ] **E25** Baselines: `kiln score --baseline` records today's findings, and from then on only new ones fail a gate. The progressive path of doctrine 9 for any repo, not only kiln's.
- [ ] **E26** Approximate detectors return candidates with a confidence: the roadmap sends the uncertain ones to Claude "to confirm" and the certain ones as gaps.
- [ ] **E27** Docs checked against the tree: every path, command and make target quoted in the README and CLAUDE.md exists (REPO-MAP-FRESH, README-COMMANDS-EXIST). A map that lies costs Claude more than no map.
- [ ] **E28** A secrets engine: provider patterns (gitleaks' rules as data), checksum-verified tokens (GitHub's `ghp_` and `github_pat_` tokens carry a CRC32, so zero false positives), entropy last; documented sample keys and placeholders (`AKIAIOSFODNN7EXAMPLE`, `changeme`, `<your-token>`) left out.
- [ ] **E29** Artefacts that should never be committed, by name and content: `.pyc`, `node_modules/`, `dist/`, `.DS_Store`, `*.log`, `*.sqlite3`, `*.tfstate`, `id_rsa`, `*.pem`, `*.p12`, `*.keystore`, `.ipynb_checkpoints`, coverage reports, virtualenvs.
- [ ] **E30** `.gitignore` compared with github/gitignore's templates for the ecosystems present: what's missing is a scripted fix.
- [ ] **E31** Freshness of generated files without running anything: the lock against its manifest, the committed OpenAPI schema against the routes it names, an action's `dist/` against its sources (approximate; `--deep` proves).
- [ ] **E32** Never read `.git/`, virtualenvs or `node_modules` as code, even when they're tracked by mistake (that's its own finding).
- [ ] **E33** A rule's condition can read the model (`component.frameworks.django.version`), so Django 4.2 and 5.2 can have different detectors.
- [ ] **E34** Inline justifications in the charter's style (`# kiln: allow NAIVE-DATETIMES, reason`): counted, shown, gone when the code they sit on goes.
- [ ] **E35** A detector can ask for several files at once (compose, Dockerfile and CI together): the engine hands it the set, each file read once.

### F · Mature tools as detectors

- [ ] **F01** A `tool` detector kind: run a tool with machine output (JSON, SARIF), map each result to a rule and a place. The tool comes from the repo's environment, PATH or kiln's bundle; it is never downloaded without `--online`.
- [ ] **F02** ruff as the Python engine wherever it has the rule: DTZ (naive datetimes), E722 (bare except), PGH003 and PGH004 (blanket ignores), S608 (SQL by strings), S602 to S607 (shell), S301 and S506 (unsafe loads), S113 (no timeout), B006 (mutable defaults), T20 (print), C901, PLR2004 (magic values), UP (modern Python at the `requires-python` target), DJ, ASYNC, PTH, ERA. Exact, string-aware, and its safe fixes become free converters.
- [ ] **F03** kiln's reference ruff selection run even on repos without a ruff config (isolated, kiln's own config), beside the repo's: "your linter says" and "the grid says" kept apart.
- [ ] **F04** zizmor for GitHub Actions (template injection, excessive permissions, unpinned uses, persisted credentials, cache poisoning, dangerous triggers, impostor commits, known-vulnerable actions): a Rust wheel, mapped onto WORKFLOW-INJECTION, PULL-REQUEST-TARGET, PINNED-ACTIONS, WORKFLOW-PERMISSIONS and new rules.
- [ ] **F05** shellcheck (the `shellcheck-py` wheel) on shell scripts and on the `run:` blocks of workflows.
- [ ] **F06** actionlint for workflow correctness (expressions, contexts, job dependencies).
- [ ] **F07** oxlint or Biome for JS/TS rules (no-eval, eqeqeq, no-debugger, accessibility) as native binaries (T-144 measures them).
- [ ] **F08** hadolint's most useful checks rewritten on the parsed Dockerfile (latest tag, root user, pipefail, apt hygiene, `ADD` of a URL, exec form) rather than shipping a Haskell binary.
- [ ] **F09** osv-scanner, or OSV's batch API, for real vulnerability counts in the locked versions. VULNERABILITY-AUDIT checks today that an audit runs, not what it would find.
- [ ] **F10** govulncheck for Go (reachable vulnerabilities only), cargo-deny for Rust, `composer audit`, bundler-audit.
- [ ] **F11** trivy's config mode or checkov for Terraform, Kubernetes, Helm and Dockerfiles, mapped onto the containers and infrastructure rules.
- [ ] **F12** kube-linter or kubeconform for Kubernetes manifests.
- [ ] **F13** deptry and knip (unused and missing dependencies) and vulture (dead code), already used by the compressor: their findings feed UNUSED-DEPENDENCIES and DEAD-CODE once their precision is measured.
- [ ] **F14** Type checkers as ratchet metrics in `--deep` (mypy, pyright, ty or pyrefly once mature, tsc, vue-tsc): the error count at strict settings.
- [ ] **F15** typos (Rust) for misspellings in identifiers and comments, with very few false positives.
- [ ] **F16** lychee for links: relative links and anchors offline, external ones with `--online`, cached.
- [ ] **F17** The REUSE tool and a licence detector in licensee's manner for the licensing theme.
- [ ] **F18** squawk and django-migration-linter for migrations, sqlfluff for SQL.
- [ ] **F19** OpenSSF Scorecard's checks redone locally where possible (they need its API otherwise): "kiln score covers Scorecard" is a claim worth making (appendix C).
- [ ] **F20** Semgrep-compatible rules ⚠ licences first: the Semgrep registry's rules have their own licence, the opengrep engine is LGPL. kiln's own rules stay in ast-grep.
- [ ] **F21** Every tool pinned by version and hash, its output cached by the hash of its inputs; a tool update is a grid change and its precision is measured again.
- [ ] **F22** Several tools on one line deduplicated: ruff's S608 and another tool on the same SQL string make one finding with both as evidence.
- [ ] **F23** A missing tool never fails a rule: "unknown: install kiln's tools extra, or run with `--deep`".
- [ ] **F24** A `kiln-cli[tools]` extra bringing the tools that ship as wheels in one install.
- [ ] **F25** The tool that detected becomes the tool that keeps it closed: `kiln fix` adds its config and its CI step when missing (ruff, zizmor, pre-commit).

### G · Rule format v2 and authoring

- [ ] **G01** Examples inside the rule file (`[[examples]]` with `expect` and inline files): the grid tests itself, packs ship tested rules, and `tests/test_grid.py` reads them instead of its `CASES`.
- [ ] **G02** Several examples per rule, edge cases included; every false positive ever reported becomes a `pass` example, so it never comes back.
- [ ] **G03** `applies` as an expression over the repo model (A).
- [ ] **G04** `any_of`: the ways one practice can be met, each with its own detector.
- [ ] **G05** `severity` (critical, high, medium, low, info), apart from `regime` (how it is enforced) and `level` (the radar).
- [ ] **G06** `effort` per place and per rule, in session minutes, and `impact`: the roadmap's order and the effort-to-100 estimate come from them.
- [ ] **G07** A `message` per place with placeholders (`{image} is named by tag: pin it as {image}@sha256:…`): the finding says what to do right there.
- [ ] **G08** A `fix` block: a converter, a ruff code, or a written recipe for Claude; `safety = "safe" | "unsafe"` as ruff marks its fixes.
- [ ] **G09** `related`, `supersedes` and `aliases`: old IDs answered forever, the stable-ID promise of v1.0.
- [ ] **G10** A `standards` table: CWE, OWASP Top 10 and ASVS, OpenSSF Scorecard, SLSA, NIST SSDF, CIS benchmarks, WCAG, the EU Cyber Resilience Act, twelve-factor.
- [ ] **G11** Profiles stay a membership list, never weights (decision 2): a rule outside the repo's profile is not applicable, so `SLO` asks nothing of a solo repo.
- [ ] **G12** `level_history`: when and why the rule moved on the radar, with the evidence (precision, sources). An auditable radar.
- [ ] **G13** `switch_when` made checkable (`django supports python 3.15`, from PyPI classifiers or endoflife data): kiln says by itself when it is time.
- [ ] **G14** `precision` and `prevalence` written by the calibration job (H), shown in `kiln grid ID` and on the rule's page.
- [ ] **G15** A Markdown page per rule beside its file (why, bad and good code, the fix, references), as ruff documents its rules; `kiln grid ID --doc` shows it, the site publishes it.
- [ ] **G16** A published JSON Schema for rule files: editors check a rule as it is typed (taplo, VS Code).
- [ ] **G17** `kiln grid new ID` scaffolds a rule and its examples; `kiln grid test [ID]` runs the examples; `kiln grid try ID --on <repo>` runs one rule with its timing.
- [ ] **G18** `kiln grid lint`: patterns that can backtrack, unknown facts, missing examples, stale sources, messages too long for a terminal line or for Claude's tokens.
- [ ] **G19** Rule IDs linted: uppercase, three words at most, naming the practice rather than the violation.
- [ ] **G20** One practice, several languages, one ID: `[detector.python]`, `[detector.typescript]`, `[detector.java]`.
- [ ] **G21** A hash per rule (content and engine version) for cache keys and for the report's `grid_version`.
- [ ] **G22** `inputs` declared per rule (the path classes it reads): the incremental engine knows what to recompute.
- [ ] **G23** `shadow = true`: a new detector runs and records on the corpus and on beta machines without showing, for one release, before it counts.
- [ ] **G24** Typed settings with defaults, for project data only (time zone, currency, integration branch): never a knob that weakens a rule (doctrine 1).
- [ ] **G25** A rule may carry its own small test repo folder (`rules/<theme>/<ID>/`) when inline examples get too big (a whole Django project).

### H · Precision and recall

- [ ] **H01** A labelled corpus: T-132's hundred repos as its first version, then 1,000 and 10,000 public repos sampled by language, size and age, each pinned to a commit, every finding labelled true or false.
- [ ] **H02** Labels from Claude in batches (20 places per rule, "to confirm"), spot-checked by antoine, stored by fingerprint; only aggregates in public, anything that names a project in `kiln-private`.
- [ ] **H03** Precision and recall per rule at every candidate; a strict rule under 99 % precision, or any drop, stops the candidate (`kiln version cut`).
- [ ] **H04** Differential tests against reference tools (zizmor, Scorecard, gitleaks, ruff): each disagreement triaged into a kiln bug or a documented difference.
- [ ] **H05** Examples mutated: failing variants generated from each `pass` example (the `USER` line removed, a SHA turned into a tag), and the detector must flip.
- [ ] **H06** Property tests (Hypothesis) on every parser (Dockerfile, workflows, compose, settings): random input never crashes, and the outcome is deterministic.
- [ ] **H07** A fuzzed tree: deep nesting, Unicode and spaces in paths, symlink loops, empty files, 100 MB files, invalid UTF-8, CRLF, BOM, case collisions.
- [ ] **H08** Known false-positive classes handled once, in the engine: tests, fixtures, templates, examples, code blocks in docs (a README showing the bad way), `.example` files, vendored and generated code, migrations, documented sample keys, localhost URLs.
- [ ] **H09** Known false negatives (from reading the code on 24 October) closed one by one: `FROM $IMAGE` skipped; the file's last `USER` read instead of the final stage's; `permissions: write-all` passes WORKFLOW-PERMISSIONS; a tsconfig strict through a local `extends` fails STRICT-TS; a linter config anywhere (even under `template/`) passes PYTHON-LINTER for the whole repo; compose, Kubernetes and CI images escape IMAGES-BY-DIGEST.
- [ ] **H10** Known false positives closed too: `requires-python = ">=3.9"` read as running 3.9 (a library's floor, not its runtime); an app with an empty `models.py`, or one under `tests/`, asked for migrations; a lone `.go` file in `docs/` announcing "Go: not covered".
- [ ] **H11** Waivers as signals beyond renewals (reported since v0.4.6): "false positive" in a reason, or one rule waived across many repos of a fleet, flags the rule for review.
- [ ] **H12** Inline markers and waivers counted per rule across the corpus: the most-waived rules are examined first.
- [ ] **H13** A confidence per finding (the rule's precision times its context: test file, generated, comment), shown as "certain" or "likely".
- [ ] **H14** Recall measured with seeded faults: secrets, unpinned images, root containers planted in copies of corpus repos must all be found.
- [ ] **H15** A crash budget of zero on the whole corpus at every candidate; a rule that crashes is reported with a minimal anonymized tree for `/kiln:report`.
- [ ] **H16** Seniors' agreement: ten senior engineers rank twenty repos, and kiln's order must agree with theirs (Kendall's tau of 0.7 or more). "Like a senior engineer would", measured.
- [ ] **H17** A regression suite of real false positives: each one reported gets a minimal repo in `tests/` that must pass forever.
- [ ] **H18** Precision shown to users ("this rule is 99.4 % precise on 1,000 repos"): trust earned with numbers.
- [ ] **H19** The corpus's labels versioned with the grid, so a rule's precision history is a plot, not a memory.
- [ ] **H20** A rule that flags more than half of the corpus is looked at twice: either the practice is rare (say so) or the detector is wrong.

### I · Scoring model v2

- [ ] **I01** A severity on each rule (critical, high, medium, low) that orders the gaps and marks the critical ones; it never weighs the number (decision 2).
- [ ] **I02** Critical findings cap the score at 49 (decision 2), each critical rule proven at 99 % precision first: a committed secret, `DEBUG = True` in production settings, `pull_request_target` checking out the pull request's code, the engine's socket mounted in a container. A repo that leaks its keys can't show 90.
- [ ] **I03** Progress shown per place, never as partial credit: "`IMAGES-BY-DIGEST`: 37 of 40 pinned" beside the rule, so every fix shows while the number keeps meaning rules met (decision 2).
- [ ] **I04** Approximate findings not counted until Claude or the user confirms them: the score never punishes a maybe.
- [ ] **I05** Scores per component and per theme, under the five pillars; under each pillar, its weakest themes (decision 5).
- [ ] **I06** The denominator explained: "31 rules apply: Python, Django, Docker, GitHub Actions"; a new Dockerfile says "5 more rules apply now, 2 met".
- [ ] **I07** The potential on every run: "58 now · 74 after `kiln fix` (no token, about 2 minutes) · 100 after the roadmap (12 items, about 3 hours of Claude Code)".
- [ ] **I08** Effort to 100 from the rules' effort estimates, in session hours, the backlog's unit.
- [ ] **I09** A percentile against the study's distribution, bundled: "better than 82 % of public Django repos" (aggregates only, no repo named).
- [ ] **I10** `grid_version` in every report and badge; `kiln score --grid 0.4.5` re-scores with an older grid (bundled history) to compare like with like.
- [ ] **I11** New `adopt` rules announced one release ahead ("counts from v0.5.6: you meet it", or "you will lose 2 points: `kiln fix` closes it"): no score drops overnight.
- [ ] **I12** `kiln score --history`: the score at each tag or merge (cheap with the cache), drawn as a curve; "41 to 78 since adoption".
- [ ] **I13** The score of a change: "this branch takes the score from 74 to 76; 1 new finding, 3 fixed". The gate is "no new finding", never an absolute number.
- [ ] **I14** Anti-gaming: presence rules check content (a README with install and usage, a SECURITY.md with a contact, tests that assert, CI that runs on pull requests and pushes). An empty file earns nothing.
- [ ] **I15** A delivery score apart, for organisation profiles with `--online`: DORA's four keys from the forge (deploy frequency from releases, lead time from merge times, change failure rate from reverts and hotfixes, time to restore from incident issues).
- [ ] **I16** Remediation time in hours per rule and in total: a debt figure for practices.
- [ ] **I17** `kiln score --explain`: the formula with this repo's numbers in it.
- [ ] **I18** One function computes the score everywhere (CLI, badge, bot, fleet, HTML), with golden tests.
- [ ] **I19** The score model versioned (`score_model` in the JSON); a change re-scores the reference repos and the release note says its effect.
- [ ] **I20** "Rules met" stays on the first line (24 of 31): plainer than a percentage for a newcomer.
- [ ] **I21** A verdict in plain words generated from the findings, no model needed: "well tested, but the supply chain is open: unpinned actions and images, no update bot".
- [ ] **I22** Upcoming deadlines in the score's margin: "Node 22 reaches its end on 30 April 2027, in 188 days" (see `--calendar`, Q).

### J · Speed

- [ ] **J01** Measure first: `kiln score --profile` (time per phase: listing, model, each rule, output; the ten slowest rules) and a benchmark suite (an empty repo, kiln, a copy of the reference repo, a 50,000-file monorepo, a synthetic million-file tree) in CI, with thresholds.
- [ ] **J02** Startup measured (`-X importtime`) and budgeted (80 ms to the first line): `urllib` imported only for `--online` (60 ms today), copier and Jinja never imported by `score`.
- [ ] **J03** A lean path: the score's dependencies kept minimal, so `uvx kiln-cli score` downloads little on a first run; the template's dependencies only for `new`, `adopt` and `update`.
- [ ] **J04** One listing (`git ls-files -s` gives each tracked file's blob SHA for free); contents through `git cat-file --batch` when the tree is clean, from disk otherwise.
- [ ] **J05** A file-to-rules index built once, every rule's globs merged into one matcher: today each rule walks every file with its own patterns.
- [ ] **J06** Only the files some applicable rule needs are read; sizes from `git cat-file --batch-check` skip the huge ones before reading.
- [ ] **J07** YAML through libyaml's `CSafeLoader` when present, several times faster than the pure-Python loader.
- [ ] **J08** All text rules for one file type in a single scan (a combined automaton: a regex set, or Hyperscan where a measurement says so).
- [ ] **J09** Rules in parallel: threads for I/O-bound rules, processes on big repos; free-threaded Python 3.14 measured.
- [ ] **J10** A cache keyed by blob SHA, rule hash and engine version in `~/.cache/kiln/score/`: a warm run recomputes nothing unchanged, in under 50 ms.
- [ ] **J11** `--changed`: only files changed since the merge base, and the repo-level rules whose inputs changed, are checked again.
- [ ] **J12** `--watch`: re-score on save (watchfiles, Rust), the changed file only.
- [ ] **J13** The Claude Code edit hook re-scores the edited file in milliseconds and tells Claude only what is new; one engine with the charter's `check_file.py`.
- [ ] **J14** A resident process only if measurements demand it, as language servers do; never by default.
- [ ] **J15** Rust only where a profile points: the walker, glob matching and the multi-pattern scan are the candidates (a `kiln-core` wheel through PyO3), or ripgrep's engine through `rg --json` when installed.
- [ ] **J16** The syntax engine runs all syntax rules of a language in one native pass (`ast-grep scan` over a rules folder), in parallel.
- [ ] **J17** A time budget (`--budget 2s`): rules by value per cost, and what didn't run is said ("not checked: budget").
- [ ] **J18** Metrics sampled on huge repos with a stated margin (sizes, complexity); security rules always exhaustive.
- [ ] **J19** `--online` calls in parallel, cached a day with ETags (endoflife.date, OSV, forge APIs), batched (OSV's `querybatch` takes hundreds of packages at once).
- [ ] **J20** Speed published as uv and ruff publish theirs: "0.3 s on Django's own repo, 4 s on a million files". Speed is part of the pitch.
- [ ] **J21** A candidate more than 10 % slower on the suite waits for an explanation.
- [ ] **J22** The repo and CI models cached across commands (score, fix, dev, check) and across runs.
- [ ] **J23** `--first` for hooks: stop at the first critical finding.
- [ ] **J24** History scans incremental: each commit's blobs scanned once, ever (the cache knows them by SHA), so `--history` costs seconds after the first run.

### K · Nothing to do

- [ ] **K01** One command, no install: `uvx kiln-cli score`. Documented beside it: `pipx run --python 3.14 kiln-cli score` (an older Python fails on PEP 758 syntax), Homebrew, a container image pinned by digest.
- [ ] **K02** A single signed binary for machines without Python or uv (PyApp, which bootstraps through uv, or a frozen build), on each GitHub release.
- [ ] **K03** `npx kiln-cli score` for JavaScript-only machines: a small npm package that runs the binary.
- [ ] **K04** Any repo by URL: `kiln score github:owner/repo`, `kiln score https://gitlab.com/…`. A shallow clone in the cache, scored, deleted; private repos through `gh` or `glab`'s login.
- [ ] **K05** Remote scoring without a clone for L0 and L1 rules: the Git Trees API lists every path in one call for most repos, then a few config files are fetched. Seconds, for T-87's fleet view.
- [ ] **K06** In the browser with Pyodide, on a tarball fetched from the forge's API, no server at all; to verify (CORS on the tarball endpoints).
- [ ] **K07** No config, no question, no `kiln adopt` needed to score; a plain folder, a zip or a tarball scored too.
- [ ] **K08** CI detected (`GITHUB_ACTIONS`, `GITLAB_CI`, `CI`): annotations, SARIF and a job summary written without a flag, colours off outside a terminal (T-116).
- [ ] **K09** Exit code 0 by default, since it is a measure; gates are explicit: `--fail-under 80`, `--fail-on critical`, `--no-new` against a baseline or the integration branch.
- [ ] **K10** Never a crash: a broken file is a finding, a rule that throws is reported as a kiln bug (with `/kiln:report`'s hint), and the run goes on.
- [ ] **K11** The next step always printed as one command: "`kiln fix` closes 5 of these 9 gaps, on a branch, no token".
- [ ] **K12** `kiln score --fix`: score, fix, score again, in one go.
- [ ] **K13** A repo generated by kiln scoring under 100 says it: kiln's bug, reported with consent ([REPORT-TO-KILN]).
- [ ] **K14** The integration branch, the main language and the profile detected; the report says what it assumed.
- [ ] **K15** Explanations a newcomer understands (one sentence, no jargon) and `--explain` for the details: "like a senior engineer would, even if you're not one".
- [ ] **K16** Offline on a plane: all but `--online` works; the data's date shown, with "12 new rules since your version" when the tool is old (`tool_update.py`).
- [ ] **K17** Claude Code does the work: the plugin's session start shows the score in one line (cached), the status line shows it, the edit hook keeps it. The user only reads.
- [ ] **K18** Nothing written in the repo by default (as today); `--output` writes a report when asked.
- [ ] **K19** kiln-bot (T-59) as the effortless default for any public repo: one copy-paste, a weekly pull request with the score and `kiln fix`'s commits.
- [ ] **K20** On a machine, `kiln install` (T-161) is the only setup; in a repo, there is none.

### L · Outputs and integrations

- [ ] **L01** `--format`: text, json, sarif, junit, markdown, html, csv, gitlab-codequality, github-annotations, checkstyle.
- [ ] **L02** Complete SARIF 2.1.0: rules with `helpUri` to their page, regions, `partialFingerprints`, `fixes` for scripted fixes, waivers as `suppressions` with their reason (T-91).
- [ ] **L03** GitLab: the Code Quality report (merge request widget) and the SAST report format for security rules.
- [ ] **L04** JUnit XML, each rule a test case, for Jenkins, Azure and any CI's test tab.
- [ ] **L05** A Markdown summary for pull request comments and `$GITHUB_STEP_SUMMARY`.
- [ ] **L06** A self-contained HTML report in one file: the score, the pillars with their weakest themes, findings with snippets, filters, the potential bar, the history curve.
- [ ] **L07** A live badge: kiln-bot publishes a shields.io endpoint JSON (Pages or a gist) instead of a number frozen in the README (T-154).
- [ ] **L08** `--compare <ref or report.json>`: new, fixed and still-open findings, the delta, the rules that started or stopped applying.
- [ ] **L09** Pull request comments by the action: the delta, new findings as review comments on the diff's lines, fixed ones thanked.
- [ ] **L10** GitHub check runs with annotations, sent in batches of 50.
- [ ] **L11** Scores kept in git notes (`refs/notes/kiln-score`), as `kiln ci` keeps its verdicts: history for free, travelling with the repo when pushed.
- [ ] **L12** A language server: diagnostics for place rules in any editor, code actions for scripted fixes ⚠ T-117 (a VS Code extension) is declined for now; a language server serves every editor at once, only if adopters ask.
- [ ] **L13** The `--json` schema published (`schema.json`), versioned with a changelog, stable at v1.0.
- [ ] **L14** `--quiet` (the number only) and `--porcelain` (stable lines for scripts).
- [ ] **L15** `kiln grid --json`: the whole catalogue for other tools.
- [ ] **L16** CSV across many repos (`kiln status --csv`): a teacher grading a class, an association checking its repos.
- [ ] **L17** `--open`: the HTML report in the browser.
- [ ] **L18** `--for-claude`: the roadmap's context packs, token-counted, nothing decorative.
- [ ] **L19** The report's absolute `root` left out by default: it names the user's home when shared.
- [ ] **L20** Messages in English only (decided on 16 October 2026), each finding short enough for one terminal line.
- [ ] **L21** A finding links to its rule's page and to the line on the forge when the remote is known (`https://github.com/o/r/blob/<sha>/path#L12`).

### M · History, forge and registries

- [ ] **M01** Secrets ever committed, scanned through history (each blob once, cached): a key removed but never rotated is still a key.
- [ ] **M02** Heavy blobs in history, which every clone carries forever: git-filter-repo or LFS suggested.
- [ ] **M03** Commit habits over the last 90 days (Conventional Commits share, size distribution): SMALL-COMMITS and a commit-message rule promoted on facts.
- [ ] **M04** Signed commits and tags (GPG, SSH, gitsign), as a share.
- [ ] **M05** Direct commits on the integration branch (first-parent commits that aren't merges): NO-COMMIT-ON-INTEGRATION from history.
- [ ] **M06** Merge style (MERGE-COMMITS) and branch names (BRANCH-NAMES) from history.
- [ ] **M07** Release rhythm from tags: the last release's age, semver tags, a changelog entry per tag (RELEASE-NOTES).
- [ ] **M08** Hotspots: churn times complexity per file (Adam Tornhill's method). The roadmap opens hotspots first, since that is where the next bug will be.
- [ ] **M09** Change coupling: files that always change together across folders show a boundary in the wrong place.
- [ ] **M10** Code untouched for years and imported by nothing: candidates for the compressor (T-138).
- [ ] **M11** `fix:` commits that come with a test change (REGRESSION-TEST from history).
- [ ] **M12** A lock changed without its manifest, or the reverse, in history: drift caught at its source.
- [ ] **M13** Reverts and hotfixes per month: the change failure rate.
- [ ] **M14** Bus factor and knowledge islands, for organisation profiles.
- [ ] **M15** Forge settings read through the CLI already logged in (`gh`, `glab`, `tea`); a token is never asked for (T-158, generalized).
- [ ] **M16** GitHub: rulesets or branch protection on the integration branch (pull requests required, checks required, no force push, no deletion), signatures required, linear history when the repo merges that way.
- [ ] **M17** GitHub: secret scanning and push protection, Dependabot alerts and security updates, code scanning, private vulnerability reporting.
- [ ] **M18** GitHub: the default `GITHUB_TOKEN` read-only, "Actions can create pull requests" off, allowed actions limited, approval for first-time contributors' workflows, environments with reviewers for deploys.
- [ ] **M19** GitHub: secret names and ages (the API gives `updated_at`): unused secrets, secrets older than a year (SECRET-ROTATION becomes detectable), long-lived cloud keys where OIDC would do.
- [ ] **M20** GitHub: deploy keys read-only, webhooks with a secret and TLS checking, immutable releases, tag rulesets.
- [ ] **M21** GitLab: protected branches and tags, merge request approvals, push rules, secret detection, protected and masked variables, the job token's scope.
- [ ] **M22** Organisations: two-factor authentication required, base permissions, SSO (organisation profiles).
- [ ] **M23** Open alerts by age: critical Dependabot or code-scanning alerts open for more than 30 days.
- [ ] **M24** Update pull requests left open (Dependabot, Renovate) for more than a few weeks: the bot is set but ignored, the real gap behind DEPENDENCY-UPDATES.
- [ ] **M25** Community health from the forge (README, licence, conduct, contributing, templates) and maintainers' responsiveness (median first response), for open-source profiles.
- [ ] **M26** Registries: trusted publishing and attestations on PyPI (PEP 740) and npm (provenance), checked on the published files.
- [ ] **M27** Registries: each dependency's health (last release, deprecated flag, yanked versions, archived source, a single maintainer) for ABANDONED-DEPENDENCIES.
- [ ] **M28** Registries: typosquat suspects (one edit from a popular name, few downloads) and known malicious packages (OSV's `MAL-` advisories).
- [ ] **M29** All of it cached and rate-limited, with "unknown: log in with gh to check" without access. Never a failure for lack of a token.
- [ ] **M30** `--at <ref>`: the repo scored as it was at a tag or a commit (a throwaway worktree, cached).

### N · Deep checks, opt-in and sandboxed

- [ ] **N01** `--deep` runs in a throwaway copy, in a container when an engine is there, network off unless a step needs it, within a time budget; never in the user's tree.
- [ ] **N02** Images built: size, final user, a shell or not, packages with known vulnerabilities (trivy or grype on the image), the health check passing.
- [ ] **N03** Containers started read-only with every capability dropped: a service that still starts gets the hardening from `kiln fix` (what T-159 needs).
- [ ] **N04** An install from the lock that works (`uv sync --locked`, `pnpm install --frozen-lockfile`): LOCK-IN-SYNC proven.
- [ ] **N05** Tests run: pass rate, duration, the slowest, the flaky (failures run again), order dependence (random order), network use (sockets blocked: NO-NETWORK proven), clock dependence (a shifted fake clock: CLOCK proven).
- [ ] **N06** Coverage measured (lines and branches) and mutation testing on a sample (mutmut, Stryker): the tests theme's ratchets fed with real numbers.
- [ ] **N07** Django's own `manage.py check --deploy` against the production settings: HSTS, SSL redirect, secure cookies, `DEBUG`, `SECRET_KEY`'s strength, `ALLOWED_HOSTS`, X-Frame-Options. Official checks, mapped onto grid rules.
- [ ] **N08** `manage.py makemigrations --check --dry-run`: models and migrations in sync.
- [ ] **N09** Migrations applied to a fresh Postgres container, then reversed; their SQL linted by squawk (through `sqlmigrate`).
- [ ] **N10** The OpenAPI schema generated and compared with the committed one (CONTRACT-DRIFT), then a short Schemathesis run (API-FUZZING).
- [ ] **N11** The front built: bundle sizes (JS-BUDGET), `nuxi typecheck`, pages rendered by Playwright for axe (ACCESSIBILITY) and for Lighthouse's lab metrics (CORE-WEB-VITALS).
- [ ] **N12** The app served locally and probed: security headers, cookie flags, CORS, error pages leaking a stack trace, `/admin` exposed, directory listings, server banners.
- [ ] **N13** A deployed URL scored too (`--url https://…`, opt-in): TLS, headers, `security.txt`, redirects; the production that the repo describes.
- [ ] **N14** N+1 queries caught while the tests run (nplusone, django-zeal), query counts per view.
- [ ] **N15** Type checkers and the repo's linters at their strictest: error counts as ratchets.
- [ ] **N16** The app's start-up time and memory, as ratchets.
- [ ] **N17** Deep results cached by commit and marked "measured at <commit>"; kiln-bot's weekly run uses `--deep` in CI, where running code is normal.
- [ ] **N18** The backup script run against a throwaway database and restored (TESTED-BACKUPS proven) for repos whose scripts kiln knows.
- [ ] **N19** `kiln dev`'s own launch reused as a probe: if the stack starts with `kiln dev`, its servers are probed while they run, with no second setup.

### O · The roadmap for Claude

- [ ] **O01** A context pack per gap: the rule (why, recipe, a passing example), the places with five lines around each, the repo's own passing example when one exists ("this repo already does it right in `x.py`"), the proof command. Claude opens nothing else.
- [ ] **O02** Tokens and effort estimated per item; items ordered by points gained per token.
- [ ] **O03** Dependencies between items (tests before a refactor, types before the compressor, the lock before the audit) give a topological order.
- [ ] **O04** Batches: one rule with many places split into chunks of under an hour of session each.
- [ ] **O05** Hotspots first among equals (M): the places that change most are fixed first.
- [ ] **O06** Risk tags: config only, pure refactor, behaviour change, product decision (the skill already stops on the last).
- [ ] **O07** Recipes as data for every judgment rule, so two sessions fix a gap the same way (and T-137 can turn the recipe into a converter).
- [ ] **O08** Each place's coverage (from `--deep` or a committed report): untested places get "write a characterization test first".
- [ ] **O09** `--roadmap --budget 2h`: the best set of items for one session (a knapsack on points and effort).
- [ ] **O10** `--roadmap --json` with the packs inline: `/kiln:modernize` reads one document and explores nothing.
- [ ] **O11** A scope guard: a modernize commit that touches files beyond its places and their tests is flagged before it merges.
- [ ] **O12** Confirmations and dismissals of "to confirm" places fed back as labels (H), with consent.
- [ ] **O13** The roadmap as GitHub or GitLab issues (`--write-issues`, labelled by rule), not only backlog tickets.
- [ ] **O14** Good first issues from the roadmap on open-source repos: small, well-placed items tagged for `/kiln:good-first-issues`.
- [ ] **O15** A one-line summary per item for the human, in the user's language when Claude speaks to them.
- [ ] **O16** A roadmap file other agents can read too (AGENTS.md style); kiln stays Claude-first.
- [ ] **O17** After a modernize session, the points won, tokens spent and items left logged per rule: the cost of a judgment gap measured, not guessed (input of T-137 and of the effort estimates).

### P · One measure drives every command

- [ ] **P01** `kiln new` proven at 100: every combination of answers (stack, size, options) generated and scored at each candidate; a template change that lowers any of them fails (T-130's matrix).
- [ ] **P02** `kiln fix` on a fresh `kiln new` repo changes nothing; when it does, the template is behind the grid.
- [ ] **P03** The radical form: `kiln new` as an empty folder, then `kiln adopt`, then `kiln fix`. The template and the converters can't drift apart.
- [ ] **P04** Each `adopt` rule names the template files that meet it (`met_by_template = […]`): `kiln grid` says "kiln new does this for you".
- [ ] **P05** Grid first: a new rule makes the template's test fail until the template meets it, test-driven development for the template.
- [ ] **P06** `kiln adopt` as a funnel: score before, lay files, `kiln fix`, score after, roadmap tickets; each step a commit on its branch.
- [ ] **P07** `kiln adopt --dry-run` shows the score it would reach.
- [ ] **P08** `kiln update` shows the score before and after, and the grid changes that touch this repo; a lower score stops the update unless the grid explains it.
- [ ] **P09** `kiln fix` reports the points each commit won.
- [ ] **P10** `kiln check` includes "no new finding against the integration branch".
- [ ] **P11** The charter and the grid as one engine (decision 4): shared detectors first, a test that makes a rule and its charter twin agree on the examples; at v1.0.0 a rule written once in the grid, `charter.toml` listing rule IDs with their regime and budget, the charter's IDs kept as aliases.
- [ ] **P12** `kiln dev`, `kiln doctor` and `kiln check` read the repo model (A).
- [ ] **P13** `kiln status` shows each local repo's score and the grid version it was scored with.
- [ ] **P14** kiln's own score at 100 gates its release (done on the branch `chore/modernize-score`, 24 October 2026).
- [ ] **P15** The reference repo's score and its potential after `kiln fix` in every release note (T-134).
- [ ] **P16** kiln-bot (T-59) posts the delta on each pull request and opens the weekly fix pull request.
- [ ] **P17** The fleet (T-87) scores an organisation's repos remotely (K) and ranks gaps by how many repos share them: one fix in kiln helps them all.
- [ ] **P18** The frozen templates (T-133) scored at each candidate too: frozen doesn't mean rotting, and their score goes in the docs.

### Q · A grid that stays current

- [ ] **Q01** A data bundle per release, dated and shown by `kiln score --version`: end-of-life dates, deprecated and malicious packages, retired CI runners and commands, retired LLM model IDs, provider secret patterns.
- [ ] **Q02** The weekly watch (T-140) refreshes the bundle and flags the rules whose sources changed.
- [ ] **Q03** Radar moves on evidence only: assess to trial needs a detector and examples; trial to adopt needs 99 % precision on the corpus (strict rules) and fresh sources; adopt to hold when the practice is superseded.
- [ ] **Q04** `hold` rules detect what is on its way out: Travis CI, Pipenv, Rye, `setup.py install`, `pytz`, `nose`, `distutils`, Python 2 idioms, TSLint, create-react-app, Vue 2, Nuxt 2, AngularJS, `node-sass`, `request`, `moment`, compose's `version:`, `docker-compose` v1, `apt-key`, `::set-output`, retired runner images.
- [ ] **Q05** A converter for each `hold` rule a script can close: `pytz` to `zoneinfo`, `::set-output` to `$GITHUB_OUTPUT`, compose's `version:` removed, `docker-compose` to `docker compose`.
- [ ] **Q06** A grid diff in each release note: rules added, promoted, demoted, retired.
- [ ] **Q07** A coverage map, themes by ecosystems with the number of scored rules in each cell, holes visible (`kiln grid --coverage`).
- [ ] **Q08** Standards coverage: the share of Scorecard, ASVS level 1, CIS Docker, SLSA build level 2 and WCAG AA controls that a grid rule covers.
- [ ] **Q09** A radar fed by the corpus: tools rising quarter after quarter become `assess` candidates, tools falling become `hold` candidates.
- [ ] **Q10** A consistency check: no two rules contradict (examples cross-run: a pass example of one never fails another).
- [ ] **Q11** A `grid-proposal` issue template (a practice with its sources), triaged by the doctrine.
- [ ] **Q12** The decision behind each rule kept with it (why adopt, why now), like an architecture decision record.
- [ ] **Q13** `kiln score --calendar`: what will break and when (Node 22 ends on 30 April 2027, 188 days from today; a runner image retired; a framework's support ending), the maintenance load the vision wanted to measure.
- [ ] **Q14** Rules retire too: a practice everyone now meets by default (a framework made it the default) leaves the score, kept as history.

### R · Packs, local rules, standards

- [ ] **R01** Repo-local rules in `.kiln/grid/` (T-91), in the same format, their examples run by `kiln grid test`.
- [ ] **R02** Packs from any git repo (T-69), pinned by SHA, behind a trust prompt that shows what their detectors run; declarative detectors only unless trusted (a Python check is code execution).
- [ ] **R03** Organisation packs for the v0.7.0 targets: a university's rules for student repos, an association network's.
- [ ] **R04** Community packs for stacks kiln won't template: FastAPI, Rails, Laravel, Spring Boot, Go services.
- [ ] **R05** An index of reviewed packs with their precision on the corpus.
- [ ] **R06** Compliance views (`kiln score --standard scorecard | asvs-l1 | slsa | cis-docker | owasp-top10 | wcag-aa | cra | gdpr`): what passes, what fails, and what can't be checked statically, honestly listed.
- [ ] **R07** EU Cyber Resilience Act readiness for companies selling software in Europe (reporting duties from September 2026, the rest from December 2027): SBOM, a vulnerability policy, security updates, a contact.
- [ ] **R08** European Accessibility Act (applied since June 2025): the front-accessibility rules as a company's evidence.
- [ ] **R09** The OpenSSF Best Practices badge's questionnaire pre-filled from the findings.
- [ ] **R10** Each security rule traced to its OWASP cheat sheet, so a reviewer can follow every rule to its source.

### S · Trust, privacy and safety

- [ ] **S01** Static by default: no code of the scored repo ever runs (no setup.py, no `eslint.config.js`, no `conftest.py`). Scoring an untrusted repo is safe, which the study needs at scale.
- [ ] **S02** Hardened parsers: YAML alias bombs, deep nesting, huge JSON, path traversal through symlinks, linear-time regexes; limits on file size, file count, time and memory.
- [ ] **S03** Secrets never printed: snippets redacted (`ghp_****abcd`) in every output (terminal, JSON, SARIF, HTML, comments).
- [ ] **S04** Shareable reports: no absolute paths, user names or e-mail addresses.
- [ ] **S05** No telemetry, ever: only T-38's report, with consent and the exact lines shown, as v0.4.6 does; every later signal (U) goes through it.
- [ ] **S06** Reproducible: the report carries kiln's version, the grid's hash, the data's date and the commit; `kiln score --verify report.json` runs again and compares.
- [ ] **S07** Signed releases and data bundles (Sigstore, PyPI attestations; T-90's provenance).
- [ ] **S08** Network calls listed before they start, as the fixers' `network` flag does, and only with `--online` or `--deep`.
- [ ] **S09** Forge tokens borrowed from `gh` or `glab`, never stored, never printed.
- [ ] **S10** Every executable thing kiln runs pinned and hashed: packs (R) and tools (F).

### T · Measuring kiln score itself

- [ ] **T01** A quality sheet in each release note: scored rules, rules with a detector, median precision, recall on seeded faults, speed on the suite, crashes on the corpus.
- [ ] **T02** User effort measured: manual corrections needed per 100 corpus repos for a right score (target 0).
- [ ] **T03** The unclaimed-file rate on the corpus (target under 1 % outside docs and assets).
- [ ] **T04** Seniors' agreement (H) measured again each quarter.
- [ ] **T05** Does the score predict anything? Public repos' advisories and incidents against their score at the time: evidence for the launch's claim, or a humbling result to publish anyway.
- [ ] **T06** Does readability lower Claude's tokens? T-53's A/B test run again with the readability pillar's score as the variable.
- [ ] **T07** kiln, its generated repos and the reference repo at 100, visibly (T-90, T-130, T-134).

### U · What the grid doesn't know

- [ ] **U01** Every tracked file claimed by a fact (code, a known tool's config, docs, asset, data); the rest listed as "kiln doesn't know these", with counts.
- [ ] **U02** A fingerprint library as data, seeded from GitHub Linguist (languages, vendored and generated patterns), the SchemaStore catalogue (config names to tools), github/gitignore, endoflife.date's products, Renovate's managers (⚠ AGPL: facts only, no code), Dependabot's and OSV's ecosystems, the pre-commit hooks index (appendix D).
- [ ] **U03** `NOTABLE_PACKAGES` (28 names in `score.py` today) grown into data: the top packages of each registry with what they are, so the gap report names what matters ("celery: background tasks, 4 drafts, 0 scored") and still never a private name.
- [ ] **U04** Practices found but unclassified (a `scripts/backup.sh`, a `docs/runbook.md`, a `chaos/` folder), named so the grid can learn them.
- [ ] **U05** T-38's report (v0.4.6: stacks, notable packages, misfiring rules) also carries the kinds of unclaimed files (a config's name, never a path) and the corrections users made; the most reported become tickets first, counted by `/kiln:backlog`.
- [ ] **U06** Suggestions from the corpus ("repos like yours, Django with Celery and Nuxt, usually also have X"): association rules mined from the corpus as `assess` candidates, never findings.

### V · Docs, teaching and reach

- [ ] **V01** A web page per rule generated from its file (why, bad and good, the fix, sources, prevalence, precision, standards): the pages people land on when they search "pin GitHub Actions", one way to get known.
- [ ] **V02** The study (T-132) repeated every quarter: "the state of Django and Nuxt repos".
- [ ] **V03** A "kiln score" action on the GitHub Marketplace and a GitLab CI component.
- [ ] **V04** An honest comparison page: kiln score beside OpenSSF Scorecard, SonarQube, Codacy, DeepSource, Snyk, repolinter and the CHAOSS metrics; what each sees and what kiln adds (practices, fixes, Claude).
- [ ] **V05** A teacher's guide: a class's repos scored each week, a rubric per theme.
- [ ] **V06** An opt-in showcase of repos at 100, never a ranking of other people's repos by name.
- [ ] **V07** `kiln score` in the README demo's first ten seconds: the number, the potential, `kiln fix`, the number again.

## Part III · Rules

Each theme starts with the drafts that already exist (an `assess` rule without a detector, or a
scored rule whose detector misses things) and the detector that would let them count, then the
new rules. Rule IDs are proposals; `kiln grid lint` (G) has the last word on them.

### ST · Structure

- [ ] **ST01** `FEATURE-FOLDERS` (draft): layer folders (`models/`, `views/`, `services/`, `controllers/`) that each span several domains, found by clustering the import graph. L3≈ · fix J · trial.
- [ ] **ST02** `REPO-MAP` (scored, "to confirm" today): judged by REPO-MAP-FRESH below, so it stops being approximate. L1 · fix J.
- [ ] **ST03** `REPO-MAP-FRESH`: every path the root CLAUDE.md's map names exists, and every top-level folder appears in it. L1 · fix J · adopt.
- [ ] **ST04** `ROOT-TIDY`: about 25 entries at most at the root; scripts in `scripts/`, docs in `docs/`. L0 · fix J · trial.
- [ ] **ST05** `SRC-LAYOUT`: a Python library's package under `src/`, as PyPA recommends. L0 · fix J · trial.
- [ ] **ST06** `ONE-CONFIG-PER-TOOL`: a tool configured in one place (ruff in `pyproject.toml` and in `ruff.toml` is two truths). L1 · fix S · adopt.
- [ ] **ST07** `CONFIG-IN-PYPROJECT`: Python tools' settings gathered in `pyproject.toml` (setup.cfg, tox.ini, .coveragerc, pytest.ini, mypy.ini merged in). L1 · fix S · trial.
- [ ] **ST08** `NO-NESTED-REPOS`: no `.git` inside the tree except declared submodules. L0 · fix J · adopt.
- [ ] **ST09** `SHALLOW-TREE`: code no deeper than about six folders. L0 · ratchet · assess.
- [ ] **ST10** `SMALL-FOLDERS`: no code folder with more than about 50 files (assets, data, migrations aside). L0 · ratchet · assess.
- [ ] **ST11** `NO-GRAB-BAG-FILES`: no `utils.py`, `helpers.ts`, `misc.py` or `common.js` past about 200 lines; the name says nothing of what's inside. L0 · fix J · trial.
- [ ] **ST12** `NO-BARREL-FILES`: no `index.ts` re-exporting a whole folder (slower bundles and tests, one more hop for Claude). L2 · fix J · assess.
- [ ] **ST13** `NO-IMPORT-CYCLES`: no cycle between modules or packages. L3 · ratchet · trial.
- [ ] **ST14** `WORKSPACE-DECLARED`: more than two components of one ecosystem are declared in a workspace (uv, pnpm). L1 · fix S · trial.
- [ ] **ST15** `GENERATED-MARKED`: generated files marked (`linguist-generated` or a header) so tools and Claude skip them. L1 · fix S · adopt.
- [ ] **ST16** `VENDORED-MARKED`: vendored code marked `linguist-vendored`. L1 · fix S · adopt.
- [ ] **ST17** `NO-BUILD-OUTPUT`: no `dist/`, `build/`, `.nuxt/`, `.output/`, `.next/`, `target/` or `*.egg-info` committed. L0 · fix S (untracked and ignored) · adopt.
- [ ] **ST18** `GITIGNORE-COMPLETE`: `.gitignore` covers the ecosystems present (virtualenvs, `node_modules`, caches, `.env`, coverage). L1 · fix S · adopt.
- [ ] **ST19** `EDITORCONFIG`: an `.editorconfig` consistent with the formatters. L0 · fix S · trial.
- [ ] **ST20** `LINE-ENDINGS`: `.gitattributes` with `* text=auto eol=lf`. L1 · fix S · trial.
- [ ] **ST21** `ONE-TEST-LAYOUT`: tests either beside the code or in a mirrored tree, one convention per component. L0≈ · fix J · assess.
- [ ] **ST22** `ENTRY-POINTS-NAMED`: an app's entry points (`manage.py`, `main.py`, `server/index.ts`) where a reader expects them, and named in the map. L0≈ · fix J · assess.

### CS · Code standards

- [ ] **CS01** `FILE-SIZE` (draft): lines per file from the index, generated code and migrations aside, a ratchet from today's numbers. L0 · ratchet · trial.
- [ ] **CS02** `FUNCTION-SIZE` (draft): function length from syntax trees in any language (ruff's PLR0915 for Python). L2 · ratchet · trial.
- [ ] **CS03** `CASE` (draft): symbols cased as their language wants (pep8-naming through ruff's N8, typescript-eslint's naming convention), from symbol tables. L2 · fix J · trial.
- [ ] **CS04** `BOOLEANS` (draft): names of `bool`-typed values start with is, has, can or should (Python annotations, TS types). L2 · fix J · assess.
- [ ] **CS05** `GENERIC-NAMES` (draft): identifiers from a deny-list (`data`, `res`, `tmp`, `obj`, `val`, `info`, `item`, `stuff`, `foo`), one list per human language. L2≈ · fix J · trial.
- [ ] **CS06** `MODERN-PYTHON` (draft): ruff's UP rules at the `requires-python` target; ruff's fixes are the converter. L4 · fix S · adopt.
- [ ] **CS07** `MODERN-VUE` (draft): `<script setup>`, no Options API in new files, `defineModel`, no `this.$`. L2 · fix J · trial.
- [ ] **CS08** `ONE-CLASS` (draft): one public class per file in Python and TS. L2 · fix J · assess.
- [ ] **CS09** `DEAD-CODE` (trial): vulture and knip, promoted once their precision is measured on the corpus. L4≈ · fix S (the compressor) · trial.
- [ ] **CS10** `EXPLICIT-IMPORTS` (draft, Nuxt): auto-imported composables used without an import, counted. L2 · fix S · assess.
- [ ] **CS11** `RETURN-VALUES` (draft): functions that return a value on some paths and nothing on others (ruff's RET503). L4 · fix J · trial.
- [ ] **CS12** `ASYNC-AWAIT` (draft, TS): `.then()` chains where `await` reads better; floating promises with `--deep`, since they need types. L2 · fix J · assess.
- [ ] **CS13** `NO-MAGIC-VALUES` (draft): ruff's PLR2004 and its JS counterpart. L4 · fix J · trial.
- [ ] **CS14** `DOMAIN-VOCABULARY` (draft): the glossary's words used (a `docs/glossary.md` checked against identifiers). L2≈ · fix J · assess.
- [ ] **CS15** `FORMATTER`: a formatter configured for each language, as `PYTHON-LINTER` and `JS-LINTER` ask a linter (ruff format or Black, Prettier or Biome, gofmt, rustfmt, Spotless, `dotnet format`, RuboCop, PHP-CS-Fixer). L1 · fix S · adopt.
- [ ] **CS16** `FORMATTED`: the code really is formatted (`ruff format --check` and the other formatters shipped as wheels). L4 · fix S · adopt.
- [ ] **CS17** `LINTER-CLEAN`: the repo's own linter config passes, or its error count only goes down. L4 · ratchet · trial.
- [ ] **CS18** `NO-DEBUGGER`: no `breakpoint()`, `pdb.set_trace()`, `debugger;`, `binding.pry` or `dd()`. L2 · fix S · adopt.
- [ ] **CS19** `NO-PRINT-DEBUG`: no `print()` or `console.log` in shipped code (ruff's T20, no-console), command-line tools aside. L2 · fix J · adopt.
- [ ] **CS20** `TODO-WITH-TICKET`: each TODO or FIXME cites a ticket (`T-12`, `#123`); the backlog is the only list. L2 · ratchet · trial.
- [ ] **CS21** `NO-COMMENTED-CODE`: no code left commented out (ruff's ERA001). L4 · fix S · trial.
- [ ] **CS22** `NO-MUTABLE-DEFAULTS` (Python): ruff's B006. L4 · fix S · adopt.
- [ ] **CS23** `NO-STAR-IMPORTS` (Python): F403, settings modules aside. L4 · fix J · adopt.
- [ ] **CS24** `NO-SILENT-EXCEPT`: no `except Exception: pass` or empty `catch {}` (S110, BLE001, no-empty), beyond `BARE-EXCEPT`. L4 · fix J · adopt.
- [ ] **CS25** `EXCEPTION-CHAINING`: `raise … from err` inside `except` (B904). L4 · fix S · adopt.
- [ ] **CS26** `NO-ASSERT-FOR-CHECKS`: no `assert` doing validation in shipped Python (S101); `-O` removes them. L4 · fix J · trial.
- [ ] **CS27** `PATHLIB`: `pathlib` rather than `os.path` (ruff's PTH). L4 · fix S · trial.
- [ ] **CS28** `COMPLEXITY`: cognitive complexity under about 15 per function. L2 · ratchet · trial.
- [ ] **CS29** `PARAMETER-COUNT`: five parameters at most, keyword-only past that (PLR0913). L4 · fix J · trial.
- [ ] **CS30** `NESTING-DEPTH`: four levels of nesting at most. L2 · ratchet · trial.
- [ ] **CS31** `DUPLICATION`: no duplicated block over about 50 tokens across files (the charter's `identical-copies`, generalized). L3 · ratchet · trial.
- [ ] **CS32** `NO-GLOBAL-MUTATION`: no `global` statements, no module-level state changed by functions. L2 · fix J · trial.
- [ ] **CS33** `NAMES-WITH-UNITS`: durations, sizes and amounts named with their unit (`timeout_seconds`, `size_bytes`). L2≈ · fix J · assess.
- [ ] **CS34** `FILE-NAMES-CASE`: file names in the language's convention (snake_case.py, PascalCase.vue components, kebab-case routes). L0 · fix J · trial.
- [ ] **CS35** `VUE-MULTI-WORD-COMPONENTS`: component names of two words or more (Vue's style guide, essential). L0 · fix J · adopt.
- [ ] **CS36** `TS-NO-NON-NULL-ASSERTION`: `!` assertions counted. L2 · ratchet · trial.
- [ ] **CS37** `TS-NO-ENUMS`: `as const` unions rather than `enum` (erasable syntax, which Node's type stripping runs). L2 · fix S · assess.
- [ ] **CS38** `ESM`: `"type": "module"` and no `require()` in TypeScript. L1 · fix J · trial.
- [ ] **CS39** `NO-VAR` and `STRICT-EQUALITY` (JS): `let` and `const`, `===`. L2 · fix S · adopt.
- [ ] **CS40** `SHELL-STRICT-MODE`: shell scripts start with `set -euo pipefail`, or say why not. L1 · fix S · adopt.
- [ ] **CS41** `SHELLCHECK-CLEAN`: shellcheck passes on every script. L4 · fix J · adopt.
- [ ] **CS42** `UTF8-SOURCES`: text files in UTF-8 without a BOM. L1 · fix S · adopt.
- [ ] **CS43** `NO-MIXED-INDENTATION`: tabs and spaces never mixed in one file. L1 · fix S · adopt.
- [ ] **CS44** `NO-NESTED-TERNARY`. L2 · fix J · trial.
- [ ] **CS45** `TYPOS`: no common misspelling in identifiers and comments (the typos dictionary). L4 · fix S · trial.

### AT · API, contracts and typing

- [ ] **AT01** `OPENAPI-IN-REPO` (draft): the API's schema committed (`openapi.json` or `.yaml`) when an API framework is present (Django Ninja, DRF, FastAPI, NestJS). L0 · fix J · trial.
- [ ] **AT02** `FROZEN-CONTRACT` (draft): CI compares the schema with the integration branch's (oasdiff's breaking-change check). L1 · fix S (the CI step) · trial.
- [ ] **AT03** `CONTRACT-DRIFT` (draft): front types generated from the committed schema (openapi-typescript or the like) with a script to regenerate them; `--deep` proves there's no drift. L1 · fix J · trial.
- [ ] **AT04** `TYPED-API` (draft, Ninja): every route has typed input and output schemas. L2 · fix J · trial.
- [ ] **AT05** `PAGINATION` (draft): list endpoints paginated (`@paginate`, DRF's `DEFAULT_PAGINATION_CLASS`). L2 · fix J · trial.
- [ ] **AT06** `DEPRECATION-HEADERS` (draft): deprecated routes send `Deprecation` (RFC 9745) and `Sunset` (RFC 8594). L2≈ · fix J · assess.
- [ ] **AT07** `IDEMPOTENCY` (draft): payment and creation endpoints accept an `Idempotency-Key`. L2≈ · fix J · assess.
- [ ] **AT08** `STRICT-TYPING` and `STRICT-TS` (scored): config read with its inheritance (`extends` chains, `[tool.mypy]` anywhere), not by one regex.
- [ ] **AT09** `TYPE-CHECK-IN-CI`: a type checker runs in CI (mypy, pyright, ty or pyrefly; tsc, vue-tsc or `nuxi typecheck`). L1 · fix S · adopt.
- [ ] **AT10** `PY-TYPED`: a typed Python library ships `py.typed`. L0 · fix S · adopt.
- [ ] **AT11** `ANNOTATIONS-COVERAGE`: the share of fully annotated functions, a ratchet (ruff's ANN counts). L4 · ratchet · trial.
- [ ] **AT12** `NO-EXPLICIT-ANY` (Python): `Any` counted (ANN401), as NO-ANY does for TS. L4 · ratchet · trial.
- [ ] **AT13** `TS-UNCHECKED-INDEX`: `noUncheckedIndexedAccess` on. L1 · fix S · trial.
- [ ] **AT14** `TS-EXACT-OPTIONAL`: `exactOptionalPropertyTypes` on. L1 · fix J · assess.
- [ ] **AT15** `TS-VERBATIM-MODULES`: `verbatimModuleSyntax` on. L1 · fix S · assess.
- [ ] **AT16** `DJANGO-STUBS`: django-stubs and its mypy plugin whenever mypy checks Django code. L1 · fix S · adopt.
- [ ] **AT17** `PROBLEM-DETAILS`: API errors as RFC 9457 problem details. L2≈ · fix J · assess.
- [ ] **AT18** `API-VERSIONED`: public APIs carry a version, in the path or a header. L2≈ · fix J · assess.
- [ ] **AT19** `OPENAPI-LINT`: the committed schema passes Spectral or Redocly's lint. L4 · fix J · trial.
- [ ] **AT20** `GENERATED-CLIENT`: the front reaches the API through generated types, never hand-copied ones. L2≈ · fix J · trial.
- [ ] **AT21** `TYPED-PROPS`: `defineProps<…>()` and `defineEmits<…>()` typed. L2 · fix J · adopt.
- [ ] **AT22** `RUNTIME-SCHEMAS`: outside data parsed by a schema library (Pydantic, Zod, Valibot) at the edge. L2≈ · fix J · trial.
- [ ] **AT23** `GRAPHQL-SCHEMA`: the GraphQL schema committed and checked for breaking changes. L1 · fix J · trial.
- [ ] **AT24** `PROTO-LINT`: `buf lint` and `buf breaking` for Protobuf APIs. L1 · fix S · trial.
- [ ] **AT25** `CSHARP-NULLABLE`: `<Nullable>enable</Nullable>` in every project. L1 · fix S · adopt.
- [ ] **AT26** `PHPSTAN-LEVEL`: PHPStan at level 6 or higher, or Psalm's equivalent. L1 · ratchet · trial.
- [ ] **AT27** `KOTLIN-EXPLICIT-API`: explicit API mode for Kotlin libraries. L1 · fix S · trial.
- [ ] **AT28** `JAVA-NULLNESS`: JSpecify annotations checked by NullAway. L1 · fix J · assess.
- [ ] **AT29** `SETTINGS-TYPED`: application settings parsed into a typed object (pydantic-settings, a schema-checked runtime config). L2≈ · fix J · trial.

### AR · Architecture

- [ ] **AR01** `NO-SIGNALS` (draft, Django): `@receiver` and model signals' `.connect(`; the charter already bans them. L2 · fix J · adopt.
- [ ] **AR02** `API-CALLS` (draft, Vue): no `$fetch` or `useFetch` in components outside a composable or a service layer. L2 · fix J · trial.
- [ ] **AR03** `THIN-VIEWS` (draft, Django): views under a few dozen lines, without ORM writes. L2≈ · fix J · trial.
- [ ] **AR04** `THIN-MODEL` (draft, Django): model methods past a few dozen lines flagged. L2≈ · fix J · assess.
- [ ] **AR05** `SERVICE-LAYER` (draft): an app whose views write data has a services module. L2≈ · fix J · assess.
- [ ] **AR06** `LAYERED-ARCHITECTURE` (draft): import contracts declared (import-linter, dependency-cruiser, eslint-plugin-boundaries) and run in CI. L1 · fix J · trial.
- [ ] **AR07** `SEALED-DOMAIN` (draft): domain packages import no web framework, HTTP client or ORM session. L3 · fix J · trial.
- [ ] **AR08** `TWELVE-FACTOR-CONFIG`: config from the environment, one settings tree, no per-environment file holding secrets. L2 · fix J · adopt.
- [ ] **AR09** `NO-GOD-MODULES`: no module both large and imported by most of the code. L3 · ratchet · assess.
- [ ] **AR10** `ADR`: decisions recorded (`docs/adr/` or `docs/decisions/`), for company profiles. L0 · fix S (folder and template) · assess.
- [ ] **AR11** `ARCHITECTURE-DIAGRAM`: a diagram as code (Mermaid, Structurizr) for repos with several services. L1 · fix J · assess.
- [ ] **AR12** `STATE-IN-STORES` (Vue): shared state in Pinia stores, not module-level `reactive()` singletons. L2 · fix J · trial.
- [ ] **AR13** `NUXT-SERVER-THIN`: `server/api` handlers delegate to services. L2≈ · fix J · assess.
- [ ] **AR14** `ONE-DB-PER-SERVICE`: two services don't share one database's tables (compose and settings read together). L1≈ · fix J · assess.
- [ ] **AR15** `ASYNC-BOUNDARY` (Django): async views never call the sync ORM without `sync_to_async`. L2 · fix J · adopt.
- [ ] **AR16** `DEPENDENCY-DIRECTION`: stable packages don't depend on volatile ones (fan-in and fan-out). L3 · ratchet · assess.
- [ ] **AR17** `NO-CIRCULAR-APPS` (Django): no import cycle between apps. L3 · fix J · trial.
- [ ] **AR18** `FLAGS-IN-ONE-PLACE`: feature flags read through one module or library, not scattered `if settings.X`. L2≈ · fix J · assess.

### DM · Data and migrations

- [ ] **DM01** `MIGRATIONS` (scored): apps with an empty `models.py`, and apps under `tests/`, no longer asked for migrations.
- [ ] **DM02** `COMMON-FIELDS` (draft, Django): models inherit a base carrying `created_at` and `updated_at`. L2 · fix J · trial.
- [ ] **DM03** `INDEXES` (draft, Postgres): fields filtered or ordered on in querysets have an index. L3≈ · fix J · assess.
- [ ] **DM04** `TRANSACTIONS` (draft): views writing several rows do it in `transaction.atomic` (or `ATOMIC_REQUESTS`). L2≈ · fix J · trial.
- [ ] **DM05** `USE-TZ` (Django): `USE_TZ = True`. L2 · fix S · adopt.
- [ ] **DM06** `REVERSIBLE-MIGRATIONS`: `RunPython` with `reverse_code`, `RunSQL` with `reverse_sql`. L2 · fix J · adopt.
- [ ] **DM07** `SAFE-MIGRATIONS`: no NOT NULL column added without a default to an existing table; indexes built concurrently on Postgres (`AddIndexConcurrently`, `atomic = False`). L2≈ · fix J · trial.
- [ ] **DM08** `SCHEMA-AND-DATA-APART`: data migrations (`RunPython`) in their own files. L2 · fix J · trial.
- [ ] **DM09** `MIGRATION-LINT-IN-CI`: django-migration-linter or squawk in CI. L1 · fix S · trial.
- [ ] **DM10** `MIGRATION-NAMES`: no `00xx_auto_<date>`: a migration's name says what it changes. L0 · fix J · trial.
- [ ] **DM11** `SQUASH-WHEN-LONG`: an app past about 100 migrations gets them squashed. L0 · fix J · assess.
- [ ] **DM12** `ALEMBIC-ONE-HEAD`: a single head in Alembic's history. L2 · fix J · adopt.
- [ ] **DM13** `NO-DUMPS`: no `.sql`, `.dump` or `.sqlite3` holding real data committed. L0 · fix S (untracked) · adopt.
- [ ] **DM14** `DB-CONSTRAINTS`: invariants enforced by the database (`UniqueConstraint`, `CheckConstraint`), not only in code. L2≈ · fix J · trial.
- [ ] **DM15** `PUBLIC-IDS`: public identifiers that aren't sequential integers (UUIDv7, ULID), so nobody can enumerate them. L2≈ · fix J · assess.
- [ ] **DM16** `CONN-REUSE` (Django): `CONN_MAX_AGE` and `CONN_HEALTH_CHECKS` set, or a pooler. L2 · fix S · trial.
- [ ] **DM17** `SUPPORTED-DATABASES`: Postgres, MySQL, Redis and MongoDB versions in compose and manifests still supported. L1 · fix S · adopt.
- [ ] **DM18** `ORM-MIGRATIONS-COMMITTED` (JS, Ruby): Prisma, Drizzle, Knex, TypeORM and Rails migrations (and `schema.rb`) committed. L0 · fix J · adopt.
- [ ] **DM19** `SEED-DATA`: a seed command or fixtures with fake data for local development. L0≈ · fix J · trial.
- [ ] **DM20** `QUERIES-OUT-OF-VIEWS`: raw SQL lives in a query module, not in views. L2 · fix J · assess.

### BG · Background tasks

- [ ] **BG01** `RETRIES` (draft): Celery tasks set `autoretry_for`, `retry_backoff` and `max_retries` (or the same in RQ, Dramatiq, Django 6's tasks). L2 · fix J · trial.
- [ ] **BG02** `OUT-OF-REQUEST` (draft): e-mails, webhooks and slow HTTP calls never sent inside a view. L2≈ · fix J · trial.
- [ ] **BG03** `TRANSACTIONAL-OUTBOX` (draft): tasks queued through `transaction.on_commit`, not inside an open transaction. L2≈ · fix J · trial.
- [ ] **BG04** `IDEMPOTENT-HANDLER` (draft): tasks guarded by a key or a state check. L2≈ · fix J · assess.
- [ ] **BG05** `TASK-TIME-LIMITS`: hard and soft time limits set. L2 · fix S · adopt.
- [ ] **BG06** `ACKS-LATE`: `task_acks_late` with `task_reject_on_worker_lost` for idempotent tasks. L2 · fix S · trial.
- [ ] **BG07** `SAFE-SERIALIZER`: tasks serialized as JSON, never pickle. L2 · fix S · adopt.
- [ ] **BG08** `ONE-SCHEDULER`: the beat or scheduler service runs as a single replica. L1 · fix J · adopt.
- [ ] **BG09** `TASKS-TAKE-IDS`: tasks receive identifiers, not model instances. L2≈ · fix J · trial.
- [ ] **BG10** `SCHEDULES-IN-CODE`: periodic jobs declared in code (beat schedule, django-q2), not in a host's crontab. L1≈ · fix J · trial.
- [ ] **BG11** `WORKER-HEALTH`: worker services have a health check and a stop grace period. L1 · fix S · trial.
- [ ] **BG12** `VISIBILITY-TIMEOUT`: with a Redis broker, the visibility timeout exceeds the longest task. L2 · fix J · trial.
- [ ] **BG13** `DEAD-LETTERS`: failed tasks land where a human sees them. L2≈ · fix J · assess.

### CC · Concurrency

- [ ] **CC01** `ATOMIC-INCREMENTS` (draft, Django): `x.n += 1` then `x.save()` becomes `F("n") + 1`. L2≈ · fix S · trial.
- [ ] **CC02** `LOCKS` (draft): a read-modify-write inside a transaction uses `select_for_update()`. L2≈ · fix J · trial.
- [ ] **CC03** `NO-BLOCKING-IN-ASYNC`: no `time.sleep`, `requests`, sync file or ORM call inside `async def` (ruff's ASYNC). L4 · fix J · adopt.
- [ ] **CC04** `TIMEOUTS`: every outgoing HTTP call has a timeout (ruff's S113; fetch with a signal, axios with `timeout`). L2 · fix S · adopt.
- [ ] **CC05** `DB-STATEMENT-TIMEOUT`: the database connection sets a statement timeout. L2 · fix S · trial.
- [ ] **CC06** `CHECK-THEN-ACT`: `if not exists(): create()` becomes `get_or_create` over a unique constraint. L2≈ · fix J · trial.
- [ ] **CC07** `ASGI-SERVER`: an async app served by an ASGI server (Uvicorn, Granian, Hypercorn, Daphne). L1 · fix J · adopt.
- [ ] **CC08** `WORKERS-SIZED`: the web server's worker count comes from the environment or the CPU count. L1 · fix S · trial.
- [ ] **CC09** `GO-RACE`: `go test -race` in CI. L1 · fix S · adopt.
- [ ] **CC10** `NO-THREADS-IN-REQUESTS`: no thread started inside a request handler. L2≈ · fix J · trial.
- [ ] **CC11** `RUST-NO-STATIC-MUT`: no `static mut`. L2 · fix J · adopt.

### CA · Cache

- [ ] **CA01** `CACHE-TAGS` (draft): invalidation by tags or versioned keys, never by guessing. L2≈ · fix J · assess.
- [ ] **CA02** `CACHE-STAMPEDE` (draft): expensive recomputations protected (a lock, early refresh, jitter). L2≈ · fix J · assess.
- [ ] **CA03** `PROD-CACHE-BACKEND`: the production cache isn't `LocMemCache` or a dummy backend. L2 · fix J · adopt.
- [ ] **CA04** `EXPLICIT-TIMEOUTS`: every `cache.set` gives a timeout. L2 · fix J · trial.
- [ ] **CA05** `IMMUTABLE-ASSETS`: hashed static assets served with `immutable` and a long max-age (Caddy, nginx, Nuxt's `routeRules`). L1 · fix S · trial.
- [ ] **CA06** `PRIVATE-RESPONSES`: authenticated responses are `private` or `no-store`; shared caches vary on authentication. L2≈ · fix J · trial.
- [ ] **CA07** `REDIS-EVICTION`: Redis runs with `maxmemory` and the eviction policy its use needs (a cache evicts, a broker never does). L1 · fix S · trial.

### EL · Errors and logs

- [ ] **EL01** `STRUCTURED-LOGGING` (draft): structlog or a JSON formatter configured; the charter's `logging` ban promoted. L1 · fix J · trial.
- [ ] **EL02** `DOMAIN-ERRORS` (draft): an exception hierarchy per domain, mapped to HTTP in one place. L2≈ · fix J · assess.
- [ ] **EL03** `ERROR-TRACKING`: Sentry, GlitchTip, Rollbar or Honeybadger configured, for production profiles. L1 · fix J · trial.
- [ ] **EL04** `NO-PII-TO-TRACKER`: `send_default_pii=False` and scrubbing configured. L2 · fix S · adopt.
- [ ] **EL05** `LOGS-TO-STDOUT`: in containers, logs go to stdout, no file handler. L2 · fix J · adopt.
- [ ] **EL06** `LOG-LEVEL-FROM-ENV`. L2 · fix S · trial.
- [ ] **EL07** `LOG-EXCEPTIONS-WITH-TRACE`: `logger.exception` in handlers rather than `logger.error(str(e))` (TRY400). L4 · fix S · adopt.
- [ ] **EL08** `LAZY-LOG-FORMAT`: no f-strings in log calls (G004); key-value pairs with structlog. L4 · fix S · trial.
- [ ] **EL09** `NO-SECRETS-IN-LOGS`: no `password`, `token`, `secret` or `authorization` values passed to a log call. L2 · fix J · adopt.
- [ ] **EL10** `NO-STACK-TRACES-SHOWN`: production error pages hide internals (Django's `DEBUG`, Express's `NODE_ENV`, Nuxt's error page, Spring's `include-stacktrace`). L2 · fix J · adopt.
- [ ] **EL11** `UNHANDLED-REJECTIONS` (Node): a process-level handler that logs and exits. L2 · fix J · trial.
- [ ] **EL12** `GO-ERROR-WRAPPING`: `fmt.Errorf("…: %w", err)`. L2 · fix J · trial.

### AS · Application security

- [ ] **AS01** `SECRETS` (draft): the secrets themselves in tracked files (provider patterns, checksum-verified tokens, entropy last), where `SECRET-SCAN` checks that a scan runs and `NO-TRACKED-ENV` that no `.env` is tracked; critical: it caps the score at 49. L2 · fix J (rotate, then remove) · adopt.
- [ ] **AS02** `SESSION-COOKIES` (draft, Django): `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` and `SAMESITE` in the production settings, evaluated statically. L2 · fix S · adopt.
- [ ] **AS03** `SECURITY-HEADERS` (draft): HSTS of a year or more, `nosniff`, frames denied, a referrer policy; in Django's settings, the reverse proxy (Caddy, nginx) or Nuxt (nuxt-security). L2 · fix S · adopt.
- [ ] **AS04** `CSP-NONCE` (draft): a Content Security Policy with nonces (Django 6.0's built-in CSP, django-csp, nuxt-security), no `unsafe-inline` for scripts. L2 · fix J · trial.
- [ ] **AS05** `CONSTANT-TIME` (draft): secrets compared with `hmac.compare_digest` or `crypto.timingSafeEqual`, never `==` on names like token, signature or digest; the charter's ban promoted. L2 · fix S · adopt.
- [ ] **AS06** `EXPLICIT-PERMISSIONS` (draft): every route states its authentication (Ninja's `auth=`, DRF's `permission_classes`), and the default isn't `AllowAny`. L2 · fix J · adopt.
- [ ] **AS07** `PUBLIC-ROUTES` (draft): public routes listed in one place, everything else authenticated by default. L2≈ · fix J · trial.
- [ ] **AS08** `UPLOADS` (draft): uploads validated (size limits, type by content, storage outside the web root, random names). L2≈ · fix J · trial.
- [ ] **AS09** `SUBRESOURCE-INTEGRITY` (draft): `<script>` and `<link>` from another origin carry `integrity`. L2 · fix S (hash computed online) · adopt.
- [ ] **AS10** `ENCRYPTION` (draft): sensitive fields encrypted at rest. L2≈ · fix J · assess.
- [ ] **AS11** `ROW-LEVEL-SECURITY` (draft, Postgres): RLS policies in migrations for multi-tenant tables. L2≈ · fix J · assess.
- [ ] **AS12** `SECRET-ROTATION` (draft): forge secrets older than a year (M). L6 · fix J · trial.
- [ ] **AS13** `VALIDATE-AT-BOUNDARIES` (draft): request data parsed by a schema before use. L2≈ · fix J · trial.
- [ ] **AS14** `NO-EVAL`: no `eval`, `exec`, `new Function` or string `setTimeout`. L2 · fix J · adopt.
- [ ] **AS15** `NO-SHELL-INJECTION`: no `shell=True` or `os.system` on non-literal input, no `child_process.exec` with template strings (S602 to S605). L2 · fix J · adopt.
- [ ] **AS16** `NO-UNSAFE-DESERIALIZATION`: no pickle, marshal, `yaml.load`, `ObjectInputStream` or `unserialize` on outside data (S301, S506). L2 · fix S (`yaml.safe_load`) · adopt.
- [ ] **AS17** `NO-XXE`: XML parsed with defusedxml or safe defaults (S313 to S320). L4 · fix S · adopt.
- [ ] **AS18** `NO-WEAK-CRYPTO`: no MD5 or SHA-1 for security, no DES, RC4 or ECB (S324, S303 to S305). L4 · fix J · adopt.
- [ ] **AS19** `SECURE-RANDOM`: tokens from `secrets` or `crypto.randomUUID`, never `random` or `Math.random` (S311). L2 · fix S · adopt.
- [ ] **AS20** `NO-HARDCODED-PASSWORDS`: S105 to S107 and their JS counterparts. L4 · fix J · adopt.
- [ ] **AS21** `TLS-VERIFIED`: no `verify=False`, `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0` or `InsecureSkipVerify: true`. L2 · fix S · adopt.
- [ ] **AS22** `CSRF-ON`: CSRF middleware on; `@csrf_exempt` only with a justification marker. L2 · fix J · adopt.
- [ ] **AS23** `CORS-STRICT`: no allow-all origins with credentials (`CORS_ALLOW_ALL_ORIGINS`, `Access-Control-Allow-Origin: *`). L2 · fix J · adopt.
- [ ] **AS24** `PASSWORD-HASHING`: Argon2 or the framework's default first, never MD5, SHA-1 or unsalted hashers. L2 · fix S · adopt.
- [ ] **AS25** `PASSWORD-VALIDATORS`: `AUTH_PASSWORD_VALIDATORS` set, or a passkey-first login. L2 · fix S · adopt.
- [ ] **AS26** `PASSKEYS`: WebAuthn offered for accounts (allauth's MFA, SimpleWebAuthn). L2≈ · fix J · assess.
- [ ] **AS27** `ADMIN-MFA`: the admin asks for a second factor. L2≈ · fix J · trial.
- [ ] **AS28** `RATE-LIMITS`: login, password reset and the API rate-limited, in the app or the proxy. L2≈ · fix J · trial.
- [ ] **AS29** `NO-OPEN-REDIRECT`: redirects to a request value checked (`url_has_allowed_host_and_scheme`). L2 · fix J · adopt.
- [ ] **AS30** `NO-SSRF`: outgoing requests to user-given URLs pass an allowlist. L2≈ · fix J · trial.
- [ ] **AS31** `NO-PATH-TRAVERSAL`: files opened from request values resolved and confined. L2≈ · fix J · trial.
- [ ] **AS32** `NO-MASS-ASSIGNMENT`: no `fields = "__all__"` in ModelForms or serializers. L2 · fix J · adopt.
- [ ] **AS33** `AUTOESCAPE`: no `|safe`, `mark_safe`, `{% autoescape off %}`, `v-html` or `dangerouslySetInnerHTML` on variables (with NO-V-HTML). L2 · fix J · adopt.
- [ ] **AS34** `JWT-SAFE`: algorithms pinned (never `none`), signature and expiry checked. L2 · fix J · adopt.
- [ ] **AS35** `HTTPS-ONLY`: `SECURE_SSL_REDIRECT`, Caddy's automatic HTTPS, `force_ssl`. L2 · fix S · adopt.
- [ ] **AS36** `NO-SECRETS-IN-FRONT`: no secret-looking key under Nuxt's `runtimeConfig.public`, `NUXT_PUBLIC_*`, `VITE_*` or `NEXT_PUBLIC_*`. L2 · fix J · adopt.
- [ ] **AS37** `PRIVATE-SOURCEMAPS`: production source maps not served publicly. L2 · fix S · trial.
- [ ] **AS38** `DEV-TOOLS-DEV-ONLY`: debug toolbars and devtools only in development settings and dependency groups. L2 · fix S · adopt.
- [ ] **AS39** `SECURITY-TXT`: production web apps serve `/.well-known/security.txt` (RFC 9116). L0 · fix S · trial.
- [ ] **AS40** `SAST-IN-CI`: CodeQL, semgrep or the language's security linter in CI. L1 · fix S · adopt.
- [ ] **AS41** `ANDROID-MANIFEST`: not debuggable, no cleartext traffic, backups off, every component's `exported` explicit. L1 · fix S · adopt.
- [ ] **AS42** `IOS-ATS`: App Transport Security left on. L1 · fix J · adopt.
- [ ] **AS43** `ELECTRON-SAFE`: `contextIsolation` on, `nodeIntegration` off, `sandbox` on. L2 · fix S · adopt.
- [ ] **AS44** `EXTENSION-PERMISSIONS`: browser extensions ask for the fewest permissions and hosts. L1 · fix J · trial.
- [ ] **AS45** `FRAMEWORK-DEBUG-OFF`: `DJANGO-DEBUG-OFF` for the other frameworks: Laravel's `APP_DEBUG`, Rails' `consider_all_requests_local`, Flask's `debug=True`, Spring's Actuator exposing more than health and info. L2 · fix S · adopt.
- [ ] **AS46** `GRAPHQL-LIMITS`: depth and cost limits, introspection off in production. L2≈ · fix J · trial.
- [ ] **AS47** `EXPRESS-HARDENED`: Helmet or equivalent headers, `x-powered-by` off. L2 · fix S · trial.

### PD · Personal data

- [ ] **PD01** `PERSONAL-DATA` (draft): fields holding personal data (e-mail, phone, address, birth date, IBAN, IP) marked as the charter marks them; unmarked ones listed. L2 · fix J · trial.
- [ ] **PD02** `PII-INVENTORY`: an inventory of personal-data fields written from the models (`docs/personal-data.md`) and kept current by a script. L2 · fix S · trial.
- [ ] **PD03** `NO-REAL-PII-IN-FIXTURES`: fixtures and seeds hold fake data (real-looking e-mails on real domains, phone numbers flagged). L2 · fix J · adopt.
- [ ] **PD04** `NO-PII-IN-URLS`: no e-mail or name in query strings. L2≈ · fix J · trial.
- [ ] **PD05** `NO-PII-IN-LOGS`: personal fields passed to log calls (the charter's ban, promoted). L2 · fix J · adopt.
- [ ] **PD06** `RETENTION`: a job deletes or anonymizes data past its retention period. L2≈ · fix J · assess.
- [ ] **PD07** `DATA-EXPORT` and `ACCOUNT-DELETION`: users can get and delete their data (GDPR articles 15, 17 and 20), for profiles holding accounts in the EU. L2≈ · fix J · assess.
- [ ] **PD08** `CONSENT-BEFORE-TRACKING`: analytics and trackers load after consent, or are cookieless (Plausible, Matomo set so). L2 · fix J · trial.
- [ ] **PD09** `SELF-HOSTED-FONTS`: no fonts from Google's CDN (a German court awarded damages over it under the GDPR in 2022); `@nuxt/fonts` or local files. L2 · fix S · adopt (EU).
- [ ] **PD10** `SUBPROCESSORS-LISTED`: the third parties receiving data (Sentry, Stripe, a mail provider) listed from dependencies and settings, ready for the privacy policy. L1 · fix S · assess.
- [ ] **PD11** `MINIMIZATION`: personal fields read nowhere flagged for removal. L3≈ · fix J · assess.

### SU · Supply chain

- [ ] **SU01** `SBOM` (draft): an SBOM (CycloneDX or SPDX) made in the release workflow (syft, cdxgen, the package manager). L1 · fix S · trial.
- [ ] **SU02** `UNUSED-DEPENDENCIES` (trial): deptry and knip, promoted once precise. L4≈ · fix S · trial.
- [ ] **SU03** `NEW-DEPENDENCY` (draft): a dependency added on a branch gets a health card in the pull request (maintainers, age, downloads, licence, install scripts). L6 · fix J · trial.
- [ ] **SU04** `IMAGES-BY-DIGEST` (scored): extended to compose, Kubernetes, Helm values and CI images, with `ARG` defaults resolved.
- [ ] **SU05** `SUPPORTED-RUNTIMES` (scored): every runtime endoflife.date knows; an app judged on what it runs, a library's support floor shown as information.
- [ ] **SU06** `DEPENDENCY-UPDATES` (scored): every manifest folder covered by the bot's config, not merely "a config exists".
- [ ] **SU07** `LOCK-IN-SYNC`: every dependency of the manifest is in the lock's root with a matching constraint. L1 · fix S · adopt.
- [ ] **SU08** `FROZEN-INSTALL-IN-CI`: CI installs from the lock (`uv sync --locked`, `npm ci`, `pnpm install --frozen-lockfile`, `cargo build --locked`, `bundle install` frozen). L1 · fix S · adopt.
- [ ] **SU09** `FROZEN-INSTALL-IN-IMAGES`: Dockerfiles install from the lock too. L1 · fix S · adopt.
- [ ] **SU10** `NO-INSTALL-SCRIPTS`: npm lifecycle scripts off by default (`ignore-scripts`, pnpm's `onlyBuiltDependencies` allowlist, Bun's trusted dependencies); the 2025 npm worms spread through install scripts. L1 · fix S · adopt.
- [ ] **SU11** `ONE-INDEX`: Python packages from one index, no `--extra-index-url` (dependency confusion); uv's pinned indexes for private packages. L1 · fix S · adopt.
- [ ] **SU12** `GIT-DEPS-PINNED`: dependencies fetched from git pinned to a commit, never a branch. L1 · fix S (online) · adopt.
- [ ] **SU13** `MALICIOUS-PACKAGES`: no dependency known to be malicious (OSV's `MAL-`). L1 with data · fix J · adopt, critical.
- [ ] **SU14** `KNOWN-VULNERABILITIES`: no known critical or high vulnerability in the locked versions (OSV's batch query, or a cached database offline). L6 · fix S (bump within range) · adopt.
- [ ] **SU15** `ABANDONED-DEPENDENCIES`: no dependency deprecated, yanked, archived, or three years without a release with open security issues. L6 · fix J · trial.
- [ ] **SU16** `TYPOSQUAT-SUSPECTS`: dependencies one edit from a popular name, with few downloads. L6 · fix J · trial.
- [ ] **SU17** `DEPENDENCY-BUDGET`: the count of transitive dependencies tracked as a ratchet (the slimming pillar). L1 · ratchet · trial.
- [ ] **SU18** `NO-DUPLICATE-MAJORS`: one package in several major versions in a JS lock. L1 · fix S (dedupe) · trial.
- [ ] **SU19** `NO-DEPRECATED-PACKAGES`: a bundled list (`request`, `node-sass`, `tslint`, `moment`, `pytz`, `nose`, `six`, backports past their Python), joined with NO-OBSOLETE-BACKPORTS. L1 · fix S where a converter exists · adopt.
- [ ] **SU20** `PINNED-PRE-COMMIT`: pre-commit hooks pinned by commit (`autoupdate --freeze`). L1 · fix S · adopt.
- [ ] **SU21** `PINNED-TOOLS`: tools run through `npx`, `uvx`, `pipx run` or `go run` in CI and scripts carry a version. L1 · fix S · adopt.
- [ ] **SU22** `NO-CURL-PIPE-SHELL`: no `curl … | sh` in Dockerfiles, CI or setup scripts: download, verify, then run. L1 · fix J · adopt (review in READMEs).
- [ ] **SU23** `CHECKSUMS-FOR-DOWNLOADS`: binaries fetched in Dockerfiles and CI checked against a SHA-256. L1≈ · fix S (online) · trial.
- [ ] **SU24** `GRADLE-WRAPPER-VERIFIED`: `distributionSha256Sum` set and the wrapper validated in CI. L1 · fix S · adopt.
- [ ] **SU25** `RUNTIME-PINNED`: one runtime version named consistently in `.python-version` or `.nvmrc`, in CI and in images. L1 · fix S · adopt.
- [ ] **SU26** `PACKAGE-MANAGER-PINNED`: `packageManager` in package.json (corepack), uv's `required-version`. L1 · fix S · adopt.
- [ ] **SU27** `SUPPORTED-FRAMEWORKS`: Django, Vue, Nuxt, Angular, Rails, Laravel, Spring Boot and the rest on a supported line (Vue 2 and Nuxt 2 are past their end). L1 with data · fix J · adopt.
- [ ] **SU28** `SUPPORTED-BASE-IMAGES`: Alpine, Debian, Ubuntu and language images on supported versions (CURRENT-DEBIAN generalized). L1 · fix S · adopt.
- [ ] **SU29** `VENDORED-JS-VULNERABILITIES`: front-end libraries copied into static folders matched against retire.js's signatures. L1 · fix J · adopt.
- [ ] **SU30** `RUNTIME-NOT-LAGGING`: the runtime within its two newest supported lines, beyond "not past its end". L1 · fix S · trial.
- [ ] **SU31** `COOLDOWN-EVERYWHERE`: `UPDATE-COOLDOWN` also met where the package manager has one (pnpm's `minimumReleaseAge`, uv's `exclude-newer`), not only in the bot. L1 · fix S · trial.
- [ ] **SU32** `DEPENDABOT-GROUPED`: updates grouped to keep the noise down. L1 · fix S · trial.
- [ ] **SU33** `LOCKS-COMMITTED` (Go, Rust): `go.sum` and `Cargo.lock` committed. L0 · fix J · adopt.
- [ ] **SU34** `NO-HTTP-INDEXES`: package indexes and registries over HTTPS only (`.npmrc`, `pip.conf`, `uv.toml`, Maven's `settings.xml`). L1 · fix S · adopt.
- [ ] **SU35** `NO-TOKENS-IN-NPMRC`: no auth token in a committed `.npmrc` or `.pypirc`. L1 · fix J · adopt, critical.
- [ ] **SU36** `NO-BINARY-ARTIFACTS`: no executable, `.jar`, `.class`, `.dll` or wheel committed outside declared fixtures (Scorecard's Binary-Artifacts). L0 · fix J · adopt.
- [ ] **SU37** `REPRODUCIBLE-LOCK`: the lock still resolves today (no yanked version, no dead URL), with `--online`. L6 · fix S · trial.

### TE · Tests

- [ ] **TE01** `TESTS-PRESENT` (scored): per component, and a test file that collects nothing doesn't count (pytest's `--collect-only` with `--deep`).
- [ ] **TE02** `TESTS-IN-CI` (scored): read from the CI's commands for each component (pytest, Vitest, `go test`, `cargo test`, `mvn verify`), on any CI (C), through `make`, `just` and package scripts, not a regex for `pytest`.
- [ ] **TE03** `CLOCK` (draft): tests calling `now()`, `date.today()` or `Date.now()` with no time-machine, freezegun or `vi.useFakeTimers` in reach. L3≈ · fix J · trial.
- [ ] **TE04** `NO-NETWORK` (draft): sockets blocked in tests (pytest-socket's `--disable-socket`, msw with `onUnhandledRequest: "error"`, nock's `disableNetConnect`). L1 · fix S · trial.
- [ ] **TE05** `PROPERTY-TESTS` (draft): Hypothesis or fast-check where parsers, serializers or money code live, found by paths and names. L1≈ · fix J · assess.
- [ ] **TE06** `MUTATION-TESTS` (draft): mutmut, cosmic-ray or Stryker configured and scheduled. L1 · fix J · assess.
- [ ] **TE07** `API-FUZZING` (draft): Schemathesis run against the committed OpenAPI schema. L1 · fix S · trial.
- [ ] **TE08** `E2E-JOURNEYS` (draft): Playwright present, its specs naming the journeys the docs list. L1≈ · fix J · trial.
- [ ] **TE09** `PERMISSION-TESTS` (draft): each protected route (from the URL conf or Ninja's routers) has a test that calls it anonymously. L3≈ · fix J · trial.
- [ ] **TE10** `REGRESSION-TEST` (draft): `fix:` commits of the last hundred that touch no test, with `--history`. L5 · ratchet · trial.
- [ ] **TE11** `COVERAGE-MEASURED`: coverage with branches (`[tool.coverage.run] branch = true`, Vitest's coverage provider). L1 · fix S · adopt.
- [ ] **TE12** `COVERAGE-FLOOR`: a floor that only rises (`fail_under`, Vitest's thresholds with `autoUpdate`). L1 · ratchet · trial.
- [ ] **TE13** `DIFF-COVERAGE`: changed lines covered in pull requests (diff-cover). L1 · fix S · assess.
- [ ] **TE14** `PYTEST-STRICT`: `--strict-markers`, `--strict-config`, `xfail_strict = true`, warnings as errors with a named allow-list. L1 · fix S · adopt.
- [ ] **TE15** `NO-FOCUSED-TESTS`: no `.only`, `fit` or `fdescribe` committed. L2 · fix S · adopt.
- [ ] **TE16** `NO-SKIPPED-TESTS`: every `skip` and `xfail` gives a reason, and their count only goes down. L2 · ratchet · trial.
- [ ] **TE17** `NO-SLEEP-IN-TESTS`: no `time.sleep` or `setTimeout` waits; a frozen clock or polling instead. L2 · fix J · trial.
- [ ] **TE18** `RANDOM-ORDER`: tests run shuffled (pytest-randomly, Vitest's `sequence.shuffle`) so hidden coupling shows. L1 · fix S · trial.
- [ ] **TE19** `PARALLEL-TESTS`: pytest-xdist or the runner's workers, for suites over a minute. L1 · fix S · trial.
- [ ] **TE20** `ASSERTIONS-PRESENT`: no test without an assertion (`expect-expect` for Vitest and Jest, a syntax check for pytest). L2 · fix J · trial.
- [ ] **TE21** `FACTORIES`: factory_boy, model-bakery or fishery rather than big JSON fixtures. L1≈ · fix J · assess.
- [ ] **TE22** `PROD-ENGINE-IN-TESTS`: tests run on the production database engine (a Postgres service in CI, Testcontainers), not SQLite. L1 · fix J · trial.
- [ ] **TE23** `MIGRATIONS-CHECKED`: `makemigrations --check --dry-run` in CI, and a migration from an empty database. L1 · fix S · adopt.
- [ ] **TE24** `TESTS-TYPE-CHECKED`: tests not excluded from the type checker. L1 · fix S · trial.
- [ ] **TE25** `TEST-NAMES`: names that state the behaviour (`test_refuses_expired_token`), never `test_1` or `test_view`. L2≈ · fix J · assess.
- [ ] **TE26** `SNAPSHOTS-IN-CHECK`: obsolete snapshots fail in CI (`--ci`), snapshot files stay small. L1 · fix S · assess.
- [ ] **TE27** `CONTRACT-TESTS`: consumer-driven contracts (Pact) between the services of one organisation. L1 · fix J · assess.
- [ ] **TE28** `LOAD-SCENARIO`: a k6 or Locust scenario kept in the repo of an app with an SLO. L0 · fix J · assess.
- [ ] **TE29** `TEST-DURATION`: suite time and slowest tests read from the CI's JUnit reports with `--online`, as a ratchet. L6 · ratchet · assess.

### PE · Performance

- [ ] **PE01** `API-LATENCY` (draft): p95 budgets as k6 thresholds in the repo, or an APM's numbers with `--online`. L1≈ · fix J · assess.
- [ ] **PE02** `CORE-WEB-VITALS` (draft): Lighthouse CI with assertions (`lighthouserc`); field data from the Chrome UX Report's API with `--online`. L1 · fix S · trial.
- [ ] **PE03** `JS-BUDGET` (draft): size-limit or bundle budgets checked at build. L1 · fix S · trial.
- [ ] **PE04** `MODERN-IMAGES` (draft): committed JPEG and PNG over about 200 KB listed with their savings; `@nuxt/image` or `<picture>` present; `width`, `height` and `loading="lazy"` set below the fold. L2 · fix S (conversion) · trial.
- [ ] **PE05** `NO-N-PLUS-ONE`: querysets iterated with related access and no `select_related` or `prefetch_related` (L3≈), proven by nplusone in tests (L7). L3≈ · fix J · trial.
- [ ] **PE06** `QUERY-COUNT-TESTS`: list views tested with `django_assert_num_queries` or `assertNumQueries`. L2 · fix J · assess.
- [ ] **PE07** `COMPRESSION`: responses compressed (Caddy's `encode zstd gzip`, nginx's `gzip on`, the platform's). L1 · fix S · adopt.
- [ ] **PE08** `STATIC-BY-PROXY`: static files hashed and served by the proxy, WhiteNoise or a CDN (`ManifestStaticFilesStorage`), never by the framework's dev server. L2 · fix S · adopt.
- [ ] **PE09** `NO-SYNC-SCRIPTS`: third-party scripts `async` or `defer`, or loaded through Nuxt Scripts. L2 · fix S · adopt.
- [ ] **PE10** `FONT-LOADING`: `font-display` set, fonts subset and preloaded (`@nuxt/fonts` does all three). L2 · fix S · trial.
- [ ] **PE11** `TREE-SHAKEN-IMPORTS`: no whole-library imports (`import _ from "lodash"`, `import * as icons`). L2 · fix S · adopt.
- [ ] **PE12** `HEAVY-DEPENDENCIES`: moment, full lodash or `core-js` for modern targets, listed with lighter options (with `NO-DEPRECATED-PACKAGES`). L1 · fix J · trial.
- [ ] **PE13** `LAZY-COMPONENTS`: heavy components and routes loaded on demand (`defineAsyncComponent`, Nuxt's `Lazy` prefix, `React.lazy`). L2≈ · fix J · assess.
- [ ] **PE14** `FK-INDEXES`: foreign keys indexed where neither the ORM nor the database does it (Prisma's relations on Postgres, raw SQL migrations); Django already does. L2 · fix S · trial.
- [ ] **PE15** `CACHEABLE-PUBLIC-PAGES`: anonymous pages cacheable (Nuxt's `routeRules` with `swr` or `isr`, `Cache-Control` on public views). L2≈ · fix J · trial.
- [ ] **PE16** `BENCHMARKS`: libraries with hot paths keep benchmarks (pytest-benchmark, Vitest's `bench`, `cargo bench`) and a ratchet on them. L1 · fix J · assess.
- [ ] **PE17** `PROFILER-IN-DEV`: a profiler wired in development only (django-silk, pyinstrument's middleware). L1 · fix S · assess.
- [ ] **PE18** `IMAGE-SIZE-BUDGET`: the final container image's size tracked; `--deep` builds it. L7 · ratchet · assess.
- [ ] **PE19** `COLD-START`: serverless functions' bundle size tracked. L1 · ratchet · assess.

### FA · Front, accessibility and i18n

- [ ] **FA01** `ACCESSIBILITY` (draft): labels and accessible names checked in templates by eslint-plugin-vuejs-accessibility or jsx-a11y, run as mapped tools (F). L2 · fix J · adopt.
- [ ] **FA02** `AUTOMATED-ACCESSIBILITY` (draft): axe in Playwright tests (`@axe-core/playwright`) or pa11y-ci on the main pages. L1 · fix S · trial.
- [ ] **FA03** `UI-STATES` (draft): results of `useFetch` and `useAsyncData` whose `status` and `error` the template never reads. L2 · fix J · trial.
- [ ] **FA04** `UTILITY-CSS-FIRST` (draft): Tailwind or UnoCSS configured; `<style scoped>` blocks counted as a ratchet. L1 · ratchet · trial.
- [ ] **FA05** `HTML-LANG`: `lang` on `<html>` (Nuxt's `app.head.htmlAttrs`, `index.html`, the base template). L2 · fix S · adopt.
- [ ] **FA06** `IMG-ALT`: every image has `alt`, empty for decoration. L2 · fix J · adopt.
- [ ] **FA07** `CLICKABLE-ELEMENTS`: no click handler on a `div` or `span` without a role and a keyboard handler: a button or a link instead. L2 · fix J · adopt.
- [ ] **FA08** `FOCUS-VISIBLE`: no `outline: none` or `outline-0` without a `:focus-visible` style. L2 · fix J · adopt.
- [ ] **FA09** `REDUCED-MOTION`: animations respect `prefers-reduced-motion` (Tailwind's `motion-safe:`). L2 · fix S · trial.
- [ ] **FA10** `VIEWPORT-META`: `width=device-width`, never `user-scalable=no` or `maximum-scale=1`. L2 · fix S · adopt.
- [ ] **FA11** `NO-AUTOPLAY`: no media that plays sound by itself. L2 · fix S · adopt.
- [ ] **FA12** `SKIP-LINK`: a skip-to-content link in layouts. L2≈ · fix S · trial.
- [ ] **FA13** `ARIA-VALID`: ARIA roles and attributes valid and not redundant. L2 · fix J · adopt.
- [ ] **FA14** `HEADINGS-ORDER`: one `h1` per page, no skipped level. L3≈ · fix J · trial.
- [ ] **FA15** `FORM-AUTOCOMPLETE`: `autocomplete` on identity and address fields (WCAG 2.2, 1.3.5). L2 · fix S · trial.
- [ ] **FA16** `TOUCH-TARGETS`: targets of 24 by 24 CSS pixels at least (WCAG 2.2, 2.5.8), read from utility classes. L3≈ · fix J · assess.
- [ ] **FA17** `COLOR-CONTRAST`: the theme's text and background pairs computed from its tokens; axe for the rendered rest. L3≈ · fix J · trial.
- [ ] **FA18** `EU-ACCESSIBILITY-ACT`: for businesses selling to consumers in the EU, the European Accessibility Act applies since 28 June 2025: in that profile the accessibility rules move to `adopt`, and an accessibility statement exists. L0 · fix J · adopt (profile).
- [ ] **FA19** `VUE-V-FOR-KEY`: `:key` on every `v-for`. L2 · fix J · adopt.
- [ ] **FA20** `VUE-NO-V-IF-WITH-V-FOR`. L2 · fix J · adopt.
- [ ] **FA21** `SSR-SAFE`: no `window`, `document` or `localStorage` at setup outside `onMounted`, `import.meta.client` or `<ClientOnly>`. L2 · fix J · adopt.
- [ ] **FA22** `HYDRATION-SAFE`: no `Math.random()`, `Date.now()` or locale formatting rendered on both sides without a stable value (`useState`, `useId`). L2≈ · fix J · trial.
- [ ] **FA23** `SEO-BASICS`: title, description, canonical URL, `robots.txt` and a sitemap on public sites (`useSeoMeta`, `@nuxtjs/sitemap`). L2 · fix S · trial.
- [ ] **FA24** `SOCIAL-CARDS`: Open Graph title and image on the pages people share. L2 · fix S · assess.
- [ ] **FA25** `CSS-LINT`: Stylelint where CSS is written by hand. L1 · fix S · trial.
- [ ] **FA26** `ERROR-PAGES`: designed 404 and 500 pages (Nuxt's `error.vue`, Django's `404.html` and `500.html`). L0 · fix S · trial.
- [ ] **FA27** `I18N-KEYS-COMPLETE`: every locale has every key and no key is unused (vue-i18n-extract, `makemessages` compared). L3 · fix S · adopt.
- [ ] **FA28** `I18N-NO-BARE-TEXT`: user-facing text in templates goes through the i18n layer once one is configured (`@intlify/vue-i18n/no-raw-text`). L2 · ratchet · trial.
- [ ] **FA29** `LOCALE-FORMATTING`: dates, numbers and currencies through `Intl` or the framework's filters, never concatenated by hand. L2≈ · fix J · assess.
- [ ] **FA30** `RTL-READY`: logical CSS properties once a right-to-left locale is configured. L2 · fix S · assess.
- [ ] **FA31** `WEB-MANIFEST`: icons and a web manifest for installable apps. L0 · fix S · assess.

### CO · Containers

- [ ] **CO01** `NON-ROOT-CONTAINERS` (scored): the final stage's `USER`, not the file's last one; a numeric UID so Kubernetes' `runAsNonRoot` can check it; compose's `user:` counted.
- [ ] **CO02** `HARDENED-CONTAINERS` (scored): also read in Kubernetes manifests and Helm values (`securityContext`, see IN).
- [ ] **CO03** `CURRENT-DEBIAN` (scored): folded into `SUPPORTED-BASE-IMAGES` (SU), the Debian line read from the tag or the digest, Alpine and Ubuntu too.
- [ ] **CO04** `DOCKERIGNORE`: beside each build context, excluding `.git`, `.env*`, `node_modules` and caches. L1 · fix S · adopt.
- [ ] **CO05** `MULTI-STAGE`: compilers and dev dependencies left in a builder stage. L2 · fix J · trial.
- [ ] **CO06** `MINIMAL-FINAL-STAGE`: a slim or distroless final image, no shell where none is needed. L2 · fix J · trial.
- [ ] **CO07** `TAG-AND-DIGEST`: `image:tag@sha256:…`, the tag kept for humans and update bots. L2 · fix S · adopt.
- [ ] **CO08** `COPY-NOT-ADD`: `COPY` rather than `ADD`, never `ADD` of a URL (hadolint's DL3020). L2 · fix S · adopt.
- [ ] **CO09** `APT-HYGIENE`: `--no-install-recommends`, lists removed or a cache mount (DL3015, DL3009). L2 · fix S · adopt.
- [ ] **CO10** `CACHE-MOUNTS`: `RUN --mount=type=cache` for uv, pnpm, pip and apt. L2 · fix S · trial.
- [ ] **CO11** `BUILD-SECRETS`: secrets through `--mount=type=secret`, never `ARG` or `ENV` (BuildKit's `SecretsUsedInArgOrEnv` check). L2 · fix J · adopt.
- [ ] **CO12** `EXEC-FORM`: `CMD` and `ENTRYPOINT` in JSON form so signals reach the process (BuildKit's `JSONArgsRecommended`). L2 · fix S · adopt.
- [ ] **CO13** `PIPEFAIL`: `SHELL [..., "-o", "pipefail", "-c"]` before a `RUN` with a pipe (DL4006). L2 · fix S · adopt.
- [ ] **CO14** `INIT-PROCESS`: `init: true` or tini where the main process doesn't reap its children. L2≈ · fix S · assess.
- [ ] **CO15** `OCI-LABELS`: `org.opencontainers.image.source`, `revision` and `licenses` on published images. L2 · fix S · trial.
- [ ] **CO16** `COMPOSE-NO-VERSION`: no top-level `version:`, obsolete in the Compose Specification. L1 · fix S · adopt.
- [ ] **CO17** `COMPOSE-HEALTHY-DEPENDS`: `depends_on` with `condition: service_healthy` on databases. L1 · fix S · adopt.
- [ ] **CO18** `NO-DOCKER-SOCKET`: no `/var/run/docker.sock` mounted, except read-only into a declared proxy with its reason; critical. L1 · fix J · adopt.
- [ ] **CO19** `NO-PRIVILEGED`: no `privileged`, `network_mode: host`, `pid: host` or added `SYS_ADMIN`, beside `HARDENED-CONTAINERS`. L1 · fix J · adopt.
- [ ] **CO20** `PORTS-ON-LOCALHOST`: databases and internal services published on `127.0.0.1` only (Docker's published ports bypass ufw's rules). L1 · fix S · adopt.
- [ ] **CO21** `LOG-ROTATION`: `max-size` and `max-file` on the logging driver (json-file grows without end by default). L1 · fix S · adopt.
- [ ] **CO22** `RESOURCE-LIMITS`: memory and CPU limits per service. L1 · fix S · trial.
- [ ] **CO23** `RESTART-POLICY`: `restart: unless-stopped` or `always` on long-running services. L1 · fix S · adopt.
- [ ] **CO24** `NAMED-VOLUMES`: database data in named volumes, never bind-mounted inside the repo. L1 · fix S · trial.
- [ ] **CO25** `NO-SECRETS-IN-COMPOSE`: no literal password under `environment:`; `env_file` or `secrets:` instead. L1 · fix J · adopt.
- [ ] **CO26** `IMAGES-SCANNED`: built images scanned (Trivy, Grype) in the release workflow. L1 · fix S · trial.
- [ ] **CO27** `IMAGES-SIGNED`: published images signed (cosign) or attested (`actions/attest-build-provenance`). L1 · fix S · assess.
- [ ] **CO28** `HADOLINT-CLEAN`: hadolint passes, as a mapped tool (F). L4 · fix J · trial.
- [ ] **CO29** `ONE-PROCESS`: no supervisord or `&` chain running several services in one container. L2 · fix J · trial.
- [ ] **CO30** `ROOTLESS-FRIENDLY`: compose files that run under rootless Podman as under Docker (`kiln dev` runs Podman). L1 · fix J · assess.

### OP · Operations

- [ ] **OP01** `HEALTH-PROBES` (scored): beyond a `HEALTHCHECK` line: the endpoint exists in the code, liveness and readiness told apart, compose and Kubernetes probes read.
- [ ] **OP02** `ASYNC-HEALTH` (draft): workers and the scheduler report health (a Celery ping, a heartbeat file probed by compose). L2≈ · fix J · trial.
- [ ] **OP03** `TESTED-BACKUPS` (draft): a backup job in code (pg_dump, restic, borg) with a scheduled restore job beside it. L1≈ · fix J · trial.
- [ ] **OP04** `REVERSIBLE-DEPLOYMENT` (draft): images deployed by immutable tag or digest, a rollback script or workflow present. L1≈ · fix J · trial.
- [ ] **OP05** `FEATURE-FLAGS` (draft): a flags library or module present where risky changes ship. L1≈ · fix J · assess.
- [ ] **OP06** `TESTED-SELF-HEALING` (draft): restart policies plus a script that exercises a known failure. L1≈ · fix J · assess.
- [ ] **OP07** `ENV-EXAMPLE-COMPLETE`: every variable the code reads (`os.environ`, `env()`, `process.env`, `useRuntimeConfig`) is in `.env.example`, and none there is stale. L3 · fix S · adopt.
- [ ] **OP08** `FAIL-FAST-CONFIG`: a missing required setting stops the start (no silent default for `SECRET_KEY` or `DATABASE_URL`): what `DJANGO-SECRET-KEY` and `DJANGO-ALLOWED-HOSTS` ask of Django, for every stack. L2 · fix J · adopt.
- [ ] **OP09** `DEPLOY-FROM-CI`: production deployed by a workflow from a commit, not from a laptop. L1 · fix J · trial.
- [ ] **OP10** `PROTECTED-ENVIRONMENTS`: production jobs run in a forge environment with reviewers or branch rules (L6, T-158). L6 · fix J · trial.
- [ ] **OP11** `OIDC-TO-CLOUD`: cloud credentials through OIDC federation (`id-token: write`), no long-lived keys in secrets. L1 · fix J · adopt.
- [ ] **OP12** `ENCRYPTED-SECRETS`: secrets committed only encrypted (sops with age, git-crypt, Ansible Vault). L1 · fix J · trial.
- [ ] **OP13** `RUNBOOK`: deploy, rollback, restore and rotate written down (`docs/runbook.md`), with commands that exist. L1 · fix J · trial.
- [ ] **OP14** `GRACEFUL-SHUTDOWN`: SIGTERM handled, a stop grace period longer than the longest request or task. L2 · fix S · trial.
- [ ] **OP15** `UTC-SERVERS`: containers and servers run in UTC, no `TZ` set to a local zone (with `TIME-ZONE`). L1 · fix S · trial.
- [ ] **OP16** `UPTIME-CHECKS`: an outside check declared (Uptime Kuma, Gatus, a cron monitor) for production profiles. L1≈ · fix J · assess.
- [ ] **OP17** `CRON-MONITORED`: scheduled jobs ping a dead man's switch. L2≈ · fix J · assess.
- [ ] **OP18** `RECOVERY-TARGETS`: RPO and RTO stated in the runbook, the backup schedule matching them. L1≈ · fix J · assess.
- [ ] **OP19** `HOSTS-AS-CODE`: servers configured by code (Ansible, cloud-init, NixOS), not by hand. L0 · fix J · trial.
- [ ] **OP20** `AUTOMATIC-TLS`: certificates renewed by themselves (Caddy, cert-manager, the platform's). L1 · fix S · adopt.
- [ ] **OP21** `ONE-COMMAND-LOCAL`: the whole stack runs locally with one command (`kiln dev`, compose, `Procfile.dev`). L0 · fix S · adopt.
- [ ] **OP22** `STAGING-LIKE-PROD`: staging differs from production by values only. L1≈ · fix J · assess.
- [ ] **OP23** `COST-GUARDS`: budgets and alerts declared with the cloud resources. L1 · fix J · assess.
- [ ] **OP24** `DATA-RESIDENCY`: regions in the IaC and settings inside the EU for profiles that promise it. L1 · fix J · assess.

### OB · Observability

- [ ] **OB01** `REQUEST-ID` (draft): a request-ID middleware (django-guid, asgi-correlation-id) with the ID in the log format and the response headers. L2 · fix S · trial.
- [ ] **OB02** `OPENTELEMETRY` (draft): the OpenTelemetry SDK configured from `OTEL_*` variables, the framework and HTTP clients instrumented, `traceparent` forwarded from the front. L2 · fix S · trial.
- [ ] **OB03** `SLO` (draft): objectives as code (OpenSLO, Sloth, Pyrra). L1 · fix J · assess.
- [ ] **OB04** `ALERT-ON-SYMPTOMS` (draft): alert rules on error rates and latency rather than CPU, read from Prometheus rule files. L2≈ · fix J · assess.
- [ ] **OB05** `METRICS-PRIVATE`: a `/metrics` endpoint behind authentication or on an internal port. L2 · fix J · trial.
- [ ] **OB06** `FRONT-ERRORS-CAPTURED`: browser errors reported (Sentry for Vue and Nuxt), source maps uploaded privately. L1 · fix S · trial.
- [ ] **OB07** `RELEASE-IN-EVENTS`: errors and traces carry the release (the commit SHA), so a regression points to a deploy. L2 · fix S · trial.
- [ ] **OB08** `DASHBOARDS-AS-CODE`: dashboards committed (Grafana JSON, Grafonnet, Perses). L0 · fix J · assess.
- [ ] **OB09** `AUDIT-TRAIL`: security-relevant actions (login, role change, export, deletion) written to an append-only log. L2≈ · fix J · trial.
- [ ] **OB10** `QUIET-HEALTH-LOGS`: health checks left out of access logs. L2 · fix S · assess.
- [ ] **OB11** `TRACE-SAMPLING`: a sampling ratio set from the environment. L2 · fix S · assess.
- [ ] **OB12** `LOG-RETENTION`: retention set in the log stack, with `RETENTION` (PD). L1 · fix S · assess.

### CI · CI/CD

- [ ] **CI01** `CI-PRESENT` (scored): "every change is checked before it ships" (decision 6): fast checks at each commit and the whole CI before each release, on the forge or on the machine with its verdict kept (`kiln ci`), or a CI on every pull request; read from any CI (C) with its triggers. With profiles (T-39), company and enterprise ask for CI on every pull request.
- [ ] **CI02** `LINT-IN-CI` (scored): lint commands read per component from any CI, as for `TESTS-IN-CI` (TE), through `make`, `just`, `task`, `nox`, `tox` and package scripts.
- [ ] **CI03** `WORKFLOW-INJECTION` (scored): zizmor's template-injection audit (F) instead of one regex; an expression passed through `env:` passes.
- [ ] **CI04** `WORKFLOW-PERMISSIONS` (scored): `write-all`, and a job's `contents: write` with no step that writes, flagged.
- [ ] **CI05** `PULL-REQUEST-TARGET` (scored): flagged when the workflow checks out or runs the pull request's head; `workflow_run` with downloaded artifacts too (zizmor's dangerous-triggers).
- [ ] **CI06** `FAST-CI` (draft): median duration and runs that passed on retry read from the forge (L6); caches and concurrency as the static part. L6 · fix J · trial.
- [ ] **CI07** `CI-CONCURRENCY`: `concurrency:` with `cancel-in-progress` on pull-request runs. L1 · fix S · adopt.
- [ ] **CI08** `CI-TIMEOUTS`: `timeout-minutes` on every job (the default is 360). L1 · fix S · adopt.
- [ ] **CI09** `CI-CACHES`: dependency caches on (setup-uv's `enable-cache`, setup-node's `cache`). L1 · fix S · adopt.
- [ ] **CI10** `NO-PERSISTED-CREDENTIALS`: `actions/checkout` with `persist-credentials: false` (zizmor's artipacked). L1 · fix S · adopt.
- [ ] **CI11** `ARTIFACT-RETENTION`: `retention-days` on uploaded artifacts. L1 · fix S · trial.
- [ ] **CI12** `SUPPORTED-RUNNERS`: no runner image GitHub has retired (`ubuntu-20.04` in 2025, older macOS ones), a calendar like the runtimes'. L1 · fix S · adopt.
- [ ] **CI13** `NO-DEPRECATED-COMMANDS`: no `::set-output` or `::save-state`; `$GITHUB_OUTPUT` and `$GITHUB_STATE`. L2 · fix S · adopt.
- [ ] **CI14** `ACTIONLINT`: actionlint passes (expressions, types, the shellcheck it embeds). L4 · fix J · adopt.
- [ ] **CI15** `ZIZMOR-CLEAN`: zizmor's audits pass, run by kiln or in CI. L4 · fix J · trial.
- [ ] **CI16** `NO-SELF-HOSTED-ON-PUBLIC`: no self-hosted runner reachable from a public repo's pull requests; critical. L1 + L6 · fix J · adopt.
- [ ] **CI17** `CACHE-POISONING`: release workflows restore no cache that pull requests can write (zizmor's cache-poisoning). L4 · fix J · trial.
- [ ] **CI18** `SECRETS-THROUGH-ENV`: `${{ secrets.X }}` passed through `env:`, never inlined in `run:`. L2 · fix S · adopt.
- [ ] **CI19** `REUSABLE-WORKFLOWS-PINNED`: `uses: org/repo/.github/workflows/x.yml@<sha>` (`PINNED-ACTIONS` extended); kiln's own workflows, cited by tag and moved by `kiln update`, stay one accepted way. L1 · fix S · adopt.
- [ ] **CI20** `ACTIONS-UPDATED`: the `github-actions` ecosystem in the update bot's config (`DEPENDENCY-UPDATES` per ecosystem). L1 · fix S · adopt.
- [ ] **CI21** `REQUIRED-CHECKS`: the integration branch requires the CI's checks (L6, T-158). L6 · fix J · trial.
- [ ] **CI22** `MATRIX-COVERS-SUPPORT`: a library's CI matrix covers the versions it claims (`requires-python`, `engines`). L1 · fix S · trial.
- [ ] **CI23** `PROVENANCE`: release artifacts attested (`actions/attest-build-provenance`, PyPI's attestations); T-90 asks it of kiln. L1 · fix S · trial.
- [ ] **CI24** `BUILD-ONCE`: the artifact deployed is the one tested (an image promoted by digest), never rebuilt per environment. L2≈ · fix J · assess.
- [ ] **CI25** `CI-REPLAYABLE`: the CI's commands run on a laptop too (`kiln ci`, `make ci`, `just ci`). L1≈ · fix J · trial.
- [ ] **CI26** `GITLAB-PIPELINE-HYGIENE`: `interruptible`, `timeout`, `rules:` rather than `only` and `except`, includes pinned to a commit, protected variables. L1 · fix S · adopt (GitLab).

### GV · Git and versions

The six drafts are questions about history: `--history` (M) gives them detectors.

- [ ] **GV01** `SMALL-COMMITS` (draft): median size of the last hundred non-merge commits, and the share of subjects in the Conventional Commits form. L5 · ratchet · trial.
- [ ] **GV02** `BRANCH-NAMES` (draft): merged branches' names, from merge subjects or the forge, carry a type prefix. L5 · fix J · trial.
- [ ] **GV03** `MERGE-COMMITS` (draft): merges kept on the integration branch, visible in history, where the profile asks for them. L5 · fix J · assess.
- [ ] **GV04** `NO-COMMIT-ON-INTEGRATION` (draft): non-merge commits made straight on the integration branch, bots aside; branch protection with `--online`. L5 · ratchet · trial.
- [ ] **GV05** `RELEASE-NOTES` (draft): each release tag has its CHANGELOG entry or forge release, breaking changes first. L5 · fix J · trial.
- [ ] **GV06** `RELEASES-FROM-MAIN` (draft): release tags reachable from main, deploy workflows triggered by tags. L5 · fix J · trial.
- [ ] **GV07** `CHANGELOG`: a `CHANGELOG.md` in the Keep a Changelog shape, or generated (release-please, git-cliff). L0 · fix S · trial.
- [ ] **GV08** `SEMVER-TAGS`: release tags parse as versions and only go up. L5 · fix J · trial.
- [ ] **GV09** `SIGNED-TAGS`: release tags signed (SSH or GPG), verified with `--online`. L5 · fix J · assess.
- [ ] **GV10** `NO-SECRETS-IN-HISTORY`: secret patterns searched in every reachable blob, not only the tree; critical. The fix rotates first; history is rewritten only on the user's decision. L5 · fix J · adopt.
- [ ] **GV11** `NO-LARGE-BLOBS`: no blob over about 5 MB in history outside LFS. L5 · fix J · adopt.
- [ ] **GV12** `LFS-FOR-BINARIES`: large binary assets tracked by LFS or stored elsewhere. L0 · fix J · trial.
- [ ] **GV13** `NO-CONFLICT-MARKERS`: no `<<<<<<<`, `=======` or `>>>>>>>` line in tracked text, docs that teach git aside. L2 · fix J · adopt.
- [ ] **GV14** `NO-CASE-COLLISIONS`: no two paths that differ only by case (they break checkouts on macOS and Windows). L0 · fix J · adopt.
- [ ] **GV15** `PORTABLE-PATHS`: no name Windows refuses (`CON`, `aux.py`, a trailing dot or space, `:*?"<>|`). L0 · fix J · adopt.
- [ ] **GV16** `BLAME-IGNORE-REVS`: mass-reformatting commits listed in `.git-blame-ignore-revs`. L5 · fix S · trial.
- [ ] **GV17** `SUBMODULES-SANE`: submodules over HTTPS, pinned to commits their remote still has. L1 + L6 · fix J · trial.
- [ ] **GV18** `CODEOWNERS-VALID`: paths that exist and owners that exist (L6), for team profiles. L1 · fix J · trial.
- [ ] **GV19** `NO-FORCE-PUSH-ON-MAIN`: force pushes and deletions blocked on the release and integration branches (L6, T-158). L6 · fix J · adopt.
- [ ] **GV20** `STALE-BRANCHES`: branches merged long ago and still on the remote (`/kiln:cleanup`, for the forge). L6 · fix S · assess.

### DT · Docs and tracking

- [ ] **DT01** `README` (scored): sections that say what it is and how to install, run, test and deploy, commands that exist (L3); the bare file isn't enough.
- [ ] **DT02** `WORK-TRACKING` (draft): one backlog file, ordered, with a done log, or the forge's issues in use (L6). L0 · fix S · trial.
- [ ] **DT03** `README-COMMANDS`: commands in the README's code blocks exist (scripts, Makefile targets, package scripts, `manage.py` commands); `--deep` runs the install ones in a sandbox. L3 · fix J · trial.
- [ ] **DT04** `LINKS-ALIVE`: links and anchors between Markdown files resolve; outside links with `--online` (lychee). L3 · fix S · trial.
- [ ] **DT05** `DOCS-BUILD-STRICT`: a docs site builds strictly in CI (`mkdocs build --strict`, Sphinx's `-W`). L1 · fix S · trial.
- [ ] **DT06** `DOCSTRINGS-PUBLIC`: public functions of libraries documented (ruff's D1, one convention). L4 · ratchet · trial.
- [ ] **DT07** `DOCS-NOT-STALE`: docs naming a function, option, command or file that no longer exists. L3 · fix J · trial.
- [ ] **DT08** `API-DOCS-SERVED`: an API with a schema serves its docs in development (Swagger UI, Scalar, Ninja's `/docs`). L2 · fix S · trial.
- [ ] **DT09** `MARKDOWN-LINT`: markdownlint or rumdl configured where docs are many. L1 · fix S · assess.
- [ ] **DT10** `GLOSSARY`: a glossary of the domain's words, read by `DOMAIN-VOCABULARY`. L0 · fix J · assess.

### AI · AI-assisted development

- [ ] **AI01** `AI-CONTEXT` (scored): from "a file exists" to its quality: under a size budget, its map's paths existing, its commands running, nothing contradicting the settings. L3.
- [ ] **AI02** `AI-CONFIDENTIALITY` (draft): Claude Code's `permissions.deny` covers `.env*`, keys and dumps; no real personal data in the fixtures an agent reads (PD). L1 · fix S · trial.
- [ ] **AI03** `AI-ACCOUNTABILITY` (draft): agent-written changes pass the same checks and review: hooks or CI enforce the rules, nothing lets an agent merge alone. L1≈ · fix J · assess.
- [ ] **AI04** `AI-FEATURES` (draft): calls to a model's API carry `max_tokens`, a timeout and a fallback; evaluations sit in the repo and run in CI (promptfoo, a pytest suite). L2 · fix J · trial.
- [ ] **AI05** `CONTEXT-BUDGET`: CLAUDE.md, the rules it loads and the skills' descriptions under a token budget (context length is the cost, measured on 22 October 2026). L1 · ratchet · trial.
- [ ] **AI06** `NARROW-PERMISSIONS`: no `Bash(*)`, no `bypassPermissions` default mode, no wildcard web access in committed settings. L1 · fix J · adopt.
- [ ] **AI07** `MCP-PINNED`: MCP servers in `.mcp.json` pinned (`npx pkg@x.y.z`, `uvx pkg==x.y.z`, an image digest). L1 · fix S · adopt.
- [ ] **AI08** `MCP-NO-LITERAL-SECRETS`: `.mcp.json` passes `${VAR}` references, never tokens; critical. L1 · fix J · adopt.
- [ ] **AI09** `PLUGINS-VALID`: skills, agents and commands well formed (name matching the folder, a description, the files they cite present), as `test_plugins.py` checks for kiln. L1 · fix J · adopt.
- [ ] **AI10** `HOOKS-SAFE`: hooks in committed settings exist at their paths and download nothing. L1 · fix J · adopt.
- [ ] **AI11** `AGENTS-MD-POINTER`: where a team uses other agents, `AGENTS.md` points to CLAUDE.md rather than holding a second truth. L0 · fix S · assess.
- [ ] **AI12** `LLM-KEYS-SERVER-SIDE`: no model provider's key reachable from front code or a public env prefix; critical. L2 · fix J · adopt.
- [ ] **AI13** `LLM-MODELS-CURRENT`: model IDs not retired, from a bundled calendar like the runtimes'. L2 · fix S · trial.
- [ ] **AI14** `LLM-OUTPUT-VALIDATED`: structured outputs parsed by a schema (tool use, JSON schema) before use. L2≈ · fix J · trial.
- [ ] **AI15** `PROMPTS-AS-FILES`: prompts versioned as files, reviewable, not scattered strings. L2≈ · fix J · assess.
- [ ] **AI16** `TOOLS-LEAST-PRIVILEGE`: an agent fed untrusted content gets read-only tools, its input delimited. L2≈ · fix J · assess.
- [ ] **AI17** `PII-TO-LLM`: personal fields sent to a model's API flagged (PD). L3≈ · fix J · trial.
- [ ] **AI18** `PROMPT-CACHING`: long static system prompts marked for caching (`cache_control` on Anthropic's API). L2 · fix S · assess.

### BD · Business domain

- [ ] **BD01** `MONEY` (draft): `FloatField`, `float` or JS `number` arithmetic on names like price, amount, total, fee or balance; integers of the smallest unit stay the grid's way. L2≈ · fix J · trial.
- [ ] **BD02** `TIME-ZONE` (draft): naive datetimes, `TIME_ZONE` set, calendar computations through `zoneinfo` (with `NAIVE-DATETIMES` and `USE-TZ`). L2 · fix J · trial.
- [ ] **BD03** `WEBHOOKS-VERIFIED`: incoming webhooks check their signature (Stripe's `construct_event`, GitHub's `X-Hub-Signature-256` compared in constant time). L2 · fix J · adopt.
- [ ] **BD04** `WEBHOOKS-DEDUPLICATED`: events stored by ID before they're handled. L2≈ · fix J · trial.
- [ ] **BD05** `PAYMENTS-BY-PROVIDER`: card numbers never reach the server (Checkout or Elements), no `card_number` field anywhere; critical. L2 · fix J · adopt.
- [ ] **BD06** `CURRENCY-WITH-AMOUNT`: every amount carries its ISO 4217 currency. L2≈ · fix J · assess.
- [ ] **BD07** `EXPLICIT-ROUNDING`: the rounding mode stated wherever amounts are divided (taxes, splits). L2≈ · fix J · trial.
- [ ] **BD08** `EMAILS-CASE-INSENSITIVE`: e-mail uniqueness ignores case (a `Lower()` unique constraint, `citext`). L2 · fix J · trial.
- [ ] **BD09** `PHONES-E164`: phone numbers stored in E.164 (phonenumbers, libphonenumber). L2≈ · fix J · assess.
- [ ] **BD10** `NAMES-AS-GIVEN`: no forced first and last name split, no ASCII-only or short-capped names. L2≈ · fix J · assess.
- [ ] **BD11** `DATES-NOT-DATETIMES`: birthdays and due dates stored as dates. L2≈ · fix J · assess.
- [ ] **BD12** `INVOICE-NUMBERING`: invoice numbers in one continuous chronological sequence where the law asks for it (France among others), taken inside a transaction. L2≈ · fix J · assess.
- [ ] **BD13** `TAX-RATES-AS-DATA`: VAT rates and thresholds held as dated data, not in code. L2≈ · fix J · assess.
- [ ] **BD14** `ONE-CLICK-UNSUBSCRIBE`: bulk mail with `List-Unsubscribe` and one-click unsubscribe (RFC 8058, required by Gmail and Yahoo for bulk senders since 2024). L2≈ · fix J · trial.
- [ ] **BD15** `MAIL-AUTHENTICATED`: SPF, DKIM and DMARC for the sending domain, checked in DNS with `--online`. L6 · fix J · trial.

### New themes

Decision 3: `licensing`, `infrastructure` and `data-science` join `THEMES` (a closed list in
`model.py`), each with its first rule, in T-141. The ideas of DX, PK and CM go to existing
themes; their sections stay here so their IDs hold.

### LI · Licensing (`licensing`)

- [ ] **LI01** `LICENSE-FILE`: a licence file whose text matches an SPDX licence (matched as licensee does), or "all rights reserved" stated for private work. L1 · fix J · adopt (open source).
- [ ] **LI02** `LICENSE-DECLARED`: the manifest's licence as an SPDX expression (`license = "MIT"` with PEP 639, package.json's `license`). L1 · fix S · adopt.
- [ ] **LI03** `LICENSE-CONSISTENT`: the file, the manifests and the README say the same licence. L1 · fix J · adopt.
- [ ] **LI04** `DEPENDENCY-LICENSES`: licences of the locked dependencies compatible with the project's and its profile (no AGPL in a closed service without a decision), from the registries (L6) or a bundled cache. L6 · fix J · trial.
- [ ] **LI05** `THIRD-PARTY-NOTICES`: vendored code keeps its licence and notice. L1 · fix J · adopt.
- [ ] **LI06** `ASSETS-LICENSED`: fonts, images and icons committed with their licence or source (a font's OFL file). L0≈ · fix J · trial.
- [ ] **LI07** `SPDX-HEADERS`: REUSE-compliant headers or a `REUSE.toml`, for projects that want them. L1 · fix S · assess.
- [ ] **LI08** `SIGN-OFF`: contributions under a DCO sign-off or a CLA, for profiles that need one. L5 · fix J · assess.

### IN · Infrastructure as code (`infrastructure`)

- [ ] **IN01** `TF-LOCK`: `.terraform.lock.hcl` committed. L0 · fix S · adopt.
- [ ] **IN02** `TF-REMOTE-STATE`: no `*.tfstate` committed (state holds secrets), a remote backend declared; critical when state is tracked. L0 · fix J · adopt.
- [ ] **IN03** `TF-VERSIONS-PINNED`: `required_version` and provider constraints set; registry modules pinned to versions, git modules to commits. L1 · fix S · adopt.
- [ ] **IN04** `TF-CHECKED`: `fmt -check`, `validate` and tflint in CI (Terraform or OpenTofu). L1 · fix S · trial.
- [ ] **IN05** `IAC-SCANNED`: checkov, Trivy's config scan or KICS in CI. L1 · fix S · trial.
- [ ] **IN06** `NO-PUBLIC-BUCKETS`: storage buckets private unless declared public with a reason; public access blocked by default. L1 · fix J · adopt.
- [ ] **IN07** `ENCRYPTED-AT-REST`: databases, volumes and buckets encrypted in the IaC. L1 · fix S · trial.
- [ ] **IN08** `K8S-SECURITY-CONTEXT`: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, capabilities dropped (the restricted Pod Security Standard). L1 · fix S · adopt.
- [ ] **IN09** `K8S-RESOURCES`: memory requests and limits, CPU requests. L1 · fix S · adopt.
- [ ] **IN10** `K8S-PROBES`: readiness and liveness probes on different endpoints. L1 · fix S · adopt.
- [ ] **IN11** `K8S-NO-LATEST`: no `:latest` or untagged image (`IMAGES-BY-DIGEST` reads manifests too). L1 · fix S · adopt.
- [ ] **IN12** `K8S-NETWORK-POLICIES`: a default-deny NetworkPolicy per namespace. L1 · fix J · trial.
- [ ] **IN13** `K8S-SECRETS-EXTERNAL`: no Secret manifest holding real data; External Secrets, Sealed Secrets or sops instead. L1 · fix J · adopt.
- [ ] **IN14** `K8S-SUPPORTED-APIS`: no API version Kubernetes has removed (`extensions/v1beta1`, `policy/v1beta1`), from pluto's data. L1 · fix S · adopt.
- [ ] **IN15** `HELM-CHARTS`: `values.schema.json` present, `Chart.lock` committed. L0 · fix J · trial.
- [ ] **IN16** `ANSIBLE-LINT`: ansible-lint clean, secrets in Vault rather than plain variables. L4 · fix J · trial.
- [ ] **IN17** `IAC-TAGS`: resources tagged with an owner and a cost centre, for company profiles. L1 · fix S · assess.

### DS · Data science (`data-science`)

The first data repos came through issues (#43, #44): v0.4.6 deploys a Streamlit or Dash front
(T-155) and adds `MODEL-TRACED` (T-156). This theme gathers what such repos need.

- [ ] **DS01** `MODEL-TRACED` (trial, v0.4.6): moves here from data-migrations; promoted once its precision is measured on data repos.
- [ ] **DS02** `NOTEBOOK-OUTPUTS-CLEAN`: notebooks committed without outputs or execution counts (nbstripout, or Jupytext pairs). L1 · fix S · adopt.
- [ ] **DS03** `NOTEBOOKS-PAIRED`: notebooks paired with a `.py` file (Jupytext's percent format) so diffs and reviews work. L1 · fix S · trial.
- [ ] **DS04** `NOTEBOOK-SECRETS`: no token in a cell or an output; `SECRETS` reads a `.ipynb` as cells, not as one JSON string. L2 · fix J · adopt.
- [ ] **DS05** `NO-ABSOLUTE-PATHS`: no `/home/…`, `C:\Users\…` or `/content/drive` path in code or notebooks. L2 · fix J · adopt.
- [ ] **DS06** `DATA-OUT-OF-GIT`: datasets over a few MB kept out of git (DVC, LFS, a bucket), described by a pointer. L0 · fix J · adopt.
- [ ] **DS07** `SEEDS-SET`: random seeds fixed where results are reported (`numpy.random.default_rng(seed)`, `torch.manual_seed`). L2≈ · fix J · trial.
- [ ] **DS08** `ENVIRONMENT-LOCKED`: the analysis environment locked (uv, conda-lock, pixi, renv). L1 · fix S · adopt.
- [ ] **DS09** `PIPELINE-DECLARED`: steps declared (DVC stages, Snakemake, a Makefile), not notebooks run by hand in order. L0 · fix J · trial.
- [ ] **DS10** `STREAMLIT-SECRETS-IGNORED`: `.streamlit/secrets.toml` ignored and untracked; critical when tracked. L0 · fix S · adopt.
- [ ] **DS11** `NOTEBOOKS-RUN-IN-CI`: notebooks that are part of the deliverable executed in CI (nbmake, papermill). L1 · fix S · trial.
- [ ] **DS12** `SAFE-MODEL-LOADING`: no `pickle.load` or `torch.load(..., weights_only=False)` on downloaded files; safetensors or ONNX for models from outside. L2 · fix S · adopt.
- [ ] **DS13** `EXPERIMENTS-TRACKED`: runs logged with their commit (MLflow, a results file). L1≈ · fix J · assess.
- [ ] **DS14** `DATA-SCHEMA`: input tables validated by a schema (pandera, Great Expectations, Pydantic). L2≈ · fix J · assess.

### DX · Developer experience (into `structure` and `docs-tracking`)

- [ ] **DX01** `ONE-COMMAND-SETUP`: one documented bootstrap command (`make setup`, `just setup`, `uv sync` with `pnpm install`). L1 · fix S · adopt.
- [ ] **DX02** `TASK-RUNNER`: common tasks named in one place (Makefile, justfile, package scripts, poe), and the README cites them. L1 · fix S · trial.
- [ ] **DX03** `PRE-COMMIT-FAST`: commit hooks run in seconds (ruff at commit, type checks and tests elsewhere). L1≈ · fix J · trial.
- [ ] **DX04** `TOOL-VERSIONS-PINNED`: tool versions in `mise.toml` or `.tool-versions`, the same as in CI. L1 · fix S · trial.
- [ ] **DX05** `NO-GLOBAL-INSTALLS`: tools run from the project (`uvx`, `pnpm dlx`, versioned `npx`), never `sudo pip install` or `npm -g` in the docs. L2 · fix J · trial.
- [ ] **DX06** `EDITOR-SETTINGS-SHARED`: recommended extensions and format-on-save shared, personal settings ignored. L0 · fix S · assess.
- [ ] **DX07** `CLEAN-CLONE-WORKS`: a fresh clone installs and passes its checks with the documented commands (`--deep`, in a sandbox). L7 · fix J · trial.
- [ ] **DX08** `DEVCONTAINER` ⚠ T-48 (declined): a dev container for teams that want one, at `hold` while T-48 stands. L0 · hold.

### PK · Packaging and publishing (into `supply-chain` and `ci-cd`)

- [ ] **PK01** `TRUSTED-PUBLISHING`: PyPI and npm publish through OIDC trusted publishing, no long-lived token. L1 · fix S · adopt.
- [ ] **PK02** `ATTESTATIONS`: PyPI attestations (PEP 740) and npm provenance on published packages. L1 · fix S · trial.
- [ ] **PK03** `RELEASE-WORKFLOW`: publishing only from CI, on a tag, in a protected environment. L1 · fix S · adopt.
- [ ] **PK04** `NPM-FILES-ALLOWLIST`: `files` in package.json so nothing private ships (`npm pack --dry-run` with `--deep`). L1 · fix S · adopt.
- [ ] **PK05** `PYPROJECT-METADATA`: `[project]` with name, version source, `requires-python`, licence expression, readme and URLs. L1 · fix S · adopt.
- [ ] **PK06** `NO-SETUP-PY`: a PEP 517 backend declared in `pyproject.toml`; `setup.py` kept only for C extensions. L1 · fix J · trial.
- [ ] **PK07** `PACKAGE-CONTENTS`: the sdist holds the tests and the licence, the wheel holds neither tests nor secrets (`--deep` builds both). L7 · fix J · trial.
- [ ] **PK08** `TYPED-EXPORTS`: package.json `exports` with `types` conditions; publint and arethetypeswrong clean. L4 · fix J · trial.
- [ ] **PK09** `ENGINES-DECLARED`: `engines.node` and `requires-python` set and matching the CI matrix. L1 · fix S · adopt.
- [ ] **PK10** `VERSION-SINGLE-SOURCE`: the version in one place, the manifest or the tag (hatch-vcs, setuptools-scm). L1 · fix J · trial.
- [ ] **PK11** `CLI-ENTRY-POINTS`: command-line tools declared in `[project.scripts]` or `bin`, with `--version` and `--help` that work (L7). L1 · fix S · trial.
- [ ] **PK12** `DEPRECATION-POLICY`: a deprecation warns for at least one release before the removal (`DeprecationWarning`), and the docs say so. L2≈ · fix J · assess.
- [ ] **PK13** `REPRODUCIBLE-BUILD`: `SOURCE_DATE_EPOCH` honoured; two builds give the same hash (`--deep`). L7 · fix J · assess.

### CM · Community (into `docs-tracking`)

For the open-source profile; kiln's own vitrine (CONTRIBUTING, Code of Conduct, SECURITY,
templates, FUNDING with T-119) is the reference example.

- [ ] **CM01** `CONTRIBUTING`: setup, tests and the pull-request flow written down. L0 · fix S · adopt (open source).
- [ ] **CM02** `CODE-OF-CONDUCT`: the Contributor Covenant or an equivalent, with a contact. L0 · fix S · adopt (open source).
- [ ] **CM03** `SECURITY-POLICY`: `SECURITY.md` with a private reporting channel; private vulnerability reporting on (L6). L0 · fix S · adopt.
- [ ] **CM04** `ISSUE-FORMS`: issue forms for bugs and requests, a pull-request template. L0 · fix S · trial.
- [ ] **CM05** `FUNDING`: `FUNDING.yml` when the maintainers accept sponsors. L0 · fix S · assess.
- [ ] **CM06** `GOOD-FIRST-ISSUES`: a few labelled issues open (L6, `/kiln:good-first-issues`). L6 · fix J · assess.
- [ ] **CM07** `RESPONSE-TIME`: median time to a first answer on issues and pull requests (L6). L6 · ratchet · assess.
- [ ] **CM08** `MAINTAINED`: commits or releases in the last 90 days, or the README says the project is finished or archived (Scorecard's Maintained). L5 · fix J · trial.
- [ ] **CM09** `CITATION`: `CITATION.cff` for research software (the university profile). L0 · fix S · trial.
- [ ] **CM10** `OPENSSF-BADGE`: the OpenSSF Best Practices badge, read with `--online`. L6 · fix J · assess.

### SP · Stack packs

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the
corpus measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

- [ ] **SP01** Go · `GO-MOD-TIDY`: `go mod tidy` would change nothing. L4 · fix S · adopt.
- [ ] **SP02** Go · `GO-LINT`: `go vet` and golangci-lint (its v2 config) in CI. L1 · fix S · adopt.
- [ ] **SP03** Go · `GOVULNCHECK`: govulncheck in CI, which reports only the vulnerable code a program reaches. L1 · fix S · adopt.
- [ ] **SP04** Go · `GO-TOOLCHAIN-SUPPORTED`: the `go` directive and `toolchain` on one of the two supported releases. L1 · fix S · adopt.
- [ ] **SP05** Go · `GO-CONTEXT-FIRST`: `context.Context` as first parameter, never stored in a struct. L2 · fix J · trial.
- [ ] **SP06** Go · `GO-NO-PANIC-IN-LIBS`: no `panic` on a library's ordinary paths. L2 · fix J · trial.
- [ ] **SP07** Rust · `CLIPPY-CLEAN`: clippy with warnings as errors in CI, a `[lints]` table in `Cargo.toml`. L1 · fix S · adopt.
- [ ] **SP08** Rust · `CARGO-DENY`: cargo-deny (advisories, licences, bans, sources) or cargo-audit in CI. L1 · fix S · adopt.
- [ ] **SP09** Rust · `RUST-EDITION-CURRENT`: edition 2024 (stable since Rust 1.85, February 2025). L1 · fix J · trial.
- [ ] **SP10** Rust · `RUST-MSRV`: `rust-version` declared and tested. L1 · fix S · trial.
- [ ] **SP11** Rust · `UNSAFE-JUSTIFIED`: every `unsafe` block with a `// SAFETY:` comment (clippy's `undocumented_unsafe_blocks`). L2 · fix J · adopt.
- [ ] **SP12** Rust · `NO-UNWRAP-IN-LIBS`: `unwrap` and `expect` counted in library code (clippy's `unwrap_used`). L2 · ratchet · trial.
- [ ] **SP13** Java and Kotlin · `JAVA-LTS`: a supported LTS (17, 21, 25) in the toolchain's config. L1 · fix S · adopt.
- [ ] **SP14** Java and Kotlin · `WRAPPER-COMMITTED`: Gradle or Maven wrapper committed with its checksum. L1 · fix S · adopt.
- [ ] **SP15** Java and Kotlin · `DEPENDENCY-LOCKING`: Gradle's dependency locking, or Maven plugins and versions pinned and checked by the enforcer. L1 · fix S · trial.
- [ ] **SP16** Java and Kotlin · `BUG-FINDER`: Error Prone or SpotBugs in the build; detekt and ktlint for Kotlin. L1 · fix S · trial.
- [ ] **SP17** C# · `CENTRAL-PACKAGES`: `Directory.Packages.props` and lock files (`RestorePackagesWithLockFile`). L1 · fix S · trial.
- [ ] **SP18** C# · `NUGET-AUDIT`: NuGetAudit on, transitive packages included, high findings as errors. L1 · fix S · adopt.
- [ ] **SP19** C# · `WARNINGS-AS-ERRORS`: `TreatWarningsAsErrors` and a current `AnalysisLevel` in `Directory.Build.props`. L1 · fix S · trial.
- [ ] **SP20** C# · `DOTNET-SUPPORTED`: the target framework on a supported .NET release. L1 · fix S · adopt.
- [ ] **SP21** C# · `GLOBAL-JSON`: the SDK pinned in `global.json` with a `rollForward` policy. L1 · fix S · trial.
- [ ] **SP22** PHP · `COMPOSER-AUDIT`: `composer audit` in CI, `composer.lock` committed for applications. L1 · fix S · adopt.
- [ ] **SP23** PHP · `STRICT-TYPES`: `declare(strict_types=1);` in every file. L2 · fix S · adopt.
- [ ] **SP24** PHP · `PHP-SUPPORTED`: `require.php` on a supported PHP line. L1 · fix S · adopt.
- [ ] **SP25** PHP · `NO-PHPINFO`: no `phpinfo()` reachable. L2 · fix S · adopt.
- [ ] **SP26** Ruby · `BUNDLER-AUDIT` and `BRAKEMAN`: both in CI for Rails apps, `Gemfile.lock` committed. L1 · fix S · adopt.
- [ ] **SP27** Ruby · `RUBOCOP`: RuboCop or Standard configured. L1 · fix S · adopt.
- [ ] **SP28** Ruby · `RUBY-SUPPORTED`: `.ruby-version` on a supported line. L1 · fix S · adopt.
- [ ] **SP29** Ruby · `RAILS-STRONG-PARAMS`: no `permit!`. L2 · fix J · adopt.
- [ ] **SP30** Mobile · `IOS-PRIVACY-MANIFEST`: `PrivacyInfo.xcprivacy` declaring the required-reason APIs (required by Apple since May 2024). L1 · fix J · adopt.
- [ ] **SP31** Mobile · `ANDROID-TARGET-SDK`: `targetSdkVersion` meets Google Play's current requirement, from a dated calendar. L1 · fix S · adopt.
- [ ] **SP32** Mobile · `NO-SERVER-SECRETS-IN-APP`: nothing secret in an app bundle (everything in it is public); client keys restricted instead. L2 · fix J · adopt.
- [ ] **SP33** Mobile · `SIGNING-OUT-OF-GIT`: no keystore, `.p12` or provisioning profile committed. L0 · fix J · adopt.
- [ ] **SP34** Mobile · `FLUTTER-STRICT`: `analysis_options.yaml` with the strict modes. L1 · fix S · trial.
- [ ] **SP35** C and C++ · `COMPILER-WARNINGS`: `-Wall -Wextra -Werror` (or `/W4 /WX`) in the build. L1 · fix S · trial.
- [ ] **SP36** C and C++ · `SANITIZERS-IN-CI`: AddressSanitizer and UndefinedBehaviorSanitizer builds in CI. L1 · fix S · trial.
- [ ] **SP37** C and C++ · `CLANG-TIDY`: configured and run. L1 · fix S · trial.
- [ ] **SP38** C and C++ · `FUZZING`: libFuzzer harnesses or OSS-Fuzz for parsers (Scorecard's Fuzzing). L1 · fix J · assess.
- [ ] **SP39** C and C++ · `MANAGED-DEPENDENCIES`: vcpkg or Conan manifests rather than copied sources. L1 · fix J · trial.
- [ ] **SP40** Elixir · `MIX-AUDIT`: mix_audit or `mix hex.audit` in CI, `mix.lock` committed. L1 · fix S · adopt.
- [ ] **SP41** Elixir · `CREDO-AND-DIALYZER`: both configured. L1 · fix S · trial.
- [ ] **SP42** Elixir · `SOBELOW`: Sobelow for Phoenix apps. L1 · fix S · adopt.

### FP · Framework packs

The `NOTABLE_PACKAGES` of `score.py` already name what the gap report sees; a pack turns one of
them into rules.

- [ ] **FP01** FastAPI · `FASTAPI-RESPONSE-MODELS`: every route declares its response model. L2 · fix J · adopt.
- [ ] **FP02** FastAPI · `FASTAPI-LIFESPAN`: `lifespan` rather than the deprecated `on_event`. L2 · fix S · adopt.
- [ ] **FP03** FastAPI · `FASTAPI-AUTH-DEPENDENCIES`: protected routes through security dependencies, set on the router rather than route by route. L2 · fix J · trial.
- [ ] **FP04** FastAPI · `FASTAPI-DOCS-IN-PROD`: `/docs` and `/openapi.json` off or protected in production for private APIs. L2 · fix J · trial.
- [ ] **FP05** Flask · `FLASK-APP-FACTORY`: a `create_app` factory, the secret key from the environment, CSRF protection on forms (Flask-WTF). L2 · fix J · trial.
- [ ] **FP06** Celery · the BG theme's rules, made exact for Celery's settings (`task_acks_late`, `task_time_limit`, the serializer, the beat replica). L1 · fix S · adopt.
- [ ] **FP07** Next.js · `NEXT-SERVER-ONLY`: secrets and database access in `server-only` modules, never imported by a `"use client"` file. L2 · fix J · adopt.
- [ ] **FP08** Next.js · `NEXT-AUTH-IN-DATA-LAYER`: authorization checked where data is read, not only in middleware (CVE-2025-29927 let a header skip middleware). L2≈ · fix J · adopt.
- [ ] **FP09** React · `REACT-HOOKS-RULES`: eslint-plugin-react-hooks on (`rules-of-hooks`, `exhaustive-deps`). L1 · fix S · adopt.
- [ ] **FP10** React · `REACT-KEYS`: keys on list items (`jsx-key`). L2 · fix J · adopt.
- [ ] **FP11** Angular · `ANGULAR-STRICT`: `strict` and `strictTemplates` on. L1 · fix S · adopt.
- [ ] **FP12** Angular · `ANGULAR-NO-SANITIZER-BYPASS`: `bypassSecurityTrust*` counted, each with its reason. L2 · fix J · adopt.
- [ ] **FP13** Angular · `MODERN-ANGULAR`: standalone components, signals and the built-in control flow; Angular's own schematics migrate. L2 · fix S · trial.
- [ ] **FP14** Svelte · `SVELTE-RUNES`: Svelte 5 runes in new files (`npx sv migrate svelte-5` for the rest). L2 · fix S · trial.
- [ ] **FP15** SvelteKit · `SVELTEKIT-CSRF`: `csrf.checkOrigin` never turned off. L1 · fix S · adopt.
- [ ] **FP16** Express · `EXPRESS-5`: Express 5, whose router passes rejected promises to the error handler. L1 · fix J · trial.
- [ ] **FP17** NestJS · `NEST-VALIDATION-PIPE`: a global `ValidationPipe` with `whitelist` and `forbidNonWhitelisted`. L2 · fix S · adopt.
- [ ] **FP18** NestJS · `NEST-GUARD-BY-DEFAULT`: a global authentication guard, public routes marked one by one. L2 · fix J · trial.
- [ ] **FP19** Streamlit and Dash · the DS theme's rules plus `STREAMLIT-SECRETS-IGNORED`, and the deploy of v0.4.6 checked (a health route, a non-root image). L1 · fix S · trial.

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
