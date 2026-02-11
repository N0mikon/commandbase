# commandbase-git-workflow

Opinionated git commit workflow with security review and docs staleness detection. Requires commandbase-core for docs agents.

For full commit enforcement, you'll also need to add deny rules from SETUP.md to your `~/.claude/settings.json`.

## Dependencies

- commandbase-core (docs agents)

## Skills

| Skill | Description |
|-------|-------------|
| /auditing-docs | Audit .docs/ documents for staleness and spawn updaters for stale files |
| /committing-changes | Commit work to git with staged file verification, security review, and docs staleness detection |
| /creating-prs | Create pull requests with commit analysis and PR descriptions |
| /reviewing-changes | Review code changes before committing — check for debug statements, split decisions |
| /reviewing-security | Review code for security vulnerabilities before committing to public repos |

## Hooks

| Event | Description |
|-------|-------------|
| PostToolUse (Bash) | Nudges toward /committing-changes when a bare `git commit` is detected |

## Installation

```shell
/plugin install commandbase-git-workflow
```
