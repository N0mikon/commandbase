# Research: researching-codebases Skill

## Overview

The `researching-codebases` skill (`~/.claude/skills/researching-codebases/SKILL.md`) researches a codebase to understand how it works. It spawns specialized agents for parallel investigation and produces documentation of findings.

**Trigger phrases**: `research codebase`, `how does this work`, `where is this defined`, `explain the code`, `explain the architecture`

## Purpose

Understand existing implementations:
- Answer questions like "how does X work"
- Document existing implementations
- Trace data flows
- Create technical documentation

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

### Step 5: Present Findings
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

## File Reference

- Main: `~/.claude/skills/researching-codebases/SKILL.md`
