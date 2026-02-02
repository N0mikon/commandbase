# Plan: updating-skills Skill

## Overview

Create a skill for systematically updating existing skills when patterns change or validation rules are violated. Two modes: Audit (read-only check) and Update (fix single skill). No batch operations.

## Context

**Research:** `.docs/research/02-02-2026-reviewing-and-updating-skills-research.md`

**Evidence of Need:**
- Wave 1: Added enforcement patterns to 9 skills
- Wave 2: Renamed 6 skills to gerund form
- Wave 3: Added progressive disclosure to 9 skills
- Each wave required systematic changes across multiple skills

**Validation Rules Source:**
- `~/.claude/skills/creating-skills/reference/validation-rules.md`

## What We're NOT Doing

- No batch updates (one skill at a time)
- No auto-fixing (always show diff, get approval)
- No creating new skills (that's `/creating-skills`)
- No skill deletion or archiving

---

## Phase 1: Define Audit Scope

### Goal
Establish what the audit checks and reports.

### Tasks
- [ ] Define audit categories
- [ ] Map to validation-rules.md
- [ ] Create audit report format

### Audit Categories

**1. Frontmatter Validation**
From `validation-rules.md:5-13`:
- Starts/ends with `---`
- Valid YAML dictionary
- Only allowed properties (name, description, license, allowed-tools, metadata)
- Required: name, description

**2. Name Validation**
From `validation-rules.md:15-25`:
- Matches `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Matches directory name
- Uses gerund form (verb-ing)

**3. Description Validation**
From `validation-rules.md:27-37`:
- Non-empty string
- Max 1024 characters
- No angle brackets
- Third person voice
- Starts with "Use this skill when..."
- Includes trigger keywords

**4. Structure Validation**
From `validation-rules.md:39-47`:
- SKILL.md exists at root
- Under 500 lines
- Reference nesting max 1 level
- No extraneous files (README, CHANGELOG)

**5. Pattern Compliance**
From enforcement pattern template:
- Has Iron Law section
- Has Gate Function section
- Has Red Flags section
- Has Rationalization Prevention table
- Has Bottom Line section

### Audit Report Format

```markdown
## Audit: [skill-name]

### Frontmatter
- ✓ Valid YAML
- ⚠️ Missing `name` field

### Name
- ✓ Matches directory
- ⚠️ Not gerund form (suggest: "creating-widgets")

### Description
- ✓ Under 1024 chars
- ⚠️ Doesn't start with "Use this skill when..."

### Structure
- ✓ SKILL.md exists
- ✓ Under 500 lines

### Enforcement Pattern
- ✓ Has Iron Law
- ⚠️ Missing Rationalization Prevention table

### Summary
3 issues found. Run `/updating-skills update [skill-name]` to fix.
```

### Success Criteria
- [ ] All 5 audit categories defined
- [ ] Maps to validation-rules.md line references
- [ ] Report format shows what to fix

---

## Phase 2: Design Two Modes

### Goal
Define Audit mode and Update mode workflows.

### Tasks
- [ ] Define Audit mode (read-only)
- [ ] Define Update mode (interactive fixes)
- [ ] Define mode detection logic

### Mode A: Audit

**Trigger:** `/updating-skills audit [skill-name]` or `/updating-skills audit all`

**Process:**
1. Read skill(s) from `~/.claude/skills/`
2. Run all 5 audit categories
3. Produce report with findings
4. No changes made

**Output:** Audit report (see Phase 1 format)

**"Audit all" variant:**
- Runs audit on every skill in `~/.claude/skills/`
- Produces summary table:
  ```
  | Skill | Issues |
  |-------|--------|
  | committing-changes | 0 ✓ |
  | creating-skills | 2 ⚠️ |
  | debating-options | 1 ⚠️ |
  ```
- Does NOT auto-fix anything

### Mode B: Update

**Trigger:** `/updating-skills update [skill-name]`

**Process:**
1. Run audit on the skill first
2. If no issues: "Skill passes all checks"
3. If issues found:
   - Show each issue
   - Propose fix
   - Show before/after diff
   - Ask for approval
   - Apply fix
   - Re-validate
4. Repeat until all issues resolved or user stops

**Fix Types:**

| Issue | Fix |
|-------|-----|
| Missing name field | Add `name: [directory-name]` |
| Name not gerund | Suggest rename, user confirms |
| Description not WHEN-focused | Rewrite using formula |
| Missing Iron Law | Add section with skill-appropriate rule |
| Missing enforcement sections | Add from template |
| Over 500 lines | Suggest splitting to reference/ |

**User Approval Required:**
- Every fix shown as diff before applying
- User can skip individual fixes
- User can stop at any point

### Success Criteria
- [ ] Both modes documented
- [ ] Mode detection is clear
- [ ] Update mode always shows diffs
- [ ] User approval required for all changes

---

## Phase 3: Write SKILL.md

### Goal
Create the main skill file.

### Tasks
- [ ] Write frontmatter
- [ ] Write mode detection
- [ ] Write Audit workflow
- [ ] Write Update workflow
- [ ] Write enforcement sections

### Structure

```
newskills/updating-skills/
├── SKILL.md                    # Main skill (~300 lines)
└── reference/
    ├── audit-checklist.md      # Full audit criteria
    └── common-fixes.md         # Fix patterns for common issues
```

### Key Sections

**Iron Law:** `NO UPDATE WITHOUT SHOWING THE DIFF FIRST`

**Gate Function:**
1. Identify mode (audit vs update)
2. Identify target skill(s)
3. Verify skill exists in ~/.claude/skills/
4. Run audit
5. If update mode: propose fixes with diffs
6. ONLY THEN: Apply approved changes

**Mode Detection:**
```
/updating-skills audit skill-name     → Audit single
/updating-skills audit all            → Audit all skills
/updating-skills update skill-name    → Update single
/updating-skills [skill-name]         → Default to audit
```

### Success Criteria
- [ ] SKILL.md follows enforcement pattern
- [ ] Under 350 lines
- [ ] Both modes clearly documented
- [ ] Description uses WHEN formula

---

## Phase 4: Add Reference Files

### Goal
Create supporting reference files.

### Tasks
- [ ] Create audit-checklist.md
- [ ] Create common-fixes.md

### audit-checklist.md

Full checklist matching validation-rules.md:
- Frontmatter checks (6 items)
- Name checks (6 items)
- Description checks (6 items)
- Structure checks (4 items)
- Pattern checks (5 items)

### common-fixes.md

Fix patterns for each issue type:

**Missing name field:**
```yaml
# Before
---
description: ...
---

# After
---
name: skill-directory-name
description: ...
---
```

**Description not WHEN-focused:**
```yaml
# Before
description: Validates code against plans

# After
description: Use this skill when verifying implementation against a plan...
```

**Missing Iron Law:**
```markdown
# Add after opening paragraph:

## The Iron Law

\`\`\`
[SKILL-SPECIFIC ABSOLUTE RULE IN CAPS]
\`\`\`
```

### Success Criteria
- [ ] audit-checklist.md covers all validation rules
- [ ] common-fixes.md has before/after for each fix type
- [ ] Reference files are actionable

---

## Phase 5: Testing

### Goal
Validate skill works on real skills.

### Tasks
- [ ] Deploy to ~/.claude/skills/
- [ ] Run audit on all existing skills
- [ ] Test update mode on a skill with known issues
- [ ] Verify diffs are shown correctly

### Test Cases

**Audit mode:**
1. Run `/updating-skills audit debating-options`
2. Verify report shows correct findings
3. Run `/updating-skills audit all`
4. Verify summary table is accurate

**Update mode:**
1. Create a test skill with known issues
2. Run `/updating-skills update test-skill`
3. Verify each fix is shown as diff
4. Verify approval is required
5. Verify re-validation after fix

### Success Criteria
- [ ] Audit mode produces accurate reports
- [ ] Update mode shows diffs before applying
- [ ] Approval required for all changes
- [ ] Re-validates after each fix

---

## Verification

After all phases complete:
- [ ] `/updating-skills audit [name]` works
- [ ] `/updating-skills audit all` produces summary
- [ ] `/updating-skills update [name]` shows diffs
- [ ] User approval required for changes
- [ ] Covers all validation-rules.md checks
