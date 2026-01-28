---
git_commit: 469a6d81ebb8b827e284d4afb090c6c622d97747
last_updated: 2026-01-27
last_updated_by: claude
topic: "Superpowers Patterns for RPI Workflow Adaptation"
tags: [research, superpowers, rpi-workflow, patterns, adaptation, skills-commands]
status: complete
references:
  - skills/test-driven-development/SKILL.md
  - skills/test-driven-development/testing-anti-patterns.md
  - skills/subagent-driven-development/SKILL.md
  - skills/subagent-driven-development/implementer-prompt.md
  - skills/subagent-driven-development/spec-reviewer-prompt.md
  - skills/subagent-driven-development/code-quality-reviewer-prompt.md
  - skills/verification-before-completion/SKILL.md
  - skills/writing-plans/SKILL.md
  - skills/systematic-debugging/SKILL.md
  - skills/brainstorming/SKILL.md
  - agents/code-reviewer.md
  - commands/brainstorm.md
  - hooks/hooks.json
  - hooks/session-start.sh
---

# Research: Superpowers Patterns for RPI Workflow Adaptation

**Date**: 2026-01-27
**Branch**: main

## Research Question

Review the Superpowers codebase for ideas that could be adapted to our rpi workflow (pcode/icode/rcode/vcode/commit/pr/handover/takeover).

## Summary

Superpowers is a comprehensive software development workflow plugin with sophisticated patterns for enforcing discipline, managing subagents, and ensuring quality. Key adaptable patterns include:

1. **Iron Laws + Gate Functions + Red Flags** - Three-tier discipline enforcement
2. **Two-Stage Sequential Review** - Spec compliance before code quality
3. **Rationalization Prevention Tables** - Pre-documented excuse counters
4. **Evidence-Based Verification** - IDENTIFY → RUN → READ → VERIFY → CLAIM
5. **Skill Cross-Reference System** - REQUIRED SUB-SKILL and REQUIRED BACKGROUND markers
6. **Hook-Based Context Injection** - Session start skill loading

---

## Part 1: Core Enforcement Patterns

### 1.1 Iron Law Pattern

**What it is:** A single, non-negotiable rule stated in ALL CAPS with zero exceptions.

**Exact structure from `skills/test-driven-development/SKILL.md:31-34`:**
```markdown
## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
```

**Found in 4 skills:**
- `test-driven-development/SKILL.md:31` - "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
- `systematic-debugging/SKILL.md:16` - "ALWAYS find root cause"
- `verification-before-completion/SKILL.md:16` - "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
- `writing-skills/SKILL.md:374` - Iron Law for skill documentation

**Enforcement language (from `test-driven-development/SKILL.md:37-45`):**
```markdown
Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.
```

**Key language patterns:**
- "No exceptions" - absolute statement
- "Delete means delete" - prevents reinterpretation
- "Period." - ends with finality

**How to adapt for RPI:**

| Command | Iron Law |
|---------|----------|
| **pcode** | NO PLAN WITHOUT CODEBASE RESEARCH FIRST |
| **icode** | NO PHASE COMPLETION WITHOUT VERIFICATION |
| **vcode** | NO VERDICT WITHOUT FRESH EVIDENCE |
| **rcode** | NO SYNTHESIS WITHOUT PARALLEL RESEARCH |

---

### 1.2 Gate Function Pattern

**What it is:** A numbered checklist that MUST be completed before any claim or action.

**Exact structure from `skills/verification-before-completion/SKILL.md:24-38`:**
```markdown
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

**Additional gate functions found:**

**From `testing-anti-patterns.md:51-61` (Mock Assertion Gate):**
```markdown
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

**From `testing-anti-patterns.md:151-175` (Mocking Gate):**
```markdown
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level
```

**Gate function structure:**
1. Trigger condition: "BEFORE [action]:"
2. Question checkpoint: "Ask: [reflection question]"
3. Conditional stop: "IF [condition]: STOP - [corrective action]"
4. Final directive: "ONLY THEN: [permitted action]"

