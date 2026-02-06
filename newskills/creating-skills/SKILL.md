---
name: creating-skills
description: "Use this skill when creating new Claude Code skills from scratch, editing existing skills to improve their structure or descriptions, or converting Claude Code sub-agents into skills. This includes writing SKILL.md files, choosing skill names, crafting invocation-focused descriptions, organizing supporting files with progressive disclosure, and validating skill structure against the official specification."
---

# Creating Skills

You are building, editing, or converting Claude Code skills. Skills are the primary mechanism for extending Claude Code with reusable domain knowledge. This skill guides you through the process with structured workflows, validated templates, and quality gates.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SKILL WITHOUT VALIDATED DESCRIPTION AND STRUCTURE
```

The description field is the triggering mechanism - it determines when Claude invokes the skill. The structure determines usability. Both must be right before the skill ships.

**No exceptions:**
- Don't write the body before the description
- Don't skip validation because "it's a simple skill"
- Don't copy another skill's description and swap keywords
- Don't create files without intention-revealing names

## The Gate Function

```
BEFORE writing any SKILL.md:

0. AGENT CHECK: Is the user actually asking to create an AGENT, not a skill?
   - If they want a single .md file with tools/model/system prompt: REDIRECT to `/creating-agents`
   - If they want a SKILL.md directory with intent-matching description: proceed here
1. GATHER: What task does this skill handle? When should it activate?
   Personal (~/.claude/skills/) or project (.claude/skills/)?
2. CHECK RESEARCH: Does `.docs/research/` have relevant analysis?
   - If YES: Read it, use findings as baseline for design decisions
   - If NO and skill is complex*: Suggest `/researching-codebases` first
   - If NO and skill is simple: Proceed directly
3. DESIGN: Name (gerund, kebab-case), description (formula), freedom tier
4. CHOOSE: Template from ./templates/ (basic or workflow)
5. WRITE: Create skill files following the template
6. VALIDATE: Run checklist from ./reference/validation-rules.md
7. ONLY THEN: Declare the skill complete

