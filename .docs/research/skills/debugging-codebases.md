---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 51 commits - added frontmatter, corrected file paths from ~/.claude/skills/ to plugins/commandbase-code/skills/, added docs-writer agent step, diagnose-only mode, resume-from-file step, and fixed integration point references"
references:
  - plugins/commandbase-code/skills/debugging-code/SKILL.md
  - plugins/commandbase-code/skills/debugging-code/templates/debug-session-template.md
  - plugins/commandbase-code/skills/debugging-code/reference/hypothesis-testing.md
  - plugins/commandbase-code/skills/debugging-code/reference/verification-patterns.md
  - plugins/commandbase-code/skills/debugging-code/reference/investigation-techniques.md
---

# Research: debugging-code Skill

## Overview

The `debugging-code` skill (`plugins/commandbase-code/skills/debugging-code/SKILL.md`) implements systematic debugging using the scientific method with persistent state across context resets. It enforces hypothesis-driven investigation rather than trial-and-error fixing.

**Trigger phrases**: `debug this`, `why is this failing`, `find the bug`, `investigate this issue`, or descriptions of unexpected behavior

## The Iron Law (SKILL.md:12-24, plugin line refs approximate)

```
HYPOTHESIS BEFORE ACTION
```

**Non-negotiable rules:**
- Don't "try things" - form hypotheses and test them
- Don't fix without understanding - find root cause first
- Don't re-investigate eliminated hypotheses - check the debug file
- Don't guess at causes - gather evidence

## The Gate Function (SKILL.md:26-38, plugin line refs approximate)

Before making ANY code change, 5 questions must be answered:

1. **HYPOTHESIS**: What specific theory am I testing?
2. **FALSIFIABLE**: What evidence would prove this wrong?
3. **TEST**: What's the minimal experiment to test this?
4. **PREDICT**: What result do I expect if hypothesis is correct?
5. **ONLY THEN**: Execute the test and observe

## Initial Response Modes (SKILL.md:42-72)

### Mode 1: Existing Sessions Resume
- Checks for `.docs/debug/*.md` files
- Lists active sessions with status and current hypothesis
- User selects number to resume or describes new issue

### Mode 2: New Issue with Arguments
- Creates debug session file immediately via `docs-writer` agent (see Step 1 below)
- Begins symptom gathering

### Mode 3: No Sessions, No Arguments
- Prompts user to describe issue
- Asks for: what should happen, what actually happens, error messages

## Step 1: Create Debug Session (docs-writer agent)

The skill spawns a `docs-writer` agent via the Task tool to create the initial session file:

```
Task prompt:
  doc_type: "debug"
  topic: "<slug derived from issue description>"
  tags: [<relevant component tags>]
  content: |
    <initial debug session structure from templates/debug-session-template.md>
    Include trigger (verbatim user input) in the Symptoms section.
    Set Current Focus next_action to "gather symptoms".
```

The agent handles frontmatter (with `status: gathering`), file naming, and directory creation. After initial creation, the debug file is a **living document** -- updated directly via Edit throughout the debugging process. The `docs-writer` agent is only used for initial creation.

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
expecting: [what result means if true/false]
next_action: [immediate next step]

## Symptoms (IMMUTABLE after gathering)
trigger: [verbatim user input that started this session]
expected: [what should happen]
actual: [what actually happens]
errors: [error messages if any]
reproduction: [how to trigger]
started: [when it broke / always broken]

## Eliminated (APPEND only - prevents re-investigation)
- hypothesis: [theory that was wrong]
  evidence: [what disproved it]
  timestamp: [when eliminated]

## Evidence (APPEND only)
- timestamp: [when found]
  checked: [what was examined]
  found: [what was observed]
  implication: [what this means]

