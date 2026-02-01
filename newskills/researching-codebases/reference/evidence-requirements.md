# Evidence Requirements

Standards for research findings and red flags to watch for.

## What Counts as Evidence

Research findings must include:

- Specific file paths with line numbers (`file.ts:45-67`)
- Actual code patterns found (not assumed)
- Cross-references between components

## Not Acceptable

These phrases indicate guessing, not research:

- "The codebase likely has..."
- "Based on typical patterns..."
- "I believe there is..."
- "Usually this would be in..."
- "Most projects have..."

Every claim needs a file:line reference from actual agent findings.

## Red Flags - STOP and Spawn Agents

If you notice any of these, STOP immediately:

- About to answer without spawning any agents
- Using "likely", "probably", "typically" about the codebase
- Describing patterns without file:line references
- Synthesizing before all agents have returned
- Answering based on similar codebases you've seen
- Feeling like the question is "too simple" for agents
- About to write research document without agent results

**When you hit a red flag:**
1. Stop and acknowledge the shortcut
2. Spawn the appropriate agents
3. Wait for results
4. Only then continue

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this codebase" | Your knowledge is stale. Spawn agents. Verify. |
| "This is a simple question" | Simple questions have complex answers. Research. |
| "Agents take too long" | Wrong answers take longer to fix. Wait. |
| "I can see the pattern" | Patterns need evidence. Find file:line refs. |
| "The user is in a hurry" | Wrong research wastes more time. Be thorough. |
| "I'll just check one file" | One file isn't research. Spawn parallel agents. |
| "Similar to another project" | This codebase is unique. Verify everything. |

## Verification Checklist

Before writing the research document:

- [ ] Spawned at least 2 agents in parallel
- [ ] All agents returned results
- [ ] Every finding has a file:line reference
- [ ] No phrases like "likely" or "probably" about the codebase
- [ ] Cross-referenced findings between agents
- [ ] Noted any gaps or areas needing follow-up agents
