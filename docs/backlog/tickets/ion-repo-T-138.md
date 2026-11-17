# ion-repo#T-138 · Less code to carry, measured first: the compressor's dry run
- **Type**: idea
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026, fourth pillar ("slim down", a lead): writing code
  costs almost nothing now, its mass is the problem

- [ ] `kiln score` gains the slimming pillar: unused dependencies (deptry, knip), dead code
  (vulture), measured on the reference repo and on the study's repos.
- [ ] The upkeep ahead, next to it: how many dependency releases the repo will absorb in a year,
  how many breaking, which ends of life are coming (libyear measures the lag behind; this
  measures what is coming), and how much removing the unused dependencies lowers it.
- [ ] The number decides the rest: "−22 % of lines, −9 dependencies, same behaviour" is worth
  building; a few percent is not.

From the kiln score ideas of 24 October 2026:
- [ ] **M10** Code untouched for years and imported by nothing: candidates for the compressor
  (ion-repo#T-138).
