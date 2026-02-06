---
git_commit: 448f0d2
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Updated integration points - starting-projects now mentions discussing-features (b124504)"
topic: "GSD vs Commandbase Skills Comparison"
tags: [research, skill-comparison, gsd, workflow]
references:
  - newskills/discussing-features/SKILL.md
  - newskills/debugging-code/SKILL.md
  - newskills/starting-projects/SKILL.md
  - .docs/plans/02-01-2026-discussing-features-skill.md
  - .docs/plans/02-01-2026-debugging-code-skill.md
---

# Get Shit Done (GSD) vs Commandbase Skills Comparison

**Date:** 2026-02-01
**Topic:** Evaluating GSD repository for skill enhancements
**Source:** C:/code/repo-library/get-shit-done

---

## Implementation Status

> **Note:** This research document led to the implementation of two new skills. See status below.

| Recommendation | Status | Implementation |
|----------------|--------|----------------|
| `/discussing-features` skill | **IMPLEMENTED** | `newskills/discussing-features/` |
| `/debugging-code` skill | **IMPLEMENTED** | `newskills/debugging-code/` |
| `/quick-implementing` skill | **DECLINED** | RPI workflow is opt-in; users can implement directly |
| UAT mode for `/validating-code` | **DECLINED** | Not pursuing at this time |
| Structured mode for `/researching-code` | **DECLINED** | Not pursuing at this time |
| Wave computation for `/planning-code` | Not started | - |
| Wave-based parallel execution for `/implementing-plans` | **DECLINED** | Complexity outweighs benefit for typical work |

---

## Executive Summary

The **get-shit-done** repository is a comprehensive meta-prompting and context engineering system for Claude Code that solves "context rot" - the quality degradation that happens as Claude fills its context window. After thorough analysis, I've identified several valuable patterns and capabilities that could enhance our existing skills.

### Key Findings

| Category | GSD Strength | Our Current Gap | Recommendation |
|----------|--------------|-----------------|----------------|
| **Phase Discussion** | `/gsd:discuss-phase` captures user intent BEFORE research | ~~We jump straight to planning~~ | ~~**ADD** - New skill~~ **DONE** - `/discussing-features` |
| **Quick Mode** | `/gsd:quick` for ad-hoc tasks with same guarantees | All tasks go through full workflow | ~~**ADD** - Lightweight implementation skill~~ [DECLINED] |
| **Debug System** | Persistent debug state with scientific method | ~~No dedicated debugging skill~~ | ~~**ADD** - New `/debugging` skill~~ **DONE** - `/debugging-code` |
| **User Acceptance Testing** | `/gsd:verify-work` - conversational UAT | `/validating-code` is code-focused | ~~**ENHANCE** - Add UAT mode~~ [DECLINED] |
| **Model Profiles** | Budget/balanced/quality agent model selection | Hard-coded model usage | **ADD** - Model selection to config |
| **Context Engineering** | Wave-based parallel execution, dependency graphs | Sequential execution | ~~**ENHANCE** - Add to `/implementing-plans`~~ [DECLINED] |
| **Codebase Mapping** | `/gsd:map-codebase` for brownfield projects | We have `/researching-code` | ~~**ENHANCE** - Add structured templates~~ [DECLINED] |
| **Session Continuity** | `STATE.md` as living memory + `CONTINUE-HERE.md` | `/handing-over` + `/taking-over` | Comparable - minor improvements |
| **Milestone Management** | Archive completed milestones, tag releases | No milestone concept | **CONSIDER** - For larger projects |

---

## Detailed Analysis

### 1. Capabilities GSD Has That We Should Add

#### A. Phase Discussion (`/gsd:discuss-phase`) - **HIGH VALUE** [IMPLEMENTED]

> **Status:** Implemented as `/discussing-features` skill. See `newskills/discussing-features/`.

**What it does:**
Before research or planning, captures user's implementation preferences through targeted questions based on feature type:
- Visual features -> Layout, density, interactions, empty states
- APIs/CLIs -> Response format, flags, error handling
- Content systems -> Structure, tone, depth, flow

**Why it matters:**
Prevents Claude from making assumptions. The output (`CONTEXT.md`) constrains both research scope AND planning decisions.

**Our implementation:**
Created `/discussing-features` skill with:
- Domain detection (visual, API, CLI, content, organization)
- 4-question rhythm with check-ins for depth control
- Outputs structured context document to `.docs/context/{feature-name}.md`
- Reference file for domain-specific question templates
- Template for context document output

---

#### B. Quick Mode (`/gsd:quick`) - ~~HIGH VALUE~~ [DECLINED]

**What it does:**
For ad-hoc tasks that don't warrant full planning:
- Same quality guarantees (atomic commits, state tracking)
- Skips research, plan-checking, verification
- Separate tracking in `.planning/quick/`

