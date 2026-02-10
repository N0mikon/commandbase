---
date: 2026-02-07
status: archived
archived: 2026-02-09
archive_reason: "Plan fully implemented in commit 3c993c9. All referenced newskills/* and newagents/* paths migrated to plugins/ in commit 87a19a3. Skills designing-code, structuring-code, and starting-refactors shipped under plugins/commandbase-code/skills/."
topic: "Phase 2 BRDSPI Core Implementation"
tags: [plan, brdspi, designing-code, structuring-code, starting-refactors, planning-code, phase-2]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived after 18 commits behind HEAD. Plan complete, all newskills/newagents references now in plugins/."
references:
  - .docs/research/02-07-2026-phase-2-brdspi-core-research.md
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/future-skills/rdspi-workflow.md
  - plugins/commandbase-code/agents/docs-writer.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-core/skills/starting-projects/SKILL.md
  - plugins/commandbase-code/skills/designing-code/SKILL.md
  - plugins/commandbase-research/skills/researching-code/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
---

# Phase 2 BRDSPI Core Implementation Plan

## Overview

Expand the RPI workflow (Research, Plan, Implement) to full BRDSPI (Brainstorm, Research, Design, Structure, Plan, Implement) for the code domain. This adds two new workflow phases (Design and Structure) as skills, creates a brownfield initialization skill, modifies the existing planning skill, and extends the docs-writer agent to support new artifact types.

## Current State Analysis

The current workflow has three phases with dedicated skills:
- **R**: `/researching-code` (233 lines), `/researching-web`, `/researching-frameworks`
- **P**: `/planning-code` (275 lines) — currently handles both architecture decisions AND task breakdown
- **I**: `/implementing-plans` — executes plans with mandatory checkpoints

The gap: `/planning-code` is overloaded. It simultaneously makes architectural decisions AND breaks them into tasks — two kinds of thinking forced into one phase. Research gets invoked twice (once for discovery, once to figure out structure) because there's no dedicated phase for either.

### Key Discoveries:
- `docs-writer` agent (`newagents/docs-writer.md:63-69`) only supports 5 doc_types: research, plan, handoff, reference, debug — needs 3 new types
- `/planning-code` Mode B (`SKILL.md:79-82`) reads input files and begins research — needs to detect structural maps
- `/implementing-plans` checkpoint pattern (`SKILL.md:86,171-175`) checks `.claude/sessions/_current` then runs `/bookmarking-code create` — pattern for `/starting-refactors`
- `/discussing-features` question domains (`reference/question-domains.md`) — technical choice patterns absorbed into `/designing-code`
- `/starting-projects` gate function (`SKILL.md`) uses DISCOVER → RESEARCH → SYNTHESIZE → CONFIRM → CREATE → PRESENT — pattern for `/starting-refactors`

## Desired End State

After this plan is complete:
1. `/designing-code` skill deployed — consumes research artifacts, produces `.docs/design/` documents with rationale, uses opus model
2. `/structuring-code` skill deployed — consumes design docs, produces `.docs/structure/` structural maps
3. `/planning-code` modified — accepts optional structural map input, works standalone for lightweight features
4. `/starting-refactors` skill deployed — initializes brownfield refactors with auto-checkpoint and scope docs
5. `docs-writer` agent extended — supports `design`, `structure`, and `refactor` doc_types
6. Full BRDSPI chain tested end-to-end

### Verification:
- Each skill passes `/auditing-skills` validation
- Each skill produces its expected `.docs/` artifact when invoked
- `/planning-code` backward compatibility confirmed (works without structural map)
- Full chain: `/designing-code` → `/structuring-code` → `/planning-code` → `/implementing-plans` produces valid phased plan from design input
- `/starting-refactors` creates checkpoint and scope doc before any design/research begins

## What We're NOT Doing

