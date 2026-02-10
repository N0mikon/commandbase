---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added missing git_commit and last_updated frontmatter to existing archive entry"
archived: 2026-02-07
archive_reason: "Triage/decision document whose decisions have all been captured in the implementation roadmap (Phase 0 Decisions) and executed through Phase 1 (Foundations) and Phase 2 (BRDSPI Core). Remaining open items tracked in roadmap Phases 4, 6/7, and incremental additions."
original_location: ".docs/future-skills/re-evaluate-existing.md"
---

# Re-evaluate Existing Skills

Status notes updated 2026-02-07 after Phase 1 Foundations implementation (Phases 1-8 of 10 complete).

## Skills to Review

These skills may have drifted from their original intent. Need to revisit whether they're doing what was actually wanted and whether they need to be reworked or replaced.

### `/auditing-skills`

Renamed from `/updating-skills` in Phase 3 of Phase 1 Foundations plan. Now has full audit checklist (5 categories), diff-first update workflow, and enforcement pattern sections.

- What was the original intent?
- What does it actually do now?
- Is it pulling its weight or just running validation checks that don't catch real issues?
- Does it overlap with manual editing + `/committing-changes`?

### `/auditing-agents`

Renamed from `/updating-agents` in Phase 4 of Phase 1 Foundations plan. Now has 6-category audit checklist (adds tool set, model/permission, and system prompt compliance checks), sibling cross-reference to `/auditing-skills`, and explicit scope restriction ("only fix what the audit found").

- What was the original intent?
- What does it actually do now?
- Same questions as `/auditing-skills` — is this useful maintenance or busywork?
- Does agent auditing need a dedicated skill or is it just editing files?

### `/bookmarking-code`

**Partially addressed by Phase 1 Foundations (Phases 5 and 7):**
- ~~How would this integrate with `/naming-session`?~~ **Done.** Phase 5 added session awareness -- checkpoints write to `.claude/sessions/{name}/checkpoints.log` when a session is active, with session-prefixed display names (e.g., `auth-mvp:phase-2-done`).
- ~~Should checkpoints be mandatory in `/implementing-plans`?~~ **Done.** Phase 7 made checkpoint creation a required step after each verified phase, not a suggestion.

**Still open:**
- Should checkpoints be created automatically as part of `/committing-changes` instead of requiring a separate manual invocation?
- Or should `/committing-changes` call `/bookmarking-code` internally before committing?
- Is anyone actually remembering to run `/checkpoint create` before risky changes, or is it only used after something breaks?
- What's the right trigger beyond `/implementing-plans` -- every commit, only before phases, only when explicitly asked?

### `/learning-from-sessions`

- What was the original intent?
- What does it actually do now?
- Is it actually producing reusable knowledge, or generating docs that never get referenced?
- Does the output format work? Are the learned patterns actually being applied in future sessions?
- ~~Could this tie into `/naming-session` and `/handing-over` for better knowledge capture?~~ **Done** -- Phase 8 reworked to deferred-action model outputting to `.docs/learnings/`, session-aware when active, reads session `errors.log`

### `docs-updater` agent

- Currently only triggered by `/committing-changes` when docs are behind HEAD
- Should it be called more broadly? Candidates:
  - ~~`/implementing-plans` — plans go stale as implementation diverges from the original spec~~ **Done** -- Phase 7 added docs-updater integration for staleness checks at start and end of implementation
  - `/handing-over` — handoff docs reference files that may have changed since last handover
  - `/structuring-code` (future) — structural changes invalidate existing research and plan docs
  - `/starting-refactors` (future) — refactor init should check if existing docs about the target area are current
- Is the current trigger (docs behind HEAD) the right heuristic, or should it also detect content staleness?
- Should skills that produce `.docs/` artifacts register them for future staleness checks?

### `/validating-code` vs `/reviewing-changes`

- These sound like they overlap — both look at code and check if it's good
- Are their purposes actually distinct in practice, or do they blur?
- Intended distinction seems to be:
  - `/validating-code` — checks implementation against a plan's success criteria (did we build what we said we'd build?)
  - `/reviewing-changes` — checks code quality before committing (debug statements, split commits, docs in sync)
- But does anyone invoke both? Or does one make the other redundant?
- Could `/validating-code` be a mode of `/reviewing-changes` or vice versa?
- In RDSPI, `/validating-code` maps to post-Implement verification. `/reviewing-changes` maps to pre-commit hygiene. Are those different enough to justify two skills?

## Action

Review each skill's SKILL.md, try invoking them, and compare actual behavior to original intent. Decide per skill: keep as-is, rework, or retire.
