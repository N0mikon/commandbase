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
- `researching-web` - this is a skill name
- `parsing-logs` - sounds like a skill invocation

**Why noun form?** Agents are specialists invoked explicitly via the Task tool. The parent orchestrator delegates work to them by name, like assigning tasks to team members. You send work to "the analyzer", not to "analyzing". Noun names reinforce that agents are **roles** you delegate to, while gerund names (used by skills) describe **actions** a user is performing.

## Naming Patterns

### Pattern 1: `{domain}-{role}`

The domain scopes what the agent works with. The role describes what it does.

| Name | Domain | Role |
|------|--------|------|
| `codebase-analyzer` | codebase | analyzer |
| `codebase-locator` | codebase | locator |
| `docs-analyzer` | docs | analyzer |
| `docs-locator` | docs | locator |
| `docs-updater` | docs | updater |

This pattern creates natural **agent families** - groups of agents sharing a domain but performing different roles.

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
~/.claude/agents/codebase-analyzer.md
                 ^^^^^^^^^^^^^^^^^
                 Must match `name: codebase-analyzer` in frontmatter
```

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

Avoid vague suffixes like `-helper`, `-handler`, or `-manager`.

## Agent Families

When building multiple agents in the same domain, use consistent naming:

```
codebase-analyzer        # Deep analysis of implementation
codebase-locator         # Find files and components
codebase-pattern-finder  # Find similar patterns and examples
```

A new codebase agent should follow the `codebase-{role}` pattern, not invent its own prefix.

## Agent-to-Skill Name Conversion

When converting between agent and skill names, flip the grammatical form:

| Agent (Noun) | Skill (Gerund) |
|-------------|----------------|
| `code-reviewer` | `reviewing-code` |
| `test-runner` | `running-tests` |
| `codebase-analyzer` | `analyzing-codebases` |
| `docs-updater` | `updating-docs` |

The conversion flips subject and action: agent names put the domain first and role second, while skill names put the action first and target second.

## Choosing a Name

1. **Identify the domain**: What does the agent work with? Files? Docs? APIs? A specific codebase area?
2. **Identify the role**: What does the agent do? Analyze? Locate? Build? Review?
3. **Compose the name**: `{domain}-{role}` or `{domain}-{qualifier}-{role}` if disambiguation is needed.
4. **Check against existing agents**: Does it fit an existing family? If you already have `codebase-analyzer` and `codebase-locator`, a new codebase agent should follow the `codebase-{role}` pattern.
