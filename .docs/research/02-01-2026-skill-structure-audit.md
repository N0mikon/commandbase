---
git_commit: 448f0d2
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Updated after 8 commits - skill count increased from 12 to 16, added 4 new skills, updated coverage table"
topic: "Current Skillset Audit vs everything-claude-code Recommendations"
tags: [research, skills, audit, gaps, workflow]
status: complete
references:
  - .docs/research/01-28-2026-everything-claude-code-comprehensive-review.md
  - C:/code/commandbase/newskills/
  - C:/Users/Jason/.claude/skills/
---

# Research: Current Skillset Audit and Gap Analysis

**Date**: 2026-02-01
**Branch**: master

## Research Question

Review our current skillset after recent updates and compare against everything-claude-code recommendations to give updated advice on what to add.

## Summary

Your skillset has evolved significantly since the January 28th review. You now have **16 skills** (15 deployed) covering the complete RPI workflow plus supporting functions. The original recommendation of `/learn` and `/checkpoint` has been implemented (as `/learning-from-sessions` and `/checkpointing`). Since this audit was written, 4 new skills have been added: `/debugging-codebases`, `/discussing-features`, `/reviewing-security`, and `/updating-claude-md`.

**Coverage Assessment:**

| everything-claude-code Item | Status | Your Skill |
|----------------------------|--------|------------|
| `/verify` | ✅ COVERED | `/validating-implementations` |
| `/plan` | ✅ COVERED | `/planning-codebases` |
| `/checkpoint` | ✅ COVERED | `/checkpointing` |
| `/learn` | ✅ COVERED | `/learning-from-sessions` |
| `/tdd` | ❌ NOT COVERED | - |
| `/code-review` | ✅ COVERED | `/reviewing-security` (added 2026-02-01) |
| `/build-fix` | ⚠️ PARTIAL | `/implementing-plans` has pattern |
| `/e2e` | ❌ NOT COVERED | - |
| `/orchestrate` | ⚠️ PARTIAL | Research agents pattern exists |
| `/eval` | ❌ NOT COVERED | - |
| Contexts | ⚠️ PARTIAL | Skills serve as implicit modes |
| `code-reviewer` agent | ✅ COVERED | `/reviewing-security` (added 2026-02-01) |
| `security-reviewer` agent | ✅ COVERED | `/reviewing-security` (added 2026-02-01) |
| `tdd-guide` agent | ❌ NOT COVERED | - |

---

## Your Current Skillset (16 Skills)

### Core RPI Workflow

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `/researching-codebases` | Document codebase with parallel agents | NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST |
| `/planning-codebases` | Create phased plans with research | NO PLAN WITHOUT CODEBASE RESEARCH FIRST |
| `/implementing-plans` | Execute plans with verification | NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE |
| `/validating-implementations` | Two-stage validation (spec + quality) | NO VERDICT WITHOUT FRESH EVIDENCE |

### Supporting Skills

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `/checkpointing` | Named git snapshots for regression detection | NO CHECKPOINT WITHOUT GIT STATE VERIFICATION |
| `/committing-changes` | Git commit with staged file verification | NO COMMIT WITHOUT STAGED FILE VERIFICATION |
| `/creating-pull-requests` | PR creation with full branch analysis | NO PR WITHOUT FULL BRANCH ANALYSIS |

### Session Management

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `/handing-over` | Write handoffs with key learnings | NO HANDOVER WITHOUT KEY LEARNINGS |
| `/taking-over` | Resume from handoff with state verification | NO WORK WITHOUT STATE VERIFICATION |

### Meta/Learning Skills

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `/learning-from-sessions` | Extract reusable knowledge as skills | NO EXTRACTION WITHOUT VERIFICATION AND USER APPROVAL |
| `/creating-skills` | Build and validate skill files | NO SKILL WITHOUT VALIDATED DESCRIPTION AND STRUCTURE |
| `/starting-projects` | Greenfield project initialization | Research before recommending |
| `/updating-claude-md` | Maintain CLAUDE.md files | NO CHANGE WITHOUT READING THE CURRENT FILE FIRST |

