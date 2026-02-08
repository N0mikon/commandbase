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
  # Convert MINGW path to Windows path for python3 compatibility
  WIN_META_FILE="$(cygpath -w "$META_FILE" 2>/dev/null || echo "$META_FILE")"
  echo "Branch:  $(python3 -c "import json; print(json.load(open(r'$WIN_META_FILE'))['gitBranch'])")"
  echo "Created: $(python3 -c "import json; print(json.load(open(r'$WIN_META_FILE'))['created'])")"
  echo "Summary: $(python3 -c "import json; print(json.load(open(r'$WIN_META_FILE'))['summary'])")"
fi

exit 0
