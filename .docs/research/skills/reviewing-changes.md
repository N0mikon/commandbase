# Research: reviewing-changes Skill

## Overview

The `reviewing-changes` skill (`~/.claude/skills/reviewing-changes/SKILL.md`) performs pre-commit/pre-PR quality review of staged or uncommitted changes. It produces a verdict (PASS/WARN) based on 5 check categories, catching issues before they enter version control.

**Trigger phrases**: `/reviewing-changes`, `review my changes`, `check before commit`, `is this ready to commit`

## The Iron Law

```
NO COMMIT WITHOUT REVIEWING CHANGES FIRST
```

Review is about catching things that pass tests but shouldn't be committed.

## The Gate Function (SKILL.md:23-33)

```
BEFORE presenting a verdict:

1. GET STATUS: Run `git status` to identify changed files
2. GET DIFF: Run `git diff` (staged) or `git diff HEAD` (all) to see changes
3. RUN CHECKS: Execute all 5 check categories
4. COMPILE: Gather findings into report format
5. DRAFT MESSAGE: Create suggested commit message from diff
6. ONLY THEN: Present verdict and let user decide
```

## Purpose

Quality gate between implementation and commit:
- Reviews code cleanliness (debug code, commented code)
- Checks diff coherence (related changes grouped)
- Validates commit atomicity
- Verifies documentation sync
- Assesses commit message quality

## Check Categories (Priority Order)

1. **Code Cleanliness** (Highest Priority)
   - Debug code in production (console.log, print statements)
   - Commented-out code blocks
   - TODO/FIXME without ticket references
   - Leftover test scaffolding

2. **Diff Coherence**
   - Unrelated changes mixed together
   - Changes that should be separate commits
   - Partial implementations

3. **Commit Atomicity**
   - Single logical unit of work
   - Complete feature/fix
   - Self-contained changes

4. **Documentation Sync**
   - Code changes without doc updates
   - README out of sync with implementation
   - Outdated comments

5. **Message Quality** (Lowest Priority)
   - Commit message describes the "why"
   - Follows conventional format
   - Under 72 characters

## Verdict System

**PASS**: No issues found, safe to commit
**WARN**: Issues found, review recommended

No BLOCK verdict - skill provides recommendations, user decides.

## Output Format

```
CHANGES REVIEW
==============

Files reviewed: [N]

Check Results:
✓ Code Cleanliness: PASS
⚠️ Diff Coherence: WARN - unrelated test file included
✓ Commit Atomicity: PASS
✓ Doc Sync: PASS
✓ Message Quality: PASS

Verdict: WARN

Findings:
- [file:line] Unrelated test file staged with feature code

Recommendations:
- Consider splitting into separate commits
- Review staged files before committing

Ready to proceed? /committing-changes
```

## Integration Points

- Invoked before `/committing-changes`
- Called from `/validating-code` as option 4
- Can be run independently for pre-commit review

## Red Flags - STOP and Verify

- About to say "PASS" without running git diff
- Skipping check categories because "changes are small"
- Not drafting a commit message
- Ignoring obvious debug statements

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just a small change" | Small changes can still have debug code or poor atomicity |
| "I'll fix it in the next commit" | Fix it now. Next commit has its own concerns. |
| "The tests pass" | Tests don't catch debug statements or poor commit messages |
| "I know what I changed" | The diff might show surprises. Run the checks. |

## File Reference

- Main: `~/.claude/skills/reviewing-changes/SKILL.md`
- Review report template: `~/.claude/skills/reviewing-changes/templates/review-report.md`
