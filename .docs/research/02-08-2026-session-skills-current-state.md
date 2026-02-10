---
date: 2026-02-08
status: complete
topic: "session-skills-current-state"
tags: [research, session-skills, starting-session, ending-session, resuming-session, learning-from-sessions, bookmarking-code, hooks, infrastructure, bare-repo, worktrees]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 8 commits - session skills v2 overhaul replaced 5 skills with 3, added git branching/worktrees, shared session_utils.py, SessionStart hook, bare repo pattern"
references:
  - plugins/commandbase-session/skills/starting-session/SKILL.md
  - plugins/commandbase-session/skills/ending-session/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-session/scripts/session_utils.py
  - plugins/commandbase-session/scripts/detect-session.py
  - plugins/commandbase-session/scripts/track-errors.py
  - plugins/commandbase-session/scripts/harvest-errors.py
  - plugins/commandbase-session/scripts/trigger-learning.py
---

# Session Skills: Current State Analysis

**Date**: 2026-02-08
**Branch**: master

## Research Question
How do the current session skills work together, what is their architecture, and what are their interaction patterns?

## Summary
The session system (v2) consists of 4 skills, 4 hooks, and 5 Python scripts organized across 2 plugins (commandbase-session and commandbase-core). The v2 overhaul consolidated 5 skills into 3 (starting-session, ending-session, resuming-session), integrated git branching and worktrees as first-class session infrastructure, extracted shared utilities into `session_utils.py`, and added a SessionStart hook for session ID bridging. Each session now creates a dedicated git branch and worktree, giving every session its own isolated workspace directory. All components coordinate through a container-level `session-map.json` and per-worktree state at `.claude/sessions/`. Projects use the "bare repo" pattern where `main/` and session branches are peer worktree directories under a shared container.

## Architecture Overview

### Plugin Distribution

| Plugin | Components | Role |
|--------|-----------|------|
| commandbase-session | 3 skills, 4 hooks, 5 scripts | Session lifecycle management |
| commandbase-core | 1 skill (bookmarking-code) | Checkpoint creation/verification |

### Skill Inventory (v2)

| Skill | Plugin | Trigger Phrases | Purpose |
|-------|--------|----------------|---------|
| `/starting-session` | commandbase-session | `start a session`, `new session`, `begin work on` | Creates git branch + worktree, registers session, migrates repo to bare-repo on first use (replaces `/naming-session`) |
| `/ending-session` | commandbase-session | `end session`, `wrap up`, `merge and end`, `hand this off` | Squash merges session branch to main, removes worktree, optional handoff creation, learning check (replaces `/handing-over`) |
| `/resuming-session` | commandbase-session | `resume session`, `continue session`, `take over`, `switch to session` | Smart auto-detect resume from worktree state or handoff documents (replaces `/resuming-sessions` + `/taking-over`) |
| `/learning-from-sessions` | commandbase-session | `/learn`, `what did we learn` | Extracts reusable knowledge from session errors/discoveries, now with post-session transcript reading mode |
| `/bookmarking-code` | commandbase-core | `/checkpoint create`, `save a checkpoint` | Creates/verifies named git state snapshots (updated for worktree-aware session detection) |

### Hook Inventory

| Hook | Event | Script | Purpose |
|------|-------|--------|---------|
| detect-session | SessionStart | `detect-session.py` | Bridges native session_id into conversation context, persists Claude UUID to meta.json |
| track-errors | PostToolUseFailure | `track-errors.py` | Real-time error logging (subagent context only) |
| harvest-errors | Stop | `harvest-errors.py` | End-of-session transcript parsing for all errors |
| trigger-learning | PreCompact | `trigger-learning.py` | Nudges user to run `/learning-from-sessions` when errors exist |

### Shared Module: session_utils.py

