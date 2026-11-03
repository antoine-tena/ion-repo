#!/usr/bin/env python3
"""At a session's start, now and then: Claude asks how the person wants to be called in the chat
and how their Claude should be called (`chat.tsx`), on any machine where the `repo` plugin is on,
in any folder.

"Yes" runs the skill `/repo:names`; "Not now" asks again after 50, 200, then every 1000
sessions; "Never" closes it. Paced by `reminders.py` under the key `names`, counted once per
session start. Called by `session_start.py`; silent when not due.
"""

import reminders

KEY = reminders.NAMES_KEY
YES, NO, NEVER = "Choose the names", "Not now", "Never ask again"


def answer_command(verdict: str) -> str:
    return f"`{reminders.SCRIPT} {verdict} {KEY}`"


def question() -> str:
    return (
        "After any other question ion-repo asks at this start, ask the user with the "
        "AskUserQuestion tool, in their language, whether they want to choose how they are called "
        "above their messages in the chat and how their Claude is called above its replies (now "
        f'their git name and "Claude") ("{YES}", "{NO}", "{NEVER}"). If "{YES}": skill '
        f'`/repo:names`. If "{NO}": {answer_command("no")}. If "{NEVER}": '
        f"{answer_command('never')}. Then resume their request."
    )


def context() -> str:
    """The question when it is due, after counting this session; empty otherwise."""
    state = reminders.load()
    reminders.count_session(state, KEY)
    reminders.save(state)
    return question() if reminders.is_due(state, KEY) else ""
