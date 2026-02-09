# Conversion Rules Reference

Detailed conversion rules for transforming `.docs/` artifacts into Obsidian vault notes.

## Frontmatter Translation

### Standard `.docs/` Properties

| `.docs/` Property | Vault Translation | Notes |
|-------------------|-------------------|-------|
| `date` | `created` or `date` | Match vault's date property name |
| `status` | `status` | Translate values to vault's taxonomy (e.g., "draft" → "seedling") |
| `topic` | `title` or note filename | Some vaults use `title` property, others use filename |
| `tags` | `tags` | Map to vault's tag taxonomy (see Tag Mapping below) |
| `git_commit` | Remove or keep as `source_commit` | Code-specific, usually not relevant in vault |
| `references` | Convert to Related Notes section | See References Conversion below |
| `doc_type` | `type` or `note-type` | Match vault's type property name |

### Translation Process

1. Read the vault's CLAUDE.md for required frontmatter properties
2. Map each `.docs/` property to its vault equivalent
3. Add any required vault properties not present in the source (e.g., `created`, `modified`)
4. Remove properties that have no vault equivalent and aren't useful as metadata
5. Ensure no nested YAML objects (Obsidian limitation)

### Example

**Source `.docs/` frontmatter:**
```yaml
---
date: 2026-02-07
status: draft
topic: "Authentication Research"
tags: [research, auth, api]
git_commit: abc1234
references:
  - .docs/plans/auth-plan.md
  - src/auth.ts
---
```

**Converted vault frontmatter (example vault conventions):**
```yaml
---
title: Authentication Research
created: 2026-02-07
status: seedling
tags: [research, authentication, api]
source: .docs/research/02-07-2026-auth-research.md
---
```

## References Conversion

### `.docs/` Path References

References to other `.docs/` files become wikilinks IF the target exists in the vault:

```markdown
<!-- Source -->
references:
  - .docs/research/02-07-2026-topic.md
  - .docs/plans/02-07-2026-plan.md

<!-- Converted (if vault notes exist) -->
## Related Notes
- [[topic-research]] — imported from .docs/research/
- [[topic-plan]] — imported from .docs/plans/

<!-- Converted (if vault notes DON'T exist) -->
## Related Notes
- Source: `.docs/research/02-07-2026-topic.md` (not yet imported)
- Source: `.docs/plans/02-07-2026-plan.md` (not yet imported)
```

### Code File References

References to source code files (`src/auth.ts:45`) stay as code references:

```markdown
<!-- Source -->
See `src/auth.ts:45` for the implementation.

<!-- Converted -->
See `src/auth.ts:45` for the implementation.
```

These are project-specific and don't have vault equivalents.

### Inline `.docs/` References

References within body text:

```markdown
<!-- Source -->
As documented in .docs/research/02-07-2026-auth.md, the API uses...

<!-- Converted (if vault note exists) -->
As documented in [[auth-research]], the API uses...

<!-- Converted (if vault note doesn't exist) -->
As documented in the auth research (`.docs/research/02-07-2026-auth.md`), the API uses...
```

## Callout Conversion

### Headers to Callouts

Common `.docs/` header patterns that should become Obsidian callouts:

```markdown
<!-- Source patterns -->
**Warning:** This approach has trade-offs...
**Note:** The API changed in v3...
**Important:** Always check permissions first...
**Tip:** Use batch mode for large operations...

<!-- Converted to Obsidian callouts -->
> [!warning] This approach has trade-offs...

> [!note] The API changed in v3...

> [!important] Always check permissions first...

> [!tip] Use batch mode for large operations...
```

### Block Quotes

Existing block quotes that aren't callouts should remain as block quotes:

```markdown
<!-- Source -->
> This is a regular quote, not a callout.

<!-- Converted (unchanged) -->
> This is a regular quote, not a callout.
```

## Tag Mapping

### Process

1. Read the vault's tag taxonomy from CLAUDE.md or by researching existing tags
2. Map each `.docs/` tag to the closest vault equivalent
3. If no equivalent exists, either:
   - Use the tag as-is (if vault allows free-form tags)
   - Suggest adding the tag to the taxonomy
   - Drop the tag and note the omission

### Common Mappings

| `.docs/` Tag | Possible Vault Equivalents |
|-------------|---------------------------|
| `research` | `type/research`, `research`, `note-type/research` |
| `plan` | `type/plan`, `plan`, `project/plan` |
| `handoff` | `type/handoff`, `handoff`, `session/handoff` |
| `learning` | `type/learning`, `learning`, `insight` |
| `brainstorm` | `type/brainstorm`, `brainstorm`, `exploration` |

The actual mapping depends entirely on the vault's conventions.

## Markdown Elements

### Elements That Transfer Directly

These markdown elements work identically in Obsidian and require no conversion:

- Headings (`#`, `##`, `###`, etc.)
- Bold (`**bold**`)
- Italic (`*italic*`)
- Code fences (triple backtick)
- Inline code (single backtick)
- Tables (pipe-delimited)
- Checkboxes (`- [ ]`, `- [x]`)
- Ordered and unordered lists
- Horizontal rules (`---` outside frontmatter)
- Images with URLs (`![alt](url)`)

### Elements That Need Attention

- **Local image paths**: `![](./images/screenshot.png)` → may need path adjustment for vault attachment folder
- **HTML elements**: Obsidian supports some HTML but may render differently
- **Footnotes**: Obsidian supports footnotes but some MCP tools may not handle them well

## Content Structure

### Section Ordering

When converting, maintain this general structure:

1. Frontmatter (translated)
2. Title heading (H1)
3. Source attribution (where this came from)
4. Main content (converted)
5. Related Notes section (from references)

### Source Attribution

Add a brief note about the import source:

```markdown
> [!info] Imported from `.docs/research/02-07-2026-topic.md` on 2026-02-07
```

This helps track provenance without cluttering the note.
