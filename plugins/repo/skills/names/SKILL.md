---
name: names
description: Choose the names above the chat's messages - the person's, their Claude's - by default their git name and Claude. Use when the user wants another name for themselves or for Claude in the chat, or from `/repo:look`.
argument-hint: "[the person's name] [Claude's name]"
---

Talk to the user in their language; nothing outside `~/.claude/` is touched.

The mod `chat.tsx` writes the person's name above their messages and Claude's above its replies.
It reads them from `~/.claude/chat-names.json` (`{"person": "...", "claude": "..."}`, each key
optional); a missing or empty key falls back to the real name: `git config user.name` for the
person, `Claude` for Claude.

1. Read `~/.claude/chat-names.json` (absent: `{}`) and `git config user.name`.
2. With `$ARGUMENTS`, the first word is the person's name, the rest Claude's: go to 3. Otherwise
   ask both with the AskUserQuestion tool, in one call, two questions:
   - how the person wants to be called: their real name first, as `<git name> (Recommended)`,
     then the first name it holds when it differs (`antoine-tena` gives `Antoine`), then the
     current choice if it is another one. "Other" takes any name typed.
   - how their Claude should be called: `Claude (Recommended)` first, then the current choice if
     it is another one. "Other" takes any name typed.
3. Write `~/.claude/chat-names.json` (`python3 -I` with `json`, indent 2, `ensure_ascii=False`): a
   real name chosen is left out of the file, so a later change of `git config user.name` follows.
   No key left: remove the file. When `chezmoi source-path ~/.claude/chat-names.json` answers,
   `chezmoi re-add` it and say chezmoi's repo has it to commit.
4. The mod reads the names again within ten seconds: the next message shows them. Ask whether
   they suit; if not, back to 2.
