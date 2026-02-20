---
name: structuring-vault
description: "Use this skill when mapping folder layout, naming conventions, and note placement rules for an Obsidian vault. This includes deciding folder hierarchy, note file naming, MOC placement, template locations, attachment organization, and migration order for vault reorganizations. Activate when the user says 'structure vault', 'organize vault folders', 'where should notes go', or after /designing-vault."
---

# Structuring Vault

You are mapping folder layout, naming conventions, and note placement rules for an Obsidian vault by analyzing design decisions and current vault organization, then producing a structural map document.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO STRUCTURE WITHOUT UNDERSTANDING WHAT EXISTS
```

Structure decisions must be grounded in the actual vault. Use MCP tools and/or file-system tools to verify current vault organization before proposing changes.

**No exceptions:**
- Don't propose folder locations without checking current patterns
- Don't ignore existing conventions in a populated vault
- Don't include implementation details in the structural map
- Don't create migration steps that break wikilinks between steps

## The Gate Function

```
BEFORE writing any structural map:

1. READ: Find and read design doc (.docs/design/) if available
2. RESEARCH: Use MCP tools and/or file-system tools to map current vault folder organization
3. ANALYZE: Compare design decisions to current vault structure
4. MAP: Determine folder layout, note placement, naming conventions
5. SEQUENCE: For reorganizations, determine migration order (each step leaves vault navigable)
6. WRITE: Create .docs/structure/ document via docs-writer
7. PRESENT: Summary to user with structural map and link

Skipping steps = structuring blind
```

## Initial Response

When this skill is invoked:

### If a design doc is provided or referenced:
- Read the design doc FULLY
- Proceed to Step 2

### If no design doc but user provides requirements directly:
- Proceed in lightweight mode (skip design doc lookup)
- Note: structural maps without design docs are valid for simple vaults

### If no parameters provided:
```
I'll help you map folder layout and note organization for your vault.

Please provide:
1. A design document (.docs/design/) or vault organization description
2. The target vault (for reorganizations)

I'll analyze current structure and create a map showing where everything goes.
```

## Process Steps

### Step 1: Gather Context

- Check for design doc in `.docs/design/` with vault tags — read FULLY if exists
- Check for brainstorm doc in `.docs/brainstorm/` — note vault philosophy preferences
- Read vault CLAUDE.md for vault path and MCP connection details
- If user provides a target area directly, note it for exploration scoping

### Step 2: Analyze Current Structure

Use MCP tools and/or file-system tools to understand what exists:

**MCP tools:**
- List vault root to get top-level folder structure
- List subdirectories for nesting depth
- Search for MOC notes, template files, attachment folders

**File-system tools:**
- `Glob("**/*.md", path=vault_path)` to find all notes
- `Glob("**/", path=vault_path)` to find all folders
- `Grep("^tags:", path=vault_path, glob="*.md")` for tag patterns
- Read sample notes from each folder to understand contents

For complex vaults, spawn `general-purpose` agents to explore different areas in parallel.

Wait for ALL exploration to complete before proceeding.

Compile findings:
- Current folder organization
- Naming conventions in use
- Note type distribution per folder
- Attachment locations
- Template file locations
- MOC note locations

### Step 3: Create Structural Map

For each organizational decision from the design doc (or user requirements):

**Folder layout:**
- Which folders to create, rename, or reorganize
- Where each note type lives
- Top-level structure following design decisions

**Note placement rules:**
- Which folder each note type goes in
- Naming conventions per note type
- Where MOCs live relative to their topic notes

**Attachment handling:**
- Where images, PDFs, and embedded files go
- Co-located with notes vs centralized folder

**Template organization:**
- Where template files live
- Template naming patterns
- Accessibility from Templater/core templates

**Convention deference:**
- For populated vaults: follow existing patterns where they don't conflict with design
- For new vaults: propose conventions and confirm with user via AskUserQuestion

### Step 4: Sequence Migrations (Reorganizations Only)

For vault reorganizations, determine migration order:
- Each step must leave the vault navigable (all wikilinks working)
- Each step must preserve link integrity — when moving notes, update all `[[references]]`
- Prefer leaf-first ordering (move notes that aren't linked to first)
- Number each step with a description of what changes and what still works after

**Critical vault concern:** Every note move must update wikilinks. Identify which notes reference the moved note and plan updates.

### Step 5: Write Structural Map

Spawn a `docs-writer` agent via the Task tool:

```
Task prompt:
  doc_type: "structure"
  topic: "<vault name/purpose>"
  tags: [vault, <relevant aspect tags>]
  references: [<design doc, key vault paths>]
  content: |
    <compiled structural map using ./templates/vault-structural-map-template.md>
```

The structural map must contain:
- Folder tree visualization (current and proposed)
- Note placement rules per type
- Naming conventions
- Attachment handling plan
- Template organization
- Migration steps (reorganizations only)
- NO implementation details — no note content, no frontmatter syntax, no template code

### Step 6: Present and Suggest Next Step

```
STRUCTURE COMPLETE
==================

Structural map: .docs/structure/MM-DD-YYYY-<topic>.md

Folders: [count of top-level folders]
Note types: [count of distinct note types with placement]
Migration steps: [count, if reorganization]

Next: /planning-vault to break this into phased implementation tasks
```

## Important Guidelines

1. **Structure captures WHERE, not WHAT** — folder layout and note placement, no implementation details
2. **Research current patterns** — explore with tools before proposing anything
3. **Defer to conventions** — in populated vaults, follow what exists where possible
4. **Every migration step must preserve links** — no broken wikilinks in intermediate states
5. **Wikilink integrity is critical** — every note move must account for references

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Research

If you notice any of these, pause:

- Proposing folder structure without exploring current vault patterns
- Ignoring existing conventions in a populated vault
- Including implementation details (note content, template code) in the structural map
- Creating migration steps that leave broken wikilinks between steps
- Assuming vault structure without using tools to verify
- Proposing new conventions in a populated vault without acknowledging existing ones

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know the standard Obsidian structure" | THIS vault has its own patterns. Research them. |
| "The design doc already specifies structure" | Design says WHAT organization. Structure says WHERE notes go. Different concerns. |
| "Migration order doesn't matter" | Every step must preserve wikilinks. Order is the hard problem. |
| "This is too simple for a structural map" | Simple structures still need documenting for the planning phase. |
| "I can see the folder layout" | Explore with tools. Folder layout alone doesn't reveal link structure. |

## The Bottom Line

**Structure captures WHERE everything goes, not WHAT it does.**

Folder layout, note placement, naming conventions. Defer to existing patterns in populated vaults. Preserve wikilink integrity in every migration step.

This is non-negotiable. Every structure. Every time.
