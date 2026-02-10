---
git_commit: 8e92bba
last_updated: 2026-01-28
last_updated_by: rcode
topic: "YYH211/Claude-meta-skill - Skill Collection and Meta-Skill Creator"
tags: [research, skill-creation, meta-skill, templates, quality-checklists, claude-code-skills]
status: complete
references:
  - https://github.com/YYH211/Claude-meta-skill
  - create-skill-file-EN/SKILL.md
  - create-skill-file-EN/templates/basic-skill-template.md
  - create-skill-file-EN/templates/workflow-skill-template.md
  - create-skill-file-EN/examples/good-example.md
  - create-skill-file-EN/examples/bad-example.md
  - create-skill-file/SKILL.md
  - README.md
---

# Research: YYH211/Claude-meta-skill - Skill Collection and Meta-Skill Creator

**Date**: 2026-01-28
**Branch**: master
**Repo**: https://github.com/YYH211/Claude-meta-skill
**Author**: YYH211

## Research Question

How does the Claude-meta-skill repository implement its skill creation workflow? What templates, patterns, quality checklists, and conventions does it use? How does it compare to other skill creator approaches like metaskills/skill-builder?

## Summary

Claude-meta-skill is a **curated skill collection** (9 skills) with a standout **meta-skill** (`create-skill-file`) that teaches Claude how to create other skills. The meta-skill provides two templates (Basic and Workflow), good/bad examples, a quality checklist, and comprehensive writing guidelines. The repo also includes domain-specific skills for frontend design, prompt optimization, DRY refactoring, MCP building, AI news aggregation, FastGPT workflow generation, deep reading analysis, and Manus-style file planning. Available in both Chinese and English versions.

## Repository Structure

```
Claude-meta-skill/
├── README.md                          # Comprehensive README (installation, all skills documented)
├── .gitignore                         # Ignores .claude/ and fastgpt_output/
├── create-skill-file/                 # Meta-skill (Chinese) - 475 lines
│   ├── SKILL.md
│   ├── templates/
│   │   ├── basic-skill-template.md    # Basic template
│   │   └── workflow-skill-template.md # Workflow template
│   └── examples/
│       ├── good-example.md            # 3 good examples
│       └── bad-example.md             # 3 bad examples + fixes
├── create-skill-file-EN/             # Meta-skill (English) - 474 lines
│   ├── SKILL.md
│   ├── templates/
│   │   ├── basic-skill-template.md    # 94 lines
│   │   └── workflow-skill-template.md # 401 lines
│   └── examples/
│       ├── good-example.md            # 907 lines
│       └── bad-example.md             # 866 lines
├── daily-ai-news/                    # AI news aggregator - 327 lines
│   ├── SKILL.md
│   └── references/ (3 files)
├── deep-reading-analyst/             # 10+ thinking framework analysis - 501 lines
│   ├── SKILL.md
│   └── references/ (10 files)
├── dry-refactoring/                  # DRY code refactoring - 964 lines
│   └── SKILL.md
├── fastgpt-workflow-generator/       # FastGPT JSON workflow gen - 754 lines
│   ├── SKILL.md
│   ├── LESSONS_LEARNED.md
│   ├── references/ (4 files)
│   ├── templates/ (4 JSON + README)
│   └── scripts/validate_workflow.js
├── frontend-design/                  # Frontend UI design - 491 lines
│   └── SKILL.md
├── mcp-builder/                      # MCP server building guide - 236 lines
│   ├── SKILL.md
│   ├── LICENSE.txt
│   ├── reference/ (4 files)
│   └── scripts/ (3 files)
├── planning-with-files/              # Manus-style file planning - 160 lines
│   ├── SKILL.md
│   ├── reference.md
│   └── examples.md
├── prompt-optimize/                  # Prompt engineering - 242 lines
│   └── SKILL.md
├── skill-intro/                      # Skill introduction docs
│   └── depp-reading-analyst-intro.md
├── workflow_temple/                  # FastGPT workflow JSON templates (10 files)
└── fastgpt_output/                   # Generated FastGPT outputs
```

## Detailed Findings

### The Meta-Skill: create-skill-file

The core meta-skill (`create-skill-file-EN/SKILL.md:1-474`) teaches Claude how to create high-quality SKILL.md files. It uses a `name` + `description` frontmatter pattern (no `model` field).

#### Frontmatter Convention

```yaml
---
name: create-skill-file
description: Guides Claude in creating well-structured SKILL.md files following best practices. Provides clear guidelines for naming, structure, and content organization to make skills easy to discover and execute.
---
```

Only two fields used across all skills: `name` and `description`. One exception: `mcp-builder` adds a `license` field (`SKILL.md:4`).

