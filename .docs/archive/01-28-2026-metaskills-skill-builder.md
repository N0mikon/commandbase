---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 61 commits - corrected local path references from newskills/ to plugins/ structure after plugin marketplace restructure"
topic: "Skill Creator Repos - Multi-Repo Analysis"
tags: [research, skill-builder, skill-creation, continuous-learning, metaskills, claudeception, blader]
status: archived
archived: 2026-02-09
archive_reason: "Research complete and findings fully consumed. Patterns from metaskills/skill-builder applied to creating-skills skill (now plugins/commandbase-meta/skills/creating-skills/); patterns from blader/claudeception applied to learning-from-sessions skill (now plugins/commandbase-session/skills/learning-from-sessions/). All references are external GitHub repos — no local code dependencies."
references:
  - https://github.com/metaskills/skill-builder
  - https://github.com/blader/claude-code-continuous-learning-skill
  - SKILL.md
  - converting-sub-agents-to-skills.md
  - reference/metadata-requirements.md
  - reference/skill-structure-and-format.md
  - reference/skill-best-practices.md
  - reference/editing-skills-guide.md
  - reference/nodejs-and-cli-patterns.md
  - templates/skill-template.md
  - scripts/claudeception-activator.sh
  - resources/research-references.md
  - resources/skill-template.md
  - examples/nextjs-server-side-error-debugging/SKILL.md
  - examples/prisma-connection-pool-exhaustion/SKILL.md
  - examples/typescript-circular-dependency/SKILL.md
---

# Research: metaskills/skill-builder - Skill Creator Workflow

**Date**: 2026-01-28
**Branch**: master
**Repo**: https://github.com/metaskills/skill-builder (68 stars, 13 forks)
**Author**: Ken Collins (metaskills) - AWS Hero, Principal Engineer

## Research Question

How does the metaskills/skill-builder repository implement its skill creator workflow? What patterns, structures, and conventions does it use for creating, editing, and converting Claude Code skills?

## Summary

The skill-builder is a **meta-skill** - a Claude Code skill that teaches Claude how to build other skills. It provides three core workflows: creating skills from scratch, editing existing skills, and converting sub-agents to skills. The repo is organized around progressive disclosure with a lean SKILL.md (the main entry point) supported by 5 reference documents, 1 template, and 1 dedicated conversion guide. The central thesis is that **the description field is the most critical element** - it determines when Claude invokes the skill, and the entire workflow revolves around crafting invocation-focused descriptions.

## Repository Structure

```
skill-builder/
├── SKILL.md                              # Main skill definition (core workflow)
├── converting-sub-agents-to-skills.md    # Dedicated conversion guide (~700 lines)
├── reference/
│   ├── editing-skills-guide.md           # How to refine existing skills (~500 lines)
│   ├── metadata-requirements.md          # YAML frontmatter deep dive (~400 lines)
│   ├── nodejs-and-cli-patterns.md        # CLI + Node.js examples (~600 lines)
│   ├── skill-best-practices.md           # Quality standards (~600 lines)
│   └── skill-structure-and-format.md     # File organization patterns (~250 lines)
└── templates/
    └── skill-template.md                 # Boilerplate starter (~150 lines)
```

## Detailed Findings

### The Skill Creator Workflow (SKILL.md)

The SKILL.md frontmatter defines when this skill activates:

```yaml
---
name: skill-builder
description: Use this skill when creating new Claude Code skills from scratch, editing
  existing skills to improve their descriptions or structure, or converting Claude Code
  sub-agents to skills. This includes designing skill workflows, writing SKILL.md files,
  organizing supporting files with intention-revealing names, and leveraging CLI tools
  and Node.js scripting.
---
```

The skill defines three modes of operation:

#### Mode 1: Creating New Skills (5-Step Process)

