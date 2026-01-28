# commandbase

Personal Claude Code workflow tools - skills, agents, and hooks for the RPI workflow (research, plan, implement, validate).

## Directory Structure

```
commandbase/
├── newskills/       # Skills in development (will become ~/.claude/skills/)
├── newagents/       # Agents in development (will become ~/.claude/agents/)
├── newhooks/        # Hooks in development (will become ~/.claude/hooks/)
└── .docs/           # Research, plans, and handoff documents
    ├── research/    # Pattern research from other repos
    ├── plans/       # Implementation plans
    └── handoffs/    # Session handover documents
```

## Development Workflow

### Develop → Deploy → Iterate
1. **Develop** in `newskills/`, `newagents/`, `newhooks/`
2. **Deploy** working versions to `~/.claude/` (global config)
3. **Iterate** using v1 tools to build v2, v2 to build v3, etc.

### Key Commands
```bash
# Deploy a skill to global config
cp newskills/pcode.md ~/.claude/skills/pcode/SKILL.md

# Deploy an agent to global config
cp newagents/codebase-analyzer.md ~/.claude/agents/codebase-analyzer.md
```

## Source Repos for Patterns

Reference these repos for patterns and inspiration:
- `C:/code/superpowers/` - Enforcement patterns, skill structure
- Other repos as discovered

## Current Focus

See `.docs/handoffs/` for latest session context and `.docs/research/` for pattern analysis.