- Phase 4 brainstorming skills (`/brainstorming-code`, `/brainstorming-vault`, `/brainstorming-services`) — depends on this phase
- Retiring `/discussing-features` — that's Phase 4d, after brainstorming absorbs its remaining functionality
- Vault or Services BRDSPI variants (Phases 6, 7) — depends on proven code domain patterns
- `docs-updater` trigger expansion for `/structuring-code` — deferred to incremental addition later
- Renaming `/validating-code` or `/reviewing-changes` — deferred to Phase 6/7

## Implementation Approach

Build in dependency order: docs-writer extension first (all skills need it), then each skill with its templates as a unit, then modify existing planning skill, then integration test. Each phase is independently deployable and testable.

---

## Phase 1: Extend docs-writer Agent

### Overview
Add three new doc_types to the docs-writer agent so that `/designing-code`, `/structuring-code`, and `/starting-refactors` can delegate document creation.

### Changes Required:

#### 1. docs-writer agent definition
**File**: `newagents/docs-writer.md`

**Change A — Update enum constraint (line 32 area):**
Add `design`, `structure`, `refactor` to the list of valid doc_types.

**Change B — Update validation count (line 44 area):**
Change "5 valid types" to "8 valid types".

**Change C — Add directory mapping rows (lines 63-69 area):**
Add to the mapping table:

```
| design    | .docs/design/    | draft   |
| structure | .docs/structure/ | draft   |
| refactor  | .docs/refactors/ | active  |
```

#### 2. Deploy to global
**File**: `~/.claude/agents/docs-writer.md`
Copy updated agent definition to global config.

### Success Criteria:
- [x] `newagents/docs-writer.md` contains 8 doc_types in enum, validation, and mapping table
- [x] `~/.claude/agents/docs-writer.md` matches repo version
- [x] Verify by reading the file and confirming all 8 types are present

---

## Phase 2: Create /designing-code Skill

### Overview
Create the Design phase skill that produces architectural decision documents. This is the "what should we build and why this approach" phase, sitting between Research and Structure in the BRDSPI chain.

### Changes Required:

#### 1. Skill directory and SKILL.md
**Directory**: `newskills/designing-code/`
**File**: `newskills/designing-code/SKILL.md`

**Frontmatter:**
```yaml
---
name: designing-code
description: "Use this skill when making architectural decisions for a feature or system. This includes choosing API shapes, selecting patterns, resolving trade-offs, defining component boundaries, deciding error handling strategies, and making state management choices. Activate when the user says 'design this', 'architecture decisions', 'how should this be structured', or after completing research with /researching-code."
---
```

**Iron Law:** `NO DESIGN WITHOUT RESEARCH ARTIFACTS FIRST`

Design decisions must be grounded in codebase research. If no research artifacts exist, redirect to `/researching-code` first.

**Gate Function:**
```
BEFORE writing any design document:

1. READ: Find and read research artifacts (.docs/research/) relevant to this task
2. ANALYZE: Identify design decisions that need to be made
3. QUESTION: Ask technical choice questions inline as they arise (AskUserQuestion)
4. DESIGN: Spawn opus-model agents to reason through architecture
5. WRITE: Create .docs/design/ document via docs-writer
6. PRESENT: Summary to user with decision list and link to design doc

Skipping steps = designing blind
```

**Process Steps:**

**Step 1: Locate Research Artifacts**
- Check for research files mentioned by user or recently created in `.docs/research/`
- Read ALL relevant research artifacts FULLY
- If no research artifacts exist, STOP — tell user to run `/researching-code` first
- Also check `.docs/context/` for any feature context from `/discussing-features`

**Step 2: Identify Design Decisions**
- Analyze research findings to determine what architectural decisions are needed
- Categorize by design domain:
  - API shape — endpoints, function signatures, data contracts
  - Pattern selection — event-driven vs polling, inheritance vs composition
  - Trade-off resolution — performance vs readability, flexibility vs simplicity
  - Component boundaries — units of work, what talks to what
  - Error handling strategy — what fails, how it recovers, what the user sees
  - State management — where data lives, how it flows, what's cached
