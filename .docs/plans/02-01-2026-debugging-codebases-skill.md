---
git_commit: a7794e1
last_updated: 2026-02-01
last_updated_by: claude
topic: "Debugging Codebases Skill"
tags: [plan, implementation, skill, debugging, rpi-workflow]
status: implemented
references:
  - newskills/debugging-codebases/SKILL.md (new)
  - newskills/debugging-codebases/templates/debug-session-template.md (new)
  - newskills/debugging-codebases/reference/investigation-techniques.md (new)
  - newskills/debugging-codebases/reference/hypothesis-testing.md (new)
  - newskills/debugging-codebases/reference/verification-patterns.md (new)
---

# Debugging Codebases Skill Implementation Plan

## Overview

Create a new `/debugging-codebases` skill that provides systematic, scientific debugging with persistent state across context resets. This fills a gap in the RPI workflow where debugging currently has no dedicated skill.

**Source:** Adapted from GSD's `gsd-debugger` agent and `/gsd:debug` command, translated to commandbase skill patterns.

## Current State Analysis

- No dedicated debugging skill exists in commandbase
- `/learning-from-sessions` captures learnings AFTER debugging, but doesn't guide the process
- References to "debug" in existing skills are incidental mentions, not systematic support
- GSD has a mature 1200+ line debugging agent with persistent state, scientific method, and hypothesis testing

### Key Discoveries:
- Commandbase skills use `SKILL.md` + optional `reference/` + optional `templates/` structure
- Skills like `researching-codebases` and `discussing-features` provide good structural patterns
- GSD stores debug state in `.planning/debug/` - we'll use `.docs/debug/` for consistency
- GSD's debug file structure (Current Focus, Symptoms, Eliminated, Evidence, Resolution) enables perfect resume after `/clear`

## Desired End State

A fully functional `/debugging-codebases` skill that:
1. Creates persistent debug session files in `.docs/debug/`
2. Guides investigation using scientific hypothesis testing
3. Tracks eliminated hypotheses to prevent re-investigation after context reset
4. Supports two modes: diagnose-only and diagnose-and-fix
5. Integrates with `/learning-from-sessions` for knowledge extraction

**Verification:**
- Skill appears in Claude Code's available skills list
- Can invoke via `/debugging-codebases [issue description]`
- Debug session files persist and enable resume after `/clear`
- Follows existing skill patterns (description triggers, progressive disclosure)

## What We're NOT Doing

- Creating a separate debugging agent (skill handles orchestration inline)
- Implementing model profile selection (future enhancement)
- Adding wave-based parallel debugging (single-threaded investigation is appropriate)
- Creating `.docs/debug/resolved/` archive (simple delete when done, `/learning-from-sessions` captures knowledge)
- Git commit integration (user commits via `/commit` when ready)

## Implementation Approach

Adapt GSD's debugging system to commandbase's skill-based architecture:
- SKILL.md contains the main process (GSD splits between command and agent)
- Reference files contain detailed techniques (progressive disclosure)
- Template file defines debug session structure
- Use `.docs/debug/` instead of `.planning/debug/`
- Integrate with existing skills rather than custom workflows

---

## Phase 1: Create SKILL.md

### Overview
Create the main skill definition file with frontmatter, iron law, process steps, and integration points.

### Changes Required:

#### 1. Create skill directory and SKILL.md
**File**: `newskills/debugging-codebases/SKILL.md`
**Changes**: New file - main skill definition

```markdown
---
name: debugging-codebases
description: "Use this skill when debugging issues in the codebase using systematic investigation. This includes tracking hypotheses, eliminating dead ends, finding root causes, and optionally fixing verified issues. Activate when the user says 'debug this', 'why is this failing', 'find the bug', 'investigate this issue', or describes unexpected behavior they want diagnosed."
---

# Debugging Codebases

You are conducting systematic debugging using scientific method with persistent state that survives context resets. Your job is to find root causes through hypothesis testing, not trial-and-error guessing.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
HYPOTHESIS BEFORE ACTION
```

Never make changes hoping they'll fix the issue. Every action must test a specific, falsifiable hypothesis.

