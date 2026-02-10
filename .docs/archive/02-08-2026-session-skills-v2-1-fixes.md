---
date: 2026-02-08
status: completed
topic: "Session Skills v2.1 Fixes"
tags: [plan, implementation, session-skills, bare-repo, worktrees, hooks, v2.1]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived after full implementation in commit aefcf6f. All 8 phases (0-7) completed, all 11 deferred actions addressed."
archived: 2026-02-09
archive_reason: "Plan fully implemented in commit aefcf6f. All phases complete, all referenced code changes landed."
references:
  - .docs/research/02-08-2026-session-v2-1-deferred-actions-research.md
  - .docs/learnings/02-08-2026-end-to-end-test-session-learnings.md
  - plugins/commandbase-session/skills/ending-session/SKILL.md
  - plugins/commandbase-session/skills/starting-session/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - plugins/commandbase-session/scripts/detect-session.py
  - plugins/commandbase-session/scripts/session_utils.py
  - plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py
---

# Session Skills v2.1 Fixes

**Date**: 2026-02-08
**Branch**: master
**Research**: `.docs/research/02-08-2026-session-v2-1-deferred-actions-research.md`
**Learnings**: `.docs/learnings/02-08-2026-end-to-end-test-session-learnings.md`

## Overview

Fix all 11 deferred actions from the end-to-end test session. Covers bare repo git command fixes, worktree cleanup redesign, Claude UUID tracking, hook installation, nudge hook suppression, and post-session learning extraction. 7 phases, dependency-ordered.

## Design Decisions

1. **`/ending-session` runs from main worktree** — User must `cd` to main before ending. If run from inside the session worktree, skill detects this and reminds user to switch. Avoids the cwd-lock issue entirely.
2. **Comment marker for nudge suppression** — `/committing-changes` appends `# via-committing-changes` to git commit/push commands. Nudge hook checks for this marker and suppresses. Simplest approach, no file I/O.
3. **Hooks point to plugin scripts directly** — `~/.claude/settings.json` hooks reference plugin paths (e.g., `/c/code/commandbase/main/plugins/.../scripts/`). No more manual copies in `~/.claude/hooks/`. Scripts use shared `session_utils.py`.
4. **`claudeSessionIds` array in meta.json** — Replaces single `sessionId`. SessionStart hook appends UUID on each fire (including after `/clear`).

## What We're NOT Doing

- Not building the full post-session transcript parsing engine yet (Phase 7 updates the skill instructions only, actual parsing is future work)
- Not migrating existing sessions to new meta.json schema (backward compat via `sessionId` field preserved)
- Not building a plugin install mechanism for hooks (manual settings.json edit for now)
- Not changing the squash merge flow in ending-session (only cleanup step changes)

## Implementation Phases

### Phase 0: Install hooks from plugin paths
**Goal**: Point all hooks at plugin scripts. Remove manual copies.

**Files to modify:**
- `~/.claude/settings.json` (lines 23-67, hooks section)

**Files to delete:**
- `~/.claude/hooks/nudge-commit-skill.py`
- `~/.claude/hooks/track-errors.py`
- `~/.claude/hooks/trigger-learning.py`
- `~/.claude/hooks/harvest-errors.py`

**Steps:**
1. Replace all 4 existing hook commands to point at plugin script paths:
   - PostToolUse: `bash -c 'python3 /c/code/commandbase/main/plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py'`
   - PostToolUseFailure: `bash -c 'python3 /c/code/commandbase/main/plugins/commandbase-session/scripts/track-errors.py'`
   - PreCompact: `bash -c 'python3 /c/code/commandbase/main/plugins/commandbase-session/scripts/trigger-learning.py'`
   - Stop: `bash -c 'python3 /c/code/commandbase/main/plugins/commandbase-session/scripts/harvest-errors.py'`
2. Add the missing SessionStart hook:
   ```json
   "SessionStart": [{
     "matcher": "",
     "hooks": [{
       "type": "command",
       "command": "bash -c 'python3 /c/code/commandbase/main/plugins/commandbase-session/scripts/detect-session.py'"
     }]
   }]
   ```
