---
git_commit: 448f0d2
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Reviewed after 8 commits - research remains relevant; informed learning-from-sessions skill"
topic: "Claudeception - Claude Code Continuous Learning Skill"
tags: [research, skills, continuous-learning, meta-skill, hooks, knowledge-extraction]
status: complete
external_source: https://github.com/blader/claude-code-continuous-learning-skill
implemented_as: newskills/learning-from-sessions/SKILL.md
references:
  - claude-code-continuous-learning-skill/SKILL.md
  - claude-code-continuous-learning-skill/README.md
  - claude-code-continuous-learning-skill/WARP.md
  - claude-code-continuous-learning-skill/scripts/claudeception-activator.sh
  - claude-code-continuous-learning-skill/resources/skill-template.md
  - claude-code-continuous-learning-skill/resources/research-references.md
  - claude-code-continuous-learning-skill/examples/
---

# Research: Claudeception - Claude Code Continuous Learning Skill

**Date**: 2026-01-28
**Branch**: master (commandbase) / main (repo: 7d7f591)
**Source**: https://github.com/blader/claude-code-continuous-learning-skill
**Author**: blader

## Research Question

How does the Claudeception skill implement persistent learning across sessions? What is its architecture, implementation patterns, and how does the skill extraction workflow function?

## Summary

Claudeception is a meta-skill for Claude Code that enables autonomous knowledge extraction from work sessions. When Claude discovers non-obvious solutions through debugging, trial-and-error, or investigation, this skill codifies that knowledge into new SKILL.md files saved to the Claude Code skills directory. The name reflects "Claude creating skills about creating skills." It achieves persistent learning by writing new skill files to disk (`~/.claude/skills/`) that Claude Code's native semantic matching system loads at the start of future sessions. There is no database, no API, no special runtime -- just markdown files with optimized descriptions that the existing skill discovery system picks up automatically.

## Repository Structure

```
claude-code-continuous-learning-skill/
├── SKILL.md                              # Main skill definition (v3.0.0)
├── README.md                             # Installation and usage docs
├── WARP.md                               # Warp terminal guidance
├── LICENSE                               # MIT License
├── scripts/
│   └── claudeception-activator.sh        # UserPromptSubmit hook script
├── resources/
│   ├── skill-template.md                 # Template for new skills
│   └── research-references.md            # Academic paper citations
└── examples/
    ├── nextjs-server-side-error-debugging/SKILL.md
    ├── prisma-connection-pool-exhaustion/SKILL.md
    └── typescript-circular-dependency/SKILL.md
```

## Detailed Findings

### Core Mechanism: How Persistence Works

The persistence model is file-based. Claude Code loads skill names and descriptions (~100 tokens each) at startup and performs semantic matching against the current context to decide which skills to activate. Claudeception exploits this by writing new `SKILL.md` files with descriptions optimized for future retrieval (`README.md:128-134`).

The write path:
1. Knowledge identified during a session
2. Skill extracted via the 6-step workflow in `SKILL.md:66-225`
3. New `SKILL.md` file written to `~/.claude/skills/[skill-name]/SKILL.md` or `.claude/skills/[skill-name]/SKILL.md`
4. On next session startup, Claude Code loads the new skill's description
5. Semantic matching surfaces the skill when context is relevant

No external storage, no database -- the Claude Code skill directory IS the persistent memory.

### Skill Definition: YAML Frontmatter

The main skill file uses YAML frontmatter for metadata (`SKILL.md:1-22`):

```yaml
---
name: claudeception
description: |
  Claudeception is a continuous learning system that extracts reusable knowledge from work sessions.
  Triggers: (1) /claudeception command to review session learnings, (2) "save this as a skill"
  or "extract a skill from this", (3) "what did we learn?", (4) After any task involving
  non-obvious debugging, workarounds, or trial-and-error discovery.
author: Claude Code
version: 3.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Skill
  - AskUserQuestion
  - TodoWrite
---
```

