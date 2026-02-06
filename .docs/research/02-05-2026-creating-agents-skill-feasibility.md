# Feasibility Analysis: Creating a `/creating-agents` Skill Based on `/creating-skills`

**Date**: 02-05-2026
**Question**: Should a `/creating-agents` skill be created, modeled after `/creating-skills`? What would it contain, and how would the two skills relate?

## Executive Summary

A `/creating-agents` skill is both feasible and well-supported by existing materials. The `/creating-skills` skill provides a proven structural pattern (Iron Law → Gate Function → Modes → Red Flags → Rationalization Prevention) that can be adapted for agent creation. The key difference: skills are directory-based with SKILL.md frontmatter and trigger descriptions, while agents are single `.md` files with richer frontmatter (tools, model, permissionMode, memory, hooks, skills) and system prompts instead of instructional bodies.

**Recommendation**: Create the skill. Sufficient reference material already exists across research docs, naming conventions, and 7 working agent examples.

---

## 1. What Already Exists for Agent Creation

### Existing Materials (No Formal Skill)

There is **no `/creating-agents` skill** today. Agent creation guidance is distributed across:

| Resource | Location | What It Provides |
|----------|----------|-----------------|
| Agent Creation Best Practices | `.docs/research/02-05-2026-agent-creation-best-practices.md` | Official spec, design patterns, anti-patterns |
| Agent Naming Conventions | `newagents/NAMING-CONVENTIONS.md` | Noun-form naming rules, patterns, suffixes |
| Gerund vs Noun Research | `.docs/research/02-05-2026-gerund-naming-skills-vs-agents.md` | Why agents use nouns, skills use gerunds |
| Converting Subagents | `newskills/creating-skills/reference/converting-subagents.md` | Agent → Skill conversion (reverse direction) |
| 7 Working Agent Examples | `newagents/*.md` | Reference implementations |

### What `/creating-skills` Covers That Agents Also Need

| Topic | In `/creating-skills`? | Applicable to Agents? | Adaptation Needed? |
|-------|----------------------|----------------------|-------------------|
| Name conventions | Yes (gerund, kebab-case) | Yes (noun, kebab-case) | Switch gerund → noun |
| Description writing | Yes (WHEN formula) | Yes (delegation trigger) | Adjust formula for agents |
| Validation checklist | Yes (frontmatter, structure) | Yes (frontmatter, format) | Different field set |
| Freedom tiers | Yes | Yes | Same concept applies |
| Templates | Yes (basic, workflow) | Needed | New templates for agents |
| Progressive disclosure | Yes (SKILL.md → reference/) | Partial | Agents are single files |

### What Agents Need That Skills Don't

| Agent-Specific Topic | Why It Matters |
|---------------------|---------------|
| Tool selection (allowlist/denylist) | Security and focus - agents must have right tools |
| Model selection | Cost/capability tradeoff (haiku vs sonnet vs opus) |
| System prompt architecture | Contract Format, enforcement patterns |
| Permission modes | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| Memory scopes | `user`, `project`, `local` for persistent state |
| Scope decision (personal/project/plugin) | Different discovery priorities |
| Agent families | Grouping related agents by domain |

---

## 2. Structural Mapping: `/creating-skills` → `/creating-agents`

### The Enforcement Pattern (Reusable As-Is)

The 5-layer enforcement architecture from `/creating-skills` transfers directly:

| Layer | `/creating-skills` | `/creating-agents` Adaptation |
|-------|-------------------|-------------------------------|
| Iron Law | "No skill without validated description and structure" | "No agent without validated description and focused tool set" |
| Gate Function | 7-step: Gather → Check Research → Design → Choose Template → Write → Validate → Declare | Similar: Gather → Check Existing Agents → Design → Choose Scope → Write → Validate → Declare |
| Process/Modes | Create, Edit, Convert | Create, Edit, Convert (Skill → Agent) |
| Red Flags | Skill-specific warnings | Agent-specific warnings |
| Rationalization Prevention | Skill-specific excuses | Agent-specific excuses |

### The Three Modes (Adapted)

| Mode | `/creating-skills` | `/creating-agents` |
|------|-------------------|-------------------|
| Mode 1: Create | Build from scratch via 5-step workflow | Build from scratch: gather requirements → design frontmatter → write system prompt → validate |
| Mode 2: Edit | Improve description/structure/content | Improve description/system prompt/tool set |
| Mode 3: Convert | Sub-agent → Skill (noun → gerund) | Skill → Agent (gerund → noun), reverse of creating-skills Mode 3 |

### Reference Files Needed

