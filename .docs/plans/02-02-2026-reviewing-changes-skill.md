# Plan: reviewing-changes Skill

## Overview

Create a pre-commit quality gate skill that reviews code changes between `/validating-code` and `/committing-changes`. Uses PASS/WARN verdicts (no auto-blocking) to surface quality issues while letting the user decide whether to proceed.

## Context

**Research:** `.docs/research/02-02-2026-reviewing-and-updating-skills-research.md`

**The Gap:**
- `/validating-code` confirms code matches plan and tests pass
- `/committing-changes` checks git status, security (public repos only)
- Between them: no check for code quality, commit structure, or message quality

**Integration Points:**
- Input: Validation complete, changed files ready
- Output: Quality report with suggested commit messages
- Next: `/committing-changes` uses the suggestions

## What We're NOT Doing

- No auto-BLOCK verdicts (user always decides)
- No security checks (that's `/reviewing-security`)
- No spec compliance (that's `/validating-code`)
- No enforcement of commit message format (suggest, don't require)

---

## Phase 1: Define Check Categories

### Goal
Establish what "quality" means for this skill.

### Tasks
- [x] Define 5 check categories with specific criteria
- [x] Define what triggers WARN for each category
- [x] Create severity guidance (which WARNs matter most) - Added ranking in SKILL.md

### Check Categories

**1. Code Cleanliness**
- Debug statements left in (console.log, print, debugger)
- Commented-out code blocks
- TODO/FIXME comments in new code
- Unused imports or variables

**2. Commit Atomicity**
- Changes span unrelated concerns
- Multiple logical changes in one diff
- Suggest split if changes are separable

**3. Commit Message Quality**
- Draft message based on diff analysis
- Flag if changes are hard to summarize (sign of poor atomicity)

**4. Diff Coherence**
- Unrelated files modified together
- Accidental inclusions (lockfiles, generated files)
- Whitespace-only changes mixed with real changes

**5. Documentation Sync**
- README mentions changed functionality
- CLAUDE.md references modified patterns
- API docs for changed endpoints

### Success Criteria
- [x] Check categories documented in SKILL.md
- [x] Each category has clear WARN triggers
- [x] Categories are actionable (can be fixed)

---

## Phase 2: Create Verdict Logic

### Goal
Define how checks combine into PASS/WARN verdicts.

### Tasks
- [x] Define PASS criteria (no issues found)
- [x] Define WARN criteria (issues found, user decides)
- [x] Create report format showing findings

### Verdict Rules

**PASS** - All checks clear
- No debug statements
- Single logical change OR user confirms intentional grouping
- Documentation appears synced
- Commit message draft provided

**WARN** - Issues found, user decides
- List all findings by category
- Suggest fixes for each
- Ask: "Proceed anyway?" or "Fix first?"

### Report Format

```markdown
## Review: [PASS|WARN]

### Findings

**Code Cleanliness**
- ⚠️ Found `console.log` at src/utils.ts:47
- ✓ No commented-out code

**Commit Atomicity**
- ⚠️ Changes span 3 unrelated areas (suggest splitting)
  - Auth changes: src/auth/*.ts
  - UI changes: src/components/*.tsx
  - Config changes: config/*.json

**Documentation**
- ⚠️ README mentions "login flow" but auth files changed

### Suggested Commit Message
[Draft based on diff analysis]

### Recommendation
[Proceed with warnings | Fix issues first]
```

### Success Criteria
- [x] Verdict logic documented
- [x] Report format specified
- [x] User decision point clear

---

## Phase 3: Write SKILL.md

### Goal
Create the main skill file following enforcement patterns.

### Tasks
- [x] Write frontmatter (name, description)
- [x] Write Iron Law
- [x] Write Gate Function
- [x] Write review process
- [x] Write Red Flags and Rationalization Prevention

### Structure

```
newskills/reviewing-changes/
├── SKILL.md              # Main skill (~200 lines)
└── templates/
    └── review-report.md  # Output template
```

### Key Sections

**Iron Law:** `NO COMMIT WITHOUT REVIEWING CHANGES FIRST`

**Gate Function:**
1. Get list of changed files (git status)
2. Get full diff (git diff)
3. Run 5 check categories
4. Compile findings into report
5. Present verdict and suggestions
6. ONLY THEN: User decides to proceed or fix

**Integration with workflow:**
- Triggered after `/validating-code` says "Continue to commit?"
- Produces report that `/committing-changes` can use
- Suggested commit message passed forward

### Success Criteria
- [x] SKILL.md follows enforcement pattern
- [x] Under 300 lines (simple skill) - 270 lines
- [x] Description uses WHEN formula
- [x] Passes validation checklist

---

## Phase 4: Add Templates

### Goal
Create output template for consistent reports.

### Tasks
- [x] Create review-report.md template
- [x] Include all check categories
- [x] Include commit message draft section

### Template Content

Located at `templates/review-report.md`:
- Header with verdict
- Findings by category (with ✓/⚠️ markers)
- Suggested commit message
- Recommendation (proceed/fix)
- User decision prompt

### Success Criteria
- [x] Template covers all check categories
- [x] Template is actionable (shows what to fix)
- [x] Commit message section included

---

## Phase 5: Integration and Testing

### Goal
Connect skill to workflow and validate it works.

### Tasks
- [x] Deploy to ~/.claude/skills/
- [x] Test on real changes
- [x] Verify report format works
- [x] Update workflow documentation - Added option 4 to /validating-code

### Integration Points

**After validation:**
```
/validating-code
   ↓ "Continue to commit/PR?"
   ↓
/reviewing-changes  <-- invoke here
   ↓ [PASS: proceed | WARN: decide]
   ↓
/committing-changes
```

**Workflow suggestion:** Add to `/validating-code` next-action prompt:
- Option 5: "Review changes before committing"

### Success Criteria
- [x] Skill deployed and invocable
- [x] Works on test changes
- [x] Report is readable and actionable
- [x] Integrates smoothly with commit workflow

---

## Verification

After all phases complete:
- [x] `/reviewing-changes` invocable
- [x] Runs 5 check categories
- [x] Produces PASS/WARN verdict
- [x] Includes suggested commit message
- [x] User decides whether to proceed
