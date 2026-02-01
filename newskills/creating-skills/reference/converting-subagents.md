# Converting Sub-Agents to Skills

Sub-agents and skills serve different purposes in Claude Code. This guide covers how to migrate a sub-agent's functionality into the skill format.

## The Key Insight

Sub-agents explain **WHAT they are**. Skills explain **WHEN to use them**.

A sub-agent says: "I am a code reviewer that analyzes pull requests for quality issues."
A skill says: "Use this skill when reviewing code for quality issues, analyzing pull requests, or checking for common bugs."

The shift is from identity (noun) to activation (gerund). This changes the name, the description, and how Claude discovers the capability.

## What Changes

| Aspect | Sub-Agent | Skill |
|--------|-----------|-------|
| **Name** | Noun form (`code-reviewer`) | Gerund form (`reviewing-code`) |
| **Description** | What it does ("Analyzes code...") | When to invoke ("Use this skill when...") |
| **Activation** | Explicit: `@mention` or Task tool | Implicit: description match against user intent |
| **Structure** | Single `.md` file | Directory with `SKILL.md` at root |
| **Configuration** | `model`, `color`, tool restrictions | `name`, `description`, optional `license` |
| **Loading** | On demand via agent system | Metadata always in context, body on trigger |

## Conversion Steps

### Step 1: Transform the Name

Convert from noun form to gerund form:

| Sub-Agent Name | Skill Name |
|---------------|------------|
| `code-reviewer` | `reviewing-code` |
| `test-runner` | `running-tests` |
| `doc-generator` | `generating-docs` |
| `bug-triager` | `triaging-bugs` |
| `deploy-manager` | `managing-deployments` |

The pattern: take the action the agent performs and express it as a present participle.

### Step 2: Rewrite the Description

Apply the description formula. Focus on WHEN, not WHAT.

**Before (sub-agent style):**
```
Analyzes pull requests for code quality issues, security vulnerabilities,
and style violations. Reports findings with severity levels.
```

**After (skill style):**
```
"Use this skill when reviewing pull requests for quality issues,
checking code for security vulnerabilities, or enforcing coding standards.
This includes analyzing diffs for common bugs, identifying style violations,
rating issue severity, and suggesting specific fixes."
```

Key changes:
- Added "Use this skill when" opener
- Changed from declarative ("Analyzes") to situational ("when reviewing")
- Added trigger keywords: "pull requests", "security vulnerabilities", "coding standards"
- Included specific operations as additional triggers

### Step 3: Create the Directory Structure

```
# Sub-agent (single file)
~/.claude/agents/code-reviewer.md

# Skill (directory)
~/.claude/skills/reviewing-code/
├── SKILL.md
└── reference/          # Only if content exceeds 300 lines
    └── review-checklist.md
```

### Step 4: Move and Transform Content

Transfer the sub-agent's instructions into SKILL.md body:
- System prompt content becomes the skill's process instructions
- Agent-specific examples become skill examples
- Domain knowledge transfers directly
- Tool-specific instructions may need updating

### Step 5: Extract Reference Material

If the combined content exceeds 300 lines:
- Move checklists, detailed rules, and reference tables to `reference/` files
- Keep the core workflow in SKILL.md
- Add skinny pointers: `See ./reference/filename.md for [topic]`

### Step 6: Add Frontmatter

Replace agent configuration with skill frontmatter:

```yaml
---
name: reviewing-code
description: "Use this skill when reviewing pull requests for quality issues,
  checking code for security vulnerabilities, or enforcing coding standards.
  This includes analyzing diffs for common bugs, identifying style violations,
  rating issue severity, and suggesting specific fixes."
---
```

### Step 7: Validate

Run the validation checklist from ./validation-rules.md. Pay special attention to:
- Name format (gerund, kebab-case, matches directory)
- Description formula (starts with "Use this skill when...")
- No leftover agent-specific metadata

## What to Preserve

These elements transfer directly from sub-agent to skill:

- **Domain knowledge** - The expertise the agent was built with
- **Process instructions** - Step-by-step workflows
- **Examples** - Concrete demonstrations of the capability
- **Quality criteria** - Standards and thresholds
- **Error handling** - What to do when things go wrong

## What to Transform

These elements need conversion:

- **Name** - Noun to gerund form
- **Description** - WHAT to WHEN
- **Activation model** - Explicit mention to implicit trigger
- **Structure** - Single file to directory with SKILL.md
- **Voice** - "I am..." / "This agent..." to "Use this skill when..."

## What to Remove

These elements don't belong in skills:

- `model` specification (e.g., `model: opus`) - skills don't control model selection
- `color` specification - skills don't have visual identity
- Tool restrictions (`allowed-tools` in agent format) - only add if genuinely needed
- Agent-specific routing metadata
- System prompt wrapper text ("You are an agent that...")

## Conversion Checklist

Run through this list after converting a sub-agent to a skill:

- [ ] Name is gerund form, kebab-case
- [ ] Name matches directory name
- [ ] Description uses "Use this skill when..." formula
- [ ] Description includes trigger keywords (not just capabilities)
- [ ] No agent-specific metadata remains (model, color)
- [ ] System prompt language removed ("You are...", "Your role is...")
- [ ] Content is in SKILL.md with proper frontmatter
- [ ] SKILL.md is under 500 lines (split to reference/ if needed)
- [ ] All reference files have intention-revealing names
- [ ] Validation checklist from ./validation-rules.md passes completely