*Complex = needs reference/ subdirectory, involves unfamiliar APIs or systems,
cross-cutting concerns, or user expresses uncertainty about structure
```

## Complexity Check

Decide whether to proceed standalone or suggest research first.

**Simple - proceed directly:**
- Single SKILL.md, no supporting files needed
- Familiar domain with clear patterns
- Well-defined workflow under 200 lines
- User knows exactly what they want

**Complex - suggest `/researching-codebases` first:**
- Will need `reference/` or `templates/` subdirectories
- Involves unfamiliar APIs, systems, or protocols
- Cross-cutting concerns spanning multiple tools
- User says "I'm not sure how to structure this"

When suggesting research:
> This skill looks complex enough to benefit from upfront research. Consider running `/researching-codebases` to analyze similar patterns and existing implementations, then return here to build the skill with those findings as a baseline.

When existing research is found:
> Found relevant research at `.docs/research/[file]`. Using its findings to inform design decisions.

## Three Modes

### Mode 1: Create New Skill

Build a skill from scratch using the 5-step workflow.

**Step 1: Gather Requirements**

Ask and answer these questions before designing anything:

- What task does this skill handle? Be specific - not "helps with testing" but "writes and runs integration tests for REST APIs."
- When should Claude invoke it? List 5 specific situations a user might describe.
- Personal (`~/.claude/skills/`) or project (`.claude/skills/`) scope?
- Are there similar existing skills to learn from? Read them first.
- How much existing Claude knowledge applies? If Claude already knows the domain well, focus the skill on project-specific patterns, not general knowledge.

**Step 2: Choose Freedom Tier**

See the Freedom Tiers section below. Match the tier to the task's error tolerance and domain variability. Most skills land in Medium. Only use Low for tasks where exact steps matter (deployment, migration). Only use High for genuinely creative tasks.

**Step 3: Design the Skill**

- **Name**: Gerund form, kebab-case (see ./reference/naming-conventions.md)
- **Description**: Use the formula from ./reference/description-writing-guide.md
  - Write the description FIRST, before the body
  - Test it mentally: "If a user said [phrase], would this description match?"
- **Template**: Basic (./templates/basic-skill-template.md) for single-workflow skills, or Workflow (./templates/workflow-skill-template.md) for multi-mode or multi-step processes
- **Supporting files**: Plan reference docs if body would exceed 300 lines
- **Frontmatter**: Only `name` and `description` are required. Add `license` if distributing.

**Step 4: Write the Skill**

- Start with YAML frontmatter (`name` + `description`)
- Write the body following the chosen template structure
- Keep SKILL.md under 500 lines (target: 200-300 lines)
- Add reference files with intention-revealing names (not `reference.md` or `helpers.md`)
- Use skinny pointers to reference files: `See ./reference/filename.md for [topic]`
- Write for Claude, not for humans - instructions should be actionable, not explanatory

**Step 5: Validate**

Run every item in ./reference/validation-rules.md. Fix all issues before declaring done.

Present the completed skill:
```
Skill created: [name]
Location: [path]
Files: [count] ([list])
Description: [first 80 chars...]
Validation: All checks passed
```

### Mode 2: Edit Existing Skill

Improve an existing skill's structure, description, or content.

1. **Read first**: Read the existing SKILL.md completely. Understand its intent, workflow, and current trigger conditions before changing anything.
2. **Diagnose**: Identify specific improvement areas:
   - Description: Is it triggering correctly? Does it follow the formula?
   - Structure: Is SKILL.md too long? Should content move to reference files?
   - Content: Are instructions actionable? Are examples concrete?
   - Frontmatter: Does it have both `name` and `description`?
3. **Preserve intent**: Apply changes while keeping the skill's core workflow intact. Don't restructure a working skill just for style points.
4. **Re-validate**: Run the full checklist from ./reference/validation-rules.md after changes.
5. **Show diffs**: For description changes, show before/after so the user can confirm the trigger conditions are still correct.

### Mode 3: Convert Sub-Agent to Skill

Transform a Claude Code sub-agent into a skill. The core shift: sub-agents explain WHAT they are, skills explain WHEN to use them.

**Direction check:** This mode converts Agent -> Skill. If the user wants to convert a Skill -> Agent, redirect to `/creating-agents` Mode 3.

1. **Read the sub-agent** file completely. Identify its purpose, instructions, and domain knowledge.
2. **Transform the name** from noun form to gerund form (e.g., `code-reviewer` becomes `reviewing-code`).
3. **Rewrite the description** using the WHEN formula. Strip "I am..." / "This agent..." language.
4. **Create the directory structure**: `skill-name/SKILL.md` at minimum.
5. **Move content** into SKILL.md body. Remove agent-specific metadata (`model`, `color`, routing config).
6. **Split if needed**: If content exceeds 300 lines, extract reference material to `reference/` files.
7. **Add frontmatter** with `name` and formula-based `description`.
8. **Validate** against ./reference/validation-rules.md.

See ./reference/converting-subagents.md for the detailed conversion guide with examples and checklist.

## Freedom Tiers

Choose how prescriptive the skill should be based on error tolerance.

| Tier | When to Use | Writing Approach |
|------|-------------|-----------------|
| **High** | Creative tasks, many valid outcomes | Guiding principles and goals, not specific steps |
| **Medium** | Standard tasks, recommended patterns | Parameterized examples, default flows with alternatives |
| **Low** | Error-prone tasks, strict execution | Step-by-step procedures, exact commands, verification gates |

**Decision criteria:**
- Is there one correct answer? → Low freedom
- Does the task need to adapt to varied scenarios? → High freedom
- Are errors costly or hard to reverse? → Low freedom
- Is the domain well-understood by Claude already? → High freedom (avoid teaching what Claude knows)

## Sibling Skill: /creating-agents

`/creating-skills` and `/creating-agents` are siblings, not overlapping:

| Aspect | /creating-skills (this skill) | /creating-agents |
|--------|-------------------------------|-----------------|
| Creates | `SKILL.md` + reference directory | Single `.md` agent files |
| Names | Gerund form (`reviewing-code`) | Noun form (`code-reviewer`) |
| Descriptions | "Use this skill when..." (intent matching) | Capability + delegation trigger |
| Converts | Agents -> Skills (Mode 3) | Skills -> Agents (Mode 3) |

**Redirect to `/creating-agents` when:**
- The user wants to create a sub-agent (single `.md` file with tools, model, system prompt)
- The user wants to convert a skill into an agent
- The user says "create an agent", "build a subagent", or describes agent-like functionality

**Stay in `/creating-skills` when:**
- The user wants to create a skill (directory with SKILL.md, intent-matching activation)
- The user wants to convert an agent into a skill
- The user says "create a skill", "build a skill", or describes skill-like functionality

## Reference Files

These contain the detailed rules and guidance referenced throughout this workflow:

- See ./reference/validation-rules.md for official spec constraints and the validation checklist
- See ./reference/description-writing-guide.md for the description formula, 4C principles, and examples
- See ./reference/naming-conventions.md for gerund form, kebab-case rules, and naming examples
- See ./reference/converting-subagents.md for the sub-agent migration workflow

## Templates

Start from one of these when creating a new skill:

- See ./templates/basic-skill-template.md for simple, linear skills with a single workflow
- See ./templates/workflow-skill-template.md for multi-step process skills with modes and decision points

## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- User actually wants an agent, not a skill - redirect to `/creating-agents`
- Writing SKILL.md body before finalizing the description
- Description says WHAT the skill does but not WHEN to invoke it
- Name uses noun form instead of gerund form (e.g., `code-reviewer` instead of `reviewing-code`)
- Copying another skill's description and swapping keywords
- SKILL.md exceeding 500 lines without splitting to reference files
- Reference files with generic names (`reference.md`, `helpers.md`, `utils.md`)
- Template has TODOs or placeholder text left in final output
- Skipping validation because the skill "looks right"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The description is good enough" | Run it through the 4C check. Every word matters for triggering. |
| "I'll add the reference files later" | If the body is already long, split now. Later means never. |
| "This is a simple skill, no validation needed" | Simple skills still need valid frontmatter and clear triggers. |
| "The name doesn't need to be gerund" | Gerund form is the convention. Follow it unless there's a strong reason not to. |
| "I already know how to structure this" | Read the research first if it exists. Prior analysis prevents blind spots. |
| "Validation is just bureaucracy" | Validation catches the mistakes that break skill loading. |

## The Bottom Line

**No skill ships without a validated description and verified structure.**

Gather requirements. Check for research. Design with intention. Write from templates. Validate every field.

This is non-negotiable. Every skill. Every time.