| File | Purpose | Source Material |
|------|---------|----------------|
| `reference/validation-rules.md` | Frontmatter spec, field constraints, checklist | `.docs/research/02-05-2026-agent-creation-best-practices.md:33-45` |
| `reference/description-writing-guide.md` | Delegation trigger formula, examples | Adapt from skills version + agent-specific patterns |
| `reference/naming-conventions.md` | Already exists as `newagents/NAMING-CONVENTIONS.md` | Can symlink or incorporate |
| `reference/system-prompt-patterns.md` | Contract Format, enforcement patterns, examples | `.docs/research/02-05-2026-agent-creation-best-practices.md:79-101` |
| `reference/tool-selection-guide.md` | When to restrict tools, allowlist vs denylist | New content based on existing agent patterns |
| `reference/converting-skills.md` | Skill → Agent conversion (reverse of creating-skills) | Invert `converting-subagents.md` |

### Templates Needed

| Template | For | Based On |
|----------|-----|----------|
| `templates/basic-agent-template.md` | Simple single-purpose agents | Pattern from `codebase-locator.md`, `docs-locator.md` |
| `templates/analysis-agent-template.md` | Read-and-report agents | Pattern from `codebase-analyzer.md`, `docs-analyzer.md` |
| `templates/action-agent-template.md` | Agents that modify state | Pattern from `docs-updater.md` |

---

## 3. Key Differences Between Skill and Agent Creation

### Frontmatter Differences

| Field | Skills | Agents |
|-------|--------|--------|
| `name` | Required, gerund-form | Required, noun-form |
| `description` | Required, "Use this skill when..." | Required, delegation trigger |
| `license` | Optional | N/A |
| `allowed-tools` | Optional | N/A (use `tools` instead) |
| `tools` | N/A | Optional allowlist |
| `disallowedTools` | N/A | Optional denylist |
| `model` | N/A | Optional (`sonnet`, `opus`, `haiku`, `inherit`) |
| `permissionMode` | N/A | Optional |
| `skills` | N/A | Optional (preload skills into agent context) |
| `hooks` | N/A | Optional (lifecycle hooks) |
| `memory` | N/A | Optional (`user`, `project`, `local`) |
| `metadata` | Optional | N/A |

### Structure Differences

| Aspect | Skills | Agents |
|--------|--------|--------|
| File structure | Directory with `SKILL.md` + optional `reference/`, `templates/` | Single `.md` file |
| Body content | Instructions for Claude when skill triggers | System prompt for the agent |
| Loading | Metadata always in context; body on trigger | Loaded when invoked via Task tool |
| Size guidance | SKILL.md < 500 lines, < 5k words | No hard limit, but concise is better (150-200 instructions max) |
| Progressive disclosure | 3 levels (metadata → body → resources) | 1 level (entire file loaded on invocation) |

### Description Formula Differences

**Skills**: "Use this skill when [primary situation]. This includes [use cases]..."
- Optimized for intent matching against user requests
- Claude sees skill descriptions always and matches against user input

**Agents**: "[What it does]. [When to delegate to it]."
- Optimized for delegation decisions by the orchestrating Claude
- Claude decides to delegate specific subtasks to specialists
- Examples from existing agents:
  - `"Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components."`
  - `"Searches the web and fetches page content to find current, sourced information. Use when you need up-to-date information beyond training data..."`

### Naming Differences

| Aspect | Skills | Agents |
|--------|--------|--------|
| Form | Gerund (`reviewing-code`) | Noun (`code-reviewer`) |
| Mental model | "User is doing X" | "Delegate to the X-er" |
| Pattern | `{action}-{target}` | `{domain}-{role}` |
| Why | Implicit activation via intent match | Explicit delegation to specialist |

---

## 4. Design Decisions for the Skill

### Decision 1: Name

**`creating-agents`** — follows gerund convention for skills. The user is "creating agents", so this skill activates.

### Decision 2: Scope

**Personal** (`~/.claude/skills/creating-agents/`) — this is a general-purpose workflow tool, not project-specific.

### Decision 3: Freedom Tier

**Medium** — There are recommended patterns (Contract Format, noun naming, tool restriction) but agents vary enough that rigid step-by-step wouldn't work. The skill should provide parameterized guidance with defaults.

### Decision 4: Template Choice

**Workflow template** — The skill has multiple modes (Create, Edit, Convert) and decision points (scope, model, tool set). This matches the workflow template, not the basic template.

### Decision 5: Complexity

**Complex** — Needs `reference/` subdirectory. Agent creation involves frontmatter specification, system prompt architecture, tool selection, naming conventions, and conversion patterns. Too much for a single SKILL.md.

### Decision 6: Relationship to `/creating-skills`

**Sibling, not child.** Both skills share structural patterns but are independent. `/creating-agents` should NOT be a mode within `/creating-skills`. Reasons:
- Different frontmatter specifications
- Different naming conventions (noun vs gerund)
- Different file structure (single file vs directory)
- Different description formulas
- Different validation rules

