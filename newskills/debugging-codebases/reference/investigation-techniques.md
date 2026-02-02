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
