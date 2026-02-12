---
name: ending-worktree
description: "Use this skill when merging a worktree's work back to main and removing it, or when discarding an abandoned worktree. This is git plumbing only -- squash merge, branch deletion, and worktree removal. Does not close session tracking -- use /ending-session for that first. Trigger phrases: '/ending-worktree', 'merge to main', 'remove worktree', 'discard worktree', 'clean up worktree'."
---

# Ending Worktree

You are merging or discarding a git worktree. This skill handles git plumbing only -- squash merge to main, branch deletion, and worktree removal. Session tracking close-out is handled separately by `/ending-session`.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO WORKTREE REMOVAL WITHOUT MERGE VERIFICATION OR EXPLICIT DISCARD
```

Never merge without a dry-run conflict check. Never discard without explicit user confirmation. Never remove a worktree with active sessions.

**No exceptions:**
- Don't merge without checking for conflicts first
- Don't remove a worktree without confirming the mode
- Don't skip the active session check
- Don't skip CLAUDE.md review for merge mode
- Don't discard without name confirmation

## The Gate Function

```
BEFORE ending any worktree:

1. VERIFY: Am I running from main worktree? (required)
2. SESSION: Check for active/handed-off sessions in target worktree
3. CLEAN: Are there uncommitted changes in target worktree?
4. MODE: Ask user: Merge / Discard?
5. CONFLICTS: For merge mode, dry-run check first
6. CLAUDE_MD: For merge mode, review CLAUDE.md changes with user
7. EXECUTE: Merge/discard based on mode
8. COMMIT: For merge mode, invoke /committing-changes
9. CLEANUP: Remove worktree + branch

Skip conflict check = surprise merge failures
```

## Step 1: Verify Running from Main

This skill must be run from the main worktree. Determine the current location:

```bash
# Get current worktree path
worktree_path=$(git rev-parse --show-toplevel)

# Get container and bare repo
container=$(dirname "$(git rev-parse --git-common-dir)")
bare="$container/.bare"

# Get main worktree path
main_worktree="$container/main"
```

If `worktree_path` != `main_worktree`:
```
You're running /ending-worktree from inside a session worktree.
Worktree cleanup requires running from main to avoid directory lock issues.

Please switch to main first:
cd {container}/main

Then run /ending-worktree again.
```
**Stop execution -- do not proceed.**

## Step 2: Identify Target Worktree

If the user specified a worktree name or branch, use that. Otherwise, list available worktrees:

```bash
git -C "$bare" worktree list
```

Present non-main worktrees:

```
Available worktrees:

  #  Branch                    Path
  1  feature/auth-mvp          /c/code/project/feature/auth-mvp
  2  refactor/session-v2       /c/code/project/refactor/session-v2

Which worktree to end?
```

## Step 3: Check for Active Sessions

Read session-map.json and find entries matching the target worktree with `status: "active"` or `"handed-off"`.

If any active or handed-off sessions exist:
```
This worktree has active/handed-off sessions:
- {session-name} (status: active)

End them with /ending-session first, or force removal with the Discard option.
```

For merge mode: **block** -- do not proceed until sessions are ended.
For discard mode: **warn** but allow with explicit confirmation (the user is deliberately abandoning work).

## Step 4: Check Uncommitted Changes

```bash
git -C "{target_worktree}" status --porcelain
```

If dirty:
```
The target worktree has uncommitted changes:
{status output}

Options:
1. Commit them first: cd {target_worktree} && /committing-changes
2. Proceed anyway (changes will be included in merge or lost in discard)
```

## Step 5: Mode Selection

Ask the user:

```
How would you like to end this worktree?

1. Merge   -- Squash merge to main, remove worktree + branch (default)
2. Discard -- Abandon all work, force remove worktree + branch (destructive)
```

## Mode A: Merge

### Step A1: Conflict detection (dry run)

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
Merge conflicts detected between this worktree and main:

CONFLICT: src/auth.ts (both modified)
CONFLICT: tests/auth.test.ts (both modified)

Options:
1. Resolve conflicts manually in the worktree, then retry /ending-worktree
2. Discard the worktree instead
3. Cancel

Which would you prefer?
```

