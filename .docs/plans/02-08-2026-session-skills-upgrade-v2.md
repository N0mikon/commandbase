---
date: 2026-02-08
status: draft
topic: "session-skills-upgrade-v2"
tags: [plan, implementation, session-skills, skills, hooks, python, concurrency, refactor, git-worktrees, branching]
git_commit: d8efed8
references:
  - plugins/commandbase-session/skills/naming-session/SKILL.md
  - plugins/commandbase-session/skills/handing-over/SKILL.md
  - plugins/commandbase-session/skills/taking-over/SKILL.md
  - plugins/commandbase-session/skills/resuming-sessions/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-session/scripts/track-errors.py
  - plugins/commandbase-session/scripts/harvest-errors.py
  - plugins/commandbase-session/scripts/trigger-learning.py
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - .docs/research/02-08-2026-analysis-session-skills-upgrade-context.md
---

# Session Skills Upgrade v2

## Overview

Consolidate 5 session skills into 3, integrate git branching and worktrees as first-class session infrastructure, extract shared Python utilities into a module, add a SessionStart hook bridge for reliable session ID discovery, fix concurrency and atomicity issues, and add session status tracking.

Each session now creates a dedicated git branch and worktree, giving every session its own isolated workspace directory. Starting a session = creating a branch + worktree. Ending a session = squash merging to main + removing the worktree. Resuming = navigating to the worktree directory.

Projects are migrated on first use to the "bare repo" pattern where main/master and all session branches are peer worktree directories under a shared container.

**Source research**: `.docs/research/02-08-2026-analysis-session-skills-upgrade-context.md`

## Scope

### In Scope
- Consolidate `/naming-session` -> `/starting-session`
- Consolidate `/handing-over` -> `/ending-session` (absorbs handoff creation + learning check)
- Merge `/resuming-sessions` + `/taking-over` -> `/resuming-session` (smart auto-detect)
- **Git branch creation on session start** (feature/, fix/, refactor/ prefixes)
- **Git worktree creation** for each session (isolated directory per branch)
- **Bare repo migration** (one-time per project, triggered by first `/starting-session`)
- **Squash merge to main** on session end
- **Conflict detection** before merge (dry run, ask user if conflicts)
- Extract `session_utils.py` shared module from 3 duplicated Python scripts
- Add `detect-session.py` SessionStart hook for session_id bridging
- Add `status` field to session-map.json entries ("active" | "ended" | "handed-off")
- Deprecate `_current` file (keep as legacy read-only fallback)
- Implement atomic writes via `os.replace()` for session-map.json
- Update `/bookmarking-code` to work with new session infrastructure
- Update plugin.json manifest and hooks.json
- Update CLAUDE.md references

