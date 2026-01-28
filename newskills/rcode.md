---
description: Research and document codebase to understand implementation details
model: opus
---

# Research Codebase

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

## Your Role

Document and explain the codebase as it exists today:
- Describe what exists, where it exists, how it works, and how components interact
- Create a technical map/documentation of the existing system
- Do NOT suggest improvements or changes unless explicitly asked
- Do NOT critique the implementation or identify problems
- Only describe the current state

## Initial Response

When this command is invoked:

1. **If a specific question or area was provided**, begin research immediately
2. **If no parameters provided**, respond with:
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.

Examples:
- "How does authentication work?"
- "Where are API endpoints defined?"
- "Explain the database schema"
- "How do components X and Y interact?"
```

Then wait for the user's query.

## Research Process

### Step 1: Read Mentioned Files First

If the user mentions specific files:
- Read them FULLY using the Read tool WITHOUT limit/offset parameters
- Read these files yourself in the main context before spawning any sub-tasks
- This ensures you have full context before decomposing the research

### Step 2: Decompose the Research Question

- Break down the query into composable research areas
- Identify specific components, patterns, or concepts to investigate
- Create a research plan using TodoWrite to track subtasks
- Consider which directories, files, or architectural patterns are relevant

### Step 3: Spawn Parallel Research Agents

Create multiple Task agents to research different aspects concurrently:

**Use these specialized agents:**
- **codebase-locator** - Find WHERE files and components live
- **codebase-analyzer** - Understand HOW specific code works
- **codebase-pattern-finder** - Find examples of existing patterns

**For historical context in `.docs/`:**
- **docs-locator** - Discover what documentation already exists about the topic
- **docs-analyzer** - Extract key insights from existing research/plans

**Agent instructions should:**
- Be specific about what to search for
- Specify which directories to focus on
- Request file:line references in responses
- Ask for documentation, not evaluation

### Step 4: Synthesize Findings

After ALL sub-agents complete:
- Compile results from all agents
- Connect findings across different components
- Include specific file paths and line numbers
- Document patterns, connections, and data flows

### Step 5: Write Research Document

Write findings to `.docs/research/MM-DD-YYYY-description.md`
- Create `.docs/research/` directory if it doesn't exist

**Format:**
- MM-DD-YYYY is today's date
- description is a brief kebab-case description of the topic

**Examples:**
- `01-27-2026-authentication-flow.md`
- `01-27-2026-api-endpoint-structure.md`

**Document Template:**

```markdown
---
git_commit: [current HEAD commit hash]
last_updated: [YYYY-MM-DD]
last_updated_by: [user or agent name]
topic: "[Research Topic]"
tags: [research, relevant-component-names]
status: complete
references:
  - [list of key files this research covers]
---

# Research: [Topic]

**Date**: [Current date]
**Branch**: [Current git branch]

## Research Question

[Original user query]

## Summary

[High-level documentation answering the user's question]

## Detailed Findings

### [Component/Area 1]
- Description of what exists ([file.ext:line](path))
- How it connects to other components
- Current implementation details

### [Component/Area 2]
...

## Code References

- `path/to/file.py:123` - Description of what's there
- `another/file.ts:45-67` - Description of the code block

## Architecture Notes

[Patterns, conventions, and design implementations found]

## Open Questions

[Any areas that need further investigation]
```

### Step 6: Present Findings

- Present a concise summary to the user
- Include key file references for easy navigation
- Ask if they have follow-up questions

## Important Guidelines

1. **Document, Don't Evaluate**
   - Describe what IS, not what SHOULD BE
   - No recommendations unless asked
   - No critiques or "improvements"

2. **Be Thorough**
   - Use parallel agents to maximize coverage
   - Always include file:line references
   - Connect related components

3. **Be Accurate**
   - Verify findings against actual code
   - Don't guess - investigate
   - Note uncertainties clearly

4. **Stay Focused**
   - Answer the specific question asked
   - Don't go on tangents
   - Keep the research scoped

## Example Interaction

```
User: /rcode how does the API handle errors?
Assistant: I'll research how the API handles errors...

[Spawns parallel research agents]

Based on my research, here's how error handling works:

**Summary:**
The API uses a centralized error handler in `src/middleware/errorHandler.ts:15-45`...

**Key findings:**
- Custom error classes defined in `src/errors/index.ts`
- HTTP status codes mapped in `src/errors/httpCodes.ts:8-25`
- Validation errors handled separately in `src/middleware/validate.ts`

I've documented the full details in `.docs/research/01-27-2026-api-error-handling.md`

Would you like me to dig deeper into any specific aspect?
```