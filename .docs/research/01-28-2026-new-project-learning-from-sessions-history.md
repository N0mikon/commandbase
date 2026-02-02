---
git_commit: 22359f4
last_updated: 2026-01-28
last_updated_by: learning-from-sessions
topic: "History of /new_project and /learning-from-sessions Creation"
tags: [research, starting-projects, learning-from-sessions, learn, newreferences, pattern-learning]
status: resolved
resolution: "/new_project renamed to /starting-projects with proper structure (reference/, templates/)"
references:
  - .docs/handoffs/01-28-2026-pattern-learning-research.md
  - .docs/plans/01-28-2026-automatic-pattern-learning.md
  - .docs/plans/learning-from-sessions-blueprint.md
  - .docs/research/01-28-2026-learning-from-sessions-blueprint.md
  - newskills/starting-projects/SKILL.md
  - newskills/learning-from-sessions/SKILL.md
  - newreferences/pattern-learning.md
---

# Research: History of /new_project and /learning-from-sessions Creation

**Date**: 2026-01-28
**Branch**: master

## Research Question

How were `/new_project` and `/learning-from-sessions` created and how do they relate? Also: items in `newreferences/` that should have gone into `new_project/references/` instead.

## Summary

The `/new_project` skill was created first as a standalone SKILL.md (`newskills/new_project/SKILL.md`, 404 lines). Later, a session researched the `everything-claude-code` repo for enhancement ideas, which led to a 5-phase plan for "automatic pattern learning." That plan created the `/learn` skill AND 3 reference docs in `newreferences/`. A subsequent session then designed `/learning-from-sessions` as a more comprehensive replacement for `/learn`, with its own `reference/` subdirectory containing 4 files. The 3 files in `newreferences/` were created as **global reference documents** for `~/.claude/reference/` deployment -- but 2 of them (`pattern-learning.md` and `automatic-behaviors.md`) are functionally scoped to the pattern learning workflow and arguably belong inside skill-specific `reference/` directories rather than as global references.

## Detailed Findings

### 1. The Timeline

**Session A** (01-27-2026): Created `/new_project` skill
- Built `newskills/new_project/SKILL.md` (404 lines)
- Standalone skill for greenfield project initialization
- Already included CLAUDE.md best practices (under 60 lines, progressive disclosure)
- No `references/` subdirectory -- everything is in SKILL.md itself

**Session B** (01-28-2026): Researched `everything-claude-code` repo
- Analyzed 16 skills, 23 commands, 12 agents from that repo
- Identified 6 patterns worth adopting, prioritized into High/Medium/Low
- Created the 5-phase plan: `.docs/plans/01-28-2026-automatic-pattern-learning.md`
- This plan explicitly links `/new_project` and `/learn` together in Phase 3

**Session B continued**: Implemented the 5-phase plan
- **Phase 1**: Created `newreferences/` directory with 3 files (see Section 3 below)
- **Phase 2**: Created `newskills/learn/SKILL.md` (172 lines)
- **Phase 3**: Updated `/new_project` SKILL.md to include "Automatic Behaviors" section in its CLAUDE.md template (`newskills/new_project/SKILL.md:282-284`)
- **Phase 4**: Updated commandbase's own `CLAUDE.md` with automatic behaviors section
- **Phase 5**: Deploy instructions (not executed)

**Session C** (01-28-2026): Designed `/learning-from-sessions` as `/learn` replacement
- Researched Claudeception + Claude-Reflect repos for deeper patterns
- Created blueprint: `.docs/plans/learning-from-sessions-blueprint.md` (258 lines)
- Blueprint designed `learning-from-sessions` with its OWN `reference/` subdirectory (4 files)
- This skill was then built: `newskills/learning-from-sessions/` (6 files, 773 total lines)

### 2. How /new_project Connects to /learning-from-sessions

The connection is through the **automatic pattern learning plan** (`.docs/plans/01-28-2026-automatic-pattern-learning.md`).

**Phase 3 of that plan** (`01-28-2026-automatic-pattern-learning.md:390-461`) specifies:
- Create `newreference/automatic-behaviors.md` (reference doc for the behavior)
- Update `/new_project`'s CLAUDE.md template to include an "Automatic Behaviors" section
- The template at `newskills/new_project/SKILL.md:282-284` now generates CLAUDE.md files that include:
  ```
  ## Automatic Behaviors
  When I mention a repeat problem ("this happened before", "same issue again", etc.),
  offer to save the solution as a learned pattern to ~/.claude/skills/learned/.
  ```

