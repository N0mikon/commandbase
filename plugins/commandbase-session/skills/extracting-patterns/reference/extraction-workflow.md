# Capture Workflow

The 6-step process for turning conversation knowledge into deferred-action learnings documents.

## Step 1: Dedup Check

Before creating anything, search for overlap. This prevents duplicate learnings.

**Search locations:**
- `.docs/learnings/` (previous learnings)
- `.claude/skills/` and `~/.claude/skills/` (existing skills)

**Search method:**
```sh
# Search existing learnings
rg -i "keyword1|keyword2" .docs/learnings 2>/dev/null

# Search existing skills
rg -i "keyword1|keyword2" .claude/skills ~/.claude/skills 2>/dev/null
```

**Decision matrix:**

| What You Find | Action |
|---------------|--------|
| Nothing related | Proceed to Step 2 |
| Existing learning with same discovery | Reference it, add new context if any |
| Existing skill covers this | Note as "already captured" in learnings |
| Partial overlap with existing learning | Supplement the existing document |

## Step 2: Identify the Knowledge

Run these four analysis questions against the discovery:

1. **What was the problem?** -- Describe the symptom, not the fix. Include exact error messages, unexpected behaviors, or misleading indicators.

2. **What was non-obvious?** -- What made this harder than expected? Misleading error messages? Undocumented behavior? Version-specific quirks? This is the core value.

3. **What would help next time?** -- If you hit this problem again tomorrow, what shortcut would save time?

4. **What are the exact trigger conditions?** -- When does this problem appear? Specific framework versions, configurations, environments, or sequences of events.

If any of these questions yields a weak answer ("it was just a typo", "the docs covered this"), the discovery may not be worth capturing. See quality-gates.md for the worth-assessment criteria.

## Step 3: Gather Error Context

Review the current conversation for errors:
1. Identify tool failures, skill failures, and repeated attempts
2. For each error: note the tool name, what was attempted, and the resolution
3. Correlate errors with discoveries — which errors led to which learnings?
4. Include correlated errors in the Error Summary section

## Step 4: Draft the Learnings Document

Structure the output using the learnings format (see ../templates/learnings-template.md):

**Sections:**
- Error Summary (from conversation review — omit if no meaningful errors)
- Discoveries (the core learnings with context)
- Debug References (from .docs/debug/ — omit if no debug files)
- Deferred Actions (concrete checklist of what to do next)

**Key decisions:**

*Deferred Actions must be specific:*
- Not: "Consider creating a skill"
- Yes: "Consider creating skill `prisma-pool-serverless` for connection pool exhaustion in Lambda"
- Not: "Maybe add to CLAUDE.md"
- Yes: "Add to CLAUDE.md Automatic Behaviors: always run `prisma generate` after schema changes"

## Step 5: Apply Quality Gates

Run every item in quality-gates.md before saving. No exceptions.

## Step 6: Save via docs-writer

1. Spawn a docs-writer agent with doc_type "research" and the structured content
2. Confirm to the user:

```
Learnings captured: [topic]
Location: .docs/learnings/[filename]
Discoveries: [count]
Deferred actions: [count] items to review
```
