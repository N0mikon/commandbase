---
date: 2026-02-09
status: draft
topic: "README.md creation for commandbase marketplace"
tags: [plan, readme, marketplace, documentation, plugins, implementation]
git_commit: f30a465
references:
  - .docs/research/02-09-2026-readme-best-practices-for-claude-code-plugin-marketplaces.md
  - README.md
  - CLAUDE.md
  - .claude-plugin/marketplace.json
---

# README.md Creation for commandbase Marketplace

## Goal
Replace the incomplete 18-line README.md with a public-facing marketplace README, add per-plugin README.md files, add an MIT LICENSE, and fix a count error in CLAUDE.md. Writing style must follow anti-AI voice patterns from the `/creating-posts` skill.

## What We're NOT Doing
- Not changing any skill, agent, or hook functionality
- Not restructuring the plugin directory layout
- Not adding CHANGELOG.md or CONTRIBUTING.md (could be future work)
- Not creating animated GIFs or screenshots (no terminal recording tooling assumed)
- Not modifying marketplace.json or plugin.json files

## Upstream Research
- `.docs/research/02-09-2026-readme-best-practices-for-claude-code-plugin-marketplaces.md` — synthesizes patterns from GitHub Docs, Make a README, Awesome README, VS Code Extension API, npm, Anthropic official plugins

## Writing Style Rules (Anti-AI Voice)
All written content must follow these rules from `~/.claude/references/voice-tone-guide.md`:
- **Use contractions**: "don't" not "do not", "it's" not "it is"
- **Active voice**: "We built this" not "This was built"
- **Vary sentence length**: Mix 5-word fragments with longer constructions
- **No throat-clearing**: Skip "It's important to note that..." — start with the point
- **Tier 1 banned words**: Never use "delve", "leverage", "utilize", "landscape", "tapestry", "groundbreaking", "revolutionary", "cutting-edge", "holistic", "synergy", "paradigm", "cornerstone", "unleash", "unlock", "embark", "pivotal", "paramount", "spearhead", "beacon", "testament to"
- **Tier 2 watch**: Limit "robust", "comprehensive", "seamless", "innovative", "transformative", "foster", "navigate" (metaphorical), "harness", "streamline", "enhance", "furthermore", "moreover", "additionally"
- **Specific over vague**: Concrete examples beat abstract claims
- **No parallel construction overuse**: If 3 sentences start the same way, rewrite one

## Phase 1: Add MIT LICENSE

### Goal
Add a standard MIT LICENSE file to unblock the license badge and establish clear terms.

### Tasks
- [x] Create `LICENSE` in repo root with MIT text, copyright "2026 N0mikon"
- [x] Verify file renders correctly on GitHub (standard MIT recognition)

### Success Criteria
- `LICENSE` file exists at repo root
- Contains standard MIT license text with correct copyright holder

---

## Phase 2: Write Root README.md

### Goal
Replace the 18-line stub with a public-facing marketplace README following the 11-section structure from research.

### Tasks
- [x] Write title line: `# commandbase`
- [x] Add 2-3 shields.io badges: license (MIT), plugins (8 plugins), skills (46 skills)
- [x] Write one-liner description (from marketplace.json: "Personal Claude Code workflow tools — skills, agents, and hooks for the RPI workflow")
- [x] Write Overview section: what commandbase is, who it's for, the BRDSPI workflow concept in 2-3 sentences
- [x] Write Plugin Inventory table with columns: Plugin | Description | Skills | Agents | Hooks | link to per-plugin README

  Plugin inventory data (verified):
  | Plugin | Description | Skills | Agents | Hooks |
  |--------|-------------|--------|--------|-------|
  | commandbase-core | Shared docs agents + utility skills. Install first. | 5 | 4 | 0 |
  | commandbase-code | Code BRDSPI workflow for software projects | 8 | 3 | 0 |
  | commandbase-vault | Vault BRDSPI workflow for Obsidian vault management | 8 | 0 | 0 |
  | commandbase-services | Services BRDSPI workflow for homelab Docker infrastructure | 6 | 0 | 0 |
  | commandbase-research | Web and framework research with sourced output | 4 | 1 | 0 |
  | commandbase-git-workflow | Opinionated git commit workflow with security review | 5 | 0 | 1 |
  | commandbase-session | Session continuity with git branching + worktrees | 4 | 0 | 4 |
  | commandbase-meta | Skill, agent, and hook authoring tools | 6 | 0 | 0 |

