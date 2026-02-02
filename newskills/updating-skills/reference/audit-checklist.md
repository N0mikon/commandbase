# Audit Checklist

Complete checklist for skill validation. Each item maps to the official validation rules at `~/.claude/skills/creating-skills/reference/validation-rules.md`.

## 1. Frontmatter Checks

| Check | Rule Source | Pass Condition |
|-------|-------------|----------------|
| Opens with delimiter | validation-rules.md:7 | First line is exactly `---` |
| Closes with delimiter | validation-rules.md:8 | Frontmatter ends with `---` on own line |
| Valid YAML | validation-rules.md:9 | Content parses as YAML without errors |
| Is dictionary | validation-rules.md:10 | Parsed YAML is object, not array or scalar |
| Allowed properties only | validation-rules.md:11 | Only: name, description, license, allowed-tools, metadata |
| Has name | validation-rules.md:13 | `name` field present and non-empty |
| Has description | validation-rules.md:13 | `description` field present and non-empty |

## 2. Name Checks

| Check | Rule Source | Pass Condition |
|-------|-------------|----------------|
| Valid format | validation-rules.md:19 | Matches `^[a-z0-9-]+$` |
| No leading hyphen | validation-rules.md:20 | Does not start with `-` |
| No trailing hyphen | validation-rules.md:21 | Does not end with `-` |
| No consecutive hyphens | validation-rules.md:22 | Does not contain `--` |
| Length limit | validation-rules.md:23 | 64 characters or fewer |
| Matches directory | validation-rules.md:24 | Name equals directory name exactly |
| Gerund form | validation-rules.md:25 | Uses verb-ing pattern |

**Gerund detection heuristic:** Name should end in `-ing` suffix on the verb component. Examples:
- `committing-changes` ✓ (committing)
- `creating-skills` ✓ (creating)
- `code-review` ✗ (should be reviewing-code)
- `skill-validator` ✗ (should be validating-skills)

## 3. Description Checks

| Check | Rule Source | Pass Condition |
|-------|-------------|----------------|
| Non-empty | validation-rules.md:31 | After trim, length > 0 |
| Is string | validation-rules.md:32 | Type is string |
| Length limit | validation-rules.md:33 | 1024 characters or fewer |
| No angle brackets | validation-rules.md:34 | Does not contain `<` or `>` |
| Third person | validation-rules.md:35 | No "I help", "I am", "This agent" |
| WHEN formula | validation-rules.md:37 | Starts with "Use this skill when" |
| Has trigger keywords | validation-rules.md:36 | Contains action verbs matching skill purpose |

**Third person detection:** Flag if description contains:
- "I help"
- "I am"
- "I will"
- "This agent"
- "My purpose"

## 4. Structure Checks

| Check | Rule Source | Pass Condition |
|-------|-------------|----------------|
| SKILL.md exists | validation-rules.md:41 | File at `[skill-dir]/SKILL.md` |
| Line count | validation-rules.md:43 | Under 500 lines |
| Nesting depth | validation-rules.md:44 | Reference files max 1 level deep |
| No README | validation-rules.md:46 | No `README.md` in skill directory |
| No CHANGELOG | validation-rules.md:46 | No `CHANGELOG.md` in skill directory |
| Allowed subdirs only | validation-rules.md:45 | Only: reference/, templates/, scripts/, assets/ |

## 5. Pattern Compliance Checks

These are not in the official spec but are commandbase conventions for enforcement patterns.

| Check | Detection Method | Pass Condition |
|-------|------------------|----------------|
| Has Iron Law | Heading search | Contains `## The Iron Law` |
| Has Gate Function | Heading search | Contains `## The Gate Function` |
| Has Red Flags | Heading search | Contains `## Red Flags` |
| Has Rationalization Prevention | Heading + table | Contains `## Rationalization Prevention` and has `\| Excuse \|` |
| Has Bottom Line | Heading search | Contains `## The Bottom Line` |

**Note:** Pattern compliance is a convention, not a hard requirement. Skills can pass validation without enforcement patterns, but they are recommended for consistency.

## Severity Levels

| Severity | Meaning | Examples |
|----------|---------|----------|
| ERROR | Skill will fail to load | Invalid YAML, missing required fields |
| WARNING | Skill loads but doesn't follow conventions | Missing gerund form, no enforcement pattern |
| INFO | Minor improvement suggested | Description could be more specific |

Audit reports should clearly distinguish severity levels.
