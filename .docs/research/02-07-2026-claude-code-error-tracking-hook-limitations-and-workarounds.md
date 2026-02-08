---
date: 2026-02-07
status: complete
topic: "Claude Code Error Tracking Hook Limitations and Workarounds"
tags: [research, claude-code, hooks, error-tracking, PostToolUseFailure, workarounds]
git_commit: ae98216
---

# Claude Code Error Tracking Hook Limitations and Workarounds

## Research Question
Are there solutions or workarounds for tracking tool errors in the main Claude Code conversation, given that PostToolUseFailure only fires in subagent contexts?

## Summary
PostToolUseFailure is documented to fire "when a tool execution fails" but empirical testing shows it only fires in subagent contexts, not the main conversation. PostToolUse intentionally only fires for successful tool completions (confirmed by GitHub Issue #6371, closed NOT_PLANNED). No unified PostToolComplete event exists. The most viable workaround is using the **Stop/SessionEnd hook with transcript_path parsing** to extract errors post-session.

## Detailed Findings

### The Gap: No Hook Fires for Main Conversation Errors
**Sources:** [Issue #6371](https://github.com/anthropics/claude-code/issues/6371), [Hooks Reference](https://code.claude.com/docs/en/hooks)

- **PostToolUse**: Intentionally only fires for successful tool completions. Confirmed by Anthropic closing #6371 as NOT_PLANNED.
- **PostToolUseFailure**: Documented to fire on tool failures, but empirically only fires in subagent contexts. No official documentation of this scope limitation.
- **Result**: Main conversation tool failures have zero hook coverage.

### Workaround 1: Stop/SessionEnd Hook + Transcript Parsing (Most Viable)
**Sources:** [Hooks Reference](https://code.claude.com/docs/en/hooks)

Every hook event receives `transcript_path` (path to conversation JSONL). The Stop and SessionEnd hooks fire at session end and can parse the full transcript to extract tool failures retroactively.

Pros:
- Catches ALL errors regardless of context (main or subagent)
- Uses officially supported fields
- No performance impact during session (runs once at end)

Cons:
- Not real-time — errors are only logged at session end
- Requires JSONL parsing logic
- Transcript can be large

### Workaround 2: External Observability Tools
**Sources:** [claude_telemetry](https://github.com/TechNickAI/claude_telemetry), [Dev-Agent-Lens](https://arize.com/blog/claude-code-observability-and-tracing-introducing-dev-agent-lens/)

- **claude_telemetry**: Drop-in wrapper (`claudia` command) that logs tool calls, errors, token usage to Logfire/Sentry/Honeycomb/Datadog via OpenTelemetry.
- **Dev-Agent-Lens (Arize)**: OpenTelemetry-based observability emitting spans for tool calls including failures.

These work at the SDK level rather than the hook level, bypassing the hook gap entirely.

### Workaround 3: Force Success Exit Codes (Not Recommended)
**Source:** [Issue #6371](https://github.com/anthropics/claude-code/issues/6371)

Wrap Bash commands to always exit 0, then check output for errors in PostToolUse. This loses the failure signal to Claude and breaks normal error handling.

### Related Issues
- **Issue #6305** (OPEN): PreToolUse/PostToolUse hooks not executing at all for some users — broader hook reliability problem
- **Issue #10936**: Hook status label shows "Hook Error" for successful executions (cosmetic)
- **v2.1.33 (Feb 2026)**: Added TeammateIdle and TaskCompleted events but no error hook improvements

## Source Conflicts
- Agent 2 claimed PostToolUseFailure fires in both contexts and suggested using `parent_tool_use_id` to differentiate. Our empirical testing contradicts this — PostToolUseFailure does not fire in main conversation at all.
- The official docs make no distinction between main/subagent scope for PostToolUseFailure, suggesting this is either a bug or undocumented limitation.

## Currency Assessment
- Most recent source: February 2026 (Claude Code v2.1.33 changelog)
- Topic velocity: fast-moving (new hook events being added regularly)
- Confidence in currency: medium — the gap may be addressed in a future release but no indication it's planned

## Recommended Approach
For the commandbase project, the **Stop hook + transcript parsing** approach is the best fit:
1. Keep PostToolUseFailure for subagent errors (it works there)
2. Add a Stop/SessionEnd hook that parses `transcript_path` for tool failures
3. This provides complete error coverage with no performance impact during the session

## Open Questions
- Is PostToolUseFailure not firing in main context a bug or intentional? Worth filing an issue.
- Does `transcript_path` contain tool error details in a parseable format? Needs investigation of the JSONL schema.
- Would Anthropic accept a feature request for a unified PostToolComplete event?
