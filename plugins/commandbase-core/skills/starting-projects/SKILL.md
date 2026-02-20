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
- Research before recommending - use `/researching-frameworks` for current docs and best practices
- Confirm before writing - get user approval at each phase
- Keep CLAUDE.md minimal - under 60 lines, universally applicable
- Adapt to answers - skip irrelevant questions, add needed ones

## The Gate Function

```
BEFORE recommending any technology or structure:

1. DISCOVER: Ask questions to understand project needs
2. RESEARCH: Use `/researching-frameworks` for current docs and best practices
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

Then immediately check the directory state before gathering project information.

## Phase 0: Repository Layout

Before discovery, detect the starting state:

```bash
git rev-parse --git-dir 2>/dev/null
```

**If already a git repo:** Skip to Phase 1.

**If not a git repo (empty or non-git directory):** Check if the current path looks like a base container directory (e.g., `/c/code/project-name/`). Offer the bare-repo + worktree layout:

```
Before we start — do you want to use the bare-repo + worktree layout?

This creates isolated directories for each piece of work:
  /c/code/{project}/main/       ← your daily working directory
  /c/code/{project}/feature/    ← session branches (created later)

Benefits: parallel branches, clean isolation.

If not, I'll do a standard git init here.
```

**If user wants bare-repo layout**, set it up before continuing:

```bash
# Initialize bare repo in current directory
git init --bare .bare

# Create main worktree (the daily working directory)
git -C .bare worktree add ../main -b main

```

Then continue all remaining phases (discovery, research, plan, CLAUDE.md) inside the `main/` worktree. Notify the user:

```
Bare-repo layout created. Continuing project setup in:
/c/code/{project}/main/

After setup, always work from this directory.
```

**If user wants standard layout**, run `git init` in the current directory and continue to Phase 1.

## Phase 1: Project Discovery

Use the AskUserQuestion tool to ask about the project. Ask 2-4 questions at a time to keep it interactive.

See ./reference/question-design.md for question design principles, context-based suggestions, and the full round-by-round discovery structure.

## Phase 2: Research Best Practices

After gathering project information, delegate to `/researching-frameworks` for current documentation:

```
I have a good understanding of your project. Let me research current documentation and best practices for [project type] with [tech stack].
```

1. **Invoke `/researching-frameworks`** with the discovered tech stack:
   - Pass the primary framework, language, and key dependencies from Phase 1
   - `/researching-frameworks` will use Context7 MCP (if available) + web search
   - It classifies dependencies by tier and researches at appropriate depth
   - It produces `.docs/references/` artifacts (framework snapshots, compatibility matrix, ADRs)

2. **Review the research output**:
   - Read the generated `.docs/references/framework-docs-snapshot.md`
   - Read `.docs/references/dependency-compatibility.md` for version conflicts
   - Review architecture decisions in `.docs/references/architecture-decisions.md`

3. **Present findings to user**:
   ```
   Based on current documentation research, here's what I recommend for your [project type]:

   **Project Structure:**
   - [Recommended directory layout from researched docs]

   **Key Dependencies (verified compatible):**
   - [Essential packages with verified version ranges]

   **Configuration Files:**
   - [List of config files to create]

   **Architecture Decisions:**
   - [Key ADRs from research]

   Full research saved to `.docs/references/`. Does this align with your expectations?
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
- `.docs/references/` - Framework documentation snapshots, compatibility matrix, architecture decisions
- `.docs/plans/project-setup.md` - Your development roadmap
- `CLAUDE.md` - Claude's project onboarding

**Next steps:**
1. Review both files and make any manual adjustments
2. Run `/implementing-plans .docs/plans/project-setup.md` to execute the setup
3. Start building!

**Your workflow going forward:**
- `/starting-worktree` - Create isolated worktrees for features/fixes (bare-repo layout only)
- `/researching-frameworks` - Research framework docs and library APIs
- `/researching-code` - Research and document codebase patterns
- `/planning-code` - Create implementation plans for new features
- `/implementing-plans` - Execute plans
- `/validating-code` - Validate implementation against plan
- `/committing-changes` - Commit and push changes
- `/creating-prs` - Create pull requests
- `/ending-worktree` - Merge or discard a worktree
- `/handing-over` - Create a handover document for context transfer
- `/extracting-patterns` - Extract reusable learnings from conversations
```

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

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
3. **Research thoroughly**: Use `/researching-frameworks` to get current documentation and best practices
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

Claude: I have a good understanding. Let me research current documentation...
[Invokes /researching-frameworks with discovered tech stack]
[Reviews .docs/references/ artifacts]
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
