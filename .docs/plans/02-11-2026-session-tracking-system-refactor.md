---
date: 2026-02-11
status: complete
topic: "Session Tracking System Refactor - Separate Worktree, Session, and Handoff Layers"
tags: [plan, implementation, session, refactor, worktree, handoff, hooks, skills]
git_commit: 09a3c1f
references:
  - plugins/commandbase-session/skills/starting-session/SKILL.md
  - plugins/commandbase-session/skills/ending-session/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-session/scripts/session_utils.py
  - plugins/commandbase-session/scripts/detect-session.py
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
  - plugins/commandbase-code/skills/starting-refactors/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - .docs/research/02-11-2026-session-tracking-system-architecture-workflow-opportunities.md
  - .docs/research/02-11-2026-old-handing-over-skill-pre-v2.md
  - .docs/research/02-11-2026-old-taking-over-skill-pre-v2.md
---

# Session Tracking System Refactor — Implementation Plan

## Overview

Refactor the session tracking system to separate three conflated concepts — worktree (git isolation), session (conversation tracking), and handoff (knowledge transfer) — into independent layers. This enables many-to-one sessions per worktree, standalone handoff skills, and a session close-out flow that feeds directly into `/learning-from-sessions`.

## Current State Analysis

The v2 session system merged three distinct concepts into a single lifecycle:
- `/starting-session` creates branches, worktrees, AND tracking state (conflated)
- `/ending-session` merges OR hands off OR discards (conflated)
- `/resuming-session` resumes worktrees OR absorbs handoffs (conflated)
- One worktree = one session (1:1 assumption, incorrect)

### Key Discoveries:
- `resolve_session()` at `session_utils.py:167-214` has a legacy `_current` fallback (Tier 3, lines 191-214) that should be removed
- `summary` field in meta.json is read by `/resuming-session` but never written by any skill or hook
- `/starting-session` creates `claudeSessionIds: []` at SKILL.md:204 without capturing the current UUID
- Three skills reference deprecated `_current`: `bookmarking-code/SKILL.md:35`, `starting-refactors/SKILL.md:76`, `implementing-plans/SKILL.md:171`
- `/learning-from-sessions` also references `_current` at SKILL.md:57 and SKILL.md:157
- Old `/handing-over` and `/taking-over` skills (preserved in `.docs/research/`) were clean standalone tools with optional session awareness
- Session state lives in `.claude/sessions/{name}/` (gitignored); close-out summaries will go to `.docs/sessions/{name}/summary.json` (committed)

## Desired End State

```
/starting-worktree    — git isolation (branch + directory), run from main or container
/starting-session     — discovery + tracking setup, run from any worktree (or regular repo)
                        asks what the session is about, captures UUID, writes summary
[work happens, hooks track via session ID]
/handing-over         — standalone handoff doc, stamps session UUID(s)
/taking-over          — standalone handoff absorption, captures new UUID
/ending-session       — closes tracking, produces summary.json for /learning-from-sessions
/ending-worktree      — merge/cleanup of worktree (git plumbing only)
/resuming-session     — worktree resume only (read state, verify, present context)
```

One worktree can have multiple sessions. session-map.json maps session IDs to worktrees (many-to-one). Only one session active per worktree at a time.

Hybrid storage:
- `.claude/sessions/{name}/` — live tracking (meta.json, errors.log, checkpoints.log) — gitignored
- `.docs/sessions/{name}/summary.json` — close-out artifact — committed, permanent

### Verification:
- All `_current` references removed from codebase (grep returns 0 matches)
- `/starting-worktree` creates worktree without session tracking
- `/starting-session` works in worktree OR regular repo (with warning if no worktree)
- `/handing-over` and `/taking-over` work standalone (with or without active session)
- `/ending-session` produces `summary.json` without touching worktree
- `/ending-worktree` checks all sessions ended before removing worktree
- session-map.json supports multiple sessions per worktree
- SessionStart hook resolves the correct active session when multiple exist

## What We're NOT Doing

- No changes to error tracking hooks (track-errors.py, harvest-errors.py) — they work correctly
- No changes to PreCompact/trigger-learning.py — works correctly
- No changes to `/bookmarking-code` beyond removing `_current` reference
- No cross-session learning aggregation (lower priority, future work)
- No session-aware `/creating-prs` (lower priority)
- No checkpoints.log format migration to JSONL (lower priority)
- No session duration tracking beyond created/ended timestamps in summary.json