- Present decision topics to user for confirmation

**Step 3: Design with Inline Questioning**
- For each design domain, spawn an opus-model Task agent to analyze options
- When a decision point requires user input, use AskUserQuestion with concrete options (not abstract choices)
- Capture rationale alongside each decision
- Key principle from `/discussing-features`: options should be concrete ("Cards", "REST", "JWT") not abstract ("Option A")

**Step 4: Write Design Document**
- Compile all decisions with rationale
- Spawn docs-writer agent with doc_type: "design"
- Design doc must contain NO implementation details — only decisions and rationale
- Include "Claude's Discretion" section for areas user delegated

**Step 5: Present and Suggest Next Step**
```
DESIGN COMPLETE
===============

Design document: .docs/design/MM-DD-YYYY-<topic>.md

Key decisions:
- [Decision 1]
- [Decision 2]
- [Decision 3]

Next: /structuring-code to map file placement and module organization
Or: /planning-code if structure is straightforward
```

**Red Flags:**
- Designing without reading research artifacts first
- Including implementation details (code, specific line changes) in the design doc
- Making decisions without asking user when multiple valid approaches exist
- Skipping inline questions to "move faster"

**Rationalization Prevention:**

| Excuse | Reality |
|--------|---------|
| "The research already decided this" | Research reveals options. Design chooses between them with user. |
| "This is obvious, no question needed" | Obvious to you ≠ obvious to user. Ask. |
| "I'll include implementation hints to help planning" | Design doc is decisions only. Structure and Plan handle the rest. |
| "User said 'you decide' for everything" | Document what you decided and why. Rationale is mandatory. |

**The Bottom Line:**
**Design captures WHY this approach, not HOW to build it.** Decisions with rationale. No implementation details. Every design. Every time.

**Target size:** ~200-250 lines for SKILL.md

#### 2. Reference file: design-domains.md
**File**: `newskills/designing-code/reference/design-domains.md`

Content: Design domain reference covering what each domain entails and example questions for each. Categories:
- API Design — endpoints, response format, versioning, authentication
- Pattern Selection — architectural patterns, data flow, state management
- Error Strategy — failure modes, recovery, user-facing errors
- Component Boundaries — modules, interfaces, dependency direction
- Data & State — storage, caching, data flow, synchronization

Include example AskUserQuestion options for each domain (concrete, not abstract). ~80-100 lines.

#### 3. Template file: design-document-template.md
**File**: `newskills/designing-code/templates/design-document-template.md`

Template structure for `.docs/design/` documents:

```markdown
# [Feature/System] Design Document

## Design Context
[What research informed this design, link to research artifacts]

## Decisions

### [Decision Domain 1: e.g., API Design]
**Decision:** [What was decided]
**Rationale:** [Why this approach over alternatives]
**Alternatives considered:** [What was rejected and why]

### [Decision Domain 2]
...

### Claude's Discretion
[Areas where user delegated decisions, with rationale for choices made]

## Constraints Discovered
[Technical constraints from research that shaped decisions]

## Out of Scope
[Design decisions deferred to later phases or not relevant]

## Next Steps
[Pointer to /structuring-code or /planning-code]
```

~60-70 lines including section guidelines.

### Success Criteria:
- [x] `newskills/designing-code/SKILL.md` exists and passes validation (name matches dir, description starts with "Use this skill when", <500 lines)
- [x] `newskills/designing-code/reference/design-domains.md` exists with domain categories and example questions
- [x] `newskills/designing-code/templates/design-document-template.md` exists with all required sections
- [x] `/auditing-skills` reports no violations for `designing-code`
- [x] Deploy to `~/.claude/skills/designing-code/` and verify skill appears in available skills list

---

## Phase 3: Create /structuring-code Skill