**How to adapt for icode:**
```markdown
BEFORE marking any phase complete:

1. IDENTIFY: What commands verify this phase?
2. RUN: Execute each command (fresh, don't trust cache)
3. READ: Full output - exit code, pass/fail counts, warnings
4. VERIFY: Does output confirm phase requirements?
   - If NO: State what failed, fix before continuing
   - If YES: State completion WITH evidence
5. ONLY THEN: Mark phase complete

Skipping steps = false completion claim
```

---

### 1.3 Red Flags Pattern

**What it is:** A list of warning signs that indicate the process is about to be violated.

**Exact structure from `skills/test-driven-development/SKILL.md:272-288`:**
```markdown
## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

All of these mean: Delete code. Start over with TDD.
```

**From `skills/verification-before-completion/SKILL.md:52-61`:**
```markdown
## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**
```

**Pattern characteristics:**
- Header format: `## Red Flags - STOP and [Action]`
- Bulleted list of specific warning signs
- Includes quoted phrases that signal rationalization
- Final line states consequence of hitting any red flag

**How to adapt for pcode:**
```markdown
## Red Flags - STOP and Research First

- About to write plan without spawning research agents
- "I already know this codebase"
- "This is a simple change"
- "The user gave detailed requirements"
- "Research takes too long"
- Skipping codebase-locator because "I remember where things are"
- Writing plan based on similar project, not THIS codebase
- Assuming integration points without verification

All of these mean: STOP. Spawn the research agents. Read the files.
```

---

## Part 2: Rationalization Prevention

### 2.1 Excuse-Reality Tables

**What it is:** A two-column table pairing common excuses with factual counter-arguments.

**From `skills/test-driven-development/SKILL.md:256-271`:**
```markdown
## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Keep as reference" | You'll adapt it. That's testing after. Delete means delete. |
| "Already spent X hours" | Sunk cost fallacy. Time is gone. Choice: delete and trust, or keep and doubt. |
```

**From `skills/verification-before-completion/SKILL.md:63-74`:**
```markdown
## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
```

**From `skills/systematic-debugging/SKILL.md:245-255`:**
```markdown
## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. |
| "Emergency, no time for process" | Systematic debugging is FASTER. |
| "I already know the cause" | Verify with evidence anyway. |
```

**How to adapt for pcode:**
```markdown
## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your memory is stale. Spawn the locator agents. Verify. |
| "This is a simple change" | Simple changes touch complex systems. Research integration points. |
| "Research takes too long" | Wrong plans take longer. Research saves rework. |
| "User gave detailed requirements" | Users know what they want, not how the code works. Verify. |
| "I've done this before in other projects" | THIS codebase has its own patterns. Find them. |
| "Let me just start and adjust" | Planning prevents false starts. Research first. |
```

---

### 2.2 Spirit vs Letter Clause

**What it is:** An explicit statement that rephrasing doesn't bypass the rule.

**From `skills/test-driven-development/SKILL.md:14`:**
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

**From `skills/verification-before-completion/SKILL.md:14`:**
```markdown
**Violating the letter of this rule is violating the spirit of this rule.**
```

**From `skills/verification-before-completion/SKILL.md:128-131`:**
```markdown
**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness
```

**How to adapt:** Add to each RPI command:
```markdown
**This rule applies to exact phrases, paraphrases, and implications.**
Rephrasing doesn't create an exception.
```

---

## Part 3: Two-Stage Review System

### 3.1 Spec Compliance → Code Quality Sequence

**What it is:** Two separate review stages that MUST happen in order.

**From `skills/subagent-driven-development/SKILL.md:8`:**
```markdown
Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.
```

**Stage 1: Spec Compliance (`spec-reviewer-prompt.md:5`):**
```markdown
**Purpose:** Verify implementer built what was requested (nothing more, nothing less)
```

