---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Refreshed frontmatter after 54 commits - updated references from newskills/ to plugins/ paths; handing-over/taking-over replaced by session plugin skills"
topic: "RPI Skill Enforcement Patterns (All Skills)"
tags: [plan, implementation, researching-code, implementing-plans, planning-code, validating-code, committing-changes, creating-prs, handing-over, taking-over, starting-projects, enforcement, superpowers-patterns]
status: historical
archived: 2026-02-02
archive_reason: "Completed implementation plan - all 17 phases executed, skills restructured and renamed to gerund form. Skills later migrated from newskills/ to plugins/ structure. handing-over and taking-over replaced by ending-session and resuming-session in commandbase-session plugin."
references:
  - plugins/commandbase-code/skills/researching-code/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-core/skills/validating-code/SKILL.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - plugins/commandbase-git-workflow/skills/creating-prs/SKILL.md
  - plugins/commandbase-session/skills/ending-session/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - plugins/commandbase-core/skills/starting-projects/SKILL.md
  - .docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md
  - C:/code/superpowers/skills/verification-before-completion/SKILL.md
  - C:/code/superpowers/skills/executing-plans/SKILL.md
---

# RPI Skill Enforcement Patterns Implementation Plan

> **Historical Note (2026-02-01)**:
> This plan has been fully executed. Skills were then renamed to gerund form:
> - `rcode` -> `researching-code`
> - `icode` -> `implementing-plans`
> - `pcode` -> `planning-code`
> - `vcode` -> `validating-code`
> - `commit` -> `committing-changes`
> - `pr` -> `creating-prs`
> - `handover` -> `handing-over`
> - `takeover` -> `taking-over`
> - `new_project` -> `starting-projects`
> See `.docs/plans/02-01-2026-skill-structure-updates.md` for the rename plan.
>
> **Historical Note (2026-02-09)**:
> Skills have since migrated from `newskills/` to `plugins/` structure. All `newskills/` paths
> in this document are obsolete. `handing-over` and `taking-over` were replaced by
> `ending-session` and `resuming-session` in the `commandbase-session` plugin.

## Overview

Enhance ALL RPI workflow skills with Superpowers enforcement patterns and restructure to directory format (`skillname/SKILL.md`). This enables supporting files and follows Claude Code best practices.

**Phases 1-10 (rcode + icode):** Complete - enhanced with Iron Laws, Gate Functions, Red Flags, Rationalization Prevention, restructured to directory format.

**Phases 11-17 (remaining skills):** Apply same patterns to pcode, vcode, commit, pr, handover, takeover, new_project.

## Current State Analysis

**Current `rcode.md` (193 lines):**
- Good workflow: decompose question → spawn parallel agents → synthesize → write document
- Has guidelines but lacks enforcement discipline
- No Iron Law preventing shortcuts (e.g., answering without research)
- No Red Flags or Rationalization Prevention

**Current `icode.md` (120 lines):**
- Basic workflow: read plan → implement phases → verify → update checkboxes
- Has verification approach but lacks enforcement discipline
- No Iron Law, Gate Functions, Red Flags, or Rationalization Prevention
- Doesn't prevent common failure modes (claiming done without evidence, skipping verification)

**Key patterns to adapt from Superpowers:**
- `verification-before-completion/SKILL.md` - Gate Function, Red Flags, Claim→Evidence mapping
- `executing-plans/SKILL.md` - Batch execution, stop conditions, REQUIRED SUB-SKILL pattern

## Desired End State

**All skills will have:**
1. Directory structure: `newskills/skillname/SKILL.md`
2. Iron Law stating the non-negotiable rule
3. Gate Function with numbered steps and clear trigger/terminator
4. Red Flags section with warning signs
5. Rationalization Prevention table with excuse counters
6. Spirit vs Letter clause to prevent rephrasing bypass
7. The Bottom Line closing emphasis

**Skill-Specific Iron Laws:**

| Skill | Iron Law |
|-------|----------|
| rcode | NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST |
| icode | NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE |
| pcode | NO PLAN WITHOUT CODEBASE RESEARCH FIRST |
| vcode | NO VERDICT WITHOUT FRESH EVIDENCE |
| commit | NO COMMIT WITHOUT STAGED FILE VERIFICATION |
| pr | NO PR WITHOUT FULL BRANCH ANALYSIS |
| handover | NO HANDOVER WITHOUT KEY LEARNINGS |
| takeover | NO WORK WITHOUT STATE VERIFICATION |
| new_project | (interactive workflow - lighter enforcement) |

**Verification:** Each enhanced skill should feel as rigorous as `verification-before-completion/SKILL.md`.

## What We're NOT Doing

- NOT changing the core workflow logic - only adding enforcement layers
- NOT adding supporting files yet (anti-patterns, examples) - SKILL.md only for now
- NOT modifying agent files in `newagents/` - skills only in this plan

## Implementation Approach

Add enforcement patterns as new sections while preserving existing workflows. Follow Superpowers section ordering:
1. Overview (with Spirit vs Letter clause)
2. Iron Law
3. Gate Function
4. Core Process (existing workflow, enhanced)
5. Red Flags
6. Rationalization Prevention
7. Guidelines/Remember section

**Execution order:** rcode first (Phases 1-4), then icode (Phases 5-10). This lets us test the patterns on rcode before applying to icode.

---

# Part 1: rcode Enforcement Patterns

---

## Phase 1: rcode - Add Iron Law and Spirit vs Letter Clause

