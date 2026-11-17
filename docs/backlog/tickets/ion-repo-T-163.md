# ion-repo#T-163 · Skills call one kiln command, the backlog first
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: antoine, 21 October 2026, after ion-repo#T-162: "skills should use one command line at most"

A skill that runs git, gh and file reads step by step pays each step in tokens and leaves every
output in the conversation, re-read by each later message; a kiln command does the mechanics in
one call and answers in a few lines. The backlog first: one full read costs about 20k tokens
here and 36k in the reference repo, and Claude read it nearly 500 times in three weeks.
- [ ] `kiln backlog next`, `show ion-repo#T-NN`, `add`, `start`, `done`: one ticket in or out, never the
  whole file; `/kiln:backlog` calls them and nothing else.
- [ ] The backlog condensed to what Claude needs (antoine, 26 October 2026: "only for Claude,
  optimize it to the max"): the thesis and appendices whose ideas are all tickets archived, each
  ticket's why in a few lines; tokens measured before and after.
- [ ] Then the mechanical skills, one command each (`merge`, `cleanup`, `worktree`, `update`);
  a skill keeps only what needs judgment.
- [ ] `test_plugins.py`: one shell command per skill at most, the skills that need judgment over
  several commands (`review`, `release`, `contribution`) listed with their reason.
