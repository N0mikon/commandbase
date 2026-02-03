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

### Workflow: This Repo ↔ Global Config

**This repo is the source of truth.** Skills are developed here and deployed to global.

```bash
# Deploy to global (after development)
cp -r newskills/skillname ~/.claude/skills/
cp newagents/agent.md ~/.claude/agents/

# Sync back to repo (after editing deployed skills)
cp ~/.claude/skills/skillname/SKILL.md newskills/skillname/SKILL.md
```

**Important:** When editing skills via `/updating-skills` or directly in `~/.claude/skills/`, always copy changes back to `newskills/` before committing. The global config is live but this repo tracks history.

## Additional Context

- `.docs/handoffs/` - Latest session context
- `.docs/research/` - Pattern analysis from other repos

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"), offer to save the solution as a learned pattern.