Key design choices:
- `description` field is heavily optimized for semantic matching with specific trigger phrases
- `allowed-tools` grants file I/O (Read/Write/Edit), search (Grep/Glob), web research (WebSearch/WebFetch), skill management (Skill), and interaction (AskUserQuestion, TodoWrite)
- Version at 3.0.0 indicates significant iteration

### Activation System: Hook + Semantic Matching

Two activation paths exist:

**1. Automatic via Hook** (`scripts/claudeception-activator.sh:1-40`)

A bash script registered as a `UserPromptSubmit` hook that injects a reminder on every user prompt:

```bash
#!/bin/bash
cat << 'EOF'
CRITICAL: After completing this user request, you MUST evaluate whether
it produced extractable knowledge using the claudeception skill.

EVALUATION PROTOCOL:
1. COMPLETE the user's request first
2. EVALUATE: Did this require non-obvious investigation or debugging?
3. IF YES: ACTIVATE Skill(claudeception) to extract the knowledge
4. IF NO: SKIP
EOF
```

Configured in `settings.json` (`README.md:38-54`):
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/claudeception-activator.sh"
          }
        ]
      }
    ]
  }
}
```

This achieves higher activation rates than semantic matching alone because it fires on every interaction rather than waiting for context to match (`README.md:87`).

**2. Explicit Invocation** (`SKILL.md:372-378`)

- `/claudeception` slash command for retrospective review
- Natural language: "save this as a skill", "what did we learn?"
- Triggers retrospective mode that reviews the full session

### 6-Step Extraction Workflow

The core workflow defined in `SKILL.md:66-225`:

**Step 1: Check for Existing Skills** (`SKILL.md:66-103`)

Search skill directories before creating:
```sh
SKILL_DIRS=(".claude/skills" "$HOME/.claude/skills" "$HOME/.codex/skills")
rg --files -g 'SKILL.md' "${SKILL_DIRS[@]}" 2>/dev/null
rg -i "keyword1|keyword2" "${SKILL_DIRS[@]}" 2>/dev/null
```

Decision matrix for duplicates:
| Found | Action |
|-------|--------|
| Nothing related | Create new |
| Same trigger and fix | Update existing (bump version) |
| Same trigger, different cause | Create new + cross-links |
| Partial overlap | Update with "Variant" subsection |
| Same domain, different problem | Create new + "See also" |
| Stale or wrong | Mark deprecated + replacement link |

Versioning: patch = typos, minor = new scenario, major = breaking changes.

**Step 2: Identify the Knowledge** (`SKILL.md:105-111`)

Four questions to evaluate:
- What was the problem?
- What was non-obvious about the solution?
- What would help solve this faster next time?
- What are exact trigger conditions?

**Step 3: Research Best Practices** (`SKILL.md:113-156`)

Web search when technology-specific topics are involved:
- Official docs: `"[technology] [feature] official docs 2026"`
- Best practices: `"[technology] [problem] best practices 2026"`
- Common issues: `"[technology] [error message] solution 2026"`

Skip research for: project-specific internal patterns, clearly context-specific solutions, stable generic concepts.

**Step 4: Structure the Skill** (`SKILL.md:158-195`)

Standard sections: Problem, Context/Trigger Conditions, Solution, Verification, Example, Notes, References.

**Step 5: Write Effective Descriptions** (`SKILL.md:197-213`)

Critical for future discovery. Include:
- Specific symptoms with exact error messages
- Context markers (framework names, file types, tool names)
- Action phrases ("Use when...", "Helps with...", "Solves...")

Good example:
```yaml
description: |
  Fix for "ENOENT: no such file or directory" errors when running npm scripts
  in monorepos. Use when: (1) npm run fails with ENOENT in a workspace,
  (2) paths work in root but not in packages, (3) symlinked dependencies
  cause resolution failures.
