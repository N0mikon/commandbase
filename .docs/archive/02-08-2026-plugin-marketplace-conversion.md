---
date: 2026-02-08
status: complete
topic: "Plugin Marketplace Conversion"
tags: [plan, implementation, plugin-marketplace, skills, agents, hooks, restructuring]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Bumped git_commit (was 23 commits behind). Removed deleted paths from references. Archive reason and body content remain accurate as historical record."
references:
  - .docs/research/02-08-2026-plugin-conversion-analysis-skills-agents-hooks.md
  - .docs/research/02-08-2026-plugin-marketplace-repo-best-practices-for-claude.md
archived: 2026-02-09
archive_reason: "Plan fully implemented in commit 87a19a3. All 10 phases completed. Old directories (newskills/, newagents/, newhooks/) deleted. Subsequent session skills v2 refactor (commits 92113aa-147ccfd) and analyzing-research skill addition (d8efed8) have evolved the plugin contents beyond what this plan describes, making it a historical record only."
---

# Plugin Marketplace Conversion Implementation Plan

## Overview

Restructure the commandbase repo from its current flat layout (newskills/, newagents/, newhooks/) into a Claude Code plugin marketplace containing 8 domain-based plugins. This is a structural conversion only — no skill content changes, no generalization for public use.

## Current State Analysis

The repo contains 47 skills in `newskills/`, 8 agents in `newagents/`, and 4 hooks in `newhooks/`. All are deployed manually via `cp -r` to `~/.claude/skills/`, `~/.claude/agents/`, and `~/.claude/hooks/` respectively. There is no plugin infrastructure (no `.claude-plugin/`, no `plugin.json`, no `marketplace.json`).

Skills follow a progressive disclosure pattern:
- Simple skills: `SKILL.md` only (e.g., `committing-changes/`)
- Medium skills: `SKILL.md` + `reference/` (e.g., `researching-code/`)
- Complex skills: `SKILL.md` + `reference/` + `templates/` (e.g., `creating-skills/`, `planning-code/`)

Hooks are Python scripts paired with `settings-snippet.json` files that show the required `~/.claude/settings.json` configuration. The snippets contain both hook definitions (bundleable in plugins) and deny rules (NOT bundleable).

### Key Discoveries:
- Plugins CAN bundle agents (`agents/` directory at plugin root)
- Plugins CAN bundle hooks (`hooks/hooks.json` or inline in `plugin.json`)
- Plugins CANNOT modify `settings.json` — deny rules need manual user setup
- No formal plugin-to-plugin dependency mechanism exists
- `reference/` and `templates/` subdirectories within skills deploy correctly in plugins
- Plugin hook scripts can reference `${CLAUDE_PLUGIN_ROOT}` for portable paths
- `discussing-features` skill is archived (absorbed by brainstorming-code + designing-code) — excluded from plugins

## Desired End State

The commandbase repo is a self-contained plugin marketplace with this structure:

```
commandbase/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest listing 8 plugins
├── plugins/
│   ├── commandbase-core/         # 5 skills + 4 agents
│   ├── commandbase-code/         # 8 skills + 3 agents
│   ├── commandbase-vault/        # 8 skills
│   ├── commandbase-services/     # 6 skills
│   ├── commandbase-research/     # 3 skills + 1 agent
│   ├── commandbase-git-workflow/ # 5 skills + 1 hook
│   ├── commandbase-session/      # 5 skills + 3 hooks
│   └── commandbase-meta/         # 6 skills
├── scripts/                      # Existing utility scripts (unchanged)
├── .docs/                        # Existing docs (unchanged)
└── CLAUDE.md                     # Updated for new structure
```

Each plugin has:
```
plugin-name/
├── .claude-plugin/plugin.json    # Plugin manifest
├── skills/                       # Skill directories with SKILL.md + reference/ + templates/
├── agents/                       # Agent .md files (if applicable)
├── hooks/hooks.json              # Hook definitions (if applicable)
└── scripts/                      # Hook Python scripts (if applicable)
```

