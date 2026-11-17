# ion-repo#T-373 · `kiln-cli` retired, the testers moved to `ion-repo` and `ion-sh`
- **Type**: task
- **Priority**: 🟠 important
- **Status**: in progress — published and proven 1 November 2026; what is left waits for the testers and the next release
- **Opened**: 2026-10-29
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine, 1 November 2026: "dès la prochaine maj de kiln, je veux que tout le monde
  transite sur ion" (replaces ion-repo#T-372's `keramos-kiln`, which never became the name)

v0.4.11 is the last `kiln-cli`: at its first run as a uv tool it installs `ion-sh` and `ion-repo`,
removes itself and moves the Claude Code catalogue (`src/ion_repo/kiln_move.py`). Proven on a real
0.4.10 from PyPI with the real next wheels on a local index, GitHub on a local copy.
- [x] `ion-sh` 0.1.0 published first, 1 November 2026 (tag `v0.1.0` of `antoine-tena/ion`).
- [x] v0.4.11 promoted, 1 November 2026: `pypi.yml` published `ion-repo` and the last `kiln-cli`; both
  pages and the tap's `formula_renames.json` checked (Homebrew: `brew tap`, `brew install` and `ion-repo --version` passed
  in the `homebrew/brew` container after `brew update`; moving a real `kiln` formula not tried).
- [x] Right after it, in a clean `HOME`, from the real PyPI: `uv tool install ion-sh`, then `ion add repo`;
  the real migration from the published `kiln-cli` 0.4.10 (`uv tool install kiln-cli@latest`, an exact pin
  stays on 0.4.10). In the first minute after publishing, uv still answered "not found".
- [x] v0.4.12, 1 November 2026: the `kiln` alias says its new name once (checked from the real
  PyPI), and a real `kiln` 0.4.10 formula became `ion-repo` 0.4.12 with `kiln` kept, through
  `brew upgrade` in the `homebrew/brew` container (Homebrew 7.0.11, tap trusted).
- [ ] The `kiln` entry of the catalogue removed once no tester is left on 0.4.10 (its hook installs
  `kiln@kiln`; without the entry the plugin disappears), not before the v0.5 milestone. With it
  `plugins/kiln/`, `ion_names.py` and the kiln → ion-repo part of `renames.py`, once each repo of
  `~/code` has had `ion repo update` past v0.4.10-28 (2 November 2026, still on kiln's names:
  annway, annway-copie, studio, sweep, vision, learnagement, mobilite-mcp, all with `kiln@kiln`;
  adopted annski, SteamLens, VoyageProjet, info734). `moved_dirs.py` and the 0.4.0 and size
  names of `renames.py` stay: any project rename and old adopted repos use them.
- [x] The release after (2 November 2026, antoine's yes): `pypi.yml`'s `kiln-cli` and `keramos-kiln` steps
  removed, the `kiln` and `kiln-cli` scripts, `src/kiln/` and `kiln_move.py` out, the Homebrew formula
  without `kiln`; `session_start.py`'s `replacing_tool` kept for late testers.
- [ ] The project left on PyPI (never deleted: a deleted name can be taken again), the PyPI token
  scoped to `kiln-cli` revoked, `PYPI_TOKEN` removed; the "Entire account" `KERAMOS_PYPI_TOKEN`
  replaced by a token scoped to `ion-repo`.
