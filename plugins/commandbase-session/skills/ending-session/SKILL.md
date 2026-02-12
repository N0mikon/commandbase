---
name: ending-session
description: "Use this skill when closing out a session's tracking, producing a summary of work done, or wrapping up session state before ending a worktree. This produces .docs/sessions/{name}/summary.json with full session data and marks the session as ended. Does not merge branches or remove worktrees -- use /ending-worktree for that. Trigger phrases: '/ending-session', 'end session', 'close session', 'finish session', 'wrap up session'."
---

# Ending Session

You are closing out a session tracking unit and producing a comprehensive summary file. This skill gathers session state (meta.json, errors.log, checkpoints.log), discovers related handoffs, and writes a permanent summary to `.docs/sessions/{name}/summary.json`.

This is NOT a merge tool. This is NOT a worktree tool. This is session close-out only.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SESSION END WITHOUT SUMMARY
```

Every session close-out must produce a summary.json. The summary captures the full session lifecycle -- purpose, conversations, handoffs, errors, and checkpoints.

**No exceptions:**
- Don't mark a session as ended without writing summary.json
- Don't skip reading errors.log or checkpoints.log
- Don't produce an empty or partial summary
- Don't merge, remove worktrees, or create handoff docs (that's other skills' jobs)

## The Gate Function

```
BEFORE ending any session:

1. DETECT: Find active session in current worktree via session-map.json
2. GATHER: Read meta.json, errors.log, checkpoints.log
3. SCAN: Find handoff docs created during this session (in .docs/handoffs/)
4. COMPOSE: Build summary.json with all session data
5. WRITE: Save to .docs/sessions/{name}/summary.json
6. UPDATE: Mark session as "ended" in session-map.json
7. SUGGEST: Recommend /learning-from-sessions if errors exist

Skip summary = session without close-out
```

## Step 1: Detect Active Session

Find the active session for the current worktree:

```bash
# Get current worktree path
worktree_path=$(git rev-parse --show-toplevel)

# Detect repo layout
git_common=$(git rev-parse --git-common-dir 2>/dev/null)
git_dir=$(git rev-parse --git-dir 2>/dev/null)
```

Read session-map.json and find entries matching this worktree with `status: "active"`.

If no active session found:
```
No active session in this worktree.

Options:
1. If you want to start tracking: /starting-session
2. If you want to merge/remove the worktree: /ending-worktree
```

If multiple active sessions (shouldn't happen, but handle gracefully): present a picker and let the user choose which to end.

## Step 2: Gather Session State

Read the session's state files from `.claude/sessions/{name}/`:

### meta.json (required)
```bash
cat {worktree}/.claude/sessions/{name}/meta.json
```

Extract: `sessionId`, `claudeSessionIds`, `name`, `branch`, `worktree`, `created`, `gitBranch`, `summary`.

If meta.json is missing or corrupt: warn and offer to create a minimal summary from session-map.json data instead.

### errors.log (optional)
```bash
cat {worktree}/.claude/sessions/{name}/errors.log 2>/dev/null
```

Parse error entries. Count total errors. Extract the most recent entries for the summary.

If missing: 0 errors (clean session).

### checkpoints.log (optional)
```bash
cat {worktree}/.claude/sessions/{name}/checkpoints.log 2>/dev/null
```

Parse checkpoint entries. Each has a name, timestamp, and SHA.

If missing: 0 checkpoints.

## Step 3: Scan for Related Handoffs

Scan `.docs/handoffs/` for handoff documents related to this session:

1. Check for files whose `topic` frontmatter contains the session name
2. Check for files whose `tags` include the session name
3. Check for files created within the session's time window (created → now)

Collect matching file paths for the summary.

## Step 4: Compose summary.json

Build the summary object:

```json
{
  "name": "<session-name>",
  "summary": "<purpose from meta.json>",
  "branch": "<branch from meta.json>",
  "worktree": "<worktree path from meta.json>",
  "created": "<ISO 8601 from meta.json>",
  "ended": "<ISO 8601 now>",
  "claudeSessionIds": ["<uuid-1>", "<uuid-2>"],
  "handoffs": [
    ".docs/handoffs/02-11-2026-session-name-description.md"
  ],
  "errors": {
    "count": 0,
    "summary": []
  },
  "checkpoints": []
}
```

**Fields:**
- `name`: Session name from meta.json
- `summary`: Purpose from meta.json (the user-provided description from discovery)
- `branch`: Git branch the session was on
- `worktree`: Worktree path
- `created`: Session start time from meta.json
- `ended`: Current time (ISO 8601)
- `claudeSessionIds`: Full list of conversation UUIDs that participated in this session
- `handoffs`: List of `.docs/handoffs/` file paths related to this session
- `errors.count`: Total number of errors logged
- `errors.summary`: Array of error objects, each with `tool`, `input`, `error`, and `source` fields
- `checkpoints`: Array of checkpoint objects, each with `name`, `timestamp`, and `sha` fields

## Step 5: Write summary.json

Write to `.docs/sessions/{name}/summary.json`:

```bash
# Create directory
mkdir -p {worktree}/.docs/sessions/{session-name}
```

Write the composed JSON to the file. Use atomic write if possible (write to temp file, then move).

This file is committed to git (NOT gitignored). It becomes a permanent record of the session.

## Step 6: Update session-map.json

Mark the session as ended in session-map.json:

Set `status: "ended"` for this session's entry. This prevents the SessionStart hook from injecting this session's context in future conversations.

## Step 7: Output

```
SESSION ENDED
=============
Name: {session-name}
Duration: {created} -> {now}
Conversations: {count} Claude sessions
Handoffs: {count} created during session
Errors: {count} logged
Checkpoints: {count} created

Summary saved: .docs/sessions/{name}/summary.json

{if errors > 0:}
This session had errors. Run /learning-from-sessions to extract learnings:
/learning-from-sessions {session-name}

The worktree is still active. Use /ending-worktree when ready to merge or discard.
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to mark session as ended without writing summary.json
- Skipping errors.log or checkpoints.log reads
- About to merge branches or remove worktrees (that's /ending-worktree)
- About to create handoff docs (that's /handing-over)
- Producing a summary with missing claudeSessionIds or empty fields
- Marking ended without confirming which session to close (when multiple exist)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "No errors, skip errors.log" | Read it anyway. Confirm zero errors explicitly. |
| "No handoffs to scan for" | Scan .docs/handoffs/ anyway. You might be wrong. |
| "User just wants to end quickly" | Summary.json takes seconds to write. Never skip. |
| "I should also merge the branch" | No. That's /ending-worktree. Stay in scope. |
| "I should create a handoff too" | No. That's /handing-over. Stay in scope. |
| "Checkpoints probably don't exist" | Read the file. Probably isn't evidence. |

## The Bottom Line

**No session end without summary.**

Detect session. Gather state. Scan handoffs. Compose summary. Write file. Update map. Present results. Nothing more.

This is non-negotiable. Every session close-out. Every time.