Verification:
- All 46 active skills (47 minus discussing-features) are placed in exactly one plugin
- All 8 agents are placed in exactly one plugin
- All 4 hooks are converted to plugin hooks.json format
- `marketplace.json` references all 8 plugins
- Each `plugin.json` is valid with name and description
- Old `newskills/`, `newagents/`, `newhooks/` directories are removed
- CLAUDE.md reflects the new structure and deployment workflow

## What We're NOT Doing

- NOT changing any skill content (SKILL.md files are moved as-is)
- NOT generalizing personal workflow patterns for public use
- NOT publishing to any marketplace (repo stays private)
- NOT changing agent system prompts or behavior
- NOT modifying hook Python script logic
- NOT removing the manual `~/.claude/` deployment path (it changes but still exists)
- NOT addressing the `keybindings-help` skill (exists in `~/.claude/skills/` but not tracked in this repo)
- NOT creating README.md files for individual plugins (can be added later)

## Implementation Approach

Move skills, agents, and hooks from their current flat directories into domain-based plugin directories using `git mv` to preserve history. Create plugin manifests and convert hook settings-snippets to plugin hooks.json format. Update CLAUDE.md with the new structure and deployment workflow. Each phase creates one complete, self-contained plugin.

Shared agents (docs-writer, docs-updater, docs-locator, docs-analyzer) live in commandbase-core. Other plugins that depend on these agents document "install commandbase-core first" in their plugin.json description. Since there's no formal dependency mechanism, this is documentation-based.

## Phase 1: Marketplace Scaffolding

### Overview
Create the marketplace structure and plugin directories. This phase establishes the skeleton that all subsequent phases populate.

### Changes Required:

#### 1. Create marketplace manifest
**File**: `.claude-plugin/marketplace.json`
**Changes**: Create the marketplace manifest listing all 8 plugins

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "commandbase",
  "version": "1.0.0",
  "description": "Personal Claude Code workflow tools — skills, agents, and hooks for the RPI workflow",
  "owner": {
    "name": "N0mikon"
  },
  "plugins": [
    {
      "name": "commandbase-core",
      "description": "Shared documentation agents and standalone utility skills. Install this first — other commandbase plugins depend on its agents.",
      "source": "./plugins/commandbase-core",
      "category": "productivity"
    },
    {
      "name": "commandbase-code",
      "description": "Code BRDSPI workflow — brainstorm, research, design, structure, plan, implement for software projects. Requires commandbase-core.",
      "source": "./plugins/commandbase-code",
      "category": "development"
    },
    {
      "name": "commandbase-vault",
      "description": "Vault BRDSPI workflow for Obsidian vault management. Requires commandbase-core.",
      "source": "./plugins/commandbase-vault",
      "category": "productivity"
    },
    {
      "name": "commandbase-services",
      "description": "Services BRDSPI workflow for homelab Docker infrastructure. Requires commandbase-core.",
      "source": "./plugins/commandbase-services",
      "category": "development"
    },
    {
      "name": "commandbase-research",
      "description": "Web and framework research with sourced documentation output. Requires commandbase-core.",
      "source": "./plugins/commandbase-research",
      "category": "productivity"
    },
    {
      "name": "commandbase-git-workflow",
      "description": "Opinionated git commit workflow with security review and docs staleness detection. Requires commandbase-core.",
      "source": "./plugins/commandbase-git-workflow",
      "category": "development"
    },
    {
      "name": "commandbase-session",
      "description": "Session continuity — naming, handover, takeover, error tracking, and learning extraction. Requires commandbase-core.",
      "source": "./plugins/commandbase-session",
      "category": "productivity"
    },
    {
      "name": "commandbase-meta",
      "description": "Skill, agent, and hook authoring tools for building Claude Code extensions.",
      "source": "./plugins/commandbase-meta",
      "category": "development"
    }
  ]
}
```

#### 2. Create plugin directory skeleton
**Directories to create**:
```
plugins/commandbase-core/.claude-plugin/
plugins/commandbase-core/skills/
plugins/commandbase-core/agents/
plugins/commandbase-code/.claude-plugin/
plugins/commandbase-code/skills/
plugins/commandbase-code/agents/
plugins/commandbase-vault/.claude-plugin/
plugins/commandbase-vault/skills/
plugins/commandbase-services/.claude-plugin/
plugins/commandbase-services/skills/
plugins/commandbase-research/.claude-plugin/
plugins/commandbase-research/skills/
plugins/commandbase-research/agents/
plugins/commandbase-git-workflow/.claude-plugin/
plugins/commandbase-git-workflow/skills/
plugins/commandbase-git-workflow/hooks/
plugins/commandbase-git-workflow/scripts/
plugins/commandbase-session/.claude-plugin/
plugins/commandbase-session/skills/
plugins/commandbase-session/hooks/
plugins/commandbase-session/scripts/
plugins/commandbase-meta/.claude-plugin/
plugins/commandbase-meta/skills/
```

### Success Criteria:
- [x] `.claude-plugin/marketplace.json` exists and is valid JSON
- [x] All 8 plugin directories exist with `.claude-plugin/` subdirectory
- [x] Plugin directories that need agents/ hooks/ scripts/ have those subdirectories

---

## Phase 2: commandbase-core Plugin

### Overview
Populate the foundation plugin with 5 utility skills and 4 documentation agents. This is the dependency layer for all other plugins.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-core/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-core",
  "version": "1.0.0",
  "description": "Shared documentation agents and standalone utility skills. Install this first — other commandbase plugins depend on its agents (docs-writer, docs-updater, docs-locator, docs-analyzer)."
}
```