## Implementation Approach

Incremental phases that maintain backward compatibility at each step. Foundation fixes first (remove tech debt), then structural splits (new skills), then schema changes (session-map many-to-one). Each phase is independently committable and testable.

---

## Phase 1: Foundation Fixes

### Overview
Remove legacy `_current` references, add `summary` field writing, and capture initial UUID in `/starting-session`. These are low-risk fixes that clean up tech debt before structural changes.

### Changes Required:

#### 1. Remove `_current` fallback from session_utils.py
**File**: `plugins/commandbase-session/scripts/session_utils.py`
**Changes**: Delete the entire Tier 3 fallback block (lines 191-214) from `resolve_session()`. The function should return `""` after Tier 2 (session_id key lookup) fails instead of falling through to `_current`.

Before:
```python
# 3. Legacy _current fallback
layout = detect_repo_layout(cwd)
if layout == "regular":
    sessions_dir = os.path.join(cwd, ".claude", "sessions")
else:
    ...
```

After:
```python
return ""
```

Also update the docstring (lines 168-175) to remove mention of `_current` from the resolution order.

#### 2. Update bookmarking-code session detection
**File**: `plugins/commandbase-core/skills/bookmarking-code/SKILL.md`
**Changes**:
- Line 35: Remove `3. Fallback: check .claude/sessions/_current for legacy sessions.` — renumber step 4 to step 3.
- Line 49 (Gate Function): Remove `Fall back to _current.` from the SESSION step.

#### 3. Update starting-refactors session check
**File**: `plugins/commandbase-code/skills/starting-refactors/SKILL.md`
**Changes**:
- Line 76: Replace `Check session awareness: read .claude/sessions/_current if exists` with `Check session awareness: detect repo layout, find session for current worktree via session-map.json`

#### 4. Update implementing-plans checkpoint integration
**File**: `plugins/commandbase-code/skills/implementing-plans/SKILL.md`
**Changes**:
- Lines 171-173: Replace the `_current` check with worktree-based detection:
  ```
  1. Detect repo layout and find active session via session-map.json (worktree match)
  2. If session exists: `/bookmarking-code create "phase-N-done"` (writes to session folder)
  3. If no session: `/bookmarking-code create "phase-N-done"` (writes to global log)
  ```

#### 5. Update learning-from-sessions session detection
**File**: `plugins/commandbase-session/skills/learning-from-sessions/SKILL.md`
**Changes**:
- Line 57: Remove `5. Fallback: check .claude/sessions/_current for legacy sessions.` — renumber step 6 to step 5.
- Line 31 (Gate Function): Remove `Fall back to _current.`
- Line 157: Replace `_current fallback` mention with `session-map.json worktree match`

#### 6. Add summary field to /starting-session
**File**: `plugins/commandbase-session/skills/starting-session/SKILL.md`
**Changes**:
- In Step 6 (Write meta.json, line 197-211): Add `"summary": ""` to the initial meta.json schema. Add a note: "The summary field is populated after session creation via the discovery process (see Phase 3 expansion)."
- For now, write an empty string. Phase 3 will add the discovery flow that populates it.

#### 7. Capture initial UUID in /starting-session
**File**: `plugins/commandbase-session/skills/starting-session/SKILL.md`
**Changes**:
- After Step 7 (Update session-map.json), add a new step:
  ```
  ### Step 8: Capture initial UUID

  The SessionStart hook injects session context including the current conversation's session ID.
  If the session ID is available from conversation context, write it into meta.json:

  Read the session ID from the SessionStart hook output injected at conversation start.
  Call update_meta_json() or manually append the UUID to claudeSessionIds.

  This ensures the conversation that created the session is recorded in the UUID list,
  rather than waiting for the next SessionStart hook fire.
  ```
- Renumber current Step 8 (Output) to Step 9.

### Success Criteria:
- [x] `grep -r "_current" plugins/` returns 0 matches (excluding archived/research docs)
- [x] `resolve_session()` in session_utils.py has no `_current` fallback code
- [x] `/starting-session` meta.json template includes `summary` field
- [x] `/starting-session` includes UUID capture step

---

## Phase 2: Extract /starting-worktree

### Overview
Split worktree creation (git plumbing) out of `/starting-session` into a new `/starting-worktree` skill. This skill handles bare-repo migration (Mode A) and worktree creation (Mode B) — everything that is git isolation, nothing that is session tracking.

