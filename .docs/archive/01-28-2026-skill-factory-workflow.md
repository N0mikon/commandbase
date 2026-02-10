---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived - external research fully consumed during commandbase skill/plugin development; 56 commits behind HEAD with no local code references"
topic: "Claude Code Skill Factory - Skill Creator Workflow Deep Dive"
tags: [research, skill-factory, skill-creation, agents, factories, workflows]
status: archived
archived: 2026-02-09
archive_reason: "Completed external research with no local file references. Findings were consumed during commandbase plugin architecture and skill development. Document is 56 commits behind HEAD with status 'complete' — no further updates needed."
references:
  - https://github.com/alirezarezvani/claude-code-skill-factory
  - https://deepwiki.com/alirezarezvani/claude-code-skill-factory
  - https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935
---

# Research: Claude Code Skill Factory - Skill Creator Workflow

**Date**: 2026-01-28
**Branch**: master
**Source Repository**: https://github.com/alirezarezvani/claude-code-skill-factory (v1.4.0)
**Author**: alirezarezvani (Alireza Rezvani)
**Stars**: 962+ | **Forks**: 143+

## Research Question

Deep-dive research on the claude-code-skill-factory repository, specifically targeting the skill creator workflow: how it generates skills, agents, commands, and hooks through its two-tier architecture of guide agents and factory templates.

## Summary

The skill factory uses a **two-tier delegation architecture**: 5 interactive **guide agents** (lightweight Q&A interviewers) gather requirements and delegate to 6 **core factory templates** (921-1,500 line generation engines) that produce validated, production-ready components. The entire pipeline follows a Build > Validate > Install > Test workflow with multi-layer quality gates at each stage.

---

## Architecture Overview

### Two-Tier System

| Tier | Location | Purpose | Size |
|------|----------|---------|------|
| **Guide Agents** | `.claude/agents/` | Interactive requirement gathering via Q&A | Lightweight scripts |
| **Factory Templates** | `documentation/templates/` | Template-driven code/config generation | 921-1,500 lines each |

### Activation Methods

Three pathways into the system:

1. **Natural Language**: "I want to build something" > `factory-guide` orchestrator > menu > specialist
2. **Slash Commands**: `/build skill`, `/build agent`, `/build prompt`, `/build hook` > direct to specialist
3. **Direct Mention**: `@skills-guide` > bypass orchestrator entirely

### Repository Structure

```
claude-code-skill-factory/
├── CLAUDE.md                     # v2.0 Modular Architecture (155 lines, 77% reduction from 665)
├── .claude/
│   ├── agents/                   # 5 Guide Agents
│   │   ├── factory-guide.md      # Master orchestrator (haiku, purple)
│   │   ├── skills-guide.md       # Skill builder (sonnet, blue)
│   │   ├── prompts-guide.md      # Prompt generator (haiku, orange)
│   │   ├── agents-guide.md       # Agent creator (sonnet, green)
│   │   └── hooks-guide.md        # Hooks builder (sonnet, green)
│   └── commands/                 # 9 Slash Commands
│       ├── build.md              # Master builder gateway
│       ├── build-hook.md         # Dedicated hook creation
│       ├── validate-output.md    # Validation + auto-ZIP
│       ├── install-skill.md      # Automated skill installation
│       ├── install-hook.md       # Automated hook installation
│       ├── test-factory.md       # System testing
│       ├── factory-status.md     # System diagnostics
│       ├── sync-agents-md.md     # Codex CLI doc sync
│       └── codex-exec.md         # Codex CLI execution
├── documentation/
│   ├── templates/                # 5 Factory Templates
│   │   ├── SKILLS_FACTORY_PROMPT.md        (921 lines)
│   │   ├── AGENTS_FACTORY_PROMPT.md        (1,123 lines)
│   │   ├── PROMPTS_FACTORY_PROMPT.md       (403KB, 69 presets)
│   │   ├── MASTER_SLASH_COMMANDS_PROMPT.md  (1,500 lines)
│   │   └── HOOKS_FACTORY_PROMPT.md
│   └── references/               # Official Anthropic docs
│       ├── claude-skills-instructions.md
│       ├── claude-agents-instructions.md
│       └── claude-hooks-instructions.md
├── generated-skills/             # 9 Production-Ready Skills
├── generated-agents/             # Generated agent files
├── generated-commands/           # Generated command files
├── generated-hooks/              # Generated hook files
└── claude-skills-examples/       # 3 Reference implementations
```

