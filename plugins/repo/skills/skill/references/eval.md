# Testing a skill

Adapted from Anthropic's skill-creator (Apache-2.0, `../LICENSE.txt`). Only when the user asks
for it, or when a skill misfires or does its job badly: each case is a Claude session on the
user's quota.

1. **Cases**, in `plugins/<tool>/evals/<case>/` (`cases.md`):
   - Trigger: 3 to 5 real sentences the user would type, each tagged `[trigger, <skill>]`;
     plus 2 or 3 near misses (same words, another need) tagged `[trigger, none]`.
   - Behavior, when the output can be checked: 2 or 3 tasks tagged `[behavior, <skill>]`, one
     `type: llm` grader per expectation, each a verifiable fact about the result.
   ion-repo's `repo` plugin commits one trigger case per skill, named after it, and only
   `none-*` beside (`tests/test_eval_skills.py`): the others run for the round, uncommitted.
   Show the user the sentences and expectations before anything runs.
2. **Run**: the user starts it, never Claude (no `claude -p`, no `claude plugin eval` from
   Bash, no subagent standing in for a run). In ion-repo: `ion repo eval-skills --skill <name>`
   (asks for `ok` three times); in another tool's repo, the same lock by hand:
   `claude plugin eval plugins/<tool> --model opus --runs 1 --ablation none -j 1 --max-cost-usd 2 --no-publish --tag <skill> none`.
   `--ablation with-without` also runs each case without the plugin, to measure what the skill
   adds: twice the sessions, say so before offering it.
3. **Read the report** (`plugins/<tool>/evals/results/<timestamp>/aggregate-result.json`, the
   HTML beside it) with `grading.md`: each failed grader and its cause in the transcript, and
   the graders that pass whatever the skill.
4. **Improve** from what failed, generalizing rather than patching the one sentence: the why
   instead of MUSTs, cut what wastes turns, move into a script or the command what every run
   rebuilt; a skill that fires too rarely or too often gets its description rewritten. Rerun
   only the cases concerned. Stop when the user is happy, the cases pass, or a round brings
   nothing.
