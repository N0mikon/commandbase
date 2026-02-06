---
name: creating-pull-requests
description: "Use this skill when creating a pull request, opening a PR for review, or generating PR descriptions. This includes analyzing commits for the PR summary, writing PR descriptions with test plans, creating the PR via gh CLI, and requesting reviewers. Trigger phrases: '/pr', 'create a PR', 'make a pull request', 'open a pull request', 'submit for review'."
---

# Create Pull Request

You are tasked with creating a pull request for the current branch.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PR WITHOUT FULL BRANCH ANALYSIS
```

If you haven't analyzed ALL commits on this branch, you cannot write the PR description.

**No exceptions:**
- Don't describe just the latest commit - analyze the full branch
- Don't create PR without user confirmation
- Don't include AI attribution in description
- Don't skip the diff review

## The Gate Function

```
BEFORE creating any pull request:

1. BRANCH: Identify current branch and base branch
2. COMMITS: Run `git log base..HEAD` to see ALL commits
3. DIFF: Run `git diff base..HEAD` to see full changes
4. ANALYZE: Understand the PURPOSE across all commits
5. DRAFT: Write title and description covering FULL scope
6. CONFIRM: Show draft to user and wait for approval
7. ONLY THEN: Create the PR with `gh pr create`

Skip any step = incomplete PR
```

## Process

### Step 1: Gather Context

Run these commands in parallel to understand the changes:

```bash
# Current branch and status
git branch --show-current
git status

# What's different from main/master
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline

# Full diff of changes
git diff main..HEAD 2>/dev/null || git diff master..HEAD
```

Also check if branch is pushed:
```bash
git status -sb
```

### Step 2: Analyze All Commits

**Important:** Look at ALL commits on this branch, not just the latest one.

- Understand the full scope of changes
- Identify the main purpose/feature
- Note any breaking changes or migration needs
- Check for related issues or tickets mentioned in commits

### Step 3: Draft PR Title and Description

Create a draft following this structure:

```markdown
## Title
[Short, descriptive title under 72 chars]

## Summary
- [Key change 1]
- [Key change 2]
- [Key change 3]

## Changes
[More detailed explanation of what changed and why]

## Testing
- [How the changes were tested]
- [What to verify during review]

## Notes
[Any additional context, breaking changes, or migration notes]
```

**Rules:**
- **NEVER** include "Generated with Claude" or similar
- **NEVER** include Co-Authored-By lines
- Write as if the user wrote it
- Summary: 1-3 bullet points
- Changes: 2-5 sentences max
- Testing: 1-3 bullet points
- Notes: Only if genuinely needed (breaking changes, migration steps). Omit if empty.
- Focus on the "why" not just the "what"

### Step 4: Present for Confirmation

Show the user the draft:

```
I've drafted the following PR:

---
**Title:** [title]

**Description:**
[full description]
---

Base branch: main (or master)
Head branch: [current branch]

Ready to create this PR? (yes/no/edit/draft)
```

**Wait for user confirmation before proceeding.**

If user says "draft":
- Create as draft PR using `gh pr create --draft`
- Note in output that it's a draft

If user says "edit" or provides feedback:
- Incorporate their changes
- Present the updated version
- Ask for confirmation again

### Step 5: Push Branch (if needed)

If the branch isn't pushed or is behind:
```bash
git push -u origin HEAD
```

### Step 6: Create Pull Request

Once confirmed, create the PR:

```bash
gh pr create --title "[title]" --body "[description]"
```

Use a HEREDOC for the body to preserve formatting:
```bash
gh pr create --title "Title here" --body "$(cat <<'EOF'
## Summary
- Point 1
- Point 2

## Changes
Description here...
EOF
)"
```

### Step 7: Report Result

```
Pull request created!

PR #[number]: [title]
URL: [pr url]

[Link to view the PR]
```

## Handling Edge Cases

**No commits ahead of main:**
```
This branch has no commits ahead of main/master.
Nothing to create a PR for.
```

**Already has open PR:**
```bash
gh pr list --head $(git branch --show-current)
```
If PR exists:
```
An open PR already exists for this branch:
PR #[number]: [title]
URL: [url]

Would you like me to update it instead?
```

**Branch not pushed:**
- Push automatically before creating PR
- Inform user: "Pushed branch to origin before creating PR"

**No remote configured:**
```
No remote configured. Please set up a remote first:
git remote add origin <repo-url>

Or use /committing-changes to auto-create a repository.
```

**gh CLI not authenticated:**
```
GitHub CLI not authenticated. Please run:
gh auth login

Then try /creating-pull-requests again.
```

## Red Flags - STOP and Analyze

If you notice any of these, STOP immediately:

- About to describe only the latest commit
- Creating PR without showing draft to user
- Including "Generated with Claude" or similar
- Branch not pushed to remote
- Skipping the full diff review

**When you hit a red flag:**
1. Stop and run full branch analysis
2. Review ALL commits, not just recent
3. Draft description and get confirmation
4. Only then create PR

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just one commit" | Check anyway. Branch history matters. |
| "User knows what changed" | PR is for reviewers. Describe fully. |
| "Description can be edited later" | Get it right first. Draft and confirm. |
| "I'll just use the commit message" | Commits are granular. PR describes the whole. |

## Important Rules

- **ALWAYS** wait for user confirmation before creating PR
- **NEVER** include AI attribution in PR description
- **NEVER** create PR without showing the description first
- **ALWAYS** check all commits, not just the most recent
- **ALWAYS** return the PR URL when complete

## The Bottom Line

**No shortcuts for PRs.**

Analyze all commits. Review full diff. Draft description. Get confirmation. THEN create.

This is non-negotiable. Every PR. Every time.
