---
name: naming-session
description: "Use this skill when naming the current work session, creating a session identity for checkpoint and error tracking, or starting a named session. This includes assigning a user-defined name to the active session, creating per-session folders at .claude/sessions/ with metadata, writing a _current pointer file, and renaming an existing session. Trigger phrases: '/naming-session', 'name this session', 'start a session', 'create a session'."
---

# Naming Session

You are assigning a user-defined name to the current Claude Code session, creating a per-session folder structure for checkpoints, errors, and learnings. This is the foundation that other session-aware skills read from.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SESSION NAME WITHOUT USER CONFIRMATION
```

The user chooses the name. Auto-suggestions are fine, but the final name must be explicitly confirmed.

**No exceptions:**
- Don't create the session folder before user confirms the name
- Don't overwrite an existing `_current` pointer without warning
- Don't skip the name validation check
- Don't assume the auto-suggested name is acceptable

## The Gate Function

```
BEFORE creating any session folder:

1. READ: Find the current session in sessions-index.json
2. CHECK: Does .claude/sessions/_current already exist?
3. SUGGEST: Auto-generate a name from the session summary
4. CONFIRM: Present the name to the user for approval or override
5. VALIDATE: Name must pass kebab-case rules
6. ONLY THEN: Create the folder and write _current

Skip confirmation = naming without consent
```

## Process

### Step 1: Find Current Session

Read the native Claude session index to identify this session:

1. Determine the encoded project path for the sessions-index lookup:
   - Get the current working directory
   - Replace path separators with `--`, remove the colon (e.g., `C:\code\commandbase` becomes `C--code-commandbase`)
2. Read `~/.claude/projects/{encoded-path}/sessions-index.json`
3. Find the most recent entry by `modified` timestamp
4. Extract: `sessionId`, `summary`, `gitBranch`

**If sessions-index.json doesn't exist or is empty:**
```
No session index found for this project.

A session folder can still be created with a manual name.
Enter a session name (kebab-case, 3-40 chars):
```

### Step 2: Check for Existing Session

Check for existing sessions in two places:

1. Read `.claude/sessions/session-map.json` — list any existing named sessions
2. Check if `.claude/sessions/_current` exists as a fallback

- **If sessions exist** (in session-map.json or `_current`): Warn:
  ```
  An active session already exists: "{current-name}"

  Options:
  1. Replace it with a new session name (old folder stays intact)
  2. Keep the current session name
  3. Cancel

  Which would you prefer?
  ```
- **If no existing sessions**: Proceed to Step 3

### Step 3: Suggest and Confirm Name

Auto-generate a suggested name from the session summary:

1. Take the `summary` field from sessions-index.json
2. Convert to kebab-case: lowercase, replace spaces with hyphens, remove special chars
3. Truncate to 40 characters at a word boundary
4. Present to user:

```
Session detected:
  ID: {sessionId} (truncated)
  Branch: {gitBranch}
  Summary: "{summary}"

Suggested name: {auto-suggested-name}

Accept this name, or enter a custom name:
```

### Step 4: Validate Name

The session name must pass these rules:

| Rule | Detail |
|------|--------|
| Format | `^[a-z0-9-]+$` (lowercase alphanumeric and hyphens only) |
| Length | 3-40 characters |
| No leading/trailing hyphens | `-name` and `name-` are invalid |
| No consecutive hyphens | `my--session` is invalid |

If validation fails, show the specific rule violation and ask for a corrected name.

### Step 5: Create Session Folder

Once the name is confirmed and validated:

1. Create directory: `.claude/sessions/{name}/`
2. Write `.claude/sessions/{name}/meta.json`:
   ```json
   {
     "sessionId": "{uuid from sessions-index}",
     "name": "{confirmed name}",
     "created": "{ISO 8601 timestamp}",
     "gitBranch": "{branch}",
     "summary": "{native summary}"
   }
   ```
3. Write `.claude/sessions/_current` with just the session name string (no newline, no JSON)
4. Update `.claude/sessions/session-map.json` — add/update the mapping from session_id to session name:
   ```json
   {
     "<session_id>": {"name": "<confirmed name>", "created": "<ISO 8601 timestamp>"}
   }
   ```
   If the file already exists, merge the new entry (read, parse, add key, write back). If it doesn't exist, create it with just this entry. Use atomic write (write to temp file, then rename) to avoid corruption from concurrent terminals.

### Step 6: Confirm Creation

```
Session named: "{name}"

Created:
  .claude/sessions/{name}/meta.json
  .claude/sessions/_current
  .claude/sessions/session-map.json (updated)

Session-aware skills will now use this session:
  /bookmarking-code  - checkpoints written to session folder
  /handing-over      - handoffs include session context
  /implementing-plans - mandatory checkpoints are session-scoped
  /resuming-sessions - session can be resumed after exit

To end this session's tracking, delete .claude/sessions/_current
```

## Output Format

When complete, produce:

```
SESSION NAMED
=============
Name: {name}
Session ID: {uuid}
Branch: {branch}
Folder: .claude/sessions/{name}/

Files created/updated:
- .claude/sessions/{name}/meta.json
- .claude/sessions/_current
- .claude/sessions/session-map.json
```

## Error Recovery

**Recoverable errors:**
- sessions-index.json missing: Proceed with manual name entry
- `_current` already exists: Offer replace/keep/cancel options
- Name validation fails: Show rule violation, ask for corrected name

**Blocking errors:**
- Cannot create `.claude/sessions/` directory: Check permissions, present error to user
- Cannot write files: Check disk space and permissions

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Creating the session folder before user confirms the name
- Overwriting `_current` without warning about existing session
- Skipping name validation because the name "looks fine"
- Writing to `sessions-index.json` (that's Claude's internal file — read only)
- Making changes beyond session folder creation

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The auto-suggested name is perfect" | User must confirm. Auto-suggest is a suggestion, not a decision. |
| "No need to check _current, this is a fresh session" | Check anyway. State can be stale from a previous session. |
| "This name is obviously valid" | Run the validation rules. Every name. Every time. |
| "I'll skip meta.json, it's just metadata" | meta.json is how other skills identify this session. Required. |

## The Bottom Line

**No session name without user confirmation.**

Read the session index. Suggest a name. Get confirmation. Validate. Create the folder. Write the pointer.

This is non-negotiable. Every session naming. Every time.