**Why it matters:**
Not every task needs the full RPI workflow. Bug fixes, small features, config changes need a faster path.

**Our gap:**
We have no lightweight implementation path. Users must either skip skills entirely or go through full `/planning-code` → `/implementing-plans`.

**Decision: DECLINED**
Not needed - the RPI workflow is already opt-in. Users can implement directly without invoking any skill when they want a lightweight path. Adding a formal `/quick-implementing` skill would add unnecessary overhead for what is essentially "just do the work."

---

#### C. Systematic Debugging (`/gsd:debug`) - **HIGH VALUE** [IMPLEMENTED]

> **Status:** Implemented as `/debugging-code` skill. See `newskills/debugging-code/`.

**What it does:**
- Persistent debug state in `.planning/debug/*.md`
- Scientific hypothesis testing with falsifiability
- Multiple investigation techniques (binary search, differential debugging, etc.)
- Cognitive bias awareness (confirmation bias, anchoring)
- Two modes: find root cause only, or find and fix

**Why it matters:**
Debugging is a significant part of development. Having a structured approach prevents thrashing and ensures lessons are captured.

**Our implementation:**
Created `/debugging-code` skill with:
- Persistent debug session files in `.docs/debug/`
- Hypothesis-driven investigation with falsifiability requirements
- Clear state transitions (gathering -> investigating -> fixing -> verifying -> resolved)
- Integration with `/learning-from-sessions` for knowledge extraction
- Reference files for investigation techniques, hypothesis testing, and verification patterns

---

#### D. Model Profile Selection - **MEDIUM VALUE**

**What it does:**
Three profiles controlling which model each agent uses:
- **quality**: Opus everywhere (highest cost)
- **balanced**: Opus for planning, Sonnet for execution (default)
- **budget**: Sonnet for writing, Haiku for research (lowest cost)

**Why it matters:**
Not all tasks need Opus. Budget-conscious users can save significantly on routine work while preserving quality for critical decisions.

**Our gap:**
No model selection capability. All agents use whatever model the user started with.

**Recommendation:**
Add `model_profile` to skill configurations. Allow per-skill model overrides.

---

#### E. Wave-Based Parallel Execution - ~~MEDIUM VALUE~~ [DECLINED]

**What it does:**
- Pre-computes dependency graphs during planning
- Assigns tasks to "waves" for parallel execution
- Independent tasks in same wave run simultaneously

**Why it matters:**
Faster execution. Fresh context per parallel agent prevents degradation.

**Our gap:**
`/implementing-plans` executes phases sequentially.

~~**Recommendation:**~~
~~Add wave computation to `/planning-code` and parallel execution to `/implementing-plans` for independent tasks.~~

**Decision: DECLINED** - Complexity outweighs benefit for typical work. Sequential execution is simpler to reason about and debug.

---

### 2. Capabilities to Enhance in Existing Skills

#### A. User Acceptance Testing Mode for `/validating-code` [DECLINED]

**GSD's approach (`/gsd:verify-work`):**
- Extracts testable deliverables from SUMMARY files
- Presents ONE test at a time (not a checklist)
- Plain text responses ("yes" = pass, anything else = describe issue)
- Infers severity from description
- Spawns debug agents for issues found

**Our current approach:**
- Spec compliance checking
- Code quality review
- Automated verification commands

~~**Enhancement:**~~
~~Add `--uat` flag to `/validating-code` that:~~
~~- Extracts user-observable behaviors from plan~~
~~- Walks user through manual testing conversationally~~
~~- Captures issues for fix planning~~

**Decision: DECLINED** - Not pursuing at this time.

---

#### B. Structured Codebase Mapping Templates for `/researching-code` [DECLINED]

**GSD's approach (`/gsd:map-codebase`):**
Produces structured documents in `.planning/codebase/`:
- `STACK.md` - Languages, runtime, frameworks, key dependencies
- `ARCHITECTURE.md` - Pattern overview, layers, data flow
- `STRUCTURE.md` - Directory layout with purposes
- `CONVENTIONS.md` - Naming, code style, import organization
- `CONCERNS.md` - Tech debt, security considerations, fragile areas
- `TESTING.md` - Test framework, coverage patterns
- `INTEGRATIONS.md` - External APIs, data storage

**Our current approach:**
Free-form research documents in `.docs/research/`

~~**Enhancement:**~~
~~Add optional `--structured` flag to `/researching-code` that produces standardized codebase documentation using GSD's templates.~~

**Decision: DECLINED** - Not pursuing at this time.

---

#### C. Goal-Backward Verification for `/implementing-plans`

