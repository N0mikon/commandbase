---
date: 2026-02-07
status: complete
topic: "Future Skills Implementation Roadmap"
tags: [plan, brdspi, skills, roadmap, infrastructure]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Frontmatter refresh only. All 7 phases complete, document is a historical record. Body references to newskills/newhooks/ paths are historically accurate (pre-plugin-marketplace). All 13 referenced sub-documents confirmed moved to .docs/archive/."
archived: 2026-02-09
archive_reason: "All 7 roadmap phases complete. Document self-recommends archival in closure notes. Repo restructured from newskills/newhooks/ to 8-plugin marketplace (commit 87a19a3). All referenced sub-documents now archived. Session skills superseded by v2 with git branching."
---

# Future Skills Implementation Roadmap

Prioritized phased plan for building future skills from `.docs/future-skills/` backlog. Organized by dependency chains, grouping related work, and separating quick wins from heavy lifts.

## Current State

**25 skills** deployed (24 original + `/naming-session`). Two renamed (`/auditing-skills`, `/auditing-agents`), four modified for session awareness (`/bookmarking-code`, `/implementing-plans`, `/handing-over`, `/learning-from-sessions`). The workflow currently follows RPI (Research, Plan, Implement). This plan expands to **BRDSPI** (Brainstorm, Research, Design, Structure, Plan, Implement) across three domains (code, vault, services), plus research completion, content creation, and remaining hook infrastructure.

**Naming convention:** All domain-specific BRDSPI skills follow `verb-domain` pattern (e.g., `/designing-code`, `/designing-vault`, `/designing-services`).

## BRDSPI Workflow

```
Brainstorm → Research → Design → Structure → Plan → Implement
    B            R          D         S          P        I
```

- **Brainstorm:** Explore direction + capture user preferences. Domain-specific.
- **Research:** Investigate codebase, web, frameworks, third-party repos.
- **Design:** Architectural decisions informed by research. Uses opus model.
- **Structure:** File placement, module organization, migration order.
- **Plan:** Task breakdown into phased implementation steps.
- **Implement:** Execute plan with verification at each phase.

**Phase weight by workflow type:**

| Workflow | B | R | D | S | P | I |
|----------|---|---|---|---|---|---|
| Greenfield MVP | Heavy | Heavy | Heavy | Heavy | Heavy | Heavy |
| Greenfield Phase | -- | Light | Medium | Light | Medium | Heavy |
| Brownfield Refactor | -- | Heavy | Medium | **Heavy** | Medium | Heavy |
| Brownfield Feature | Optional | Light | Light | Light | Light | Medium |

## Dependency Map

```
/naming-session ──────────────────────────────────────┐
     |                                                |
     ├── /bookmarking-code (session-named checkpoints) |
     ├── /implementing-plans (mandatory checkpoints)   |
     ├── /handing-over (auto-titled handoffs)          |
     └── /learning-from-sessions (session context)     |
                                                      |
              Voice/Tone Reference                    |
                    |                                 |
               /creating-posts                        |
                                                      |
Renames (/auditing-*) ─── independent                 |
                                                      |
/researching-repo ──────── independent                |
                                                      v
                              BRDSPI Core (Code)
                              /designing-code (opus)
                              /structuring-code
                              /starting-refactors
                              modified /planning-code
                                    |
                    ┌───────────────┼───────────────┐
                    v               v               v
              Vault BRDSPI    Services BRDSPI   Brainstorming skills
              (7 skills)      (5 skills)        (3 skills)
                                                + retire /discussing-features
```

---

## Phase 0: Triage & Review Existing Skills — COMPLETE
**Status:** All decisions made.

### Decisions

