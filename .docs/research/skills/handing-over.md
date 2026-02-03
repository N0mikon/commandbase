# Research: handing-over Skill

## Overview

The `handing-over` skill (`~/.claude/skills/handing-over/SKILL.md`) documents current session state for future sessions to continue. It produces handover documents in `.docs/handoffs/` that capture progress, learnings, and next steps.

**Trigger phrases**: `/handover`, `hand this off`, `document where we are`, `save progress for later`, `end session`

## Purpose

Enable session continuity by capturing:
- What was being worked on
- What was accomplished
- Key learnings discovered
- Current state verification
- Next steps to continue

## Process

### Step 1: Gather Context
- Review conversation history
- Check git status and recent commits
- Identify modified files

### Step 2: Capture Progress
Document:
- Task being worked on
- Work completed
- Work in progress
- Blockers encountered

### Step 3: Extract Learnings
Key insights discovered during session:
- Non-obvious patterns found
- Gotchas encountered
- Workarounds developed

### Step 4: Document State
- Current git branch
- Recent commits
- Modified/created files
- Test status

### Step 5: Define Next Steps
Prioritized list of what to do next:
1. Immediate next action
2. Follow-up tasks
3. Future considerations

## Output Format

Written to `.docs/handoffs/MM-DD-YYYY-description.md`:

```markdown
---
git_commit: [current HEAD]
last_updated: [YYYY-MM-DD]
last_updated_by: claude
topic: "[Brief description]"
tags: [handover, relevant-tags]
status: active
references:
  - [key files modified]
---

# Handover: [Description]

**Date**: [YYYY-MM-DD]
**Branch**: [current branch]

## What I Was Working On

[Description of task]

## What I Accomplished

- [Key accomplishment 1]
- [Key accomplishment 2]

## Key Learnings

1. [Important learning with file:line reference]
2. [Pattern or gotcha discovered]

## Current State

- [Git state verification]
- [Test status]
- [Files modified]

## Next Steps

1. [First priority]
2. [Second priority]
3. [Future consideration]

## Context & References

- Plan: [path to plan if applicable]
- Research: [path to research docs]
```

## Integration Points

- Creates handover for `/taking-over` to consume
- References plans from `/planning-codebases`
- Links to research from `/researching-codebases`

## File Reference

- Main: `~/.claude/skills/handing-over/SKILL.md`