### Overview
Create the Structure phase skill that produces structural maps. This is the "where does everything go and how does it connect" phase, sitting between Design and Plan in the BRDSPI chain.

### Changes Required:

#### 1. Skill directory and SKILL.md
**Directory**: `newskills/structuring-code/`
**File**: `newskills/structuring-code/SKILL.md`

**Frontmatter:**
```yaml
---
name: structuring-code
description: "Use this skill when mapping file placement, module organization, and dependency structure for a feature or refactor. This includes deciding where new files go, how modules connect, what interfaces to define, how tests are organized, and sequencing migrations for brownfield work. Activate when the user says 'structure this', 'where should files go', 'organize the codebase', or after /designing-code."
---
```

**Iron Law:** `NO STRUCTURE WITHOUT UNDERSTANDING WHAT EXISTS`

Structure decisions must be grounded in the actual codebase. Spawn agents to verify current file organization before proposing changes.

**Gate Function:**
```
BEFORE writing any structural map:

1. READ: Find and read design doc (.docs/design/) if available
2. RESEARCH: Spawn agents to map current file organization in target area
3. ANALYZE: Compare design decisions to current structure
4. MAP: Determine file placement, module boundaries, dependency direction
5. SEQUENCE: For refactors, determine migration order (each step deployable)
6. WRITE: Create .docs/structure/ document via docs-writer
7. PRESENT: Summary to user with structural map and link

Skipping steps = structuring blind
```

**Process Steps:**

**Step 1: Gather Context**
- Check for design doc in `.docs/design/` — read FULLY if exists
- If no design doc and user provides requirements directly, proceed (lightweight mode)
- Spawn code-locator agents to map current directory structure in target area

**Step 2: Analyze Current Structure**
- Spawn code-analyzer agents to understand:
  - Current file organization patterns
  - Naming conventions in use
  - Import/dependency patterns
  - Test file placement conventions
  - Module boundary patterns
- For brownfield: identify what exists that must be preserved or migrated

**Step 3: Create Structural Map**
- For each component from the design doc, determine:
  - Which files to create, modify, or split
  - Where new code lives relative to existing
  - Dependency direction (what imports what)
  - Interface boundaries (public vs internal)
  - Test placement (co-located vs separate, unit/integration/e2e)
- For refactors: determine migration order where each step keeps things working
- **Convention deference:** For brownfield work, follow existing patterns. For greenfield, propose conventions and confirm with user.

**Step 4: Write Structural Map**
- Spawn docs-writer agent with doc_type: "structure"
- Include file tree visualization
- Include dependency diagram (text-based)
- For refactors: numbered migration steps

**Step 5: Present and Suggest Next Step**
```
STRUCTURE COMPLETE
==================

Structural map: .docs/structure/MM-DD-YYYY-<topic>.md

Files affected: [count]
New files: [list]
Modified files: [list]
Migration steps: [count, if refactor]

Next: /planning-code to break this into phased implementation tasks
```

**Red Flags:**
- Proposing file structure without researching current patterns
- Ignoring existing conventions in brownfield work
- Including implementation details (actual code) in the structural map
- Creating migration steps that leave the codebase broken between steps

**Rationalization Prevention:**

| Excuse | Reality |
|--------|---------|
| "I know the standard structure for this" | THIS codebase has its own patterns. Research them. |
| "The design doc already specifies structure" | Design says WHAT. Structure says WHERE. Different concerns. |
| "Migration order doesn't matter" | Every step must leave things working. Order is the hard problem. |
| "This is too simple for a structural map" | Simple structures still need documenting for the planning phase. |

**The Bottom Line:**
**Structure captures WHERE everything goes, not WHAT it does.** File placement, module organization, dependency direction. Defer to existing patterns in brownfield. Every structure. Every time.

**Target size:** ~200-250 lines for SKILL.md

#### 2. Reference file: structure-patterns.md
**File**: `newskills/structuring-code/reference/structure-patterns.md`

