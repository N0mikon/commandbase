---
git_commit: 22359f4
created: 2026-02-01
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Plan fully executed - all 6 skills renamed and cross-references updated"
status: completed
research: .docs/research/02-01-2026-skill-structure-audit.md
archived: 2026-02-01
archive_reason: "Plan completed - all 6 skills successfully renamed with cross-references updated"
---

# Plan: Update Remaining Skills to creating-skills Format

## Overview

Update 6 non-compliant skills to match the `/creating-skills` format. Each skill needs:
1. Directory renamed to gerund form
2. `name:` field added to frontmatter
3. Description rewritten to WHEN-focused with trigger phrases
4. Cross-references updated in other skills
5. Deployed to `~/.claude/skills/`

**Research reference**: `.docs/research/02-01-2026-skill-structure-audit.md`

**If original intent is unclear**: Use `/learning-from-sessions` to review the session where the skill was created.

## Phase 1: vcode → validating-implementations

Most referenced skill. Update first to establish the pattern.

### Changes

**1. Rename directory:**
```bash
mv newskills/vcode newskills/validating-implementations
```

**2. Update frontmatter** (`newskills/validating-implementations/SKILL.md:1-3`):

Before:
```yaml
---
description: Validate implementation against plan, verify success criteria
---
```

After:
```yaml
---
name: validating-implementations
description: "Use this skill when verifying implementation against a plan, checking success criteria, or after /implementing-plans completes. This includes running validation commands, comparing code to plan specifications, checking test coverage, and confirming all phases meet their success criteria. Trigger phrases: '/vcode', 'validate the implementation', 'check against the plan', 'verify success criteria'."
---
```

**3. Update cross-references** (replace `/vcode` with `/validating-implementations`):
- `newskills/implementing-plans/SKILL.md`
- `newskills/planning-codebases/SKILL.md`
- `newskills/checkpoint/SKILL.md` (will be renamed in Phase 2)

**4. Deploy:**
```bash
rm -rf ~/.claude/skills/vcode
cp -r newskills/validating-implementations ~/.claude/skills/
```

### Success Criteria
- [x] `ls newskills/validating-implementations/SKILL.md` exists
- [x] `grep -c "^name: validating-implementations" newskills/validating-implementations/SKILL.md` returns 1
- [x] `grep -c "Use this skill when" newskills/validating-implementations/SKILL.md` returns 1
- [x] `grep "/vcode" newskills/` returns no matches (all updated)
- [x] `ls ~/.claude/skills/validating-implementations/SKILL.md` exists

---

## Phase 2: checkpoint → checkpointing

### Changes

**1. Rename directory:**
```bash
mv newskills/checkpoint newskills/checkpointing
```

**2. Update frontmatter** (`newskills/checkpointing/SKILL.md:1-3`):

Before:
```yaml
---
description: Create and verify named checkpoints for regression detection
---
```

After:
```yaml
---
name: checkpointing
description: "Use this skill when saving development checkpoints, comparing against previous states, or detecting regressions between phases. This includes creating named snapshots before risky changes, verifying no regressions after implementation, listing available checkpoints, and clearing old checkpoints. Trigger phrases: '/checkpoint create', '/checkpoint verify', '/checkpoint list', 'save a checkpoint', 'compare to checkpoint'."
---
```

**3. Update cross-references** (replace `/checkpoint` with `/checkpointing`):
- `newskills/implementing-plans/SKILL.md`
- `newskills/validating-implementations/SKILL.md` (already renamed)

**4. Deploy:**
```bash
rm -rf ~/.claude/skills/checkpoint
cp -r newskills/checkpointing ~/.claude/skills/
```

### Success Criteria
- [x] `ls newskills/checkpointing/SKILL.md` exists
- [x] `grep -c "^name: checkpointing" newskills/checkpointing/SKILL.md` returns 1
- [x] `grep -c "Use this skill when" newskills/checkpointing/SKILL.md` returns 1
- [x] `grep "/checkpoint" newskills/` returns no matches except within checkpointing skill itself
- [x] `ls ~/.claude/skills/checkpointing/SKILL.md` exists

---

## Phase 3: commit → committing-changes

### Changes

**1. Rename directory:**
```bash
mv newskills/commit newskills/committing-changes
```

**2. Update frontmatter** (`newskills/committing-changes/SKILL.md:1-3`):

Before:
```yaml
---
description: Commit and push changes, auto-create private repo if needed
---
```

After:
```yaml
---
name: committing-changes
description: "Use this skill when committing work to git, pushing changes to GitHub, or ending a session with saved progress. This includes staging files, writing commit messages, pushing to remote, and auto-creating private repos when needed. Trigger phrases: '/commit', 'commit this', 'save my work', 'push changes', 'git commit', 'commit and push'."
---
```

**3. Update cross-references** (replace `/commit` with `/committing-changes`):
- `newskills/validating-implementations/SKILL.md`
- `newskills/implementing-plans/SKILL.md`

**4. Deploy:**
```bash
rm -rf ~/.claude/skills/commit
cp -r newskills/committing-changes ~/.claude/skills/
```

### Success Criteria
- [x] `ls newskills/committing-changes/SKILL.md` exists
- [x] `grep -c "^name: committing-changes" newskills/committing-changes/SKILL.md` returns 1
- [x] `grep -c "Use this skill when" newskills/committing-changes/SKILL.md` returns 1
- [x] `grep "/commit" newskills/` returns no matches except within committing-changes skill itself
- [x] `ls ~/.claude/skills/committing-changes/SKILL.md` exists

---

