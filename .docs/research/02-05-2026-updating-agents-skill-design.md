# Research: /updating-agents Skill Design

**Date:** 02-05-2026
**Question:** What should an `/updating-agents` skill look like, modeled after `/updating-skills`?

## Summary

An `/updating-agents` skill would audit and fix deployed agent `.md` files against the agent specification, paralleling how `/updating-skills` audits skill directories. The key differences are: agents are single files (not directories), use noun-form naming (not gerund), have tool/model/permission fields to validate, require Contract Format system prompts, and use delegation-trigger descriptions instead of "Use this skill when..." descriptions.

## Existing `/updating-skills` Structure

The current skill (`~/.claude/skills/updating-skills/SKILL.md`) provides:
- **Two modes**: Audit (read-only analysis) and Update (interactive fix with diffs)
- **Five audit categories**: Frontmatter, Name, Description, Structure, Pattern Compliance
- **One-at-a-time fixes**: Each change shown as before/after diff, requires user approval
- **Reference files**: `audit-checklist.md` (detailed checks per category), `common-fixes.md` (fix patterns with before/after examples)

## Agent vs Skill Validation Differences

### Shared Checks (Both Skills and Agents)
| Check | Detail |
|-------|--------|
| Frontmatter delimiters | `---` open and close |
| Valid YAML dictionary | Parses without errors |
| Required: name, description | Both fields present |
| Name format | `^[a-z0-9-]+$`, no leading/trailing/consecutive hyphens, max 64 chars |
| Description constraints | Non-empty string, max 1024 chars, no angle brackets, not first person |

### Agent-Specific Checks (New for /updating-agents)
| Check | Detail |
|-------|--------|
| **Name convention** | Noun/role form (not gerund). Flag `-ing` suffix as skill pattern. |
| **Name matches filename** | `name` field === filename minus `.md` (not directory name) |
| **Allowed frontmatter properties** | `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `hooks`, `memory` |
| **Tool set validation** | `tools` XOR `disallowedTools` (not both). Valid tool names. Minimal set. |
| **State-modifying tool guardrails** | If Edit/Write/Bash/NotebookEdit present, system prompt must have guardrails |
| **Model validation** | Valid values: `sonnet`, `opus`, `haiku`, `inherit`. Matches task complexity. |
| **Permission mode validation** | Valid values: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| **Single-file structure** | Agent is one `.md` file, no supporting files |
| **Line budget** | Under 300 lines (target 80-200) |
| **Description: delegation trigger** | Must express WHEN to delegate, not start with "Use this skill when..." |
| **System prompt: Contract Format** | Role statement, Core Responsibilities, Strategy/Process, Output Format, Guidelines, What NOT to Do, Meta-Reminder |
| **System prompt: identity framing** | Uses "You are...", not "I am..." |

### Checks That DON'T Apply to Agents
| Skill Check | Why Not Applicable |
|-------------|-------------------|
| Directory structure (SKILL.md, reference/, templates/) | Agents are single files |
| Gerund naming convention | Agents use noun/role form |
| "Use this skill when..." description opener | Agents use delegation trigger formula |
| Pattern compliance (Iron Law, Gate Function, etc.) | Agents use Contract Format instead |
| 500-line body limit | Agents have 300-line limit |

## Proposed Audit Categories for /updating-agents

Six categories (vs five for skills):

### 1. Frontmatter Validation
- Opens/closes with `---`
- Valid YAML dictionary
- Only allowed properties (name, description, tools, disallowedTools, model, permissionMode, skills, hooks, memory)
- Required: name, description

### 2. Name Validation
- Matches `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Matches filename minus `.md`
- Uses noun/role form (not gerund)
- No vague suffixes (-helper, -handler, -manager)

### 3. Description Validation
- Non-empty string, max 1024 chars
- No angle brackets
- Not first person
- Contains delegation trigger
- Does NOT start with "Use this skill when..."
- Distinguishable from sibling agents

### 4. Tool Set Validation
- `tools` and `disallowedTools` not both present
- All listed tools are valid tool names
- Tool set appropriate for agent role
- State-modifying tools have guardrails in system prompt
- No unnecessary tools (WebSearch without web need, Bash used only for grep)

### 5. Model & Permission Validation
- Model is valid value or absent (inherits)
- Model matches task complexity
- Permission mode is valid value or absent
- `bypassPermissions` flagged for review

### 6. System Prompt Compliance
- Uses "You are..." role statement (not first person)
- Has Core Responsibilities section (3-5 items)
- Has Strategy/Process section
- Has Output Format with example/template
- Has What NOT to Do section (especially for read-only agents)
- Has meta-reminder closing
- Under 300 lines total
- No placeholder text or TODOs

## Deployed Agent Inventory (Current State)

| Agent | Lines | Model | Tools | Has "What NOT to Do" |
|-------|-------|-------|-------|---------------------|
| docs-analyzer | 160 | sonnet | Read, Grep, Glob, LS | Yes |
| docs-locator | 116 | sonnet | Grep, Glob, LS | Yes |
| codebase-analyzer | 144 | sonnet | Read, Grep, Glob, LS | Yes |
| codebase-locator | 123 | sonnet | Grep, Glob, LS | Yes |
| codebase-pattern-finder | 179 | sonnet | Grep, Glob, Read, LS | Yes |
| web-search-researcher | 83 | sonnet | WebSearch, WebFetch | No |
| docs-updater | 180 | opus | Read, Grep, Glob, LS, Edit, Bash | Yes |

**Notable patterns:**
- All 7 agents have explicit `tools` fields (good practice)
- All use `name`, `description`, `tools`, `model` in frontmatter
- 6 of 7 have "What NOT to Do" enforcement sections
- `web-search-researcher` lacks enforcement section (potential audit finding)
- `docs-updater` is the only state-modifier with `opus` model (appropriate)
- 3 codebase agents use consistent "REMEMBER:" meta-reminder pattern

## Structural Parallels with /updating-skills

| Aspect | /updating-skills | /updating-agents (proposed) |
|--------|-----------------|----------------------------|
| Target | `~/.claude/skills/*/SKILL.md` | `~/.claude/agents/*.md` |
| Modes | Audit + Update | Audit + Update |
| Audit categories | 5 | 6 |
| Batch update | Prohibited | Prohibited |
| Diff approval | Required per change | Required per change |
| Reference files | audit-checklist.md, common-fixes.md | audit-checklist.md, common-fixes.md |
| "Audit all" | Lists all skill dirs | Lists all agent files |

## Key Design Decisions

1. **Six categories vs five**: Agents need tool set validation and model/permission validation as separate categories that skills don't have.
2. **Contract Format replaces Pattern Compliance**: Skills check for Iron Law/Gate Function/etc. Agents check for Contract Format sections.
3. **Single-file simplifies structure checks**: No directory structure to validate, but must verify no companion files exist.
4. **Tool-to-prompt alignment**: Unique to agents - verifying that the tools listed match what the system prompt describes.
5. **Sibling agent differentiation**: Check that descriptions don't overlap with other agents in the same family.
