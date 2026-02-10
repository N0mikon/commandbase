---
date: 2026-02-09
status: current
topic: "starting-projects skill analysis"
tags: [research, skill, starting-projects, project-setup, commandbase-core]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after plugin migration - refreshed file paths from ~/.claude/skills/ to plugins/commandbase-core/skills/, updated process to reflect /researching-frameworks delegation and .docs/references/ artifacts, added automatic-behaviors.md reference"
references:
  - plugins/commandbase-core/skills/starting-projects/SKILL.md
  - plugins/commandbase-core/skills/starting-projects/reference/question-design.md
  - plugins/commandbase-core/skills/starting-projects/reference/claude-md-guidelines.md
  - plugins/commandbase-core/skills/starting-projects/reference/automatic-behaviors.md
  - plugins/commandbase-core/skills/starting-projects/templates/claude-md-template.md
  - plugins/commandbase-core/skills/starting-projects/templates/project-setup-plan-template.md
---

# Research: starting-projects Skill

## Overview

The `starting-projects` skill (`plugins/commandbase-core/skills/starting-projects/SKILL.md`) initializes new greenfield projects from scratch. It guides users through project discovery, researches best practices via `/researching-frameworks`, and creates initial project structure including `.docs/references/` artifacts.

**Plugin**: commandbase-core
**Trigger phrases**: `new project`, `start a project`, `initialize a project`, `set up a new repo`, `scaffold a project`

## The Iron Law

```
NO RECOMMENDATION WITHOUT RESEARCH
```

Don't recommend tools, structures, or practices without researching current best practices first.

## The Gate Function

```
BEFORE recommending any technology or structure:

1. DISCOVER: Ask questions to understand project needs
2. RESEARCH: Use /researching-frameworks for current docs and best practices
3. SYNTHESIZE: Combine findings into recommendations
4. CONFIRM: Get user approval before proceeding
5. CREATE: Write plan and CLAUDE.md only after approval
6. ONLY THEN: Present next steps

Skip research = outdated recommendations
```

## Guiding Principles

- Research before recommending - use `/researching-frameworks` for current docs and best practices
- Confirm before writing - get user approval at each phase
- Keep CLAUDE.md minimal - under 60 lines, universally applicable
- Adapt to answers - skip irrelevant questions, add needed ones

## Process

### Phase 1: Project Discovery
Uses the AskUserQuestion tool in 2-4 question rounds to gather project information interactively. See `reference/question-design.md` for round-by-round structure:

- **Round 1 (Core Identity)**: Project type, primary language/framework, project purpose
- **Round 2 (Technical Details)**: Package manager, testing framework, additional tooling
- **Round 3 (Development Workflow)**: Build/run commands, code quality, special requirements
- **Round 4 (Scope & Goals, optional)**: MVP scope, key features

### Phase 2: Research Best Practices
Delegates to `/researching-frameworks` with the discovered tech stack:
- `/researching-frameworks` uses Context7 MCP (if available) + web search
- Classifies dependencies by tier and researches at appropriate depth
- Produces `.docs/references/` artifacts:
  - `framework-docs-snapshot.md` - Framework documentation snapshots
  - `dependency-compatibility.md` - Version compatibility matrix
  - `architecture-decisions.md` - Architecture decision records (ADRs)

### Phase 3: Create Development Plan
Write plan to `.docs/plans/project-setup.md` using the plan template:
- Fill in all sections from discovery and research findings
- Initial project structure
- Core dependencies with verified version ranges
- Setup steps and phases
- First feature phases (MVP goals)

### Phase 4: Generate CLAUDE.md
Creates a minimal CLAUDE.md using `templates/claude-md-template.md` and following `reference/claude-md-guidelines.md`. Key structure:

```markdown
# [Project Name]

[One sentence: what and why]

## Project Structure
[Brief directory layout - key directories only]

## Development
### Quick Start
### Key Commands
### Verification

## Architecture Notes
[2-3 sentences if non-obvious]

## Additional Context
[Pointers to detailed docs]

## Git Safety
See ~/.claude/CLAUDE.md for global git rules.

## Automatic Behaviors
See ~/.claude/CLAUDE.md for global behaviors.
```

### Phase 5: Wrap Up

```
Your project is initialized!

**Created:**
- `.docs/references/` - Framework documentation snapshots, compatibility matrix, architecture decisions
- `.docs/plans/project-setup.md` - Your development roadmap
- `CLAUDE.md` - Claude's project onboarding

**Next steps:**
1. Review both files and make any manual adjustments
2. Run `/implementing-plans .docs/plans/project-setup.md` to execute the setup
3. Start building!

**Your workflow going forward:**
- `/researching-frameworks` - Research framework docs and library APIs
- `/researching-code` - Research and document codebase patterns
- `/planning-code` - Create implementation plans for new features
- `/implementing-plans` - Execute plans
- `/validating-code` - Validate implementation against plan
- `/committing-changes` - Commit and push changes
- `/creating-prs` - Create pull requests
- `/ending-session` - End a session (merge, handoff, or discard)
- `/resuming-session` - Resume a session or pick up from a handover
```

## Integration Points

- Delegates research to `/researching-frameworks` (Phase 2)
- Creates plans for `/implementing-plans` (Phase 3)
- Sets up `.docs/` structure for other skills (references, plans, handoffs)
- Creates CLAUDE.md for project context (Phase 4)
- Lists workflow skills in wrap-up for ongoing development

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

## Hierarchy Awareness

The `claude-md-guidelines.md` reference file includes a Hierarchy Awareness section explaining that project CLAUDE.md inherits from global (`~/.claude/CLAUDE.md`).

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

The `claude-md-template.md` template's Automatic Behaviors section references `~/.claude/CLAUDE.md` for global behaviors instead of inlining specific instructions.

## File Reference

- Main: `plugins/commandbase-core/skills/starting-projects/SKILL.md`
- Question design: `plugins/commandbase-core/skills/starting-projects/reference/question-design.md`
- CLAUDE.md guidelines: `plugins/commandbase-core/skills/starting-projects/reference/claude-md-guidelines.md`
- Automatic behaviors: `plugins/commandbase-core/skills/starting-projects/reference/automatic-behaviors.md`
- CLAUDE.md template: `plugins/commandbase-core/skills/starting-projects/templates/claude-md-template.md`
- Plan template: `plugins/commandbase-core/skills/starting-projects/templates/project-setup-plan-template.md`
