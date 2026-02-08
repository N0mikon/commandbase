---
date: 2026-02-07
status: complete
topic: "Session Status Script Integration Test"
tags: [plan, implementation, scripts, integration-test]
git_commit: ae98216
last_updated: 2026-02-08
last_updated_by: docs-updater
references:
  - CLAUDE.md
  - .claude/sessions/_current
---

# Session Status Script — Integration Test Plan

## Overview

Add a minimal `scripts/session-status.sh` utility that reads `.claude/sessions/_current` and prints session info. This plan exists to exercise the `/implementing-plans` workflow end-to-end during integration testing.

## Current State Analysis

- The project has no `scripts/` directory
- `.claude/sessions/_current` contains the active session name (plain text)
- `.claude/sessions/{name}/meta.json` contains session metadata (JSON)
- `CLAUDE.md` documents the directory structure but does not include `scripts/`

## Desired End State

A working `scripts/session-status.sh` that:
1. Reads the current session name from `.claude/sessions/_current`
2. Reads metadata from `.claude/sessions/{name}/meta.json`
3. Prints a formatted status summary
4. Exits cleanly with appropriate codes (0 = session active, 1 = no session)

Verification: `bash scripts/session-status.sh` prints the active session info.

## What We're NOT Doing

- Not adding session management logic (start/stop/rename)
- Not integrating with other skills
- Not adding tests — this is a trivial utility for integration testing
- Not deploying to global config

## Implementation Approach

Two phases: create the script, then update CLAUDE.md to reference it.

## Phase 1: Create Session Status Script

### Overview
Create the `scripts/` directory and write `session-status.sh`.

### Changes Required:

#### 1. Create `scripts/session-status.sh`
**File**: `scripts/session-status.sh`
**Changes**: New file

```bash
#!/usr/bin/env bash
# session-status.sh — Print active Claude Code session info
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CURRENT_FILE="$PROJECT_ROOT/.claude/sessions/_current"

if [[ ! -f "$CURRENT_FILE" ]]; then
  echo "No active session."
  exit 1
fi

SESSION_NAME=$(cat "$CURRENT_FILE")
META_FILE="$PROJECT_ROOT/.claude/sessions/$SESSION_NAME/meta.json"

echo "Session: $SESSION_NAME"

if [[ -f "$META_FILE" ]]; then
  echo "Branch:  $(python3 -c "import json; print(json.load(open('$META_FILE'))['gitBranch'])")"
  echo "Created: $(python3 -c "import json; print(json.load(open('$META_FILE'))['created'])")"
  echo "Summary: $(python3 -c "import json; print(json.load(open('$META_FILE'))['summary'])")"
fi

exit 0
```

### Success Criteria:
- [x] `scripts/` directory exists
- [x] `scripts/session-status.sh` exists and is executable
- [x] Running `bash scripts/session-status.sh` prints session name "integration-test"
- [x] Running `bash scripts/session-status.sh` prints branch, created, and summary fields

---

## Phase 2: Update CLAUDE.md Directory Reference

### Overview
Add `scripts/` to the directory structure documentation in CLAUDE.md.

### Changes Required:

#### 1. Update `CLAUDE.md`
**File**: `CLAUDE.md`
**Changes**: Add `scripts/` entry to the directory structure block

The directory structure in CLAUDE.md currently shows:
```
commandbase/
├── newskills/
├── newagents/
├── newhooks/
└── .docs/
```

Update to:
```
commandbase/
├── newskills/
├── newagents/
├── newhooks/
├── scripts/
└── .docs/
```

### Success Criteria:
- [x] CLAUDE.md directory structure includes `scripts/` with description
- [x] No other CLAUDE.md content modified

---

## References

- `.claude/sessions/_current` — session pointer file
- `.claude/sessions/{name}/meta.json` — session metadata format
- `CLAUDE.md` — project directory structure documentation
