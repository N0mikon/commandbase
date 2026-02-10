---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Removed duplicate plans file (.docs/plans/creating-skills-blueprint.md) - archive is the authoritative copy"
topic: "Creating-Skills Blueprint: Active Skill Creator Analysis"
tags: [research, creating-skills, skill-builder, meta-skill, anthropic, validation, templates]
status: archived
implementation_status: implemented
implementation_commit: a7794e1
archived: 2026-02-09
archive_reason: "Blueprint fully implemented (commit a7794e1) and skill shipped. Skill moved from newskills/creating-skills/ to plugins/commandbase-meta/skills/creating-skills/ in commit 87a19a3 (marketplace restructure). Old newskills path deleted. Referenced research docs archived."
references:
  - .docs/archive/01-28-2026-metaskills-skill-builder.md
  - .docs/research/01-28-2026-claude-meta-skill-repo.md
  - .docs/research/01-28-2026-anthropic-skills-repo.md
  - .docs/archive/01-28-2026-skill-factory-workflow.md
  - .docs/archive/01-28-2026-agent-skill-creator-workflow.md
  - .docs/research/01-28-2026-skillcreator-repos.md
  - C:/code/repo-library/skill-builder/SKILL.md
  - C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/SKILL.md
  - C:/code/repo-library/skills/skills/skill-creator/SKILL.md
  - plugins/commandbase-meta/skills/creating-skills/SKILL.md
---

# Research: Creating-Skills Blueprint

**Date**: 2026-01-28
**Branch**: master

## Research Question

Analyze the `creating-skills-blueprint.md` plan document and all its referenced influences to document: the active creator trigger model, the primary influences (Skill Builder description formula/gerund naming, Claude Meta-Skill templates/freedom tiers, Anthropic validation rules), the proposed output structure (SKILL.md + 4 reference files + 2 templates), and the prompt at the bottom.

## Summary

**Implementation Status**: The blueprint has been fully implemented. The `creating-skills` skill now exists at `plugins/commandbase-meta/skills/creating-skills/` (originally at `newskills/creating-skills/`, moved in commit `87a19a3` during the marketplace restructure). See commit `a7794e1` for the original implementation.

The blueprint at `.docs/plans/creating-skills-blueprint.md` designs a meta-skill (`creating-skills`) that activates when a user wants to build, edit, or convert Claude Code skills. It synthesizes patterns from 5 community repos and 1 official Anthropic repo into a unified workflow. The output structure is `SKILL.md` (200-300 lines) + `reference/` (4 files) + `templates/` (2 files). The blueprint includes a copy-paste prompt (lines 127-178) for executing the build in a separate Claude Code session.

The three primary influences contribute distinct capabilities:
- **Skill Builder** (metaskills): Description writing formula, gerund naming convention, sub-agent conversion workflow, progressive disclosure pattern
- **Claude Meta-Skill** (YYH211): Basic + Workflow templates, freedom-tier model (High/Medium/Low), good/bad example pairs, quality checklist
- **Anthropic Official** (anthropics/skills): Validation rules (name regex, description max 1024, 5 allowed frontmatter keys), packaging scripts, three-level progressive disclosure spec

## Detailed Findings

### 1. Blueprint Structure

The blueprint (`.docs/plans/creating-skills-blueprint.md`, 179 lines) is organized into:

| Section | Lines | Content |
|---------|-------|---------|
| Purpose | 9-11 | Three modes: create new, edit existing, convert sub-agent |
| Research Files | 15-22 | Links to 6 research documents |
| Cloned Repos | 24-30 | Paths to 5 local repo clones |
| What to Take | 34-66 | Specific patterns from each influence |
| Proposed Structure | 69-82 | File tree for the skill |
| Frontmatter | 84-91 | YAML name + description |
| Core Workflow | 93-124 | 5-step process |
| Prompt | 127-178 | Copy-paste prompt for separate session |

### 2. Active Creator Trigger Model

The blueprint defines the skill's activation via its description field (lines 88-90):

```yaml
description: Use this skill when creating new Claude Code skills from scratch, editing
  existing skills to improve their structure or descriptions, or converting Claude Code
  sub-agents into skills. This includes writing SKILL.md files, choosing skill names,
  crafting invocation-focused descriptions, organizing supporting files with progressive
  disclosure, and validating skill structure against the official specification.
```

