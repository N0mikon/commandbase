---
date: 2026-02-07
status: in-progress
topic: "Phase 1 Foundations and Modifications Implementation"
tags: [plan, implementation, phase-1, naming-session, voice-tone, auditing-skills, auditing-agents, bookmarking-code, implementing-plans, handing-over, learning-from-sessions, hooks, track-errors, trigger-learning]
git_commit: 5beb0c1
last_updated: 2026-02-07
last_updated_by: docs-updater
last_updated_note: "Phases 1-8 complete (success criteria verified); phases 9-10 (hooks) remain. Updated from phases 1-5 note after 6/7/8 checkbox verification."
references:
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/research/02-07-2026-phase-1-foundations-skill-internals-research.md
  - .docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md
  - newskills/bookmarking-code/SKILL.md
  - newskills/implementing-plans/SKILL.md
  - newskills/handing-over/SKILL.md
  - newskills/learning-from-sessions/SKILL.md
  - newskills/auditing-skills/SKILL.md
  - newskills/auditing-agents/SKILL.md
---

# Phase 1: Foundations & Modifications — Implementation Plan

## Overview

Phase 1 of the future-skills roadmap creates the `/naming-session` primitive, a voice/tone reference, renames 2 skills, updates 4 skills for session awareness, and adds 2 new hooks for error tracking and learning triggers. This is the foundation that all later phases depend on.

10 phases across 3 implementation sessions. Estimated effort: Medium.

## Current State Analysis

**Session-scoped state:** Does not exist. No skill currently stores metadata that persists across skill invocations within a session. `/naming-session` will be the first session primitive.

**Native Claude session support:** Claude Code creates UUID v4 session IDs stored in `~/.claude/projects/{project}/sessions-index.json` with auto-generated `summary` fields. We will augment this with user-defined names and per-session folders.

**Checkpoint storage:** `.claude/checkpoints.log` is a flat file mixing all sessions. Format: `YYYY-MM-DD-HH:MM | checkpoint-name | git-sha`.

**Skills to modify:** All 4 target skills (bookmarking-code, handing-over, implementing-plans, learning-from-sessions) are synchronized between `newskills/` (source) and `~/.claude/skills/` (deployed).

**Skills to rename:** `updating-skills` and `updating-agents` exist only in `newskills/` (not deployed to `~/.claude/skills/`). Rename is source + deploy.

**Voice/tone guidance:** None exists. `~/.claude/references/` directory does not exist.

**Error tracking:** No hook currently tracks errors. Only one hook deployed: `nudge-commit-skill` (PostToolUse on Bash).

## Desired End State

After Phase 1:
- `/naming-session` creates per-session folders at `.claude/sessions/{name}/` with `meta.json`, `checkpoints.log`, and `errors.log`
- `.claude/sessions/_current` contains the active session name (read by all session-aware skills)
- If no session is named, all skills behave exactly as they do today (no fallback folder)
- `~/.claude/references/voice-tone-guide.md` provides tiered anti-AI-voice guidance
- `/auditing-skills` and `/auditing-agents` replace the old `updating-*` names
- `/bookmarking-code` writes to session folder when session exists
- `/handing-over` includes session name in handoff title and metadata
- `/implementing-plans` creates mandatory checkpoints (session-aware when available)
- `/learning-from-sessions` captures learnings to `.docs/learnings/` with deferred action
- `track-errors` hook logs tool failures to session error log
- `trigger-learning` hook nudges `/learning-from-sessions` on compaction/handover when errors exist

**Verification:** Each phase has specific success criteria. Final verification: invoke `/naming-session`, create a checkpoint, trigger an error, run `/handing-over`, and confirm all session-scoped files are populated correctly.

