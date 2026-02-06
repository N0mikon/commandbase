# Research Document Template

Use this template when writing research findings to `.docs/research/`.

## File Naming

**Format:** `MM-DD-YYYY-description.md`

- MM-DD-YYYY is today's date
- description is a brief kebab-case description of the topic

**Examples:**
- `01-27-2026-authentication-flow.md`
- `01-27-2026-api-endpoint-structure.md`
- `01-28-2026-database-schema.md`

## Template

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

## Section Guidelines

### Summary
- 2-4 sentences answering the research question directly
- No jargon; someone unfamiliar with the codebase should understand
- Include the most important file locations

### Detailed Findings
- One subsection per major component or area
- Each finding needs a file:line reference
- Explain connections between components

### Code References
- Deduplicated list of all files mentioned
- Brief description of each file's role
- Sorted by importance or logical grouping

### Architecture Notes
- Patterns observed (naming conventions, directory structure)
- Design decisions evident from the code
- Non-obvious relationships

### Open Questions
- Areas that need deeper investigation
- Ambiguities found during research
- Suggestions for follow-up research
