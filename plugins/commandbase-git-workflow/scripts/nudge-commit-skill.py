#!/usr/bin/env python3
"""PostToolUse hook: nudge Claude to use /committing-changes for git commits."""
import json
import re
import sys


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    if input_data.get("tool_name") != "Bash":
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")

    # Detect direct git commit or git push
    if re.search(r"\bgit\s+(commit|push)\b", command):
        print(
            "NOTICE: A direct git commit/push was detected. "
            "Per project rules, all commits should go through the "
            "/committing-changes skill, which handles staged file "
            "verification, security review, and commit message standards. "
            "Please use /committing-changes for future commits.",
            file=sys.stderr,
        )
        # Exit 0 — PostToolUse cannot block (tool already ran).
        # stderr on exit 0 is shown to Claude via verbose mode.
        # Use exit 2 to show stderr to Claude as feedback.
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
