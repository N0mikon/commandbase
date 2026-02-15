# Plugin Layout Guide

How to structure a Claude Code plugin — directory layout, component placement, shared references, dependency decisions, and suite completeness testing.

Based on findings from `.docs/research/02-14-2026-plugin-architecture-patterns-for-ai-coding-assistants.md`.

## Standard Plugin Structure

```
plugins/plugin-name/
├── README.md              # Required: plugin description, skill table, install instructions
├── skills/                # Skill directories (gerund-form names)
│   ├── doing-thing-a/
│   │   ├── SKILL.md       # Core instructions (<500 lines)
│   │   ├── reference/     # On-demand detail files
│   │   └── templates/     # Output templates
│   └── doing-thing-b/
│       └── SKILL.md
├── agents/                # Optional: subagent .md files (noun-form names)
│   ├── thing-doer.md
│   └── thing-finder.md
├── hooks/                 # Optional: hooks.json defining lifecycle hooks
│   └── hooks.json
├── scripts/               # Optional: executable scripts referenced by hooks/skills
├── reference/             # Optional: plugin-level shared reference material
│   └── reusable-pattern.md
└── SETUP.md               # Optional: manual configuration steps (deny rules, env vars)
```

## Component Placement Rules

| Component | Location | Name Convention | When to Use |
|-----------|----------|-----------------|-------------|
| Skills | `skills/<gerund-name>/SKILL.md` | `doing-thing` | Primary user-facing capabilities |
| Agents | `agents/<noun-name>.md` | `thing-doer` | Delegated subtasks spawned by skills |
| Hooks | `hooks/hooks.json` | N/A | Lifecycle automation (PreToolUse, PostToolUse, Stop, etc.) |
| Scripts | `scripts/<name>.py` or `.sh` | Descriptive | Executed by hooks or skills, never enters context window |
| Skill references | `skills/<name>/reference/` | Intention-revealing | On-demand detail for a specific skill |
| Plugin references | `reference/` | Intention-revealing | Design-time patterns reusable across plugins |

## Reference File Architecture

### Skill-Level References (runtime)

Each skill's `reference/` directory contains files loaded on demand when that skill is active. These are scoped to how the skill uses the knowledge.

**Split by use case, not by topic.** When multiple skills need the same domain knowledge, give each skill a reference file scoped to its consumption pattern:

```
# BAD: One monolithic reference shared across skills
skills/linting-vault/reference/ofm-reference.md      # Too broad
skills/capturing-vault/reference/ofm-reference.md     # Same file, wastes tokens

# GOOD: Split by how each skill uses the knowledge
skills/linting-vault/reference/ofm-validation-rules.md    # Regex patterns, structural rules
skills/capturing-vault/reference/ofm-note-formats.md      # Templates, frontmatter schemas
```

### Plugin-Level References (design-time)

A plugin's top-level `reference/` directory holds canonical patterns that other plugins can adapt. These are not referenced at runtime by other plugins — skills are self-contained. They serve as documented sources of truth.

```
plugins/commandbase-core/reference/
└── batch-safety-protocol.md    # Generalized pattern: dry-run → checkpoint → chunked
```

Other plugins create their own domain-specific adaptations:
```
plugins/commandbase-vault/skills/maintaining-vault/reference/
└── batch-safety-protocol.md    # Vault-specific version, cites core as source
```

## Dependency Decisions

### Runtime Dependencies (acceptable when needed)

One plugin needs another plugin's tools, agents, or hooks at execution time.

**When to use:**
- Infrastructure/cross-cutting concerns (docs agents, error tracking)
- Stable interfaces unlikely to change
- The dependency provides functionality, not just knowledge

**How to declare:** Document in README.md under `## Dependencies`.

```markdown
## Dependencies
- commandbase-core (docs agents: docs-writer, docs-updater, docs-locator, docs-analyzer)
```

### Knowledge Dependencies (prefer duplication)

One plugin uses another plugin's patterns or reference content at design time.

**When to use:**
- Domain-specific reference material (syntax rules, safety protocols)
- Patterns that different consumers use differently
- Content that would bloat consumers with irrelevant material if shared

**How to handle:** Bake the knowledge into your own skill's reference files. Cite the source.

```markdown
# My Domain-Specific Safety Protocol

Adapted from `commandbase-core/reference/batch-safety-protocol.md`.
[Domain-specific content follows...]
```

### Decision Framework

| Question | If YES → | If NO → |
|----------|----------|---------|
| Does the skill need another plugin's agent/hook at runtime? | Runtime dependency | Not a runtime dependency |
| Can I do this with Read/Write/Glob instead of an external tool? | Knowledge dependency (bake it in) | May need runtime dependency |
| Would sharing this file bloat the consumer with irrelevant content? | Split and bake in use-case-specific version | Consider sharing if truly identical |
| Is the source pattern stable and unlikely to change? | Either approach works | Bake in — avoids breaking when source evolves |

## Suite Completeness: The Tuesday Test

After designing a plugin with 5+ skills, run this gap analysis before considering the suite complete.

### Procedure

1. **List all skills** and classify each as:
   - **Episodic** — project-level, run occasionally (setup, architecture, major restructuring)
   - **Habitual** — daily/weekly, run routinely (capture, review, commit, maintain)

2. **Walk through a typical day:**
   > "What does a user do with this tool on a normal Tuesday?"

   Map each daily activity to a skill. Uncovered activities = gaps.

3. **Check the Red Routes matrix:**

   | | Few users | All users |
   |---|-----------|-----------|
   | **Always** | Niche automation | **Red route — must have skill** |
   | **Often** | Power-user feature | Important daily operation |
   | **Rarely** | Edge case | Setup/migration (episodic) |

   Every cell in the top-right quadrant (high frequency, all users) needs a skill.

4. **Apply Big Hire / Little Hire (JTBD):**
   - Big hire = when users adopt the tool (setup, initial architecture)
   - Little hire = when users actually use it daily
   - "Real value is created in the little hire" — if your suite only covers big hires, it will be abandoned after setup

### Example: commandbase-vault

**Before Tuesday test** (8 skills): starting, researching, designing, structuring, planning, implementing, importing, auditing — all episodic.

**After Tuesday test** (+5 skills): capturing, reviewing, connecting, maintaining, linting — all habitual.

## README Structure

Every plugin needs a README.md with:

```markdown
# plugin-name

One-line description of what this plugin does and its workflow coverage.

## Dependencies

- dependency-plugin (what it provides)

## Skills (N)

| Skill | Description |
|-------|-------------|
| /skill-name | One-line description |

## Agents (N)          # If applicable

| Agent | Description |
|-------|-------------|
| agent-name | One-line description |

## Installation

\```shell
/plugin install plugin-name
\```
```

Add additional sections for architecture principles, companion skills, or setup instructions as needed.
