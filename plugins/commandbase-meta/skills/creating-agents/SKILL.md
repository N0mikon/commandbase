---
name: creating-agents
description: "Use this skill when creating new Claude Code agents (subagents) from scratch, editing existing agents to improve their descriptions or system prompts, or converting skills into agents. This includes writing agent .md files, choosing agent names, crafting delegation-trigger descriptions, designing system prompts using the Contract Format, selecting tool sets, and validating agent structure against the specification."
---

# Creating Agents

You are building, editing, or converting Claude Code agents (subagents). Agents are single Markdown files with YAML frontmatter that define specialized AI assistants with isolated context windows, specific tool access, and custom system prompts. This skill guides you through the process with structured workflows, validated templates, and quality gates.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO AGENT WITHOUT VALIDATED DESCRIPTION AND FOCUSED TOOL SET
```

The description field determines when the orchestrator delegates to the agent. The tool set determines what the agent can do - and what it can't. Both must be right before the agent ships.

**No exceptions:**
- Don't write the system prompt before the description
- Don't skip validation because "it's a simple agent"
- Don't give an agent all tools when it only needs three
- Don't copy another agent's description and swap keywords

## The Gate Function

```
BEFORE writing any agent .md file:

1. GATHER: What task does this agent handle? When should it be delegated to?
   Personal (~/.claude/agents/) or project (.claude/agents/)?
2. CHECK EXISTING: Are there similar agents? Read them to avoid overlap.
   Does `.docs/research/` have relevant analysis? Use findings as baseline.
3. DESIGN: Name (noun, kebab-case), description (delegation trigger),
   tools (minimal set), model (cost/capability tradeoff), scope
4. CHOOSE: Template from ./templates/ (basic, analysis, or action)
5. WRITE: Create agent file following the template
6. VALIDATE: Run checklist from ./reference/validation-rules.md
7. ONLY THEN: Declare the agent complete