### Key Discoveries:
- Claude natively stores session IDs in `~/.claude/projects/{project}/sessions-index.json` with UUID, summary, timestamps, git branch (research agent finding)
- `sessions-index.json` is managed by Claude Code — we use a separate `.claude/sessions/` directory to avoid conflicts
- PostToolUseFailure hook event fires specifically on tool failures — ideal for error tracking without exit code parsing
- PreCompact hook event fires before `/compact` or automatic compaction — receives `trigger` field
- Hooks cannot directly invoke skills — they send stderr feedback (exit 2) that nudges Claude toward skill usage
- `/learning-from-sessions` is 298 lines with 4 reference files + 1 template (larger rework than initially estimated)
- `/handing-over` docs-writer call is at SKILL.md:62-72 with topic field at line 67
- `/implementing-plans` checkpoint section is at SKILL.md:166-178 — currently SUGGESTS checkpoints, not mandatory
- `CLAUDE.md:31` references `/updating-skills` — must update during rename
- `updating-skills` has 219 lines (not 235), sibling section is in `updating-agents:221-233`

## What We're NOT Doing

- NOT modifying `sessions-index.json` — separate `.claude/sessions/` directory avoids conflicts with Claude internals
- NOT creating a `_default/` session folder — unnamed sessions use current behavior unchanged
- NOT migrating old `.claude/checkpoints.log` entries — historical file stays as-is
- NOT updating historical `.docs/` files (handoffs, research, old plans) during renames — docs-updater decides per-file
- NOT making `/naming-session` mandatory — it's opt-in, everything is gated on `_current` file existence
- NOT building session resume/teleport features — that's future scope
- NOT adding voice/tone enforcement to skills yet — just creating the reference document

## Implementation Approach

Three implementation sessions with clear dependency boundaries:
- **Session 1** (Phases 1-4): Independent items — can be done in any order
- **Session 2** (Phases 5-8): Skill modifications that depend on Phase 1's session folder structure
- **Session 3** (Phases 9-10): New hooks that depend on the session folder structure

All skill changes follow: edit source in `newskills/` → deploy to `~/.claude/skills/` → verify.
All hook changes follow: create in `newhooks/` → deploy to `~/.claude/hooks/` → merge settings snippet → restart Claude Code → verify.

---

## Phase 1: Create `/naming-session` Skill

### Overview
Create a new skill that assigns a user-defined name to the current session, creates a per-session folder structure, and writes a `_current` pointer file.

### Changes Required:

#### 1. Create skill directory and SKILL.md
**File**: `newskills/naming-session/SKILL.md`
**Changes**: New file. Skill structure:

- **Iron Law**: `NO SESSION NAME WITHOUT USER CONFIRMATION`
- **Gate Function**: Read `sessions-index.json` to find current session UUID, auto-suggest name from session summary, user confirms or overrides
- **Workflow**:
  1. Read `~/.claude/projects/{encoded-cwd}/sessions-index.json`
  2. Find most recent entry by `modified` timestamp → get `sessionId`, `summary`, `gitBranch`
  3. Auto-suggest name: kebab-case slug from `summary` field (max 40 chars)
  4. Present suggestion to user, allow override
  5. Create `.claude/sessions/{name}/` directory
  6. Write `.claude/sessions/{name}/meta.json`:
     ```json
     {
       "sessionId": "<uuid>",
       "name": "<user-defined-name>",
       "created": "<ISO timestamp>",
       "gitBranch": "<branch>",
       "summary": "<native summary>"
     }
     ```
  7. Write `.claude/sessions/_current` with just the session name string
- **Validation**: Name must be kebab-case, 3-40 chars, no special chars beyond hyphens
- **Re-invocation**: If `_current` already exists, warn user and allow rename (update `_current`, create new folder, old folder stays)

#### 2. Deploy to global
**Command**: `cp -r newskills/naming-session ~/.claude/skills/`

### Success Criteria:
- [x] `newskills/naming-session/SKILL.md` created with proper frontmatter
- [x] Skill creates `.claude/sessions/{name}/` directory with `meta.json`
- [x] Skill writes `.claude/sessions/_current` with session name
- [x] `meta.json` contains correct sessionId from `sessions-index.json`
- [x] Skill deployed to `~/.claude/skills/naming-session/`
- [x] Re-invocation updates `_current` without destroying old session folder

---

## Phase 2: Create Voice/Tone Reference

