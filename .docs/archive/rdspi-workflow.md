---
archived: 2026-02-07
archive_reason: "Concept fully implemented as Phase 2 BRDSPI Core. All proposed skills deployed: /designing-code (192 lines), /structuring-code (195 lines), /starting-refactors (179 lines), /planning-code modified (299 lines), docs-writer extended with 3 new doc_types. Superseded by actual skill files and implementation plan."
original_location: .docs/future-skills/rdspi-workflow.md
superseded_by:
  - newskills/designing-code/SKILL.md
  - newskills/structuring-code/SKILL.md
  - newskills/starting-refactors/SKILL.md
  - newskills/planning-code/SKILL.md
  - .docs/plans/02-07-2026-phase-2-brdspi-core-implementation.md
---

# RDSPI Workflow Evolution

## Problem

The current RPI skills (research, plan, implement) force a conceptual jump between "I understand what exists" and "here are the exact steps." In practice:

- `/planning-code` simultaneously makes architectural decisions *and* breaks them into tasks — two kinds of thinking forced into one phase
- `/researching-code` gets invoked twice — once for discovery, once to figure out structure — because there's no dedicated phase for either
- The workflow works but feels clunky and overloads each phase

## Concept

Expand RPI into RDSPI — Research, Design, Structure, Plan, Implement. Two new phases split out the work currently crammed into Plan and hacked through extra Research passes. Each phase produces a compacted artifact (~200 lines) that feeds the next, adding two more compaction points that keep context under the "dumb zone" threshold.

## New Skills

### `/designing-code`

The "what should we build and why this approach" phase:

- API shape — endpoints, function signatures, data contracts
- Pattern selection — event-driven vs polling, inheritance vs composition, reuse vs introduce
- Trade-off resolution — performance vs readability, flexibility vs simplicity
- Component boundaries — units of work, what talks to what
- Error handling strategy — what fails, how it recovers, what the user sees
- State management — where data lives, how it flows, what's cached
- **Artifact:** Design doc capturing decisions and rationale, no implementation details

### `/structuring-code`

The "where does everything go and how does it connect" phase:

- File placement — which files to create, modify, or split
- Module/directory organization — where new code lives relative to existing
- Dependency direction — what imports what, circular dependency avoidance
- Interface boundaries — public vs internal, where the seams are
- Test organization — where tests go, what kind (unit/integration/e2e) per component
- For refactors: migration order that keeps things working at each step
- **Artifact:** Structural map giving Plan phase a clear skeleton

### `/starting-refactors`

Brownfield parallel to `/starting-projects`. Initializes a refactor context:

- Establish scope and goals in a `.docs/` artifact
- Snapshot current state (ties into `/checkpoint create`)
- Set up CLAUDE.md context pointers for the target area
- Generate initial audit of what's being refactored
- Then RDSPI runs inside that context

## Modified Existing Skills

### `/starting-projects` — unchanged

Stays as pre-RDSPI workspace setup (CLAUDE.md, .gitignore, `.docs/`, scaffold). It's infrastructure, not a design phase. RDSPI runs inside the workspace it creates.

### `/planning-code` — simplified

No longer has to figure out "where things go" — receives a structural map as input. Focuses purely on atomic task breakdown with success criteria.

## Complete Workflows

### Greenfield Project MVP

```
/brainstorming-code          <- explore ideas, settle on direction
/starting-projects           <- workspace setup, CLAUDE.md configured
  R  /researching-frameworks, /researching-web
  D  /designing-code         <- architecture decisions for full MVP
  S  /structuring-code       <- file map, module boundaries
  P  /planning-code          <- full MVP task breakdown, phased
  I  /implementing-plans
```

### Greenfield Project — Phase by Phase

**Outer loop (once):**
```
/brainstorming-code
/starting-projects
  R  /researching-frameworks, /researching-web
  D  /designing-code         <- full MVP architecture
  S  /structuring-code       <- full project scaffold
  P  /planning-code          <- break MVP into phases
```

**Inner loop (per phase, separate session each):**
```
/naming-session "mvp-phase-1-auth"
  R  /researching-code       <- scoped to phase plan + current state
  D  /designing-code         <- decisions specific to this phase
  S  /structuring-code       <- which files change/create for this phase
  P  /planning-code          <- tasks for this phase only
  I  /implementing-plans
/handing-over
```

### Brownfield Project — Refactor

```
/starting-refactors          <- scope defined, baseline captured
  R  /researching-code       <- deep audit of target area
  D  /designing-code         <- target architecture, before/after comparison
  S  /structuring-code       <- migration order (each step stays deployable)
  P  /planning-code          <- atomic tasks, each ends with green tests
  I  /implementing-plans
```

### Brownfield Project — New Feature

```
/brainstorming-code          <- optional, skip if feature is well-defined
  R  /researching-code       <- scoped to what the feature touches
  D  /designing-code         <- how it fits existing architecture (often lightweight)
  S  /structuring-code       <- which files change, where new code goes (often lightweight)
  P  /planning-code
  I  /implementing-plans
```

## Phase Weight by Workflow

| Workflow | Brainstorm | Init | R | D | S | P | I |
|---|---|---|---|---|---|---|---|
| Greenfield MVP | Heavy | `/starting-projects` | Heavy | Heavy | Heavy | Heavy | Heavy |
| Greenfield Phase | -- | `/naming-session` | Light | Medium | Light | Medium | Heavy |
| Brownfield Refactor | -- | `/starting-refactors` | Heavy | Medium | **Heavy** | Medium | Heavy |
| Brownfield New Feature | Optional | -- | Light | Light | Light | Light | Medium |

Refactors shift weight into Structure because the hard problem is sequencing change, not deciding what to build. Brownfield features are lightest because most decisions are already made by the existing codebase.

## Open Questions

- Should `/designing-code` use a reasoning model (like the current Plan phase suggests) or stay with the default?
- How opinionated should `/structuring-code` be about directory conventions vs deferring to existing patterns?
- Should `/starting-refactors` auto-run `/checkpoint create` as part of init?
- Implementation order — build Design and Structure skills first, then update existing skills, then add domain variants?
