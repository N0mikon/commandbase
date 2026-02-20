---
name: planning-services
description: "Use this skill when creating or iterating on implementation plans for homelab service changes. This includes phased deployment plans with success criteria, rollback steps, and verification checklists. Activate when the user says 'plan services', 'create deployment plan', 'implementation plan for services', or provides a path to an existing services plan in .docs/plans/."
---

# Planning Services

You are creating or updating service implementation plans through an interactive, iterative process. Be skeptical, thorough, and work collaboratively with the user to produce high-quality infrastructure task specifications.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PLAN WITHOUT INFRASTRUCTURE RESEARCH FIRST
```

If you haven't explored the homelab repo using file-system tools and examined the results, you cannot write the plan.

**No exceptions:**
- Don't plan from memory - explore the homelab repo with tools
- Don't skip exploration for "simple" changes - simple changes touch complex dependency chains
- Don't assume service topology - verify in THIS repo
- Don't write the plan before ALL exploration is complete

## The Gate Function

```
BEFORE writing any service implementation plan:

1. IDENTIFY: What aspects of the infrastructure need investigation?
2. EXPLORE: Use file-system Glob/Grep/Read to verify current repo state
3. WAIT: All exploration must complete before proceeding
4. READ: Read all upstream artifacts (research, design, structure docs)
5. VERIFY: Do you have specific file/config references for affected services?
   - If NO: Explore further to get specific references
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

**If a task description or infrastructure requirements are provided:**
- Skip the default message
- Read any provided files FULLY
- Detect upstream BRDSPI artifacts (see Input Detection below)
- Begin the research process

### Input Detection

When invoked, check for upstream services BRDSPI artifacts:
1. If a `.docs/structure/` file with services tags is provided or referenced → **Structured mode**: use structural map as skeleton for plan phases
2. If a `.docs/design/` file with services tags is provided but no structure → suggest running `/structuring-services` first, but proceed if user prefers
3. If neither → **Standalone mode**: works as before (full research + planning)

**If no parameters provided:**
```
I'll help you create a detailed service implementation plan. Let me start by understanding what we're changing.

Please provide:
1. The infrastructure task description or reference to a requirements file
2. Any relevant context, constraints, or specific requirements
3. Links to related research, design, or structure documents

I'll analyze this information and work with you to create a comprehensive plan.

Tip: To update an existing plan, provide the path:
/planning-services .docs/plans/MM-DD-YYYY-description.md
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Research

See ./reference/services-research-workflow.md for the full infrastructure research process.

**Summary:**
1. Read all mentioned files immediately and FULLY
2. Explore the homelab repo using file-system tools
3. Read all compose files and configs identified during exploration
4. Present informed understanding with file references
5. Ask only questions exploration couldn't answer

### Step 2: Deep Research & Discovery

After getting initial clarifications:

1. If the user corrects a misunderstanding, explore further to verify
2. Use file-system tools for comprehensive repo exploration
3. Wait for ALL exploration to complete
4. Present findings and options

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

**If structural map is available (Structured mode):**
- Derive phase boundaries from the structural map's file groups or migration steps
- Each structural group/migration step becomes a candidate implementation phase
- Focus on: task breakdown, success criteria, commands to execute, rollback commands
- Do NOT re-decide organization — honor the design doc decisions

**In Structured mode, /planning-services does NOT:**
- Re-debate architectural decisions (those are in the design doc)
- Re-organize file layout (that's in the structural map)
- Re-research infrastructure architecture (structure already provides this)

It DOES still:
- Explore the repo to verify current state matches structural map assumptions
- Break structural map into atomic, verifiable implementation phases
- Define success criteria for each phase
- Generate Commands to Execute and Rollback Commands per phase
- Identify risks and dependencies between phases

### Step 4: Detailed Plan Writing

After structure approval:

1. **Spawn a `docs-writer` agent** via the Task tool to create the plan file:

   ```
   Task prompt:
     doc_type: "plan"
     topic: "<infrastructure task name>"
     tags: [services, implementation, <relevant aspect tags>]
     references: [<key repo files this plan will modify>]
     content: |
       <compiled plan using the body sections from ./templates/services-plan-template.md>
   ```

   The agent handles frontmatter, file naming, and directory creation.

2. **Body sections** — use the template at ./templates/services-plan-template.md

**Services-specific plan features:**
- Each phase includes "Config Changes" — what files to create/modify/move
- Each phase includes "Commands to Execute" — deployment commands for USER to run (hands-off)
- Each phase includes "Rollback Commands" — how to undo if something goes wrong
- Each phase includes "Verification Checklist" — how to confirm the phase worked
- Success criteria reference service reachability, not test passing

### Step 5: Review

1. **Present the draft plan location**:
   ```
   I've created the service implementation plan at:
   `.docs/plans/MM-DD-YYYY-description.md`

   Please review it and let me know:
   - Are the phases properly scoped?
   - Are the commands correct for your environment?
   - Are the rollback steps sufficient?
   - Missing edge cases or considerations?
   ```

2. **Iterate based on feedback**

3. **Suggest baseline checkpoint**:
   ```
   Plan finalized at `.docs/plans/[filename].md`

   Would you like to create a checkpoint before implementation?
   /bookmarking-code create "plan-approved"

   This captures the pre-implementation state, enabling:
   - Comparison after each /implementing-services phase
   - Full delta review during validation
   - Rollback reference if needed
   ```

## Important Guidelines

1. **Be Skeptical**: Question vague requirements. Identify potential issues early. Don't assume - verify with tools.

2. **Be Interactive**: Don't write the full plan in one shot. Get buy-in at each major step.

3. **Be Thorough**: Read all context files COMPLETELY. Include specific file references.

4. **Be Practical**: Focus on incremental, verifiable changes. Include "what we're NOT doing".

5. **Commands are for the user**: All deployment commands in the plan are marked for USER execution. The plan generates commands, never executes them.

6. **Rollback is mandatory**: Every phase must have rollback commands. No exceptions.

7. **No Open Questions in Final Plan**: If you encounter open questions during planning, STOP. Research or ask for clarification immediately. The plan must be complete and actionable.

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Research First

If you notice any of these, STOP immediately:

- About to write plan without exploring the repo
- Using "typically", "usually", "in most setups" about THIS infrastructure
- Planning changes without file references
- Assuming repo structure without verification
- Thinking "I remember the repo layout"
- Feeling like research "takes too long"
- Writing a phase without Commands to Execute
- Writing a phase without Rollback Commands
- Including .env values instead of referencing .env.example

**When you hit a red flag:**
1. Stop and acknowledge the assumption
2. Explore the repo with file-system tools
3. Wait for results
4. Only then continue planning

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this infrastructure" | Your knowledge is stale. Explore with tools. Verify. |
| "This is a simple change" | Simple changes touch complex dependency chains. Research. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |
| "User gave detailed requirements" | Users know what they want, not how the repo is structured. Verify. |
| "Rollback isn't needed for this phase" | Every phase needs rollback. Murphy's Law applies to infrastructure. |
| "Commands are obvious" | Write them out. Obvious to you ≠ correct for their setup. |

## The Bottom Line

**No shortcuts for planning.**

Explore the repo. Wait for results. Cite file references. Include commands AND rollback. THEN plan.

This is non-negotiable. Every plan. Every time.
