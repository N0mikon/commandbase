# Research: implementing-plans Skill

## Overview

The `implementing-plans` skill (`~/.claude/skills/implementing-plans/SKILL.md`) executes technical plans from `.docs/plans/` with mandatory verification at each phase. It enforces evidence-based completion through "The Iron Law" and a five-step "Gate Function" that prevents proceeding without fresh verification output.

**Trigger phrases**: `implement this plan`, `execute the plan`, or provide a plan path

## The Iron Law (SKILL.md:12-24)

```
NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

**Absolute rules with no exceptions:**
- Don't mark checkboxes without running verification
- Don't proceed to next phase without evidence
- Don't trust previous runs - run fresh
- Don't claim "should pass" - show it passes

## The Gate Function (verification-workflow.md:6-19)

5-step verification process before marking any phase complete:

1. **IDENTIFY**: What commands verify this phase's success criteria?
2. **RUN**: Execute each command fresh and complete (not cached)
3. **READ**: Full output examination (exit codes, pass/fail counts, errors)
4. **VERIFY**: Does output confirm ALL phase requirements?
5. **ONLY THEN**: Update the checkbox in the plan file

## Phase-by-Phase Execution

For each phase, 6 mandatory steps:

1. **Implement the changes** - Execute what the plan describes
2. **Run verification** - Use Gate Function
3. **Fix any failures** - Do not proceed until verification passes
4. **Show evidence** - State what commands ran and their output
5. **Update checkboxes** - Edit plan file only after evidence shown
6. **Move to next phase** - Only after evidence is shown

**Continuous Execution**: "Do NOT pause between phases. Execute all phases continuously until complete or blocked."

## Evidence Format

**Acceptable:**
```
Phase 1 complete.

Verification:
- `npm test`: 47/47 passing, exit 0
- `npm run typecheck`: no errors, exit 0
- `npm run lint`: 0 warnings, exit 0

✓ All success criteria met. Proceeding to Phase 2...
```

**NOT Acceptable:**
- "Tests should pass now"
- "I've implemented the changes"
- "Phase complete" (without evidence)

## Checkpoint Integration

After completing each phase with evidence, suggest checkpoint creation:
```
Phase [N] complete.

Verification:
- [test results]

Create checkpoint before next phase?
/bookmarking-code create "phase-N-done"
```

## Full Workflow Integration

```
/planning-code → /bookmarking-code create "plan-approved"
   ↓
/implementing-plans Phase 1 → Evidence → /bookmarking-code create "phase-1-done"
   ↓
/implementing-plans Phase 2 → /bookmarking-code verify → Evidence → /bookmarking-code create "phase-2-done"
   ↓
/validating-code → /bookmarking-code verify "plan-approved"
   ↓
/committing-changes
```

## Anti-Patterns

**Red Flags - Stop if noticing:**
- About to mark checkbox without running verification
- Using "should", "probably", "seems to" about test results
- Saying "Done!" before showing evidence
- Proceeding to next phase without verification output
- Thinking "the change is simple, verification not needed"

**Rationalization Prevention:**

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier" | Run them again. State changes. |
| "It's a simple change" | Simple changes break things. Verify. |
| "I'm confident it works" | Confidence ≠ evidence |
| "Verification takes too long" | Rework takes longer. Verify now. |
| "I'll verify at the end" | Errors compound. Verify each phase. |

## The "Obviously Works" Trap

Most dangerous changes are those that "obviously work":
- Single-line fixes
- Copy-paste from working code
- "Just renaming"
- "Trivial refactoring"

These are exactly the changes that introduce subtle bugs. Verify them like everything else.

## File References

- Main: `~/.claude/skills/implementing-plans/SKILL.md`
- Verification workflow: `~/.claude/skills/implementing-plans/reference/verification-workflow.md`
- Anti-patterns: `~/.claude/skills/implementing-plans/reference/anti-patterns.md`
