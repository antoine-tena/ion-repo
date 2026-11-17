# ion-repo#T-145 · A public benchmark: Claude Code with and without kiln
- **Type**: idea
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-18
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026, ideas in reserve ("a public benchmark, Claude Code with
  and without kiln, that could serve as proof"); widened on 21 October 2026 at antoine's
  request: the tokens kiln saves, shown each session

ion-repo#T-53 measures one hypothesis (small files); this one measures the whole promise. Only rtk's
savings are measured live (`rtk gain`); the rest (repo map, skills, charter) can only be
estimated, and an estimate is credible only from a published A/B run.
- [ ] The same tasks given to headless Claude Code (`claude -p`, its usage read per run) on
  local copies of the training repos, with and without kiln, then before and after `kiln fix`
  and `/kiln:modernize`, several runs each: tokens, turns, red CIs, rules broken, tasks done;
  its cost on the Pro quota said before it runs, stopped at the budget.
- [ ] Published with its method and script whatever the result; after ion-repo#T-53, which sets the
  method. If the number is net, it joins the README and the launch (ion-repo#T-03).
- [ ] Status line: rtk's savings since the session started (measured, cached), and the
  benchmark's figure marked `≈` with a link to its method; tokens, never dollars (a Pro plan
  pays no tokens).
