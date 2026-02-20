---
name: structuring-code
description: "Use this skill when mapping file placement, module organization, and dependency structure for a feature or refactor. This includes deciding where new files go, how modules connect, what interfaces to define, how tests are organized, and sequencing migrations for brownfield work. Activate when the user says 'structure this', 'where should files go', 'organize the codebase', or after /designing-code."
---

# Structuring Code

You are mapping file placement, module organization, and dependency structure for a feature or refactor by analyzing design decisions and current codebase patterns, then producing a structural map document.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO STRUCTURE WITHOUT UNDERSTANDING WHAT EXISTS
```

Structure decisions must be grounded in the actual codebase. Spawn agents to verify current file organization before proposing changes.

**No exceptions:**
- Don't propose file locations without checking current patterns
- Don't ignore existing conventions in brownfield work
- Don't include implementation details in the structural map
- Don't create migration steps that leave the codebase broken between steps

## The Gate Function

```
BEFORE writing any structural map:

1. READ: Find and read design doc (.docs/design/) if available
2. RESEARCH: Spawn agents to map current file organization in target area
3. ANALYZE: Compare design decisions to current structure
4. MAP: Determine file placement, module boundaries, dependency direction
5. SEQUENCE: For refactors, determine migration order (each step deployable)
6. WRITE: Create .docs/structure/ document via docs-writer
7. PRESENT: Summary to user with structural map and link

Skipping steps = structuring blind
```

## Initial Response

When this skill is invoked:

### If a design doc is provided or referenced:
- Read the design doc FULLY
- Proceed to Step 2

### If no design doc but user provides requirements directly:
- Proceed in lightweight mode (skip design doc lookup)
- Note: structural maps without design docs are valid for simple features

### If no parameters provided:
```
I'll help you map file placement and module organization.

Please provide:
1. A design document (.docs/design/) or feature description
2. The target area of the codebase (for refactors)

I'll analyze current patterns and create a structural map showing where everything goes.
```

## Process Steps

### Step 1: Gather Context

- Check for design doc in `.docs/design/` — read FULLY if exists
- Check for refactor scope doc in `.docs/refactors/` — read FULLY if exists
- If user provides a target area directly, note it for agent scoping

### Step 2: Analyze Current Structure

Spawn parallel research agents to understand what exists:

- **code-locator** agent: Map current directory structure in the target area — find all files, directories, and naming patterns
- **code-analyzer** agent: Understand current architecture patterns — imports, exports, module boundaries, dependency direction
- **code-librarian** agent: Find test file placement conventions — co-located vs separate, naming patterns, test types used

Wait for ALL agents to complete before proceeding.

Compile findings:
- Current file organization patterns
- Naming conventions in use
- Import/dependency patterns
- Test file placement conventions
- Module boundary patterns

### Step 3: Create Structural Map

For each component from the design doc (or user requirements):

**File placement:**
- Which files to create, modify, or split
- Where new code lives relative to existing files
- Follow existing naming conventions

**Module boundaries:**
- Dependency direction (what imports what)
- Interface boundaries (public vs internal)
- Shared vs module-local code

**Test organization:**
- Test file placement following existing conventions
- Test types per component (unit/integration/e2e)
- Test naming patterns

**Convention deference:**
- For brownfield work: follow existing patterns. Do not propose new conventions.
- For greenfield: propose conventions and confirm with user via AskUserQuestion.

### Step 4: Sequence Migrations (Refactors Only)

For refactors, determine migration order:
- Each step must leave the codebase in a working state
- No step should break existing tests
- Prefer leaf-first ordering (dependencies before dependents)
- Number each step with a description of what changes and what still works after

### Step 5: Write Structural Map

Spawn a `docs-writer` agent via the Task tool:

```
Task prompt:
  doc_type: "structure"
  topic: "<feature/system name>"
  tags: [<relevant component tags>]
  references: [<design doc, key files affected>]
  content: |
    <compiled structural map using ./templates/structural-map-template.md>
```

The structural map must contain:
- File tree visualization (current and proposed)
- New files with purpose descriptions
- Modified files with change descriptions
- Module boundary diagram
- Test organization plan
- Migration steps (refactors only)
- NO implementation details — no code, no function bodies, no algorithms

### Step 6: Present and Suggest Next Step

```
STRUCTURE COMPLETE
==================

Structural map: .docs/structure/MM-DD-YYYY-<topic>.md

Files affected: [count]
New files: [list]
Modified files: [list]
Migration steps: [count, if refactor]

Next: /planning-code to break this into phased implementation tasks
```

## Important Guidelines

1. **Structure captures WHERE, not WHAT** — file placement and organization, no implementation details
2. **Research current patterns** — spawn agents before proposing anything
3. **Defer to conventions** — in brownfield work, follow what exists
4. **Every migration step must work** — no broken intermediate states
5. **Dependency direction matters** — document what imports what

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Research

If you notice any of these, pause:

- Proposing file structure without researching current patterns
- Ignoring existing conventions in brownfield work
- Including implementation details (actual code) in the structural map
- Creating migration steps that leave the codebase broken between steps
- Assuming directory structure without spawning agents to verify
- Proposing new conventions in brownfield without acknowledging existing ones

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know the standard structure for this" | THIS codebase has its own patterns. Research them. |
| "The design doc already specifies structure" | Design says WHAT. Structure says WHERE. Different concerns. |
| "Migration order doesn't matter" | Every step must leave things working. Order is the hard problem. |
| "This is too simple for a structural map" | Simple structures still need documenting for the planning phase. |
| "I can see the directory layout" | Spawn agents. Directory layout alone doesn't reveal dependency direction. |

## The Bottom Line

**Structure captures WHERE everything goes, not WHAT it does.**

File placement, module organization, dependency direction. Defer to existing patterns in brownfield.

This is non-negotiable. Every structure. Every time.