All hook scripts import from `plugins/commandbase-session/scripts/session_utils.py` instead of duplicating code. The module provides:
- `normalize_path()` -- MINGW `/c/...` to `C:\...` conversion
- `detect_repo_layout()` -- Returns `"bare-worktree"` or `"regular"`
- `get_container_dir()` -- Finds the container directory for bare repo or repo root for regular
- `get_session_map_path()`, `read_session_map()`, `update_session_map()` -- Session map I/O
- `resolve_session()` -- Worktree-aware session resolution (worktree match -> session_id -> `_current` fallback)
- `get_session_dir()` -- Returns `.claude/sessions/{name}/` path
- `atomic_write_json()` -- Atomic JSON write via temp file + `os.replace()`
- `update_meta_json()` -- Appends Claude UUIDs to `claudeSessionIds` array
- `summarize_input()`, `summarize_response()` -- Log truncation utilities

## Shared State Layer

Session state is split across two levels:

### Container Level (outside any worktree, not tracked by git)

| File | Format | Written By | Read By |
|------|--------|-----------|---------|
| `session-map.json` | JSON `{session_id: {name, branch, worktree, created, status}}` | `/starting-session`, `/ending-session`, `detect-session.py` | All skills, all hooks |

The container directory sits above all worktrees (e.g., `/c/code/commandbase/`). `session-map.json` lives here because it is a shared registry across all sessions -- putting it inside a worktree would make it invisible to other worktrees.

**session-map.json entry format (v2):**
```json
{
  "<session_id>": {
    "name": "auth-mvp",
    "branch": "feature/auth-mvp",
    "worktree": "/c/code/commandbase/feature/auth-mvp",
    "created": "2026-02-08T12:00:00.000Z",
    "status": "active"
  }
}
```

Status values: `"active"`, `"ended"`, `"handed-off"`. Entries without `status` are treated as `"active"` (lazy migration from v1).

### Per-Worktree Level (gitignored, `.claude/sessions/{name}/`)

| File | Format | Written By | Read By |
|------|--------|-----------|---------|
| `meta.json` | JSON `{sessionId, claudeSessionIds[], name, branch, worktree, created, gitBranch, summary}` | `/starting-session`, `detect-session.py` | `/resuming-session`, `/ending-session`, `/learning-from-sessions` |
| `checkpoints.log` | Pipe-delimited `YYYY-MM-DD-HH:MM \| name \| sha` | `/bookmarking-code` | `/resuming-session`, `/ending-session`, `/bookmarking-code verify` |
| `errors.log` | JSONL `{timestamp, session_id, tool, input, error}` | `track-errors.py`, `harvest-errors.py` | `/resuming-session`, `/ending-session`, `/learning-from-sessions`, `trigger-learning.py` |

### Legacy State (deprecated, read-only fallback)

| File | Format | Written By | Read By |
|------|--------|-----------|---------|
| `_current` | Plain text (session name, no newline) | (no longer written) | `resolve_session()` as last-resort fallback |

`_current` is preserved for backward compatibility with sessions created before the v2 upgrade but is no longer written by any skill.

### Session Resolution Pattern (v2)

All 4 hooks and all skills use `resolve_session()` from `session_utils.py`:

1. **Primary**: For bare-worktree repos, find the session-map.json entry whose `worktree` field matches the current working directory
2. **Fallback**: Look up by `session_id` key in session-map.json
3. **Legacy fallback**: Read `_current` file (for non-migrated repos)
4. **No session**: Return empty string, skip session-specific behavior

This worktree-based approach eliminates the `_current` singleton problem -- each terminal works in its own worktree directory, so there is no race condition.

### External State: Claude's sessions-index.json

Only `/starting-session` reads Claude's native session index at `~/.claude/projects/{encoded-path}/sessions-index.json`. This is read-only -- no skill writes to it. The encoded path format is: `C:\code\commandbase` -> `C--code-commandbase`.

### Bare Repo Container Layout

After migration, a project looks like this:
```
/c/code/commandbase/                  <- container directory
  .bare/                              <- git object store + refs
  session-map.json                    <- shared session registry (outside git)
  main/                               <- worktree: main branch
    .gitignore                         <- includes .claude/sessions/
    .claude/sessions/                  <- gitignored session runtime state
    plugins/
    CLAUDE.md
  feature/auth-mvp/                   <- worktree: session branch
    .claude/sessions/auth-mvp/         <- gitignored session runtime state
      meta.json
      errors.log
      checkpoints.log
  fix/login-timeout/                  <- worktree: another session
```

