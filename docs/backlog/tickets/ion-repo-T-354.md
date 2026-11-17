# ion-repo#T-354 · Fast CI: the generated test suites in parallel
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q85: "CI is always the longest, but it matters a
  lot: as complete and fast as possible"; Q112: the reference repo's `kiln ci`, 25 min 59 s of
  which pytest 1,497 s), decision 33

- [ ] The Django template runs pytest across cores (pytest-xdist), with the test settings that cost
  nothing in safety (a fast password hasher, emails in memory); TE19 `PARALLEL-TESTS` promoted.
- [ ] Measured on a copy of the reference repo, before and after; the job's duration in `kiln ci`'s
  verdict.
- [ ] What `kiln ci` does not replay yet, said on 26 October: the end-to-end job (its own
  services), the `infra` and `sbom` workflows.
