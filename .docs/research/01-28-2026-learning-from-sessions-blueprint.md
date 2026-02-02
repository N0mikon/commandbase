---
git_commit: 448f0d2
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Updated after 8 commits - marked as implemented, removed deleted references, resolved open questions"
topic: "Learning-from-Sessions Blueprint Analysis"
tags: [research, learning-from-sessions, claudeception, claude-reflect, skill-extraction, reflective-learning]
status: implemented
references:
  - .docs/plans/learning-from-sessions-blueprint.md
  - newskills/learning-from-sessions/SKILL.md
  - newskills/learning-from-sessions/reference/extraction-workflow.md
  - newskills/learning-from-sessions/reference/quality-gates.md
  - newskills/learning-from-sessions/reference/description-optimization.md
  - newskills/learning-from-sessions/reference/research-foundations.md
  - newskills/learning-from-sessions/templates/extracted-skill-template.md
  - newskills/creating-skills/SKILL.md
  - C:/code/repo-library/Claudeception/SKILL.md
  - C:/code/repo-library/Claudeception/scripts/claudeception-activator.sh
  - C:/code/repo-library/Claudeception/resources/skill-template.md
  - C:/code/repo-library/Claudeception/resources/research-references.md
  - C:/code/repo-library/Claudeception/examples/
  - C:/code/repo-library/claude-reflect/commands/reflect.md
  - C:/code/repo-library/claude-reflect/commands/reflect-skills.md
  - C:/code/repo-library/claude-reflect/scripts/lib/reflect_utils.py
  - C:/code/repo-library/claude-reflect/scripts/lib/semantic_detector.py
  - C:/code/repo-library/claude-reflect/hooks/hooks.json
  - C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py
---

# Research: Learning-from-Sessions Blueprint

**Date**: 2026-01-28
**Branch**: master
**Implementation Status**: IMPLEMENTED (2026-01-28)

## Implementation Note

This blueprint has been implemented. The `learning-from-sessions` skill now exists at `newskills/learning-from-sessions/` with the structure proposed in Section 6. The old `newskills/learn/SKILL.md` and `newreference/pattern-learning.md` were replaced by this implementation.

This document is preserved as design context for anyone maintaining or extending the skill.

## Research Question

Comprehensive analysis of the `learning-from-sessions-blueprint.md` plan file: what it specifies, what its primary influences contain, how the output structure maps to existing patterns, and what the implementation prompt at the bottom prescribes.

## Summary

The blueprint defines a reflective meta-skill called `learning-from-sessions` that extracts reusable knowledge from work sessions. It synthesizes two primary influences: **Claudeception** (6-step extraction workflow, self-reflection prompts, dedup-first, quality gates) and **Claude-Reflect** (two-stage capture/process architecture, queue bridge, semantic+regex hybrid detection, skill improvement routing). The output is a skill directory with 6 files: `SKILL.md` + 4 reference docs + 1 template. The existing `learn` skill (`newskills/learn/SKILL.md`) is a simpler predecessor that handles manual pattern extraction but lacks the extraction workflow depth, web research step, dedup system, and description optimization that the blueprint prescribes.

## Detailed Findings

### 1. The Blueprint Structure

The plan file lives at `.docs/plans/learning-from-sessions-blueprint.md` (258 lines). It contains seven sections:

| Section | Lines | Purpose |
|---------|-------|---------|
| Purpose | 9-11 | One-paragraph mission statement |
| Research Files | 15-21 | Links to 5 research documents |
| Cloned Repos | 23-28 | 4 repos with specific files to read |
| What to Take from Each | 32-67 | Pattern extraction from 3 influences |
| Proposed Structure | 71-98 | Directory layout + SKILL.md frontmatter |
| Core Workflow | 101-198 | Detailed workflow for SKILL.md body |
| Prompt for Separate Window | 202-257 | Copy-paste implementation prompt |

The blueprint is a **build specification**, not a research document. It tells the implementer exactly what to read, what to take from each source, how to structure the output, and what workflow the skill should execute.

### 2. Primary Influence: Claudeception

**Repo**: `C:/code/repo-library/Claudeception/`

Claudeception contributes the **core extraction workflow** -- the step-by-step process the learning skill executes when extracting knowledge.

