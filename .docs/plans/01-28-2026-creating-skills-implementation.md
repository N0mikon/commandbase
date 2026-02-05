---
git_commit: 2d50723
last_updated: 2026-02-05
last_updated_by: docs-updater
last_updated_note: "Updated git_commit to current HEAD - no content changes needed, plan remains completed"
topic: "Creating-Skills Skill Implementation"
tags: [plan, implementation, creating-skills, meta-skill, skill-builder]
status: completed
completed_date: 2026-01-28
completed_in_commit: a7794e1
references:
  - .docs/plans/creating-skills-blueprint.md
  - .docs/research/01-28-2026-creating-skills-blueprint.md
  - newskills/creating-skills/SKILL.md
  - newskills/creating-skills/reference/validation-rules.md
  - newskills/creating-skills/reference/description-writing-guide.md
  - newskills/creating-skills/reference/naming-conventions.md
  - newskills/creating-skills/reference/converting-subagents.md
  - newskills/creating-skills/templates/basic-skill-template.md
  - newskills/creating-skills/templates/workflow-skill-template.md
---

# Creating-Skills Skill Implementation Plan

## Overview

Build a meta-skill (`creating-skills`) that guides Claude through creating, editing, or converting Claude Code skills. Standalone by default, but RPI-aware: if `/rcode` research exists it uses that as a baseline, and it suggests `/rcode` first when the skill being created looks complex enough to warrant research.

## Current State Analysis

- `newskills/creating-skills/` does not exist yet
- All 11 existing skills use the Iron Law / Gate Function / Red Flags / Rationalization Prevention / Bottom Line enforcement pattern
- Existing skills are flat (single SKILL.md per directory) - this will be the first to use `reference/` and `templates/` subdirectories
- Blueprint exists at `.docs/plans/creating-skills-blueprint.md` with proposed structure, frontmatter, 5-step workflow, and a copy-paste prompt
- Research exists at `.docs/research/01-28-2026-creating-skills-blueprint.md` documenting all influences and conflicts

### Key Discoveries:
- Enforcement pattern is universal across all commandbase skills (`newskills/learn/SKILL.md`, `newskills/checkpoint/SKILL.md` confirm non-RPI skills use it too)
- `rcode` writes to `.docs/research/MM-DD-YYYY-*.md`, `pcode` reads from `.docs/research/` via docs-locator agents (`newskills/pcode/SKILL.md:176-179`)
- Existing skills use `description` only in frontmatter (no `name` field), but Anthropic spec requires both (`quick_validate.py:52-55`)
- Research-heavy skills use `model: opus` (`rcode`, `pcode`, `new_project`); execution skills use default
- Progressive disclosure: SKILL.md < 500 lines, reference files for depth, max 1 level deep

## Desired End State

A 7-file skill at `newskills/creating-skills/` that:

1. Activates when a user wants to create, edit, or convert skills
2. Follows the commandbase enforcement pattern (Iron Law, Gate Function, etc.)
3. Runs standalone by default with its own 5-step workflow
4. Detects and uses existing `/rcode` research files when available
5. Suggests `/rcode` first when the target skill looks complex (multi-file, cross-system, unfamiliar domain)
6. Synthesizes the best patterns from Skill Builder, Claude Meta-Skill, and Anthropic official into original content
7. Keeps SKILL.md at 200-300 lines with depth in reference/ and templates/

### Verification:
- All 7 files exist with non-empty content
- SKILL.md has valid YAML frontmatter with `name` and `description`
- SKILL.md is 200-300 lines
- Each reference file has substantive content (not placeholders)
- Each template is a usable starting point (not a skeleton with TODOs)
- No content copied verbatim from reference repos

## What We're NOT Doing

- NOT splitting into /rskill /pskill /iskill /vskill - single skill, RPI-aware
- NOT adding a validation script (no Python/Node.js scripts in this skill)
- NOT adding `allowed-tools` to frontmatter
- NOT creating a marketplace.json or .skill packaging
- NOT updating existing newskills to add `name` frontmatter (separate task)
- NOT adding hooks or activation systems beyond the description field

