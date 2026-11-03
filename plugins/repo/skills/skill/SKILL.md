---
name: skill
description: Write, test and improve a skill of an Ion tool's plugin - intent, SKILL.md, trigger and behavior cases for `claude plugin eval`, report read, description tuned. Use when the user wants a new skill, to fix or sharpen one, or to check one fires and does its job.
argument-hint: "[skill, or what it must do]"
metadata:
  author: Anthropic (skill-creator), adapted for Ion
  source: https://github.com/anthropics/skills/tree/main/skills/skill-creator
  license: Apache-2.0 (LICENSE.txt), changed from the original
---

The skill: `$ARGUMENTS`; without it, what the user just asked for. Talk to the user in their
language; the skill itself is written in English (Claude reads it), its answers to the user
in the user's language.

Find where the user stands and start there: an idea (step 1), a draft (step 3), a skill that
misfires or does its job badly (step 4 with its old version as the baseline). If they only want
a quick draft without cases, do that.

1. **Intent.** If this conversation already holds the workflow ("turn this into a skill"), draw
   it from there: the tools used, the order, the corrections the user made. Settle, asking only
   what nothing gives: what the skill lets Claude do, which sentences should start it (and
   which close ones should not), what it hands back, and whether its output can be checked
   (file, command, fixed steps: yes; tone, taste: by the user's eye).
2. **Place.** A skill holds a craft's know-how: it goes in the plugin of the tool of that craft
   (`plugins/<tool>/skills/<name>/SKILL.md` in `ion-<tool>`), never in a client project nor in
   the conversation. Read the plugin's other skills first: one that already covers the need is
   sharpened, not doubled. Name: a plain English verb or word, the folder's name (`/<tool>:<name>`).
   Work on a branch (`/repo:worktree`).
3. **Write the SKILL.md**, following `references/writing.md`:
   - Front matter: `name`, `description`, `argument-hint` when it takes one. The description
     is the only thing Claude sees before choosing it, read at every message of every session:
     what it does, then `Use when …` with the user's own words and the near cases it must win,
     at most 300 characters (`tests/test_plugins.py`).
   - Body: steps in the order of the work, each with its why; under 500 lines, the long parts in
     `references/` (read when a step says so), the repeated mechanics in `scripts/` or, better,
     in the tool's command (Rust or Python, no tokens).
   - End of work: the answer follows the debrief output style, framed by
     `ion-repo frame <tool> <skill>` (the session's [SKILL-FRAME]); don't invent another format.
4. **Cases**, beside the plugin in `plugins/<tool>/evals/<case>/`, as `claude plugin eval` reads
   them (`references/cases.md`):
   - Trigger: 3 to 5 real sentences the user would type, each a case tagged
     `[trigger, <skill>]` with a `tool_used: Skill` grader on `<tool>:<skill>`; plus 2 or 3 near
     misses (same words, another need) tagged `[trigger, none]` that no skill may take.
   - Behavior, when the output can be checked: 2 or 3 tasks tagged `[behavior, <skill>]`, one
     `type: llm` grader per expectation, each a verifiable fact about the result, not "is good".
   ion-repo's own `repo` plugin commits one trigger case per skill, named after it, and only
   `none-*` beside (`tests/test_eval_skills.py`): the other cases run for the round, uncommitted.
   Show the user the sentences and the expectations before running anything.
5. **Run**: each case is a Claude session on the user's quota, so the user starts it, never
   Claude (no `claude -p`, no `claude plugin eval` from Bash, no subagent standing in for a run).
   In ion-repo give `ion repo eval-skills --skill <name>` (it asks for `ok` three times); in
   another tool's repo, the same lock by hand:
   `claude plugin eval plugins/<tool> --model opus --runs 1 --ablation none -j 1 --max-cost-usd 2 --no-publish --tag <skill> none`.
   To measure what the skill adds, `--ablation with-without` runs each case without the plugin
   too (twice the sessions): say so before offering it.
6. **Read the report** (`plugins/<tool>/evals/results/<timestamp>/aggregate-result.json`, the
   HTML report beside it) with `references/grading.md`: each failed grader, why from the
   transcript, and the graders that pass whatever the skill (they prove nothing).
7. **Improve** from what failed, generalizing rather than patching the one sentence: explain the
   why instead of adding MUSTs, cut what makes runs waste turns, move into a script what every
   run rebuilt. A skill that fires too rarely or too often gets its description rewritten,
   then the trigger cases rerun. Repeat 5 to 7 until the user is happy, the cases all pass, or
   a round brings nothing.
8. **Finish**: the docs of the plugin's repo in the same branch (both references, the READMEs,
   the plugin's description in `plugin.json` when the list of skills shows there), the cases
   committed with the skill, then `/repo:merge`. Code or idea taken from another repo: a line
   in `~/code/Ion/sources.md`.