#### 6-Step Extraction Workflow (`Claudeception/SKILL.md:66-223`)

1. **Check Existing Skills (Dedup-First)** (`SKILL.md:66-103`): Search `.claude/skills`, `~/.claude/skills`, `~/.codex/skills` using `rg` before creating. Decision matrix with 6 outcomes (create new, update existing, cross-link, add variant, deprecate, replace).

2. **Identify the Knowledge** (`SKILL.md:105-111`): Four analysis questions: What was the problem? What was non-obvious? What would help next time? What are exact trigger conditions?

3. **Research Best Practices** (`SKILL.md:113-156`): Web search for technology-specific topics. Skip for project-internal, context-specific, or stable generic concepts. Search pattern: `"[technology] [problem] best practices 2026"`.

4. **Structure the Skill** (`SKILL.md:158-195`): Standard 7-section template: Problem, Context/Trigger Conditions, Solution, Verification, Example, Notes, References.

5. **Write Effective Descriptions** (`SKILL.md:197-213`): Descriptions must contain specific symptoms, context markers (framework names), and action phrases ("Use when..."). This is the retrieval key for semantic matching.

6. **Save the Skill** (`SKILL.md:215-223`): Project-level (`.claude/skills/`) or user-level (`~/.claude/skills/`) based on scope.

#### Self-Reflection Prompts (`Claudeception/SKILL.md:236-244`)

Five introspection questions run after task completion:
- "What did I just learn that wasn't obvious before starting?"
- "If I faced this exact problem again, what would I wish I knew?"
- "What error message or symptom led me here, and what was the actual cause?"
- "Is this pattern specific to this project, or would it help in similar projects?"
- "What would I tell a colleague who hits this same issue?"

#### Quality Gates (`Claudeception/SKILL.md:257-269`)

Nine-item checklist:
1. Description contains specific trigger conditions
2. Solution has been verified to work
3. Content is specific enough to be actionable
4. Content is general enough to be reusable
5. No sensitive information (credentials, internal URLs)
6. Doesn't duplicate existing docs/skills
7. Web research conducted when appropriate
8. References section included if web sources consulted
9. Post-2025 best practices incorporated

#### Anti-Patterns (`Claudeception/SKILL.md:271-277`)

Five patterns to avoid: over-extraction, vague descriptions, unverified solutions, documentation duplication, stale knowledge.

#### Forced Evaluation Hook (`Claudeception/scripts/claudeception-activator.sh:12-39`)

A `UserPromptSubmit` hook that injects evaluation protocol on every prompt. Three evaluation questions, then activates `Skill(claudeception)` if any answer YES. Achieves 84% activation rate per the `skillcreator-repos.md` research.

#### Output Template (`Claudeception/resources/skill-template.md:1-96`)

Standard sections: frontmatter (name, description, author, version, date), Problem, Context/Trigger Conditions, Solution (multi-step), Verification, Example (Before/After), Notes. Includes a 10-item extraction checklist in an HTML comment to be removed before saving.

#### Example Skills (`Claudeception/examples/`)

Three example extracted skills demonstrate the output format:
- `nextjs-server-side-error-debugging/SKILL.md` -- Error messages in wrong location
- `prisma-connection-pool-exhaustion/SKILL.md` -- Serverless connection exhaustion
- `typescript-circular-dependency/SKILL.md` -- Runtime undefined from circular imports

All three share identical structure: frontmatter with numbered trigger conditions `(1)...(2)...(3)...(4)`, Problem (emphasizing the misleading aspect), Context/Trigger with exact error strings, Solution with 3-4 numbered steps and code blocks, Verification, Example, Notes.

#### Academic Foundation (`Claudeception/resources/research-references.md:5-169`)

Five core papers inform the design:
- **Voyager** (Wang et al., 2023): Ever-growing skill library, self-verification, compositional skills
- **CASCADE** (2024): Meta-skills for learning, knowledge codification, memory consolidation
- **SEAgent** (Sun et al., 2025): Trial-and-error experiential learning
- **Reflexion** (Shinn et al., 2023): Self-reflection prompts, verbal reinforcement, long-term memory
- **EvoFSM** (2024): Experience pools, strategy distillation

