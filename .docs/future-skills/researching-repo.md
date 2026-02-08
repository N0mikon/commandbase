---
status: implemented
implemented_in: newskills/researching-repo/
implemented_date: 2026-02-07
---

# Repository Analysis (`/researching-repo`)

## Problem

There's a gap between knowing what a project claims to do (web research, docs) and understanding how it actually works (reading code). `/researching-web` gives blog posts and discussions. `/researching-frameworks` gives API surfaces. `/researching-code` only works on the current project. None of them let you deeply analyze someone else's implementation.

## Concept

Clone a third-party repo and produce a thorough structural analysis, then persist findings as a `.docs/research/` artifact that survives the clone being deleted.

```
/researching-repo humanlayer/riptide-rpi
  -> shallow clone to temp location
  -> analyze structure, patterns, conventions
  -> produce .docs/research/ artifact
  -> cleanup clone (or keep if requested)
```

## What It Analyzes

- **Project structure** — directory layout, module organization, entry points
- **Architecture patterns** — how components connect, dependency flow, abstraction layers
- **Conventions** — naming, file organization, config patterns, test structure
- **Key implementations** — how the interesting parts actually work, not just what they expose
- **Scoped analysis** — user can target specific directories ("just look at `src/skills/`")

## Use Cases

- **Steal patterns** — "how does this well-architected project structure their tests?"
- **Evaluate libraries** — understand internals before adopting, not just API surface
- **Compare alternatives** — clone two competing projects, analyze both, produce comparison
- **Pre-contribution** — deep structural analysis before your first PR to an open source project
- **Reference implementations** — "how does HumanLayer actually implement RPI in their skills?"

## How It Fits the Research Stack

| Skill | Answers | Source |
|---|---|---|
| `/researching-web` | What do people say about it? | Blog posts, docs, discussions |
| `/researching-frameworks` | What's the API surface? | Official docs via Context7 |
| `/researching-code` | How does our code work? | Current project |
| `/researching-repo` | How does their code work? | Cloned source |

During RDSPI Research phase, all four can run together:
- `/researching-web` for landscape and community consensus
- `/researching-frameworks` for API docs of dependencies
- `/researching-repo` on a reference implementation to steal patterns
- `/researching-code` on the current project's existing state

## Mechanics

- **Shallow clone** — `git clone --depth 1`, no full history needed for analysis
- **Temp location** — clone into scratch dir, not the working project
- **Scoped analysis** — user specifies directories of interest to avoid noise
- **Artifact output** — `.docs/research/` file with findings, survives clone deletion
- **Cleanup** — default to deleting clone after analysis, flag to keep for reference

## Open Questions

- Where to clone? System temp dir, a `.scratch/` dir, or user-configured location?
- Should it support non-GitHub repos (GitLab, Bitbucket, local paths)?
- How to handle large repos — sparse checkout for targeted analysis?
- Should it detect and summarize the repo's own CLAUDE.md / AGENTS.md if present?
- Could it produce a reusable "patterns" artifact that `/designing-code` or `/structuring-code` can reference?

## Implementation Status

**Implemented on 2026-02-07** in `newskills/researching-repo/` and deployed to `~/.claude/skills/researching-repo/`.

All concepts from this document were realized in the implementation:
- Clone strategy evolved from shallow clone to blobless clone (`--filter=blob:none --no-checkout`) for remote repos, with selective checkout via `git show HEAD:path` -- more efficient than the original concept
- Temp directory uses system temp via `mktemp -d` (resolving the "where to clone?" question)
- Non-GitHub repos fully supported: git URLs, local paths, and GitHub shorthand expansion
- Large repos handled via blobless clone with on-demand blob fetching
- CLAUDE.md/AGENTS.md detection explicitly included in the analysis workflow
- Research artifact written via docs-writer agent delegation
- Security hardening added beyond original concept: `core.symlinks=false`, `core.hooksPath=/dev/null`, `--no-recurse-submodules`, post-clone hooks verification

Implementation files:
- `newskills/researching-repo/SKILL.md` -- Full skill definition with 7-step process
- `newskills/researching-repo/reference/clone-management.md` -- Clone security and strategy patterns
- `newskills/researching-repo/reference/analysis-strategies.md` -- Agent decomposition patterns
- `newskills/researching-repo/templates/repo-research-template.md` -- Output template for research artifacts
