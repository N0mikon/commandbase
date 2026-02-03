# Research: committing-changes Skill

## Overview

The `committing-changes` skill (`~/.claude/skills/committing-changes/SKILL.md`) is a comprehensive git workflow skill that enforces strict safety protocols for staging, committing, and pushing code changes. It integrates security review for public repositories, auto-creates GitHub repositories when needed, and checks for stale documentation after successful pushes.

**Trigger phrases**: `/commit`, `commit this`, `save my work`, `push changes`, `git commit`, `commit and push`

## The Iron Law (SKILL.md:12-24)

```
NO COMMIT WITHOUT STAGED FILE VERIFICATION
```

**Absolute restrictions:**
- Don't use `git add -A` or `git add .` - stage specific files only
- Don't commit without understanding the diff
- Don't stage sensitive files (.env, credentials, keys)
- Don't assume previous state - check fresh every time

## The Gate Function (SKILL.md:26-44)

7-step checklist before any `git commit`:

1. **STATUS**: Run `git status` to see current state
2. **DIFF**: Run `git diff` to understand changes
3. **REVIEW**: Identify logical groups of changes
4. **STAGE**: Add SPECIFIC files (never -A or .)
5. **VERIFY**: Check for sensitive files in staging
6. **SECURITY**: If PUBLIC repo, run `/reviewing-security` on staged files
7. **ONLY THEN**: Commit with clear message

## Process Steps

### Step 1: Check Repository Status
```bash
git status
git remote -v
```

### Step 2: Analyze Changes
- Run `git status` to see all changes
- Run `git diff` to understand modifications
- Determine if changes should be one commit or multiple

### Step 3: Create Commits
Stage specific files (NEVER use `git add -A` or `git add .`):
```bash
git add path/to/file1 path/to/file2
git commit -m "Clear description of what changed and why"
```

**Commit message guidelines:**
- Use imperative mood ("Add feature" not "Added feature")
- Focus on why, not just what
- Keep first line under 72 characters
- **NEVER include Co-Authored-By or Claude attribution**

### Step 4: Security Review (Public Repos Only)
1. Check visibility: `gh repo view --json visibility -q '.visibility'`
2. If public: Invoke `/reviewing-security` with staged files
3. Handle verdict: BLOCK (halt), WARN (ask confirmation), PASS (continue)

### Step 5: Ensure Remote Exists
Auto-create private repo if no remote:
```bash
gh repo create <repo-name> --private --source=. --remote=origin
```

### Step 6: Push Changes
```bash
git push -u origin HEAD
```

### Step 7: Report Results
```
Committed and pushed:
[commit hash] [commit message]
Remote: [remote url]
Branch: [branch name]
```

### Step 8: Check for Stale Documentation
Find docs >5 commits behind HEAD and offer to spawn `docs-updater` agent.

## Security Review Integration

The `/reviewing-security` skill integrates at Step 4:
- **BLOCK verdict**: Stop commit, show remediation
- **WARN verdict**: Show warning, ask user confirmation
- **PASS verdict**: Continue to commit

## Important Rules

- **NEVER** add Claude attribution or Co-Authored-By lines
- **NEVER** use `git add -A` or `git add .`
- **NEVER** force push without explicit user request
- **NEVER** commit sensitive files
- **ALWAYS** create private repos by default
- **ALWAYS** run `/reviewing-security` before public commits

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what changed" | Run git diff anyway. Verify. |
| "`git add .` is faster" | Faster to commit wrong files too. Stage specifically. |
| "It's just this once" | One wrong commit can leak secrets. Never. |
| ".env is in .gitignore" | Check anyway. Gitignore can have holes. |

## File Reference

- Main: `~/.claude/skills/committing-changes/SKILL.md`
- Related: `~/.claude/skills/reviewing-security/SKILL.md`
