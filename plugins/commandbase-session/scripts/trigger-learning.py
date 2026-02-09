#!/usr/bin/env python3
"""PreCompact hook: nudges /learning-from-sessions when errors exist."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_utils import normalize_path, resolve_session, get_session_dir


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check for active session
    cwd = normalize_path(input_data.get("cwd", "."))
    session_id = input_data.get("session_id", "")
    session_name = resolve_session(cwd, session_id)

    if not session_name:
        sys.exit(0)  # No session, no nudge

    # Check if errors exist
    session_dir = get_session_dir(cwd, session_name)
    errors_path = os.path.join(session_dir, "errors.log")

    if not os.path.exists(errors_path):
        sys.exit(0)  # No errors, no nudge

    try:
        with open(errors_path, "r") as f:
            error_count = sum(1 for line in f if line.strip())
    except (IOError, OSError):
        sys.exit(0)

    if error_count == 0:
        sys.exit(0)

    # Nudge Claude toward /learning-from-sessions
    print(
        f"SESSION LEARNING REMINDER: This session ({session_name}) has "
        f"{error_count} error(s) logged in .claude/sessions/{session_name}/errors.log. "
        f"Note: these are real-time subagent errors only. Complete error harvesting "
        f"runs at session end (Stop hook). For full error coverage, run "
        f"/learning-from-sessions at the start of the next session. "
        f"To capture what's available now, run /learning-from-sessions.",
        file=sys.stderr,
    )
    sys.exit(2)  # Exit 2 sends stderr to Claude as feedback


if __name__ == "__main__":
    main()