### Out of Scope (Not Doing)
- MCP-based session state server (no evidence it's needed)
- Native `/rename` bridge (wait for native maturity)
- Auto Session Memory integration (native handles this)
- File locking (`fcntl`/`msvcrt`) -- atomic `os.replace()` is sufficient
- Auto-learning hook (Windsurf-style) -- current explicit extraction is preferred
- MINGW test matrix (important but separate effort)
- CI/CD pipeline (not needed for personal tooling repo)

## Architecture Decisions

### AD-1: Three Skills, Not Subcommands
**Decision**: Separate skills (`/starting-session`, `/ending-session`, `/resuming-session`) rather than a single `/session start|end|resume` skill with subcommands.
**Rationale**: Separate skills control context window size -- each skill only loads its own SKILL.md body when triggered. A combined skill would load all session logic for every invocation. (Research doc: "User Design Decisions" section)

### AD-2: Session = Branch = Worktree
**Decision**: Every session creates a git branch and a git worktree. The session name, branch name, and worktree directory name are all linked. Sessions are not optional metadata -- they are isolated workspaces.
**Rationale**: Git branches provide code isolation. Worktrees provide directory isolation. Together they eliminate the concurrency problem entirely -- each terminal works in its own directory on its own branch. No `_current` singleton fights, no session-map.json races. The research doc identified "Git State Is Foundational to Session Integrity" as a shared finding across 3 documents.

### AD-3: Bare Repo Pattern
**Decision**: Projects using sessions are migrated to the bare repo + worktrees directory structure:
```
/c/code/projectname/           <- container (not a working directory)
  .bare/                       <- git internals
  session-map.json             <- shared session registry
  main/                        <- worktree for main/master
  feature/auth-mvp/            <- worktree for session
  fix/login-timeout/           <- worktree for another session
```
**Rationale**: Git worktrees cannot live inside the main working tree. The bare repo pattern puts all branches as peer directories under a shared container. No branch is "special." The user's daily path changes from `/c/code/project` to `/c/code/project/main`, but all session worktrees are clean peers. One-time migration per project, triggered automatically by `/starting-session`.

### AD-4: Branch Naming Convention
**Decision**: Branch names use a type prefix matching the work type:
- `feature/<session-name>` -- new functionality (default)
- `fix/<session-name>` -- bug fixes
- `refactor/<session-name>` -- restructuring

The skill auto-suggests a prefix based on session description context and the user confirms.
**Rationale**: Type prefixes are industry standard practice. They make branch lists scannable and communicate intent. The prefix is suggested, not forced -- user always confirms.

### AD-5: Squash Merge on Session End
**Decision**: `/ending-session` squash merges the session branch into main, producing a single clean commit on main that summarizes the session's work.
**Rationale**: Squash merge keeps main history clean -- one commit per session rather than every intermediate commit. The full commit history is preserved in git reflog and in session state files (checkpoints.log) if needed. For a solo developer, clean main history is more valuable than preserving every work-in-progress commit.

### AD-6: Conflict Detection Before Merge
**Decision**: Before squash merging, `/ending-session` performs a dry-run merge check. If conflicts exist, it aborts, returns to the session branch, and presents the conflicts to the user.
**Rationale**: Merging should never surprise the user with conflicts mid-operation. The dry run is cheap, and presenting conflicts explicitly lets the user decide how to resolve them before any state changes.

### AD-7: Deprecate `_current`, Don't Delete
**Decision**: Stop writing to `_current` in new code. Keep reading it as the last fallback in `resolve_session()`.
**Rationale**: Existing session folders created before the upgrade have `_current` but may lack session-map.json entries. Removing the read fallback would break backward compatibility for active sessions during migration.

### AD-8: SessionStart Hook Bridge via stderr (exit 2)
**Decision**: A new `detect-session.py` hook on SessionStart that emits the native `session_id` to stderr and exits with code 2, injecting it into Claude's conversation context.
**Rationale**: Skills have no reliable way to identify which Claude Code terminal instance they're running in. Exit code 2 sends stderr content to Claude as a feedback message, making session_id available in conversation context for skills to read. (Research doc: "Session ID Discovery Gap" and "Potential Concurrency Solutions" sections)

### AD-9: Smart Resume with Auto-Detection
**Decision**: `/resuming-session` auto-detects whether to use session state files or handoff documents based on available inputs.
**Rationale**: The research shows every competitor has ONE resume mechanism. Two paths (`/resuming-sessions` vs `/taking-over`) create user confusion. The merged skill uses worktree presence as the primary indicator. (Research doc: "The Two Resume Paths Need Merging" section)

### AD-10: Session Status for Lifecycle Tracking
**Decision**: Add a `status` field to session-map.json entries with values: "active", "ended", "handed-off".
**Rationale**: Enables smart resume decisions (skip ended sessions, highlight handed-off ones), prevents re-ending already-ended sessions. Lazy migration: entries without `status` are treated as "active" and upgraded on next write. (Research doc: "Potential Concurrency Solutions" section, item 6)
**Growth**: Ended entries accumulate over time. This is acceptable for personal tooling (dozens of sessions, not thousands). If it ever becomes a problem, a future cleanup could prune entries older than N days with status "ended".

### AD-11: Atomic Writes via os.replace()
**Decision**: All session-map.json writes use write-to-temp-then-`os.replace()` pattern.
**Rationale**: Python's `os.replace()` is atomic on both POSIX and Windows NTFS. Temp file + atomic rename eliminates the truncation window. (Research doc: "File Operation Safety Matrix" section)

### AD-12: Container-Level session-map.json
**Decision**: In the bare repo pattern, session-map.json lives at the container level (alongside `.bare/` and worktree directories), not inside any individual worktree.
**Rationale**: session-map.json is a shared registry across all sessions. Each worktree represents one session -- putting the registry inside a worktree would make it invisible to other worktrees. Container-level placement makes it accessible from any worktree by navigating to the parent directory. For non-migrated (regular) repos, session-map.json stays at `.claude/sessions/session-map.json` for backward compatibility.

## Container Layout

After bare repo migration, a project looks like this:

```
/c/code/commandbase/                  <- container directory
  .bare/                              <- git object store + refs
  session-map.json                    <- shared session registry (outside git)
  main/                               <- worktree: main branch
    .gitignore                         <- includes .claude/sessions/ (runtime state)
    .claude/sessions/                  <- per-session state (gitignored, not tracked)
    plugins/
    CLAUDE.md
    ...
  feature/auth-mvp/                   <- worktree: session branch
    .claude/sessions/auth-mvp/         <- gitignored session runtime state
      meta.json
      errors.log
      checkpoints.log
    plugins/
    ...
  fix/login-timeout/                  <- worktree: another session
    .claude/sessions/login-timeout/    <- gitignored session runtime state
      meta.json
      errors.log
      checkpoints.log
    ...
```

**Key locations:**
- `session-map.json`: container-level, outside any worktree (not tracked by git)
- `.claude/sessions/{name}/`: per-worktree, gitignored session runtime state (errors, checkpoints). Never committed, deleted when worktree is removed.
- `.bare/`: git internals (objects, refs, config)
- `.docs/`: tracked in git, lives in each worktree. Drafts created during a session stay on the session branch until squash merge brings them to main -- this is intentional isolation.
- Each worktree: full working copy of the repo at that branch

**session-map.json format** (updated with worktree + branch fields):
```json
{
  "<session_id>": {
    "name": "auth-mvp",
    "branch": "feature/auth-mvp",
    "worktree": "/c/code/commandbase/feature/auth-mvp",
    "created": "2026-02-08T12:00:00.000Z",
    "status": "active"
  }
}
```

## Phase 0: Migrate commandbase to Bare Repo (Offline, Manual)

**Goal**: Migrate the commandbase repo itself to the bare repo pattern before starting implementation. This must be done outside Claude Code since the migration moves the `.git` directory.

**Prerequisites**: Close all Claude Code sessions in commandbase. Commit or stash any uncommitted work.

### Commands (run from Git Bash, outside Claude Code)

```bash
cd /c/code

# Verify clean state
git -C commandbase status --porcelain
# If dirty: commit or stash first

# Detect default branch
DEFAULT_BRANCH=$(git -C commandbase symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
[ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH=$(git -C commandbase branch --list main master | head -1 | tr -d ' *')
echo "Default branch: $DEFAULT_BRANCH"

# Move repo to become container
mv commandbase commandbase-migrating
mkdir commandbase
mv commandbase-migrating/.git commandbase/.bare

# Configure as bare repo
git -C commandbase/.bare config core.bare true

# Create main worktree (checks out all tracked files automatically)
git -C commandbase/.bare worktree add ../main $DEFAULT_BRANCH

# Copy untracked/ignored files that worktree add didn't check out
cp -r commandbase-migrating/.claude commandbase/main/.claude 2>/dev/null
cp -r commandbase-migrating/.docs commandbase/main/.docs 2>/dev/null

# Clean up old directory
rm -rf commandbase-migrating

# Create container-level session-map.json
echo '{}' > commandbase/session-map.json

# Add .claude/sessions/ to .gitignore (session runtime state)
echo '.claude/sessions/' >> commandbase/main/.gitignore

# Verify
cd commandbase/main
git status
git log --oneline -3
ls -la
```

### Verification Checklist

After running the commands, verify before opening Claude Code:
- [ ] `/c/code/commandbase/.bare/` exists and contains git internals
- [ ] `/c/code/commandbase/main/` exists with all project files
- [ ] `/c/code/commandbase/session-map.json` exists (contains `{}`)
- [ ] `git status` from `commandbase/main/` works correctly
- [ ] `git log` shows the expected commit history
- [ ] `.claude/sessions/` listed in `.gitignore`
- [ ] CLAUDE.md, plugins/, .docs/ all present in `main/`

### After Migration

Open Claude Code in `/c/code/commandbase/main/` (not `/c/code/commandbase/`). This is your new daily working directory for the main branch.

**CLAUDE.md path update**: After migration, update the directory structure section in CLAUDE.md to note the bare repo layout. This will be done properly in Phase 8, but you may want to add a temporary note so Claude Code understands the new layout.

## Phase 1: Create `session_utils.py` Shared Module

**Goal**: Extract duplicated code from 3 Python hook scripts into a shared module, eliminating 3x copy-paste of `normalize_path()` and `_resolve_session()`, and adding atomic write, git, and worktree utility support.

### Files to Create
- `plugins/commandbase-session/scripts/session_utils.py`

### Implementation Details

**`session_utils.py` must contain:**

**Path utilities:**
1. `normalize_path(path)` -- MINGW `/c/...` -> `C:\...` conversion via `cygpath -w`
   - Source: `track-errors.py:13-25` (identical in all 3 scripts)

**Repo layout detection:**
2. `detect_repo_layout(cwd)` -- Returns `"bare-worktree"` or `"regular"`
   - Check if `cwd` is inside a worktree: compare `git rev-parse --git-common-dir` vs `git rev-parse --git-dir`
   - If they differ: we're in a worktree -> `"bare-worktree"`
   - If same: regular repo -> `"regular"`

3. `get_container_dir(cwd)` -- Returns the container directory path
   - For bare-worktree: use `git rev-parse --git-common-dir` to find `.bare/` path directly, then container = parent of `.bare/`. This works regardless of worktree nesting depth (e.g., `feature/auth-mvp/` is two levels below container, not one).
   - For regular repo: container = repo root (same as `git rev-parse --show-toplevel`)

**Session map operations:**
4. `get_session_map_path(cwd)` -- Returns the path to session-map.json
   - For bare-worktree: `<container>/session-map.json`
   - For regular repo: `<repo-root>/.claude/sessions/session-map.json`

5. `read_session_map(cwd)` -- Read and parse session-map.json from the correct location, return dict (empty dict if missing/corrupt)

6. `update_session_map(cwd, session_id, entry)` -- Read-modify-write session-map.json with atomic write
   - Reads existing map, merges new entry, writes atomically
   - `entry` is a dict with keys: `name`, `branch`, `worktree`, `created`, `status`

7. `resolve_session(cwd, session_id)` -- Session name resolution
   - For bare-worktree: find session-map.json entry whose `worktree` field matches `cwd`
   - Fallback: lookup by `session_id` key in session-map.json
   - Legacy fallback: `_current` file read (for non-migrated repos, per AD-7)
   - Source pattern: `track-errors.py:28-53`

**Session directory operations:**
8. `get_session_dir(cwd, session_name)` -- Returns `.claude/sessions/{session_name}/` path relative to worktree root
   - Creates directory if it doesn't exist (`os.makedirs(exist_ok=True)`)

**Atomic I/O:**
9. `atomic_write_json(path, data)` -- Atomic JSON write via temp file + `os.replace()`
   - Write to `{path}.tmp` with `json.dumps(data, indent=2)`
   - `os.replace("{path}.tmp", path)` -- atomic on POSIX and NTFS (per AD-11)
   - On failure: clean up temp file

**Log utilities:**
10. `summarize_input(tool_input)` -- Extract most relevant part of tool input for logging
    - Source: `track-errors.py:93-100`

11. `summarize_response(response)` -- Truncate response for log storage (500 chars)
    - Source: `track-errors.py:103-105`

**Git/worktree operations:**
12. `create_worktree(container_dir, branch_name, worktree_name)` -- Create a git worktree
    - `git worktree add <container>/<worktree_name> -b <branch_name>`
    - Called from skill context (SKILL.md instructions), not from hooks

13. `remove_worktree(container_dir, worktree_name)` -- Remove a git worktree
    - `git worktree remove <container>/<worktree_name>`
    - Called from skill context during `/ending-session`

14. `migrate_to_bare_repo(repo_path)` -- One-time migration from regular repo to bare repo + worktrees
    - Steps documented below in Phase 3
    - Returns the new container path and main worktree path

Note: Functions 12-14 are reference implementations. Skills will execute these git commands directly via Bash tool, but the functions document the exact commands and error handling.

### Success Criteria
- [ ] `session_utils.py` exists at `plugins/commandbase-session/scripts/session_utils.py`
- [ ] All 14 functions are implemented
- [ ] `detect_repo_layout` correctly distinguishes worktree vs regular repo
- [ ] `get_container_dir` finds container for both layouts
- [ ] `get_session_map_path` returns correct path for both layouts
- [ ] `resolve_session` resolves by worktree path match first, then session_id, then `_current` fallback
- [ ] `atomic_write_json` uses `os.replace()` pattern (not direct `open("w")`)
- [ ] Module imports successfully: `python3 -c "from session_utils import resolve_session"`
- [ ] No external dependencies (stdlib only: `json`, `os`, `sys`, `subprocess`, `tempfile`, `datetime`)

## Phase 2: Add `detect-session.py` SessionStart Hook

**Goal**: Bridge Claude Code's native `session_id` into conversation context so skills can reliably identify their terminal instance. Now also reports the worktree context.

### Files to Create
- `plugins/commandbase-session/scripts/detect-session.py`

### Files to Modify
- `plugins/commandbase-session/hooks/hooks.json` -- Add SessionStart hook entry

### Implementation Details

**`detect-session.py` logic:**

1. Read stdin JSON -- extract `session_id` and `cwd`
2. Normalize `cwd` via `session_utils.normalize_path()`
3. Detect repo layout via `session_utils.detect_repo_layout()`
4. Read session-map.json via `session_utils.read_session_map()`
5. Find session matching this `cwd` (worktree match) or `session_id`
6. Emit to stderr based on findings:

   If mapped to active session:
   ```
   SESSION DETECTED: "{name}" on branch {branch} (status: {status}).
   Worktree: {worktree_path}
   Session ID: {session_id}
   ```

   If in main worktree (no session):
   ```
   MAIN BRANCH: Working in {cwd} on main. Run /starting-session to create a session branch.
   Session ID: {session_id}
   ```

   If not in bare repo pattern:
   ```
   SESSION ID: {session_id} (regular repo, no worktree layout). Run /starting-session to migrate and create a session.
   ```

7. Exit 2 to inject into Claude's context

**`hooks.json` addition:**
```json
"SessionStart": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash -c 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/detect-session.py'"
      }
    ]
  }
]
```

### Empirical Verification Required
Before completing this phase, verify:
- Does SessionStart hook event exist and reliably fire?
- Does exit code 2 from SessionStart hooks inject stderr into Claude's conversation context?
- Test with: `echo '{"session_id":"test","cwd":"/c/code/commandbase/main"}' | python3 detect-session.py`

If SessionStart + exit 2 does NOT work as expected, fallback approach: the `/starting-session` skill itself prints the session_id at the end of its output, and `/resuming-session` reads it from session-map.json. The hook becomes informational only (exit 0).

### Success Criteria
- [ ] `detect-session.py` exists and imports from `session_utils`
- [ ] Correctly detects bare-worktree vs regular repo layout
- [ ] Reports session name + branch + worktree path when mapped
- [ ] Reports "main branch" context when in main worktree
- [ ] Reports "regular repo" context when not migrated
- [ ] `hooks.json` has SessionStart entry
- [ ] Hook fires on Claude Code session start (manual test)
- [ ] Session info appears in Claude's conversation context (manual test)

## Phase 3: Create `/starting-session` Skill

**Goal**: Replace `/naming-session` with an upgraded session creation skill that creates a git branch + worktree, migrates the repo to bare repo pattern on first use, and registers the session in container-level session-map.json.

### Files to Create
- `plugins/commandbase-session/skills/starting-session/SKILL.md`

### Implementation Details

**Frontmatter:**
```yaml
---
name: starting-session
description: "Use this skill when starting a new work session, creating an isolated workspace for a feature or fix, or beginning tracked development work. This includes migrating the repo to bare-repo layout on first use, creating a git branch and worktree for the session, registering the session in session-map.json, and setting up per-session error and checkpoint tracking. Trigger phrases: '/starting-session', 'start a session', 'new session', 'create a session', 'begin work on'."
---
```

**The skill has two modes:**

#### Mode A: First-Time Migration (repo not yet bare repo pattern)

Triggered when `detect_repo_layout(cwd)` returns `"regular"`. One-time per project.

**Migration steps:**

1. Confirm with user:
   ```
   This project hasn't been set up for session-based development yet.

   I'll reorganize it so each session gets its own isolated directory:

   Before: /c/code/commandbase/          (single directory, all branches)
   After:  /c/code/commandbase/main/     (main branch)
           /c/code/commandbase/feature/  (session branches)

   Your daily path will change to /c/code/commandbase/main/

   Proceed with migration?
   ```

2. Verify clean git state:
   ```bash
   git status --porcelain
   ```
   If dirty: "You have uncommitted changes. Commit or stash them first."

3. Detect the default branch name:
   ```bash
   git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
   # Fallback: check for main or master
   git branch --list main master | head -1 | tr -d ' *'
   ```

4. Execute migration (user must run these commands since Claude is in the directory being moved):
   ```bash
   # From OUTSIDE the repo (e.g., /c/code/)
   cd /c/code

   # Move the repo to become the container
   mv commandbase commandbase-migrating
   mkdir commandbase
   mv commandbase-migrating/.git commandbase/.bare

   # Configure as bare repo
   git -C commandbase/.bare config core.bare true

   # Create main worktree from bare repo
   # (this checks out all tracked files into main/ automatically)
   git -C commandbase/.bare worktree add ../main master  # or 'main' if default branch

   # Copy only untracked/ignored files that worktree add didn't check out
   cp -r commandbase-migrating/.claude commandbase/main/.claude 2>/dev/null
   cp -r commandbase-migrating/.docs commandbase/main/.docs 2>/dev/null
   # Add any other untracked directories your project uses

   # Clean up the old directory
   rm -rf commandbase-migrating

   # Create container-level session-map.json
   echo '{}' > commandbase/session-map.json

   # Add .claude/sessions/ to .gitignore (session runtime state, not project code)
   echo '.claude/sessions/' >> commandbase/main/.gitignore
   ```

   **Important**: The skill must present these commands for the user to run, or execute them step-by-step with confirmation, because Claude Code's cwd will change during migration. The `git worktree add` command checks out all tracked files automatically -- only untracked/ignored files (`.claude/`, `.docs/`) need manual copying.

5. After migration, tell user:
   ```
   Migration complete!

   Your project is now at: /c/code/commandbase/main/
   Open a new Claude Code session in that directory to continue.

   Next time you run /starting-session, it will create a session branch directly.
   ```

#### Mode B: Create Session (repo already in bare repo pattern)

Triggered when `detect_repo_layout(cwd)` returns `"bare-worktree"` and cwd is the main worktree.

**Steps:**

1. **Find session ID**: Read from conversation context (injected by SessionStart hook from Phase 2). Fallback to sessions-index.json unmapped heuristic if hook didn't fire.

2. **Choose branch type**: Ask user:
   ```
   What type of work is this session for?
   1. feature  (new functionality)
   2. fix      (bug fix)
   3. refactor (restructuring)
   ```

3. **Name the session**: Auto-suggest from conversation summary, user confirms.
   - Validation: same kebab-case rules (3-40 chars, `^[a-z0-9-]+$`, no leading/trailing/consecutive hyphens)
   - Full branch name: `{type}/{session-name}` (e.g., `feature/auth-mvp`)

4. **Create branch + worktree**:
   ```bash
   # From container directory
   cd /c/code/commandbase
   git worktree add {type}/{session-name} -b {type}/{session-name}
   ```

5. **Create session state directory** in the new worktree:
   ```bash
   mkdir -p {type}/{session-name}/.claude/sessions/{session-name}
   ```
   Verify `.claude/sessions/` is in the worktree's `.gitignore` (should already be there from migration, but check).

6. **Write meta.json** to `{worktree}/.claude/sessions/{session-name}/meta.json`:
   ```json
   {
     "sessionId": "<uuid from hook or sessions-index>",
     "name": "<session-name>",
     "branch": "<type/session-name>",
     "worktree": "/c/code/commandbase/<type>/<session-name>",
     "created": "<ISO 8601>",
     "gitBranch": "<type/session-name>",
     "summary": "<native summary>"
   }
   ```

7. **Update container-level session-map.json** (atomic write):
   ```json
   {
     "<session_id>": {
       "name": "<session-name>",
       "branch": "<type/session-name>",
       "worktree": "/c/code/commandbase/<type>/<session-name>",
       "created": "<ISO 8601>",
       "status": "active"
     }
   }
   ```

8. **Output**:
   ```
   SESSION STARTED
   ===============
   Name: auth-mvp
   Branch: feature/auth-mvp
   Worktree: /c/code/commandbase/feature/auth-mvp

   Switch to this directory to begin work:
   cd /c/code/commandbase/feature/auth-mvp

   Open Claude Code there for a session-aware workspace.
   ```

**Iron Law**: `NO SESSION WITHOUT USER CONFIRMATION OF NAME AND BRANCH TYPE`

**Gate Function:**
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

### Success Criteria
- [ ] `starting-session/SKILL.md` exists with valid frontmatter (name matches directory)
- [ ] Description follows formula: "Use this skill when..."
- [ ] Uses gerund-form name: `starting-session`
- [ ] SKILL.md under 500 lines
- [ ] Mode A: bare repo migration documented with exact commands
- [ ] Mode A: migration adds `.claude/sessions/` to `.gitignore`
- [ ] Mode A: warns user their daily path will change
- [ ] Mode B: creates git branch with type prefix
- [ ] Mode B: creates worktree in container directory
- [ ] Mode B: writes meta.json to worktree's `.claude/sessions/`
- [ ] Mode B: updates container-level session-map.json with branch + worktree fields
- [ ] Mode B: instructs user to `cd` to new worktree

## Phase 4: Create `/ending-session` Skill

**Goal**: Create a session end skill that squash merges the session branch into main, removes the worktree, creates optional handoff documents, and marks the session as ended.

### Files to Create
- `plugins/commandbase-session/skills/ending-session/SKILL.md`

### Implementation Details

**Frontmatter:**
```yaml
---
name: ending-session
description: "Use this skill when ending a work session, merging work back to main, switching context, creating a handoff for another session, or wrapping up current work. This includes squash merging the session branch into main, removing the worktree, optionally creating handover documents to .docs/handoffs/, checking for uncaptured learnings, and updating session status. Trigger phrases: '/ending-session', 'end session', 'wrap up', 'merge and end', 'hand this off', 'finish session'."
---
```

**Three modes:**

#### Mode A: Merge End (default)

User is done with the session and wants to merge work into main.

**Steps:**

1. **Verify session context**: Confirm we're in a session worktree (not main):
   ```bash
   git rev-parse --show-toplevel  # Get worktree path
   # Check session-map.json for matching entry
   ```
   If in main: "You're on the main branch. No session to end."

2. **Check for uncommitted changes**:
   ```bash
   git status --porcelain
   ```
   If dirty: "You have uncommitted changes. Commit them first, or choose to discard."

3. **Conflict detection (dry run)**:
   ```bash
   # Navigate to main worktree
   cd /c/code/commandbase/main
   git merge --no-commit --no-ff <session-branch>
   ```

   If conflicts:
   ```bash
   git merge --abort
   ```
   Then present to user:
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

4. **Squash merge**:
   ```bash
   cd /c/code/commandbase/main
   git merge --squash <session-branch>
   ```

5. **CLAUDE.md review**: Check if CLAUDE.md was modified during the session:
   ```bash
   git diff main -- CLAUDE.md
   ```
   If it differs, show the diff and ask:
   ```
   CLAUDE.md was modified during this session:

   [diff output]

   Include these changes on main?
   1. Yes - merge CLAUDE.md changes to main
   2. No  - discard session-only CLAUDE.md changes
   ```
   If user chooses No:
   ```bash
   git checkout main -- CLAUDE.md
   ```
   This handles the case where CLAUDE.md was updated with session-specific instructions (e.g., "use adapter pattern for all new services") that shouldn't persist on main.

6. **Commit + Push via `/committing-changes`**:
   Invoke `/committing-changes` with context that this is a squash merge commit. The skill handles:
   - Diff review (shows the full session's work)
   - Sensitive file verification on staged content
   - Security review for public repos
   - Commit with session summary message (meta.json summary + key accomplishments)
   - Push to remote (handles remote divergence)

   `/committing-changes` recognizes the squash merge context: files are pre-staged by `git merge --squash`, so it skips manual staging and stale docs check. See Phase 8 for the `/committing-changes` update.

7. **Learning check**: Read `{worktree}/.claude/sessions/{name}/errors.log`. If errors exist:
   ```
   This session had N error(s). Consider running /learning-from-sessions before I remove the worktree.
   ```
   Wait for user response before proceeding.

8. **Remove worktree + branch**:
   ```bash
   cd /c/code/commandbase
   git worktree remove <type>/<session-name>
   git branch -d <type>/<session-name>
   ```

9. **Update session-map.json**: Set `status: "ended"`.

10. **Output**:
   ```
   SESSION ENDED
   =============
   Name: auth-mvp
   Branch: feature/auth-mvp (merged + deleted)
   Squash commit: abc1234 on main
   Worktree: removed

   Work merged to main. You're now in: /c/code/commandbase/main/
   ```

#### Mode B: Handoff End

User wants to pass work to another session. Branch stays open.

**Steps:**

1. Same verification as Mode A (steps 1-2)
2. **Do NOT merge** -- branch stays open for the next session
3. Create handoff document via docs-writer agent (same content template as current `/handing-over`:
   What I Was Working On, What I Accomplished, Key Learnings, Files Changed, Current State, Session Context, Next Steps, Context & References, Notes)
4. **Update session-map.json**: Set `status: "handed-off"`.
5. Learning check (same as Mode A step 7)
6. **Do NOT remove worktree** -- it stays for the next session to use
7. **Output**:
   ```
   SESSION HANDED OFF
   ==================
   Name: auth-mvp
   Branch: feature/auth-mvp (kept open)
   Worktree: /c/code/commandbase/feature/auth-mvp (kept)
   Handoff: .docs/handoffs/02-08-2026-auth-mvp-handoff.md

   To resume this work:
   /resuming-session (from the worktree directory)
   ```

#### Mode C: Discard End

User wants to abandon the session's work entirely.

**Steps:**

1. Confirm with user (destructive action):
   ```
   This will permanently discard all work on branch feature/auth-mvp.

   Are you absolutely sure? Type the session name to confirm: auth-mvp
   ```
2. Remove worktree:
   ```bash
   cd /c/code/commandbase
   git worktree remove --force <type>/<session-name>
   git branch -D <type>/<session-name>
   ```
3. Update session-map.json: Set `status: "ended"`.

**Iron Law**: `NO SESSION END WITHOUT MERGE VERIFICATION OR EXPLICIT DISCARD`

**Gate Function:**
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

### Success Criteria
- [ ] `ending-session/SKILL.md` exists with valid frontmatter
- [ ] Description follows formula, includes merge + handoff trigger phrases
- [ ] Mode A: dry-run conflict check before squash merge
- [ ] Mode A: CLAUDE.md diff review before commit (keep or discard session-only changes)
- [ ] Mode A: squash merge + commit + push via `/committing-changes`
- [ ] Mode A: removes worktree + deletes branch after merge
- [ ] Mode B: creates handoff doc, keeps branch + worktree open
- [ ] Mode B: sets status "handed-off" (not "ended")
- [ ] Mode C: requires explicit confirmation before discarding
- [ ] Learning check fires in all modes (before worktree removal)
- [ ] Updates session-map.json status in all modes
- [ ] SKILL.md under 500 lines

## Phase 5: Create `/resuming-session` Skill

**Goal**: Merge `/resuming-sessions` and `/taking-over` into a single smart-resume skill that auto-detects the best resume approach based on worktree presence, session status, and handoff documents.

### Files to Create
- `plugins/commandbase-session/skills/resuming-session/SKILL.md`

### Implementation Details

**Frontmatter:**
```yaml
---
name: resuming-session
description: "Use this skill when resuming a previous session after restarting Claude Code, picking up work from a handover document, continuing where you or another session left off, or switching to an existing session worktree. This includes navigating to session worktrees, reading session state files (meta.json, errors.log, checkpoints.log), reading handover documents from .docs/handoffs/, auto-detecting the best resume source, and verifying git state. Trigger phrases: '/resuming-session', 'resume session', 'continue session', 'pick up where I left off', 'take over', 'switch to session'."
---
```

**Smart auto-detection logic:**

```
1. If a file path argument was provided:
   -> If it points to .docs/handoffs/ -> Handoff Mode (Mode B)
   -> Otherwise -> try reading it as a handoff document

2. If no argument provided:
   a. Detect repo layout
   b. If bare-worktree: read container-level session-map.json
   c. List sessions by status:
      - "active" sessions with existing worktrees -> State Resume (Mode A)
      - "handed-off" sessions with existing worktrees -> Handoff Resume (Mode B)
      - "ended" sessions (worktree removed) -> show as completed, not resumable
   d. If no sessions but .docs/handoffs/ has documents -> Handoff Resume (Mode B)
   e. If nothing -> "No sessions or handoffs found" with guidance
```

**Three modes:**

#### Mode A: Worktree Resume (was `/resuming-sessions`)
- Session has an existing worktree (status "active")
- User just needs to navigate there and restore context

**Steps:**
1. Read session-map.json, find active sessions with existing worktrees
2. If multiple: present picker with session names, branches, and last modified dates
3. Read meta.json, errors.log, checkpoints.log from the selected session's worktree
4. Scan `.docs/handoffs/` and `.docs/learnings/` for related context (in the worktree)
5. Staleness auto-update for found docs (>3 commits behind -> docs-updater)
6. Present session summary:
   ```
   SESSION READY TO RESUME
   =======================
   Name: auth-mvp
   Branch: feature/auth-mvp
   Worktree: /c/code/commandbase/feature/auth-mvp

   Errors: 2 logged
   Checkpoints: phase-1-done (abc1234)

   Switch to this directory to continue:
   cd /c/code/commandbase/feature/auth-mvp
   ```

#### Mode B: Handoff Resume (was `/taking-over`)
- Session was handed off (status "handed-off") or a handoff document was provided
- Worktree may or may not still exist

**Steps:**
1. Read the handoff document fully
2. Staleness auto-update for handoff and linked docs
3. Absorb context (tasks, accomplishments, learnings, next steps)
4. Check if the session's worktree still exists:
   - If yes: "The worktree is still at {path}. Switch there to continue."
   - If no: "The worktree was removed. Run /starting-session to create a new one, or I can create a new session on the same branch."
5. Verify git state matches handoff
6. Present takeover summary, get confirmation
7. If worktree exists: direct user to `cd` there
8. If no worktree: offer to run `/starting-session`

#### Mode C: Session Picker (multiple candidates)
- When multiple resume candidates exist (active + handed-off sessions)
- Present a unified picker:
  ```
  Available sessions:
  1. [active]     auth-mvp        feature/auth-mvp       /c/code/.../feature/auth-mvp
  2. [handed-off] session-v2      refactor/session-v2    /c/code/.../refactor/session-v2
  3. [handoff]    .docs/handoffs/02-08-2026-deploy-fix.md

  Which would you like to resume?
  ```
- Route to Mode A or B based on selection

**Staleness detection** (shared subsection, not duplicated per mode):
```bash
f="<doc-path>"
commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
  git rev-parse "$commit" >/dev/null 2>&1 && \
  behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
  [ -n "$behind" ] && [ "$behind" -gt 3 ] && echo "$behind"
fi
```
- If >3 commits behind: spawn docs-updater agent to refresh before presenting
- If docs-updater archives it: note it was archived
- If current: include normally

**Iron Law**: `NO RESUME WITHOUT READING SOURCE FILES`

**Gate Function:**
```
BEFORE resuming any session:

1. DETECT: What resume candidates exist? (worktrees, handoffs, both)
2. SELECT: If multiple candidates, present picker
3. READ: Load all session state files or handoff document
4. VERIFY: Does git state match expectations?
5. PRESENT: Show context summary
6. DIRECT: Tell user which directory to work in
7. ONLY THEN: User begins work

Skip reading = guessing instead of knowing
```

### Success Criteria
- [ ] `resuming-session/SKILL.md` exists with valid frontmatter
- [ ] Description covers resume, takeover, and switch-to-session trigger phrases
- [ ] Auto-detection logic documented in Gate Function
- [ ] Mode A: reads worktree state files, directs user to worktree directory
- [ ] Mode B: reads handoff doc, checks worktree existence, offers recovery
- [ ] Mode C: unified picker for multiple candidates
- [ ] Staleness detection is a single shared section, not duplicated
- [ ] Session status awareness: "active" vs "handed-off" affects mode selection
- [ ] SKILL.md under 500 lines (use reference files if needed)

## Phase 6: Refactor Hook Scripts to Use `session_utils.py`

**Goal**: Refactor all 3 existing Python hook scripts to import from `session_utils.py` instead of duplicating code. Update `resolve_session` to use worktree-aware resolution.

### Files to Modify
- `plugins/commandbase-session/scripts/track-errors.py`
- `plugins/commandbase-session/scripts/harvest-errors.py`
- `plugins/commandbase-session/scripts/trigger-learning.py`

### Implementation Details

**Step 0: Disable hooks before refactoring**

The hooks being refactored are actively running in the current Claude Code session. Modifying them while live risks broken error tracking mid-session. Disable first:
```bash
mv plugins/commandbase-session/hooks/hooks.json plugins/commandbase-session/hooks/hooks.json.bak
```
Claude Code will no longer fire the session hooks. Proceed with refactoring. Re-enable in the final step after verification.

**For each script:**
1. Add `sys.path` insertion at top to find `session_utils.py`:
   ```python
   import sys, os
   sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
   ```
2. Replace inline `normalize_path()` with `from session_utils import normalize_path`
3. Replace inline `_resolve_session()` with `from session_utils import resolve_session`
4. Replace inline `_summarize_input()` and `_summarize_response()` with imports
5. In `track-errors.py`: use `get_session_dir()` from utils instead of manual path construction (line 80-81)
6. In `harvest-errors.py`: Replace `open("w")` rewrite pattern with atomic write for backfill operations

**harvest-errors.py specific changes:**
- The backfill rewrite (currently `open("w")` at line ~286-293) must use write-to-temp + `os.replace()` to prevent the race condition documented in the research: "harvest-errors rewrite races with track-errors append"
- For append operations (new errors only), `open("a")` is acceptable

**Worktree-aware behavior:**
- `resolve_session` now uses the updated function from `session_utils.py` which checks worktree path match first
- Hooks receive `cwd` as the worktree directory (e.g., `/c/code/commandbase/feature/auth-mvp`)
- The updated `resolve_session` finds the container, reads container-level session-map.json, and matches by worktree path
- Fallback chain: worktree match -> session_id match -> `_current` file -> empty string

**Step Final: Re-enable hooks after verification**

After all scripts pass manual testing:
```bash
mv plugins/commandbase-session/hooks/hooks.json.bak plugins/commandbase-session/hooks/hooks.json
```
Hooks resume firing with the refactored scripts. If a script fails after re-enabling, the hook exits non-zero and Claude Code shows the error -- fix immediately or re-disable.

### Success Criteria
- [ ] Hooks disabled before any script modifications
- [ ] All 3 scripts import from `session_utils` instead of inline functions
- [ ] No duplicate `normalize_path()` in any script
- [ ] No duplicate `_resolve_session()` (now `resolve_session()`) in any script
- [ ] `resolve_session` uses worktree-aware resolution from session_utils
- [ ] `harvest-errors.py` backfill uses atomic write pattern
- [ ] All 3 scripts still function correctly (manual test: run each with sample stdin JSON)
- [ ] `detect-session.py` (from Phase 2) also imports from `session_utils`
- [ ] Hooks re-enabled after verification

## Phase 7: Update `/bookmarking-code`

**Goal**: Update the bookmarking-code skill to work with the new session infrastructure (worktree-aware, session-map.json with status).

### Files to Modify
- `plugins/commandbase-core/skills/bookmarking-code/SKILL.md`

### Implementation Details

**Changes needed:**

1. **Session discovery**: Update from checking `_current` existence to checking session-map.json for active sessions matching the current worktree.
   - Current (line 29): `Check if .claude/sessions/_current exists`
   - New: `Check container-level session-map.json for entry matching current worktree. Fall back to _current if not in bare repo layout.`

2. **Session awareness section** (lines 26-36): Update to describe worktree-based session detection.

3. **Gate Function** (line 44): Update step 2 from `Check .claude/sessions/_current` to `Detect repo layout, find session for current worktree`

4. **Checkpoint log location** references: Keep the same `.claude/sessions/{name}/checkpoints.log` paths -- the worktree root contains `.claude/sessions/` so paths are relative to worktree, which works for both layouts.

5. **Workflow integration** (line 248-262): Update `/naming-session` reference to `/starting-session`.

6. **No structural changes** to the checkpoint format, operations, or storage. This is a surgical edit to session discovery only.

### Success Criteria
- [ ] Session discovery uses worktree-aware detection, `_current` as fallback
- [ ] All references to `/naming-session` updated to `/starting-session`
- [ ] Gate Function updated
- [ ] Session Awareness section updated
- [ ] Checkpoint operations unchanged (create, verify, list, clear)
- [ ] Works in both bare-worktree and regular repo layouts
- [ ] SKILL.md under 500 lines

## Phase 8: Update Plugin Manifests, Hooks, CLAUDE.md, and `/committing-changes`

**Goal**: Wire everything together -- update plugin.json, hooks.json, project CLAUDE.md, and add squash merge awareness to `/committing-changes`.

### Files to Modify
- `plugins/commandbase-session/.claude-plugin/plugin.json` -- bump version, update description
- `plugins/commandbase-session/hooks/hooks.json` -- add SessionStart hook (if not done in Phase 2)
- `CLAUDE.md` -- update skill references, directory structure, and document the bare repo pattern
- `plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md` -- add squash merge context handling

### Implementation Details

**plugin.json:**
```json
{
  "name": "commandbase-session",
  "version": "2.0.0",
  "description": "Session continuity with git branching -- start, end, resume sessions as isolated worktrees. Includes error tracking and learning extraction. Requires commandbase-core for docs agents."
}
```

**CLAUDE.md updates:**
- Update directory structure section: `commandbase-session` now has `3 skills + 4 hooks`
- List the 4 hooks: PostToolUseFailure, Stop, PreCompact, SessionStart
- Update skill names: `/naming-session` -> `/starting-session`, `/handing-over` -> `/ending-session`, `/resuming-sessions` + `/taking-over` -> `/resuming-session`
- Add section documenting the bare repo pattern and container layout
- Note that `/starting-session` handles first-time migration

**`/committing-changes` update -- Squash Merge Context:**

Add a "Squash Merge Context" section (after Edge Case Handling) that adapts the workflow when invoked by `/ending-session` after `git merge --squash`:

1. **Skip stale docs check** (Step 2) -- the session's docs are the new content being committed; staleness doesn't apply
2. **Skip manual staging** (Step 4) -- files are pre-staged by `git merge --squash`. The skill should detect this state (`git diff --cached` shows content, `git diff` is empty) and confirm: "Squash merge detected. Files are pre-staged. Reviewing staged changes."
3. **Diff review still applies** (Step 3) -- use `git diff --cached` to show what's being committed. This is the session's entire body of work.
4. **Sensitive file verification still applies** (Step 5) -- scan staged files for .env, credentials, keys
5. **Security review still applies** (Step 6) -- run `/reviewing-security` on staged files for public repos
6. **Commit message** (Step 7) -- should summarize the session's work (e.g., "Add JWT authentication with login/logout endpoints"). `/ending-session` provides the session summary context.
7. **Push still applies** (Step 8) -- push to remote, handle divergence

Detection: the skill can recognize the squash merge context when `git diff --cached` has content and `MERGE_MSG` exists in `.git/` (git creates this file during `--squash`).

### Success Criteria
- [ ] plugin.json version bumped to 2.0.0
- [ ] plugin.json description mentions git branching and worktrees
- [ ] hooks.json has all 4 hook entries (PostToolUseFailure, Stop, PreCompact, SessionStart)
- [ ] CLAUDE.md references updated -- no old skill names remain
- [ ] CLAUDE.md documents bare repo container layout
- [ ] `/committing-changes` handles squash merge context (skip staging, skip stale docs, review cached diff)
- [ ] `/committing-changes` detects pre-staged state via `git diff --cached` + `MERGE_MSG` presence

## Phase 9: Remove Old Skills

**Goal**: Delete the 4 replaced skill directories.

### Files to Delete
- `plugins/commandbase-session/skills/naming-session/` (entire directory)
- `plugins/commandbase-session/skills/handing-over/` (entire directory)
- `plugins/commandbase-session/skills/taking-over/` (entire directory)
- `plugins/commandbase-session/skills/resuming-sessions/` (entire directory)

### Important: Keep `/learning-from-sessions`
`/learning-from-sessions` is NOT being merged into `/ending-session`. The ending-session skill only does a learning CHECK (reminds user to run it). The full learning extraction workflow stays as its own skill because:
- It has its own complex workflow with 6 steps, quality gates, and dedup checks
- It can be invoked mid-session (not just at end)
- It has 4 reference files and 2 template files that would bloat ending-session

### `/learning-from-sessions` Update
Update session discovery in `/learning-from-sessions` to use worktree-aware detection:
- Replace `_current` check with session-map.json worktree match
- Keep fallback to `_current` for backward compat
- Update references to `/naming-session` -> `/starting-session`

### Migration Notes
- Old session folders in `.claude/sessions/` remain intact -- they're just data directories
- session-map.json entries without `status` field are treated as "active" (lazy migration)
- `_current` file may still exist from old sessions -- new skills read it as fallback but don't write it
- Users who have installed the plugin need to reinstall to pick up new skills
- Projects not yet migrated to bare repo pattern continue working with regular repo layout until first `/starting-session`

### Success Criteria
- [ ] `naming-session/` directory deleted
- [ ] `handing-over/` directory deleted
- [ ] `taking-over/` directory deleted
- [ ] `resuming-sessions/` directory deleted
- [ ] `learning-from-sessions/` directory STILL EXISTS (not deleted)
- [ ] `learning-from-sessions` session discovery updated to worktree-aware
- [ ] No broken references to deleted skills in remaining files

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Bare repo migration fails mid-way | Medium | High | Migration verifies clean git state first; each step is reversible; user confirms before starting |
| Merge conflicts on session end | Medium | Medium | Dry-run conflict check before any merge; abort and present conflicts if found |
| SessionStart hook doesn't inject into context | Medium | Medium | Fallback: skills read session-map.json directly; hook becomes informational only |
| `os.replace()` behaves differently on MINGW | Low | Medium | Test empirically; fallback to direct write with warning |
| Users confused by path change (repo root -> main/) | Medium | Low | Clear messaging during migration; session start reminds about paths |
| Worktree operations fail on Windows | Low | High | Git worktrees are well-supported on Windows; test core operations during Phase 1 |
| Users confused by skill name changes | Medium | Low | CLAUDE.md documents new names; old trigger phrases included in new descriptions |
| Concurrent terminals still race on session-map.json | Low | Medium | Each terminal is in its own worktree; atomic `os.replace()` for writes |
| `/learning-from-sessions` breaks without session context | Low | Medium | Already handles no-session case gracefully (line 58-61) |
| Remote main diverges during session | Medium | Low | `/committing-changes` handles push + remote divergence during squash merge commit |
| Large repos slow to create worktrees | Low | Low | Git worktrees are lightweight (shared objects); only working tree files are copied |

## Verification Plan

After all phases complete, verify end-to-end:

1. **Migration**: Run `/starting-session` on a regular repo -> migrates to bare repo pattern, creates `main/` worktree, `session-map.json` at container level
2. **Session start**: Run `/starting-session` from `main/` worktree -> creates branch `feature/test-session`, creates worktree at `feature/test-session/`, registers in session-map.json
3. **Worktree isolation**: Verify `main/` and `feature/test-session/` have independent file states
4. **Error tracking**: In session worktree, trigger a tool failure -> `track-errors.py` resolves session from container session-map.json via worktree path match, appends to worktree's errors.log
5. **Checkpoint**: Run `/bookmarking-code create "test"` in session worktree -> checkpoint written to worktree's session folder
6. **Merge end**: Run `/ending-session` (Merge End) -> conflict dry-run passes, CLAUDE.md review offered, squash merge staged, `/committing-changes` handles commit + push, removes worktree + branch, updates session-map.json status
7. **CLAUDE.md isolation**: Modify CLAUDE.md during session, choose "No" at merge review -> CLAUDE.md changes excluded from squash commit on main
8. **Handoff end**: Start new session, run `/ending-session` (Handoff End) -> creates handoff doc, keeps branch + worktree, sets status "handed-off"
9. **Smart resume (worktree)**: Run `/resuming-session` -> finds active session worktree, presents state summary, directs user to worktree
10. **Smart resume (handoff)**: Run `/resuming-session .docs/handoffs/...` -> reads handoff doc, finds existing worktree, directs user there
11. **Conflict detection**: Make conflicting changes in main and session branch -> `/ending-session` detects conflicts, aborts, presents them
12. **Concurrent**: Open two terminals in different worktrees -> verify both sessions tracked independently in session-map.json
13. **Learning**: Run `/learning-from-sessions` in session worktree -> still works with new session infrastructure

## Dependencies

```
Phase 0 (migrate commandbase) -- OFFLINE, before opening Claude Code
  |
  v
Phase 1 (session_utils.py) -- first Claude Code phase, from commandbase/main/
  |
  |-> Phase 2 (detect-session.py) -- depends on session_utils
  |
  |-> Phase 6 (refactor hooks) -- depends on session_utils, disable hooks first
  |
  v
Phase 3 (starting-session) -- depends on session_utils for migration + worktree ops
Phase 4 (ending-session)   -- independent of Phase 3 (can be written in parallel)
Phase 5 (resuming-session) -- independent of Phase 3/4 (can be written in parallel)
  |
  v
Phase 7 (bookmarking-code) -- depends on new session infrastructure patterns
  |
  v
Phase 8 (manifests + CLAUDE.md + /committing-changes) -- depends on all skills existing
  |
  v
Phase 9 (remove old skills) -- depends on all new skills being verified
```

Phase 0 is done manually offline (close Claude Code, run migration, reopen in commandbase/main/).
Phases 1-6 are done in Claude Code from the main worktree.
Phases 3, 4, 5, and 6 can all be done in parallel after Phase 1.
Phase 2 can be done in parallel with Phases 3-6.
Phases 7-9 are sequential after all skills are created.