Content: Common structural patterns to look for and follow. Categories:
- File placement conventions (co-location vs separation)
- Module boundary patterns (barrel exports, feature folders, layer architecture)
- Test organization patterns (co-located, mirror tree, by type)
- Dependency direction rules (inward, layered, clean architecture)
- Migration sequencing patterns (leaf-first, interface-first, strangler fig)

~70-90 lines.

#### 3. Template file: structural-map-template.md
**File**: `newskills/structuring-code/templates/structural-map-template.md`

Template structure for `.docs/structure/` documents:

```markdown
# [Feature/System] Structural Map

## Design Reference
[Link to design doc that informed this structure]

## Current Structure
[Relevant portion of current file tree in target area]

## Proposed Structure
[File tree showing new/modified/removed files]

### New Files
- `path/to/new/file.ext` — [Purpose]

### Modified Files
- `path/to/existing/file.ext` — [What changes and why]

### Removed/Split Files
- `path/to/old/file.ext` → split into [new files]

## Module Boundaries
[Which modules/directories are independent units]
[Dependency direction: what imports what]

## Test Organization
[Where tests go for each component]
[Test types per component (unit/integration/e2e)]

## Migration Order (refactors only)
1. [Step] — [What changes, what still works after]
2. [Step] — [What changes, what still works after]

## Conventions Followed
[Which existing codebase conventions this structure follows]

## Next Steps
[Pointer to /planning-code]
```

~70-80 lines including section guidelines.

### Success Criteria:
- [x] `newskills/structuring-code/SKILL.md` exists and passes validation
- [x] `newskills/structuring-code/reference/structure-patterns.md` exists with pattern categories
- [x] `newskills/structuring-code/templates/structural-map-template.md` exists with all sections
- [x] `/auditing-skills` reports no violations for `structuring-code`
- [x] Deploy to `~/.claude/skills/structuring-code/` and verify skill appears

---

## Phase 4: Modify /planning-code

### Overview
Add optional structural map input to `/planning-code` so it can receive structure from the new S phase, while maintaining full backward compatibility for lightweight features that skip D+S.

### Changes Required:

#### 1. SKILL.md — Mode B input detection
**File**: `newskills/planning-code/SKILL.md`

**Change A — Add structural map detection in Mode B (after line 82):**
Add logic to detect when a structural map (.docs/structure/) is provided or referenced:

```markdown
### Input Detection

When invoked, check for upstream BRDSPI artifacts:
1. If a `.docs/structure/` file is provided or referenced → **Structured mode**: use structural map as skeleton for plan phases
2. If a `.docs/design/` file is provided but no structure → suggest running `/structuring-code` first, but proceed if user prefers
3. If neither → **Standalone mode**: works as before (full research + architecture + planning)
```

**Change B — Modify Step 3: Plan Structure Development (around line 127):**
In Structured mode, the plan outline should derive phases from the structural map's file groups and migration steps, rather than requiring architecture research.

Add after the existing plan structure presentation:

```markdown
**If structural map is available:**
- Derive phase boundaries from the structural map's file groups or migration steps
- Each structural group/migration step becomes a candidate implementation phase
- Focus on: task breakdown, success criteria, verification commands
- Do NOT re-decide architecture — honor the design doc decisions
```

**Change C — Add note about what planning does NOT do in Structured mode:**

```markdown
**In Structured mode, /planning-code does NOT:**
- Re-debate architectural decisions (those are in the design doc)
- Re-organize file placement (that's in the structural map)
- Spawn architecture research agents (structure already provides this)

It DOES still:
- Spawn code-analyzer agents to verify integration points mentioned in the structural map
- Break structural map into atomic, testable implementation phases
- Define success criteria for each phase
- Identify risks and dependencies between phases
```

#### 2. research-workflow.md — Add structural map awareness
**File**: `newskills/planning-code/reference/research-workflow.md`

