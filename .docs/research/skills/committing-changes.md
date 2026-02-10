---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated after 62 commits - refreshed file paths to plugin structure, added via-committing-changes marker, squash merge context, red flags, edge cases, expanded commit message guidelines"
references:
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - plugins/commandbase-git-workflow/skills/reviewing-security/SKILL.md
---

# Research: committing-changes Skill

> **Updated 2026-02-09**: Refreshed to match current SKILL.md after plugin marketplace restructure. Added `# via-committing-changes` hook suppression marker, squash merge context, red flags section, edge case handling, and expanded commit message guidelines. File paths updated from `~/.claude/skills/` to `plugins/commandbase-git-workflow/skills/`.
>
> **Updated 2026-02-05**: Stale docs check moved from Step 8 (post-push) to Step 2 (pre-commit gate). Process steps renumbered accordingly.

## Overview

The `committing-changes` skill (`plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md`) is a comprehensive git workflow skill that enforces strict safety protocols for staging, committing, and pushing code changes. It integrates security review for public repositories, auto-creates GitHub repositories when needed, and checks for stale documentation as a pre-commit gate.

**Trigger phrases**: `/commit`, `commit this`, `save my work`, `push changes`, `git commit`, `commit and push`

## The Iron Law (SKILL.md:14-24)

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
   - If .env, credentials, keys found: STOP and unstage
6. **SECURITY**: If PUBLIC repo, run `/reviewing-security` on staged files
   - If BLOCK verdict: STOP and show remediation
   - If WARN verdict: Show warning, ask for confirmation
   - If PASS verdict: Continue
7. **ONLY THEN**: Commit with clear message

## Process Steps

### Step 1: Check Repository Status
```bash
git status
git remote -v
```

If no git repo exists, run `git init`. If no remote exists, continue (will create remote before push).

### Step 2: Check for Stale Documentation (Pre-Commit Gate)
Before staging, check if any `.docs/` files need updating. Finds tracked docs with `git_commit` frontmatter that are behind HEAD. If docs are >5 commits behind, offers to spawn `docs-updater` agent to include updated docs in the same commit. User can say "yes", "pick", or "skip". Skipped if `.docs/` directory doesn't exist.

### Step 3: Analyze Changes
- Run `git status` to see all changes
- Run `git diff` to understand modifications
- Review conversation history to understand what was accomplished
- Determine if changes should be one commit or multiple logical commits

### Step 4: Create Commits
Stage specific files (NEVER use `git add -A` or `git add .`):
```bash
git add path/to/file1 path/to/file2
```

**Note:** Files removed via `git rm` earlier in the session are already staged for deletion. Do not re-add them -- `git add` will fail with `fatal: pathspec did not match any files`.

Commit with a clear message. Append the `# via-committing-changes` marker to suppress the PostToolUse nudge hook:
```bash
git commit -m "Clear description of what changed and why" # via-committing-changes
```

**Commit message guidelines:**
- Use imperative mood ("Add feature" not "Added feature")
- Focus on why, not just what
- Keep first line under 72 characters
- **NEVER include Co-Authored-By or Claude attribution**
- Write as if the user wrote it
- Body: 0-3 bullet points max. If you need more, the commit is too large -- suggest splitting it.
- Total commit message (including body) should rarely exceed 5 lines

### Step 5: Security Review (Public Repos Only)
1. Check visibility: `gh repo view --json visibility -q '.visibility'`
2. If public (or visibility unknown and pushing to github.com): Invoke `/reviewing-security` with staged files
3. Handle verdict:
   - **BLOCK**: Stop the commit. Show security report with remediation. Do not proceed until CRITICAL/HIGH issues are fixed.
   - **WARN**: Show warning. Ask user: "Security review found MEDIUM issues. Proceed anyway? (yes/no)"
   - **PASS**: Continue to Step 6.
4. If private repo: Skip security review, continue to Step 6.

### Step 6: Ensure Remote Exists
Auto-create private repo if no remote:
```bash
gh repo create <repo-name> --private --source=. --remote=origin
```
Falls back to manual instructions if `gh` is not available or not authenticated.

### Step 7: Push Changes
Append the `# via-committing-changes` marker to suppress the nudge hook:
```bash
git push -u origin HEAD # via-committing-changes
```
If push fails due to diverged history, inform the user rather than force pushing.

### Step 8: Report Results
```
Committed and pushed:

[commit hash] [commit message]
[commit hash] [commit message] (if multiple)

Remote: [remote url]
Branch: [branch name]

[N] file(s) changed, [X] insertions(+), [Y] deletions(-)
```

## Security Review Integration

The `/reviewing-security` skill integrates at Step 5:
- **BLOCK verdict**: Stop commit, show remediation
- **WARN verdict**: Show warning, ask user confirmation
- **PASS verdict**: Continue to commit

## Red Flags -- STOP and Review

If any of these are noticed, STOP immediately:
- About to use `git add -A` or `git add .`
- Staging files you haven't reviewed
- Committing without understanding the diff
- .env, credentials, or keys in staged files
- About to force push
- Feeling rushed to commit

**When you hit a red flag:** Stop, run `git status`, unstage suspicious files, review the diff carefully, and stage specific files only.

## Squash Merge Context

When invoked by `/ending-session` after `git merge --squash`, the workflow adapts. Detection: `git diff --cached --stat` has content AND `$(git rev-parse --git-dir)/MERGE_MSG` exists.

**Adapted steps:**
1. **Skip Step 2** (stale docs check) -- the session's docs are the new content being committed; staleness doesn't apply.
2. **Step 3** (analyze changes): Use `git diff --cached` instead of `git diff`.
3. **Skip Step 4 staging** -- files are pre-staged by `git merge --squash`. Do NOT re-stage or unstage.
4. **Step 5** (sensitive file verification and security review): Still applies.
5. **Commit message**: Summarize the session's work. Read `MERGE_MSG` for context.
6. **Step 7** (push): Still applies.

**Iron Law still holds**: Review `git diff --cached` before committing.

## Handling Edge Cases

- **No changes to commit**: Report clean working tree.
- **Untracked sensitive files**: Warn about detected .env/credentials and suggest adding to .gitignore.
- **Push failure**: Inform user of possible causes (diverged history, permissions, network) and offer `git pull --rebase`.
- **gh CLI not available**: Provide manual instructions for creating a repo and adding a remote.

## Important Rules

- **NEVER** add Claude attribution or Co-Authored-By lines
- **NEVER** use `git add -A` or `git add .`
- **NEVER** force push without explicit user request
- **NEVER** commit sensitive files (.env, credentials, keys)
- **NEVER** skip security review for public repos
- **ALWAYS** create private repos by default when auto-creating
- **ALWAYS** push after committing
- **ALWAYS** run `/reviewing-security` before public commits

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what changed" | Run git diff anyway. Verify. |
| "`git add .` is faster" | Faster to commit wrong files too. Stage specifically. |
| "It's just this once" | One wrong commit can leak secrets. Never. |
| ".env is in .gitignore" | Check anyway. Gitignore can have holes. |
| "I need to push quickly" | Fast mistakes take longer to fix. Take time. |

## File Reference

- Main: `plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md`
- Related: `plugins/commandbase-git-workflow/skills/reviewing-security/SKILL.md`
