---
date: 2026-02-09
status: current
topic: updating-claude-md skill analysis
tags: [skill, claude-md, commandbase-core, configuration]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file paths from old newskills/ layout to plugins/ layout, expanded content to reflect actual skill capabilities"
references:
  - plugins/commandbase-core/skills/updating-claude-md/SKILL.md
  - plugins/commandbase-core/skills/updating-claude-md/reference/standard-sections.md
  - plugins/commandbase-core/skills/updating-claude-md/reference/validation-checklist.md
---

# Research: updating-claude-md Skill

## Overview

The `updating-claude-md` skill (`plugins/commandbase-core/skills/updating-claude-md/SKILL.md`) updates existing CLAUDE.md files, adding new sections or modifying project configuration for Claude. Part of the `commandbase-core` plugin.

**Trigger phrases**: `update CLAUDE.md`, `add to CLAUDE.md`, `modify project instructions`, `change the project config`

## Purpose

Maintain project instructions:
- Adding commands
- Updating directory structures
- Adding context pointers to new documentation
- Recording learned patterns as automatic behaviors
- Restructuring files that have grown too large

## Core Concepts

### The Iron Law
No change without reading the current file first. CLAUDE.md is the foundation of every Claude session -- blind edits corrupt project context.

### The Gate Function
Before proposing any edit: READ the file, PARSE sections/lines, CLASSIFY the update type, VALIDATE against principles, then propose. Skipping any step risks corrupting project configuration.

### Scope Detection
The skill detects whether it is updating a **global** (`~/.claude/CLAUDE.md`) or **project** (`./CLAUDE.md`) file, and enforces different rules for each:
- Global: identity, NEVER rules, scaffolding, cross-project behaviors
- Project: project identity, structure, commands, verification

### The 5 Principles
Every change is validated against these before applying:

| # | Principle | Rule |
|---|-----------|------|
| 1 | Less is more | Under 60 lines ideal, never exceed 300 |
| 2 | Universally applicable | Only info relevant to every session |
| 3 | Progressive disclosure | Point to docs, don't inline everything |
| 4 | No code style rules | Let linters handle formatting |
| 5 | WHAT, WHY, HOW | Cover identity, purpose, and commands |

## Process

### Step 1: Read Current CLAUDE.md
Load the existing file completely to understand current structure. Detect scope (global vs project). Report current state including line count and section listing.

### Step 2: Classify Update Type
The skill recognizes 6 update types:
1. **Add Section** -- new `##` section (e.g., Deployment, Testing)
2. **Update Commands** -- modifying Key Commands section
3. **Add Context Pointer** -- reference to `.docs/` documentation
4. **Add Automatic Behavior** -- recording a learned pattern
5. **Restructure** -- file too large, needs reorganization
6. **Remove Outdated** -- deleting obsolete content

### Step 3: Propose with Validation
Present every change in a structured proposal format showing: update type, target section, line impact (before/after), current content, proposed content, and a principles check against all 5 principles.

### Step 4: Apply After Approval
No changes applied without explicit user approval. This is enforced.

### Step 5: Report Changes
```
CLAUDE.MD UPDATED
=================

Change applied: [brief description]
Lines: [before] -> [after]
Section: [## Section Name]

The file now has [N] lines ([status relative to 60-line ideal]).
```

## Reference Files

The skill includes two reference files:

- **standard-sections.md** -- Expected CLAUDE.md section order and line budgets per section (title: 2-3 lines, structure: 8-15 lines, development: 15-25 lines, total ideal: 38 lines, max: 68 lines)
- **validation-checklist.md** -- Pre-change, principle, content quality, and post-change validation checklists; red flag triggers and content placement guide

## Integration Points

- Called after significant project changes
- Works with `/learning-from-sessions` for pattern recording
- Maintains project context for all skills
- Enforces same guidelines as `/starting-projects`

## File References

- Skill: `plugins/commandbase-core/skills/updating-claude-md/SKILL.md`
- Standard sections reference: `plugins/commandbase-core/skills/updating-claude-md/reference/standard-sections.md`
- Validation checklist reference: `plugins/commandbase-core/skills/updating-claude-md/reference/validation-checklist.md`
