# Anti-Patterns Reference

Red flags and rationalizations to watch for during plan implementation.

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
2. Run the Gate Function (see reference/verification-workflow.md)
3. Only proceed with evidence

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

## The Trap of "Obviously Works"

The most dangerous changes are the ones that "obviously work":
- Single-line fixes
- Copy-paste from working code
- "Just renaming"
- "Trivial refactoring"

These are exactly the changes that introduce subtle bugs. Verify them like everything else.