## Detailed Skill Flows

### 1. /starting-session -- Session Creation (replaces /naming-session)

**Two modes:**

**Mode A: First-Time Migration** (repo not yet bare-repo pattern)
Triggered when `detect_repo_layout(cwd)` returns `"regular"`. One-time per project.
1. Confirm with user that daily path will change (e.g., `/c/code/project` -> `/c/code/project/main/`)
2. Verify clean git state
3. Execute migration: move `.git` to `.bare/`, configure as bare, create main worktree, copy untracked files, create container-level session-map.json
4. Direct user to open Claude Code in the new `main/` worktree

**Mode B: Create Session** (repo already in bare-repo pattern)
1. **Find session ID**: Read from conversation context (injected by SessionStart hook) or sessions-index.json
2. **Choose branch type**: Ask user for `feature/`, `fix/`, or `refactor/` prefix
3. **Name the session**: Auto-suggest kebab-case name (3-40 chars, `^[a-z0-9-]+$`), user confirms
4. **Create branch + worktree**: `git worktree add {type}/{session-name} -b {type}/{session-name}`
5. **Create session state**: mkdir `.claude/sessions/{name}/`, write `meta.json` (with empty `claudeSessionIds` array)
6. **Register in session-map.json**: Atomic write with `name`, `branch`, `worktree`, `created`, `status: "active"`
7. **Direct user**: Instruct to `cd` to new worktree directory

**Iron Law**: NO SESSION WITHOUT USER CONFIRMATION OF NAME AND BRANCH TYPE

### 2. /ending-session -- Session End (replaces /handing-over)

**Three modes:**

**Mode A: Merge End** (default -- squash merge to main)
1. **Verify**: Confirm in a session worktree, not main. If in session worktree, remind user to `cd` to main first (avoids cwd-lock)
2. **Check uncommitted changes**: Require commit or stash first
3. **Conflict detection**: Dry-run merge (`git merge --no-commit --no-ff`), abort if conflicts, present to user
4. **Squash merge**: `git merge --squash <session-branch>` from main worktree
5. **CLAUDE.md review**: Show diff, ask if session-only CLAUDE.md changes should be kept or discarded
6. **Commit + push**: Invoke `/committing-changes` (recognizes squash merge context: pre-staged files, skip stale docs check)
7. **Learning check**: Read errors.log, remind if errors exist
8. **Remove worktree + branch**: `git -C "$bare" worktree remove`, `git -C "$bare" branch -d`, push `--delete` to remote
9. **Update session-map.json**: Set `status: "ended"`

**Mode B: Handoff End** (branch stays open for another session)
1. Verify session context
2. Create handoff document via docs-writer agent (same rich template: tasks, accomplishments, learnings, files, state, next steps)
3. Set `status: "handed-off"` in session-map.json
4. Learning check
5. Keep worktree and branch open

**Mode C: Discard End** (abandon session work)
1. Require explicit confirmation (type session name)
2. Force remove worktree + delete branch
3. Set `status: "ended"`

**Iron Law**: NO SESSION END WITHOUT MERGE VERIFICATION OR EXPLICIT DISCARD

### 3. /resuming-session -- Smart Resume (replaces /resuming-sessions + /taking-over)

**Auto-detection logic:**
- If a file path argument was provided pointing to `.docs/handoffs/` -> Mode B
- If no argument: read session-map.json, list active/handed-off sessions with existing worktrees
- If multiple candidates -> Mode C (picker)

**Mode A: Worktree Resume** (was `/resuming-sessions`)
- Session has an existing worktree (status `"active"`)
1. Read session-map.json, find active sessions with existing worktrees
2. If multiple: present picker with session names, branches, last modified dates
3. Read meta.json, errors.log, checkpoints.log from the selected session's worktree
4. Scan `.docs/handoffs/` and `.docs/learnings/` for related context (staleness auto-update)
5. Present session summary, direct user to worktree directory

