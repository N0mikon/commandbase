#!/usr/bin/env python3
"""Stop hook: harvests errors from session transcript at session end.

Parses the full JSONL transcript and backfills errors.log with any
main-conversation tool errors missed by the real-time track-errors hook
(which only fires in subagent contexts via PostToolUseFailure).

Skips:
- progress entries (subagent errors, already covered by track-errors)
- file-history-snapshot entries (internal bookkeeping)
- user-rejected tool uses ("Sibling tool call errored", user cancel)

Always exits 0 — never exit 2 (which would restart the conversation).
"""
import json
import re
import subprocess
import sys
import os
from datetime import datetime, timezone


EXIT_CODE_RE = re.compile(r"Exit code: (\d+)")
SKIP_ERRORS = frozenset([
    "Sibling tool call errored",
    "The user doesn't want to proceed with this tool use.",
])


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


def _summarize_input(tool_input):
    """Extract the most relevant part of tool input for logging."""
    if isinstance(tool_input, dict):
        for key in ("command", "file_path", "pattern", "query"):
            if key in tool_input:
                return str(tool_input[key])[:200]
        return str(tool_input)[:200]
    return str(tool_input)[:200]


def _extract_error_text(content):
    """Extract error text from tool_result content."""
    if isinstance(content, str):
        return content[:500]
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "".join(parts)[:500]
    return str(content)[:500]


def _is_skippable_error(error_text):
    """Check if this error should be skipped (sibling errors, user cancels)."""
    for skip in SKIP_ERRORS:
        if skip in error_text:
            return True
    return False


def _is_tool_error(tool_result):
    """Detect if a tool_result represents an error.

    Returns (is_error, error_text) tuple.

    Detection:
    - is_error === true on the tool_result (Read/Write/Edit failures)
    - Exit code: N where N != 0 in Bash content (is_error is false for these)
    """
    content = tool_result.get("content", "")
    is_error = tool_result.get("is_error")

    # Explicit error flag (Read/Write/Edit failures, tool_use_error)
    if is_error is True:
        error_text = _extract_error_text(content)
        if _is_skippable_error(error_text):
            return False, ""
        return True, error_text

    # Bash non-zero exit code (is_error is False for these)
    text = _extract_error_text(content) if not isinstance(content, str) else content
    match = EXIT_CODE_RE.search(text)
    if match and match.group(1) != "0":
        return True, text[:500]

    return False, ""


def _load_existing_entries(log_path):
    """Load existing errors.log entries for dedup and backfill.

    Returns (entries_list, key_to_index_map) where key is (tool, input).
    """
    entries = []
    key_to_index = {}
    if not os.path.exists(log_path):
        return entries, key_to_index
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    idx = len(entries)
                    entries.append(entry)
                    key = (entry.get("tool", ""), entry.get("input", ""))
                    key_to_index[key] = idx
                except json.JSONDecodeError:
                    continue
    except (IOError, OSError):
        pass
    return entries, key_to_index


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

    # Guard: prevent re-entry if stop hook is already active
    if input_data.get("stop_hook_active"):
        sys.exit(0)

    # Normalize paths
    cwd = normalize_path(input_data.get("cwd", "."))
    transcript_path = normalize_path(input_data.get("transcript_path", ""))

    if not transcript_path or not os.path.exists(transcript_path):
        sys.exit(0)

    # Check for active session
    session_id = input_data.get("session_id", "")
    session_name = _resolve_session(cwd, session_id)

    if not session_name:
        sys.exit(0)

    # Prepare output path
    session_dir = os.path.join(cwd, ".claude", "sessions", session_name)
    os.makedirs(session_dir, exist_ok=True)
    log_path = os.path.join(session_dir, "errors.log")

    # Load existing entries for deduplication and backfill
    existing_entries, existing_keys = _load_existing_entries(log_path)
    backfilled = False

    # Build tool_use_id -> {name, input} index from assistant messages,
    # then match against tool_results in user messages.
    # Stream line-by-line for constant memory.
    tool_index = {}  # tool_use_id -> {"name": str, "input": any}
    new_errors = []

    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                entry_type = obj.get("type", "")

                # Skip non-message entries
                if entry_type in ("file-history-snapshot", "progress"):
                    continue

                if entry_type == "assistant":
                    # Index tool_use blocks
                    msg = obj.get("message", {})
                    content = msg.get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if (
                                isinstance(block, dict)
                                and block.get("type") == "tool_use"
                            ):
                                tool_index[block["id"]] = {
                                    "name": block.get("name", "unknown"),
                                    "input": block.get("input", {}),
                                }

                elif entry_type == "user":
                    msg = obj.get("message", {})
                    content = msg.get("content", [])
                    if not isinstance(content, list):
                        continue

                    for block in content:
                        if not isinstance(block, dict):
                            continue

                        # Skip progress entries embedded in user messages
                        if block.get("type") == "progress":
                            continue

                        if block.get("type") != "tool_result":
                            continue

                        is_err, error_text = _is_tool_error(block)
                        if not is_err:
                            continue

                        # Look up the tool from the index
                        tool_use_id = block.get("tool_use_id", "")
                        tool_info = tool_index.get(tool_use_id, {})
                        tool_name = tool_info.get("name", "unknown")
                        tool_input = _summarize_input(tool_info.get("input", {}))

                        # Deduplicate against existing entries
                        dedup_key = (tool_name, tool_input)
                        if dedup_key in existing_keys:
                            # Backfill: if existing entry has empty error, upgrade it
                            idx = existing_keys[dedup_key]
                            if not existing_entries[idx].get("error", "").strip():
                                existing_entries[idx]["error"] = error_text
                                existing_entries[idx]["source"] = "backfilled"
                                backfilled = True
                            continue
                        existing_keys[dedup_key] = len(existing_entries) + len(new_errors)

                        new_errors.append({
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "session_id": session_id,
                            "tool": tool_name,
                            "input": tool_input,
                            "error": error_text,
                            "source": "harvest",
                        })

    except (IOError, OSError):
        sys.exit(0)

    # Write results
    if backfilled:
        # Rewrite entire file (existing entries updated + new errors)
        try:
            all_entries = existing_entries + new_errors
            with open(log_path, "w", encoding="utf-8") as f:
                for entry in all_entries:
                    f.write(json.dumps(entry) + "\n")
        except (IOError, OSError):
            pass
    elif new_errors:
        # Append-only (no backfills needed)
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                for entry in new_errors:
                    f.write(json.dumps(entry) + "\n")
        except (IOError, OSError):
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
