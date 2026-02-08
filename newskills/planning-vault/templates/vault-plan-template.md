# Vault Implementation Plan Template

Use this template when writing vault plans to `.docs/plans/MM-DD-YYYY-description.md`.

Frontmatter is handled by the `docs-writer` agent. Provide these body sections as the `content` field:

```markdown
# [Vault Task Name] Implementation Plan

## Overview

[Brief description of what vault changes we're implementing and why]

## Current State Analysis

**What exists:**
- [Current folder structure relevant to changes]
- [Current note counts in affected areas]
- [Current conventions in use]

**What's missing:**
- [What needs to be created or reorganized]

### Key Discoveries:
- [Important finding with note/folder reference]
- [Pattern to follow]
- [Constraint to work within]

## Desired End State

[Description of what the vault should look like after all phases complete]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach

[High-level strategy and reasoning]

---

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Operation Type: Create/Move/Update]
**Notes affected**: [list of notes or patterns]
**Changes**: [Summary of changes]

### Success Criteria:
- [ ] Note exists at expected path (verify via Read or MCP read)
- [ ] Frontmatter contains required properties (verify via Grep)
- [ ] Wikilinks resolve correctly (verify via Grep for old references = 0)
- [ ] No orphan notes created (verify incoming links exist)

---

## Phase 2: [Descriptive Name]

[Similar structure with vault-specific success criteria...]

---

## Verification Strategy

### Per-Phase Verification:
- Note existence: Read/MCP read on expected paths
- Wikilink integrity: Grep for broken references
- Frontmatter completeness: Grep for required properties
- Folder structure: Glob to verify note placement

### Final Verification:
- All notes in expected locations
- All wikilinks resolve
- All frontmatter complete
- No orphan notes

## Performance Considerations

[For large vaults: batch operations, progress indicators, scope limiting]

## Migration Notes

[How to handle existing notes, wikilink updates, backup recommendations]

## References

- [Link to vault design document]
- [Link to vault structural map]
- [Link to vault research]
```

## Template Usage Notes

- **File creation**: Delegate to `docs-writer` agent with `doc_type: "plan"`
- **Naming and location**: Handled by the `docs-writer` agent
- **Frontmatter**: Handled by the `docs-writer` agent (date, status, topic, tags, git_commit, references)
- **Status**: docs-writer defaults to `draft`; update to `approved` after user review via Edit
- **Success criteria**: Use vault verification commands (see `reference/vault-verification-commands.md`)
