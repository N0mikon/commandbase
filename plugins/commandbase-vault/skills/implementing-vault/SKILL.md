---
name: implementing-vault
description: "Use this skill when executing vault implementation plans from .docs/plans/. This includes creating notes, moving notes, updating wikilinks after moves, applying frontmatter properties, managing folder structure, and running vault linting validation. Activate when the user says 'implement vault plan', 'execute vault changes', 'apply vault structure', or after completing planning with /planning-vault."
---

# Implementing Vault

You are tasked with implementing an approved vault plan from `.docs/plans/`. These plans contain phases with specific vault operations and success criteria.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO IMPLEMENTATION WITHOUT A PLAN AND CHECKPOINT FIRST
```

If you haven't read the plan and created a baseline checkpoint, you cannot begin vault changes.

**No exceptions:**
- Don't start vault changes without reading the plan fully
- Don't skip the baseline checkpoint
- Don't mark phases complete without vault linting verification
- Don't claim "should work" - show it works with tool output

## The Gate Function

```
BEFORE claiming any phase is complete:

1. READ: The plan phase requirements fully
2. CHECKPOINT: Create baseline via /bookmarking-code create (first phase only)
3. EXECUTE: Implement vault changes using MCP and/or file-system tools
4. LINT: Run /linting-vault targeted on affected notes
5. VERIFY: Check success criteria with tool output as evidence
6. ONLY THEN: Mark checkboxes and proceed

Skip verification = false completion claim
```

## Getting Started

When given a plan path:
- Read the plan completely and check for any existing checkmarks (- [x])
- Read the vault CLAUDE.md for vault path and MCP config
- **Read files fully** - never use limit/offset parameters, you need complete context
- Think deeply about how the phases fit together
- Create a todo list to track your progress
- Create baseline checkpoint: `/bookmarking-code create "pre-implementation"`
- Start implementing if you understand what needs to be done

If no plan path provided, ask for one or list available plans in `.docs/plans/`.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan exactly. If reality requires deviation, STOP and present the deviation before making it.
- Implement each phase fully before moving to the next
- Verify your work with vault linting after each phase
- Update checkboxes in the plan as you complete sections
- Continue through all phases without stopping for manual confirmation

When things don't match the plan exactly, STOP and present the mismatch to the user.

## Vault Operations

See ./reference/vault-operations.md for detailed guidance on each operation type.

### Creating Notes
- Use MCP write tool or file-system Write tool
- Ensure frontmatter is valid YAML (no nested objects — Obsidian limitation)
- Add wikilinks to relevant MOCs or related notes

### Moving Notes
- Move the file to new location
- **Critical:** Find ALL `[[wikilinks]]` referencing the old note name
- Update every reference to point to the new location
- Verify no broken links remain

### Updating Frontmatter
- Use MCP frontmatter tools or file-system Edit on the YAML block
- Only modify specified properties
- Preserve existing properties not mentioned in the plan

### Applying Tags
- Add to frontmatter `tags:` property or inline in note body
- Follow the vault's tag convention (property vs inline, hierarchical vs flat)

### Creating Folders
- Use Bash `mkdir -p` for new vault folders
- Verify folder exists after creation

### Managing Wikilinks
- Use Grep to find all references: `Grep("\\[\\[target\\]\\]", path=vault_path)`
- Use Edit to update references in each file
- After updates, verify old references are gone

## Vault Linting

Run `/linting-vault` in targeted mode on notes affected by this phase. See linting-vault for the full check procedures (broken wikilinks, frontmatter validation, orphan detection, heading structure, and more).

For reference on the core check types, see ./reference/vault-linting.md.

## Execution Flow

For each phase:

1. **Implement the vault changes** described in the plan
2. **Run `/linting-vault`** targeted on affected notes
3. **Fix any failures** - do not proceed until linting passes
4. **Show evidence** - state what tools you ran and their output
5. **Update checkboxes** in the plan file using Edit
6. **Create checkpoint** - `/bookmarking-code create "phase-N-done"`
7. **Move to the next phase** - only after evidence is shown and checkpoint created

**Remember:** Steps 4 and 6 are not optional. No evidence = no completion. No checkpoint = no proceeding.

Do NOT pause between phases. Execute all phases continuously until complete or blocked.

## If You Get Stuck

When something isn't working as expected:
- First, make sure you've read the plan and vault CLAUDE.md completely
- Consider if the vault has changed since the plan was written
- Try exploring with MCP/file-system tools to understand current state
- If truly blocked, present the issue clearly and ask for guidance

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done
- Pick up from the first unchecked item
- Verify previous work only if something seems off

## Completion

When all phases are complete:
```
Implementation complete!

All phases executed:
- [x] Phase 1: [name]
- [x] Phase 2: [name]
- [x] Phase 3: [name]

Final vault linting (fresh run):
- Broken wikilinks: 0 found
- Frontmatter validation: all notes pass
- Orphan notes: 0 created
- Folder structure: matches plan

All success criteria verified with evidence above.
The plan at `.docs/plans/[filename].md` has been fully implemented.
```

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to mark a checkbox without running vault linting
- Claiming "should work" or "looks correct" without evidence
- Proceeding to next phase without showing tool output
- Moving notes without updating wikilink references
- Skipping the baseline checkpoint
- Making changes not described in the plan without explaining why

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Linting passed earlier" | Run it again. Vault state changes. Fresh evidence only. |
| "This phase is trivial" | Trivial phases still need linting. No exceptions. |
| "I can see the note is correct" | Show tool output. Visual inspection isn't evidence. |
| "User is waiting" | Wrong vault changes waste more time. Verify first. |
| "I'll lint at the end" | Per-phase linting catches issues early. Do it now. |
| "Wikilinks will update themselves" | Obsidian may auto-update, but verify. Don't assume. |
| "While I'm here, I should also reorganize..." | Only change what the plan specifies. |

## The Bottom Line

**No shortcuts for verification.**

Execute the plan. Lint the vault. Show the evidence. THEN claim completion.

This is non-negotiable. Every phase. Every time.
