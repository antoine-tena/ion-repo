# ion-repo#T-177 · kiln's own docs in English only
- **Type**: task
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: — · **Due**: before the v0.5.0 candidate
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
- ion-repo#T-164 (French docs translated at the candidate) and ion-repo#T-55 (README in Chinese, Japanese,
  Spanish, Portuguese) ruled out by antoine on 24 Oct (`rejected.md`); ion-repo#T-30 keeps no French
  summary.
