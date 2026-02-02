---
git_commit: 22359f4
last_updated: 2026-01-28
last_updated_by: rcode
topic: "Iterative Retrieval - Smarter Agent Context"
tags: [research, agents, retrieval, context]
status: complete
references:
  - C:/code/everything-claude-code/skills/iterative-retrieval/SKILL.md
  - C:/code/everything-claude-code/the-longform-guide.md
---

# Research: Iterative Retrieval Pattern

**Date**: 2026-01-28
**Source**: everything-claude-code

## Summary

Solves the "subagent context problem" where agents don't know what context they need until they start working. Implements a 4-phase progressive refinement loop (DISPATCH → EVALUATE → REFINE → LOOP) running up to 3 cycles.

## The Problem (`SKILL.md:10-20`)

Standard approaches fail:
- **Send everything**: Exceeds context limits
- **Send nothing**: Agent lacks critical information
- **Guess what's needed**: Often wrong

## The 4-Phase Loop

### Phase 1: DISPATCH (`SKILL.md:42-56`)

Initial broad query:
```javascript
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};
```

### Phase 2: EVALUATE (`SKILL.md:58-78`)

Score each file's relevance (0-1):

| Score | Classification | Meaning |
|-------|----------------|---------|
| 0.8-1.0 | High | Directly implements target |
| 0.5-0.7 | Medium | Contains related patterns |
| 0.2-0.4 | Low | Tangentially related |
| 0-0.2 | None | Not relevant, exclude |

Also identifies `missingContext` - gaps driving next refinement.

### Phase 3: REFINE (`SKILL.md:80-104`)

Update search criteria:
```javascript
{
  patterns: [...previous, ...extractPatterns(evaluation)],
  keywords: [...previous, ...extractKeywords(evaluation)],
  excludes: [...previous, ...lowRelevanceFiles],
  focusAreas: evaluation.flatMap(e => e.missingContext)
}
```

Key refinements:
- Add patterns discovered in high-relevance files
- Learn project terminology (e.g., "throttle" not "rate limit")
- Exclude files scoring < 0.2
- Target identified gaps

### Phase 4: LOOP (`SKILL.md:106-132`)

Repeat max 3 cycles. Terminate early if:
- At least 3 files with relevance >= 0.7
- No critical gaps identified

## Practical Example (`SKILL.md:154-175`)

**Task**: "Add rate limiting to API endpoints"

**Cycle 1**:
- DISPATCH: Search "rate", "limit", "api"
- EVALUATE: No matches - codebase uses "throttle"
- REFINE: Add "throttle", "middleware"

**Cycle 2**:
- DISPATCH: Search refined terms
- EVALUATE: Found throttle.ts (0.9), middleware/index.ts (0.7)
- REFINE: Need router patterns

**Cycle 3**:
- DISPATCH: Search "router", "express"
- EVALUATE: Found router-setup.ts (0.8)
- TERMINATE: Sufficient context

**Result**: throttle.ts, middleware/index.ts, router-setup.ts

## Best Practices (`SKILL.md:190-196`)

1. **Start broad, narrow progressively** - Don't over-specify initial queries
2. **Learn codebase terminology** - First cycle reveals naming conventions
3. **Track what's missing** - Explicit gap identification drives refinement
4. **Stop at "good enough"** - 3 high-relevance files beats 10 mediocre ones
5. **Exclude confidently** - Low-relevance files won't become relevant

## Adaptation for Commandbase

### Enhance Existing Agents

Add to codebase-locator, codebase-analyzer, codebase-pattern-finder:

```markdown
## Context Retrieval

When gathering context:
1. Start with broad keyword search
2. Evaluate each file's relevance (0-1 scale)
3. Identify what context is still missing
4. Refine search with new keywords/patterns
5. Repeat max 3 cycles
6. Return files with relevance >= 0.7
```

### Integration with /rcode

Current /rcode spawns agents with static prompts. With iterative retrieval:

```markdown
## Agent Instructions

When researching [topic]:
1. DISPATCH: Search broadly for [keywords]
2. EVALUATE: Score relevance of each file
3. REFINE: Note codebase terminology, adjust search
4. LOOP: Max 3 cycles until 3+ high-relevance files
5. RETURN: Files with relevance >= 0.7 and file:line refs
```

### Trade-offs

**Pros**:
- Better context efficiency
- Discovers project terminology
- Adapts to unfamiliar codebases

**Cons**:
- More agent cycles = more time
- Adds complexity to agent prompts
- Current agents may work well enough

### Recommendation

**Medium priority** - Worth adding to agent prompts if we notice agents missing relevant files or using wrong terminology. Monitor agent results before implementing.

## Code References

- Full skill: `C:/code/everything-claude-code/skills/iterative-retrieval/SKILL.md:1-203`
- 4-phase diagram: `SKILL.md:26-40`
- Scoring criteria: `SKILL.md:73-78`
- Example: `SKILL.md:154-175`
- Best practices: `SKILL.md:190-196`
