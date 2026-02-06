# Agent Naming Conventions

Agent names are identifiers that describe a specialist role. They must be precise, scannable, and distinct from skill naming conventions.

## The Noun Rule

Agents use noun/role form because the name describes **what the agent is**, not an action being performed.

**Good (noun - describes the specialist):**
- `codebase-analyzer` - a specialist that analyzes codebases
- `docs-locator` - a specialist that locates documents
- `web-search-researcher` - a specialist that researches via web search
- `log-parser` - a specialist that parses logs

**Bad (gerund - describes the action):**
- `analyzing-codebases` - skill-style naming, not agent-style
- `locating-docs` - describes an activity, not a role
- `researching-web` - this is a skill name (and is one)
- `parsing-logs` - sounds like a skill invocation

**Why noun form?** Agents are specialists invoked explicitly via the Task tool. The parent orchestrator delegates work to them by name, like assigning tasks to team members. You send work to "the analyzer", not to "analyzing". Noun names reinforce that agents are **roles** you delegate to, while gerund names (used by skills) describe **actions** a user is performing.

## How Agents Differ from Skills

| Aspect | Agent (Noun) | Skill (Gerund) |
|--------|-------------|----------------|
| **Name** | `codebase-analyzer` | `researching-codebases` |
| **Describes** | What it IS (a role) | What the user is DOING (an action) |
| **Activation** | Explicit: Task tool invocation | Implicit: description match against user intent |
| **Structure** | Single `.md` file | Directory with `SKILL.md` + supporting files |
| **Mental model** | "Delegate this to the analyzer" | "The user is researching codebases" |

If you're unsure whether something should be a skill or an agent, the naming test helps: does it sound natural as "send this to the {name}" (agent) or "the user is {name}-ing" (skill)?

## Naming Patterns

Agents in this codebase follow one of two structural patterns:

### Pattern 1: `{domain}-{role}`

The domain scopes what the agent works with. The role describes what it does.

| Name | Domain | Role |
|------|--------|------|
| `codebase-analyzer` | codebase | analyzer |
| `codebase-locator` | codebase | locator |
| `docs-analyzer` | docs | analyzer |
| `docs-locator` | docs | locator |
| `docs-updater` | docs | updater |

This pattern creates natural **agent families** - groups of agents sharing a domain but performing different roles. The `codebase-*` family and `docs-*` family each have consistent, predictable names.

### Pattern 2: `{domain}-{qualifier}-{role}`

When a domain has multiple agents with similar roles, add a qualifier to differentiate.

| Name | Domain | Qualifier | Role |
|------|--------|-----------|------|
| `codebase-pattern-finder` | codebase | pattern | finder |
| `web-search-researcher` | web-search | - | researcher |

Use qualifiers sparingly. If the role alone is unambiguous within the domain, don't add one.

## Format Rules

| Rule | Specification |
|------|--------------|
| Allowed characters | `^[a-z0-9-]+$` (lowercase letters, digits, hyphens) |
| No uppercase | `Codebase-Analyzer` is invalid |
| No underscores | `codebase_analyzer` is invalid |
| No spaces | `codebase analyzer` is invalid |
| No leading hyphen | `-codebase-analyzer` is invalid |
| No trailing hyphen | `codebase-analyzer-` is invalid |
| No consecutive hyphens | `codebase--analyzer` is invalid |
| Max length | 64 characters |
| Practical sweet spot | 15-30 characters |

## Filename Match

The `name` field in frontmatter must exactly match the filename (minus `.md`):

```
newagents/codebase-analyzer.md
          ^^^^^^^^^^^^^^^^^
          Must match `name: codebase-analyzer` in frontmatter
```

If they don't match, agent discovery may fail.

## Role Suffixes

Common role suffixes that describe what the agent does:

| Suffix | Meaning | Example |
|--------|---------|---------|
| `-analyzer` | Reads and explains implementation details | `codebase-analyzer` |
| `-locator` | Finds files, components, or documents | `docs-locator` |
| `-finder` | Searches for patterns, examples, or matches | `codebase-pattern-finder` |
| `-updater` | Modifies content to keep it current | `docs-updater` |
| `-researcher` | Gathers information from external sources | `web-search-researcher` |
| `-validator` | Checks correctness against criteria | `schema-validator` |
| `-builder` | Constructs or generates artifacts | `config-builder` |
| `-reviewer` | Evaluates quality or correctness | `code-reviewer` |

Pick the suffix that most accurately describes the agent's primary responsibility. Avoid vague suffixes like `-helper`, `-handler`, or `-manager`.

## Description Field

The `description` field in agent frontmatter is critical for delegation. It tells the parent orchestrator **when to use this agent**.

**Good descriptions** answer: "Call this agent when you need to..."

```yaml
# Clear delegation trigger
description: Analyzes codebase implementation details. Call the codebase-analyzer
  agent when you need to find detailed information about specific components.

# Specific scope
description: Finds relevant documents across .docs/ directory (plans, research,
  handoffs). Use when you need to discover what documentation exists about a topic.
```

**Bad descriptions** are vague or miss the delegation trigger:

```yaml
# Too vague - when would you call this?
description: Helps with code stuff.

# Missing trigger - describes capability but not when to delegate
description: Can read files and search for patterns in codebases.
```

## Choosing a Name

### Step 1: Identify the domain

What does the agent work with? Files? Docs? APIs? A specific codebase area?

### Step 2: Identify the role

What does the agent do with that domain? Analyze? Locate? Build? Review?

### Step 3: Compose the name

`{domain}-{role}` or `{domain}-{qualifier}-{role}` if disambiguation is needed.

### Step 4: Check against existing agents

Does it fit an existing family? If you already have `codebase-analyzer` and `codebase-locator`, a new codebase agent should follow the `codebase-{role}` pattern.

## Agent-to-Skill Name Conversion

When an agent capability should become a skill (or vice versa), flip the grammatical form:

| Agent (Noun) | Skill (Gerund) |
|-------------|----------------|
| `code-reviewer` | `reviewing-code` |
| `test-runner` | `running-tests` |
| `doc-generator` | `generating-docs` |
| `bug-triager` | `triaging-bugs` |
| `deploy-manager` | `managing-deployments` |
| `codebase-analyzer` | `analyzing-codebases` |

The conversion flips subject and action: agent names put the domain first and role second (`code-reviewer`), while skill names put the action first and target second (`reviewing-code`).

## Examples

| Name | Domain | Role | Characters |
|------|--------|------|-----------|
| `codebase-analyzer` | codebase | analyzer | 18 |
| `codebase-locator` | codebase | locator | 17 |
| `codebase-pattern-finder` | codebase | pattern-finder | 24 |
| `docs-analyzer` | docs | analyzer | 13 |
| `docs-locator` | docs | locator | 12 |
| `docs-updater` | docs | updater | 12 |
| `web-search-researcher` | web-search | researcher | 22 |
| `api-validator` | api | validator | 13 |
| `schema-builder` | schema | builder | 14 |
| `test-runner` | test | runner | 11 |
| `config-reviewer` | config | reviewer | 15 |
| `migration-builder` | migration | builder | 17 |
