---
git_commit: 2d50723
last_updated: 2026-02-05
last_updated_by: docs-updater
last_updated_note: "Updated git_commit to current HEAD - no content changes needed, plan remains completed"
topic: "Checkpoint Skill with RPI Workflow Integration"
tags: [plan, checkpoint, implementing-plans, planning-codebases, validating-implementations, regression]
status: completed
references:
  - C:/code/commandbase/.docs/research/01-28-2026-checkpoint-command-pattern.md
  - C:/code/commandbase/newskills/planning-codebases/SKILL.md
  - C:/code/commandbase/newskills/implementing-plans/SKILL.md
  - C:/code/commandbase/newskills/validating-implementations/SKILL.md
  - C:/code/commandbase/newskills/checkpointing/SKILL.md
---

# Checkpoint Skill with RPI Workflow Integration

> **Historical Note (2026-02-01)**:
> Skills referenced in this plan have been renamed:
> - `/checkpoint` -> `/checkpointing`
> - `/pcode` -> `/planning-codebases`
> - `/icode` -> `/implementing-plans`
> - `/vcode` -> `/validating-implementations`
> - `/commit` -> `/committing-changes`
> See `newskills/checkpointing/SKILL.md` for the implemented skill.

## Overview

Create a `/checkpoint` skill that enables named snapshots during development, then integrate automatic checkpoint suggestions into `/pcode`, `/icode`, and `/vcode` to catch regressions between phases.

## Desired End State

1. `/checkpoint create "name"` - Creates a named checkpoint with current git SHA
2. `/checkpoint verify "name"` - Compares current state to checkpoint (files changed, git diff summary)
3. `/checkpoint list` - Shows all checkpoints for current project
4. `/checkpoint clear` - Removes old checkpoints, keeps last 5
5. Other skills automatically suggest checkpoints at key moments:
   - `/pcode` → offers checkpoint after plan approval
   - `/icode` → offers checkpoint after each phase, verifies before next phase
   - `/vcode` → offers checkpoint verification against baseline

### Verification

- [ ] `/checkpoint create "test"` creates entry in `.claude/checkpoints.log`
- [ ] `/checkpoint verify "test"` shows files changed since checkpoint
- [ ] `/checkpoint list` displays all checkpoints with timestamps
- [ ] `/pcode` mentions checkpoint after plan finalization
- [ ] `/icode` suggests checkpoint after phase completion
- [ ] `/vcode` offers checkpoint comparison option

## What We're NOT Doing

- Test result storage at checkpoint time (too complex, git diff is sufficient)
- Coverage delta tracking (requires tooling integration)
- Automatic checkpoint creation (always user-initiated or suggested)
- Hook-based automation (keeping it lightweight per user preference)

## Implementation Approach

Use git-based checkpoints (SHA storage in log file) rather than file-based snapshots. Integration is via documentation/suggestions in skill files, not code coupling.

---

## Phase 1: Create /checkpoint Skill

### Overview
Create the core checkpoint skill with all four operations.

### Changes Required:

#### 1. Create skill directory and file
**Directory**: `newskills/checkpoint/`
**File**: `newskills/checkpoint/SKILL.md`

```markdown
---
description: Create and verify named checkpoints for regression detection
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

### /checkpoint create "name"

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
   /checkpoint verify "name"
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

### /checkpoint verify "name"

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

### /checkpoint list

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
   /checkpoint verify "checkpoint-name"
   ```

**If no checkpoints:**
```
No checkpoints found for this project.

Create one with:
/checkpoint create "checkpoint-name"
```

### /checkpoint clear

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
- `plan-approved` - After /pcode plan is finalized
- `phase-N-done` - After completing /icode phase N
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
/pcode → Plan approved → /checkpoint create "plan-approved"
   ↓
/icode Phase 1 → Complete → /checkpoint create "phase-1-done"
   ↓
/icode Phase 2 → Start → /checkpoint verify "phase-1-done"
   ↓
/icode Phase 2 → Complete → /checkpoint create "phase-2-done"
   ↓
/vcode → Validate → /checkpoint verify "plan-approved"
   ↓
/commit → Commit changes
```

## The Bottom Line

**Checkpoints are verification anchors.**

Create them at known-good states. Verify against them to catch regressions. Keep the log clean.
```

### Success Criteria:
- [x] `newskills/checkpoint/SKILL.md` exists
- [x] Skill follows Iron Law / Gate Function pattern
- [x] All four operations documented (create/verify/list/clear)
- [x] Storage format specified

---

## Phase 2: Integrate with /pcode

### Overview
Add checkpoint suggestion after plan finalization in /pcode skill.

### Changes Required:

#### 1. Update /pcode SKILL.md
**File**: `newskills/pcode/SKILL.md`
**Location**: After Step 5 (Review section), around line 354

**Add after "3. Continue refining until the user is satisfied":**

```markdown
4. **Suggest baseline checkpoint**:
   ```
   Plan finalized at `.docs/plans/[filename].md`

   Would you like to create a checkpoint before implementation?
   /checkpoint create "plan-approved"

   This captures the pre-implementation state, enabling:
   - Comparison after each /icode phase
   - Full delta review during /vcode
   - Rollback reference if needed
   ```
```

### Success Criteria:
- [x] `/pcode` SKILL.md mentions checkpoint after plan approval
- [x] Suggestion explains the benefit

---

## Phase 3: Integrate with /icode

### Overview
Add checkpoint suggestions after phase completion and verification before next phase.

### Changes Required:

#### 1. Update /icode SKILL.md
**File**: `newskills/icode/SKILL.md`
**Location**: Update Workflow Integration section (lines 208-221)

**Replace existing Workflow Integration section with:**

```markdown
## Workflow Integration

**REQUIRED:** Apply verification-before-completion discipline throughout.

### Checkpoint Integration

After completing each phase with evidence, suggest a checkpoint:

```
Phase [N] complete.

Verification:
- [test results]
- [other checks]

Create checkpoint before next phase?
/checkpoint create "phase-N-done"

This enables regression detection if Phase [N+1] breaks something.
```

Before starting a new phase (if previous checkpoint exists):

```
Starting Phase [N+1].

Verify no regressions from previous phase?
/checkpoint verify "phase-N-done"

[If verify shows unexpected changes, investigate before proceeding]
```

### Full Workflow

```
/pcode → /checkpoint create "plan-approved"
   ↓
/icode Phase 1 → Evidence → /checkpoint create "phase-1-done"
   ↓
/icode Phase 2 → /checkpoint verify "phase-1-done" → Evidence → /checkpoint create "phase-2-done"
   ↓
... continue pattern ...
   ↓
/vcode → /checkpoint verify "plan-approved"
   ↓
/commit
```

**After all phases complete:**
- Run `/vcode` to get independent validation
- Run `/checkpoint verify "plan-approved"` for full delta review
- Only then proceed to `/commit`
```

### Success Criteria:
- [x] `/icode` suggests checkpoint after each phase
- [x] `/icode` suggests verification before starting new phase
- [x] Workflow diagram shows checkpoint integration

---

## Phase 4: Integrate with /vcode

### Overview
Add checkpoint verification as a validation option.

### Changes Required:

#### 1. Update /vcode SKILL.md - Step 5 options
**File**: `newskills/vcode/SKILL.md`
**Location**: Step 5 "Present Results" section (around line 155-163)

**Update the "Would you like me to:" list:**

```markdown
### Step 5: Present Results

Show the validation report and ask:
```
Validation complete. [Summary of status]

[Show report]

Would you like me to:
1. Fix the failing issues
2. Update the plan to reflect changes
3. Run checkpoint comparison (if checkpoints exist)
4. Continue to commit/PR
```
```

#### 2. Add Checkpoint Verification subsection
**Location**: Before "## Relationship to Other Commands" (around line 209)

**Add new section:**

```markdown
### Checkpoint Verification (Optional)

If checkpoints were created during `/icode` phases:

```
Checkpoint comparison available.

/checkpoint list
- plan-approved (2026-01-28-10:30) @ abc1234
- phase-1-done (2026-01-28-11:45) @ def5678
- phase-2-done (2026-01-28-14:20) @ ghi7890

Run full comparison to plan baseline?
/checkpoint verify "plan-approved"
```

This shows:
- Total files changed since plan approval
- All commits made during implementation
- Clear audit trail for PR description

**Combine with validation report:**
```
## Validation Report: [Plan Name]

### Implementation Delta (from checkpoint)
Files changed since plan-approved: 15
Commits: 5
Test delta: +12 passing, -0 failing

### Phase Status
[rest of report...]
```
```

### Success Criteria:
- [x] `/vcode` offers checkpoint verification option
- [x] New subsection explains checkpoint integration
- [x] Combined report format documented

---

## Phase 5: Deploy and Test

### Overview
Deploy all changes to ~/.claude/skills/ and verify functionality.

### Tasks:

1. **Deploy checkpoint skill**
```bash
cp -r newskills/checkpoint ~/.claude/skills/
```

2. **Redeploy updated skills**
```bash
cp -r newskills/pcode ~/.claude/skills/
cp -r newskills/icode ~/.claude/skills/
cp -r newskills/vcode ~/.claude/skills/
```

3. **Verify deployments**
```bash
ls -la ~/.claude/skills/checkpoint/
ls -la ~/.claude/skills/pcode/
ls -la ~/.claude/skills/icode/
ls -la ~/.claude/skills/vcode/
```

4. **Manual testing**
- New session: Run `/checkpoint list` (should report no checkpoints)
- Run `/checkpoint create "test"`
- Verify `.claude/checkpoints.log` created
- Run `/checkpoint verify "test"` (should show no changes)
- Run `/checkpoint list` (should show test checkpoint)
- Run `/checkpoint clear` (should keep checkpoint, only 1 exists)

### Success Criteria:
- [x] `~/.claude/skills/checkpoint/` exists with SKILL.md
- [x] Updated skills deployed
- [x] `/checkpoint create` creates log entry (skill documented)
- [x] `/checkpoint verify` shows git diff (skill documented)
- [x] `/checkpoint list` displays checkpoints (skill documented)
- [x] Integration mentions visible in deployed skill files

---

## Testing Strategy

### Manual Tests:
1. **Checkpoint lifecycle**: create → list → verify → clear
2. **Integration flow**: /pcode → checkpoint → /icode phases → checkpoints → /vcode
3. **Error handling**: verify non-existent checkpoint, create with dirty git state

### Integration Tests:
1. **/pcode integration**: Run /pcode, verify checkpoint suggestion appears
2. **/icode integration**: Complete a phase, verify checkpoint suggestion appears
3. **/vcode integration**: Run /vcode, verify checkpoint option in menu

---

## References

- Research: `.docs/research/01-28-2026-checkpoint-command-pattern.md`
- Source pattern: `C:/code/everything-claude-code/commands/checkpoint.md`
- Skill pattern: `newskills/learn/SKILL.md` (for structure reference)
