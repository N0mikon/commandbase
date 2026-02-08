---
date: 2026-02-07
status: complete
topic: "Phase 2 BRDSPI Core (Code Domain) - Pre-Planning Research"
tags: [research, brdspi, designing-code, structuring-code, starting-refactors, planning-code, phase-2]
git_commit: aabffde
last_updated: 2026-02-07
last_updated_by: docs-updater
last_updated_note: "Marked complete — all 6 open questions resolved by Phase 2 implementation. Skills created: designing-code, structuring-code, starting-refactors; planning-code modified."
references:
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/future-skills/rdspi-workflow.md
  - .docs/future-skills/re-evaluate-existing.md
  - newskills/planning-code/SKILL.md
  - newskills/starting-projects/SKILL.md
  - newskills/discussing-features/SKILL.md
  - newskills/researching-code/SKILL.md
  - newskills/designing-code/SKILL.md
  - newskills/structuring-code/SKILL.md
  - newskills/starting-refactors/SKILL.md
---

# Phase 2 BRDSPI Core (Code Domain) - Pre-Planning Research

**Date**: 2026-02-07
**Branch**: master

## Research Question

What does the current codebase look like, what patterns exist, and what decisions have already been made — so that a Phase 2 implementation plan can be written with full context?

## Summary

Phase 2 expands the RPI workflow (Research, Plan, Implement) to BRDSPI (Brainstorm, Research, Design, Structure, Plan, Implement) by adding two new phases (Design and Structure) as skills, creating a brownfield initialization skill, and simplifying the existing `/planning-code` skill. This research documents the current state of all relevant skills, the spec that new skills must follow, the design decisions already captured, and the integration points between skills.

## Scope: 4 Work Items

| Item | Type | Complexity | Key Challenge |
|------|------|-----------|---------------|
| 2a. `/designing-code` | New skill | Medium | Consumes research output, produces design docs, uses opus model |
| 2b. `/structuring-code` | New skill | Medium | Consumes design docs, produces structural maps, heaviest in refactors |
| 2c. `/planning-code` modification | Modify existing | Low | Simplify to receive structural map, maintain backward compat |
| 2d. `/starting-refactors` | New skill | Medium | Brownfield parallel to `/starting-projects`, auto-checkpoints |

## Detailed Findings

### 1. Design Decisions Already Made (from rdspi-workflow.md and roadmap)

These decisions are settled and should NOT be re-debated during planning:

**`/designing-code`:**
- Covers: API shape, pattern selection, trade-off resolution, component boundaries, error handling strategy, state management
- Model: **opus** (design decisions benefit from deeper reasoning)
- Input: research artifacts from `/researching-code`, `/researching-web`, `/researching-frameworks`
- Absorbs from `/discussing-features`: research-informed technical choice questioning (e.g., "what error format?", "auth approach?")
- Output: `.docs/design/` document with rationale and decisions, NO implementation details
- The "what should we build and why this approach" phase

**`/structuring-code`:**
- Covers: file placement, module organization, dependency direction, interface boundaries, test organization
- For refactors: migration order that keeps things working at each step (heaviest phase in brownfield work)
- Input: design doc from `/designing-code`
- Output: structural map document
- The "where does everything go and how does it connect" phase