#### 2. Move skills (git mv)
- `newskills/bookmarking-code/` → `plugins/commandbase-core/skills/bookmarking-code/`
- `newskills/updating-claude-md/` → `plugins/commandbase-core/skills/updating-claude-md/`
- `newskills/debating-options/` → `plugins/commandbase-core/skills/debating-options/`
- `newskills/validating-code/` → `plugins/commandbase-core/skills/validating-code/`
- `newskills/starting-projects/` → `plugins/commandbase-core/skills/starting-projects/`

#### 3. Move agents (git mv)
- `newagents/docs-writer.md` → `plugins/commandbase-core/agents/docs-writer.md`
- `newagents/docs-updater.md` → `plugins/commandbase-core/agents/docs-updater.md`
- `newagents/docs-locator.md` → `plugins/commandbase-core/agents/docs-locator.md`
- `newagents/docs-analyzer.md` → `plugins/commandbase-core/agents/docs-analyzer.md`

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 5 skills moved with all subdirectories (reference/, templates/) preserved
- [x] 4 agents moved
- [x] Original locations are empty (git mv removes source)

---

## Phase 3: commandbase-code Plugin

### Overview
Populate the code development workflow plugin with 8 BRDSPI skills and 3 code analysis agents.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-code/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-code",
  "version": "1.0.0",
  "description": "Code BRDSPI workflow — brainstorm, research, design, structure, plan, implement chain for software projects. Requires commandbase-core for docs agents."
}
```

#### 2. Move skills (git mv)
- `newskills/brainstorming-code/` → `plugins/commandbase-code/skills/brainstorming-code/`
- `newskills/researching-code/` → `plugins/commandbase-code/skills/researching-code/`
- `newskills/designing-code/` → `plugins/commandbase-code/skills/designing-code/`
- `newskills/structuring-code/` → `plugins/commandbase-code/skills/structuring-code/`
- `newskills/planning-code/` → `plugins/commandbase-code/skills/planning-code/`
- `newskills/implementing-plans/` → `plugins/commandbase-code/skills/implementing-plans/`
- `newskills/starting-refactors/` → `plugins/commandbase-code/skills/starting-refactors/`
- `newskills/debugging-code/` → `plugins/commandbase-code/skills/debugging-code/`

#### 3. Move agents (git mv)
- `newagents/code-locator.md` → `plugins/commandbase-code/agents/code-locator.md`
- `newagents/code-analyzer.md` → `plugins/commandbase-code/agents/code-analyzer.md`
- `newagents/code-librarian.md` → `plugins/commandbase-code/agents/code-librarian.md`

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 8 skills moved with all subdirectories preserved (especially planning-code/reference/, planning-code/templates/, researching-code/reference/, researching-code/templates/, designing-code/reference/, designing-code/templates/, creating reference dirs)
- [x] 3 agents moved
- [x] Original locations are empty

---

## Phase 4: commandbase-vault Plugin

### Overview
Populate the Obsidian vault workflow plugin with 8 vault BRDSPI skills.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-vault/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-vault",
  "version": "1.0.0",
  "description": "Vault BRDSPI workflow for Obsidian vault management — brainstorm, research, design, structure, plan, implement chain. Requires commandbase-core for docs agents."
}
```

