# commandbase

Personal Claude Code workflow tools - skills, agents, and hooks for the RPI workflow (research, plan, implement, validate).

## Directory Structure

```
commandbase/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace manifest (8 plugins)
├── plugins/
│   ├── commandbase-core/     # 5 skills + 4 agents (install first)
│   ├── commandbase-code/     # 8 skills + 3 agents
│   ├── commandbase-vault/    # 8 skills
│   ├── commandbase-services/ # 6 skills
│   ├── commandbase-research/ # 3 skills + 1 agent
│   ├── commandbase-git-workflow/ # 5 skills + 1 hook
│   ├── commandbase-session/  # 5 skills + 3 hooks
│   └── commandbase-meta/     # 6 skills
├── scripts/                  # Utility scripts
└── .docs/                    # Research, plans, and handoff documents
```

## Development & Deployment

### Install from Local Marketplace
```bash
# Add this repo as a marketplace source
/plugin marketplace add /c/code/commandbase

# Install plugins (core first, then domains)
/plugin install commandbase-core
/plugin install commandbase-code
/plugin install commandbase-vault
# ... etc
```

### Editing Skills in Plugins
Skills are now at `plugins/<plugin>/skills/<skill>/SKILL.md` instead of `newskills/<skill>/SKILL.md`. Edit directly in the plugin directory.

### Commit Enforcement (3 layers)
1. **CLAUDE.md rule** — `~/.claude/CLAUDE.md` Git Workflow section
2. **PostToolUse nudge hook** — bundled in commandbase-git-workflow plugin
3. **Deny rules** — manually configured in `~/.claude/settings.json` (see `plugins/commandbase-git-workflow/SETUP.md`)

## Additional Context

- `.docs/handoffs/` - Latest session context
- `.docs/research/` - Pattern analysis from other repos
- `/auditing-docs` - Standalone skill to audit `.docs/` staleness; 4 upstream-reading skills (taking-over, planning-code, designing-code, resuming-sessions) auto-refresh stale docs via docs-updater before reading

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"), offer to save the solution as a learned pattern.
