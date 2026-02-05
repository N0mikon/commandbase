# Research: researching-codebases Skill

> **Updated 2026-02-05**: Gate Function expanded to 7 steps with mandatory research file creation. Added Red Flags and Rationalization Prevention sections that were added to the global version.

## Overview

The `researching-codebases` skill (`~/.claude/skills/researching-codebases/SKILL.md`) researches a codebase to understand how it works. It spawns specialized agents for parallel investigation and produces documentation of findings. Research MUST be written to a `.docs/research/` file before presenting to the user.

**Trigger phrases**: `research codebase`, `how does this work`, `where is this defined`, `explain the code`, `explain the architecture`

## Purpose

Understand existing implementations:
- Answer questions like "how does X work"
- Document existing implementations
- Trace data flows
- Create technical documentation

## The Gate Function (7 Steps)

```
BEFORE completing research:

1. IDENTIFY: What specific questions need answering?
2. PLAN: Which agents to spawn and what to search for?
3. RESEARCH: Spawn parallel agents
4. COLLECT: Wait for all results
5. SYNTHESIZE: Combine into coherent understanding
6. WRITE: Save research file to .docs/research/ (MANDATORY)
7. PRESENT: Show findings to user

Research without a file = research that will be lost
```

## Process

### Step 1: Identify Research Questions
Parse user query to understand what needs to be researched:
- Specific component understanding
- Architecture overview
- Pattern identification
- Data flow tracing

### Step 2: Spawn Research Agents
Launch specialized agents in parallel:
- **codebase-locator**: Find relevant files
- **codebase-analyzer**: Understand implementation details
- **codebase-pattern-finder**: Find similar patterns
- **docs-locator**: Find existing documentation

### Step 3: Collect Results
Wait for all agents to complete, aggregate findings with file:line references.

### Step 4: Synthesize Understanding
Combine agent outputs into coherent understanding:
- Key components identified
- Data flows traced
- Patterns documented
- Dependencies mapped

### Step 5: Write Research File (MANDATORY)
Save findings to `.docs/research/MM-DD-YYYY-topic.md` before presenting.

### Step 6: Present Findings
Output comprehensive documentation with:
- File:line references
- Code snippets
- Architecture diagrams (textual)
- Integration points

## Output Format

```markdown
# Research: [Topic]

## Overview
[High-level understanding]

## Key Components
- [Component 1]: [file:line] - [purpose]
- [Component 2]: [file:line] - [purpose]

## Data Flow
1. [Step 1 with file:line]
2. [Step 2 with file:line]

## Patterns Identified
- [Pattern 1]: Used in [files]
- [Pattern 2]: Used in [files]

## Integration Points
- [Integration 1]: [how it connects]
```

## Integration Points

- Produces context for `/planning-codebases`
- Informs `/discussing-features` decisions
- Supports `/debugging-codebases` investigation

## Red Flags - STOP and Verify

- About to present findings without writing to a research file
- Synthesizing from memory without spawning agents
- Skipping agents because "I already know this codebase"
- Presenting partial results without waiting for all agents
- Not including file:line references in findings

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Verify with agents. Memory drifts. |
| "The user just wants a quick answer" | Quick answers without evidence are guesses. |
| "I'll write the research file later" | Later never comes after context resets. Write it now. |
| "The findings are too small for a file" | Small findings are still worth preserving. |
| "I can present first and save after" | Write the file. THEN present findings. |

## File Reference

- Main: `~/.claude/skills/researching-codebases/SKILL.md`