**Trigger keywords embedded**: "creating", "skills", "editing", "structure", "descriptions", "converting", "sub-agents", "SKILL.md", "skill names", "invocation-focused", "progressive disclosure", "validating", "specification"

**Three activation modes** (blueprint lines 9-11, 96-98):
1. **Create New** - Building a skill from scratch
2. **Edit Existing** - Improving structure, descriptions, or organization
3. **Convert Sub-Agent** - Migrating a sub-agent to skill format

### 3. Primary Influence: Skill Builder (metaskills)

**Source repo**: `C:/code/repo-library/skill-builder/`
**Research doc**: `.docs/research/01-28-2026-metaskills-skill-builder.md`
**Total lines across all files**: 2,931

#### Description Writing Formula

Defined in `skill-builder/SKILL.md:80-86` and `skill-builder/reference/metadata-requirements.md:60-64`:

```
Use this skill when [primary situation]. This includes [specific use cases with trigger
keywords], [more use cases], and [edge cases].
```

Key principles from `metadata-requirements.md:48-90`:
- Description is "THE MOST CRITICAL field" - determines when Claude invokes the skill
- Start with "Use this skill when..." (not "This skill can...")
- Include trigger keywords users might say
- Write in third person (not first person)
- Think from Claude's perspective: "When would I know to use this?"
- Max 1024 characters

#### Gerund Naming Convention

Defined in `skill-builder/SKILL.md:77-79` and `skill-builder/reference/metadata-requirements.md:20-44`:

| Good (gerund) | Bad (noun) |
|----------------|------------|
| `processing-pdfs` | `pdf-processor` |
| `analyzing-spreadsheets` | `spreadsheet-analyzer` |
| `deploying-lambdas` | `lambda-tool` |

Format: verb + -ing + noun, lowercase, hyphens only, max 64 chars

#### Sub-Agent Conversion Workflow

Detailed in `skill-builder/converting-sub-agents-to-skills.md` (627 lines):

- **Key insight** (line 83-86): Sub-agents explain WHAT they are (noun forms: `code-reviewer`), skills explain WHEN to use them (gerund forms: `reviewing-code`)
- Three complete conversion examples (lines 157-487)
- Conversion checklist (lines 488-507)
- Common issues and solutions (lines 538-585)

#### Progressive Disclosure Pattern

From `skill-builder/reference/skill-best-practices.md:49-106`:
- SKILL.md: <500 lines target, core workflow only
- Reference files: "Fat" files with comprehensive details
- "Skinny pointers": `See ./reference/filename.md for [description]`
- Max 1 level deep from SKILL.md
- Intention-revealing file names (NOT `reference.md`, `helpers.md`, `utils.md`)

#### File Inventory

| File | Lines | Purpose |
|------|-------|---------|
| `SKILL.md` | 274 | Core skill instructions and overview |
| `converting-sub-agents-to-skills.md` | 627 | Conversion guide with 3 examples |
| `reference/editing-skills-guide.md` | 473 | Editing workflows and improvements |
| `reference/metadata-requirements.md` | 231 | Name and description requirements |
| `reference/nodejs-and-cli-patterns.md` | 578 | CLI tools and Node.js ESM patterns |
| `reference/skill-best-practices.md` | 575 | Best practices and anti-patterns |
| `reference/skill-structure-and-format.md` | 173 | Directory and file structure |

### 4. Primary Influence: Claude Meta-Skill (YYH211)

**Source repo**: `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/`
**Research doc**: `.docs/research/01-28-2026-claude-meta-skill-repo.md`

#### Freedom-Tier Model

Defined in `create-skill-file-EN/SKILL.md:90-102`:

| Tier | Use Case | Writing Approach |
|------|----------|-----------------|
| **High** | Creative tasks, multiple valid solutions | Guiding principles, not specific steps |
| **Medium** | Standard tasks, recommended patterns | Parameterized examples, default flows |
| **Low** | Error-prone, strict execution required | Step-by-step scripts, exact commands |

Decision criteria (`SKILL.md:98-102`):
- Clear "correct answer"? → Low freedom
- Needs to adapt to scenarios? → High freedom
- High cost of errors? → Low freedom

