---
name: researching-frameworks
description: "Use this skill when researching framework documentation and library APIs before building a new project or adding a major dependency. This includes fetching current docs via Context7 MCP, gathering version-specific patterns and breaking changes, building dependency compatibility matrices, recording architecture decisions as ADRs, and producing .docs/references/ artifacts for offline use. Activate when the user says 'research this framework', 'get current docs for', 'what are the latest patterns for', or before scaffolding a new project with /starting-projects."
---

# Researching Frameworks

You are tasked with gathering current, authoritative framework and library documentation before any code is written. This skill combines Context7 MCP (live framework docs) with web research (ecosystem patterns, gotchas) to produce structured reference artifacts in `.docs/references/`.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Solve the stale training data problem. Frameworks iterate fast - patterns from 6 months ago may be deprecated. Your job is to fetch what's current, verify it, and persist it so this project has a reliable documentation baseline.

## The Iron Law

```
NO RECOMMENDATION WITHOUT CURRENT DOCUMENTATION
```

Don't suggest patterns, configurations, or dependency versions based on training data alone. Fetch current docs first.

**No exceptions:**
- Don't skip Context7 because "I already know this framework well"
- Don't recommend a version without checking the latest release
- Don't describe an API without verifying it exists in the current version
- Don't produce reference docs without source URLs

## The Gate Function

```
BEFORE producing any framework reference artifacts:

Phase 1 — PLAN:    Detect Context7, classify deps by tier, present plan
Phase 2 — FETCH:   Research ONE TIER at a time:
                     launch subagents → collect → persist to disk → checkpoint → next tier
Phase 3 — ANALYZE: Read from disk, build compatibility matrix + ADRs, persist
Phase 4 — FINALIZE: Suggest MCP config, present summary

Each tier and phase persists to .docs/references/ BEFORE the next starts.
Each tier boundary AND phase boundary is a /compact or /handing-over point.
Phase 3+ reads from persisted files, never from conversation memory.

Skip persistence between tiers = research lost to context compaction
Launch all tiers in parallel = no checkpoint opportunities, no recovery
Skip subagent delegation in Phase 2 = context fills before Phase 3
```

## Initial Response

When this skill is invoked, determine the situation:

1. **If called with a specific framework/stack**: Begin research immediately
2. **If called by `/starting-projects`**: Receive the tech stack from discovery, begin research
3. **If no parameters**: Ask what frameworks to research

```
I'll research current documentation for your tech stack. First, let me check what documentation tools are available.
```

Then immediately check for Context7 MCP availability.

## Modes

### Mode A: Standalone Research

Use when the user directly invokes this skill with a framework or tech stack.

**Steps:**
1. Parse the requested frameworks/libraries from user input
2. Detect Context7 availability
3. Classify dependencies by tier
4. Execute research (see Process below)
5. Write `.docs/references/` artifacts
6. Present findings with recommendations

### Mode B: Called by /starting-projects

Use when `/starting-projects` delegates Phase 2 research to this skill.

**Steps:**
1. Receive tech stack from discovery phase (framework, language, key dependencies)
2. Detect Context7 availability
3. Classify all discovered dependencies by tier
4. Execute research (see Process below)
5. Write `.docs/references/` artifacts
6. Return findings to `/starting-projects` for plan creation

### Mode C: Adding a Dependency

Use when researching a single new framework/library to add to an existing project.

**Steps:**
1. Identify the new dependency and the existing stack
2. Detect Context7 availability
3. Research the new dependency at Tier 1 depth
4. Check compatibility with existing dependencies
5. Update `.docs/references/` with new dependency info
6. Present integration guidance

## Process: Four Phases

This skill runs in four phases. Each phase **persists its output to disk before the next phase starts**. This ensures research survives context compaction (`/compact`) and enables handover (`/handing-over`) between phases if context runs low.

**Phase boundary rule:** After each phase, present results and offer a checkpoint. If context is getting large, suggest `/compact` before continuing. If context is critically low, suggest `/handing-over` with the current phase noted.

---

### Phase 1: Plan (detect + classify)

Light on context. Produces the research plan.

1. **Detect Context7** — Use ToolSearch for "resolve-library-id". See ./reference/context7-usage.md for detection and fallback logic. **Record the actual tool names** (e.g., `mcp__MCP_DOCKER__resolve-library-id` and `mcp__MCP_DOCKER__get-library-docs`) — subagents need the exact names in their prompts.
2. **Classify dependencies** by tier. See ./reference/research-tiers.md for definitions.
   - **Tier 1** (always): Primary framework, language runtime — full depth
   - **Tier 2** (major): Testing, build tools, CSS framework — focused
   - **Tier 3** (on request): Database, auth, deployment — if user specifies
   - **Tier 4** (AI-specific): MCP servers, AI SDKs — if applicable