3. Delete the 4 manual hook scripts from `~/.claude/hooks/`
4. Copy `session_utils.py` to `~/.claude/hooks/` as a fallback import (or ensure plugin scripts can find it via relative import)

**Success criteria:**
- [ ] All 5 hooks fire correctly (test by starting a new Claude Code session)
- [ ] SessionStart hook outputs session detection message
- [ ] No import errors from plugin scripts referencing `session_utils`
- [ ] `~/.claude/hooks/` no longer contains the 4 old script copies

### Phase 1: Fix ending-session bare repo commands
**Goal**: All git commands in ending-session use `git -C "$bare"` with absolute paths.

**File to modify:** `plugins/commandbase-session/skills/ending-session/SKILL.md`

**Changes:**

1. **Add bare path detection** after line 53 (Session Verification):
   ```bash
   bare="$container/.bare"
   ```

2. **Fix Merge Mode cleanup** (lines 165-171):
   Replace:
   ```bash
   cd {container}
   git worktree remove {type}/{session-name}
   git branch -d {type}/{session-name}
   ```
   With:
   ```bash
   git -C "$bare" worktree remove "$container/{type}/{session-name}"
   git -C "$bare" branch -d {type}/{session-name}
   ```
   Add explanation: **Why `-C "$bare"`**: The container directory is not a git repo — `.bare/` is.

3. **Fix Discard Mode cleanup** (lines 232-236):
   Replace:
   ```bash
   cd {container}
   git worktree remove --force {type}/{session-name}
   git branch -D {type}/{session-name}
   ```
   With:
   ```bash
   git -C "$bare" worktree remove --force "$container/{type}/{session-name}"
   git -C "$bare" branch -D {type}/{session-name}
   ```

**Success criteria:**
- [ ] No `cd {container}` before git commands in cleanup sections
- [ ] All 6 git command locations use `git -C "$bare"` pattern
- [ ] `bare="$container/.bare"` defined in Session Verification section

### Phase 2: Add worktree cleanup handling to ending-session
**Goal**: ending-session detects when run from session worktree and handles cleanup gracefully.

**File to modify:** `plugins/commandbase-session/skills/ending-session/SKILL.md`

**Changes:**

1. **Add cwd detection** to Session Verification (after line 56):
   ```bash
   current_worktree=$(git rev-parse --show-toplevel)
   main_worktree="$container/main"
   ```
   If `current_worktree` != `main_worktree`:
   ```
   You're running /ending-session from inside the session worktree.
   Worktree cleanup requires running from main to avoid directory lock issues.

   Please switch to main first:
   cd {container}/main

   Then run /ending-session again.
   ```
   Stop execution — do not proceed with merge.

2. **Add ghost worktree detection** after worktree removal (after line 169 / line 235):
   ```bash
   # Verify removal succeeded
   if [ -d "$container/{type}/{session-name}" ]; then
     echo "Worktree directory persists (ghost state). Manual cleanup needed:"
     echo "rm -rf $container/{type}/{session-name}"
   fi
   ```

3. **Add remote branch cleanup** after local branch deletion:
   ```bash
   git -C "$bare" push origin --delete {type}/{session-name} 2>/dev/null || true
   ```
   Note: `|| true` because remote branch may not exist (local-only sessions).

4. **Update output template** (lines 177-188) to include cleanup status:
   ```
   Worktree: removed
   Branch: deleted (local + remote)
   ```

**Success criteria:**
- [x] Running from session worktree shows redirect message and stops
- [x] Running from main proceeds with merge + cleanup normally
- [x] Ghost worktree detection present after removal commands
- [x] Remote branch cleanup attempted (with graceful failure)

### Phase 3: Update meta.json schema + starting-session
**Goal**: New sessions write `claudeSessionIds: []` in meta.json. Preserve `sessionId` for backward compat.

**Files to modify:**
- `plugins/commandbase-session/skills/starting-session/SKILL.md`

**Changes:**