### Changes Required:

#### 1. Create /starting-worktree skill
**File**: `plugins/commandbase-session/skills/starting-worktree/SKILL.md` (new file)
**Changes**: New skill containing:
- **Mode A (Migration)**: Transplant directly from current `/starting-session` Mode A (lines 62-141). Identical migration flow.
- **Mode B (Create Worktree)**: Transplant from current `/starting-session` Mode B Steps 1-4 only (lines 143-185):
  - Step 1: Verify we're in main worktree
  - Step 2: Choose branch type (feature/fix/refactor)
  - Step 3: Name validation (kebab-case)
  - Step 4: Create branch + worktree via `git worktree add`
- **Does NOT**: Create session state directory, write meta.json, update session-map.json, or capture UUIDs
- **Output**: Reports worktree path and suggests running `/starting-session` in the new worktree
- **Iron Law**: `NO WORKTREE WITHOUT USER CONFIRMATION OF NAME AND BRANCH TYPE` (same as current)
- **Gate Function**: Detect layout → Check if in main → Ask type → Ask name → Validate → Create

#### 2. Strip worktree creation from /starting-session
**File**: `plugins/commandbase-session/skills/starting-session/SKILL.md`
**Changes**:
- Remove Mode A (migration) entirely — now lives in `/starting-worktree`
- Remove Mode B Steps 1-4 (branch type, name, worktree creation) — now lives in `/starting-worktree`
- Keep Mode B Steps 5-9 (session state dir, meta.json, session-map, UUID capture, output) — these become the core of the expanded `/starting-session` in Phase 3
- Add worktree detection: if not in a worktree (bare-worktree layout) and not in main, warn and suggest `/starting-worktree` first. If in a regular repo, proceed with warning.
- Update description to reflect session-tracking-only purpose

### Success Criteria:
- [x] `/starting-worktree` skill file exists with migration and worktree creation logic
- [x] `/starting-session` no longer contains git worktree creation commands
- [x] `/starting-worktree` output suggests running `/starting-session` next
- [x] Mode A migration is fully preserved in `/starting-worktree`

---

## Phase 3: Expand /starting-session with Discovery

### Overview
Transform `/starting-session` from a state-file creator into a session onboarding experience. Borrow the discovery pattern from `/starting-projects`: ask what the session is about, gather relevant context, establish purpose. The session's `summary` field becomes meaningful because the user is prompted for it.

### Changes Required:

#### 1. Rewrite /starting-session skill
**File**: `plugins/commandbase-session/skills/starting-session/SKILL.md`
**Changes**: Complete rewrite with the following flow:

**New Iron Law**: `NO SESSION WITHOUT PURPOSE`

**New Gate Function**:
```
1. DETECT: Am I in a worktree? If not, warn (but allow proceeding in regular repo)
2. CHECK: Is there already an active session in this worktree? If yes, warn.
3. DISCOVER: Ask what this session is about (purpose, scope, target area)
4. CONTEXT: Read relevant plans/research/handoffs mentioned by user
5. ESTABLISH: Write meta.json with summary, capture UUID
6. REGISTER: Update session-map.json
7. OUTPUT: Present session brief
```

**Discovery Step (borrowed from /starting-projects)**:
Use AskUserQuestion to gather:
- What are you working on? (brief purpose — becomes `summary` field)
- Related docs? (plans, research, handoffs to read for context)
- Session name suggestion based on purpose

**Session Name**: Auto-suggest from purpose description. Same kebab-case validation as before (3-40 chars, `^[a-z0-9][a-z0-9-]*[a-z0-9]$`).

**Worktree Warning**: If not in a bare-worktree layout:
```
You're not in a worktree. Sessions work without worktrees, but you won't
get git isolation. Run /starting-worktree first for isolated branches.

Continue without worktree? (Y/n)
```

**Active Session Check**: Read session-map.json for entries matching this worktree with `status: "active"`. If found:
```
There's already an active session in this worktree: {name}
End it with /ending-session first, or continue working in that session.
```

**Output**:
```
SESSION STARTED
===============
Name: {session-name}
Purpose: {summary}
Worktree: {worktree_path} (or "regular repo" if no worktree)

Context loaded:
- {plan/research/handoff if any were read}

Ready to work. Hooks are tracking errors and conversation UUIDs.
```

