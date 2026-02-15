# Maintenance Operations

Detailed procedures for each batch maintenance operation, including tool patterns for finding affected notes.

## Operation 1: Tag Normalization (Mode A)

### Purpose
Rename, merge, or reorganize tags across vault notes to maintain taxonomy consistency.

### Sub-operations

**Rename tag:**
1. Find all notes using the old tag:
   - Frontmatter: `Grep("tags:.*old-tag", path=vault_path, glob="*.md")`
   - Inline: `Grep("#old-tag", path=vault_path, glob="*.md")`
2. Dry-run: list all notes that would change, show old → new tag
3. After approval: Edit each note to replace old tag with new tag
4. Verify: Search for old tag should return 0 results

**Merge tags:**
1. Find all notes using either tag
2. Dry-run: show which notes would be updated, which tag is the merge target
3. After approval: Replace all instances of the deprecated tag with the target tag
4. Verify: Only the target tag remains

**Reorganize hierarchy:**
1. Map current tag tree
2. Dry-run: show proposed restructuring (e.g., `#project` → `#work/project`)
3. After approval: Update all instances
4. Verify: New hierarchy is consistent

### Finding Tags
```
# Frontmatter tags
Grep("tags:.*target-tag", path=vault_path, glob="*.md")

# Inline tags (word boundary to avoid partial matches)
Grep("#target-tag[^a-z0-9/-]", path=vault_path, glob="*.md")

# All unique tags in vault
Grep("^tags:", path=vault_path, glob="*.md", output_mode="content")
```

## Operation 2: Frontmatter Bulk Update (Mode B)

### Purpose
Add, modify, or remove frontmatter properties across matching notes.

### Sub-operations

**Add property to notes missing it:**
1. Find notes without the property: Grep for notes in scope, filter those missing the property
2. Dry-run: list notes that would gain the new property and its value
3. After approval: Edit each note's frontmatter to add the property
4. Verify: Re-check that all target notes now have the property

**Modify property value:**
1. Find notes with the old value: `Grep("property: old-value", path=vault_path, glob="*.md")`
2. Dry-run: list notes and the old → new value change
3. After approval: Edit each note
4. Verify: Search for old value returns 0

**Remove property:**
1. Find notes with the property: `Grep("^property:", path=vault_path, glob="*.md")`
2. Dry-run: list notes that would lose the property
3. After approval: Edit each note to remove the property line
4. Verify: Property is gone from all target notes

### Important
- Never add nested YAML objects (Obsidian limitation)
- Respect the vault's global type registry (property types are vault-wide)
- Preserve existing properties not being modified

## Operation 3: Link Rot Detection (Mode C)

### Purpose
Find external URLs in notes that are dead (404, timeout, domain expired).

### Procedure
1. Find all external URLs in vault:
   - `Grep("https?://[^\\s)\\]]+", path=vault_path, glob="*.md")`
2. For each unique URL, check accessibility:
   - Use WebFetch to test the URL (HEAD request or light fetch)
   - Classify: accessible, redirect, 404, timeout, connection error
3. Dry-run: list broken URLs with the notes containing them
4. Suggest fixes:
   - For redirects: update URL to redirect target
   - For 404s: suggest archive.org link or removal
   - For timeouts: flag for manual review

### Rate Limiting
- Process URLs in batches of 10
- Wait between batches to avoid being rate-limited
- Skip duplicate URLs (same URL in multiple notes)

## Operation 4: Stale Note Identification (Mode D)

### Purpose
Find notes not modified in N days and surface them for review.

### Procedure
1. Determine staleness threshold (default: 90 days, or user-specified)
2. Scan vault notes for modification dates:
   - Check frontmatter `modified` or `updated` field if present
   - Fall back to file system modification time via Glob (sorted by mtime)
3. Filter to notes older than threshold
4. Categorize:
   - **Intentionally stable**: Reference notes, MOCs, templates (exclude by type/folder)
   - **Potentially stale**: Notes with `status: draft` or `status: in-progress` older than threshold
   - **Review candidates**: All other old notes
5. Present findings sorted by age

### Report Format
```
Stale Notes (not modified in 90+ days):
Draft/In-progress (likely forgotten):
- note-1.md — last modified 120 days ago — status: draft
- note-2.md — last modified 95 days ago — status: in-progress

Review candidates:
- note-3.md — last modified 200 days ago
- note-4.md — last modified 150 days ago

Excluded (intentionally stable): [N] notes (MOCs, templates, references)
```

## Operation 5: Cleanup (Mode E)

### Purpose
Find and handle empty files, placeholder-only notes, and notes with no meaningful content.

### Sub-operations

**Empty file detection:**
1. Find .md files with 0 bytes or only whitespace
2. Find .md files with frontmatter but no body content
3. Dry-run: list empty files with their locations

**Placeholder detection:**
1. Find notes containing only placeholder text:
   - `Grep("^# TODO", path=vault_path, glob="*.md")`
   - `Grep("^# Untitled", path=vault_path, glob="*.md")`
   - Notes with body < 50 characters after stripping frontmatter
2. Dry-run: list placeholder notes

**Actions:**
- Delete: Remove the file entirely (after user approval)
- Archive: Move to an archive folder
- Flag: Add a `status: needs-content` tag for later attention
