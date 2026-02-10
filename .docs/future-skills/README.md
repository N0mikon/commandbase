---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated services status to Implemented, removed dead naming-session link, corrected skill locations from newskills/ to plugins/"
---

# Future Skills

Design documents for skills that were conceived here and later implemented. Each file captures the original concept with motivation, design notes, and resolution of open questions. All skills in this index are now implemented and live in `plugins/<plugin>/skills/`.

## Index

| File | Skill(s) | Plugin | Status |
|---|---|---|---|
| ~~rdspi-workflow.md~~ | `/designing-code`, `/structuring-code`, `/starting-refactors` | commandbase-code | Archived (Phase 2 BRDSPI Core) |
| [brainstorming.md](brainstorming.md) | `/brainstorming-code`, `/brainstorming-vault`, `/brainstorming-services` | commandbase-code, commandbase-vault, commandbase-services | Implemented (Phase 4) |
| ~~naming-session.md~~ | `/naming-session` (absorbed into `/starting-session` in session v2) | commandbase-session | Archived (Phase 1; replaced by git-branching workflow) |
| [vault-rdspi.md](vault-rdspi.md) | `/starting-vault`, `/researching-vault`, `/designing-vault`, `/structuring-vault`, `/planning-vault`, `/implementing-vault`, `/importing-vault` | commandbase-vault | Implemented (Phase 6) |
| [services-rdspi.md](services-rdspi.md) | `/brainstorming-services`, `/researching-services`, `/designing-services`, `/structuring-services`, `/planning-services`, `/implementing-services` | commandbase-services | Implemented (Phase 7) |
| [researching-repo.md](researching-repo.md) | `/researching-repo` | commandbase-research | Implemented (Phase 3) |
| [creating-posts.md](creating-posts.md) | `/creating-posts` | commandbase-meta | Implemented (Phase 5) |
| ~~re-evaluate-existing.md~~ | `/auditing-skills`, `/auditing-agents`, `/bookmarking-code`, `/learning-from-sessions`, `docs-updater`, `/validating-code` vs `/reviewing-changes` | commandbase-core, commandbase-meta | Archived (Phases 0-2) |

## How These Connect

All three domains (code, vault, services) share the same BRDSPI phase structure with domain-specific tooling at each step. `/starting-session` (formerly `/naming-session`) ties into phase-by-phase work across all domains. Brainstorming skills are the pre-BRDSPI entry point for each domain. `/researching-repo` completes the research stack alongside `/researching-web`, `/researching-frameworks`, and `/researching-code`.

All three domains are fully implemented. Skills live in the plugin structure at `plugins/<plugin>/skills/<skill>/SKILL.md`.
