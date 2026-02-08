# commandbase

Personal Claude Code workflow tools - skills, agents, and hooks for the RPI workflow (research, plan, implement, validate).

## Directory Structure

```
commandbase/
├── newskills/       # Skills in development (→ ~/.claude/skills/)
├── newagents/       # Agents in development (→ ~/.claude/agents/)
├── newhooks/        # Hooks in development (→ ~/.claude/hooks/)
│   └── nudge-commit-skill/  # PostToolUse hook enforcing /committing-changes
├── scripts/         # Utility scripts
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

**Important:** When editing skills via `/auditing-skills` or directly in `~/.claude/skills/`, always copy changes back to `newskills/` before committing. The global config is live but this repo tracks history.

### Hooks Deployment

Hooks are developed in `newhooks/` and deployed to `~/.claude/hooks/`. Each hook directory includes:
- The hook script (`.py`)
- A `settings-snippet.json` showing the required `~/.claude/settings.json` config

```bash
# Deploy hook
cp newhooks/hookname/hookname.py ~/.claude/hooks/
# Then merge settings-snippet.json into ~/.claude/settings.json
```

### Commit Enforcement (3 layers)

All commits must go through `/committing-changes`. Enforced by:
1. **CLAUDE.md rule** — `~/.claude/CLAUDE.md` Git Workflow section
2. **PostToolUse nudge hook** — `~/.claude/hooks/nudge-commit-skill.py` sends feedback if direct `git commit`/`push` detected
3. **Deny rules** — `~/.claude/settings.json` hard-blocks patterns the skill never uses (`git add -A`, `--no-verify`, `--force`, `reset --hard`, etc.)

## Additional Context

- `.docs/handoffs/` - Latest session context
- `.docs/research/` - Pattern analysis from other repos
- `/auditing-docs` - Standalone skill to audit `.docs/` staleness; 4 upstream-reading skills (taking-over, planning-code, designing-code, resuming-sessions) auto-refresh stale docs via docs-updater before reading

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"), offer to save the solution as a learned pattern.
