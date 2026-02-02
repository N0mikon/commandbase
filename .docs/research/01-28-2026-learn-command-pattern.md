---
git_commit: 22359f4
last_updated: 2026-01-28
last_updated_by: rcode
topic: "/learn Command - Mid-Session Pattern Extraction"
tags: [research, learn, patterns, skills]
status: complete
references:
  - C:/code/everything-claude-code/commands/learn.md
  - C:/code/everything-claude-code/skills/continuous-learning/SKILL.md
  - C:/code/everything-claude-code/skills/continuous-learning-v2/SKILL.md
---

# Research: /learn Command Pattern

**Date**: 2026-01-28
**Source**: everything-claude-code

## Summary

The `/learn` command captures reusable patterns mid-session when a non-trivial problem is solved. It's documentation-only (no executable script) - Claude interprets and follows instructions to extract patterns and save them as skill files.

## How It Works

### Trigger
User manually runs `/learn` during a session after solving a non-trivial problem (`commands/learn.md:7`).

### What Gets Extracted (`commands/learn.md:11-32`)

| Pattern Type | Examples |
|--------------|----------|
| **Error Resolution** | Root cause, what fixed it, reusable for similar errors |
| **Debugging Techniques** | Non-obvious steps, tool combinations |
| **Workarounds** | Library quirks, API limitations, version-specific fixes |
| **Project-Specific** | Codebase conventions, architecture decisions |

### What Gets Excluded (`commands/learn.md:66-70`)
- Trivial fixes (typos, simple syntax errors)
- One-time issues (specific API outages)

### Output Format (`commands/learn.md:36-55`)

Saves to `~/.claude/skills/learned/[pattern-name].md`:

```markdown
# [Descriptive Pattern Name]

**Extracted:** [Date]
**Context:** [Brief description of when this applies]

## Problem
[What problem this solves - be specific]

## Solution
[The pattern/technique/workaround]

## Example
[Code example if applicable]

## When to Use
[Trigger conditions - what should activate this skill]
```

### Process Flow (`commands/learn.md:58-64`)

1. Claude reviews session for extractable patterns
2. Identifies most valuable/reusable insight
3. Drafts skill file
4. Asks user to confirm before saving
5. Saves to `~/.claude/skills/learned/`

## Comparison: /learn vs /handover

| Aspect | /learn | /handover |
|--------|--------|-----------|
| **Timing** | Mid-session | End of session |
| **Focus** | Reusable patterns | Session context |
| **Output** | Skill files | Handoff documents |
| **Scope** | Atomic (one pattern) | Comprehensive (full state) |
| **Reuse** | Auto-loaded in future sessions | Manual /takeover |

## Adaptation for Commandbase

### Option A: Separate /learn Command
Create `newskills/learn/SKILL.md` that saves to `.docs/learnings/MM-DD-YYYY-pattern-name.md`

### Option B: Enhance /handover
Add "Key Learnings" section to handover that extracts patterns in skill format

### Option C: Both
- `/learn` for immediate pattern capture (saves globally)
- `/handover` includes learnings in handoff doc (project-specific)

## Key Implementation Details

- No executable script - Claude interprets markdown instructions
- User confirmation required before saving
- One pattern per skill file (focused)
- Storage: `~/.claude/skills/learned/` (auto-loaded by Claude Code)

## Code References

- Command definition: `C:/code/everything-claude-code/commands/learn.md:1-71`
- Output format: `commands/learn.md:36-55`
- Process flow: `commands/learn.md:58-64`
- Filtering rules: `commands/learn.md:66-70`
