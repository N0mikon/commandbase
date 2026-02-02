---
name: reviewing-changes
description: Use this skill when reviewing code changes before committing, checking commit quality, or preparing changes for a PR. This includes reviewing diffs for debug statements, checking if changes should be split into multiple commits, drafting commit messages, and verifying documentation is in sync. Trigger phrases: '/reviewing-changes', 'review my changes', 'check before commit', 'is this ready to commit'.
---

# Reviewing Changes

Review code changes before committing to surface quality issues and draft commit messages. Uses PASS/WARN verdicts - user always decides whether to proceed.

**Violating the letter of these rules is violating the spirit of these rules.**

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

## What This Skill Does NOT Do

- **No auto-blocking** - WARN only, user decides
- **No security checks** - that's `/reviewing-security`
- **No spec compliance** - that's `/validating-implementations`
- **No style enforcement** - that's linters

## The Five Check Categories

**Severity ranking** (highest to lowest priority):
1. **Code Cleanliness** - Debug code in production is embarrassing
2. **Diff Coherence** - Accidental inclusions can leak secrets or break builds
3. **Commit Atomicity** - Affects code review quality and git history
4. **Documentation Sync** - Important but can be fixed in follow-up
5. **Commit Message Quality** - Least critical, easily amended

### 1. Code Cleanliness

**What to check:**
- Debug statements: `console.log`, `print()`, `debugger`, `var_dump`, `dd()`
- Commented-out code blocks (not explanatory comments)
- TODO/FIXME in newly added lines
- Obvious unused variables in changed code

**WARN triggers:**
- Any debug statement found
- Commented-out code block > 3 lines
- TODO without issue reference

**How to check:**
```bash
# Debug statements in staged changes
git diff --cached | grep -E "(console\.log|debugger|print\(|var_dump|dd\()"

# TODO/FIXME in new lines
git diff --cached | grep "^+" | grep -E "(TODO|FIXME)"
```

### 2. Commit Atomicity

**What to check:**
- Do changes span unrelated concerns?
- Could this logically be multiple commits?
- Is there a single clear purpose?

**WARN triggers:**
- Changes touch 3+ unrelated directories
- Mix of feature code + refactoring + config changes
- Hard to write a single-sentence summary

**How to assess:**
- Group changed files by purpose
- If groups are independent, suggest splitting
- If tightly coupled, single commit is fine

### 3. Commit Message Quality

**What to do:**
- Analyze the diff to understand what changed
- Draft a commit message that explains WHY not just WHAT
- Flag if changes are hard to summarize (atomicity problem)

**Good message pattern:**
```
[Type]: [What] because [Why]

- Specific change 1
- Specific change 2
```

**Types:** feat, fix, refactor, docs, test, chore

### 4. Diff Coherence

**What to check:**
- Unrelated files modified together
- Accidental inclusions (lockfiles without package changes, generated files)
- Whitespace-only changes mixed with real changes

**WARN triggers:**
- Lockfile changed but no dependency changes
- Build artifacts in diff
- Formatting changes mixed with logic changes

**How to check:**
```bash
# List changed files
git diff --cached --name-only

# Check for generated/lock files
git diff --cached --name-only | grep -E "(lock|\.min\.|dist/|build/)"
```

### 5. Documentation Sync

**What to check:**
- If public API changed, are docs updated?
- If new feature, is README updated?
- If patterns changed, is CLAUDE.md updated?

**WARN triggers:**
- Changed exports without doc updates
- New commands/endpoints without usage docs
- CLAUDE.md references files that changed

**How to assess:**
- Check if README mentions changed functionality
- Check if CLAUDE.md references modified files
- Look for doc files in changed file list

## The Review Process

### Step 1: Gather Information

```bash
# See what's staged
git status

# See the actual changes
git diff --cached    # staged only
git diff HEAD        # all changes
```

### Step 2: Run Checks

For each category:
1. Run the relevant commands/analysis
2. Note any findings
3. Classify as ✓ (clear) or ⚠️ (warning)

### Step 3: Draft Commit Message

Based on the diff:
1. Identify the primary change type (feat/fix/refactor/etc)
2. Write a one-line summary
3. Add bullet points for specific changes if needed
4. Include Co-Authored-By if pair programming

### Step 4: Compile Report

Use the template at `templates/review-report.md`

### Step 5: Present Verdict

**PASS** - No issues found
```
Review: PASS

All checks clear. Ready to commit.

Suggested commit message:
[draft message]

Proceed with `/committing-changes`?
```

**WARN** - Issues found, user decides
```
Review: WARN

Found [N] issues across [categories].

[Findings list]

Suggested commit message:
[draft message]

Options:
1. Proceed anyway (issues are acceptable)
2. Fix issues first
3. Split into multiple commits
```

## Report Format

```markdown
## Review: [PASS|WARN]

### Findings

**Code Cleanliness**
- [✓|⚠️] [finding or "No issues"]

**Commit Atomicity**
- [✓|⚠️] [finding or "Single logical change"]

**Diff Coherence**
- [✓|⚠️] [finding or "All changes related"]

**Documentation Sync**
- [✓|⚠️] [finding or "Docs appear current"]

### Suggested Commit Message

[Draft message based on diff analysis]

### Recommendation

[PASS: Ready to commit | WARN: Review findings above]

Would you like to:
1. Proceed to `/committing-changes`
2. Fix issues first
3. Split into multiple commits
```

## Workflow Integration

**Position in workflow:**
```
/validating-implementations
   ↓ "Continue to commit?"
/reviewing-changes  <-- YOU ARE HERE
   ↓ [PASS: proceed | WARN: decide]
/committing-changes
```

**When to invoke:**
- After validation passes
- Before committing
- When unsure if changes are commit-ready

## Red Flags - STOP

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

## The Bottom Line

**Review changes. Draft message. Present findings. User decides.**

This is a quality gate, not a roadblock. WARN doesn't mean stop - it means "here's what I found, you decide."
