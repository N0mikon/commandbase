# commandbase

Personal Claude Code workflow tools - skills, agents, and hooks for the RPI workflow (research, plan, implement, validate).

## Directory Structure

```
commandbase/
├── newskills/       # Skills in development (→ ~/.claude/skills/)
├── newagents/       # Agents in development (→ ~/.claude/agents/)
├── newhooks/        # Hooks in development (→ ~/.claude/hooks/)
└── .docs/           # Research, plans, and handoff documents
```

## Development

### Deploy to Global Config
```bash
cp -r newskills/skillname ~/.claude/skills/
cp newagents/agent.md ~/.claude/agents/
```

## Additional Context

- `.docs/handoffs/` - Latest session context
- `.docs/research/` - Pattern analysis from other repos

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"), offer to save the solution as a learned pattern.