1. **Update meta.json template** (lines 199-209):
   ```json
   {
     "sessionId": "<session-name>",
     "claudeSessionIds": [],
     "name": "<session-name>",
     "branch": "<type/session-name>",
     "worktree": "/c/code/{project}/{type}/{session-name}",
     "created": "<ISO 8601>",
     "gitBranch": "<type/session-name>"
   }
   ```
   - `sessionId` stays as session name for backward compat
   - `claudeSessionIds` starts empty, populated by SessionStart hook

**Success criteria:**
- [x] meta.json template includes `claudeSessionIds: []`
- [x] `sessionId` field preserved (not removed)
- [x] Step 6 (Write meta.json) updated with new schema

### Phase 4: Update detect-session.py to persist UUIDs
**Goal**: SessionStart hook appends Claude UUID to meta.json on every fire.

**Files to modify:**
- `plugins/commandbase-session/scripts/detect-session.py`
- `plugins/commandbase-session/scripts/session_utils.py`

**Changes to session_utils.py:**

1. **Add `update_meta_json()` function** after `update_session_map()` (after line 146):
   ```python
   def update_meta_json(session_dir, claude_session_id):
       """Append a Claude session UUID to meta.json's claudeSessionIds array."""
       meta_path = os.path.join(session_dir, "meta.json")
       meta = {}
       if os.path.exists(meta_path):
           try:
               with open(meta_path, "r") as f:
                   meta = json.load(f)
           except (json.JSONDecodeError, OSError):
               return  # Don't corrupt existing meta.json

       ids = meta.get("claudeSessionIds", [])
       if claude_session_id and claude_session_id not in ids:
           ids.append(claude_session_id)
           meta["claudeSessionIds"] = ids
           atomic_write_json(meta_path, meta)
   ```

**Changes to detect-session.py:**

1. **After session match** (after line 52), add UUID persistence:
   ```python
   # Persist Claude session UUID to meta.json
   if session_id and name:
       session_dir = get_session_dir(cwd, name)
       update_meta_json(session_dir, session_id)
   ```

2. **Import the new function** at the top:
   ```python
   from session_utils import (
       ..., update_meta_json, get_session_dir
   )
   ```

**Success criteria:**
- [x] `update_meta_json()` function exists in session_utils.py
- [x] detect-session.py calls `update_meta_json()` after session match
- [x] Deduplication: same UUID not appended twice
- [x] Graceful failure: corrupt meta.json doesn't crash the hook
- [ ] New Claude Code session in a session worktree appends UUID to meta.json (deferred to Phase 7 live test)

### Phase 5: Fix nudge hook false positives
**Goal**: Nudge hook suppresses when git commands come from `/committing-changes`.

**Files to modify:**
- `plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py`
- `plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md`

**Changes to nudge-commit-skill.py:**

1. **Add comment marker check** before the nudge output (after line 20):
   ```python
   # Suppress nudge when invoked from /committing-changes skill
   if "# via-committing-changes" in command:
       sys.exit(0)
   ```

**Changes to committing-changes/SKILL.md:**

1. **Add marker instruction** to the git commit and git push command sections:
   ```
   When running git commit or git push commands, append the comment marker
   `# via-committing-changes` to the command to suppress the nudge hook:

   git commit -m "message" # via-committing-changes
   git push origin branch # via-committing-changes
   ```

**Success criteria:**
- [x] Nudge hook checks for `# via-committing-changes` in command string
- [x] `/committing-changes` skill instructs appending the marker
- [x] Direct `git commit` without marker still triggers nudge
- [x] `git commit # via-committing-changes` does NOT trigger nudge

### Phase 6: Update skills for new schema + post-session mode
**Goal**: Update learning-from-sessions and resuming-session to use `claudeSessionIds` array and support post-session transcript reading.

**Files to modify:**
- `plugins/commandbase-session/skills/learning-from-sessions/SKILL.md`
- `plugins/commandbase-session/skills/resuming-session/SKILL.md`

**Changes to learning-from-sessions/SKILL.md:**

