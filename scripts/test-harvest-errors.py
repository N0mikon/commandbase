#!/usr/bin/env python3
"""Verification tests for harvest-errors.py"""
import json
import os
import sys
import tempfile
import subprocess

HOOK_PATH = os.path.expanduser("~/.claude/hooks/harvest-errors.py")
PASS = 0
FAIL = 0


def test(name, passed):
    global PASS, FAIL
    if passed:
        PASS += 1
        print(f"  PASS: {name}")
    else:
        FAIL += 1
        print(f"  FAIL: {name}")


def run_hook(input_data):
    return subprocess.run(
        ["python3", HOOK_PATH],
        input=json.dumps(input_data),
        capture_output=True, text=True, timeout=10
    )


# ========== Test 1: stop_hook_active guard ==========
print("\n=== Test 1: stop_hook_active guard ===")
with tempfile.TemporaryDirectory() as tmpdir:
    result = run_hook({
        "stop_hook_active": True,
        "session_id": "test-123",
        "transcript_path": "/nonexistent/path.jsonl",
        "cwd": tmpdir,
    })
    test("Exit code is 0", result.returncode == 0)
    test("No files written", not os.path.exists(os.path.join(tmpdir, ".claude")))


# ========== Test 2: No session fast exit ==========
print("\n=== Test 2: No-session fast exit ===")
with tempfile.TemporaryDirectory() as tmpdir:
    transcript = os.path.join(tmpdir, "transcript.jsonl")
    with open(transcript, "w") as f:
        f.write("{}\n")

    result = run_hook({
        "session_id": "test-123",
        "transcript_path": transcript,
        "cwd": tmpdir,
    })
    test("Exit code is 0", result.returncode == 0)
    test("No errors.log created", not os.path.exists(
        os.path.join(tmpdir, ".claude", "sessions")
    ))


# ========== Test 3: Error detection (mixed patterns) ==========
print("\n=== Test 3: Error detection with mixed patterns ===")
with tempfile.TemporaryDirectory() as tmpdir:
    session_dir = os.path.join(tmpdir, ".claude", "sessions")
    os.makedirs(session_dir)
    with open(os.path.join(session_dir, "_current"), "w") as f:
        f.write("test-session")
    os.makedirs(os.path.join(session_dir, "test-session"), exist_ok=True)

    transcript = os.path.join(tmpdir, "transcript.jsonl")
    lines = [
        # file-history-snapshot (should be skipped)
        {"type": "file-history-snapshot", "snapshot": {}},
        # assistant tool_use: Read
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_001", "name": "Read",
             "input": {"file_path": "/nonexistent/file.txt"}}
        ]}},
        # tool_result: is_error=true (should be caught)
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_001", "is_error": True,
             "content": "<tool_use_error>File does not exist.</tool_use_error>"}
        ]}},
        # assistant tool_use: Bash (success)
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_002", "name": "Bash",
             "input": {"command": "echo hello"}}
        ]}},
        # tool_result: success (should be skipped)
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_002", "is_error": False,
             "content": "hello\nExit code: 0"}
        ]}},
        # assistant tool_use: Bash (failure)
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_003", "name": "Bash",
             "input": {"command": "cat /nonexistent"}}
        ]}},
        # tool_result: Bash non-zero exit (is_error=false, should be caught)
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_003", "is_error": False,
             "content": "cat: /nonexistent: No such file or directory\nExit code: 1"}
        ]}},
        # progress entry (subagent, should be skipped entirely)
        {"type": "progress", "data": {"type": "hookEvent"}},
        # assistant tool_use: Edit (sibling error)
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_004", "name": "Edit",
             "input": {"file_path": "/test.txt", "old_string": "x", "new_string": "y"}}
        ]}},
        # tool_result: Sibling error (should be skipped)
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_004", "is_error": True,
             "content": "<tool_use_error>Sibling tool call errored</tool_use_error>"}
        ]}},
        # assistant tool_use: Write (real error)
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_005", "name": "Write",
             "input": {"file_path": "/test.txt", "content": "hello"}}
        ]}},
        # tool_result: real Write error
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_005", "is_error": True,
             "content": "<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>"}
        ]}},
        # assistant tool_use: user rejected
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_006", "name": "ExitPlanMode", "input": {}}
        ]}},
        # tool_result: user rejection (should be skipped)
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_006", "is_error": True,
             "content": "The user doesn't want to proceed with this tool use. The tool use was rejected."}
        ]}},
    ]
    with open(transcript, "w") as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")

    result = run_hook({
        "session_id": "test-session-id",
        "transcript_path": transcript,
        "cwd": tmpdir,
    })
    test("Exit code is 0", result.returncode == 0)

    log_path = os.path.join(session_dir, "test-session", "errors.log")
    test("errors.log exists", os.path.exists(log_path))

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            entries = [json.loads(line) for line in f if line.strip()]

        test(f"Exactly 3 errors logged (got {len(entries)})", len(entries) == 3)

        if len(entries) >= 3:
            test("Error 1 is Read tool", entries[0]["tool"] == "Read")
            test("Error 1 has harvest source", entries[0]["source"] == "harvest")
            test("Error 1 has session_id", entries[0]["session_id"] == "test-session-id")

            test("Error 2 is Bash tool", entries[1]["tool"] == "Bash")
            test("Error 2 input is 'cat /nonexistent'",
                 entries[1]["input"] == "cat /nonexistent")

            test("Error 3 is Write tool", entries[2]["tool"] == "Write")
            test("Error 3 contains 'not been read'",
                 "not been read" in entries[2]["error"])

        tools_in_log = [e["tool"] for e in entries]
        test("No Edit (sibling) in log", "Edit" not in tools_in_log)
        test("No ExitPlanMode (user cancel) in log",
             "ExitPlanMode" not in tools_in_log)
    else:
        print("  SKIP: errors.log not found, skipping content checks")