### Overview
Create `~/.claude/references/voice-tone-guide.md` distilling the anti-AI voice research into actionable tiers. This is a reference document, not a skill.

### Changes Required:

#### 1. Create references directory
**Command**: `mkdir -p ~/.claude/references`

#### 2. Create voice-tone-guide.md
**File**: `~/.claude/references/voice-tone-guide.md`
**Changes**: New file. Distilled from `.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md`.

Structure:
- **Purpose**: Anti-AI-voice patterns for public-facing content (social posts, PRs, commit messages)
- **Tier 1 — Absolute Bans**: Words/phrases that instantly flag AI (delve, tapestry, leverage, "In the ever-evolving landscape", "It's important to note", etc.)
- **Tier 2 — Strong Avoidance**: High-correlation AI words to avoid in public content (robust, comprehensive, nuanced, furthermore, moreover, etc.)
- **Tier 3 — Contextual**: Words fine in moderation but suspicious when clustered (significant, notable, therefore)
- **Structural Rules**: Vary sentence length, use contractions, active voice, break parallel constructions, skip throat-clearing
- **Platform Norms**: Twitter/X (authenticity > polish, soft CTAs), LinkedIn (short paragraphs, hooks under 200 chars, personal stories), GitHub (imperative mood, explain why not what, conventional commits)
- **Quick Check**: 3 questions to ask before posting (Would you say this aloud? Specific example included? Jargon-free?)

#### 3. Source copy for commandbase repo
**File**: `newskills/naming-session/` is not the right place — this is a reference, not a skill.
**File**: Create a copy at a trackable location. Since `~/.claude/references/` is global config, track the source in this repo for history.
**Decision**: No source copy needed in commandbase — this is global config like agents. Track via git in `~/.claude/` if desired.

### Success Criteria:
- [x] `~/.claude/references/` directory created
- [x] `~/.claude/references/voice-tone-guide.md` created with tiered guidance
- [x] Tier 1 contains minimum 20 banned words/phrases with AI frequency data
- [x] Tier 2 contains minimum 30 strong-avoidance words categorized by type
- [x] Platform norms section covers Twitter/X, LinkedIn, and GitHub
- [x] Quick-check section is actionable (3 yes/no questions)

---

## Phase 3: Rename `/updating-skills` → `/auditing-skills`

### Overview
Rename the skill directory, update all internal references, update cross-references, and deploy.

### Changes Required:

#### 1. Rename source directory
**Command**: `mv newskills/updating-skills newskills/auditing-skills`

#### 2. Update SKILL.md frontmatter and content
**File**: `newskills/auditing-skills/SKILL.md` (219 lines)
**Changes**:
- Frontmatter `name:` field: `updating-skills` → `auditing-skills`
- Frontmatter `description:`: Update "updating skills" language to "auditing skills" language
- H1 title: `# Updating Skills` → `# Auditing Skills`
- All ~15 self-references: `updating-skills` → `auditing-skills`, `/updating-skills` → `/auditing-skills`
- Update description to emphasize auditing/validation over updating

#### 3. Update reference files
**Files**: `newskills/auditing-skills/reference/audit-checklist.md`, `newskills/auditing-skills/reference/common-fixes.md`
**Changes**: Replace any references to `updating-skills` with `auditing-skills`

#### 4. Update CLAUDE.md
**File**: `CLAUDE.md` (line 31)
**Changes**: `/updating-skills` → `/auditing-skills`

#### 5. Run docs-updater on cross-referencing files
**Files to check**:
- `.docs/future-skills/re-evaluate-existing.md` (4 refs — actively referenced, should update)
- `.docs/handoffs/02-02-2026-reviewing-changes-skill.md` (20+ refs — historical)
- `.docs/handoffs/02-05-2026-agent-audit-and-rename.md` (5+ refs — historical)
- `.docs/research/02-02-2026-reviewing-and-updating-skills-research.md` (15+ refs — historical)
- `.docs/plans/02-02-2026-updating-skills-skill.md` (30+ refs — historical)
- `.docs/research/skills/updating-skills.md` (10+ refs — historical)
- `.docs/plans/02-05-2026-opus-4-6-skill-hardening.md` (15+ refs — historical)
**Action**: Spawn docs-updater agent for each file. It decides whether to update, deprecate, or leave as-is based on document status.