#### 2. Update meta.json schema
**File**: `plugins/commandbase-session/skills/starting-session/SKILL.md`
**Changes**: The meta.json written during session creation now includes:
```json
{
  "sessionId": "<session-name>",
  "claudeSessionIds": ["<initial-uuid>"],
  "name": "<session-name>",
  "branch": "<current-branch>",
  "worktree": "<worktree-path-or-cwd>",
  "created": "<ISO 8601>",
  "gitBranch": "<current-branch>",
  "summary": "<user-provided purpose>"
}
```

Key changes from current:
- `claudeSessionIds` starts with the current UUID (not empty)
- `summary` is populated from user's purpose description
- `branch` reflects the current branch (not necessarily a session-created branch)

### Success Criteria:
- [x] `/starting-session` uses AskUserQuestion for discovery
- [x] `summary` field is populated in meta.json from user input
- [x] `claudeSessionIds` contains initial UUID at creation time
- [x] Active session check prevents duplicate active sessions in same worktree
- [x] Worktree warning displayed when running in regular repo (but proceeds if user confirms)

---

## Phase 4: Restore /handing-over and /taking-over

### Overview
Bring back `/handing-over` and `/taking-over` as standalone v3 skills. Based on the preserved pre-v2 versions (in `.docs/research/`), updated with session-map awareness and UUID stamping. These are independent knowledge transfer tools that optionally read session context when available.

### Changes Required:

#### 1. Create /handing-over skill
**File**: `plugins/commandbase-session/skills/handing-over/SKILL.md` (new file)
**Changes**: Based on preserved old skill at `.docs/research/02-11-2026-old-handing-over-skill-pre-v2.md`, with these v3 updates:

- **Session Awareness**: Replace `_current` check (old line 69) with worktree-based detection:
  ```
  1. Detect repo layout
  2. If bare-worktree: read session-map.json, find active session matching cwd
  3. If session found: read meta.json for session name, summary, claudeSessionIds
  4. If no session: proceed without session context (default behavior)
  ```
- **UUID Stamping**: When session is active, stamp current conversation UUID(s) into the handoff document's Session Context section. This creates traceability: which conversation produced this handoff.
- **Session Context section** (old lines 146-153): Update to read from meta.json via session-map.json resolution instead of `_current`. Include `summary` from meta.json.
- **Learning Check** (old lines 189-195): Update session detection to use session-map.json.
- **Iron Law, Gate Function, Process, Red Flags, Rationalization Prevention**: Preserve from old skill — they were clean.
- **Description**: Update to remove "ending a session" from trigger phrases (that's `/ending-session`'s job now).

#### 2. Create /taking-over skill
**File**: `plugins/commandbase-session/skills/taking-over/SKILL.md` (new file)
**Changes**: Based on preserved old skill at `.docs/research/02-11-2026-old-taking-over-skill-pre-v2.md`, with these v3 updates:

- **Staleness auto-update**: Preserve from old skill (lines 67-82) — works correctly.
- **Session Context**: After absorbing the handoff, check if the handoff references a session. If in the same worktree and session is active, associate this conversation's UUID with that session.
- **New Session Option**: After presenting the takeover summary, offer:
  ```
  Would you like to start a new session for this work?
  1. Yes - run /starting-session to create a tracking session
  2. No - continue without session tracking
  ```
- **Iron Law, Gate Function, Process, Red Flags, Rationalization Prevention**: Preserve from old skill — they were clean.

### Success Criteria:
- [x] `/handing-over` skill exists and creates handoff docs without requiring `/ending-session`
- [x] `/taking-over` skill exists and absorbs handoffs without requiring `/resuming-session`
- [x] Both skills detect sessions via session-map.json (no `_current` references)
- [x] `/handing-over` stamps UUID(s) into handoff document when session is active
- [x] `/taking-over` offers `/starting-session` for new tracking after absorption

---

## Phase 5: Redesign /ending-session + Extract /ending-worktree

### Overview
Transform `/ending-session` from a conflated merge/handoff/discard tool into a session close-out that produces a comprehensive summary file. Extract worktree teardown into a new `/ending-worktree` skill.

### Changes Required:

#### 1. Rewrite /ending-session as session close-out
**File**: `plugins/commandbase-session/skills/ending-session/SKILL.md`
**Changes**: Complete rewrite. The skill now closes a session tracking unit and produces a summary file.

