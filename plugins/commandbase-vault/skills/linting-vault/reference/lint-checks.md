# Lint Check Procedures

Detailed procedures for each vault lint check. These expand on the checks originally defined in implementing-vault's vault-linting.md, adding empty file detection, duplicate detection, and tag consistency.

## Check 1: Broken Wikilinks

**Purpose:** Verify all `[[wikilinks]]` in target notes point to existing notes.

**Procedure:**
1. For each target note, read its content
2. Extract all `[[target]]` patterns (including `[[target|alias]]`, `[[target#heading]]`, `[[target#^block]]`)
3. Parse the note name from each link (strip alias, heading, block ref)
4. For each target note name, verify it exists:
   - `Glob("**/target-name.md", path=vault_path)` — should find at least one match
   - Or MCP search for the note — should return a result
5. For heading/block links, also verify the heading or block ID exists in the target note

**Report format:**
```
Broken Wikilinks:
- [[target-1]]: FOUND at folder/target-1.md
- [[target-2]]: NOT FOUND
- [[target-3#Heading]]: note FOUND, heading FOUND
- [[target-4#^ref]]: note FOUND, block ref NOT FOUND
Total: X checked, Y broken
```

**Auto-fix suggestions:**
- Suggest closest matching note name (Glob with fuzzy pattern)
- Suggest creating the missing note
- For heading links, suggest closest heading match

## Check 2: Frontmatter Validation

**Purpose:** Verify notes have required frontmatter and properties conform to the vault schema.

**Prerequisites:** Read the vault CLAUDE.md to determine required properties and type constraints.

**Procedure:**
1. For each target note, read the file
2. Verify frontmatter exists (starts with `---`, has closing `---`)
3. Verify YAML is parseable (no syntax errors)
4. Check required properties exist (from vault CLAUDE.md schema)
5. Validate property types match vault registry (see ofm-validation-rules.md)
6. Check for nested YAML objects (forbidden by Obsidian)
7. Verify `tags`, `aliases`, `cssclasses` use plural form

**Report format:**
```
Frontmatter Validation:
- note-1.md: tags=PRESENT type=PRESENT status=PRESENT — PASS
- note-2.md: tags=PRESENT type=MISSING status=PRESENT — FAIL (missing: type)
- note-3.md: YAML SYNTAX ERROR on line 4 — FAIL
Total: X checked, Y failing
```

## Check 3: Orphan Detection

**Purpose:** Find notes with zero incoming links (no other note links to them).

**Procedure:**
1. For each target note, extract its note name (filename without .md)
2. Search the vault for incoming links:
   - `Grep("\\[\\[note-name", path=vault_path, glob="*.md")`
   - Covers `[[note-name]]`, `[[note-name|alias]]`, `[[note-name#heading]]`
3. Exclude self-references (the note linking to itself)
4. Count remaining incoming links

**Report format:**
```
Orphan Detection:
- note-1: 5 incoming links — OK
- note-2: 1 incoming link — OK
- note-3: 0 incoming links — ORPHAN
Total: X checked, Y orphans
```

**Auto-fix suggestions:**
- Suggest relevant MOC to add the orphan to
- Suggest related notes that could link to it (by shared tags or folder)

## Check 4: Heading Structure

**Purpose:** Verify heading hierarchy has no skipped levels.

**Procedure:**
1. For each target note, read its content
2. Extract all headings with their levels (`#` = 1, `##` = 2, etc.)
3. Walk through headings in order:
   - First heading should be H1 (note title) or H2 if the note uses frontmatter title
   - Each subsequent heading can be same level, one level deeper, or any level shallower
   - Skipping deeper (e.g., H2 → H4 without H3) is invalid
4. Check for multiple H1 headings (warn, not error)

**Report format:**
```
Heading Structure:
- note-1.md: H1 → H2 → H3 → H2 — PASS
- note-2.md: H1 → H3 (skipped H2) — FAIL
- note-3.md: H1 → H1 (multiple H1) — WARN
Total: X checked, Y failures, Z warnings
```

