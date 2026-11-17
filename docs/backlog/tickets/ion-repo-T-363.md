# ion-repo#T-363 · New tools found the week they come out, assessed before recommended
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine, 26 October 2026 ("a technology watch, so that as soon as a tool comes out
  kiln knows"): ion-repo#T-140 watches the tools the grid already names; this finds the ones it doesn't

- [ ] Collection by script, no tokens, once a week: the lines added to the stacks' `awesome-*`
  lists (a diff of their README: curated already), the newsletters' feeds (PyCoder's Weekly,
  Django News, JavaScript Weekly, Vue and Nuxt news), Show HN above a points threshold through
  the Algolia API, the packages whose dependents grow fastest on ecosyste.ms, and the unknown
  packages several gap reports name (ion-repo#T-38). Proven libraries only (`feedparser`, `httpx`, a git
  diff): no crawler of kiln's own.
- [ ] A deterministic filter: already seen (a state file), no stack of kiln's, no licence, no
  release in a year; what is left is a short list, about 5 to 15 a week.
- [ ] A scheduled workflow of kiln's repo (free on a public repo, like ion-repo#T-349) opens or updates one
  issue per week, `Watch, week N`, one line per candidate with its sources; nothing on an empty
  week.
- [ ] Judgment by Claude on that list only, in a normal session (a step of `/kiln:backlog`, or a
  skill of its own): replaces a tool of the grid, completes one, or nothing; a yes becomes a
  ticket or a pull request that adds the rule at `assess`, its sources attached.
- [ ] Known the week it comes out, recommended only on evidence: a new tool enters at `assess`
  and moves to `trial` then `adopt` through ion-repo#T-140's doctrine (maturity, sources, G12's
  `level_history`), never because it is new.
