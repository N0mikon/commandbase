---
date: 2026-02-08
status: complete
topic: "Document Staleness Skill and Auto-Update Integration"
tags: [plan, implementation, auditing-docs, docs-updater, staleness, skills]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 11 commits - refreshed all file references from newskills/newagents/ to plugins/ paths after plugin marketplace restructure"
references:
  - plugins/commandbase-core/agents/docs-updater.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-meta/skills/auditing-skills/SKILL.md
  - plugins/commandbase-meta/skills/auditing-agents/SKILL.md
  - plugins/commandbase-git-workflow/skills/auditing-docs/SKILL.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/designing-code/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - .docs/research/02-08-2026-document-staleness-detection-and-update-opportunities.md
---

# Document Staleness Skill and Auto-Update Integration

**Upstream Research**: `.docs/research/02-08-2026-document-staleness-detection-and-update-opportunities.md`

## Goal

Address two document freshness problems:
1. No standalone way to methodically audit all `.docs/` files for staleness
2. Skills that read upstream documents never check freshness — they trust stale content blindly

## What We're NOT Doing

- Not changing how docs-writer creates documents (frontmatter format stays the same)
- Not changing the docs-updater agent itself (its logic is solid)
- Not changing `/committing-changes` staleness detection (it keeps its >5 commit threshold and user prompt)
- Not adding staleness checks to medium-value skills (structuring-code, starting-projects, importing-vault) — keep scope tight, can add later
- Not creating a new agent — reusing the existing docs-updater agent

## Architecture Decision

**Auto-update, not guard**: When an upstream-reading skill detects a stale document, it automatically spawns docs-updater to refresh it before proceeding. No user prompt for individual staleness — the skill just quietly ensures the document is current. This is different from `/committing-changes` which prompts the user because committing is a deliberate act. Reading an upstream doc should just work with fresh data.

**Shared reference snippet**: The staleness detection bash script (currently duplicated only in `/committing-changes`) will be extracted into a reference file that multiple skills can include.

---

## Phase 1: Create Shared Staleness Detection Reference

**Goal**: Extract the staleness detection script into a reusable reference file.

### Tasks

- [x] Create `plugins/commandbase-git-workflow/skills/auditing-docs/reference/staleness-detection.md` containing:
  - The bash script from `plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md:67-76`
  - Explanation of how the script works (find → filter tracked → extract git_commit → count behind)
  - Single-file variant: a version that checks ONE specific file path (for upstream-reading skills)
  - docs-updater spawn pattern: how to invoke the agent via Task tool
- [x] Verify the single-file variant works by tracing through the logic

### Single-File Detection Script

For upstream-reading skills that need to check ONE document (not scan all of `.docs/`):

```bash
# Check single file staleness
f="<path-to-doc>"
commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
  git rev-parse "$commit" >/dev/null 2>&1 && \
  behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
  [ -n "$behind" ] && [ "$behind" -gt 0 ] && echo "$behind"
fi
```

Returns the number of commits behind, or nothing if current/no commit recorded.

### Success Criteria

- Reference file exists at `plugins/commandbase-git-workflow/skills/auditing-docs/reference/staleness-detection.md`
- Contains both full-scan and single-file variants
- Contains docs-updater spawn pattern
- Script logic matches the proven `/committing-changes` implementation

---

## Phase 2: Create `/auditing-docs` Skill via `/creating-skills`

**Goal**: Build a new skill for methodically auditing all `.docs/` files for staleness and freshness.

### Tasks

- [x] Invoke `/creating-skills` with the research doc as input
- [x] Skill name: `auditing-docs`
- [x] Skill location: `plugins/commandbase-git-workflow/skills/auditing-docs/`
- [x] Development location: `plugins/commandbase-git-workflow/skills/auditing-docs/`

### Skill Design Inputs for `/creating-skills`

**Name**: `auditing-docs` (gerund form: "auditing", noun target: "docs")

**Description formula**: "Use this skill when auditing `.docs/` documents for staleness, checking document health across the project, or reviewing which documents need updating or archiving. This includes scanning all `.docs/` subdirectories for stale frontmatter, spawning docs-updater for each stale document, presenting audit dashboards with staleness metrics, and archiving obsolete documents."

**Trigger phrases**: `/auditing-docs`, `audit docs`, `check document freshness`, `which docs are stale`, `review documents`

