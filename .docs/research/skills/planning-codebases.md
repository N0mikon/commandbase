# Research: planning-codebases Skill

## Overview

The `planning-codebases` skill (`~/.claude/skills/planning-codebases/SKILL.md`) creates or iterates on implementation plans through an interactive, research-first process. It enforces mandatory codebase research before planning using an Iron Law and Gate Function that prevents planning from memory or assumptions.

**Trigger phrases**: `create a plan`, `implementation plan`, `plan this feature`, or provide a path to an existing plan in `.docs/plans/`

## The Iron Law (SKILL.md:12-24)

```
NO PLAN WITHOUT CODEBASE RESEARCH FIRST
```

**Absolute requirements:**
- Cannot plan from memory - must spawn codebase-locator and codebase-analyzer agents
- Cannot skip research for "simple" changes
- Cannot assume patterns - must verify them in THIS codebase
- Cannot write the plan before ALL research agents complete

## The Gate Function (SKILL.md:26-41)

6-step mandatory checkpoint before writing any plan:

1. **IDENTIFY**: What aspects of the codebase need investigation?
2. **SPAWN**: Create parallel research agents (minimum 2: codebase-locator + codebase-analyzer)
3. **WAIT**: All agents must complete before proceeding
4. **READ**: Read ALL files identified by agents into main context
5. **VERIFY**: Check for file:line references for integration points
6. **ONLY THEN**: Write the implementation plan

## Two Operating Modes

### Mode A: Iterate on Existing Plan
- Triggered when a path to `.docs/plans/*.md` is provided
- Reads the existing plan fully
- Makes surgical edits without rewriting entire plan
- Only researches what's necessary for specific changes

### Mode B: Create New Plan
- Triggered by task description or requirements file
- Reads mentioned files fully
- Spawns research agents before planning
- Produces phased plan with success criteria

## Research Agent Spawning

### Initial Research
1. Read all mentioned files immediately and FULLY
2. Spawn initial research tasks in parallel:
   - **codebase-locator**: Find all files related to the task
   - **codebase-analyzer**: Understand how current implementation works
3. Read all files identified by research tasks
4. Present informed understanding with file:line references

### Deep Research
- **codebase-pattern-finder**: Find similar features to model after
- **docs-locator**: Find existing research, plans, or decisions
- **docs-analyzer**: Extract key insights from relevant documents

## Plan Document Format

**Location**: `.docs/plans/MM-DD-YYYY-description.md`

**Structure:**
```markdown
---
git_commit: [current HEAD]
last_updated: [YYYY-MM-DD]
topic: "[Feature/Task Name]"
tags: [plan, implementation, relevant-tags]
status: draft
references:
  - [key files this plan will modify]
---

# [Feature Name] Implementation Plan

## Overview
[Brief description]

## Current State Analysis
[What exists now, what's missing]

## Desired End State
[Specification and verification criteria]

## What We're NOT Doing
[Explicitly out-of-scope items]

## Phase 1: [Name]
### Overview
### Changes Required
### Success Criteria
- [ ] Automated verification command
- [ ] Specific testable outcome

## Phase 2: [Name]
...
```

## Success Criteria Guidelines

Success criteria must be automated and verifiable:
- Commands that can be run (test commands, lint commands)
- Specific files that should exist
- Code compilation/type checking
- Automated test suites

## Common Implementation Patterns

**Database Changes:**
1. Start with schema/migration
2. Add store methods
3. Update business logic
4. Expose via API
5. Update clients

**New Features:**
1. Research existing patterns first
2. Start with data model
3. Build backend logic
4. Add API endpoints
5. Implement UI last

## Red Flags - Stop Signals

Pause if you notice:
- About to write plan without spawning research agents
- Using "typically", "usually" about THIS codebase
- Planning integration points without file:line references
- Assuming directory structure without verification

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your knowledge is stale. Spawn agents. Verify. |
| "This is a simple change" | Simple changes touch complex systems. Research. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |

## The Bottom Line

**No shortcuts for planning.**

Spawn the agents → Wait for results → Read the files → Cite file:line references → THEN plan

## File References

- Main: `~/.claude/skills/planning-codebases/SKILL.md`
- Research workflow: `~/.claude/skills/planning-codebases/reference/research-workflow.md`
- Plan template: `~/.claude/skills/planning-codebases/templates/plan-template.md`
- Common patterns: `~/.claude/skills/planning-codebases/reference/common-patterns.md`