---

## The Five Guide Agents

### 1. factory-guide.md (Master Orchestrator)

```yaml
name: factory-guide
description: Main navigation guide for Claude Code Skills Factory
tools: Read, Grep
model: haiku
color: purple
field: orchestration
expertise: beginner
```

**Role**: Triage and delegate. Does NOT generate anything itself.

**Workflow**:
1. Greet user, explain four build options (Skill, Prompt, Agent, Hook)
2. Detect intent via keyword matching (max 1-2 questions)
3. Delegate immediately to specialist with full context
4. Provide final summary after specialist completes

**Key Design**: Minimal model (haiku), minimal tools (Read, Grep), minimal questions. Pure routing.

---

### 2. skills-guide.md (Skill Builder)

```yaml
name: skills-guide
description: Interactive guide for building custom Claude Skills
tools: Read, Write, Bash, Grep, Glob
model: sonnet
color: blue
field: skills
expertise: expert
```

**Five-Question Workflow**:
1. What business domain? (FinTech, Healthcare, E-commerce, etc.)
2. What specific use cases? (2-4 targeted tasks)
3. Python code vs. prompt-only approach?
4. How many skills to generate? (1-5)
5. Special requirements? (compliance, tech stack, integrations)

**Generation Pipeline (7 Steps)**:
1. Read `SKILLS_FACTORY_PROMPT.md` template
2. Substitute variables into template
3. Multi-stage validation (YAML, naming, completeness)
4. Create files in structured directories
5. ZIP package for distribution
6. Installation guidance (project/user/system level)
7. Testing and next-steps recommendations

**Output Structure**:
```
generated-skills/[skill-name]/
├── SKILL.md              # Core prompt with YAML frontmatter
├── implementation.py     # Python code (if functional)
├── sample_input.json     # Example data
├── expected_output.json  # Expected results
├── HOW_TO_USE.md         # Installation and usage guide
└── [skill-name].zip      # Distributable package
```

---

### 3. agents-guide.md (Agent Creator)

```yaml
name: agents-guide
description: Interactive guide for building custom Claude Code Agents and subagents
tools: Read, Write, Grep
model: sonnet
color: green
field: agents
expertise: expert
```

**Six-Question Workflow**:
1. Agent purpose/use case
2. Agent type classification (Strategic/Implementation/Quality/Coordination)
3. Tool selection (based on type)
4. Model preference (sonnet/opus/haiku/inherit)
5. Field/domain specification
6. Expertise level

**Agent Type Classifications**:

| Type | Color | Tools | Concurrency | Examples |
|------|-------|-------|-------------|---------|
| **Strategic** | blue | Read, Write, Grep | Parallel (4-5) | planner, researcher |
| **Implementation** | green | Read, Write, Edit, Bash, Grep, Glob | Coordinated (2-3) | frontend-dev, backend-dev |
| **Quality** | red | Full tools | Sequential only | test-runner, code-reviewer |
| **Coordination** | purple | Read, Write, Grep | Lightweight | workflow-manager |
| **Domain-Specific** | orange | Varies | Varies | data-analyst, ai-specialist |

**Output**: Single `.md` file with enhanced YAML frontmatter:
```yaml
---
name: agent-name
description: Clear purpose statement (WHEN to invoke)
model: claude-sonnet-4-5
allowed-tools: [specific tools]
trigger: auto-invocation phrase
color: green
field: domain
expertise: expert
---
```

---

### 4. prompts-guide.md (Prompt Generator)

```yaml
name: prompts-guide
description: Interactive guide for using prompt-factory skill to generate mega-prompts
tools: Read, Grep
model: haiku
color: orange
field: prompts
expertise: intermediate
```

**Two Modes**:
- **Quick-Start** (2 questions): Select from 69 presets > choose format > done
- **Custom** (7 questions): Domain > role > expertise > format > style > constraints > success criteria

**69 Presets Across 15 Domains**:
Technical (8), Business (8), Legal (4), Finance (4), HR (4), Design (4), Customer-Facing (4), Executive (7), plus others

**Four Output Formats**: XML, Claude, ChatGPT, Gemini

**Key Rule**: "Don't Generate Prompts Yourself: Use the prompt-factory skill" -- delegates to dedicated skill rather than generating inline.

