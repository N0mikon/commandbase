---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file reference from ~/.claude/skills/ to plugin path, added session awareness section, updated Gate Function from 5 to 6 steps, added session-scoped operations and naming conventions"
references:
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
---

# Research: bookmarking-code Skill

## Overview

The `bookmarking-code` skill (`plugins/commandbase-core/skills/bookmarking-code/SKILL.md`) creates and manages named snapshots of git state during development. It enables comparison against previous known-good states, providing verification anchors for regression detection across implementation phases.

**Trigger phrases**: `/checkpoint create`, `/checkpoint verify`, `/checkpoint list`, `save a checkpoint`, `compare to checkpoint`

## The Iron Law

```
NO CHECKPOINT WITHOUT GIT STATE VERIFICATION
```

**Enforcement Rules:**
- Before creating checkpoint: Confirm git state is clean or user acknowledges uncommitted changes
- Before verifying: Check that checkpoint name exists in log file
- No assumptions: Always verify checkpoint log exists, create if needed

## Session Awareness

Before creating or verifying checkpoints, the skill detects the active session:

1. Detect repo layout via `git rev-parse --git-common-dir` vs `--git-dir`
2. If bare-worktree layout (paths differ): read container-level `session-map.json`, find entry whose `worktree` matches current cwd. Use `.claude/sessions/{name}/checkpoints.log` in the worktree.
3. Fallback: check `.claude/sessions/_current` for legacy sessions.
4. If no session found: Use `.claude/checkpoints.log` (default behavior).

When session-scoped:
- Checkpoint names are automatically prefixed: `{session-name}:{checkpoint-name}`
- The prefix is for display/search only -- storage uses the session folder for isolation
- Verification commands search the session-scoped log first

## The Gate Function

6-step process before ANY operation:

1. **IDENTIFY**: Which operation? (create/verify/list/clear)
2. **SESSION**: Detect repo layout, find session for current worktree via session-map.json. Fall back to _current.
3. **CHECK**: Does checkpoint log exist? Create if needed.
   - Session active: `.claude/sessions/{name}/checkpoints.log` (in worktree root)
   - No session: `.claude/checkpoints.log`
4. **VERIFY**: For create - is git state acceptable? For verify - does checkpoint name exist?
5. **EXECUTE**: Perform the operation
6. **REPORT**: Show clear output with evidence

## Operations

### Create Operation
**Command**: `/bookmarking-code create "name"`

**Process:**
1. Check git status for uncommitted changes
2. If dirty state, present 3 options to user
3. Capture git SHA via `git rev-parse --short HEAD`
4. Determine checkpoint log location (using session detection from Gate Function step 2):
   - If session found: use `.claude/sessions/{name}/checkpoints.log`
   - Otherwise: use `.claude/checkpoints.log`
5. Append to checkpoint log
6. Report success

**Success Output:**
```
Checkpoint created: "name"
Git SHA: abc1234
Timestamp: 2026-01-28-14:30

To verify against this checkpoint later:
/bookmarking-code verify "name"
```

### Verify Operation
**Command**: `/bookmarking-code verify "name"`

**Process:**
1. Determine checkpoint log location (using session detection from Gate Function step 2):
   - If session found: search `.claude/sessions/{name}/checkpoints.log` first
   - If not found in session log (or no session): fall back to `.claude/checkpoints.log`
2. Find checkpoint by name (use most recent if duplicates)
3. If not found in either log, list available checkpoints
4. Run git comparison:
   ```bash
   git diff --stat <checkpoint-sha>..HEAD
   git log --oneline <checkpoint-sha>..HEAD
   ```
5. Report comparison results

**Output:**
```
CHECKPOINT COMPARISON: "name"
==============================
Checkpoint SHA: abc1234 (2026-01-28-10:30)
Current SHA:    def5678

Commits since checkpoint: 3
Files changed: 12
```

### List Operation
**Command**: `/bookmarking-code list`

Shows all checkpoints with status (current vs N commits behind).

### Clear Operation
**Command**: `/bookmarking-code clear`

Keeps 5 most recent checkpoints, requires user confirmation before deletion.

## Storage Format

**File**: `.claude/checkpoints.log` (project root)

**Format**: Pipe-delimited, one checkpoint per line
```
YYYY-MM-DD-HH:MM | checkpoint-name | git-sha
```

## Naming Conventions

Suggested names aligned with RPI workflow:
- `plan-approved` - After `/planning-code` plan is finalized
- `phase-N-done` - After completing `/implementing-plans` phase N
- `pre-refactor` - Before major refactoring
- `feature-complete` - Before validation/PR

When a session is active, checkpoints display with session prefix:
- `auth-mvp:phase-2-done` (session-scoped)
- `auth-mvp:pre-refactor` (session-scoped)

## RPI Workflow Integration

Checkpoints integrate with the RPI workflow. When a session is created via `/starting-session`, all checkpoints are automatically scoped to the session's worktree folder.

```
/planning-code → Plan approved → /bookmarking-code create "plan-approved"
   ↓
/implementing-plans Phase 1 → Complete → /bookmarking-code create "phase-1-done"
   ↓
/implementing-plans Phase 2 → Start → /bookmarking-code verify "phase-1-done"
   ↓
/implementing-plans Phase 2 → Complete → /bookmarking-code create "phase-2-done"
   ↓
/validating-code → Validate → /bookmarking-code verify "plan-approved"
   ↓
/committing-changes → Commit changes
```

**Integration Points:**
- `/starting-session` - Creates session scope; all subsequent checkpoints are isolated to the session worktree
- `/planning-code` suggests checkpoint after plan approval
- `/implementing-plans` suggests checkpoints between phases
- `/validating-code` offers checkpoint comparison in validation report

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Git state is probably clean" | Check with `git status`. Verify. |
| "Checkpoint probably exists" | Read the log file. Confirm. |
| "User wants to clear all" | Confirm before destructive action. |

## File Reference

- Main: `plugins/commandbase-core/skills/bookmarking-code/SKILL.md`
