#!/usr/bin/env python3
"""PostToolUseFailure hook: logs errors to session error log.

Only fires in subagent contexts (known Claude Code limitation).
"""
import json
import subprocess
import sys
import os
from datetime import datetime, timezone


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
        sys.exit(0)  # No session, no tracking

    # Build log entry
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": input_data.get("session_id", ""),
        "tool": input_data.get("tool_name", "unknown"),
        "input": _summarize_input(input_data.get("tool_input", {})),
        "error": _summarize_response(input_data.get("tool_response", ""))
    }

    # Append to session error log
    session_dir = os.path.join(cwd, ".claude", "sessions", session_name)
    os.makedirs(session_dir, exist_ok=True)
    log_path = os.path.join(session_dir, "errors.log")

    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except (IOError, OSError):
        sys.exit(1)

    sys.exit(0)


def _summarize_input(tool_input):
    """Extract the most relevant part of tool input for logging."""
    if isinstance(tool_input, dict):
        for key in ("command", "file_path", "pattern", "query"):
            if key in tool_input:
                return str(tool_input[key])[:200]
        return str(tool_input)[:200]
    return str(tool_input)[:200]


def _summarize_response(response):
    """Truncate response for log storage."""
    return str(response)[:500]


if __name__ == "__main__":
    main()
