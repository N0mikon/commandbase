# Batch Safety Protocol

Vault-specific adaptation of the three-layer batch safety pattern. See `commandbase-core/reference/batch-safety-protocol.md` for the generalized, domain-agnostic version.

Safety requirements for batch maintenance operations on vault notes. These are non-negotiable.

## The Three Gates

Every batch operation must pass through three gates before execution:

### Gate 1: Dry Run
Before any changes, produce a complete preview of what would change.

**Dry-run format:**
```
DRY RUN — [Operation Name]
==========================
Notes affected: [N]
Changes per note:

1. path/to/note-1.md
   - [what would change]

2. path/to/note-2.md
   - [what would change]

[... up to 20 notes per batch]

Total: [N] notes, [M] changes
This is a preview. No changes have been made.
```

**Rules:**
- Show every note that would be affected
- Show the exact change for each note
- If more than 20 notes, show first 20 and summarize the rest
- Never skip the dry run, even for "simple" operations

### Gate 2: Checkpoint
Before execution, create a git checkpoint to enable rollback.

**Procedure:**
1. Run `/bookmarking-code create "pre-maintenance-[operation]"`
2. Verify the checkpoint was created successfully
3. Only proceed after checkpoint confirmation

**If checkpoint fails:**
- Do NOT proceed with batch changes
- Investigate why checkpoint failed
- Ask user how to proceed

### Gate 3: User Approval
After dry run and checkpoint, get explicit user approval.

```
Dry run complete. Checkpoint created.
[N] notes will be modified.

Proceed with applying changes?
```

Wait for explicit "yes" or approval before executing.

## Chunk Processing

### Why Chunks
Large batches (100+ notes) should be processed in chunks to:
- Allow verification between chunks
- Limit blast radius if something goes wrong
- Keep operations manageable

### Chunk Size
- Default: 20 notes per chunk
- User can adjust if needed
- After each chunk, briefly verify (spot-check 2-3 notes)
- **Rationale**: 20 balances meaningful progress per batch against context window limits — each note's dry-run output, edit operation, and verification consumes context. This default emerged from design analysis, not production testing. Adjust downward if notes are large (>500 lines each) or operations produce verbose output; adjust upward for small metadata-only changes.

### Between Chunks
```
Chunk [X]/[Y] complete.
- [N] notes modified
- Spot check: [note-1] ✓, [note-2] ✓

Continue with next chunk?
```

### If a Chunk Fails
1. Stop immediately
2. Report which notes were modified and which weren't
3. Suggest rollback to checkpoint if needed
4. Ask user how to proceed

## Rollback Procedure

If something goes wrong after changes are applied:

1. **Identify the problem**: What notes were incorrectly modified?
2. **Assess scope**: How many notes are affected?
3. **Rollback options**:
   - **Targeted undo**: If only a few notes, use Edit to revert specific changes
   - **Full rollback**: Use `/bookmarking-code` to restore to pre-maintenance checkpoint
4. **Verify rollback**: Confirm notes are restored to their pre-change state

## Operation-Specific Safety

### Tag operations
- Verify the target tag doesn't conflict with existing tags
- Check for partial matches (renaming `#project` shouldn't affect `#project-alpha`)
- Use word boundary matching in Grep patterns

### Frontmatter operations
- Never add nested YAML objects
- Preserve all properties not being modified
- Validate YAML syntax after each edit

### File deletion
- ALWAYS require explicit user approval per file (or per batch with file list)
- Prefer archiving (moving to archive folder) over deletion
- Never delete files that have incoming wikilinks without warning

### Link operations
- Verify replacement URLs are accessible before batch-replacing
- Don't auto-replace URLs without showing the old → new mapping

## Safety Checklist

Before every batch operation, verify:
- [ ] Dry run completed and reviewed
- [ ] Git checkpoint created via /bookmarking-code
- [ ] User has approved the changes
- [ ] Chunk size is set (default 20)
- [ ] Rollback path is clear (checkpoint name noted)

After every batch operation, verify:
- [ ] All target notes were modified as expected
- [ ] No unintended notes were affected
- [ ] Spot check confirms changes are correct
- [ ] No YAML syntax errors introduced
- [ ] No broken wikilinks created
