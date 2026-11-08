# Cases for `claude plugin eval`

Adapted from Anthropic's skill-creator (Apache-2.0, `../LICENSE.txt`): its `evals.json`,
assertions and trigger queries become the case folders `claude plugin eval` reads.

Each case is a folder `plugins/<tool>/evals/<case>/` holding `prompt.md` (front matter, then the
user's sentence) and `graders/*.md` (one file per check). Name the folder after what it tests
(`prompt`, `prompt-subagent`, `none-rename`), never `eval-0`.

## Trigger case

```
plugins/<tool>/evals/<skill>/prompt.md
---
tags: [trigger, <skill>]
max_turns: 3
timeout_seconds: 120
allowed_tools: [Skill, Read, Glob, Grep]
---

<the sentence a user would type>
```

```
plugins/<tool>/evals/<skill>/graders/fires.md
---
type: tool_used
tool: Skill
input_match: '"skill":\s*"(<tool>:)?<skill>"'
---
```

A near miss is the same `prompt.md` tagged `[trigger, none]`, folder `none-<what>`, whose grader
allows no skill (copy one of `plugins/repo/evals/none-*/`).

Good sentences are real: casual or formal, a typo, a path, a bit of context, the user's
language. Bad: "Create a chart". The should-fire ones vary the wording of one intent and include
cases where the user never names the skill. The near misses share words with it but need
something else: an adjacent skill, Claude alone, a question rather than a task. An obviously
unrelated sentence tests nothing.

## Behavior case

```
plugins/<tool>/evals/<skill>-<what>/prompt.md
---
tags: [behavior, <skill>]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

<a full task, with the context a real user gives>
```

```
plugins/<tool>/evals/<skill>-<what>/graders/<expectation>.md
---
type: llm
weight: 1
---

<one fact a reader of the transcript can check: "the prompt opens with the goal and its why",
"no secret appears in the answer">
```

One grader per expectation, each named after what it checks so the report reads at a glance.
An expectation any answer would meet (a file exists, some text came back) proves nothing: check
the content. What needs taste is left to the user's eye, not forced into a grader.

Tools beyond `Read`, `Glob`, `Grep`, `Skill` (`Bash`, `Write`, `Edit`) are gated: the run needs
`--allow-tools`, which `ion repo eval-skills` does not pass. Prefer cases that answer in text;
otherwise give the user the `claude plugin eval` line with `--allow-tools`.
