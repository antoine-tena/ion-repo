# Releases

A candidate every two days, about 4 of its 7 session-hours planned, the rest margin. The launch of
11 November 2026 is cancelled and has no new date (antoine, 30 October 2026: a few more months of
work on his machine first), so no release below carries a date. Every open ticket has its release and is listed under it, the
1,070 [kiln score ideas](../kiln-score-the-thesis.md) included: each became a box of a ticket (ion-repo#T-186 to
ion-repo#T-319, or the existing ticket it extended) in the release it was planned in (antoine, 25 October
2026: everything a ticket, in one format, in its place). A milestone takes its minor in the release
that reaches it, so the work leading to it carries the minor before: every common stack is v0.7.x,
and v0.8.0 is the release where the last one is scored. Each stack gets two releases, about what
Django and Nuxt each took once the engine is set aside, and its pack holds the rules of its most
used frameworks as well as its language's (framework coverage review of 26 October 2026: Spring
Boot, ASP.NET Core, Laravel, Rails; the Node back ends a release of their own). The stacks come in
the order of the 2025 surveys until the corpus measures its own, and games and R have a release each
(stack coverage review of the same day). The launch's releases (v0.5.0 to v0.5.4) keep their order:
they are what a launch needs, whenever it comes, and what comes after them is written for after it.
Once antoine sets a date, they are dated back from it, and he may move other releases ahead of them. The public view of this plan is
[`ROADMAP.md`](../../../ROADMAP.md), drawn from these files by `scripts/roadmap.py`.

## Shipped: v0.4.0 to v0.4.10
- v0.4.0 · kiln speaks English: promoted on Mon 19 Oct, the milestone decided by antoine
  (⚠ breaking, all converted by `kiln update`).
- v0.4.1 · The grid, as data: `kiln grid`, 105 drafts from the reference repo.
- v0.4.2 · Any repo scored against the best, in seconds: ion-repo#T-125, ion-repo#T-46, ion-repo#T-157.
- v0.4.3 · What a script can fix, fixed by script: ion-repo#T-126, ion-repo#T-127, ion-repo#T-128.
- v0.4.4 · The rest handed to Claude: ion-repo#T-129, ion-repo#T-161, and most of ion-repo#T-130 (the template's gaps
  closed), promoted on Wed 21 Oct.
- v0.4.5 · Cheaper sessions, CI only at the release: promoted on Fri 23 Oct, with the outside
  fixes #54 to #56 (thanks @NathanBarrachin). Its planned theme slipped: ion-repo#T-90's rest moved to
  v0.4.11, ion-repo#T-130's proof to v0.5.0, ion-repo#T-160 to v0.6.23.
- v0.4.6 · Every issue closed, adoption at full strength: promoted on Mon 26 Oct (urgent, on
  antoine's request: no repo of the code folder runs candidates since they all follow `beta`),
  `kiln adopt` at the level of `kiln new`, #42 to #44 and #58 to #60.
- v0.4.7 to v0.4.9 · pnpm 11 in repos kiln did not make: promoted on Mon 26 Oct, three fixes
  outside the plan (a front without a lockfile, build scripts `allowBuilds` does not list, in
  `kiln install` then in `kiln ci` and the workflows); the planned releases moved by three numbers.
- v0.4.10 · Every gap seen, wherever the code lives: promoted on Fri 30 Oct.
- v0.4.12 · The `kiln` alias fixed, urgent on antoine's request (1 Nov): its notice said once,
  the Homebrew formula keeping `kiln`; cut from v0.4.11 with these two fixes only, the planned
  releases moved by one number.
