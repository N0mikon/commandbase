---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter; updated file path from ~/.claude/agents/ to plugin location; corrected integration points; expanded output format to match actual agent definition; added documentarian identity note"
references:
  - plugins/commandbase-code/agents/code-analyzer.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/researching-code/SKILL.md
  - plugins/commandbase-code/skills/structuring-code/SKILL.md
  - plugins/commandbase-code/skills/starting-refactors/SKILL.md
  - plugins/commandbase-research/skills/researching-repo/SKILL.md
---

# Research: code-analyzer Agent

## Overview

The `code-analyzer` agent (`plugins/commandbase-code/agents/code-analyzer.md`) analyzes codebase implementation details. It's a read-only agent that provides detailed information about specific components. Its core identity is that of a **documentarian, not a critic** -- it explains HOW code works without suggesting improvements, identifying bugs, or critiquing design.

**When to Use**: When you need to find detailed information about specific components -- implementation details, data flow, architectural patterns, or how modules interact.

**Model**: sonnet

## Capabilities

- Read files with Read tool
- Search code with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Read, Grep, Glob, LS

## Core Responsibilities

1. **Analyze Implementation Details** -- Read specific files, identify key functions and their purposes, trace method calls and data transformations
2. **Trace Data Flow** -- Follow data from entry to exit points, map transformations and validations, identify state changes and side effects
3. **Identify Architectural Patterns** -- Recognize design patterns in use, note architectural decisions, find integration points between systems

## Analysis Strategy

The agent follows a three-step process:
1. **Read Entry Points** -- Start with main files, look for exports/public methods/route handlers
2. **Follow the Code Path** -- Trace function calls step by step, read each file involved
3. **Document Key Logic** -- Describe business logic, validation, transformation, error handling as-is (no evaluation)

## Use Cases

1. **Component Analysis**: Understand how a specific module works
2. **Data Flow Tracing**: Track data through the system
3. **Dependency Mapping**: Find what depends on what
4. **Pattern Identification**: Discover recurring patterns

## Output Format

Returns structured analysis with file:line references:
```markdown
## Analysis: [Feature/Component Name]

### Overview
[2-3 sentence summary of how it works]

### Entry Points
- `api/routes.js:45` - POST /webhooks endpoint
- `handlers/webhook.js:12` - handleWebhook() function

### Core Implementation
#### 1. [Step Name] (`file:lines`)
- [Detail with specific references]

### Data Flow
1. Request arrives at `file:line`
2. Routed to `file:line`
3. Processing at `file:line`

### Key Patterns
- **[Pattern Name]**: [Where it appears with file:line]

### Configuration
- [Config source with file:line]

### Error Handling
- [Error scenario with file:line]
```

## Integration Points

- Spawned by `/planning-code` for initial codebase research (paired with code-locator)
- Spawned by `/researching-code` for deep investigation
- Spawned by `/structuring-code` to understand current architecture patterns
- Spawned by `/starting-refactors` to understand current architecture before refactoring
- Spawned by `/researching-repo` for architecture, conventions, and deep-dive analysis (multiple instances)

## Key Constraints

The agent is explicitly instructed to NOT:
- Suggest improvements or changes
- Perform root cause analysis
- Critique implementation or identify problems
- Comment on code quality, performance, or security
- Recommend best practices or alternative implementations

## File Reference

- Agent: `plugins/commandbase-code/agents/code-analyzer.md`
- Plugin: `commandbase-code`
