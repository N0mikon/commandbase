---
name: handing-over
description: "Use this skill when ending a session, switching context, or preparing for another session to continue your work. This includes documenting current progress, capturing open questions, listing modified files, and writing handover documents to .docs/handoffs/. Trigger phrases: '/handover', 'hand this off', 'document where we are', 'save progress for later', 'end session'."
---

# Handover

You are creating a handover document to pass your work to another session (or yourself later). The goal is to distill your context to its essential elements - what matters, what you learned, what's next.

This is NOT a lossy auto-summary. This is intelligent extraction of crucial context.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO HANDOVER WITHOUT KEY LEARNINGS
```

If you haven't captured what you learned (not just what you did), the handover is incomplete.

**No exceptions:**
- Don't just list tasks - capture insights
- Don't skip learnings because "nothing special happened"
- Don't hand over without file:line references
- Don't assume the next session knows anything

## The Gate Function

```
BEFORE writing the handover document:

1. REVIEW: What tasks were worked on?
2. EXTRACT: What were the KEY LEARNINGS?
   - Patterns discovered
   - Gotchas encountered
   - Decisions made and WHY
3. REFERENCE: What file:line locations matter?
4. PRIORITIZE: What should the next session do FIRST?
5. VERIFY: Is "Key Learnings" section substantive?
   - If NO: Think harder - every session teaches something
   - If YES: Proceed to write
6. ONLY THEN: Write the handover document

Skip learnings = useless handover
```

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

Spawn a `docs-writer` agent via the Task tool to create the handover file:

```
Task prompt:
  doc_type: "handoff"
  topic: "<brief description of work>"
  tags: [<relevant component names>]
  references: [<key files worked on>]
  content: |
    <compiled handover using the body sections below>
```

The agent handles frontmatter, file naming (`MM-DD-YYYY-description.md`), and directory creation.

**Body sections to include in `content`:**

```markdown
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
/taking-over .docs/handoffs/MM-DD-YYYY-description.md
```

## Red Flags - STOP and Extract Learnings

If you notice any of these, STOP immediately:

- Key Learnings section is empty or generic
- Writing "nothing special to note"
- Listing only tasks without insights
- No file:line references in the handover
- Handover reads like a status report, not a knowledge transfer

**When you hit a red flag:**
1. Stop and reflect on the session
2. What would you tell a colleague taking over?
3. What mistakes should they avoid?
4. Add these insights to Key Learnings

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Nothing special happened" | Every session teaches something. Find it. |
| "Next session can figure it out" | That wastes time. Capture it now. |
| "It's all in the code" | Context and reasoning aren't in code. Document. |
| "I'm in a hurry" | Hurried handovers cause rework. Take time. |

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

## The Bottom Line

**No shortcuts for handover.**

Distill the learnings. Cite file:line references. Write for someone with zero context.

This is non-negotiable. Every handover. Every time.