#### 2. Move skills (git mv)
- `newskills/brainstorming-vault/` → `plugins/commandbase-vault/skills/brainstorming-vault/`
- `newskills/starting-vault/` → `plugins/commandbase-vault/skills/starting-vault/`
- `newskills/researching-vault/` → `plugins/commandbase-vault/skills/researching-vault/`
- `newskills/designing-vault/` → `plugins/commandbase-vault/skills/designing-vault/`
- `newskills/structuring-vault/` → `plugins/commandbase-vault/skills/structuring-vault/`
- `newskills/planning-vault/` → `plugins/commandbase-vault/skills/planning-vault/`
- `newskills/implementing-vault/` → `plugins/commandbase-vault/skills/implementing-vault/`
- `newskills/importing-vault/` → `plugins/commandbase-vault/skills/importing-vault/`

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 8 skills moved with all subdirectories preserved
- [x] Original locations are empty

---

## Phase 5: commandbase-services Plugin

### Overview
Populate the homelab services workflow plugin with 6 services BRDSPI skills.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-services/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-services",
  "version": "1.0.0",
  "description": "Services BRDSPI workflow for homelab Docker infrastructure — brainstorm, research, design, structure, plan, implement chain. Requires commandbase-core for docs agents."
}
```

#### 2. Move skills (git mv)
- `newskills/brainstorming-services/` → `plugins/commandbase-services/skills/brainstorming-services/`
- `newskills/researching-services/` → `plugins/commandbase-services/skills/researching-services/`
- `newskills/designing-services/` → `plugins/commandbase-services/skills/designing-services/`
- `newskills/structuring-services/` → `plugins/commandbase-services/skills/structuring-services/`
- `newskills/planning-services/` → `plugins/commandbase-services/skills/planning-services/`
- `newskills/implementing-services/` → `plugins/commandbase-services/skills/implementing-services/`

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 6 skills moved with all subdirectories preserved
- [x] Original locations are empty

---

## Phase 6: commandbase-research Plugin

### Overview
Populate the web/framework research plugin with 3 research skills and the web-researcher agent.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-research/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-research",
  "version": "1.0.0",
  "description": "Web and framework research with sourced documentation output. Requires commandbase-core for docs agents."
}
```

#### 2. Move skills (git mv)
- `newskills/researching-web/` → `plugins/commandbase-research/skills/researching-web/`
- `newskills/researching-frameworks/` → `plugins/commandbase-research/skills/researching-frameworks/`
- `newskills/researching-repo/` → `plugins/commandbase-research/skills/researching-repo/`

#### 3. Move agent (git mv)
- `newagents/web-researcher.md` → `plugins/commandbase-research/agents/web-researcher.md`

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 3 skills moved with all subdirectories preserved
- [x] 1 agent moved
- [x] Original locations are empty

---

## Phase 7: commandbase-git-workflow Plugin

### Overview
Populate the git workflow plugin with 5 skills and convert the nudge-commit-skill hook to plugin format. Document deny rules that must be configured manually.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-git-workflow/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-git-workflow",
  "version": "1.0.0",
  "description": "Opinionated git commit workflow with security review and docs staleness detection. Requires commandbase-core for docs agents. NOTE: For full commit enforcement, manually add deny rules from SETUP.md to your ~/.claude/settings.json."
}
```

#### 2. Move skills (git mv)
- `newskills/committing-changes/` → `plugins/commandbase-git-workflow/skills/committing-changes/`
- `newskills/reviewing-changes/` → `plugins/commandbase-git-workflow/skills/reviewing-changes/`
- `newskills/reviewing-security/` → `plugins/commandbase-git-workflow/skills/reviewing-security/`
- `newskills/creating-prs/` → `plugins/commandbase-git-workflow/skills/creating-prs/`
- `newskills/auditing-docs/` → `plugins/commandbase-git-workflow/skills/auditing-docs/`

#### 3. Move and convert hook
- `newhooks/nudge-commit-skill/nudge-commit-skill.py` → `plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py`

#### 4. Create hooks.json
**File**: `plugins/commandbase-git-workflow/hooks/hooks.json`
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nudge-commit-skill.py'"
          }
        ]
      }
    ]
  }
}
```

