---
name: starting-session
description: "Use this skill when starting a new work session, creating an isolated workspace for a feature or fix, or beginning tracked development work. This includes migrating the repo to bare-repo layout on first use, creating a git branch and worktree for the session, registering the session in session-map.json, and setting up per-session error and checkpoint tracking. Trigger phrases: '/starting-session', 'start a session', 'new session', 'create a session', 'begin work on'."
---

# Starting Session

You are creating an isolated session workspace with its own git branch and worktree.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SESSION WITHOUT USER CONFIRMATION OF NAME AND BRANCH TYPE
```

Never create a branch or worktree without explicit user approval of the session name and branch type prefix.

**No exceptions:**
- Don't auto-create sessions silently
- Don't skip the branch type selection
- Don't bypass name validation
- Don't proceed without confirming the migration in Mode A

## The Gate Function

```
BEFORE creating any session:

1. DETECT: Is repo migrated? If not -> Mode A (migration)
2. CHECK: Are we in the main worktree? If not -> warn (already in a session)
3. SESSION_ID: Read from conversation context or sessions-index.json
4. TYPE: Ask user for branch type (feature/fix/refactor)
5. NAME: Suggest name, get user confirmation
6. VALIDATE: Name passes kebab-case rules
7. ONLY THEN: Create branch + worktree + session state

Skip confirmation = session without consent
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
To start a new session, switch to the main worktree first:
cd {container}/main
```

## Mode A: First-Time Migration

Triggered when the repo is NOT in bare-worktree layout. One-time per project.

### Step 1: Confirm with user

```
This project hasn't been set up for session-based development yet.

I'll reorganize it so each session gets its own isolated directory:

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

Next time you run /starting-session, it will create a session branch directly.
```

## Mode B: Create Session

Triggered when the repo is already in bare-worktree layout and we're in the main worktree.

### Step 1: Find session ID

Read from conversation context (injected by SessionStart hook). If not available, note that session_id will be generated.

### Step 2: Choose branch type

Ask the user:

```
What type of work is this session for?
1. feature  (new functionality) -- default
2. fix      (bug fix)
3. refactor (restructuring)
```

### Step 3: Name the session

Auto-suggest a name based on conversation context. User confirms.

**Validation rules (kebab-case):**
- 3-40 characters
- Pattern: `^[a-z0-9][a-z0-9-]*[a-z0-9]$`
- No leading/trailing/consecutive hyphens
- Examples: `auth-mvp`, `login-timeout-fix`, `session-v2`

Full branch name: `{type}/{session-name}` (e.g., `feature/auth-mvp`)

### Step 4: Create branch + worktree

Determine container directory:
```bash
container=$(git rev-parse --git-common-dir | xargs dirname)
```

Create the worktree:
```bash
cd $container
git worktree add {type}/{session-name} -b {type}/{session-name}
```

### Step 5: Create session state directory

```bash
mkdir -p {container}/{type}/{session-name}/.claude/sessions/{session-name}
```

Verify `.claude/sessions/` is in the worktree's `.gitignore`.

### Step 6: Write meta.json

Write to `{worktree}/.claude/sessions/{session-name}/meta.json`:

```json
{
  "sessionId": "<session_id from hook or generated>",
  "name": "<session-name>",
  "branch": "<type/session-name>",
  "worktree": "/c/code/{project}/{type}/{session-name}",
  "created": "<ISO 8601>",
  "gitBranch": "<type/session-name>"
}
```

### Step 7: Update session-map.json

Update the container-level `session-map.json` atomically:

```python
# Via session_utils.update_session_map()
{
  "<session_id>": {
    "name": "<session-name>",
    "branch": "<type/session-name>",
    "worktree": "/c/code/{project}/{type}/{session-name}",
    "created": "<ISO 8601>",
    "status": "active"
  }
}
```

Use the `session_utils.py` functions from `plugins/commandbase-session/scripts/` for atomic write operations. Run via:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_utils.py  # (import and call)
```

Or construct the JSON manually and write via Bash with a temp file + `mv` pattern.

### Step 8: Output

```
SESSION STARTED
===============
Name: {session-name}
Branch: {type}/{session-name}
Worktree: /c/code/{project}/{type}/{session-name}

Switch to this directory to begin work:
cd /c/code/{project}/{type}/{session-name}

Open Claude Code there for a session-aware workspace.
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
