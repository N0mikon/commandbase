# Re-evaluate Existing Skills

## Skills to Review

These skills may have drifted from their original intent. Need to revisit whether they're doing what was actually wanted and whether they need to be reworked or replaced.

### `/updating-skills`

- What was the original intent?
- What does it actually do now?
- Is it pulling its weight or just running validation checks that don't catch real issues?
- Does it overlap with manual editing + `/committing-changes`?

### `/updating-agents`

- What was the original intent?
- What does it actually do now?
- Same questions as `/updating-skills` — is this useful maintenance or busywork?
- Does agent updating need a dedicated skill or is it just editing files?

### `/bookmarking-code`

- Should checkpoints be created automatically as part of `/committing-changes` instead of requiring a separate manual invocation?
- Or should `/committing-changes` call `/bookmarking-code` internally before committing?
- Is anyone actually remembering to run `/checkpoint create` before risky changes, or is it only used after something breaks?
- What's the right trigger — every commit, only before phases, only when explicitly asked?
- How would this integrate with `/naming-session`? Checkpoints named by session ("auth-phase-pre-commit-3") would be far more findable than timestamps alone

### `/learning-from-sessions`

- What was the original intent?
- What does it actually do now?
- Is it actually producing reusable knowledge, or generating docs that never get referenced?
- Does the output format work? Are the learned patterns actually being applied in future sessions?
- Could this tie into `/naming-session` and `/handing-over` for better knowledge capture?

### `docs-updater` agent

- Currently only triggered by `/committing-changes` when docs are behind HEAD
- Should it be called more broadly? Candidates:
  - `/implementing-plans` — plans go stale as implementation diverges from the original spec
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