#### 5. Create SETUP.md for deny rules
**File**: `plugins/commandbase-git-workflow/SETUP.md`
Document the deny rules that must be manually added to `~/.claude/settings.json`:
```json
{
  "permissions": {
    "deny": [
      "Bash(git add -A*)",
      "Bash(git add . *)",
      "Bash(git add .)",
      "Bash(git commit --no-verify*)",
      "Bash(git commit -n *)",
      "Bash(git push --force*)",
      "Bash(git push -f *)",
      "Bash(git reset --hard*)",
      "Bash(git checkout .)",
      "Bash(git restore .)",
      "Bash(git clean -f*)"
    ]
  }
}
```

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 5 skills moved with all subdirectories preserved
- [x] `hooks/hooks.json` exists with PostToolUse hook using `${CLAUDE_PLUGIN_ROOT}`
- [x] `scripts/nudge-commit-skill.py` exists (moved from newhooks/)
- [x] `SETUP.md` documents required deny rules
- [x] Original locations are empty

---

## Phase 8: commandbase-session Plugin

### Overview
Populate the session management plugin with 5 skills and convert 3 hooks to plugin format.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-session/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-session",
  "version": "1.0.0",
  "description": "Session continuity — naming, handover, takeover, resume, error tracking, and learning extraction. Requires commandbase-core for docs agents."
}
```

#### 2. Move skills (git mv)
- `newskills/naming-session/` → `plugins/commandbase-session/skills/naming-session/`
- `newskills/handing-over/` → `plugins/commandbase-session/skills/handing-over/`
- `newskills/taking-over/` → `plugins/commandbase-session/skills/taking-over/`
- `newskills/resuming-sessions/` → `plugins/commandbase-session/skills/resuming-sessions/`
- `newskills/learning-from-sessions/` → `plugins/commandbase-session/skills/learning-from-sessions/`

#### 3. Move hook scripts
- `newhooks/track-errors/track-errors.py` → `plugins/commandbase-session/scripts/track-errors.py`
- `newhooks/harvest-errors/harvest-errors.py` → `plugins/commandbase-session/scripts/harvest-errors.py`
- `newhooks/trigger-learning/trigger-learning.py` → `plugins/commandbase-session/scripts/trigger-learning.py`

#### 4. Create hooks.json
**File**: `plugins/commandbase-session/hooks/hooks.json`
```json
{
  "hooks": {
    "PostToolUseFailure": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/track-errors.py'"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/harvest-errors.py'"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/trigger-learning.py'"
          }
        ]
      }
    ]
  }
}
```

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 5 skills moved with all subdirectories preserved
- [x] `hooks/hooks.json` exists with all 3 hook events using `${CLAUDE_PLUGIN_ROOT}`
- [x] 3 Python scripts in `scripts/` (moved from newhooks/)
- [x] Original locations are empty

---

## Phase 9: commandbase-meta Plugin

### Overview
Populate the meta/authoring plugin with 6 skills for creating and auditing Claude Code extensions.

### Changes Required:

#### 1. Create plugin manifest
**File**: `plugins/commandbase-meta/.claude-plugin/plugin.json`
```json
{
  "name": "commandbase-meta",
  "version": "1.0.0",
  "description": "Skill, agent, and hook authoring tools for building Claude Code extensions."
}
```

#### 2. Move skills (git mv)
- `newskills/creating-skills/` → `plugins/commandbase-meta/skills/creating-skills/`
- `newskills/creating-agents/` → `plugins/commandbase-meta/skills/creating-agents/`
- `newskills/creating-hooks/` → `plugins/commandbase-meta/skills/creating-hooks/`
- `newskills/auditing-skills/` → `plugins/commandbase-meta/skills/auditing-skills/`
- `newskills/auditing-agents/` → `plugins/commandbase-meta/skills/auditing-agents/`
- `newskills/creating-posts/` → `plugins/commandbase-meta/skills/creating-posts/`

### Success Criteria:
- [x] `plugin.json` exists and is valid
- [x] 6 skills moved with all subdirectories preserved (especially creating-skills/reference/, creating-skills/templates/)
- [x] Original locations are empty

---

## Phase 10: Cleanup and Migration

### Overview
Remove old directories, archive the deprecated discussing-features skill, update CLAUDE.md, and verify the complete marketplace structure.

### Changes Required:

#### 1. Archive discussing-features
- Move `newskills/discussing-features/` to `.docs/archive/discussing-features/` (or delete if preferred — it's been absorbed by brainstorming-code + designing-code)

#### 2. Remove empty old directories
After all git mv operations, these should be empty:
- `newskills/` — should be empty (all 46 active skills moved, 1 archived)
- `newagents/` — should be empty (all 8 agents moved)
- `newhooks/` — should be empty (all 4 hook dirs processed)

Remove these directories once confirmed empty.

#### 3. Update CLAUDE.md
Replace the current directory structure and deployment sections with:

```markdown
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
```

#### 4. Update .gitignore if needed
Ensure `.claude-plugin/` directories are NOT gitignored (they need to be tracked).

### Success Criteria:
- [x] `newskills/` directory removed (empty)
- [x] `newagents/` directory removed (empty)
- [x] `newhooks/` directory removed (empty)
- [x] `discussing-features` archived or deleted
- [x] CLAUDE.md updated with new structure and deployment workflow
- [x] Final inventory check: 46 skills + 8 agents + 4 hooks across 8 plugins
- [x] `marketplace.json` lists all 8 plugins with correct relative paths
- [x] Each `plugin.json` is valid JSON with at minimum `name` and `description`

---

## Testing Strategy

### Structure Validation:
- Verify all 8 `plugin.json` files are valid JSON
- Verify `marketplace.json` is valid JSON and lists all 8 plugins
- Verify each plugin's `source` path resolves correctly from marketplace root
- Count skills per plugin matches expected (5+8+8+6+3+5+5+6 = 46)
- Count agents per plugin matches expected (4+3+0+0+1+0+0+0 = 8)
- Verify no skills remain in `newskills/` after migration

### Hook Validation:
- Verify `hooks.json` files are valid JSON
- Verify `${CLAUDE_PLUGIN_ROOT}` references point to existing script files
- Verify Python scripts are present in `scripts/` directories

### Subdirectory Preservation:
- Verify skills with `reference/` directories still have them (researching-code, creating-skills, planning-code, designing-code, etc.)
- Verify skills with `templates/` directories still have them

## Migration Notes

### Deployment Model Change
- **Before**: Manual `cp -r newskills/skillname ~/.claude/skills/`
- **After**: `/plugin marketplace add /c/code/commandbase` then `/plugin install commandbase-<name>`
- The `~/.claude/skills/` and `~/.claude/agents/` deployments from the old model should be cleaned up after confirming plugin installation works

### Deny Rules (Manual Step)
Plugins cannot inject deny rules into `settings.json`. The commit enforcement deny rules currently in `~/.claude/settings.json` remain there — they were already manually configured. The `SETUP.md` in commandbase-git-workflow documents these for reference/new installations.

### Hook Script Path Change
Hook scripts previously referenced `~/.claude/hooks/script.py`. In plugin format, they use `${CLAUDE_PLUGIN_ROOT}/scripts/script.py`. The Python scripts themselves don't need modification — only the `hooks.json` wrapper that calls them uses the new path variable.

## References

- `.docs/research/02-08-2026-plugin-conversion-analysis-skills-agents-hooks.md` — Component inventory and plugin architecture
- `.docs/research/02-08-2026-plugin-marketplace-repo-best-practices-for-claude.md` — Marketplace structure and best practices
- Official plugin docs: https://code.claude.com/docs/en/plugins
- Plugin reference: https://code.claude.com/docs/en/plugins-reference