**No exceptions:**
- Don't "try things" - form hypotheses and test them
- Don't fix without understanding - find root cause first
- Don't re-investigate eliminated hypotheses - check the debug file
- Don't guess at causes - gather evidence

## The Gate Function

```
BEFORE making any code change:

1. HYPOTHESIS: What specific theory am I testing?
2. FALSIFIABLE: What evidence would prove this wrong?
3. TEST: What's the minimal experiment to test this?
4. PREDICT: What result do I expect if hypothesis is correct?
5. ONLY THEN: Execute the test and observe

Skipping steps = guessing, not debugging
```

## Initial Response

When this skill is invoked:

### If debug sessions exist AND no arguments:
```bash
ls .docs/debug/*.md 2>/dev/null
```

Display active sessions:
```
Active debug sessions found:

1. [slug] - Status: [status], Hypothesis: [current hypothesis]
2. [slug] - Status: [status], Hypothesis: [current hypothesis]

Enter number to resume, or describe a new issue to start fresh.
```

### If arguments provided OR user describes new issue:
1. Create debug session file immediately (see templates/debug-session-template.md)
2. Begin symptom gathering

### If no sessions AND no arguments:
```
I'll help you debug systematically. Describe the issue you're experiencing:

- What should happen?
- What actually happens?
- Any error messages?

Or provide the issue description directly: /debugging-codebases [description]
```

## Process

### Step 1: Create Debug Session

Create `.docs/debug/` directory if needed, then create session file:

**File naming:** `{slug}.md` where slug is derived from issue description (lowercase, hyphens, max 30 chars)

**Initial state:**
- status: gathering
- trigger: verbatim user input
- Current Focus: next_action = "gather symptoms"

See `templates/debug-session-template.md` for full structure.

### Step 2: Gather Symptoms

Collect information the USER knows (not technical investigation):

1. **Expected behavior** - What should happen?
2. **Actual behavior** - What happens instead?
3. **Error messages** - Any errors shown?
4. **Timeline** - When did this start? Did it ever work?
5. **Reproduction** - How do you trigger this?

Update debug file after EACH answer. When complete:
- Mark Symptoms section as complete
- Update status to "investigating"
- Proceed to investigation

### Step 3: Investigation Loop

**Update debug file BEFORE each action, not after.**

#### Phase A: Initial Evidence Gathering
- Search codebase for error text if errors exist
- Identify relevant code area from symptoms
- Read relevant files COMPLETELY
- Run code/tests to observe behavior
- APPEND to Evidence section after each finding

#### Phase B: Form Hypothesis
Based on evidence, form a SPECIFIC, FALSIFIABLE hypothesis.

See `reference/hypothesis-testing.md` for:
- What makes a hypothesis falsifiable
- How to design experiments
- Cognitive biases to avoid

Update Current Focus with:
- hypothesis: [specific theory]
- test: [how to test it]
- expecting: [what result means]
- next_action: [immediate next step]

#### Phase C: Test Hypothesis
- Execute ONE test at a time
- Observe result
- Append to Evidence

#### Phase D: Evaluate
- **CONFIRMED:** Update Resolution.root_cause, proceed to Step 4 or Step 5
- **ELIMINATED:** Append to Eliminated section, return to Phase B with new hypothesis

See `reference/investigation-techniques.md` for debugging techniques.

### Step 4: Diagnose Only (Optional)

If user wants diagnosis without fix:

```
ROOT CAUSE IDENTIFIED
=====================

Debug session: .docs/debug/{slug}.md

Root Cause: [specific cause with evidence]

Evidence:
- [key finding 1]
- [key finding 2]

Files Involved:
- [file]: [what's wrong]

Suggested Fix Direction: [brief hint, not implementation]

Next steps:
- "Fix it" - I'll implement and verify the fix
- "I'll fix it manually" - Done, session saved
- "/learning-from-sessions" - Extract learnings from this debug
```

### Step 5: Fix and Verify

If proceeding with fix:

1. Update status to "fixing"
2. Implement MINIMAL change that addresses root cause
3. Update Resolution.fix and Resolution.files_changed
4. Update status to "verifying"
5. Test against original Symptoms
6. If verification FAILS: status -> "investigating", return to Step 3
7. If verification PASSES: Update Resolution.verification