- [x] **`/updating-skills` + `/updating-agents`** → **RENAME** to `/auditing-skills` + `/auditing-agents`. Primary function is compliance auditing. `/creating-skills` edit mode handles actual modifications.
- [x] **`/bookmarking-code`** → **KEEP, MODIFY.** Add `/naming-session` integration → make mandatory in `/implementing-plans`.
- [x] **`/learning-from-sessions`** → **REWORK.** Automatic learning capture with deferred action. Output `.docs/learnings/` docs. Integrate with `/debugging-code` output. Don't break flow.
- [x] **`/validating-code` vs `/reviewing-changes`** → **KEEP BOTH.** Distinct purposes. Defer renaming to Phase 6/7.
- [x] **`docs-updater` agent** → **KEEP, EXPAND TRIGGERS** incrementally as skills are built.
- [x] **`/discussing-features`** → **RETIRE IN PHASE 4.** Absorb into brainstorming (preferences) + design (technical choices). Brainstorming gets domain detection + preference questions. Design gets research-informed choice questions.

---

## Phase 1: Foundations & Modifications — COMPLETE
**Effort:** Medium | **Duration:** 3 sessions | **Status:** All 10 phases done

Foundational pieces that many future skills depend on, plus Phase 0 follow-through.

**Implementation plan:** `.docs/plans/02-07-2026-phase-1-foundations-and-modifications-implementation.md`
**Handoffs:** `.docs/handoffs/02-07-2026-phase-1-foundations-implementation-phases-1-5-of-10.md`, `.docs/handoffs/02-07-2026-phase-1-foundations-implementation-phases-6-8-of-10.md`, `.docs/handoffs/02-07-2026-integration-test-end-to-end-session-workflow-test.md`

### Session 1 — Independent items — COMPLETE

#### 1a. Create `/naming-session` skill — DONE
**Complexity:** Low | **Depends on:** Nothing

- Assign short descriptive name to current session (e.g., "hook-enforcement-debug", "mvp-phase-1-auth")
- Storage: `.claude/sessions/{name}/` directory with `meta.json`, `_current` pointer file
- Auto-suggests name from native `sessions-index.json` summary field, user confirms or overrides
- Referenced by: `/handing-over`, `/bookmarking-code`, `/learning-from-sessions`
- Critical for phase-by-phase BRDSPI workflows
- Deployed to `~/.claude/skills/naming-session/`

#### 1b. Create voice/tone reference — DONE
**Complexity:** Low | **Depends on:** Nothing

- Created `~/.claude/references/voice-tone-guide.md` (116 lines) with anti-AI-voice patterns
- Three tiers: 30+ Tier 1 absolute bans, 50+ Tier 2 strong avoidance, Tier 3 contextual
- Platform norms for Twitter/X, LinkedIn, GitHub
- 3-question quick check
- Single source of truth — prevents duplication across skills

**Not a skill — shared reference document. Global config only (not tracked in commandbase).**

#### 1f. Rename `/updating-skills` to `/auditing-skills` — DONE
**Complexity:** Low | **Depends on:** Nothing

- Renamed directory, updated frontmatter `name:`, updated ~15 self-references
- Updated `CLAUDE.md:31` reference
- docs-updater ran on active `.docs/` files (2 files updated, historical docs left as-is)
- Deployed to `~/.claude/skills/auditing-skills/`

#### 1g. Rename `/updating-agents` to `/auditing-agents` — DONE
**Complexity:** Low | **Depends on:** 1f (sibling cross-references)

- Same as 1f, including sibling section now references `/auditing-skills`
- Deployed to `~/.claude/skills/auditing-agents/`
- **Note:** Old deployed copies (`~/.claude/skills/updating-skills/`, `~/.claude/skills/updating-agents/`) still need manual cleanup

### Session 2 — Dependent modifications — COMPLETE

#### 1c. Update `/bookmarking-code` for session names — DONE
**Complexity:** Low | **Depends on:** 1a

- Added Session Awareness section (checks `_current`, reads session name)
- Create workflow writes to session folder when active, global log otherwise
- Verify workflow searches session log first with global fallback
- Session-prefixed naming examples added (e.g., "auth-mvp:phase-2-done")
- Deployed to `~/.claude/skills/bookmarking-code/`

#### 1d. Update `/implementing-plans` for mandatory checkpoints — DONE
**Complexity:** Low | **Depends on:** 1c