### Overview
Establish the non-negotiable rule for research: no answering without spawning research agents first.

### Changes Required:

#### 1. Add Spirit vs Letter clause after Overview
**File**: `newskills/rcode.md`
**Location**: After line 8 (after "spawning parallel sub-agents and synthesizing their findings.")

```markdown

**Violating the letter of these rules is violating the spirit of these rules.**
```

#### 2. Add Iron Law section
**File**: `newskills/rcode.md`
**Location**: After "## Your Role" section (after line 17), before "## Initial Response"

```markdown

## The Iron Law

```
NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST
```

If you haven't spawned research agents and waited for their results, you cannot synthesize findings.

**No exceptions:**
- Don't answer from memory - spawn agents to verify
- Don't skip agents for "simple" questions - simple questions have complex answers
- Don't synthesize partial results - wait for ALL agents to complete
- Don't guess at file locations - let agents find them
```

### Success Criteria:
- [x] `grep -c "Iron Law" newskills/rcode.md` returns 1
- [x] `grep -c "Violating the letter" newskills/rcode.md` returns 1
- [x] `grep -c "NO SYNTHESIS WITHOUT" newskills/rcode.md` returns 1

---

## Phase 2: rcode - Add Gate Function

### Overview
Add the verification protocol that must be followed before synthesizing findings.

### Changes Required:

#### 1. Add Gate Function section
**File**: `newskills/rcode.md`
**Location**: After Iron Law section, before "## Initial Response"

```markdown

## The Gate Function

```
BEFORE synthesizing findings or writing the research document:

1. IDENTIFY: What aspects of the question need investigation?
2. SPAWN: Create parallel agents for each aspect (minimum 2 agents)
3. WAIT: All agents must complete before proceeding
4. VERIFY: Did agents return file:line references?
   - If NO: Spawn follow-up agents to get specific references
   - If YES: Proceed to synthesis
5. ONLY THEN: Synthesize findings with evidence

Skipping steps = guessing, not researching
```

## Evidence Requirements

Research findings must include:
- Specific file paths with line numbers (`file.ts:45-67`)
- Actual code patterns found (not assumed)
- Cross-references between components

**Not acceptable:**
- "The codebase likely has..."
- "Based on typical patterns..."
- "I believe there is..."
```

### Success Criteria:
- [x] `grep -c "Gate Function" newskills/rcode.md` returns 1
- [x] `grep -c "BEFORE synthesizing" newskills/rcode.md` returns 1
- [x] `grep -c "Evidence Requirements" newskills/rcode.md` returns 1

---

## Phase 3: rcode - Add Red Flags and Rationalization Prevention

### Overview
Add warning signs and excuse counters for research shortcuts.

### Changes Required:

#### 1. Add Red Flags section
**File**: `newskills/rcode.md`
**Location**: After "## Important Guidelines" section (after line 170)

```markdown

## Red Flags - STOP and Spawn Agents

If you notice any of these, STOP immediately:

- About to answer without spawning any agents
- Using "likely", "probably", "typically" about the codebase
- Describing patterns without file:line references
- Synthesizing before all agents have returned
- Answering based on similar codebases you've seen
- Feeling like the question is "too simple" for agents
- About to write research document without agent results

**When you hit a red flag:**
1. Stop and acknowledge the shortcut
2. Spawn the appropriate agents
3. Wait for results
4. Only then continue

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your knowledge is stale. Spawn agents. Verify. |
| "This is a simple question" | Simple questions have complex answers. Research. |
| "Agents take too long" | Wrong answers take longer to fix. Wait. |
| "I can see the pattern" | Patterns need evidence. Find file:line refs. |
| "The user is in a hurry" | Wrong research wastes more time. Be thorough. |
| "I'll just check one file" | One file isn't research. Spawn parallel agents. |
| "Similar to another project" | This codebase is unique. Verify everything. |
```

### Success Criteria:
- [x] `grep -c "Red Flags" newskills/rcode.md` returns 1
- [x] `grep -c "STOP and Spawn" newskills/rcode.md` returns 1
- [x] `grep -c "Rationalization Prevention" newskills/rcode.md` returns 1

---

## Phase 4: rcode - Add Bottom Line and Enhance Guidelines

### Overview
Add closing emphasis and strengthen existing guidelines.

### Changes Required:

#### 1. Add The Bottom Line section
**File**: `newskills/rcode.md`
**Location**: At the very end of the file

```markdown

## The Bottom Line

**No shortcuts for research.**

Spawn the agents. Wait for results. Cite file:line references. THEN synthesize.

This is non-negotiable. Every question. Every time.
```

#### 2. Update "Be Accurate" guideline
**File**: `newskills/rcode.md`
**Location**: In "## Important Guidelines" section, item 3 (around line 162)

**Current:**
```markdown
3. **Be Accurate**
   - Verify findings against actual code
   - Don't guess - investigate
   - Note uncertainties clearly
```

**Replace with:**
```markdown
3. **Be Accurate**
   - Verify findings against actual code via agents
   - Don't guess - spawn agents to investigate
   - Every claim needs a file:line reference
   - Note uncertainties clearly and spawn follow-up agents
```

### Success Criteria:
- [x] `grep -c "The Bottom Line" newskills/rcode.md` returns 1
- [x] `grep -c "non-negotiable" newskills/rcode.md` returns 1
- [x] `grep -c "spawn agents to investigate" newskills/rcode.md` returns 1

---

