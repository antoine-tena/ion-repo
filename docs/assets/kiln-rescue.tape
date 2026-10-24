# The README's second demo: an old Django repo rescued. `kiln score` on a public repo kept
# deliberately outdated (antoine-tena/kiln-demo-legacy), `kiln adopt`, `kiln fix`, the roadmap
# left to Claude Code, `/kiln:modernize` working through it, then `kiln score` again. Replay it
# from kiln's root before each release candidate (needs vhs, ttyd, ffmpeg and a logged-in
# Claude Code; it spends a real session, about 10 minutes):
#
#     vhs docs/assets/kiln-rescue.tape
#     scripts/shrink_demo.sh docs/assets/kiln-rescue.gif 96 <still from> <still to>
#
# The second line cuts the stretch where Claude Code's summary stands still (its run takes five
# to ten minutes) and brings the GIF under 5 MB.
#
# A real run from this checkout, played at 1.5 times its speed and cut while it waits. Claude
# Code's part is a time-lapse: a glimpse every 15 seconds, as VHS cannot speed one part up. It
# runs as a visitor's would (`scripts/demo_shell.sh`): none of this machine's settings, kiln's
# plugin from this checkout. `tests/test_docs.py` fails when a command typed here is no longer
# kiln's.

Output docs/assets/kiln-rescue.gif

Set Shell "bash"
Set FontSize 22
Set Width 1280
Set Height 880
Set Padding 28
Set WindowBar Colorful
Set BorderRadius 10
Set Framerate 20
Set PlaybackSpeed 1.5
Set TypingSpeed 50ms
Set Theme { "name": "kiln", "black": "#1c1b19", "red": "#cd3223", "green": "#82be6e", "yellow": "#f79628", "blue": "#8fa7c4", "magenta": "#e68278", "cyan": "#8fbcb0", "white": "#e6e3dc", "brightBlack": "#5f5f5c", "brightRed": "#e0574a", "brightGreen": "#9dd389", "brightYellow": "#ffe178", "brightBlue": "#a9bfd9", "brightMagenta": "#f0a39b", "brightCyan": "#a8d1c6", "brightWhite": "#ffffff", "background": "#1c1b19", "foreground": "#e6e3dc", "selection": "#3a3833", "cursor": "#f79628" }

# The first frame, the one shown when animations are paused, already says what is run.
Hide
Type "source scripts/demo_shell.sh"
Enter
Wait+Line@2m /\$$/
Type "git clone -q https://github.com/antoine-tena/kiln-demo-legacy && cd kiln-demo-legacy"
Show
Sleep 1s
Enter
Wait+Line@1m /\$$/
Type "kiln score"
Sleep 600ms
Enter
Sleep 7s

Type "clear && git switch -qc rescue && kiln adopt"
Sleep 600ms
Enter
Hide
Wait+Line@3m /\$$/
Show
Sleep 5s
Type `clear && git add -A && git commit -qm "chore: adopt kiln" && kiln fix`
Sleep 600ms
Enter
Hide
Wait+Line@5m /\$$/
Show
Sleep 7s

Type "clear && kiln score --roadmap"
Sleep 600ms
Enter
Sleep 9s

Type `clear && claude --permission-mode auto "/kiln:modernize the whole roadmap, one gap after another, on this branch, without asking"`
Sleep 1s
Enter
# Claude Code asks whether to trust a folder it has never seen.
Wait+Screen@1m /trust this folder/
Sleep 1.5s
Down
Sleep 800ms
Enter
Sleep 6s

# The time-lapse: Claude Code at work, a glimpse every 15 seconds.
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms
Hide
Sleep 15s
Show
Sleep 400ms

# Claude Code writes "· done" and the time once its turn ends.
Hide
Wait+Screen@90m /· done \d{1,2}:\d{2}/
Show
Sleep 6s
Hide
Type "/exit"
Enter
Wait+Line@1m /\$$/
Type "clear"
Enter
Show
Type "kiln score"
Sleep 600ms
Enter
Sleep 9s

# A cleared screen, so the wait reads it again.
Hide
Type `clear && cd / && rm -rf "$KILN_DEMO_HOME" && echo "demo folder removed"`
Enter
Wait+Screen@2m /demo folder removed/
