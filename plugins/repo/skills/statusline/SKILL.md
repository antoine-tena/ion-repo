---
name: statusline
description: Change the look of the status line - its style, its colors, among them the chat's (the person's and Claude's) - each shown before it is chosen. Use when the user wants another status line, other colors for it, or from `/repo:look`.
argument-hint: "[a style] [a palette]"
---

Talk to the user in their language. The choice is made with ion-repo's machine settings, nothing
else is touched.

The status line is `plugins/repo/scripts/statusline.py` of ion-repo. Its style and its palette
are machine settings (`ion repo set statusline=… statusline_palette=…`), read at each redraw: a
change shows within 5 seconds, no restart. `ion repo set` without a value, run in `~` (a repo
ion-repo did not generate refuses it), lists the choices and the current ones.

1. Read the current choices: `cd ~ && ion repo set` (lines `statusline` and `statusline_palette`).
2. With `$ARGUMENTS`, a known style and/or palette is the choice: go to 4.
3. Ask both with the AskUserQuestion tool, in one call, two questions, each option with a
   `preview` drawn by the script itself, in plain text (`python3 <script> --style <style>
   --palette <palette> <<<'{}' | sed 's/\x1b\[[0-9;]*m//g'`, the script's path from the
   `statusLine` command of `~/.claude/settings.json`):
   - the style: the current one first, then the others of `plain`, `band`, `classic`,
     `classic-band` (`none`: no status line; `custom`: their own, left as it is, both through
     "Other").
   - the colors: `chat` first, the person's color and Claude's from the chat, then the current
     palette if it is another one, then two others that stand apart. "Other" takes any palette
     `ion repo set` lists.
   A palette's name says nothing to the person: offer each by its colors, from `python3 <script>
   --levels` (each palette's four levels in the current theme, `#rrggbb`). Its label names its
   four colors in plain words, in the user's language (`Gris, jaune, orange, rouge`), with
   `(Recommended)` after the first; its description says what each color means, one level each:
   all well (the neutral one, most of the line), to watch (not urgent), to handle (fairly
   urgent), urgent (in French: `Normal`, `À surveiller`, `À traiter`, `Urgent`), then the
   palette's name for `ion repo set`. Its preview lists the four levels, one a line, each with
   its color's name and hex; `chat` adds that the person's color is theirs in the chat, the
   orange Claude's.
4. `ion repo set statusline=<style> statusline_palette=<palette>` (only what changed).
5. Ask whether it suits, the status line being redrawn already; if not, back to 3. With `chat`,
   say it follows `/repo:color`: a new color for their messages is the status line's too.
