---
name: resuming-session
description: "Use this skill when resuming a previous session after restarting Claude Code, picking up work from a handover document, continuing where you or another session left off, or switching to an existing session worktree. This includes navigating to session worktrees, reading session state files (meta.json, errors.log, checkpoints.log), reading handover documents from .docs/handoffs/, auto-detecting the best resume source, and verifying git state. Trigger phrases: '/resuming-session', 'resume session', 'continue session', 'pick up where I left off', 'take over', 'switch to session'."
---

# Resuming Session

You are restoring session context by auto-detecting the best resume source -- worktree state files, handoff documents, or both. Your job is to read all available state, verify it against reality, and present a full context summary so the user can continue where they left off.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO RESUME WITHOUT READING SOURCE FILES
```

You must read actual session state or handoff documents before presenting any summary. Never guess, summarize from memory, or skip verification.

**No exceptions:**
- Don't assume you know what the session was about without reading files
- Don't skip errors.log even if you think the session was clean
- Don't trust a handoff blindly -- verify state matches
- Don't pick a session automatically when multiple candidates exist
- Don't start work before the user confirms the approach

## The Gate Function

```
BEFORE resuming any session:

1. DETECT: What resume candidates exist? (worktrees, handoffs, both)
2. SELECT: If multiple candidates, present picker (Mode C)
3. READ: Load all session state files or handoff document
4. VERIFY: Does git state match expectations?
5. PRESENT: Show context summary
6. DIRECT: Tell user which directory to work in
7. ONLY THEN: User begins work

Skip reading = guessing instead of knowing
```

## Auto-Detection Logic

### If a file path argument was provided

```
- If path points to .docs/handoffs/ -> Mode B (Handoff Resume)
- Otherwise -> try reading it as a handoff document -> Mode B
```

### If no argument provided

1. Detect repo layout:
   ```bash
   git_common=$(git rev-parse --git-common-dir 2>/dev/null)
   git_dir=$(git rev-parse --git-dir 2>/dev/null)
   ```

2. If bare-worktree layout: read container-level session-map.json:
   ```bash
   container=$(cd "$(git rev-parse --git-common-dir)" && cd .. && pwd)
   ```
   Parse `$container/session-map.json`.

3. If regular repo: read `.claude/sessions/session-map.json`. Fall back to `_current`.

4. Categorize sessions by status:
   - `"active"` with existing worktree -> Worktree Resume candidates (Mode A)
   - `"handed-off"` with existing worktree -> Handoff Resume candidates (Mode B)
   - `"ended"` -> show as completed, not resumable

5. Also scan `.docs/handoffs/` for handoff documents not tied to a session-map entry.

6. Route:
   - Single candidate -> Mode A or B directly
   - Multiple candidates -> Mode C (picker)
   - No candidates -> guidance message (see Error Recovery)

## Mode A: Worktree Resume

For sessions with status `"active"` and an existing worktree. The user restarted Claude Code and wants to continue their own work.

### Step 1: Read session state

From the selected session's worktree, read `.claude/sessions/{name}/`:

1. **meta.json** (required): sessionId, name, branch, worktree, created, gitBranch, summary
   - If missing: warn and offer to run `/starting-session` instead
2. **errors.log** (optional): count total errors, extract most recent 3
3. **checkpoints.log** (optional): list all checkpoint names and timestamps

### Step 2: Scan for related context

1. Check `.docs/handoffs/` in the worktree for documents mentioning the session name
2. Check `.docs/learnings/` for session-specific learnings
3. Run staleness check on each found document (see Staleness Detection below)

### Step 3: Verify git state

```bash
git -C {worktree_path} branch --show-current
git -C {worktree_path} status --short
git -C {worktree_path} log --oneline -3
```

Compare branch with `meta.json.gitBranch`. If different, warn about branch mismatch.

### Step 4: Present summary

```
SESSION READY TO RESUME
=======================
Name: {name}
Branch: {branch}
Worktree: {worktree_path}
Created: {created}
Summary: {summary}

Errors: {error_count} logged
{if errors > 0:}
  Recent errors:
  - [{tool}] {input_summary}: {error_text_truncated}

Checkpoints: {checkpoint_count}
{if checkpoints > 0:}
  - {checkpoint_name} ({timestamp})

Related docs:
{if handoffs found:}
  - .docs/handoffs/{filename}
{if learnings found:}
  - .docs/learnings/{filename}

Suggested next steps:
{if errors > 0 and no learnings doc:}
  - Run /learning-from-sessions to capture error learnings
{if handoff exists:}
  - Review handoff doc for detailed context
{always:}
  - Continue working on: {summary}

