---
name: researching-code
description: "Use this skill when researching a codebase to understand how it works. This includes answering questions like 'how does X work', 'where is Y defined', 'explain the architecture', documenting existing implementations, tracing data flows, and creating technical documentation. Activate when the user says 'research codebase', 'how does this work', 'where is this defined', or 'explain the code'."
---

# Researching Codebases

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Document and explain the codebase as it exists today:
- Describe what exists, where it exists, how it works, and how components interact
- Create a technical map/documentation of the existing system
- Do NOT suggest improvements or changes unless explicitly asked
- Do NOT critique the implementation or identify problems
- Only describe the current state

## The Iron Law

```
NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST
```

If you haven't spawned research agents and waited for their results, you cannot synthesize findings.

**No exceptions:**
- Don't answer from memory - spawn agents to verify
- Don't skip agents for "simple" questions - simple questions have complex answers
- Don't synthesize partial results - wait for ALL agents to complete
- Don't guess at file locations - let agents find them

## The Gate Function

```
BEFORE completing research:

1. IDENTIFY: What aspects of the question need investigation?
2. SPAWN: Create parallel agents for each aspect (minimum 2 agents)
3. WAIT: All agents must complete before proceeding
4. VERIFY: Did agents return file:line references?
   - If NO: Spawn follow-up agents to get specific references
   - If YES: Proceed to synthesis
5. SYNTHESIZE: Compile findings with evidence
6. WRITE: Create .docs/research/MM-DD-YYYY-description.md (MANDATORY)
7. PRESENT: Summary to user with link to research file

Skipping steps = incomplete research
Research without a file = research that will be lost
```

## Initial Response

When this skill is invoked:

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

Create multiple Task agents to research different aspects concurrently.

See ./reference/research-agents.md for the full guide on available agents and how to use them effectively.

### Step 4: Synthesize Findings

After ALL sub-agents complete:
- Compile results from all agents
- Connect findings across different components
- Include specific file paths and line numbers
- Document patterns, connections, and data flows

### Step 5: Write Research Document

Spawn a `docs-writer` agent via the Task tool to create the research file:

```
Task prompt:
  doc_type: "research"
  topic: "<research topic from user query>"
  tags: [<relevant component/area tags>]
  references: [<key files discovered during research>]
  content: |
    <compiled findings using the body sections below>
```

The agent handles frontmatter, file naming, and directory creation.

**Body sections to include in `content`** (see ./templates/research-document-template.md for section guidelines):

```markdown
# [Topic]

**Date**: [Current date]
**Branch**: [Current git branch]

## Research Question
[Original user query]

## Summary
[High-level documentation answering the user's question]

## Detailed Findings
### [Component/Area 1]
- Description of what exists ([file.ext:line](path))

## Code References
- `path/to/file.py:123` - Description

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
   - Verify findings against actual code via agents
   - Don't guess - spawn agents to investigate
   - Every claim needs a file:line reference
   - Note uncertainties clearly and spawn follow-up agents

4. **Stay Focused**
   - Answer the specific question asked
   - Don't go on tangents
   - Keep the research scoped

## Evidence Requirements

See ./reference/evidence-requirements.md for:
- What counts as valid evidence
- Red flags that indicate guessing
- Rationalization prevention
- Verification checklist

## Example Interaction

```
User: /researching-code how does the API handle errors?
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

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting findings without creating a research file first
- Saying "I'll document this later" or "if you want I can save this"
- Completing research without a `.docs/research/` file path in your response
- Skipping the research file because "it was a simple question"
- Synthesizing without spawning parallel agents first

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It was a quick answer, no file needed" | Every research produces a file. No exceptions. |
| "I'll create the file if they ask" | Create it first. They shouldn't have to ask. |
| "The question was about non-code topics" | Still create a research file documenting findings. |
| "I already presented the findings" | File comes BEFORE presentation, not after. |
| "There wasn't much to document" | Short findings = short file. Still required. |

## The Bottom Line

**No shortcuts for research.**

Spawn the agents. Wait for results. Cite file:line references. Write the research file. THEN present findings.

This is non-negotiable. Every question. Every time.
