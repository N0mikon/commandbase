---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, added IMPLEMENTED status banner, resolved open questions, updated skill naming to match deployed implementation (verb-domain pattern), corrected file locations from newskills/ to plugins/commandbase-services/skills/"
references:
  - plugins/commandbase-services/skills/brainstorming-services/SKILL.md
  - plugins/commandbase-services/skills/researching-services/SKILL.md
  - plugins/commandbase-services/skills/designing-services/SKILL.md
  - plugins/commandbase-services/skills/structuring-services/SKILL.md
  - plugins/commandbase-services/skills/planning-services/SKILL.md
  - plugins/commandbase-services/skills/implementing-services/SKILL.md
---

# Homelab Services RDSPI Workflow

> **Status: IMPLEMENTED** -- Deployed in Phase 7 (2026-02-08). All 6 services BRDSPI skills live at `plugins/commandbase-services/skills/`: `/brainstorming-services`, `/researching-services`, `/designing-services`, `/structuring-services`, `/planning-services`, `/implementing-services`. Naming evolved from `verb-noun` (`/services-research`) to `verb-domain` (`/researching-services`) to match the code and vault domain conventions. See `.docs/archive/02-08-2026-phase-7-services-brdspi-skills.md` for the full implementation plan.

## Problem

Homelab services (Docker Compose stacks, reverse proxy configs, DNS entries, backup jobs) live in a plan repo but changes are applied ad-hoc. No structured workflow for understanding state, designing changes, and executing with verification.

## Concept

Full RDSPI for infrastructure managed through a plan repo, with `/brainstorming-services` as the pre-step:

```
/brainstorming-services      <- "should I add Authelia or use Cloudflare tunnels?"
  R  /researching-services   <- map services, ports, networks, volumes, dependencies, gaps
  D  /designing-services     <- stack decisions, networking strategy, auth approach, backup policy
  S  /structuring-services   <- which compose files change, env templates, proxy routes, ordering
  P  /planning-services      <- phased tasks with success criteria
  I  /implementing-services  <- edit configs, generate deploy commands (pause for user to run)
```

## Services-Specific Considerations

- **Deployment is hands-off** — generate commands/scripts, don't execute directly
- **Secrets handling** — compose files reference `.env` files that shouldn't be read/committed
- **Post-deploy verification** — connectivity checks, log review, backup registration
- The plan repo is already file-based — Claude Code's tools work natively on it

## Open Questions (All Resolved)

- ~~How to reference the homelab plan repo? Separate working directory, env var, or CLAUDE.md pointer?~~ **Resolved: CLAUDE.md pointer. Skills read `homelab_repo_path` from CLAUDE.md; fall back to current directory if not set.**
- ~~Should research pull live state (e.g., `docker ps` via SSH) or only analyze repo files?~~ **Resolved: Both, conditionally. If `homelab_same_machine: true` in CLAUDE.md, `/researching-services` auto-runs read-only docker commands. Otherwise, it presents commands for the user to run and share output.**
- ~~Integration with monitoring (Uptime Kuma, Prometheus) for post-deploy verification?~~ **Resolved: Not built into skills. `/implementing-services` generates verification checklists (port checks, proxy routes, health checks, backup coverage) but monitoring integration is left to user's existing setup.**
- ~~Does `/starting-refactors` have a services equivalent for infrastructure reorganization?~~ **Resolved: No dedicated equivalent. `/brainstorming-services` covers infrastructure reorganization as one of its entry prompts ("Reorganizing Docker compose setup"). The full BRDSPI chain handles it from there.**
