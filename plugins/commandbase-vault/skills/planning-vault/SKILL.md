---
name: planning-vault
description: "Create or iterate on vault implementation plans with thorough vault research. Use when the user says 'plan vault changes', 'vault implementation plan', 'plan vault reorganization', or provides a path to an existing vault plan in .docs/plans/. Researches vault structure before planning, produces phased plans with success criteria."
---

# Planning Vault

You are creating or updating vault implementation plans through an interactive, iterative process. Be skeptical, thorough, and work collaboratively with the user to produce high-quality vault task specifications.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PLAN WITHOUT VAULT RESEARCH FIRST
```

If you haven't explored the vault using MCP tools and/or file-system tools and examined the results, you cannot write the plan.

**No exceptions:**
- Don't plan from memory - explore the vault with tools
- Don't skip exploration for "simple" changes - simple changes touch complex link structures
- Don't assume vault patterns - verify them in THIS vault
- Don't write the plan before ALL exploration is complete

## The Gate Function

```
BEFORE writing any vault implementation plan:

1. IDENTIFY: What aspects of the vault need investigation?
2. EXPLORE: Use MCP tools and/or file-system Glob/Grep/Read to verify current vault state
3. WAIT: All exploration must complete before proceeding
4. READ: Read all vault artifacts (research, design, structure docs)
5. VERIFY: Do you have specific note/folder references for affected areas?
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

**If a task description or vault requirements are provided:**
- Skip the default message
- Read any provided files FULLY
- Detect upstream BRDSPI artifacts (see Input Detection below)
- Begin the research process

### Input Detection

When invoked, check for upstream vault BRDSPI artifacts:
1. If a `.docs/structure/` file with vault tags is provided or referenced → **Structured mode**: use structural map as skeleton for plan phases
2. If a `.docs/design/` file with vault tags is provided but no structure → suggest running `/structuring-vault` first, but proceed if user prefers
3. If neither → **Standalone mode**: works as before (full research + planning)

**If no parameters provided:**
```
I'll help you create a detailed vault implementation plan. Let me start by understanding what we're changing.

Please provide:
1. The vault task description or reference to a requirements file
2. Any relevant context, constraints, or specific requirements
3. Links to related research, design, or structure documents

I'll analyze this information and work with you to create a comprehensive plan.

Tip: To update an existing plan, provide the path:
/planning-vault .docs/plans/MM-DD-YYYY-description.md
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Research

See ./reference/research-workflow.md for the full vault research process.

**Summary:**
1. Read all mentioned files immediately and FULLY
2. Explore the vault using MCP tools and/or file-system tools
3. Read all notes/folders identified during exploration
4. Present informed understanding with note/folder references
5. Ask only questions exploration couldn't answer

### Step 2: Deep Research & Discovery

After getting initial clarifications:

1. If the user corrects a misunderstanding, explore further to verify
2. Use MCP tools and/or file-system tools for comprehensive vault exploration
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
- Derive phase boundaries from the structural map's folder groups or migration steps
- Each structural group/migration step becomes a candidate implementation phase
- Focus on: task breakdown, success criteria, verification commands
- Do NOT re-decide organization — honor the design doc decisions

**In Structured mode, /planning-vault does NOT:**
- Re-debate organizational decisions (those are in the design doc)
- Re-organize folder layout (that's in the structural map)
- Re-research vault architecture (structure already provides this)

It DOES still:
- Explore the vault to verify current state matches structural map assumptions
- Break structural map into atomic, verifiable implementation phases
- Define success criteria for each phase
- Identify risks and dependencies between phases

### Step 4: Detailed Plan Writing

After structure approval:

1. **Spawn a `docs-writer` agent** via the Task tool to create the plan file:

   ```
   Task prompt:
     doc_type: "plan"
     topic: "<vault task name>"
     tags: [vault, implementation, <relevant aspect tags>]
     references: [<key vault paths this plan will modify>]
     content: |
       <compiled plan using the body sections from ./templates/vault-plan-template.md>
   ```

   The agent handles frontmatter, file naming, and directory creation.

2. **Body sections** — use the template at ./templates/vault-plan-template.md

### Step 5: Review

1. **Present the draft plan location**:
   ```
   I've created the vault implementation plan at:
   `.docs/plans/MM-DD-YYYY-description.md`

   Please review it and let me know:
   - Are the phases properly scoped?
   - Are the success criteria specific enough?
   - Any vault-specific details that need adjustment?
   - Missing edge cases or considerations?
   ```

2. **Iterate based on feedback**

3. **Suggest baseline checkpoint**:
   ```
   Plan finalized at `.docs/plans/[filename].md`

   Would you like to create a checkpoint before implementation?
   /bookmarking-code create "plan-approved"

   This captures the pre-implementation state, enabling:
   - Comparison after each /implementing-vault phase
   - Full delta review during validation
   - Rollback reference if needed
   ```

## Important Guidelines

1. **Be Skeptical**: Question vague requirements. Identify potential issues early. Don't assume - verify with tools.

2. **Be Interactive**: Don't write the full plan in one shot. Get buy-in at each major step.

3. **Be Thorough**: Read all context files COMPLETELY. Include specific note/folder references.

4. **Be Practical**: Focus on incremental, verifiable changes. Include "what we're NOT doing".

5. **No Open Questions in Final Plan**: If you encounter open questions during planning, STOP. Research or ask for clarification immediately. The plan must be complete and actionable.

## Red Flags - STOP and Research First

If you notice any of these, STOP immediately:

- About to write plan without exploring the vault
- Using "typically", "usually", "in most vaults" about THIS vault
- Planning changes without note/folder references
- Assuming vault structure without verification
- Thinking "I remember the vault layout"
- Feeling like research "takes too long"

**When you hit a red flag:**
1. Stop and acknowledge the assumption
2. Explore the vault with appropriate tools
3. Wait for results
4. Only then continue planning

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this vault" | Your knowledge is stale. Explore with tools. Verify. |
| "This is a simple change" | Simple changes touch complex link structures. Research. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |
| "User gave detailed requirements" | Users know what they want, not how the vault is structured. Verify. |
| "I've organized other vaults" | THIS vault has its own patterns. Find them. |

## The Bottom Line

**No shortcuts for planning.**

Explore the vault. Wait for results. Cite note/folder references. THEN plan.

This is non-negotiable. Every plan. Every time.
