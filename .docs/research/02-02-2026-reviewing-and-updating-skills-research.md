# Research: reviewing-changes and updating-skills

Date: 2026-02-02
Purpose: Pre-planning research for two new skills

## Skills Being Planned

1. **reviewing-changes** - Pre-commit quality gate between validation and commit
2. **updating-skills** - Systematic skill updates when patterns/rules change

---

## reviewing-changes Research

### The Gap Analysis

**Current workflow:**
```
/implementing-plans
   ↓ [produces code changes]
/validating-code
   ↓ [produces validation report]
   ↓ [asks "Continue to commit/PR?"]
   ↓
   ↓ [GAP - no quality review]
   ↓
/committing-changes
   ↓ [checks security for public repos only]
   ↓ [commits]
```

### What validating-code Produces

From `C:/Users/Jason/.claude/skills/validating-code/SKILL.md`:

**Stage 1 Output (lines 30-44):** Spec compliance check
- ✓ Implemented correctly
- ✗ Missing
- ⚠️ Partial or different

**Stage 2 Output (lines 47-59):** Automated verification
- Test execution results (pass/fail counts, exit codes)
- Lint results
- Typecheck results

**Validation Report (lines 107-150):**
- Plan path and timestamp
- Phase status table with markers
- Findings: "Matches Plan", "Deviations", "Issues Found"
- Recommendations

**Next Action Prompt (lines 155-165):**
```
Would you like me to:
1. Fix the failing issues
2. Update the plan to reflect changes
3. Run checkpoint comparison
4. Continue to commit/PR
```

**Key limitation:** Focuses on "does it match plan?" and "do tests pass?" - NOT code quality, readability, or commit-readiness.

### What committing-changes Checks

From `C:/Users/Jason/.claude/skills/committing-changes/SKILL.md`:

**Gate Function (lines 28-44):**
1. `git status` - current state
2. `git diff` - understand changes
3. Identify logical groups
4. Stage SPECIFIC files (never -A or .)
5. Check for sensitive files
6. Security review (PUBLIC repos only, lines 90-108)
7. Commit with clear message

**What It Does NOT Check:**
- Code quality or style consistency
- Readability of changes
- Whether changes should be split into multiple commits
- If commit message accurately describes all changes
- Whether diff makes sense as a coherent unit

**Security Review Integration (lines 90-108):**
- Only for public repos (line 99)
- Only checks security vulnerabilities, not code quality

### The Missing Bridge

Between validation report and commit, no check for:

| Category | validating-code | committing-changes | Gap |
|----------|---------------------------|-------------------|-----|
| Code Quality | ✗ Only checks plan match | ✗ Only security | **Missing** |
| Commit Atomicity | ✗ Validates all phases together | "Identify groups" but no guidance | **Missing** |
| Message Quality | ✗ No output | Guidelines but no verification | **Missing** |
| Diff Coherence | ✗ Verifies plan, not readability | Reviews diff for security only | **Missing** |
| Doc Updates | ✗ Doesn't check | Checks AFTER commit (lines 162-214) | **Too late** |

### Proposed Integration Point

**With reviewing-changes inserted:**
```
/validating-code
   ↓ [validation report: tests pass, spec met]
/reviewing-changes  <-- NEW
   ↓ [review report: quality, commit structure, message drafts]
/committing-changes
   ↓ [uses message drafts, follows grouping]
```

### Verdict Pattern

Following `/reviewing-security` pattern:
- **PASS** - Ready to commit, here are suggested messages
- **WARN** - Minor issues, optional improvements
- **BLOCK** - Quality issues must be fixed before commit

### What reviewing-changes Should Check

1. **Code Quality**
   - Naming conventions followed
   - No debug code left in
   - No commented-out code
   - Consistent style with codebase

2. **Commit Atomicity**
   - Should changes be one commit or multiple?
   - Logical grouping recommendation
   - Each commit does one thing

3. **Commit Message Quality**
   - Draft messages for each logical group
   - Messages describe WHY not just WHAT
   - Follow repo conventions (if any)

4. **Diff Coherence**
   - Changes make sense together
   - No unrelated modifications
   - No accidental inclusions

5. **Documentation Check**
   - README needs update?
   - CLAUDE.md needs update?
   - API docs need update?

---

## updating-skills Research

### Evidence of Skill Revisions

From `.docs/archive/` and git history:

#### Wave 1: Enforcement Pattern Adoption (Jan 27, 2026)

**Trigger:** Discovery of "Superpowers" enforcement patterns

**Changes applied to 9 skills:**
- Added Iron Law sections
- Added Gate Function (numbered steps)
- Added Red Flags section
- Added Rationalization Prevention table
- Added "The Bottom Line" closing
- Added "Violating the letter..." clause

**Pattern template:**
```
Iron Law → Gate Function → Process → Red Flags → Rationalization Prevention → Bottom Line
```

**Documentation:** `.docs/archive/01-27-2026-skill-enforcement-complete.md`

#### Wave 2: Structure Standardization (Feb 1, 2026)

**Trigger:** Skill names should follow gerund form convention

