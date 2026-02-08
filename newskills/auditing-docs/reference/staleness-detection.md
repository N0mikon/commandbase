# Staleness Detection Scripts

Reusable bash scripts for detecting stale `.docs/` files via `git_commit` frontmatter comparison.

## Full-Scan Variant

Scans all `.docs/*.md` files and reports staleness sorted by commits behind.

Used by: `/auditing-docs` audit mode, `/committing-changes` Step 2.

```bash
find .docs -name "*.md" -type f 2>/dev/null | while read -r f; do
  git ls-files --error-unmatch "$f" >/dev/null 2>&1 || continue
  commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
  [ -z "$commit" ] || [ "$commit" = "n/a" ] && continue
  if git rev-parse "$commit" >/dev/null 2>&1; then
    behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
    [ -n "$behind" ] && [ "$behind" -gt 0 ] && echo "$behind commits behind: $f"
  fi
done | sort -rn
```

**How it works:**
1. `find .docs -name "*.md"` — discover all markdown files under `.docs/`
2. `git ls-files --error-unmatch` — skip untracked files (new docs not yet committed)
3. `head -10 | grep "^git_commit:"` — extract commit hash from frontmatter (first 10 lines)
4. Skip files without a commit hash or with `n/a`
5. `git rev-parse` — verify the commit hash is valid
6. `git rev-list "$commit"..HEAD --count` — count commits between doc's snapshot and current HEAD
7. Report files that are behind, sorted by staleness (most behind first)

## Single-File Variant

Checks ONE specific file path and returns the number of commits behind. Used by upstream-reading skills that need to check a document before reading it.

```bash
f="<path-to-doc>"
commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
  git rev-parse "$commit" >/dev/null 2>&1 && \
  behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
  [ -n "$behind" ] && [ "$behind" -gt 0 ] && echo "$behind"
fi
```

**Returns:** The number of commits behind (e.g., `7`), or nothing if the file is current or has no `git_commit` frontmatter.

**Threshold guidance:**
- `/committing-changes` uses >5 commits (lenient — commit-time gate)
- `/auditing-docs` uses >2 commits for STALE category (methodical audit)
- Upstream-reading skills use >3 commits (tighter — decisions depend on content)

## docs-updater Spawn Pattern

How to invoke the docs-updater agent via Task tool to refresh a stale document:

```
Spawn a Task agent with subagent_type "docs-updater":

  prompt: "Check and update this document for staleness: <path-to-doc>
           It is <N> commits behind HEAD.
           Assess whether to update or archive it."
```

The docs-updater agent will:
1. Read the document and its frontmatter
2. Check if referenced files still exist
3. Run `git diff --name-only <git_commit>..HEAD` to see what changed
4. Decide: UPDATE (content still relevant) or ARCHIVE (obsolete/superseded)
5. Execute the decision and report results

**After docs-updater completes:**
- If it updated the doc: re-read the refreshed version
- If it archived the doc: handle gracefully (warn user or omit from context)
