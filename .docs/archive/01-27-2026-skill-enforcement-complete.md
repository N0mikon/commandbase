---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Frontmatter refresh after 64 commits - still valid historical archive, updated references note"
topic: "RPI Skill Enforcement Patterns - Implementation Complete"
tags: [handover, skills, enforcement, rpi-workflow]
status: historical
archived: 2026-02-01
archive_reason: "Completed handoff - work was committed in a7794e1, skills have been renamed and restructured since"
references:
  - .docs/plans/01-27-2026-rpi-enforcement-patterns.md
  - .docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md
  - newskills/*/SKILL.md
---

# Handover: RPI Skill Enforcement Complete

**Date**: 2026-01-27
**Branch**: master

> **Historical Note (2026-02-01)**: Skills referenced in this handover have been renamed:
> - `pcode` -> `planning-code`
> - `vcode` -> `validating-code`
> - `commit` -> `committing-changes`
> - `pr` -> `creating-prs`
> - `handover` -> `handing-over`
> - `takeover` -> `taking-over`
> - `new_project` -> `starting-projects`
>
> **Historical Note (2026-02-09)**: Skills were further restructured from `newskills/` into the
> plugin system at `plugins/*/skills/*/SKILL.md`. The `handing-over` and `taking-over` skills
> were replaced by session skills (`starting-session`, `ending-session`, `resuming-session`,
> `learning-from-sessions`) in the `commandbase-session` plugin. The enforcement patterns
> (Iron Law, Gate Function, etc.) are still present in the surviving skills.

## What I Was Working On

Implementing Phases 11-17 of the RPI enforcement patterns plan. All 9 skills now have:
- Directory structure (`skillname/SKILL.md`)
- Iron Law (or Key Principles for new_project)
- Gate Function
- Red Flags section
- Rationalization Prevention table
- The Bottom Line closing

## What I Accomplished

- **Phase 11 (pcode)**: Added Iron Law "NO PLAN WITHOUT CODEBASE RESEARCH FIRST", Gate Function, Red Flags, Rationalization Prevention, Bottom Line. Restructured to `pcode/SKILL.md`.

- **Phase 12 (vcode)**: Added two-stage review (Stage 1: Spec Compliance, Stage 2: Code Quality). Iron Law "NO VERDICT WITHOUT FRESH EVIDENCE". Restructured to `vcode/SKILL.md`.

- **Phase 13 (commit)**: Added Iron Law "NO COMMIT WITHOUT STAGED FILE VERIFICATION", focus on never using `git add -A`. Restructured to `commit/SKILL.md`.

- **Phase 14 (pr)**: Added Iron Law "NO PR WITHOUT FULL BRANCH ANALYSIS", emphasis on analyzing ALL commits. Restructured to `pr/SKILL.md`.

- **Phase 15 (handover)**: Added Iron Law "NO HANDOVER WITHOUT KEY LEARNINGS". Restructured to `handover/SKILL.md`.

- **Phase 16 (takeover)**: Added Iron Law "NO WORK WITHOUT STATE VERIFICATION". Restructured to `takeover/SKILL.md`.

- **Phase 17 (new_project)**: Added lighter enforcement (Key Principles, Red Flags, Bottom Line - no Gate Function since interactive). Restructured to `new_project/SKILL.md`.

## Key Learnings

- **Directory format matters**: Skills need `skillname/SKILL.md` format to be recognized as slash commands
- **Enforcement pattern anatomy**: Iron Law → Gate Function → Red Flags → Rationalization Prevention → Bottom Line
- **Two-stage validation is powerful**: vcode's spec compliance THEN code quality catches different issues
- **Spirit vs Letter clause**: Adding this at the top prevents rephrasing bypass
- **new_project is special**: Interactive workflows need lighter enforcement - Key Principles instead of Iron Law

## Files Changed

All skills restructured from flat files to directory format:
- `newskills/pcode/SKILL.md` - planning skill with research enforcement
- `newskills/vcode/SKILL.md` - validation skill with two-stage review
- `newskills/commit/SKILL.md` - commit skill with staged file verification
- `newskills/pr/SKILL.md` - PR skill with full branch analysis
- `newskills/handover/SKILL.md` - handover skill with learnings requirement
- `newskills/takeover/SKILL.md` - takeover skill with state verification
- `newskills/new_project/SKILL.md` - project init with lighter enforcement

Previous flat files deleted: `pcode.md`, `vcode.md`, `commit.md`, `pr.md`, `handover.md`, `takeover.md`, `new_project.md`

## Current State

- All 9 skills (rcode, icode, pcode, vcode, commit, pr, handover, takeover, new_project) enhanced
- All in directory format
- All have enforcement patterns (except new_project has lighter version)
- Changes NOT yet committed

## Next Steps

1. **Update plan checkboxes** - Mark Phases 11-17 as complete in `.docs/plans/01-27-2026-rpi-enforcement-patterns.md`
2. **Commit all changes** - Stage and commit the skill restructuring
3. **Deploy to global config** - `cp -r newskills/* ~/.claude/skills/`
4. **Test each skill** - Run `/pcode`, `/vcode`, `/commit`, `/pr`, `/handover`, `/takeover`, `/new_project` in testbed
5. **Iterate** - Adjust based on friction discovered in real use

## Context & References

- Plan: `.docs/plans/01-27-2026-rpi-enforcement-patterns.md`
- Research: `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md`
- Previous handover: `.docs/handoffs/01-27-2026-rpi-enforcement-patterns.md`

## Notes

- The plan still has unchecked boxes for Phases 11-17 - need to update them
- Consider session-start hook to inject RPI workflow rules (from research Part 6)
- new_project intentionally has no Gate Function - it's an interactive workflow where rigid gates don't fit
