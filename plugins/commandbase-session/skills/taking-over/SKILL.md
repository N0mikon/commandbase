---
name: taking-over
description: "Use this skill when picking up work from a handover document or continuing where another session left off. This includes reading handover documents from .docs/handoffs/, understanding prior context, reviewing modified files, and preparing to continue implementation. Standalone -- does not require /resuming-session. Trigger phrases: '/takeover', 'continue from handover', 'pick up where we left off', 'read the handover', 'absorb handoff'."
---

# Takeover

You are picking up work from a handover document. Your job is to absorb the context, verify the current state, and prepare to continue the work.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO WORK WITHOUT STATE VERIFICATION
```

If you haven't verified the current state matches the handover, you cannot start working.

**No exceptions:**
- Don't trust the handover blindly - verify state
- Don't skip reading linked docs
- Don't start work before confirming approach with user
- Don't ignore drift between handover and reality

## The Gate Function

```
BEFORE starting any work from a handover:

1. READ: The handover document FULLY
2. READ: All linked plans and research docs
3. VERIFY: Run `git status`, `git log -5`, check file existence
4. COMPARE: Does reality match the handover?
   - If NO: Note the differences, ask user how to proceed
   - If YES: Continue to step 5
5. ABSORB: Internalize the Key Learnings section
6. CONFIRM: Present summary and get user approval
7. ONLY THEN: Begin work

Skip verification = working blind
```

## Process

### Step 1: Load the Handover

**If a file path was provided:**
- Read the handover document FULLY (no limit/offset)
- **Staleness auto-update**: Before proceeding, check the handoff document's freshness:
  ```bash
  f="<handoff-path>"
  commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
  if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
    git rev-parse "$commit" >/dev/null 2>&1 && \
    behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
    [ -n "$behind" ] && [ "$behind" -gt 3 ] && echo "$behind"
  fi
  ```
  - If >3 commits behind: spawn docs-updater agent to refresh it, then re-read the updated version
  - If docs-updater archives it (all references deleted): warn the user that the handoff may be obsolete and ask whether to proceed
  - If current or no git_commit: proceed normally
- Read any linked plans or research documents mentioned
- Apply the same staleness check to each linked document before reading it
- Begin analysis

**If no path provided:**
```
I'll help you pick up from a handover.

Available handovers in .docs/handoffs/:
[List files if directory exists]

Which handover would you like to resume from?

Usage: /taking-over .docs/handoffs/MM-DD-YYYY-description.md
```

### Step 2: Absorb Context

Read and internalize:
- What was being worked on
- What was accomplished
- Key learnings (pay special attention here)
- Current state
- Next steps

### Step 3: Verify Current State

Check that reality matches the handover:

```bash
# Check git state
git status
git branch --show-current
git log --oneline -5
```

- Verify mentioned files exist
- Check that described changes are present
- Look for any drift since the handover

### Step 4: Session Association

After absorbing the handoff, check for session context:

1. Detect repo layout:
   ```bash
   git_common=$(git rev-parse --git-common-dir 2>/dev/null)
   git_dir=$(git rev-parse --git-dir 2>/dev/null)
   ```
2. If bare-worktree layout: read container-level `session-map.json`, find entry whose `worktree` matches current cwd with `status: "active"`.
3. If in the same worktree and session is active: associate this conversation's UUID with that session by calling `update_meta_json()` to append to `claudeSessionIds`.
4. If no active session: note this for the session offer in Step 6.

### Step 5: Present Takeover Summary

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
3. [Any adjustments based on current state]

Ready to continue with [first next step]?
```

### Step 6: Session and Confirmation

After presenting the summary, if no active session was found in Step 4, offer:

```
Would you like to start a new session for this work?
1. Yes - run /starting-session to create a tracking session
2. No - continue without session tracking
```

Wait for user to confirm the approach before starting work.

If user wants adjustments:
- Incorporate their feedback
- Adjust the plan
- Confirm again

### Step 7: Begin Work

Once confirmed:
- Start with the first next step
- Apply learnings throughout
- Reference the handover when relevant

## Red Flags - STOP and Verify

If you notice any of these, STOP immediately:

- Starting work without reading full handover
- Skipping linked documents
- Not running `git status` to verify state
- State doesn't match handover but continuing anyway
- Ignoring Key Learnings section
- Starting work without user confirmation

**When you hit a red flag:**
1. Stop and read the handover fully
2. Verify state with git commands
3. Note any differences
4. Get user confirmation before proceeding

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I read the summary" | Read the full handover. Details matter. |
| "State probably hasn't changed" | Verify anyway. Time passes. Things change. |
| "I'll check files as I go" | Upfront verification prevents wasted work. |
| "User is waiting" | Wrong assumptions waste more time. Verify first. |

## Guidelines

1. **Read Everything First**
   - Read the full handover before acting
   - Read linked docs (plans, research)
   - Don't skim - absorb

2. **Verify Before Trusting**
   - State may have changed since handover
   - Files may have been modified
   - Check git status and recent commits

3. **Apply the Learnings**
   - The learnings section is gold
   - Don't repeat mistakes documented there
   - Follow patterns that were discovered

4. **Ask If Unclear**
   - If handover is ambiguous, ask
   - If state doesn't match, clarify
   - Better to confirm than assume

5. **Maintain Continuity**
   - You're continuing work, not starting fresh
   - Build on what was done
   - Keep the same conventions/patterns

## Handling Edge Cases

**Handover file not found:**
```
I couldn't find that handover document.

Available handovers:
[List .docs/handoffs/ contents]

Please provide a valid path.
```

**State has diverged:**
```
I notice the current state differs from the handover:

Handover says: [expected state]
Current state: [actual state]

This might be because:
- Someone else made changes
- Time has passed
- Branch was switched

How would you like to proceed?
1. Follow the handover as written
2. Adapt based on current state
3. Create a fresh plan
```

**Linked docs missing:**
```
The handover references these docs that I can't find:
- .docs/plans/missing-plan.md
- .docs/research/missing-research.md

Should I proceed without them, or can you provide updated paths?
```

## The Bottom Line

**No shortcuts for takeover.**

Read everything. Verify state. Apply learnings. Get confirmation. THEN work.

This is non-negotiable. Every takeover. Every time.
