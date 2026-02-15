# Batch Safety Protocol

Reusable safety pattern for any skill that modifies more than 10 files in a single invocation. This protocol is not domain-specific — it applies to vault maintenance, code refactoring, config migrations, or any destructive batch operation.

## The Three Layers

Every batch operation must pass through three layers before execution:

### Layer 1: Dry Run

Produce a complete preview of what would change without changing anything.

**Requirements:**
- Show every file that would be affected
- Show the exact change per file
- If more than 20 files, show first 20 and summarize the rest
- End with "This is a preview. No changes have been made."

### Layer 2: Git Checkpoint

Create a commit before any modifications so rollback is one command.

**Requirements:**
- Use `/bookmarking-code create "pre-[operation-name]"` (or equivalent git checkpoint)
- Verify the checkpoint was created successfully
- If checkpoint fails, do NOT proceed — ask user how to continue

### Layer 3: Chunked Processing

Process files in batches with pause points between chunks.

**Default chunk size:** 20 files

**Between chunks:**
- Spot-check 2-3 files from the completed chunk
- Report progress: "Chunk [X]/[Y] complete. [N] files modified."
- Ask to continue (or auto-continue if user pre-approved)

**If a chunk fails:**
1. Stop immediately
2. Report which files were modified and which weren't
3. Suggest rollback to checkpoint
4. Ask user how to proceed

## Chunk Size Guidance

The default of 20 balances meaningful progress per batch against context window limits — each file's dry-run output, edit operation, and verification consumes context.

**Adjust downward** (10-15) when:
- Files are large (>500 lines each)
- Operations produce verbose output
- Changes are complex (multi-site edits per file)

**Adjust upward** (30-50) when:
- Changes are small metadata-only operations
- Files are short
- User explicitly requests faster processing

## Rollback

If something goes wrong after changes are applied:

1. **Targeted undo**: If only a few files affected, use Edit to revert specific changes
2. **Full rollback**: Restore to the pre-operation checkpoint via `/bookmarking-code`
3. **Verify**: Confirm files are restored to their pre-change state

## Adoption Checklist

When adding batch safety to a new skill:

- [ ] Identify which operations affect >10 files
- [ ] Add dry-run output format specific to the operation
- [ ] Add checkpoint step before execution
- [ ] Set chunk size (default 20 or adjusted per guidance above)
- [ ] Add rollback instructions referencing the checkpoint
- [ ] Add a Red Flag entry: "About to apply batch changes without completing dry-run"
- [ ] Add a Rationalization Prevention entry: "It's just N files, no need for chunking"
