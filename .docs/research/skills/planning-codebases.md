---
date: 2026-02-09
status: current
topic: "planning-code skill analysis"
tags: [research, skill, planning-code, commandbase-code, BRDSPI]
git_commit: 56416f1
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after plugin conversion - refreshed file paths, added BRDSPI integration, staleness auto-update, docs-writer delegation, structured mode, and checkpoint suggestion"
references:
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/planning-code/reference/research-workflow.md
  - plugins/commandbase-code/skills/planning-code/templates/plan-template.md
  - plugins/commandbase-code/skills/planning-code/reference/common-patterns.md
---

# Research: planning-code Skill

## Overview

The `planning-code` skill (`plugins/commandbase-code/skills/planning-code/SKILL.md`) creates or iterates on implementation plans through an interactive, research-first process. It enforces mandatory codebase research before planning using an Iron Law and Gate Function that prevents planning from memory or assumptions.

**Trigger phrases**: `create a plan`, `implementation plan`, `plan this feature`, or provide a path to an existing plan in `.docs/plans/`

**Plugin**: `commandbase-code`

## The Iron Law (SKILL.md:12-24)

```
NO PLAN WITHOUT CODEBASE RESEARCH FIRST
```

**Absolute requirements:**
- Cannot plan from memory - must spawn code-locator and code-analyzer agents
- Cannot skip research for "simple" changes
- Cannot assume patterns - must verify them in THIS codebase
- Cannot write the plan before ALL research agents complete

## The Gate Function (SKILL.md:26-41)

6-step mandatory checkpoint before writing any plan:

1. **IDENTIFY**: What aspects of the codebase need investigation?
2. **SPAWN**: Create parallel research agents (minimum 2: code-locator + code-analyzer)
3. **WAIT**: All agents must complete before proceeding
4. **READ**: Read ALL files identified by agents into main context
5. **VERIFY**: Check for file:line references for integration points
   - If NO: Spawn follow-up agents to get specific references
   - If YES: Proceed to planning
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
- Detects upstream BRDSPI artifacts (see Input Detection below)
- Spawns research agents before planning
- Produces phased plan with success criteria

## BRDSPI Input Detection

When invoked, the skill checks for upstream BRDSPI artifacts:

1. If a `.docs/structure/` file is provided or referenced: **Structured mode** -- uses structural map as skeleton for plan phases
2. If a `.docs/design/` file is provided but no structure: suggests running `/structuring-code` first, but proceeds if user prefers
3. If neither: **Standalone mode** -- works as before (full research + architecture + planning)

### Staleness Auto-Update

When a `.docs/structure/` or `.docs/design/` file is detected as input, the skill checks its freshness via `git_commit` frontmatter. If >3 commits behind HEAD, it spawns a `docs-updater` agent to refresh the artifact before using it. If the docs-updater archives the artifact, the skill warns the user that the upstream artifact is obsolete and suggests re-running the upstream skill.

## Structured Mode Behavior

When a structural map is available, `/planning-code` changes its behavior:

**It DOES:**
- Spawn code-analyzer agents to verify integration points mentioned in the structural map
- Break structural map into atomic, testable implementation phases
- Define success criteria for each phase
- Identify risks and dependencies between phases

**It does NOT:**
- Re-debate architectural decisions (those are in the design doc)
- Re-organize file placement (that's in the structural map)
- Spawn architecture research agents (structure already provides this)

## Research Agent Spawning

### Initial Research
1. Read all mentioned files immediately and FULLY
2. Spawn initial research tasks in parallel:
   - **code-locator**: Find all files related to the task
   - **code-analyzer**: Understand how current implementation works
3. Read all files identified by research tasks
4. Present informed understanding with file:line references

### Deep Research
- **code-librarian**: Find similar features to model after
- **docs-locator**: Find existing research, plans, or decisions
- **docs-analyzer**: Extract key insights from relevant documents

## Plan Creation via docs-writer

Plan documents are created by spawning a `docs-writer` agent via the Task tool. The agent handles frontmatter, file naming (`MM-DD-YYYY-description.md`), and directory creation. The planning skill provides:
- `doc_type: "plan"`
- `topic`, `tags`, `references`
- `content` compiled from the plan template at `./templates/plan-template.md`

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

## Post-Plan: Checkpoint Suggestion

After a plan is finalized, the skill suggests creating a baseline checkpoint:
```
/bookmarking-code create "plan-approved"
```
This captures the pre-implementation state, enabling comparison after each `/implementing-plans` phase, full delta review during `/validating-code`, and rollback reference if needed.

## Success Criteria Guidelines

Success criteria must be automated and verifiable:
- Commands that can be run (test commands, lint commands)
- Specific files that should exist
- Code compilation/type checking
- Automated test suites
- API responses or CLI output verification

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

**Refactoring:**
1. Document current behavior
2. Plan incremental changes
3. Maintain backwards compatibility
4. Include migration strategy

## Red Flags - Stop Signals

Pause if you notice:
- About to write plan without spawning research agents
- Using "typically", "usually" about THIS codebase
- Planning integration points without file:line references
- Assuming directory structure without verification
- Thinking "I remember where this is"
- Feeling like research "takes too long"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your knowledge is stale. Spawn agents. Verify. |
| "This is a simple change" | Simple changes touch complex systems. Research integration points. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |
| "User gave detailed requirements" | Users know what they want, not how the code works. Verify. |
| "I've done this in other projects" | THIS codebase has its own patterns. Find them. |

## The Bottom Line

**No shortcuts for planning.**

Spawn the agents --> Wait for results --> Read the files --> Cite file:line references --> THEN plan

## File References

- Main: `plugins/commandbase-code/skills/planning-code/SKILL.md`
- Research workflow: `plugins/commandbase-code/skills/planning-code/reference/research-workflow.md`
- Plan template: `plugins/commandbase-code/skills/planning-code/templates/plan-template.md`
- Common patterns: `plugins/commandbase-code/skills/planning-code/reference/common-patterns.md`
