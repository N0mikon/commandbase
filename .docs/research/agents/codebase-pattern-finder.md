# Research: code-librarian Agent

## Overview

The `code-librarian` agent (`~/.claude/agents/code-librarian.md`) finds similar implementations, usage examples, or existing patterns that can be modeled after. It provides concrete code examples.

**When to Use**: When looking for patterns to follow or examples to model after.

## Capabilities

- Search code with Grep tool
- Find files with Glob tool
- Read files with Read tool
- List directories with LS tool

**Tools Available**: Grep, Glob, Read, LS

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "code-librarian"
prompt: "Find examples of [pattern] in the codebase"
```

## Use Cases

1. **Pattern Discovery**: Find how something is done elsewhere
2. **Example Finding**: Locate code to model after
3. **Convention Identification**: Discover coding conventions
4. **Consistency Checking**: See how similar things are implemented

## Output Format

Returns patterns with code examples:
```markdown
## Patterns Found: [Topic]

### Pattern 1: [Name]
**Location**: `path/to/file.ts:42-56`
**Usage**: [When this pattern is used]

```typescript
// Code example
```

### Pattern 2: [Name]
**Location**: `path/to/other.ts:15-30`
**Usage**: [When this pattern is used]

```typescript
// Code example
```

### Recommendation
Based on existing patterns, you should [recommendation].
```

## Integration Points

- Deep research phase of `/planning-code`
- Pattern identification for `/researching-code`
- Convention discovery for `/creating-skills`

## File Reference

- Agent: `~/.claude/agents/code-librarian.md`