**Change — Add section after "Read all mentioned files" (around line 14):**

```markdown
### Upstream BRDSPI Artifacts

If structural map or design doc is provided as input:
- Read the structural map FULLY — this replaces architecture research
- Read the referenced design doc FULLY — this provides decision context
- Research scope narrows to: verifying integration points, confirming test patterns, checking for breaking changes
- Do NOT re-research topics already covered in design/structure docs
```

#### 3. Deploy to global
Copy modified files to `~/.claude/skills/planning-code/`.

### Success Criteria:
- [x] `newskills/planning-code/SKILL.md` updated with structural map detection and structured mode
- [x] `newskills/planning-code/reference/research-workflow.md` updated with upstream artifact awareness
- [x] **Backward compat test**: invoke `/planning-code` with a plain task description (no structural map) — should work exactly as before
- [x] **Structured mode test**: invoke `/planning-code` with a `.docs/structure/` file — should derive phases from structural map without re-researching architecture
- [x] Deploy to `~/.claude/skills/planning-code/` and verify both modes work

---

## Phase 5: Create /starting-refactors Skill

### Overview
Create the brownfield initialization skill that establishes refactor scope, creates a safety checkpoint, and generates an initial audit of the target area. This is the brownfield parallel to `/starting-projects`.

### Changes Required:

#### 1. Skill directory and SKILL.md
**Directory**: `newskills/starting-refactors/`
**File**: `newskills/starting-refactors/SKILL.md`

**Frontmatter:**
```yaml
---
name: starting-refactors
description: "Use this skill when initializing a brownfield refactor, establishing refactor scope, or capturing the current state before restructuring existing code. This includes defining refactor goals, snapshotting baseline state via checkpoint, auditing the target area, and setting up CLAUDE.md context pointers. Activate when the user says 'refactor this', 'restructure this code', 'start a refactor', or before running BRDSPI on existing code."
---
```

**Iron Law:** `NO REFACTOR WITHOUT BASELINE FIRST`

A checkpoint must exist before any refactoring work begins. This captures the pristine pre-refactor state for regression detection and rollback.

**Gate Function:**
```
BEFORE any refactor work begins:

1. DISCOVER: What is being refactored and why?
2. CHECKPOINT: Create baseline via /bookmarking-code create (mandatory, not optional)
3. AUDIT: Spawn agents to analyze the target area
4. SCOPE: Define boundaries — what changes, what doesn't
5. WRITE: Create .docs/refactors/ scope document via docs-writer
6. PRESENT: Summary with scope doc link and next steps

Skipping the checkpoint = refactoring without a safety net
```

**Process Steps:**

**Step 1: Discover Refactor Scope**
- If target area provided, confirm scope with user
- If no target provided, ask via AskUserQuestion:
  - What area of the codebase?
  - What's the goal? (performance, readability, modularity, migration, etc.)
  - What's the trigger? (tech debt, new requirements, scaling issues, etc.)
- Read the target area files to understand current state

**Step 2: Create Baseline Checkpoint (MANDATORY)**
- Check session awareness: read `.claude/sessions/_current` if exists
- Run `/bookmarking-code create "pre-refactor-<area>"` (session-aware)
- This is NOT optional — same enforcement pattern as `/implementing-plans` phase checkpoints
- If uncommitted changes exist, warn user and ask to commit first
- Checkpoint must complete successfully before proceeding

**Step 3: Audit Target Area**
- Spawn parallel research agents:
  - code-locator: find all files in the target area
  - code-analyzer: understand current architecture, patterns, dependencies
  - code-librarian: find tests covering the target area
- Wait for ALL agents to complete
- Compile: file count, line count, dependency map, test coverage assessment

**Step 4: Define Scope Document**
- Compile audit results into scope document
- Include: what's in scope, what's explicitly out of scope, risks, dependencies
- Spawn docs-writer agent with doc_type: "refactor"
- Update CLAUDE.md with context pointer to refactor scope doc (if project has one)

