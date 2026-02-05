---
git_commit: 469a6d81ebb8b827e284d4afb090c6c622d97747
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Marked historical - skills renamed since this handover"
topic: "RPI Workflow Enhancement with Superpowers Patterns"
tags: [handover, rpi-workflow, superpowers, enforcement-patterns]
status: historical
archived: 2026-02-05
archive_reason: "Historical handoff from 2026-01-27, superseded by subsequent work. All proposed patterns were implemented across 19 skills. git_commit reference (469a6d8) no longer in local history."
references:
  - .docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md
  - newskills/
  - newagents/
---

# Handover: RPI Workflow Enhancement with Superpowers Patterns

**Date**: 2026-01-27
**Branch**: main

> **Historical Note (2026-02-01)**: Skills referenced in this handover have been renamed:
> - `pcode` -> `planning-codebases`
> - `icode` -> `implementing-plans`
> - `rcode` -> `researching-codebases`
> - `vcode` -> `validating-implementations`
> - `commit` -> `committing-changes`
> - `pr` -> `creating-pull-requests`
> - `handover` -> `handing-over`
> - `takeover` -> `taking-over`
> See `.docs/plans/02-01-2026-skill-structure-updates.md` for the rename plan.

## What I Was Working On

Adapting patterns from the Superpowers Claude Code plugin to enhance our RPI workflow (pcode/icode/rcode/vcode/commit/pr/handover/takeover).

- Research Superpowers patterns: **completed**
- Create implementation plan: **in-progress** (clarifying questions answered, ready to write plan)

## What I Accomplished

1. **Recovered lost agents** from Claude session log at `~/.claude/projects/C--code-humanlayer/6947d63e-f308-4e4b-a9bd-3efccb70d2bb.jsonl`
   - Extracted all 7 agents to `newagents/`
   - Applied 2 fixes from original handover (docs-updater, codebase-pattern-finder)

2. **Comprehensive research** of Superpowers codebase using 5 parallel agents
   - Documented in `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md`
   - ~600 lines of detailed patterns with exact file:line references

3. **Clarified implementation approach** with user:
   - Workflow finishers: All commands except handover/takeover should suggest next step
   - Pattern distribution: Full patterns for pcode/icode/vcode/rcode, lighter for commit/pr
   - Architecture: Keep commands self-contained (don't adopt Superpowers' command→skill separation yet)
   - Scope: Include agent enhancements

## Key Learnings

### Superpowers Core Patterns (from research)

1. **Iron Law** - Single ALL CAPS non-negotiable rule per command
   - `skills/test-driven-development/SKILL.md:31-45`
   - Pattern: Rule + "No exceptions" + specific prohibitions + "Delete means delete"

2. **Gate Function** - Numbered checklist BEFORE any action
   - `skills/verification-before-completion/SKILL.md:24-38`
   - Pattern: IDENTIFY → RUN → READ → VERIFY → ONLY THEN claim

3. **Red Flags** - Warning signs that process is being violated
   - `skills/test-driven-development/SKILL.md:272-288`
   - Include quoted phrases like "I already know this codebase"

4. **Rationalization Table** - Excuse | Reality two-column format
   - `skills/test-driven-development/SKILL.md:256-271`
   - Pre-written rebuttals to common excuses

5. **Two-Stage Review** - Spec compliance THEN code quality (never parallel)
   - `skills/subagent-driven-development/SKILL.md:70-76`
   - Stage 1: Missing? Extra? Wrong?
   - Stage 2: Quality (only after Stage 1 passes)

6. **Spirit vs Letter** - Rephrasing doesn't bypass the rule
   - `skills/verification-before-completion/SKILL.md:128-131`

### Agent Recovery Technique

Session logs are JSONL files at `~/.claude/projects/`. Can extract Write tool calls:
```javascript
// Look for tool_use blocks with name: "Write" and input.file_path containing target
```

## Files Changed

- `newagents/` - All 7 agents recovered and verified
  - `codebase-pattern-finder.md:36` - Fixed "preferred" → "most commonly used"
  - `docs-updater.md:98` - Fixed invalid codebase-analyzer reference
- `newcommands/` - 9 commands copied from `~/.claude/commands/`
- `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md` - Full research document

## Current State

- **Working**: All files in place, research complete
- **Partially done**: Plan clarification complete, ready to write implementation plan
- **Waiting**: User approval on pattern distribution and architecture approach

### Agreed Pattern Distribution

| Command | Iron Law | Gate Function | Red Flags | Rational. Table | Two-Stage | Finisher |
|---------|----------|---------------|-----------|-----------------|-----------|----------|
| pcode | ✓ | ✓ | ✓ | ✓ | - | → icode |
| icode | ✓ | ✓ | ✓ | ✓ | - | → vcode |
| vcode | ✓ | ✓ | ✓ | ✓ | ✓ | → commit/fix |
| rcode | ✓ | ✓ | ✓ | ✓ | - | → pcode/done |
| commit | - | ✓ | ✓ | - | - | → pr |
| pr | - | - | ✓ | - | - | done |

## Next Steps

1. **Get final user approval** on pattern distribution table above
2. **Write implementation plan** to `.docs/plans/01-27-2026-rpi-workflow-enhancement.md`
3. **Implement Phase 1**: Add patterns to pcode (template for others)
4. **Implement remaining phases**: icode, vcode, rcode, commit, pr, agents
5. **Test the enhanced workflow** on a real task

## Context & References

- **Research**: `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md` - ESSENTIAL, has all patterns with exact quotes and file:line refs
- **Superpowers repo**: `C:\code\superpowers\` - The codebase we're learning from
- **Original handover**: `.docs/handoffs/01-27-2026-portable-plugin-system.md` - Where this work originated

## Notes

### Resolved: Skills vs Commands

**Decision**: Use `newskills/` directory structure (not `newcommands/`)

Since we're NOT making a plugin, project-level skills work reliably:
- `.claude/skills/pcode/SKILL.md` → Creates `/pcode`
- Can include supporting files (examples, templates)
- Official recommended approach per [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

The plugin skills bug (Issue #17271) doesn't affect us.

### Open Questions (need user input)

1. Should we create a shared `newskills/enforcement-patterns.md` reference file, or inline patterns in each skill?
   - User leaning toward inline (simpler)
   - Hybrid option: shared reference that skills can `@include`

### Key Insight

Superpowers' power comes from treating process documentation with the same rigor as code:
- Test it with adversarial scenarios
- Track rationalizations as "bugs" and fix them
- Iterate until bulletproof under pressure

### Workflow Finisher Format (proposed)

```markdown
## Next Step

Research complete. Document saved to `.docs/research/[file].md`

**Ready to plan?** Run: `/pcode .docs/research/[file].md`

Or ask follow-up questions if more research is needed.
```