# Part 2: icode Enforcement Patterns

---

## Phase 5: icode - Add Iron Law and Spirit vs Letter Clause

### Overview
Establish the non-negotiable rule and prevent rephrasing bypass.

### Changes Required:

#### 1. Add Spirit vs Letter clause after Overview
**File**: `newskills/icode.md`
**Location**: After line 8 (after "These plans contain phases with specific changes and success criteria.")

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**
```

#### 2. Add Iron Law section
**File**: `newskills/icode.md`
**Location**: After the Spirit vs Letter clause, before "## Getting Started"

```markdown
## The Iron Law

```
NO PHASE COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification commands in this response, you cannot claim the phase is complete.

**No exceptions:**
- Don't mark checkboxes without running verification
- Don't proceed to next phase without evidence
- Don't trust previous runs - run fresh
- Don't claim "should pass" - show it passes
```

### Success Criteria:
- [x] `grep -c "Iron Law" newskills/icode.md` returns 1
- [x] `grep -c "Violating the letter" newskills/icode.md` returns 1
- [x] `grep -c "NO PHASE COMPLETION" newskills/icode.md` returns 1

---

## Phase 6: icode - Add Gate Function

### Overview
Add the 5-step verification protocol that must be followed before any phase completion claim.

### Changes Required:

#### 1. Add Gate Function section
**File**: `newskills/icode.md`
**Location**: After Iron Law section, before "## Getting Started"

```markdown
## The Gate Function

```
BEFORE marking any phase complete or updating checkboxes:

1. IDENTIFY: What commands verify this phase's success criteria?
2. RUN: Execute each command (fresh, complete - not cached)
3. READ: Full output - exit codes, pass/fail counts, error messages
4. VERIFY: Does output confirm ALL phase requirements?
   - If NO: State what failed, fix before continuing
   - If YES: State completion WITH evidence (command + output summary)
5. ONLY THEN: Update the checkbox in the plan file

Skip any step = false completion claim
```

## Evidence Format

When completing a phase, show evidence:
```
Phase 1 complete.

Verification:
- `npm test`: 47/47 passing, exit 0
- `npm run typecheck`: no errors, exit 0
- `npm run lint`: 0 warnings, exit 0

✓ All success criteria met. Proceeding to Phase 2...
```

**Not acceptable:**
- "Tests should pass now"
- "I've implemented the changes"
- "Phase complete" (without evidence)
```

### Success Criteria:
- [x] `grep -c "Gate Function" newskills/icode.md` returns 1
- [x] `grep -c "BEFORE marking any phase" newskills/icode.md` returns 1
- [x] `grep -c "Evidence Format" newskills/icode.md` returns 1

---

## Phase 7: icode - Add Red Flags Section

### Overview
Add warning signs that indicate the process is about to be violated.

### Changes Required:

#### 1. Add Red Flags section
**File**: `newskills/icode.md`
**Location**: After "## If You Get Stuck" section (around line 80)

```markdown
## Red Flags - STOP and Verify

If you notice any of these, STOP immediately:

- About to mark a checkbox without running verification
- Using "should", "probably", "seems to" about test results
- Saying "Done!" or "Complete!" before showing evidence
- Proceeding to next phase without verification output
- Trusting that previous verification is still valid
- Thinking "the change is simple, verification not needed"
- Feeling pressure to move faster
- About to commit without running full verification suite

**When you hit a red flag:**
1. Stop what you're doing
2. Run the Gate Function
3. Only proceed with evidence
```

### Success Criteria:
- [x] `grep -c "Red Flags" newskills/icode.md` returns 1
- [x] `grep -c "STOP and Verify" newskills/icode.md` returns 1
- [x] `grep -c "About to mark a checkbox" newskills/icode.md` returns 1

---

## Phase 8: icode - Add Rationalization Prevention Table

### Overview
Add excuse-reality table to counter common rationalizations.

### Changes Required:

#### 1. Add Rationalization Prevention section
**File**: `newskills/icode.md`
**Location**: After Red Flags section

```markdown
## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier" | Run them again. State changes. |
| "It's a simple change" | Simple changes break things. Verify. |
| "I'm confident it works" | Confidence ≠ evidence |
| "Verification takes too long" | Rework takes longer. Verify now. |
| "The plan said to do X, I did X" | Doing ≠ working. Prove it works. |
| "I'll verify at the end" | Errors compound. Verify each phase. |
| "Just this once" | No exceptions. |
| "I already showed evidence for similar code" | Each phase needs fresh evidence. |
```

### Success Criteria:
- [x] `grep -c "Rationalization Prevention" newskills/icode.md` returns 1
- [x] `grep -c "Confidence ≠ evidence" newskills/icode.md` returns 1

---

## Phase 9: icode - Enhance Existing Sections

### Overview
Update existing sections to reference the enforcement patterns and strengthen language.

### Changes Required:

#### 1. Update Execution Flow section
**File**: `newskills/icode.md`
**Location**: "## Execution Flow" section (around line 44)

**Current:**
```markdown
For each phase:

1. **Implement the changes** described in the plan
2. **Run automated verification** - execute the success criteria commands
3. **Fix any failures** before proceeding
4. **Update checkboxes** in the plan file using Edit
5. **Move to the next phase** immediately
```

