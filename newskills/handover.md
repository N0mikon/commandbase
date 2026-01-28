---
description: Document current work context for handover to another session
---

# Handover

You are creating a handover document to pass your work to another session (or yourself later). The goal is to distill your context to its essential elements - what matters, what you learned, what's next.

This is NOT a lossy auto-summary. This is intelligent extraction of crucial context.

## Process

### Step 1: Analyze Current Session

Review the conversation and gather:
- What tasks were you working on?
- What did you accomplish?
- What did you learn (patterns, gotchas, discoveries)?
- What files did you create or modify?
- What's the current state?
- What should happen next?

### Step 2: Create Handover Document

Write to `.docs/handoffs/MM-DD-YYYY-description.md`
- Create `.docs/handoffs/` directory if it doesn't exist

**Format:**
- MM-DD-YYYY is today's date
- description is a brief kebab-case description of the work

**Examples:**
- `01-27-2026-auth-implementation.md`
- `01-27-2026-api-refactor.md`
- `01-27-2026-vault-reorganization.md`

**Template:**

```markdown
---
git_commit: [current HEAD commit hash]
last_updated: [YYYY-MM-DD]
last_updated_by: [user or agent name]
topic: "[Brief Description of Work]"
tags: [handover, relevant-component-names]
status: active
references:
  - [list of key files worked on]
---

# Handover: [Brief Description]

**Date**: [Current date and time]
**Branch**: [Current git branch, if applicable]

## What I Was Working On

[Description of the task(s) and their current status]
- Task 1: [status - completed/in-progress/planned]
- Task 2: [status]

## What I Accomplished

[Concrete deliverables and progress made]
- [Accomplishment 1]
- [Accomplishment 2]

## Key Learnings

[Important discoveries that the next session MUST know]
- [Learning 1 - with file:line reference if relevant]
- [Learning 2 - patterns discovered, gotchas found]
- [Learning 3 - why something was done a certain way]

## Files Changed

[List of files created or modified]
- `path/to/file.ext` - [what was done]
- `path/to/another.ext:45-60` - [specific changes]

## Current State

[Where things stand right now]
- [What's working]
- [What's partially done]
- [What's blocked or needs attention]

## Next Steps

[Prioritized list of what should happen next]
1. [Most important next action]
2. [Second priority]
3. [Additional tasks]

## Context & References

[Links to relevant docs, plans, or resources]
- Plan: `.docs/plans/[relevant-plan].md`
- Research: `.docs/research/[relevant-research].md`
- [Other relevant files or URLs]

## Notes

[Anything else the next session should know]
- [Warnings, edge cases, things to watch out for]
- [Decisions made and why]
- [Open questions]
```

### Step 3: Confirm Creation

After writing the document:

```
Handover created at:
.docs/handoffs/MM-DD-YYYY-description.md

To resume this work in a new session:
/takeover .docs/handoffs/MM-DD-YYYY-description.md
```

## Guidelines

1. **Distill, Don't Dump**
   - Extract the essence, not everything
   - Focus on what the next session NEEDS to know
   - Remove noise, keep signal

2. **Be Specific**
   - Use file:line references, not vague descriptions
   - Name specific functions, variables, patterns
   - Include concrete next steps, not "continue working"

3. **Capture Learnings**
   - This is the most valuable part
   - What would you tell a co-worker taking over?
   - What mistakes should they avoid?
   - What patterns should they follow?

4. **Think Continuity**
   - Write for someone with zero context
   - Don't assume they remember anything
   - Make it self-contained

5. **Keep It Concise**
   - Aim for clarity, not length
   - Bullet points over paragraphs
   - Code references over code blocks