### Quality/Security Skills (NEW)

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `/reviewing-security` | Security review before public commits | NO PUBLIC COMMIT WITH CRITICAL SECURITY ISSUES |
| `/debugging-codebases` | Systematic hypothesis-driven debugging | HYPOTHESIS BEFORE ACTION |
| `/discussing-features` | Capture user intent before planning | CAPTURE HOW PREFERENCES BEFORE RESEARCH |

---

## Gap Analysis: What You're Missing

### Tier 1: High Value Additions

#### 1. `/code-reviewing` - Security and Quality Review
**Status**: ✅ IMPLEMENTED as `/reviewing-security` (commit eab1cb7)

The skill now provides:
- Hardcoded secret detection
- SQL injection and XSS vulnerability scanning
- OWASP Top 10 issue detection
- CRITICAL/HIGH/MEDIUM/LOW severity classification
- PASS/WARN/BLOCK verdicts
- Iron Law: "NO PUBLIC COMMIT WITH CRITICAL SECURITY ISSUES"

**Integration point**: Run before `/committing-changes` for public repos

#### 2. `/tdd-testing` - Test-Driven Development
**Why needed**: Your workflow assumes tests exist but doesn't enforce writing tests first. TDD pattern:
- RED: Write failing test
- GREEN: Minimal code to pass
- REFACTOR: Clean up while green

**Integration point**: Use within `/implementing-plans` phases

**Iron Law suggestion**: "NO CODE WITHOUT FAILING TEST FIRST"

### Tier 2: Medium Value Additions

#### 3. `/build-fixing` - Incremental Error Resolution
**Why needed**: `/implementing-plans` has the pattern but not formalized:
- Fix ONE error at a time
- Re-run build after each fix
- Stop if fix introduces new errors

**Your current pattern** (`implementing-plans/SKILL.md:76-84`): "Getting Stuck" section addresses this but not as structured process

**Recommendation**: Could be a reference doc in `/implementing-plans/reference/build-fix-workflow.md` rather than separate skill

#### 4. `/e2e-testing` - End-to-End Testing
**Why needed**: No browser/Playwright testing workflow. Useful for:
- UI component testing
- Multi-page flows
- Screenshot regression testing

**Integration point**: Part of validation phase for frontend projects

#### 5. `/refactoring-safely` - Dead Code Removal
**Why needed**: Safe refactoring with test verification:
- Run static analysis (knip, depcheck)
- Categorize changes by risk
- Test after each removal
- Rollback if tests fail

**Integration point**: Standalone skill for code cleanup tasks

### Tier 3: Lower Priority

#### 6. `/orchestrating-agents` - Agent Pipelines
**Why needed**: Your skills already spawn agents, but no formal pipeline definition. Would enable:
- `feature`: planner → tdd-guide → code-reviewer
- `bugfix`: explorer → tdd-guide → reviewer
- `refactor`: architect → reviewer → tdd-guide

**Note**: You may not need this - your skill-based workflow already orchestrates implicitly

#### 7. `/evaluating-code` - Eval-Driven Development
**Why needed**: Formal success metrics beyond "tests pass":
- Capability evals (new features work)
- Regression evals (old features still work)
- pass@k metrics

**Note**: Overkill for most projects

### Tier 4: Consider but Not Recommended

#### Contexts (dev, research, review)
**Your skills already serve as implicit contexts**:
- `/researching-codebases` = research mode
- `/implementing-plans` = dev mode
- `/validating-implementations` = review mode

**Recommendation**: Don't add formal contexts - your Iron Laws in skills already enforce correct behavior

---

## Updated Workflow Recommendation

```
Current:
/researching-codebases → /planning-codebases → /implementing-plans → /validating-implementations → /committing-changes

Recommended Addition (Tier 1 only):
/researching-codebases → /planning-codebases → /implementing-plans → /validating-implementations → /code-reviewing → /committing-changes
                                                    ↑
                                            (use /tdd-testing within phases)
```

---

## What You Already Cover Well

### ✅ Verification (maps to `/verify`)
Your `/validating-implementations` does two-stage review:
- **Stage 1**: Spec compliance (does code match plan?)
- **Stage 2**: Code quality (do tests pass? type check?)

Reference: `validating-implementations/SKILL.md:26-59`