**`/planning-code` modification:**
- Simplify: no longer does architecture work (that's D+S now)
- Receives structural map as input, focuses purely on atomic task breakdown with success criteria
- **Backward compatible**: if no structural map provided, works as before (for lightweight features that skip D+S)

**`/starting-refactors`:**
- Brownfield parallel to `/starting-projects`
- Establishes refactor scope, snapshots current state, sets up CLAUDE.md context
- Generates initial audit of target area
- **Auto-runs `/bookmarking-code` create** before refactor starts (safety net)
- Then RDSPI runs inside that context

**Open questions resolved in roadmap:**
- `/designing-code` uses opus model: YES (confirmed in roadmap 2a)
- `/starting-refactors` auto-runs checkpoint: YES (confirmed in roadmap 2d)
- Implementation order: Design → Structure → modified Planning → Starting Refactors (dependency chain)

### 2. Skill Specification Format (from /creating-skills)

All Phase 2 skills must follow these constraints:

**Frontmatter:**
```yaml
---
name: skill-name-in-gerund-form
description: "Use this skill when [primary situation]. This includes [specific use case], [another use case], and [edge case]."
---
```

**Naming rules:**
- Pattern: `^[a-z0-9-]+$`, gerund form (verb-ing + noun)
- Must match directory name exactly
- 15-40 characters practical range

**Description rules:**
- Start with "Use this skill when..."
- 200-400 characters target
- Third person voice, no angle brackets
- Cover WHEN to activate, not just WHAT it does

**Structure rules:**
- SKILL.md under 500 lines / 5,000 words (target 200-300 lines)
- Subdirectories: `reference/`, `templates/`, `scripts/`, `assets/`
- Reference nesting max 1 level deep
- No README, CHANGELOG, or extraneous files

**Required sections (from templates):**
1. Title + role statement
2. "Violating the letter..." enforcement line
3. The Iron Law (primary rule)
4. The Gate Function (step-by-step verification)
5. Process steps (skill-specific)
6. Red Flags - STOP and [Action]
7. Rationalization Prevention table
8. The Bottom Line

### 3. Existing Skill Patterns to Follow

**`/researching-code` (233 lines) — pattern for agent-spawning skills:**
- Iron Law: "NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST"
- Gate Function: 7 steps (IDENTIFY → SPAWN → WAIT → VERIFY → SYNTHESIZE → WRITE → PRESENT)
- Spawns parallel Task agents for different research aspects
- Delegates document creation to `docs-writer` agent
- Mandatory `.docs/research/` output file
- Reference files: `research-agents.md` (71 lines), `evidence-requirements.md` (65 lines)
- Template: `research-document-template.md` (85 lines)

**`/planning-code` (275 lines) — the skill being modified:**
- Iron Law: "NO PLAN WITHOUT CODEBASE RESEARCH FIRST"
- Gate Function: 6 steps ending with "ONLY THEN: Write the implementation plan"
- Two modes: A (iterate existing plan) and B (create new plan)
- 5-step process: Context Gathering → Deep Research → Plan Structure Development → Detailed Plan Writing → Review
- Delegates to `docs-writer` agent for plan creation
- Reference files: `research-workflow.md` (127 lines), `common-patterns.md` (58 lines)
- Template: `plan-template.md` (93 lines)
- Interactive: gets buy-in at structure level before writing details

**`/starting-projects` (214 lines) — the greenfield parallel for /starting-refactors:**
- Iron Law: "NO RECOMMENDATION WITHOUT RESEARCH"
- Gate Function: 6 steps (DISCOVER → RESEARCH → SYNTHESIZE → CONFIRM → CREATE → PRESENT)
- Uses AskUserQuestion for interactive discovery (4 rounds of questions)
- Delegates to `/researching-frameworks` for tech stack research
- Creates `.docs/plans/project-setup.md` and minimal CLAUDE.md
- Reference files: `automatic-behaviors.md`, `question-design.md`, `claude-md-guidelines.md`
- Templates: `project-setup-plan-template.md`, `claude-md-template.md`

**`/discussing-features` (188 lines) — being partially absorbed:**
- Iron Law: "CAPTURE HOW PREFERENCES BEFORE RESEARCH"
- Domain detection: visual | api | cli | content | organization
- 4-question rhythm per topic using AskUserQuestion
- Scope guardrail for deferred ideas
- Output: `.docs/context/{feature-name}.md` with XML-tagged sections
- Reference: `question-domains.md` (151 lines) — domain-specific question templates
- Template: `context-template.md` (93 lines)
- Key absorption targets:
  - Research-informed technical choices → `/designing-code`
  - Domain detection + preference questions → `/brainstorming-code` (Phase 4, not Phase 2)

### 4. `/bookmarking-code` Integration (for /starting-refactors)

- Storage: `.claude/checkpoints.log` or `.claude/sessions/{name}/checkpoints.log`
- Format: `YYYY-MM-DD-HH:MM | checkpoint-name | git-sha`
- Create operation: verifies git state, warns about uncommitted changes, logs SHA
- Session-aware: checks `.claude/sessions/_current` for active session
- `/starting-refactors` needs to invoke checkpoint creation as part of initialization
- Pattern: same as `/implementing-plans` which creates mandatory checkpoints after each phase

### 5. Output Artifact Locations

Each new skill produces artifacts in its own `.docs/` subdirectory:

| Skill | Output Location | Purpose |
|-------|----------------|---------|
| `/designing-code` | `.docs/design/` | Design decisions with rationale |
| `/structuring-code` | TBD (structural map) | File placement, module organization |
| `/planning-code` | `.docs/plans/` (unchanged) | Phased implementation tasks |
| `/starting-refactors` | `.docs/` (scope doc) | Refactor scope, baseline, audit |

**Decision needed during planning:** Where does `/structuring-code` output go? Options:
- `.docs/structure/` (new directory, parallel to `.docs/design/`)
- `.docs/plans/` (alongside plans, since structure feeds planning)
- Inline in the design doc (combined D+S output)

**Decision needed:** Where does `/starting-refactors` scope document go? Options:
- `.docs/refactors/` (new directory)
- `.docs/plans/` (as a special plan type)
- `.docs/context/` (reusing discussing-features' output location)

### 6. Workflow Integration Points

**Full BRDSPI chain (greenfield MVP):**
```
/brainstorming-code (Phase 4)
/starting-projects
  R  /researching-frameworks, /researching-web
  D  /designing-code          ← NEW (Phase 2a)
  S  /structuring-code        ← NEW (Phase 2b)
  P  /planning-code           ← MODIFIED (Phase 2c)
  I  /implementing-plans
```

**Full BRDSPI chain (brownfield refactor):**
```
/starting-refactors           ← NEW (Phase 2d) — auto-checkpoint
  R  /researching-code
  D  /designing-code          ← NEW — target architecture, before/after
  S  /structuring-code        ← NEW — migration order (each step deployable)
  P  /planning-code           ← MODIFIED — receives structural map
  I  /implementing-plans
```

**Lightweight feature (backward compat):**
```
  R  /researching-code
  P  /planning-code           ← works standalone, no structural map needed
  I  /implementing-plans
```

### 7. What /discussing-features Contributes to /designing-code

From `/discussing-features`, the following should be absorbed into `/designing-code`:

**Research-informed technical choice questioning:**
- These are questions asked AFTER research has been done, where the user needs to make a technical decision
- Examples: "What error format?", "REST or GraphQL?", "Auth approach?"
- Currently in discussing-features as domain-specific question templates
- Key difference from brainstorming: these questions are informed by codebase research, not exploratory

**What stays with brainstorming (Phase 4, not Phase 2):**
- Domain detection (visual | api | cli | content | organization)
- Preference questions (layout, density, interaction patterns)
- Pre-research exploration

**What `/designing-code` absorbs:**
- The concept of structured questioning for technical choices
- Using AskUserQuestion for design decisions
- The principle of concrete options, not abstract choices
- Capturing rationale alongside decisions

### 8. Model Selection

| Skill | Model | Rationale |
|-------|-------|-----------|
| `/designing-code` | opus | Design decisions benefit from deeper reasoning (confirmed in roadmap) |
| `/structuring-code` | default (sonnet) | Structural mapping is more mechanical than creative |
| `/planning-code` | default (unchanged) | Task breakdown doesn't need opus |
| `/starting-refactors` | default (sonnet) | Initialization workflow, not deep reasoning |

Note: "opus model" in the skill context means the skill should specify that research/design agents spawned via Task tool should use `model: "opus"`.

### 9. Existing .docs/ Infrastructure

Directories that already exist:
- `.docs/research/` — research output (used by /researching-code)
- `.docs/plans/` — implementation plans (used by /planning-code)
- `.docs/handoffs/` — session handovers
- `.docs/learnings/` — pattern extraction
- `.docs/future-skills/` — concept backlog
- `.docs/references/` — architecture decisions
- `.docs/context/` — feature context docs (from /discussing-features)
- `.docs/archive/` — superseded documents

Directories that would be new:
- `.docs/design/` — design decisions (for /designing-code)
- `.docs/structure/` — structural maps (for /structuring-code, if separate)
- `.docs/refactors/` — refactor scope docs (for /starting-refactors, if separate)

### 10. Dependencies and Build Order

```
2a. /designing-code       ← build first (no skill dependencies, only needs spec format)
     |
2b. /structuring-code     ← build second (references design doc as input)
     |
2c. /planning-code mod    ← build third (needs to accept structural map)
     |
2d. /starting-refactors   ← build last (references all three + /bookmarking-code)
```

Each can be built and deployed independently, but testing the full chain requires all four.

## Code References

- `newskills/planning-code/SKILL.md` — Current planning skill (275 lines), will be modified in 2c
- `newskills/planning-code/reference/research-workflow.md` — Research process (127 lines), pattern for /designing-code
- `newskills/planning-code/reference/common-patterns.md` — Implementation patterns (58 lines)
- `newskills/planning-code/templates/plan-template.md` — Plan output template (93 lines)
- `newskills/starting-projects/SKILL.md` — Greenfield init (214 lines), pattern for /starting-refactors
- `newskills/starting-projects/reference/question-design.md` — Question design patterns (56 lines)
- `newskills/starting-projects/templates/project-setup-plan-template.md` — Setup plan template (103 lines)
- `newskills/discussing-features/SKILL.md` — Feature discussion (188 lines), partially absorbed by 2a
- `newskills/discussing-features/reference/question-domains.md` — Domain question templates (151 lines)
- `newskills/discussing-features/templates/context-template.md` — Context doc template (93 lines)
- `newskills/researching-code/SKILL.md` — Research skill (233 lines), agent-spawning pattern
- `newskills/researching-code/reference/research-agents.md` — Agent catalog (71 lines)
- `newskills/researching-code/reference/evidence-requirements.md` — Evidence standards (65 lines)
- `.docs/future-skills/rdspi-workflow.md` — RDSPI concept document (blueprint for Phase 2)
- `.docs/future-skills/re-evaluate-existing.md` — Triage decisions (docs-updater expansion notes)
- `.docs/references/architecture-decisions.md` — ADRs (skill format, hooks, commit enforcement)

## Architecture Notes

### Pattern: Skill Chain with Artifact Handoff

The BRDSPI chain follows a consistent pattern: each skill consumes the previous skill's artifact and produces its own. This is the core architectural principle:

```
Research artifact → /designing-code → Design doc
Design doc → /structuring-code → Structural map
Structural map → /planning-code → Implementation plan
Implementation plan → /implementing-plans → Code changes
```

Each handoff point is a `.docs/` document that serves as a compaction boundary — the downstream skill reads a compact artifact rather than needing the full context of the upstream skill's work.

### Pattern: Backward Compatibility via Optional Input

`/planning-code` must accept structural maps when provided but work standalone when not. This pattern is: check if the input artifact exists, use it if present, skip if absent. The skill's Iron Law and Gate Function remain unchanged — the modification is additive (new input source) not destructive (changed behavior).

### Pattern: Pre-Work Safety Net

`/starting-refactors` establishes a safety net before any changes begin. This mirrors `/implementing-plans`' mandatory checkpoints but at the workflow level rather than the phase level. The checkpoint must be created BEFORE any research or design work begins, capturing the pristine pre-refactor state.

### Naming Convention Compliance

All Phase 2 skills follow the established `verb-domain` naming pattern:
- `designing-code` (gerund + domain)
- `structuring-code` (gerund + domain)
- `starting-refactors` (gerund + activity — exception: "refactors" is the activity being started, not a domain)

## Open Questions (All Resolved)

All 6 open questions have been resolved by the Phase 2 implementation.

1. **Output location for `/structuring-code`**: RESOLVED -- `.docs/structure/`. The skill's Gate Function step 6 writes to `.docs/structure/`, and the structural-map-template.md confirms this location. Clean separation was chosen as recommended.

2. **Output location for `/starting-refactors`**: RESOLVED -- `.docs/refactors/`. The skill's Gate Function step 5 writes to `.docs/refactors/`, and the refactor-scope-template.md confirms this location. Distinct from plans and context docs as recommended.

3. **How does `/designing-code` integrate AskUserQuestion for technical choices?** RESOLVED -- inline during the design process. Step 3 ("Design with Inline Questioning") in the SKILL.md asks questions as they arise per design domain, not in a dedicated questioning step. The Gate Function lists this as step 3: "QUESTION: Ask technical choice questions inline as they arise (AskUserQuestion)."

4. **Should `/structuring-code` run `docs-updater` on existing research/plan docs that structural changes would invalidate?** RESOLVED -- deferred. The implemented `/structuring-code` skill does not trigger docs-updater. This was not included in Phase 2 scope; it remains a candidate for future enhancement as noted in `re-evaluate-existing.md`.

5. **Template format for design docs and structural maps**: RESOLVED -- templates created in each skill. `/designing-code` has `templates/design-document-template.md` with sections: Design Context, Decisions (per domain with rationale and alternatives), Claude's Discretion, Constraints Discovered, Out of Scope, Next Steps. `/structuring-code` has `templates/structural-map-template.md` with sections: Design Reference, Current Structure, Proposed Structure, New/Modified/Removed Files, Module Boundaries, Test Organization, Migration Order (refactors only), Conventions Followed, Next Steps.

6. **How opinionated should `/structuring-code` be about directory conventions vs deferring to existing patterns?** RESOLVED -- defers to existing patterns in brownfield, proposes conventions for greenfield. The SKILL.md Step 3 states: "For brownfield work: follow existing patterns. Do not propose new conventions." and "For greenfield: propose conventions and confirm with user via AskUserQuestion." The Bottom Line reinforces: "Defer to existing patterns in brownfield."