## Implementation Approach

Single phase - all 7 files created together since they're tightly coupled. The SKILL.md references the reference/ and templates/ files, so they need to exist coherently from the start.

Content will be synthesized from the three primary influences but written as original content:
- **Structure and workflow**: Follow commandbase's own enforcement pattern (Iron Law, Gate Function, etc.), not the Skill Builder's Role → Core Knowledge → Process → Best Practices pattern
- **Domain knowledge**: Synthesize from Skill Builder (description formula, gerund naming), Claude Meta-Skill (freedom tiers, templates, good/bad examples), Anthropic (validation rules, progressive disclosure)
- **RPI awareness**: New pattern not in any influence - the skill checks for existing research and suggests it for complex cases

## Phase 1: Create All Skill Files

### Overview
Create the directory structure and all 7 files. SKILL.md is the anchor; reference files and templates are its progressive disclosure layer.

### Changes Required:

#### 1. Directory Structure
Create:
```
newskills/creating-skills/
├── SKILL.md
├── reference/
│   ├── validation-rules.md
│   ├── description-writing-guide.md
│   ├── naming-conventions.md
│   └── converting-subagents.md
└── templates/
    ├── basic-skill-template.md
    └── workflow-skill-template.md
```

#### 2. SKILL.md (200-300 lines)

**Frontmatter:**
```yaml
---
name: creating-skills
description: "Use this skill when creating new Claude Code skills from scratch, editing existing skills to improve their structure or descriptions, or converting Claude Code sub-agents into skills. This includes writing SKILL.md files, choosing skill names, crafting invocation-focused descriptions, organizing supporting files with progressive disclosure, and validating skill structure against the official specification."
---
```

**Structure (following commandbase enforcement pattern):**

```
# Creating Skills

[Opening paragraph: meta-skill for creating, editing, converting skills]

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law
NO SKILL WITHOUT VALIDATED DESCRIPTION AND STRUCTURE
[Explanation: description is the triggering mechanism, structure determines usability]

## The Gate Function
BEFORE writing any SKILL.md:
1. GATHER: What task? When invoke? Personal vs project?
2. CHECK RESEARCH: Does `.docs/research/` have relevant analysis?
   - If YES: Read it, use as baseline for design decisions
   - If NO and skill is complex*: Suggest `/rcode` first
   - If NO and skill is simple: Proceed
3. DESIGN: Name (gerund, kebab-case), description (formula), freedom tier
4. CHOOSE: Template (basic or workflow) from ./templates/
5. VALIDATE: Run validation checklist from ./reference/validation-rules.md
6. ONLY THEN: Write the skill files

*Complex = multi-file with reference/, cross-system integration, or unfamiliar domain

## Complexity Check
[When to suggest /rcode first vs proceed standalone]
- Simple (proceed): Single SKILL.md, familiar domain, clear workflow
- Complex (suggest /rcode): Needs reference/, involves unfamiliar APIs/systems,
  cross-cutting concerns, user says "I'm not sure how to structure this"

## Three Modes

### Mode 1: Create New Skill
[5-step workflow from blueprint, with RPI awareness added at step 1]

### Mode 2: Edit Existing Skill
[Read existing skill fully, identify improvement areas, apply changes]

### Mode 3: Convert Sub-Agent to Skill
[WHAT→WHEN transformation, pointer to ./reference/converting-subagents.md]

## Freedom Tiers
[High/Medium/Low from Claude Meta-Skill, with decision criteria]

## Reference Files
- See ./reference/validation-rules.md for official spec constraints
- See ./reference/description-writing-guide.md for the formula and examples
- See ./reference/naming-conventions.md for gerund form and kebab-case rules
- See ./reference/converting-subagents.md for sub-agent migration

## Templates
- See ./templates/basic-skill-template.md for simple, linear skills
- See ./templates/workflow-skill-template.md for multi-step process skills

## Red Flags - STOP and Check
[List of shortcuts to watch for]

## Rationalization Prevention
[Table of excuses vs reality, adapted for skill creation context]

## The Bottom Line
No shortcuts for skill creation.
Gather requirements. Check for research. Design with intention. Validate before saving.
This is non-negotiable. Every skill. Every time.
```

