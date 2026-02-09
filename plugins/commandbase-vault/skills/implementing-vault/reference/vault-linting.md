# Vault Linting Reference

Linting checks to run after each implementation phase. These are built into the implementation workflow, not a standalone tool.

## Broken Wikilink Detection

**Purpose:** Verify all `[[wikilinks]]` in modified notes point to existing notes.

**Procedure:**
1. For each modified/created note, read its content
2. Extract all `[[target]]` patterns (including `[[target|alias]]`)
3. For each target, verify the note exists:
   - `Glob("**/target.md", path=vault_path)` — should find at least one match
   - Or MCP read on the target note — should succeed

**Report format:**
```
Broken wikilinks check:
- [[target-1]]: FOUND at folder/target-1.md
- [[target-2]]: FOUND at other/target-2.md
- [[target-3]]: NOT FOUND — broken link
```

**Fix:** Either create the missing note or update the wikilink to point to an existing note.

## Frontmatter Validation

**Purpose:** Verify modified notes have required frontmatter properties.

**Procedure:**
1. Identify required properties from the plan or vault design doc
2. For each modified/created note:
   - Read the note
   - Check that each required property exists in the YAML block
   - Check property values are valid types

**Report format:**
```
Frontmatter validation:
- note-1.md: tags=PRESENT, status=PRESENT, created=PRESENT — PASS
- note-2.md: tags=PRESENT, status=MISSING, created=PRESENT — FAIL
```

**Fix:** Add missing properties using Edit on the YAML block.

## Orphan Detection

**Purpose:** After note moves, verify moved notes still have at least one incoming link.

**Procedure:**
1. For each note that was moved or whose name changed:
   - Extract the note name
   - `Grep("\\[\\[note-name\\]\\]", path=vault_path, glob="*.md")`
   - Count matches (excluding self-references)

**Report format:**
```
Orphan detection:
- moved-note-1: 3 incoming links — OK
- moved-note-2: 0 incoming links — ORPHAN
```

**Fix:** Add the orphaned note to a relevant MOC or link from a related note.

## Heading Structure

**Purpose:** Verify no skipped heading levels in created/modified notes.

**Procedure:**
1. For each created/modified note, read the content
2. Check heading hierarchy:
   - First heading should be `#` (H1) — typically the note title
   - No skipping levels (H1 → H3 without H2 is invalid)

**Report format:**
```
Heading structure:
- note-1.md: H1 → H2 → H3 — PASS
- note-2.md: H1 → H3 (skipped H2) — FAIL
```

**Fix:** Insert the missing heading level or adjust heading hierarchy.

## Linting Summary Format

After each phase, present a linting summary:
```
Vault Linting — Phase [N]:
- Broken wikilinks: [X] checked, [Y] broken
- Frontmatter: [X] notes checked, [Y] missing required properties
- Orphans: [X] moved notes checked, [Y] orphaned
- Headings: [X] notes checked, [Y] with issues

[If all pass]: All linting checks pass.
[If failures]: [List specific failures and fixes needed]
```

## When to Lint

**After every phase:**
- Run all 4 checks on notes affected by that phase
- Do NOT proceed to next phase if linting fails

**After final phase:**
- Run comprehensive linting on ALL notes mentioned in the plan
- This is the final verification before declaring implementation complete

## Scope of Linting

Lint only notes affected by the current phase, not the entire vault. This keeps linting fast while still catching issues.

For the final comprehensive lint after all phases, expand scope to all notes referenced anywhere in the plan.
