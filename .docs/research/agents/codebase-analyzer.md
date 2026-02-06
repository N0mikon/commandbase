# Research: code-analyzer Agent

## Overview

The `code-analyzer` agent (`~/.claude/agents/code-analyzer.md`) analyzes codebase implementation details. It's a read-only agent that provides detailed information about specific components.

**When to Use**: When you need to find detailed information about specific components.

## Capabilities

- Read files with Read tool
- Search code with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Read, Grep, Glob, LS

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "code-analyzer"
prompt: "Analyze how [component] works in [directory]"
```

## Use Cases

1. **Component Analysis**: Understand how a specific module works
2. **Data Flow Tracing**: Track data through the system
3. **Dependency Mapping**: Find what depends on what
4. **Pattern Identification**: Discover recurring patterns

## Output Format

Returns analysis with file:line references:
```markdown
## Analysis: [Component]

### Overview
[How it works]

### Key Files
- [file:line] - [purpose]

### Data Flow
1. [Step with file:line]
2. [Step with file:line]

### Dependencies
- Depends on: [components]
- Used by: [components]
```

## Integration Points

- Spawned by `/planning-code` for research
- Spawned by `/researching-code` for investigation
- Spawned by `/debugging-code` for understanding

## File Reference

- Agent: `~/.claude/agents/code-analyzer.md`
