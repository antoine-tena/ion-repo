# The README's demo: `kiln new`, its three questions, then `kiln check` on the new repo.
# Replay it from kiln's root before each release candidate (needs vhs, ttyd and ffmpeg):
#
#     vhs docs/assets/kiln-new.tape
#
# A real run from this checkout (Django + Nuxt, without GitHub), played at 1.5 times its speed and
# cut while it waits: the durations kiln prints are the real ones. The waits are fixed, generous
# and hidden, as VHS stops reading the screen once it scrolls. `tests/test_docs.py` fails when a
# command typed here is no longer kiln's.

Output docs/assets/kiln-new.gif

Set Shell "bash"
Set FontSize 22
Set Width 1280
Set Height 880
Set Padding 28
Set WindowBar Colorful
Set BorderRadius 10
Set Framerate 20
Set PlaybackSpeed 1.5
Set TypingSpeed 60ms
Set Theme { "name": "kiln", "black": "#1c1b19", "red": "#cd3223", "green": "#82be6e", "yellow": "#f79628", "blue": "#8fa7c4", "magenta": "#e68278", "cyan": "#8fbcb0", "white": "#e6e3dc", "brightBlack": "#5f5f5c", "brightRed": "#e0574a", "brightGreen": "#9dd389", "brightYellow": "#ffe178", "brightBlue": "#a9bfd9", "brightMagenta": "#f0a39b", "brightCyan": "#a8d1c6", "brightWhite": "#ffffff", "background": "#1c1b19", "foreground": "#e6e3dc", "selection": "#3a3833", "cursor": "#f79628" }

# The first frame, the one shown when animations are paused, already says what is run.
Hide
Type "source scripts/demo_shell.sh"
Enter
Wait+Line@2m /\$$/
Type "kiln new my-app --no-github"
Show
Sleep 1.5s
Enter
Sleep 3s
Type "1"
Sleep 600ms
Enter
Sleep 2.2s
Type "2"
Sleep 600ms
Enter
Sleep 2s
Enter
Sleep 9s
Hide
Sleep 50s
Show
Sleep 6s

Type "cd my-app && kiln check"
Sleep 900ms
Enter
Sleep 7s
Hide
Sleep 40s
Show
Sleep 8s

# A cleared screen, so the wait reads it again: the demo folder weighs about 500 MB.
Hide
Type `clear && cd / && rm -rf "$KILN_DEMO_HOME" && echo "demo folder removed"`
Enter
Wait+Screen@2m /demo folder removed/
