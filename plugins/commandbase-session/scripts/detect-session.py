# Session skills v2 validated
#!/usr/bin/env python3
"""SessionStart hook: bridges native session_id into conversation context.

Detects repo layout and reports session/worktree info to Claude via stdout
(exit 0 with stdout injects context into conversation for SessionStart hooks).
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
    get_session_dir,
    update_meta_json,
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
        )
        sys.exit(0)

    # Read container-level session-map.json
    session_map = read_session_map(cwd)
    container = get_container_dir(cwd)
    cwd_norm = os.path.normpath(cwd)

    # Find ACTIVE session matching this worktree (not ended/handed-off)
    matched_entry = None
    for _sid, entry in session_map.items():
        wt = entry.get("worktree", "")
        if wt and os.path.normpath(normalize_path(wt)) == cwd_norm:
            if entry.get("status") == "active":
                matched_entry = entry
                break

    if matched_entry:
        name = matched_entry.get("name", "unknown")
        branch = matched_entry.get("branch", "unknown")
        status = matched_entry.get("status", "active")
        worktree = matched_entry.get("worktree", cwd)

        # Persist Claude session UUID to meta.json
        if session_id and name:
            try:
                session_dir = get_session_dir(cwd, name)
                update_meta_json(session_dir, session_id)
            except Exception:
                pass  # Don't crash the hook on meta.json write failure

        summary = matched_entry.get("summary", "")
        summary_line = f"\nPurpose: {summary}" if summary else ""
        print(
            f'SESSION DETECTED: "{name}" on branch {branch} (status: {status}).{summary_line}\n'
            f"Worktree: {worktree}\n"
            f"Session ID: {session_id}",
        )
    else:
        # In bare repo but no matching session -- likely main worktree
        print(
            f"MAIN BRANCH: Working in {cwd} on main. "
            f"Run /starting-session to create a session branch.\n"
            f"Session ID: {session_id}",
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
