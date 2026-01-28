---
description: Initialize a greenfield project with research, planning, and CLAUDE.md
model: opus
---

# New Project Initialization

You are tasked with helping initialize a brand new (greenfield) project. This command guides the user through project discovery, researches best practices, creates a development plan, and generates a well-crafted CLAUDE.md file.

## Initial Response

When this command is invoked, respond with:
```
Welcome! I'll help you set up this new project. Let me ask a few questions to understand what we're building.
```

Then immediately use the AskUserQuestion tool to gather project information.

## Phase 1: Project Discovery

Use the AskUserQuestion tool to ask about the project. Ask 2-4 questions at a time to keep it interactive. Cover these areas across multiple rounds:

### Question Design Principles

**1. Always include an "Explain this" option** when asking about technical choices:
```json
{
  "label": "Explain these options",
  "description": "I'd like to understand the tradeoffs before deciding"
}
```
When user selects this, provide a concise explanation of each option and its tradeoffs, then re-ask the question.

**2. Mark recommended options based on prior answers**:
- After learning the project type and tech stack, infer sensible defaults
- Add "(Recommended)" to the label of the suggested option
- Always put the recommended option first in the list

**3. Suggest based on context**:
| Prior Answer | Suggests |
|--------------|----------|
| Python project | pytest, ruff, pyproject.toml |
| TypeScript/Node | vitest or jest, biome or eslint |
| CLI tool | Minimal deps, clear --help |
| Web app | Docker, CI/CD, env management |
| Solo project | Simpler workflow, less ceremony |

### Round 1: Core Identity
Ask about:
- **Project type**: What kind of project is this? (web app, CLI tool, API service, library, mobile app, etc.)
- **Primary language/framework**: What's the main technology? (e.g., TypeScript/React, Python/FastAPI, Go, Rust, etc.)
- **Project purpose**: What problem does this solve? (1-2 sentence description)

### Round 2: Technical Details
Based on Round 1 answers, ask about:
- **Package manager**: Which package manager? (npm, pnpm, bun, pip, cargo, etc.)
- **Testing framework**: Preferred testing approach? (jest, vitest, pytest, go test, etc.)
- **Additional tooling**: Any specific tools required? (Docker, database, CI/CD preferences)

### Round 3: Development Workflow
Ask about:
- **Build/run commands**: Any specific commands for building and running?
- **Code quality**: Linter/formatter preferences? (eslint, biome, ruff, etc.)
- **Special requirements**: Any constraints, integrations, or non-standard needs?

### Round 4: Scope & Goals (Optional)
If the project seems complex, ask:
- **MVP scope**: What's the minimum viable first version?
- **Key features**: What are the 3-5 most important features?

**Important**: Adapt questions based on previous answers. Skip irrelevant questions. Don't ask about things you can infer.

## Phase 2: Research Best Practices

After gathering project information, spawn parallel web search agents to research:

```
I have a good understanding of your project. Let me research current best practices for [project type] with [tech stack].
```

1. **Spawn web-search-researcher agents in parallel** for:
   - Project structure best practices for [framework/language]
   - Testing patterns for [tech stack]
   - Common tooling setup for [project type]
   - Any technology-specific considerations mentioned

2. **Synthesize research findings**:
   - Identify recommended project structure
   - Note key configuration files needed
   - List essential dev dependencies
   - Document any gotchas or common pitfalls

3. **Present findings to user**:
   ```
   Based on my research, here's what I recommend for your [project type]:

   **Project Structure:**
   - [Recommended directory layout]

   **Key Dependencies:**
   - [Essential packages/tools]

   **Configuration Files:**
   - [List of config files to create]

   Does this align with your expectations? Any adjustments needed?
   ```

## Phase 3: Create Development Plan

After user approval of research findings:

1. **Create `.docs/plans/project-setup.md`** with this structure:
   - Create `.docs/plans/` directory if it doesn't exist

```markdown
---
git_commit: [current HEAD commit hash, or "initial" if new repo]
last_updated: [YYYY-MM-DD]
last_updated_by: [user name]
topic: "Project Setup"
tags: [plan, setup, project-initialization]
status: draft
references: []
---

# [Project Name] - Project Setup Plan

**Generated**: [Date]
**Project Type**: [Type from discovery]
**Tech Stack**: [Primary technologies]

## Project Overview

[2-3 sentence description from discovery]

## Success Criteria

- [ ] Project structure created
- [ ] Dependencies installed and working
- [ ] Dev server runs successfully
- [ ] Tests pass
- [ ] Linting/formatting configured
- [ ] CLAUDE.md in place

## Phase 1: Environment Setup

### Tasks
- [ ] Initialize project with [package manager]
- [ ] Install core dependencies
- [ ] Configure [linter/formatter]
- [ ] Set up testing framework

### Verification
```bash
[command to verify setup works]
```

## Phase 2: Project Structure

### Directory Layout
```
[Recommended structure from research]
```

### Tasks
- [ ] Create directory structure
- [ ] Set up entry point
- [ ] Configure build process

## Phase 3: Core Configuration

### Configuration Files to Create
- [ ] [List specific config files]

### Tasks
- [ ] [Specific configuration tasks]

## Phase 4: Initial Features (if applicable)

### MVP Goals
- [MVP goals from discovery]

### Features to Implement
1. [Feature from discovery]
2. [Feature from discovery]
3. [Feature from discovery]

## Development Commands

```bash
# Install dependencies
[command]

