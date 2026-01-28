---
description: Create or iterate on implementation plans with thorough research
model: opus
---

# Implementation Plan

You are tasked with creating or updating implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

## Initial Response

When this command is invoked, determine the mode:

### Mode A: Iterate on Existing Plan

**If a path to an existing plan in `.docs/plans/` is provided:**

1. Read the existing plan FULLY
2. Ask what changes the user wants:
   ```
   I've read the plan at `.docs/plans/[filename].md`

   Current phases:
   1. [Phase 1 name]
   2. [Phase 2 name]
   ...

   What would you like to change?
   - Add/remove/modify phases
   - Update success criteria
   - Adjust scope
   - Other changes
   ```
3. Research if needed to validate the changes
4. Make surgical edits (don't rewrite the whole plan)
5. Present the changes made

**Iterate Guidelines:**
- Be surgical - precise edits, not wholesale rewrites
- Preserve good content that doesn't need changing
- Only research what's necessary for specific changes
- Confirm understanding before making changes

### Mode B: Create New Plan

**If a task description or requirements file is provided:**
- Skip the default message
- Read any provided files FULLY
- Begin the research process

**If no parameters provided:**
```
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task description or reference to a requirements file
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.

Tip: To update an existing plan, provide the path:
/pcode .docs/plans/MM-DD-YYYY-description.md
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Requirements documents
   - Research documents
   - Related implementation plans
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: DO NOT spawn sub-tasks before reading these files yourself in the main context
   - **NEVER** read files partially - if a file is mentioned, read it completely

2. **Spawn initial research tasks to gather context**:
   Before asking the user any questions, use specialized agents to research in parallel:

   - Use the **codebase-locator** agent to find all files related to the task
   - Use the **codebase-analyzer** agent to understand how the current implementation works

   These agents will:
   - Find relevant source files, configs, and tests
   - Identify the specific directories to focus on
   - Trace data flow and key functions
   - Return detailed explanations with file:line references

3. **Read all files identified by research tasks**:
   - After research tasks complete, read ALL files they identified as relevant
   - Read them FULLY into the main context
   - This ensures you have complete understanding before proceeding

4. **Analyze and verify understanding**:
   - Cross-reference the requirements with actual code
   - Identify any discrepancies or misunderstandings
   - Note assumptions that need verification
   - Determine true scope based on codebase reality

5. **Present informed understanding and focused questions**:
   ```
   Based on the requirements and my research of the codebase, I understand we need to [accurate summary].

   I've found that:
   - [Current implementation detail with file:line reference]
   - [Relevant pattern or constraint discovered]
   - [Potential complexity or edge case identified]

   Questions that my research couldn't answer:
   - [Specific technical question that requires human judgment]
   - [Business logic clarification]
   - [Design preference that affects implementation]
   ```

   Only ask questions that you genuinely cannot answer through code investigation.

### Step 2: Research & Discovery

After getting initial clarifications:

1. **If the user corrects any misunderstanding**:
   - DO NOT just accept the correction
   - Spawn new research tasks to verify the correct information
   - Read the specific files/directories they mention
   - Only proceed once you've verified the facts yourself

2. **Create a research todo list** using TodoWrite to track exploration tasks

3. **Spawn parallel sub-tasks for comprehensive research**:
   - Create multiple Task agents to research different aspects concurrently
   - Use the right agent for each type of research:

   **For deeper investigation:**
   - **codebase-locator** - To find more specific files (e.g., "find all files that handle [specific component]")
   - **codebase-analyzer** - To understand implementation details (e.g., "analyze how [system] works")
   - **codebase-pattern-finder** - To find similar features we can model after

   **For historical context:**
   - **docs-locator** - To find existing research, plans, or decisions in `.docs/`
   - **docs-analyzer** - To extract key insights from the most relevant documents

   Each agent knows how to:
   - Find the right files and code patterns
   - Identify conventions and patterns to follow
   - Look for integration points and dependencies
   - Return specific file:line references
   - Find tests and examples

4. **Wait for ALL sub-tasks to complete** before proceeding

5. **Present findings and design options**:
   ```
   Based on my research, here's what I found:

   **Current State:**
   - [Key discovery about existing code]
   - [Pattern or convention to follow]

   **Design Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]

   **Open Questions:**
   - [Technical uncertainty]
   - [Design decision needed]

   Which approach aligns best with your vision?
   ```

### Step 3: Plan Structure Development

Once aligned on approach:

1. **Create initial plan outline**:
   ```
   Here's my proposed plan structure:

   ## Overview
   [1-2 sentence summary]

   ## Implementation Phases:
   1. [Phase name] - [what it accomplishes]
   2. [Phase name] - [what it accomplishes]
   3. [Phase name] - [what it accomplishes]

   Does this phasing make sense? Should I adjust the order or granularity?
   ```

2. **Get feedback on structure** before writing details

### Step 4: Detailed Plan Writing

After structure approval:

1. **Write the plan** to `.docs/plans/MM-DD-YYYY-description.md`
   - Create `.docs/plans/` directory if it doesn't exist
   - Format: `MM-DD-YYYY-description.md` where:
     - MM-DD-YYYY is today's date
     - description is a brief kebab-case description
   - Examples:
     - `01-27-2026-user-authentication.md`
     - `01-27-2026-improve-error-handling.md`

2. **Use this template structure**:

````markdown
---
git_commit: [current HEAD commit hash]
last_updated: [YYYY-MM-DD]
last_updated_by: [user or agent name]
topic: "[Feature/Task Name]"
tags: [plan, implementation, relevant-component-names]
status: draft
references:
  - [list of key files this plan will modify]
---

# [Feature/Task Name] Implementation Plan

## Overview

[Brief description of what we're implementing and why]

## Current State Analysis

[What exists now, what's missing, key constraints discovered]

## Desired End State

[A Specification of the desired end state after this plan is complete, and how to verify it]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach

[High-level strategy and reasoning]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

```[language]
// Specific code to add/modify
```

### Success Criteria:
- [ ] Unit tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Integration tests pass

---

## Phase 2: [Descriptive Name]

[Similar structure with success criteria...]

---

## Testing Strategy

### Unit Tests:
- [What to test]
- [Key edge cases]

### Integration Tests:
- [End-to-end scenarios]

## Performance Considerations

[Any performance implications or optimizations needed]

## Migration Notes

[If applicable, how to handle existing data/systems]

## References

- [Link to requirements or related documents]
- Similar implementation: `[file:line]`
````

### Step 5: Review

1. **Present the draft plan location**:
   ```
   I've created the initial implementation plan at:
   `.docs/plans/MM-DD-YYYY-description.md`

   Please review it and let me know:
   - Are the phases properly scoped?
   - Are the success criteria specific enough?
   - Any technical details that need adjustment?
   - Missing edge cases or considerations?
   ```

2. **Iterate based on feedback** - be ready to:
   - Add missing phases
   - Adjust technical approach
   - Clarify success criteria
   - Add/remove scope items

3. **Continue refining** until the user is satisfied

## Important Guidelines

1. **Be Skeptical**:
   - Question vague requirements
   - Identify potential issues early
   - Ask "why" and "what about"
   - Don't assume - verify with code

2. **Be Interactive**:
   - Don't write the full plan in one shot
   - Get buy-in at each major step
   - Allow course corrections
   - Work collaboratively

3. **Be Thorough**:
   - Read all context files COMPLETELY before planning
   - Research actual code patterns using parallel sub-tasks
   - Include specific file paths and line numbers
   - Write measurable, automated success criteria

4. **Be Practical**:
   - Focus on incremental, testable changes
   - Consider migration and rollback
   - Think about edge cases
   - Include "what we're NOT doing"

5. **Track Progress**:
   - Use TodoWrite to track planning tasks
   - Update todos as you complete research
   - Mark planning tasks complete when done

6. **No Open Questions in Final Plan**:
   - If you encounter open questions during planning, STOP
   - Research or ask for clarification immediately
   - Do NOT write the plan with unresolved questions
   - The implementation plan must be complete and actionable
   - Every decision must be made before finalizing the plan

## Success Criteria Guidelines

**Success criteria should be automated and verifiable:**

- Commands that can be run: test commands, lint commands, etc.
- Specific files that should exist
- Code compilation/type checking
- Automated test suites
- API responses or CLI output verification

## Common Patterns

### For Database Changes:
- Start with schema/migration
- Add store methods
- Update business logic
- Expose via API
- Update clients

### For New Features:
- Research existing patterns first
- Start with data model
- Build backend logic
- Add API endpoints
- Implement UI last

### For Refactoring:
- Document current behavior
- Plan incremental changes
- Maintain backwards compatibility
- Include migration strategy

## Sub-task Spawning Best Practices

When spawning research sub-tasks:

1. **Spawn multiple tasks in parallel** for efficiency
2. **Each task should be focused** on a specific area
3. **Provide detailed instructions** including:
   - Exactly what to search for
   - Which directories to focus on
   - What information to extract
   - Expected output format
4. **Specify read-only tools** to use
5. **Request specific file:line references** in responses
6. **Wait for all tasks to complete** before synthesizing
7. **Verify sub-task results**:
   - If a sub-task returns unexpected results, spawn follow-up tasks
   - Cross-check findings against the actual codebase
   - Don't accept results that seem incorrect

## Example Interaction Flows

### Creating a New Plan
```
User: /pcode
Assistant: I'll help you create a detailed implementation plan...

User: We need to add user authentication to the app
Assistant: Let me research the codebase first...

[Spawns research agents]

Based on my research, I understand we need to add authentication. I've found that the app currently has no auth middleware...

[Interactive process continues...]
```

### Iterating on Existing Plan
```
User: /pcode .docs/plans/01-27-2026-auth-implementation.md
Assistant: I've read the plan. Current phases:
1. Database schema for users
2. Authentication middleware
3. Login/logout endpoints

What would you like to change?

User: Add a phase for password reset functionality
Assistant: I'll add a new phase for password reset. Let me research the email setup first...

[Researches, then makes surgical edit to add Phase 4]

I've updated the plan with a new Phase 4: Password Reset
- Added email service integration
- Added reset token generation
- Added reset endpoint

Would you like any other changes?
```
