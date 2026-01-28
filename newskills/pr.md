---
description: Generate PR description and create pull request with confirmation
---

# Create Pull Request

You are tasked with creating a pull request for the current branch.

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
- Be concise but thorough
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

Or use /commit to auto-create a repository.
```

**gh CLI not authenticated:**
```
GitHub CLI not authenticated. Please run:
gh auth login

Then try /pr again.
```

## Important Rules

- **ALWAYS** wait for user confirmation before creating PR
- **NEVER** include AI attribution in PR description
- **NEVER** create PR without showing the description first
- **ALWAYS** check all commits, not just the most recent
- **ALWAYS** return the PR URL when complete
