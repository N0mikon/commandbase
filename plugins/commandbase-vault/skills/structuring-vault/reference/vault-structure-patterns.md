# Vault Structure Patterns Reference

Common vault structural patterns to recognize and follow. Use these as recognition aids — always verify which patterns the actual vault uses.

## Folder Organization Patterns

### PARA Method
Projects, Areas, Resources, Archives.
```
vault/
  Projects/        (active, time-bound work)
  Areas/           (ongoing responsibilities)
  Resources/       (topic references)
  Archives/        (completed/inactive)
  Templates/       (note templates)
  Attachments/     (images, PDFs)
```
**When to follow:** Users who want clear action-oriented organization.

### Zettelkasten Minimal
Flat structure with linking as primary organization.
```
vault/
  notes/           (all permanent notes, flat)
  fleeting/        (inbox, quick captures)
  literature/      (source notes)
  Templates/       (note templates)
  Attachments/     (images, PDFs)
```
**When to follow:** Users who prefer link-based navigation over folder-based.

### Topic-Based
Folders by subject area.
```
vault/
  Programming/
  Writing/
  Finance/
  Health/
  Templates/
  Attachments/
```
**When to follow:** Users with clear, distinct knowledge domains.

### Hybrid
Minimal top-level folders with tags/links for organization.
```
vault/
  Inbox/           (new, unsorted notes)
  MOCs/            (Maps of Content)
  Templates/
  Attachments/
  daily/           (daily notes)
```
**When to follow:** Users who want minimal folder structure but some navigation aids.

## Naming Convention Patterns

### Descriptive Titles
Notes named by their content.
```
How to Set Up Docker Compose.md
Meeting Notes 2026-02-07.md
```
**Signal:** Human-readable titles, may include spaces.

### ID-Prefixed
Notes with timestamp or sequential IDs.
```
202602071200 Docker Compose Setup.md
20260207-meeting-notes.md
```
**Signal:** Numeric prefix, Zettelkasten influence.

### Kebab-Case
Lowercase with hyphens, file-system friendly.
```
docker-compose-setup.md
meeting-notes-2026-02-07.md
```
**Signal:** Developer-oriented vaults, compatible with git.

### Date-Prefixed
Date prefix for chronological ordering.
```
2026-02-07 Docker Compose Setup.md
2026-02-07 Meeting Notes.md
```
**Signal:** Journal or log-oriented vaults.

## Attachment Organization Patterns

### Centralized
All attachments in one folder.
```
Attachments/
  image-001.png
  document.pdf
```
**Pro:** Easy to manage, clear where files go.
**Con:** No context for what each attachment relates to.

### Co-located
Attachments next to the notes that reference them.
```
Projects/my-project/
  notes.md
  diagram.png
  spec.pdf
```
**Pro:** Context preserved.
**Con:** Harder to find all attachments, potential naming conflicts.

### Subfolder Per Note
Each note with attachments gets its own folder.
```
Projects/
  my-project/
    my-project.md
    attachments/
      diagram.png
```
**Pro:** Clean, scalable.
**Con:** Deep nesting, more folder management.

## MOC Placement Patterns

### Dedicated MOC Folder
All MOCs live in one top-level folder.
```
MOCs/
  Programming MOC.md
  Writing MOC.md
```
**Pro:** Easy to find all MOCs.
**Con:** Separated from their topic notes.

### Co-located with Topic
MOCs live alongside their topic notes.
```
Programming/
  Programming MOC.md
  python-notes.md
  docker-notes.md
```
**Pro:** Context preserved.
**Con:** MOCs mixed with regular notes.

### Root Level
MOCs in vault root as top-level navigation.
```
vault/
  Programming MOC.md
  Writing MOC.md
  folders/
```
**Pro:** Immediate access.
**Con:** Root gets cluttered with many MOCs.

## Migration Sequencing for Vault Reorganization

### Leaf-First
Move notes with no incoming links first, then work inward.
- Safe: nothing references what you're moving
- Each step is independently navigable

### MOC-First
Create MOC structure first, then reorganize notes into it.
1. Create new folder structure and MOCs
2. Move notes folder by folder, updating MOC links
3. Clean up old structure

### Incremental
Move one folder/topic at a time, fully completing each before the next.
1. Move all notes in Topic A, update all references
2. Move all notes in Topic B, update all references
3. Continue until complete

**Critical for all approaches:** After every step, verify wikilinks still resolve. A vault with broken links is worse than an unorganized vault.