---

### 5. hooks-guide.md (Hooks Builder)

```yaml
name: hooks-guide
description: Interactive guide for building custom Claude Code hooks
tools: Read, Write, Bash, Grep, Glob
model: sonnet
color: green
field: hooks
expertise: expert
```

**Seven Hook Event Types**:
1. `SessionStart` - When Claude Code starts/resumes
2. `PostToolUse` - After tool execution (formatting, git staging)
3. `PreToolUse` - Before tool execution (can cancel)
4. `PrePush` - Before git push (validation)
5. `SubagentStart` - When subagent launches
6. `SubagentStop` - When subagent completes
7. `FileWrite` - Before file modifications

**5-7 Question Workflow**:
1. Hook purpose
2. Event type selection
3. Trigger conditions
4. Required tools
5. Actions to perform
6. Failure behavior
7. Special requirements (optional)

**5 Mandatory Safety Patterns**:
1. Tool detection: `if ! command -v TOOL &> /dev/null; then exit 0; fi`
2. Silent failure: All commands end with `|| exit 0`
3. Permission checking: Validate file access
4. Destructive operation prevention: Confirm before deletes
5. Environment validation: Check dependencies

**Design Principle**: "Hooks should NEVER interrupt Claude Code workflow"

---

## The Six Core Factories

### Factory vs. Guide Agent Comparison

| Aspect | Factories | Guide Agents |
|--------|-----------|--------------|
| **Purpose** | Template-driven generation | Interactive requirement gathering |
| **Location** | `documentation/templates/` | `.claude/agents/` |
| **Size** | 921-1,500 lines | Lightweight |
| **Automation** | High (encodes domain expertise) | Medium (structured conversations) |
| **Scope** | Syntax, structure, quality gates | Intent detection, delegation |

---

### 1. Skills Factory (SKILLS_FACTORY_PROMPT.md - 921 lines)

**Input Variables**:
- `BUSINESS_TYPE` - Industry classification
- `USE_CASES` - Comma-separated task list
- `NUMBER_OF_SKILLS` - Quantity to generate
- `ADDITIONAL_CONTEXT` - Preferences/constraints

**Output**: SKILL.md + Python files + sample data + HOW_TO_USE.md + ZIP

**YAML Frontmatter Requirements**:
```yaml
---
name: kebab-case-skill-name
description: 10-25 word single sentence
version: 1.0.0
---
```

**8 Standard SKILL.md Sections**: Title, Capabilities, Input Requirements, Output Formats, How to Use, Scripts, Best Practices, Limitations

**Four Generation Rules**:
1. No duplication (unique, focused purpose)
2. Composability (output feeds into input)
3. Kebab-case convention (all identifiers)
4. Complete packaging (documentation + samples included)

**Python Decision Logic**:
- **Use Python for**: calculations, data transformation, file generation, API interactions, complex algorithms
- **Omit Python for**: instructional content, templates, decision guidance, prompt-based formatting

---

### 2. Agents Factory (AGENTS_FACTORY_PROMPT.md - 1,123 lines)

**Input Variables**: Agent identity, purpose, tools, model, MCP integrations, system prompt, color, expertise

**Output**: Single `.md` file with enhanced YAML frontmatter

**Critical Formatting Rules**:
- Tools field is "comma-separated string (NOT array)"
- Name must be kebab-case exclusively
- Description must specify WHEN to invoke
- Color must match agent type (blue/green/red/purple/orange)

**Concurrency Limits**:
- Strategic agents: 15-20 processes
- Implementation agents: 20-30 processes
- Quality agents: 12-18 processes (sequential only)

---

### 3. Prompt Factory (PROMPTS_FACTORY_PROMPT.md - 403KB)

**10 Core Input Fields**:
1. Domain identification
2. Role inventory (10-20 presets)
3. Use case mapping
4. Compliance landscape
5. Standards and frameworks
6. Technology stack
7. Communication norms
8. Output types
9. Preset quantity
10. Domain nuances

**Output**: Self-contained prompt builder with domain-specific presets, 4 format options, quality validation

**7-Point Quality Gates**: XML structure, completeness, tokens, placeholders, workflow, best practices, examples

**Key Rule**: ONE industry per factory output (reject generic builders)

---

### 4. Slash Command Factory (MASTER_SLASH_COMMANDS_PROMPT.md - 1,500 lines)

