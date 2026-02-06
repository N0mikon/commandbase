---
git_commit: 119d2bd
last_updated: 2026-02-05
last_updated_by: claude
topic: "Opus 4.6 Skill Hardening"
tags: [plan, implementation, skills, opus-4-6, enforcement-patterns]
status: complete
references:
  - .docs/research/02-05-2026-opus-4-6-skill-audit.md
  - ~/.claude/skills/implementing-plans/SKILL.md
  - ~/.claude/skills/committing-changes/SKILL.md
  - ~/.claude/skills/creating-pull-requests/SKILL.md
  - ~/.claude/skills/reviewing-changes/SKILL.md
---

# Opus 4.6 Skill Hardening Implementation Plan

## Overview

Apply four targeted updates to skills that have gaps against Opus 4.6 behavioral tendencies (verbosity, unexpected modifications, stronger persistence). Each phase uses `/updating-skills update <skill-name>` to make changes through the standard audit-and-approve workflow, then syncs changes back to the commandbase repo.

## Current State Analysis

All 22 skills pass the standard 5-category structural audit. However, four skills have specific content gaps that Opus 4.6 behaviors can exploit:

### Key Discoveries:
- `implementing-plans/SKILL.md:56`: "Follow the plan's intent while adapting to what you find" - too permissive for a model that makes unsolicited changes
- `implementing-plans/SKILL.md:89`: "Do NOT pause between phases" amplifies verbosity + unexpected modification risks
- `committing-changes/SKILL.md:119`: 72-char first-line limit exists, but no body length constraint
- `creating-pull-requests/SKILL.md:102`: "Be concise but thorough" is subjective with no numeric limits
- `reviewing-changes/SKILL.md:97-103`: Commit message template lacks length constraints

## Desired End State

After this plan is complete:
1. implementing-plans has explicit Red Flag and Rationalization Prevention entries for out-of-plan changes, and tightened adaptation language
2. committing-changes has explicit commit message body length guidance
3. creating-pull-requests has explicit section length limits in the PR description template
4. reviewing-changes mirrors the commit message length guidance from committing-changes

### Verification:
- Each skill still passes all 5 standard audit categories after updates
- Each change is surgical (only adding/modifying the flagged sections)
- Global config (`~/.claude/skills/`) and repo (`newskills/`) stay in sync

## What We're NOT Doing

- Rewriting skills from scratch
- Adding model-specific language (no "Because Opus 4.6 tends to...")
- Changing skills rated Low risk (checkpointing, discussing-features, reviewing-security, taking-over, updating-skills)
- Modifying enforcement architecture (Iron Law, Gate Function structure stays the same)
- Updating debugging-codebases or validating-implementations (the audit found their persistence risk is actually positive)

## Implementation Approach

Run `/updating-skills update <skill-name>` for each of the four skills in priority order. Each invocation will:
1. Audit the skill
2. Propose the specific changes from the audit research as diffs
3. Get user approval
4. Apply the changes to `~/.claude/skills/<skill-name>/SKILL.md`
5. Copy the updated file back to `newskills/<skill-name>/SKILL.md`

The changes are independent, so each phase is self-contained. If any phase is rejected, the others still work.

---

## Phase 1: implementing-plans (Unexpected Modifications + Persistence)

### Overview
Highest combined risk. Add guardrails against out-of-plan changes and tighten the "adapt" language that gives license for unsolicited modifications.

### Changes Required:

#### 1. Tighten adaptation language
**File**: `~/.claude/skills/implementing-plans/SKILL.md`
**Location**: Lines 55-62 (Implementation Philosophy section)
**Change**: Replace permissive "adapting" language with strict plan-adherence language

Before:
```
- Follow the plan's intent while adapting to what you find
```
After:
```
- Follow the plan exactly. If reality requires deviation, STOP and present the deviation before making it.
```

Before:
```
When things don't match the plan exactly, think about why and adapt. The plan is your guide, but your judgment matters too.
```
After:
```
When things don't match the plan exactly, STOP and present the mismatch to the user. Do not adapt silently - explain what's different and propose the deviation. The plan is your contract, not a suggestion.
```

#### 2. Add Red Flag for out-of-plan changes
**File**: `~/.claude/skills/implementing-plans/SKILL.md`
**Location**: Red Flags section (lines 140-148)
**Change**: Add new Red Flag entry

