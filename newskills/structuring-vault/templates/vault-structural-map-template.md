# Vault Structural Map Template

Template for `.docs/structure/` documents produced by `/structuring-vault`. The docs-writer agent handles frontmatter — this template defines body sections.

---

## Body Sections

```markdown
# [Vault Name/Purpose] Structural Map

## Design Reference

[Link to .docs/design/ document that informed this structure]
[Or: "Lightweight mode — no design doc, requirements provided directly"]

## Current Structure

[Relevant portion of the current vault folder tree]
[Include only folders and note counts relevant to this reorganization]

```
vault/
  folder-a/          (12 notes)
  folder-b/          (5 notes)
  unsorted/          (34 notes)
  Attachments/       (images, PDFs)
```

## Proposed Structure

[Folder tree showing the target state after changes]
[Mark new, reorganized, and removed folders]

```
vault/
  Projects/          (new)
  Areas/             (new)
  Resources/         (new — absorbs unsorted/)
  Archives/          (new)
  MOCs/              (new)
  Templates/         (unchanged)
  Attachments/       (unchanged)
  daily/             (new)
```

### New Folders

- `folder/path/` — [Purpose: what note types live here]

### Reorganized Folders

- `old/path/` → `new/path/` — [What moves and why]

### Note Placement Rules

| Note Type | Folder | Naming Convention |
|-----------|--------|------------------|
| [Type 1] | [Folder] | [Pattern] |
| [Type 2] | [Folder] | [Pattern] |
| [MOCs] | [Folder] | [Pattern] |
| [Templates] | [Folder] | [Pattern] |
| [Daily notes] | [Folder] | [Pattern] |

### Attachment Handling

[Where images, PDFs, and embedded files go]
[Co-located vs centralized, naming pattern]

### Template Organization

[Where template files live, naming pattern, how they're accessed]

## Link Direction

[How notes connect — which types link to which]

```
MOCs → Topic Notes
Topic Notes → Related Notes
Daily Notes → Topic Notes (contextual links)
All Notes ✗ Direct cross-topic links without MOC  (discouraged/encouraged)
```

## Migration Order (reorganizations only)

[Numbered steps, each leaving the vault fully navigable with working wikilinks]

1. **[Step name]** — [What changes]. Wikilink updates: [which references change]. After this step: [what still works]
2. **[Step name]** — [What changes]. Wikilink updates: [which references change]. After this step: [what still works]
3. **[Step name]** — [What changes]. After this step: [everything works with new structure]

## Conventions Followed

[Which existing vault conventions this structure follows]

- Folder naming: [pattern observed, e.g., PascalCase, lowercase]
- Note naming: [pattern, e.g., descriptive titles, kebab-case]
- Link format: [wikilinks / markdown links]
- Attachment placement: [centralized / co-located]

## Next Steps

- Run `/planning-vault .docs/structure/MM-DD-YYYY-<topic>.md` to break this into phased implementation tasks
```

## Section Guidelines

- **Design Reference**: Always link back to the design doc. Traceability matters.
- **Current Structure**: Only include relevant folders. Don't dump the entire vault tree if only reorganizing one area.
- **Proposed Structure**: Mark every folder as new, reorganized, unchanged, or removed.
- **Note Placement Rules**: Table format for quick reference during implementation.
- **Migration Order**: Required for reorganizations, omit for new vaults. Each step MUST preserve wikilink integrity.
- **Conventions Followed**: Explicitly state which patterns were observed and followed.

## What Does NOT Belong

- Note content or frontmatter syntax
- Template code (Templater syntax, YAML examples)
- Design rationale (that's in the design doc)
- Task breakdown or phasing (that's for /planning-vault)
- Plugin configuration

These belong in Design (rationale), Plan (tasks), or Implementation (execution).

## Frontmatter

Handled by `docs-writer`. Provide these fields in the Task prompt:

```yaml
doc_type: "structure"
topic: "<vault name/purpose>"
tags: [vault, <relevant aspect tags>]
```
