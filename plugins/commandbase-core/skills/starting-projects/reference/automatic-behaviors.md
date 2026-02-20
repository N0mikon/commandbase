# Automatic Claude Behaviors

Behaviors that should be included in every CLAUDE.md for consistent experience.

## Pattern Learning Detection

When the user indicates a repeat problem, offer to save the pattern:

### Trigger Phrases
- "this happened before"
- "same issue again"
- "we already solved this"
- "I keep hitting this"
- "every time I..."
- "always have to..."
- "not again"
- "this keeps happening"

### Response

When triggered, after solving the problem:

```
I notice this seems like a recurring issue. Would you like me to save this as a learned pattern?

If yes, I'll extract it to `~/.claude/skills/learned/` so it's automatically available in future sessions.
```

If user agrees, follow the /extracting-patterns skill process.

### Why This Matters

- Users often re-solve the same problems across sessions
- LLMs are stateless - they don't remember previous solutions
- Learned patterns auto-load, providing persistent knowledge
- Saves time and frustration on repeat issues
