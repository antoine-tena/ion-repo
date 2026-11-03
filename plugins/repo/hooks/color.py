#!/usr/bin/env python3
"""At a session's start, now and then: Claude asks whether the person wants another color for
their bar in the chat (`chat.tsx`), on any machine where the `repo` plugin is on, in any folder.

"Yes" runs the skill `/repo:color`; "Not now" asks again after 50, 200, then every 1000 sessions;
"Never" closes it. Paced by `reminders.py` under the key `color`, counted once per session start.
Called by `session_start.py`; silent when not due.
"""

import reminders

KEY = reminders.COLOR_KEY
YES, NO, NEVER = "Change my color", "Not now", "Never ask again"


def answer_command(verdict: str) -> str:
    return f"`{reminders.SCRIPT} {verdict} {KEY}`"


def question() -> str:
    return (
        "After any other question ion-repo asks at this start, ask the user with the "
        "AskUserQuestion tool, in their language, whether they want another color for the bar "
        f'beside their messages in the chat ("{YES}", "{NO}", "{NEVER}"). If "{YES}": skill '
        f'`/repo:color`. If "{NO}": {answer_command("no")}. If "{NEVER}": '
        f"{answer_command('never')}. Then resume their request."
    )


def context() -> str:
    """The question when it is due, after counting this session; empty otherwise."""
    state = reminders.load()
    reminders.count_session(state, KEY)
    reminders.save(state)
    return question() if reminders.is_due(state, KEY) else ""