# ========== Test 4: Deduplication ==========
print("\n=== Test 4: Deduplication ===")
with tempfile.TemporaryDirectory() as tmpdir:
    session_dir = os.path.join(tmpdir, ".claude", "sessions")
    os.makedirs(os.path.join(session_dir, "dedup-session"))
    with open(os.path.join(session_dir, "_current"), "w") as f:
        f.write("dedup-session")

    log_path = os.path.join(session_dir, "dedup-session", "errors.log")
    existing_entry = json.dumps({
        "timestamp": "2026-01-01T00:00:00+00:00",
        "session_id": "old-session",
        "tool": "Read",
        "input": "/nonexistent/file.txt",
        "error": "File does not exist.",
        "source": "track-errors",
    })
    with open(log_path, "w") as f:
        f.write(existing_entry + "\n")

    transcript = os.path.join(tmpdir, "transcript.jsonl")
    lines = [
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_dup1", "name": "Read",
             "input": {"file_path": "/nonexistent/file.txt"}}
        ]}},
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_dup1", "is_error": True,
             "content": "<tool_use_error>File does not exist.</tool_use_error>"}
        ]}},
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_dup2", "name": "Bash",
             "input": {"command": "false"}}
        ]}},
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_dup2", "is_error": False,
             "content": "\nExit code: 1"}
        ]}},
    ]
    with open(transcript, "w") as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")

    result = run_hook({
        "session_id": "test-dedup",
        "transcript_path": transcript,
        "cwd": tmpdir,
    })
    test("Exit code is 0", result.returncode == 0)

    with open(log_path, "r") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    test(f"Exactly 2 entries total (1 existing + 1 new, got {len(entries)})",
         len(entries) == 2)

    if len(entries) == 2:
        test("First entry is original (track-errors source)",
             entries[0]["source"] == "track-errors")
        test("Second entry is new Bash error (harvest source)",
             entries[1]["source"] == "harvest" and entries[1]["tool"] == "Bash")


# ========== Test 5: Backfill empty error text ==========
print("\n=== Test 5: Backfill empty error text ===")
with tempfile.TemporaryDirectory() as tmpdir:
    session_dir = os.path.join(tmpdir, ".claude", "sessions")
    os.makedirs(os.path.join(session_dir, "backfill-session"))
    with open(os.path.join(session_dir, "_current"), "w") as f:
        f.write("backfill-session")

    log_path = os.path.join(session_dir, "backfill-session", "errors.log")
    # Pre-populate with an entry that has empty error text
    # (simulates track-errors logging a subagent error with no response text)
    empty_error_entry = json.dumps({
        "timestamp": "2026-01-01T00:00:00+00:00",
        "session_id": "old-session",
        "tool": "Read",
        "input": "/missing/file.txt",
        "error": "",
    })
    with open(log_path, "w") as f:
        f.write(empty_error_entry + "\n")

    # Transcript has the same error but WITH error text
    transcript = os.path.join(tmpdir, "transcript.jsonl")
    lines = [
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "tool_bf1", "name": "Read",
             "input": {"file_path": "/missing/file.txt"}}
        ]}},
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool_bf1", "is_error": True,
             "content": "<tool_use_error>File does not exist: /missing/file.txt</tool_use_error>"}
        ]}},
    ]
    with open(transcript, "w") as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")

    result = run_hook({
        "session_id": "test-backfill",
        "transcript_path": transcript,
        "cwd": tmpdir,
    })
    test("Exit code is 0", result.returncode == 0)

    with open(log_path, "r") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    test(f"Still 1 entry (not duplicated, got {len(entries)})", len(entries) == 1)

    if len(entries) == 1:
        test("Error field is now populated",
             "File does not exist" in entries[0]["error"])
        test("Source is 'backfilled'", entries[0]["source"] == "backfilled")
        test("Tool is still Read", entries[0]["tool"] == "Read")
        test("Input is still /missing/file.txt",
             entries[0]["input"] == "/missing/file.txt")


# ========== Summary ==========
print(f"\n{'='*40}")
print(f"Results: {PASS} passed, {FAIL} failed")
if FAIL > 0:
    sys.exit(1)
print("All tests passed!")
