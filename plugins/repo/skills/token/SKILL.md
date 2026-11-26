---
name: token
description: Set up a service's credentials (PyPI, Stripe, an API, a host…) - the token in Bitwarden when the machine has the `secrets` command, else in `.<service>/token` (chmod 600), and `.<service>/config` on its scope - with one command that pastes the token unseen. Use when a task needs an API key or a token, or when the user wants to give one.
argument-hint: "<service> [what the token is for]"
---

Service: the first word of `$ARGUMENTS` (lowercase, e.g. `pypi`); the rest says what the token
is for. The user always pastes the secret themselves: never ask them to type it in the
conversation, never read it back, never print it, never commit it.

1. At the repo root (`git rev-parse --show-toplevel` of the main tree, not of a worktree), create
   `.<service>/` and add `.<service>/` to `.git/info/exclude` if it is not there; check with
   `git check-ignore -q .<service>/config`.
2. Write `.<service>/config`: `key=value` lines, with comments that say what the token is for,
   the scope to choose when creating it (as narrow as possible) and where it is used (a GitHub
   secret, an env variable…) and how to read it (`# Secrets : secrets get <repo>/.<service>/token`
   when the machine has `secrets`). Keep an existing `config`: complete it, don't overwrite it.
3. Give the direct link of the page that creates the token (e.g.
   https://pypi.org/manage/account/token/), the scope to pick, then this command, to run in
   their own terminal (not with Claude Code's `!`: it waits for keyboard input):

       read -rs -p "<Service> token: " t && printf '%s' "$t" > <root>/.<service>/token && chmod 600 <root>/.<service>/token && unset t && echo " ok"

   Nothing shows while pasting: the token stays hidden and out of the shell history. When the
   machine has the `secrets` command (`command -v secrets`), append
   `&& cd <root> && secrets push .<service>/token && rm .<service>/token`: Bitwarden keeps the
   only copy.
4. When they say it is done: check that it exists without displaying it - in Bitwarden
   (`secrets list` names it), else the file is not empty and is `600` (`stat -c %a`). Then use it
   only inside the command that needs it: `$(secrets get <repo>/.<service>/token)`, else
   `$(cat <root>/.<service>/token)`; `gh secret set <NAME>` reads either on its standard input.