Skip any step = agent that triggers wrong, has wrong tools, or overlaps with existing agents
```

## Complexity Check

Decide whether to proceed standalone or suggest research first.

**Simple - proceed directly:**
- Single-purpose agent with clear tool set
- Familiar domain with existing agent patterns to follow
- Adapting an existing agent for a new domain
- User knows exactly what they want

**Complex - suggest `/researching-code` or `/researching-web` first:**
- Novel system prompt architecture (no existing pattern to follow)
- Involves unfamiliar APIs, external services, or MCP tools
- Agent needs to coordinate with other agents (family design)
- User says "I'm not sure what tools it needs"

When suggesting research:
> This agent looks complex enough to benefit from upfront research. Consider running `/researching-code` to analyze similar agent patterns, or `/researching-web` for external best practices, then return here to build the agent with those findings as a baseline.

When existing research is found:
> Found relevant research at `.docs/research/[file]`. Using its findings to inform design decisions.

## Three Modes

### Mode 1: Create New Agent

Build an agent from scratch using the 5-step workflow.

**Step 1: Gather Requirements**

Ask and answer these questions before designing anything:

- What task does this agent handle? Be specific - not "helps with code" but "locates files and directories relevant to a feature or task."
- When should the orchestrator delegate to it? List 3-5 specific delegation scenarios.
- Personal (`~/.claude/agents/`) or project (`.claude/agents/`) scope?
- Are there similar existing agents? Read them first - check for agent families to join.
- What tools does it need? Start from deny-all and add only what's necessary.
- Does it need to modify state? This determines the template choice and tool set.

**Step 2: Choose Freedom Tier**

See the Freedom Tiers section below. Match the tier to the task's error tolerance.

**Step 3: Design the Agent**

- **Name**: Noun/role form, kebab-case (see ./reference/naming-conventions.md)
- **Description**: Delegation trigger formula (see ./reference/description-writing-guide.md)
  - Write the description FIRST, before the system prompt
  - Test it mentally: "If the orchestrator needed [task], would this description be selected?"
- **Tools**: Minimal set for the job (see ./reference/tool-selection-guide.md)
- **Model**: Choose based on task complexity (haiku for simple, sonnet for standard, opus for complex reasoning)
- **Frontmatter**: `name` and `description` are required. Add `tools`, `model`, and other fields as needed.

**Step 4: Write the Agent**

- Start with YAML frontmatter (name + description + tools + model at minimum)
- Write the system prompt using the Contract Format (see ./reference/system-prompt-patterns.md)
- Keep the file concise - target 80-200 lines total
- Include enforcement patterns: What NOT to Do sections, role reinforcement
- End with a meta-reminder of the agent's identity and boundaries

**Step 5: Validate**

Run every item in ./reference/validation-rules.md. Fix all issues before declaring done.

Present the completed agent:
```
Agent created: [name]
Location: [path]
Description: [first 80 chars...]
Tools: [list]
Model: [model]
Validation: All checks passed
```

### Mode 2: Edit Existing Agent

Improve an existing agent's description, system prompt, or tool set.

1. **Read first**: Read the agent file completely. Understand its purpose, tool set, and current delegation trigger before changing anything.
2. **Diagnose**: Identify specific improvement areas:
   - Description: Is it triggering correctly? Does it express when to delegate?
   - Tools: Too many? Too few? Missing a critical tool? Has unnecessary ones?
   - System prompt: Is it using the Contract Format? Are enforcement patterns present?
   - Model: Is the model appropriate for the task complexity?
3. **Preserve intent**: Apply changes while keeping the agent's core purpose intact. Don't restructure a working agent just for style points.
4. **Re-validate**: Run the full checklist from ./reference/validation-rules.md after changes.
5. **Show diffs**: For description changes, show before/after so the user can confirm delegation triggers are still correct.

### Mode 3: Convert Skill to Agent

Transform a Claude Code skill into an agent. The core shift: skills explain WHEN to use them, agents explain WHAT they are.

1. **Read the skill** directory completely. Read SKILL.md and any reference files. Identify its purpose, workflow, and domain knowledge.
2. **Transform the name** from gerund form to noun form (e.g., `reviewing-code` becomes `code-reviewer`).
3. **Rewrite the description** using the delegation trigger formula. Strip "Use this skill when..." language.
4. **Select tools**: Determine what tools the agent needs based on what the skill's workflow does (reads files? searches? edits? runs commands?).
5. **Choose model**: Match to task complexity. Default to `sonnet` unless the task requires `opus`-level reasoning.
6. **Collapse structure**: Merge SKILL.md body and key reference content into a single .md file system prompt.
7. **Add frontmatter** with all required and relevant optional fields.
8. **Validate** against ./reference/validation-rules.md.

See ./reference/converting-skills.md for the detailed conversion guide with examples and checklist.

## Freedom Tiers

Choose how prescriptive the agent's system prompt should be based on error tolerance.

| Tier | When to Use | System Prompt Approach |
|------|-------------|----------------------|
| **High** | Creative tasks, many valid outcomes | Role + success criteria + general principles |
| **Medium** | Standard tasks, recommended patterns | Contract Format with examples and guidelines |
| **Low** | Error-prone tasks, strict execution | Step-by-step procedures, explicit DON'Ts, verification gates |

**Decision criteria:**
- Is there one correct approach? -> Low freedom
- Does the task need to adapt to varied inputs? -> High freedom
- Are errors costly or hard to reverse? -> Low freedom (and consider `opus` model)
- Does the agent modify state (Edit, Bash, Write)? -> Lower freedom, more guardrails

## Sibling Skill: /creating-skills

`/creating-agents` and `/creating-skills` are siblings, not overlapping:

| Aspect | /creating-agents | /creating-skills |
|--------|-----------------|-----------------|
| Creates | Single `.md` agent files | `SKILL.md` + reference directory |
| Names | Noun form (`code-reviewer`) | Gerund form (`reviewing-code`) |
| Descriptions | Delegation triggers | Intent-matching triggers |
| Converts | Skills -> Agents (Mode 3) | Agents -> Skills (Mode 3) |

If the user wants to create a **skill** (directory with SKILL.md, intent-matching activation), redirect to `/creating-skills`.
If the user wants to convert an **agent to a skill**, redirect to `/creating-skills` Mode 3.

## Reference Files

These contain the detailed rules and guidance referenced throughout this workflow:

- See ./reference/validation-rules.md for frontmatter spec, field constraints, and the validation checklist
- See ./reference/description-writing-guide.md for the delegation trigger formula and examples
- See ./reference/naming-conventions.md for noun-form naming, kebab-case rules, and agent families
- See ./reference/system-prompt-patterns.md for Contract Format, enforcement patterns, and examples
- See ./reference/tool-selection-guide.md for tool allowlist/denylist decisions and common tool sets
- See ./reference/converting-skills.md for the skill-to-agent migration workflow

## Templates

Start from one of these when creating a new agent:

- See ./templates/basic-agent-template.md for simple, single-purpose agents (locators, finders)
- See ./templates/analysis-agent-template.md for read-and-report agents (analyzers, researchers)
- See ./templates/action-agent-template.md for agents that modify state (updaters, builders)

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- Writing the system prompt before finalizing the description
- Description says WHAT the agent does but not WHEN to delegate to it
- Name uses gerund form instead of noun form (e.g., `reviewing-code` instead of `code-reviewer`)
- Agent has all tools inherited (no explicit `tools` field) when it doesn't need them all
- Agent modifies state (Edit, Write, Bash) without explicit guardrails in the system prompt
- System prompt exceeds 300 lines without clear justification
- Copying another agent's system prompt and swapping domain keywords
- No "What NOT to Do" section in the system prompt for a constrained agent
- Skipping validation because the agent "looks right"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The description is good enough" | Test it: would the orchestrator select this agent for the right tasks and not the wrong ones? |
| "It needs all the tools" | Start from deny-all. Each tool in the set must be justified by a specific action in the workflow. |
| "This is a simple agent, no validation needed" | Simple agents still need valid frontmatter and clear delegation triggers. |
| "The name doesn't need to be noun form" | Noun form is the convention. Follow it unless there's a strong reason not to. |
| "I'll add the enforcement patterns later" | System prompts without guardrails produce unreliable agents. Build them in from the start. |
| "It doesn't need a What NOT to Do section" | The agents that work best all have explicit boundaries. Omitting them invites scope creep. |

## The Bottom Line

**No agent ships without a validated description and a justified tool set.**

Gather requirements. Check existing agents. Design with intention. Write from templates. Validate every field.

This is non-negotiable. Every agent. Every time.
