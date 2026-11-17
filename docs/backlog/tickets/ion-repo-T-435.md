# ion-repo#T-435 · The Ion logo in flight, animated
- **Type**: idea
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-11-04
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine, 4 November 2026: the new logo (an ion in flight) kept static for now, its
  animation set aside "to see later"

A preview exists on antoine's machine (`~/.local/share/ion-logo/ion-en-vol-anime.py`): a
particle simulation, not a filter. The ion flies in from the left and brakes to its place, a
flash flows back along its trail, the head bobs and sheds particles that cool from white to
violet, then the frame melts pixel for pixel into the static logo; 7 ms a frame, synchronized
output. Only a terminal typed in by a person shows it (not Claude's Bash, not the session-start
notice, not logs or CI), and it delays the command.
- [ ] Decide where: the home screen alone (`ion-repo`, `--help`), about 1.2 s, any key skips it;
  the README's logo as an animated SVG, where most people would see it.