**Critical trust verification (`spec-reviewer-prompt.md:21-36`):**
```markdown
## CRITICAL: Do Not Trust the Report

The implementer finished suspiciously quickly. Their report may be incomplete,
inaccurate, or optimistic. You MUST verify everything independently.

**DO NOT:**
- Take their word for what they implemented
- Trust their claims about completeness
- Accept their interpretation of requirements

**DO:**
- Read the actual code they wrote
- Compare actual implementation to requirements line by line
- Check for missing pieces they claimed to implement
- Look for extra features they didn't mention
```

**Spec review criteria (`spec-reviewer-prompt.md:38-56`):**
```markdown
**Missing requirements:**
- Did they implement everything that was requested?
- Are there requirements they skipped or missed?
- Did they claim something works but didn't actually implement it?

**Extra/unneeded work:**
- Did they build things that weren't requested?
- Did they over-engineer or add unnecessary features?
- Did they add "nice to haves" that weren't in spec?

**Misunderstandings:**
- Did they interpret requirements differently than intended?
- Did they solve the wrong problem?
- Did they implement the right feature but wrong way?
```

**Stage 2: Code Quality (`code-quality-reviewer-prompt.md:7`):**
```markdown
**Only dispatch after spec compliance review passes.**
```

**How to adapt for vcode:**
```markdown
## Two-Stage Validation

### Stage 1: Spec Compliance Check
For each phase in plan:
1. Read phase requirements from plan
2. Read the actual implementation files
3. Compare line-by-line:
   - ❌ Missing: Requirements not implemented
   - ❌ Extra: Features not in spec (scope creep)
   - ❌ Wrong: Misunderstood requirements

**Do not proceed to Stage 2 until Stage 1 passes.**

### Stage 2: Quality Check
For verified implementations:
1. Run all success criteria commands
2. Read full output, check exit codes
3. Categorize issues:
   - Critical (blocks completion)
   - Important (should fix)
   - Minor (optional)
```

---

## Part 4: Skill Structure Patterns

### 4.1 Common Section Headers

**Found across 15+ skills:**

| Header | Purpose | Example Location |
|--------|---------|------------------|
| `## Overview` | 1-3 sentence core principle | `test-driven-development/SKILL.md:8` |
| `## When to Use` | Triggering conditions | `test-driven-development/SKILL.md:16` |
| `## The Iron Law` | Non-negotiable rule | `test-driven-development/SKILL.md:31` |
| `## The Process` | Step-by-step workflow | `brainstorming/SKILL.md:14` |
| `## Red Flags` | Warning signs | `test-driven-development/SKILL.md:272` |
| `## Common Rationalizations` | Excuse-reality table | `test-driven-development/SKILL.md:256` |
| `## Quick Reference` | Condensed checklist | `test-driven-development/SKILL.md:327` |
| `## The Bottom Line` | Final 2-3 sentence summary | `verification-before-completion/SKILL.md:133` |
| `## Integration` | Related skills | `subagent-driven-development/SKILL.md:229` |

---

### 4.2 Skill Cross-Reference Patterns

**REQUIRED SUB-SKILL - For workflow dependencies:**
```markdown
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
```
Location: `writing-plans/SKILL.md:110`, `executing-plans/SKILL.md:49`

**REQUIRED BACKGROUND - For prerequisite knowledge:**
```markdown
**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development
```
Location: `writing-skills/SKILL.md:18`

**@ Syntax for file references:**
```markdown
read @testing-anti-patterns.md to avoid common pitfalls
```
Location: `test-driven-development/SKILL.md:359`

**Announcement pattern:**
```markdown
**Announce at start:** "I'm using the executing-plans skill to implement this plan."
```
Location: `executing-plans/SKILL.md:14`

---

### 4.3 Frontmatter Structure

**Minimal, consistent format across all skills:**
```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions] - [what it does]
---
```

**Only 2 fields used:**
- `name` - kebab-case identifier
- `description` - WHEN to use (not HOW it works)

