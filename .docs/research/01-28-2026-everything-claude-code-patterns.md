---
git_commit: 448f0d2
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Updated after 8 commits - marked implemented recommendations, added implementation status section"
topic: "Workflow Enhancement Ideas from everything-claude-code"
tags: [research, workflow, skills, agents, hooks]
status: complete
references:
  - C:/code/everything-claude-code/skills/continuous-learning-v2/SKILL.md
  - C:/code/everything-claude-code/skills/iterative-retrieval/SKILL.md
  - C:/code/everything-claude-code/skills/verification-loop/SKILL.md
  - C:/code/everything-claude-code/skills/strategic-compact/SKILL.md
  - C:/code/everything-claude-code/commands/orchestrate.md
  - C:/code/everything-claude-code/commands/checkpoint.md
  - C:/code/everything-claude-code/commands/learn.md
  - C:/code/everything-claude-code/commands/skill-create.md
---

# Research: Workflow Enhancement Ideas from everything-claude-code

**Date**: 2026-01-28
**Branch**: master

## Research Question

Review everything-claude-code repo for ideas that could enhance our RPI workflow.

## Summary

The everything-claude-code repo contains 16 skills, 23 commands, 12 agents, and comprehensive hook configurations. Several patterns could enhance our workflow, particularly around learning capture, verification checkpoints, and agent orchestration.

## High-Value Patterns for Our Workflow

### 1. `/learn` Command - Mid-Session Pattern Extraction

**Source**: `commands/learn.md:1-71`

Captures reusable patterns during a session, not just at handover time.

**How it works**:
- Run `/learn` when you solve a non-trivial problem
- Extracts: error resolutions, debugging techniques, workarounds, project patterns
- Saves to `~/.claude/skills/learned/[pattern-name].md`

**Relevance to RPI**:
- Our `/handover` captures session context but not reusable patterns
- `/learn` would complement handover by extracting atomic learnings
- Could feed into a "lessons learned" directory separate from handoffs

**Potential adaptation**:
```
/learn → .docs/learnings/MM-DD-YYYY-pattern-name.md
```

### 2. `/checkpoint` Command - Progress Verification Gates

**Source**: `commands/checkpoint.md:1-75`

Creates named verification points during long implementations.

**How it works**:
- `/checkpoint create "feature-start"` - Saves state (git SHA, test status)
- `/checkpoint verify "feature-start"` - Compares current state to checkpoint
- Reports: files changed, tests delta, coverage delta

**Relevance to RPI**:
- Our `/icode` implements in phases but doesn't checkpoint between them
- Checkpoints would allow mid-implementation rollback
- Fits naturally between `/pcode` phases

**Potential workflow**:
```
/pcode → /checkpoint create "plan-approved"
/icode Phase 1 → /checkpoint create "phase-1-done"
/icode Phase 2 → /checkpoint verify "phase-1-done" (ensure no regression)
```

### 3. Iterative Retrieval Pattern - Smarter Agent Context

**Source**: `skills/iterative-retrieval/SKILL.md:1-203`

Solves "subagents don't know what context they need" problem with 4-phase loop.

**How it works**:
```
DISPATCH (broad search) → EVALUATE (score relevance 0-1) → REFINE (update keywords) → LOOP (max 3 cycles)
```

**Key insight** (`iterative-retrieval/SKILL.md:17-19`):
> Standard approaches fail:
> - Send everything: Exceeds context limits
> - Send nothing: Agent lacks critical information
> - Guess what's needed: Often wrong

**Relevance to RPI**:
- Our `/rcode` spawns agents with static prompts
- Iterative retrieval would let agents refine their search
- Particularly useful for `/pcode` research phase

**Potential integration**: Teach codebase-locator and codebase-analyzer to do 2-3 refinement cycles before returning results.

### 4. `/orchestrate` Command - Agent Pipelines

**Source**: `commands/orchestrate.md:1-173`

Chains agents in predefined sequences with structured handoffs.

**Predefined workflows**:
| Workflow | Agent Chain |
|----------|-------------|
| feature | planner → tdd-guide → code-reviewer → security-reviewer |
| bugfix | explorer → tdd-guide → code-reviewer |
| refactor | architect → code-reviewer → tdd-guide |

**Handoff format** (`orchestrate.md:48-65`):
```markdown
## HANDOFF: [previous-agent] -> [next-agent]
### Context
### Findings
### Files Modified
### Open Questions
### Recommendations
```

**Relevance to RPI**:
- Our workflow is: rcode → pcode → icode → vcode
- Each step is manual - `/orchestrate` would automate the chain
- Could create `/rpi feature "description"` that runs full cycle

### 5. `/skill-create` - Extract Patterns from Git History

**Source**: `commands/skill-create.md:1-175`

Analyzes git history to generate skills from actual codebase patterns.

**What it detects** (`skill-create.md:45-53`):
- Commit conventions (feat:, fix:, chore:)
- File co-changes (files that always change together)
- Workflow sequences (repeated patterns)
- Architecture patterns

**Relevance to RPI**:
- Could generate project-specific skills from any codebase
- Useful for onboarding to new projects
- Complements `/rcode` by codifying discovered patterns

### 6. Contexts - Mode Switching

**Source**: `contexts/dev.md:1-21`

Short markdown files that inject behavior modes.

