---
last_updated: 2026-02-02
topic: Blueprint - creating-skills skill
tags: [blueprint, reference, creating-skills]
status: historical
note: "Reference document used to create newskills/creating-skills/. Skill is fully implemented."
---

# Blueprint: `creating-skills` (Active Skill Creator)

**Date:** 2026-01-28
**Target:** `newskills/creating-skills/`
**Deploy to:** `~/.claude/skills/creating-skills/`

---

## Purpose

A skill that activates when the user wants to build a new Claude Code skill from scratch, edit an existing skill, or convert a sub-agent to a skill. It guides the process with structured templates, validation rules, and progressive disclosure.

---

## Research Files

- [Skill Builder (metaskills)](file:///C:/code/commandbase/.docs/research/01-28-2026-metaskills-skill-builder.md) -- Description formula, gerund naming, sub-agent conversion, progressive disclosure
- [Claude Meta-Skill (YYH211)](file:///C:/code/commandbase/.docs/research/01-28-2026-claude-meta-skill-repo.md) -- Basic + Workflow templates, good/bad examples, freedom-tier model, quality checklist
- [Anthropic Skills (official)](file:///C:/code/commandbase/.docs/research/01-28-2026-anthropic-skills-repo.md) -- Validation rules (name regex, description max 1024, allowed frontmatter), packaging scripts, progressive disclosure spec
- [Skill Factory (alirezarezvani)](file:///C:/code/commandbase/.docs/research/01-28-2026-skill-factory-workflow.md) -- Two-tier delegation, Build > Validate > Install pipeline, slash command patterns
- [Agent Skill Creator (FrancyJGLisboa)](file:///C:/code/commandbase/.docs/research/01-28-2026-agent-skill-creator-workflow.md) -- 6-phase protocol, DECISIONS.md convention, activation system design
- [All Repos Index](file:///C:/code/commandbase/.docs/research/01-28-2026-skillcreator-repos.md)

## Cloned Repos (read for reference patterns)

- `C:/code/repo-library/skill-builder/` -- Primary reference (lean, opinionated, description-focused)
- `C:/code/repo-library/Claude-meta-skill/` -- Templates at `create-skill-file-EN/templates/`, examples at `create-skill-file-EN/examples/`
- `C:/code/repo-library/skills/` -- Official Anthropic: `skills/skill-creator/SKILL.md`, validation at `skills/skill-creator/scripts/quick_validate.py`
- `C:/code/repo-library/claude-code-skill-factory/` -- Factory templates at `documentation/templates/`
- `C:/code/repo-library/agent-skill-creator/` -- Phase guides at `references/phase*.md`, quality standards at `references/quality-standards.md`

---

## What to Take from Each

### From Skill Builder (metaskills) -- PRIMARY INFLUENCE
- Description writing formula: `"Use this skill when [primary situation]. This includes [specific use cases]..."`
- Gerund naming convention: `processing-pdfs`, `analyzing-data`
- Three modes: Create new / Edit existing / Convert sub-agent
- Progressive disclosure: SKILL.md < 500 lines, reference files for depth, 1 level deep
- Intention-revealing file names
- Sub-agent-to-skill conversion workflow (the key insight: sub-agents explain WHAT, skills explain WHEN)

### From Claude Meta-Skill (YYH211) -- TEMPLATES & TEACHING
- Two templates: Basic Skill Template + Workflow Skill Template
- Freedom-tier model (High/Medium/Low) to decide how prescriptive the skill should be
- Good/bad example pairs as the teaching mechanism
- Quality checklist with 5 categories (Core Quality, Functional Completeness, Structure Standards, Scripts/Templates, Final Check)
- 4C description principles: Clear, Concise, Contextual, Complete

### From Anthropic Skills (official) -- VALIDATION RULES
- Allowed frontmatter properties: `name`, `description`, `license`, `allowed-tools`, `metadata`
- Name: `^[a-z0-9-]+$`, no start/end hyphens, no double hyphens, max 64 chars
- Description: max 1024 chars, no angle brackets
- Three-level progressive disclosure: metadata (~100 tokens) → SKILL.md body (<5k words) → bundled resources
- Skill = directory with SKILL.md, not a single file

### From Agent Skill Creator (FrancyJGLisboa) -- PROCESS RIGOR
- DECISIONS.md convention: document every architectural choice with rationale
- Quality standards: production-ready output, no TODOs, no placeholders
- Marketplace.json synchronization (description must match SKILL.md frontmatter)

### From Skill Factory (alirezarezvani) -- PIPELINE
- Build > Validate > Install pipeline concept
- Composability principle: output from one skill feeds into another

---

## Proposed Structure

```
newskills/creating-skills/
├── SKILL.md                              # Core workflow (target: 200-300 lines)
├── reference/
│   ├── validation-rules.md               # Official spec constraints (from Anthropic)
│   ├── description-writing-guide.md      # Formula + good/bad examples
│   ├── naming-conventions.md             # Gerund form, kebab-case rules
│   └── converting-subagents.md           # Sub-agent to skill migration
└── templates/
    ├── basic-skill-template.md           # Simple skills
    └── workflow-skill-template.md         # Multi-step process skills
```

## SKILL.md Frontmatter

```yaml
---
name: creating-skills
description: Use this skill when creating new Claude Code skills from scratch, editing existing skills to improve their structure or descriptions, or converting Claude Code sub-agents into skills. This includes writing SKILL.md files, choosing skill names, crafting invocation-focused descriptions, organizing supporting files with progressive disclosure, and validating skill structure against the official specification.
---
```

## Core Workflow (for SKILL.md body)

### Step 1: Gather Requirements
- What task does this skill handle?
- When should Claude invoke it? (trigger conditions)
- Personal (`~/.claude/skills/`) or project (`.claude/skills/`)?
- Are there similar existing skills?

### Step 2: Choose Freedom Level
- **High freedom** (creative tasks): guiding principles, not specific steps
- **Medium freedom** (standard tasks): parameterized examples, default flows
- **Low freedom** (error-prone tasks): step-by-step scripts, exact commands

### Step 3: Design the Skill
- Name: gerund form (`verb-ing-noun`), max 64 chars, kebab-case
- Description: `"Use this skill when [primary situation]. This includes [specific use cases]..."`, max 1024 chars, third person
- Template: Basic (simple tasks) or Workflow (multi-step processes)
- Plan supporting files (reference docs, scripts, assets)

### Step 4: Create the Skill
- Write SKILL.md with YAML frontmatter (`name` + `description` only, unless `license` or `allowed-tools` needed)
- Keep SKILL.md under 500 lines (ideally 200-300)
- Add reference files with intention-revealing names
- Add scripts if needed (test by running them)

### Step 5: Validate
- Name: `^[a-z0-9-]+$`, no start/end `-`, no `--`, max 64 chars, gerund form
- Description: max 1024 chars, no angle brackets, includes trigger keywords, third person
- SKILL.md: under 500 lines, has clear "When to Use" section
- Reference depth: max 1 level from SKILL.md
- No extraneous files (no README.md, CHANGELOG.md in skills)

---

## Prompt for Separate Window

Copy the following into a new Claude Code session:

```
I need you to build a Claude Code skill called `creating-skills`. This is a meta-skill that helps create other Claude Code skills.

Working directory: C:/code/commandbase/newskills/creating-skills/

BEFORE writing any code, read these research files and cloned repos for context:

Research files (read all):
- C:/code/commandbase/.docs/research/01-28-2026-metaskills-skill-builder.md
- C:/code/commandbase/.docs/research/01-28-2026-claude-meta-skill-repo.md
- C:/code/commandbase/.docs/research/01-28-2026-anthropic-skills-repo.md

Reference repos (read the key files):
- C:/code/repo-library/skill-builder/SKILL.md (PRIMARY model -- follow this structure)
- C:/code/repo-library/skill-builder/reference/ (all 5 files)
- C:/code/repo-library/skill-builder/converting-sub-agents-to-skills.md
- C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/SKILL.md
- C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/templates/ (both templates)
- C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/examples/ (good and bad)
- C:/code/repo-library/skills/skills/skill-creator/SKILL.md
- C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py (validation rules)

Blueprint with full instructions:
- C:/code/commandbase/.docs/plans/creating-skills-blueprint.md

Create the skill with this structure:
newskills/creating-skills/
├── SKILL.md                              # Core workflow (200-300 lines)
├── reference/
│   ├── validation-rules.md               # Official spec constraints
│   ├── description-writing-guide.md      # Formula + good/bad examples
│   ├── naming-conventions.md             # Gerund form, kebab-case rules
│   └── converting-subagents.md           # Sub-agent to skill migration
└── templates/
    ├── basic-skill-template.md           # Simple skills
    └── workflow-skill-template.md         # Multi-step process skills

Key requirements:
1. SKILL.md frontmatter: name=creating-skills, description focused on WHEN to invoke (creating, editing, converting skills)
2. Three modes: Create New / Edit Existing / Convert Sub-Agent
3. Include the freedom-tier model (High/Medium/Low) from Claude Meta-Skill
4. Use Skill Builder's description formula as the standard
5. Validation rules from Anthropic's quick_validate.py (name regex, description length, allowed frontmatter keys)
6. Templates adapted from Claude Meta-Skill's Basic + Workflow templates
7. Good/bad examples in the description writing guide
8. Keep SKILL.md under 300 lines -- put depth in reference/ files
9. DO NOT copy content verbatim from repos -- synthesize the best patterns into original content
```
