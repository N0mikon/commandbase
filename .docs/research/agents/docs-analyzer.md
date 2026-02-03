# Research: docs-analyzer Agent

## Overview

The `docs-analyzer` agent (`~/.claude/agents/docs-analyzer.md`) extracts high-value insights from `.docs/` documents. It understands decisions, constraints, and learnings without reading every document.

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

## Output Format

Returns extracted insights:
```markdown
## Analysis: [Document]

### Key Decisions
1. [Decision 1] - [Rationale]
2. [Decision 2] - [Rationale]

### Constraints Identified
- [Constraint 1]
- [Constraint 2]

### Learnings
1. [Learning with file:line reference]

### Open Questions
- [Question still unanswered]
```

## Integration Points

- Deep research phase of `/planning-codebases`
- Context gathering for `/taking-over`
- Learning extraction for `/learning-from-sessions`

## File Reference

- Agent: `~/.claude/agents/docs-analyzer.md`