**Pattern**: Follow `/auditing-skills` and `/auditing-agents` sibling pattern — same Iron Law ("NO UPDATE WITHOUT ASSESSMENT FIRST"), same Gate Function structure, same Mode Detection (audit/update/audit all), same one-at-a-time discipline.

**Iron Law**: `NO UPDATE WITHOUT STALENESS ASSESSMENT FIRST`

**Modes**:

| Input | Mode | Target |
|-------|------|--------|
| `/auditing-docs audit` | Audit | All docs (dashboard only) |
| `/auditing-docs audit .docs/plans/` | Audit | Single directory |
| `/auditing-docs update` | Update | All stale docs, one-by-one |
| `/auditing-docs update .docs/plans/file.md` | Update | Single doc |
| `/auditing-docs` | Audit | All docs (default) |

**Mode A: Audit** (read-only):
1. Run staleness detection script (full-scan variant from reference)
2. For each stale doc, also check if referenced files still exist (via `ls`)
3. Present dashboard:
   ```
   DOCUMENT AUDIT
   ==============
   | Document | Commits Behind | References | Status |
   |----------|---------------|------------|--------|
   | .docs/plans/01-15-auth.md | 12 | 2/3 exist | STALE |
   | .docs/handoffs/01-20-session.md | 8 | 0/2 exist | OBSOLETE |
   | .docs/research/01-10-patterns.md | 3 | all exist | OK |

   Summary: 5 stale, 2 obsolete, 8 current
   Run `/auditing-docs update` to process stale documents.
   ```
4. Categorize: CURRENT (0-2 behind), STALE (3+ behind, refs exist), OBSOLETE (refs deleted or very old handoff)

**Mode B: Update** (interactive):
1. Run audit first (same as Mode A)
2. Sort by staleness (most behind first)
3. For each stale/obsolete doc, one at a time:
   - Show the assessment (commits behind, reference status, content summary)
   - Spawn docs-updater agent
   - Show what docs-updater did (updated content or archived)
   - Ask user to confirm result before moving to next doc
4. After all processed, show final dashboard

**Reference files**:
- `reference/staleness-detection.md` — shared detection script (created in Phase 1)
- `reference/audit-checklist.md` — document health checks (frontmatter present, git_commit valid, references exist, status field current)

### Success Criteria

- [x] Skill passes `/auditing-skills audit auditing-docs` with 0 issues
- [x] `audit` mode produces a dashboard table for all `.docs/` files
- [x] `update` mode spawns docs-updater one-by-one with user confirmation between each
- [x] Follows the auditing-skills/auditing-agents sibling pattern
- [x] Reference files exist and are loaded by the skill

---

## Phase 3: Add Auto-Update to 4 Upstream-Reading Skills via `/creating-skills`

**Goal**: Skills that read `.docs/` files as input should auto-refresh stale documents before proceeding.

**Method**: Use `/creating-skills` in **edit mode** for each skill. This ensures edits go through the same validation pipeline as new skills — description updates, structural checks, and audit compliance.

### Architecture

**Pattern**: Before reading an upstream doc, check its staleness. If >3 commits behind, silently spawn docs-updater to refresh it, then read the updated version. No user prompt — auto-update is the default because these skills need current data to function correctly.

