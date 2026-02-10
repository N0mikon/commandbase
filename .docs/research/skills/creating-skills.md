---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 64 commits - corrected file paths from ~/.claude/skills/ to plugin structure, added agent deferral, freedom tiers, complexity check, sibling skill section, and updated reference/template file listings"
references:
  - plugins/commandbase-meta/skills/creating-skills/SKILL.md
  - plugins/commandbase-meta/skills/creating-skills/reference/validation-rules.md
  - plugins/commandbase-meta/skills/creating-skills/reference/description-writing-guide.md
  - plugins/commandbase-meta/skills/creating-skills/reference/naming-conventions.md
  - plugins/commandbase-meta/skills/creating-skills/reference/converting-subagents.md
  - plugins/commandbase-meta/skills/creating-skills/templates/basic-skill-template.md
  - plugins/commandbase-meta/skills/creating-skills/templates/workflow-skill-template.md
---

# Research: creating-skills Skill

## Overview

The `creating-skills` skill (`plugins/commandbase-meta/skills/creating-skills/SKILL.md`) creates new Claude Code skills from scratch, edits existing skills, or converts sub-agents into skills. It enforces the official skill specification. Part of the `commandbase-meta` plugin.

**Invocation**: `/creating-skills`, `create a skill`, `make a new skill`

## Purpose

Create and validate skills:
- Writing SKILL.md files
- Choosing skill names (gerund form)
- Crafting invocation-focused descriptions
- Organizing supporting files with progressive disclosure
- Validating skill structure against official specification
- Differentiating skills from agents and redirecting when appropriate

## Skill Structure

```
plugins/<plugin>/skills/[skill-name]/
├── SKILL.md                    # Required - main skill file
├── reference/                  # Optional - supporting docs
│   ├── validation-rules.md
│   ├── description-writing-guide.md
│   ├── naming-conventions.md
│   └── converting-subagents.md
├── templates/                  # Optional - output templates
│   ├── basic-skill-template.md
│   └── workflow-skill-template.md
├── scripts/                    # Optional - automation
└── assets/                     # Optional - images, data
```

## Three Modes

### Mode 1: Create New Skill
Build from scratch using the 5-step workflow: gather requirements, choose freedom tier, design (name + description + template), write, validate.

### Mode 2: Edit Existing Skill
Read existing SKILL.md, diagnose improvements, preserve intent, re-validate, show diffs.

### Mode 3: Convert Sub-Agent to Skill
Transform agent files into skill directories. Core shift: agents explain WHAT they are, skills explain WHEN to use them. Name transforms from noun to gerund form.

## Agent Deferral

The Gate Function includes an agent check at step 0: if the user wants a single `.md` file with tools/model/system prompt, redirect to `/creating-agents`. The two skills are siblings with clear boundaries documented in a comparison table within SKILL.md.

## Freedom Tiers

Skills are written at one of three freedom levels based on error tolerance:

| Tier | When to Use | Writing Approach |
|------|-------------|-----------------|
| **High** | Creative tasks, many valid outcomes | Guiding principles and goals, not specific steps |
| **Medium** | Standard tasks, recommended patterns | Parameterized examples, default flows with alternatives |
| **Low** | Error-prone tasks, strict execution | Step-by-step procedures, exact commands, verification gates |

## Complexity Check

Before proceeding, the skill evaluates whether to build directly or suggest `/researching-code` first:
- **Simple** (proceed directly): Single SKILL.md, familiar domain, under 200 lines, user knows what they want
- **Complex** (suggest research first): Needs reference/ subdirectories, unfamiliar APIs, cross-cutting concerns, user uncertain

## Validation Rules

### Frontmatter
- Must start and end with `---`
- Valid YAML dictionary
- Only allowed properties: name, description, license, allowed-tools, metadata
- Required: name, description

### Name Validation
- Matches `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Must match directory name
- Uses gerund form (verb-ing)

### Description Validation
- Non-empty string
- Max 1024 characters
- No angle brackets `<>`
- Third person voice (no "I help", "I am")
- Starts with "Use this skill when..."
- Must describe WHEN to activate, not just WHAT it does
- Follows the 4C principles: Clear, Concise, Contextual, Complete

### Structure Validation
- SKILL.md exists at root
- Under 500 lines, under 5,000 words
- Reference nesting max 1 level
- Allowed subdirectories: reference/, templates/, scripts/, assets/
- No extraneous files (README, CHANGELOG, INSTALLATION_GUIDE, QUICK_REFERENCE)
- File names must be intention-revealing

## Enforcement Pattern

Skills should include:
1. **Iron Law**: Core non-negotiable rule ("No skill without validated description and structure")
2. **Gate Function**: Steps before main action (including agent check at step 0)
3. **Red Flags**: Warning signs to stop (11 specific red flags defined)
4. **Rationalization Prevention**: Common excuses and reality (6 entries)
5. **Bottom Line**: Summary principle

## Process (Mode 1 Detail)

### Step 1: Gather Requirements
Ask and answer:
- What task does this skill handle? (Be specific)
- When should Claude invoke it? (List 5 specific situations)
- Personal or project scope?
- Similar existing skills to learn from?
- How much existing Claude knowledge applies?

### Step 2: Choose Freedom Tier
Match tier to error tolerance and domain variability. Most skills land in Medium.

### Step 3: Design the Skill
- **Name**: Gerund form, kebab-case (see reference/naming-conventions.md)
- **Description**: WHEN formula from reference/description-writing-guide.md -- write FIRST before body
- **Template**: Basic (templates/basic-skill-template.md) or Workflow (templates/workflow-skill-template.md)
- **Supporting files**: Plan reference docs if body would exceed 300 lines

### Step 4: Write the Skill
- Start with YAML frontmatter (name + description)
- Follow chosen template structure
- Keep SKILL.md under 500 lines (target: 200-300 lines)
- Use skinny pointers to reference files
- Write for Claude, not humans
- For structured output skills: specify explicit format constraints (line counts, bullet limits)
- For state-modifying skills: include Red Flag for scope creep

### Step 5: Validate
Run every item in reference/validation-rules.md. Fix all issues before declaring done.

## Output

```
Skill created: [name]
Location: [path]
Files: [count] ([list])
Description: [first 80 chars...]
Validation: All checks passed
```

## Sibling Skill: /creating-agents

| Aspect | /creating-skills | /creating-agents |
|--------|-----------------|-----------------|
| Creates | SKILL.md + reference directory | Single .md agent files |
| Names | Gerund form (reviewing-code) | Noun form (code-reviewer) |
| Descriptions | "Use this skill when..." (intent matching) | Capability + delegation trigger |
| Converts | Agents -> Skills (Mode 3) | Skills -> Agents (Mode 3) |

## File References

- Main: `plugins/commandbase-meta/skills/creating-skills/SKILL.md`
- Validation rules: `plugins/commandbase-meta/skills/creating-skills/reference/validation-rules.md`
- Description guide: `plugins/commandbase-meta/skills/creating-skills/reference/description-writing-guide.md`
- Naming conventions: `plugins/commandbase-meta/skills/creating-skills/reference/naming-conventions.md`
- Sub-agent conversion: `plugins/commandbase-meta/skills/creating-skills/reference/converting-subagents.md`
- Basic template: `plugins/commandbase-meta/skills/creating-skills/templates/basic-skill-template.md`
- Workflow template: `plugins/commandbase-meta/skills/creating-skills/templates/workflow-skill-template.md`