**Target: 250-280 lines**

#### 3. reference/validation-rules.md (80-120 lines)

Content synthesized from `quick_validate.py:12-86` and Anthropic's skill-creator spec:

```
# Validation Rules

## Frontmatter Requirements
- Must start with `---` and end with `---`
- Valid YAML dictionary
- Allowed properties: name, description, license, allowed-tools, metadata
- Required: name, description

## Name Rules
- Regex: ^[a-z0-9-]+$
- No start/end hyphens, no consecutive hyphens
- Max 64 characters
- Must match directory name
- Gerund form recommended (see ./naming-conventions.md)

## Description Rules
- Max 1024 characters
- No angle brackets (< or >)
- Must include trigger keywords
- Third person voice
- Formula: "Use this skill when [situation]. This includes [use cases]..."

## Structure Rules
- SKILL.md required at directory root
- SKILL.md body: <500 lines, <5k words
- Reference nesting: max 1 level from SKILL.md
- No extraneous files (no README.md, CHANGELOG.md, etc.)

## Progressive Disclosure
[Three levels: metadata always loaded, body on trigger, resources on demand]

## Validation Checklist
[Checkbox list combining Anthropic rules + Meta-Skill quality checklist]
```

#### 4. reference/description-writing-guide.md (120-180 lines)

Content synthesized from Skill Builder's metadata-requirements.md and Meta-Skill's good/bad examples:

```
# Description Writing Guide

## The Formula
"Use this skill when [primary situation]. This includes [specific use cases
with trigger keywords], [more use cases], and [edge cases]."

## The 4C Principles
- Clear: No jargon, no vague terms
- Concise: 1-2 sentences for core functionality
- Contextual: Describe when to activate
- Complete: Functionality + trigger conditions

## Good Examples
[3-4 examples with analysis of WHY they work]

## Bad Examples
[3-4 examples with analysis of WHY they fail, plus fixes]

## Common Mistakes
- Too vague: "Helps with code" → no trigger keywords
- Too broad: "Handles all Python tasks" → Claude can't distinguish
- First person: "I help you..." → should be third person
- Missing trigger: describes WHAT but not WHEN

## Writing Process
1. List 5 specific situations when Claude should use this skill
2. Identify the trigger keywords from those situations
3. Write the description using the formula
4. Check: Does it tell Claude WHEN, not just WHAT?
5. Verify: Under 1024 chars, no angle brackets
```

#### 5. reference/naming-conventions.md (60-90 lines)

Content synthesized from Skill Builder's gerund convention and Anthropic's regex:

```
# Naming Conventions

## The Gerund Rule
Skills use verb-ing form: the name describes the ACTION, not the thing.

Good: creating-skills, processing-pdfs, deploying-lambdas
Bad: skill-creator, pdf-processor, lambda-tool

## Format Rules
- Regex: ^[a-z0-9-]+$
- Lowercase only, hyphens as separators
- No start/end hyphens, no consecutive hyphens
- Max 64 characters (practical sweet spot: 15-40)
- Must match directory name exactly

## File Naming
- SKILL.md (always uppercase, always this exact name)
- Reference files: lowercase, intention-revealing (not reference.md, helpers.md)
- Subdirectories: reference/, templates/, scripts/, assets/

## Directory Location
- Personal: ~/.claude/skills/skill-name/
- Project: .claude/skills/skill-name/

## Examples
[Table of 8-10 good names with their purpose]
```

#### 6. reference/converting-subagents.md (100-150 lines)

Content synthesized from Skill Builder's converting-sub-agents-to-skills.md:

```
# Converting Sub-Agents to Skills

## The Key Insight
Sub-agents explain WHAT they are → Skills explain WHEN to use them

## What Changes
| Aspect | Sub-Agent | Skill |
|--------|-----------|-------|
| Name | Noun form (code-reviewer) | Gerund form (reviewing-code) |
| Description | What it does | When to invoke it |
| Activation | @mention or Task agent | Automatic via description match |
| Structure | Single .md file | Directory with SKILL.md |

## Conversion Steps
1. Transform the name (noun → gerund)
2. Rewrite description (WHAT → WHEN, add trigger keywords)
3. Create directory structure
4. Move content to SKILL.md body
5. Extract reference material to reference/ files if >500 lines
6. Add frontmatter (name + description)
7. Validate against rules (see ./validation-rules.md)

## What to Preserve
[Instructions, examples, domain knowledge]

## What to Transform
[Name, description, activation model, structure]

## What to Remove
[Agent-specific metadata, tool restrictions, color/model specs]

## Conversion Checklist
[Checkbox list for verification]
```

#### 7. templates/basic-skill-template.md (80-100 lines)

Adapted from Claude Meta-Skill's basic template, restyled to commandbase enforcement pattern:

```yaml
---
name: [skill-name-gerund-form]
description: "Use this skill when [primary situation]. This includes [specific use cases]."
---
```

```
# [Skill Title]

[One paragraph: what this skill does and when it activates]

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law
[ONE ABSOLUTE RULE IN CAPS]
[Why this rule exists]

## The Gate Function
BEFORE [main action]:
1. [Verification step]
2. [Verification step]
3. [Verification step]
4. ONLY THEN: [Proceed]

## Process
### Step 1: [Name]
[Instructions]

### Step 2: [Name]
[Instructions]

### Step 3: [Name]
[Instructions]

## Red Flags - STOP and [Action]
- [Warning sign]
- [Warning sign]

## Rationalization Prevention
| Excuse | Reality |
|--------|---------|
| "[Common shortcut]" | [Why it's wrong] |

## The Bottom Line
[Bold summary]. This is non-negotiable.
```

#### 8. templates/workflow-skill-template.md (120-160 lines)

Adapted from Claude Meta-Skill's workflow template, restyled to commandbase pattern:

```yaml
---
name: [skill-name-gerund-form]
description: "Use this skill when [primary situation]. This includes [specific use cases]."
---
```

```
# [Skill Title]

[One paragraph: what this multi-step workflow does and when it activates]

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law
[ONE ABSOLUTE RULE IN CAPS]

## The Gate Function
BEFORE [main action]:
1. [Step]
2. [Step]
...
N. ONLY THEN: [Proceed]

## Initial Response
[What to do when invoked - read files, check state, present options]

### Mode A: [Primary Path]
[Steps for the common case]

### Mode B: [Alternative Path]
[Steps for the alternative case]

## Process

### Step 1: [Name]
[Detailed instructions with decision points]
- If [condition A]: [action]
- If [condition B]: [action]

### Step 2: [Name]
[Instructions with verification]

### Step 3: [Name]
[Instructions]

### Step N: [Name]
[Final step with output]

## Output Format
[What this skill produces - files, reports, etc.]

## Error Recovery
[What to do when things go wrong]

## Red Flags - STOP and [Action]
[Warning signs]

## Rationalization Prevention
[Table]

## The Bottom Line
[Summary]
```

### Success Criteria:
- [x] Directory `newskills/creating-skills/` exists with correct structure
- [x] `SKILL.md` has valid YAML frontmatter with `name: creating-skills` and description
- [x] `SKILL.md` is 200-300 lines
- [x] `SKILL.md` includes: Iron Law, Gate Function, Three Modes, Freedom Tiers, Complexity Check, RPI awareness, Red Flags, Rationalization Prevention, The Bottom Line
- [x] `SKILL.md` Gate Function includes research-check step (check `.docs/research/`, suggest `/rcode` for complex skills)
- [x] `reference/validation-rules.md` covers all rules from `quick_validate.py` (name regex, description limits, allowed frontmatter keys, structure rules)
- [x] `reference/description-writing-guide.md` includes the formula, 4C principles, good examples, bad examples with fixes
- [x] `reference/naming-conventions.md` covers gerund form, regex, max length, file naming
- [x] `reference/converting-subagents.md` covers WHAT→WHEN transformation, conversion steps, checklist
- [x] `templates/basic-skill-template.md` is a usable template with Iron Law/Gate Function/Red Flags/Bottom Line sections
- [x] `templates/workflow-skill-template.md` is a usable template with modes, decision points, error recovery
- [x] No content copied verbatim from reference repos
- [x] All reference/template files have substantive content (no TODOs, no placeholders, no "add content here")

