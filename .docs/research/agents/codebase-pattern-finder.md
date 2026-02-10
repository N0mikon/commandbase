---
title: "Research: code-librarian Agent"
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file path from ~/.claude/agents/ to plugin location, refreshed capabilities and integration points to match current agent definition"
references:
  - plugins/commandbase-code/agents/code-librarian.md
  - plugins/commandbase-code/skills/planning-code/reference/research-workflow.md
  - plugins/commandbase-code/skills/researching-code/reference/research-agents.md
  - plugins/commandbase-code/skills/structuring-code/SKILL.md
  - plugins/commandbase-code/skills/starting-refactors/SKILL.md
---

# Research: code-librarian Agent

## Overview

The `code-librarian` agent (`plugins/commandbase-code/agents/code-librarian.md`) finds similar implementations, usage examples, or existing patterns that can be modeled after. It provides concrete code examples. Runs on the `sonnet` model.

**When to Use**: When looking for patterns to follow or examples to model after.

**Key Constraint**: The agent is a documentarian, not a critic. It shows existing patterns exactly as they appear without evaluating, critiquing, or recommending improvements unless explicitly asked.

## Capabilities

- Search code with Grep tool
- Find files with Glob tool
- Read files with Read tool
- List directories with LS tool

**Tools Available**: Grep, Glob, Read, LS

## Search Strategy

The agent follows a structured approach:

1. **Identify Pattern Types** -- Categorize what the user is seeking (feature, structural, integration, or testing patterns)
2. **Search** -- Use Grep, Glob, and LS to locate relevant code
3. **Read and Extract** -- Read files, extract relevant sections, note context, identify variations

## Use Cases

1. **Pattern Discovery**: Find how something is done elsewhere
2. **Example Finding**: Locate code to model after
3. **Convention Identification**: Discover coding conventions
4. **Consistency Checking**: See how similar things are implemented

## Output Format

Returns patterns with code examples:
```markdown
## Pattern Examples: [Pattern Type]

### Pattern 1: [Descriptive Name]
**Found in**: `src/api/users.js:45-67`
**Used for**: [When this pattern is used]

```code
// Code example with full context
```

**Key aspects**:
- Notable implementation details

### Pattern 2: [Alternative Approach]
**Found in**: `path/to/other.ts:15-30`
**Used for**: [When this pattern is used]

### Pattern Usage in Codebase
- **Pattern A**: Found in X, Y, Z
- **Pattern B**: Found in A, B, C
```

## Integration Points

- Deep research phase of `/planning-code` (via `reference/research-workflow.md`)
- Pattern identification for `/researching-code` (via `reference/research-agents.md`)
- Convention discovery for `/creating-skills`
- Test file placement conventions for `/structuring-code`
- Test coverage assessment for `/starting-refactors`

## File Reference

- Agent: `plugins/commandbase-code/agents/code-librarian.md`