- Checkpoint creation now mandatory ("This is NOT optional") after each phase
- Session-aware: writes to session folder when available
- Added Documentation Freshness section that spawns docs-updater for stale plan references
- Deployed to `~/.claude/skills/implementing-plans/`

#### 1e. Update `/handing-over` for session names — DONE
**Complexity:** Low | **Depends on:** 1a

- Added Session Awareness section (checks `_current`, prefixes topic with session name)
- Added Session Context body section (checkpoints, errors, meta.json link)
- Updated docs-writer call with session prefix
- Deployed to `~/.claude/skills/handing-over/`

#### 1h. Rework `/learning-from-sessions` — DONE
**Complexity:** Medium | **Depends on:** 1a

- Changed from "immediate skill creator" to "automatic learning capture with deferred action"
- Output: `.docs/learnings/` documents via docs-writer with Deferred Actions checklist
- Added Session Awareness and Debug File Integration sections
- Updated `reference/extraction-workflow.md` (fully rewritten) and `reference/quality-gates.md`
- Created new `templates/learnings-template.md` (old `extracted-skill-template.md` kept for other uses)
- Deployed all files to `~/.claude/skills/learning-from-sessions/`

### Session 3 — Hooks — COMPLETE

#### 1i. Create `track-errors` hook (Phase 9) — DONE
**Complexity:** Medium | **Depends on:** 1a

- PostToolUseFailure hook that logs tool failures to session error log
- Deployed to `newhooks/track-errors/` with `settings-snippet.json`
- Also created `harvest-errors` companion hook for backfilling errors from conversation history
- Created `/resuming-sessions` skill for session continuity

#### 1j. Create `trigger-learning` hook (Phase 10) — DONE
**Complexity:** Medium | **Depends on:** 1i

- PreCompact hook that nudges `/learning-from-sessions` when errors exist
- Also adds Learning Check section to `/handing-over`
- Deployed to `newhooks/trigger-learning/` with `settings-snippet.json`
- Requires Claude Code restart after settings.json merge

### Success Criteria
- [x] `/naming-session` skill deployed and tested
- [x] Voice/tone reference created in `~/.claude/references/`
- [x] `/auditing-skills` deployed (renamed from `/updating-skills`)
- [x] `/auditing-agents` deployed (renamed from `/updating-agents`)
- [x] `/bookmarking-code` updated with session-name integration
- [x] `/implementing-plans` updated with mandatory checkpoints + docs-updater trigger
- [x] `/handing-over` updated to use session name in handoff title
- [x] `/learning-from-sessions` reworked to automatic capture + deferred action
- [x] `track-errors` hook created and deployed (Phase 9)
- [x] `trigger-learning` hook created and deployed (Phase 10)
- [x] End-to-end integration test passed

---

## Phase 2: BRDSPI Core (Code Domain) — COMPLETE
**Effort:** High | **Duration:** 1 session | **Blocks:** Phases 4, 6, 7

The centerpiece: expand RPI to BRDSPI by adding Design and Structure phases.

### 2a. `/designing-code` skill
**Complexity:** Medium | **Depends on:** Phase 0 complete

- New D (Design) phase: architectural decisions, API shape, pattern selection, trade-offs, component boundaries, error handling, state management
- **Model: opus** — design decisions benefit from deeper reasoning
- Input: research artifacts from `/researching-code`, `/researching-web`, `/researching-frameworks`
- Also includes: technical choice questioning absorbed from `/discussing-features` (research-informed questions like "what error format?", "auth approach?")
- Output: `.docs/design/` document with rationale and decisions

### 2b. `/structuring-code` skill
**Complexity:** Medium | **Depends on:** `/designing-code` exists

- New S (Structure) phase: file placement, module organization, dependency direction, interface boundaries, test organization
- For refactors: migration order, change sequencing (heaviest phase in brownfield work)
- Input: design doc from `/designing-code`
- Output: structural map document

### 2c. Modify `/planning-code`
**Complexity:** Low | **Depends on:** `/structuring-code` exists