```
DEBUG COMPLETE
==============

Debug session: .docs/debug/{slug}.md

Root Cause: [what was wrong]
Fix Applied: [what was changed]
Verification: [how verified]

Files Changed:
- [file]: [change]

Next steps:
- "/commit" - Commit the fix
- "/learning-from-sessions" - Extract learnings
- Delete .docs/debug/{slug}.md when done
```

### Step 6: Resume from File

When resuming an existing session:

1. Read full debug file
2. Announce: "Resuming debug session: {slug}"
3. Report: status, current hypothesis, evidence count, eliminated count
4. Continue from Current Focus.next_action

The debug file IS the debugging brain. Perfect resume from any interruption.

## Integration Points

- **`/learning-from-sessions`**: After resolving, offer to extract learnings
- **`/commit`**: After fix verified, suggest committing
- **`/researching-codebases`**: If investigation reveals need for broader codebase understanding

## Red Flags - STOP and Refocus

If you notice any of these, pause:

- About to make a change without a specific hypothesis
- Re-investigating something in the Eliminated section
- "Let me just try..." (trial and error, not science)
- Changing multiple things at once
- Acting on weak evidence ("seems like", "might be")
- Debug file not updated before taking action

## Verification Patterns

See `reference/verification-patterns.md` for:
- What "verified" means
- Reproduction verification
- Regression testing
- Stability testing

## The Bottom Line

**Debug systematically, not hopefully.**

Form hypothesis. Design test. Predict result. Execute. Evaluate. Document.

This is non-negotiable. Every bug. Every time.
```

### Success Criteria:
- [ ] File exists at `newskills/debugging-codebases/SKILL.md`
- [ ] Frontmatter has correct name and description
- [ ] Description includes trigger phrases
- [ ] Iron Law and Gate Function defined
- [ ] All process steps documented
- [ ] Integration points specified

---

## Phase 2: Create Debug Session Template

### Overview
Define the persistent debug file structure that enables resume after context reset.

### Changes Required:

#### 1. Create templates directory and template file
**File**: `newskills/debugging-codebases/templates/debug-session-template.md`
**Changes**: New file - debug session structure

```markdown
# Debug Session Template

Use this template for debug session files in `.docs/debug/{slug}.md`.

## File Naming

- **Location**: `.docs/debug/`
- **Format**: `{slug}.md` (lowercase, hyphens, max 30 chars)
- **Derived from**: First few words of issue description
- **Examples**: `login-fails-silently.md`, `api-returns-500.md`

## Template

```markdown
---
status: gathering | investigating | fixing | verifying | resolved
trigger: "[verbatim user input that started this session]"
created: [ISO timestamp]
updated: [ISO timestamp]
---

## Current Focus
<!-- OVERWRITE on each update - always reflects NOW -->

hypothesis: [current theory being tested]
test: [how testing it]
expecting: [what result means if true/false]
next_action: [immediate next step]

## Symptoms
<!-- Written during gathering, then IMMUTABLE -->

expected: [what should happen]
actual: [what actually happens]
errors: [error messages if any]
reproduction: [how to trigger]
started: [when it broke / always broken]

## Eliminated
<!-- APPEND only - prevents re-investigating after /clear -->

- hypothesis: [theory that was wrong]
  evidence: [what disproved it]
  timestamp: [when eliminated]

## Evidence
<!-- APPEND only - facts discovered during investigation -->

- timestamp: [when found]
  checked: [what was examined]
  found: [what was observed]
  implication: [what this means]

## Resolution
<!-- OVERWRITE as understanding evolves -->

root_cause: [empty until found]
fix: [empty until applied]
verification: [empty until verified]
files_changed: []
```

## Section Rules

| Section | Rule | Rationale |
|---------|------|-----------|
| Frontmatter.status | OVERWRITE | Reflects current phase |
| Frontmatter.trigger | IMMUTABLE | Original problem statement |
| Frontmatter.updated | OVERWRITE | Track last modification |
| Current Focus | OVERWRITE | Always reflects NOW |
| Symptoms | IMMUTABLE after gathering | Reference point for verification |
| Eliminated | APPEND only | Prevents re-investigation |
| Evidence | APPEND only | Builds case for root cause |
| Resolution | OVERWRITE | Evolves as understanding grows |