- [x] Write Quick Start section with prerequisite (Claude Code installed), marketplace add command, and install sequence (core first, then others)
- [x] Write Windows Setup section (preserve existing content about CLAUDE_CODE_GIT_BASH_PATH, refine wording)
- [x] Write Development section covering: bare repo + worktrees layout, editing skills in plugins, commit enforcement (3 layers)
- [x] Write Contributing section (brief: fork, edit, test, PR)
- [x] Write License section (MIT, link to LICENSE file)
- [x] Add Table of Contents after badges/one-liner (linking to all major sections)

### Structure
```markdown
# commandbase

[badges]

One-liner description.

## Table of Contents
[auto-linked sections]

## Overview
[2-3 sentences: what, who, why, BRDSPI concept]

## Plugins
[inventory table with links to per-plugin READMEs]

## Quick Start
[prerequisites + install commands]

## Windows Setup
[CLAUDE_CODE_GIT_BASH_PATH requirement]

## Development
### Bare Repo Layout
### Editing Skills
### Commit Enforcement

## Contributing

## License
```

### Success Criteria
- README.md contains all 10 sections listed above
- All plugin counts match verified data (46 skills, 8 agents, 5 hooks)
- Installation instructions use `/plugin marketplace add` and `/plugin install` syntax
- No Tier 1 banned words appear anywhere
- Contractions used throughout (don't, it's, won't, etc.)
- Sentence length varies (no uniform 15-25 word sentences)
- Table of Contents links resolve to correct anchors

---

## Phase 3: Write Per-Plugin README.md Files

### Goal
Create 8 README.md files, one per plugin, listing all skills, agents, and hooks with one-line descriptions.

### Tasks
- [x] For each plugin, read every SKILL.md to extract the one-line description from the skill's description field or first paragraph
- [x] For each plugin, read every agent .md to extract the one-line description
- [x] For each plugin with hooks, describe what each hook does
- [x] Write `plugins/commandbase-core/README.md`
- [x] Write `plugins/commandbase-code/README.md`
- [x] Write `plugins/commandbase-vault/README.md`
- [x] Write `plugins/commandbase-services/README.md`
- [x] Write `plugins/commandbase-research/README.md`
- [x] Write `plugins/commandbase-git-workflow/README.md`
- [x] Write `plugins/commandbase-session/README.md`
- [x] Write `plugins/commandbase-meta/README.md`

### Per-Plugin README Structure
```markdown
# [plugin-name]

[Description from plugin.json]

## Dependencies
[What must be installed first, if any]

## Skills
| Skill | Description |
|-------|-------------|
| /skill-name | One-line description |

## Agents (if any)
| Agent | Description |
|-------|-------------|
| agent-name | One-line description |

## Hooks (if any)
| Event | Description |
|-------|-------------|
| HookEvent | What it does |

## Installation
```shell
/plugin install [plugin-name]
```
```

### Success Criteria
- 8 README.md files created, one per plugin directory
- Every skill listed with accurate one-line description
- Every agent listed with accurate one-line description
- Every hook listed with event type and description
- Dependencies noted (most depend on commandbase-core)
- No Tier 1 banned words
- Contractions used throughout

---

## Phase 4: Fix CLAUDE.md Session Count

### Goal
Correct the commandbase-session skills count from "3 skills" to "4 skills" in CLAUDE.md.

### Tasks
- [x] Edit `CLAUDE.md` line 18: change `# 3 skills + 4 hooks` to `# 4 skills + 4 hooks`

### Success Criteria
- CLAUDE.md shows "4 skills + 4 hooks" for commandbase-session
- No other changes to CLAUDE.md

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Skill descriptions extracted incorrectly | Verify each against SKILL.md file |
| Badge URLs break | Use standard shields.io static badge format |
| Anti-AI voice violations slip through | Run Tier 1 word scan on final README before committing |
| Links to per-plugin READMEs break | Use relative paths: `plugins/commandbase-core/README.md` |
| CLAUDE.md has other stale counts | Only fix the verified error (session count) |

## Execution Order
Phase 1 (LICENSE) → Phase 2 (root README) → Phase 3 (per-plugin READMEs) → Phase 4 (CLAUDE.md fix)

Phases 1 and 4 are independent and could run in any order, but the sequence above reads naturally for review.