#### 3-Step Quick Start (`SKILL.md:16-45`)

1. Create directory: `mkdir -p .claude/skill/your-skill-name`
2. Create SKILL.md with YAML frontmatter
3. Test with trigger keywords

#### Core Principles (`SKILL.md:49-102`)

**Principle 1: Keep It Concise** - Only add knowledge Claude doesn't already have. No general programming knowledge. Project-specific workflows, naming conventions, and custom tool usage only.

**Principle 2: Set Appropriate Freedom** - Three-tier freedom model:

| Freedom | Use Case | Writing Approach |
|---------|----------|------------------|
| High | Creative, multiple solutions | Guiding principles, not specific steps |
| Medium | Recommended patterns with variations | Parameterized examples and default flows |
| Low | Error-prone, strict execution | Detailed step-by-step or scripts |

Decision criteria: Is there a clear "correct answer"? (Low freedom). Needs adaptation? (High freedom). High error cost? (Low freedom).

**Principle 3: Progressive Disclosure** - SKILL.md (200-500 lines) + reference.md + examples.md + scripts/. Rule: SKILL.md > 500 lines means split. Sub-files > 100 lines need table of contents. Reference depth max 1 level.

#### Naming Standards (`SKILL.md:133-170`)

- Format: Lowercase letters, numbers, hyphens only, max 64 chars
- Name must match directory name
- Recommended: verb-ing + noun form (`processing-csv-files`, `generating-api-docs`)
- Prohibited: XML tags, reserved words (`anthropic`, `claude`), vague terms (`helper`, `utility`, `manager`), spaces or underscores

Note: Unlike metaskills/skill-builder which strictly enforces gerund naming, this repo **recommends** gerund form but doesn't mandate it (existing skills use noun forms like `daily-ai-news`, `mcp-builder`).

#### Description Writing Rules (`SKILL.md:166-178`)

- Must use third person (NOT "I help you...")
- 4C Principles: Clear, Concise, Contextual, Complete
- Max 1024 characters
- Include trigger keywords and applicable scenarios

#### Content Writing Guide

**"When to Use" Section** (`SKILL.md:180-198`): Four trigger patterns:
- Direct request: "User asks to X"
- Keywords: "User mentions 'keyword'"
- Context: "User is working with X"
- Task type: "User needs to X"

**Workflow Design** (`SKILL.md:200-240`): Three patterns offered:
1. Simple Linear Flow - numbered steps
2. Conditional Branching Flow - if/else decision trees
3. Checklist Pattern - ordered checklist, stop on failure

