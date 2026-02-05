# Research: starting-projects Skill

## Overview

The `starting-projects` skill (`~/.claude/skills/starting-projects/SKILL.md`) initializes new greenfield projects from scratch. It guides users through project discovery, researches best practices, and creates initial project structure.

**Trigger phrases**: `new project`, `start a project`, `initialize a project`, `set up a new repo`, `scaffold a project`

## The Iron Law

```
NO RECOMMENDATION WITHOUT RESEARCH
```

Don't recommend tools, structures, or practices without researching current best practices first.

## The Gate Function (SKILL.md:28-39)

```
BEFORE recommending any technology or structure:

1. DISCOVER: Ask questions to understand project needs
2. RESEARCH: Spawn web-search agents for current best practices
3. SYNTHESIZE: Combine findings into recommendations
4. CONFIRM: Get user approval before proceeding
5. CREATE: Write plan and CLAUDE.md only after approval
6. ONLY THEN: Present next steps
```

## Purpose

Scaffold new projects with:
- Project discovery questions
- Current best practices research
- Development plan creation
- Minimal CLAUDE.md generation

## Process

### Step 1: Project Discovery
Ask questions to understand:
- What is the project's purpose?
- What tech stack to use?
- What are the key features?
- Any specific requirements?

### Step 2: Research Best Practices
For the chosen tech stack:
- Current recommended structure
- Testing frameworks
- Build tools
- Common patterns

### Step 3: Create Development Plan
Write plan to `.docs/plans/`:
- Initial project structure
- Core dependencies
- Setup steps
- First feature phases

### Step 4: Generate CLAUDE.md
Create minimal project instructions:
```markdown
# [Project Name]

[Brief description]

## Directory Structure

```
project/
├── src/           # Source code
├── tests/         # Test files
├── .docs/         # Plans, research, handoffs
└── scripts/       # Build/deploy scripts
```

## Development

[Key commands]

## Additional Context

- `.docs/handoffs/` - Latest session context
```

### Step 5: Initialize Git
- Create `.gitignore`
- Initialize repository
- Create initial commit

## Output

```
PROJECT INITIALIZED
===================

Created:
- CLAUDE.md (project instructions)
- .gitignore
- .docs/plans/[initial-plan].md
- src/ (empty)
- tests/ (empty)

Next steps:
- Review .docs/plans/[plan].md
- Run /implementing-plans to start development
```

## Integration Points

- Creates plans for `/implementing-plans`
- Sets up `.docs/` structure for other skills
- Creates CLAUDE.md for project context

## Red Flags - STOP and Verify

- Recommending tools without researching current best practices
- Writing CLAUDE.md over 60 lines
- Including code style rules in CLAUDE.md (use linters)
- Skipping user confirmation at major decision points
- Assuming technology choices without asking

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know this tech stack well" | Best practices change. Research anyway. |
| "User seems in a hurry" | Bad foundations waste more time. Do the research. |
| "CLAUDE.md needs more context" | 60 lines max. Move details to .docs/ if needed. |
| "This is a common setup" | Common doesn't mean current. Verify best practices. |
| "I'll ask about that later" | Ask now. Discovery happens before research. |

## Hierarchy Awareness (Added 2026-02-05)

The `claude-md-guidelines.md` reference file now includes a Hierarchy Awareness section explaining that project CLAUDE.md inherits from global (`~/.claude/CLAUDE.md`).

**Don't duplicate in project CLAUDE.md:**
- Security NEVER rules (defined globally)
- Git safety rules (defined globally)
- Personal identity/accounts (defined globally)
- Pattern learning behaviors (defined globally)

**Do include in project CLAUDE.md:**
- Project-specific identity and purpose
- This project's directory structure
- This project's commands
- This project's verification steps
- Pointers to this project's .docs/

The `claude-md-template.md` template's Automatic Behaviors section now references `~/.claude/CLAUDE.md` for global behaviors instead of inlining specific instructions.

## File Reference

- Main: `~/.claude/skills/starting-projects/SKILL.md`
- Question design: `~/.claude/skills/starting-projects/reference/question-design.md`
- CLAUDE.md guidelines: `~/.claude/skills/starting-projects/reference/claude-md-guidelines.md`
- CLAUDE.md template: `~/.claude/skills/starting-projects/templates/claude-md-template.md`
- Plan template: `~/.claude/skills/starting-projects/templates/project-setup-plan-template.md`
