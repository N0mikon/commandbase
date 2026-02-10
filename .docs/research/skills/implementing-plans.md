---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file paths from ~/.claude/skills/ to plugins/commandbase-code/skills/, refreshed Gate Function to current 6-step version, updated execution flow to 7 steps, added documentation freshness and new sections"
references:
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/reference/verification-workflow.md
  - plugins/commandbase-code/skills/implementing-plans/reference/anti-patterns.md
---

# Research: implementing-plans Skill

## Overview

The `implementing-plans` skill (`plugins/commandbase-code/skills/implementing-plans/SKILL.md`) executes technical plans from `.docs/plans/` with mandatory verification at each phase. It enforces evidence-based completion through "The Iron Law" and a six-step "Gate Function" that prevents proceeding without fresh verification output.

**Trigger phrases**: `implement this plan`, `execute the plan`, `continue implementation`, or provide a plan path

## The Iron Law

```
NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

**Absolute rules with no exceptions:**
- Don't mark checkboxes without running verification
- Don't proceed to next phase without evidence
- Don't trust previous runs - run fresh
- Don't claim "should pass" - show it passes

## The Gate Function

6-step verification process before marking any phase complete:

1. **READ**: The plan phase requirements fully
2. **IMPLEMENT**: Make the required changes
3. **RUN**: Execute verification commands fresh
4. **READ**: Full output - exit codes, pass/fail counts
5. **EVIDENCE**: Show command output in response
6. **ONLY THEN**: Mark checkboxes and proceed

The reference file (`reference/verification-workflow.md`) provides additional detail with an alternative framing: IDENTIFY, RUN, READ, VERIFY, ONLY THEN.

## Getting Started

When given a plan path:
- Read the plan completely and check for existing checkmarks (`- [x]`)
- Read all files mentioned in the plan
- Read files fully (never use limit/offset parameters)
- Think deeply about how the pieces fit together
- Create a todo list to track progress
- Start implementing if you understand what needs to be done

If no plan path provided, ask for one or list available plans in `.docs/plans/`.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. The skill enforces:
- Follow the plan exactly. If deviation is needed, STOP and present it before making it.
- Implement each phase fully before moving to the next
- Verify work with automated tests after each phase
- Update checkboxes in the plan as sections complete
- Continue through all phases without stopping for manual confirmation

When things don't match the plan, STOP and present the mismatch. The plan is a contract, not a suggestion.

## Phase-by-Phase Execution

For each phase, 7 mandatory steps:

1. **Implement the changes** - Execute what the plan describes
2. **Run verification** - Use Gate Function (see `reference/verification-workflow.md`)
3. **Fix any failures** - Do not proceed until verification passes
4. **Show evidence** - State what commands ran and their output
5. **Update checkboxes** - Edit plan file only after evidence shown
6. **Create checkpoint** - `/bookmarking-code create "phase-N-done"` (session-aware when available)
7. **Move to next phase** - Only after evidence is shown and checkpoint created

**Steps 4 and 6 are not optional.** No evidence = no completion. No checkpoint = no proceeding.

**Continuous Execution**: "Do NOT pause between phases. Execute all phases continuously until complete or blocked."

## Evidence Format

**Acceptable:**
```
Phase 1 complete.

Verification:
- `npm test`: 47/47 passing, exit 0
- `npm run typecheck`: no errors, exit 0
- `npm run lint`: 0 warnings, exit 0

All success criteria met. Proceeding to Phase 2...
```

**NOT Acceptable:**
- "Tests should pass now"
- "I've implemented the changes"
- "Phase complete" (without evidence)

## Checkpoint Integration

After completing each phase with verified evidence, create a checkpoint:

1. Check if `.claude/sessions/_current` exists
2. If session exists: `/bookmarking-code create "phase-N-done"` (writes to session folder)
3. If no session: `/bookmarking-code create "phase-N-done"` (writes to global log)

This is NOT optional. Every verified phase gets a checkpoint before proceeding.

```
Phase [N] complete.

Verification:
- [test results]

Checkpoint created: phase-N-done
```

## Documentation Freshness

At the start of implementation and after completing the final phase:

1. Identify `.docs/` files referenced in the plan
2. Spawn docs-updater agent for each to check staleness
3. Report any stale documents to user before proceeding

This catches plans referencing outdated research or handoffs.

## Full Workflow Integration

```
/planning-code -> /bookmarking-code create "plan-approved"
   |
/implementing-plans Phase 1 -> Evidence -> /bookmarking-code create "phase-1-done"
   |
/implementing-plans Phase 2 -> /bookmarking-code verify -> Evidence -> /bookmarking-code create "phase-2-done"
   |
... continue pattern ...
   |
/validating-code -> /bookmarking-code verify "plan-approved"
   |
/committing-changes
```

**After all phases complete:**
- Run `/validating-code` to get independent validation
- Run `/bookmarking-code verify "plan-approved"` for full delta review
- Only then proceed to `/committing-changes`

## Anti-Patterns

**Red Flags - Stop if noticing:**
- About to mark checkbox without running verification
- Using "should", "probably", "seems to" about test results
- Saying "Done!" before showing evidence
- Proceeding to next phase without verification output
- Trusting that previous verification is still valid
- Thinking "the change is simple, verification not needed"
- Making changes not described in the plan without explaining why
- "Improving" or refactoring code the plan didn't ask to touch

**Rationalization Prevention:**

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier" | Run them again. State changes. Fresh evidence only. |
| "It's a simple change" | Simple changes break things. Verify. |
| "I'm confident it works" | Confidence does not equal evidence. |
| "Verification takes too long" | Rework takes longer. Verify now. |
| "I'll verify at the end" | Errors compound. Verify each phase. |
| "This related code could use cleanup" | Only change what the plan specifies. File a separate task. |
| "While I'm here, I should also..." | No. Finish the planned work. Scope creep is how plans fail. |

## The "Obviously Works" Trap

Most dangerous changes are those that "obviously work":
- Single-line fixes
- Copy-paste from working code
- "Just renaming"
- "Trivial refactoring"

These are exactly the changes that introduce subtle bugs. Verify them like everything else.

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done
- Pick up from the first unchecked item
- Verify previous work only if something seems off

## File References

- Main: `plugins/commandbase-code/skills/implementing-plans/SKILL.md`
- Verification workflow: `plugins/commandbase-code/skills/implementing-plans/reference/verification-workflow.md`
- Anti-patterns: `plugins/commandbase-code/skills/implementing-plans/reference/anti-patterns.md`
