#!/usr/bin/env python3
"""SessionStart hook: bridges native session_id into conversation context.

Detects repo layout and reports session/worktree info to Claude via stderr
(exit 2 injects stderr into conversation context).
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_utils import (
    normalize_path,
    detect_repo_layout,
    read_session_map,
    get_container_dir,
)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    session_id = input_data.get("session_id", "")
    cwd = normalize_path(input_data.get("cwd", "."))

    layout = detect_repo_layout(cwd)

    if layout != "bare-worktree":
        # Not in bare repo pattern
        print(
            f"SESSION ID: {session_id} (regular repo, no worktree layout). "
            f"Run /starting-session to migrate and create a session.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Read container-level session-map.json
    session_map = read_session_map(cwd)
    container = get_container_dir(cwd)
    cwd_norm = os.path.normpath(cwd)

    # Find session matching this worktree
    matched_entry = None
    for _sid, entry in session_map.items():
        wt = entry.get("worktree", "")
        if wt and os.path.normpath(normalize_path(wt)) == cwd_norm:
            matched_entry = entry
            break

    if matched_entry:
        name = matched_entry.get("name", "unknown")
        branch = matched_entry.get("branch", "unknown")
        status = matched_entry.get("status", "active")
        worktree = matched_entry.get("worktree", cwd)
        print(
            f'SESSION DETECTED: "{name}" on branch {branch} (status: {status}).\n'
            f"Worktree: {worktree}\n"
            f"Session ID: {session_id}",
            file=sys.stderr,
        )
    else:
        # In bare repo but no matching session -- likely main worktree
        print(
            f"MAIN BRANCH: Working in {cwd} on main. "
            f"Run /starting-session to create a session branch.\n"
            f"Session ID: {session_id}",
            file=sys.stderr,
        )

    sys.exit(2)


if __name__ == "__main__":
    main()