**Replace with:**
```markdown
For each phase:

1. **Implement the changes** described in the plan
2. **Run the Gate Function** - IDENTIFY, RUN, READ, VERIFY (see above)
3. **Fix any failures** - do not proceed until verification passes
4. **Show evidence** - state what commands you ran and their output
5. **Update checkboxes** in the plan file using Edit
6. **Move to the next phase** - only after evidence is shown

**Remember:** Step 4 (show evidence) is not optional. No evidence = no completion.
```

#### 2. Update Verification Approach section
**File**: `newskills/icode.md`
**Location**: "## Verification Approach" section (around line 56)

**Current:**
```markdown
After implementing each phase:
- Run the success criteria checks (tests, linting, type checking)
- If tests fail, debug and fix before proceeding
- Update your progress in both the plan and your todos
- Check off completed items in the plan file itself using Edit
```

**Replace with:**
```markdown
After implementing each phase, follow the Gate Function:

1. **IDENTIFY** the verification commands from the plan's success criteria
2. **RUN** each command fresh (don't trust cached results)
3. **READ** full output:
   - Exit codes (0 = success)
   - Pass/fail counts
   - Error messages or warnings
4. **VERIFY** all criteria are met
5. **SHOW EVIDENCE** in your response before updating checkboxes

If any check fails:
- Do NOT update checkboxes
- Do NOT proceed to next phase
- Debug and fix the issue
- Re-run ALL verification commands
- Only then continue
```

#### 3. Update Completion section
**File**: `newskills/icode.md`
**Location**: "## Completion" section (around line 91)

**Current example output - update to include evidence:**
```markdown
When all phases are complete:
```
Implementation complete!

All phases executed:
- [x] Phase 1: [name]
- [x] Phase 2: [name]
- [x] Phase 3: [name]

Final verification (fresh run):
- `[test command]`: [X]/[X] passing, exit 0
- `[lint command]`: 0 errors, exit 0
- `[typecheck command]`: no errors, exit 0

All success criteria verified with evidence above.
The plan at `.docs/plans/[filename].md` has been fully implemented.
```
```

### Success Criteria:
- [x] `grep -c "Run the Gate Function" newskills/icode.md` returns 1
- [x] `grep -c "SHOW EVIDENCE" newskills/icode.md` returns 1
- [x] `grep -c "Final verification (fresh run)" newskills/icode.md` returns 1

---

## Phase 10: icode - Add Bottom Line and Integration

### Overview
Add closing emphasis and workflow context with REQUIRED SUB-SKILL pattern.

### Changes Required:

#### 1. Add The Bottom Line section
**File**: `newskills/icode.md`
**Location**: At the end of the file, before "## Workflow Context"

```markdown
## The Bottom Line

**No shortcuts for verification.**

Run the commands. Read the output. Show the evidence. THEN claim completion.

This is non-negotiable. Every phase. Every time.
```

#### 2. Update Workflow Context with skill references
**File**: `newskills/icode.md`
**Location**: "## Workflow Context" section (end of file)

**Replace with:**
```markdown
## Workflow Integration

**REQUIRED:** Apply verification-before-completion discipline throughout.

Typical workflow:
1. `/pcode` - Create the plan
2. `/icode` - Implement the plan (you are here)
3. `/vcode` - Validate implementation (additional verification layer)
4. `/commit` - Commit changes
5. `/pr` - Create pull request

**After all phases complete:**
- Run `/vcode` to get independent validation
- Only then proceed to `/commit`
```

### Success Criteria:
- [x] `grep -c "The Bottom Line" newskills/icode.md` returns 1
- [x] `grep -c "non-negotiable" newskills/icode.md` returns 1
- [x] `grep -c "REQUIRED:" newskills/icode.md` returns 1

---

# Part 3: Remaining Skills

---

## Phase 11: pcode - Add Enforcement Patterns and Restructure

### Overview
Add enforcement patterns to pcode (planning skill) and restructure to directory format. The Iron Law ensures research happens before planning.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/pcode
mv newskills/pcode.md newskills/pcode/SKILL.md
```

#### 2. Add Spirit vs Letter clause
**File**: `newskills/pcode/SKILL.md`
**Location**: After line 8 (after overview paragraph)

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**
```

#### 3. Add Iron Law section
**File**: `newskills/pcode/SKILL.md`
**Location**: After Spirit vs Letter clause, before "## Initial Response"

```markdown
## The Iron Law

```
NO PLAN WITHOUT CODEBASE RESEARCH FIRST
```

If you haven't spawned research agents and read the results, you cannot write the plan.

**No exceptions:**
- Don't plan from memory - spawn code-locator and code-analyzer agents
- Don't skip research for "simple" changes - simple changes touch complex systems
- Don't assume patterns - verify them in THIS codebase
- Don't write the plan before ALL research agents complete
```

#### 4. Add Gate Function section
**File**: `newskills/pcode/SKILL.md`
**Location**: After Iron Law section

```markdown
## The Gate Function

```
BEFORE writing any implementation plan:

1. IDENTIFY: What aspects of the codebase need investigation?
2. SPAWN: Create parallel research agents (minimum 2: code-locator + code-analyzer)
3. WAIT: All agents must complete before proceeding
4. READ: Read ALL files identified by agents into main context
5. VERIFY: Do you have file:line references for integration points?
   - If NO: Spawn follow-up agents to get specific references
   - If YES: Proceed to planning
6. ONLY THEN: Write the implementation plan

Skipping steps = planning blind
```
```

#### 5. Add Red Flags section
**File**: `newskills/pcode/SKILL.md`
**Location**: After "## Important Guidelines" section

