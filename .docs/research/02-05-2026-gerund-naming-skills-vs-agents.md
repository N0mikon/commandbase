# Gerund Naming Convention: Skills vs Agents

**Date**: 02-05-2026
**Question**: What is the reasoning behind gerund format naming for skills? Should agents use the same format or a different one?

## Key Finding

Skills and agents deliberately use **different naming conventions** because they serve different purposes and have different activation models.

| Component | Naming Format | Example | Mental Model |
|-----------|--------------|---------|--------------|
| **Skills** | Gerund (verb-ing) | `reviewing-code` | User is performing an action |
| **Agents** | Noun/role | `code-reviewer` | A specialist being delegated to |

## Why Skills Use Gerund Form

**Source**: `newskills/creating-skills/reference/naming-conventions.md:5-21`

Skills activate when Claude recognizes the user is **performing an action**. Gerund names align with that mental model:

- The user is "creating skills" -> `creating-skills` skill activates
- The user is "researching codebases" -> `researching-code` skill activates
- The user is "reviewing changes" -> `reviewing-changes` skill activates

Noun names (e.g., `skill-creator`) describe a tool that exists. Gerund names describe an action being performed. Skills are triggered by intent matching against descriptions, so the name reinforces the activation-oriented framing.

**Source**: `newskills/creating-skills/reference/naming-conventions.md:15-18`

The naming conventions doc explicitly calls out noun-form names as "agent-style naming, not skill-style":
- `lambda-deployer` - "agent-style naming, not skill-style"
- `skill-creator` - "names the tool, not the action"

## Why Agents Use Noun/Role Form

**Source**: `newskills/creating-skills/reference/converting-subagents.md:5-12`

The distinction is explicit:
- **Sub-agents explain WHAT they are** (identity/noun form)
- **Skills explain WHEN to use them** (activation/gerund form)

An agent says: "I am a code reviewer that analyzes pull requests."
A skill says: "Use this skill when reviewing code for quality issues."

Agents are invoked explicitly via the Task tool or `@mention`. They don't need intent-matching activation - they're called by name when Claude (or the user) decides to delegate work to a specialist. The noun form makes them read as **roles** or **specialists**:

- `code-analyzer` - a specialist that analyzes codebases
- `docs-locator` - a specialist that locates documents
- `web-researcher` - a specialist that researches via web search

## Current Agent Names (All 7)

**Source**: `~/.claude/agents/` and `newagents/`

| Agent Name | Pattern |
|-----------|---------|
| `code-analyzer` | {subject}-{role} |
| `code-locator` | {subject}-{role} |
| `code-librarian` | {subject}-{role} |
| `docs-analyzer` | {subject}-{role} |
| `docs-locator` | {subject}-{role} |
| `docs-updater` | {subject}-{role} |
| `web-researcher` | {domain}-{role} |

## Conversion Table (Agent <-> Skill)

**Source**: `newskills/creating-skills/reference/converting-subagents.md:31-37`

| Agent Name (Noun) | Skill Name (Gerund) |
|-------------------|-------------------|
| `code-reviewer` | `reviewing-code` |
| `test-runner` | `running-tests` |
| `doc-generator` | `generating-docs` |
| `bug-triager` | `triaging-bugs` |
| `deploy-manager` | `managing-deployments` |

## The Reasoning Gap

There is **no formal agent naming convention document** equivalent to the skill naming conventions doc at `newskills/creating-skills/reference/naming-conventions.md`. Agent naming is inferred from existing examples rather than formally specified.

The closest documentation is:
- `converting-subagents.md` which contrasts the two conventions
- `.docs/research/02-05-2026-agent-creation-best-practices.md` which covers agent frontmatter but doesn't prescribe a naming pattern

## Summary

**Should agents use gerund form?** No. The deliberate distinction serves a purpose:

1. **Skills = gerund** because they activate via intent matching ("the user is doing X")
2. **Agents = noun/role** because they're delegated to as specialists ("send this to the X-er")

The naming convention difference reinforces the different mental models for how each component is discovered and invoked. Applying gerund naming to agents would blur this useful distinction.

However, there is no formal agent naming guide - only the implicit convention from existing agents. A formal document parallel to the skill naming conventions could be valuable.