### 3. Architecture Influence: Claude-Reflect

**Repo**: `C:/code/repo-library/claude-reflect/`

Claude-Reflect contributes the **system architecture** -- how capture and processing are separated, how detection works, and how learnings route to targets.

#### Two-Stage Architecture

- **Stage 1 (Capture)**: 4 hooks fire during sessions, detect patterns via regex, append to JSON queue. Non-blocking (exit 0).
- **Stage 2 (Process)**: `/reflect` command loads queue, validates with semantic AI, presents to user, applies to CLAUDE.md files. Human approval gate.
- **Bridge**: `~/.claude/learnings-queue.json` connects stages asynchronously.

#### Four Hooks (`claude-reflect/hooks/hooks.json:2-47`)

1. `UserPromptSubmit` → `capture_learning.py` (correction detection)
2. `PreCompact` → `check_learnings.py` (queue backup before context loss)
3. `PostToolUse(Bash)` → `post_commit_reminder.py` (git commit trigger)
4. `SessionStart` → `session_start_reminder.py` (pending learnings notification)

#### Regex Detection Patterns (`claude-reflect/scripts/lib/reflect_utils.py:167-235`)

Five categories with confidence scores and decay:

| Category | Examples | Confidence | Decay |
|----------|----------|------------|-------|
| Explicit | `remember:` | 0.90 | 120 days |
| Guardrail | `don't add X unless`, `only change what I asked` | 0.85-0.90 | 90-120 days |
| Correction | `no,`, `that's wrong`, `I meant`, `use X not Y` | 0.70-0.85 | 60-120 days |
| Positive | `perfect!`, `exactly right` | 0.70 | 90 days |
| False Positive | Questions (`?$`), task requests (`please/can you`) | filtered | - |

#### Confidence Scoring (`reflect_utils.py:296-320`)

Pattern-count and length-based:
- "I told you" pattern: 0.85 confidence
- 3+ patterns matched: 0.85
- 2 patterns: 0.75
- 1 strong: 0.70
- 1 weak: 0.55
- Short message (<80 chars): +0.10 boost
- Long message (>300 chars): -0.15 reduction

#### Semantic AI Validation (`claude-reflect/scripts/lib/semantic_detector.py:41-119`)

Uses `claude -p --output-format json` to analyze messages during `/reflect`. Returns `{is_learning, type, confidence, reasoning, extracted_learning}`. Acts as a second-pass filter after regex capture. Takes the maximum of regex and semantic confidence scores (`semantic_detector.py:228-230`).

#### Multi-Target Writing (`claude-reflect/commands/reflect.md:21-58`)

Five write destinations:
1. Global CLAUDE.md (`~/.claude/CLAUDE.md`)
2. Project CLAUDE.md (`./CLAUDE.md`)
3. Subdirectory CLAUDE.md (auto-discovered via `find`)
4. Skill files (when correction relates to skill invocation)
5. AGENTS.md (with marker comments for safe updates)

#### Skill Improvement Routing (`reflect.md:773-816`)

When a correction follows a skill invocation (e.g., `/deploy`), the system detects context and offers to route the learning to the skill file itself. Creates a feedback loop: skills improve from usage corrections.

#### Queue Item Structure (`reflect_utils.py:327-346`)

```json
{
  "type": "auto|explicit|positive|guardrail",
  "message": "user's original text",
  "timestamp": "ISO8601",
  "project": "/path/to/project",
  "patterns": "matched pattern names",
  "confidence": 0.75,
  "sentiment": "correction|positive",
  "decay_days": 90
}
```

### 4. Validation Rules: Anthropic Official

**Repo**: `C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py`

Any skills generated by `learning-from-sessions` must pass these constraints:

| Field | Rule | Reference |
|-------|------|-----------|
| `name` | `^[a-z0-9-]+$`, max 64 chars, no leading/trailing/consecutive hyphens | `quick_validate.py:64-71` |
| `description` | Max 1024 chars, no angle brackets (`<` or `>`) | `quick_validate.py:73-84` |
| Frontmatter keys | Only: `name`, `description`, `license`, `allowed-tools`, `metadata` | `quick_validate.py:41-50` |
| Required fields | `name` and `description` | `quick_validate.py:52-56` |
| Format | YAML dict between `---` delimiters | `quick_validate.py:21-39` |