```markdown
## Red Flags - STOP and Research First

If you notice any of these, STOP immediately:

- About to write plan without spawning research agents
- Using "typically", "usually", "in most codebases" about THIS codebase
- Planning integration points without file:line references
- Assuming directory structure without verification
- Thinking "I remember where this is"
- Feeling like research "takes too long"
- Planning based on similar projects, not THIS codebase

**When you hit a red flag:**
1. Stop and acknowledge the assumption
2. Spawn the appropriate research agents
3. Wait for results and read the files
4. Only then continue planning

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your knowledge is stale. Spawn agents. Verify. |
| "This is a simple change" | Simple changes touch complex systems. Research integration points. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |
| "User gave detailed requirements" | Users know what they want, not how the code works. Verify. |
| "I've done this in other projects" | THIS codebase has its own patterns. Find them. |
| "Let me just start and adjust" | Planning prevents false starts. Research first. |
```

#### 6. Add The Bottom Line
**File**: `newskills/pcode/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**No shortcuts for planning.**

Spawn the agents. Wait for results. Read the files. Cite file:line references. THEN plan.

This is non-negotiable. Every plan. Every time.
```

### Success Criteria:
- [ ] `ls newskills/pcode/SKILL.md` - file exists in directory format
- [ ] `grep -c "Iron Law" newskills/pcode/SKILL.md` returns 1+
- [ ] `grep -c "Gate Function" newskills/pcode/SKILL.md` returns 1
- [ ] `grep -c "Red Flags" newskills/pcode/SKILL.md` returns 1
- [ ] `grep -c "Rationalization Prevention" newskills/pcode/SKILL.md` returns 1
- [ ] `grep -c "The Bottom Line" newskills/pcode/SKILL.md` returns 1
- [ ] `grep -c "NO PLAN WITHOUT" newskills/pcode/SKILL.md` returns 1

---

## Phase 12: vcode - Add Two-Stage Review and Restructure

### Overview
Add enforcement patterns to vcode (validation skill) with two-stage review pattern from Superpowers. Restructure to directory format.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/vcode
mv newskills/vcode.md newskills/vcode/SKILL.md
```

#### 2. Add Spirit vs Letter clause and Iron Law
**File**: `newskills/vcode/SKILL.md`
**Location**: After overview paragraph

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO VERDICT WITHOUT FRESH EVIDENCE
```

If you haven't run verification commands in this response, you cannot claim pass or fail.

**No exceptions:**
- Don't trust previous test runs - run fresh
- Don't trust icode's evidence - verify independently
- Don't extrapolate from partial checks - run everything
- Don't say "should work" - show it works
```

#### 3. Add Two-Stage Gate Function
**File**: `newskills/vcode/SKILL.md`
**Location**: After Iron Law section

```markdown
## The Gate Function: Two-Stage Review

Validation happens in TWO sequential stages. Do not skip or combine.

### Stage 1: Spec Compliance (REQUIRED FIRST)

```
BEFORE checking code quality:

1. READ: The implementation plan FULLY
2. LIST: All phase requirements and success criteria
3. READ: The actual implementation files
4. COMPARE: Line by line - what was requested vs what was built
5. VERDICT: For each requirement:
   - ✓ Implemented correctly
   - ✗ Missing
   - ⚠️ Partial or different

Do NOT proceed to Stage 2 until Stage 1 is complete and documented.
```

### Stage 2: Code Quality (ONLY AFTER STAGE 1)

```
AFTER spec compliance passes:

1. IDENTIFY: What verification commands to run?
2. RUN: Execute each command (tests, lint, typecheck)
3. READ: Full output - exit codes, pass/fail counts
4. VERIFY: Does output confirm all criteria?
5. DOCUMENT: Show evidence for each check

Skip any step = incomplete validation
```
```

#### 4. Add Red Flags and Rationalization Prevention
**File**: `newskills/vcode/SKILL.md`
**Location**: After two-stage sections

```markdown
## Red Flags - STOP and Verify

If you notice any of these, STOP immediately:

- Skipping Stage 1 and jumping straight to tests
- Trusting icode's verification output
- Using "should pass", "looks correct", "seems fine"
- About to give verdict without running commands
- Combining stages to "save time"
- Partial verification ("tests pass, so it works")

**When you hit a red flag:**
1. Stop and acknowledge the shortcut
2. Complete BOTH stages fully
3. Show evidence for each

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "icode already verified" | Verify independently. Trust but verify. |
| "Tests pass = spec met" | Tests prove behavior, not requirements. Check both. |
| "Stage 1 is obvious" | Compare requirements line by line. Document findings. |
| "I can do both stages together" | Sequential stages catch different issues. Do both. |
| "It's the same codebase I just read" | Fresh verification catches state changes. |
| "Just need to check the important parts" | Partial verification proves nothing. Full check. |
```

#### 5. Add The Bottom Line
**File**: `newskills/vcode/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**No shortcuts for validation.**

Stage 1: Check spec compliance. Stage 2: Check code quality. Show evidence for both.

This is non-negotiable. Every validation. Every time.
```

### Success Criteria:
- [ ] `ls newskills/vcode/SKILL.md` - file exists in directory format
- [ ] `grep -c "Two-Stage" newskills/vcode/SKILL.md` returns 1+
- [ ] `grep -c "Stage 1" newskills/vcode/SKILL.md` returns 2+
- [ ] `grep -c "Stage 2" newskills/vcode/SKILL.md` returns 2+
- [ ] `grep -c "NO VERDICT WITHOUT" newskills/vcode/SKILL.md` returns 1
- [ ] `grep -c "Rationalization Prevention" newskills/vcode/SKILL.md` returns 1

---

## Phase 13: commit - Add Verification Enforcement and Restructure

### Overview
Add enforcement patterns to commit skill. Focus on staged file verification and preventing accidental sensitive file commits.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/commit
mv newskills/commit.md newskills/commit/SKILL.md
```

