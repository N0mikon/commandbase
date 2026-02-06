# Skill Drift Comparison: Global vs newskills

**Date:** 02-05-2026
**Question:** Which skills have drifted between `~/.claude/skills/` (global/deployed) and `newskills/` (repo/source of truth)?

## Summary

Out of 19 skills, **3 skills have drifts** across **4 files**. In all cases, the **global version is newer** -- changes were made while working in other repos and not synced back.

## Findings

### Identical Skills (16 of 19)

The following skills are fully in sync (SKILL.md and all subdirectory files match):

- bookmarking-code
- creating-prs
- creating-skills (+ reference/ + templates/)
- debating-options
- debugging-code (+ reference/ + templates/)
- discussing-features (+ reference/ + templates/)
- handing-over
- implementing-plans (+ reference/)
- learning-from-sessions (+ reference/ + templates/)
- planning-code (+ reference/ + templates/)
- reviewing-changes (+ templates/)
- reviewing-security
- taking-over
- updating-claude-md (+ reference/)
- updating-skills (+ reference/)
- validating-code

### Changed Skill 1: committing-changes

**File:** `committing-changes/SKILL.md`
**Direction:** Global is newer

**What changed:**
- **Global** moved the stale documentation check to **Step 2** (pre-commit gate) -- docs are checked before analyzing changes, and the `docs-updater` agent is offered to include updated docs in the same commit
- **Repo** has the stale docs check as **Step 8** (post-push advisory) -- docs are checked after pushing, processed one at a time with continue prompts, and skipping ends the command

**Impact:** The global version treats stale docs as a blocking pre-commit concern. The repo version treats it as a post-push notification. This is a significant workflow difference.

### Changed Skill 2: researching-code

**File:** `researching-code/SKILL.md`
**Direction:** Global is newer

**What changed:**
- Gate Function expanded from 5 steps to 7 steps -- added step 6 (WRITE research file, marked MANDATORY) and step 7 (PRESENT to user)
- Enforcement preamble changed from "BEFORE synthesizing findings" to "BEFORE completing research"
- Warning lines expanded: added "Research without a file = research that will be lost"
- **New section added:** "Red Flags - STOP and Verify" checklist (5 items)
- **New section added:** "Rationalization Prevention" table (5 excuse/reality pairs)
- Closing enforcement line updated to include "Write the research file. THEN present findings."

**Impact:** The global version has significantly stronger enforcement around mandatory research file creation. The repo version lacks these guardrails entirely.

### Changed Skill 3: starting-projects

**Files:** Two subdirectory files changed (SKILL.md itself is identical)
**Direction:** Global is newer

#### reference/claude-md-guidelines.md
- Added bullet points: "Security NEVER rules (defined in ~/.claude/CLAUDE.md)" and "Personal identity/accounts (defined in ~/.claude/CLAUDE.md)"
- Added entire new section: **"Hierarchy Awareness"** explaining that project CLAUDE.md inherits from global, with lists of what NOT to duplicate vs what to include

#### templates/claude-md-template.md
- Line 52 changed from a specific learned-pattern instruction to:
  ```
  See ~/.claude/CLAUDE.md for global behaviors.
  Project-specific behaviors can be added here if needed.
  ```
- Reflects the hierarchy-aware approach where behaviors live in global CLAUDE.md

**Impact:** These changes implement a "hierarchy awareness" pattern -- project CLAUDE.md files should reference global rather than duplicating rules.

## File Inventory

| Skill | File | Status | Newer |
|-------|------|--------|-------|
| committing-changes | SKILL.md | DIFFERS | Global |
| researching-code | SKILL.md | DIFFERS | Global |
| starting-projects | reference/claude-md-guidelines.md | DIFFERS | Global |
| starting-projects | templates/claude-md-template.md | DIFFERS | Global |

## Action Required

Copy these 4 files from `~/.claude/skills/` to `newskills/` to sync the repo:

```bash
cp ~/.claude/skills/committing-changes/SKILL.md newskills/committing-changes/SKILL.md
cp ~/.claude/skills/researching-code/SKILL.md newskills/researching-code/SKILL.md
cp ~/.claude/skills/starting-projects/reference/claude-md-guidelines.md newskills/starting-projects/reference/claude-md-guidelines.md
cp ~/.claude/skills/starting-projects/templates/claude-md-template.md newskills/starting-projects/templates/claude-md-template.md
```

**Status:** All 4 files synced (global -> repo) on 2026-02-05.