**GSD's approach:**
- Plans include `must_haves` field with:
  - `truths`: Observable behaviors from user perspective
  - `artifacts`: Files that must exist with specific properties
  - `key_links`: Wiring between components (Component→API, API→Database)
- Verifier checks ALL three levels, not just file existence

**Our current approach:**
Success criteria as checkboxes, verification commands in plan

**Enhancement:**
Add structured `must_haves` to plan template. Enhance verification to check:
1. **Exists** - File present
2. **Substantive** - Not a stub (line count, exports, no TODOs)
3. **Wired** - Actually imported and used

---

### 3. Capabilities We Have That GSD Lacks

| Our Capability | Description |
|----------------|-------------|
| `/creating-skills` | Skill development workflow - GSD has no meta-skill for creating new skills |
| `/learning-from-sessions` | Knowledge extraction from sessions - GSD tracks state but doesn't extract reusable patterns |
| `/reviewing-security` | Security-focused review before commits - GSD has no security scanning |
| Skill progressive disclosure | Reference files, templates - GSD uses flat command + workflow files |
| Plugin architecture | Agents, hooks, MCP integration - GSD is commands-only |

---

### 4. Architectural Differences

| Aspect | GSD | Commandbase |
|--------|-----|-------------|
| **Structure** | Slash commands that delegate to workflows | Skills with SKILL.md + supporting files |
| **State** | `.planning/` directory with STATE.md, config.json | `.docs/` directory with handoffs, research, plans |
| **Agents** | Named agents with specific roles (planner, executor, verifier) | Generic subagent types (code-analyzer, etc.) |
| **Execution** | Wave-based parallel with dependency graphs | Sequential phase execution |
| **Context** | @-references for lazy loading, strict size limits | Full file reads, no explicit limits |
| **Git** | Per-task atomic commits, conventional commit format | Per-change commits |
| **Documentation** | XML-heavy for machine parsing | Markdown-heavy for human reading |

---

## Recommendations Summary

### Immediate Additions (High Value)

1. **~~Create `/discussing-features` skill~~** - Pre-planning discovery to capture user intent **[IMPLEMENTED]**
2. ~~**Create `/quick-implementing` skill** - Lightweight path for ad-hoc tasks~~ **[DECLINED]** - RPI workflow is opt-in; users can implement directly
3. **~~Create `/debugging-code` skill~~** - Systematic debugging with persistent state **[IMPLEMENTED]**

### Enhancements to Existing Skills

4. ~~**Enhance `/validating-code`** - Add `--uat` mode for conversational testing~~ **[DECLINED]** - Not pursuing at this time
5. ~~**Enhance `/researching-code`** - Add `--structured` mode with codebase templates~~ **[DECLINED]** - Not pursuing at this time
6. ~~**Enhance `/planning-code`** - Add wave computation for parallel execution~~ **[DECLINED]** - See item 7
7. ~~**Enhance `/implementing-plans`** - Add wave-based parallel execution~~ **[DECLINED]** - Complexity outweighs benefit for typical work

### Consider for Future

8. **Model profile selection** - Allow per-skill model configuration
9. **Milestone management** - Archive completed milestones for large projects
10. **Enhance `/implementing-plans`** - Add three-level verification (exists/substantive/wired) - Not yet evaluated

---

## Workflow Integration: Where `/discussing-features` Fits

### The Core Insight

GSD's `/gsd:discuss-phase` comes BEFORE `/gsd:research-phase` because discussion context **constrains** what gets researched. No point researching card layouts if the user already said they want a table view.

### Skill Purpose Distinction

| Skill | Purpose | Questions Asked |
|-------|---------|-----------------|
| `/starting-projects` | **WHAT** are we building? | Project type, tech stack, goals, constraints |
| `/discussing-features` | **HOW** should this feature work? | Layout preferences, API design, UX decisions |
| `/researching-code` | **WHAT EXISTS** in the codebase? | How does X work, where is Y defined |
| `/planning-code` | **HOW TO IMPLEMENT** the feature? | Implementation approaches, file structure |

### The Correct Order: Discuss → Research → Plan → Implement

**GREENFIELD Workflow:**
```
/starting-projects              → Project setup + CLAUDE.md (once)
    ↓
For each feature:
    /discussing-features        → Capture HOW preferences (user intent)
        ↓
    /researching-code      → Understand relevant existing code (as codebase grows)
        ↓
    /planning-code         → Research approaches + create plan
        ↓                         (constrained by discussion context)
    /implementing-plans         → Execute
        ↓
    /validating-code → Verify against plan
```

**BROWNFIELD Workflow:**
```
/researching-code          → Understand existing codebase patterns (initial)
    ↓
For each feature:
    /discussing-features        → Capture HOW preferences (user intent)
        ↓
    /researching-code      → Deep dive on relevant areas (optional)
        ↓
    /planning-code         → Plan informed by research + discussion
        ↓
    /implementing-plans         → Execute
        ↓
    /validating-code → Verify
```