#### Basic Skill Template

`create-skill-file-EN/templates/basic-skill-template.md` (95 lines):
- YAML frontmatter placeholder
- Title + one-line summary
- "When to Use" with 4 trigger bullet patterns
- Quick Start code block
- "How It Works" (3 numbered steps)
- Examples (Basic + Advanced usage)
- Best Practices (do/don't checklist)
- Troubleshooting (problem/solution pairs)

#### Workflow Skill Template

`create-skill-file-EN/templates/workflow-skill-template.md` (402 lines):
- ASCII art flowchart diagram
- Preparation Phase with failure handling
- Multi-step workflow with decision points and validation at each step
- Error Handling with 3 categories (Recoverable / User Input Needed / Critical)
- Rollback Procedure (4-step process)
- Workflow Variations (Quick Mode vs Strict Mode)
- Monitoring and structured logging
- Post-workflow report template
- Testing with `--dry-run` and `--inject-error`

#### Good/Bad Example Pairs

`create-skill-file-EN/examples/good-example.md` (908 lines) - 3 complete good examples:
1. **Database Migration** - measurable criteria, multi-complexity examples
2. **API Documentation** - 4-phase workflow, multi-framework support
3. **Code Review** - high-freedom guiding principles, priority severity framework

`create-skill-file-EN/examples/bad-example.md` (867 lines) - 3 anti-patterns with fixes:
1. **Overly Vague** (`helper` → `python-code-refactoring`) - generic name/description
2. **Overly Verbose** (`python-basics` → `project-python-conventions`) - teaching Claude what it already knows
3. **Lacking Context** (`deployment` → `deploy-to-production`) - abstract steps without commands

Teaching patterns demonstrated:
- Specificity over generality
- Project-specific vs general knowledge
- Executable vs abstract instructions
- Verification criteria with measurable thresholds
- Error recovery procedures

#### Quality Checklist (5 Categories)

From `create-skill-file-EN/SKILL.md:365-403`:

1. **Core Quality** - name conventions, description triggers, no redundancy
2. **Functional Completeness** - "When to Use" section, 2-3 examples, error handling
3. **Structure Standards** - TOC for >200 lines, nesting ≤1 level, forward slashes
4. **Scripts and Templates** - usage instructions, error handling, no magic numbers
5. **Final Check** - read-through, test triggering, appropriate length

#### 4C Description Principles

From `create-skill-file-EN/SKILL.md:207-212`:
1. **Clear** - avoid jargon and vague terms
2. **Concise** - 1-2 sentences for core functionality
3. **Contextual** - describe applicable scenarios
4. **Complete** - functionality + trigger conditions

### 5. Primary Influence: Anthropic Official (anthropics/skills)

**Source repo**: `C:/code/repo-library/skills/`
**Research doc**: `.docs/research/01-28-2026-anthropic-skills-repo.md`

#### Validation Rules (quick_validate.py)

From `skills/skill-creator/scripts/quick_validate.py:12-86`:

| Rule | Spec | Line |
|------|------|------|
| SKILL.md exists | Required in skill directory | 16-19 |
| Frontmatter format | Must start with `---`, valid YAML dict | 22-39 |
| Allowed properties | `{name, description, license, allowed-tools, metadata}` only | 41-50 |
| Name required | String type, stripped | 52-62 |
| Name format | `^[a-z0-9-]+$`, no start/end `-`, no `--` | 64-68 |
| Name length | Max 64 characters | 69-71 |
| Description required | String type, stripped | 73-77 |
| No angle brackets | `<` and `>` forbidden in description | 79-81 |
| Description length | Max 1024 characters | 82-84 |

#### Three-Level Progressive Disclosure

From `skills/skill-creator/SKILL.md:114-201`:

| Level | When Loaded | Size Limit | Content |
|-------|-------------|------------|---------|
| 1. Metadata | Always in context | ~100 words | name + description |
| 2. SKILL.md body | When skill triggers | <5k words, <500 lines | Instructions |
| 3. Bundled resources | As needed by Claude | Unlimited | scripts/, references/, assets/ |

Critical insight (line 309-311): Description is the **primary triggering mechanism**. All "when to use" guidance MUST be in the description, not the body.

#### Packaging Pipeline

From `skills/skill-creator/scripts/package_skill.py:19-82`:
1. Validate skill folder exists
2. Check SKILL.md exists
3. **Mandatory validation** via `validate_skill()` - cannot skip
4. Create ZIP with `.skill` extension using `ZIP_DEFLATED`
5. Preserve directory structure with relative paths

#### Official Skill Patterns Observed

Across 16 official skills:
- Average SKILL.md length: 212 lines (range: 32-483)
- 15/16 include `license` field
- 0/16 use `allowed-tools` or `metadata` fields
- Description lengths: 194-383 characters (well under 1024 limit)
- Directory naming varies: some use `references/`, some use `reference/` (singular), some put docs at skill root

#### What NOT to Include in Skills

From `skills/skill-creator/SKILL.md:102-112`:
- No README.md
- No INSTALLATION_GUIDE.md
- No QUICK_REFERENCE.md
- No CHANGELOG.md
- Only information needed for the AI agent to do the job

### 6. Secondary Influences

#### Skill Factory (alirezarezvani)

**Research doc**: `.docs/research/01-28-2026-skill-factory-workflow.md`

Key contributions to the blueprint:
- **Build → Validate → Install pipeline** (blueprint line 65-66): Explicit quality gates between stages
- **Composability principle**: Output from one skill feeds into another
- **Two-tier delegation**: Lightweight orchestrator → specialist agents → factory templates

#### Agent Skill Creator (FrancyJGLisboa)

**Research doc**: `.docs/research/01-28-2026-agent-skill-creator-workflow.md`

Key contributions to the blueprint:
- **DECISIONS.md convention** (blueprint line 59): Document every architectural choice with rationale
- **Quality standards**: "Production-ready, not prototype" - no TODOs, no placeholders
- **6-phase protocol**: Discovery → Design → Architecture → Detection → Implementation → Testing

### 7. Proposed Output Structure

The blueprint proposes this file tree (lines 71-82):

```
plugins/commandbase-meta/skills/creating-skills/
├── SKILL.md                              # Core workflow (241 lines)
├── reference/
│   ├── validation-rules.md               # Official spec constraints (from Anthropic)
│   ├── description-writing-guide.md      # Formula + good/bad examples
│   ├── naming-conventions.md             # Gerund form, kebab-case rules
│   └── converting-subagents.md           # Sub-agent to skill migration
└── templates/
    ├── basic-skill-template.md           # Simple skills
    └── workflow-skill-template.md         # Multi-step process skills
```

> **Note (2026-02-09)**: The blueprint originally proposed this under `newskills/creating-skills/`. It was implemented there in commit `a7794e1`, then moved to the plugin structure in commit `87a19a3`.

**How this differed from the original newskills patterns**:

At the time of writing, the 11 existing skills in `newskills/` were all flat: one `SKILL.md` per directory, no subdirectories. The `creating-skills` skill was the first to use `reference/` and `templates/` subdirectories. This is consistent with the progressive disclosure pattern from all three primary influences, which recommend keeping SKILL.md lean (200-300 lines) and putting depth into supporting files.

| File | Source Influence | Content |
|------|-----------------|---------|
| `SKILL.md` | All three | 5-step workflow, frontmatter, freedom tiers, three modes |
| `validation-rules.md` | Anthropic `quick_validate.py` | Name regex, description limits, allowed frontmatter keys |
| `description-writing-guide.md` | Skill Builder `metadata-requirements.md` | Formula + examples from Meta-Skill good/bad pairs |
| `naming-conventions.md` | Skill Builder gerund convention | Gerund form rules, kebab-case, max 64 chars |
| `converting-subagents.md` | Skill Builder `converting-sub-agents-to-skills.md` | WHAT→WHEN transformation, checklist |
| `basic-skill-template.md` | Meta-Skill basic template | Adapted from 95-line template |
| `workflow-skill-template.md` | Meta-Skill workflow template | Adapted from 402-line template |

### 8. Core Workflow (5 Steps)

From blueprint lines 95-124:

**Step 1: Gather Requirements** (lines 96-99)
- What task? When should Claude invoke? Personal vs project? Similar existing skills?

**Step 2: Choose Freedom Level** (lines 101-104)
- High freedom: creative tasks → guiding principles
- Medium freedom: standard tasks → parameterized examples
- Low freedom: error-prone tasks → step-by-step scripts

**Step 3: Design the Skill** (lines 106-110)
- Name: gerund form, max 64 chars, kebab-case
- Description: "Use this skill when..." formula, max 1024 chars
- Template: Basic or Workflow
- Plan supporting files

**Step 4: Create the Skill** (lines 112-116)
- Write SKILL.md with YAML frontmatter
- Keep under 500 lines (ideally 200-300)
- Add reference files, add scripts if needed

**Step 5: Validate** (lines 118-123)
- Name regex: `^[a-z0-9-]+$`, no start/end `-`, no `--`, max 64 chars, gerund form
- Description: max 1024 chars, no angle brackets, trigger keywords, third person
- SKILL.md: under 500 lines, clear "When to Use" section
- Reference depth: max 1 level
- No extraneous files

### 9. The Build Prompt

Blueprint lines 127-178 contain a copy-paste prompt for a separate Claude Code session. It instructs Claude to:

1. Read 3 research files and key files from 3 reference repos before writing
2. Use the blueprint as the master plan
3. Create the 7-file structure
4. Follow 9 explicit requirements:
   - Frontmatter: name=creating-skills, description focused on WHEN to invoke
   - Three modes: Create / Edit / Convert
   - Freedom-tier model from Claude Meta-Skill
   - Skill Builder description formula as standard
   - Anthropic validation rules from `quick_validate.py`
   - Templates adapted from Claude Meta-Skill
   - Good/bad examples in description writing guide
   - Keep SKILL.md under 300 lines
   - **Do NOT copy content verbatim** - synthesize original content

### 10. Conflicts Between Influences (Resolved in Blueprint)

| Conflict | Skill Builder | Meta-Skill | Anthropic | Blueprint Resolution |
|----------|--------------|------------|-----------|---------------------|
| Naming convention | Strictly gerund | Recommends gerund, not enforced | Hyphen-case, no gerund req. | Gerund form (follows Skill Builder) |
| Script language | Node.js only, Python forbidden | Python-friendly | Python for tooling | Not specified (implicit: either) |
| `allowed-tools` field | Explicitly prohibited | Not mentioned | Allowed but unused | Not included in frontmatter |
| SKILL.md length | <500 (ideally 150-200) | 200-500, split at 500 | <500 lines, <5k words | 200-300 lines target |
| Description formula | "Use this skill when..." | 4C principles | "[What]. [When]." pattern | Skill Builder formula as primary |

## Code References

- `.docs/plans/creating-skills-blueprint.md:1-179` - Full blueprint
- `.docs/plans/creating-skills-blueprint.md:88-90` - Proposed description/trigger
- `.docs/plans/creating-skills-blueprint.md:127-178` - Copy-paste prompt
- `C:/code/repo-library/skill-builder/SKILL.md:77-86` - Gerund naming + description formula
- `C:/code/repo-library/skill-builder/reference/metadata-requirements.md:60-64` - Description writing template
- `C:/code/repo-library/skill-builder/converting-sub-agents-to-skills.md:83-86` - WHAT→WHEN key insight
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/SKILL.md:90-102` - Freedom-tier model
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/SKILL.md:365-403` - Quality checklist
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/templates/basic-skill-template.md:1-95` - Basic template
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/templates/workflow-skill-template.md:1-402` - Workflow template
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/examples/good-example.md:1-908` - 3 good examples
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/examples/bad-example.md:1-867` - 3 bad examples with fixes
- `C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py:12-86` - Validation function
- `C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py:42` - ALLOWED_PROPERTIES set
- `C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py:65` - Name regex pattern
- `C:/code/repo-library/skills/skills/skill-creator/SKILL.md:114-201` - Progressive disclosure spec
- `C:/code/repo-library/skills/skills/skill-creator/SKILL.md:279-318` - SKILL.md writing guidelines
- `.docs/research/01-28-2026-metaskills-skill-builder.md` - Skill Builder analysis
- `.docs/research/01-28-2026-claude-meta-skill-repo.md` - Meta-Skill analysis
- `.docs/research/01-28-2026-anthropic-skills-repo.md` - Anthropic official analysis
- `.docs/research/01-28-2026-skill-factory-workflow.md` - Factory pipeline analysis
- `.docs/research/01-28-2026-agent-skill-creator-workflow.md` - 6-phase protocol analysis

## Architecture Notes

### How This Fits Into commandbase

> **Note (2026-02-09)**: The `newskills/` directory no longer exists. All skills were migrated to the plugin structure under `plugins/` in commit `87a19a3`.

At the time of writing, the `creating-skills` directory was the first skill in `newskills/` to use subdirectories (`reference/` and `templates/`). All 11 existing skills were flat single-file SKILL.md structures. This was by design: the meta-skill needs supporting reference material to guide skill creation, while the existing workflow skills (commit, pr, rcode, etc.) are self-contained processes.

### Pattern Inheritance

The existing skills (originally in `newskills/`, now in `plugins/`) share an enforcement pattern (Iron Law, Gate Function, Red Flags, Rationalization Prevention) that the blueprint does not explicitly include. The blueprint's 5-step workflow is more process-oriented than enforcement-oriented. The prompt instructs the builder to follow the Skill Builder's structure as the PRIMARY model, which uses a different organizational pattern (Role → Core Knowledge → Process → Best Practices → Approach).

### Frontmatter Differences

At the time of writing, existing skills used `description` only (with optional `model: opus`). The blueprint uses `name` + `description`, which aligns with the Anthropic spec and all three primary influences. This is the correct approach per `quick_validate.py:52-55` which requires both fields. All skills now use `name` + `description` in frontmatter.

### The `creating-skills` Skill Directory

**Updated 2026-02-01**: The skill has been implemented. **Updated 2026-02-09**: Now located at `plugins/commandbase-meta/skills/creating-skills/` (moved from `newskills/creating-skills/` in commit `87a19a3`). The directory contains:
- `SKILL.md` (241 lines) - Core workflow with Iron Law, Gate Function, and Rationalization Prevention
- `reference/` - 4 files: validation-rules.md, description-writing-guide.md, naming-conventions.md, converting-subagents.md
- `templates/` - 2 files: basic-skill-template.md, workflow-skill-template.md

This matches the proposed structure from the blueprint (Section 7).

## Open Questions (Resolved)

The blueprint was implemented in commit `a7794e1` (2026-01-28). The following questions have been resolved:

1. **Should creating-skills adopt the Iron Law / Gate Function / Rationalization Prevention enforcement pattern** used by all other newskills, or follow the Skill Builder's organizational pattern as the prompt instructs?
   - **RESOLVED**: The implementation adopted the Iron Law / Gate Function / Rationalization Prevention pattern (SKILL.md lines 12, 26, 195), integrating it with the Skill Builder's process-oriented workflow. This hybrid approach uses the enforcement structure from existing newskills while incorporating the 5-step workflow from the blueprint.

2. **Gerund naming strictness**: The blueprint mandates gerund form (from Skill Builder), but Anthropic's 16 official skills don't follow this. Should the creating-skills skill recommend gerund form or allow flexibility?
   - **RESOLVED**: The implementation recommends gerund form as the default convention but provides guidance in `reference/naming-conventions.md`. The enforcement is recommendation-level, not mandatory.

3. **Python vs Node.js scripts**: The blueprint is silent on this. Skill Builder forbids Python; Anthropic uses Python for its validation tools. The creating-skills skill may need to take a position.
   - **RESOLVED**: The implementation does not take a hard position on script language. The skill focuses on structure and description quality, leaving implementation language flexible.

4. **Frontmatter field `name`**: Existing newskills omit `name` from frontmatter (using only `description`). The blueprint includes it. This creates an inconsistency - should existing skills be updated?
   - **RESOLVED**: The implementation uses `name: creating-skills` in frontmatter. All skills migrated in commit `a7794e1` now use the `name` field, establishing consistency across the codebase.

5. **Template adaptation depth**: The blueprint says "DO NOT copy content verbatim - synthesize." How much should the Basic and Workflow templates diverge from the Claude Meta-Skill originals?
   - **RESOLVED**: The templates in `templates/` are significantly adapted, keeping the structural concepts while rewriting content to match the enforcement patterns used in this codebase.