#### 6. Deploy to global
**Command**: `cp -r newskills/auditing-skills ~/.claude/skills/`
**Cleanup**: `~/.claude/skills/updating-skills/` does not exist (confirmed by research), so no removal needed.

### Success Criteria:
- [x] `newskills/auditing-skills/` directory exists (old `updating-skills/` gone)
- [x] Zero references to "updating-skills" remain in `newskills/auditing-skills/`
- [x] `CLAUDE.md:31` references `/auditing-skills`
- [x] docs-updater ran on all cross-referencing `.docs/` files
- [x] Skill deployed to `~/.claude/skills/auditing-skills/`
- [x] `/auditing-skills` invocable in a test session

---

## Phase 4: Rename `/updating-agents` → `/auditing-agents`

### Overview
Same as Phase 3 but for the agents skill. Also updates the sibling cross-reference to point to `/auditing-skills`.

### Changes Required:

#### 1. Rename source directory
**Command**: `mv newskills/updating-agents newskills/auditing-agents`

#### 2. Update SKILL.md frontmatter and content
**File**: `newskills/auditing-agents/SKILL.md` (~266 lines)
**Changes**:
- Frontmatter `name:` field: `updating-agents` → `auditing-agents`
- Frontmatter `description:`: Update language to auditing
- H1 title: `# Updating Agents` → `# Auditing Agents`
- All ~10 self-references: `updating-agents` → `auditing-agents`
- **Sibling section (lines 221-233)**: Update header to `## Sibling Skill: /auditing-skills`, update table references from `/updating-skills` to `/auditing-skills` and `/updating-agents` to `/auditing-agents`

#### 3. Update reference files
**Files**: `newskills/auditing-agents/reference/audit-checklist.md`, `newskills/auditing-agents/reference/common-fixes.md`
**Changes**: Replace any references to `updating-agents` or `updating-skills` with `auditing-agents` or `auditing-skills`

#### 4. Run docs-updater on cross-referencing files
**Action**: Same approach as Phase 3 — docs-updater decides per-file.

#### 5. Deploy to global
**Command**: `cp -r newskills/auditing-agents ~/.claude/skills/`
**Cleanup**: `~/.claude/skills/updating-agents/` does not exist, so no removal needed.

### Success Criteria:
- [x] `newskills/auditing-agents/` directory exists (old `updating-agents/` gone)
- [x] Zero references to "updating-agents" or "updating-skills" remain in `newskills/auditing-agents/`
- [x] Sibling section correctly references `/auditing-skills`
- [x] docs-updater ran on cross-referencing `.docs/` files
- [x] Skill deployed to `~/.claude/skills/auditing-agents/`

---

## Phase 5: Update `/bookmarking-code` for Session Names

### Overview
Add session awareness to checkpoints. When a session is named, write checkpoints to the session folder. When no session exists, behave exactly as today.

### Changes Required:

#### 1. Add session detection logic
**File**: `newskills/bookmarking-code/SKILL.md` (244 lines)
**Changes**: Add a new section after the Iron Law (before the workflow):

```markdown
## Session Awareness

Before creating or verifying checkpoints, check for an active session:

1. Check if `.claude/sessions/_current` exists
2. If YES: Read session name, use `.claude/sessions/{name}/checkpoints.log`
3. If NO: Use `.claude/checkpoints.log` (default behavior)

When session-scoped:
- Checkpoint names are automatically prefixed: `{session-name}:{checkpoint-name}`
- The prefix is for display/search only — storage uses the session folder for isolation
- Verification commands search the session-scoped log first
```

#### 2. Update checkpoint create workflow
**File**: `newskills/bookmarking-code/SKILL.md`
**Changes**: In the create workflow section, add session folder logic:
- If session exists: write to `.claude/sessions/{name}/checkpoints.log`
- If no session: write to `.claude/checkpoints.log` (unchanged)

