# Research: creating-skills Skill

## Overview

The `creating-skills` skill (`~/.claude/skills/creating-skills/SKILL.md`) creates new Claude Code skills from scratch, editing existing skills, or converting sub-agents into skills. It enforces the official skill specification.

**Invocation**: `/creating-skills`, `create a skill`, `make a new skill`

## Purpose

Create and validate skills:
- Writing SKILL.md files
- Choosing skill names (gerund form)
- Crafting invocation-focused descriptions
- Organizing supporting files with progressive disclosure
- Validating skill structure against official specification

## Skill Structure

```
~/.claude/skills/[skill-name]/
├── SKILL.md                    # Required - main skill file
├── reference/                  # Optional - supporting docs
│   └── [topic].md
├── templates/                  # Optional - output templates
│   └── [template].md
├── scripts/                    # Optional - automation
└── assets/                     # Optional - images, data
```

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

### Structure Validation
- SKILL.md exists at root
- Under 500 lines
- Reference nesting max 1 level
- No extraneous files (README, CHANGELOG)

## Enforcement Pattern

Skills should include:
1. **Iron Law**: Core non-negotiable rule
2. **Gate Function**: Steps before main action
3. **Red Flags**: Warning signs to stop
4. **Rationalization Prevention**: Common excuses and reality
5. **Bottom Line**: Summary principle

## Process

### Step 1: Understand Requirements
Read plan or user request to understand:
- What the skill does
- When it activates
- What output it produces

### Step 2: Choose Name
Select gerund-form name:
- `committing-changes` not `commit`
- `reviewing-security` not `security-review`

### Step 3: Write Description
Follow WHEN formula:
```
"Use this skill when [primary situation]. This includes [specific use case], [another use case], and [edge case]. Trigger phrases: '[phrase1]', '[phrase2]'."
```

### Step 4: Structure Content
Apply progressive disclosure:
- Core content in SKILL.md
- Details in reference/ files
- Templates in templates/ files

### Step 5: Add Enforcement Pattern
Include Iron Law, Gate Function, Red Flags, Rationalization Prevention, Bottom Line.

### Step 6: Validate
Run validation checks against official rules.

## Output

```
SKILL CREATED
=============

Location: ~/.claude/skills/[name]/

Files:
- SKILL.md ([N] lines)
- reference/[files]
- templates/[files]

Validation: PASS

Deploy with:
cp -r newskills/[name] ~/.claude/skills/
```

## File References

- Main: `~/.claude/skills/creating-skills/SKILL.md`
- Validation rules: `~/.claude/skills/creating-skills/reference/validation-rules.md`
- Description guide: `~/.claude/skills/creating-skills/reference/description-writing-guide.md`
