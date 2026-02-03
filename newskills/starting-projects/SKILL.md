---
name: starting-projects
description: "Use this skill when initializing a new greenfield project from scratch. This includes guiding users through project discovery questions, researching current best practices for their tech stack, creating a development plan in .docs/plans/, and generating a minimal CLAUDE.md file. Activate when the user says 'new project', 'start a project', 'initialize a project', 'set up a new repo', or 'scaffold a project'."
---

# Starting Projects

You are tasked with helping initialize a brand new (greenfield) project. This skill guides the user through project discovery, researches best practices, creates a development plan, and generates a well-crafted CLAUDE.md file.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO RECOMMENDATION WITHOUT RESEARCH
```

Don't recommend tools, structures, or practices without researching current best practices first.

**Guiding Principles:**
- Research before recommending - spawn web-search agents for current best practices
- Confirm before writing - get user approval at each phase
- Keep CLAUDE.md minimal - under 60 lines, universally applicable
- Adapt to answers - skip irrelevant questions, add needed ones

## The Gate Function

```
BEFORE recommending any technology or structure:

1. DISCOVER: Ask questions to understand project needs
2. RESEARCH: Spawn web-search agents for current best practices
3. SYNTHESIZE: Combine findings into recommendations
4. CONFIRM: Get user approval before proceeding
5. CREATE: Write plan and CLAUDE.md only after approval
6. ONLY THEN: Present next steps

Skip research = outdated recommendations
```

## Initial Response

When this skill is invoked, respond with:
```
Welcome! I'll help you set up this new project. Let me ask a few questions to understand what we're building.
```

Then immediately use the AskUserQuestion tool to gather project information.

## Phase 1: Project Discovery

Use the AskUserQuestion tool to ask about the project. Ask 2-4 questions at a time to keep it interactive.

See ./reference/question-design.md for question design principles, context-based suggestions, and the full round-by-round discovery structure.

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

1. **Create `.docs/plans/project-setup.md`** using the template at ./templates/project-setup-plan-template.md
   - Create `.docs/plans/` directory if it doesn't exist
   - Fill in all sections from discovery and research findings

2. **Present the plan**:
   ```
   I've created `.docs/plans/project-setup.md` with your development plan.

   Would you like me to:
   1. Review and adjust the plan
   2. Proceed to create the CLAUDE.md file
   3. Both - finalize plan then create CLAUDE.md
   ```

## Phase 4: Create CLAUDE.md

Generate a CLAUDE.md file using the template and process at ./templates/claude-md-template.md.

For detailed guidelines on what to include and exclude, see ./reference/claude-md-guidelines.md.

For the automatic behaviors section, see ./reference/automatic-behaviors.md.

## Phase 5: Wrap Up

After creating both files:

```
Your project is initialized!

**Created:**
- `.docs/plans/project-setup.md` - Your development roadmap
- `CLAUDE.md` - Claude's project onboarding

**Next steps:**
1. Review both files and make any manual adjustments
2. Run `/implementing-plans .docs/plans/project-setup.md` to execute the setup
3. Start building!

**Your workflow going forward:**
- `/researching-codebases` - Research and document codebase patterns
- `/planning-codebases` - Create implementation plans for new features
- `/implementing-plans` - Execute plans
- `/validating-implementations` - Validate implementation against plan
- `/committing-changes` - Commit and push changes
- `/creating-pull-requests` - Create pull requests
- `/handing-over` - Save context when ending a session
- `/taking-over` - Resume from a handover document
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

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

## Important Guidelines

1. **Be conversational**: This is a collaborative process, not a form to fill out
2. **Adapt dynamically**: Skip questions that don't apply, add questions when needed
3. **Research thoroughly**: Use web search to get current best practices
4. **Keep CLAUDE.md minimal**: Resist the urge to add "nice to have" information
5. **Respect user expertise**: If they have strong preferences, defer to them
6. **Focus on greenfield**: This skill assumes an empty or nearly-empty repo

## Example Interaction Flow

```
User: /starting-projects

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

## The Bottom Line

**Interactive, but principled.**

Research best practices. Confirm decisions. Keep CLAUDE.md minimal. Adapt to the user.