### 5. Former Learn Skill vs. Blueprint

**Note**: The old `learn` skill has been replaced by the implemented `learning-from-sessions` skill.

The former `learn` skill (`newskills/learn/SKILL.md`, 172 lines) was a simpler predecessor:

| Feature | Current `learn` | Blueprint `learning-from-sessions` |
|---------|----------------|--------------------------------------|
| Trigger | Manual only (`/learn` or natural language) | Manual + automatic (hook + semantic) |
| Dedup check | None | rg search across skill dirs with decision matrix |
| Web research | None | Step 3: search for best practices |
| Description optimization | None | Dedicated reference file on writing retrieval keys |
| Quality gates | Basic worth-assessment (4 criteria) | 9-item checklist + anti-patterns |
| Self-reflection | None | 5 introspection questions post-task |
| Output format | Simple markdown (Problem, Solution, Example, When to Use) | Full 7-section template (adds Verification, Notes, References) |
| Output validation | None | Anthropic validator compliance |
| Versioning | None | Semantic versioning on extracted skills |
| Storage | `~/.claude/skills/learned/` flat files | `.claude/skills/` (project) or `~/.claude/skills/` (user) |
| Reference docs | `newreference/pattern-learning.md` (56 lines) | 4 reference files in `reference/` subdirectory |

The blueprint represents a significant expansion: from a 172-line manual extraction tool to a 250-350 line workflow skill backed by 4 reference documents and a template.

### 6. Proposed Output Structure

```
newskills/learning-from-sessions/
├── SKILL.md                              # Core workflow (250-350 lines)
├── reference/
│   ├── extraction-workflow.md            # Detailed 6-step process with examples
│   ├── quality-gates.md                  # Checklist, anti-patterns, when NOT to extract
│   ├── description-optimization.md       # How to write descriptions for semantic retrieval
│   └── research-foundations.md           # Academic papers informing the design
└── templates/
    └── extracted-skill-template.md       # Standard template for generated skills
```

**SKILL.md content plan** (from blueprint lines 101-198):
- When to Activate (5 automatic trigger conditions)
- Self-Reflection Prompts (5 questions)
- Step 1: Check for Existing Skills (dedup-first with rg)
- Step 2: Identify the Knowledge (4 analysis questions)
- Step 3: Research Best Practices (web search when appropriate)
- Step 4: Structure and Save (template + description optimization)
- Step 5: Quality Gates (9-item checklist + anti-patterns)
- Retrospective Mode (explicit /learn invocation: review, identify, prioritize, extract, summarize)
- Output Decision (skill file vs CLAUDE.md entry)
- Optional hook for automatic activation

### 7. The Implementation Prompt

The blueprint concludes with a copy-paste prompt (lines 207-257) for a separate Claude Code session. It prescribes:

**Pre-read requirements** (3 research files + 10 repo files + blueprint itself):
- All 3 research docs (Claudeception, continuous-learning, Claude-Reflect)
- Claudeception: SKILL.md, activator script, skill template, research references, all 3 examples
- Claude-Reflect: reflect.md, reflect-skills.md, reflect_utils.py, semantic_detector.py, hooks.json

**12 implementation requirements**:
1. Frontmatter with name=learning-from-sessions, multi-trigger description
2. Combine Claudeception's 6-step extraction with Claude-Reflect's two-stage concept
3. Include 5 self-reflection prompts
4. Include dedup-first check
5. Include quality gates and anti-patterns
6. Include web research step
7. Output decision: skill file vs CLAUDE.md entry
8. Template follows Claudeception structure (Problem, Context, Solution, Verification, Example, Notes, References)
9. Description optimization guide for semantic matching
10. SKILL.md under 350 lines, depth in reference/ files
11. Do NOT copy verbatim -- synthesize
12. Reference `creating-skills` skill for validation rules

## Code References

