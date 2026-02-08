---
name: auditing-docs
description: "Use this skill when auditing .docs/ documents for staleness, checking document health across the project, or reviewing which documents need updating or archiving. This includes scanning all .docs/ subdirectories for stale frontmatter, spawning docs-updater for each stale document, presenting audit dashboards with staleness metrics, and archiving obsolete documents. Trigger phrases: '/auditing-docs', 'audit docs', 'check document freshness', 'which docs are stale', 'review documents'."
---

# Auditing Docs

You are systematically auditing `.docs/` documents for staleness and freshness. This skill activates when checking document health or updating stale documents and produces audit dashboards or refreshed documents.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO UPDATE WITHOUT STALENESS ASSESSMENT FIRST
```

Every update must be preceded by a staleness assessment showing commits behind, reference status, and content summary. No blind updates.

**No exceptions:**
- Don't spawn docs-updater without assessing staleness first
- Don't update multiple documents simultaneously — one at a time
- Don't skip user confirmation in update mode
- Don't assume a document is stale — measure it

## The Gate Function

```
BEFORE updating any document:

1. IDENTIFY: Mode (audit vs update) and target (all, directory, or single file)
2. SCAN: Run staleness detection script on target
3. CHECK: For each stale doc, verify reference file existence
4. CATEGORIZE: CURRENT / STALE / OBSOLETE / UNKNOWN
5. REPORT: Present dashboard with metrics
6. If update mode: PROCESS stale docs one at a time with user confirmation
7. ONLY THEN: Move to next document

Skip assessment = blind updates
```

## Mode Detection

Parse the user's request to determine mode:

| Input | Mode | Target |
|-------|------|--------|
| `/auditing-docs audit` | Audit | All docs (dashboard only) |
| `/auditing-docs audit .docs/plans/` | Audit | Single directory |
| `/auditing-docs update` | Update | All stale docs, one-by-one |
| `/auditing-docs update .docs/plans/file.md` | Update | Single doc |
| `/auditing-docs` | Audit | All docs (default) |

## Mode A: Audit (Read-Only)

Produces a dashboard without making any changes.

### Process

1. Run the staleness detection script (full-scan variant from `./reference/staleness-detection.md`):

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

2. For each document found, also check reference file existence:
   - Read the document's `references:` frontmatter
   - Run `ls` on each referenced file
   - Count: X of Y references exist

3. Categorize each document (see `./reference/audit-checklist.md`):
   - **CURRENT**: 0-2 commits behind
   - **STALE**: 3+ commits behind, references exist
   - **OBSOLETE**: References deleted, or very old handoff (>30 days + >20 commits behind)
   - **UNKNOWN**: No git_commit frontmatter

4. Present the dashboard:

   ```
   DOCUMENT AUDIT
   ==============
   | Document | Commits Behind | References | Status |
   |----------|---------------|------------|--------|
   | .docs/plans/01-15-auth.md | 12 | 2/3 exist | STALE |
   | .docs/handoffs/01-20-session.md | 8 | 0/2 exist | OBSOLETE |
   | .docs/research/01-10-patterns.md | 3 | all exist | STALE |
   | .docs/learnings/01-05-tips.md | 1 | all exist | CURRENT |
   | .docs/debug/01-12-crash.md | — | — | UNKNOWN |

   Summary: X stale, Y obsolete, Z current, W unknown
   Run `/auditing-docs update` to process stale documents.
   ```

**If target is a single directory:** Only scan files in that directory.

**If no `.docs/` directory exists:**
```
No .docs/ directory found. Nothing to audit.
```

**If no stale docs found:**
```
DOCUMENT AUDIT
==============
All documents are current. No staleness detected.

Total: X documents checked, 0 stale.
```

## Mode B: Update (Interactive)

Processes stale and obsolete documents one at a time with user confirmation.

### Process

1. Run the full audit first (same as Mode A) — present the dashboard
2. Sort results by staleness (most commits behind first)
3. For each stale or obsolete document, one at a time:

   a. Show the assessment:
      ```
      DOCUMENT: .docs/plans/01-15-auth.md
      Status: STALE (12 commits behind)
      References: 2/3 exist (src/auth.ts deleted)
      Summary: [first 2-3 lines of content]

      Spawning docs-updater to assess and refresh...
      ```

   b. Spawn docs-updater agent via Task tool:
      ```
      prompt: "Check and update this document for staleness: .docs/plans/01-15-auth.md
               It is 12 commits behind HEAD.
               Assess whether to update or archive it."
      ```

   c. Show what docs-updater did:
      ```
      docs-updater result:
      - Decision: UPDATE
      - Changes: Updated file paths, refreshed code references
      - Now current at HEAD

      Proceed to next document? (yes/stop)
      ```

   d. If user says "stop": End the update cycle, show final dashboard
   e. If user says "yes": Move to next stale document

4. After all documents processed (or user stops), show final dashboard:
   ```
   UPDATE COMPLETE
   ===============
   Processed: 3 documents
   - Updated: 2
   - Archived: 1
   - Skipped: 0

   Remaining stale: X documents
   ```

**If target is a single file:** Skip the dashboard, go directly to assessment + docs-updater for that file.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Spawning docs-updater without showing the assessment first
- Processing multiple documents simultaneously
- Proceeding to next document without user confirmation in update mode
- Marking a document as CURRENT without running the staleness script
- Assuming reference existence without checking with `ls`
- Skipping the dashboard in audit mode

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This doc is obviously stale" | Run the script. Measure commits behind. Show evidence. |
| "I'll batch these updates together" | One at a time. Each needs assessment and confirmation. |
| "References probably still exist" | Check with ls. Existence is binary — verify it. |
| "User wants speed, skip the dashboard" | Dashboard is the whole point of audit mode. Always show it. |
| "docs-updater will figure it out" | Assessment first. docs-updater needs context about what's stale. |
| "No need to confirm, user said 'update all'" | Confirm each one. User may want to skip specific documents. |

## The Bottom Line

**No update without staleness assessment first.**

Scan all documents. Categorize by staleness. Present the dashboard. Process one at a time with confirmation.

This is non-negotiable. Every audit. Every time.