**Script Integration** (`SKILL.md:275-310`): Python-oriented (contrast with skill-builder's Node.js-only stance). Scripts must include shebang, docstring, type annotations, constants, parameter validation, error handling, clear return values.

#### Quality Checklist (`SKILL.md:335-385`)

Five categories with specific checkboxes:

**Core Quality:**
- `name` follows naming conventions (lowercase, hyphens, <=64 chars)
- `description` includes trigger keywords and scenarios (<=1024 chars)
- Name matches directory name
- Only includes info Claude doesn't know
- No redundant/duplicate content

**Functional Completeness:**
- Has "When to Use" with 3-5 trigger scenarios
- Clear execution flow/steps
- At least 2-3 complete examples
- Includes input and expected output
- Error handling guidance

**Structure Standards:**
- Clear section organization
- Table of contents for >200 lines
- Reference nesting <=1 level
- Forward slashes for paths
- Consistent terminology

**Scripts and Templates:**
- Scripts include usage instructions and parameter docs
- Error handling present
- No magic numbers, use configuration
- Template format clear and usable

**Final Check:**
- Read-through for fluency
- Test triggering with actual scenarios
- Appropriate length (200-500 lines, or split)

#### FAQ Section (`SKILL.md:395-430`)

Key answers:
- Length: Minimum 50-100, ideal 200-500, max 500 (split if exceeded)
- Activation: Use keywords in description, state specific scenarios, mention tool names
- Overlap: More specific descriptions, explain relationships in "When to Use", consider merging
- Maintenance: Review quarterly, iterate on feedback, update when tools/APIs change

### Two Template Patterns

#### Basic Skill Template (`templates/basic-skill-template.md:1-94`)

A straightforward template with sections:
1. YAML frontmatter (`name` + `description`)
2. Skill Title with one-line summary
3. "When to Use This Skill" (4 bullet triggers)
4. Quick Start (bash example)
5. "How It Works" (3 numbered steps)
6. Examples (2: Basic + Advanced, each with User Request/Action/Output)
7. Best Practices (Do/Don't with checkmarks/crosses)
8. Troubleshooting (2 Problem/Solution pairs)
9. References
10. Version footer

#### Workflow Skill Template (`templates/workflow-skill-template.md:1-401`)

A comprehensive template for multi-step processes with:
1. YAML frontmatter
2. ASCII flowchart diagram (preparation -> steps -> complete)
3. Preparation Phase with checklist
4. Multi-step workflow with per-step: Purpose, Actions, Validation, On Success/Failure branches
5. Examples showing standard execution AND error recovery
6. Error Handling with 3 categories (Recoverable/User Input Needed/Critical)
7. Rollback Procedure (identify last success, undo, verify, report)
8. Workflow Variations (Quick Mode vs Strict Mode trade-offs)
9. Monitoring and Logging with timestamp format
10. Post-Workflow Report template
11. Advanced Features: Parallel Execution and Conditional Branching
12. Testing with `--dry-run` and `--inject-error` patterns

### Good vs Bad Examples

#### Good Examples (`examples/good-example.md:1-907`)

Three complete, high-quality skills demonstrating different patterns:

1. **Database Migration Skill** (Basic Skill) - Alembic/SQLAlchemy focus. Has complete code examples for adding columns and data migrations, troubleshooting for 3 common errors, configuration section with project structure.

2. **API Documentation Generation Skill** (Workflow Skill) - 4-phase workflow: Discovery, Enhancement, Generation, Validation. Decision points (ask user before adding docs). Multi-framework support (FastAPI + Flask).

3. **Code Review Skill** (High-Flexibility Skill) - 5 review dimensions (Correctness, Security, Performance, Maintainability, Best Practices). Severity ratings (Critical/High/Medium/Low). Shows full code transformation from bad to good.

Each example includes a "Why This Is Good" analysis table.

#### Bad Examples (`examples/bad-example.md:1-866`)

Three anti-patterns with fixes:

1. **Overly Vague Skill** - `name: helper`, `description: Helps with code`. Fixed to `python-code-refactoring` with specific triggers and complete refactoring examples.

2. **Overly Verbose Skill** - `name: python-basics`, teaches Python fundamentals Claude already knows. Fixed to `project-python-conventions` with only project-specific rules.

3. **Skill Lacking Context** - `name: deployment`, 4 vague steps. Fixed to `deploy-to-production` with complete AWS deployment commands, blue-green deployment, monitoring, and rollback.

### Other Skills in the Collection

| Skill | Lines | Key Feature |
|-------|-------|-------------|
| `daily-ai-news` | 327 | Multi-source AI news aggregation with WebSearch + MCP web reader |
| `deep-reading-analyst` | 501 | 10+ thinking frameworks (SCQA, 5W2H, Six Hats, etc.) with 10 reference files |
| `dry-refactoring` | 964 | 4-step DRY refactoring with complete e-commerce example |
| `fastgpt-workflow-generator` | 754 | JSON workflow generation with 3-layer validation and built-in templates |
| `frontend-design` | 491 | Anti-generic AI aesthetics, typography guides, animation patterns |
| `mcp-builder` | 236 | MCP server creation guide for FastMCP (Python) and MCP SDK (Node.js) |
| `planning-with-files` | 160 | Manus-style 3-file pattern (task_plan.md, notes.md, deliverable.md) |
| `prompt-optimize` | 242 | "Alpha-Prompt" persona with CoT, ToT, Self-Consistency, ReAct architectures |

### Frontmatter Patterns Across All Skills

All skills use the same two-field pattern with `name` + `description`. Descriptions are consistently written in third person and include trigger keywords. Examples:

```yaml
# Terse, keyword-rich
name: dry-refactoring
description: Guides systematic code refactoring following the DRY principle...

# Long, scenario-heavy (quoted YAML)
name: deep-reading-analyst
description: "Comprehensive framework for deep analysis of articles... Use when users want to: (1) deeply understand... (2) analyze arguments... Triggered by phrases like 'analyze this article'..."

# Includes license
name: mcp-builder
description: Guide for creating high-quality MCP servers...
license: Complete terms in LICENSE.txt
```

## Comparison with metaskills/skill-builder

| Aspect | Claude-meta-skill (YYH211) | skill-builder (metaskills) |
|--------|---------------------------|---------------------------|
| **Scope** | 9 skills + meta-skill | Meta-skill only |
| **Templates** | 2 (Basic + Workflow) | 1 (generic) |
| **Examples** | 6 (3 good, 3 bad with fixes) | In-line examples only |
| **Naming** | Recommends gerund, doesn't enforce | Strictly requires gerund form |
| **Scripts** | Python-friendly | Node.js only, Python forbidden |
| **Frontmatter fields** | `name` + `description` | `name` + `description` |
| **SKILL.md length** | 200-500 lines target | 150-200 lines target (stricter) |
| **Progressive disclosure** | Yes, max 1 level depth | Yes, max 1 level depth |
| **Sub-agent conversion** | Not addressed | Dedicated 700-line guide |
| **Freedom levels** | 3 tiers (High/Medium/Low) | Not explicitly tiered |
| **Quality checklist** | 5 categories with checkboxes | Validation steps in workflow |
| **Languages** | Chinese + English | English only |
| **Description formula** | 4C principles (Clear, Concise, Contextual, Complete) | "Use this skill when [primary]. This includes [specifics]..." |

## Architecture Notes

### Design Patterns

1. **Dual-Language Architecture**: Every core file exists in Chinese (`create-skill-file/`) and English (`create-skill-file-EN/`) with identical structure but different content language.

2. **Example-Driven Teaching**: Unlike skill-builder which relies on reference documents, this repo uses extensive good/bad example pairs (1773 lines of examples total) as the primary teaching mechanism.

3. **Freedom-Tiered Design**: The three-tier freedom model (High/Medium/Low) is a unique framework for deciding how prescriptive a skill should be. This maps to: creative tasks (principles), standard tasks (parameterized patterns), error-prone tasks (step-by-step scripts).

4. **Multi-Domain Skill Collection**: Beyond the meta-skill, the repo serves as a curated library of production skills spanning frontend, AI, workflows, code quality, and planning. Each demonstrates different patterns (basic vs workflow, minimal vs reference-heavy).

5. **Progressive Disclosure with Concrete Boundaries**: Hard limits on file sizes (SKILL.md 200-500 lines, split at >500, sub-files get TOC at >100 lines) provide actionable structure rather than vague guidelines.

6. **Install via cp**: All skills designed for `cp -r skill-name .claude/skills/` installation. No package manager, no build step.

### What Makes This Repo Distinct

- **Dual template system**: Basic vs Workflow templates target different skill complexity levels
- **Teaching by counter-example**: Bad examples with detailed problem analysis + fixes are rare in the ecosystem
- **Freedom-level framework**: Explicit guidance on WHEN to be prescriptive vs permissive
- **Bilingual**: Chinese/English parity enables broader adoption
- **Skill library alongside meta-skill**: The other 8 skills serve as living examples of the meta-skill's teachings
- **Python-friendly**: Unlike skill-builder's strict Node.js mandate, this repo embraces Python scripting

## Code References

- `create-skill-file-EN/SKILL.md:1-474` - English meta-skill (full writing guide)
- `create-skill-file/SKILL.md:1-475` - Chinese meta-skill
- `create-skill-file-EN/templates/basic-skill-template.md:1-94` - Basic template
- `create-skill-file-EN/templates/workflow-skill-template.md:1-401` - Workflow template
- `create-skill-file-EN/examples/good-example.md:1-907` - 3 good examples
- `create-skill-file-EN/examples/bad-example.md:1-866` - 3 bad examples with fixes
- `README.md:1-370` - Full README with installation and skill catalog
- `planning-with-files/SKILL.md:1-160` - Manus-style 3-file pattern skill
- `daily-ai-news/SKILL.md:1-327` - AI news aggregation skill
- `deep-reading-analyst/SKILL.md:1-501` - Multi-framework analysis skill
- `dry-refactoring/SKILL.md:1-964` - DRY refactoring skill
- `fastgpt-workflow-generator/SKILL.md:1-754` - FastGPT workflow skill
- `frontend-design/SKILL.md:1-491` - Frontend design skill
- `mcp-builder/SKILL.md:1-236` - MCP server building skill
- `prompt-optimize/SKILL.md:1-242` - Prompt engineering skill

## Open Questions

1. **Quality checklist enforcement**: The checklist is defined but there's no automated validation. How effectively does Claude self-evaluate against it during skill creation?
2. **Template selection**: How does Claude decide between Basic vs Workflow template? The guide doesn't provide explicit decision criteria.
3. **Cross-skill consistency**: The 8 non-meta skills don't all follow the meta-skill's own guidelines (e.g., `dry-refactoring` at 964 lines exceeds the 500-line max without splitting).
4. **Activation reliability**: With 9 skills installed, how well does Claude disambiguate between overlapping trigger keywords?
5. **Gerund naming gap**: The guide recommends gerund names but existing skills don't follow it (`daily-ai-news`, `mcp-builder`, `prompt-optimize`), creating a "do as I say, not as I do" tension.
