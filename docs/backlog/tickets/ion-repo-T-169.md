# ion-repo#T-169 · `kiln new` asks about your situation, not about tools
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: antoine, 24 October 2026: "what should `kiln new` ask to fit the user best?"

Ask only what kiln cannot guess and what really changes the repo, worded the way a senior
engineer would ask a beginner: who uses it, what happens if it breaks, never "Django or
FastAPI?". Today: what you build, the size ("How big are the stakes?"), the language; the
description defaults to `"{{ title }}."`, so `CLAUDE.md`, the README and the north star start
empty for Claude.
- [ ] "What is it for, in one sentence?" (free text, Enter skips): fills `description`, and the
  north star when `--goal` is not given. The most useful line for Claude per keystroke.
- [ ] The size deduced from three concrete questions instead of the four notches: who uses it
  (me / people I know / the public), who works on it (alone / two or three / several teams), if
  it breaks (nothing serious / annoying / money or data lost); kiln then says "→ medium".
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
- [ ] Built with ion-repo#T-184 (the tailored door): one recap, one machine profile for both.
