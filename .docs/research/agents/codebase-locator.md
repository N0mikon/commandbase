# Research: codebase-locator Agent

## Overview

The `codebase-locator` agent (`~/.claude/agents/codebase-locator.md`) locates files, directories, and components relevant to a feature or task. It's a "Super Grep/Glob/LS tool" for finding things.

**When to Use**: When searching for a keyword or file and not confident you'll find the right match in the first few tries.

## Capabilities

- Search code with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Grep, Glob, LS

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "codebase-locator"
prompt: "Find all files related to [feature/component]"
```

## Use Cases

1. **File Discovery**: Find files matching a pattern
2. **Component Location**: Locate where a component is defined
3. **Feature Mapping**: Find all files related to a feature
4. **Structure Understanding**: Map directory structure

## Output Format

Returns list of relevant files:
```markdown
## Located Files: [Topic]

### Primary Files
- `path/to/main.ts` - Main implementation
- `path/to/types.ts` - Type definitions

### Related Files
- `path/to/tests/` - Test files
- `path/to/utils.ts` - Utility functions

### Directory Structure
```
component/
├── index.ts
├── types.ts
└── tests/
```
```

## Integration Points

- First step in `/planning-codebases` research
- Used by `/researching-codebases` for exploration
- Supports `/debugging-codebases` investigation

## File Reference

- Agent: `~/.claude/agents/codebase-locator.md`
