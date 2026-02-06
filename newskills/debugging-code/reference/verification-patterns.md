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
// X TypeError: Cannot read property 'name' of undefined

// 3. Fix the code
function processUserData(user) {
  if (!user) return null;
  return user.name;
}

// 4. Verify test passes
// OK should handle undefined user data

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
