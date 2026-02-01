---
git_commit: 22359f4
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Marked historical - newreference/ approach superseded by skill-local reference/ dirs"
topic: "Pattern Learning Research and Planning"
tags: [handover, learn, patterns, hooks, reference]
status: historical
references:
  - .docs/research/01-28-2026-everything-claude-code-patterns.md
  - .docs/research/01-28-2026-learn-command-pattern.md
  - .docs/research/01-28-2026-checkpoint-command-pattern.md
  - .docs/research/01-28-2026-contexts-pattern.md
  - .docs/research/01-28-2026-iterative-retrieval-pattern.md
  - .docs/research/01-28-2026-orchestrate-command-pattern.md
  - .docs/research/01-28-2026-skill-create-command-pattern.md
  - .docs/plans/01-28-2026-automatic-pattern-learning.md
---

# Handover: Pattern Learning Research and Planning

**Date**: 2026-01-28
**Branch**: master

> **Historical Note (2026-02-01)**:
> - The `newreference/` approach discussed in this handover was superseded by skill-local `reference/` subdirectories (each skill has its own `reference/` folder)
> - Skills mentioned here have been renamed:
>   - `/handover` -> `/handing-over`
>   - `/new_project` -> `/starting-projects`
>   - `/learn` is now `/learning-from-sessions`
> See `.docs/plans/02-01-2026-skill-structure-updates.md` for details.

## What I Was Working On

- Researching everything-claude-code repo for workflow enhancement ideas: **completed**
- Deep-diving into 6 specific patterns: **completed**
- Creating implementation plan for automatic pattern learning: **completed**
- Implementing the plan: **not started**

## What I Accomplished

1. **Comprehensive research** of everything-claude-code repo
   - Analyzed 16 skills, 23 commands, 12 agents, hooks configuration
   - Created `.docs/research/01-28-2026-everything-claude-code-patterns.md`

2. **Deep research** on 6 key patterns (individual research docs created):
   - `/learn` - Mid-session pattern extraction
   - `/checkpoint` - Progress verification gates
   - Contexts - Mode switching via CLI
   - Iterative retrieval - Smarter agent context
   - `/orchestrate` - Agent pipelines
   - `/skill-create` - Extract patterns from git

3. **Prioritized recommendations**:
   - 🔴 High: `/learn` and `/checkpoint`
   - 🟡 Medium: Contexts and iterative retrieval
   - 🟢 Low: `/orchestrate` and `/skill-create`

4. **Created implementation plan** for automatic pattern learning:
   - `.docs/plans/01-28-2026-automatic-pattern-learning.md`
   - 5 phases covering reference folder, /learn skill, CLAUDE.md template

## Key Learnings

1. **CLAUDE.md should use progressive disclosure** (`~/.claude/reference/Writing a good CLAUDE.md:79-101`)
   - Keep under 60 lines, point to reference docs
   - Don't inline everything - let Claude read docs when needed
   - Instructions beyond ~150-200 get ignored uniformly

2. **Hooks vs CLAUDE.md for automatic behavior** - decided CLAUDE.md instruction is lighter
   - everything-claude-code uses PreToolUse/PostToolUse hooks with background Haiku analysis
   - That's overkill for pattern detection - simple phrase matching suffices
   - User decided against hooks earlier in session for similar reasons

3. **Pattern learning fills gap between /handover and persistent knowledge**
   - /handover = session STATE (project-specific, requires /takeover)
   - /learn = reusable PATTERNS (global, auto-loaded)
   - Both needed for complete knowledge capture

4. **Reference folder pattern** - user already has `~/.claude/reference/`
   - Contains "Writing a good CLAUDE.md" article
   - Should create `newreference/` in commandbase for development
   - Deploy to `~/.claude/reference/` for global use

5. **User's /new_project skill** already follows CLAUDE.md best practices (`newskills/new_project/SKILL.md:239-244`)
   - Under 60 lines principle
   - Progressive disclosure
   - No code style rules
   - WHAT/WHY/HOW structure

## Files Changed

- `.docs/research/01-28-2026-everything-claude-code-patterns.md` - Main research summary
- `.docs/research/01-28-2026-learn-command-pattern.md` - /learn deep dive
- `.docs/research/01-28-2026-checkpoint-command-pattern.md` - /checkpoint deep dive
- `.docs/research/01-28-2026-contexts-pattern.md` - Contexts deep dive
- `.docs/research/01-28-2026-iterative-retrieval-pattern.md` - Iterative retrieval deep dive
- `.docs/research/01-28-2026-orchestrate-command-pattern.md` - /orchestrate deep dive
- `.docs/research/01-28-2026-skill-create-command-pattern.md` - /skill-create deep dive
- `.docs/plans/01-28-2026-automatic-pattern-learning.md` - Implementation plan

## Current State

- **Research**: Complete - 7 research documents covering patterns from everything-claude-code
- **Plan**: Complete - 5-phase plan for automatic pattern learning ready for implementation
- **Implementation**: Not started
- **Git**: All changes uncommitted

## Next Steps

1. **Review and approve plan** at `.docs/plans/01-28-2026-automatic-pattern-learning.md`
2. **Run `/icode`** to implement the 5 phases:
   - Phase 1: Create `newreference/` with pattern-learning.md, claude-md-guidelines.md
   - Phase 2: Create `/learn` skill
   - Phase 3: Add automatic behaviors to /new_project CLAUDE.md template
   - Phase 4: Update commandbase CLAUDE.md
   - Phase 5: Deploy and test
3. **Commit changes** after implementation verified

## Context & References

- Plan: `.docs/plans/01-28-2026-automatic-pattern-learning.md`
- Source repo: `C:/code/everything-claude-code/`
- CLAUDE.md article: `~/.claude/reference/Writing a good CLAUDE.md`
- Existing reference folder: `~/.claude/reference/`

## Notes

- **Hooks decision**: User explicitly decided against hooks for now - current skill enforcement is sufficient
- **Checkpoint pattern**: Worth implementing separately (not in this plan) - natural fit for /icode phases
- **Contexts pattern**: Lower priority - skills already have Iron Laws for behavior enforcement
- **Storage location**: Learned patterns go to `~/.claude/skills/learned/` (auto-loaded by Claude Code)
- **Confirmation required**: /learn must NEVER save without user approval (Iron Law in plan)