**Mode B: Handoff Resume** (was `/taking-over`)
- Session was handed off or a handoff document was provided
1. Read handoff document fully, staleness auto-update
2. Absorb context (tasks, accomplishments, learnings, next steps)
3. Check if session's worktree still exists (direct there, or offer `/starting-session`)
4. Verify git state matches handoff, present takeover summary, get confirmation

**Mode C: Session Picker** (multiple candidates)
- Present unified picker showing active + handed-off sessions + handoff documents
- Route to Mode A or B based on selection

**Staleness detection** (shared, not duplicated per mode): Read `git_commit` from frontmatter -> count commits behind HEAD -> if >3 -> spawn docs-updater agent -> re-read updated version

**Iron Law**: NO RESUME WITHOUT READING SOURCE FILES

### 4. /bookmarking-code -- Checkpoint Management

**Four operations** (unchanged from v1):
- **create "name"**: Check git status -> warn if dirty -> get SHA -> append to checkpoints.log
- **verify "name"**: Find checkpoint -> run `git diff --stat` and `git log --oneline` -> report changes
- **list**: Read checkpoints.log -> display table with Name/Timestamp/SHA/Status
- **clear**: Count entries -> confirm if >5 -> keep last 5 lines

**Session awareness** (updated for v2): Detects repo layout via git commands. For bare-worktree, reads container-level session-map.json, finds entry matching current worktree. Falls back to `_current` for legacy sessions. If no session, uses `.claude/checkpoints.log`.

**Integration point**: `/implementing-plans` mandates `bookmarking-code create "phase-N-done"` after every verified phase.

### 5. /learning-from-sessions -- Knowledge Extraction

**Process (10-step gate function):**

1. **Session check**: Detect repo layout, find session via session-map.json worktree match. Fall back to `_current`. If post-session: read `claudeSessionIds` from meta.json.
2. **Detect**: Recognize extractable knowledge via signals (non-obvious debugging, misleading errors, workaround discovery, configuration insights, trial-and-error)
3. **Read errors**: If session active, read `errors.log` for error context
4. **Scan debug**: Check `.docs/debug/` for recent debug files
5. **Dedup**: Search `.docs/learnings/` and skill directories via ripgrep
6. **Analyze**: Run 4 identification questions + worth assessment (must pass 3 of 4 criteria: recurrence, non-triviality, transferability, time savings)
7. **Draft**: Structure via docs-writer with sections: Error Summary, Discoveries, Debug References, Deferred Actions
8. **Validate**: Run quality gates checklist (16 items)
9. **Confirm**: Present draft to user, wait for approval (Iron Law: never save without confirmation)
10. **Write**: docs-writer creates `.docs/learnings/MM-DD-YYYY-session-learnings.md`

**Post-Session Mode** (new in v2.1): When invoked with a session name after the session has ended, reads `claudeSessionIds` from meta.json, locates transcripts at `~/.claude/projects/{path-encoded-worktree}/{uuid}.jsonl`, and parses them for error/resolution pairs and debugging sequences.

**Deferred Actions routing**:
- Create skill -> when reusable across projects, multi-step solution
- Add to CLAUDE.md -> when project-specific preference/convention
- Update existing skill -> when new edge case for known pattern
- Not worth capturing -> simple typo, one-time issue, well-documented knowledge

**Error timing note**: Mid-session invocations only see real-time subagent errors (from track-errors hook). For complete error coverage, run at start of next session after harvest-errors has parsed the transcript.

## Hook System

### 1. detect-session.py (SessionStart) -- new in v2

**Trigger**: Claude Code session start (including after `/clear`)
**Process**: Read stdin JSON (session_id, cwd) -> normalize path -> detect repo layout -> read session-map.json -> find matching worktree entry -> if matched, persist Claude UUID to meta.json's `claudeSessionIds` array -> emit session context to stderr -> exit 2 (injects into conversation)
**Three output modes**:
- Active session matched: reports name, branch, status, worktree path
- Main worktree (no session): suggests `/starting-session`
- Regular repo (not migrated): suggests `/starting-session` to migrate

