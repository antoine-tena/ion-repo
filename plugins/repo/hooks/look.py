#!/usr/bin/env python3
"""At a session's start, now and then: Claude asks whether the person wants another look for the
status line (its style, its colors, those of the chat among them), on any machine where the
`repo` plugin is on, in any folder.

"Yes" runs the skill `/repo:statusline`; "Not now" asks again after 50, 200, then every 1000
sessions; "Never" closes it. Paced by `reminders.py` under the key `statusline`, counted once
per session start. Called by `session_start.py`; silent when not due.
"""

import reminders

KEY = reminders.STATUSLINE_KEY
YES, NO, NEVER = "Change the status line", "Not now", "Never ask again"


def answer_command(verdict: str) -> str:
    return f"`{reminders.SCRIPT} {verdict} {KEY}`"


def question() -> str:
    return (
        "After any other question ion-repo asks at this start, ask the user with the "
        "AskUserQuestion tool, in their language, whether they want another look for the status "
        "line: its style, its colors, among them those of the chat, theirs and Claude's "
        f'("{YES}", "{NO}", "{NEVER}"). If "{YES}": skill `/repo:statusline`. If "{NO}": '
        f'{answer_command("no")}. If "{NEVER}": {answer_command("never")}. Then resume their '
        "request."
    )


def context() -> str:
    """The question when it is due, after counting this session; empty otherwise."""
    state = reminders.load()
    reminders.count_session(state, KEY)
    reminders.save(state)
    return question() if reminders.is_due(state, KEY) else ""
