# Research: taking-over Skill

## Overview

The `taking-over` skill (`~/.claude/skills/taking-over/SKILL.md`) picks up work from a handover document. It absorbs context, verifies current state, and continues the work from where it was left off.

**Trigger phrases**: `/takeover`, `continue from handover`, `resume previous work`, `pick up where we left off`, `read the handover`

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

Before starting any work from a handover:

1. **READ**: The handover document FULLY
2. **READ**: All linked plans and research docs
3. **VERIFY**: Run `git status`, `git log -5`, check file existence
4. **COMPARE**: Does reality match the handover?
5. **ABSORB**: Internalize the Key Learnings section
6. **CONFIRM**: Present summary and get user approval
7. **ONLY THEN**: Begin work

## Process

### Step 1: Load the Handover
If file path provided, read completely. If not, list available handovers in `.docs/handoffs/`.

### Step 2: Absorb Context
Read and internalize:
- What was being worked on
- What was accomplished
- Key learnings
- Current state
- Next steps

### Step 3: Verify Current State
```bash
git status
git branch --show-current
git log --oneline -5
```

Check that mentioned files exist and described changes are present.

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
- [Confirmation that state matches]

**Recommended Next Steps:**
1. [First priority from handover]
2. [Second priority]

Ready to continue with [first next step]?
```

### Step 5: Get Confirmation
Wait for user to confirm the approach before starting work.

### Step 6: Begin Work
Once confirmed:
- Create a todo list
- Start with the first next step
- Apply learnings throughout

## Handling Edge Cases

**State has diverged:**
```
I notice the current state differs from the handover:

Handover says: [expected state]
Current state: [actual state]

How would you like to proceed?
```

**Handover is stale:**
```
This handover is from [date], and significant changes have occurred since.

Want me to:
1. Follow the handover as written
2. Adapt based on current state
3. Create a fresh plan
```

**Linked docs missing:**
```
The handover references these docs that I can't find:
- .docs/plans/missing-plan.md

Should I proceed without them?
```

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I read the summary" | Read the full handover. Details matter. |
| "State probably hasn't changed" | Verify anyway. Time passes. |
| "I'll check files as I go" | Upfront verification prevents wasted work. |

## Integration Points

- Consumes handovers from `/handing-over`
- References plans from `/planning-code`
- Links to research from `/researching-code`

## File Reference

- Main: `~/.claude/skills/taking-over/SKILL.md`
