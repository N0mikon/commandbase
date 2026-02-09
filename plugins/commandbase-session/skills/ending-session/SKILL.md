---
name: ending-session
description: "Use this skill when ending a work session, merging work back to main, switching context, creating a handoff for another session, or wrapping up current work. This includes squash merging the session branch into main, removing the worktree, optionally creating handover documents to .docs/handoffs/, checking for uncaptured learnings, and updating session status. Trigger phrases: '/ending-session', 'end session', 'wrap up', 'merge and end', 'hand this off', 'finish session'."
---

# Ending Session

You are ending a session by merging, handing off, or discarding the session's work.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SESSION END WITHOUT MERGE VERIFICATION OR EXPLICIT DISCARD
```

Never merge without a dry-run conflict check. Never discard without explicit user confirmation.

**No exceptions:**
- Don't merge without checking for conflicts first
- Don't remove a worktree without confirming the mode
- Don't skip the learning check
- Don't skip CLAUDE.md review for merge mode

## The Gate Function

```
BEFORE ending any session:

1. VERIFY: Am I in a session worktree? (not main)
2. CLEAN: Are there uncommitted changes?
3. MODE: Ask user: Merge / Handoff / Discard?
4. CONFLICTS: For merge mode, dry-run check first
5. CLAUDE_MD: For merge mode, review CLAUDE.md changes with user
6. LEARN: Check for uncaptured errors
7. EXECUTE: Merge/handoff/discard based on mode
8. COMMIT: For merge mode, invoke /committing-changes (handles commit + push)
9. CLEANUP: Remove worktree (merge/discard) or keep (handoff)

Skip conflict check = surprise merge failures
```

## Session Verification

First, confirm we're in a session worktree:

```bash
# Get current worktree path
worktree_path=$(git rev-parse --show-toplevel)

# Get container
container=$(dirname "$(git rev-parse --git-common-dir)")

# Get current branch
branch=$(git rev-parse --abbrev-ref HEAD)
```

Read container-level `session-map.json` and find the entry matching this worktree.

If in main: "You're on the main branch. No session to end."
If no matching session: "No session found for this worktree."

## Check Uncommitted Changes

```bash
git status --porcelain
```

If dirty: "You have uncommitted changes. Commit them first with /committing-changes, or choose to discard."

## Mode Selection

Ask the user:

```
How would you like to end this session?

1. Merge   -- Squash merge to main, remove worktree (default)
2. Handoff -- Keep branch open, create handoff doc for another session
3. Discard -- Abandon all work on this branch (destructive)
```

## Mode A: Merge End (default)

### Step 1: Conflict detection (dry run)

```bash
cd {container}/main
git merge --no-commit --no-ff {session-branch}
```

If conflicts:
```bash
git merge --abort
```

Present to user:
```
Merge conflicts detected between your session and main:

CONFLICT: src/auth.ts (both modified)
CONFLICT: tests/auth.test.ts (both modified)

Options:
1. Resolve conflicts manually, then retry /ending-session
2. Hand off the session instead (keep branch open)
3. Cancel

Which would you prefer?
```

Return to session worktree after aborting.

If clean:
```bash
git merge --abort  # Clean up the dry run
```

### Step 2: Squash merge

```bash
cd {container}/main
git merge --squash {session-branch}
```

### Step 3: CLAUDE.md review

Check if CLAUDE.md was modified during the session:

```bash
git diff HEAD -- CLAUDE.md
```

If modified, show the diff:
```
CLAUDE.md was modified during this session:

[diff output]

Include these changes on main?
1. Yes - merge CLAUDE.md changes to main
2. No  - discard session-only CLAUDE.md changes
```

If user chooses No:
```bash
git checkout HEAD -- CLAUDE.md
```

### Step 4: Commit + Push

Invoke `/committing-changes` with squash merge context. The files are pre-staged by `git merge --squash`. The commit message should summarize the session's work.

### Step 5: Learning check

Read `{worktree}/.claude/sessions/{name}/errors.log`. If errors exist:

```
This session had N error(s). Consider running /learning-from-sessions before I remove the worktree.
```

Wait for user response before proceeding.

### Step 6: Remove worktree + branch

```bash
cd {container}
git worktree remove {type}/{session-name}
git branch -d {type}/{session-name}
```

### Step 7: Update session-map.json

Set `status: "ended"` for this session's entry in container-level session-map.json.

### Step 8: Output

```
SESSION ENDED
=============
Name: {session-name}
Branch: {type}/{session-name} (merged + deleted)
Squash commit: {sha} on main
Worktree: removed

Work merged to main. You're now in: {container}/main/
```

## Mode B: Handoff End

Branch stays open for another session to pick up.

### Steps

1. Same verification as Mode A (session context + uncommitted changes)
2. **Do NOT merge** -- branch stays open
3. Create handoff document via `docs-writer` agent:
   - Template: What I Was Working On, What I Accomplished, Key Learnings, Files Changed, Current State, Session Context, Next Steps, Context & References, Notes
   - Write to `.docs/handoffs/{date}-{session-name}-handoff.md`
4. Update session-map.json: Set `status: "handed-off"`
5. Learning check (same as Mode A Step 5)
6. **Do NOT remove worktree** -- it stays for the next session

### Output

```
SESSION HANDED OFF
==================
Name: {session-name}
Branch: {type}/{session-name} (kept open)
Worktree: {container}/{type}/{session-name} (kept)
Handoff: .docs/handoffs/{date}-{session-name}-handoff.md

To resume this work:
/resuming-session (from the worktree directory)
```

## Mode C: Discard End

Permanently abandons the session's work.

### Steps

1. Confirm with user (destructive action):
   ```
   This will permanently discard all work on branch {type}/{session-name}.

   Are you absolutely sure? Type the session name to confirm: {session-name}
   ```

2. Remove worktree + branch:
   ```bash
   cd {container}
   git worktree remove --force {type}/{session-name}
   git branch -D {type}/{session-name}
   ```

3. Update session-map.json: Set `status: "ended"`.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to merge without dry-run conflict check
- About to remove worktree without confirming mode
- Skipping CLAUDE.md review in merge mode
- Skipping learning check when errors.log has entries
- About to discard without explicit user confirmation
- Running destructive commands without session name confirmation

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "No conflicts, skip dry run" | Run it anyway. Conflicts can appear after rebase. |
| "CLAUDE.md probably didn't change" | Check the diff. Session-specific edits are common. |
| "User wants to end quickly" | Learning check catches valuable knowledge. Don't skip. |
| "Discard is fine, user said so" | Require name confirmation. Destructive = explicit consent. |
