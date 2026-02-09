# Vault Research Document Template

Use this template when writing vault research findings to `.docs/research/`.

## File Naming

**Format:** `MM-DD-YYYY-description.md`

- MM-DD-YYYY is today's date
- description is a brief kebab-case description of the topic

**Examples:**
- `02-07-2026-vault-folder-structure.md`
- `02-07-2026-vault-tag-taxonomy.md`
- `02-07-2026-vault-orphan-analysis.md`

## Body Sections Template

Frontmatter is handled by the `docs-writer` agent. Provide these body sections as the `content` field:

```markdown
# [Vault Research Topic]

**Date**: [Current date]
**Vault**: [Vault name/path]

## Research Question

[Original user query]

## Summary

[High-level documentation answering the user's question about the vault]

## Detailed Findings

### Folder Structure
- [Folder tree with note counts]

### Tag Usage
- [Tag taxonomy with frequency data]

### Link Patterns
- [Link density, hub notes, connection patterns]

### Frontmatter Conventions
- [Property names, types, consistency analysis]

### MOC Structure
- [MOC inventory, coverage, linking patterns]

### Orphan Notes
- [Notes with no incoming links]

[Include only dimensions relevant to the research question]

## Vault References

- `path/to/note.md` - Description of its role
- `folder/` - Description of folder purpose

## Organization Notes

[Patterns, conventions, and organizational decisions observed]

## Open Questions

[Any areas that need further investigation]
```

## Section Guidelines

### Summary
- 2-4 sentences answering the research question directly
- No jargon; someone unfamiliar with the vault should understand
- Include the most important paths/locations

### Detailed Findings
- One subsection per vault dimension investigated
- Each finding needs a note path or folder reference
- Explain connections between vault areas

### Vault References
- Deduplicated list of all notes/folders mentioned
- Brief description of each item's role
- Sorted by importance or logical grouping

### Organization Notes
- Patterns observed (naming conventions, folder structure)
- Organizational decisions evident from the vault
- Non-obvious relationships between vault areas

### Open Questions
- Areas that need deeper investigation
- Ambiguities found during research
- Suggestions for follow-up exploration

## Frontmatter

Handled by `docs-writer`. Provide these fields in the Task prompt:

```yaml
doc_type: "research"
topic: "<vault research topic>"
tags: [vault, <relevant aspect tags>]
```
