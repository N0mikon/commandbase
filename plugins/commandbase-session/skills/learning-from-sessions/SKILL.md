---
name: learning-from-sessions
description: "Use this skill to extract reusable knowledge from work sessions. This includes reviewing what was learned during debugging, capturing session learnings to .docs/learnings/ for deferred action, running /learn to capture session learnings, responding to 'what did we learn' or 'capture learnings', and extracting knowledge after trial-and-error investigation that produced a solution."
---

# Learning from Sessions

You are extracting reusable knowledge from work sessions and capturing it to `.docs/learnings/` for deferred action. This skill activates when a session produces non-obvious discoveries, debugging breakthroughs, workarounds, or configuration insights worth preserving. Rather than immediately creating skills or CLAUDE.md entries, learnings are documented with a Deferred Actions checklist for a future session to act on.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO LEARNINGS DOCUMENT WITHOUT VERIFIED DISCOVERIES AND USER APPROVAL
```

Never document a learning that wasn't verified during the session. Never save without explicit user confirmation. Unverified knowledge is worse than no knowledge -- it misleads future sessions.

**No exceptions:**
- Don't document "should work" solutions that weren't tested
- Don't save without showing the user the draft first
- Don't document every fix -- most aren't worth capturing
- Don't skip the dedup check because "this is definitely new"

## The Gate Function

```
BEFORE capturing learnings:

1. SESSION: Detect repo layout, find session for current worktree via session-map.json. Fall back to _current. If post-session: read claudeSessionIds from meta.json.
2. DETECT: Recognize that extractable knowledge exists (trigger conditions or user request)
3. ERRORS: Read session errors.log if available (pull error context)
4. DEBUG: Scan .docs/debug/ for recent debug files from this session
5. DEDUP: Search existing .docs/learnings/ and skills before creating
6. ANALYZE: Run 4 identification questions + worth assessment
7. DRAFT: Structure using the learnings output format
8. VALIDATE: Run quality gates checklist
9. CONFIRM: Present to user for approval
10. ONLY THEN: Write to .docs/learnings/ via docs-writer