**dev.md example**:
```markdown
Mode: Active development
Focus: Implementation, coding, building features

## Behavior
- Write code first, explain after
- Prefer working solutions over perfect solutions

## Priorities
1. Get it working
2. Get it right
3. Get it clean
```

**Relevance to RPI**:
- We could have contexts for each RPI phase
- `/context research` - favor exploration over implementation
- `/context implement` - favor action over research
- `/context validate` - favor thoroughness over speed

### 7. Continuous Learning v2 - Instinct Architecture

**Source**: `skills/continuous-learning-v2/SKILL.md:1-258`

Captures atomic learned behaviors with confidence scoring.

**Instinct format** (`continuous-learning-v2/SKILL.md:26-43`):
```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
---
## Action
Use functional patterns over classes
## Evidence
- Observed 5 instances of preference
- User corrected class-based approach on 2025-01-15
```

**Key innovation** (`continuous-learning-v2/SKILL.md:46-49`):
- Atomic: one trigger, one action
- Confidence-weighted: 0.3 = tentative, 0.9 = near certain
- Evidence-backed: tracks what observations created it

**Relevance to RPI**:
- More granular than our handover documents
- Could track "what worked" across sessions
- Confidence scoring surfaces reliable vs experimental patterns

## Patterns We Already Have Covered

### Verification Loop
`skills/verification-loop/SKILL.md` - Similar to our `/vcode` but less structured. Our two-stage gate (spec compliance → code quality) is more rigorous.

### Strategic Compact
`skills/strategic-compact/SKILL.md` - Suggests manual compaction at logical points. We already do `/handover` → `/clear` → `/takeover` which achieves similar goal.

## Patterns to Consider but Not Priority

### Hook-Based Observation
Continuous-learning-v2 uses PreToolUse/PostToolUse hooks to capture every action. Heavy infrastructure for uncertain benefit - we decided against hooks for now.

### Agent Model Assignments
everything-claude-code assigns models per agent (Opus for planning, Haiku for observation). Could optimize cost but adds complexity.

## Recommended Enhancements

| Priority | Pattern | Adaptation | Status |
|----------|---------|------------|--------|
| 🔴 High | `/learn` | Create `/learn` to capture patterns mid-session | **IMPLEMENTED** as `learning-from-sessions` skill |
| 🔴 High | `/checkpoint` | Add checkpoint support to `/icode` phases | **IMPLEMENTED** as `checkpointing` skill |
| 🟡 Medium | Contexts | Create RPI phase contexts | Not started |
| 🟡 Medium | Iterative retrieval | Enhance agents with refinement loops | Not started |
| 🟢 Low | `/orchestrate` | Create `/rpi` for full workflow automation | Not started |
| 🟢 Low | `/skill-create` | Add project pattern extraction | Partially covered by `creating-skills` skill |

## Implementation Status (Updated 2026-02-01)

### Completed

**`learning-from-sessions` skill** (newskills/learning-from-sessions/SKILL.md)
- Implements the `/learn` pattern from everything-claude-code
- Goes beyond the original with: dedup checking, complexity assessment, quality gates, research integration
- Includes extraction workflow, retrospective mode, and output routing
- Reference files: description-optimization.md, extraction-workflow.md, quality-gates.md, research-foundations.md

**`checkpointing` skill** (newskills/checkpointing/SKILL.md)
- Implements the `/checkpoint` pattern with create/verify/list/clear operations
- Uses file-based storage (.claude/checkpoints.log) as recommended in Open Questions
- Integrates with RPI workflow: plan-approved -> phase-N-done checkpoints
- Git-aware with uncommitted change warnings

### Remaining

- **Contexts**: Could still add RPI phase contexts for mode switching
- **Iterative retrieval**: Agents could be enhanced but current research approach works
- **Orchestrate**: Full workflow automation remains aspirational

## Architecture Notes

### File Organization
everything-claude-code uses:
```
skills/          # Directory format (skillname/SKILL.md)
commands/        # Flat files (command.md)
agents/          # Flat files (agent.md)
contexts/        # Flat files (context.md)
rules/           # Flat files (rule.md)
```

Our structure matches this for skills (newskills/skillname/SKILL.md).

### Plugin vs Manual Install
everything-claude-code supports both plugin install and manual copy. Our commandbase is manual-only (develop → deploy to ~/.claude/).

## Code References

- `C:/code/everything-claude-code/commands/learn.md:34-55` - Skill file output format
- `C:/code/everything-claude-code/commands/checkpoint.md:16-42` - Checkpoint workflow
- `C:/code/everything-claude-code/skills/iterative-retrieval/SKILL.md:42-132` - 4-phase loop implementation
- `C:/code/everything-claude-code/commands/orchestrate.md:11-34` - Predefined workflows
- `C:/code/everything-claude-code/skills/continuous-learning-v2/SKILL.md:22-49` - Instinct model

## Open Questions

1. ~~Should `/learn` patterns go in `.docs/learnings/` or `~/.claude/skills/learned/`?~~ **RESOLVED**: `learning-from-sessions` routes to `.claude/skills/` (project) or `~/.claude/skills/` (user) based on scope, with CLAUDE.md for simple entries.
2. ~~Should checkpoints be git-based (stash/tag) or file-based (.claude/checkpoints.log)?~~ **RESOLVED**: File-based via `.claude/checkpoints.log` with pipe-delimited format.
3. Would contexts conflict with skill enforcement patterns? (Still open)
