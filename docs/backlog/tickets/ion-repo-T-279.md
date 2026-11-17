# ion-repo#T-279 · History: secrets ever committed, heavy blobs, hotspots
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Speed, History, forge and
  registries, The roadmap for Claude, Git and versions), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.47, "History: what every clone carries": Secrets once committed, heavy blobs, locks
drifting from their manifests, each blob read once and cached; hotspots open the roadmap.

The six drafts are questions about history: `--history` (M) gives them detectors.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A33** Git LFS patterns known: a binary tracked by LFS is fine, the same binary outside it is
  a finding.
- [ ] **J24** History scans incremental: each commit's blobs scanned once, ever (the cache knows
  them by SHA), so `--history` costs seconds after the first run.
- [ ] **M01** Secrets ever committed, scanned through history (each blob once, cached): a key
  removed but never rotated is still a key.
- [ ] **M02** Heavy blobs in history, which every clone carries forever: git-filter-repo or LFS
  suggested.
- [ ] **M08** Hotspots: churn times complexity per file (Adam Tornhill's method). The roadmap opens
  hotspots first, since that is where the next bug will be.
- [ ] **M12** A lock changed without its manifest, or the reverse, in history: drift caught at its
  source.
- [ ] **O05** Hotspots first among equals (M): the places that change most are fixed first.
- [ ] **GV10** `NO-SECRETS-IN-HISTORY`: secret patterns searched in every reachable blob, not only
  the tree; critical. The fix rotates first; history is rewritten only on the user's decision. L5 ·
  fix J · adopt.
- [ ] **GV11** `NO-LARGE-BLOBS`: no blob over about 5 MB in history outside LFS. L5 · fix J · adopt.
- [ ] **GV12** `LFS-FOR-BINARIES`: large binary assets tracked by LFS or stored elsewhere. L0 · fix
  J · trial.