```
- Making changes not described in the plan without explaining why and getting approval
- "Improving" or refactoring code that the plan didn't ask you to touch
```

#### 3. Add Rationalization Prevention row for scope creep
**File**: `~/.claude/skills/implementing-plans/SKILL.md`
**Location**: Rationalization Prevention table (lines 150-158)
**Change**: Add new row

```
| "This related code could use cleanup" | Only change what the plan specifies. File a separate task for other improvements. |
| "While I'm here, I should also..." | No. Finish the planned work. Scope creep is how plans fail. |
```

### Success Criteria:
- [x] `/updating-skills update implementing-plans` completes with user approval
- [x] Updated skill passes all 5 audit categories
- [x] Changes synced to `newskills/implementing-plans/SKILL.md`

---

## Phase 2: committing-changes (Verbosity)

### Overview
Highest frequency impact - every session ends with a commit. Add explicit body length guidance to prevent bloated multi-paragraph commit messages.

### Changes Required:

#### 1. Add commit message body length guidance
**File**: `~/.claude/skills/committing-changes/SKILL.md`
**Location**: Commit message guidelines section (lines 116-120)
**Change**: Add body length constraint after the existing guidelines

```
- Body: 0-3 bullet points max. If you need more, the commit is too large - suggest splitting it.
- Total commit message (including body) should rarely exceed 5 lines
```

### Success Criteria:
- [x] `/updating-skills update committing-changes` completes with user approval
- [x] Updated skill passes all 5 audit categories
- [x] Changes synced to `newskills/committing-changes/SKILL.md`

---

## Phase 3: creating-pull-requests (Verbosity)

### Overview
External visibility impact - PR descriptions are read by reviewers. Add explicit section length limits to replace subjective "concise but thorough" guidance.

### Changes Required:

#### 1. Add section length limits to PR description template
**File**: `~/.claude/skills/creating-pull-requests/SKILL.md`
**Location**: PR description rules section (around line 99-103)
**Change**: Replace "Be concise but thorough" with explicit limits

Before:
```
- Be concise but thorough
```
After:
```
- Summary: 1-3 bullet points
- Changes: 2-5 sentences max
- Testing: 1-3 bullet points
- Notes: Only if genuinely needed (breaking changes, migration steps). Omit if empty.
```

### Success Criteria:
- [x] `/updating-skills update creating-pull-requests` completes with user approval
- [x] Updated skill passes all 5 audit categories
- [x] Changes synced to `newskills/creating-pull-requests/SKILL.md`

---

## Phase 4: reviewing-changes (Verbosity)

### Overview
Feeds into committing-changes. Mirror the commit message length guidance for consistency.

### Changes Required:

#### 1. Add length constraints to commit message template
**File**: `~/.claude/skills/reviewing-changes/SKILL.md`
**Location**: Commit message template section (lines 97-106)
**Change**: Add length guidance to the template section

```
- First line: under 72 characters
- Body: 0-3 bullet points max. More bullets = commit too large, suggest splitting.
```

### Success Criteria:
- [x] `/updating-skills update reviewing-changes` completes with user approval
- [x] Updated skill passes all 5 audit categories
- [x] Changes synced to `newskills/reviewing-changes/SKILL.md`

---

## Testing Strategy

### Per-Phase Validation:
- `/updating-skills` runs its own 5-category audit before and after changes
- User approves each diff before application (enforced by updating-skills Iron Law)

### Post-Implementation:
- Run `/updating-skills audit all` after all four phases to confirm no regressions
- Verify repo/global sync with diff between `newskills/` and `~/.claude/skills/`

## Execution Notes

- Run phases sequentially (one `/updating-skills update` at a time per Iron Law)
- After each phase, copy the updated skill back to the repo: `cp ~/.claude/skills/<name>/SKILL.md newskills/<name>/SKILL.md`
- Commit after all four phases are complete (single commit for the plan, separate commits for the skill updates if preferred)

## References

- Audit research: `.docs/research/02-05-2026-opus-4-6-skill-audit.md`
- Opus 4.6 behavioral changes: `.docs/research/02-05-2026-opus-4-6-vs-4-5-changes.md`
- Updating-skills workflow: `~/.claude/skills/updating-skills/SKILL.md`
