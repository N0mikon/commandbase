# Vault Implementation Checklist Template

Per-phase checklist template for vault implementation operations.

## Phase Checklist

Use this checklist pattern for each phase during vault implementation:

```markdown
## Phase [N]: [Phase Name]

### Pre-Phase
- [ ] Read phase requirements fully
- [ ] Identify all notes/folders affected
- [ ] Verify current vault state matches plan assumptions

### Execution
- [ ] [Operation 1: e.g., Create folder Projects/]
- [ ] [Operation 2: e.g., Move note-a.md to Projects/]
- [ ] [Operation 3: e.g., Update wikilinks referencing note-a]
- [ ] [Operation 4: e.g., Apply frontmatter to all moved notes]

### Vault Linting
- [ ] Broken wikilinks: [X] checked, 0 broken
- [ ] Frontmatter validation: [X] notes pass
- [ ] Orphan detection: 0 orphans created
- [ ] Heading structure: all notes pass

### Post-Phase
- [ ] Success criteria from plan all met (with evidence)
- [ ] Plan checkboxes updated
- [ ] Checkpoint created: phase-[N]-done
```

## Operation-Specific Checklists

### Note Creation Checklist
```
- [ ] Note written at correct path
- [ ] Frontmatter valid (no nested YAML, required properties present)
- [ ] Wikilinks added to relevant MOCs/related notes
- [ ] Note reachable from at least one other note
```

### Note Move Checklist
```
- [ ] Note exists at new location
- [ ] Note removed from old location
- [ ] All [[wikilinks]] to old name updated (if renamed)
- [ ] Grep for old name returns 0 matches
- [ ] Note still has incoming links (not orphaned)
```

### Folder Reorganization Checklist
```
- [ ] New folders created
- [ ] Notes moved to correct folders
- [ ] All wikilinks still resolve
- [ ] No orphan notes created
- [ ] Old empty folders cleaned up (if applicable)
```

### Frontmatter Application Checklist
```
- [ ] Target notes identified
- [ ] Required properties added
- [ ] Existing properties preserved
- [ ] YAML syntax valid (no nested objects)
- [ ] Property values match expected types
```

### Tag Application Checklist
```
- [ ] Tags added to correct notes
- [ ] Tag format matches vault convention (frontmatter vs inline)
- [ ] No unintended tag changes to other notes
- [ ] Tag taxonomy consistency maintained
```
