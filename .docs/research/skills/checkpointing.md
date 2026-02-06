# Research: bookmarking-code Skill

## Overview

The `bookmarking-code` skill (`~/.claude/skills/bookmarking-code/SKILL.md`) creates and manages named snapshots of git state during development. It enables comparison against previous known-good states, providing verification anchors for regression detection across implementation phases.

**Trigger phrases**: `/checkpoint create`, `/checkpoint verify`, `/checkpoint list`, `save a checkpoint`, `compare to checkpoint`

## The Iron Law (SKILL.md:12-24)

```
NO CHECKPOINT WITHOUT GIT STATE VERIFICATION
```

**Enforcement Rules:**
- Before creating checkpoint: Confirm git state is clean or user acknowledges uncommitted changes
- Before verifying: Check that checkpoint name exists in log file
- No assumptions: Always verify checkpoint log exists, create if needed

## The Gate Function (SKILL.md:26-38)

5-step process before ANY operation:

1. **IDENTIFY**: Which operation? (create/verify/list/clear)
2. **CHECK**: Does .claude/checkpoints.log exist? Create if needed.
3. **VERIFY**: For create - is git state acceptable? For verify - does checkpoint name exist?
4. **EXECUTE**: Perform the operation
5. **REPORT**: Show clear output with evidence

## Operations

### Create Operation
**Command**: `/bookmarking-code create "name"`

**Process:**
1. Check git status for uncommitted changes
2. If dirty state, present 3 options to user
3. Capture git SHA via `git rev-parse --short HEAD`
4. Append to `.claude/checkpoints.log`
5. Report success

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
1. Read log file, find checkpoint by name
2. Run git comparison:
   ```bash
   git diff --stat <checkpoint-sha>..HEAD
   git log --oneline <checkpoint-sha>..HEAD
   ```
3. Report comparison results

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

## RPI Workflow Integration

```
/planning-code → /bookmarking-code create "plan-approved"
   ↓
/implementing-plans Phase 1 → /bookmarking-code create "phase-1-done"
   ↓
/implementing-plans Phase 2 → /bookmarking-code verify "phase-1-done" → /bookmarking-code create "phase-2-done"
   ↓
/validating-code → /bookmarking-code verify "plan-approved"
   ↓
/committing-changes
```

**Integration Points:**
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

- Main: `~/.claude/skills/bookmarking-code/SKILL.md`
