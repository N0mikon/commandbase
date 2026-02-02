---
git_commit: 22359f413f53a227cf695a4c10141a1379ed74a0
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Marked historical - skills renamed since this handover"
topic: "RPI Skill Enforcement Patterns Implementation"
tags: [handover, rcode, icode, enforcement, superpowers-patterns]
status: historical
archived: 2026-02-01
archive_reason: "Completed work from 2026-01-27, superseded by 01-27-2026-skill-enforcement-complete.md which documents final state of all phases"
references:
  - newskills/researching-codebases/SKILL.md
  - newskills/implementing-plans/SKILL.md
  - .docs/plans/01-27-2026-rpi-enforcement-patterns.md
  - .docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md
---

# Handover: RPI Skill Enforcement Patterns

**Date**: 2026-01-27
**Branch**: master

> **Historical Note (2026-02-01)**: Skills referenced in this handover have been renamed:
> - `rcode` -> `researching-codebases`
> - `icode` -> `implementing-plans`
> - `pcode` -> `planning-codebases`
> - `vcode` -> `validating-implementations`
> - `commit` -> `committing-changes`
> - `pr` -> `creating-pull-requests`
> - `handover` -> `handing-over`
> - `takeover` -> `taking-over`
> - `new_project` -> `starting-projects`
> See `.docs/plans/02-01-2026-skill-structure-updates.md` for the rename plan.

## What I Was Working On

Adapting Superpowers enforcement patterns (Iron Laws, Gate Functions, Red Flags, Rationalization Prevention) to the RPI workflow skills.

- Research Superpowers patterns: **completed**
- Create implementation plan: **completed**
- Implement rcode.md enhancements: **completed**
- Implement icode.md enhancements: **completed**
- Restructure to directory format: **completed**
- Test in testbed: **completed** (rcode works, spawns agents properly)

## What I Accomplished

1. **Created research document** analyzing Superpowers patterns (`.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md`)
2. **Created implementation plan** with 10 phases (`.docs/plans/01-27-2026-rpi-enforcement-patterns.md`)
3. **Enhanced rcode.md** with:
   - Iron Law: "NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST"
   - Gate Function (5-step: IDENTIFY → SPAWN → WAIT → VERIFY → SYNTHESIZE)
   - Red Flags section
   - Rationalization Prevention table
   - The Bottom Line
4. **Enhanced icode.md** with:
   - Iron Law: "NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE"
   - Gate Function (5-step: IDENTIFY → RUN → READ → VERIFY → UPDATE)
   - Evidence Format requirements
   - Red Flags section
   - Rationalization Prevention table
   - The Bottom Line
5. **Restructured to directory format**: `newskills/rcode/SKILL.md`, `newskills/icode/SKILL.md`
6. **Created testbed** at `C:/code/testbed/` with sample codebase for testing
7. **Tested rcode** - confirmed it spawns agents, waits for results, cites file:line refs

## Key Learnings

1. **Skills need directory format** to be recognized as slash commands: `skillname/SKILL.md` not `skillname.md`
2. **Superpowers patterns are composable**: Iron Law → Gate Function → Red Flags → Rationalization Prevention → Bottom Line
3. **Spirit vs Letter clause** prevents rephrasing bypass: "Violating the letter is violating the spirit"
4. **Gate Functions need numbered steps** with clear trigger ("BEFORE...") and terminator ("ONLY THEN...")
5. **Rationalization tables** are two-column: Excuse | Reality - short, punchy counters
6. **"Skip any step = [consequence]"** is the enforcement hammer at end of Gate Function

## Files Changed

**Enhanced (directory format):**
- `newskills/rcode/SKILL.md` - Added Iron Law, Gate Function, Red Flags, Rationalization Prevention, Bottom Line (275 lines)
- `newskills/icode/SKILL.md` - Added same patterns adapted for implementation (221 lines)

**Created:**
- `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md` - Pattern analysis
- `.docs/plans/01-27-2026-rpi-enforcement-patterns.md` - Implementation plan (all checkboxes marked)
- `C:/code/testbed/` - Full testbed with sample codebase, skills, agents

**Updated:**
- `CLAUDE.md` - Updated directory structure and deploy commands

## Current State

- **rcode and icode are enhanced** with all enforcement patterns
- **Both use directory format** (`skillname/SKILL.md`)
- **Testbed works** - rcode tested, spawns agents correctly
- **Other skills still flat files**: pcode.md, vcode.md, commit.md, pr.md, handover.md, takeover.md, new_project.md
- **Changes not committed** - working tree has modifications

## Next Steps

1. **Commit the changes** in commandbase (`/commit`)
2. **Deploy to global config** (`cp -r newskills/rcode ~/.claude/skills/` etc.)
3. **Apply patterns to pcode.md** - Iron Law: "NO PLAN WITHOUT CODEBASE RESEARCH FIRST"
4. **Apply patterns to vcode.md** - Add two-stage review (spec compliance → code quality)
5. **Restructure remaining skills** to directory format as they're enhanced
6. **Consider session-start hook** to inject RPI workflow rules (from research Part 6)

## Context & References

- Research: `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md`
- Plan: `.docs/plans/01-27-2026-rpi-enforcement-patterns.md`
- Superpowers source: `C:/code/superpowers/skills/verification-before-completion/SKILL.md`
- Testbed: `C:/code/testbed/`

## Notes

- **Phased approach**: One skill at a time, rcode first since it's earlier in workflow
- **Directory restructure deferred**: Only rcode/icode converted, others remain flat files
- **vcode should get two-stage review** pattern from `subagent-driven-development` (spec compliance first, then code quality)
- **pcode already has good structure** but needs Iron Law and Red Flags added