If clean:
```bash
git merge --abort  # Clean up the dry run
```

### Step A2: Squash merge

```bash
cd {container}/main
git merge --squash {session-branch}
```

### Step A3: CLAUDE.md review

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

### Step A4: Commit + Push

Invoke `/committing-changes` with squash merge context. The files are pre-staged by `git merge --squash`. The commit message should summarize the worktree's work.

### Step A5: Remove worktree + branch

```bash
git -C "$bare" worktree remove "$container/{type}/{worktree-name}"
git -C "$bare" branch -d {type}/{worktree-name}
git -C "$bare" push origin --delete {type}/{worktree-name} 2>/dev/null || true
```

**Why `-C "$bare"`**: The container directory is not a git repo -- `.bare/` is. Running git commands from the container fails with `fatal: not a git repository`.

**Why `|| true` on remote delete**: Remote branch may not exist for local-only sessions.

After removal, verify the worktree directory is actually gone:
```bash
if [ -d "$container/{type}/{worktree-name}" ]; then
  echo "Worktree directory persists (ghost state). Manual cleanup needed:"
  echo "rm -rf $container/{type}/{worktree-name}"
fi
```

### Step A6: Output

```
WORKTREE ENDED (MERGED)
========================
Branch: {type}/{worktree-name} (merged + deleted)
Squash commit: {sha} on main
Worktree: removed
Branch: deleted (local + remote)

Work merged to main. You're now in: {container}/main/
```

## Mode B: Discard

### Step B1: Confirmation

Destructive action requires explicit consent:

```
This will permanently discard all work on branch {type}/{worktree-name}.
All uncommitted and committed changes on this branch will be lost.

Are you absolutely sure? Type the session name to confirm: {worktree-name}
```

Wait for exact name match before proceeding.

### Step B2: Force remove worktree + branch

```bash
git -C "$bare" worktree remove --force "$container/{type}/{worktree-name}"
git -C "$bare" branch -D {type}/{worktree-name}
git -C "$bare" push origin --delete {type}/{worktree-name} 2>/dev/null || true
```

After removal, verify the worktree directory is actually gone:
```bash
if [ -d "$container/{type}/{worktree-name}" ]; then
  echo "Worktree directory persists (ghost state). Manual cleanup needed:"
  echo "rm -rf $container/{type}/{worktree-name}"
fi
```

### Step B3: Update session-map.json

For any sessions associated with this worktree in session-map.json, set `status: "ended"`.

### Step B4: Output

```
WORKTREE ENDED (DISCARDED)
===========================
Branch: {type}/{worktree-name} (force deleted)
Worktree: removed
All work on this branch has been discarded.

You're now in: {container}/main/
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to merge without dry-run conflict check
- About to remove worktree with active sessions (merge mode)
- About to remove worktree without confirming mode
- Skipping CLAUDE.md review in merge mode
- About to discard without explicit user name confirmation
- Running from inside the target worktree (not main)
- About to close session tracking (that's /ending-session)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "No conflicts, skip dry run" | Run it anyway. Conflicts can appear after rebase. |
| "CLAUDE.md probably didn't change" | Check the diff. Session-specific edits are common. |
| "Sessions are probably ended" | Check session-map.json. Probably isn't evidence. |
| "User wants to clean up quickly" | Active session check catches lost tracking data. |
| "Discard is fine, user said so" | Require name confirmation. Destructive = explicit consent. |
| "I should also close the session" | No. That's /ending-session. Stay in scope. |

## The Bottom Line

**Worktree removal is git plumbing only.**

Verify from main. Check sessions. Check conflicts. Merge or discard. Clean up. Nothing more.

This is non-negotiable. Every worktree removal. Every time.
