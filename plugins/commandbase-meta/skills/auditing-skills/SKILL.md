---
name: auditing-skills
description: "Use this skill when auditing existing skills for validation issues, updating skills to fix compliance problems, or checking skill health after pattern changes. This includes running validation checks against all skills, fixing frontmatter issues, correcting name format violations, rewriting descriptions to follow the WHEN formula, and adding missing enforcement pattern sections."
---

# Auditing Skills

You are systematically auditing and updating existing skills to ensure they follow validation rules and enforcement patterns. This skill activates when checking skill health or fixing compliance issues and produces audit reports or updated skill files.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO UPDATE WITHOUT SHOWING THE DIFF FIRST
```

Every change must be shown as a before/after diff and approved before applying. Batch updates are prohibited - one skill at a time.

**No exceptions:**
- Don't auto-fix without showing the proposed change
- Don't update multiple skills in one operation
- Don't skip user approval for any fix
- Don't assume the audit is correct - verify findings

## The Gate Function

```
BEFORE updating any skill:

1. IDENTIFY: Mode (audit vs update) and target (single skill or "all")
2. VERIFY: Target skill(s) exist in ~/.claude/skills/
3. READ: Full SKILL.md content (no offset/limit)
4. AUDIT: Run all 5 check categories
5. REPORT: Show findings with specific line references
6. If update mode: PROPOSE fixes one at a time with diffs
7. ONLY THEN: Apply approved changes

Skip verification = breaking a working skill
```

## Mode Detection

Parse the user's request to determine mode:

| Input | Mode | Target |
|-------|------|--------|
| `/auditing-skills audit skill-name` | Audit | Single skill |
| `/auditing-skills audit all` | Audit | All skills |
| `/auditing-skills update skill-name` | Update | Single skill |
| `/auditing-skills skill-name` | Audit | Single skill (default) |

**No batch update mode.** To update multiple skills, run update on each individually.

## Mode A: Audit

Read-only analysis of skill(s) against validation rules.

**Single Skill Audit:**
1. Read `~/.claude/skills/[skill-name]/SKILL.md` completely
2. Run all 5 audit categories (see Audit Categories below)
3. Produce audit report showing findings
4. No changes made

**All Skills Audit:**
1. List all directories in `~/.claude/skills/`
2. Run audit on each skill
3. Produce summary table:

```
SKILL AUDIT SUMMARY
===================
| Skill                  | Issues |
|------------------------|--------|
| committing-changes     | 0 ✓    |
| creating-skills        | 0 ✓    |
| debating-options       | 2 ⚠️   |
| ...                    | ...    |

Total: X skills, Y with issues
Run `/auditing-skills update [skill-name]` to fix specific skills.
```

## Mode B: Update

Interactive fix workflow for a single skill.

**Process:**
1. Run audit first (same as Mode A)
2. If no issues: "Skill passes all validation checks."
3. If issues found, for each issue:
   - Show the finding with line reference
   - Propose the fix
   - Show before/after diff
   - Ask for approval
   - Apply if approved, skip if declined
   - Re-validate after fix
4. Repeat until all issues resolved or user stops

**User approval is required for every change.** Never auto-apply.

## Audit Categories

Five categories, checked in order. See `./reference/audit-checklist.md` for full details.

### 1. Frontmatter Validation

From validation-rules.md:5-13:
- Starts with `---`, ends with `---`
- Valid YAML dictionary
- Only allowed properties: name, description, license, allowed-tools, metadata
- Required: name, description

### 2. Name Validation

From validation-rules.md:15-25:
- Matches `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Matches directory name
- Uses gerund form (verb-ing)

### 3. Description Validation

From validation-rules.md:27-37:
- Non-empty string
- Max 1024 characters
- No angle brackets
- Third person voice
- Starts with "Use this skill when..."
- Includes trigger keywords

### 4. Structure Validation

From validation-rules.md:39-47:
- SKILL.md exists at root
- Under 500 lines
- Reference nesting max 1 level
- No extraneous files (README, CHANGELOG)

### 5. Pattern Compliance

Enforcement pattern checks:
- Has Iron Law section
- Has Gate Function section
- Has Red Flags section
- Has Rationalization Prevention table
- Has Bottom Line section

## Audit Report Format

For each skill audited:

```
AUDIT: [skill-name]
==================

Frontmatter:
  ✓ Valid YAML
  ✓ Required fields present
  ⚠️ Missing `name` field

Name:
  ✓ Matches directory
  ⚠️ Not gerund form (current: "code-review", suggest: "reviewing-code")

Description:
  ✓ Under 1024 chars (current: 287)
  ⚠️ Doesn't start with "Use this skill when..."

Structure:
  ✓ SKILL.md exists
  ✓ Under 500 lines (current: 245)

Enforcement Pattern:
  ✓ Has Iron Law
  ⚠️ Missing Rationalization Prevention table

Summary: 3 issues found
```

## Common Fixes

See `./reference/common-fixes.md` for detailed fix patterns. Key fixes:

| Issue | Fix Approach |
|-------|--------------|
| Missing name field | Add `name: [directory-name]` to frontmatter |
| Name not gerund | Propose rename with migration steps |
| Description not WHEN-focused | Rewrite using formula from description-writing-guide.md |
| Missing enforcement sections | Add section from template, customize for skill |
| Over 500 lines | Suggest splitting to reference/ subdirectory |

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Applying a fix without showing the diff first
- Updating multiple skills in a single operation
- Proceeding after user declines a fix without asking what to do
- Assuming a finding is correct without checking the actual content
- Skipping re-validation after applying a fix

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This fix is obvious, no need to show diff" | Show every diff. User context matters. |
| "I'll batch these small fixes together" | One fix at a time. Each needs approval. |
| "The audit said it's wrong, so it's wrong" | Verify against actual content. Audits can have false positives. |
| "User approved the first fix, they'll approve the rest" | Each fix needs explicit approval. |
| "Re-validation is slow, I'll skip it" | Re-validate after every fix. Catches regressions. |

## The Bottom Line

**No update without showing the diff first.**

Audit thoroughly. Fix one at a time. Get approval for every change. Re-validate after every fix. This is non-negotiable. Every skill update. Every time.
