# ion-repo#T-212 · The syntax engine: ast-grep, one parse per file, settings and configs resolved
- **Type**: improvement
- **Priority**: 🟡 normal
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
  text (doctrine 11, ion-repo#T-144).
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
