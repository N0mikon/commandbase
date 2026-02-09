---
name: starting-refactors
description: "Use this skill when initializing a brownfield refactor, establishing refactor scope, or capturing the current state before restructuring existing code. This includes defining refactor goals, snapshotting baseline state via checkpoint, auditing the target area, and setting up CLAUDE.md context pointers. Activate when the user says 'refactor this', 'restructure this code', 'start a refactor', or before running BRDSPI on existing code."
---

# Starting Refactors

You are initializing a brownfield refactor by establishing scope, creating a safety checkpoint, and auditing the target area before any restructuring work begins.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO REFACTOR WITHOUT BASELINE FIRST
```

A checkpoint must exist before any refactoring work begins. This captures the pristine pre-refactor state for regression detection and rollback.

**No exceptions:**
- Don't audit before checkpointing - checkpoint captures pristine state
- Don't start design work before scoping - scope defines boundaries
- Don't skip the audit for familiar code - spawn agents, verify
- Don't expand scope beyond what user specified

## The Gate Function

```
BEFORE any refactor work begins:

1. DISCOVER: What is being refactored and why?
2. CHECKPOINT: Create baseline via /bookmarking-code create (mandatory, not optional)
3. AUDIT: Spawn agents to analyze the target area
4. SCOPE: Define boundaries - what changes, what doesn't
5. WRITE: Create .docs/refactors/ scope document via docs-writer
6. PRESENT: Summary with scope doc link and next steps

Skipping the checkpoint = refactoring without a safety net
```

## Initial Response

When this skill is invoked:

### If a target area is provided:
- Confirm the target area and goal with the user
- Proceed to Step 2 (Checkpoint)

### If no target area provided:
```
I'll help you initialize a refactor with a safety baseline.

Please provide:
1. The target area of the codebase (directory, module, or component)
2. The refactor goal (performance, modularity, migration, cleanup, etc.)

I'll create a checkpoint, audit the area, and produce a scope document for the BRDSPI chain.
```

## Process Steps

### Step 1: Discover Refactor Scope

If the user hasn't specified clearly, ask via AskUserQuestion:

- **What area?** — directory, module, component, or specific files
- **What goal?** — performance, readability, modularity, migration, scaling, cleanup
- **What trigger?** — tech debt, new requirements, scaling issues, team feedback

Read the target area files to understand current state. Get enough context to define scope.

### Step 2: Create Baseline Checkpoint (MANDATORY)

This step is NOT optional. Same enforcement as `/implementing-plans` phase checkpoints.

1. Check session awareness: read `.claude/sessions/_current` if exists
2. Check for uncommitted changes:
   - If uncommitted changes exist, warn user:
     ```
     Warning: Uncommitted changes detected. These should be committed before
     creating a refactor baseline, so the checkpoint captures a clean state.

     Would you like to commit first, or proceed with the checkpoint as-is?
     ```
3. Run `/bookmarking-code create "pre-refactor-<area>"` (session-aware)
4. Checkpoint must complete successfully before proceeding

### Step 3: Audit Target Area

Spawn parallel research agents to understand what exists:

- **code-locator** agent: Find all files in the target area — count, types, sizes
- **code-analyzer** agent: Understand current architecture — patterns, dependencies, module boundaries
- **code-librarian** agent: Find tests covering the target area — count, types, coverage assessment

Wait for ALL agents to complete before proceeding.

Compile audit results:
- File count and line count in target area
- Current architecture patterns
- Dependency map (what depends on target, what target depends on)
- Test coverage assessment (existing tests, gaps)

### Step 4: Define Scope Document

Compile audit results into a scope document:

1. Include: what's in scope, what's explicitly out of scope
2. Include: risks identified during audit, mitigation strategies
3. Include: dependencies that constrain refactor approach
4. Spawn `docs-writer` agent with doc_type: "refactor":

   ```
   Task prompt:
     doc_type: "refactor"
     topic: "<area> refactor scope"
     tags: [<relevant component tags>]
     references: [<key files in target area>]
     content: |
       <compiled scope document using ./templates/refactor-scope-template.md>
   ```

5. If the project has a CLAUDE.md, suggest adding a context pointer to the refactor scope doc

### Step 5: Present and Suggest Next Steps

```
REFACTOR INITIALIZED
====================

Scope document: .docs/refactors/MM-DD-YYYY-<area>.md
Baseline checkpoint: pre-refactor-<area> (SHA: <hash>)

Target area:
- [file count] files, [line count] lines
- [test count] tests covering target

Next steps (BRDSPI chain):
1. /researching-code — deep audit of target area patterns
2. /designing-code — target architecture, before/after comparison
3. /structuring-code — migration order (each step deployable)
4. /planning-code — atomic tasks with success criteria
5. /implementing-plans — execute with mandatory checkpoints
```

## Important Guidelines

1. **Checkpoint first, always** — before audit, before scope, before anything
2. **Audit with agents** — don't rely on memory, spawn agents to verify
3. **Scope is a boundary** — resist expanding beyond what user specified
4. **Warn about uncommitted changes** — checkpoint should capture clean state
5. **Downstream skills need the scope doc** — don't skip writing it

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Starting audit work before checkpoint is created
- Skipping the checkpoint ("it's a small refactor")
- Scope creep — including areas beyond what user specified
- Not warning about uncommitted changes before checkpointing
- Making design decisions during scoping (that's for /designing-code)
- Writing the scope doc without spawning audit agents first

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's a small refactor, no checkpoint needed" | Small refactors grow. Checkpoint anyway. |
| "I'll checkpoint after the audit" | Checkpoint captures pristine state. Must come first. |
| "The user already knows the scope" | Document it anyway. Downstream skills need the scope doc. |
| "I can skip the audit for familiar code" | Spawn agents. Verify. Your memory is stale. |
| "Let me start designing while I scope" | Scope first. Design is a separate phase. |

## The Bottom Line

**Checkpoint first, audit second, scope document third.**

No exceptions. Every refactor starts with a safety net. Every refactor. Every time.