- Simplify: no longer does architecture work (that's D+S now)
- Receives structural map, focuses purely on task breakdown into phased implementation steps
- **Backward compatible:** if no structural map provided, works as before (for lightweight features that skip D+S)

### 2d. `/starting-refactors` skill
**Complexity:** Medium | **Depends on:** `/designing-code`, `/structuring-code`

- Brownfield parallel to `/starting-projects`
- Establishes refactor scope, snapshots current state, sets up CLAUDE.md context
- Generates initial audit of target area
- **Auto-runs `/bookmarking-code` create** before refactor starts (safety net)

### Success Criteria
- [x] `/designing-code` deployed — produces design docs with rationale, uses opus
- [x] `/structuring-code` deployed — produces structural maps
- [x] `/planning-code` modified — accepts structural map when provided, works standalone for lightweight features
- [x] `/starting-refactors` deployed — brownfield initialization works, auto-checkpoints
- [x] Full BRDSPI chain tested end-to-end (structural verification)

---

## Phase 3: Research Stack Completion — COMPLETE
**Effort:** Medium | **Duration:** 1 session | **Status:** All 4 phases done

**Implementation plan:** `.docs/plans/02-07-2026-phase-3-researching-repo-skill-implementation.md`
**Research:** `.docs/research/02-07-2026-phase-3-researching-repo-skill-pre-planning-research.md`

### `/researching-repo` skill — DONE
**Complexity:** Medium | **Depends on:** Nothing

- Clone any git repo (blobless clone to **system temp dir** with CVE-2024-32002 hardening), analyze structure/patterns/conventions
- **Before cleanup, offer:** "Keep this clone somewhere? (provide path or skip to delete)"
- Produce `.docs/research/` artifact via docs-writer agent
- **Supports any git remote:** GitHub, GitLab, Bitbucket, LinuxServer, local paths (with depth=1 fallback)
- **GitHub shorthand:** Expands `user/repo` to `https://github.com/user/repo.git`
- **Detects CLAUDE.md/AGENTS.md** if present — summarize with context awareness (in a skills repo they're the product; in an app repo they're just dev tooling)
- Analysis: directory layout, architecture patterns, naming conventions, key implementations via parallel agents
- Completes research stack:
  - `/researching-web` — community knowledge
  - `/researching-frameworks` — official API docs (Context7)
  - `/researching-code` — our code
  - `/researching-repo` — their code

**Files created:**
- `newskills/researching-repo/SKILL.md` — Main skill (10-section research skill template)
- `newskills/researching-repo/reference/clone-management.md` — Secure clone commands, temp dirs, cleanup
- `newskills/researching-repo/reference/analysis-strategies.md` — Agent decomposition, CLAUDE.md detection
- `newskills/researching-repo/templates/repo-research-template.md` — Output format for docs-writer

**Deployed to:** `~/.claude/skills/researching-repo/`

### Success Criteria
- [x] `/researching-repo` deployed and tested on a real third-party repo
- [x] Supports GitHub + non-GitHub git URLs + local paths
- [x] Offers to keep clone before cleanup
- [x] Produces useful `.docs/research/` artifact
- [x] Context-aware CLAUDE.md/AGENTS.md detection

---

## Phase 4: Brainstorming Entry Points + `/discussing-features` Retirement — COMPLETE
**Effort:** Medium | **Duration:** 1 session | **Depends on:** Phase 2 (BRDSPI Core)

**Implementation plan:** `.docs/plans/02-07-2026-phase-4-brainstorming-skills-implementation.md`
**Research:** `.docs/research/02-07-2026-phase-4-brainstorming-skills-pre-planning-research.md`

Domain-specific brainstorming as pre-BRDSPI exploratory phase. Absorbs `/discussing-features`' domain detection and preference question templates.

### 4a. `/brainstorming-code` — DONE
**Complexity:** Low-Medium | **Depends on:** BRDSPI core exists to flow into

- Pre-BRDSPI exploration: patterns, APIs, data models, existing codebase conventions
- Absorbs from `/discussing-features`: domain detection (visual/api/cli/content/system) + preference questions
- Questions: direction choices ("REST or GraphQL?") + user preferences ("cards or table?")
- **Produces `.docs/brainstorm/` artifact** capturing direction + preferences for downstream phases
- Flows into `/starting-projects` or `/starting-refactors` → R → D → S → P → I

**Files created:**
- `newskills/brainstorming-code/SKILL.md` — Main skill (5-layer structure)
- `newskills/brainstorming-code/reference/question-domains.md` — Domain-specific question templates
- `newskills/brainstorming-code/templates/brainstorm-template.md` — Output format for docs-writer

**Deployed to:** `~/.claude/skills/brainstorming-code/`

### 4b. `/brainstorming-vault` — DONE
**Complexity:** Low-Medium | **Depends on:** Nothing directly (more useful after Phase 6)

- Vault-specific exploration: structure, MOCs, tags, linking strategies
- Questions: "flat tags or nested folders?", "one MOC or topic hubs?"
- **Produces `.docs/brainstorm/` artifact**
- Flows into Vault BRDSPI when built

**Files created:**
- `newskills/brainstorming-vault/SKILL.md` — Main skill
- `newskills/brainstorming-vault/reference/vault-question-domains.md` — Vault domain questions
- `newskills/brainstorming-vault/templates/brainstorm-template.md` — Output format

**Deployed to:** `~/.claude/skills/brainstorming-vault/`

### 4c. `/brainstorming-services` — DONE
**Complexity:** Low-Medium | **Depends on:** Nothing directly (more useful after Phase 7)

- Infrastructure exploration: Docker, networking, reverse proxy, backup, dependencies
- Questions: "Authelia or Cloudflare tunnels?", "single compose or per-service?"
- **Produces `.docs/brainstorm/` artifact**
- Flows into Services BRDSPI when built

**Files created:**
- `newskills/brainstorming-services/SKILL.md` — Main skill
- `newskills/brainstorming-services/reference/services-question-domains.md` — Services domain questions
- `newskills/brainstorming-services/templates/brainstorm-template.md` — Output format

**Deployed to:** `~/.claude/skills/brainstorming-services/`

### 4d. Retire `/discussing-features` — DONE
**Complexity:** Low | **Depends on:** 4a deployed

- Archive `/discussing-features` — its content has been absorbed:
  - Domain detection + preference questions → `/brainstorming-code`
  - Research-informed technical choices → `/designing-code`
- Remove from deployed skills, keep in `newskills/` archive for reference
- `/designing-code` updated to read `.docs/brainstorm/` artifacts when available

### Success Criteria
- [x] `/brainstorming-code` deployed — produces `.docs/brainstorm/` artifacts with direction + preferences
- [x] `/brainstorming-vault` deployed and tested
- [x] `/brainstorming-services` deployed and tested
- [x] `/discussing-features` archived
- [x] Each brainstorming skill flows naturally into its domain's BRDSPI chain

---

## Phase 5: Content & Communication — COMPLETE
**Effort:** Low-Medium | **Duration:** 1 session | **Depends on:** Phase 1b (voice/tone reference)

**Implementation plan:** `.docs/plans/02-07-2026-phase-5-creating-posts-skill-implementation.md`
**Research:** `.docs/research/02-07-2026-phase-5-creating-posts-skill-pre-planning-research.md`

### `/creating-posts` — DONE
**Complexity:** Medium | **Depends on:** Voice/tone reference exists

- Draft social media posts that sound human-written
- **Generate + critique modes:** draft new posts AND review/rewrite user drafts for AI-sounding language
- Platform-aware: Reddit, Twitter/X, HN, LinkedIn, Discord
- Anti-AI-voice enforcement using voice/tone reference
- **Auto-reads project files** (README, CLAUDE.md, package.json) for context, asks user clarifying questions when needed

**Files created:**
- `newskills/creating-posts/SKILL.md` — Main skill (5-layer structure, generate + critique modes)
- `newskills/creating-posts/reference/platform-guides.md` — Per-platform voice, format, constraints, examples
- `newskills/creating-posts/templates/post-output-template.md` — Output format for variants and critique results

**Deployed to:** `~/.claude/skills/creating-posts/`

### Success Criteria
- [x] `/creating-posts` deployed and tested
- [x] Produces natural-sounding posts for at least 2 platforms
- [x] Critique mode successfully identifies and rewrites AI-sounding language
- [x] Auto-reads project context without requiring user to describe the project

---

## Phase 6: Vault BRDSPI — COMPLETE
**Effort:** High | **Duration:** 2 sessions | **Depends on:** Phase 2 (proven BRDSPI patterns)

**Implementation plan:** `.docs/plans/02-07-2026-phase-6-vault-brdspi-implementation.md`
**Research:** `.docs/research/02-07-2026-phase-6-vault-brdspi-pre-planning-research.md`

Applied the BRDSPI pattern (proven in code domain) to Obsidian vault management. Uses `verb-domain` naming convention. All 7 skills follow the proven 11-section BRDSPI structure. Skills use the best tool for each job -- MCP tools for vault search/metadata operations, file-system tools for direct note creation/editing.

### Skills (all deployed)

#### 6a. `/starting-vault` — DONE
- Parallel to `/starting-projects` but for vault setup
- Creates CLAUDE.md with vault path configuration, MCP server setup
- Defers MCP server choice to user during setup flow

**Deployed to:** `~/.claude/skills/starting-vault/`

#### 6b. `/researching-vault` — DONE
- Explore structure, tags, orphans, link graphs, conventions
- Uses MCP tools for vault content analysis

**Deployed to:** `~/.claude/skills/researching-vault/`

#### 6c. `/designing-vault` — DONE
- MOC strategy, tagging taxonomy, template designs
- Uses opus model (like `/designing-code`)

**Deployed to:** `~/.claude/skills/designing-vault/`

#### 6d. `/structuring-vault` — DONE
- Folder layout, naming conventions, note placement

**Deployed to:** `~/.claude/skills/structuring-vault/`

#### 6e. `/planning-vault` — DONE
- Ordered tasks with success criteria

**Deployed to:** `~/.claude/skills/planning-vault/`

#### 6f. `/implementing-vault` — DONE
- Create/move notes, update links, apply frontmatter
- Includes vault linting validation via MCP-based verification (verify link targets exist via read operations)

**Deployed to:** `~/.claude/skills/implementing-vault/`

#### 6g. `/importing-vault` — DONE
- Bridge: convert `.docs/research/` artifacts to Obsidian notes with frontmatter, wikilinks, tags, callouts, Dataview fields

**Deployed to:** `~/.claude/skills/importing-vault/`

### Success Criteria
- [x] Pre-work research complete (MCP keys, linting tools)
- [x] `/starting-vault` deployed — sets up vault context and MCP config
- [x] All 7 vault BRDSPI skills deployed (6 BRDSPI + `/starting-vault`)
- [x] `/importing-vault` converts `.docs/research/` to Obsidian note
- [x] Vault linting approach decided (MCP-based verification) and implemented in `/implementing-vault`

---

## Phase 7: Services BRDSPI — COMPLETE
**Effort:** High | **Duration:** 2-3 sessions | **Depends on:** Phase 2 (proven BRDSPI patterns)

**Implementation plan:** `.docs/plans/02-08-2026-phase-7-services-brdspi-skills.md`
**Research:** `.docs/research/02-08-2026-phase-7-services-brdspi-pre-planning-research.md`

Applied the BRDSPI pattern to homelab/infrastructure service management. Uses `verb-domain` naming convention. All 5 skills follow the proven 11-section BRDSPI structure. Entry point (`/brainstorming-services`) deployed in Phase 4.

### Skills (all deployed)

#### 7a. `/researching-services` — DONE
- Map services, ports, networks, volumes, dependencies, gaps
- Supports repo files for planned services + live docker state for deployed ones
- **Deployed to:** `~/.claude/skills/researching-services/`

#### 7b. `/designing-services` — DONE
- Stack decisions, networking strategy, auth approach, backup policy
- Uses opus model for architectural reasoning
- **Deployed to:** `~/.claude/skills/designing-services/`

#### 7c. `/structuring-services` — DONE
- Compose file organization, env templates, proxy routes, ordering
- Respects existing repo conventions
- **Deployed to:** `~/.claude/skills/structuring-services/`

#### 7d. `/planning-services` — DONE
- Phased tasks with success criteria
- Mode A (iterate existing plans) + Mode B (create from research)
- **Deployed to:** `~/.claude/skills/planning-services/`

#### 7e. `/implementing-services` — DONE
- Edit configs, generate deploy commands (user executes, never auto-run)
- Post-deploy verification checklists
- Optional same-machine read-only verification when configured
- **Deployed to:** `~/.claude/skills/implementing-services/`

### Configuration
- **Homelab plan repo location:** CLAUDE.md pointer (`homelab_repo_path`)
- This is for maintaining an existing homelab plan, not creating from scratch
- Optional same-machine execution: `homelab_same_machine: true` enables read-only docker commands for verification
- Future consideration: `/starting-homelab` for others who want to set up new homelabs

### Special Considerations
- Deployment is hands-off (generate commands/scripts, never execute) — IMPLEMENTED
- Secrets handling (reference `.env` files without reading/committing) — IMPLEMENTED
- Works on homelab plan repo files with convention deference — IMPLEMENTED
- Vault linting equivalent implemented as service health verification (ports, networks, volumes, routes, backups) — IMPLEMENTED

### Success Criteria
- [x] All 5 services skills deployed
- [x] Full BRDSPI chain completed and tested
- [x] `/researching-services` uses repo files for planned + live state for deployed
- [x] Generates safe, user-executable deploy commands
- [x] Secrets never exposed in output
- [x] Optional same-machine verification mode works correctly

---

## Quick Reference: Phase Dependencies

| Phase | Depends On | Can Parallel With | Status |
|-------|-----------|-------------------|--------|
| 1 Session 1 (1a, 1b, 1f, 1g) | Nothing | Phase 3 | DONE |
| 1 Session 2 (1c, 1d, 1e, 1h) | 1a | Phase 3 | DONE |
| 1 Session 3 (hooks: 1i, 1j) | 1a | Phase 3 | DONE |
| 2: BRDSPI Core | Phase 0 | Phase 3, Phase 5 | DONE |
| 3: /researching-repo | Nothing | Any phase | DONE |
| 4: Brainstorming | Phase 2 | Phase 5 | DONE |
| 5: /creating-posts | Phase 1b | Phase 2, Phase 4 | DONE |
| 6: Vault BRDSPI | Phase 2 + pre-work research | Phase 7 | DONE |
| 7: Services BRDSPI | Phase 2 | None (final phase) | DONE |

## Complexity Summary

| Phase | Work Items | Effort | Sessions | Status |
|-------|-----------|--------|----------|--------|
| 0: Triage | 6 reviews (decisions) | Low | 1 | DONE |
| 1: Foundations | 1 new skill, 1 reference, 2 renames, 1 rework, 3 updates, 2 hooks | Med | 3 | DONE |
| 2: BRDSPI Core | 3 new + 1 modified + 1 agent | High | 1 | DONE |
| 3: Research | 1 skill | Medium | 1 | DONE |
| 4: Brainstorming | 3 new + 1 retirement | Medium | 1 | DONE |
| 5: Content | 1 skill | Low-Med | 1 | DONE |
| 6: Vault | 7 skills + pre-work research | High | 2 | DONE |
| 7: Services | 5 skills + pre-work research | High | 2-3 | DONE |
| **Total** | **33 new + 7 modified/renamed + 2 hooks + 15 reference/template files** | | **~16-19 sessions** | **ALL COMPLETE** |

## Recommended Session Plan

```
Session 1:  Phase 1 Session 1 — /naming-session, voice/tone ref, renames     ✓ DONE
Session 2:  Phase 1 Session 2 — /bookmarking-code, /implementing-plans,      ✓ DONE
            /handing-over, /learning-from-sessions updates

Session 3:  Phase 1 Session 3 — track-errors + trigger-learning hooks        ✓ DONE
            + harvest-errors hook, /resuming-sessions skill, integration test

Session 4:  Phase 2 — BRDSPI Core (/designing-code, /structuring-code,     ✓ DONE
               modified /planning-code, /starting-refactors, docs-writer ext)

Session 5:  Phase 3 — /researching-repo (parallel, independent)             ✓ DONE
Session 6:  Phase 5 — /creating-posts (needs 1b only, quick win)           ✓ DONE

Session 7:  Phase 4 — Brainstorming skills + retire /discussing-features    ✓ DONE

Sessions 8-9:   Phase 6 — Vault BRDSPI (pre-work research + 7 skills)      ✓ DONE

Sessions 10-12: Phase 7 — Services BRDSPI (5 skills)                        ✓ DONE
```

**Critical path:** ~~Phase 1~~ (done) → ~~Phase 2~~ (done) → ~~Phase 4~~ (done) → ~~Phase 5~~ (done) → ~~Phase 6~~ (done) → ~~Phase 7~~ (done)

**Completion:** All 7 phases of the BRDSPI expansion roadmap are now complete. 33 new skills deployed plus 2 hooks plus infrastructure. The RPI workflow has been successfully expanded to full BRDSPI across three domains: code, vault, and services.

**Quick wins (completed):** ~~`/researching-repo` (Phase 3)~~ (done), ~~`/creating-posts` (Phase 5)~~ (done)

**Roadmap closure notes:**
- `docs-updater` trigger expansion: completed through Phase 7 with all BRDSPI skills
- `/validating-code` + `/reviewing-changes` rename: deferred (still useful as-is, no urgent need to consolidate)
- `/starting-homelab`: future enhancement opportunity beyond this roadmap — would create new homelab plans from scratch
- All BRDSPI domain patterns proven and documented; future domain extensions (e.g., documentation, testing) can follow established formulas

---

## Roadmap Closure Summary

### Delivered
- **33 new skills** across BRDSPI workflow phases (code domain: 5, vault domain: 7, services domain: 5, + brainstorming: 3, research/content: 10, supporting: 3)
- **7 complete BRDSPI chains** (one per domain: code, vault, services; plus 3 brainstorming entry points; plus research & content chains)
- **2 hooks** (track-errors, trigger-learning) + 1 companion hook (harvest-errors) + 1 companion skill (/resuming-sessions)
- **5 domain-specific modification** to existing skills (renames, session awareness, checkpoint enforcement, learning capture rework)
- **1 voice/tone reference** — reusable across social media and content creation
- **Iron Law + Gate Function structure** proven across code, vault, and services domains
- **Hands-off deployment pattern** for services infrastructure (generate commands, never execute auto)
- **Secrets handling best practices** consistently applied (name references, never values)

### Results
- The original RPI workflow (Research, Plan, Implement) has been **expanded to full BRDSPI** (Brainstorm, Research, Design, Structure, Plan, Implement)
- Work can now be planned with **explicit architectural reasoning phase** (Design + Structure)
- Work can be **pre-planned with preference exploration** (Brainstorm phase entry points)
- Infrastructure changes are **hands-off by default** with optional same-machine read-only verification
- Session continuity is **automated** with `/naming-session` and `/resuming-sessions`
- Learnings are **captured systematically** with deferred action model
- Post-session documentation is **automatic** with `/learning-from-sessions`
- Social media content can be **drafted and critiqued** with human voice verification

### Next Steps (Beyond This Roadmap)
1. **Commit Phase 7 implementation** — all skills built and deployed, ready for history
2. **Archive completed roadmap** — this document served its purpose
3. **Create next-phase planning document** if desired for future expansions (e.g., documentation BRDSPI, testing BRDSPI)

---
