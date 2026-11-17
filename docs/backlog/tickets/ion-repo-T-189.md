# ion-repo#T-189 · A stranger's first run: no install, never a crash, the next step printed
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every forge, CI, host and
  machine, Nothing to do), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.4, "The first week with strangers": promoted after the launch.
What the launch brings in (issues, reports, the first gap reports of ion-repo#T-38) comes first; these give
way to it. From here each milestone is announced (ion-repo#T-118).

- [ ] On Windows without WSL, `kiln score` says what to do (WSL and its link) instead of a
  traceback; ion-repo#T-94 stays declined (decision 38 of 26 October 2026).
- [ ] **A29** Shallow clones, sparse checkouts, partial clones, worktrees, bare repos and submodules
  handled; what wasn't checked out is said, never guessed.
- [ ] **C20** The integration branch read from the remote's HEAD (main, master, develop, trunk),
  never assumed.
- [ ] **K01** One command, no install: `uvx kiln-cli score`. Documented beside it: `pipx run
  --python 3.14 kiln-cli score` (an older Python fails on PEP 758 syntax), Homebrew, a container
  image pinned by digest.
- [ ] **K10** Never a crash: a broken file is a finding, a rule that throws is reported as a kiln
  bug (with `/kiln:report`'s hint), and the run goes on.
- [ ] **K11** The next step always printed as one command: "`kiln fix` closes 5 of these 9 gaps, on
  a branch, no token".
- [ ] **K20** On a machine, `kiln install` (ion-repo#T-161) is the only setup; in a repo, there is none.
