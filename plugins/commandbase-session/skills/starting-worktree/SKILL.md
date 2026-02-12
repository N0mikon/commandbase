---
name: starting-worktree
description: "Use this skill when creating an isolated git worktree for a feature, fix, or refactor, or when migrating a repo to bare-repo layout for the first time. This is git plumbing only -- no session tracking. Trigger phrases: '/starting-worktree', 'create a worktree', 'new worktree', 'migrate to bare repo'."
---

# Starting Worktree

You are creating an isolated git worktree with its own branch. This skill handles git plumbing only -- branch creation and worktree setup. Session tracking is handled separately by `/starting-session`.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO WORKTREE WITHOUT USER CONFIRMATION OF NAME AND BRANCH TYPE
```

Never create a branch or worktree without explicit user approval of the name and branch type prefix.

**No exceptions:**
- Don't auto-create worktrees silently
- Don't skip the branch type selection
- Don't bypass name validation
- Don't proceed without confirming the migration in Mode A

## The Gate Function

```
BEFORE creating any worktree:

1. DETECT: Is repo migrated? If not -> Mode A (migration)
2. CHECK: Are we in the main worktree? If not -> warn
3. TYPE: Ask user for branch type (feature/fix/refactor)
4. NAME: Suggest name, get user confirmation
5. VALIDATE: Name passes kebab-case rules
6. ONLY THEN: Create branch + worktree

Skip confirmation = worktree without consent
```

## Mode Detection

Run the following to determine which mode to use:

```bash
# Check if we're in a bare-worktree layout
git_common=$(git rev-parse --git-common-dir 2>/dev/null)
git_dir=$(git rev-parse --git-dir 2>/dev/null)
```

If `git_common` and `git_dir` resolve to different absolute paths: **bare-worktree layout** -> Mode B.
If they're the same: **regular repo** -> Mode A (first-time migration).

If already in a session worktree (not main):
```
You're already in a session worktree: {branch_name}
To create a new worktree, switch to the main worktree first:
cd {container}/main
```

## Mode A: First-Time Migration

Triggered when the repo is NOT in bare-worktree layout. One-time per project.

### Step 1: Confirm with user

```
This project hasn't been set up for worktree-based development yet.

I'll reorganize it so each workspace gets its own isolated directory:

Before: /c/code/{project}/          (single directory, all branches)
After:  /c/code/{project}/main/     (main branch)
        /c/code/{project}/feature/  (session branches)

Your daily path will change to /c/code/{project}/main/

Proceed with migration?
```

### Step 2: Verify clean git state

```bash
git status --porcelain
```

If dirty: "You have uncommitted changes. Commit or stash them first."

### Step 3: Detect default branch

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
# Fallback:
git branch --list main master | head -1 | tr -d ' *'
```

### Step 4: Present migration commands

Because Claude Code's cwd will change during migration, present these commands for the user to run from **outside** the repo:

```bash
cd /c/code

# Move repo to become container
mv {project} {project}-migrating
mkdir {project}
mv {project}-migrating/.git {project}/.bare

# Configure as bare repo
git -C {project}/.bare config core.bare true

# Create main worktree (checks out all tracked files)
git -C {project}/.bare worktree add ../main {default_branch}

# Copy untracked/ignored files (no-clobber to avoid nested duplicates)
cp -rn {project}-migrating/.claude/* {project}/main/.claude/ 2>/dev/null
cp -rn {project}-migrating/.docs/* {project}/main/.docs/ 2>/dev/null

# Clean up
rm -rf {project}-migrating

# Create container-level session-map.json
echo '{}' > {project}/session-map.json

# Ensure .claude/sessions/ is in .gitignore
grep -q '.claude/sessions/' {project}/main/.gitignore 2>/dev/null || echo '.claude/sessions/' >> {project}/main/.gitignore
```

**WARNING**: The `cp -rn` commands use `-n` (no-clobber) to prevent nested duplicates when copying directories that `git worktree add` already checked out. Check for duplicates (`.claude/.claude/`, `.docs/.docs/`) after running.

### Step 5: Post-migration message

```
Migration complete!

Your project is now at: /c/code/{project}/main/
Open a new Claude Code session in that directory to continue.

Next time you run /starting-worktree, it will create a worktree directly.
To start session tracking in the new worktree, run /starting-session.
```

## Mode B: Create Worktree

Triggered when the repo is already in bare-worktree layout and we're in the main worktree.

### Step 1: Verify we're in main worktree

Check that the current worktree is the main worktree (not already inside a session worktree).

### Step 2: Choose branch type

Ask the user:

```
What type of work is this worktree for?
1. feature  (new functionality) -- default
2. fix      (bug fix)
3. refactor (restructuring)
```

### Step 3: Name the worktree

Auto-suggest a name based on conversation context. User confirms.

**Validation rules (kebab-case):**
- 3-40 characters
- Pattern: `^[a-z0-9][a-z0-9-]*[a-z0-9]$`
- No leading/trailing/consecutive hyphens
- Examples: `auth-mvp`, `login-timeout-fix`, `session-v2`

Full branch name: `{type}/{worktree-name}` (e.g., `feature/auth-mvp`)

### Step 4: Create branch + worktree

Determine container and bare repo directories:
```bash
container=$(git rev-parse --git-common-dir | xargs dirname)
bare="$container/.bare"
```

Create the worktree using the bare repo and an absolute worktree path:
```bash
git -C "$bare" worktree add "$container/{type}/{worktree-name}" -b {type}/{worktree-name}
```

**Why `-C "$bare"`**: The container directory itself is not a git repo -- `.bare/` is. Running `git worktree add` from the container (or without `-C`) fails with `fatal: not a git repository`. Always target the bare repo explicitly.

### Step 5: Output

```
WORKTREE CREATED
================
Name: {worktree-name}
Branch: {type}/{worktree-name}
Path: /c/code/{project}/{type}/{worktree-name}

Switch to this directory to begin work:
cd /c/code/{project}/{type}/{worktree-name}

To start session tracking in this worktree, run:
/starting-session
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to create a branch without user confirmation
- Skipping the branch type selection
- Name doesn't match kebab-case validation
- Creating a worktree inside another worktree
- Running migration commands without user confirmation
- Proceeding when git state is dirty

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User wants to start quickly" | Confirmation is one question. Never skip. |
| "Feature is the obvious type" | Ask anyway. User decides. |
| "Name looks fine" | Validate against the regex. Every time. |
| "Migration can happen silently" | User must confirm path changes. |

## The Bottom Line

**Worktree creation is git plumbing only.**

Create the branch. Create the worktree. Suggest `/starting-session` for tracking. Nothing more.