---

## Key Design Decision: RPI Awareness

The Gate Function in SKILL.md includes a research-check step:

```
2. CHECK RESEARCH: Does `.docs/research/` have relevant analysis?
   - If YES: Read it, use as baseline for design decisions
   - If NO and skill is complex*: Suggest `/rcode` first
   - If NO and skill is simple: Proceed
```

**Complexity heuristic** (embedded in SKILL.md):
- **Simple** (proceed standalone): Single SKILL.md, familiar domain, clear workflow, <200 lines expected
- **Complex** (suggest `/rcode`): Will need `reference/` subdirectory, involves unfamiliar APIs or systems, cross-cutting concerns, user expresses uncertainty about structure

When suggesting `/rcode`, the skill should say something like:
> This skill looks complex enough to benefit from research first. Consider running `/rcode` to analyze similar patterns in the codebase before designing, then come back to build the skill.

When using existing research, the skill reads the `.docs/research/` file and uses its findings (file:line references, patterns, conventions) to inform design decisions rather than starting from scratch.

## Testing Strategy

### Manual Testing:
- Invoke `creating-skills` with a simple skill request → should proceed standalone
- Invoke with a complex skill request → should suggest `/rcode`
- Create a `.docs/research/` file first, then invoke → should detect and use it
- Test each mode: Create New, Edit Existing, Convert Sub-Agent
- Verify templates are usable as starting points

### Structural Verification:
- Count SKILL.md lines (target: 200-300)
- Verify frontmatter passes Anthropic validation rules
- Check all reference files have substantive content
- Confirm no verbatim copying from source repos

## References

- `.docs/plans/creating-skills-blueprint.md` - Original blueprint with proposed structure and prompt
- `.docs/research/01-28-2026-creating-skills-blueprint.md` - Research documenting all influences
- `newskills/learn/SKILL.md` - Example of non-RPI skill using enforcement pattern (172 lines)
- `newskills/checkpoint/SKILL.md` - Example of non-RPI skill with multiple operations (243 lines)
- `newskills/rcode/SKILL.md` - Research skill pattern for RPI awareness
- `C:/code/repo-library/skill-builder/SKILL.md` - Primary structure influence (274 lines)
- `C:/code/repo-library/Claude-meta-skill/create-skill-file-EN/SKILL.md` - Templates and freedom tiers
- `C:/code/repo-library/skills/skills/skill-creator/scripts/quick_validate.py` - Validation rules

---

## Implementation Complete

**Completed:** 2026-01-28 in commit `a7794e1` (Migrate skills to directory-based structure with Iron Laws)

### Final Implementation Summary

All 7 planned files were created with substantive content:

| File | Target Lines | Actual Lines | Status |
|------|--------------|--------------|--------|
| SKILL.md | 200-300 | 212 | Met |
| reference/validation-rules.md | 80-120 | 97 | Met |
| reference/description-writing-guide.md | 120-180 | 173 | Met |
| reference/naming-conventions.md | 60-90 | 92 | Met |
| reference/converting-subagents.md | 100-150 | 157 | Slightly over |
| templates/basic-skill-template.md | 80-100 | 83 | Met |
| templates/workflow-skill-template.md | 120-160 | 176 | Slightly over |

### Success Criteria Verification

All success criteria from Phase 1 were met:
- Directory structure created with correct hierarchy
- SKILL.md has valid frontmatter with `name` and `description`
- SKILL.md is 212 lines (within 200-300 target)
- All sections implemented: Iron Law, Gate Function, Three Modes, Freedom Tiers, Complexity Check, Red Flags, Rationalization Prevention, Bottom Line
- Gate Function includes research-check step with complexity heuristic
- All reference and template files have substantive content (no placeholders)
- Content synthesized from influences without verbatim copying