**Present and checkpoint:**
```
PHASE 1 COMPLETE — Research Plan
==================================
Context7: [available/unavailable]

Tier 1 (full depth): Next.js 15, React 19
Tier 2 (focused): Vitest, Tailwind CSS 4
Tier 3 (if needed): Prisma, NextAuth

Proceed to Phase 2 (fetching docs)?
```

---

### Phase 2: Fetch (the heavy phase)

This is where context fills up. **Delegate to subagents** and **persist each tier to disk before starting the next**.

**CRITICAL (Mode A/B only): Never call Context7 MCP directly in the main context during multi-dep research.** Each `get-library-docs` response is 10-14k tokens. Three direct calls fill the context window; ten will crash it. All Context7 calls MUST go through subagents. Mode C (single dependency) may call directly — see below.

Phase 2 is a loop: **research tier → collect results → persist to disk → checkpoint → next tier**. Do NOT launch all tiers in parallel — that defeats persistence checkpoints and removes the user's opportunity to `/compact` or `/handing-over` between tiers.

#### Per-tier loop

For each tier (1, then 2, then 3/4 if applicable):

**Step 1 — Launch subagents for this tier only:**
- Spawn parallel foreground `general-purpose` agents (one per library) with the Context7 tool names detected in Phase 1, token limits, and output format — see ./reference/context7-usage.md for the prompt template
- Spawn parallel `web-researcher` agents for ecosystem patterns and gotchas
- Wait for all agents in this tier to complete
- **general-purpose agents MUST run foreground** — MCP tools are unavailable in background mode

**Step 2 — Persist this tier's findings to disk immediately:**
- Write to `.docs/references/framework-docs-snapshot.md` via `docs-writer`
- First tier creates the file; subsequent tiers append their section
- Use the per-tier sections from ./templates/framework-research-template.md

**Step 3 — Checkpoint:**
```
TIER [N] COMPLETE — [Tier 1: Core Frameworks / Tier 2: Key Libraries / etc.]
==============================================================================
Researched: [list of deps in this tier]
Sources: [N] Context7 + [M] web
Persisted to: .docs/references/framework-docs-snapshot.md

[If more tiers remain:]
  Next: Tier [N+1] ([list of deps])
  This is a good point to /compact if context is getting large.
  Ready to continue?

[If all tiers done:]
  All tiers complete. Ready for Phase 3 (compatibility + ADRs)?
```

Wait for user confirmation before proceeding to the next tier. This gives the user a natural pause to `/compact`, `/handing-over`, or adjust the remaining research plan.

#### Why general-purpose instead of context7-researcher

Plugin subagents (like `context7-researcher`) cannot access MCP tools due to a Claude Code limitation — they don't inherit MCP server connections. `general-purpose` is a built-in agent type that does inherit MCP access. Each agent gets the exact tool names and output format in its prompt, keeping results structured.

#### Fallback when Context7 is unavailable

If `general-purpose` agents fail (MCP unavailable, rate limited):
- Do NOT fall back to direct MCP calls in the main context
- Fall back to `web-researcher` agents for those libraries
- The entire point of Phase 2 subagents is keeping large MCP responses out of the main context

#### Single-dependency exception (Mode C only)

For single-dependency lookups (Mode C), call Context7 directly — **always set the `tokens` parameter**. See ./reference/context7-usage.md for per-tier token budgets. Single-dep mode is the ONLY case where direct calls are acceptable.

**Token management:** Never call `get-library-docs` without setting `tokens`. Default is 10,000 tokens. For multi-dep stacks, always use the subagent strategy.

---

### Phase 3: Analyze (compatibility + decisions)

Read from persisted `.docs/references/` artifacts — **do not rely on conversation history** for the raw docs fetched in Phase 2.

1. **Build compatibility matrix** — Read the snapshot file, cross-reference version requirements:
   - Which versions are compatible with each other?
   - Known conflicts between dependencies?
   - Minimum version requirements?

2. **Draft ADRs** — For each significant technology choice:
   - What was chosen and why
   - What alternatives were considered
   - What trade-offs were accepted
   - See ./templates/architecture-decision-template.md for format

3. **Persist both:**
   - Write compatibility matrix to `.docs/references/dependency-compatibility.md` via `docs-writer`
   - Write ADRs to `.docs/references/architecture-decisions.md` directly (ADRs use their own format)

**Present ADRs for user confirmation before finalizing.**

**Checkpoint after Phase 3:**
```
PHASE 3 COMPLETE — Analysis Done
==================================
Persisted:
- .docs/references/dependency-compatibility.md
- .docs/references/architecture-decisions.md

Ready for Phase 4 (finalization)?
```

