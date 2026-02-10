---
date: 2026-01-28
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated file paths from ~/.claude/skills/ to plugin location, refreshed process to match current two-stage validation design"
status: current
topic: validating-code skill analysis
tags: [skill, validation, rpi-workflow, commandbase-core]
git_commit: 8e92bba
references:
  - plugins/commandbase-core/skills/validating-code/SKILL.md
---

# Research: validating-code Skill

## Overview

The `validating-code` skill (`plugins/commandbase-core/skills/validating-code/SKILL.md`) verifies implementation against a plan, checking success criteria and confirming all phases meet their requirements. It produces a validation report with verdicts and next-step options.

**Trigger phrases**: `/vcode`, `validate the implementation`, `check against the plan`, `verify success criteria`

## Purpose

Provides independent validation after `/implementing-plans` completes:
- Runs validation commands from plan's success criteria
- Compares code to plan specifications
- Checks test coverage
- Confirms all phases meet their success criteria

## Core Principles

### The Iron Law

```
NO VERDICT WITHOUT FRESH EVIDENCE
```

The skill enforces that every verdict must be backed by commands run in the current response. No trusting previous test runs, no trusting `/implementing-plans` evidence, no extrapolation from partial checks.

### Two-Stage Gate Function

Validation happens in TWO sequential stages that must not be skipped or combined:

1. **Stage 1: Spec Compliance** -- Read the plan fully, list all requirements, read implementation files, compare line-by-line what was requested vs. what was built, and give a per-requirement verdict.
2. **Stage 2: Code Quality** -- Only after Stage 1 passes. Identify verification commands, run them (tests, lint, typecheck), read full output, verify criteria, and document evidence.

## Process

### Step 1: Locate and Read the Plan
If a plan path is provided, read it fully and identify all phases and success criteria. If no path is provided, list available plans in `.docs/plans/` and prompt the user.

### Step 2: Gather Implementation Evidence
Run commands to understand current state: recent git log, git status, and project-specific test commands.

### Step 3: Validate Each Phase
For each phase in the plan:
1. Check completion markers (look for `[x]` checkmarks)
2. Verify code exists (read files mentioned in the plan)
3. Run success criteria (execute each automated check)
4. Document results (pass/fail for each criterion)

### Step 4: Generate Validation Report
The report uses a structured markdown table format:

```markdown
## Validation Report: [Plan Name]

**Plan:** `.docs/plans/[filename].md`
**Validated:** [current date/time]
**Branch:** [current branch]

### Phase Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: [name] | PASS | All criteria pass |
| Phase 2: [name] | PARTIAL | 1 test failing |
| Phase 3: [name] | NOT DONE | Not implemented |

### Automated Verification

| Check | Result | Command |
|-------|--------|---------|
| Tests | PASS | `npm test` |
| Lint | PASS | `npm run lint` |
| Types | FAIL | `npm run typecheck` |

### Findings
- Matches Plan: [what was implemented correctly]
- Deviations: [differences from plan]
- Issues Found: [problems needing attention]

### Recommendations
1. [Most important fix needed]
2. [Secondary improvement]
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

## Red Flags and Rationalization Prevention

The skill includes explicit guardrails against common validation shortcuts:

- Skipping Stage 1 and jumping straight to tests
- Trusting `/implementing-plans` verification output without independent checks
- Using language like "should pass", "looks correct", "seems fine"
- Giving a verdict without running commands
- Combining stages to "save time"
- Partial verification ("tests pass, so it works")

## Checkpoint Integration

If checkpoints were created during `/implementing-plans` phases:
```
Checkpoint comparison available.

/bookmarking-code list
- plan-approved (2026-01-28-10:30) @ abc1234
- phase-1-done (2026-01-28-11:45) @ def5678

Run full comparison to plan baseline?
/bookmarking-code verify "plan-approved"
```

This shows:
- Total files changed since plan approval
- All commits made during implementation
- Clear audit trail for PR description

## Integration Points

Typical workflow position:
1. `/planning-code` -- Create the plan
2. `/implementing-plans` -- Implement the plan
3. `/vcode` -- Validate (this skill)
4. `/committing-changes` -- Commit changes
5. `/creating-prs` -- Create pull request

Also integrates with:
- `/reviewing-changes` -- Can invoke before commit
- `/bookmarking-code verify` -- For delta comparison against checkpoints

## File Reference

- Main: `plugins/commandbase-core/skills/validating-code/SKILL.md`
