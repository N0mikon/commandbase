# Research: validating-implementations Skill

## Overview

The `validating-implementations` skill (`~/.claude/skills/validating-implementations/SKILL.md`) verifies implementation against a plan, checking success criteria and confirming all phases meet their requirements. It produces a validation report with verdicts and next-step options.

**Trigger phrases**: `/vcode`, `validate the implementation`, `check against the plan`, `verify success criteria`

## Purpose

Provides independent validation after `/implementing-plans` completes:
- Runs validation commands from plan's success criteria
- Compares code to plan specifications
- Checks test coverage
- Confirms all phases meet their success criteria

## Process

### Step 1: Load Plan
Read the implementation plan from `.docs/plans/` to understand what was supposed to be built.

### Step 2: Run Success Criteria
For each phase's success criteria, run the verification commands fresh and capture results.

### Step 3: Compare to Specifications
Check that implementation matches what the plan specified:
- Required files exist
- Expected functionality works
- Tests pass

### Step 4: Generate Report
```
VALIDATION REPORT
=================

Plan: .docs/plans/[name].md

Phase Status:
- [x] Phase 1: [name] - PASS
- [x] Phase 2: [name] - PASS
- [ ] Phase 3: [name] - FAIL (tests failing)

Issues Found:
- [description of any issues]

Overall Verdict: [PASS/WARN/FAIL]
```

### Step 5: Present Options
```
Would you like me to:
1. Fix the failing issues
2. Update the plan to reflect changes
3. Run checkpoint comparison (if checkpoints exist)
4. Review changes before committing (/reviewing-changes)
5. Continue to commit/PR
```

## Checkpoint Integration

If checkpoints were created during `/implementing-plans` phases:
```
Checkpoint comparison available.

/checkpointing list
- plan-approved (2026-01-28-10:30) @ abc1234
- phase-1-done (2026-01-28-11:45) @ def5678

Run full comparison to plan baseline?
/checkpointing verify "plan-approved"
```

This shows:
- Total files changed since plan approval
- All commits made during implementation
- Clear audit trail for PR description

## Integration Points

- Runs after `/implementing-plans` completes
- Can invoke `/reviewing-changes` before commit
- Can invoke `/checkpointing verify` for delta comparison
- Leads to `/committing-changes` when validation passes

## File Reference

- Main: `~/.claude/skills/validating-implementations/SKILL.md`