1. **Gather Requirements** - Ask the user: what task, when to invoke, personal vs project, similar patterns in docs
2. **Design the Skill** - Choose gerund-form name, draft invocation-focused description, plan instruction structure, plan supporting files
3. **Leverage CLI and Node.js** - Use CLI tools (gh, aws, npm), Node.js v24+ with ESM, provide runnable commands
4. **Create the Skill** - Write SKILL.md with YAML frontmatter, add supporting files with intention-revealing names, organize for progressive disclosure
5. **Validate** - Check name (gerund, max 64 chars), description (clear, trigger-focused, third person), no `allowed-tools` field, no Python scripts

#### Mode 2: Editing Existing Skills

Six common improvement scenarios:
1. Refine description (most impactful change)
2. Apply progressive disclosure (move detail to reference files)
3. Improve organization
4. Add CLI/Node.js patterns
5. Update outdated content
6. Add supporting files

#### Mode 3: Converting Sub-Agents to Skills

Delegates to `./converting-sub-agents-to-skills.md` for comprehensive guidance. Quick overview:
1. Analyze sub-agent's YAML frontmatter and instructions
2. Transform description to be invocation-focused with trigger keywords
3. Convert to skill format (remove `model`, `tools` fields)
4. Enhance with progressive disclosure and supporting files
5. Create in `~/.claude/skills/` for global availability

### Critical Design Principles

#### 1. Description as Invocation Trigger (metadata-requirements.md)

The description field is treated as THE most critical element in the entire skill system.

**Writing Formula**: `"Use this skill when [primary situation]. This includes [specific use cases]..."`

**Key principles**:
- Be specific about WHEN, not just WHAT
- Include trigger keywords users might say
- List concrete use cases
- Write in third person
- Think from Claude's perspective: "When would I know to use this?"
- Max 1024 characters

**Good example**: "Use this skill when working with CSV files using xsv CLI, including exploring structure, filtering data, selecting columns, or transforming files"
**Bad example**: "CSV helper skill"

#### 2. Gerund Form Naming Convention

All skill names use verb + -ing form:
- `processing-pdfs` (not `pdf-processor`)
- `analyzing-data` (not `data-analyzer`)
- `deploying-lambdas` (not `lambda-deployer`)

Max 64 characters, lowercase, hyphens only.

#### 3. Progressive Disclosure Pattern (skill-best-practices.md)

- SKILL.md: Keep under 500 lines (ideally 150-200), core workflow only
- Reference files: Detailed content with intention-revealing names
- Link with relative paths: `./reference/aws-lambda-patterns.md`
- One level deep - no nested references from reference files

#### 4. Intention-Revealing File Names

- `./converting-sub-agents-to-skills.md` (what the file teaches)
- `./reference/nodejs-and-cli-patterns.md` (what patterns it contains)
- NOT: `./reference.md`, `./helpers.md`, `./utils.md`

#### 5. CLI-First, Node.js for Complex Logic (nodejs-and-cli-patterns.md)

**CLI tools emphasized**: gh, aws, npm, git, jq
**Node.js**: v24+ with ESM imports, `.js` files only (no TypeScript)
**Explicitly forbidden**: Python scripts

Node.js script template pattern:
```javascript
#!/usr/bin/env node
import { readFile } from 'fs/promises';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);
```

#### 6. No Restrictive Fields

Skills inherit ALL Claude Code CLI capabilities. No `allowed-tools`, `model`, or `tools` fields should appear in SKILL.md frontmatter.

### Sub-Agent to Skill Conversion (converting-sub-agents-to-skills.md)

The key transformation insight:
- **Sub-agents** explain WHAT they are (noun forms: `code-reviewer`)
- **Skills** explain WHEN to use them (gerund forms: `reviewing-code`)

Three detailed conversion examples provided:

| Sub-Agent | Skill Name | Key Change |
|-----------|------------|------------|
| Code Reviewer | `reviewing-code` | Description → invocation triggers |
| Debugger | `debugging-applications` | Remove model/tools fields |
| Data Scientist | `analyzing-data` | Add progressive disclosure |

