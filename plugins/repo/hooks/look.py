#!/usr/bin/env python3
"""At a session's start: Claude asks whether the person wants to change the look of the chat and
the status line (their color, their name, Claude's name, the status line's style and colors), on
any machine where the `repo` plugin is on, in any folder.

A question of taste, no update: asked once, then again only when what `/repo:look` offers grows
(`NEWS` in `reminders.py`, its new things in `WHATS_NEW`), whatever the answer; "Never" closes it
for good. "Yes" runs the skill `/repo:look`. Called by `session_start.py`; silent when not due.
"""

import reminders

KEY = reminders.LOOK_KEY
YES, NO, NEVER = "Change the look", "Not now", "Never ask again"
# What each version of `/repo:look` brought, told when the question comes back for it.
WHATS_NEW = {
    1: "their color, their name and Claude's above the messages, the status line in the chat's "
    "colors",
}


def answer_command(verdict: str) -> str:
    return f"`{reminders.SCRIPT} {verdict} {KEY}`"


def news(since: int) -> str:
    return "; ".join(text for version, text in sorted(WHATS_NEW.items()) if version > since)


def question(since: int) -> str:
    new = f" (new: {news(since)})" if since > 0 else ""
    return (
        "After any other question ion-repo asks at this start, ask the user with the "
        "AskUserQuestion tool, in their language, whether they want to change the look of the "
        "chat and the status line: their color, their name and Claude's above the messages, the "
        f'status line\'s style and colors{new} ("{YES}", "{NO}", "{NEVER}"). If "{YES}": skill '
        f'`/repo:look`. If "{NO}": {answer_command("no")}. If "{NEVER}": '
        f"{answer_command('never')}. Then resume their request."
    )


def context() -> str:
    """The question when it is due, after counting this session; empty otherwise."""
    state = reminders.load()
    entry = reminders.count_session(state, KEY)
    reminders.save(state)
    return question(int(entry.get("version", 0))) if reminders.is_due(state, KEY) else ""
