# ion-repo#T-184 · `kiln new` tailored: it starts from what you know, then what the project needs
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: antoine, 24 October 2026: "kiln new should offer two modes: one like today, and
  another with a ton of questions where the user ticks the languages they use most, the same
  for frameworks".

Two doors at the start of `kiln new`: "Quick: 3 questions, kiln picks the rest" (default, made
better by ion-repo#T-169) and "Tailored: your profile, your project, every setting (~5 min)", which
replaces `--all-questions` (today Copier's raw questionnaire). Rule for every question: its
answer changes a generated file, or it is written into a "Project context" section of
`CLAUDE.md`; none is lost. Each question says what it changes, takes "I don't know" (kiln's
default and its reason), and each section can be skipped ("later").

Stage 1, on what the template already has (this ticket's effort):
- [ ] The profile, about the person, kept on the machine (`~/.config/kiln/config.toml`,
  `machine.py`), never in `.copier-answers.yml` (a team repo is not one person's habits):
  languages, then the frameworks of the ticked languages, then databases, JS package manager,
  container engine; three levels per box (know well / a little / want to learn). Filled once,
  used by every `kiln new`, the quick one too; changed by `kiln set profile`.
- [ ] Asked once at install (`kiln install`), at `kiln new` only if never answered (antoine,
  26 October 2026, Q53); with the agent the person uses (ion-repo#T-357) and the profile of structure
  (ion-repo#T-39).
- [ ] Pre-ticked from the repos of the code directory (`fleet.py`): "3 Django repos, 1 Nuxt".
- [ ] "Is this to ship or to learn?": ship recommends within what you know well (React, not
  Vue → Next.js); learn picks a "want to learn" box and makes the Claude rules teach (explain
  each choice, propose before doing).
- [ ] The profile written for Claude too: "knows Python well, new to TypeScript: detail the
  front, be brief on the back".
- [ ] Tools kiln does not generate stay tickable (Go, Rust, PHP, Ruby, C#, Kotlin, Svelte,
  Angular…): "Go: no template yet, report it?", counted with consent like ion-repo#T-38's gap reports,
  to choose the next stacks on facts.
- [ ] Sections: you (ship or learn, developer or not, Claude's autonomy, languages of talk, code
  and commits); the project (purpose in one sentence, type, lifetime); people (who uses it, how
  many in a year, who works on it: the size deduced, not asked); risks (cost of an outage, who is
  told, personal data, money); the stack recommended with its reason and alternatives, the last
  word to the user; operations (where it runs, monthly budget, domain, backups); openness
  (public or private, licence, outside contributions → contributor files, `good-first-issues`);
  kiln's settings (podman, serena, `compact_window`, CI runner, status line, time zone), each
  shown with kiln's choice and why.
- [ ] A numbered recap with the tree about to be generated: Enter generates, a number changes it.
- [ ] Checkboxes in the terminal (questionary or a small menu of ours), with a "1,3,5" fallback
  outside a terminal; a draft kept on Ctrl-C and offered back.
- [ ] `tests/test_questions.py`, the references (both languages), a demo of the profile and the
  recommendation for the README.

Later stages, each its own ticket when planned:
- Stage 2, the features: accounts, emails, payments (the `stripe` plugin), uploads, several
  languages, realtime, search, PWA, accessibility, admin; one at a time, the most ticked first.
  Until one exists, its question only feeds the project context of `CLAUDE.md`.
- Stage 3, the stacks the "not yet" boxes ask for most (Go, Rust, Hono, SvelteKit, Expo…).
- Around: `kiln new --answers <file>` replayed without asking, a team profile exported,
  `kiln new --like <repo>`, `kiln new "<one sentence>"` pre-filling the tailored mode, a local
  form (`kiln new --web`), later an online configurator printing the command.
- Watch: every stack × size × feature must render and pass its checks (`test_template.py`), a
  cost paid at each release; a stack kiln generates but `kiln score` does not grade is said so in
  the recommendation.