**Step 5: Present and Suggest Next Steps**
```
REFACTOR INITIALIZED
====================

Scope document: .docs/refactors/MM-DD-YYYY-<area>.md
Baseline checkpoint: pre-refactor-<area> (SHA: <hash>)

Target area:
- [file count] files, [line count] lines
- [test count] tests covering target

Next steps (BRDSPI chain):
1. /researching-code — deep audit of target area patterns
2. /designing-code — target architecture, before/after comparison
3. /structuring-code — migration order (each step deployable)
4. /planning-code — atomic tasks with success criteria
5. /implementing-plans — execute with mandatory checkpoints
```

**Red Flags:**
- Starting refactor work before checkpoint is created
- Skipping the audit phase ("I already know this code")
- Scope creep — including areas beyond what user specified
- Not warning about uncommitted changes before checkpointing

**Rationalization Prevention:**

| Excuse | Reality |
|--------|---------|
| "It's a small refactor, no checkpoint needed" | Small refactors grow. Checkpoint anyway. |
| "I'll checkpoint after the audit" | Checkpoint captures pristine state. Audit doesn't change code but checkpoint must be first. |
| "The user already knows the scope" | Document it anyway. Downstream skills need the scope doc. |
| "I can skip the audit for familiar code" | Spawn agents. Verify. Your memory is stale. |

**The Bottom Line:**
**Checkpoint first, audit second, scope document third.** No exceptions. Every refactor starts with a safety net. Every refactor. Every time.

**Target size:** ~200-250 lines for SKILL.md

#### 2. Reference file: refactor-discovery.md
**File**: `newskills/starting-refactors/reference/refactor-discovery.md`

Content: Discovery question templates for different refactor types:
- Performance refactors — what's slow, where are bottlenecks
- Modularity refactors — what's coupled, what should be independent
- Migration refactors — what's the target tech/pattern, what's the bridge
- Cleanup refactors — what's the tech debt, what's the priority
- Scaling refactors — what's the growth pattern, what breaks first

Include audit agent prompt templates for each type. ~60-80 lines.

#### 3. Template file: refactor-scope-template.md
**File**: `newskills/starting-refactors/templates/refactor-scope-template.md`

Template structure for `.docs/refactors/` documents:

```markdown
# [Area] Refactor Scope

## Baseline
**Checkpoint:** [checkpoint name] (SHA: [hash])
**Date:** [date]
**Session:** [session name if active]

## Goal
[What the refactor aims to achieve — 1-2 sentences]

## Trigger
[Why now — what motivated this refactor]

## Target Area

### Files in Scope
- `path/to/file.ext` — [current role, line count]

### Files Explicitly Out of Scope
- `path/to/other.ext` — [why excluded]

## Current State Audit
### Architecture
[Current patterns, module boundaries, dependency direction]

### Test Coverage
[Existing tests, gaps, what's covered vs not]

### Dependencies
[What depends on this area, what this area depends on]

## Risks
- [Risk 1 — mitigation]
- [Risk 2 — mitigation]

## CLAUDE.md Context
[Any context pointers added to project CLAUDE.md]

## Next Steps
[Pointer to BRDSPI chain: /researching-code → /designing-code → ...]
```

~70-80 lines including section guidelines.

### Success Criteria:
- [x] `newskills/starting-refactors/SKILL.md` exists and passes validation
- [x] `newskills/starting-refactors/reference/refactor-discovery.md` exists with refactor type templates
- [x] `newskills/starting-refactors/templates/refactor-scope-template.md` exists with all sections
- [x] `/auditing-skills` reports no violations for `starting-refactors`
- [x] Deploy to `~/.claude/skills/starting-refactors/` and verify skill appears
- [x] Checkpoint creation is enforced before any audit work begins

---

## Phase 6: End-to-End Chain Test

