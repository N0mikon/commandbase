# Research: docs-locator Agent

## Overview

The `docs-locator` agent (`~/.claude/agents/docs-locator.md`) finds relevant documents across the `.docs/` directory (plans, research, handoffs). It's the discovery tool for documentation.

**When to Use**: When you need to discover what documentation exists about a topic before creating new docs or when looking for historical context.

## Capabilities

- Search content with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Grep, Glob, LS

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "docs-locator"
prompt: "Find documents related to [topic] in .docs/"
```

## Use Cases

1. **Doc Discovery**: Find what documentation already exists
2. **History Search**: Locate historical context
3. **Duplication Prevention**: Check before creating new docs
4. **Reference Finding**: Find related research or plans

## Output Format

Returns list of relevant documents:
```markdown
## Located Docs: [Topic]

### Plans
- `.docs/plans/01-27-2026-feature.md` - [Brief description]

### Research
- `.docs/research/01-27-2026-patterns.md` - [Brief description]

### Handoffs
- `.docs/handoffs/01-27-2026-session.md` - [Brief description]

### Relevance Notes
- Most relevant: [file] - [why]
- Related but older: [file] - [why]
```

## Integration Points

- Used by `/planning-codebases` to find existing research
- Supports `/taking-over` for context gathering
- Helps `/researching-codebases` avoid duplication

## File Reference

- Agent: `~/.claude/agents/docs-locator.md`
