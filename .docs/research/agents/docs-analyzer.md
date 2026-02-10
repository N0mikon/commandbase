---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, corrected agent file path from legacy ~/.claude/agents/ to plugin location, updated integration points to reflect actual usage, expanded output format to match real agent definition"
references:
  - plugins/commandbase-core/agents/docs-analyzer.md
  - plugins/commandbase-core/.claude-plugin/plugin.json
  - plugins/commandbase-research/skills/analyzing-research/SKILL.md
  - plugins/commandbase-code/skills/planning-code/reference/research-workflow.md
  - plugins/commandbase-code/skills/researching-code/reference/research-agents.md
---

# Research: docs-analyzer Agent

## Overview

The `docs-analyzer` agent (`plugins/commandbase-core/agents/docs-analyzer.md`) extracts high-value insights from `.docs/` documents. It understands decisions, constraints, and learnings without reading every document. It runs on the `sonnet` model.

**When to Use**: When you need to understand what decisions were made, what constraints exist, or what learnings were captured.

## Capabilities

- Read files with Read tool
- Search code with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Read, Grep, Glob, LS

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "docs-analyzer"
prompt: "Extract key decisions from [document path]"
```

## Use Cases

1. **Decision Extraction**: Find what decisions were made and why
2. **Constraint Identification**: Discover constraints and limitations
3. **Learning Extraction**: Pull out key learnings from sessions
4. **Context Gathering**: Understand historical context
5. **Staleness Detection**: Checks frontmatter `git_commit` and `last_updated` to assess document freshness

## Output Format

Returns extracted insights with document freshness context:
```markdown
## Analysis of: [Document Path]

### Document Context
- **Date**: [When written]
- **git_commit**: [Commit when last updated]
- **Commits Behind**: [How many commits since last update]
- **Status**: [Is this still relevant/implemented/superseded?]

### Key Decisions
1. **[Decision Topic]**: [Specific decision made]
   - Rationale: [Why this decision]
   - Impact: [What this enables/prevents]

### Critical Constraints
- **[Constraint Type]**: [Specific limitation and why]

### Technical Specifications
- [Specific config/value/approach decided]

### Key Learnings
- [Gotcha or edge case discovered]
- [Pattern that worked well]

### File References
- `src/path/file.ts:45` - [What's relevant there]

### Actionable Insights
- [Something that should guide current implementation]

### Still Open/Unclear
- [Questions that weren't resolved]

### Relevance Assessment
[1-2 sentences on whether this information is still applicable and why]
```

## Integration Points

- **Primary consumer**: Extraction phase of `/analyzing-research` (spawns parallel docs-analyzer agents, batching 3-5 docs per agent)
- Research workflow reference for `/planning-code` (via `reference/research-workflow.md`)
- Agent catalog reference for `/researching-code` (via `reference/research-agents.md`)

## File Reference

- Agent definition: `plugins/commandbase-core/agents/docs-analyzer.md`
- Plugin manifest: `plugins/commandbase-core/.claude-plugin/plugin.json`
