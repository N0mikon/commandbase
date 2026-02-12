---
name: starting-session
description: "Use this skill when starting session tracking in a worktree or regular repo. This runs discovery to establish session purpose, sets up per-session error and checkpoint tracking, registers the session in session-map.json, and captures the initial conversation UUID. Does not create branches or worktrees -- use /starting-worktree for that. Trigger phrases: '/starting-session', 'start a session', 'new session', 'create a session', 'begin tracking'."
---

# Starting Session

You are setting up session tracking for the current worktree or repository. This skill handles session discovery and state -- establishing purpose, writing meta.json, registering in session-map.json, and capturing the initial UUID. Git branch and worktree creation is handled separately by `/starting-worktree`.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SESSION WITHOUT PURPOSE
```

Every session must have a stated purpose. The discovery step is not optional -- it makes the `summary` field meaningful, feeds into SessionStart hook context injection, and provides input for the close-out summary.

**No exceptions:**
- Don't create sessions without asking what the work is about
- Don't leave the summary field empty
- Don't bypass name validation
- Don't skip the worktree warning when applicable

## The Gate Function

```
BEFORE creating any session:

1. DETECT: Am I in a worktree? If not, warn (but allow proceeding in regular repo)
2. CHECK: Is there already an active session in this worktree? If yes, warn.
3. DISCOVER: Ask what this session is about (purpose, scope, target area)
4. CONTEXT: Read relevant plans/research/handoffs mentioned by user
5. ESTABLISH: Write meta.json with summary, capture UUID
6. REGISTER: Update session-map.json
7. OUTPUT: Present session brief

Skip discovery = session without purpose
```

## Step 1: Worktree Detection

Run the following to detect the environment:

```bash
# Check if we're in a bare-worktree layout
git_common=$(git rev-parse --git-common-dir 2>/dev/null)
git_dir=$(git rev-parse --git-dir 2>/dev/null)
```

If `git_common` and `git_dir` resolve to different absolute paths: **bare-worktree layout**.
If they're the same: **regular repo**.

### If in bare-worktree layout but NOT in a worktree (in main):
```
You're in the main worktree. Sessions are typically started in feature/fix/refactor worktrees.

Run /starting-worktree first to create an isolated worktree, then run /starting-session there.

Or continue here if you want to track a session in the main worktree.
```

### If in a regular repo (not bare-worktree layout):
```
You're not in a worktree. Sessions work without worktrees, but you won't
get git isolation. Run /starting-worktree first for isolated branches.

Continue without worktree? (Y/n)
```

## Step 2: Check for active session

Read session-map.json for entries matching this worktree with `status: "active"`. If found:
```
There's already an active session in this worktree: {name}
End it with /ending-session first, or continue working in that session.
```

## Step 3: Discovery

Use AskUserQuestion to gather session context. This is the key step that makes sessions purposeful.

Ask the user:
- **What are you working on?** -- Brief purpose description. This becomes the `summary` field in meta.json and is injected by the SessionStart hook in future conversations.
- **Related docs?** -- Plans, research, or handoffs to read for context (optional). Provide options like "None", or let user specify paths.
- **Session name** -- Auto-suggest a kebab-case name based on the purpose description. User confirms or provides their own.

**Session Name Validation (kebab-case):**
- 3-40 characters
- Pattern: `^[a-z0-9][a-z0-9-]*[a-z0-9]$`
- No leading/trailing/consecutive hyphens
- Examples: `auth-mvp`, `login-timeout-fix`, `session-v2`

## Step 4: Load Context

If the user mentioned related docs in the discovery step:
1. Read each referenced document (plans, research, handoffs)
2. Internalize the context for the session brief
3. Note which docs were loaded for the output

If no docs mentioned, skip this step.

## Step 5: Create session state directory

```bash
mkdir -p {worktree}/.claude/sessions/{session-name}
```

Verify `.claude/sessions/` is in the worktree's `.gitignore`.

## Step 6: Write meta.json

Write to `{worktree}/.claude/sessions/{session-name}/meta.json`:

```json
{
  "sessionId": "<session-name>",
  "claudeSessionIds": ["<initial-uuid>"],
  "name": "<session-name>",
  "branch": "<current-branch>",
  "worktree": "<worktree-path-or-cwd>",
  "created": "<ISO 8601>",
  "gitBranch": "<current-branch>",
  "summary": "<user-provided purpose>"
}
```

- `sessionId` stays as session name for backward compatibility
- `claudeSessionIds` starts with the current conversation's UUID (read from SessionStart hook injection at conversation start). If UUID is not available, start with an empty array.
- `summary` is populated from the user's purpose description in the discovery step
- `branch` reflects the current branch (not necessarily a session-created branch)

## Step 7: Update session-map.json

Update the container-level `session-map.json` atomically:

```python
# Via session_utils.update_session_map()
{
  "<session_id>": {
    "name": "<session-name>",
    "branch": "<current-branch>",
    "worktree": "<worktree-path-or-cwd>",
    "created": "<ISO 8601>",
    "status": "active",
    "summary": "<user-provided purpose>"
  }
}
```

Use the `session_utils.py` functions from `plugins/commandbase-session/scripts/` for atomic write operations. Run via:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_utils.py  # (import and call)
```

Or construct the JSON manually and write via Bash with a temp file + `mv` pattern.

## Step 8: Output

```
SESSION STARTED
===============
Name: {session-name}
Purpose: {summary}
Worktree: {worktree_path} (or "regular repo" if no worktree)

Context loaded:
- {plan/research/handoff if any were read}

Ready to work. Hooks are tracking errors and conversation UUIDs.
```

If no context docs were loaded, omit the "Context loaded" section.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to create session state without running discovery
- Leaving the summary field empty
- Skipping the active session check
- Name doesn't match kebab-case validation
- Creating session state without checking worktree context
- Proceeding when an active session already exists

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User wants to start quickly" | Discovery is two questions. Never skip. |
| "Purpose is obvious from context" | Ask anyway. User states purpose explicitly. |
| "Name looks fine" | Validate against the regex. Every time. |
| "No need to check for active sessions" | Check anyway. Duplicate sessions cause confusion. |
| "Worktree warning isn't important" | User needs to know they lack git isolation. |
| "Summary can be filled in later" | No. Summary is written at creation. That's the Iron Law. |

## The Bottom Line

**No session without purpose.**

Detect worktree. Check for active sessions. Discover purpose. Load context. Write state. Register. Present brief. Every session. Every time.
