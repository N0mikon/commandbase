# Research: debugging-code Skill

## Overview

The `debugging-code` skill (`~/.claude/skills/debugging-code/SKILL.md`) implements systematic debugging using the scientific method with persistent state across context resets. It enforces hypothesis-driven investigation rather than trial-and-error fixing.

**Trigger phrases**: `debug this`, `why is this failing`, `find the bug`, `investigate this issue`, or descriptions of unexpected behavior

## The Iron Law (SKILL.md:12-24)

```
HYPOTHESIS BEFORE ACTION
```

**Non-negotiable rules:**
- Don't "try things" - form hypotheses and test them
- Don't fix without understanding - find root cause first
- Don't re-investigate eliminated hypotheses - check the debug file
- Don't guess at causes - gather evidence

## The Gate Function (SKILL.md:26-38)

Before making ANY code change, 5 questions must be answered:

1. **HYPOTHESIS**: What specific theory am I testing?
2. **FALSIFIABLE**: What evidence would prove this wrong?
3. **TEST**: What's the minimal experiment to test this?
4. **PREDICT**: What result do I expect if hypothesis is correct?
5. **ONLY THEN**: Execute the test and observe

## Activation Modes (SKILL.md:42-72)

### Mode 1: Existing Sessions Resume
- Checks for `.docs/debug/*.md` files
- Lists active sessions with status and current hypothesis
- User selects number to resume or describes new issue

### Mode 2: New Issue with Arguments
- Creates debug session file immediately
- Begins symptom gathering

### Mode 3: No Sessions, No Arguments
- Prompts user to describe issue
- Asks for: what should happen, what actually happens, error messages

## Hypothesis Tracking (File-Based Persistent State)

Debug sessions tracked in `.docs/debug/{slug}.md`:

```yaml
---
status: gathering | investigating | fixing | verifying | resolved
trigger: "[verbatim user input]"
created: [ISO timestamp]
updated: [ISO timestamp]
---

## Current Focus (OVERWRITE - always reflects NOW)
hypothesis: [current theory being tested]
test: [how testing it]
expecting: [what result means]
next_action: [immediate next step]

## Symptoms (IMMUTABLE after gathering)
expected: [what should happen]
actual: [what actually happens]
errors: [error messages]
reproduction: [how to trigger]

## Eliminated (APPEND only - prevents re-investigation)
- hypothesis: [theory that was wrong]
  evidence: [what disproved it]

## Evidence (APPEND only)
- checked: [what was examined]
  found: [what was observed]
  implication: [what this means]

## Resolution (OVERWRITE as understanding evolves)
root_cause: [empty until found]
fix: [empty until applied]
verification: [empty until verified]
```

## Investigation Loop (SKILL.md:104-138)

### Phase A: Initial Evidence Gathering
- Search codebase for error text
- Identify relevant code area from symptoms
- Read relevant files COMPLETELY
- Run code/tests to observe behavior
- APPEND to Evidence section after each finding

### Phase B: Form Hypothesis
Based on evidence, form a SPECIFIC, FALSIFIABLE hypothesis:

**Bad (unfalsifiable):**
- "Something is wrong with the state"
- "The timing is off"

**Good (falsifiable):**
- "User state resets because component remounts when route changes"
- "API call completes after unmount, causing state update on unmounted component"

### Phase C: Test Hypothesis
- Execute ONE test at a time
- Observe result
- Append to Evidence

### Phase D: Evaluate
- **CONFIRMED**: Update Resolution.root_cause, proceed to fix
- **ELIMINATED**: Append to Eliminated section, return to Phase B

## Fix Verification Process (SKILL.md:167-196)

1. Update status to "fixing"
2. Implement MINIMAL change that addresses root cause
3. Update Resolution.fix and Resolution.files_changed
4. Update status to "verifying"
5. Test against original Symptoms
6. If verification FAILS: status -> "investigating", return
7. If verification PASSES: Update Resolution.verification
8. Output completion report

## Verification Standards

A fix is verified when ALL are true:
1. Original issue no longer occurs
2. You understand why the fix works
3. Related functionality still works (regression testing)
4. Fix is stable (works consistently, not "worked once")

## Investigation Techniques Reference

| Situation | Technique |
|-----------|-----------|
| Large codebase, many files | Binary Search |
| Confused about what's happening | Rubber Duck, Observability First |
| Complex system, many interactions | Minimal Reproduction |
| Know the desired output | Working Backwards |
| Used to work, now doesn't | Differential Debugging, Git Bisect |
| Many possible causes | Comment Out Everything |

## Red Flags - Stop and Refocus

- About to make a change without a specific hypothesis
- Re-investigating something in the Eliminated section
- Using phrases like "Let me just try..."
- Changing multiple things at once
- Acting on weak evidence ("seems like", "might be")

## Integration Points

- `/learning-from-sessions`: After resolving, offer to extract learnings
- `/commit`: After fix verified, suggest committing
- `/researching-code`: If investigation reveals need for broader understanding

## File References

- Main: `~/.claude/skills/debugging-code/SKILL.md`
- Debug session template: `~/.claude/skills/debugging-code/templates/debug-session-template.md`
- Hypothesis testing: `~/.claude/skills/debugging-code/reference/hypothesis-testing.md`
- Verification patterns: `~/.claude/skills/debugging-code/reference/verification-patterns.md`
- Investigation techniques: `~/.claude/skills/debugging-code/reference/investigation-techniques.md`
