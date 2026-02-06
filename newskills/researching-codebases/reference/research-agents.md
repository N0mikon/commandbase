# Research Agents

Guide to using specialized sub-agents for codebase research.

## Available Agents

### Codebase Agents

| Agent | Purpose | Use When |
|-------|---------|----------|
| **code-locator** | Find WHERE files and components live | Need to discover file locations, directory structures |
| **code-analyzer** | Understand HOW specific code works | Need deep analysis of specific files or functions |
| **code-librarian** | Find examples of existing patterns | Need to see how similar things are implemented |

### Documentation Agents

| Agent | Purpose | Use When |
|-------|---------|----------|
| **docs-locator** | Discover what documentation exists | Starting research, need to find prior work |
| **docs-analyzer** | Extract key insights from existing docs | Have docs, need to understand their content |

## Agent Instructions

When spawning agents, instructions should:

- Be specific about what to search for
- Specify which directories to focus on
- Request file:line references in responses
- Ask for documentation, not evaluation

## Example Agent Prompts

**code-locator**:
```
Find all files related to authentication in this codebase.
Focus on src/ and lib/ directories.
Return file paths with brief descriptions of each file's role.
```

**code-analyzer**:
```
Analyze the error handling in src/middleware/errorHandler.ts.
Document the error classes, how they're caught, and what responses they produce.
Include file:line references for each finding.
```

**code-librarian**:
```
Find examples of how API endpoints are defined in this codebase.
Look for patterns in route definitions, middleware usage, and response formatting.
Return 3-5 concrete examples with file:line references.
```

**docs-locator**:
```
Search .docs/ directory for any existing research or documentation about the authentication system.
Return paths to relevant documents.
```

## Parallel vs Sequential

**Spawn in parallel** when:
- Researching independent aspects of a question
- Each agent can work without the other's results
- Maximizing coverage quickly

**Spawn sequentially** when:
- Later agents need results from earlier ones
- Following a chain of dependencies
- Drilling deeper based on initial findings