---

### Phase 4: Finalize (MCP config + summary)

Light phase. Suggest MCP configuration if relevant:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

Only suggest MCP servers directly relevant to the chosen stack.

Then present the final output (see Output Format below).

---

### Resuming After Compaction or Handover

If this skill is resumed after `/compact` or picked up from a `/handing-over`:

1. **Check what exists:** Read `.docs/references/` to determine which phases and tiers completed
2. **Resume from the next incomplete step:**
   - No snapshot file → resume at Phase 2, Tier 1
   - Snapshot exists with Tier 1 but not Tier 2 → resume at Phase 2, Tier 2
   - Snapshot exists with all tiers but no compatibility matrix → resume at Phase 3
   - All files exist but no summary presented → resume at Phase 4
3. **Read from disk, not memory:** Phase 3+ must read persisted artifacts, never rely on conversation history for fetched documentation
4. **Re-detect Context7:** After `/compact`, tool detection state is lost. Run ToolSearch for "resolve-library-id" again before spawning subagents

## Output Format

When complete, present:

```
FRAMEWORK RESEARCH COMPLETE
============================

Researched: [list of frameworks/libraries]
Sources: Context7 MCP + [N] web sources
Date: [YYYY-MM-DD]

Key Findings:
- [Most important finding per Tier 1 dependency]
- [Version compatibility summary]
- [Notable gotchas or breaking changes]

Files created:
- .docs/references/framework-docs-snapshot.md
- .docs/references/dependency-compatibility.md
- .docs/references/architecture-decisions.md

Suggested MCP config: [yes/no - .mcp.json]

Next steps:
- Review architecture decisions and confirm choices
- Run `/starting-projects` to create the project plan (if not already in progress)
- Or run `/planning-code` to plan implementation with these references
```

## Error Recovery

**Recoverable errors (fix and continue):**
- Context7 rate limited: Switch to web-only research for remaining queries
- Context7 library not found: Use web search for that specific library
- Web search returns stale results: Note staleness in output, flag for user review

**Blocking errors (stop and ask):**
- No research sources available (no Context7, no web search): Cannot proceed - ask user to configure at least one
- Framework doesn't exist or name is ambiguous: Ask user to clarify

**Prevention:**
- Always check Context7 availability before querying
- Use focused queries to stay within rate limits
- Note the date on all persisted documentation

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Recommending patterns without having fetched current docs
- Persisting documentation without source URLs
- Skipping the compatibility matrix for multi-dependency stacks
- Writing ADRs without presenting them for user confirmation
- Dumping entire library docs instead of focused topic queries
- Calling `get-library-docs` without setting the `tokens` parameter (default is 10k — context fills fast)
- Running ANY Context7 queries in the main context during multi-dep research (Mode A/B) — even 1 direct `get-library-docs` call returns 10-14k tokens. Use general-purpose subagents or web-researcher fallback, NEVER direct calls
- Proceeding without checking Context7 availability first
- Making changes beyond the research scope (writing code, modifying configs)
- Moving to the next tier or phase without persisting to disk first
- Launching all tiers in parallel instead of sequentially (removes checkpoint opportunities)
- Relying on conversation memory for raw docs instead of reading from `.docs/references/`
- Skipping the checkpoint message between tiers or phases

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know Next.js 15 well from training" | Training data has a cutoff. Fetch current docs. |
| "Context7 is slow, I'll skip it" | Stale patterns are slower to debug. Wait for the query. |
| "One web search is enough" | One angle isn't research. Cross-reference sources. |
| "The user just wants to start coding" | Starting with wrong patterns wastes more time. Research first. |
| "I'll write the docs later" | Docs written later are docs forgotten. Persist now. |
| "This stack is too simple to need ADRs" | Simple decisions still benefit from recorded rationale. |
| "I don't need the compatibility matrix" | Version conflicts are the #1 cause of setup failures. Check compatibility. |
| "I'll persist everything at the end" | Context may not survive to the end. Persist after each phase. |
| "I remember the docs from Phase 2" | After /compact, you won't. Read from disk in Phase 3+. |
| "I'll just call Context7 directly in multi-dep mode" | That's exactly how you fill 200k tokens in 10 calls. Use general-purpose subagents or web-researcher fallback. |
| "I'll launch all tiers at once for speed" | Speed means nothing if you can't persist or checkpoint. One dead tier kills recovery for all. Sequential tiers with disk writes between. |

## The Bottom Line

**No code without current documentation.**

Detect tools. Tier your research. Fetch current docs. Cross-reference. Persist everything. Every framework. Every project. Every time.
