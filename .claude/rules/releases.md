---
paths:
  - "CHANGELOG.md"
  - "src/kiln/release.py"
  - "src/kiln/shipping.py"
  - "src/kiln/versions.py"
  - "src/kiln/github_ci.py"
  - "tests/test_shipping.py"
  - "scripts/refresh_images.py"
  - ".github/workflows/kiln.yml"
  - ".github/workflows/pypi.yml"
  - "plugins/kiln/skills/release/**"
---

# kiln's releases

**Why** (antoine's choices): kiln must stay stable for the repos that depend on it while it
changes a lot, so a release first runs as a candidate on its own repos (`-rc.N`, like Python or
Linux) and only ships once it has proven itself, measured rather than assumed. 0.x semver, made
for a start where anything can break (like uv or ruff), rather than a fourth number. Clients
update at every release, fixes included.

**Numbering**: like Claude Code (2.1.301 in October 2026), not like Vercel CLI (64 majors, a
number that no longer says anything). Nobody depends on kiln through a range (`^0.3`): repos cite
its workflows at the exact tag and only move through `kiln update`, which converts what breaks.
The number dates a release; the release note says what changes. From Next.js, the discipline
(candidates, breaking changes first in the notes, automatic migration), not the numbering.
- In 0.x every release bumps the patch (`v0.3.1`, `v0.3.2`… `v0.3.192` if need be).
- The minor moves only for a milestone decided by antoine (`kiln version cut --minor`). Decided:
  v0.5.0 public launch (T-03), v0.6.0 Claude works alone in the repo, v0.7.0 kiln for teams and
  organizations, v0.8.0 every common stack scored, v0.9.0 any CI, machine and size, v1.0.0 the
  stability promise, just before the community modules (T-69). Their content and the v1.0.0 bar
  are in the backlog (`## 🚀 Releases`, `## 🧭 Vision`); `ROADMAP.md`'s two hand-written
  milestone tables follow them.
- From 1.0, strict semver like Next.js: breaking → major (rare and planned), `feat` → minor, the
  rest → patch. `kiln version` (`release.py`) proposes the number and says which candidates are
  ready.

**Rhythm**: one release every two days (the session budget: the how-to of
`docs/backlog/backlog.md`). The second day of a release absorbs overruns and lets the candidate
run on the `internal` channel before its promotion (promoted 45 minutes after it came out, a
candidate has checked nothing). Breaking changes stay grouped at the milestones; a security fix
ships at once. What spares users is grouping the question: `kiln update` crosses every late
release at once (one note per release crossed), the in-session reminder only comes back at the
pace set by `kiln set update-reminders` (once a week by default, T-45), and kiln-bot (T-59) will
make the update free.

**Two stages**, through `/kiln:release` (no deployment: the tag publishes, and the promoted tag
publishes the `kiln-cli` package on PyPI through `pypi.yml`):
1. **Candidate**: branch `release/vX.Y.Z` from `develop`, a `## vX.Y.Z — date` entry at the top
   of `CHANGELOG.md`, `version = "X.Y.Z"` in `pyproject.toml`, the template's image digests
   refreshed (`uv run python scripts/refresh_images.py`), the demos re-recorded if what they show
   changed (`.claude/rules/docs.md`), the full checks, the branch pushed, **GitHub CI awaited on
   its commit** (macOS and the end-to-end tests only run there: v0.4.0's rc.1 had gone out on a
   red nobody read), tag `vX.Y.Z-rc.1` pushed only on green. A fix of the candidate: a `fix:`
   commit on its branch, tag `-rc.N+1`.
2. **Promotion**, when `kiln version` says it's ready, on facts (`release.py`): the candidate's
   GitHub CI is green, **24 hours of soak** since its tag (each `-rc.N` restarts the count), and
   **at least one repo of the code folder updated to it** (`kiln update` passed the repo's checks
   there). **Fast lane**: a candidate with only fixes since the last public release (no `feat`,
   nothing breaking) ships after **2 hours**, no repo required; a security fix ships at once.
   Then: tag `vX.Y.Z` on the exact commit of its last candidate, merge into `main`, back into
   `develop`.

**Channels**: `public` (the default) only sees promoted releases; machines on `internal`
(`kiln set channel=internal`) follow the candidates; antoine's machine is on `beta` (his choice:
while kiln improves fast, a new feature must serve at once): the tool is the `~/code/kiln`
checkout installed as editable, so `develop` read live, with neither version nor update;
releases remain what goes out to others.

**Other repos**: generated repos cite kiln's workflows at the exact tag they start from
(`ci.yml`), and `kiln update` moves it forward. On antoine's machine a release stops at the
candidate or at the promotion: neither run nor offer `kiln update --all` (nor `--rehearse`); a
candidate is checked through the witness repo (`antoine-tena/kiln-rehearsal`) and local copies,
and antoine updates his repos himself.