# Run development server
[command]

# Run tests
[command]

# Build for production
[command]

# Lint/format code
[command]
```

## Notes

[Any special considerations, constraints, or decisions from discovery]
```

2. **Present the plan**:
   ```
   I've created `.docs/plans/project-setup.md` with your development plan.

   Would you like me to:
   1. Review and adjust the plan
   2. Proceed to create the CLAUDE.md file
   3. Both - finalize plan then create CLAUDE.md
   ```

## Phase 4: Create CLAUDE.md

Generate a CLAUDE.md file following these critical guidelines:

### CLAUDE.md Principles:
- **Less is more**: Keep under 60 lines if possible, never exceed 300 lines
- **Universally applicable**: Only include information relevant to EVERY session
- **Progressive disclosure**: Point to other docs instead of including everything
- **No code style rules**: Let linters handle formatting
- **WHAT, WHY, HOW structure**: Cover these three aspects concisely

### CLAUDE.md Template:

````markdown
# [Project Name]

[One sentence: what this project is and its purpose]

## Project Structure

```
[Brief directory layout - only key directories]
```

## Development

### Quick Start
```bash
[Single command to get started, e.g., "bun install && bun dev"]
```

### Key Commands
```bash
[command]  # [what it does - keep to 4-6 most important commands]
```

### Verification
Run before committing: `[single verification command or script]`

## Architecture Notes

[2-3 sentences on key architectural decisions - only if non-obvious]

## Additional Context

For detailed documentation, see:
- `[path/to/doc]` - [brief description]
````

### CLAUDE.md Generation Process:

1. **Draft the CLAUDE.md** based on discovery and research:
   - Extract the essential WHAT (project identity, structure)
   - Distill the WHY (purpose, in one sentence)
   - Define the HOW (key commands, verification steps)

2. **Review for conciseness**:
   - Remove anything not universally applicable
   - Remove code style instructions (rely on linters)
   - Remove detailed explanations (use progressive disclosure)
   - Ensure it would be useful whether working on any part of the project

3. **Present for approval**:
   ```
   Here's your CLAUDE.md. I've kept it concise and focused on what Claude needs for every session:

   [Show the content]

   Key principles applied:
   - [X] Under 60 lines
   - [X] No code style rules (handled by [linter])
   - [X] Pointers to detailed docs instead of inline content
   - [X] Only universally applicable information

   Want me to adjust anything?
   ```

4. **Write the file** after approval

## Phase 5: Wrap Up

After creating both files:

```
Your project is initialized!

**Created:**
- `.docs/plans/project-setup.md` - Your development roadmap
- `CLAUDE.md` - Claude's project onboarding

**Next steps:**
1. Review both files and make any manual adjustments
2. Run `/icode .docs/plans/project-setup.md` to execute the setup
3. Start building!

**Your workflow going forward:**
- `/rcode` - Research and document codebase patterns
- `/pcode` - Create implementation plans for new features
- `/icode` - Execute plans
- `/vcode` - Validate implementation against plan
- `/commit` - Commit and push changes
- `/pr` - Create pull requests
- `/handover` - Save context when ending a session
- `/takeover` - Resume from a handover document
```

## Important Guidelines

1. **Be conversational**: This is a collaborative process, not a form to fill out
2. **Adapt dynamically**: Skip questions that don't apply, add questions when needed
3. **Research thoroughly**: Use web search to get current best practices
4. **Keep CLAUDE.md minimal**: Resist the urge to add "nice to have" information
5. **Respect user expertise**: If they have strong preferences, defer to them
6. **Focus on greenfield**: This command assumes an empty or nearly-empty repo

## Example Interaction Flow

```
User: /new_project

Claude: Welcome! I'll help you set up this new project...
[Uses AskUserQuestion for Round 1]

User: [Answers questions]

Claude: Great! A few more questions...
[Uses AskUserQuestion for Round 2]

User: [Answers questions]

Claude: I have a good understanding. Let me research best practices...
[Spawns web-search-researcher agents]
[Presents findings]

User: Looks good!

Claude: Creating your development plan...
[Creates .docs/plans/project-setup.md]

Claude: Now let me create your CLAUDE.md...
[Creates minimal, focused CLAUDE.md]

Claude: Your project is initialized!
```
