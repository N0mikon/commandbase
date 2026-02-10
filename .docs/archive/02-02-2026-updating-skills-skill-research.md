---
date: 2026-02-02
status: archived
topic: updating-skills skill research
tags: [skills, auditing, validation, meta]
git_commit: 8e92bba
archived: 2026-02-09
archive_reason: "Skill renamed from updating-skills to auditing-skills and moved to plugins/commandbase-meta/skills/auditing-skills/. All file paths and invocation references are stale. The SKILL.md itself supersedes this research document."
references:
  - plugins/commandbase-meta/skills/auditing-skills/SKILL.md
---

# Research: updating-skills Skill

## Overview

The `updating-skills` skill (`~/.claude/skills/updating-skills/SKILL.md`) audits existing skills for validation issues and fixes compliance problems. It operates in two modes: Audit (read-only) and Update (interactive fixes).

**Invocation**: `/updating-skills audit [skill-name]`, `/updating-skills update [skill-name]`

## The Iron Law

```
NO UPDATE WITHOUT SHOWING THE DIFF FIRST
```

Every change must be shown as before/after diff and approved before applying. Batch updates are prohibited - one skill at a time.

## The Gate Function

Before updating any skill:

1. **IDENTIFY**: Mode (audit vs update) and target (single skill or "all")
2. **VERIFY**: Target skill(s) exist in ~/.claude/skills/
3. **READ**: Full SKILL.md content (no offset/limit)
4. **AUDIT**: Run all 5 check categories
5. **REPORT**: Show findings with specific line references
6. **If update mode**: PROPOSE fixes one at a time with diffs
7. **ONLY THEN**: Apply approved changes

## Mode Detection

| Input | Mode | Target |
|-------|------|--------|
| `/updating-skills audit skill-name` | Audit | Single skill |
| `/updating-skills audit all` | Audit | All skills |
| `/updating-skills update skill-name` | Update | Single skill |
| `/updating-skills skill-name` | Audit | Single skill (default) |

**No batch update mode.** To update multiple skills, run update on each individually.

## Audit Categories

### 1. Frontmatter Validation
- Starts/ends with `---`
- Valid YAML dictionary
- Only allowed properties: name, description, license, allowed-tools, metadata
- Required: name, description

### 2. Name Validation
- Matches `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Matches directory name
- Uses gerund form (verb-ing)

### 3. Description Validation
- Non-empty string
- Max 1024 characters
- No angle brackets
- Third person voice
- Starts with "Use this skill when..."

### 4. Structure Validation
- SKILL.md exists at root
- Under 500 lines
- Reference nesting max 1 level
- No extraneous files

### 5. Pattern Compliance
- Has Iron Law section
- Has Gate Function section
- Has Red Flags section
- Has Rationalization Prevention table
- Has Bottom Line section

## Audit Report Format

```
AUDIT: [skill-name]
==================

Frontmatter:
  ✓ Valid YAML
  ⚠️ Missing `name` field

Name:
  ✓ Matches directory
  ⚠️ Not gerund form (suggest: "reviewing-code")

Description:
  ✓ Under 1024 chars
  ⚠️ Doesn't start with "Use this skill when..."

Structure:
  ✓ SKILL.md exists
  ✓ Under 500 lines

Enforcement Pattern:
  ✓ Has Iron Law
  ⚠️ Missing Rationalization Prevention table

Summary: 3 issues found
```

## Update Mode Process

1. Run audit first
2. If no issues: "Skill passes all validation checks."
3. If issues found, for each issue:
   - Show the finding with line reference
   - Propose the fix
   - Show before/after diff
   - Ask for approval
   - Apply if approved, skip if declined
   - Re-validate after fix
4. Repeat until all issues resolved or user stops

**User approval is required for every change.**

## Common Fixes

| Issue | Fix Approach |
|-------|--------------|
| Missing name field | Add `name: [directory-name]` to frontmatter |
| Name not gerund | Propose rename with migration steps |
| Description not WHEN-focused | Rewrite using formula |
| Missing enforcement sections | Add section from template |
| Over 500 lines | Suggest splitting to reference/ |

## File References

- Main: `~/.claude/skills/updating-skills/SKILL.md`
- Audit checklist: `~/.claude/skills/updating-skills/reference/audit-checklist.md`
- Common fixes: `~/.claude/skills/updating-skills/reference/common-fixes.md`