#### 2. Add Spirit vs Letter clause and Iron Law
**File**: `newskills/commit/SKILL.md`
**Location**: After overview paragraph

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO COMMIT WITHOUT STAGED FILE VERIFICATION
```

If you haven't reviewed what you're staging and why, you cannot commit.

**No exceptions:**
- Don't use `git add -A` or `git add .` - stage specific files
- Don't commit without understanding the diff
- Don't stage sensitive files (.env, credentials, keys)
- Don't assume previous state - check fresh
```

#### 3. Add Gate Function
**File**: `newskills/commit/SKILL.md`
**Location**: After Iron Law section

```markdown
## The Gate Function

```
BEFORE running git commit:

1. STATUS: Run `git status` to see current state
2. DIFF: Run `git diff` to understand changes
3. REVIEW: Identify logical groups of changes
4. STAGE: Add SPECIFIC files (never -A or .)
5. VERIFY: Check for sensitive files in staging
   - If .env, credentials, keys found: STOP and unstage
6. ONLY THEN: Commit with clear message

Skip any step = risky commit
```
```

#### 4. Add Red Flags and Rationalization Prevention
**File**: `newskills/commit/SKILL.md`
**Location**: Before existing "## Important Rules" section

```markdown
## Red Flags - STOP and Review

If you notice any of these, STOP immediately:

- About to use `git add -A` or `git add .`
- Staging files you haven't reviewed
- Committing without understanding the diff
- .env, credentials, or keys in staged files
- About to force push
- Feeling rushed to commit

**When you hit a red flag:**
1. Stop and run `git status`
2. Unstage suspicious files
3. Review the diff carefully
4. Stage specific files only

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what changed" | Run git diff anyway. Verify. |
| "`git add .` is faster" | Faster to commit wrong files too. Stage specifically. |
| "It's just this once" | One wrong commit can leak secrets. Never. |
| ".env is in .gitignore" | Check anyway. Gitignore can have holes. |
| "I need to push quickly" | Fast mistakes take longer to fix. Take time. |
```

#### 5. Add The Bottom Line
**File**: `newskills/commit/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**No shortcuts for committing.**

Check status. Review diff. Stage specific files. Verify no secrets. THEN commit.

This is non-negotiable. Every commit. Every time.
```

### Success Criteria:
- [ ] `ls newskills/commit/SKILL.md` - file exists in directory format
- [ ] `grep -c "Iron Law" newskills/commit/SKILL.md` returns 1+
- [ ] `grep -c "Gate Function" newskills/commit/SKILL.md` returns 1
- [ ] `grep -c "Red Flags" newskills/commit/SKILL.md` returns 1
- [ ] `grep -c "NO COMMIT WITHOUT" newskills/commit/SKILL.md` returns 1

---

## Phase 14: pr - Add Branch Analysis Enforcement and Restructure

### Overview
Add enforcement patterns to pr skill. Focus on analyzing ALL commits, not just the latest.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/pr
mv newskills/pr.md newskills/pr/SKILL.md
```

#### 2. Add Spirit vs Letter clause and Iron Law
**File**: `newskills/pr/SKILL.md`
**Location**: After overview paragraph

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PR WITHOUT FULL BRANCH ANALYSIS
```

If you haven't analyzed ALL commits on this branch, you cannot write the PR description.

**No exceptions:**
- Don't describe just the latest commit - analyze the full branch
- Don't create PR without user confirmation
- Don't include AI attribution in description
- Don't skip the diff review
```

#### 3. Add Gate Function
**File**: `newskills/pr/SKILL.md`
**Location**: After Iron Law section

```markdown
## The Gate Function

```
BEFORE creating any pull request:

1. BRANCH: Identify current branch and base branch
2. COMMITS: Run `git log base..HEAD` to see ALL commits
3. DIFF: Run `git diff base..HEAD` to see full changes
4. ANALYZE: Understand the PURPOSE across all commits
5. DRAFT: Write title and description covering FULL scope
6. CONFIRM: Show draft to user and wait for approval
7. ONLY THEN: Create the PR with `gh pr create`

Skip any step = incomplete PR
```
```

#### 4. Add Red Flags and Rationalization Prevention
**File**: `newskills/pr/SKILL.md`
**Location**: Before existing "## Important Rules" section

```markdown
## Red Flags - STOP and Analyze

If you notice any of these, STOP immediately:

- About to describe only the latest commit
- Creating PR without showing draft to user
- Including "Generated with Claude" or similar
- Branch not pushed to remote
- Skipping the full diff review

**When you hit a red flag:**
1. Stop and run full branch analysis
2. Review ALL commits, not just recent
3. Draft description and get confirmation
4. Only then create PR

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just one commit" | Check anyway. Branch history matters. |
| "User knows what changed" | PR is for reviewers. Describe fully. |
| "Description can be edited later" | Get it right first. Draft and confirm. |
| "I'll just use the commit message" | Commits are granular. PR describes the whole. |
```

#### 5. Add The Bottom Line
**File**: `newskills/pr/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**No shortcuts for PRs.**

