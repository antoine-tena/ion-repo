# ion-repo#T-222 · Locks and installs you can trust: every lockfile, frozen installs, pinned runtimes
- **Type**: improvement
- **Priority**: 🟡 normal
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
