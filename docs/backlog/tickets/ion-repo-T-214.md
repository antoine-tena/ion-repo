# ion-repo#T-214 · Instant the second time: one listing, one index, a cache by blob SHA
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Rule format v2 and
  authoring, Speed), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.11, "Instant the second time": One listing from git, one matcher for every rule, a
cache keyed by blob SHA: a warm run recomputes nothing unchanged, in under 50 ms.

- [ ] **A34** The model cached by the blob SHAs of the manifests: every kiln command reuses it in
  milliseconds.
- [ ] **G22** `inputs` declared per rule (the path classes it reads): the incremental engine knows
  what to recompute.
- [ ] **J04** One listing (`git ls-files -s` gives each tracked file's blob SHA for free); contents
  through `git cat-file --batch` when the tree is clean, from disk otherwise.
- [ ] **J05** A file-to-rules index built once, every rule's globs merged into one matcher: today
  each rule walks every file with its own patterns.
- [ ] **J06** Only the files some applicable rule needs are read; sizes from `git cat-file
  --batch-check` skip the huge ones before reading.
- [ ] **J07** YAML through libyaml's `CSafeLoader` when present, several times faster than the
  pure-Python loader.
- [ ] **J08** All text rules for one file type in a single scan (a combined automaton: a regex set,
  or Hyperscan where a measurement says so).
- [ ] **J10** A cache keyed by blob SHA, rule hash and engine version in `~/.cache/kiln/score/`: a
  warm run recomputes nothing unchanged, in under 50 ms.
- [ ] **J22** The repo and CI models cached across commands (score, fix, dev, check) and across
  runs.
- [ ] **J25** The grid compiled once into one index (each rule's `applies`, inputs and detector),
  at build or on the first run: a run parses only the rules whose facts the repo has, and a test
  proves a Django repo loads no Go rule. Measured on 26 October 2026: 138 rules parsed one by one
  in 30 ms (0.22 ms each), so the plan's 800 or so would cost about 170 ms on every run; budget:
  under 30 ms whatever the grid's size.
