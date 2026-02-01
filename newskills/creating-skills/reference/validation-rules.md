# Validation Rules

Every skill must pass these checks before it can be considered complete. These rules are derived from the official Claude Code skill specification.

## Frontmatter Requirements

- File must start with `---` on the first line
- Frontmatter must end with `---` on its own line
- Content between delimiters must be valid YAML
- YAML must parse as a dictionary (not a list or scalar)
- Allowed properties: `name`, `description`, `license`, `allowed-tools`, `metadata`
- Any other property will cause validation failure
- Required properties: `name` and `description`

## Name Rules

| Rule | Detail |
|------|--------|
| Format | `^[a-z0-9-]+$` (lowercase alphanumeric and hyphens only) |
| No leading hyphen | Name cannot start with `-` |
| No trailing hyphen | Name cannot end with `-` |
| No consecutive hyphens | `--` is not allowed anywhere in the name |
| Max length | 64 characters |
| Directory match | Name must exactly match the skill's directory name |
| Convention | Gerund form recommended (see ../reference/naming-conventions.md) |

## Description Rules

| Rule | Detail |
|------|--------|
| Required | Must be present and non-empty after stripping whitespace |
| Type | Must be a string |
| Max length | 1024 characters |
| No angle brackets | `<` and `>` are forbidden anywhere in the description |
| Voice | Third person ("Use this skill when...") not first person ("I help you...") |
| Trigger keywords | Must include words that match user intent for activation |
| Formula | Start with "Use this skill when [situation]. This includes [use cases]..." |

## Structure Rules

- `SKILL.md` must exist at the root of the skill directory
- `SKILL.md` is the only required file
- SKILL.md body: under 500 lines, under 5,000 words
- Reference file nesting: maximum 1 level deep from SKILL.md
- Allowed subdirectories: `reference/`, `templates/`, `scripts/`, `assets/`
- No extraneous files: no `README.md`, `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, `QUICK_REFERENCE.md`
- Only include files the AI agent needs to do the job

## Progressive Disclosure Levels

| Level | When Loaded | Budget | Contains |
|-------|-------------|--------|----------|
| Metadata | Always in context | ~100 words | `name` + `description` from frontmatter |
| Body | When skill triggers | <500 lines, <5k words | Instructions, workflow, rules |
| Resources | On demand by Claude | No hard limit | reference/, templates/, scripts/, assets/ |

The description is loaded at Level 1 and is the primary triggering mechanism. All "when to use" guidance must be in the description, not buried in the body.

## Validation Checklist

Run through every item before declaring a skill complete:

### Frontmatter
- [ ] Starts with `---`, ends with `---`
- [ ] Valid YAML dictionary
- [ ] Only allowed properties present
- [ ] `name` field present, non-empty string
- [ ] `description` field present, non-empty string

### Name
- [ ] Matches `^[a-z0-9-]+$`
- [ ] No leading/trailing hyphens
- [ ] No consecutive hyphens
- [ ] 64 characters or fewer
- [ ] Matches directory name exactly
- [ ] Uses gerund form (verb-ing)

### Description
- [ ] 1024 characters or fewer
- [ ] No angle brackets (`<` or `>`)
- [ ] Third person voice
- [ ] Includes trigger keywords
- [ ] Starts with "Use this skill when..."
- [ ] Describes WHEN to activate, not just WHAT it does

### Structure
- [ ] SKILL.md exists at directory root
- [ ] SKILL.md under 500 lines
- [ ] Reference nesting max 1 level deep
- [ ] No extraneous files (README, CHANGELOG, etc.)
- [ ] File names are intention-revealing

### Content Quality
- [ ] No TODO comments or placeholder text
- [ ] No content copied verbatim from other sources
- [ ] Examples are concrete and actionable
- [ ] Instructions are specific to the task, not generic advice