### ✅ Planning with Confirmation (maps to `/plan`)
Your `/planning-codebases` requires:
- Research agents BEFORE planning
- Interactive development with user confirmation
- Checkpoint suggestion after plan approval

Reference: `planning-codebases/SKILL.md:26-41, 159-184`

### ✅ Checkpointing (maps to `/checkpoint`)
Your `/checkpointing` provides:
- Named git snapshots
- State verification before checkpoint
- Regression detection via comparison

Reference: `checkpointing/SKILL.md:42-178`

### ✅ Pattern Learning (maps to `/learn`)
Your `/learning-from-sessions` provides:
- Dedup checking before extraction
- 4 identification questions
- Quality gates for skill creation
- User confirmation required

Reference: `learning-from-sessions/SKILL.md:26-42, 175-188`

---

## Specific Recommendations

### Immediate Actions

1. **~~Create `/code-reviewing`~~** - ✅ DONE as `/reviewing-security`
   - Security/quality gate before commits
   - Checks for CRITICAL (secrets, injection), HIGH (exploitable vulnerabilities), MEDIUM (context-dependent), LOW (best practice)
   - Blocks commit if CRITICAL or HIGH found
   - Iron Law: "NO PUBLIC COMMIT WITH CRITICAL SECURITY ISSUES"

2. **Create `/tdd-testing`** - Test-driven development enforcement (STILL NEEDED)
   - RED → GREEN → REFACTOR cycle
   - 80% coverage target
   - Iron Law: "NO IMPLEMENTATION WITHOUT FAILING TEST FIRST"

### Near-Term Actions

3. **Add reference doc** `implementing-plans/reference/build-fix-workflow.md`
   - Formalize the "Getting Stuck" pattern
   - One error at a time
   - Stop conditions

4. **Consider `/e2e-testing`** only if you work on frontend projects

### Skip For Now

- `/orchestrating-agents` - Your skills already orchestrate implicitly
- `/evaluating-code` - Overkill unless you need formal metrics
- Contexts - Your Iron Laws already enforce correct behavior
- `/refactoring-safely` - Can be added when needed

---

## Architecture Notes

### Skill Structure Pattern
All your skills follow consistent pattern:
- Purpose description in first 10 lines
- Iron Law clearly stated
- Gate Function with step-by-step process
- Progressive disclosure via `reference/` subdirectories
- Templates for outputs

### Deployment Status
16 skills in development, 15 deployed:
- Development: `C:/code/commandbase/newskills/` (16 skills)
- Deployed: `C:/Users/Jason/.claude/skills/` (15 skills - `/debugging-codebases` pending deployment)

### Reference Directory Usage
Skills with `reference/` subdirectories: 10+
- creating-skills (4 files + templates)
- learning-from-sessions (4 files + templates)
- starting-projects (3 files + templates)
- researching-codebases (2 files + templates)
- planning-codebases (2 files + templates)
- implementing-plans (2 files)
- debugging-codebases (3 files + templates) - NEW
- discussing-features (1 file + templates) - NEW
- updating-claude-md (2 files) - NEW
- validating-implementations (0 files - references exist in SKILL.md but files not created)

---

## Code References

- `validating-implementations/SKILL.md:26-59` - Two-stage review gate function
- `planning-codebases/SKILL.md:159-184` - Confirmation gate and checkpoint suggestion
- `implementing-plans/SKILL.md:76-84` - Getting stuck guidance
- `checkpointing/SKILL.md:42-178` - Full checkpoint operations
- `learning-from-sessions/SKILL.md:26-42` - Gate function for extraction
- `committing-changes/SKILL.md:12-24` - Staged file verification iron law

---

## Open Questions

1. ~~Should `/code-reviewing` be integrated into `/committing-changes` or standalone?~~ **RESOLVED**: Created as standalone `/reviewing-security` skill
2. Should `/tdd-testing` be a skill or a reference doc in `/implementing-plans`?
3. Do you need `/e2e-testing` for your current projects?
4. Should `/debugging-codebases` be deployed to production? (Currently in development only)

---

## Update History

| Date | Commits Behind | Changes |
|------|----------------|---------|
| 2026-02-01 | 8 | Updated skill count 12->16, marked `/code-reviewing` as DONE (`/reviewing-security`), added new skills to tables, updated deployment status |