### Why This Order Matters

1. **`/discussing-features` BEFORE `/researching-code`**
   - User preferences constrain research scope
   - Prevents wasted research on ruled-out approaches
   - User intent captured while fresh, not retrofitted

2. **`/researching-code` BEFORE `/planning-code`**
   - Understand existing patterns before proposing new ones
   - Identify reusable components and conventions
   - Avoid reinventing existing abstractions

3. **Discussion context flows downstream**
   - `/planning-code` reads discussion output
   - Research is focused, not exploratory
   - Plans honor user decisions, don't revisit them

### Integration Points to Implement

1. **`/starting-projects`** should mention `/discussing-features` in "workflow going forward" - **DONE** (commit b124504)
2. **`/discussing-features`** should output `.docs/context/{feature-name}.md` - **DONE** (outputs to `.docs/context/`)
3. **`/planning-code`** should check for and honor existing context documents - Not yet implemented
4. **`/researching-code`** should be aware of discussion context to focus research - Not yet implemented

### Standalone vs Embedded

**`/discussing-features` should be STANDALONE**, not embedded in `/starting-projects`:
- `/starting-projects` is one-time project initialization
- `/discussing-features` is per-feature, reused throughout project lifecycle
- Different trigger phrases ("new project" vs "let's discuss this feature")
- Different outputs (CLAUDE.md + setup plan vs feature context document)

---

## Patterns Worth Adopting

### 1. Context Size Awareness
GSD explicitly tracks context usage:
- 0-30%: Peak quality
- 30-50%: Good quality
- 50-70%: Degrading
- 70%+: Poor quality

**Action:** Add context budget awareness to skills, recommend `/clear` at thresholds.

### 2. Deviation Rules for Autonomous Execution
GSD defines when Claude can act without asking:
- Rule 1: Auto-fix bugs (always)
- Rule 2: Auto-add missing critical functionality (always)
- Rule 3: Auto-fix blocking issues (always)
- Rule 4: Ask about architectural changes (never auto)

**Action:** Document similar rules in `/implementing-plans`.

### 3. Authentication Gates
GSD treats auth errors as normal flow pause points, not failures:
- Claude automates everything possible
- Pauses for human to complete OAuth/MFA
- Resumes automatically after

**Action:** Add authentication gate handling to skill documentation.

### 4. XML Task Structure
GSD uses consistent XML for machine-readable tasks:
```xml
<task type="auto">
  <name>Task Name</name>
  <files>path/to/file.ext</files>
  <action>What to do</action>
  <verify>How to prove it worked</verify>
  <done>Acceptance criteria</done>
</task>
```

**Action:** Consider adopting for plan phases where machine parsing is beneficial.

---

## Files of Interest for Reference

| GSD File | Our Equivalent | Notes |
|----------|----------------|-------|
| `agents/gsd-debugger.md` | `/debugging-code` | **IMPLEMENTED** |
| `commands/gsd/discuss-phase.md` | `/discussing-features` | **IMPLEMENTED** |
| `commands/gsd/quick.md` | None | Lightweight execution |
| `commands/gsd/verify-work.md` | `/validating-code` | UAT approach |
| `templates/codebase/*.md` | None | Structured codebase docs |
| `references/verification-patterns.md` | None | Three-level verification |
| `references/checkpoints.md` | `/bookmarking-code` | More detailed patterns |

---

## Conclusion

GSD is a mature, well-designed system with several capabilities that would meaningfully enhance our skill set. ~~The highest-value additions are:~~

**Implemented (2026-02-01):**
1. **Pre-planning discussion** - `/discussing-features` skill captures user intent before research
2. **Systematic debugging** - `/debugging-code` skill with persistent state and scientific method

**Declined (2026-02-01):**
3. ~~**Quick mode** for lightweight task execution (`/quick-implementing`)~~ - RPI workflow is opt-in; users can implement directly without a skill
4. ~~**UAT mode** for `/validating-code`~~ - Not pursuing at this time
5. ~~**Structured codebase mapping** for `/researching-code`~~ - Not pursuing at this time
6. ~~**Wave-based parallel execution** for `/implementing-plans`~~ - Complexity outweighs benefit for typical work

The key philosophical difference is GSD's focus on **context engineering** - actively managing Claude's context window to prevent quality degradation. This is worth adopting across our skills.

~~I recommend prioritizing the three new skills above, then incrementally enhancing existing skills with GSD's verification patterns and structured templates.~~

**Status:** Core high-value additions are complete. Remaining enhancements (model profiles, milestone management, three-level verification) remain under consideration for future work.
