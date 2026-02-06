# Converting Skills to Agents

Skills and agents serve different purposes in Claude Code. This guide covers how to migrate a skill's functionality into the agent format.

## The Key Insight

Skills explain **WHEN to use them**. Agents explain **WHAT they are**.

A skill says: "Use this skill when reviewing code for quality issues, analyzing pull requests, or checking for common bugs."
An agent says: "Reviews code for quality issues, security vulnerabilities, and style violations. Call when code needs thorough review."

The shift is from activation (gerund) to identity (noun). This changes the name, the description, and how the capability is discovered.

## What Changes

| Aspect | Skill | Agent |
|--------|-------|-------|
| **Name** | Gerund form (`reviewing-code`) | Noun form (`code-reviewer`) |
| **Description** | "Use this skill when..." (intent matching) | Capability + trigger (delegation) |
| **Activation** | Implicit: description match against user intent | Explicit: Task tool invocation |
| **Structure** | Directory with `SKILL.md` + reference files | Single `.md` file |
| **Configuration** | `name`, `description`, optional `license` | `name`, `description`, `tools`, `model`, etc. |
| **Loading** | Metadata always in context, body on trigger | Loaded on demand via Task tool |

## Conversion Steps

### Step 1: Transform the Name

Convert from gerund form to noun form:

| Skill Name | Agent Name |
|------------|-----------|
| `reviewing-code` | `code-reviewer` |
| `running-tests` | `test-runner` |
| `generating-docs` | `doc-generator` |
| `analyzing-codebases` | `codebase-analyzer` |
| `managing-deployments` | `deploy-manager` |

The pattern: take the action the skill performs and express it as a noun/role.

### Step 2: Rewrite the Description

Apply the delegation trigger formula. Focus on WHAT + WHEN TO DELEGATE.

**Before (skill style):**
```
"Use this skill when reviewing pull requests for quality issues,
checking code for security vulnerabilities, or enforcing coding standards.
This includes analyzing diffs for common bugs, identifying style violations,
rating issue severity, and suggesting specific fixes."
```

**After (agent style):**
```
Reviews pull requests for quality issues, security vulnerabilities, and
style violations. Call when code needs a thorough review before merging
or when checking specific files for common bugs and coding standard compliance.
```

Key changes:
- Removed "Use this skill when" opener
- Changed from situational ("when reviewing") to declarative ("Reviews")
- Added delegation trigger: "Call when..."
- Kept specific capability mentions but reframed as agent capabilities

### Step 3: Determine the Tool Set

Map the skill's workflow to specific tools:

| Skill Action | Required Tool |
|-------------|--------------|
| Reads files to analyze content | `Read` |
| Searches for patterns in code | `Grep` |
| Finds files by name/pattern | `Glob` |
| Lists directory contents | `LS` |
| Modifies file content | `Edit` |
| Runs shell commands | `Bash` |
| Creates new files | `Write` |
| Fetches web content | `WebFetch` |
| Searches the web | `WebSearch` |

Start with the minimum set. If the skill workflow doesn't require a tool, don't include it.

### Step 4: Choose the Model

| Skill Complexity | Recommended Model |
|-----------------|-------------------|
| Simple lookup or categorization | `haiku` |
| Standard analysis, research, review | `sonnet` |
| Complex reasoning, state modification, judgment calls | `opus` |

### Step 5: Collapse the Structure

Skills use progressive disclosure (SKILL.md -> reference/ -> templates/). Agents are single files. You must merge relevant content.

**What to include in the agent file:**
- Core workflow from SKILL.md body
- Critical rules from reference files
- Essential examples (1-2, not exhaustive)

**What to leave out:**
- Meta-instructions about the skill format itself
- Extensive example galleries (pick the best 1-2)
- Content that Claude already knows (general knowledge)
- Validation checklists (those are for skill creation, not agent runtime)

### Step 6: Write the System Prompt

Transform skill instructions into a Contract Format system prompt:

```markdown
---
name: code-reviewer
description: Reviews code for quality issues, security vulnerabilities,
  and style violations. Call when code needs thorough review before merging.
tools: Read, Grep, Glob, LS
model: sonnet
---

You are a code review specialist. Your job is to analyze code for quality
issues and provide specific, actionable feedback.

## Core Responsibilities

1. **Identify bugs**: Find logic errors, edge cases, and potential crashes
2. **Check security**: Spot injection vulnerabilities, auth issues, data exposure
3. **Evaluate style**: Flag violations of project coding standards

[... rest of Contract Format ...]
```

### Step 7: Validate

Run the agent validation checklist from ./validation-rules.md. Pay special attention to:
- Name format (noun, kebab-case, matches filename)
- Description uses delegation trigger (not "Use this skill when...")
- Tool set is minimal and justified
- No leftover skill-specific metadata or language
- System prompt follows Contract Format

## What to Preserve

These elements transfer directly from skill to agent:
- **Domain knowledge** - The expertise the skill was built with
- **Process logic** - Core workflow steps
- **Quality criteria** - Standards and thresholds
- **Enforcement patterns** - What NOT to Do rules (these transfer especially well)

## What to Remove

These elements don't belong in agents:
- "Use this skill when..." language
- Progressive disclosure structure (reference/, templates/)
- Gerund-form naming
- Skill-specific metadata (`license`, `allowed-tools` in skill format)
- Iron Law / Gate Function / Rationalization Prevention framework (skill-creation meta-patterns)
- Freedom tier discussions (decide the tier, apply it, don't document it in the agent)

## Conversion Checklist

Run through this list after converting a skill to an agent:

- [ ] Name is noun/role form, kebab-case
- [ ] Name matches filename (minus `.md`)
- [ ] Description uses delegation trigger formula (not skill formula)
- [ ] Description includes when to delegate (not when to invoke)
- [ ] Tools are explicitly listed (allowlist, not inherit-all)
- [ ] Model is appropriate for task complexity
- [ ] Skill-specific language removed ("Use this skill when...")
- [ ] Content is in a single `.md` file with proper frontmatter
- [ ] System prompt uses Contract Format
- [ ] "What NOT to Do" section present for constrained agents
- [ ] No leftover skill metadata (`license`, `allowed-tools`)
- [ ] Agent file is under 300 lines
