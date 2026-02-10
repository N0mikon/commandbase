---
date: 2026-02-08
status: complete
topic: "Trunk-Based Development: Deep Dive"
tags: [research, git, trunk-based-development, branching, CI-CD, feature-flags, DORA]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Refreshed after 8 commits - no content changes needed, standalone research with no code references"
references: []
---

# Trunk-Based Development: Deep Dive

## Research Question
What is trunk-based development, how does it work in practice, what enables it, how does it scale, and what are its limitations?

## Summary
Trunk-based development (TBD) is a branching model where all developers commit to a single main branch ("trunk") at least once daily, using only short-lived feature branches (max 1-2 days). DORA research links TBD to elite software delivery performance — teams practicing it deploy nearly 1000x more frequently than low performers. TBD is enabled by feature flags, branch by abstraction, comprehensive automated testing, fast CI/CD pipelines, and synchronous code review. Google (35,000 developers), Microsoft (200+ PRs/day), Netflix, and Spotify all practice TBD at scale, though each requires substantial infrastructure investment. However, TBD is not universal — it requires mature testing, experienced developers, fast builds, and cultural buy-in. It redistributes complexity rather than eliminating it, and feature flag mismanagement can create catastrophic risk (Knight Capital lost $460M in 45 minutes from a stale flag).

## Detailed Findings

### 1. Core Principles and Rules

