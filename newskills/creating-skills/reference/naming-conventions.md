# Naming Conventions

Skill names are identifiers, not marketing. They must be precise, scannable, and consistent with the convention used across all skills.

## The Gerund Rule

Skills use verb-ing form because the name describes the **action** the skill performs, not the thing it is.

**Good (gerund - describes the action):**
- `creating-skills` - the act of creating skills
- `processing-pdfs` - the act of processing PDFs
- `deploying-lambdas` - the act of deploying Lambda functions
- `reviewing-code` - the act of reviewing code

**Bad (noun - describes the thing):**
- `skill-creator` - names the tool, not the action
- `pdf-processor` - sounds like a standalone utility
- `lambda-deployer` - agent-style naming, not skill-style
- `code-review` - ambiguous (is it a noun or a verb?)

**Why gerund form?** Skills activate when Claude recognizes the user is performing an action. Gerund names align with that mental model: the user is "creating skills", so the `creating-skills` skill activates. Noun names describe a tool that exists, not an action being performed.

## Format Rules

| Rule | Specification |
|------|--------------|
| Allowed characters | `^[a-z0-9-]+$` (lowercase letters, digits, hyphens) |
| No uppercase | `Creating-Skills` is invalid |
| No underscores | `creating_skills` is invalid |
| No spaces | `creating skills` is invalid |
| No leading hyphen | `-creating-skills` is invalid |
| No trailing hyphen | `creating-skills-` is invalid |
| No consecutive hyphens | `creating--skills` is invalid |
| Max length | 64 characters |
| Practical sweet spot | 15-40 characters |

## Directory Match

The `name` field in frontmatter must exactly match the directory name:

```
newskills/creating-skills/SKILL.md
         ^^^^^^^^^^^^^^^^^
         This must match the `name: creating-skills` in frontmatter
```

If they don't match, the skill will fail validation.

## File Naming Within a Skill

| File/Directory | Convention |
|----------------|-----------|
| `SKILL.md` | Always uppercase, always this exact name |
| Reference files | Lowercase, kebab-case, intention-revealing |
| Subdirectories | Lowercase: `reference/`, `templates/`, `scripts/`, `assets/` |

**Good reference file names:**
- `validation-rules.md` - says what's inside
- `description-writing-guide.md` - says what it teaches
- `converting-subagents.md` - says what process it covers

**Bad reference file names:**
- `reference.md` - too generic, says nothing
- `helpers.md` - vague, could contain anything
- `utils.md` - not intention-revealing
- `notes.md` - not actionable

## Directory Locations

Skills can live in two places:

| Location | Scope | Loaded When |
|----------|-------|-------------|
| `~/.claude/skills/skill-name/` | Personal (all projects) | Every Claude Code session |
| `.claude/skills/skill-name/` | Project (this repo only) | Sessions in this repo |

Personal skills should be general-purpose. Project skills should be repo-specific.

## Examples

| Name | Purpose | Characters |
|------|---------|-----------|
| `creating-skills` | Building Claude Code skills | 15 |
| `processing-pdfs` | Extracting and converting PDFs | 15 |
| `deploying-lambdas` | AWS Lambda deployment workflows | 18 |
| `reviewing-code` | Code review with quality gates | 14 |
| `managing-migrations` | Database migration workflows | 20 |
| `writing-tests` | Test creation and coverage analysis | 13 |
| `configuring-ci` | CI/CD pipeline setup | 14 |
| `analyzing-logs` | Log analysis and debugging | 14 |
| `handling-auth` | Authentication flow implementation | 13 |
| `generating-docs` | Documentation generation | 15 |