Conversion checklist includes:
- Name transformed to gerund form
- Description rewritten for invocation focus
- `model` and `tools` fields removed
- Content enhanced with CLI/Node.js emphasis
- Supporting files given intention-revealing names
- SKILL.md kept under 500 lines

### Skill Template (templates/skill-template.md)

Provides a boilerplate starting point with sections:
- YAML frontmatter (name + description)
- Overview
- Core Approach
- Step-by-Step Instructions (with CLI tools)
- Examples
- CLI Tools section
- Node.js patterns section
- Best practices
- Validation checklist
- Troubleshooting
- Supporting file references

### Skill Locations

- **Personal Skills**: `~/.claude/skills/` - Available across all projects
- **Project Skills**: `.claude/skills/` - Project-specific, shared with team via git

## Code References

- `SKILL.md` - Main skill definition, three workflow modes, validation steps
- `converting-sub-agents-to-skills.md` - ~700 line conversion guide with 3 examples
- `reference/metadata-requirements.md` - Description writing formula and validation
- `reference/skill-structure-and-format.md` - Directory layout and YAML syntax
- `reference/skill-best-practices.md` - Progressive disclosure, naming, quality gates
- `reference/editing-skills-guide.md` - 6 improvement scenarios, editing workflow
- `reference/nodejs-and-cli-patterns.md` - CLI tools catalog, Node.js ESM patterns, 2 complete script examples
- `templates/skill-template.md` - Boilerplate starter template

## Architecture Notes

### Design Patterns

1. **Meta-Skill Pattern**: A skill that creates other skills - self-referential architecture where the skill-builder follows its own conventions
2. **Progressive Disclosure**: SKILL.md as thin entry point, reference files for depth - keeps context window lean
3. **Intention-Revealing Organization**: Every file name communicates its purpose without needing to open it
4. **Description-Driven Invocation**: The entire system pivots on crafting descriptions that tell Claude WHEN to activate
5. **CLI-First Philosophy**: Prefer shell tools over custom code; use Node.js only when CLI tools aren't sufficient
6. **No Restriction Pattern**: Skills inherit full Claude CLI capabilities - no artificial tool/model restrictions

### What Makes This Repo Distinct

Compared to other skill creators in the ecosystem:
- **Focus on conversion**: The sub-agent-to-skill migration guide is unique to this repo
- **Reference-heavy approach**: 5 dedicated reference documents vs. monolithic instruction files
- **Strong opinions**: Explicit anti-patterns (no Python, no TypeScript, no `allowed-tools`)
- **Production focus**: Quality gates, validation checklists, testing guidance
- **Author credibility**: Ken Collins (AWS Hero, Experts.js creator with 709 stars) brings multi-agent systems expertise

### Key Conventions for Adoption

| Convention | Requirement |
|------------|-------------|
| Skill name | Gerund form, max 64 chars, lowercase, hyphens |
| Description | Max 1024 chars, invocation-focused, third person |
| SKILL.md length | Under 500 lines (ideally 150-200) |
| File names | Intention-revealing, lowercase with hyphens |
| Scripts | Node.js v24+ ESM only, no Python/TypeScript |
| Frontmatter | Only `name` and `description` fields |
| Reference depth | One level deep from SKILL.md |

## Open Questions

1. **Activation reliability**: How does skill-builder's description-focused approach compare to Scott Spence's "Forced Eval Hook" pattern (84% success rate)?
2. **Scale limits**: At what point does the progressive disclosure pattern break down (too many reference files)?
3. **Node.js exclusivity**: The strict "no Python" stance may limit adoption for data science workflows where Python tooling is standard
4. **Version tracking**: No versioning system for skills - how to manage skill evolution across teams?

## Application in This Codebase

This research directly informed the design of the creating-skills skill (originally at `newskills/creating-skills/`, now at `plugins/commandbase-meta/skills/creating-skills/`):

