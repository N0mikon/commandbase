---
name: debugging-code
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

Or provide the issue description directly: /debugging-code [description]
```

## Process

### Step 1: Create Debug Session

Spawn a `docs-writer` agent via the Task tool to create the session file:

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

The agent handles frontmatter (with `status: gathering`), file naming, and directory creation.

**Note:** After initial creation, the debug file is a **living document** — update it directly via Edit throughout the debugging process. The `docs-writer` agent is only used for initial creation.

See `templates/debug-session-template.md` for full structure and mutation rules.

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
- "/committing-changes" - Commit the fix
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
- **`/committing-changes`**: After fix verified, suggest committing
- **`/researching-code`**: If investigation reveals need for broader codebase understanding

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
