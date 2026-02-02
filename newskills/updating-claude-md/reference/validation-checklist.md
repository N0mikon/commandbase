# CLAUDE.md Validation Checklist

Run through these checks before applying any change to CLAUDE.md.

## Pre-Change Validation

Before proposing a change:

- [ ] Read the current CLAUDE.md completely
- [ ] Count current lines
- [ ] Identify existing sections
- [ ] Understand the project context

## Principle Checks

For every proposed change:

### 1. Less Is More
- [ ] Will the file stay under 60 lines? (Ideal)
- [ ] Will the file stay under 300 lines? (Maximum)
- [ ] Is every line necessary?
- [ ] Could this be condensed?

**If NO**: Suggest progressive disclosure or condensation.

### 2. Universally Applicable
- [ ] Is this relevant to EVERY Claude session?
- [ ] Is this project-wide, not feature-specific?
- [ ] Would removing this hurt any session?

**If NO**: This content doesn't belong in CLAUDE.md.

### 3. Progressive Disclosure
- [ ] Is detailed content moved to `.docs/`?
- [ ] Are pointers used instead of inline content?
- [ ] Can Claude find details when needed?

**If NO**: Create a `.docs/` file and add a pointer.

### 4. No Code Style Rules
- [ ] No formatting preferences included?
- [ ] No linting rules repeated?
- [ ] No indentation/naming conventions?

**If NO**: Remove style rules, rely on linter config.

### 5. WHAT, WHY, HOW
- [ ] Project identity clear? (WHAT)
- [ ] Purpose stated? (WHY)
- [ ] Key commands included? (HOW)

**If NO**: Ensure these fundamentals are covered first.

## Content Quality Checks

- [ ] No placeholder text or TODOs
- [ ] No duplicate information
- [ ] No contradictory instructions
- [ ] Commands are accurate and current
- [ ] Paths are correct

## Post-Change Validation

After applying a change:

- [ ] Final line count reported
- [ ] Status relative to 60-line ideal stated
- [ ] No validation warnings remain
- [ ] Change summary provided

## Red Flag Triggers

Stop and reconsider if:

| Condition | Action |
|-----------|--------|
| File would exceed 300 lines | Must restructure first |
| Adding code style rules | Remove them |
| Inline documentation > 10 lines | Move to `.docs/` |
| Content is session-specific | Don't add to CLAUDE.md |
| Duplicating linter config | Remove duplication |
| No user approval | Don't apply |

## Quick Reference: What Belongs Where

| Content Type | Location |
|--------------|----------|
| Project identity | CLAUDE.md |
| Key commands (4-6) | CLAUDE.md |
| Verification command | CLAUDE.md |
| Brief structure | CLAUDE.md |
| Automatic behaviors | CLAUDE.md |
| Detailed documentation | `.docs/` |
| API documentation | `.docs/` |
| Database schemas | `.docs/` |
| All commands list | `.docs/` |
| Architecture deep dive | `.docs/` |
| Code style rules | Linter config |