```

**Step 6: Save the Skill** (`SKILL.md:215-223`)

- Project-specific: `.claude/skills/[skill-name]/SKILL.md`
- User-wide: `~/.claude/skills/[skill-name]/SKILL.md`
- Supporting scripts in `scripts/` subdirectory

### Quality Gates

Before finalizing any skill (`SKILL.md:256-269`):

- Description contains specific trigger conditions
- Solution has been verified to work
- Content is specific enough to be actionable
- Content is general enough to be reusable
- No sensitive information (credentials, internal URLs)
- Skill doesn't duplicate existing documentation
- Web research conducted when appropriate
- References section included if web sources consulted
- Current best practices (post-2025) incorporated

### Automatic Trigger Conditions

Self-evaluation criteria for when to extract (`SKILL.md:358-370`):

1. Non-obvious debugging (>10 minutes investigation, not in docs)
2. Error resolution (misleading error message, non-obvious root cause)
3. Workaround discovery (tool/framework limitation requiring experimentation)
4. Configuration insight (project-specific setup differing from standard)
5. Trial-and-error success (multiple approaches before working solution)

Self-check questions after tasks (`SKILL.md:379-386`):
- "Did I just spend meaningful time investigating something?"
- "Would future-me benefit from having this documented?"
- "Was the solution non-obvious from documentation alone?"

### Retrospective Mode

When `/claudeception` is invoked (`SKILL.md:226-233`):

1. Review session conversation history
2. List potential skill candidates with justifications
3. Prioritize highest-value, most reusable knowledge
4. Extract skills for top candidates (typically 1-3 per session)
5. Summarize what was created and why

### Self-Reflection Prompts

Used during work to identify opportunities (`SKILL.md:235-243`):
- "What did I just learn that wasn't obvious before starting?"
- "If I faced this exact problem again, what would I wish I knew?"
- "What error message or symptom led me here, and what was the actual cause?"
- "Is this pattern specific to this project, or would it help in similar projects?"
- "What would I tell a colleague who hits this same issue?"

### Memory Consolidation

When extracting skills (`SKILL.md:245-253`):
1. Combine related knowledge: one comprehensive skill vs. separate focused skills
2. Update existing skills rather than creating duplicates
3. Cross-reference related skills in documentation

### Skill Lifecycle

Four stages (`SKILL.md:279-285`):
1. **Creation**: Initial extraction with documented verification
2. **Refinement**: Update based on additional use cases or edge cases
3. **Deprecation**: Mark deprecated when underlying tools/patterns change
4. **Archival**: Remove or archive skills no longer relevant

### Anti-Patterns

What to avoid (`SKILL.md:271-277`):
- **Over-extraction**: Not every task deserves a skill
- **Vague descriptions**: "Helps with React problems" won't surface
- **Unverified solutions**: Only extract what actually worked
- **Documentation duplication**: Don't recreate official docs
- **Stale knowledge**: Mark with versions and dates

### Example Skills

Three complete examples demonstrate the pattern:

**1. Next.js Server-Side Error Debugging** (`examples/nextjs-server-side-error-debugging/SKILL.md:1-119`)
- Problem: Server-side errors don't appear in browser console
- Trigger: Generic error page + empty browser console + `getServerSideProps`
- Solution: Check terminal, add try-catch, check production logs, common causes

**2. Prisma Connection Pool Exhaustion** (`examples/prisma-connection-pool-exhaustion/SKILL.md`)
- Problem: Serverless functions exhaust database connection limits
- Trigger: `P2024: Timed out fetching a new connection` or `FATAL: too many connections`
- Solution: Connection pooling (PgBouncer/Prisma Accelerate), configure limits, singleton pattern

**3. TypeScript Circular Dependency** (`examples/typescript-circular-dependency/SKILL.md`)
- Problem: Circular imports compile fine but fail at runtime with `undefined`
- Trigger: `ReferenceError: Cannot access before initialization`, import is `undefined`
- Solution: Detect with madge, identify pattern, resolve via extraction/DI/dynamic imports

### Research Foundation

The skill cites academic papers (`resources/research-references.md`):

| Paper | Year | Key Concept Applied |
|-------|------|---------------------|
| Voyager (Wang et al.) | 2023 | Ever-growing skill library, self-verification |
| CASCADE | 2024 | Meta-skills for learning, knowledge codification |
| SEAgent (Sun et al.) | 2025 | Experiential learning, learning from failures |
| Reflexion (Shinn et al.) | 2023 | Self-reflection prompts, verbal reinforcement |
| EvoFSM | 2024 | Self-evolving memory, experience pools |

Also references Anthropic's engineering blog on agent skills and Claude Code skills documentation.

### Skill Template

A reusable template at `resources/skill-template.md:1-96` provides the standard structure for all extracted skills with YAML frontmatter, Problem, Context/Trigger Conditions, Solution, Verification, Example, Notes, and References sections.

## Code References

- `SKILL.md:1-22` - Main skill definition with YAML frontmatter
- `SKILL.md:36-53` - When to extract (5 categories)
- `SKILL.md:55-63` - Quality criteria (reusable, non-trivial, specific, verified)
- `SKILL.md:66-103` - Step 1: Check existing skills with search commands
- `SKILL.md:105-111` - Step 2: Identify the knowledge
- `SKILL.md:113-156` - Step 3: Research best practices
- `SKILL.md:158-195` - Step 4: Structure the skill
- `SKILL.md:197-213` - Step 5: Write effective descriptions
- `SKILL.md:215-223` - Step 6: Save locations
- `SKILL.md:226-243` - Retrospective mode and self-reflection prompts
- `SKILL.md:245-253` - Memory consolidation
- `SKILL.md:256-269` - Quality gates checklist
- `SKILL.md:271-285` - Anti-patterns and skill lifecycle
- `SKILL.md:287-354` - Complete extraction flow example
- `SKILL.md:358-386` - Automatic trigger conditions and self-check
- `scripts/claudeception-activator.sh:1-40` - Hook script
- `README.md:9-21` - Installation (clone to skills directory)
- `README.md:38-54` - Hook configuration in settings.json
- `README.md:128-134` - How Claude Code skill loading works
- `resources/skill-template.md:1-96` - Full skill template
- `resources/research-references.md:7-93` - Academic papers
- `examples/nextjs-server-side-error-debugging/SKILL.md:1-119` - Example skill
- `examples/prisma-connection-pool-exhaustion/SKILL.md` - Example skill
- `examples/typescript-circular-dependency/SKILL.md` - Example skill

## Architecture Notes

### Design Patterns

1. **File-as-Database**: Persistence via markdown files in known directories -- no external dependencies
2. **Semantic Discovery**: Description field acts as a search index for Claude Code's matching system
3. **Hook Injection**: `UserPromptSubmit` hook ensures evaluation on every interaction without relying solely on semantic matching
4. **Progressive Disclosure**: Only ~100 tokens (name + description) loaded at startup; full content on demand
5. **Self-Referential Meta-Skill**: The skill itself teaches Claude how to create more skills
6. **Quality-Gated Extraction**: Multiple checkpoints prevent low-value or duplicate skill creation
7. **Deduplication Strategy**: Search-before-create with a decision matrix for update vs. new

### Key Insight

The system's power comes from exploiting Claude Code's native skill loading mechanism. Rather than building a custom memory system, it writes to the same directory Claude Code already reads from at startup. The description field becomes the retrieval key, and optimizing it is equivalent to optimizing a database index.

## Open Questions

- How effective is semantic matching in practice for surfacing extracted skills at the right moment?
- What is the practical skill count limit before description matching degrades?
- How does the `Skill` tool in `allowed-tools` interact -- can claudeception invoke itself recursively?
- No mechanism exists for skill pruning/archival automation -- lifecycle management is manual