**Critical insight (`writing-skills/SKILL.md:150`):**
```markdown
**CRITICAL: Description = When to Use**
```

Bad: "Use to write code in test-first order. Write failing test → watch it fail..."
Good: "Use when about to write code without failing test first"

**Why:** Claude reads description, thinks it has the workflow, skips reading full skill.

---

## Part 5: Evidence Specification Pattern

### 5.1 Claim → Evidence Mapping

**From `skills/verification-before-completion/SKILL.md:42-50`:**

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

**Checklist format (`verification-before-completion/SKILL.md:78-82`):**
```markdown
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**How to adapt:** Add evidence requirements to vcode validation report.

---

## Part 6: Hook System

### 6.1 Session Start Context Injection

**From `hooks/hooks.json:2-14`:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```

**What session-start.sh does (`hooks/session-start.sh:42-50`):**
```bash
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n${using_superpowers_escaped}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF
```

**Key insight:** Wrapping in `<EXTREMELY_IMPORTANT>` tags increases prompt weight.

---

## Part 7: Implementation Priority

### Immediate (High Impact, Low Effort)

1. **Add Iron Laws** to pcode, icode, vcode, rcode
2. **Add Red Flags sections** with specific warning signs
3. **Add Rationalization Prevention tables** with excuse counters

### Short-Term (High Impact, Medium Effort)

4. **Add Gate Functions** to icode verification protocol
5. **Implement two-stage review** in vcode (spec → quality)
6. **Add Spirit vs Letter clause** to prevent rephrasing bypass

### Medium-Term (Medium Impact, Higher Effort)

7. **Add Claim→Evidence mapping** to vcode
8. **Review command descriptions** for Claude Search Optimization
9. **Add REQUIRED SUB-SKILL markers** for workflow dependencies

### Future

10. **Consider session-start hook** to inject workflow rules
11. **Add announcement patterns** ("I'm using the X command...")
12. **Pressure test commands** with adversarial scenarios

---

## Code References Summary

| Pattern | Primary Source | Line Numbers |
|---------|----------------|--------------|
| Iron Law | `test-driven-development/SKILL.md` | 31-45 |
| Gate Function | `verification-before-completion/SKILL.md` | 24-38 |
| Red Flags | `test-driven-development/SKILL.md` | 272-288 |
| Rationalization Table | `test-driven-development/SKILL.md` | 256-271 |
| Two-Stage Review | `subagent-driven-development/SKILL.md` | 70-76 |
| Spec Reviewer Trust | `spec-reviewer-prompt.md` | 21-36 |
| Evidence Mapping | `verification-before-completion/SKILL.md` | 42-50 |
| Hook Config | `hooks/hooks.json` | 2-14 |
| Context Injection | `hooks/session-start.sh` | 42-50 |

---

## Open Questions

1. Should we add session-start hooks to inject RPI workflow rules?
2. How formal should gate functions be in output? (Checkboxes vs prose)
3. Should rationalization tables be inline or in separate reference files?
4. Do we want "Announce at start" patterns for each command?

---

## Part 8: Skills vs Commands - Post-Unification Reality

**Research Date**: 2026-01-27
**Claude Code Version**: 2.1.3+ (post-unification)

### 8.1 The Unification Announcement vs Reality

Claude Code 2.1.3 (January 2026) announced that commands and skills were "merged, simplifying the mental model with no change in behavior." However, practical testing reveals this was **conceptual unification, not functional fixes**.

**What the documentation claims:**
> "Custom slash commands have been merged into skills. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way."

**What actually happens:**

| Feature | Project-Level | Plugin-Level |
|---------|---------------|--------------|
| Skills create `/commands` | ✅ Works | ❌ Broken |
| Commands create `/commands` | ✅ Works | ✅ Works |
| Hot-reload | ✅ Works | ✅ Works |
| Auto-invocation reliability | ~50% | ~50% |
| `/skills` command | ❌ Shows "No skills found" | ❌ Same bug |