However, `/creating-agents` Mode 3 (Convert Skill → Agent) is the inverse of `/creating-skills` Mode 3 (Convert Agent → Skill). They can cross-reference each other.

---

## 5. What the Skill Would Look Like

### File Structure

```
creating-agents/
├── SKILL.md                              # Core workflow (~250-350 lines)
├── reference/
│   ├── validation-rules.md               # Frontmatter spec, field constraints, checklist
│   ├── description-writing-guide.md      # Delegation trigger formula, examples
│   ├── naming-conventions.md             # Noun-form rules (based on newagents/NAMING-CONVENTIONS.md)
│   ├── system-prompt-patterns.md         # Contract Format, enforcement patterns
│   ├── tool-selection-guide.md           # Allowlist/denylist decision framework
│   └── converting-skills.md             # Skill → Agent conversion guide
└── templates/
    ├── basic-agent-template.md           # Simple single-purpose agents
    ├── analysis-agent-template.md        # Read-and-report agents
    └── action-agent-template.md          # Agents that modify state
```

### SKILL.md Outline

```
---
name: creating-agents
description: "Use this skill when creating new Claude Code agents (subagents),
  editing existing agents to improve their descriptions or system prompts,
  or converting skills into agents. This includes writing agent .md files,
  choosing agent names, crafting delegation-trigger descriptions, designing
  system prompts using the Contract Format, selecting tool sets, and
  validating agent structure against the specification."
---

# Creating Agents
[Introduction]

## The Iron Law
NO AGENT WITHOUT VALIDATED DESCRIPTION AND FOCUSED TOOL SET

## The Gate Function
BEFORE writing any agent .md file:
1. GATHER requirements
2. CHECK existing agents (avoid overlap)
3. DESIGN (name, description, tools, model, scope)
4. CHOOSE template
5. WRITE agent file
6. VALIDATE
7. ONLY THEN: Declare complete

## Complexity Check
[Simple vs Complex agent decision]

## Three Modes
### Mode 1: Create New Agent
### Mode 2: Edit Existing Agent
### Mode 3: Convert Skill to Agent

## Freedom Tiers
[Same concept as creating-skills]

## Reference Files
[Skinny pointers]

## Templates
[Skinny pointers]

## Red Flags
[Agent-specific warnings]

## Rationalization Prevention
[Agent-specific excuses mapped to truths]

## The Bottom Line
```

---

## 6. Risk Assessment

### Low Risk
- Structural pattern is proven (creating-skills has been working)
- Reference material already exists (research docs, naming conventions, 7 examples)
- Clear domain boundaries (agents ≠ skills, no overlap in guidance)

### Medium Risk
- Agent specification may evolve (new frontmatter fields added by Anthropic)
  - **Mitigation**: validation-rules.md can be updated independently
- Description formula for agents is less standardized than for skills
  - **Mitigation**: Extract patterns from existing 7 agents to establish convention

### No Risk
- Naming convention already formally documented (`NAMING-CONVENTIONS.md`)
- System prompt patterns well-documented in research
- Template patterns derivable from 7 existing agents

---

## 7. Source References

### Internal Files (file:line references)
- `newskills/creating-skills/SKILL.md:1-213` — Full creating-skills skill
- `newskills/creating-skills/reference/validation-rules.md:1-98` — Skill validation rules
- `newskills/creating-skills/reference/description-writing-guide.md:1-174` — Description formula
- `newskills/creating-skills/reference/naming-conventions.md:1-93` — Skill naming (gerund)
- `newskills/creating-skills/reference/converting-subagents.md:1-158` — Agent → Skill conversion
- `newskills/creating-skills/templates/basic-skill-template.md:1-84` — Basic skill template
- `newskills/creating-skills/templates/workflow-skill-template.md:1-177` — Workflow skill template
- `newagents/NAMING-CONVENTIONS.md:1-182` — Agent naming (noun-form)
- `newagents/web-search-researcher.md:1-83` — Example: Contract Format agent
- `newagents/codebase-analyzer.md:1-144` — Example: Analysis agent with enforcement
- `newagents/codebase-locator.md:1-123` — Example: Minimal locator agent
- `newagents/codebase-pattern-finder.md:1-179` — Example: Pattern finding agent
- `newagents/docs-analyzer.md:1-160` — Example: Document analysis agent
- `newagents/docs-locator.md:1-116` — Example: Document finding agent
- `newagents/docs-updater.md:1-180` — Example: State-modifying agent (opus model)
- `.docs/research/02-05-2026-agent-creation-best-practices.md:1-335` — Web research on agent best practices
- `.docs/research/02-05-2026-gerund-naming-skills-vs-agents.md:1-94` — Naming convention rationale

### External Sources
- [Claude Code: Create custom subagents](https://code.claude.com/docs/en/sub-agents) — Official spec
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic: Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) — 100+ agent examples