Switch to this directory to continue:
cd {worktree_path}
```

## Mode B: Handoff Resume

For sessions with status `"handed-off"`, or when a handoff document path was provided. Another session wrote a handoff for you to pick up.

### Step 1: Load the handoff

- Read the handoff document FULLY (no limit/offset)
- Run staleness check (see Staleness Detection below)
  - If >3 commits behind: spawn docs-updater agent to refresh, then re-read
  - If docs-updater archives it: warn user it may be obsolete, ask whether to proceed
- Read all linked plans and research documents mentioned in the handoff
- Apply the same staleness check to each linked document

### Step 2: Absorb context

Read and internalize:
- What was being worked on
- What was accomplished
- Key learnings (pay special attention)
- Current state described
- Next steps listed

### Step 3: Check worktree existence

If the handoff mentions a session branch/worktree:
```bash
container=$(cd "$(git rev-parse --git-common-dir)" && cd .. && pwd)
ls -d "$container"/{type}/{session-name} 2>/dev/null
```

- If worktree exists: "The worktree is still at {path}. Switch there to continue."
- If worktree removed: "The worktree was removed. Run `/starting-session` to create a new session, or I can re-create the worktree on the same branch if it still exists."

### Step 4: Verify current state

```bash
git status
git branch --show-current
git log --oneline -5
```

- Verify mentioned files exist
- Check that described changes are present
- Note any drift between handoff and reality

If state has diverged:
```
I notice the current state differs from the handover:

Handover says: [expected state]
Current state: [actual state]

How would you like to proceed?
1. Follow the handover as written
2. Adapt based on current state
3. Create a fresh plan
```

### Step 5: Present takeover summary

```
I've absorbed the handover from [date].

**Previous Work:**
- [What was being done]
- [What was accomplished]

**Key Learnings I'll Apply:**
- [Critical learning 1]
- [Critical learning 2]

**Current State Verified:**
- [Confirmation that state matches, or noting differences]

**Recommended Next Steps:**
1. [First priority from handover]
2. [Second priority]

{if worktree exists:}
Switch to the session worktree to continue:
cd {worktree_path}

Ready to continue with [first next step]?
```

### Step 6: Get confirmation

Wait for user to confirm the approach before starting any work. If user wants adjustments, incorporate feedback and confirm again.

## Mode C: Session Picker

When multiple resume candidates exist (active worktrees + handed-off sessions + handoff documents).

### Present unified picker

```
Available sessions:

  #  Status       Name              Branch                    Path
  1  [active]     auth-mvp          feature/auth-mvp          /c/code/.../feature/auth-mvp
  2  [handed-off] session-v2        refactor/session-v2       /c/code/.../refactor/session-v2
  3  [handoff]    (document)        --                        .docs/handoffs/02-08-2026-deploy-fix.md
  ---
  [ended]         old-session       feature/old-session       (completed, not resumable)

Which would you like to resume?
```

Route to Mode A or B based on selection.

## Staleness Detection

Shared logic for checking document freshness. Apply to every `.docs/` document before presenting it.

```bash
f="<doc-path>"
commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
  git rev-parse "$commit" >/dev/null 2>&1 && \
  behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
  [ -n "$behind" ] && [ "$behind" -gt 3 ] && echo "STALE: $behind commits behind"
fi
```

- If >3 commits behind: spawn docs-updater agent to refresh before presenting
- If docs-updater archives it: note it was archived, omit from context
- If current or no git_commit: include normally

## Error Recovery

**No candidates found:**
```
No sessions or handoffs found to resume.

Options:
1. Run /starting-session to create a new session
2. Provide a handoff path: /resuming-session .docs/handoffs/...

Would you like to start a new session?
```

**Handoff file not found:**
```
I couldn't find that handoff document.

Available handovers in .docs/handoffs/:
[List files if directory exists]

Please provide a valid path.
```

**meta.json missing:** Warn, show what state files do exist, offer `/starting-session`.

**errors.log missing:** Report "0 errors" (clean session).

**checkpoints.log missing:** Report "0 checkpoints".

**Linked docs missing:**
```
The handover references docs I can't find:
- {missing_path_1}
- {missing_path_2}

Should I proceed without them, or can you provide updated paths?
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting session context without reading state files or handoff
- Automatically picking a session when multiple candidates exist
- Skipping git state verification
- Starting work without user confirmation (Mode B)
- Making changes to session files (this skill is read-only except for staleness refresh)
- Ignoring the Key Learnings section of a handoff

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I remember what this session was about" | Read the files. Memory is not state. |
| "Only one session, no need to check state" | Read state files anyway. Errors and checkpoints matter. |
| "State probably hasn't changed" | Verify. Time passes. Things change. |
| "I'll check files as I go" | Upfront verification prevents wasted work. |
| "Skip handoff scan, user didn't ask" | Handoffs provide context the user may have forgotten. |
| "User is waiting" | Wrong assumptions waste more time. Verify first. |

## The Bottom Line

**No resume without reading source files.**

Detect candidates. Select if multiple. Read all state. Verify against reality. Present context. Get confirmation. THEN work.

This is non-negotiable. Every resume. Every time.
