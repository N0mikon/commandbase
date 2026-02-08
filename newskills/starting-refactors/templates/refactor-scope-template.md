# Refactor Scope Template

Template for `.docs/refactors/` documents produced by `/starting-refactors`. The docs-writer agent handles frontmatter — this template defines body sections.

---

## Body Sections

```markdown
# [Area] Refactor Scope

## Baseline

**Checkpoint:** [checkpoint name, e.g., pre-refactor-auth]
**SHA:** [git commit hash at checkpoint time]
**Date:** [checkpoint date]
**Session:** [session name if active, or "no session"]

## Goal

[What the refactor aims to achieve — 1-2 sentences]

## Trigger

[Why now — what motivated this refactor]

## Target Area

### Files in Scope

- `path/to/file.ext` — [current role, line count]
- `path/to/other.ext` — [current role, line count]

### Files Explicitly Out of Scope

- `path/to/excluded.ext` — [why excluded]

## Current State Audit

### Architecture

[Current patterns, module boundaries, dependency direction]
[How the target area is organized today]

### Test Coverage

[Existing tests that cover target area]
[Gaps: what's tested vs what's not]

### Dependencies

**Depends on (target area uses):**
- [dependency] — [how it's used]

**Depended on by (other code uses target area):**
- [dependent] — [what it uses from target]

## Risks

- [Risk 1] — **Mitigation:** [strategy]
- [Risk 2] — **Mitigation:** [strategy]

## CLAUDE.md Context

[Context pointer added to project CLAUDE.md, or "N/A — no project CLAUDE.md"]

## Next Steps

Run the BRDSPI chain for this refactor:
1. `/researching-code` — deep audit of target area patterns
2. `/designing-code` — target architecture decisions
3. `/structuring-code` — migration order (each step deployable)
4. `/planning-code` — atomic tasks with success criteria
5. `/implementing-plans` — execute with mandatory checkpoints

To verify no regressions at any point:
`/bookmarking-code verify "pre-refactor-<area>"`
```

## Section Guidelines

- **Baseline**: Always include checkpoint name, SHA, and date. This is the rollback reference.
- **Goal**: Keep to 1-2 sentences. If it takes more, the scope may be too broad.
- **Files in Scope**: List every file with its line count. Precision matters for downstream phases.
- **Files Out of Scope**: Explicit exclusions prevent scope creep.
- **Current State Audit**: Populated from agent results. Architecture, tests, dependencies.
- **Risks**: At least 2 risks with mitigations. If you can't think of risks, audit harder.
- **Next Steps**: Always point to the BRDSPI chain and the verify command.

## What Does NOT Belong

- Design decisions (that's for /designing-code)
- Implementation plans or task breakdowns (that's for /planning-code)
- Code changes or refactored code
- Performance benchmarks (collect those during research phase)
