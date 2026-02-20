---
name: validating-code
description: "Use this skill when verifying implementation against a plan, checking success criteria, or after /implementing-plans completes. This includes running validation commands, comparing code to plan specifications, checking test coverage, and confirming all phases meet their success criteria. Trigger phrases: '/vcode', 'validate the implementation', 'check against the plan', 'verify success criteria'."
---

# Validate Implementation

You are tasked with validating that an implementation plan was correctly executed, verifying all success criteria and identifying any deviations or issues.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO VERDICT WITHOUT FRESH EVIDENCE
```

If you haven't run verification commands in this response, you cannot claim pass or fail.

**No exceptions:**
- Don't trust previous test runs - run fresh
- Don't trust icode's evidence - verify independently
- Don't extrapolate from partial checks - run everything
- Don't say "should work" - show it works

## The Gate Function: Two-Stage Review

Validation happens in TWO sequential stages. Do not skip or combine.

### Stage 1: Spec Compliance (REQUIRED FIRST)

```
BEFORE checking code quality:

1. READ: The implementation plan FULLY
2. LIST: All phase requirements and success criteria
3. READ: The actual implementation files
4. COMPARE: Line by line - what was requested vs what was built
5. VERDICT: For each requirement:
   - ✓ Implemented correctly
   - ✗ Missing
   - ⚠️ Partial or different

Do NOT proceed to Stage 2 until Stage 1 is complete and documented.
```

### Stage 2: Code Quality (ONLY AFTER STAGE 1)

```
AFTER spec compliance passes:

1. IDENTIFY: What verification commands to run?
2. RUN: Execute each command (tests, lint, typecheck)
3. READ: Full output - exit codes, pass/fail counts
4. VERIFY: Does output confirm all criteria?
5. DOCUMENT: Show evidence for each check

Skip any step = incomplete validation
```

## Process

### Step 1: Locate and Read the Plan

**If plan path provided:**
- Read the plan FULLY
- Identify all phases and success criteria

**If no path provided:**
```
I'll help validate an implementation against its plan.

Available plans in .docs/plans/:
[List files if directory exists]

Which plan would you like to validate?

Usage: /vcode .docs/plans/MM-DD-YYYY-description.md
```

### Step 2: Gather Implementation Evidence

Run commands to understand current state:

```bash
# Check recent commits
git log --oneline -n 20

# Current status
git status

# Run tests and checks
[project-specific test commands]
```

### Step 3: Validate Each Phase

For each phase in the plan:

1. **Check completion markers** - Look for `[x]` checkmarks
2. **Verify code exists** - Read files mentioned in the plan
3. **Run success criteria** - Execute each automated check
4. **Document results** - Pass/fail for each criterion

### Step 4: Generate Validation Report

```markdown
## Validation Report: [Plan Name]

**Plan:** `.docs/plans/[filename].md`
**Validated:** [current date/time]
**Branch:** [current branch]

### Phase Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: [name] | ✓ Complete | All criteria pass |
| Phase 2: [name] | ⚠️ Partial | 1 test failing |
| Phase 3: [name] | ✗ Not done | Not implemented |

### Automated Verification

| Check | Result | Command |
|-------|--------|---------|
| Tests | ✓ Pass | `npm test` |
| Lint | ✓ Pass | `npm run lint` |
| Types | ✗ Fail | `npm run typecheck` |

### Findings

**Matches Plan:**
- [What was implemented correctly]
- [Code follows specified patterns]

**Deviations:**
- [Differences from plan - may be improvements or issues]
- [Missing pieces]

**Issues Found:**
- [Problems that need attention]
- [Test failures]
- [Missing functionality]

### Recommendations

1. [Most important fix needed]
2. [Secondary improvement]
3. [Nice to have]
```

### Step 5: Present Results

Show the validation report and ask:
```
Validation complete. [Summary of status]

[Show report]

Would you like me to:
1. Fix the failing issues
2. Update the plan to reflect changes
3. Run checkpoint comparison (if checkpoints exist)
4. Review changes before committing (`/reviewing-changes`)
5. Continue to commit/PR
```

## Validation Checklist

Always verify:
- [ ] All phases marked complete are actually done
- [ ] Automated tests pass
- [ ] Code follows existing patterns
- [ ] No regressions introduced
- [ ] Error handling is present
- [ ] Files mentioned in plan exist

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Verify

If you notice any of these, STOP immediately:

- Skipping Stage 1 and jumping straight to tests
- Trusting icode's verification output
- Using "should pass", "looks correct", "seems fine"
- About to give verdict without running commands
- Combining stages to "save time"
- Partial verification ("tests pass, so it works")

**When you hit a red flag:**
1. Stop and acknowledge the shortcut
2. Complete BOTH stages fully
3. Show evidence for each

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "icode already verified" | Verify independently. Trust but verify. |
| "Tests pass = spec met" | Tests prove behavior, not requirements. Check both. |
| "Stage 1 is obvious" | Compare requirements line by line. Document findings. |
| "I can do both stages together" | Sequential stages catch different issues. Do both. |
| "It's the same codebase I just read" | Fresh verification catches state changes. |
| "Just need to check the important parts" | Partial verification proves nothing. Full check. |

## Guidelines

1. **Be Thorough** - Check every success criterion
2. **Be Honest** - Report actual state, not optimistic assumptions
3. **Be Constructive** - Identify issues with solutions
4. **Be Efficient** - Run checks in parallel where possible

### Checkpoint Verification (Optional)

If checkpoints were created during `/implementing-plans` phases:

```
Checkpoint comparison available.

/bookmarking-code list
- plan-approved (2026-01-28-10:30) @ abc1234
- phase-1-done (2026-01-28-11:45) @ def5678
- phase-2-done (2026-01-28-14:20) @ ghi7890

Run full comparison to plan baseline?
/bookmarking-code verify "plan-approved"
```

This shows:
- Total files changed since plan approval
- All commits made during implementation
- Clear audit trail for PR description

**Combine with validation report:**
```
## Validation Report: [Plan Name]

### Implementation Delta (from checkpoint)
Files changed since plan-approved: 15
Commits: 5
Test delta: +12 passing, -0 failing

### Phase Status
[rest of report...]
```

## Relationship to Other Commands

Typical workflow:
1. `/planning-code` - Create the plan
2. `/implementing-plans` - Implement the plan
3. `/vcode` - Validate (you are here)
4. `/committing-changes` - Commit changes
5. `/creating-prs` - Create pull request

## Example Interaction

```
User: /vcode .docs/plans/01-27-2026-auth-implementation.md
Assistant: I'll validate the auth implementation against the plan...

[Reads plan, runs checks, verifies files]

## Validation Report: Auth Implementation

### Phase Status
| Phase | Status |
|-------|--------|
| Phase 1: Database schema | ✓ Complete |
| Phase 2: Auth middleware | ✓ Complete |
| Phase 3: Endpoints | ⚠️ Partial |

### Automated Verification
- Tests: ✓ Pass (47 passing)
- Lint: ✓ Pass
- Types: ✓ Pass

### Issues Found
- Phase 3: Logout endpoint missing token invalidation
  - `src/routes/auth.ts:45` - returns 200 but doesn't clear session

### Recommendations
1. Add session clearing to logout endpoint

Would you like me to fix the logout endpoint issue?
```

## The Bottom Line

**No shortcuts for validation.**

Stage 1: Check spec compliance. Stage 2: Check code quality. Show evidence for both.

This is non-negotiable. Every validation. Every time.