Skip any step = risk saving bad knowledge
```

## Session Awareness

Before capturing learnings, detect the active session:

1. Detect repo layout:
   ```bash
   git_common=$(git rev-parse --git-common-dir 2>/dev/null)
   git_dir=$(git rev-parse --git-dir 2>/dev/null)
   ```
2. If bare-worktree layout (paths differ): read container-level `session-map.json`, find entry whose `worktree` matches current cwd. Read session name.
3. If session-map entry has `claudeSessionIds` array: note these for transcript access.
4. If session status is `"ended"` and a session name argument was provided: use Post-Session Mode (see below).
5. Fallback: check `.claude/sessions/_current` for legacy sessions.
6. If no session found: Use current date instead of session name (default behavior).

When session-scoped:
- Read `.claude/sessions/{name}/errors.log` if it exists — incorporate error context into learnings
- Title format: `Session Learnings: {session-name}`
- Tags include the session name

When no session:
- Skip error log reading
- Title format: `Session Learnings: {YYYY-MM-DD}`
- Everything else works identically

**Timing note:** errors.log is populated by two hooks:
- `track-errors` (PostToolUseFailure) — real-time, subagent errors only
- `harvest-errors` (Stop) — end-of-session, catches ALL errors from transcript

Mid-session invocations only see real-time subagent errors. For complete
error coverage, run at the start of the next session after harvest has run.

## Debug File Integration

Before drafting learnings, scan `.docs/debug/` for recent debug files:

1. Check if `.docs/debug/` exists and has files from the current session timeframe
2. If YES: Reference the debug file in learnings (don't duplicate its content)
3. Extract the key learning from the debug file — the root cause and resolution

## When to Activate

### Automatic Recognition

Watch for these signals during sessions:

- **Non-obvious debugging**: Investigation took multiple attempts, the root cause wasn't what the error message suggested, or the fix required domain-specific knowledge not in docs
- **Misleading errors**: The error message pointed to the wrong location or cause, and the actual fix was elsewhere
- **Workaround discovery**: The standard approach didn't work, requiring experimentation to find an alternative
- **Configuration insight**: Setup differed from documented patterns, or undocumented options were required
- **Trial-and-error success**: Multiple approaches were tried before finding one that worked

When you recognize these signals, suggest capture:
```
This session produced a non-obvious discovery: [brief description].
This could be worth capturing to .docs/learnings/. Want me to document it?
```

### Explicit Invocation

When the user says `/learn`, "what did we learn", "capture learnings", or similar:
- Switch to Retrospective Mode (see below)
- Review the full session for learning candidates

## Self-Reflection Prompts

After completing a significant task, run these questions internally:

1. "What did I just learn that wasn't obvious before starting?"
2. "If I faced this exact problem again, what would I wish I knew?"
3. "What error message or symptom led me here, and what was the actual cause?"
4. "Is this pattern specific to this project, or would it help in similar projects?"
5. "What would I tell a colleague who hits this same issue?"

If any question produces a substantive answer, suggest extraction to the user.

## Capture Workflow

### Step 1: Dedup Check

Search existing learnings and skills BEFORE doing anything else.

```sh
# Search for existing learnings and skills
rg -i "keyword1|keyword2" .docs/learnings 2>/dev/null
rg -i "keyword1|keyword2" .claude/skills ~/.claude/skills 2>/dev/null
```

**Decision matrix:**

| What You Find | Action |
|---------------|--------|
| Nothing related | Proceed to Step 2 |
| Existing learning with same discovery | Reference it, add new context if any |
| Existing skill covers this | Note in learnings as "already captured" |
| Partial overlap with existing learning | Supplement the existing document |

See ./reference/extraction-workflow.md for the full dedup process.

### Step 2: Identify the Knowledge

Answer these four questions:

1. **What was the problem?** -- The symptom, not the fix. Include exact errors.
2. **What was non-obvious?** -- Why was this harder than expected?
3. **What would help next time?** -- The shortcut for future sessions.
4. **What are the trigger conditions?** -- When does this problem appear?

If answers are thin ("it was just a typo"), the discovery fails the worth assessment. See ./reference/quality-gates.md for the full criteria.

### Step 3: Gather Error Context

When a session is active (detected via session-map.json worktree match or `_current` fallback):

1. Read `.claude/sessions/{name}/errors.log` if it exists
2. For each error: extract tool name, input summary, and error summary
3. Correlate errors with discoveries — which errors led to which learnings?

When no session is active, skip this step.

### Step 4: Draft and Write

Spawn a `docs-writer` agent via the Task tool to create the learnings document:

```
Task prompt:
  doc_type: "learnings"
  topic: "Session Learnings: <session-name or YYYY-MM-DD>"
  tags: [learnings, <session-name if available>, <categories found>]
  references: [<files involved in learnings>]
  content: |
    # Session Learnings: <session-name or YYYY-MM-DD>

    ## Error Summary
    [From session errors.log — omit section if no session or no errors]
    - [error 1]: [context, what was tried, resolution]
    - [error 2]: [context, what was tried, resolution]

    ## Discoveries
    - **[finding 1]**: [context, why it matters, where it applies]
    - **[finding 2]**: [context, why it matters, where it applies]

    ## Debug References
    [From .docs/debug/ — omit section if no debug files found]
    - `.docs/debug/[filename]` — [key learning extracted]

    ## Deferred Actions
    - [ ] Consider creating skill for: [pattern]
    - [ ] Consider adding to CLAUDE.md: [rule]
    - [ ] Consider updating skill [name]: [what to add]
```

### Step 5: Quality Gates

Run every item before saving. See ./reference/quality-gates.md for the full checklist.

**Critical checks:**
- [ ] Each discovery was verified during this session
- [ ] Content is specific enough to be actionable
- [ ] No sensitive information (credentials, internal URLs, API keys)
- [ ] Doesn't duplicate existing learnings or skills
- [ ] Deferred Actions are concrete and actionable
- [ ] Error context is included when session errors exist

### Step 6: Present and Save

Show the complete draft to the user:

```
I've captured learnings from this session:

Discoveries: [count]
Deferred actions: [count]
Error context: [included/not available]

Save to: .docs/learnings/MM-DD-YYYY-session-learnings.md