## Resolution (OVERWRITE as understanding evolves)
root_cause: [empty until found]
fix: [empty until applied]
verification: [empty until verified]
files_changed: []
```

### Section Mutation Rules

| Section | Rule | Rationale |
|---------|------|-----------|
| Frontmatter `status` | OVERWRITE | Reflects current phase |
| Current Focus | OVERWRITE | Always reflects NOW |
| Symptoms | IMMUTABLE after gathering | Reference point for verification |
| Eliminated | APPEND only | Prevents re-investigation |
| Evidence | APPEND only | Builds case for root cause |
| Resolution | OVERWRITE | Evolves as understanding grows |

### Status Transitions

```
gathering -> investigating -> fixing -> verifying -> resolved
                  ^              |           |
                  |______________|___________|
                  (if verification fails)
```

## Step 2: Gather Symptoms

Collect information the USER knows (not technical investigation):

1. **Expected behavior** - What should happen?
2. **Actual behavior** - What happens instead?
3. **Error messages** - Any errors shown?
4. **Timeline** - When did this start? Did it ever work?
5. **Reproduction** - How do you trigger this?

Update debug file after EACH answer. When complete, mark Symptoms section as complete, update status to "investigating", and proceed.

## Step 3: Investigation Loop

**Update debug file BEFORE each action, not after.**

### Phase A: Initial Evidence Gathering
- Search codebase for error text if errors exist
- Identify relevant code area from symptoms
- Read relevant files COMPLETELY
- Run code/tests to observe behavior
- APPEND to Evidence section after each finding

### Phase B: Form Hypothesis
Based on evidence, form a SPECIFIC, FALSIFIABLE hypothesis.

See `reference/hypothesis-testing.md` for what makes a hypothesis falsifiable, how to design experiments, and cognitive biases to avoid.

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
- **CONFIRMED**: Update Resolution.root_cause, proceed to Step 4 or Step 5
- **ELIMINATED**: Append to Eliminated section, return to Phase B with new hypothesis

See `reference/investigation-techniques.md` for debugging techniques.

## Step 4: Diagnose Only (Optional)

If user wants diagnosis without fix, output a report with root cause, evidence, files involved, and suggested fix direction. Offer options: "Fix it", "I'll fix it manually", or "/learning-from-sessions" to extract learnings.

## Step 5: Fix and Verify

1. Update status to "fixing"
2. Implement MINIMAL change that addresses root cause
3. Update Resolution.fix and Resolution.files_changed
4. Update status to "verifying"
5. Test against original Symptoms
6. If verification FAILS: status -> "investigating", return to Step 3
7. If verification PASSES: Update Resolution.verification
8. Output completion report

## Step 6: Resume from File

When resuming an existing session:

1. Read full debug file
2. Announce: "Resuming debug session: {slug}"
3. Report: status, current hypothesis, evidence count, eliminated count
4. Continue from Current Focus.next_action

The debug file IS the debugging brain. Perfect resume from any interruption.

## Verification Standards

A fix is verified when ALL are true:
1. Original issue no longer occurs
2. You understand why the fix works
3. Related functionality still works (regression testing)
4. Fix is stable (works consistently, not "worked once")

See `reference/verification-patterns.md` for reproduction, regression, and stability testing details.

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
- Debug file not updated before taking action

## Integration Points

- `/learning-from-sessions`: After resolving, offer to extract learnings
- `/committing-changes`: After fix verified, suggest committing
- `/researching-code`: If investigation reveals need for broader codebase understanding

## File References

- Main: `plugins/commandbase-code/skills/debugging-code/SKILL.md`
- Debug session template: `plugins/commandbase-code/skills/debugging-code/templates/debug-session-template.md`
- Hypothesis testing: `plugins/commandbase-code/skills/debugging-code/reference/hypothesis-testing.md`
- Verification patterns: `plugins/commandbase-code/skills/debugging-code/reference/verification-patterns.md`
- Investigation techniques: `plugins/commandbase-code/skills/debugging-code/reference/investigation-techniques.md`