**New Iron Law**: `NO SESSION END WITHOUT SUMMARY`

**New Gate Function**:
```
1. DETECT: Find active session in current worktree via session-map.json
2. GATHER: Read meta.json, errors.log, checkpoints.log
3. SCAN: Find handoff docs created during this session (in .docs/handoffs/)
4. COMPOSE: Build summary.json with all session data
5. WRITE: Save to .docs/sessions/{name}/summary.json
6. UPDATE: Mark session as "ended" in session-map.json
7. SUGGEST: Recommend /learning-from-sessions if errors exist
```

**Summary File Schema** (`.docs/sessions/{name}/summary.json`):
```json
{
  "name": "<session-name>",
  "summary": "<purpose from meta.json>",
  "branch": "<branch>",
  "worktree": "<worktree-path>",
  "created": "<ISO 8601 from meta.json>",
  "ended": "<ISO 8601 now>",
  "claudeSessionIds": ["<uuid-1>", "<uuid-2>", ...],
  "handoffs": [
    ".docs/handoffs/02-11-2026-session-name-description.md"
  ],
  "errors": {
    "count": 5,
    "summary": [
      {"tool": "Bash", "input": "npm test", "error": "exit code 1", "source": "harvest"}
    ]
  },
  "checkpoints": [
    {"name": "pre-refactor-auth", "timestamp": "2026-02-11T10:00:00Z", "sha": "abc123"}
  ]
}
```

**Handoff Discovery**: Scan `.docs/handoffs/` for files whose topic or tags reference the session name, or whose date falls within the session's created-to-now window.

**Output**:
```
SESSION ENDED
=============
Name: {session-name}
Duration: {created} → {now}
Conversations: {count} Claude sessions
Handoffs: {count} created during session
Errors: {count} logged
Checkpoints: {count} created

Summary saved: .docs/sessions/{name}/summary.json

{if errors > 0:}
This session had errors. Run /learning-from-sessions to extract learnings:
/learning-from-sessions {session-name}

The worktree is still active. Use /ending-worktree when ready to merge or discard.
```

**Key Difference from v2**: Does NOT merge, does NOT remove worktree, does NOT create handoff docs. Pure tracking close-out.

#### 2. Create /ending-worktree skill
**File**: `plugins/commandbase-session/skills/ending-worktree/SKILL.md` (new file)
**Changes**: New skill containing worktree teardown (git plumbing only). Two modes:

**Mode A: Merge**
- Transplant from current `/ending-session` Mode A (lines 100-218):
  - Conflict detection dry run
  - Squash merge to main
  - CLAUDE.md review
  - Commit via `/committing-changes`
  - Remove worktree + branch
- **Pre-check**: Verify all sessions in this worktree are ended (scan session-map.json for entries matching this worktree with `status: "active"` or `"handed-off"`). If any active/handed-off sessions exist:
  ```
  This worktree has active/handed-off sessions:
  - {session-name} (status: active)

  End them with /ending-session first, or force removal with option 3.
  ```

**Mode B: Discard**
- Transplant from current `/ending-session` Mode C (lines 249-278):
  - Confirmation with name typing
  - Force remove worktree + branch
  - Same pre-check for active sessions (warn but allow with explicit force)

**Iron Law**: `NO WORKTREE REMOVAL WITHOUT MERGE VERIFICATION OR EXPLICIT DISCARD`

**Must run from main worktree** (same restriction as current /ending-session).

#### 3. Create .docs/sessions/ directory support
**File**: `plugins/commandbase-session/scripts/session_utils.py`
**Changes**: Add helper function:
```python
def get_session_summary_path(cwd, session_name):
    """Return .docs/sessions/{session_name}/summary.json path.
    Creates the directory if needed.
    """
    layout = detect_repo_layout(cwd)
    if layout == "bare-worktree":
        toplevel = ...  # git rev-parse --show-toplevel
        base = normalize_path(toplevel)
    else:
        base = cwd
    summary_dir = os.path.join(base, ".docs", "sessions", session_name)
    os.makedirs(summary_dir, exist_ok=True)
    return os.path.join(summary_dir, "summary.json")
```