**Input Variables**: `BUSINESS_TYPE`, `USE_CASES`, `NUMBER_OF_COMMANDS`, `COMMAND_TYPES`, `BASH_PERMISSIONS`, `OUTPUT_STYLE`, `STRUCTURE_PREFERENCE`, `ADDITIONAL_CONTEXT`

**Three Official Patterns**:

**Pattern A - Simple (Context then Task)**:
```markdown
---
description: Review code for best practices
allowed-tools: [Read, Grep]
---
# Context
# Task
```

**Pattern B - Multi-Phase (Discovery then Analysis then Task)**:
```markdown
---
description: Comprehensive codebase analysis
allowed-tools: [Read, Grep, Bash(find:*)]
---
# Phase 1: Discovery
# Phase 2: Analysis
# Phase 3: Task
```

**Pattern C - Agent-Style (Role then Process then Guidelines)**:
```markdown
---
description: API integration specialist
allowed-tools: [Read, Write, WebSearch, Bash(curl:*)]
model: claude-sonnet-4-5
---
# Role
# Process
# Guidelines
```

**Naming Validation**: `^[a-z0-9]+(-[a-z0-9]+){1,3}$` (2-4 words, kebab-case)
**Arguments**: Must use `$ARGUMENTS` standard (no `$1`, `$2` positional)

---

### 5. Hooks Factory (HOOKS_FACTORY_PROMPT.md)

**Input Variables**: `HOOK_PURPOSE`, `EVENT_TYPE`, `LANGUAGE`, `TOOL_REQUIRED`, `TRIGGER_CONDITION`, `FILE_PATTERNS`, `TOOL_NAMES`, `TIMEOUT`, `ACTION_DESCRIPTION`

**Output**: `hook.json` + `README.md` + validation report

**5-Layer Security Validation**:
1. Tool detection (graceful exit if missing)
2. Silent failure (all commands `|| exit 0`)
3. Safety constraints (forbid `rm -rf`, force pushes, DB drops)
4. File path protection (prevent directory traversal)
5. JSON structure verification (required fields present)

---

### 6. Validation Factory (Cross-Cutting Quality Layer)

**Skills Validation**:
- YAML frontmatter accuracy
- Kebab-case naming
- Required files exist (SKILL.md, HOW_TO_USE.md, code files)
- Documentation quality
- ZIP creation upon passing

**Agents Validation**:
- YAML frontmatter with proper metadata fields
- Kebab-case naming
- Tools as comma-separated strings
- Description indicates WHEN to invoke

**Prompts Validation**:
- XML structure integrity
- No placeholder text remaining
- Examples included
- Token counts within guidelines (3-6K core, 8-12K advanced)

**Hooks Validation (Security-Critical)**:
- JSON structure validity
- Safety patterns (tool detection, silent failure)
- No destructive operations
- Path safety
- Security score assignment

---

## Slash Commands (Complete List)

| Command | Purpose |
|---------|---------|
| `/build` | Gateway to factory-guide orchestrator (interactive or direct: `/build skill`, `/build agent`, etc.) |
| `/build-hook` | Dedicated hook creation tool |
| `/validate-output` | Validates generated assets + auto-ZIP for skills |
| `/install-skill` | Automated skill installation to `.claude/skills/` or `~/.claude/skills/` |
| `/install-hook` | Automated hook installation to `settings.json` |
| `/test-factory` | System testing and validation |
| `/factory-status` | System monitoring and diagnostics |
| `/sync-agents-md` | Documentation sync for Codex CLI interoperability |
| `/codex-exec` | CLI command execution for Codex compatibility |

**Recommended Pipeline**: Build > Validate > Install > Test

---

## Generated Skills (9 Production-Ready)

| Skill | Purpose |
|-------|---------|
| **aws-solution-architect** | Infrastructure design and analysis |
| **content-trend-researcher** | Multi-platform trend analysis |
| **microsoft-365-tenant-manager** | M365 administration automation |
| **agent-factory** | Meta-skill for creating new agents |
| **prompt-factory** | 69 professional role-based prompts across 15 domains |
| **slash-command-factory** | Custom command generation |
| **codex-cli-bridge** | 48KB Python bridge for Claude Code / Codex CLI interop |
| **hook-factory** | Automated hook generation with 7 event types |
| **claudemd-enhancer** | Documentation analysis and enhancement |