Save these learnings?
```

After user approves, the docs-writer agent writes the file. Confirm:

```
Learnings captured: [topic]
Location: .docs/learnings/[filename]
Deferred actions: [count] items for future sessions to review
```

## Retrospective Mode

When explicitly invoked (`/learn` or "what did we learn"):

1. **Review**: Scan the session conversation for learning candidates. Look for debugging sequences, error resolutions, workarounds, corrections, and non-obvious discoveries.

2. **Gather context**: Read session errors.log and .docs/debug/ files if available.

3. **Identify**: List candidates with brief justifications:
   ```
   Session learning candidates:
   1. [Discovery] -- Worth capturing because [reason]
   2. [Discovery] -- Worth capturing because [reason]
   3. [Discovery] -- Not worth capturing: [why it fails the worth assessment]
   ```

4. **Prioritize**: Rank by reuse value. Prefer knowledge that applies across projects, saves significant time, and involves non-obvious solutions.

5. **Capture**: Process all worthy candidates into a single learnings document via the Capture Workflow (Steps 1-6). Consolidate into one `.docs/learnings/` file, not one per discovery.

6. **Summarize**:
   ```
   Session learning summary:
   - Captured: [count] discovery/discoveries
   - Deferred actions: [count] items
   - Location: .docs/learnings/[filename]
   - Skipped: [count] candidate(s)
     - [reason for each skip]
   ```

## Post-Session Mode

When invoked with a session name argument after the session has ended
(e.g., `/learning-from-sessions auth-mvp`):

1. **Locate session**: Look up session name in container-level `session-map.json`
2. **Read meta.json**: Get `claudeSessionIds` array from the session's state directory
   - Fall back to `sessionId` if `claudeSessionIds` is missing (old schema)
3. **Find transcripts**: For each UUID, locate transcript at:
   `~/.claude/projects/{path-encoded-worktree}/{uuid}.jsonl`
   Path encoding: replace path separators with `--`
   (e.g., `/c/code/project/feature/auth` -> `C--code-project-feature-auth`)
4. **Parse transcripts**: Stream JSONL, extract:
   - Tool failures (`is_error: true` in tool_result)
   - Debugging sequences (multiple tool attempts on same problem)
   - Error -> resolution pairs (error followed by successful fix)
   - Thinking blocks discussing root causes
5. **Correlate with errors.log**: Match transcript errors against errors.log entries
6. **Proceed to Capture Workflow** (Steps 1-6) with extracted candidates

**Transcript parsing guidance**: Reuse the JSONL streaming pattern from `harvest-errors.py` — stream line by line, filter by entry type, index tool_use blocks, and extract error sequences. See `.docs/research/02-08-2026-session-v2-1-deferred-actions-research.md` Section 4 for transcript format details.

## Output Routing

All learnings go to `.docs/learnings/` as deferred-action documents. The Deferred Actions checklist tells future sessions what to do with each learning:

**Deferred: Create skill** when:
- Reusable across projects
- Multi-step solution with clear trigger conditions
- Involves debugging, workarounds, or non-obvious fixes

**Deferred: Add to CLAUDE.md** when:
- Project-specific preference or convention
- Simple behavioral correction ("always use X not Y")
- Coding style rule for this project

**Deferred: Update existing skill** when:
- Discovery adds to an existing skill's knowledge
- New edge case or variant for a known pattern

**Not worth capturing** when:
- Simple typo or syntax error
- One-time issue that won't recur
- Knowledge already well-documented in official docs

## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- About to save without user confirmation
- Discovery wasn't verified during this session
- Immediately creating a skill instead of writing to .docs/learnings/
- Skipping session error context when errors.log exists
- Skipping the dedup check
- The discovery is a simple typo or syntax fix
- Content restates official documentation without adding non-obvious insight
- Deferred Actions are vague ("maybe create a skill")

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User will want this saved" | Ask. Never assume. Confirmation is mandatory. |
| "This should be a skill right now" | Defer it. Write to .docs/learnings/ with a deferred action. |
| "No need to dedup, this is definitely new" | Search anyway. You might find an existing learning to supplement. |
| "No errors.log, so skip error context" | Correct — but only skip if _current doesn't exist or errors.log is empty. |
| "I'll skip quality gates, the content is solid" | Run the checklist. Every item. Every time. |
| "Deferred actions can be vague" | Each action must name the specific skill, CLAUDE.md section, or pattern. |

## The Bottom Line

**No learnings without verification and user approval.**

Detect the signal. Gather session context. Dedup first. Analyze thoroughly. Write to .docs/learnings/. Validate rigorously. Confirm with the user. Then save.

This is non-negotiable. Every capture. Every time.