### 2. track-errors.py (PostToolUseFailure)

**Trigger**: Every tool failure in subagent contexts
**Process**: Import from `session_utils` -> resolve session via `resolve_session(cwd, session_id)` -> if no session, exit -> build JSON entry (timestamp, session_id, tool, input, error) -> append to `errors.log`
**Limitation**: Only fires in subagent contexts (Claude Code limitation). Main conversation errors are missed until harvest runs.

### 3. harvest-errors.py (Stop)

**Trigger**: Session end
**Process**: Import from `session_utils` -> resolve session -> stream JSONL transcript line-by-line (constant memory) -> index tool_use blocks -> match tool_result blocks -> detect errors (is_error flag OR non-zero Bash exit) -> deduplicate against existing errors.log -> backfill empty error fields -> write new entries using `atomic_write_json` for backfill operations
**Skips**: "Sibling tool call errored", "user doesn't want to proceed", "progress" entries, "file-history-snapshot"
**Always exits 0**: Never triggers conversation restart

### 4. trigger-learning.py (PreCompact)

**Trigger**: Before conversation compaction
**Process**: Import from `session_utils` -> resolve session -> if no session, exit -> read errors.log -> count entries -> if >0, print reminder to stderr -> exit 2 (sends message to Claude as feedback)
**Nudge message**: "SESSION LEARNING REMINDER: This session ({name}) has {count} error(s) logged..."

### Common Patterns Across Hooks

All 4 scripts share:
- **Import from session_utils**: No duplicated utility code across scripts
- **Worktree-aware session resolution**: `resolve_session()` matches by worktree path first, then session_id, then `_current` fallback
- **MINGW path normalization**: Via `normalize_path()` from session_utils
- **Fast exit on no session**: If no session name resolved, exit immediately (no tracking/nudging)

## Data Flow Diagram

```
[Claude Code starts in worktree]
    │
    ├─> SessionStart → detect-session.py
    │       Reads: session-map.json (worktree match)
    │       Persists: Claude UUID to meta.json claudeSessionIds[]
    │       Emits: session context to Claude conversation
    │
    ▼
/starting-session (from main/ worktree)
    │
    ├─> Creates: git branch + worktree (feature/, fix/, refactor/)
    ├─> Creates: {worktree}/.claude/sessions/{name}/meta.json
    ├─> Updates: container-level session-map.json (atomic write)
    ├─> Directs: user to cd to new worktree
    │
    ▼
Work Session (in session worktree)
    │
    ├─> Tool Failure → PostToolUseFailure → track-errors.py → errors.log (subagent only)
    ├─> /bookmarking-code create → checkpoints.log (worktree-scoped)
    │
    ▼
/ending-session (from main/ worktree)
    │
    ├─> Merge End: dry-run conflict check → squash merge → CLAUDE.md review →
    │       /committing-changes → remove worktree + branch → status: "ended"
    │
    ├─> Handoff End: create handoff doc via docs-writer → status: "handed-off"
    │       Keeps: branch + worktree open
    │
    ├─> Discard End: force remove worktree + branch → status: "ended"
    │
    ├─> Learning check: remind if errors.log has entries
    │
    ▼
Session End
    │
    ├─> Stop → harvest-errors.py → errors.log (full transcript parse, dedup + backfill)
    │
    ▼
[Claude Code restarts]
    │
    └─> /resuming-session (smart auto-detect)
            Mode A (Worktree): Reads session-map.json → meta.json → errors.log →
                    checkpoints.log → scans .docs/ → directs to worktree
            Mode B (Handoff): Reads handoff doc → verifies state → checks worktree →
                    presents takeover summary
            Mode C (Picker): Multiple candidates → unified selection
    │
    ▼
Conversation grows large
    │
    ├─> PreCompact → trigger-learning.py → nudge if errors exist
    │
    ▼
/learning-from-sessions
    │
    ├─> Reads: session-map.json (worktree match), errors.log, .docs/debug/
    ├─> Post-session: reads claudeSessionIds from meta.json, parses transcripts
    ├─> Dedup: .docs/learnings/, skill directories
    ├─> Creates: .docs/learnings/MM-DD-YYYY-session-learnings.md (via docs-writer agent)
    └─> Deferred Actions checklist for future implementation
```