### Overview
Test the full BRDSPI chain on a real (small) task to verify all skills integrate correctly, artifacts flow between phases, and backward compatibility is maintained.

### Test Plan:

#### Test 1: Full BRDSPI Chain (Greenfield-style)
Pick a small, real feature to design and plan (can be a commandbase skill enhancement or a test project).

1. Run `/designing-code` with research artifacts → verify `.docs/design/` doc created
2. Run `/structuring-code` with design doc → verify `.docs/structure/` map created
3. Run `/planning-code` with structural map → verify plan derives phases from structure
4. Confirm plan references design decisions without re-debating them

#### Test 2: Backward Compatibility
1. Run `/planning-code` with a plain task description (no design doc, no structural map)
2. Verify it works exactly as before — spawns research agents, makes architecture decisions, produces plan

#### Test 3: Brownfield Refactor Init
1. Run `/starting-refactors` on a target area
2. Verify checkpoint created BEFORE audit
3. Verify scope document created in `.docs/refactors/`
4. Verify next steps point to BRDSPI chain

#### Test 4: Lightweight Feature Path
1. Run `/researching-code` on a small question
2. Skip D+S, go directly to `/planning-code`
3. Verify standalone planning still works without structural map

### Success Criteria:
- [x] Test 1 passes: full chain produces valid design → structure → plan artifacts
- [x] Test 2 passes: /planning-code backward compatibility confirmed
- [x] Test 3 passes: /starting-refactors creates checkpoint + scope doc
- [x] Test 4 passes: lightweight R → P path still works
- [x] No skill produces artifacts in wrong directories
- [x] All artifacts use docs-writer (consistent frontmatter format)

---

## Phase 7: Sync Commandbase Repo

### Overview
Copy all deployed skills and agent back to the commandbase repo (source of truth) and verify consistency.

### Changes Required:

#### 1. Sync new skills to newskills/
```
cp -r ~/.claude/skills/designing-code/ newskills/designing-code/
cp -r ~/.claude/skills/structuring-code/ newskills/structuring-code/
cp -r ~/.claude/skills/starting-refactors/ newskills/starting-refactors/
```

#### 2. Sync modified skill to newskills/
```
cp ~/.claude/skills/planning-code/SKILL.md newskills/planning-code/SKILL.md
cp ~/.claude/skills/planning-code/reference/research-workflow.md newskills/planning-code/reference/research-workflow.md
```

#### 3. Sync modified agent to newagents/
```
cp ~/.claude/agents/docs-writer.md newagents/docs-writer.md
```

#### 4. Verify consistency
Diff each deployed file against repo version to confirm they match.

### Success Criteria:
- [x] All 3 new skill directories exist in `newskills/`
- [x] Modified `planning-code` files match deployed versions
- [x] Modified `docs-writer.md` matches deployed version
- [x] `diff` shows no differences between deployed and repo versions
- [x] Ready for `/committing-changes`

---

## Testing Strategy

### Per-Skill Validation:
- `/auditing-skills` run against each new/modified skill
- Frontmatter validation (name matches dir, description format)
- Structure validation (SKILL.md <500 lines, reference nesting ≤1 level)

### Integration Tests:
- Full BRDSPI chain (Test 1 above)
- Backward compatibility (Test 2 above)
- Brownfield refactor init (Test 3 above)
- Lightweight path (Test 4 above)

### Artifact Validation:
- Each skill produces its expected `.docs/` artifact type
- All artifacts have correct frontmatter (via docs-writer)
- Artifacts contain required sections per their templates

## References

- Research: `.docs/research/02-07-2026-phase-2-brdspi-core-research.md`
- Roadmap: `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md`
- RDSPI concept: `.docs/future-skills/rdspi-workflow.md`
- Skill spec: via `/creating-skills` validation rules
- Checkpoint pattern: `newskills/implementing-plans/SKILL.md:86,171-175`
- docs-writer interface: `newagents/docs-writer.md:32,63-69`
