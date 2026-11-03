# Writing a skill

Adapted from Anthropic's skill-creator (Apache-2.0, `../LICENSE.txt`).

## Anatomy

```
<name>/
├── SKILL.md        front matter (name, description) + instructions
├── references/     docs read when a step points to them
├── scripts/        code for deterministic or repeated work
└── assets/         files used in the output (templates, icons)
```

Three levels load in turn: the name and description always (in every session where the plugin
is on, so every word costs), the body when the skill fires, the bundled files only when a step
opens them (a script runs without being read). Keep the body under 500 lines; past that, split
into `references/` with a clear pointer saying when to read each. A reference over 300 lines
opens with a table of contents. A skill covering several variants (frameworks, hosts) keeps the
choice in `SKILL.md` and one reference per variant, so Claude reads only the one it needs.

## The description

It is the whole triggering mechanism: Claude sees only names and descriptions when it decides.
Say what the skill does, then when to use it, in the words a user really types, including the
cases where it should win over a close skill or over Claude doing it alone. Claude tends to
under-use skills, so the `Use when …` part is concrete and a little insistent; but Ion's
descriptions stay under 300 characters, so every word must earn its place. Claude consults a
skill for work it cannot do easily alone: a one-step request ("read this file") will not fire
any skill, whatever the description.

## The body

- Imperative, in the order of the work.
- The why of each step rather than CAPITALS: a model that knows why a rule exists applies it to
  the cases the skill did not foresee. ALWAYS or NEVER in capitals is a yellow flag: reframe.
- General, not fitted to the examples it was tested on: it will run on sentences nobody wrote.
- An exact output format, when one matters, shown as a template; an example when the form is
  unusual (input, then output).
- Lean: cut what does not change what Claude does. Write a draft, then reread it as someone
  who has never seen this conversation.
- No surprise: a skill does what its description says, nothing hidden, nothing that would
  shock the user if described (no data sent away, no access beyond the task).

## Ion's conventions

- English for Claude, the user's language for what the user reads.
- A step that a command could do without tokens belongs in the tool's command, and the skill
  calls it: a script in `scripts/` is the fallback when no command fits.
- The end-of-work answer follows the debrief output style inside the [SKILL-FRAME].
- Every skill, command, setting and hook appears in the repo's two references and its READMEs.
