#!/usr/bin/env python3
"""Shared session utilities for commandbase-session hooks and skills.

Provides path normalization, repo layout detection, session map operations,
atomic I/O, git/worktree operations, and log summarization utilities.

No external dependencies -- stdlib only.
"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# 1. Path utilities
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 2-3. Repo layout detection
# ---------------------------------------------------------------------------

def detect_repo_layout(cwd):
    """Detect whether cwd is inside a bare-repo worktree or a regular repo.

    Returns "bare-worktree" or "regular".
    """
    try:
        common_dir = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            capture_output=True, text=True, cwd=cwd, timeout=5
        ).stdout.strip()
        git_dir = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True, text=True, cwd=cwd, timeout=5
        ).stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        return "regular"

    # Normalize for comparison
    common_abs = os.path.normpath(os.path.join(cwd, common_dir))
    git_abs = os.path.normpath(os.path.join(cwd, git_dir))

    if common_abs != git_abs:
        return "bare-worktree"
    return "regular"


def get_container_dir(cwd):
    """Return the container directory path.

    For bare-worktree: parent of .bare/ (found via --git-common-dir).
    For regular repo: repo root (git rev-parse --show-toplevel).
    """
    layout = detect_repo_layout(cwd)

    if layout == "bare-worktree":
        try:
            common_dir = subprocess.run(
                ["git", "rev-parse", "--git-common-dir"],
                capture_output=True, text=True, cwd=cwd, timeout=5
            ).stdout.strip()
            # common_dir points to .bare/ -- container is its parent
            bare_abs = os.path.normpath(os.path.join(cwd, common_dir))
            return os.path.dirname(bare_abs)
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass

    # Regular repo: use show-toplevel
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=cwd, timeout=5
        )
        if result.returncode == 0:
            return normalize_path(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass

    return cwd


# ---------------------------------------------------------------------------
# 4-7. Session map operations
# ---------------------------------------------------------------------------

def get_session_map_path(cwd):
    """Return the path to session-map.json.

    For bare-worktree: <container>/session-map.json
    For regular repo: <repo-root>/.claude/sessions/session-map.json
    """
    layout = detect_repo_layout(cwd)
    container = get_container_dir(cwd)

    if layout == "bare-worktree":
        return os.path.join(container, "session-map.json")
    else:
        return os.path.join(container, ".claude", "sessions", "session-map.json")


def read_session_map(cwd):
    """Read and parse session-map.json. Returns dict (empty if missing/corrupt)."""
    map_path = get_session_map_path(cwd)
    if not os.path.exists(map_path):
        return {}
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, IOError, OSError):
        pass
    return {}


def update_session_map(cwd, session_id, entry):
    """Read-modify-write session-map.json with atomic write.

    Args:
        cwd: Current working directory (used to locate session-map.json).
        session_id: The session ID key.
        entry: Dict with keys like name, branch, worktree, created, status.
    """
    session_map = read_session_map(cwd)
    session_map[session_id] = entry
    map_path = get_session_map_path(cwd)
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    atomic_write_json(map_path, session_map)


def resolve_session(cwd, session_id=""):
    """Resolve the session name for the given cwd and/or session_id.

    Resolution order:
    1. Worktree path match in session-map.json (bare-worktree layout)
    2. session_id key lookup in session-map.json
    3. Legacy _current file fallback

    Returns session name string, or "" if no session found.
    """
    cwd_norm = os.path.normpath(cwd)
    session_map = read_session_map(cwd)

    # 1. Worktree path match
    for _sid, entry in session_map.items():
        wt = entry.get("worktree", "")
        if wt and os.path.normpath(normalize_path(wt)) == cwd_norm:
            return entry.get("name", "")

    # 2. session_id key lookup
    if session_id and session_id in session_map:
        entry = session_map[session_id]
        return entry.get("name", "")

    # 3. Legacy _current fallback
    layout = detect_repo_layout(cwd)
    if layout == "regular":
        sessions_dir = os.path.join(cwd, ".claude", "sessions")
    else:
        # In a worktree, .claude/sessions/ is per-worktree
        try:
            toplevel = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, cwd=cwd, timeout=5
            ).stdout.strip()
            sessions_dir = os.path.join(normalize_path(toplevel), ".claude", "sessions")
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
            sessions_dir = os.path.join(cwd, ".claude", "sessions")

    current_file = os.path.join(sessions_dir, "_current")
    if os.path.exists(current_file):
        try:
            with open(current_file, "r") as f:
                return f.read().strip()
        except (IOError, OSError):
            pass

    return ""


# ---------------------------------------------------------------------------
# 8. Session directory operations
# ---------------------------------------------------------------------------

def get_session_dir(cwd, session_name):
    """Return .claude/sessions/{session_name}/ path relative to worktree root.

    Creates the directory if it doesn't exist.
    """
    layout = detect_repo_layout(cwd)

    if layout == "bare-worktree":
        try:
            toplevel = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, cwd=cwd, timeout=5
            ).stdout.strip()
            worktree_root = normalize_path(toplevel)
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
            worktree_root = cwd
    else:
        worktree_root = cwd

    session_dir = os.path.join(worktree_root, ".claude", "sessions", session_name)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


# ---------------------------------------------------------------------------
# 9. Atomic I/O
# ---------------------------------------------------------------------------

def atomic_write_json(path, data):
    """Atomic JSON write via temp file + os.replace().

    Writes to {path}.tmp then atomically replaces. On failure, cleans up
    the temp file. os.replace() is atomic on both POSIX and NTFS.
    """
    tmp_path = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        # Clean up temp file on failure
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# 10-11. Log utilities
# ---------------------------------------------------------------------------

def summarize_input(tool_input):
    """Extract the most relevant part of tool input for logging."""
    if isinstance(tool_input, dict):
        for key in ("command", "file_path", "pattern", "query"):
            if key in tool_input:
                return str(tool_input[key])[:200]
        return str(tool_input)[:200]
    return str(tool_input)[:200]


def summarize_response(response):
    """Truncate response for log storage (500 chars)."""
    return str(response)[:500]


# ---------------------------------------------------------------------------
# 12-14. Git/worktree operations (reference implementations)
# ---------------------------------------------------------------------------

def create_worktree(container_dir, branch_name, worktree_name):
    """Create a git worktree.

    Runs: git worktree add <container>/<worktree_name> -b <branch_name>
    from the .bare directory.
    """
    bare_dir = os.path.join(container_dir, ".bare")
    worktree_path = os.path.join(container_dir, worktree_name)
    result = subprocess.run(
        ["git", "worktree", "add", worktree_path, "-b", branch_name],
        capture_output=True, text=True, cwd=bare_dir, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"git worktree add failed: {result.stderr.strip()}")
    return worktree_path


def remove_worktree(container_dir, worktree_name):
    """Remove a git worktree.

    Runs: git worktree remove <container>/<worktree_name>
    """
    bare_dir = os.path.join(container_dir, ".bare")
    worktree_path = os.path.join(container_dir, worktree_name)
    result = subprocess.run(
        ["git", "worktree", "remove", worktree_path],
        capture_output=True, text=True, cwd=bare_dir, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"git worktree remove failed: {result.stderr.strip()}")


def migrate_to_bare_repo(repo_path):
    """One-time migration from regular repo to bare repo + worktrees.

    Steps:
    1. Verify clean git state
    2. Detect default branch
    3. Move .git to .bare, configure as bare
    4. Create main worktree
    5. Copy untracked files
    6. Create container-level session-map.json

    Returns (container_path, main_worktree_path).

    NOTE: This is a reference implementation. In practice, the
    /starting-session skill presents these commands for the user to run,
    since Claude Code's cwd changes during migration.
    """
    # 1. Verify clean state
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=repo_path, timeout=10
    )
    if result.stdout.strip():
        raise RuntimeError("Repository has uncommitted changes. Commit or stash first.")

    # 2. Detect default branch
    branch_result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        capture_output=True, text=True, cwd=repo_path, timeout=5
    )
    if branch_result.returncode == 0:
        default_branch = branch_result.stdout.strip().split("/")[-1]
    else:
        list_result = subprocess.run(
            ["git", "branch", "--list", "main", "master"],
            capture_output=True, text=True, cwd=repo_path, timeout=5
        )
        branches = [b.strip().lstrip("* ") for b in list_result.stdout.strip().split("\n") if b.strip()]
        default_branch = branches[0] if branches else "main"

    parent_dir = os.path.dirname(repo_path)
    repo_name = os.path.basename(repo_path)
    container_path = os.path.join(parent_dir, repo_name)
    migrating_path = os.path.join(parent_dir, f"{repo_name}-migrating")

    # 3. Move repo, set up bare
    os.rename(repo_path, migrating_path)
    os.makedirs(container_path, exist_ok=True)
    os.rename(os.path.join(migrating_path, ".git"), os.path.join(container_path, ".bare"))

    subprocess.run(
        ["git", "config", "core.bare", "true"],
        cwd=os.path.join(container_path, ".bare"), timeout=5
    )

    # 4. Create main worktree
    main_worktree = os.path.join(container_path, "main")
    subprocess.run(
        ["git", "worktree", "add", main_worktree, default_branch],
        cwd=os.path.join(container_path, ".bare"), timeout=30
    )

    # 5. Copy untracked files (best-effort)
    for dirname in [".claude", ".docs"]:
        src = os.path.join(migrating_path, dirname)
        dst = os.path.join(main_worktree, dirname)
        if os.path.isdir(src):
            # Copy contents, don't overwrite existing
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if not os.path.exists(d):
                    if os.path.isdir(s):
                        import shutil
                        shutil.copytree(s, d)
                    else:
                        import shutil
                        shutil.copy2(s, d)

    # 6. Create container-level session-map.json
    atomic_write_json(os.path.join(container_path, "session-map.json"), {})

    # 7. Clean up
    import shutil
    shutil.rmtree(migrating_path, ignore_errors=True)

    return container_path, main_worktree
