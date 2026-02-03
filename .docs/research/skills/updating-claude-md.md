# Research: updating-claude-md Skill

## Overview

The `updating-claude-md` skill (`~/.claude/skills/updating-claude-md/SKILL.md`) updates existing CLAUDE.md files, adding new sections or modifying project configuration for Claude.

**Trigger phrases**: `update CLAUDE.md`, `add to CLAUDE.md`, `modify project instructions`, `change the project config`

## Purpose

Maintain project instructions:
- Adding commands
- Updating directory structures
- Adding context pointers to new documentation
- Recording learned patterns as automatic behaviors
- Restructuring files that have grown too large

## Process

### Step 1: Read Current CLAUDE.md
Load the existing file completely to understand current structure.

### Step 2: Identify Changes Needed
Based on user request, determine:
- What section to add/modify
- Where it fits in the structure
- How to maintain consistency

### Step 3: Make Surgical Edits
Don't rewrite the entire file - make targeted changes:
- Add new sections in appropriate locations
- Update existing sections
- Maintain formatting consistency

### Step 4: Validate Structure
Ensure the updated file:
- Has proper markdown formatting
- Sections are logically organized
- No duplicate information
- Commands are accurate

### Step 5: Report Changes
```
CLAUDE.md UPDATED
=================

Changes made:
- Added: [new section]
- Updated: [modified section]

Current structure:
- [Section 1]
- [Section 2]
- [New Section] (added)
```

## Common Update Types

### Adding Commands
```markdown
## Commands

### [New Command]
```bash
[command]
```
```

### Adding Context Pointers
```markdown
## Additional Context

- `.docs/[new-docs]/` - [Description]
```

### Recording Automatic Behaviors
```markdown
## Automatic Behaviors

When [trigger], [behavior].
```

## Integration Points

- Called after significant project changes
- Works with `/learning-from-sessions` for pattern recording
- Maintains project context for all skills

## File Reference

- Main: `~/.claude/skills/updating-claude-md/SKILL.md`