So `/new_project` generates CLAUDE.md files that trigger the pattern learning behavior, and `/learning-from-sessions` (or its predecessor `/learn`) is the skill that handles the actual extraction.

### 3. The `newreferences/` Files and Where They Should Live

Three files exist in `newreferences/`:

| File | Lines | Content | Created By |
|------|-------|---------|------------|
| `pattern-learning.md` | 56 | What makes a good pattern, categories, file format, trigger phrases, storage location | Phase 1 of automatic-pattern-learning plan |
| `claude-md-guidelines.md` | 61 | CLAUDE.md best practices from Kyle's article -- principles, template, what NOT to include | Phase 1 of automatic-pattern-learning plan |
| `automatic-behaviors.md` | 37 | Pattern learning detection triggers and response template | Phase 3 of automatic-pattern-learning plan |

**The plan's intent** (`01-28-2026-automatic-pattern-learning.md:56-64`):
> Phase 1: Create Reference Folder Structure
> Establish `newreference/` in commandbase for reference documents, deployable to `~/.claude/reference/`.

These were designed as **global reference documents** to deploy to `~/.claude/reference/` for progressive disclosure -- Claude reads them on-demand rather than having them always in context.

**What actually happened afterward**: The `learning-from-sessions` skill was created with its OWN `reference/` subdirectory containing 4 files:
- `reference/extraction-workflow.md` (121 lines)
- `reference/quality-gates.md` (109 lines)
- `reference/description-optimization.md` (103 lines)
- `reference/research-foundations.md` (64 lines)

### 4. The Overlap / Misplacement Analysis

**`newreferences/pattern-learning.md`** (56 lines):
- Content: What makes a good pattern, categories, file format, trigger phrases, storage
- Overlap with: `newskills/learning-from-sessions/reference/quality-gates.md` (worth assessment criteria, anti-patterns) and `newskills/learning-from-sessions/reference/extraction-workflow.md` (the extraction process)
- **Verdict**: This is pattern learning reference material. It was created for the simpler `/learn` skill before `learning-from-sessions` existed. Now that `learning-from-sessions` has its own `reference/` directory with more comprehensive versions of this content, `pattern-learning.md` is either redundant or should be folded into `learning-from-sessions/reference/`

**`newreferences/automatic-behaviors.md`** (37 lines):
- Content: Trigger phrases for pattern detection, response template
- Used by: `/new_project`'s CLAUDE.md template references this concept (but doesn't point to this file)
- **Verdict**: This describes a behavior that `/new_project` bakes into generated CLAUDE.md files. It could live in `newskills/new_project/references/` as supporting context for that skill. Alternatively, it stays global if other skills also need it.

**`newreferences/claude-md-guidelines.md`** (61 lines):
- Content: CLAUDE.md authoring best practices from Kyle's article
- Used by: `/new_project` Phase 4 generates CLAUDE.md files following these principles
- **Verdict**: This IS genuinely global -- it applies to any skill or workflow that generates CLAUDE.md files. It makes sense as a global reference document at `~/.claude/reference/`. However, `/new_project` could also reference it from its own `references/` directory.

### 5. Current State of /new_project

`newskills/new_project/SKILL.md` (404 lines) has NO `references/` subdirectory. The skill is entirely self-contained in one file. It references concepts from `newreferences/` implicitly (CLAUDE.md principles, automatic behaviors) but does not point to those files.

The skill structure:
```
newskills/new_project/
└── SKILL.md         # 404 lines, everything inline
```

Compare with `learning-from-sessions`:
```
newskills/learning-from-sessions/
├── SKILL.md                           # 299 lines (core workflow)
├── reference/
│   ├── extraction-workflow.md         # 121 lines
│   ├── quality-gates.md              # 109 lines
│   ├── description-optimization.md   # 103 lines
│   └── research-foundations.md        # 64 lines
└── templates/
    └── extracted-skill-template.md    # 77 lines
```

## Code References

