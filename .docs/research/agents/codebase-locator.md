---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, corrected agent file path from ~/.claude/agents/ to plugins/commandbase-code/agents/, updated output format and integration points to match actual agent, added key behavioral notes"
references:
  - plugins/commandbase-code/agents/code-locator.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/researching-code/reference/research-agents.md
  - plugins/commandbase-code/skills/structuring-code/SKILL.md
  - plugins/commandbase-code/skills/starting-refactors/SKILL.md
---

# Research: code-locator Agent

## Overview

The `code-locator` agent (`plugins/commandbase-code/agents/code-locator.md`) locates files, directories, and components relevant to a feature or task. It's a "Super Grep/Glob/LS tool" -- use it when you find yourself wanting to use Grep, Glob, or LS more than once.

**When to Use**: When searching for a keyword or file and not confident you'll find the right match in the first few tries.

**Model**: sonnet

## Capabilities

- Search code with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Grep, Glob, LS

## Key Behavioral Notes

The agent operates as a **documentarian, not a critic or consultant**. It has strict constraints:

- Does NOT read file contents -- only reports locations
- Does NOT analyze what code does or suggest improvements
- Does NOT critique file organization or naming conventions
- Does NOT propose enhancements or identify "problems"
- ONLY describes what exists, where it exists, and how components are organized

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "code-locator"
prompt: "Find all files related to [feature/component]"
```

## Use Cases

1. **File Discovery**: Find files matching a pattern
2. **Component Location**: Locate where a component is defined
3. **Feature Mapping**: Find all files related to a feature
4. **Structure Understanding**: Map directory structure

## Search Strategy

The agent follows a structured search approach:

1. **Initial broad search** with Grep for keywords
2. **Glob** for file patterns
3. **Refine by language/framework** -- checks language-specific directories (src/, lib/, components/, pkg/, internal/, cmd/)
4. **Common patterns**: `*service*`, `*handler*`, `*controller*`, `*test*`, `*spec*`, `*.config.*`, `*.d.ts`, `*.types.*`

## Output Format

Returns categorized file locations:
```markdown
## File Locations for [Feature/Topic]

### Implementation Files
- `src/services/feature.js` - Main service logic
- `src/handlers/feature-handler.js` - Request handling

### Test Files
- `src/services/__tests__/feature.test.js` - Service tests
- `e2e/feature.spec.js` - End-to-end tests

### Configuration
- `config/feature.json` - Feature-specific config

### Type Definitions
- `types/feature.d.ts` - TypeScript definitions

### Related Directories
- `src/services/feature/` - Contains 5 related files

### Entry Points
- `src/index.js` - Imports feature module at line 23
- `api/routes.js` - Registers feature routes
```

## Integration Points

- Spawned by `/planning-code` as part of initial research (minimum 2 agents: code-locator + code-analyzer)
- Used by `/researching-code` for exploration via research-agents reference
- Used by `/structuring-code` to map current directory structure
- Used by `/starting-refactors` to find all files in the target area

## File Reference

- Agent: `plugins/commandbase-code/agents/code-locator.md`
- Plugin: `commandbase-code`