**Sources:** [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/), [DORA](https://dora.dev/capabilities/trunk-based-development/), [Atlassian](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)

TBD is "a source-control branching model where developers collaborate on code in a single main branch, avoiding long-lived development branches." The name comes from tree anatomy — "the fattest and longest span is the trunk, not the branches."

**The three DORA rules** (from 2016-2017 research):
1. Have **three or fewer active branches** in the code repository
2. **Merge branches to trunk at least once a day**
3. **Don't have code freezes** and don't have integration phases

**Core philosophy:** "Never break the build, and always be release ready." As Frank Compagner of Guerrilla Games states: "Branches create distance between developers and we do not want that."

**What TBD is NOT:**
- Just having a branch called "trunk"
- Multiple developers working on the same feature branch
- Feature branches lasting more than 2 days
- Fixing bugs on release branches and merging down (fix on trunk first, cherry-pick to release)

### 2. Enabling Techniques

**Sources:** [trunkbaseddevelopment.com/feature-flags](https://trunkbaseddevelopment.com/feature-flags/), [Martin Fowler](https://martinfowler.com/articles/feature-toggles.html), [Harness](https://developer.harness.io/docs/feature-flags/get-started/trunk-based-development/)

#### Feature Flags
The foundation of TBD — allow incomplete code to exist in trunk without affecting production. Implementation approaches range from command-line arguments to runtime-switchable flags using distributed stores (Consul, Etcd).

**Critical risk:** Feature flag tech debt. Abandoned flags accumulate. Knight Capital lost $460M in 45 minutes because a deprecated flag from 2003 was repurposed in 2012 — old code sat dormant for 8 years, one server didn't get updated, and the stale code triggered an infinite trading loop.

**Best practices:** Establish "review for delete" dates, conduct monthly/quarterly flag reviews, implement CI "time bombs" that fail builds when obsolete flags persist, classify flags (release, experiment, ops, permission) with different lifecycles.

#### Branch by Abstraction
Martin Fowler's technique for large-scale refactors within TBD. Five steps: (1) create abstraction layer, (2) build new implementation behind it, (3) activate new code, (4) remove old code, (5) remove abstraction. ThoughtWorks migrated Go CI-daemon from iBatis to Hibernate this way.

Key advantage: migrations can **pause and resume** without restart penalties, unlike feature branches that rot.

#### Dark Launching
Run new back-end code in production without users seeing results. Monitor load and performance impact safely. Martin Fowler: works best for features that "enhance existing user interactions and isn't something users choose to do."

#### Canary Releases / Progressive Delivery
Deploy to a small subset (5-10%) first, monitor, then gradually increase. Feature flags decouple code deployment from feature release — "a game-changer in continuous delivery."

### 3. CI/CD Requirements

**Sources:** [trunkbaseddevelopment.com/continuous-integration](https://trunkbaseddevelopment.com/continuous-integration/), [DORA](https://dora.dev/capabilities/trunk-based-development/), [Aviator](https://www.aviator.co/blog/trunk-based-development/)

TBD is "a required practice for continuous integration" (DORA). CI is defined as "the combination of practicing trunk-based development and maintaining a suite of fast automated tests that run after each commit."

**Pipeline targets:**
- CI pipelines should complete within **10-15 minutes**
- Build times exceeding **30 minutes** significantly reduce developer throughput
- VCS operations: **under 3 seconds** when current, **max 15 seconds** when behind trunk
- ~60,000 tests in under 5 minutes (Microsoft's approach)

**Testing layers:**
- Short-running unit and integration tests: during development and upon merge
- Longer full-stack, end-to-end tests: in later pipeline phases
- Tests must be **reliable (not flaky)** — flaky tests trigger false CI alerts and erode trust

**Prevention over rollback:** Highest-performing teams verify commits before merging to trunk, preventing breakages rather than fixing them afterward.

### 4. Code Review in TBD

**Sources:** [trunkbaseddevelopment.com/continuous-review](https://trunkbaseddevelopment.com/continuous-review/), [DORA](https://dora.dev/capabilities/trunk-based-development/)

Code review speed is critical. "A few minutes for the review is best, and tens of minutes acceptable. More than an hour or two, and you are negatively affecting cycle times."

**Synchronous vs. async:** DORA recommends synchronous review — "when the developer is ready to commit, they should ask somebody else to review right then." If async reviews take a day or more, "you're no longer practicing trunk-based development — you're practicing delayed integration."

**Pair programming** can serve as review: "one pair of eyes counts toward code approval." Guido van Rossum characterized code review as "basically asynchronous pair-programming."

**PostHog's real metrics:** 4,344 PRs merged in 2023, median PR age of 8 hours, ~20 PRs merged per day.

### 5. TBD at Scale: Case Studies

**Sources:** [QE Unit](https://qeunit.com/blog/how-google-does-monorepo/), [Microsoft Learn](https://learn.microsoft.com/en-us/devops/develop/how-microsoft-develops-devops), [Spotify Engineering](https://engineering.atspotify.com/2025/4/how-we-release-the-spotify-app-part-1)

#### Google
- **35,000 developers** in a single monorepo trunk
- **2 billion lines of code**, 86 TB storage
- **40,000 commits daily** from 10,000+ engineers
- Custom tooling: Piper (distributed storage), CitC (cloud workspaces), Tricorder (presubmit validation), Critique (code review)
- Validation pipeline auto-withdraws risky commits

#### Microsoft
- Several **hundred developers** in single repo
- **200+ PRs/day**, 300+ CI builds/day, 500+ test runs/24hrs
- **60,000 tests in under 5 minutes** during PR review
- Three-week sprint cycles, ring-based deployment

#### Spotify
- Trunk-based: developers merge as soon as code is tested and reviewed
- Exception: large infrastructure changes merge early in cycle (Friday of Week 1) for extended testing

#### Netflix
- Trunk-based with frequent merges for stability
- Static code analysis and comprehensive testing

**The Google caveat:** "While Google is a proponent of TBD, what people forget is that Google has a system they developed that runs complete integration tests on every commit. Not everyone has that."

### 6. Team Size Considerations

**Sources:** [d4b.dev](https://www.d4b.dev/blog/2025-12-23-trunk-based-development), [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/), [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-trunk-strategy.html)

| Team Size | TBD Fit | Notes |
|-----------|---------|-------|
| 2-10 devs | Ideal | Minimal coordination overhead |
| 10-50 devs | Good with tooling | Need solid CI/CD, feature flags |
| 50-100 devs | Requires investment | Need merge queues, modular architecture |
| 100+ devs | Possible but demanding | Exceptional tooling, clear ownership boundaries, often hybrid approaches |

"The larger a team is, the shorter branches should be." High-commit-frequency environments may hit serialization bottlenecks requiring merge bots.

Most enterprises use **hybrid approaches**: trunk-based daily work with short-lived release branches.

### 7. Challenges and Criticisms

**Sources:** [Ben Morris](https://www.ben-morris.com/why-trunk-based-development-isnt-for-everybody/), [Tim Abell](https://0x5.uk/2024/04/18/trunk-based-development-is-wrong/), [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-trunk-strategy.html)

**TBD redistributes complexity, doesn't eliminate it.** Complexity moves "downstream to code design and application configuration."

**Key criticisms:**
- **Loss of grouping:** Mainlining eliminates organizing related commits into coherent feature groups (Tim Abell)
- **No pre-merge verification:** Without feature branches, you lose the ability to CI-check changes before they hit trunk
- **Irreversible history:** Bad approaches are permanently in history vs. throwaway branches
- **Legacy systems:** "A legacy monolith with poorly defined layers or thousands of stored procedures isn't always amenable to new abstraction layers"
- **Build speed:** "If you have a large, monolithic architecture or a complex suite of tests then your build may not be quick enough"

**The senior developer requirement:**
- "Only experienced developers on your team" (Perforce)
- Developers with "16+ years of experience take full benefit" (DORA/Toptal)
- "Junior developers could merge in immature code that could destabilize your entire project"

**Cultural resistance:** TBD is "a challenge to the mythos of the developer-as-hero." Teams accustomed to feature branches feel fear and stress from the "build must always work" pressure.

### 8. When TBD Is NOT the Right Choice

**Sources:** [Splunk](https://www.splunk.com/en_us/blog/learn/trunk-based-development-vs-gitflow.html), [Appsilon](https://www.appsilon.com/post/comparison-of-gitflow-and-trunk-based-development), [CircleCI](https://circleci.com/blog/trunk-vs-feature-based-dev/)

Git Flow or feature branching is better when:
- **Regulated industries** requiring audit trails and controlled release processes (pharma, finance, government)
- **Scheduled releases** with features that must ship together
- **Multiple production versions** maintained simultaneously
- **Large, fragmented teams** with less experienced developers
- **Test coverage is weak** or CI/CD is unreliable
- **Codebase lacks modularity** and is a tightly-coupled monolith

**Hybrid approach:** "Many modern orgs use Trunk-Based for internal services, Git Flow for client-facing or regulated products."

### 9. Migration Path: Git Flow to TBD

**Sources:** [Aviator](https://www.aviator.co/blog/how-to-transition-from-gitflow-to-trunk-based-development/), [Unleash](https://www.getunleash.io/blog/how-to-implement-trunk-based-development-a-practical-guide)

**Prerequisites before starting:**
1. Version control proficiency
2. Automated CI/CD pipeline
3. Comprehensive automated test suite
4. Feature flag tooling
5. Team buy-in and alignment

**Implementation steps:**
1. Consolidate to one branch
2. Commit frequently in small increments
3. Establish fast peer review process
4. Automate testing, builds, deployments
5. Monitor and optimize (build times, test coverage, deployment frequency)

**Common blockers:** "Without reliable CI, automated testing, and guardrails, trunk can get messy."

### 10. The Knight Capital Warning

**Sources:** [Statsig](https://blog.statsig.com/how-to-lose-half-a-billion-dollars-with-bad-feature-flags-ccebb26adeec), [Flagsmith](https://flagsmith.medium.com/when-feature-flags-go-wrong-e929144d589a)

The most dramatic feature flag failure in history:
- August 1, 2012: Knight Capital lost **$460 million in 45 minutes**
- A deprecated "Power Peg" flag from 2003 was repurposed for a new feature
- Old code sat dormant for **8 years** but was never deleted
- One of eight servers didn't receive the deployment (silent script failure)
- That server's stale code triggered an infinite trading loop: **4 million executions in 154 stocks**
- Lessons: Never reuse flags. Flags should have short lifespans. Delete dead code.

## Source Conflicts

- **Universal applicability:** DORA research strongly advocates TBD for all teams, while practitioners like Ben Morris and Tim Abell argue it's context-dependent and not universally superior
- **Junior developers:** DORA data suggests 16+ years experience correlates with TBD success, but some sources argue good tooling and process can compensate for experience gaps
- **Feature branches vs. no branches:** The official TBD site allows short-lived feature branches (1-2 days), while purists argue for direct trunk commits only. In practice, most teams use short-lived branches with PRs
- **AI impact:** DORA 2024 found AI tends to increase batch size, which works against TBD principles — a tension the industry hasn't resolved

## Currency Assessment
- Most recent source: December 23, 2025 (d4b.dev analysis)
- Topic velocity: moderate-high (core principles stable, tooling and practices evolving)
- Confidence in currency: high — DORA 2024 report provides recent data, multiple 2025 sources confirm trends

## Open Questions
- What percentage of teams attempting TBD adoption succeed vs. abandon it?
- How does AI-assisted coding (larger batch sizes) interact with TBD's small-commit philosophy?
- Specific infrastructure cost comparisons for TBD at different team sizes
- Detailed migration timelines from Git Flow to TBD at various organizational sizes
- How do regulated industries (finance, healthcare) adapt TBD for compliance requirements?
- Does TBD work for open-source projects with distributed, occasional contributors?