## Status Transitions

```
gathering -> investigating -> fixing -> verifying -> resolved
                  ^              |           |
                  |______________|___________|
                  (if verification fails)
```

## Resume Behavior

When reading debug file after `/clear`:

1. Parse frontmatter -> know status
2. Read Current Focus -> know exactly what was happening
3. Read Eliminated -> know what NOT to retry
4. Read Evidence -> know what's been learned
5. Continue from next_action

The file IS the debugging brain. Claude should resume perfectly from any interruption.

## Update Discipline

**CRITICAL:** Update the file BEFORE taking action, not after.

If context resets mid-action, the file shows what was about to happen, enabling seamless resume.

## Size Constraints

Keep debug files focused:
- Evidence entries: 1-2 lines each, just facts
- Eliminated: brief - hypothesis + why it failed
- No narrative prose - structured data only

If evidence grows large (10+ entries), check if you're going in circles. Review Eliminated section.

## Cleanup

After debug complete:
- Option 1: Delete file (if learnings extracted via `/learning-from-sessions`)
- Option 2: Keep for reference (if complex issue worth preserving)

No automatic archival - user decides.
```

### Success Criteria:
- [ ] File exists at `newskills/debugging-codebases/templates/debug-session-template.md`
- [ ] Template includes all sections (Current Focus, Symptoms, Eliminated, Evidence, Resolution)
- [ ] Section rules clearly documented
- [ ] Resume behavior explained
- [ ] Update discipline emphasized

---

## Phase 3: Create Investigation Techniques Reference

### Overview
Document debugging techniques for different scenarios.

### Changes Required:

#### 1. Create reference directory and techniques file
**File**: `newskills/debugging-codebases/reference/investigation-techniques.md`
**Changes**: New file - debugging techniques guide

```markdown
# Investigation Techniques

Reference guide for systematic debugging techniques. Choose based on the situation.

## Technique Selection

| Situation | Technique |
|-----------|-----------|
| Large codebase, many files | Binary Search |
| Confused about what's happening | Rubber Duck, Observability First |
| Complex system, many interactions | Minimal Reproduction |
| Know the desired output | Working Backwards |
| Used to work, now doesn't | Differential Debugging, Git Bisect |
| Many possible causes | Comment Out Everything |
| Always | Observability First (before changes) |

---

## Binary Search / Divide and Conquer

**When:** Large codebase, long execution path, many possible failure points.

**How:** Cut problem space in half repeatedly until isolated.

1. Identify boundaries (where works, where fails)
2. Add logging/testing at midpoint
3. Determine which half contains the bug
4. Repeat until exact location found

**Example:** API returns wrong data
- Data leaves database correctly? YES
- Data reaches frontend correctly? NO
- Data leaves API route correctly? YES
- Data survives serialization? NO
- **Found:** Bug in serialization (4 tests eliminated 90% of code)

---

## Rubber Duck Debugging

**When:** Stuck, confused, mental model doesn't match reality.

**How:** Explain the problem in complete detail (write or speak).

1. "The system should do X"
2. "Instead it does Y"
3. "I think this is because Z"
4. "The code path is: A -> B -> C -> D"
5. "I've verified that..." (list tested)
6. "I'm assuming that..." (list assumptions)

Often you'll spot the bug mid-explanation.

---

## Minimal Reproduction

**When:** Complex system, many moving parts, unclear which part fails.

**How:** Strip away everything until smallest code reproduces bug.

1. Copy failing code to new file
2. Remove one piece
3. Test: Still reproduces? YES = keep removed. NO = put back.
4. Repeat until bare minimum
5. Bug is now obvious

---

## Working Backwards

**When:** Know correct output, don't know why not getting it.

**How:** Start from desired end state, trace backwards.

1. Define desired output precisely
2. What function produces this output?
3. Test function with expected input - correct output?
   - YES: Bug is earlier (wrong input)
   - NO: Bug is here
4. Repeat backwards through call stack

---

## Differential Debugging

**When:** Something used to work and now doesn't. Works in one environment but not another.