## Check 5: Empty File Detection

**Purpose:** Find notes that are empty or contain only frontmatter with no body content.

**Procedure:**
1. For each target note, read its content
2. Strip frontmatter (everything between `---` delimiters)
3. Strip whitespace from remaining content
4. If remaining content is empty, the note is effectively empty

**Report format:**
```
Empty Files:
- note-1.md: 0 body characters — EMPTY
- note-2.md: frontmatter only, no body — EMPTY
Total: X checked, Y empty
```

## Check 6: Duplicate Note Detection

**Purpose:** Find notes with identical or near-identical titles that may represent duplicates.

**Procedure:**
1. Collect all note filenames in scope
2. Normalize names: lowercase, strip hyphens/underscores/spaces
3. Group notes with identical normalized names
4. For groups with >1 note, check content similarity (shared headings, similar word count)

**Report format:**
```
Duplicate Detection:
- "meeting-notes" and "Meeting Notes" — POTENTIAL DUPLICATE (same normalized name)
- "api-guide" in folder-a/ and folder-b/ — POTENTIAL DUPLICATE (same name, different folders)
Total: X notes checked, Y potential duplicate groups
```

## Check 7: Tag Consistency

**Purpose:** Verify tags follow vault conventions and detect tag drift.

**Prerequisites:** Read vault CLAUDE.md for tag taxonomy.

**Procedure:**
1. Collect all tags from target notes (frontmatter + inline)
2. Check each tag against vault conventions:
   - Correct case (should be lowercase)
   - Valid nesting hierarchy (parent tags should exist if nested)
   - No typos (suggest corrections for unknown tags)
3. Check for tags not in the documented taxonomy (may be new, may be typos)
4. Check for inconsistent nesting (e.g., `#project` and `#projects`)

**Report format:**
```
Tag Consistency:
- #status/active: 12 uses — OK (in taxonomy)
- #Status/Active: 2 uses — WARN (case mismatch, should be #status/active)
- #proect: 1 use — WARN (possible typo for #project)
- #new-topic/subtopic: 3 uses — INFO (not in documented taxonomy)
Total: X unique tags, Y warnings
```

## Mode A: Targeted Lint

Run after specific operations (note creation, moves, frontmatter changes).

**Scope:** Only notes specified by the user or affected by a recent operation.

**Checks to run:**
1. Broken wikilinks (on affected notes only)
2. Frontmatter validation (on affected notes only)
3. Heading structure (on affected notes only)
4. Orphan detection (on moved notes only)

**Summary format:**
```
Targeted Lint — [N] notes:
- Wikilinks: X checked, Y broken
- Frontmatter: X checked, Y invalid
- Headings: X checked, Y issues
- Orphans: X checked, Y orphaned
[PASS/FAIL with details]
```

## Mode B: Full Vault Lint

Comprehensive health report for the entire vault.

**Scope:** All .md files in the vault.

**Checks to run:** All 7 checks.

**Phases:**
1. **Inventory**: Count all notes, collect metadata
2. **Structure checks**: Headings, empty files, duplicates (no cross-reference needed)
3. **Link checks**: Broken wikilinks, orphans (cross-vault reference analysis)
4. **Metadata checks**: Frontmatter validation, tag consistency
5. **Report**: Generate full health report

**Summary format:**
```
Full Vault Lint — [vault name]
================================
Notes scanned: [N]

1. Broken wikilinks: X found
2. Frontmatter issues: X notes
3. Orphan notes: X found
4. Heading issues: X notes
5. Empty files: X found
6. Potential duplicates: X groups
7. Tag inconsistencies: X warnings

Overall health: [HEALTHY / NEEDS ATTENTION / CRITICAL]
[Details for each finding]
```

**Health thresholds:**
- HEALTHY: 0 broken links, 0 frontmatter errors, <5% orphans
- NEEDS ATTENTION: Any broken links or frontmatter errors, or 5-15% orphans
- CRITICAL: >10 broken links, or >15% orphans, or YAML syntax errors
