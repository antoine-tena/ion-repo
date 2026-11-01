#!/usr/bin/env python3
"""Tokens used since forever, summed over every Claude Code transcript of the machine.

Prints the total (input, output and prompt cache, read and written). The sums per transcript
are kept in a state file: only the transcripts that changed are read again, and a deleted
transcript keeps counting. Run in the background by statusline.py, through its cache.
"""

import json
import os
from pathlib import Path

PROJECTS = Path(os.path.expanduser("~/.claude/projects"))
STATE = Path(os.path.expanduser("~/.cache/claude-statusline/lifetime-tokens-state.json"))
USAGE_KEYS = (
    "input_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
)


def transcript_tokens(path: Path) -> int:
    """The tokens of one transcript, each message counted once (it is logged once per block)."""
    tokens_by_message: dict[str, int] = {}
    with path.open(encoding="utf-8", errors="replace") as transcript:
        for line in transcript:
            if '"usage"' not in line:
                continue
            try:
                message = json.loads(line).get("message") or {}
            except json.JSONDecodeError:
                continue  # a line being written
            usage = message.get("usage") if isinstance(message, dict) else None
            if isinstance(usage, dict):
                key = str(message.get("id") or len(tokens_by_message))
                tokens_by_message[key] = sum(int(usage.get(k) or 0) for k in USAGE_KEYS)
    return sum(tokens_by_message.values())


def load_state() -> dict[str, dict[str, float]]:
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except OSError, json.JSONDecodeError:
        return {}
    return state if isinstance(state, dict) else {}


def main() -> None:
    state = load_state()
    for path in PROJECTS.rglob("*.jsonl"):
        try:
            stat = path.stat()
        except FileNotFoundError:
            continue  # deleted while listed
        known = state.get(str(path)) or {}
        if known.get("size") != stat.st_size or known.get("mtime") != stat.st_mtime:
            tokens = transcript_tokens(path)
            state[str(path)] = {"size": stat.st_size, "mtime": stat.st_mtime, "tokens": tokens}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    partial = STATE.with_suffix(".partial")
    partial.write_text(json.dumps(state), encoding="utf-8")
    partial.replace(STATE)
    print(sum(int(entry.get("tokens") or 0) for entry in state.values()))


if __name__ == "__main__":
    main()
