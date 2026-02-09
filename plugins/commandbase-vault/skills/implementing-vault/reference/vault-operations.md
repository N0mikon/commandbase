# Vault Operations Reference

Detailed guide for vault operations using MCP tools and file-system tools.

## Creating Notes

### Using MCP Write Tool
- MCP write tool creates a note at the specified vault path
- Supports overwrite, append, and prepend modes
- Frontmatter must be valid YAML

### Using File-System Write Tool
- `Write(file_path=vault_path + "/folder/note-name.md", content="...")`
- Full control over note content
- Must ensure vault path is correct

### Frontmatter Rules
- Must be valid YAML between `---` delimiters
- No nested YAML objects (Obsidian limitation)
- Supported types: text, list, number, checkbox, date
- Lists use YAML array syntax: `tags: [tag1, tag2]` or multiline `- tag1`

### Example
```markdown
---
title: My Note
tags: [project, active]
status: draft
created: 2026-02-07
---

# My Note

Content here with [[wikilinks]] to related notes.
```

## Moving Notes

Moving a note is a multi-step operation that must preserve vault integrity.

### Procedure
1. **Read the note** at the old location
2. **Write the note** at the new location (same content)
3. **Find all references** to the old note:
   - `Grep("\\[\\[old-note-name\\]\\]", path=vault_path, glob="*.md")`
   - Also check for aliases: `Grep("\\[\\[old-note-name\\|", path=vault_path, glob="*.md")`
4. **Update each reference** to use the new note name (if name changed) or just verify they still resolve (if only folder changed — Obsidian resolves by name, not path)
5. **Delete the old file** (or verify it's been moved, not copied)
6. **Verify** no references to the old note remain

### Important: Obsidian Link Resolution
Obsidian resolves `[[wikilinks]]` by **note name**, not by file path. So if you move `folder-a/note.md` to `folder-b/note.md` without renaming, existing `[[note]]` links will still resolve.

However, if you **rename** the note (e.g., `old-name.md` → `new-name.md`), ALL `[[old-name]]` references must be updated to `[[new-name]]`.

## Updating Frontmatter

### Using MCP Frontmatter Tools
Some MCP servers provide atomic frontmatter operations (set property, remove property).

### Using File-System Edit
1. Read the note to get current content
2. Identify the YAML block between `---` delimiters
3. Use Edit to modify specific properties
4. Preserve all properties not mentioned in the plan

### Example Edit
```
Old: status: draft
New: status: active
```

Use the Edit tool with `old_string` / `new_string` targeting the specific property line.

## Applying Tags

### Frontmatter Tags
```yaml
tags: [existing-tag, new-tag]
```
Add to the existing tags list, don't replace it.

### Inline Tags
```markdown
Some content #new-tag here.
```
Placed within note body, not frontmatter.

### Which to Use
Follow the vault's convention (from design doc or CLAUDE.md):
- If vault uses frontmatter tags: add to `tags:` property
- If vault uses inline tags: add in note body
- If vault uses both: follow the specific rule for this tag type

## Creating Folders

### Using Bash
```bash
mkdir -p /path/to/vault/new-folder
```

### Verification
After creation, verify with:
- `Glob("new-folder/*", path=vault_path)` — should return the folder (empty initially)
- Or `ls` via Bash to confirm

## Managing Wikilinks

### Finding References
```
Grep("\\[\\[target-name\\]\\]", path=vault_path, glob="*.md")
```
This finds all notes that link to `target-name`.

Also check for aliased links:
```
Grep("\\[\\[target-name\\|", path=vault_path, glob="*.md")
```

### Updating References
For each file containing a reference:
1. Read the file
2. Use Edit to replace `[[old-name]]` with `[[new-name]]`
3. Use `replace_all: true` if multiple references in the same file

### Verifying Updates
After updating, verify old references are gone:
```
Grep("\\[\\[old-name\\]\\]", path=vault_path, glob="*.md")
```
Should return 0 matches.
