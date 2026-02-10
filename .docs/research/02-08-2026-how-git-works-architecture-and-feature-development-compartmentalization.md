---
date: 2026-02-08
status: complete
topic: "How Git Works: Architecture and Feature Development Compartmentalization"
tags: [research, git, branching, version-control, feature-isolation, workflows]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 8 commits - content still accurate; added note linking to session skills v2 implementation that adopted worktree patterns from this research"
---

# How Git Works: Architecture and Feature Development Compartmentalization

## Research Question
How does Git work, especially when it comes to compartmentalization of feature development?

## Summary
Git's architecture is built on a content-addressable filesystem using three core object types (blobs, trees, commits) that form a Directed Acyclic Graph (DAG). Branches are lightweight 41-byte pointers to commits, making creation instant and enabling Git's "killer feature" of effortless parallel development. The industry has largely shifted from complex branching models (Git Flow) toward trunk-based development with short-lived feature branches, supported by feature flags, merge queues, and CI/CD integration. Multiple isolation techniques exist beyond basic branching: worktrees for parallel checkouts, sparse checkout for monorepos, and submodules/subtrees for component boundaries.

## Detailed Findings

### 1. Git's Core Architecture

**Sources:** [Pro Git Book - Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects), [MIT Missing Semester](https://missing.csail.mit.edu/2020/version-control/)

Git is fundamentally a **content-addressable filesystem** with a version control interface built on top.

**Three core object types:**
- **Blobs**: Store raw file content (no filename/directory info), named by SHA-1 hash
- **Trees**: Represent directory structure, organize blobs and other trees (like UNIX directories)
- **Commits**: Reference a tree (complete project snapshot), parent commit(s), author/committer metadata, and message

Objects are stored compressed via zlib in `.git/objects/[first 2 chars]/[remaining 38 chars]`.

**The DAG (Directed Acyclic Graph):** History is structured as a DAG where each commit refers to parent snapshots. This enables multiple branches diverging from common ancestors, merge commits with multiple parents, and complete preservation of parallel development history. Commits are immutable -- "edits" create new commits and update references.

**Branches are just pointers:** A branch is a 41-byte text file (40-char SHA-1 + newline) in `.git/refs/heads/`. HEAD is a symbolic reference (`ref: refs/heads/master`) pointing to the current branch. When you commit, Git reads HEAD, finds the current branch ref, and updates it to the new commit SHA-1. This is why branching is instant and why Git encourages frequent branching.

### 2. Branching Strategies for Feature Compartmentalization

**Sources:** [LaunchDarkly](https://launchdarkly.com/blog/git-branching-strategies-vs-trunk-based-development/), [Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow), [Assembla](https://get.assembla.com/blog/trunk-based-development-vs-git-flow/)

**Git Flow** (legacy, declining): Multiple long-lived branches (main, develop, feature, release, hotfix). Clear separation of concerns but high maintenance burden. "Gitflow is a legacy Git workflow... fallen in popularity in favor of trunk-based workflows."

**GitHub Flow** (simple): One main branch + short-lived feature branches + PRs. Good for small-medium teams with continuous deployment. Cons: hard to scale for large teams, bad merges can leave main undeployable.

**GitLab Flow** (middle ground): GitHub Flow simplicity + environment branches (dev, staging, production). Good for teams needing deployment gates without Git Flow complexity.

**Trunk-Based Development** (modern consensus): All developers integrate to shared trunk daily. Short-lived feature branches (max 2 days). Feature flags for incomplete work. The industry question has shifted from "is TBD viable?" to "why aren't you doing TBD yet?"

**When Git Flow still makes sense:** Scheduled releases, multiple production versions, heavily regulated industries.

### 3. Feature Isolation Techniques

**Sources:** [AWS DevOps Guidance](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/dl.scm.2-keep-feature-branches-short-lived.html), [Martin Fowler](https://martinfowler.com/articles/branching-patterns.html), [Atlassian](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

**Short-lived feature branches:** Merge at least once per day. One developer per branch. Branches lasting longer than 2 days risk becoming problematic. Merge conflict probability exceeds 50% after 10 days and 90% after 30 days (Microsoft Research).

**Git worktrees:** Multiple working directories from a single repository, each linked to a different branch. Created with `git worktree add <path> <branch>`. Shared Git objects reduce resource consumption vs. multiple clones. Teams report completing work in hours that previously took days. *This pattern was adopted by the commandbase session skills v2 implementation (see `.docs/plans/02-08-2026-session-skills-upgrade-v2.md`), where each session creates a dedicated branch and worktree under a bare repo container.*

**Git stash:** Temporarily shelves uncommitted changes. Stack-based (most recent on top). Local only. Best for temporary context switches, not long-term storage.

**Interactive rebase:** Cleans history on private branches before merging. Options: pick, reword, edit, squash, fixup. Never rebase public/pushed branches.

**Cherry-pick:** Selectively applies specific commits to another branch. Best reserved for hotfixes or saving commits from abandoned branches. Prefer merge/rebase when possible.

**Merge vs. rebase:**
- Merge: preserves history as it happened (non-destructive), use for shared branches
- Rebase: rewrites history for clean linear narrative, use for private branches
- Hybrid approach recommended: rebase locally, merge for team integration

### 4. Component Isolation: Submodules vs. Subtrees

**Sources:** [Atlassian](https://www.atlassian.com/git/tutorials/git-subtree), [GitScripts](https://gitscripts.com/git-submodules-vs-subtrees)

| Aspect | Submodules | Subtrees |
|--------|-----------|----------|
| Storage | Links only (smaller repo) | Full code embedded (larger repo) |
| Isolation | Clear boundaries | More integrated |
| Workflow | Component-based | System-based |
| Push back | Easy to push to external repo | Harder to contribute back |

**Choose submodules** when isolating ownership and history is critical, working with independent subprojects. **Choose subtrees** when you want simplicity, single-repo history, and don't need to push changes back.

### 5. Monorepo Techniques

**Sources:** [GitHub Blog](https://github.blog/open-source/git/bring-your-monorepo-down-to-size-with-sparse-checkout/), [GitLab](https://about.gitlab.com/blog/speed-up-your-monorepo-workflow-in-git/)

**Sparse checkout:** Reduces working directory to a subset of the repo. Cone mode specifies directories to include. Performance improvement from O(N*M) to O(M+N) using hashsets.

**Partial clone:** `--filter=blob:none` skips downloading file contents until needed. Combined with sparse checkout for maximum performance.

**Monorepo tools:** Nx (comprehensive, intelligent dependency graph), Turborepo (fast, Rust-based, simpler), Lerna (versioning, bootstrapping). Turborepo is 3x faster than Nx, 16x faster than Lerna in benchmarks.

### 6. Collaboration Patterns and Guardrails

**Sources:** [GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [Aviator](https://www.aviator.co/blog/what-is-a-merge-queue/), [Graphite](https://graphite.com/guides/what-do-merge-queues-do)

**Protected branches:** Prevent direct pushes, enforce review processes. Key requirements: PR reviews, status checks (strict or loose), signed commits, linear history, code owner approvals.

**Merge queues:** Line up PRs for merging, create temporary branches combining latest target + queued PRs, run checks before auto-merging. Solve: outdated PRs, merge conflicts, incompatible changes, broken builds. GitHub uses them to merge tens of thousands of PRs daily.

**CI/CD integration:** Automated pipelines run on each PR. Required status checks must pass before merging. Job names should be unique across workflows to avoid blocking.

**Code review best practices:** Right-size PRs (split features into manageable chunks), assign knowledgeable reviewers, use CODEOWNERS for automatic suggestions, provide tactful feedback focused on code.

### 7. Avoiding Merge Hell

**Sources:** [STX Next](https://www.stxnext.com/blog/escape-merge-hell-why-i-prefer-trunk-based-development-over-feature-branching-and-gitflow), [Martin Fowler](https://martinfowler.com/articles/branching-patterns.html)

**The problem:** Long-lived branches create complicated merges, increased technical debt, bugs, and complex deployment processes. 100 developers with separate feature branches create exponential merge complexity.

**The solution:** "Frequency reduces difficulty" (Martin Fowler). High-performing teams integrate significantly more frequently. Key practices:
- Keep branches short-lived (max days, not weeks)
- Break large features into small, independently mergeable chunks
- Use feature flags to hide incomplete work in production
- Branch by abstraction for large-scale changes
- Merge at least daily
- Maintain three or fewer active branches

## Source Conflicts
- **Git Flow status:** Some enterprise-focused sources still recommend Git Flow for large teams, while DevOps-focused sources strongly advocate trunk-based development. The consensus is moving toward TBD but Git Flow remains valid for specific use cases (scheduled releases, multiple production versions).
- **Team size guidance:** Sources disagree on thresholds -- some say "smaller teams" for TBD without defining size. General pattern: under ~10 developers favors TBD, larger teams may benefit from more structure.
- **Monorepo tool performance:** Turborepo benchmarks vary by source, with some showing Lerna+Nx as fastest for very large repos.

## Currency Assessment
- Most recent source: January 24, 2026 (OneUpTime blog)
- Topic velocity: moderate (Git fundamentals are stable; workflows evolve with tooling)
- Confidence in currency: high -- core Git architecture is settled, workflow trends are well-documented

## Open Questions
- Specific adoption percentages for each branching strategy across the industry
- Concrete case studies of major companies transitioning from Git Flow to TBD
- Performance metrics comparing strategies (deployment frequency, failure rates)
- How AI-assisted coding tools are changing branching patterns (early evidence with worktrees + AI agents) -- *Partially answered: commandbase session skills v2 pairs each Claude Code agent session with a dedicated worktree, validating the worktree + AI agent pattern in practice*
- Security implications of submodule vs subtree approaches
