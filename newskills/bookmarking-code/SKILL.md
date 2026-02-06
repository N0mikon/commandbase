---
name: bookmarking-code
description: "Use this skill when saving development checkpoints, comparing against previous states, or detecting regressions between phases. This includes creating named snapshots before risky changes, verifying no regressions after implementation, listing available checkpoints, and clearing old checkpoints. Trigger phrases: '/checkpoint create', '/checkpoint verify', '/checkpoint list', 'save a checkpoint', 'compare to checkpoint'."
---

# Checkpoint

You are managing development checkpoints - named snapshots that enable comparison against previous known-good states.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO CHECKPOINT WITHOUT GIT STATE VERIFICATION
```

Before creating or verifying checkpoints, confirm git state is clean or intentionally dirty.

**No exceptions:**
- Don't create checkpoints with uncommitted changes unless user confirms
- Don't verify against non-existent checkpoints
- Don't assume checkpoint exists - check the log first

## The Gate Function

```
BEFORE any checkpoint operation:

1. IDENTIFY: Which operation? (create/verify/list/clear)
2. CHECK: Does .claude/checkpoints.log exist? Create if needed.
3. VERIFY: For create - is git state acceptable?
          For verify - does checkpoint name exist?
4. EXECUTE: Perform the operation
5. REPORT: Show clear output with evidence

Skip verification = unreliable checkpoints
```

## Operations

### /bookmarking-code create "name"

Creates a named checkpoint at current git state.

**Process:**
1. Check git status for uncommitted changes
2. If dirty, ask user to confirm or commit first
3. Get current git SHA: `git rev-parse --short HEAD`
4. Append to `.claude/checkpoints.log`:
   ```
   YYYY-MM-DD-HH:MM | checkpoint-name | abc1234
   ```
5. Report success:
   ```
   Checkpoint created: "name"
   Git SHA: abc1234
   Timestamp: 2026-01-28-14:30

   To verify against this checkpoint later:
   /bookmarking-code verify "name"
   ```

**If uncommitted changes exist:**
```
Warning: You have uncommitted changes.

Creating a checkpoint now will capture the committed state (abc1234),
not your working directory changes.

Options:
1. Create checkpoint anyway (captures last commit)
2. Commit changes first, then checkpoint
3. Cancel

Which would you prefer?
```

### /bookmarking-code verify "name"

Compares current state to a named checkpoint.

**Process:**
1. Read `.claude/checkpoints.log`
2. Find checkpoint by name (use most recent if duplicates)
3. If not found, list available checkpoints
4. Run comparison:
   ```bash
   git diff --stat <checkpoint-sha>..HEAD
   git log --oneline <checkpoint-sha>..HEAD
   ```
5. Report results:
   ```
   CHECKPOINT COMPARISON: "name"
   ==============================
   Checkpoint SHA: abc1234 (2026-01-28-10:30)
   Current SHA:    def5678

   Commits since checkpoint: 3
   - def5678 Phase 2: Add validation
   - cde4567 Phase 1: Core implementation
   - bcd3456 Fix typo in config

   Files changed: 12
   - src/auth.ts (+45, -12)
   - src/middleware.ts (+23, -0)
   - tests/auth.test.ts (+67, -0)
   ...

   No regressions detected in file structure.
   Run tests to verify behavior: [project test command if known]
   ```

**If checkpoint not found:**
```
Checkpoint "name" not found.

Available checkpoints:
- plan-approved (2026-01-28-10:30) @ abc1234
- phase-1-done (2026-01-28-11:45) @ def5678

Did you mean one of these?
```

### /bookmarking-code list

Shows all checkpoints for current project.

**Process:**
1. Read `.claude/checkpoints.log`
2. Parse and display:
   ```
   CHECKPOINTS
   ===========
   Name              Timestamp         SHA      Status
   ----              ---------         ---      ------
   plan-approved     2026-01-28-10:30  abc1234  12 commits behind
   phase-1-done      2026-01-28-11:45  def5678  5 commits behind
   phase-2-done      2026-01-28-14:20  ghi7890  current

   Total: 3 checkpoints

   To verify against a checkpoint:
   /bookmarking-code verify "checkpoint-name"
   ```

**If no checkpoints:**
```
No checkpoints found for this project.

Create one with:
/bookmarking-code create "checkpoint-name"
```

### /bookmarking-code clear

Removes old checkpoints, keeping the most recent 5.

**Process:**
1. Read `.claude/checkpoints.log`
2. Count entries
3. If more than 5, confirm deletion:
   ```
   Found 8 checkpoints. Keep the 5 most recent?

   Will remove:
   - old-feature (2026-01-15-09:00)
   - experiment-1 (2026-01-16-14:30)
   - experiment-2 (2026-01-17-11:00)

   Proceed? (yes/no)
   ```
4. After confirmation, keep last 5 lines in log
5. Report:
   ```
   Cleared 3 old checkpoints.
   Remaining: 5 checkpoints
   ```

## Storage

**Location**: `.claude/checkpoints.log` (project root)

**Format**: Pipe-delimited, one checkpoint per line
```
YYYY-MM-DD-HH:MM | checkpoint-name | git-sha
```

**Example**:
```
2026-01-28-10:30 | plan-approved | 3f4a2b1
2026-01-28-11:45 | phase-1-done | 8c9d5e2
2026-01-28-14:20 | phase-2-done | 2a3b4c5
```

## Naming Conventions

Suggested checkpoint names:
- `plan-approved` - After /planning-code plan is finalized
- `phase-N-done` - After completing /implementing-plans phase N
- `pre-refactor` - Before major refactoring
- `feature-complete` - Before validation/PR

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Creating checkpoint without checking git status
- Verifying against checkpoint that doesn't exist
- Assuming checkpoint log exists without checking
- Clearing checkpoints without user confirmation

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Git state is probably clean" | Check with `git status`. Verify. |
| "Checkpoint probably exists" | Read the log file. Confirm. |
| "User wants to clear all" | Confirm before destructive action. |

## Workflow Integration

Checkpoints integrate with the RPI workflow:

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

## The Bottom Line

**Checkpoints are verification anchors.**

Create them at known-good states. Verify against them to catch regressions. Keep the log clean.