Analyze all commits. Review full diff. Draft description. Get confirmation. THEN create.

This is non-negotiable. Every PR. Every time.
```

### Success Criteria:
- [ ] `ls newskills/pr/SKILL.md` - file exists in directory format
- [ ] `grep -c "Iron Law" newskills/pr/SKILL.md` returns 1+
- [ ] `grep -c "Gate Function" newskills/pr/SKILL.md` returns 1
- [ ] `grep -c "NO PR WITHOUT" newskills/pr/SKILL.md` returns 1

---

## Phase 15: handover - Add Learnings Enforcement and Restructure

### Overview
Add enforcement patterns to handover skill. Focus on capturing key learnings, not just status.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/handover
mv newskills/handover.md newskills/handover/SKILL.md
```

#### 2. Add Spirit vs Letter clause and Iron Law
**File**: `newskills/handover/SKILL.md`
**Location**: After overview paragraph

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO HANDOVER WITHOUT KEY LEARNINGS
```

If you haven't captured what you learned (not just what you did), the handover is incomplete.

**No exceptions:**
- Don't just list tasks - capture insights
- Don't skip learnings because "nothing special happened"
- Don't hand over without file:line references
- Don't assume the next session knows anything
```

#### 3. Add Gate Function
**File**: `newskills/handover/SKILL.md`
**Location**: After Iron Law section

```markdown
## The Gate Function

```
BEFORE writing the handover document:

1. REVIEW: What tasks were worked on?
2. EXTRACT: What were the KEY LEARNINGS?
   - Patterns discovered
   - Gotchas encountered
   - Decisions made and WHY
3. REFERENCE: What file:line locations matter?
4. PRIORITIZE: What should the next session do FIRST?
5. VERIFY: Is "Key Learnings" section substantive?
   - If NO: Think harder - every session teaches something
   - If YES: Proceed to write
6. ONLY THEN: Write the handover document

Skip learnings = useless handover
```
```

#### 4. Add Red Flags and Rationalization Prevention
**File**: `newskills/handover/SKILL.md`
**Location**: Before existing "## Guidelines" section

```markdown
## Red Flags - STOP and Extract Learnings

If you notice any of these, STOP immediately:

- Key Learnings section is empty or generic
- Writing "nothing special to note"
- Listing only tasks without insights
- No file:line references in the handover
- Handover reads like a status report, not a knowledge transfer

**When you hit a red flag:**
1. Stop and reflect on the session
2. What would you tell a colleague taking over?
3. What mistakes should they avoid?
4. Add these insights to Key Learnings

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Nothing special happened" | Every session teaches something. Find it. |
| "Next session can figure it out" | That wastes time. Capture it now. |
| "It's all in the code" | Context and reasoning aren't in code. Document. |
| "I'm in a hurry" | Hurried handovers cause rework. Take time. |
```

#### 5. Add The Bottom Line
**File**: `newskills/handover/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**No shortcuts for handover.**

Distill the learnings. Cite file:line references. Write for someone with zero context.

This is non-negotiable. Every handover. Every time.
```

### Success Criteria:
- [ ] `ls newskills/handover/SKILL.md` - file exists in directory format
- [ ] `grep -c "Iron Law" newskills/handover/SKILL.md` returns 1+
- [ ] `grep -c "Key Learnings" newskills/handover/SKILL.md` returns 2+
- [ ] `grep -c "NO HANDOVER WITHOUT" newskills/handover/SKILL.md` returns 1

---

## Phase 16: takeover - Add State Verification Enforcement and Restructure

### Overview
Add enforcement patterns to takeover skill. Focus on verifying state before starting work.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/takeover
mv newskills/takeover.md newskills/takeover/SKILL.md
```

#### 2. Add Spirit vs Letter clause and Iron Law
**File**: `newskills/takeover/SKILL.md`
**Location**: After overview paragraph

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO WORK WITHOUT STATE VERIFICATION
```

If you haven't verified the current state matches the handover, you cannot start working.

**No exceptions:**
- Don't trust the handover blindly - verify state
- Don't skip reading linked docs
- Don't start work before confirming approach with user
- Don't ignore drift between handover and reality
```

#### 3. Add Gate Function
**File**: `newskills/takeover/SKILL.md`
**Location**: After Iron Law section

```markdown
## The Gate Function

```
BEFORE starting any work from a handover:

1. READ: The handover document FULLY
2. READ: All linked plans and research docs
3. VERIFY: Run `git status`, `git log -5`, check file existence
4. COMPARE: Does reality match the handover?
   - If NO: Note the differences, ask user how to proceed
   - If YES: Continue to step 5
5. ABSORB: Internalize the Key Learnings section
6. CONFIRM: Present summary and get user approval
7. ONLY THEN: Begin work

Skip verification = working blind
```
```

#### 4. Add Red Flags and Rationalization Prevention
**File**: `newskills/takeover/SKILL.md`
**Location**: Before existing "## Guidelines" section

```markdown
## Red Flags - STOP and Verify

If you notice any of these, STOP immediately:

- Starting work without reading full handover
- Skipping linked documents
- Not running `git status` to verify state
- State doesn't match handover but continuing anyway
- Ignoring Key Learnings section
- Starting work without user confirmation

