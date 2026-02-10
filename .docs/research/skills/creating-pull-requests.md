---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file path from ~/.claude/skills/ to plugin location, synced content with current SKILL.md (draft handling, red flags section, bottom line section)"
references:
  - plugins/commandbase-git-workflow/skills/creating-prs/SKILL.md
---

# Research: creating-prs Skill

## Overview

The `creating-prs` skill (`plugins/commandbase-git-workflow/skills/creating-prs/SKILL.md`) orchestrates the complete workflow for creating GitHub pull requests via the `gh` CLI. It enforces mandatory analysis of ALL commits on a branch before drafting PR descriptions, requiring user confirmation before execution.

**Trigger phrases**: `/pr`, `create a PR`, `make a pull request`, `open a pull request`, `submit for review`

## The Iron Law (SKILL.md:12-24)

```
NO PR WITHOUT FULL BRANCH ANALYSIS
```

**Absolute requirements:**
- Must analyze ALL commits on the branch, not just the latest
- Cannot create PR without user confirmation
- Cannot include AI attribution in description
- Cannot skip the diff review

## The Gate Function (SKILL.md:26-40)

7-step mandatory process:

1. **BRANCH**: Identify current branch and base branch
2. **COMMITS**: Run `git log base..HEAD` to see ALL commits
3. **DIFF**: Run `git diff base..HEAD` to see full changes
4. **ANALYZE**: Understand the PURPOSE across all commits
5. **DRAFT**: Write title and description covering FULL scope
6. **CONFIRM**: Show draft to user and wait for approval
7. **ONLY THEN**: Create the PR with `gh pr create`

## Process Steps

### Step 1: Gather Context
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
- Look at ALL commits on branch, not just latest
- Identify main purpose/feature
- Note breaking changes or migration needs
- Check for related issues mentioned in commits

### Step 3: Draft PR Title and Description
```markdown
## Title
[Short, descriptive title under 72 chars]

## Summary
- [Key change 1]
- [Key change 2]

## Changes
[Detailed explanation of what changed and why]

## Testing
- [How changes were tested]
- [What to verify during review]

## Notes
[Additional context, breaking changes, migration notes]
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
```
I've drafted the following PR:

---
**Title:** [title]
**Description:** [full description]
---

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
```bash
git push -u origin HEAD
```

### Step 6: Create Pull Request
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
```

## Edge Cases

- **No commits ahead**: Report "Nothing to create a PR for"
- **Already has open PR**: Offer to update existing PR
- **Branch not pushed**: Push automatically first
- **No remote configured**: Direct to `/committing-changes` for repo creation
- **gh CLI not authenticated**: Instruct user to run `gh auth login`

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
- **ALWAYS** check all commits, not just the most recent
- **ALWAYS** return the PR URL when complete
- **NEVER** include AI attribution in PR description
- **NEVER** create PR without showing the description first

## The Bottom Line

**No shortcuts for PRs.**

Analyze all commits. Review full diff. Draft description. Get confirmation. THEN create.

This is non-negotiable. Every PR. Every time.

## File Reference

- Main: `plugins/commandbase-git-workflow/skills/creating-prs/SKILL.md`