- `newskills/new_project/SKILL.md:1-404` - Full /new_project skill definition
- `newskills/new_project/SKILL.md:282-284` - Automatic behaviors section in CLAUDE.md template
- `newskills/new_project/SKILL.md:239-244` - CLAUDE.md principles (under 60 lines, progressive disclosure)
- `.docs/plans/01-28-2026-automatic-pattern-learning.md:56-64` - Phase 1: newreference/ creation rationale
- `.docs/plans/01-28-2026-automatic-pattern-learning.md:390-461` - Phase 3: /new_project CLAUDE.md template update
- `.docs/plans/01-28-2026-automatic-pattern-learning.md:439-456` - Phase 3: automatic-behaviors.md creation
- `.docs/plans/learning-from-sessions-blueprint.md:71-83` - learning-from-sessions proposed structure with reference/
- `.docs/handoffs/01-28-2026-pattern-learning-research.md:71-74` - Reference folder pattern decision
- `.docs/handoffs/01-28-2026-pattern-learning-research.md:76-80` - /new_project already follows best practices
- `.docs/research/01-28-2026-learning-from-sessions-blueprint.md:218-233` - learn vs learning-from-sessions comparison
- `newreferences/pattern-learning.md:1-56` - Pattern learning guidelines (global reference)
- `newreferences/claude-md-guidelines.md:1-61` - CLAUDE.md guidelines (global reference)
- `newreferences/automatic-behaviors.md:1-37` - Automatic behaviors reference (global reference)
- `newskills/learning-from-sessions/SKILL.md:1-299` - Full learning-from-sessions skill
- `newskills/learning-from-sessions/reference/extraction-workflow.md:1-121` - Extraction workflow reference
- `newskills/learning-from-sessions/reference/quality-gates.md:1-109` - Quality gates reference

## Architecture Notes

### The Reference Doc Placement Pattern

The commandbase project uses two patterns for reference documents:

1. **Global references** (`newreferences/` → `~/.claude/reference/`): Documents applicable across all skills and projects. Claude Code loads these on-demand via progressive disclosure.

2. **Skill-local references** (`newskills/[skill]/reference/`): Documents specific to one skill's workflow. Loaded when that skill activates.

The 5-phase plan created `newreferences/` before `learning-from-sessions` existed. When `learning-from-sessions` was later designed, it created its own `reference/` directory with more comprehensive content. This left the `newreferences/` files as partially redundant -- they serve the simpler `/learn` skill but overlap with `learning-from-sessions/reference/`.

### The Skill Evolution Chain

```
/learn (172 lines, manual pattern extraction)
   ↓ superseded by
/learning-from-sessions (773 lines across 6 files, comprehensive extraction workflow)
   ↑ also enhances
/new_project (generates CLAUDE.md with automatic behavior triggers)
```

## Resolution (2026-01-28)

The open questions were resolved by restructuring `/new_project` → `/starting-projects`:

**Renamed**: `new_project` → `starting-projects` (gerund form per naming conventions, no underscores)

**New structure**:
```
newskills/starting-projects/
├── SKILL.md                              # 184 lines (trimmed from 404)
├── reference/
│   ├── claude-md-guidelines.md           # moved from newreferences/
│   ├── automatic-behaviors.md            # moved from newreferences/
│   └── question-design.md               # extracted from old SKILL.md
└── templates/
    ├── claude-md-template.md             # extracted from old SKILL.md
    └── project-setup-plan-template.md    # extracted from old SKILL.md
```

**Frontmatter fixed**: Added `name: starting-projects`, removed invalid `model: opus`

**newreferences/ cleanup**:
- `claude-md-guidelines.md` → moved to `starting-projects/reference/`
- `automatic-behaviors.md` → moved to `starting-projects/reference/`
- `pattern-learning.md` → left in place (redundant with `learning-from-sessions/reference/quality-gates.md`, separate cleanup)

**Open questions resolved**:
1. ✅ Moved both files into skill-local `reference/` directory
2. ✅ Skill now has `reference/` and `templates/` subdirectories
3. ⏳ `/learn` status still TBD
4. ✅ `claude-md-guidelines.md` now lives in the skill that uses it

---

## Original Open Questions (Historical)

1. **Should `newreferences/pattern-learning.md` and `automatic-behaviors.md` move into `newskills/new_project/references/`?** They were created as global refs but their content is primarily consumed by the pattern learning workflow and /new_project respectively.

2. **Should `/new_project` get a `references/` subdirectory?** At 404 lines, SKILL.md is long. The CLAUDE.md guidelines and automatic behaviors content could be extracted into reference files for progressive disclosure, matching the pattern used by `learning-from-sessions`.

3. **Is `/learn` still needed?** Now that `learning-from-sessions` exists with a superset of functionality, `/learn` may be redundant. The handoff doesn't address this explicitly.

4. **Should `claude-md-guidelines.md` stay global?** It's the most defensibly "global" of the three -- any skill that generates CLAUDE.md files could reference it. But currently only `/new_project` uses those principles.