### Success Criteria:
- [x] `/ending-session` produces `.docs/sessions/{name}/summary.json` with full session data
- [x] `/ending-session` does NOT merge, remove worktree, or create handoff docs
- [x] `/ending-worktree` handles merge and discard modes
- [x] `/ending-worktree` checks for active sessions before removal
- [x] `session_utils.py` has `get_session_summary_path()` helper
- [x] summary.json contains all claudeSessionIds, handoffs, errors, and checkpoints

---

## Phase 6: Update Session-Map Schema + SessionStart Hook

### Overview
Update session-map.json to support many-to-one sessions per worktree. Update the SessionStart hook to detect which session is active when multiple exist for the same worktree.

### Changes Required:

#### 1. Update session-map.json schema
**Changes**: The schema stays flat (keyed by session name) but now multiple entries can share the same `worktree` value. No structural change needed — the current schema already supports this. The behavioral change is in how consumers interpret it:

- Multiple entries can have the same `worktree`
- Only ONE entry per worktree should have `status: "active"` at a time
- `/starting-session` enforces this (active session check from Phase 3)

#### 2. Update SessionStart hook for multi-session resolution
**File**: `plugins/commandbase-session/scripts/detect-session.py`
**Changes**: Update the worktree matching logic (lines 48-53) to handle multiple sessions per worktree:

```python
# Find ACTIVE session matching this worktree (not ended/handed-off)
matched_entry = None
for _sid, entry in session_map.items():
    wt = entry.get("worktree", "")
    if wt and os.path.normpath(normalize_path(wt)) == cwd_norm:
        if entry.get("status") == "active":
            matched_entry = entry
            break
```

Key change: Filter by `status == "active"` when matching worktree. If no active session but handed-off/ended sessions exist, report the worktree state without injecting session tracking context.

**Also add**: When matched, include session summary in the injected context:
```python
summary = matched_entry.get("summary", "")
summary_line = f"\nPurpose: {summary}" if summary else ""
print(
    f'SESSION DETECTED: "{name}" on branch {branch} (status: {status}).{summary_line}\n'
    f"Worktree: {worktree}\n"
    f"Session ID: {session_id}",
)
```

#### 3. Update update_session_map() for validation
**File**: `plugins/commandbase-session/scripts/session_utils.py`
**Changes**: Add an optional validation function:
```python
def get_active_session_for_worktree(cwd):
    """Find the active session for the current worktree, if any.
    Returns (session_name, entry) or (None, None).
    """
    session_map = read_session_map(cwd)
    cwd_norm = os.path.normpath(cwd)
    for sid, entry in session_map.items():
        wt = entry.get("worktree", "")
        if wt and os.path.normpath(normalize_path(wt)) == cwd_norm:
            if entry.get("status") == "active":
                return entry.get("name"), entry
    return None, None
```

This function is used by `/starting-session` (Phase 3 active session check) and `/ending-worktree` (Phase 5 pre-check).

### Success Criteria:
- [x] SessionStart hook only matches `status: "active"` sessions for a worktree
- [x] SessionStart hook includes session summary in injected context
- [x] `get_active_session_for_worktree()` utility function exists in session_utils.py
- [x] Multiple ended sessions + one active session on same worktree resolves correctly

---

## Phase 7: Simplify /resuming-session

### Overview
Remove Mode B (handoff resume) and Mode C (session picker with mixed types) from `/resuming-session`. Handoff absorption now lives in `/taking-over`. The skill becomes pure worktree session resume.

### Changes Required:

#### 1. Rewrite /resuming-session
**File**: `plugins/commandbase-session/skills/resuming-session/SKILL.md`
**Changes**: Simplify to worktree resume only:

**New Gate Function**:
```
1. DETECT: Find session(s) for current worktree in session-map.json
2. SELECT: If multiple sessions exist for this worktree, present picker (active sessions only, or show history)
3. READ: Load session state files (meta.json, errors.log, checkpoints.log)
4. VERIFY: Does git state match expectations?
5. PRESENT: Show context summary including session purpose (summary field)
6. ONLY THEN: User begins work
```

**Remove entirely**:
- Mode B (Handoff Resume) — now lives in `/taking-over`
- Mode C (Session Picker) as currently designed — replace with worktree-scoped session history
- All staleness detection logic for handoff documents (that's `/taking-over`'s job)
- References to scanning `.docs/handoffs/` for handoff documents to absorb

