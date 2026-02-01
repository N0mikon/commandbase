---
name: committing-changes
description: "Use this skill when committing work to git, pushing changes to GitHub, or ending a session with saved progress. This includes staging files, writing commit messages, pushing to remote, and auto-creating private repos when needed. Trigger phrases: '/commit', 'commit this', 'save my work', 'push changes', 'git commit', 'commit and push'."
---

# Commit and Push

You are tasked with committing and pushing all changes from this session.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO COMMIT WITHOUT STAGED FILE VERIFICATION
```

If you haven't reviewed what you're staging and why, you cannot commit.

**No exceptions:**
- Don't use `git add -A` or `git add .` - stage specific files
- Don't commit without understanding the diff
- Don't stage sensitive files (.env, credentials, keys)
- Don't assume previous state - check fresh

## The Gate Function

```
BEFORE running git commit:

1. STATUS: Run `git status` to see current state
2. DIFF: Run `git diff` to understand changes
3. REVIEW: Identify logical groups of changes
4. STAGE: Add SPECIFIC files (never -A or .)
5. VERIFY: Check for sensitive files in staging
   - If .env, credentials, keys found: STOP and unstage
6. SECURITY: If PUBLIC repo, run /reviewing-security on staged files
   - If BLOCK verdict: STOP and show remediation
   - If WARN verdict: Show warning, ask for confirmation
   - If PASS verdict: Continue
7. ONLY THEN: Commit with clear message

Skip any step = risky commit
```

## Process

### Step 1: Check Repository Status

```bash
git status
git remote -v
```

If no git repo exists:
- Run `git init`
- Continue to Step 2

If no remote exists:
- Continue to Step 2 (will create remote before push)

### Step 2: Analyze Changes

- Run `git status` to see all changes
- Run `git diff` to understand modifications
- Review conversation history to understand what was accomplished
- Determine if changes should be one commit or multiple logical commits

### Step 3: Create Commit(s)

For each logical group of changes:

1. Stage specific files (never use `git add -A` or `git add .`):
   ```bash
   git add path/to/file1 path/to/file2
   ```

2. Commit with a clear message:
   ```bash
   git commit -m "Clear description of what changed and why"
   ```

**Commit message guidelines:**
- Use imperative mood ("Add feature" not "Added feature")
- Focus on why, not just what
- Keep first line under 72 characters
- **NEVER include Co-Authored-By or Claude attribution**
- Write as if the user wrote it

### Step 4: Security Review (Public Repos Only)

Before committing to a public repository, run security review:

1. Check if repo is public:
   ```bash
   gh repo view --json visibility -q '.visibility' 2>/dev/null || echo "unknown"
   ```

2. If public (or visibility unknown and pushing to github.com):
   - Invoke `/reviewing-security` skill with staged files
   - Pass the list of staged files for review

3. Handle the verdict:
   - **BLOCK**: Stop the commit. Show the security report with remediation steps. Do not proceed until CRITICAL/HIGH issues are fixed.
   - **WARN**: Show the warning. Ask user: "Security review found MEDIUM issues. Proceed anyway? (yes/no)"
   - **PASS**: Continue to Step 5.

4. If private repo: Skip security review, continue to Step 5.

### Step 5: Ensure Remote Exists

Check if remote exists:
```bash
git remote -v
```

**If no remote exists**, create a GitHub repository:

1. Determine repo name from directory name:
   ```bash
   basename $(pwd)
   ```

2. Create private repo and add as remote:
   ```bash
   gh repo create <repo-name> --private --source=. --remote=origin
   ```

   If `gh` is not authenticated or available, inform the user:
   ```
   No remote configured and couldn't auto-create repository.
   Please create a repository and run:
   git remote add origin <your-repo-url>
   ```

### Step 6: Push Changes

Push to remote:
```bash
git push -u origin HEAD
```

If the branch doesn't exist on remote yet, this creates it.

If push fails due to diverged history, inform the user rather than force pushing.

### Step 7: Report Results

```
Committed and pushed:

[commit hash] [commit message]
[commit hash] [commit message] (if multiple)

Remote: [remote url]
Branch: [branch name]

[N] file(s) changed, [X] insertions(+), [Y] deletions(-)
```

### Step 8: Check for Stale Documentation

After successful push, check if any `.docs/` files are stale:

1. Find all docs with frontmatter:
   ```bash
   # List docs and their git_commit from frontmatter
   for f in .docs/**/*.md; do
     if [ -f "$f" ]; then
       commit=$(grep -m1 "^git_commit:" "$f" 2>/dev/null | cut -d' ' -f2)
       if [ -n "$commit" ]; then
         behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null || echo "?")
         echo "$behind commits behind: $f"
       fi
     fi
   done
   ```

2. If any docs are significantly behind (>5 commits), report:
   ```
   Documentation status:
   - .docs/plans/01-15-2026-auth-impl.md (12 commits behind)
   - .docs/research/01-10-2026-auth-patterns.md (18 commits behind)

   Oldest doc is 18 commits behind.

   Update stale docs? (yes/skip/pick)
   ```

3. If user says "yes" or "pick":
   - For "yes": spawn `docs-updater` agent for the oldest doc, then ask again
   - For "pick": let user choose which doc to update
   - Process one doc at a time
   - After each update, ask if they want to continue with the next

4. If user says "skip":
   - End the command
   - Docs remain unchanged

**Note**: Skip this step if `.docs/` directory doesn't exist or contains no files with `git_commit` frontmatter.

## Red Flags - STOP and Review

If you notice any of these, STOP immediately:

- About to use `git add -A` or `git add .`
- Staging files you haven't reviewed
- Committing without understanding the diff
- .env, credentials, or keys in staged files
- About to force push
- Feeling rushed to commit

**When you hit a red flag:**
1. Stop and run `git status`
2. Unstage suspicious files
3. Review the diff carefully
4. Stage specific files only

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what changed" | Run git diff anyway. Verify. |
| "`git add .` is faster" | Faster to commit wrong files too. Stage specifically. |
| "It's just this once" | One wrong commit can leak secrets. Never. |
| ".env is in .gitignore" | Check anyway. Gitignore can have holes. |
| "I need to push quickly" | Fast mistakes take longer to fix. Take time. |

## Important Rules

- **NEVER** add Claude attribution or Co-Authored-By lines
- **NEVER** use `git add -A` or `git add .` (stage specific files)
- **NEVER** force push without explicit user request
- **NEVER** commit sensitive files (.env, credentials, keys)
- **NEVER** skip security review for public repos
- **ALWAYS** create private repos by default when auto-creating
- **ALWAYS** push after committing
- **ALWAYS** run `/reviewing-security` before public commits

## Handling Edge Cases

**No changes to commit:**
```
No changes to commit. Working tree is clean.
```

**Untracked sensitive files detected:**
```
Warning: Detected potentially sensitive files that won't be committed:
- .env
- credentials.json

These files should be in .gitignore.
```

**Remote exists but push fails:**
```
Push failed. This might be because:
- Branch has diverged from remote
- No permission to push
- Network issue

Error: [actual error message]

Would you like me to try `git pull --rebase` first?
```

**gh CLI not available:**
```
Cannot auto-create repository (gh CLI not available or not authenticated).

To set up manually:
1. Create a repo at https://github.com/new
2. Run: git remote add origin <repo-url>
3. Run: /committing-changes again
```

## The Bottom Line

**No shortcuts for committing.**

Check status. Review diff. Stage specific files. Verify no secrets. THEN commit.

This is non-negotiable. Every commit. Every time.
