# Research: learning-from-sessions Skill

## Overview

The `learning-from-sessions` skill (`~/.claude/skills/learning-from-sessions/SKILL.md`) extracts reusable knowledge from work sessions, converting discoveries and workarounds into skill files or documentation.

**Trigger phrases**: `/learn`, `save this as a skill`, `what did we learn`, `extract knowledge`

## Purpose

Capture session learnings:
- Reviewing what was learned during debugging
- Saving non-obvious discoveries as skill files
- Extracting knowledge after trial-and-error investigation
- Converting workarounds into documented patterns

## Process

### Step 1: Review Session
Analyze the conversation to identify:
- Problems solved
- Non-obvious discoveries
- Workarounds developed
- Patterns established

### Step 2: Categorize Learnings
Determine the type of knowledge:
- **Skill-worthy**: Complex enough to warrant a skill file
- **Pattern**: Reusable approach to document
- **Gotcha**: Non-obvious behavior to remember
- **Reference**: Useful information for future sessions

### Step 3: Extract Core Knowledge
For each learning:
- What was the problem?
- What was the solution?
- Why did it work?
- When to apply it?

### Step 4: Choose Output Format
Based on categorization:
- **Skill file**: Create in `~/.claude/skills/`
- **CLAUDE.md update**: Add to automatic behaviors
- **Documentation**: Write to `.docs/`

### Step 5: Present Findings
```
SESSION LEARNINGS
=================

Identified:
1. [Learning 1] - [Category]
2. [Learning 2] - [Category]

Recommendations:
- Save [learning 1] as skill: /creating-skills
- Add [learning 2] to CLAUDE.md: /updating-claude-md
- Document [learning 3] in .docs/

Which would you like to save?
```

## Output Formats

### For Skills
Invoke `/creating-skills` with the extracted knowledge.

### For CLAUDE.md
```markdown
## Automatic Behaviors

When [trigger condition], [specific action to take].
```

### For Documentation
Write to `.docs/research/` or `.docs/learnings/`.

## Integration Points

- Called after `/debugging-codebases` resolves
- Can invoke `/creating-skills` for skill generation
- Can invoke `/updating-claude-md` for pattern recording

## File Reference

- Main: `~/.claude/skills/learning-from-sessions/SKILL.md`
