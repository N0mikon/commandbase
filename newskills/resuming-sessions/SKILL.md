---
name: resuming-sessions
description: "Use this skill when resuming a previous session after restarting Claude Code, restoring session context, or picking up where you left off without a handoff document. This includes reading session-map.json and session state files (meta.json, errors.log, checkpoints.log), presenting session context, and suggesting next steps. Trigger phrases: '/resuming-sessions', 'resume session', 'restore session', 'what session was I in', 'continue my session'."
---

# Resuming Sessions

You are restoring session context after a Claude Code restart. Your job is to read session state files and present the user with full context so they can continue where they left off.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SESSION RESUME WITHOUT READING STATE FILES
```

You must read and present actual session state. Never guess, summarize from memory, or skip state files.

**No exceptions:**
- Don't assume you know what the session was about without reading meta.json
- Don't skip errors.log even if you think the session was clean
- Don't present a session summary without reading the files first
- Don't pick a session automatically when multiple exist

## The Gate Function

```
BEFORE presenting session context:

1. READ: .claude/sessions/session-map.json for all named sessions
2. FALLBACK: Check .claude/sessions/_current if no session-map.json
3. SELECT: If multiple sessions, ask user which to resume
4. LOAD: Read meta.json, errors.log, checkpoints.log from session folder
5. SCAN: Check .docs/handoffs/ for related handoff documents
6. VERIFY: Check current git branch matches session branch
7. ONLY THEN: Present the session summary

Skip reading state = guessing instead of knowing
```

## Key Difference from /taking-over

| | /resuming-sessions | /taking-over |
|---|---|---|
| **Input** | Session state files (meta.json, errors.log, checkpoints.log) | Handoff document (.docs/handoffs/) |
| **When** | After restarting Claude Code | After another session wrote a handoff |
| **Context** | Reconstructed from state files | Narrated by the previous session |
| **Action** | Present context, suggest next steps | Verify state, continue work |

Use `/resuming-sessions` when you restarted Claude and want to pick up your own session. Use `/taking-over` when another session (or person) wrote a handoff for you.

## Process

### Step 1: Discover Sessions

Read `.claude/sessions/session-map.json`:

```json
{
  "c0f93740-...": {"name": "integration-test", "created": "2026-02-07T..."},
  "ff6eb348-...": {"name": "harvest-testing", "created": "2026-02-07T..."}
}
```

**If session-map.json doesn't exist or is empty:** Fall back to `.claude/sessions/_current`:
- If `_current` exists: use that session name
- If neither exists:
  ```
  No named sessions found.

  Options:
  1. Run /naming-session to name a new session
  2. Run /taking-over to resume from a handoff document

  Which would you prefer?
  ```

### Step 2: Select Session

- **If 1 session**: Use it automatically
- **If multiple sessions**: Present the list and ask:
  ```
  Found {count} named sessions:

  1. {name1} (created: {date1})
  2. {name2} (created: {date2})
  ...

  Which session would you like to resume?
  ```

### Step 3: Load Session State

Read from `.claude/sessions/{name}/`:

1. **meta.json** (required):
   - sessionId, name, created, gitBranch, summary
   - If missing: warn and offer to run /naming-session instead

2. **errors.log** (optional):
   - Count total errors
   - Extract most recent 3 errors (tool, input summary, error text)

3. **checkpoints.log** (optional):
   - List all checkpoint names and timestamps

### Step 4: Scan for Related Context

1. Check `.docs/handoffs/` for documents mentioning the session name
2. Check `.docs/learnings/` for session-specific learnings
3. **Staleness auto-update**: For each handoff or learning document found, check its freshness before presenting to user:
   ```bash
   f="<doc-path>"
   commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
   if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
     git rev-parse "$commit" >/dev/null 2>&1 && \
     behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
     [ -n "$behind" ] && [ "$behind" -gt 3 ] && echo "$behind"
   fi
   ```
   - If >3 commits behind: spawn docs-updater agent to refresh it before presenting to user
   - If docs-updater archives it: omit from session context (note it was archived)
   - If current or no git_commit: include normally

### Step 5: Verify Git State

1. Get the current git branch
2. Compare with `meta.json.gitBranch`
3. If different, warn:
   ```
   Branch mismatch:
     Session branch: {meta.gitBranch}
     Current branch: {current branch}

   You may need to switch branches: git checkout {meta.gitBranch}
   ```

### Step 6: Present Session Summary

```
SESSION RESUMED
===============
Name: {name}
Session ID: {sessionId} (truncated)
Branch: {gitBranch} {branch_status}
Created: {created}
Summary: {summary}

Errors: {error_count} logged
{if errors > 0:}
  Recent errors:
  - [{tool}] {input_summary}: {error_text_truncated}
  - [{tool}] {input_summary}: {error_text_truncated}
  - [{tool}] {input_summary}: {error_text_truncated}

Checkpoints: {checkpoint_count}
{if checkpoints > 0:}
  - {checkpoint_name} ({timestamp})
  ...

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
```

## Output Format

The session summary above IS the output. No separate output section needed.

## Error Recovery

**Recoverable errors:**
- session-map.json missing: Fall back to `_current`
- meta.json missing: Warn, offer /naming-session
- errors.log missing: Report "0 errors" (clean session)
- checkpoints.log missing: Report "0 checkpoints"
- No handoffs found: Skip that section

**Blocking errors:**
- No sessions exist and no `_current`: Cannot resume (offer alternatives)
- Session folder doesn't exist: Cannot resume (offer /naming-session)

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting session context without reading meta.json
- Automatically picking a session when multiple exist
- Skipping the git branch check
- Making changes to session files (this skill is read-only)
- Suggesting /taking-over when the user clearly wants to resume their own session

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I remember what this session was about" | Read meta.json. Memory is not state files. |
| "Only one session, no need to check state" | Read state files anyway. The session may have errors or checkpoints. |
| "No errors means nothing to report" | Report "0 errors" — confirming a clean session is valuable context. |
| "Git branch doesn't matter" | Branch mismatch can cause confusion. Always verify. |
| "Skip handoff scan, user didn't ask" | Handoffs provide context the user may have forgotten. Always scan. |

## The Bottom Line

**No session resume without reading state files.**

Discover sessions. Select if multiple. Read meta.json, errors.log, checkpoints.log. Scan for related docs. Verify git branch. Present the full picture.

This is non-negotiable. Every resume. Every time.
