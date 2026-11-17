# ion-repo#T-174 · More converters: the code
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

The second half of ion-repo#T-173: rules on the code itself, each change proven by the repo's tests.
- [ ] NOQA-CODES and TYPE-IGNORE-CODES: ruff or mypy run, the code of each error read and
  written into the bare comment.
- [ ] JS-LINTER: a minimal flat ESLint config, as `add_ruff` does for Python.
- [ ] HEALTH-PROBES: a `HEALTHCHECK` in the `Dockerfile` when the port and the route are
  obvious, left to judgment otherwise.
- [ ] BARE-EXCEPT: `except:` → `except Exception:`, kept only when the tests stay green.
