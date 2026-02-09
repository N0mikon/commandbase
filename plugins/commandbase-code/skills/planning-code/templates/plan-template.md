# Implementation Plan Template

Use this template when writing plans to `.docs/plans/MM-DD-YYYY-description.md`.

Frontmatter is handled by the `docs-writer` agent. Provide these body sections as the `content` field:

```markdown
# [Feature/Task Name] Implementation Plan

## Overview

[Brief description of what we're implementing and why]

## Current State Analysis

[What exists now, what's missing, key constraints discovered]

## Desired End State

[A Specification of the desired end state after this plan is complete, and how to verify it]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach

[High-level strategy and reasoning]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

```[language]
// Specific code to add/modify
```

### Success Criteria:
- [ ] Unit tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Integration tests pass

---

## Phase 2: [Descriptive Name]

[Similar structure with success criteria...]

---

## Testing Strategy

### Unit Tests:
- [What to test]
- [Key edge cases]

### Integration Tests:
- [End-to-end scenarios]

## Performance Considerations

[Any performance implications or optimizations needed]

## Migration Notes

[If applicable, how to handle existing data/systems]

## References

- [Link to requirements or related documents]
- Similar implementation: `[file:line]`
```

## Template Usage Notes

- **File creation**: Delegate to `docs-writer` agent with `doc_type: "plan"`
- **Naming and location**: Handled by the `docs-writer` agent
- **Frontmatter**: Handled by the `docs-writer` agent (date, status, topic, tags, git_commit, references)
- **Status**: docs-writer defaults to `draft`; update to `approved` after user review via Edit