## Phase 4: pr → creating-pull-requests

### Changes

**1. Rename directory:**
```bash
mv newskills/pr newskills/creating-pull-requests
```

**2. Update frontmatter** (`newskills/creating-pull-requests/SKILL.md:1-3`):

Before:
```yaml
---
description: Generate PR description and create pull request with confirmation
---
```

After:
```yaml
---
name: creating-pull-requests
description: "Use this skill when creating a pull request, opening a PR for review, or generating PR descriptions. This includes analyzing commits for the PR summary, writing PR descriptions with test plans, creating the PR via gh CLI, and requesting reviewers. Trigger phrases: '/pr', 'create a PR', 'make a pull request', 'open a pull request', 'submit for review'."
---
```

**3. Update cross-references** (replace `/pr` with `/creating-pull-requests`):
- `newskills/validating-implementations/SKILL.md`

**4. Deploy:**
```bash
rm -rf ~/.claude/skills/pr
cp -r newskills/creating-pull-requests ~/.claude/skills/
```

### Success Criteria
- [x] `ls newskills/creating-pull-requests/SKILL.md` exists
- [x] `grep -c "^name: creating-pull-requests" newskills/creating-pull-requests/SKILL.md` returns 1
- [x] `grep -c "Use this skill when" newskills/creating-pull-requests/SKILL.md` returns 1
- [x] `grep "/pr" newskills/` returns no matches except within creating-pull-requests skill itself
- [x] `ls ~/.claude/skills/creating-pull-requests/SKILL.md` exists

---

## Phase 5: handover → handing-over

### Changes

**1. Rename directory:**
```bash
mv newskills/handover newskills/handing-over
```

**2. Update frontmatter** (`newskills/handing-over/SKILL.md:1-3`):

Before:
```yaml
---
description: Document current work context for handover to another session
---
```

After:
```yaml
---
name: handing-over
description: "Use this skill when ending a session, switching context, or preparing for another session to continue your work. This includes documenting current progress, capturing open questions, listing modified files, and writing handover documents to .docs/handoffs/. Trigger phrases: '/handover', 'hand this off', 'document where we are', 'save progress for later', 'end session'."
---
```

**3. Update cross-references** (replace `/handover` with `/handing-over`):
- `newskills/takeover/SKILL.md` (will be renamed in Phase 6)

**4. Deploy:**
```bash
rm -rf ~/.claude/skills/handover
cp -r newskills/handing-over ~/.claude/skills/
```

### Success Criteria
- [x] `ls newskills/handing-over/SKILL.md` exists
- [x] `grep -c "^name: handing-over" newskills/handing-over/SKILL.md` returns 1
- [x] `grep -c "Use this skill when" newskills/handing-over/SKILL.md` returns 1
- [x] `grep "/handover" newskills/` returns no matches except within handing-over skill itself
- [x] `ls ~/.claude/skills/handing-over/SKILL.md` exists

---

## Phase 6: takeover → taking-over

### Changes

**1. Rename directory:**
```bash
mv newskills/takeover newskills/taking-over
```

**2. Update frontmatter** (`newskills/taking-over/SKILL.md:1-3`):

Before:
```yaml
---
description: Resume work from a handover document
---
```

After:
```yaml
---
name: taking-over
description: "Use this skill when picking up work from a handover document, resuming a previous session, or continuing where another session left off. This includes reading handover documents from .docs/handoffs/, understanding prior context, reviewing modified files, and continuing implementation. Trigger phrases: '/takeover', 'continue from handover', 'resume previous work', 'pick up where we left off', 'read the handover'."
---
```

**3. Update cross-references** (replace `/takeover` with `/taking-over`):
- `newskills/handing-over/SKILL.md` (already renamed)

**4. Deploy:**
```bash
rm -rf ~/.claude/skills/takeover
cp -r newskills/taking-over ~/.claude/skills/
```

### Success Criteria
- [x] `ls newskills/taking-over/SKILL.md` exists
- [x] `grep -c "^name: taking-over" newskills/taking-over/SKILL.md` returns 1
- [x] `grep -c "Use this skill when" newskills/taking-over/SKILL.md` returns 1
- [x] `grep "/takeover" newskills/` returns no matches except within taking-over skill itself
- [x] `ls ~/.claude/skills/taking-over/SKILL.md` exists

---

## Final Verification

After all phases complete:

```bash
# Verify all skills have proper frontmatter
for skill in checkpointing committing-changes creating-pull-requests handing-over taking-over validating-implementations; do
  echo "=== $skill ==="
  head -5 newskills/$skill/SKILL.md
done

# Verify no old skill names remain in cross-references
grep -r "/vcode\|/checkpoint\|/commit\|/pr\|/handover\|/takeover" newskills/ --include="*.md" | grep -v "name:"

# Verify deployment
ls ~/.claude/skills/
```

### Final Success Criteria
- [x] All 6 skills have `name:` field matching directory name
- [x] All 6 skills have WHEN-focused descriptions starting with "Use this skill when"
- [x] No cross-references use old skill names
- [x] All 6 skills deployed to `~/.claude/skills/`
- [x] Old skill directories removed from `~/.claude/skills/`

## What We're NOT Doing

- Not adding `reference/` or `templates/` subdirectories (none of these skills need them based on line counts)
- Not modifying skill body content beyond frontmatter
- Not changing skill behavior or workflow logic
- Not updating `.docs/` historical documents (they document what existed at time of writing)

## Rollback

If issues arise, restore from the git working tree:
```bash
git checkout -- newskills/
```

And restore deployed skills from backup or re-copy from newskills/.
