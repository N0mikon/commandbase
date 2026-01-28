---
description: Validate implementation against plan, verify success criteria
---

# Validate Implementation

You are tasked with validating that an implementation plan was correctly executed, verifying all success criteria and identifying any deviations or issues.

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
3. Continue to PR creation
```

## Validation Checklist

Always verify:
- [ ] All phases marked complete are actually done
- [ ] Automated tests pass
- [ ] Code follows existing patterns
- [ ] No regressions introduced
- [ ] Error handling is present
- [ ] Files mentioned in plan exist

## Guidelines

1. **Be Thorough** - Check every success criterion
2. **Be Honest** - Report actual state, not optimistic assumptions
3. **Be Constructive** - Identify issues with solutions
4. **Be Efficient** - Run checks in parallel where possible

## Relationship to Other Commands

Typical workflow:
1. `/pcode` - Create the plan
2. `/icode` - Implement the plan
3. `/vcode` - Validate (you are here)
4. `/commit` - Commit changes
5. `/pr` - Create pull request

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