### 8.2 Critical Open Issues (as of 2026-01-27)

**High Priority:**

1. **[Issue #18454](https://github.com/anthropics/claude-code/issues/18454)** - Claude ignores CLAUDE.md and skills during multi-step tasks
   - Labels: `priority:high`, `bug`, `area:core`
   - Claude acknowledges skills, then violates them in the next action
   - Status: OPEN

2. **[Issue #17271](https://github.com/anthropics/claude-code/issues/17271)** - Plugin skills don't appear in slash command autocomplete
   - 24+ reactions
   - Root cause: `name` frontmatter field strips plugin namespace prefix
   - Status: OPEN

3. **[Issue #14577](https://github.com/anthropics/claude-code/issues/14577)** - `/skills` command shows "No skills found"
   - Affects v2.0.73, v2.0.76, v2.1.2, v2.1.9, v2.1.14
   - Debug logs confirm skills ARE loaded, but UI shows nothing
   - Cross-platform (macOS, Windows, Linux)
   - Status: OPEN

4. **[Issue #17445](https://github.com/anthropics/claude-code/issues/17445)** - Skills not discoverable after restart
   - Must explicitly mention skill name to load it
   - Status: OPEN

### 8.3 Auto-Invocation Reliability

From [Scott Spence's practical testing](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably):

| Scenario | Success Rate |
|----------|--------------|
| Simple instruction hooks | ~50% (coin flip) |
| Multi-skill tasks | 0% without workarounds |
| With aggressive "forced eval hooks" | ~84% |

**Key observation:** Claude "sees skills, acknowledges them mentally, then completely ignores them."

The unification did NOT improve auto-invocation reliability. Users still need aggressive hook workarounds to achieve reasonable success rates.

### 8.4 Why Superpowers Uses Command→Skill Separation

Given the plugin skills bug, Superpowers' architecture makes sense:

```
commands/brainstorm.md          → Creates /brainstorm reliably
  ↓ invokes
skills/brainstorming/SKILL.md   → Contains actual logic
```

**Pattern from `commands/brainstorm.md:1-6`:**
```yaml
---
description: "You MUST use this before any creative work..."
disable-model-invocation: true
---

Invoke the superpowers:brainstorming skill and follow it exactly as presented to you
```

This works around plugin skills not creating `/commands` by:
1. Using explicit `commands/` for reliable slash command creation
2. Using `skills/` for reusable logic and cross-referencing
3. Adding `disable-model-invocation: true` to prevent unreliable auto-triggering

### 8.5 Decision: Use Skills (Not Commands)

**UPDATE (2026-01-27)**: After reviewing official documentation and clarifying we're NOT building a plugin, the recommendation changes:

**Use `newskills/` (not `newcommands/`)** because:
1. **Project-level skills create `/commands` reliably** - the plugin bug doesn't affect us
2. Skills support **supporting files** (examples, templates, scripts in same directory)
3. Skills support **`context: fork`** for subagent execution
4. Skills support **dynamic context injection** with `!`command`` syntax
5. Skills are the **officially recommended** modern approach
6. Commands are backward-compatible but considered legacy

**Updated structure:**
```
newskills/
├── pcode/
│   ├── SKILL.md              # Main skill instructions
│   └── examples/
│       └── good-plan.md      # Example plan format
├── icode/
│   └── SKILL.md
├── vcode/
│   └── SKILL.md
├── rcode/
│   └── SKILL.md
├── commit/
│   └── SKILL.md
└── pr/
    └── SKILL.md
```

**Frontmatter for each skill:**
```yaml
---
name: pcode
description: "Create or iterate on implementation plans with thorough research"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Task, Write
---
```

The `disable-model-invocation: true` prevents unreliable auto-triggering while allowing explicit `/pcode` invocation.

### 8.6 Official Documentation: Skills vs Slash Commands

**Source**: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

The official documentation states:

> **"Custom slash commands have been merged into skills."** A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way.

**Key points from official docs:**

1. **Unified system** - Skills and commands create the same `/slash-command` functionality
2. **Skills recommended** - Support additional features (supporting files, fork context)
3. **Backward compatible** - `.claude/commands/` files continue working
4. **Conflict resolution** - If both exist with same name, skill takes precedence

**Complete frontmatter options:**

| Field                      | Description                                                                 |
|:---------------------------|:----------------------------------------------------------------------------|
| `name`                     | Display name (defaults to directory name). Lowercase, hyphens only, max 64. |
| `description`              | What skill does and when to use it. Claude uses this for auto-invocation.   |
| `argument-hint`            | Hint shown in autocomplete. Example: `[issue-number]`                       |
| `disable-model-invocation` | `true` = prevent Claude auto-loading. Use for manual workflows.             |
| `user-invocable`           | `false` = hide from `/` menu. Use for background knowledge.                 |
| `allowed-tools`            | Tools Claude can use without permission when skill is active.               |
| `model`                    | Model to use when skill is active.                                          |
| `context`                  | `fork` = run in forked subagent context.                                    |
| `agent`                    | Subagent type when `context: fork` (`Explore`, `Plan`, etc.).               |
| `hooks`                    | Hooks scoped to skill's lifecycle.                                          |

**Invocation control:**

| Frontmatter                      | You can invoke | Claude can invoke |
|:---------------------------------|:---------------|:------------------|
| (default)                        | Yes            | Yes               |
| `disable-model-invocation: true` | Yes            | No                |
| `user-invocable: false`          | No             | Yes               |

**String substitutions:**

| Variable               | Description                                    |
|:-----------------------|:-----------------------------------------------|
| `$ARGUMENTS`           | All arguments passed when invoking             |
| `$ARGUMENTS[N]` / `$N` | Specific argument by 0-based index             |
| `${CLAUDE_SESSION_ID}` | Current session ID                             |

**Dynamic context injection:**
```markdown
## Context
- Current diff: !`git diff HEAD`
- PR comments: !`gh pr view --comments`
```

Commands in `` !`command` `` run before skill is sent to Claude (preprocessing).

### 8.7 What DID Improve in 2.1.3

Despite the auto-invocation issues, several things work well:

- ✅ **Project-level skills create `/commands`** reliably
- ✅ **Hot-reload** - modify skill, immediately available without restart
- ✅ **Explicit control** - can use `/skill-name` instead of hoping for auto-detection
- ✅ **Backward compatibility** - `.claude/commands/` files still work
- ✅ **Documentation consolidated** - no more contradictory comparison tables
- ✅ **Supporting files** - skills can include templates, examples, scripts in directory

### 8.8 Sources

**Official:**
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills) - **Primary reference**
- [Slash Commands in the SDK](https://platform.claude.com/docs/en/agent-sdk/slash-commands)
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**GitHub Issues:**
- [Issue #18454](https://github.com/anthropics/claude-code/issues/18454) - Skills ignored during multi-step tasks
- [Issue #17271](https://github.com/anthropics/claude-code/issues/17271) - Plugin skills slash command bug
- [Issue #14577](https://github.com/anthropics/claude-code/issues/14577) - `/skills` shows "No skills found"
- [Issue #17578](https://github.com/anthropics/claude-code/issues/17578) - Documentation inconsistency (CLOSED)
- [Issue #13115](https://github.com/anthropics/claude-code/issues/13115) - Original merge discussion (CLOSED)

**User Experiences:**
- [How to Make Claude Code Skills Activate Reliably](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - Practical testing with success rates
- [Claude Code 2.1: Pain Points Addressed](https://paddo.dev/blog/claude-code-21-pain-points-addressed/) - Post-2.1 analysis
- [Claude Code Merges Slash Commands Into Skills](https://medium.com/@joe.njenga/claude-code-merges-slash-commands-into-skills-dont-miss-your-update-8296f3989697) - Merger explanation