1. **Add Post-Session Mode** as a third operational mode (after Retrospective Mode, ~line 259):

   ```markdown
   ## Post-Session Mode

   When invoked with a session name argument after the session has ended
   (e.g., `/learning-from-sessions auth-mvp`):

   1. **Locate session**: Look up session name in container-level `session-map.json`
   2. **Read meta.json**: Get `claudeSessionIds` array from the session's state directory
   3. **Find transcripts**: For each UUID, locate transcript at:
      `~/.claude/projects/{path-encoded-worktree}/{uuid}.jsonl`
      Path encoding: replace path separators with `--`
      (e.g., `/c/code/project/feature/auth` → `C--code-project-feature-auth`)
   4. **Parse transcripts**: Stream JSONL, extract:
      - Tool failures (`is_error: true` in tool_result)
      - Debugging sequences (multiple tool attempts on same problem)
      - Error → resolution pairs (error followed by successful fix)
      - Thinking blocks discussing root causes
   5. **Correlate with errors.log**: Match transcript errors against errors.log entries
   6. **Proceed to Capture Workflow** (Steps 1-6) with extracted candidates
   ```

2. **Update Session Awareness** (~line 54) to handle ended sessions:
   - If session status is `"ended"`: use Post-Session Mode
   - If session-map entry has `claudeSessionIds`: include in context

3. **Update Gate Function** (line 31) to add transcript reading step:
   ```
   1. SESSION: Detect repo layout, find session. If post-session: read claudeSessionIds from meta.json.
   ```

**Changes to resuming-session/SKILL.md:**

1. **Update meta.json reading** in Mode A Step 1 to handle both schemas:
   - Read `claudeSessionIds` if present (new schema)
   - Fall back to `sessionId` if `claudeSessionIds` missing (old schema)

2. **Show transcript info** in resume summary when `claudeSessionIds` exists:
   ```
   Transcripts: {count} Claude sessions recorded
   ```

**Success criteria:**
- [x] learning-from-sessions has Post-Session Mode section with transcript reading instructions
- [x] Session Awareness handles ended sessions and `claudeSessionIds`
- [x] resuming-session reads `claudeSessionIds` array with fallback to `sessionId`
- [x] Post-session mode documents the path-encoding pattern for transcript lookup

### Phase 7: Sync global skills + validate
**Goal**: All modified skills synced to `~/.claude/skills/` and end-to-end validation.

**Steps:**
1. Copy all modified SKILL.md files to `~/.claude/skills/{name}/SKILL.md`:
   - ending-session
   - starting-session
   - learning-from-sessions
   - resuming-session
   - committing-changes
2. Verify all 45 skills match between plugin source and global
3. Run validation:
   - Start a new Claude Code session to verify SessionStart hook fires
   - Check that `detect-session.py` outputs session context
   - Verify no import errors from plugin scripts

**Success criteria:**
- [x] All modified skills synced to plugin cache (adapted: plugins deliver via cache, not ~/.claude/skills/)
- [x] SessionStart hook fires and outputs session detection (verified at session start)
- [x] No Python import errors in any hook script (all 6 scripts compile clean)
- [x] All 11 deferred actions from learnings doc addressed

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Plugin path in settings.json breaks if repo moves | Document the dependency. Future: plugin install system handles this. |
| Comment marker stripped by shell | Unlikely — bash preserves `#` comments in quoted strings. Test during Phase 5. |
| Large transcripts slow down learning extraction | Post-session mode is instruction-only for now. Actual parsing perf addressed when building the engine. |
| Old sessions missing `claudeSessionIds` | Backward compat: skills fall back to `sessionId` field. No migration needed. |
| SessionStart hook slows session startup | `detect-session.py` is fast (~50ms). Already tested in plugin. |

## Dependencies

```
Phase 0 (hooks) ← no deps, do first
Phase 1 (bare repo fix) ← no deps
Phase 2 (worktree cleanup) ← Phase 1 (needs bare path pattern)
Phase 3 (meta.json schema) ← no deps
Phase 4 (UUID persistence) ← Phase 0 (hook must be installed) + Phase 3 (schema must exist)
Phase 5 (nudge fix) ← no deps
Phase 6 (skill updates) ← Phase 3 (schema) + Phase 4 (UUID persistence)
Phase 7 (sync + validate) ← all phases complete
```

Phases 0, 1, 3, 5 can run in parallel. Phase 2 after 1. Phase 4 after 0+3. Phase 6 after 3+4. Phase 7 last.
