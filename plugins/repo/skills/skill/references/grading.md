# Reading the report

Adapted from Anthropic's skill-creator (Apache-2.0, `../LICENSE.txt`): its grader and analyzer
agents, done by Claude itself from the report rather than by subagents.

`claude plugin eval` writes `aggregate-result.json` and an HTML report in
`plugins/<tool>/evals/results/<timestamp>/` (ignored by git). Read the JSON; point the user to
the HTML for the transcripts.

## Each failed grader

1. Find the run's transcript and what the model actually did, not what it said it did.
2. Trigger case: which skill fired instead, or none; what in the description pulled or failed
   to pull. Behavior case: the step of the skill that was skipped, misread or missing.
3. Say whether the skill is at fault or the case is (an unrealistic sentence, an expectation
   the task never asked for). Fix the case only with the user's yes: a case bent to pass hides
   a defect.

## The graders themselves

A passing grader on a weak check is worse than none: it gives false confidence. Flag:

- graders that pass with or without the skill (with `--ablation with-without`): they do not
  measure the skill;
- an outcome that matters and that no grader checks;
- a case that passes on one run and fails on another: rerun it before drawing a conclusion
  from it.

## Across the cases

- The same failure in several cases points to one missing idea in the skill: add it once,
  with its why.
- Runs that all rebuild the same helper (a script, a long command): that helper belongs in
  `scripts/` or in the tool's command.
- Turns and cost against the baseline: a skill that wins on score but triples the turns may
  need a leaner body.

Report to the user in a few lines: what passed, each failure with its cause, the change
proposed. Then improve, and rerun only the cases concerned.
