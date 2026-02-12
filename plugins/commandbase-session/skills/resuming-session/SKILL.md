---
name: resuming-session
description: "Use this skill when resuming a previous session after restarting Claude Code, continuing where a previous conversation left off, or checking session state before starting work. This includes reading session state files (meta.json, errors.log, checkpoints.log), verifying git state, and presenting a context summary. For absorbing handoff documents, use /taking-over instead. Trigger phrases: '/resuming-session', 'resume session', 'continue session', 'pick up where I left off', 'switch to session'."
---

# Resuming Session

You are restoring session context by reading worktree session state files. Your job is to read session state, verify it against reality, and present a full context summary so the user can continue where they left off.

This is worktree session resume only. For absorbing handoff documents, use `/taking-over`.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO RESUME WITHOUT READING SOURCE FILES
```

You must read actual session state files before presenting any summary. Never guess, summarize from memory, or skip verification.

**No exceptions:**
- Don't assume you know what the session was about without reading files
- Don't skip errors.log even if you think the session was clean
- Don't pick a session automatically when multiple candidates exist
- Don't start work before presenting the context summary

## The Gate Function

```
BEFORE resuming any session:

1. DETECT: Find session(s) for current worktree in session-map.json
2. SELECT: If multiple sessions exist for this worktree, present picker
3. READ: Load session state files (meta.json, errors.log, checkpoints.log)
4. VERIFY: Does git state match expectations?
5. PRESENT: Show context summary including session purpose (summary field)
6. ONLY THEN: User begins work

Skip reading = guessing instead of knowing
```

## Step 1: Detect Sessions

Detect repo layout and find sessions for the current worktree:

```bash
# Detect layout
git_common=$(git rev-parse --git-common-dir 2>/dev/null)
git_dir=$(git rev-parse --git-dir 2>/dev/null)

# Get worktree path
worktree_path=$(git rev-parse --show-toplevel)
```

Read session-map.json and find ALL entries matching this worktree path (any status).

### If no sessions found for this worktree:

```
No active session in this worktree.

Options:
1. /starting-session - Start a new session
2. /taking-over - Pick up from a handoff document
```

### If one active session found:

Proceed directly to Step 2 (read state files).

### If multiple sessions found for this worktree:

Present the worktree-scoped session history:

```
Sessions in this worktree:

  #  Status   Name              Created              Summary
  1  [active] auth-refactor     2026-02-11 10:00     Refactoring auth middleware
  2  [ended]  initial-setup     2026-02-10 14:00     Initial project scaffolding

Which session to resume? (Only active sessions can be resumed)
```

Only active sessions can be selected for resume. Ended sessions are shown for context only.

If no active sessions exist among the matches:
```
No active session in this worktree. All sessions are ended.

Options:
1. /starting-session - Start a new session
2. /taking-over - Pick up from a handoff document
```

## Step 2: Read Session State

From the selected session's worktree, read `.claude/sessions/{name}/`:

### meta.json (required)

Read the full file. Extract: `sessionId`, `claudeSessionIds`, `name`, `branch`, `worktree`, `created`, `gitBranch`, `summary`.

- Read `claudeSessionIds` array if present (new schema)
- Fall back to `sessionId` if `claudeSessionIds` is missing (old schema)
- If missing: warn and offer to run `/starting-session` instead

### errors.log (optional)

Count total errors, extract most recent 3 for display.

If missing: 0 errors (clean session).

### checkpoints.log (optional)

List all checkpoint names and timestamps.

If missing: 0 checkpoints.

## Step 3: Scan for Related Context

Check for documents related to this session:

1. Check `.docs/handoffs/` for documents mentioning the session name
2. Check `.docs/learnings/` for session-specific learnings
3. Check `.docs/plans/` for plans referenced in meta.json or recent handoffs

For each found document, run staleness check:

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

## Step 4: Verify Git State

```bash
git -C {worktree_path} branch --show-current
git -C {worktree_path} status --short
git -C {worktree_path} log --oneline -3
```

Compare branch with `meta.json.gitBranch`. If different, warn about branch mismatch.

## Step 5: Present Summary

```
SESSION READY TO RESUME
=======================
Name: {name}
Branch: {branch}
Worktree: {worktree_path}
Created: {created}
Purpose: {summary}

Transcripts: {count} Claude sessions recorded
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

## Error Recovery

**meta.json missing:** Warn, show what state files do exist, offer `/starting-session`.

**errors.log missing:** Report "0 errors" (clean session).

**checkpoints.log missing:** Report "0 checkpoints".

**Worktree doesn't exist:**
```
The worktree for this session no longer exists.

Options:
1. /starting-session - Start a new session in the current directory
2. /taking-over - Pick up from a handoff document
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting session context without reading state files
- Automatically picking a session when multiple candidates exist
- Skipping git state verification
- Making changes to session files (this skill is read-only except for staleness refresh)
- Trying to absorb a handoff document (that's /taking-over)
- Skipping errors.log or checkpoints.log reads

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I remember what this session was about" | Read the files. Memory is not state. |
| "Only one session, no need to check state" | Read state files anyway. Errors and checkpoints matter. |
| "State probably hasn't changed" | Verify. Time passes. Things change. |
| "I'll check files as I go" | Upfront verification prevents wasted work. |
| "User is waiting" | Wrong assumptions waste more time. Verify first. |
| "I should absorb this handoff too" | No. That's /taking-over. Stay in scope. |

## The Bottom Line

**No resume without reading source files.**

Detect sessions. Select if multiple. Read state. Verify git. Present context. THEN work.

This is non-negotiable. Every resume. Every time.
