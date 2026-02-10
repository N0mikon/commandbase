---
date: 2026-02-02
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after plugin conversion - corrected file paths, check category ordering, output format, and integration details to match current SKILL.md"
status: current
topic: reviewing-changes skill analysis
tags:
  - skill
  - reviewing-changes
  - git-workflow
  - quality-gate
git_commit: 8e92bba
references:
  - plugins/commandbase-git-workflow/skills/reviewing-changes/SKILL.md
  - plugins/commandbase-git-workflow/skills/reviewing-changes/templates/review-report.md
---

# Research: reviewing-changes Skill

## Overview

The `reviewing-changes` skill (`plugins/commandbase-git-workflow/skills/reviewing-changes/SKILL.md`) performs pre-commit/pre-PR quality review of staged or uncommitted changes. It produces a verdict (PASS/WARN) based on 5 check categories, catching issues before they enter version control.

**Trigger phrases**: `/reviewing-changes`, `review my changes`, `check before commit`, `is this ready to commit`

## The Iron Law

```
NO COMMIT WITHOUT REVIEWING CHANGES FIRST
```

Review is about catching things that pass tests but shouldn't be committed.

## The Gate Function

```
BEFORE presenting a verdict:

1. GET STATUS: Run `git status` to identify changed files
2. GET DIFF: Run `git diff` (staged) or `git diff HEAD` (all) to see changes
3. RUN CHECKS: Execute all 5 check categories
4. COMPILE: Gather findings into report format
5. DRAFT MESSAGE: Create suggested commit message from diff
6. ONLY THEN: Present verdict and let user decide

No verdict without running the checks.
```

## Purpose

Quality gate between implementation and commit:
- Reviews code cleanliness (debug code, commented code)
- Validates commit atomicity (single logical change)
- Assesses commit message quality (why, not what)
- Checks diff coherence (related changes grouped)
- Verifies documentation sync

## What This Skill Does NOT Do

- **No auto-blocking** -- WARN only, user decides
- **No security checks** -- that is `/reviewing-security`
- **No spec compliance** -- that is `/validating-code`
- **No style enforcement** -- that is linters

## Check Categories (Priority Order)

1. **Code Cleanliness** (Highest Priority)
   - Debug statements: `console.log`, `print()`, `debugger`, `var_dump`, `dd()`
   - Commented-out code blocks (not explanatory comments)
   - TODO/FIXME in newly added lines
   - Obvious unused variables in changed code

2. **Commit Atomicity**
   - Do changes span unrelated concerns?
   - Could this logically be multiple commits?
   - Is there a single clear purpose?

3. **Commit Message Quality**
   - Analyze the diff to understand what changed
   - Draft a commit message that explains WHY not just WHAT
   - Flag if changes are hard to summarize (atomicity problem)
   - First line under 72 characters; body 0-3 bullet points max

4. **Diff Coherence**
   - Unrelated files modified together
   - Accidental inclusions (lockfiles without package changes, generated files)
   - Whitespace-only changes mixed with real changes

5. **Documentation Sync** (Lowest Priority)
   - If public API changed, are docs updated?
   - If new feature, is README updated?
   - If patterns changed, is CLAUDE.md updated?

## Verdict System

**PASS**: No issues found, safe to commit
**WARN**: Issues found, review recommended

No BLOCK verdict -- skill provides recommendations, user decides.

## Output Format

The skill uses the report template at `plugins/commandbase-git-workflow/skills/reviewing-changes/templates/review-report.md`:

```markdown
## Review: [PASS|WARN]

**Files reviewed:** [N] files
**Lines changed:** +[added] / -[removed]

### Findings

**Code Cleanliness**
- [check mark or warning] [Description]

**Commit Atomicity**
- [check mark or warning] [Description]

**Diff Coherence**
- [check mark or warning] [Description]

**Documentation Sync**
- [check mark or warning] [Description]

### Suggested Commit Message

[Draft message based on diff analysis]

### Recommendation

[PASS: Ready to commit | WARN: Review findings above]

Would you like to:
1. Proceed to `/committing-changes`
2. Fix issues first
3. Split into multiple commits
```

## Integration Points

Position in workflow:

```
/validating-code
   |  "Continue to commit?"
/reviewing-changes  <-- THIS SKILL
   |  [PASS: proceed | WARN: decide]
/committing-changes
```

- Invoked after validation passes, before `/committing-changes`
- Can be run independently for pre-commit review
- When unsure if changes are commit-ready

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

- Main: `plugins/commandbase-git-workflow/skills/reviewing-changes/SKILL.md`
- Review report template: `plugins/commandbase-git-workflow/skills/reviewing-changes/templates/review-report.md`
