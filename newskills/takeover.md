---
description: Resume work from a handover document
---

# Takeover

You are picking up work from a handover document. Your job is to absorb the context, verify the current state, and continue the work.

## Process

### Step 1: Load the Handover

**If a file path was provided:**
- Read the handover document FULLY (no limit/offset)
- Read any linked plans or research documents mentioned
- Begin analysis

**If no path provided:**
```
I'll help you pick up from a handover.

Available handovers in .docs/handoffs/:
[List files if directory exists]

Which handover would you like to resume from?

Usage: /takeover .docs/handoffs/MM-DD-YYYY-description.md
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

### Step 4: Present Takeover Summary

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

### Step 5: Get Confirmation

Wait for user to confirm the approach before starting work.

If user wants adjustments:
- Incorporate their feedback
- Adjust the plan
- Confirm again

### Step 6: Begin Work

Once confirmed:
- Create a todo list with TodoWrite
- Start with the first next step
- Apply learnings throughout
- Reference the handover when relevant

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
```

**Handover is stale:**
```
This handover is from [date], and significant changes have occurred since:
- [Change 1]
- [Change 2]

The next steps may need adjustment. Want me to:
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

## Example Interaction

```
User: /takeover .docs/handoffs/01-27-2026-auth-implementation.md
Assistant: I've absorbed the handover from January 27th.

**Previous Work:**
Alex was implementing JWT authentication. Completed the token generation
and validation middleware. Login endpoint working.

**Key Learnings I'll Apply:**
- Must use RS256 not HS256 (security requirement in auth.config.ts:12)
- Token refresh logic is tricky - see pattern in middleware/refresh.ts:34-56
- Tests require MOCK_JWT_SECRET env var

**Current State Verified:**
- On branch: feature/auth
- Last commit: "Add token validation middleware"
- Files match handover description ✓

**Recommended Next Steps:**
1. Implement logout endpoint (clear refresh tokens)
2. Add token refresh endpoint
3. Write integration tests

Ready to continue with the logout endpoint?

User: Yes, go ahead
Assistant: [Creates todos and begins implementation]
```
