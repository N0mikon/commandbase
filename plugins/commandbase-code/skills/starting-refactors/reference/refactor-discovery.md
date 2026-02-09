# Refactor Discovery Reference

Discovery question templates for different refactor types. Use these to guide the initial conversation and tailor audit agent prompts.

## Performance Refactors

**Trigger signals:** "too slow", "bottleneck", "optimize", "latency"

**Discovery questions:**
- What's slow? (specific operation, page load, API response, build time)
- How do you know? (profiling data, user complaints, monitoring alerts)
- What's the target? (specific metric, or "noticeably faster")

**Audit agent focus:**
- Hot paths and frequently-called functions
- Database queries and I/O operations
- Memory allocation patterns
- Caching opportunities

## Modularity Refactors

**Trigger signals:** "too coupled", "can't test independently", "need to split", "circular dependency"

**Discovery questions:**
- What's coupled that shouldn't be? (specific modules, files, or concepts)
- What should be independently deployable/testable?
- Are there circular dependencies to break?

**Audit agent focus:**
- Import/dependency graphs
- Shared mutable state
- Cross-module function calls
- Interface boundaries (or lack thereof)

## Migration Refactors

**Trigger signals:** "upgrade to", "move from X to Y", "deprecation", "new version"

**Discovery questions:**
- What's the source and target? (framework version, language, pattern)
- Is incremental migration possible, or does it need to be all-at-once?
- What's the bridge strategy? (adapter pattern, feature flags, parallel runs)

**Audit agent focus:**
- All usage sites of the thing being migrated
- Breaking changes between source and target
- Test coverage of migration-affected areas
- Third-party dependencies that may also need updating

## Cleanup Refactors

**Trigger signals:** "tech debt", "messy code", "hard to understand", "inconsistent patterns"

**Discovery questions:**
- What's the worst area? (specific files or patterns)
- What conventions should the cleaned-up code follow?
- Is there a deadline or priority driver?

**Audit agent focus:**
- Code duplication
- Inconsistent naming or patterns
- Dead code and unused exports
- Missing or outdated tests

## Scaling Refactors

**Trigger signals:** "won't scale", "too many users", "data growing", "concurrency issues"

**Discovery questions:**
- What's the growth pattern? (users, data volume, request rate)
- What breaks first? (database, memory, CPU, network)
- What's the target scale? (10x, 100x, "handle production")

**Audit agent focus:**
- Single points of failure
- In-memory data structures that grow unbounded
- Sequential operations that could be parallelized
- Database queries without proper indexing
