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
| **Availability** | Recent bugs -> assume similar cause | Treat each bug as novel until evidence suggests otherwise |
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
// - Fails at [2] with timeout -> Network
// - Fails at [1] with validation error -> Validation
// - Succeeds but [3] has wrong data -> Race condition
// - Fails at [2] with 429 status -> Rate limiting
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
