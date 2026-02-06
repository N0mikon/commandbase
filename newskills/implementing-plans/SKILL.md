---
name: implementing-plans
description: "Use this skill when implementing technical plans from .docs/plans/ with automated verification. This includes executing phased plans, running success criteria checks, updating completion checkboxes, and continuing implementation after interruption. Trigger phrases: 'implement this plan', 'execute the plan', 'continue implementation', or providing a plan path."
---

# Implementing Plans

You are tasked with implementing an approved technical plan from `.docs/plans/`. These plans contain phases with specific changes and success criteria.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification commands in this response, you cannot claim the phase is complete.

**No exceptions:**
- Don't mark checkboxes without running verification
- Don't proceed to next phase without evidence
- Don't trust previous runs - run fresh
- Don't claim "should pass" - show it passes

## The Gate Function

```
BEFORE claiming any phase is complete:

1. READ: The plan phase requirements fully
2. IMPLEMENT: Make the required changes
3. RUN: Execute verification commands fresh
4. READ: Full output - exit codes, pass/fail counts
5. EVIDENCE: Show command output in response
6. ONLY THEN: Mark checkboxes and proceed

Skip verification = false completion claim
```

## Getting Started

When given a plan path:
- Read the plan completely and check for any existing checkmarks (- [x])
- Read all files mentioned in the plan
- **Read files fully** - never use limit/offset parameters, you need complete context
- Think deeply about how the pieces fit together
- Create a todo list to track your progress
- Start implementing if you understand what needs to be done

If no plan path provided, ask for one or list available plans in `.docs/plans/`.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan exactly. If reality requires deviation, STOP and present the deviation before making it.
- Implement each phase fully before moving to the next
- Verify your work with automated tests after each phase
- Update checkboxes in the plan as you complete sections
- Continue through all phases without stopping for manual confirmation

When things don't match the plan exactly, STOP and present the mismatch to the user. Do not adapt silently - explain what's different and propose the deviation. The plan is your contract, not a suggestion.

If you encounter a significant mismatch that blocks progress:
- STOP and think deeply about why the plan can't be followed
- Present the issue clearly:
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```

## Execution Flow

For each phase:

1. **Implement the changes** described in the plan
2. **Run verification** - see `reference/verification-workflow.md` for the Gate Function
3. **Fix any failures** - do not proceed until verification passes
4. **Show evidence** - state what commands you ran and their output
5. **Update checkboxes** in the plan file using Edit
6. **Move to the next phase** - only after evidence is shown

**Remember:** Step 4 (show evidence) is not optional. No evidence = no completion.

Do NOT pause between phases. Execute all phases continuously until complete or blocked.

## If You Get Stuck

When something isn't working as expected:
- First, make sure you've read and understood all the relevant code
- Consider if the codebase has evolved since the plan was written
- Try debugging with targeted searches or test runs
- If truly blocked, present the issue clearly and ask for guidance

Use sub-tasks sparingly - mainly for targeted debugging or exploring unfamiliar territory.

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done
- Pick up from the first unchecked item
- Verify previous work only if something seems off

## Completion

When all phases are complete:
```
Implementation complete!

All phases executed:
- [x] Phase 1: [name]
- [x] Phase 2: [name]
- [x] Phase 3: [name]

Final verification (fresh run):
- `[test command]`: [X]/[X] passing, exit 0
- `[lint command]`: 0 errors, exit 0
- `[typecheck command]`: no errors, exit 0

All success criteria verified with evidence above.
The plan at `.docs/plans/[filename].md` has been fully implemented.
```

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.

## The Bottom Line

**No shortcuts for verification.**

Run the commands. Read the output. Show the evidence. THEN claim completion.

This is non-negotiable. Every phase. Every time.

See `reference/anti-patterns.md` for detailed anti-patterns.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to mark a checkbox without running verification
- Claiming "should pass" or "looks correct" without evidence
- Proceeding to next phase without showing command output
- Trusting previous test runs instead of running fresh
- Skipping phases because they "seem simple"
- Making changes not described in the plan without explaining why and getting approval
- "Improving" or refactoring code that the plan didn't ask you to touch

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier" | Run them again. State changes. Fresh evidence only. |
| "This phase is trivial" | Trivial phases still need verification. No exceptions. |
| "I can see the code is correct" | Show command output. Visual inspection isn't evidence. |
| "User is waiting" | Wrong implementation wastes more time. Verify first. |
| "I'll verify at the end" | Per-phase verification catches issues early. Do it now. |
| "This related code could use cleanup" | Only change what the plan specifies. File a separate task for other improvements. |
| "While I'm here, I should also..." | No. Finish the planned work. Scope creep is how plans fail. |

## Workflow Integration

### Checkpoint Integration

After completing each phase with evidence, suggest a checkpoint:

```
Phase [N] complete.

Verification:
- [test results]

Create checkpoint before next phase?
/bookmarking-code create "phase-N-done"
```

### Full Workflow

```
/planning-code → /bookmarking-code create "plan-approved"
   ↓
/implementing-plans Phase 1 → Evidence → /bookmarking-code create "phase-1-done"
   ↓
/implementing-plans Phase 2 → /bookmarking-code verify → Evidence → /bookmarking-code create "phase-2-done"
   ↓
... continue pattern ...
   ↓
/validating-code → /bookmarking-code verify "plan-approved"
   ↓
/committing-changes
```

**After all phases complete:**
- Run `/validating-code` to get independent validation
- Run `/bookmarking-code verify "plan-approved"` for full delta review
- Only then proceed to `/committing-changes`
