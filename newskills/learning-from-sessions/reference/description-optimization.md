# Description Optimization

When this skill generates new skills, their descriptions must work as retrieval keys for semantic matching. A perfectly written skill with a weak description will never activate.

## How Descriptions Trigger Skills

Claude Code loads skill descriptions at Level 1 (always in context, ~100 tokens per skill). When a user's request matches a description, the full SKILL.md body loads. This means:

- The description is the ONLY text Claude uses to decide whether to load the skill
- Keywords in the description must match the words users actually say
- Vague descriptions match everything (useless) or nothing (invisible)

## The Retrieval Key Formula

```
"Use this skill when [symptom or situation the user describes].
This includes [specific error message or behavior], [framework/tool name + scenario],
[alternative phrasing of the problem], and [edge case that's easy to miss]."
```

**Every component serves retrieval:**
- "Use this skill when" -- primes Claude's matching logic
- Symptom/situation -- the broad trigger
- Specific error message -- exact-match keyword for common searches
- Framework/tool + scenario -- namespace the skill to avoid false matches
- Alternative phrasing -- catches users who describe the problem differently
- Edge case -- prevents the skill from being overlooked in non-obvious situations

## Embedding Error Messages

For debugging skills, embed the actual error text users will see:

**Weak:**
```
"Use this skill when Node.js connections fail."
```

**Strong:**
```
"Use this skill when Node.js database connections fail with 'ECONNREFUSED' or
'connection pool exhausted' errors. This includes Prisma connection timeouts in
serverless environments, pg pool drain issues after deployment, and intermittent
'too many clients' errors under load."
```

The strong version matches when a user pastes an error message. The weak version matches everything and nothing.

## Embedding Framework Names

Namespace skills to their technology stack:

**Weak:**
```
"Use this skill when imports cause runtime errors."
```

**Strong:**
```
"Use this skill when TypeScript circular imports cause runtime 'undefined' errors.
This includes barrel file re-export cycles, class decorator circular references,
and module initialization order issues in NestJS or Angular projects."
```

## Embedding Action Phrases

Include the verbs users actually use when asking for help:

- "debug", "fix", "resolve", "troubleshoot" -- problem-solving actions
- "set up", "configure", "install", "deploy" -- setup actions
- "optimize", "speed up", "reduce", "improve" -- performance actions
- "migrate", "upgrade", "convert", "move" -- transition actions

## Testing Descriptions

After writing a description, test it with three scenarios:

1. **Direct match**: "I'm getting [exact error from description]" -- should clearly match
2. **Indirect match**: "[Describes the symptom without using the exact error]" -- should still match
3. **Non-match**: "[Related but different problem in the same domain]" -- should NOT match

If scenario 1 fails, the description lacks keywords.
If scenario 2 fails, the description is too narrow.
If scenario 3 matches, the description is too broad.

## Constraints

All descriptions must satisfy:
- Under 1024 characters
- No angle brackets (< or >)
- Third person voice ("Use this skill when..." not "I help you...")
- Starts with "Use this skill when..."

## Common Description Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Too vague | "Helps with database issues" | Add specific error messages and scenarios |
| Too broad | "Use for all Python development" | Narrow to specific problem domain |
| No trigger words | "A skill about React hooks" | Add "Use this skill when..." + action verbs |
| Missing technology | "Use when state management breaks" | Add framework name: "React Context" or "Redux" |
| First person | "I fix deployment failures" | "Use this skill when deployments fail..." |
| WHAT not WHEN | "Handles API rate limiting" | "Use this skill when API calls return 429..." |
