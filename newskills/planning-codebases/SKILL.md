---
name: planning-codebases
description: "Create or iterate on implementation plans with thorough codebase research. Use when the user says 'create a plan', 'implementation plan', 'plan this feature', or provides a path to an existing plan in .docs/plans/. Spawns research agents before planning, produces phased plans with success criteria."
---

# Implementation Planning

You are creating or updating implementation plans through an interactive, iterative process. Be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PLAN WITHOUT CODEBASE RESEARCH FIRST
```

If you haven't spawned research agents and read the results, you cannot write the plan.

**No exceptions:**
- Don't plan from memory - spawn code-locator and code-analyzer agents
- Don't skip research for "simple" changes - simple changes touch complex systems
- Don't assume patterns - verify them in THIS codebase
- Don't write the plan before ALL research agents complete

## The Gate Function

```
BEFORE writing any implementation plan:

1. IDENTIFY: What aspects of the codebase need investigation?
2. SPAWN: Create parallel research agents (minimum 2: code-locator + code-analyzer)
3. WAIT: All agents must complete before proceeding
4. READ: Read ALL files identified by agents into main context
5. VERIFY: Do you have file:line references for integration points?
   - If NO: Spawn follow-up agents to get specific references
   - If YES: Proceed to planning
6. ONLY THEN: Write the implementation plan

Skipping steps = planning blind
```

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
/planning-codebases .docs/plans/MM-DD-YYYY-description.md
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Research

See ./reference/research-workflow.md for the full research process.

**Summary:**
1. Read all mentioned files immediately and FULLY
2. Spawn initial research agents (code-locator, code-analyzer)
3. Read all files identified by research tasks
4. Present informed understanding with file:line references
5. Ask only questions research couldn't answer

### Step 2: Deep Research & Discovery

After getting initial clarifications:

1. If the user corrects a misunderstanding, spawn new research to verify
2. Create a research todo list using TodoWrite
3. Spawn parallel sub-tasks for comprehensive research
4. Wait for ALL sub-tasks to complete
5. Present findings and design options

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
   - Format: `MM-DD-YYYY-description.md`

2. **Use the template** at ./templates/plan-template.md

3. **Reference common patterns** at ./reference/common-patterns.md

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

2. **Iterate based on feedback**

3. **Suggest baseline checkpoint**:
   ```
   Plan finalized at `.docs/plans/[filename].md`

   Would you like to create a checkpoint before implementation?
   /checkpointing create "plan-approved"

   This captures the pre-implementation state, enabling:
   - Comparison after each /implementing-plans phase
   - Full delta review during /validating-implementations
   - Rollback reference if needed
   ```

## Important Guidelines

1. **Be Skeptical**: Question vague requirements. Identify potential issues early. Don't assume - verify with code.

2. **Be Interactive**: Don't write the full plan in one shot. Get buy-in at each major step.

3. **Be Thorough**: Read all context files COMPLETELY. Include specific file paths and line numbers.

4. **Be Practical**: Focus on incremental, testable changes. Include "what we're NOT doing".

5. **No Open Questions in Final Plan**: If you encounter open questions during planning, STOP. Research or ask for clarification immediately. The plan must be complete and actionable.

## Red Flags - STOP and Research First

If you notice any of these, STOP immediately:

- About to write plan without spawning research agents
- Using "typically", "usually", "in most codebases" about THIS codebase
- Planning integration points without file:line references
- Assuming directory structure without verification
- Thinking "I remember where this is"
- Feeling like research "takes too long"

**When you hit a red flag:**
1. Stop and acknowledge the assumption
2. Spawn the appropriate research agents
3. Wait for results and read the files
4. Only then continue planning

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your knowledge is stale. Spawn agents. Verify. |
| "This is a simple change" | Simple changes touch complex systems. Research integration points. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |
| "User gave detailed requirements" | Users know what they want, not how the code works. Verify. |
| "I've done this in other projects" | THIS codebase has its own patterns. Find them. |

## Example Interaction Flows

### Creating a New Plan
```
User: /planning-codebases
Assistant: I'll help you create a detailed implementation plan...

User: We need to add user authentication to the app
Assistant: Let me research the codebase first...

[Spawns research agents]

Based on my research, I understand we need to add authentication. I've found that the app currently has no auth middleware...

[Interactive process continues...]
```

### Iterating on Existing Plan
```
User: /planning-codebases .docs/plans/01-27-2026-auth-implementation.md
Assistant: I've read the plan. Current phases:
1. Database schema for users
2. Authentication middleware
3. Login/logout endpoints

What would you like to change?

User: Add a phase for password reset functionality
Assistant: I'll add a new phase for password reset. Let me research the email setup first...

[Researches, then makes surgical edit to add Phase 4]
```

## The Bottom Line

**No shortcuts for planning.**

Spawn the agents. Wait for results. Read the files. Cite file:line references. THEN plan.

This is non-negotiable. Every plan. Every time.
