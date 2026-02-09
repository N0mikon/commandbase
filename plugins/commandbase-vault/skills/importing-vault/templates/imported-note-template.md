# Imported Note Template

Template for converting `.docs/` artifacts into Obsidian vault notes.

## Template

```markdown
---
[vault-required-property-1]: [value]
[vault-required-property-2]: [value]
tags: [mapped-tag-1, mapped-tag-2]
source: [original .docs/ path]
created: [original date or import date]
---

# [Note Title]

> [!info] Imported from `[source path]` on [import date]

[Converted main content — all markdown elements preserved,
references converted to wikilinks where targets exist,
callouts converted to Obsidian format]

## Related Notes

- [[existing-vault-note-1]] — [relationship description]
- [[existing-vault-note-2]] — [relationship description]
- Source: `[.docs/path/not-yet-imported.md]` (not yet in vault)
```

## Usage Notes

- **Frontmatter**: Replace bracketed properties with vault-specific fields from CLAUDE.md
- **Source attribution**: The `> [!info]` callout tracks where the note came from
- **Related Notes**: Only use `[[wikilinks]]` for notes confirmed to exist in the vault
- **Content**: Preserve the source's structure but convert elements per conversion-rules.md
- **Title**: Use the vault's naming convention (kebab-case filename, title property, etc.)

## Minimal Example

```markdown
---
title: Authentication API Research
created: 2026-02-07
status: seedling
tags: [research, authentication]
source: .docs/research/02-07-2026-auth-research.md
---

# Authentication API Research

> [!info] Imported from `.docs/research/02-07-2026-auth-research.md` on 2026-02-07

## Overview

Research into authentication patterns for the user service.

## Findings

### OAuth 2.0 vs JWT

> [!important] JWT was selected for its stateless nature and simpler infrastructure requirements.

OAuth 2.0 provides better token revocation but requires a token store.
JWT tokens are self-contained and validate without database lookups.

### Session Management

Sessions use short-lived JWTs (15 min) with refresh tokens stored server-side.

## Related Notes

- [[api-design]] — API design decisions that depend on auth approach
- Source: `.docs/plans/02-07-2026-auth-plan.md` (not yet in vault)
```
