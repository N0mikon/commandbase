# Review Report Template

Use this format when presenting review findings.

---

## Review: [PASS|WARN]

**Files reviewed:** [N] files
**Lines changed:** +[added] / -[removed]

---

### Findings

**Code Cleanliness**
- [✓|⚠️] [Description]
  - [Details if warning]

**Commit Atomicity**
- [✓|⚠️] [Description]
  - [File groupings if suggesting split]

**Diff Coherence**
- [✓|⚠️] [Description]
  - [Suspicious files if warning]

**Documentation Sync**
- [✓|⚠️] [Description]
  - [Specific docs to update if warning]

---

### Suggested Commit Message

```
[type]: [summary]

[Optional body with details]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Type options:** feat | fix | refactor | docs | test | chore

---

### Recommendation

**[PASS]** Ready to commit. No issues found.

**[WARN]** Found issues that may warrant attention:
- [Issue 1]
- [Issue 2]

---

### Next Steps

Would you like to:
1. **Proceed** - Continue to `/committing-changes` with suggested message
2. **Fix first** - Address warnings before committing
3. **Split commits** - Break into multiple logical commits

---

## Example: PASS Report

```markdown
## Review: PASS

**Files reviewed:** 3 files
**Lines changed:** +47 / -12

### Findings

**Code Cleanliness**
- ✓ No debug statements found
- ✓ No commented-out code

**Commit Atomicity**
- ✓ Single logical change (adding user validation)

**Diff Coherence**
- ✓ All files related to validation feature

**Documentation Sync**
- ✓ No public API changes requiring doc updates

### Suggested Commit Message

feat: Add email validation to user registration

- Add validateEmail function in src/utils/validation.ts
- Integrate validation in registration form
- Add unit tests for email validation

Co-Authored-By: Claude <noreply@anthropic.com>

### Recommendation

Ready to commit. No issues found.

Proceed to `/committing-changes`?
```

---

## Example: WARN Report

```markdown
## Review: WARN

**Files reviewed:** 7 files
**Lines changed:** +156 / -23

### Findings

**Code Cleanliness**
- ⚠️ Found debug statement
  - `console.log` at src/api/users.ts:47

**Commit Atomicity**
- ⚠️ Changes span unrelated concerns
  - Auth changes: src/auth/*.ts (3 files)
  - UI refactor: src/components/*.tsx (2 files)
  - Config update: config/settings.json (1 file)

**Diff Coherence**
- ⚠️ package-lock.json changed without package.json changes

**Documentation Sync**
- ✓ No public API changes requiring doc updates

### Suggested Commit Message

[Hard to summarize - consider splitting]

Option A (if keeping together):
refactor: Update auth flow and UI components

Option B (if splitting):
1. feat: Implement new auth token refresh
2. refactor: Simplify component hierarchy
3. chore: Update config settings

### Recommendation

Found 3 issues that may warrant attention:
- Debug statement should be removed
- Consider splitting into 3 commits by concern
- Verify package-lock.json change is intentional

### Next Steps

Would you like to:
1. Proceed anyway (issues are acceptable)
2. Fix the debug statement and review again
3. Split into multiple commits
```