---

## CLAUDE.md Design (Modular v2.0)

The repo uses a modular CLAUDE.md architecture with context-specific files:

- Root `CLAUDE.md` (155 lines, 77% reduction from v1's 665 lines)
- `.github/CLAUDE.md` - GitHub workflows, task hierarchy
- `claude-skills-examples/CLAUDE.md` - Skill architecture patterns
- `generated-skills/CLAUDE.md` - Production skills catalog
- `documentation/CLAUDE.md` - Templates and references structure

**Critical Validation Rule (#0)**:
> "Always validate your output against official native examples before declaring complete."

**Other Principles**: Don't Overengineer, Edit Existing Files, Validate Inputs, Document Assumptions, Industry Context

---

## Key Patterns for Commandbase

### 1. Two-Tier Delegation Pattern
Lightweight orchestrator (haiku) to specialist agents (sonnet) to factory templates. This separates intent detection from generation, keeping each component focused.

### 2. Agent Type Color System
Strategic (blue), Implementation (green), Quality (red), Coordination (purple), Domain-Specific (orange). Provides visual categorization and implicit tool/concurrency constraints.

### 3. Factory Template as Knowledge Base
Each factory template (921-1,500 lines) encodes domain expertise, validation rules, naming conventions, and output formatting. Templates are the real intellectual property.

### 4. Build > Validate > Install > Test Pipeline
Explicit pipeline with quality gates between each stage. Validation is a separate command, not just inline checking.

### 5. Kebab-Case Everything Convention
Universal naming: `^[a-z0-9]+(-[a-z0-9]+){1,3}$` for skills, agents, commands. Consistent across all component types.

### 6. Modular CLAUDE.md Architecture
Context-specific CLAUDE.md files in subdirectories rather than one monolithic file. Reduces context loading overhead by 77%.

### 7. Tools as Comma-Separated Strings
Agent YAML frontmatter uses comma-separated string format for tools field, NOT arrays. This is specific to Claude Code's parser.

### 8. Description as Discovery Trigger
Agent descriptions specify WHEN to invoke, not WHAT the agent does. This enables Claude Code's auto-invocation matching.

### 9. Silent Failure for Hooks
All hooks use `|| exit 0` and tool detection guards. Hooks must never interrupt the main workflow.

### 10. Composability Principle
Skills designed so output from one feeds as input to another. No isolated tools -- everything connects.

---

## Codex CLI Bridge (Cross-Tool Interoperability)

**Seven-Module Architecture** (48KB Python):
1. `bridge.py` - CLI interface and orchestration
2. `safety_mechanism.py` - Environment validation with auto-recovery
3. `claude_parser.py` - CLAUDE.md parsing with YAML frontmatter support
4. `project_analyzer.py` - Directory scanning and metadata extraction
5. `agents_md_generator.py` - Template-based AGENTS.md assembly
6. `skill_documenter.py` - Reference-based documentation
7. `codex_executor.py` - Codex CLI command wrappers

**Translation**: CLAUDE.md to AGENTS.md for Codex CLI consumption. Reference-based approach (19KB AGENTS.md pointing to skills) vs. duplication.

---

## Open Questions

1. How does the Validation Factory differ from `/validate-output` command? (Possibly the same thing accessed differently)
2. What specific metrics does `/test-factory` check beyond `/validate-output`?
3. How does the `claudemd-enhancer` skill work -- does it modify existing CLAUDE.md files or create new ones?
4. The 6th "factory" may be the validation layer itself rather than a separate template file
5. How does the factory handle version upgrades (v1.3 to v1.4)?

---

## Sources

- [GitHub Repository](https://github.com/alirezarezvani/claude-code-skill-factory)
- [DeepWiki Architecture](https://deepwiki.com/alirezarezvani/claude-code-skill-factory)
- [Interactive Guide Agents](https://deepwiki.com/hysteam/claude-code-skill-factory/4-interactive-guide-agents)
- [Ultimate Guide Gist](https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935)
- [Codex CLI Bridge](https://deepwiki.com/alirezarezvani/claude-code-skill-factory/7.1-codex-cli-bridge)
- [Slash Command Factory SKILL.md](https://github.com/alirezarezvani/claude-code-skill-factory/blob/dev/generated-skills/slash-command-factory/SKILL.md)