**When you hit a red flag:**
1. Stop and read the handover fully
2. Verify state with git commands
3. Note any differences
4. Get user confirmation before proceeding

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I read the summary" | Read the full handover. Details matter. |
| "State probably hasn't changed" | Verify anyway. Time passes. Things change. |
| "I'll check files as I go" | Upfront verification prevents wasted work. |
| "User is waiting" | Wrong assumptions waste more time. Verify first. |
```

#### 5. Add The Bottom Line
**File**: `newskills/takeover/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**No shortcuts for takeover.**

Read everything. Verify state. Apply learnings. Get confirmation. THEN work.

This is non-negotiable. Every takeover. Every time.
```

### Success Criteria:
- [ ] `ls newskills/takeover/SKILL.md` - file exists in directory format
- [ ] `grep -c "Iron Law" newskills/takeover/SKILL.md` returns 1+
- [ ] `grep -c "Gate Function" newskills/takeover/SKILL.md` returns 1
- [ ] `grep -c "NO WORK WITHOUT" newskills/takeover/SKILL.md` returns 1

---

## Phase 17: new_project - Light Enforcement and Restructure

### Overview
Add lighter enforcement patterns to new_project skill. This is an interactive workflow so heavy enforcement is less appropriate.

### Changes Required:

#### 1. Create directory structure
```bash
mkdir -p newskills/new_project
mv newskills/new_project.md newskills/new_project/SKILL.md
```

#### 2. Add Spirit vs Letter clause (lighter enforcement)
**File**: `newskills/new_project/SKILL.md`
**Location**: After overview paragraph

```markdown
**Violating the letter of these rules is violating the spirit of these rules.**

## Key Principles

This is an interactive workflow, so enforcement is lighter. But these principles apply:

1. **Research before recommending** - Spawn web-search agents for current best practices
2. **Confirm before writing** - Get user approval at each phase
3. **Keep CLAUDE.md minimal** - Under 60 lines, universally applicable
4. **Adapt to answers** - Skip irrelevant questions, add needed ones
```

#### 3. Add Red Flags (lighter version)
**File**: `newskills/new_project/SKILL.md`
**Location**: After "## Important Guidelines" section

```markdown
## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- Recommending tools without researching current best practices
- Writing CLAUDE.md over 60 lines
- Including code style rules in CLAUDE.md (use linters)
- Skipping user confirmation at major decision points
- Assuming technology choices without asking

**When you hit a red flag:**
1. Stop and consider the principle being violated
2. Research if needed
3. Ask user if unsure
4. Proceed with confirmation
```

#### 4. Add The Bottom Line
**File**: `newskills/new_project/SKILL.md`
**Location**: At the end of the file

```markdown
## The Bottom Line

**Interactive, but principled.**

Research best practices. Confirm decisions. Keep CLAUDE.md minimal. Adapt to the user.
```

### Success Criteria:
- [ ] `ls newskills/new_project/SKILL.md` - file exists in directory format
- [ ] `grep -c "Key Principles" newskills/new_project/SKILL.md` returns 1
- [ ] `grep -c "Red Flags" newskills/new_project/SKILL.md` returns 1
- [ ] `grep -c "The Bottom Line" newskills/new_project/SKILL.md` returns 1

---

## Testing Strategy

### Manual Verification:

For each enhanced skill:
1. Read the enhanced SKILL.md end-to-end
2. Verify enforcement patterns are present and feel natural
3. Test by invoking the skill on a real task

### Automated Checks:

```bash
# Verify all skills are in directory format
ls -la newskills/*/SKILL.md

# Check each skill has required patterns
for skill in rcode icode pcode vcode commit pr handover takeover; do
  echo "=== $skill ==="
  grep -c "Iron Law" newskills/$skill/SKILL.md
  grep -c "Gate Function" newskills/$skill/SKILL.md
  grep -c "Red Flags" newskills/$skill/SKILL.md
  grep -c "The Bottom Line" newskills/$skill/SKILL.md
done

# new_project has lighter enforcement
echo "=== new_project ==="
grep -c "Key Principles" newskills/new_project/SKILL.md
grep -c "Red Flags" newskills/new_project/SKILL.md
```

### Directory Structure Verification:

```bash
# Expected structure after all phases complete:
# newskills/
# ├── rcode/SKILL.md      (complete)
# ├── icode/SKILL.md      (complete)
# ├── pcode/SKILL.md
# ├── vcode/SKILL.md
# ├── commit/SKILL.md
# ├── pr/SKILL.md
# ├── handover/SKILL.md
# ├── takeover/SKILL.md
# └── new_project/SKILL.md
```

---

## Performance Considerations

None - this is a documentation/prompt file, not executable code.

---

## Migration Notes

None - this enhances an existing skill file in place. No data migration needed.

---

## References

- Research: `.docs/research/01-27-2026-superpowers-patterns-for-rpi-workflow.md`
- Pattern source: `C:/code/superpowers/skills/verification-before-completion/SKILL.md`
- Pattern source: `C:/code/superpowers/skills/executing-plans/SKILL.md`
- Pattern source: `C:/code/superpowers/skills/subagent-driven-development/SKILL.md` (two-stage review)
- Target directory: `newskills/*/SKILL.md` (all skills in directory format)

---

## Next Steps After This Plan

1. **Complete Phases 11-17** - Enhance and restructure remaining skills
2. **Deploy all skills** to `~/.claude/skills/` for global availability
3. **Test each skill** with real tasks in the testbed
4. **Iterate** based on friction points discovered during use
5. **Consider session-start hook** to inject RPI workflow rules (from research Part 6)
6. **Add supporting files** (anti-patterns, examples) to skill directories as needed
