# ion-repo#T-386 · Sessions named on their own: at the branch, then at the ticket
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: the user, 2026-10-30: which Keramos tool should rename Claude sessions? kiln, not
  grog (grog rereads finished sessions, on request: too late and too rare for a name that serves
  while the session lives and to resume it; it reads the names, it does not give them)

ion-repo#T-344 names a session only when someone runs `kiln pause`, and left the rest to Claude Code's
`/rename` and its automatic title. Most sessions end unnamed by us, though kiln already knows
what each one works on: `suggested_names()` in `src/kiln/pause.py` draws a name from the branch,
the ticket in progress and the last commit, with no call to the model (no token spent).
- [ ] When `/kiln:worktree` creates the branch, the session takes the branch made readable as its
  name; when `/kiln:backlog start ion-repo#T-NN` runs, it becomes `ion-repo#T-NN: <title>`. A session left on the
  integration branch keeps Claude Code's own title.
- [ ] A name the user gave (`/rename`, `kiln pause "<name>"`) is never overwritten.
- [ ] Where the name lives, decided first: `/rename` appends
  `{"type":"custom-title","customTitle":…,"sessionId":…}` to the session's transcript (seen
  on 2026-10-30, beside Claude Code's `ai-title` lines), an undocumented format written by the
  live process. Either a supported way for a hook or a command to set that title exists, or
  kiln keeps its own name in `~/.local/state/kiln/sessions/<id>.json` (as `kiln pause` does) and
  shows it in its status line and the list at session start, Claude Code's title untouched.
- [ ] grog's `/grog:distill` offers the sessions by these names.
