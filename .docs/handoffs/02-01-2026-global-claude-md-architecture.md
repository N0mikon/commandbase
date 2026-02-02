---
git_commit: fe26d61
last_updated: 2026-02-01
last_updated_by: claude
topic: "Global CLAUDE.md Architecture - Research and Planning"
tags: [handover, claude-md, security, configuration, hierarchy]
status: active
references:
  - newskills/updating-claude-md/SKILL.md
  - newskills/starting-projects/reference/claude-md-guidelines.md
  - .docs/research/02-01-2026-global-claude-md-architecture.md
  - .docs/plans/02-01-2026-global-claude-md-implementation.md
---

# Handover: Global CLAUDE.md Architecture

**Date**: 2026-02-01
**Branch**: master

## What I Was Working On

Implementing a global CLAUDE.md architecture to separate universal security rules from project-specific content.

- Task 1: Create `updating-claude-md` skill - **completed**
- Task 2: Research global vs project CLAUDE.md hierarchy - **completed**
- Task 3: Create implementation plan - **completed**
- Task 4: Implement the plan - **not started**

## What I Accomplished

1. **Created `/updating-claude-md` skill** (deployed to `~/.claude/skills/`)
   - 6 update types: add section, update commands, add pointer, add behavior, restructure, remove outdated
   - Enforces same 5 principles as `/starting-projects`
   - Proposal format with before/after and principles check

2. **Researched global CLAUDE.md architecture**
   - Documented memory hierarchy (Enterprise → Global → Project → Local)
   - Identified security rules scattered across skills that should consolidate globally
   - Designed separation of concerns (what belongs where)

3. **Created implementation plan** at `.docs/plans/02-01-2026-global-claude-md-implementation.md`
   - Phase 1: Create `~/.claude/CLAUDE.md`
   - Phase 2: Update project guidelines
   - Phase 3: Add scope awareness to skill

## Key Learnings

1. **No global CLAUDE.md currently exists** - `~/.claude/CLAUDE.md` does not exist, so security rules are repeated in individual skills (`committing-changes/SKILL.md:23,36,209,234`)

2. **Claude reads .env automatically** - This is a security risk. Global CLAUDE.md creates behavioral guardrails even when Claude has file access. Defense-in-depth: Global rules + Skill enforcement + .gitignore

3. **Scope detection is path-based** - If path contains `~/.claude/` → GLOBAL scope, else → PROJECT scope. The `updating-claude-md` skill currently treats all files identically (`SKILL.md:56`)

4. **Automatic behaviors should be global** - The pattern learning trigger ("this happened before") is currently in project template (`starting-projects/templates/claude-md-template.md:50-52`) but should be global since it applies everywhere

5. **Security NEVER rules from committing-changes** - These exact rules should move to global:
   - `SKILL.md:234`: `**NEVER** commit sensitive files (.env, credentials, keys)`
   - `SKILL.md:232`: `**NEVER** use git add -A or git add .`
   - `SKILL.md:233`: `**NEVER** force push without explicit request`

## Files Changed

**Created this session:**
- `newskills/updating-claude-md/SKILL.md` (251 lines) - Main skill
- `newskills/updating-claude-md/reference/standard-sections.md` - Section structure reference
- `newskills/updating-claude-md/reference/validation-checklist.md` - Validation rules
- `.docs/research/02-01-2026-updating-claude-md-skill-design.md` - Skill design research
- `.docs/research/02-01-2026-global-claude-md-architecture.md` - Architecture research
- `.docs/plans/02-01-2026-global-claude-md-implementation.md` - Implementation plan

**Deployed:**
- `~/.claude/skills/updating-claude-md/` - Skill now active

## Current State

- **updating-claude-md skill**: Deployed and validated, but lacks scope detection
- **Global CLAUDE.md**: Does not exist yet
- **Project guidelines**: Don't mention hierarchy yet
- **Plan**: Ready for implementation

## Next Steps

1. **Implement Phase 1**: Create `~/.claude/CLAUDE.md` with content from plan
2. **Implement Phase 2**: Update `starting-projects` guidelines to explain hierarchy
3. **Implement Phase 3**: Add scope detection to `updating-claude-md` skill
4. **Commit and push**: After all phases complete

Run `/implementing-plans .docs/plans/02-01-2026-global-claude-md-implementation.md` to continue.

## Context & References

- Research: `.docs/research/02-01-2026-global-claude-md-architecture.md`
- Plan: `.docs/plans/02-01-2026-global-claude-md-implementation.md`
- Skill design: `.docs/research/02-01-2026-updating-claude-md-skill-design.md`
- Guidelines to update: `newskills/starting-projects/reference/claude-md-guidelines.md:38-44`
- Template to update: `newskills/starting-projects/templates/claude-md-template.md:50-52`
- Skill to update: `newskills/updating-claude-md/SKILL.md:52-63` (Initial Response section)

## Notes

- User provided extensive context about CLAUDE.md hierarchy from external research (Boris Cherny, Backslash Security findings)
- The "mistakes become documentation" pattern from Anthropic's team should inform how we evolve these files
- Consider dotfiles sync (GNU Stow) for multi-machine consistency - documented in research but not in plan
- Enterprise-level `/etc/claude-code/CLAUDE.md` support is out of scope for now
