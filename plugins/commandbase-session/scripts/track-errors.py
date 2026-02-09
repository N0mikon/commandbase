#!/usr/bin/env python3
"""PostToolUseFailure hook: logs errors to session error log.

Only fires in subagent contexts (known Claude Code limitation).
"""
import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_utils import normalize_path, resolve_session, get_session_dir, summarize_input, summarize_response


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
        sys.exit(0)  # No session, no tracking

    # Build log entry
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": input_data.get("session_id", ""),
        "tool": input_data.get("tool_name", "unknown"),
        "input": summarize_input(input_data.get("tool_input", {})),
        "error": summarize_response(input_data.get("tool_response", ""))
    }

    # Append to session error log
    session_dir = get_session_dir(cwd, session_name)
    log_path = os.path.join(session_dir, "errors.log")

    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except (IOError, OSError):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
