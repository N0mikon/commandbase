---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file paths from newskills/newagents to plugins/ structure, updated agent count from 7 to 8, noted that the agent naming gap has been filled"
references:
  - plugins/commandbase-meta/skills/creating-skills/reference/naming-conventions.md
  - plugins/commandbase-meta/skills/creating-skills/reference/converting-subagents.md
  - plugins/commandbase-meta/skills/creating-agents/reference/naming-conventions.md
  - plugins/commandbase-code/agents/code-analyzer.md
  - plugins/commandbase-code/agents/code-librarian.md
  - plugins/commandbase-code/agents/code-locator.md
  - plugins/commandbase-core/agents/docs-analyzer.md
  - plugins/commandbase-core/agents/docs-locator.md
  - plugins/commandbase-core/agents/docs-updater.md
  - plugins/commandbase-core/agents/docs-writer.md
  - plugins/commandbase-research/agents/web-researcher.md
---

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

**Source**: `plugins/commandbase-meta/skills/creating-skills/reference/naming-conventions.md:5-21`

Skills activate when Claude recognizes the user is **performing an action**. Gerund names align with that mental model:

- The user is "creating skills" -> `creating-skills` skill activates
- The user is "researching codebases" -> `researching-code` skill activates
- The user is "reviewing changes" -> `reviewing-changes` skill activates

Noun names (e.g., `skill-creator`) describe a tool that exists. Gerund names describe an action being performed. Skills are triggered by intent matching against descriptions, so the name reinforces the activation-oriented framing.

**Source**: `plugins/commandbase-meta/skills/creating-skills/reference/naming-conventions.md:15-18`

The naming conventions doc explicitly calls out noun-form names as "agent-style naming, not skill-style":
- `lambda-deployer` - "agent-style naming, not skill-style"
- `skill-creator` - "names the tool, not the action"

## Why Agents Use Noun/Role Form

**Source**: `plugins/commandbase-meta/skills/creating-skills/reference/converting-subagents.md:5-12`

The distinction is explicit:
- **Sub-agents explain WHAT they are** (identity/noun form)
- **Skills explain WHEN to use them** (activation/gerund form)

An agent says: "I am a code reviewer that analyzes pull requests."
A skill says: "Use this skill when reviewing code for quality issues."

Agents are invoked explicitly via the Task tool or `@mention`. They don't need intent-matching activation - they're called by name when Claude (or the user) decides to delegate work to a specialist. The noun form makes them read as **roles** or **specialists**:

- `code-analyzer` - a specialist that analyzes codebases
- `docs-locator` - a specialist that locates documents
- `web-researcher` - a specialist that researches via web search

## Current Agent Names (All 8)

**Source**: `plugins/commandbase-code/agents/`, `plugins/commandbase-core/agents/`, `plugins/commandbase-research/agents/`

| Agent Name | Plugin | Pattern |
|-----------|--------|---------|
| `code-analyzer` | commandbase-code | {subject}-{role} |
| `code-locator` | commandbase-code | {subject}-{role} |
| `code-librarian` | commandbase-code | {subject}-{role} |
| `docs-analyzer` | commandbase-core | {subject}-{role} |
| `docs-locator` | commandbase-core | {subject}-{role} |
| `docs-updater` | commandbase-core | {subject}-{role} |
| `docs-writer` | commandbase-core | {subject}-{role} |
| `web-researcher` | commandbase-research | {domain}-{role} |

## Conversion Table (Agent <-> Skill)

**Source**: `plugins/commandbase-meta/skills/creating-skills/reference/converting-subagents.md:31-37`

| Agent Name (Noun) | Skill Name (Gerund) |
|-------------------|-------------------|
| `code-reviewer` | `reviewing-code` |
| `test-runner` | `running-tests` |
| `doc-generator` | `generating-docs` |
| `bug-triager` | `triaging-bugs` |
| `deploy-manager` | `managing-deployments` |

## The Reasoning Gap (Resolved)

~~There is **no formal agent naming convention document** equivalent to the skill naming conventions doc.~~

**Update (2026-02-09):** This gap has been filled. A formal agent naming conventions document now exists at `plugins/commandbase-meta/skills/creating-agents/reference/naming-conventions.md`. It covers the noun rule, `{domain}-{role}` patterns, format rules, role suffixes, agent families, and agent-to-skill name conversion -- providing the same level of formal specification that skills already had.

Related documentation:
- `plugins/commandbase-meta/skills/creating-skills/reference/converting-subagents.md` which contrasts the two conventions
- `.docs/research/02-05-2026-agent-creation-best-practices.md` which covers agent frontmatter

## Summary

**Should agents use gerund form?** No. The deliberate distinction serves a purpose:

1. **Skills = gerund** because they activate via intent matching ("the user is doing X")
2. **Agents = noun/role** because they're delegated to as specialists ("send this to the X-er")

The naming convention difference reinforces the different mental models for how each component is discovered and invoked. Applying gerund naming to agents would blur this useful distinction.

A formal agent naming guide now exists at `plugins/commandbase-meta/skills/creating-agents/reference/naming-conventions.md`, providing parity with the skill naming conventions.
