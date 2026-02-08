# Vault Verification Commands

How to verify vault changes using MCP tools and file-system tools. These replace traditional test/lint/typecheck commands used in code plans.

## Verification Approaches

### Note Existence
Verify a note exists at the expected path.

**MCP:** Use MCP read tool on the note path — success means it exists.
**File-system:** `Read(vault_path + "/note-name.md")` — file found means it exists.

### Wikilink Resolution
Verify `[[wikilinks]]` point to existing notes.

**MCP:** For each `[[target]]`, use MCP search for a note named "target".
**File-system:** `Grep("\\[\\[target\\]\\]", path=vault_path)` to find references, then `Glob("**/target.md", path=vault_path)` to verify target exists.

### Frontmatter Validation
Verify notes have expected frontmatter properties.

**MCP:** Use MCP read on notes and inspect YAML block.
**File-system:** `Grep("^property-name:", path=vault_path, glob="*.md")` to check property exists across files.

### Folder Structure
Verify folders exist and contain expected note types.

**MCP:** Use MCP list on folder path — verify expected notes present.
**File-system:** `Glob("folder-name/*.md", path=vault_path)` to list notes in folder.

### Tag Application
Verify tags are applied to expected notes.

**MCP:** Use MCP tag listing or search for tag.
**File-system:** `Grep("tags:.*tag-name", path=vault_path, glob="*.md")` to find notes with tag.

### MOC Coverage
Verify MOC notes link to expected target notes.

**File-system:** Read MOC note, verify it contains `[[target-note]]` for each expected note.

### Orphan Detection
Verify no notes are left without incoming links after changes.

**File-system:** For each moved/created note, `Grep("\\[\\[note-name\\]\\]", path=vault_path)` to verify at least one incoming link exists.

## Common Success Criteria Patterns

### For Note Creation
```
- [ ] Note exists at expected path (MCP read or file-system Read)
- [ ] Frontmatter contains required properties
- [ ] Note is linked from at least one MOC or related note
```

### For Note Move
```
- [ ] Note exists at new path (MCP read or file-system Read)
- [ ] Note no longer exists at old path
- [ ] All [[wikilinks]] referencing old name updated
- [ ] No broken links introduced (Grep for old reference returns 0 matches)
```

### For Folder Reorganization
```
- [ ] New folder structure matches plan (Glob verification)
- [ ] All notes in expected locations
- [ ] No orphan notes created by the move
- [ ] All wikilinks resolve correctly
```

### For Frontmatter Application
```
- [ ] Target notes contain expected properties (Grep verification)
- [ ] Property values match expected types/formats
- [ ] No YAML syntax errors (notes readable via MCP or Read)
```

### For Tag Application
```
- [ ] Target notes have expected tags (Grep for tag in frontmatter)
- [ ] No unintended tag changes to other notes
```

## Evidence Format

When completing a vault plan phase, show evidence:
```
Phase 1 complete.

Verification:
- Note exists at Projects/my-project.md: PASS (Read successful)
- Frontmatter contains 'status' property: PASS (Grep: 5/5 notes)
- All wikilinks resolve: PASS (Grep for [[old-name]]: 0 matches)
- MOC links to new note: PASS (Read MOC, contains [[my-project]])
```
