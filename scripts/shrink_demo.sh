#!/usr/bin/env bash
# Brings a recorded demo under the 5 MB that `tests/test_docs.py` allows: a smaller palette and,
# when given, a still stretch cut out (Claude Code's summary left on screen once its turn ends,
# as the time-lapse of `kiln-rescue.tape` is sized for its longest runs). Find the stretch by
# eye on the GIF, then:
#
#     scripts/shrink_demo.sh docs/assets/kiln-rescue.gif 96 49 54.6
#
# keeps 0 to 49 s and 54.6 s to the end, on 96 colours. Needs ffmpeg.
set -euo pipefail
gif="$1" colors="$2"
cut="" source="[0]"
if [ $# -ge 4 ]; then
    cut="[0]trim=0:$3,setpts=PTS-STARTPTS[a];[0]trim=start=$4,setpts=PTS-STARTPTS[b];"
    cut+="[a][b]concat=n=2:v=1[c];"
    source="[c]"
fi
shrunk="$(mktemp --suffix=.gif)"
trap 'rm -f "$shrunk"' EXIT
ffmpeg -loglevel error -y -i "$gif" -filter_complex \
    "${cut}${source}split[x][y];[x]palettegen=max_colors=$colors:stats_mode=diff[p];[y][p]paletteuse=dither=none:diff_mode=rectangle" \
    "$shrunk"
mv "$shrunk" "$gif"
ls -la "$gif"