#### 3. Update checkpoint verify workflow
**File**: `newskills/bookmarking-code/SKILL.md`
**Changes**: In the verify workflow:
- If session exists: search session-scoped log first, fall back to global
- If no session: search `.claude/checkpoints.log` (unchanged)

#### 4. Update Naming Conventions section (SKILL.md:196-202)
**Changes**: Add session-prefixed examples:
- `auth-mvp:phase-2-done` (session-scoped)
- `auth-mvp:pre-refactor` (session-scoped)

#### 5. Update Workflow Integration section (SKILL.md:221-237)
**Changes**: Add note about session-aware checkpoints in the RPI workflow diagram.

#### 6. Deploy
**Commands**: `cp newskills/bookmarking-code/SKILL.md ~/.claude/skills/bookmarking-code/SKILL.md`

### Success Criteria:
- [x] Session detection logic reads `.claude/sessions/_current`
- [x] With active session: checkpoints written to `.claude/sessions/{name}/checkpoints.log`
- [x] Without active session: checkpoints written to `.claude/checkpoints.log` (unchanged)
- [x] Verify command searches session log first, falls back to global
- [x] Naming conventions section includes session-prefixed examples
- [x] Deployed to `~/.claude/skills/bookmarking-code/`

---

## Phase 6: Update `/handing-over` for Session Names

### Overview
Include session name in handoff document title and metadata when a session is named.

### Changes Required:

#### 1. Add session detection
**File**: `newskills/handing-over/SKILL.md` (210 lines)
**Changes**: Add section before Step 1:

```markdown
## Session Awareness

Before creating the handover document, check for an active session:

1. Check if `.claude/sessions/_current` exists
2. If YES: Read session name, include in handoff metadata and title
3. If NO: Proceed without session context (default behavior)
```

#### 2. Update docs-writer call (SKILL.md:62-72)
**Changes**: Add `session` field to docs-writer invocation when session exists:

```
Task prompt:
  doc_type: "handoff"
  topic: "<session-name> - <brief description of work>"  # session prefix when available
  tags: [<relevant component names>]
  references: [<key files worked on>]
  content: |
    <compiled handover with session context section>
```

#### 3. Add session context to handover body
**Changes**: When session exists, add a "Session Context" section to the handover body:
- Session name
- Session-scoped checkpoints (list from `.claude/sessions/{name}/checkpoints.log`)
- Session errors (count from `.claude/sessions/{name}/errors.log`)
- Link to session meta.json for UUID/teleport reference

#### 4. Deploy
**Command**: `cp newskills/handing-over/SKILL.md ~/.claude/skills/handing-over/SKILL.md`

### Success Criteria:
- [x] Session detection reads `.claude/sessions/_current`
- [x] With active session: handoff title includes session name prefix
- [x] With active session: handoff body includes Session Context section
- [x] Without active session: behaves identically to current version
- [x] Deployed to `~/.claude/skills/handing-over/`

---

## Phase 7: Update `/implementing-plans` for Mandatory Checkpoints

### Overview
Make checkpoint creation mandatory (not just suggested) after phase completion, session-aware when available. Add docs-updater trigger for stale plan detection.

### Changes Required:

#### 1. Update Checkpoint Integration section (SKILL.md:166-178)
**File**: `newskills/implementing-plans/SKILL.md` (200 lines)
**Changes**: Replace the suggestion with a mandatory step:

```markdown
### Checkpoint Integration

After completing each phase with verified evidence, create a checkpoint:

1. Check if `.claude/sessions/_current` exists
2. If session exists: `/bookmarking-code create "phase-N-done"` (writes to session folder)
3. If no session: `/bookmarking-code create "phase-N-done"` (writes to global log)

This is NOT optional. Every verified phase gets a checkpoint before proceeding.
```

#### 2. Update phase completion flow
**File**: `newskills/implementing-plans/SKILL.md`
**Changes**: In the phase completion flow (around lines 100-130 area), add checkpoint creation as a required step after verification passes, not a suggestion.

#### 3. Add docs-updater integration
**File**: `newskills/implementing-plans/SKILL.md`
**Changes**: Add new section:

```markdown
### Documentation Freshness

At the start of implementation and after completing the final phase:

1. Identify `.docs/` files referenced in the plan
2. Spawn docs-updater agent for each to check staleness
3. Report any stale documents to user before proceeding

This catches plans referencing outdated research or handoffs.
```

#### 4. Deploy
**Command**: `cp newskills/implementing-plans/SKILL.md ~/.claude/skills/implementing-plans/SKILL.md`

### Success Criteria:
- [x] Checkpoint creation is mandatory language ("This is NOT optional")
- [x] Checkpoint is session-aware (checks `_current`, writes to session folder if available)
- [x] Phase completion flow includes checkpoint as required step (not suggestion)
- [x] docs-updater integration section exists
- [x] Deployed to `~/.claude/skills/implementing-plans/`

---

## Phase 8: Rework `/learning-from-sessions`

### Overview
Transform from "immediate skill creator" to "automatic learning capture with deferred action." Output goes to `.docs/learnings/` instead of immediately creating skills or CLAUDE.md entries.

### Changes Required:

#### 1. Rewrite core workflow
**File**: `newskills/learning-from-sessions/SKILL.md` (298 lines)
**Changes**: Major rework of the workflow section:

**Old flow**: Review → Identify → Categorize → Immediately create skill/CLAUDE.md entry → Present
**New flow**: Review → Identify → Categorize → Write to `.docs/learnings/` via docs-writer → Present summary → Defer action to future session

#### 2. Add session awareness
**Changes**: Add session detection at the start:
- Read `.claude/sessions/_current` if it exists
- Include session name in learnings metadata
- Read `.claude/sessions/{name}/errors.log` if it exists (pull error context)

#### 3. Add `.docs/debug/` integration
**Changes**: Add step to scan `.docs/debug/` for recent debug files:
- If debug files exist from current session timeframe, incorporate findings
- Don't duplicate — reference the debug file, extract the key learning

#### 4. Update output format
**Changes**: Replace skill/CLAUDE.md creation with docs-writer call:

```
Task prompt:
  doc_type: "research"  # learnings are a form of research
  topic: "Session Learnings: <session-name or date>"
  tags: [learnings, <categories found>]
  references: [<files involved in learnings>]
  content: |
    # Session Learnings: <session-name or date>

    ## Error Summary (from session errors.log)
    - [error 1]: [context, what was tried, resolution]

    ## Discoveries
    - [finding]: [context, why it matters, where it applies]

    ## Deferred Actions
    - [ ] Consider creating skill for: [pattern]
    - [ ] Consider adding to CLAUDE.md: [rule]
    - [ ] Consider updating skill [name]: [what to add]
```

#### 5. Update reference files
**Files**: `reference/extraction-workflow.md`, `reference/output-formats.md`
**Changes**: Update to reflect deferred-action model and `.docs/learnings/` output

#### 6. Update template
**File**: `templates/extracted-skill-template.md`
**Changes**: Replace or supplement with a learnings document template

#### 7. Update description
**Changes**: Update frontmatter description to reflect the new behavior:
- Remove: "saving non-obvious discoveries or workarounds as skill files"
- Add: "capturing session learnings to .docs/learnings/ for deferred action"

#### 8. Deploy
**Command**: `cp -r newskills/learning-from-sessions ~/.claude/skills/`

### Success Criteria:
- [x] Workflow creates `.docs/learnings/` documents instead of immediate skill/CLAUDE.md entries
- [x] Session awareness reads `_current` and `errors.log` when available
- [x] `.docs/debug/` files are referenced (not duplicated) when relevant
- [x] Output includes "Deferred Actions" checklist
- [x] Reference files updated to reflect new model
- [x] Template updated for learnings format
- [x] Description updated in frontmatter
- [x] Without active session: still works (uses date instead of session name, skips error log)
- [x] Deployed to `~/.claude/skills/learning-from-sessions/`

---

## Phase 9: Create `track-errors` Hook

### Overview
PostToolUseFailure hook that logs tool failures to the active session's error log.

### Changes Required:

#### 1. Create hook script
**File**: `newhooks/track-errors/track-errors.py`
**Changes**: New Python script:

```python
#!/usr/bin/env python3
"""PostToolUseFailure hook: logs errors to session error log."""
import json
import sys
import os
from datetime import datetime, timezone

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check for active session
    cwd = input_data.get("cwd", ".")
    current_file = os.path.join(cwd, ".claude", "sessions", "_current")

    if not os.path.exists(current_file):
        sys.exit(0)  # No session, no tracking

    try:
        with open(current_file, "r") as f:
            session_name = f.read().strip()
    except (IOError, OSError):
        sys.exit(0)

    if not session_name:
        sys.exit(0)

    # Build log entry
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": input_data.get("session_id", ""),
        "tool": input_data.get("tool_name", "unknown"),
        "input": _summarize_input(input_data.get("tool_input", {})),
        "error": _summarize_response(input_data.get("tool_response", ""))
    }

    # Append to session error log
    session_dir = os.path.join(cwd, ".claude", "sessions", session_name)
    os.makedirs(session_dir, exist_ok=True)
    log_path = os.path.join(session_dir, "errors.log")

    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except (IOError, OSError):
        sys.exit(1)  # Non-blocking error

    sys.exit(0)

def _summarize_input(tool_input):
    """Extract the most relevant part of tool input for logging."""
    if isinstance(tool_input, dict):
        return tool_input.get("command", tool_input.get("pattern", str(tool_input)[:200]))
    return str(tool_input)[:200]

def _summarize_response(response):
    """Truncate response for log storage."""
    return str(response)[:500]

if __name__ == "__main__":
    main()
```

#### 2. Create settings snippet
**File**: `newhooks/track-errors/settings-snippet.json`
**Changes**: New file:

```json
{
  "hooks": {
    "PostToolUseFailure": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ~/.claude/hooks/track-errors.py'"
          }
        ]
      }
    ]
  }
}
```

#### 3. Deploy
**Commands**:
- Copy script: `cp newhooks/track-errors/track-errors.py ~/.claude/hooks/`
- Merge settings snippet into `~/.claude/settings.json`

### Success Criteria:
- [ ] `newhooks/track-errors/track-errors.py` created and functional
- [ ] `newhooks/track-errors/settings-snippet.json` created
- [ ] Hook silently exits when no session is active (exit 0)
- [ ] Hook appends JSON entries to `.claude/sessions/{name}/errors.log` on tool failure
- [ ] Log entries contain timestamp, tool, input summary, and error summary
- [ ] Deployed to `~/.claude/hooks/track-errors.py`
- [ ] Settings merged into `~/.claude/settings.json`
- [ ] Hook verified in live session (trigger a deliberate bash failure, check log)

---

## Phase 10: Create `trigger-learning` Hook

### Overview
PreCompact hook that nudges `/learning-from-sessions` when context compaction occurs and the session has recorded errors. Also add a reminder to `/handing-over` for the same trigger.

### Changes Required:

#### 1. Create hook script
**File**: `newhooks/trigger-learning/trigger-learning.py`
**Changes**: New Python script:

```python
#!/usr/bin/env python3
"""PreCompact hook: nudges /learning-from-sessions when errors exist."""
import json
import sys
import os

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check for active session
    cwd = input_data.get("cwd", ".")
    current_file = os.path.join(cwd, ".claude", "sessions", "_current")

    if not os.path.exists(current_file):
        sys.exit(0)  # No session, no nudge

    try:
        with open(current_file, "r") as f:
            session_name = f.read().strip()
    except (IOError, OSError):
        sys.exit(0)

    if not session_name:
        sys.exit(0)

    # Check if errors exist
    errors_path = os.path.join(cwd, ".claude", "sessions", session_name, "errors.log")

    if not os.path.exists(errors_path):
        sys.exit(0)  # No errors, no nudge

    try:
        with open(errors_path, "r") as f:
            error_count = sum(1 for line in f if line.strip())
    except (IOError, OSError):
        sys.exit(0)

    if error_count == 0:
        sys.exit(0)

    # Nudge Claude toward /learning-from-sessions
    print(
        f"SESSION LEARNING REMINDER: This session ({session_name}) has "
        f"{error_count} error(s) logged in .claude/sessions/{session_name}/errors.log. "
        f"Before compacting/ending, consider running /learning-from-sessions "
        f"to capture what was learned from these errors.",
        file=sys.stderr,
    )
    sys.exit(2)  # Exit 2 sends stderr to Claude as feedback

if __name__ == "__main__":
    main()
```