**New session picker** (replaces Mode C): When multiple sessions exist for the current worktree, show session history:
```
Sessions in this worktree:

  #  Status   Name              Created              Summary
  1  [active] auth-refactor     2026-02-11 10:00     Refactoring auth middleware
  2  [ended]  initial-setup     2026-02-10 14:00     Initial project scaffolding

Which session to resume? (Only active sessions can be resumed)
```

**If no active session**: Suggest `/starting-session` or `/taking-over` depending on context:
```
No active session in this worktree.

Options:
1. /starting-session - Start a new session
2. /taking-over - Pick up from a handoff document
```

**Keep**: Staleness detection for `.docs/` documents referenced by the session (plans, research). Session state file reading. Git state verification. Summary presentation.

**Update description**: Remove handoff/takeover trigger phrases.

### Success Criteria:
- [x] `/resuming-session` no longer scans `.docs/handoffs/` or absorbs handoff documents
- [x] Mode B and Mode C (as currently designed) are removed
- [x] Session picker shows worktree-scoped session history
- [x] Session summary (purpose) is displayed in the resume output
- [x] Suggests `/taking-over` when no active session exists

---

## Phase 8: Plugin Manifest + Documentation

### Overview
Register new skills in the plugin manifest, update the README, and refresh session lifecycle documentation.

### Changes Required:

#### 1. Update plugin.json
**File**: `plugins/commandbase-session/.claude-plugin/plugin.json`
**Changes**: Add new skills to the manifest:
- `starting-worktree`
- `handing-over`
- `taking-over`
- `ending-worktree`

#### 2. Update plugin README
**File**: `plugins/commandbase-session/README.md`
**Changes**: Update skill list, add new conceptual model diagram, document the three-layer architecture (worktree / session / handoff).

#### 3. Update session lifecycle docs
**File**: `docs/session-lifecycle.md`
**Changes**: Rewrite to reflect the new separated lifecycle:
- Worktree lifecycle: /starting-worktree → work → /ending-worktree
- Session lifecycle: /starting-session → work → /ending-session
- Handoff lifecycle: /handing-over → /taking-over (independent)

#### 4. Update CLAUDE.md
**File**: `CLAUDE.md`
**Changes**: Update the commandbase-session skill count and add the new skills to any skill listings.

#### 5. Add .docs/sessions/ to .gitignore exception
**File**: `.gitignore`
**Changes**: Ensure `.docs/sessions/` is NOT gitignored (it should be committed). Verify `.claude/sessions/` IS gitignored (live tracking data).

### Success Criteria:
- [x] plugin.json lists all 8 skills (4 original + 4 new)
- [x] README documents the three-layer architecture
- [x] Session lifecycle docs reflect the new separated flow
- [x] `.docs/sessions/` is committed (not gitignored)
- [x] `.claude/sessions/` remains gitignored

---

## Testing Strategy

### Manual Verification per Phase:
Each phase has explicit success criteria that can be verified with grep, file existence checks, and functional walkthroughs.

### End-to-End Scenario:
After all phases, verify the full lifecycle:
1. `/starting-worktree` creates a new worktree
2. `cd` to worktree, `/starting-session` runs discovery, creates tracking
3. Work happens, hooks track UUIDs and errors
4. `/handing-over` creates standalone handoff doc with UUID stamps
5. New conversation: `/taking-over` absorbs handoff, optionally starts new session
6. `/ending-session` produces summary.json
7. `/learning-from-sessions` reads summary.json for learning extraction
8. `/ending-worktree` merges to main and cleans up

### Regression Checks:
- SessionStart hook still fires and injects context
- Error tracking hooks still write to errors.log
- `/bookmarking-code` still creates session-scoped checkpoints
- `/committing-changes` still works in squash merge context

## Migration Notes

- No data migration needed — session-map.json schema is backward compatible
- Existing active sessions continue working (single session per worktree is a valid case of many-to-one)
- Old `_current` files in `.docs/archive/sessions-v1/` are untouched (already archived)
- Skills removed from `/ending-session` (handoff mode) are now standalone skills — no functionality lost

## References

- Research: `.docs/research/02-11-2026-session-tracking-system-architecture-workflow-opportunities.md`
- Old /handing-over: `.docs/research/02-11-2026-old-handing-over-skill-pre-v2.md`
- Old /taking-over: `.docs/research/02-11-2026-old-taking-over-skill-pre-v2.md`
- Handoff: `.docs/handoffs/02-11-2026-session-finetuning-session-tracking-refactor-research-and-direction.md`
