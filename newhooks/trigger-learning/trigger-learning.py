#!/usr/bin/env python3
"""PreCompact hook: nudges /learning-from-sessions when errors exist."""
import json
import subprocess
import sys
import os


def normalize_path(path):
    """Convert MINGW paths (/c/...) to Windows paths (C:\\...) on win32."""
    if sys.platform != "win32" or not path.startswith("/"):
        return path
    try:
        result = subprocess.run(
            ["cygpath", "-w", path], capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    return path


def _resolve_session(cwd, session_id):
    """Resolve session name from session-map.json, fall back to _current."""
    sessions_dir = os.path.join(cwd, ".claude", "sessions")

    # Try session-map.json first (concurrent-safe)
    map_path = os.path.join(sessions_dir, "session-map.json")
    if session_id and os.path.exists(map_path):
        try:
            with open(map_path, "r", encoding="utf-8") as f:
                session_map = json.load(f)
            entry = session_map.get(session_id)
            if entry:
                return entry.get("name", "")
        except (json.JSONDecodeError, IOError, OSError):
            pass

    # Fall back to _current (backward compat)
    current_file = os.path.join(sessions_dir, "_current")
    if os.path.exists(current_file):
        try:
            with open(current_file, "r") as f:
                return f.read().strip()
        except (IOError, OSError):
            pass

    return ""


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check for active session
    cwd = normalize_path(input_data.get("cwd", "."))
    session_id = input_data.get("session_id", "")
    session_name = _resolve_session(cwd, session_id)

    if not session_name:
        sys.exit(0)  # No session, no nudge

    # Check if errors exist
    errors_path = os.path.join(cwd, ".claude", "sessions", session_name, "errors.log")

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