## Interaction Patterns Between Skills

### Skill Pairs

| Producer | Consumer | Shared Artifact |
|----------|----------|----------------|
| `/starting-session` | All session-aware skills + hooks | `session-map.json` (container-level), `meta.json` (per-worktree) |
| `detect-session.py` | `/learning-from-sessions` (post-session mode) | `meta.json` `claudeSessionIds` array |
| `/bookmarking-code` | `/resuming-session`, `/ending-session` | `checkpoints.log` |
| `track-errors.py` + `harvest-errors.py` | `/resuming-session`, `/ending-session`, `/learning-from-sessions`, `trigger-learning.py` | `errors.log` |
| `/ending-session` (Handoff mode) | `/resuming-session` (Mode B) | `.docs/handoffs/MM-DD-YYYY-*.md` |
| `/learning-from-sessions` | Future sessions (manual) | `.docs/learnings/MM-DD-YYYY-*.md` |

### Smart Resume (unified in v2)

The two resume paths from v1 (`/resuming-sessions` and `/taking-over`) are now unified into `/resuming-session` with auto-detection:

| | Mode A (Worktree Resume) | Mode B (Handoff Resume) |
|---|---|---|
| **Input source** | Session state files (meta.json, errors.log, checkpoints.log) | Handoff document (.docs/handoffs/) |
| **Best for** | Same person restarting Claude Code in a worktree | Different person or different context picking up work |
| **Context type** | Reconstructed from structured data | Narrated by previous session (richer context) |
| **Worktree** | Directs user to existing worktree | Checks if worktree exists, offers `/starting-session` if not |
| **State verification** | Branch mismatch check | Full git status/log verification + drift detection |

### Staleness Auto-Update Pattern

Skills that read `.docs/` documents implement a staleness check:

- `/resuming-session`: Checks related handoffs and learnings
- `/planning-code`, `/designing-code`: Check referenced plans/research (upstream skills, not session-specific)

Pattern: Read `git_commit` from frontmatter -> count commits behind HEAD -> if >3 -> spawn `docs-updater` agent -> re-read updated version (or note if archived)

## Shared Agent Dependencies

| Agent | Used By | Purpose |
|-------|---------|---------|
| `docs-writer` (commandbase-core) | `/ending-session` (Handoff mode), `/learning-from-sessions` | Creates .docs/ files with standardized frontmatter |
| `docs-updater` (commandbase-core) | `/resuming-session` | Refreshes or archives stale .docs/ files |

## Iron Laws Summary

Each session skill enforces a non-negotiable rule:

| Skill | Iron Law |
|-------|----------|
| `/starting-session` | No session without user confirmation of name and branch type |
| `/ending-session` | No session end without merge verification or explicit discard |
| `/resuming-session` | No resume without reading source files |
| `/bookmarking-code` | No checkpoint without git state verification |
| `/learning-from-sessions` | No learnings document without verified discoveries and user approval |

## Open Questions

- The track-errors hook only fires in subagent contexts, meaning main conversation errors are invisible until session end when harvest-errors runs
- `/ending-session` requires the user to `cd` to main worktree before running -- this is a workaround for the cwd-lock issue when removing the directory you are standing in
- Post-session transcript parsing in `/learning-from-sessions` is instruction-only; the actual parsing engine has not been built yet
- Hook installation requires manual `~/.claude/settings.json` edits pointing to plugin paths -- no automated plugin install mechanism for hooks yet
- SessionStart hook fires on every session start including after `/clear`, which means `claudeSessionIds` grows over the session lifetime
