---
name: importing-vault
description: "Use this skill when converting .docs/ artifacts into Obsidian vault notes. This includes transforming research documents, plans, handoffs, and learnings into vault-native format with wikilinks, callouts, tags, and frontmatter. Activate when the user says 'import to vault', 'convert docs to vault', 'move research to obsidian', or after completing a research/planning cycle."
---

# Importing to Vault

You are tasked with converting `.docs/` artifacts into Obsidian vault notes. These artifacts — research documents, plans, handoffs, learnings, brainstorms — contain project knowledge that belongs in the user's knowledge base. Your job is to transform them into vault-native format while respecting the vault's conventions.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO IMPORT WITHOUT UNDERSTANDING VAULT CONVENTIONS FIRST
```

If you haven't read the vault's CLAUDE.md and understood its conventions, you cannot begin converting.

**No exceptions:**
- Don't convert artifacts without reading the vault CLAUDE.md first
- Don't generate wikilinks to notes that don't exist in the vault
- Don't assume frontmatter schema — read the vault's conventions
- Don't auto-place notes in the vault — user reviews first

## The Gate Function

```
BEFORE converting any artifact:

1. READ: Vault CLAUDE.md for vault path, conventions, frontmatter schema, tag taxonomy
2. DISCOVER: Find .docs/ artifacts to import (user-specified or list available)
3. MAP: Determine conversion rules (frontmatter translation, tag mapping, wikilink targets)
4. CONVERT: Transform each artifact to vault-native format
5. VERIFY: Check converted notes for broken wikilinks, proper frontmatter, tag consistency
6. ONLY THEN: Present converted note for user review and vault placement

Skip vault convention reading = wrong format, wrong tags, broken links
```

## Initial Response

When invoked:

**If a specific `.docs/` path is provided as argument:**
```
Reading vault conventions from CLAUDE.md...
[Read vault CLAUDE.md, extract: vault path, frontmatter schema, tag conventions, folder structure]

Reading artifact at [path]...
[Read the .docs/ artifact, analyze its structure]

Conversion plan:
- Source: .docs/research/02-07-2026-topic.md
- Target type: [research/plan/handoff/learning/brainstorm]
- Frontmatter translation: [field mappings]
- Tag mapping: [.docs tags → vault tags]
- Wikilink candidates: [existing vault notes that could be linked]
- Suggested vault location: [folder path]

Converting now...
```

**If no argument provided:**
```
I'll help you import .docs/ artifacts into your vault.

Let me check what's available to import...
[List .docs/ subdirectories and recent files]

Available artifacts:
- .docs/research/ (N files)
- .docs/plans/ (N files)
- .docs/handoffs/ (N files)
- .docs/learnings/ (N files)
- .docs/brainstorm/ (N files)

[AskUserQuestion: What would you like to import?]
```

## Import Scope

Present import options via AskUserQuestion:

```
question: "What would you like to import?"
options:
  - "Single file" → user provides path
  - "All files of a type" → user selects .docs/ subdirectory
  - "Full .docs/ import" → convert everything
```

For batch imports, process each file individually and present a summary at the end.

## Conversion Process

See `./reference/conversion-rules.md` for detailed conversion rules.
See `./reference/docs-types.md` for `.docs/` artifact types and their vault mappings.

### Step 1: Read Vault Conventions

Before any conversion:
1. Read the vault's CLAUDE.md for vault path, MCP config, conventions
2. Identify the vault's frontmatter schema (required properties, naming)
3. Identify the vault's tag taxonomy (hierarchical vs flat, property vs inline)
4. Identify the vault's folder structure (where different note types go)

### Step 2: Analyze Source Artifact

For each `.docs/` artifact:
1. Read the full file
2. Identify the doc type from frontmatter or directory (research, plan, design, etc.)
3. Extract existing frontmatter properties
4. Identify internal references (other `.docs/` files, code file paths)
5. Note any warning/info/tip headers that could become callouts

### Step 3: Build Conversion Map

Map source elements to vault equivalents:
- **Frontmatter fields** → vault property schema (rename, add required fields, remove irrelevant ones)
- **`.docs/` references** → `[[wikilinks]]` (only if target note exists in vault)
- **Code references** (`file:line`) → keep as-is in a code block or remove based on context
- **`references:` list** → "Related Notes" section with wikilinks
- **Warning/info/tip headers** → Obsidian callouts (`> [!warning]`, `> [!info]`, `> [!tip]`)
- **Tags** → vault tag taxonomy (translate naming conventions)
- **Checkboxes** → keep as-is (Obsidian supports them natively)
- **Tables** → keep as-is (Obsidian renders markdown tables)
- **Code fences** → keep as-is (Obsidian renders code fences)

### Step 4: Convert and Present

1. Build the converted note content using the template from `./templates/imported-note-template.md`
2. Present the converted note to the user for review — do NOT write to vault automatically
3. Include:
   - The full converted note content
   - Suggested vault path
   - Suggested MOC to link from (if applicable)
   - Any wikilinks that couldn't be resolved (targets don't exist)
4. Ask: "Write this note to the vault?" with options for path adjustment

### Step 5: Write and Verify

After user approval:
1. Write the note to the vault at the agreed path
2. Verify the note exists at the target path
3. If MOC integration was agreed, add a wikilink to the note from the MOC
4. Check for broken wikilinks in the converted note

## Important Guidelines

- **User reviews before placement**: Never auto-write to vault. Always present the converted note and get approval.
- **Wikilinks only to existing notes**: Don't generate `[[links]]` to notes that don't exist. If a reference target doesn't exist in the vault, mention it as plain text or suggest creating the note.
- **Preserve original**: Don't modify the `.docs/` source file. Import is a copy+transform operation.
- **Frontmatter translation, not duplication**: Map `.docs/` frontmatter to vault conventions. Don't blindly copy properties that don't exist in the vault schema.
- **Batch imports need summaries**: When importing multiple files, present a summary table showing source → target mappings before starting conversion.
- **Duplicate detection**: Before writing, check if a note with a similar title already exists in the vault. If so, warn the user and ask how to proceed.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to write to vault without user reviewing the converted note
- Generating wikilinks to notes you haven't verified exist
- Converting without having read the vault's CLAUDE.md
- Assuming frontmatter schema without checking vault conventions
- Modifying the source `.docs/` file during import
- Skipping duplicate detection for batch imports

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The vault probably uses standard frontmatter" | Read the CLAUDE.md. Every vault is different. |
| "This wikilink target probably exists" | Verify with Glob or MCP search. Don't assume. |
| "User won't mind if I auto-place it" | Always present for review. User chooses placement. |
| "I'll check conventions after converting" | Wrong order. Conventions drive conversion rules. |
| "Batch import is too slow with review" | Show summary table for batch, then process. Quality > speed. |
| "The original formatting is close enough" | Transform fully. Half-converted notes create confusion. |

## The Bottom Line

**Read conventions. Convert faithfully. Let the user decide placement.**

Import is a bridge between project artifacts and personal knowledge. Get the translation right.
