# Structural Map Template

Template for `.docs/structure/` documents produced by `/structuring-code`. The docs-writer agent handles frontmatter — this template defines body sections.

---

## Body Sections

```markdown
# [Feature/System] Structural Map

## Design Reference

[Link to .docs/design/ document that informed this structure]
[Or: "Lightweight mode — no design doc, requirements provided directly"]

## Current Structure

[Relevant portion of the current file tree in the target area]
[Include only files/directories relevant to this feature or refactor]

```
src/
  existing-dir/
    file-a.ts
    file-b.ts
  other-dir/
    file-c.ts
```

## Proposed Structure

[File tree showing the target state after changes]
[Mark new, modified, and removed files]

```
src/
  existing-dir/
    file-a.ts        (modified)
    file-b.ts        (unchanged)
    new-file.ts      (new)
  other-dir/
    file-c.ts        (modified)
  new-dir/           (new)
    feature.ts       (new)
    feature.test.ts  (new)
```

### New Files

- `path/to/new/file.ext` — [Purpose: what this file is responsible for]

### Modified Files

- `path/to/existing/file.ext` — [What changes: new exports, modified interface, etc.]

### Removed/Split Files

- `path/to/old/file.ext` → split into [list of new files and why]

## Module Boundaries

[Which modules/directories are independent units]
[Dependency direction: what imports what]

```
feature-a → shared/utils
feature-b → shared/utils
feature-a ✗ feature-b   (no direct dependency)
```

## Test Organization

[Where tests go for each component — following existing conventions]
[Test types per component: unit, integration, e2e]

- `feature.test.ts` — unit tests for [component]
- `feature.integration.test.ts` — integration test for [flow]

## Migration Order (refactors only)

[Numbered steps, each leaving the codebase in a working state]

1. **[Step name]** — [What changes]. After this step: [what still works]
2. **[Step name]** — [What changes]. After this step: [what still works]
3. **[Step name]** — [What changes]. After this step: [everything works with new structure]

## Conventions Followed

[Which existing codebase conventions this structure follows]

- File naming: [pattern observed, e.g., kebab-case, camelCase]
- Test placement: [co-located / mirror tree / by type]
- Module exports: [barrel / direct / mixed]

## Next Steps

- Run `/planning-code .docs/structure/MM-DD-YYYY-<topic>.md` to break this into phased implementation tasks
```

## Section Guidelines

- **Design Reference**: Always link back to the design doc. Traceability matters.
- **Current Structure**: Only include relevant files. Don't dump the entire tree.
- **Proposed Structure**: Mark every file as new, modified, unchanged, or removed.
- **Module Boundaries**: Show dependency direction with arrows. Flag violations.
- **Test Organization**: Follow whatever pattern the codebase already uses.
- **Migration Order**: Required for refactors, omit for greenfield. Each step must be independently viable.
- **Conventions Followed**: Explicitly state which patterns were observed and followed.

## What Does NOT Belong

- Implementation code or pseudocode
- Function signatures or API details
- Design rationale (that's in the design doc)
- Task breakdown or phasing (that's for /planning-code)
- Performance considerations
