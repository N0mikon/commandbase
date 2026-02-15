---
name: maintaining-vault
description: "Use this skill when performing batch maintenance operations on vault content. This includes normalizing tags across notes, bulk-updating frontmatter properties, detecting and fixing link rot, identifying stale notes needing review, cleaning up empty or placeholder notes, and running batch metadata corrections. Activate when the user says 'maintain vault', 'normalize tags', 'bulk update frontmatter', 'find stale notes', 'clean up vault', or 'fix link rot'."
---

# Maintaining Vault

You are performing batch maintenance operations on an Obsidian vault. These operations affect multiple notes at once — tag normalization, frontmatter updates, link rot detection, stale note cleanup. Because batch operations are high-risk, every operation follows a strict safety protocol: dry-run first, checkpoint before execution, process in chunks.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO BATCH CHANGES WITHOUT DRY-RUN AND CHECKPOINT FIRST
```

Batch operations can corrupt many notes at once. The dry-run shows exactly what will change. The checkpoint enables rollback. Skipping either means no safety net.

**No exceptions:**
- Don't apply tag renames without a dry-run preview
- Don't modify frontmatter across notes without a git checkpoint
- Don't delete files without showing the full list first
- Don't process more than 20 notes without chunking

## The Gate Function

```
BEFORE applying any batch changes:

1. READ: Vault CLAUDE.md for conventions, schema, tag taxonomy
2. SCOPE: Determine operation mode and target notes
3. DRY-RUN: Show complete preview of what would change (Gate 1)
4. CHECKPOINT: Create git checkpoint via /bookmarking-code (Gate 2)
5. APPROVE: Get explicit user approval (Gate 3)
6. EXECUTE: Apply changes in chunks of 20, verify between chunks
7. ONLY THEN: Report results

Skip dry-run = blind changes. Skip checkpoint = no rollback. Both are unacceptable.
```

## Safety Protocol

See ./reference/batch-safety-protocol.md for the complete safety protocol including:
- Three gates (dry-run, checkpoint, user approval)
- Chunk processing rules (20 notes per chunk, verify between chunks)
- Rollback procedures
- Operation-specific safety requirements

**This protocol is non-negotiable for every mode.**

## Modes

### Mode A: Tag Normalization

Use this mode to rename, merge, or reorganize tags across notes.

**Steps:**
1. Read vault CLAUDE.md for tag taxonomy
2. Identify the tag operation (rename, merge, reorganize hierarchy)
3. Find all affected notes (frontmatter tags + inline tags)
4. **DRY-RUN**: Show each note and the tag change
5. **CHECKPOINT**: `/bookmarking-code create "pre-tag-normalization"`
6. After approval, apply changes in chunks
7. Verify: old tag should return 0 search results

See ./reference/maintenance-operations.md "Operation 1: Tag Normalization" for procedures.

### Mode B: Frontmatter Bulk Update

Use this mode to add, modify, or remove frontmatter properties across matching notes.

**Steps:**
1. Read vault CLAUDE.md for frontmatter schema
2. Identify the property operation (add, modify, remove)
3. Find all affected notes
4. **DRY-RUN**: Show each note and the property change
5. **CHECKPOINT**: `/bookmarking-code create "pre-frontmatter-update"`
6. After approval, apply changes in chunks
7. Verify: property state matches expectations

See ./reference/maintenance-operations.md "Operation 2: Frontmatter Bulk Update" for procedures.

### Mode C: Link Rot Detection

Use this mode to find dead external URLs in vault notes.

**Steps:**
1. Find all external URLs across vault notes
2. Test each unique URL for accessibility
3. Classify results (accessible, redirect, 404, timeout)
4. **DRY-RUN**: Show broken URLs with containing notes and suggested fixes
5. If user wants fixes applied:
   - **CHECKPOINT**: `/bookmarking-code create "pre-link-rot-fix"`
   - Apply URL replacements in chunks
6. Verify: re-test fixed URLs

See ./reference/maintenance-operations.md "Operation 3: Link Rot Detection" for procedures.

### Mode D: Stale Note Identification

Use this mode to find notes not modified in N days.

**Steps:**
1. Read vault CLAUDE.md for note type conventions (to exclude intentionally stable notes)
2. Determine staleness threshold (default: 90 days, or user-specified)
3. Scan vault for notes older than threshold
4. Categorize: forgotten drafts, review candidates, intentionally stable
5. Present findings — this mode is read-only (no automatic changes)
6. Suggest follow-up actions: archive, update, or delete

See ./reference/maintenance-operations.md "Operation 4: Stale Note Identification" for procedures.

### Mode E: Cleanup

Use this mode to find empty files, placeholder notes, and notes with no meaningful content.

**Steps:**
1. Scan vault for empty/minimal notes
2. Categorize: truly empty, frontmatter-only, placeholder text
3. **DRY-RUN**: Show each file and its status
4. Present options per file (delete, archive, flag for attention)
5. If deletion/archival approved:
   - **CHECKPOINT**: `/bookmarking-code create "pre-cleanup"`
   - Check for incoming wikilinks before deleting (warn if found)
   - Execute in chunks
6. Verify: target files removed/archived as requested

See ./reference/maintenance-operations.md "Operation 5: Cleanup" for procedures.

## Output Format

After each operation completes:

```
Maintenance Complete — [Operation Name]
========================================
Notes processed: [N]
Changes applied: [M]
Errors: [E]

Checkpoint: [checkpoint-name]
Rollback: /bookmarking-code restore "[checkpoint-name]" if needed

[Summary of changes]
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to apply batch changes without completing dry-run
- Skipping the git checkpoint
- Processing more than 20 notes without chunking
- Deleting files with incoming wikilinks
- Adding nested YAML objects to frontmatter
- Modifying notes outside the specified scope
- Applying changes that the user didn't explicitly approve

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just a tag rename, no need for dry-run" | Tag renames affect every note with that tag. Always dry-run. |
| "Checkpoint takes too long" | Rollback without checkpoint takes longer. Always checkpoint. |
| "These are obviously empty, just delete them" | Check for incoming links first. Empty files might be link targets. |
| "20 notes per chunk is too slow" | Slow and safe beats fast and corrupted. Chunk size is non-negotiable. |
| "User already approved, no need for per-chunk verification" | State can change between chunks. Verify between chunks. |

## The Bottom Line

**Dry-run. Checkpoint. Approve. Chunk. Verify.**

Batch maintenance is the most dangerous vault operation. Every shortcut creates risk across many notes at once. This is non-negotiable. Every batch. Every time.