| Pattern from skill-builder | Applied in creating-skills |
|---------------------------|---------------------------|
| Gerund-form naming | `./reference/naming-conventions.md` |
| Description-as-invocation-trigger | `./reference/description-writing-guide.md` |
| Progressive disclosure | Reference file structure, skinny pointers |
| 5-step creation workflow | Mode 1: Create New Skill (Steps 1-5) |
| Sub-agent conversion | Mode 3 + `./reference/converting-subagents.md` |
| Validation checklists | `./reference/validation-rules.md` |

Key decisions informed by this research:
- Adopted gerund naming over kebab-case nouns (metaskills pattern)
- Chose description-first workflow (description determines triggering)
- Kept SKILL.md under 500 lines with reference file overflow
- Used intention-revealing file names (not generic `helpers.md`)

---
---

# Research: blader/claude-code-continuous-learning-skill (Claudeception)

**Date**: 2026-01-28
**Branch**: master
**Repo**: https://github.com/blader/claude-code-continuous-learning-skill
**Author**: blader
**Latest Commit**: 7d7f591 (Merge pull request #13)

## Research Question

How does the blader/claude-code-continuous-learning-skill repository implement persistent learning across Claude Code sessions? What patterns does it use for autonomous skill extraction, activation, and quality control?

## Summary

Claudeception is a **self-referential meta-skill** that enables Claude Code to autonomously extract reusable knowledge from work sessions and save it as new skills. Unlike skill-builder (which teaches Claude to build skills on request), Claudeception operates as a **continuous learning system** - it evaluates every interaction for extractable knowledge and creates skills without explicit user requests. The repo implements a two-tier activation system: semantic description matching (passive) + a `UserPromptSubmit` hook (active), with the hook injecting mandatory evaluation instructions on every prompt. The system is grounded in academic research from Voyager, CASCADE, SEAgent, Reflexion, and EvoFSM.

## Repository Structure

```
claude-code-continuous-learning-skill/
├── SKILL.md                                          # Main skill definition (390 lines, v3.0.0)
├── README.md                                         # Installation & usage guide
├── WARP.md                                           # Warp.dev integration guide
├── LICENSE                                           # MIT
├── scripts/
│   └── claudeception-activator.sh                    # UserPromptSubmit hook (40 lines)
├── resources/
│   ├── skill-template.md                             # Template for new skills (96 lines)
│   └── research-references.md                        # Academic research basis (184 lines)
└── examples/
    ├── nextjs-server-side-error-debugging/SKILL.md   # Example: Next.js debugging (119 lines)
    ├── prisma-connection-pool-exhaustion/SKILL.md     # Example: Prisma connection pooling (162 lines)
    └── typescript-circular-dependency/SKILL.md        # Example: TS circular deps (238 lines)
```

## Detailed Findings

### Core Architecture: Two-Tier Activation

Claudeception uses two independent activation mechanisms to maximize knowledge capture:

#### Tier 1: Semantic Description Matching (SKILL.md:3-8)

The YAML frontmatter description triggers activation when Claude detects relevant context:

```yaml
description: |
  Claudeception is a continuous learning system that extracts reusable knowledge from work sessions.
  Triggers: (1) /claudeception command to review session learnings, (2) "save this as a skill"
  or "extract a skill from this", (3) "what did we learn?", (4) After any task involving
  non-obvious debugging, workarounds, or trial-and-error discovery.
```

#### Tier 2: UserPromptSubmit Hook (claudeception-activator.sh:12-39)

A bash script outputs mandatory evaluation instructions on **every** user prompt:

```bash
cat << 'EOF'
🧠 MANDATORY SKILL EVALUATION REQUIRED
CRITICAL: After completing this user request, you MUST evaluate whether
it produced extractable knowledge using the claudeception skill.
EOF
```

**Why both tiers**: The README explains (README.md:87): "This achieves higher activation rates than relying on semantic description matching alone."

**Data flow**:
1. User submits prompt → `UserPromptSubmit` event fires
2. Hook script outputs evaluation protocol text
3. Claude processes user's request with injected instructions
4. After task completion, Claude self-evaluates using 4-step protocol
5. If criteria met, Claude invokes `Skill(claudeception)` to extract knowledge

### The 6-Step Extraction Process (SKILL.md:66-223)

#### Step 1: Check for Existing Skills (SKILL.md:66-104)

Before creating, search skill directories for duplicates:

```sh
SKILL_DIRS=(".claude/skills" "$HOME/.claude/skills" "$HOME/.codex/skills")
rg --files -g 'SKILL.md' "${SKILL_DIRS[@]}" 2>/dev/null
rg -i "keyword1|keyword2" "${SKILL_DIRS[@]}" 2>/dev/null
```

Decision matrix (SKILL.md:92-99):

| Found | Action |
|-------|--------|
| Nothing related | Create new |
| Same trigger and fix | Update existing (version bump) |
| Same trigger, different root cause | Create new, add `See also:` links |
| Partial overlap | Update existing with new "Variant" subsection |
| Stale or wrong | Mark deprecated, add replacement link |

Versioning: patch = typos, minor = new scenario, major = breaking changes (SKILL.md:101).

#### Step 2: Identify the Knowledge (SKILL.md:105-111)

Four analysis questions:
- What was the problem or task?
- What was non-obvious about the solution?
- What would someone need to know to solve this faster next time?
- What are the exact trigger conditions?

#### Step 3: Research Best Practices (SKILL.md:113-155)

Web search for current information when the topic involves specific technologies.

**Always search for**: best practices, current documentation, common patterns, known gotchas, alternatives.

**Search strategy** (SKILL.md:137-144):
```
1. "[technology] [feature] official docs 2026"
2. "[technology] [problem] best practices 2026"
3. "[technology] [error message] solution 2026"
```

**Skip searching when**: project-specific internals, context-specific solutions, stable generic concepts.

#### Step 4: Structure the Skill (SKILL.md:157-195)

Required YAML frontmatter fields:
- `name`: descriptive-kebab-case
- `description`: multi-line with exact use cases, trigger conditions, problem description
- `author`: original-author or "Claude Code"
- `version`: semantic versioning
- `date`: YYYY-MM-DD

Required markdown sections:
1. `# [Skill Name]`
2. `## Problem` - What the skill addresses
3. `## Context / Trigger Conditions` - When to use, exact error messages
4. `## Solution` - Step-by-step
5. `## Verification` - How to confirm it worked
6. `## Example` - Concrete application
7. `## Notes` - Caveats, edge cases
8. `## References` - Optional source links

#### Step 5: Write Effective Descriptions (SKILL.md:197-213)

The description must include:
- **Specific symptoms**: Exact error messages, unexpected behaviors
- **Context markers**: Framework names, file types, tool names
- **Action phrases**: "Use when...", "Helps with...", "Solves..."

Good example (SKILL.md:206-213):
```
Fix for "ENOENT: no such file or directory" errors when running npm scripts
in monorepos. Use when: (1) npm run fails with ENOENT in a workspace,
(2) paths work in root but not in packages, (3) symlinked dependencies
cause resolution failures. Covers Lerna, Turborepo, and npm workspaces.
```

#### Step 6: Save the Skill (SKILL.md:215-223)

- **Project-specific**: `.claude/skills/[skill-name]/SKILL.md`
- **User-wide**: `~/.claude/skills/[skill-name]/SKILL.md`
- Supporting scripts in `scripts/` subdirectory

### Allowed Tools (SKILL.md:11-21)

The skill explicitly allows 10 tools:
1. Read, Write, Edit (file operations)
2. Grep, Glob (search)
3. WebSearch, WebFetch (web research)
4. Skill (invoke other skills)
5. AskUserQuestion (user interaction)
6. TodoWrite (task tracking)

**Note**: Unlike metaskills/skill-builder which prohibits `allowed-tools`, Claudeception explicitly restricts its tool set. This constrains the skill to file operations, search, and web research - no Bash execution.

### Quality Gates (SKILL.md:257-269)

9-item checklist before finalizing:
- [ ] Description contains specific trigger conditions
- [ ] Solution has been verified to work
- [ ] Content is specific enough to be actionable
- [ ] Content is general enough to be reusable
- [ ] No sensitive information (credentials, internal URLs)
- [ ] Skill doesn't duplicate existing documentation or skills
- [ ] Web research conducted when appropriate
- [ ] References section included if web sources consulted
- [ ] Current best practices (post-2025) incorporated when relevant

### Retrospective Mode (SKILL.md:225-234)

When `/claudeception` is invoked at session end:
1. **Review** conversation history for extractable knowledge
2. **Identify** potential skills with justifications
3. **Prioritize** highest-value, most reusable knowledge
4. **Extract** top candidates (typically 1-3 per session)
5. **Summarize** what was created and why

### Self-Reflection Prompts (SKILL.md:236-244)

Five introspection questions during work:
1. "What did I just learn that wasn't obvious before starting?"
2. "If I faced this exact problem again, what would I wish I knew?"
3. "What error message or symptom led me here, and what was the actual cause?"
4. "Is this pattern specific to this project, or would it help in similar projects?"
5. "What would I tell a colleague who hits this same issue?"

### Anti-Patterns (SKILL.md:271-277)

1. **Over-extraction**: Not every task deserves a skill
2. **Vague descriptions**: "Helps with React problems" won't match
3. **Unverified solutions**: Only extract what actually worked
4. **Documentation duplication**: Don't recreate official docs
5. **Stale knowledge**: Mark skills with versions and dates

### Skill Lifecycle (SKILL.md:279-286)

Four stages: Creation → Refinement → Deprecation → Archival

### Hook Activation Protocol (claudeception-activator.sh:20-36)

The 4-step evaluation protocol injected on every prompt:

1. **COMPLETE** the user's request first
2. **EVALUATE**: Did this require non-obvious investigation? Would it help in future situations? Was it beyond documentation lookup?
3. **IF YES**: Use `Skill(claudeception)` NOW to extract knowledge
4. **IF NO**: Skip extraction

Key design: The hook enforces evaluation; the skill itself applies quality gates before creating files. Two-tier quality control.

### Example Skill Patterns (examples/)

All three examples follow identical structure:

**Common YAML frontmatter pattern**:
```yaml
---
name: kebab-case-problem-description
description: |
  [Action verb] [technology] [problem]. Use when:
  (1) [exact error/symptom], (2) [exact error/symptom],
  (3) [behavioral symptom], (4) [environmental condition].
author: Claude Code
version: 1.0.0
date: YYYY-MM-DD
---
```

**Common description formula**: One-line summary → "Use when:" → 4-5 numbered symptoms with exact error messages → optional context sentence.

**Metrics across examples**:

| Aspect | Next.js | Prisma | TypeScript |
|--------|---------|--------|------------|
| Symptoms in description | 4 | 4 | 5 |
| Solution steps | 4 | 4 | 4 (+ 5 sub-strategies) |
| Code blocks | 4 | 7 | 12 |
| Total lines | 119 | 162 | 238 |
| Exact error messages | 1 | 3 | 3 |

**Key patterns**:
- Solutions progress simple → complex (diagnostic → fix → production → prevention)
- Every example includes Before/After in the Example section
- Notes section always 5-6 bullets covering edge cases
- File paths embedded in code block comments
- Provider/tool names are explicit (never generic)

### Academic Research Foundation (resources/research-references.md)

The design draws from 5 core papers:

| Paper | Year | Key Concept Applied |
|-------|------|---------------------|
| **Voyager** (Wang et al.) | 2023 | Ever-growing skill library, self-verification before adding to library |
| **CASCADE** | 2024 | Meta-skills for learning, knowledge codification into shareable format |
| **SEAgent** (Sun et al.) | 2025 | Experiential learning from both failures and successes |
| **Reflexion** (Shinn et al.) | 2023 | Self-reflection prompts, verbal reinforcement, long-term memory |
| **EvoFSM** | 2024 | Experience pools, distilling strategies from sessions |

**Anthropic blog reference** (research-references.md:118-128): Cites the "Equipping Agents for the Real World with Agent Skills" post. Key quote: "We hope to enable agents to create, edit, and evaluate Skills on their own" - Claudeception is an implementation of this vision.

**Research-to-implementation mapping**:
- Voyager self-verification → Quality Gates checklist
- Reflexion self-reflection → 5 self-reflection prompts
- SEAgent trial-and-error → Retrospective mode
- CASCADE memory consolidation → Skill lifecycle (Creation → Archival)
- EvoFSM experience pools → Skill library with directory search

## Code References

- `SKILL.md:1-22` - YAML frontmatter with 10 allowed tools, v3.0.0
- `SKILL.md:29-55` - Skill quality criteria (reusable, non-trivial, specific, verified)
- `SKILL.md:66-104` - Step 1: Check existing skills with rg search commands and decision matrix
- `SKILL.md:105-111` - Step 2: Identify knowledge with 4 analysis questions
- `SKILL.md:113-155` - Step 3: Web research strategy with search templates
- `SKILL.md:157-195` - Step 4: Skill structure template with required sections
- `SKILL.md:197-213` - Step 5: Description writing guidelines with examples
- `SKILL.md:215-223` - Step 6: Save locations (project vs user-wide)
- `SKILL.md:225-234` - Retrospective mode (5-step session review)
- `SKILL.md:236-244` - 5 self-reflection prompts
- `SKILL.md:257-269` - 9-item quality gate checklist
- `SKILL.md:271-277` - 5 anti-patterns to avoid
- `SKILL.md:279-286` - 4-stage skill lifecycle
- `SKILL.md:356-389` - Workflow integration (automatic triggers + self-check)
- `claudeception-activator.sh:12-39` - Hook output with 4-step evaluation protocol
- `resources/skill-template.md:1-96` - Skill creation template with extraction checklist
- `resources/research-references.md:7-93` - 5 core academic papers
- `resources/research-references.md:118-140` - Anthropic skills documentation references
- `README.md:40-54` - User-level hook settings.json configuration
- `README.md:69-83` - Project-level hook settings.json configuration
- `examples/nextjs-server-side-error-debugging/SKILL.md` - Example: server-side errors
- `examples/prisma-connection-pool-exhaustion/SKILL.md` - Example: connection pooling
- `examples/typescript-circular-dependency/SKILL.md` - Example: circular imports

## Architecture Notes

### Design Patterns

1. **Continuous Learning Loop**: Task → Self-Evaluate → Extract (if worthy) → Save → Available for future sessions
2. **Two-Tier Activation**: Semantic matching (passive) + UserPromptSubmit hook (active) for maximum knowledge capture
3. **Two-Tier Quality Control**: Hook enforces evaluation step; skill applies quality gates before file creation
4. **Academic-Grounded Design**: Every major feature traces to a published research paper
5. **Self-Referential Meta-Skill**: A skill whose purpose is creating other skills from experience
6. **Explicit Tool Restriction**: Uses `allowed-tools` to constrain to file ops, search, web - no Bash execution
7. **Decision Matrix Pattern**: Codifies update-vs-create decisions into a lookup table (SKILL.md:92-99)
8. **Semantic-First Descriptions**: All descriptions follow "Action + Technology + 'Use when:' + numbered symptoms" formula

### What Makes This Repo Distinct (vs. metaskills/skill-builder)

| Aspect | Claudeception (blader) | Skill-Builder (metaskills) |
|--------|------------------------|---------------------------|
| **Primary purpose** | Autonomous learning from sessions | Teaching Claude to build skills on request |
| **Activation model** | Two-tier: semantic + hook | Description-only (semantic matching) |
| **Trigger** | Automatic after every task | User-initiated (`/skill-builder` or context) |
| **`allowed-tools`** | Yes (10 tools explicitly listed) | Prohibited (inherit all capabilities) |
| **Naming convention** | kebab-case (noun-form, problem-focused) | Gerund form (verb-ing, action-focused) |
| **Research basis** | 5 academic papers + Anthropic blog | Practical experience + Anthropic docs |
| **Web research step** | Explicit step with search templates | Not mentioned |
| **Hook system** | UserPromptSubmit hook script | No hook |
| **Example skills** | 3 complete examples (119-238 lines each) | References + templates |
| **Skill lifecycle** | 4 stages (Creation → Archival) | Not formally defined |
| **Version tracking** | Semantic versioning with rules | Not specified |

### Key Conventions for Adoption

| Convention | Requirement |
|------------|-------------|
| Skill name | kebab-case, problem-descriptive |
| Description | "Use when:" + 4-5 numbered symptoms with exact error messages |
| SKILL.md frontmatter | name, description, author, version, date, allowed-tools |
| Sections | Problem, Context/Trigger, Solution, Verification, Example, Notes, References |
| Quality gates | 9-item checklist (verified, actionable, reusable, no sensitive data) |
| Activation | Semantic matching + UserPromptSubmit hook (dual-tier) |
| Versioning | Semantic (patch/minor/major) with defined rules |
| Web research | Required for technology-specific topics |
| Save location | `~/.claude/skills/[name]/SKILL.md` or `.claude/skills/[name]/SKILL.md` |

## Open Questions

1. **Hook overhead**: The hook injects ~25 lines of text on every single prompt - what is the context window cost at scale?
2. **Activation rate**: The README claims hooks achieve "higher activation rates" than semantic matching alone, but no metrics are provided
3. **allowed-tools conflict**: Claudeception uses `allowed-tools` while skill-builder explicitly forbids it - which approach is correct for Claude Code skills?
4. **Bash exclusion**: No Bash in allowed-tools means skills can't include runnable verification commands - is this intentional?
5. **Version 3.0.0**: The skill is at v3.0.0 but the repo has limited git history - what changed between major versions?
6. **Cross-skill deduplication**: The existing-skill check uses `rg` search, but how reliable is text-based dedup for semantic similarity?

## Application in This Codebase

This research directly informed the design of the learning-from-sessions skill (originally at `newskills/learning-from-sessions/`, now at `plugins/commandbase-session/skills/learning-from-sessions/`):

| Pattern from Claudeception | Applied in learning-from-sessions |
|---------------------------|----------------------------------|
| 6-step extraction workflow | Steps 1-6 in Extraction Workflow section |
| 5 self-reflection prompts | Self-Reflection Prompts section (identical) |
| Quality gates checklist | `./reference/quality-gates.md` + Step 5 |
| Dedup decision matrix | Step 1: Dedup Check with decision table |
| Symptom-based descriptions | `./reference/description-optimization.md` |
| Retrospective mode | Retrospective Mode section |
| Output template sections | `./templates/extracted-skill-template.md` |

The academic research basis (Voyager, CASCADE, SEAgent, Reflexion, EvoFSM) is documented in `./reference/research-foundations.md`, which explicitly credits Claudeception as an implementation source.

Key decisions informed by this research:
- Adopted verify-before-storing principle (Iron Law)
- Implemented dedup-first workflow
- Used symptom-based description formulas with exact error messages
- Added complexity check to route to /rcode for complex extractions
- Set 3-skill-per-session limit based on quality-over-quantity principle