- `.docs/plans/learning-from-sessions-blueprint.md:1-258` - Full blueprint specification
- `newskills/learn/SKILL.md:1-172` - Existing simpler learn skill
- `newreference/pattern-learning.md:1-56` - Current pattern learning reference
- `C:/code/repo-library/Claudeception/SKILL.md:66-223` - 6-step extraction workflow
- `C:/code/repo-library/Claudeception/SKILL.md:236-244` - Self-reflection prompts
- `C:/code/repo-library/Claudeception/SKILL.md:257-277` - Quality gates + anti-patterns
- `C:/code/repo-library/Claudeception/scripts/claudeception-activator.sh:12-39` - Forced eval hook
- `C:/code/repo-library/Claudeception/resources/skill-template.md:1-96` - Output template
- `C:/code/repo-library/Claudeception/resources/research-references.md:5-169` - Academic foundation
- `C:/code/repo-library/Claudeception/examples/` - 3 example extracted skills
- `C:/code/repo-library/claude-reflect/commands/reflect.md:21-58` - Multi-target sync
- `C:/code/repo-library/claude-reflect/commands/reflect.md:773-816` - Skill improvement routing
- `C:/code/repo-library/claude-reflect/scripts/lib/reflect_utils.py:167-235` - Regex patterns (5 categories)
- `C:/code/repo-library/claude-reflect/scripts/lib/reflect_utils.py:237-324` - Confidence scoring
- `C:/code/repo-library/claude-reflect/scripts/lib/reflect_utils.py:327-346` - Queue item creation
- `C:/code/repo-library/claude-reflect/scripts/lib/semantic_detector.py:41-119` - Semantic analysis
- `C:/code/repo-library/claude-reflect/hooks/hooks.json:2-47` - 4 hook definitions
- `C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py:12-87` - Validation rules

## Architecture Notes

### Pattern: Progressive Disclosure (3-Level Loading)

The Anthropic skills system loads skills in 3 levels:
- **Level 1**: Name + description (~100 tokens) -- always in context
- **Level 2**: SKILL.md body (<500 lines) -- loaded when skill triggers
- **Level 3**: Bundled resources (unlimited) -- loaded on demand via Read tool

This means the `description` field is the PRIMARY triggering mechanism. The blueprint's `description-optimization.md` reference file exists specifically to teach writing descriptions as "retrieval keys" for semantic matching.

### Pattern: Dedup-First with Decision Matrix

Before creating any new skill, search existing skill directories with `rg`. The decision matrix has 6 outcomes:

| Found | Action |
|-------|--------|
| Nothing related | Create new skill |
| Same trigger and fix | Update existing (version bump) |
| Same trigger, different cause | Create new + cross-links |
| Partial overlap | Add variant subsection |
| Same domain, different problem | Create new + `See also:` link |
| Stale or wrong | Deprecate + create replacement |

### Pattern: Two-Stage Capture/Process with Queue Bridge

Claude-Reflect's architecture separates real-time capture (hooks, regex, non-blocking) from batch processing (command, semantic AI, human approval). The queue JSON file bridges the two stages asynchronously. The blueprint adopts this concept but makes the hook optional (lines 183-198).

### Pattern: Hybrid Detection (Fast Regex + Accurate Semantic)

Real-time capture uses regex for speed and zero API cost. Batch processing uses `claude -p --output-format json` for accuracy. The maximum of both confidence scores is used. Graceful fallback: if semantic fails, regex results are kept.

### Pattern: Skill Improvement Routing

When a correction is detected during/after skill invocation, the system routes the learning back to the skill file rather than CLAUDE.md. This creates a feedback loop where skills improve from usage.

## Open Questions (Resolved)

1. **Relationship to existing `learn` skill**: RESOLVED - The `learning-from-sessions` skill replaced `newskills/learn/`. The old skill was deleted and is no longer present in the codebase.

2. **Hook implementation**: OPEN - The implemented skill does not include the `UserPromptSubmit` hook. Activation depends on semantic matching and explicit `/learn` invocation. The forced eval hook concept was not adopted.

3. **Queue infrastructure**: RESOLVED - The implementation uses on-demand workflow only, not the capture-then-process queue architecture from Claude-Reflect.

4. **Reference to `creating-skills`**: RESOLVED - The `creating-skills` skill now exists at `newskills/creating-skills/` with full validation rules and templates.

5. **Deployment overlap**: RESOLVED - Since the old `learn` skill was deleted, there is no overlap concern.