**Threshold**: >3 commits behind (tighter than `/committing-changes`'s >5, because upstream-reading skills make decisions based on the doc content).

**Insertion point**: Each skill already has a step where it reads the upstream doc. The staleness check goes immediately before that read.

### Edit Specifications

Each sub-phase invokes `/creating-skills` in edit mode with a description of the change needed. The edit instructions for each skill:

#### 3a. `/creating-skills edit taking-over`

**Edit request**: Add a staleness auto-update step before reading upstream `.docs/` files in Step 1.

**What to add** (Step 1, before "Begin analysis"):
- Before reading the handoff document, check its `git_commit` frontmatter
- If >3 commits behind HEAD: spawn docs-updater to refresh it, then read the refreshed version
- If docs-updater archives it (all references deleted): warn the user that the handoff may be obsolete and ask whether to proceed
- Apply the same check to linked plans/research documents mentioned in the handoff

**Where**: Step 1: Load the Handover, after the "Read the handover document FULLY" instruction

#### 3b. `/creating-skills edit planning-code`

**Edit request**: Add a staleness auto-update step when detecting upstream BRDSPI artifacts as input.

**What to add** (Input Detection section):
- When a `.docs/structure/` or `.docs/design/` file is detected as input, check its `git_commit` frontmatter
- If >3 commits behind HEAD: spawn docs-updater to refresh it before using it as plan input
- If docs-updater archives it: warn user that the upstream artifact is obsolete — suggest re-running the upstream skill

**Where**: Input Detection section, after detecting artifact type but before using it

#### 3c. `/creating-skills edit designing-code`

**Edit request**: Add a staleness auto-update step before reading research artifacts in Step 1.

**What to add** (Step 1: Locate and Read Research Artifacts):
- For each research artifact found, check its `git_commit` frontmatter
- If >3 commits behind HEAD: spawn docs-updater to refresh it before reading
- If docs-updater archives it: skip this artifact and note it was obsolete
- Apply the same check to `.docs/brainstorm/` artifacts

**Where**: Step 1, before reading each research/brainstorm artifact

#### 3d. `/creating-skills edit resuming-sessions`

**Edit request**: Add a staleness auto-update step before scanning handoffs and learnings in Step 4.

**What to add** (Step 4: Scan for Related Context):
- For each handoff or learning document found, check its `git_commit` frontmatter
- If >3 commits behind HEAD: spawn docs-updater to refresh it before presenting to user
- If docs-updater archives it: omit from session context (note it was archived)

**Where**: Step 4, before presenting context to user

### Success Criteria

- [x] All 4 skills edited via `/creating-skills` edit mode (not manual edits)
- [x] Each skill contains the auto-update pattern with >3 commit threshold
- [x] Each uses the single-file staleness detection variant
- [x] Archive results are handled gracefully (warn or omit, don't crash)
- [x] The pattern is consistent across all 4 skills (same threshold, same behavior)
- [x] All 4 skills pass `/auditing-skills audit` after editing

---

## Phase 4: Deploy and Verify

**Goal**: Copy new/modified skills to global config and verify everything works.

### Tasks

- [x] Skills deployed to plugin directories (plugin marketplace restructure replaced manual copy to `~/.claude/skills/`):
  - `plugins/commandbase-git-workflow/skills/auditing-docs/SKILL.md`
  - `plugins/commandbase-code/skills/planning-code/SKILL.md`
  - `plugins/commandbase-code/skills/designing-code/SKILL.md`
  - `plugins/commandbase-session/skills/resuming-session/SKILL.md`
- [x] Run `/auditing-skills audit auditing-docs` to validate the new skill
- [x] Run `/auditing-skills audit taking-over` to check modified skill health
- [x] Run `/auditing-skills audit planning-code` to check modified skill health
- [x] Run `/auditing-skills audit designing-code` to check modified skill health
- [x] Run `/auditing-skills audit resuming-sessions` to check modified skill health

### Success Criteria

- [x] All 5 skills pass audit with 0 issues
- [x] `/auditing-docs audit` produces a valid dashboard for the project's `.docs/` files
- [x] Upstream-reading skills auto-refresh stale docs without user prompts

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| docs-updater takes too long, slowing upstream skills | docs-updater is spawned as a single Task agent — typical execution is <30s |
| Auto-update modifies a doc the user didn't want changed | docs-updater is conservative (update > archive), and the change is visible in git diff before commit |
| Circular updates (skill updates doc, triggers another skill) | Only upstream-reading skills auto-update, and docs-updater doesn't trigger other skills |
| Stale doc has no git_commit frontmatter | Single-file script handles this — returns nothing, skill proceeds normally |

## Execution Order

Phase 1 → Phase 2 (uses `/creating-skills`) → Phase 3 → Phase 4

Phase 2 depends on Phase 1 (reference file must exist before skill references it).
Phase 3 is independent of Phase 2 but shares the reference snippet concept.
Phase 4 depends on all prior phases.

---

## Post-Completion Notes

**2026-02-09 (docs-updater refresh)**: All file references updated from `newskills/` and `newagents/` paths to `plugins/` paths following the plugin marketplace restructure (commit `87a19a3`). The `taking-over` skill referenced in Phase 3a was deleted in commit `92113aa` (session skills v2) and superseded by `plugins/commandbase-session/skills/resuming-session/SKILL.md`. The auto-update pattern from Phase 3a was carried forward into the `resuming-session` skill. Phase 3 body text preserved as-is for historical accuracy.