**Time-based (worked, now doesn't):**
- What changed in code?
- What changed in environment?
- What changed in data?
- What changed in configuration?

**Environment-based (works here, fails there):**
- Configuration values
- Environment variables
- Network conditions
- Data volume

**Process:** List differences, test each in isolation, find the causal difference.

---

## Git Bisect

**When:** Feature worked in past, broke at unknown commit.

**How:** Binary search through git history.

```bash
git bisect start
git bisect bad              # Current commit is broken
git bisect good abc123      # This commit worked
# Git checks out middle commit
git bisect bad              # or good, based on testing
# Repeat until culprit found
```

100 commits between working and broken: ~7 tests to find exact breaking commit.

---

## Observability First

**When:** Always. Before making any fix.

**Add visibility before changing behavior:**

```javascript
// Strategic logging
console.log('[handleSubmit] Input:', { email, password: '***' });
console.log('[handleSubmit] Validation result:', validationResult);

// Assertion checks
console.assert(user !== null, 'User is null!');

// Timing measurements
console.time('Database query');
const result = await db.query(sql);
console.timeEnd('Database query');
```

**Workflow:** Add logging -> Run -> Observe -> Hypothesize -> Then change.

---

## Comment Out Everything

**When:** Many possible interactions, unclear which code causes issue.

**How:**
1. Comment out everything in function/file
2. Verify bug is gone
3. Uncomment one piece at a time
4. After each, test
5. When bug returns, found the culprit

---

## Combining Techniques

Techniques compose. Often use multiple together:

1. **Differential debugging** to identify what changed
2. **Binary search** to narrow down where in code
3. **Observability first** to add logging at that point
4. **Rubber duck** to articulate what you're seeing
5. **Minimal reproduction** to isolate just that behavior
6. **Working backwards** to find the root cause
```

### Success Criteria:
- [ ] File exists at `newskills/debugging-codebases/reference/investigation-techniques.md`
- [ ] Technique selection table included
- [ ] Each technique has When/How/Example
- [ ] Combining techniques section present

---

## Phase 4: Create Hypothesis Testing Reference

### Overview
Document the scientific method for debugging: hypothesis formation, testing, and cognitive bias prevention.

### Changes Required:

#### 1. Create hypothesis testing reference file
**File**: `newskills/debugging-codebases/reference/hypothesis-testing.md`
**Changes**: New file - scientific debugging guide

```markdown
# Hypothesis Testing

The scientific method applied to debugging. Form hypotheses, design experiments, avoid biases.

## Falsifiability Requirement

A good hypothesis can be proven wrong. If you can't design an experiment to disprove it, it's not useful.

**Bad (unfalsifiable):**
- "Something is wrong with the state"
- "The timing is off"
- "There's a race condition somewhere"

**Good (falsifiable):**
- "User state resets because component remounts when route changes"
- "API call completes after unmount, causing state update on unmounted component"
- "Two async operations modify same array without locking, causing data loss"

**The difference:** Specificity. Good hypotheses make specific, testable claims.

---

## Forming Hypotheses

1. **Observe precisely:** Not "it's broken" but "counter shows 3 when clicking once, should show 1"
2. **Ask "What could cause this?"** - List every possible cause (don't judge yet)
3. **Make each specific:** Not "state is wrong" but "state updates twice because handleClick called twice"
4. **Identify evidence:** What would support/refute each hypothesis?

---

## Experimental Design

For each hypothesis:

1. **Prediction:** If H is true, I will observe X
2. **Test setup:** What do I need to do?
3. **Measurement:** What exactly am I measuring?
4. **Success criteria:** What confirms H? What refutes H?
5. **Run:** Execute the test
6. **Observe:** Record what actually happened
7. **Conclude:** Does this support or refute H?

**One hypothesis at a time.** Multiple changes = no idea what mattered.

---

## Evidence Quality

**Strong evidence:**
- Directly observable ("I see in logs that X happens")
- Repeatable ("This fails every time I do Y")
- Unambiguous ("The value is definitely null, not undefined")
- Independent ("Happens even in fresh browser with no cache")

**Weak evidence:**
- Hearsay ("I think I saw this fail once")
- Non-repeatable ("It failed that one time")
- Ambiguous ("Something seems off")
- Confounded ("Works after restart AND cache clear AND update")

---

## Decision Point: When to Act

Act when you can answer YES to all:
1. **Understand the mechanism?** Not just "what fails" but "why it fails"
2. **Reproduce reliably?** Either always reproduces, or understand trigger conditions
3. **Have evidence, not just theory?** Observed directly, not guessing
4. **Ruled out alternatives?** Evidence contradicts other hypotheses

**Don't act if:** "I think it might be X" or "Let me try changing Y and see"

---

## Cognitive Biases to Avoid

| Bias | Trap | Antidote |
|------|------|----------|
| **Confirmation** | Only look for evidence supporting hypothesis | Actively seek disconfirming evidence. "What would prove me wrong?" |
| **Anchoring** | First explanation becomes your anchor | Generate 3+ independent hypotheses before investigating any |
| **Availability** | Recent bugs → assume similar cause | Treat each bug as novel until evidence suggests otherwise |
| **Sunk Cost** | Spent 2 hours on one path, keep going | Every 30 min: "If I started fresh, is this still the path I'd take?" |

---

## Recovery from Wrong Hypotheses

When disproven:
1. **Acknowledge explicitly** - "This hypothesis was wrong because [evidence]"
2. **Extract the learning** - What did this rule out? What new information?
3. **Revise understanding** - Update mental model
4. **Form new hypotheses** - Based on what you now know
5. **Don't get attached** - Being wrong quickly is better than being wrong slowly

---

## Multiple Hypotheses Strategy

Don't fall in love with your first hypothesis. Generate alternatives.

**Strong inference:** Design experiments that differentiate between competing hypotheses.

```javascript
// Problem: Form submission fails intermittently

try {
  console.log('[1] Starting validation');
  const validation = await validate(formData);
  console.log('[1] Validation passed:', validation);

  console.log('[2] Starting submission');
  const response = await api.submit(formData);
  console.log('[2] Response received:', response.status);

  console.log('[3] Updating UI');
  updateUI(response);
  console.log('[3] Complete');
} catch (error) {
  console.log('[ERROR] Failed at stage:', error);
}

// Results differentiate four hypotheses:
// - Fails at [2] with timeout → Network
// - Fails at [1] with validation error → Validation
// - Succeeds but [3] has wrong data → Race condition
// - Fails at [2] with 429 status → Rate limiting
```

---

## When to Restart

Consider starting over when:
1. **2+ hours with no progress** - Likely tunnel-visioned
2. **3+ "fixes" that didn't work** - Mental model is wrong
3. **Can't explain the current behavior** - Don't add changes on top of confusion
4. **Debugging the debugger** - Something fundamental is wrong
5. **Fix works but you don't know why** - This isn't fixed, this is luck

**Restart protocol:**
1. Close all files and terminals
2. Write down what you know for certain
3. Write down what you've ruled out
4. List new hypotheses (different from before)
5. Begin again from evidence gathering
```

### Success Criteria:
- [ ] File exists at `newskills/debugging-codebases/reference/hypothesis-testing.md`
- [ ] Falsifiability requirement explained with examples
- [ ] Experimental design framework documented
- [ ] Cognitive biases table included
- [ ] Recovery from wrong hypotheses covered

---

## Phase 5: Create Verification Patterns Reference

### Overview
Document what "verified" means and how to confirm fixes actually work.

### Changes Required:

#### 1. Create verification patterns reference file
**File**: `newskills/debugging-codebases/reference/verification-patterns.md`
**Changes**: New file - verification guide

```markdown
# Verification Patterns

What "verified" means and how to confirm fixes actually work.

## What "Verified" Means

A fix is verified when ALL of these are true:

1. **Original issue no longer occurs** - Exact reproduction steps now produce correct behavior
2. **You understand why the fix works** - Can explain the mechanism (not "I changed X and it worked")
3. **Related functionality still works** - Regression testing passes
4. **Fix is stable** - Works consistently, not "worked once"

**Anything less is not verified.**

---

## Reproduction Verification

**Golden rule:** If you can't reproduce the bug, you can't verify it's fixed.

**Before fixing:** Document exact steps to reproduce
**After fixing:** Execute the same steps exactly
**Test edge cases:** Related scenarios

**If you can't reproduce original bug:**
- You don't know if fix worked
- Maybe it's still broken
- Maybe fix did nothing
- **Solution:** Revert fix. If bug comes back, you've verified fix addressed it.

---

## Regression Testing

**The problem:** Fix one thing, break another.

**Protection:**
1. Identify adjacent functionality (what else uses the code you changed?)
2. Test each adjacent area
3. Run existing tests (unit, integration, e2e)

---

## Stability Testing

**For intermittent bugs:**

```bash
# Repeated execution
for i in {1..100}; do
  npm test -- specific-test.js || echo "Failed on run $i"
done
```

If it fails even once, it's not fixed.

**Race condition testing:**
```javascript
// Add random delays to expose timing bugs
async function testWithRandomTiming() {
  await randomDelay(0, 100);
  triggerAction1();
  await randomDelay(0, 100);
  triggerAction2();
  await randomDelay(0, 100);
  verifyResult();
}
// Run 100+ times
```

---

## Test-First Debugging

**Strategy:** Write a failing test that reproduces the bug, then fix until test passes.

**Benefits:**
- Proves you can reproduce the bug
- Provides automatic verification
- Prevents regression in the future
- Forces precise understanding

**Process:**
```javascript
// 1. Write test that reproduces bug
test('should handle undefined user data', () => {
  const result = processUserData(undefined);
  expect(result).toBe(null); // Currently throws error
});

// 2. Verify test fails (confirms reproduction)
// ✗ TypeError: Cannot read property 'name' of undefined

// 3. Fix the code
function processUserData(user) {
  if (!user) return null;
  return user.name;
}

// 4. Verify test passes
// ✓ should handle undefined user data

// 5. Test is now regression protection forever
```

---

## Verification Checklist

```markdown
### Original Issue
- [ ] Can reproduce original bug before fix
- [ ] Have documented exact reproduction steps

### Fix Validation
- [ ] Original steps now work correctly
- [ ] Can explain WHY the fix works
- [ ] Fix is minimal and targeted

### Regression Testing
- [ ] Adjacent features work
- [ ] Existing tests pass
- [ ] Added test to prevent regression (if appropriate)

### Stability Testing
- [ ] Tested multiple times: zero failures
- [ ] Tested edge cases
```

---

## Verification Red Flags

Your verification might be wrong if:
- You can't reproduce original bug anymore (forgot how, environment changed)
- Fix is large or complex (too many moving parts)
- You're not sure why it works
- It only works sometimes ("seems more stable")

**Red flag phrases:** "It seems to work", "I think it's fixed", "Looks good to me"

**Trust-building phrases:** "Verified 50 times - zero failures", "All tests pass including new regression test", "Root cause was X, fix addresses X directly"

---

## Verification Mindset

**Assume your fix is wrong until proven otherwise.**

Questions to ask yourself:
- "How could this fix fail?"
- "What haven't I tested?"
- "What am I assuming?"

The cost of insufficient verification: bug returns, user frustration, emergency debugging, rollbacks.
```

### Success Criteria:
- [ ] File exists at `newskills/debugging-codebases/reference/verification-patterns.md`
- [ ] "What verified means" clearly defined
- [ ] Reproduction verification covered
- [ ] Test-first debugging explained
- [ ] Verification checklist included

---

## Testing Strategy

### Manual Testing:
After each phase:
1. Copy skill directory to `~/.claude/skills/debugging-codebases/`
2. Start new Claude Code session
3. Verify skill appears in available skills
4. Test invocation with `/debugging-codebases test issue`
5. Verify debug file created in `.docs/debug/`

### Integration Testing:
- Test session resume after `/clear`
- Test integration with `/learning-from-sessions`
- Test both diagnose-only and diagnose-and-fix modes

---

## References

- GSD debugger agent: `C:/code/repo-library/get-shit-done/agents/gsd-debugger.md`
- GSD debug command: `C:/code/repo-library/get-shit-done/commands/gsd/debug.md`
- GSD debug template: `C:/code/repo-library/get-shit-done/get-shit-done/templates/DEBUG.md`
- Research document: `.docs/research/02-01-2026-get-shit-done-skill-comparison.md`
- Similar skill pattern: `newskills/researching-codebases/SKILL.md`
- Similar skill pattern: `newskills/discussing-features/SKILL.md`
