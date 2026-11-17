# ion-repo#T-216 · Error handling, shell scripts and encodings, decided by tools
- **Type**: improvement
- **Priority**: 🟡 normal
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