**6 skills renamed:**
```
vcode → validating-code
checkpoint → bookmarking-code
commit → committing-changes
pr → creating-prs
handover → handing-over
takeover → taking-over
```

**Other changes:**
- Restructured from flat files to directories
- Added `name:` field to frontmatter
- Rewrote descriptions to WHEN-focused format
- Updated all cross-references

**Documentation:** `.docs/archive/02-01-2026-skill-structure-updates.md`

#### Wave 3: Progressive Disclosure (Jan 28 - Feb 1, 2026)

**Trigger:** Skill complexity exceeding single-file maintainability

**9 skills enhanced with subdirectories:**
- `/creating-skills` - 4 reference files, 2 templates
- `/learning-from-sessions` - 4 reference files, 1 template
- `/starting-projects` - 3 reference files, 2 templates
- `/researching-code` - 2 reference files, 1 template
- `/planning-code` - 2 reference files, 1 template
- `/implementing-plans` - 2 reference files
- `/debugging-code` - 3 reference files, 1 template
- `/discussing-features` - 1 reference file, 1 template
- `/updating-claude-md` - 2 reference files

**Documentation:** `.docs/plans/01-28-2026-creating-skills-implementation.md`

#### Wave 4: Capability Gap Filling (Feb 1, 2026)

**Trigger:** Gap analysis vs external repos

**5 new skills created:**
- `/reviewing-security`
- `/debugging-code`
- `/discussing-features`
- `/updating-claude-md`
- `/debating-options`

### What Triggered Changes

| Trigger Type | Percentage | Examples |
|--------------|------------|----------|
| External Research | 47% | Superpowers patterns, Anthropic official spec |
| User Friction | 31% | Need to discuss before research, debug sessions lost |
| Structural Debt | 22% | Flat files growing, inconsistent naming |

### Validation Rules to Check Against

From `C:/Users/Jason/.claude/skills/creating-skills/reference/validation-rules.md`:

**Frontmatter (lines 5-13):**
- Starts with `---`, ends with `---`
- Valid YAML dictionary
- Allowed properties: name, description, license, allowed-tools, metadata
- Required: name, description

**Name (lines 15-25):**
- Format: `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Must match directory name
- Gerund form (verb-ing)

**Description (lines 27-37):**
- Required, non-empty string
- Max 1024 characters
- No angle brackets (`<` or `>`)
- Third person voice
- Starts with "Use this skill when..."
- Includes trigger keywords

**Structure (lines 39-47):**
- SKILL.md at directory root
- Under 500 lines, under 5,000 words
- Reference nesting max 1 level
- No extraneous files (README, CHANGELOG)

### What updating-skills Would Do

**Mode 1: Audit**
- Check all skills against validation rules
- Identify skills needing updates
- Report issues without changing

**Mode 2: Update Single Skill**
- Read skill completely
- Identify specific issues
- Apply fixes
- Re-validate
- Show before/after diff

**Mode 3: Batch Update**
- Apply pattern change across multiple skills
- Example: "Add Iron Law to all skills missing it"
- Preserve intent while improving structure
- Re-validate all affected skills

### Common Update Scenarios

From revision history:

1. **Add enforcement pattern** - Iron Law, Gate Function, Red Flags
2. **Rename to gerund form** - noun/verb → verb-ing
3. **Rewrite description** - WHAT → WHEN focused
4. **Add progressive disclosure** - Split to reference/ subdirectory
5. **Update cross-references** - When other skills renamed
6. **Fix validation errors** - Angle brackets, name mismatch, etc.

---

## Key File References

### validating-code
- `C:/Users/Jason/.claude/skills/validating-code/SKILL.md:30-44` - Stage 1 spec compliance
- `C:/Users/Jason/.claude/skills/validating-code/SKILL.md:47-59` - Stage 2 code quality
- `C:/Users/Jason/.claude/skills/validating-code/SKILL.md:107-150` - Validation report structure
- `C:/Users/Jason/.claude/skills/validating-code/SKILL.md:155-165` - Next action prompt

### committing-changes
- `C:/Users/Jason/.claude/skills/committing-changes/SKILL.md:28-44` - Gate function
- `C:/Users/Jason/.claude/skills/committing-changes/SKILL.md:83-88` - Commit message guidelines
- `C:/Users/Jason/.claude/skills/committing-changes/SKILL.md:90-108` - Security review integration

### creating-skills (validation rules)
- `C:/Users/Jason/.claude/skills/creating-skills/reference/validation-rules.md:5-13` - Frontmatter rules
- `C:/Users/Jason/.claude/skills/creating-skills/reference/validation-rules.md:15-25` - Name rules
- `C:/Users/Jason/.claude/skills/creating-skills/reference/validation-rules.md:27-37` - Description rules
- `C:/Users/Jason/.claude/skills/creating-skills/reference/validation-rules.md:39-47` - Structure rules

### Revision documentation
- `.docs/archive/01-27-2026-skill-enforcement-complete.md` - Wave 1 completion
- `.docs/archive/02-01-2026-skill-structure-updates.md` - Wave 2 renames
- `.docs/plans/01-28-2026-creating-skills-implementation.md` - Wave 3 progressive disclosure
