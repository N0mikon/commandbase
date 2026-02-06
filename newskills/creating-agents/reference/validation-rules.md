# Validation Rules

Every agent must pass these checks before it can be considered complete. These rules are derived from the official Claude Code agent specification.

## Frontmatter Requirements

- File must start with `---` on the first line
- Frontmatter must end with `---` on its own line
- Content between delimiters must be valid YAML
- YAML must parse as a dictionary (not a list or scalar)
- Required properties: `name` and `description`
- Optional properties: `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `hooks`, `memory`
- Unknown properties are ignored but may indicate a typo

## Name Rules

| Rule | Detail |
|------|--------|
| Format | `^[a-z0-9-]+$` (lowercase alphanumeric and hyphens only) |
| No leading hyphen | Name cannot start with `-` |
| No trailing hyphen | Name cannot end with `-` |
| No consecutive hyphens | `--` is not allowed anywhere in the name |
| Max length | 64 characters |
| Filename match | Name must match the filename minus `.md` extension |
| Convention | Noun/role form recommended (see ./naming-conventions.md) |

## Description Rules

| Rule | Detail |
|------|--------|
| Required | Must be present and non-empty after stripping whitespace |
| Type | Must be a string |
| Max length | 1024 characters |
| No angle brackets | `<` and `>` are forbidden anywhere in the description |
| Voice | Describes capability and delegation trigger, not first person |
| Delegation trigger | Must clearly express when the orchestrator should delegate to this agent |

## Tool Set Rules

| Rule | Detail |
|------|--------|
| `tools` field | Array of tool names the agent can access. If omitted, inherits all parent tools |
| `disallowedTools` field | Array of tools to deny. Removed from inherited set |
| Mutual exclusivity | Don't use both `tools` and `disallowedTools` on the same agent |
| Minimal set | Only include tools the agent actually needs for its workflow |
| State-modifying tools | Edit, Write, Bash, NotebookEdit require explicit justification and guardrails in the system prompt |

## Model Rules

| Rule | Detail |
|------|--------|
| Valid values | `sonnet`, `opus`, `haiku`, `inherit` |
| Default | `inherit` (uses parent's model) |
| Guideline | `haiku` for fast/simple, `sonnet` for standard, `opus` for complex reasoning or state modification |

## Permission Mode Rules

| Rule | Detail |
|------|--------|
| Valid values | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| Default | `default` (user prompted for risky actions) |
| Security | `bypassPermissions` should only be used for trusted, well-tested agents |

## Structure Rules

- Agent is a single `.md` file (not a directory)
- File lives in `~/.claude/agents/` (personal) or `.claude/agents/` (project)
- System prompt is the body content after the frontmatter
- Keep total file under 300 lines (target: 80-200 lines)
- No supporting files - all content must be in the single `.md` file

## Validation Checklist

Run through every item before declaring an agent complete:

### Frontmatter
- [ ] Starts with `---`, ends with `---`
- [ ] Valid YAML dictionary
- [ ] `name` field present, non-empty string
- [ ] `description` field present, non-empty string
- [ ] No unrecognized field names (check for typos)

### Name
- [ ] Matches `^[a-z0-9-]+$`
- [ ] No leading/trailing hyphens
- [ ] No consecutive hyphens
- [ ] 64 characters or fewer
- [ ] Matches filename (minus `.md`)
- [ ] Uses noun/role form (not gerund)

### Description
- [ ] 1024 characters or fewer
- [ ] No angle brackets (`<` or `>`)
- [ ] Not first person voice
- [ ] Includes delegation trigger (when to call this agent)
- [ ] Distinguishable from other agents' descriptions

### Tools
- [ ] `tools` or `disallowedTools` specified (not relying on inherit-all)
- [ ] Every listed tool is needed by the workflow
- [ ] State-modifying tools have guardrails in the system prompt
- [ ] No overlap between `tools` and `disallowedTools`

### Model
- [ ] Model matches task complexity (haiku/sonnet/opus)
- [ ] If omitted, `inherit` is appropriate for this agent

### System Prompt
- [ ] Uses Contract Format or clear equivalent structure
- [ ] Role/identity stated in first paragraph
- [ ] Core responsibilities defined (2-4 clear jobs)
- [ ] Output format specified or exemplified
- [ ] Enforcement patterns present (What NOT to Do, guidelines, or equivalent)
- [ ] No placeholder text or TODOs
- [ ] No first-person voice in identity framing ("You are...", not "I am...")
