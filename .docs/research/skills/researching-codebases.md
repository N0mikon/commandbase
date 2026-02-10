---
date: 2026-02-05
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after plugin restructure - fixed file paths, aligned Gate Function and process steps with current SKILL.md, added Iron Law, reference files, and docs-writer integration"
status: current
topic: researching-code skill analysis
tags:
  - skill
  - research
  - codebase-analysis
  - commandbase-code
git_commit: 8e92bba
references:
  - plugins/commandbase-code/skills/researching-code/SKILL.md
  - plugins/commandbase-code/skills/researching-code/reference/research-agents.md
  - plugins/commandbase-code/skills/researching-code/reference/evidence-requirements.md
  - plugins/commandbase-code/skills/researching-code/templates/research-document-template.md
---

# Research: researching-code Skill

> **Updated 2026-02-09**: Aligned with current skill after plugin marketplace restructure. Updated file paths from `~/.claude/skills/` to `plugins/commandbase-code/skills/`. Aligned Gate Function steps, added Iron Law section, updated process steps to match current 6-step flow, added reference file documentation.

## Overview

The `researching-code` skill (`plugins/commandbase-code/skills/researching-code/SKILL.md`) researches a codebase to understand how it works. It spawns specialized agents for parallel investigation and produces documentation of findings. Research MUST be written to a `.docs/research/` file before presenting to the user.

The skill enforces a strict "Document, Don't Evaluate" philosophy: describe what IS, not what SHOULD BE. No recommendations or critiques unless explicitly asked.

**Trigger phrases**: `research codebase`, `how does this work`, `where is this defined`, `explain the code`, `explain the architecture`

## Purpose

Understand existing implementations:
- Answer questions like "how does X work"
- Document existing implementations
- Trace data flows
- Create technical documentation

## The Iron Law

```
NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST
```

If research agents have not been spawned and their results collected, synthesis cannot proceed. This applies regardless of question complexity -- "simple" questions have complex answers, and answering from memory leads to drift.

## The Gate Function (7 Steps)

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

## Process

### Step 1: Read Mentioned Files First
If the user mentions specific files, read them FULLY using the Read tool (without limit/offset parameters) in the main context before spawning any sub-tasks. This ensures full context before decomposing the research.

### Step 2: Decompose the Research Question
- Break down the query into composable research areas
- Identify specific components, patterns, or concepts to investigate
- Create a research plan using TodoWrite to track subtasks
- Consider which directories, files, or architectural patterns are relevant

### Step 3: Spawn Parallel Research Agents
Create multiple Task agents to research different aspects concurrently. Agent configuration details are documented in `plugins/commandbase-code/skills/researching-code/reference/research-agents.md`.

### Step 4: Synthesize Findings
After ALL sub-agents complete:
- Compile results from all agents
- Connect findings across different components
- Include specific file paths and line numbers
- Document patterns, connections, and data flows

### Step 5: Write Research Document (MANDATORY)
Spawn a `docs-writer` agent via the Task tool to create the research file:

```
Task prompt:
  doc_type: "research"
  topic: "<research topic from user query>"
  tags: [<relevant component/area tags>]
  references: [<key files discovered during research>]
  content: |
    <compiled findings using the output format below>
```

The agent handles frontmatter, file naming, and directory creation.

### Step 6: Present Findings
- Present a concise summary to the user
- Include key file references for easy navigation
- Ask if they have follow-up questions

## Output Format

The research document body should follow this structure (see `plugins/commandbase-code/skills/researching-code/templates/research-document-template.md` for full section guidelines):

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

## Integration Points

- Produces context for `/planning-code`
- Informs `/discussing-features` decisions
- Supports `/debugging-code` investigation

## Red Flags - STOP and Verify

- Presenting findings without creating a research file first
- Saying "I'll document this later" or "if you want I can save this"
- Completing research without a `.docs/research/` file path in the response
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

## Evidence Requirements

See `plugins/commandbase-code/skills/researching-code/reference/evidence-requirements.md` for:
- What counts as valid evidence
- Red flags that indicate guessing
- Rationalization prevention
- Verification checklist

## Skill Directory Structure

```
plugins/commandbase-code/skills/researching-code/
  SKILL.md                                    # Main skill definition
  reference/research-agents.md                # Agent spawning guide
  reference/evidence-requirements.md          # Evidence standards
  templates/research-document-template.md     # Output template
```

## File Reference

- Plugin: `plugins/commandbase-code/`
- Skill: `plugins/commandbase-code/skills/researching-code/SKILL.md`
