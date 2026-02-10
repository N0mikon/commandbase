---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Reviewed after 62 commits - archived document verified, source files unchanged, content still accurate"
topic: "/skill-create Command - Extract Patterns from Git"
tags: [research, skill-create, git, patterns]
status: archived
archived: 2026-02-09
archive_reason: "Research complete and consumed during creating-skills skill development. All references are external to this repo. 56 commits behind HEAD with no further relevance to active work."
references:
  - C:/code/everything-claude-code/commands/skill-create.md
  - C:/code/everything-claude-code/skills/continuous-learning-v2/SKILL.md
  - C:/code/everything-claude-code/skills/continuous-learning-v2/scripts/instinct-cli.py
---

# Research: /skill-create Command Pattern

**Date**: 2026-01-28
**Source**: everything-claude-code

## Summary

Analyzes git history to extract coding patterns and generate SKILL.md files. Can also generate "instincts" for the continuous-learning-v2 system. Serves as local alternative to Skill Creator GitHub App.

## Usage (`commands/skill-create.md:13-18`)

```bash
/skill-create                    # Analyze current repo, 200 commits
/skill-create --commits 100      # Custom commit count
/skill-create --output ./skills  # Custom output directory
/skill-create --instincts        # Also generate instincts
```

## Git Analysis Commands (`commands/skill-create.md:29-40`)

```bash
# Commit log with file changes
git log --oneline -n ${COMMITS:-200} --name-only --pretty=format:"%H|%s|%ad" --date=short

# File change frequency (top 20)
git log --oneline -n 200 --name-only | grep -v "^$" | grep -v "^[a-f0-9]" | sort | uniq -c | sort -rn | head -20

# Commit message patterns
git log --oneline -n 200 | cut -d' ' -f2- | head -50
```

## Pattern Detection (`commands/skill-create.md:45-53`)

| Pattern Type | Detection Method |
|--------------|------------------|
| **Commit conventions** | Regex on messages (feat:, fix:, chore:) |
| **File co-changes** | Files that always change together |
| **Workflow sequences** | Repeated file change patterns |
| **Architecture** | Folder structure and naming |
| **Testing patterns** | Test file locations, naming, coverage |

## Output: SKILL.md (`commands/skill-create.md:55-80`)

```markdown
---
name: {repo-name}-patterns
description: Coding patterns extracted from {repo-name}
version: 1.0.0
source: local-git-analysis
analyzed_commits: {count}
---

# {Repo Name} Patterns

## Commit Conventions
{detected commit message patterns}

## Code Architecture
{detected folder structure}

## Workflows
{detected repeating file change patterns}

## Testing Patterns
{detected test conventions}
```

## Output: Instincts (`commands/skill-create.md:82-103`)

With `--instincts` flag, also generates:

```yaml
---
id: {repo}-commit-convention
trigger: "when writing a commit message"
confidence: 0.8
domain: git
source: local-repo-analysis
---

# Use Conventional Commits

## Action
Prefix commits with: feat:, fix:, chore:, docs:, test:, refactor:

## Evidence
- Analyzed {n} commits
- {percentage}% follow conventional commit format
```

Saved to `~/.claude/homunculus/instincts/inherited/`

## Related Commands

| Command | Purpose |
|---------|---------|
| `/instinct-status` | View learned instincts with confidence |
| `/instinct-import` | Import instincts from others |
| `/instinct-export` | Export instincts for sharing |
| `/evolve` | Cluster instincts into skills/commands/agents |

## Adaptation for Commandbase

### Project Onboarding

Use /skill-create when starting work on a new codebase:

```bash
/skill-create --commits 500 --output .docs/project-patterns/
```

Generates:
- Commit conventions to follow
- File organization patterns
- Workflow sequences to maintain
- Testing conventions

### Integration with /rcode

After `/skill-create` runs, reference the generated patterns in research:

```markdown
## Existing Patterns (from /skill-create)

See `.docs/project-patterns/SKILL.md` for:
- Commit conventions: {format}
- File organization: {structure}
- Testing: {conventions}
```

### Trade-offs

**Pros**:
- Automated pattern discovery
- Onboards to new codebases quickly
- Generates reusable skill files

**Cons**:
- Requires meaningful git history
- Detection is heuristic-based
- May miss implicit patterns

### Recommendation

**Low priority** - Useful for onboarding to new projects but not core to RPI workflow. Consider as utility command rather than workflow improvement.

## Code References

- Command definition: `C:/code/everything-claude-code/commands/skill-create.md:1-175`
- Git commands: `commands/skill-create.md:29-40`
- Pattern detection: `commands/skill-create.md:45-53`
- SKILL.md format: `commands/skill-create.md:55-80`
- Instinct format: `commands/skill-create.md:82-103`
- CLI implementation: `skills/continuous-learning-v2/scripts/instinct-cli.py`
