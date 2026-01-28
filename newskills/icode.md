---
description: Implement technical plans from .docs/plans with automated verification
---

# Implement Plan

You are tasked with implementing an approved technical plan from `.docs/plans/`. These plans contain phases with specific changes and success criteria.

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
- Follow the plan's intent while adapting to what you find
- Implement each phase fully before moving to the next
- Verify your work with automated tests after each phase
- Update checkboxes in the plan as you complete sections
- Continue through all phases without stopping for manual confirmation

When things don't match the plan exactly, think about why and adapt. The plan is your guide, but your judgment matters too.

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
2. **Run automated verification** - execute the success criteria commands
3. **Fix any failures** before proceeding
4. **Update checkboxes** in the plan file using Edit
5. **Move to the next phase** immediately

Do NOT pause between phases. Execute all phases continuously until complete or blocked.

## Verification Approach

After implementing each phase:
- Run the success criteria checks (tests, linting, type checking)
- If tests fail, debug and fix before proceeding
- Update your progress in both the plan and your todos
- Check off completed items in the plan file itself using Edit

Example verification:
```
Phase 1 complete. Running verification:
- Unit tests: PASS
- Type checking: PASS
- Linting: PASS

All checks passed. Proceeding to Phase 2...
```

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

Final verification:
- All tests passing
- No linting errors
- Types check successfully

The plan at `.docs/plans/[filename].md` has been fully implemented.
```

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.

## Workflow Context

Typical workflow:
1. `/pcode` - Create the plan
2. `/icode` - Implement the plan (you are here)
3. `/vcode` - Validate implementation
4. `/commit` - Commit changes
5. `/pr` - Create pull request