#### 2. Create settings snippet
**File**: `newhooks/trigger-learning/settings-snippet.json`
**Changes**: New file:

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ~/.claude/hooks/trigger-learning.py'"
          }
        ]
      }
    ]
  }
}
```

#### 3. Add reminder to `/handing-over`
**File**: `newskills/handing-over/SKILL.md`
**Changes**: Add to the end of the handover workflow (after creating handoff doc):

```markdown
### Learning Check

After creating the handover document, check for session errors:

1. If `.claude/sessions/_current` exists AND `.claude/sessions/{name}/errors.log` has entries:
   - Remind user: "This session had N error(s). Consider running /learning-from-sessions before ending."
2. If no session or no errors: skip this step
```

#### 4. Deploy
**Commands**:
- Copy script: `cp newhooks/trigger-learning/trigger-learning.py ~/.claude/hooks/`
- Merge settings snippet into `~/.claude/settings.json`
- Redeploy handing-over: `cp newskills/handing-over/SKILL.md ~/.claude/skills/handing-over/SKILL.md`

### Success Criteria:
- [ ] `newhooks/trigger-learning/trigger-learning.py` created and functional
- [ ] `newhooks/trigger-learning/settings-snippet.json` created
- [ ] Hook silently exits when no session or no errors (exit 0)
- [ ] Hook sends stderr nudge when errors exist (exit 2)
- [ ] Nudge message includes error count and skill invocation suggestion
- [ ] `/handing-over` includes Learning Check section
- [ ] Deployed to `~/.claude/hooks/trigger-learning.py`
- [ ] Settings merged into `~/.claude/settings.json`
- [ ] Verified: trigger compaction with errors logged → nudge appears

---

## Testing Strategy

### Per-Phase Verification:
Each phase has inline success criteria checked during implementation.

### End-to-End Integration Test (after all phases):
1. Start a new session
2. Run `/naming-session` → name it "integration-test"
3. Verify `.claude/sessions/integration-test/` exists with `meta.json`
4. Verify `.claude/sessions/_current` contains "integration-test"
5. Run `/bookmarking-code create "test-checkpoint"` → verify writes to session folder
6. Trigger a deliberate bash failure → verify `track-errors` hook writes to `errors.log`
7. Run `/implementing-plans` on a small plan → verify mandatory checkpoint created in session folder
8. Run `/handing-over` → verify handoff includes session name and Learning Check reminder
9. Trigger compaction → verify `trigger-learning` hook sends nudge
10. Run `/learning-from-sessions` → verify `.docs/learnings/` document created with error context

### Regression Check:
- Without `/naming-session`: verify all skills behave exactly as before (no session folder, global checkpoints.log)

## Migration Notes

- **Old `.claude/checkpoints.log`**: Stays as-is. Not migrated. New session-scoped checkpoints go to session folders.
- **Old handoff format**: Unchanged when no session is active. New format only activates with session.
- **Hook deployment**: Requires Claude Code restart after settings.json merge. Plan for restart between Session 2 and Session 3.
- **Skill descriptions in system prompts**: After renaming, the old `/updating-skills` and `/updating-agents` trigger phrases will stop matching. Users must use `/auditing-skills` and `/auditing-agents`.

## References

- Master roadmap: `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md`
- Skill internals research: `.docs/research/02-07-2026-phase-1-foundations-skill-internals-research.md`
- Anti-AI voice research: `.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md`
- Hook specification: `newskills/creating-hooks/SKILL.md`
- docs-writer agent: `~/.claude/agents/docs-writer.md`
- Native session storage: `~/.claude/projects/{project}/sessions-index.json`
